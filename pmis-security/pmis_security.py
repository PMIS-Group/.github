#!/usr/bin/env python3
"""PMIS Security: read-only, dependency-free GitHub repository audit.
It never executes project code, database migrations, package hooks, or deploy scripts.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path.cwd(); SKIP={'.git','node_modules','vendor','.next','target','build','dist','coverage','.venv','venv'}
TEXT={'.java','.kt','.ts','.tsx','.js','.jsx','.mjs','.cjs','.py','.php','.rb','.go','.cs','.sql','.yml','.yaml','.json','.xml','.properties','.env','.md','.txt','.sh','.ps1','.toml'}
WEIGHT={'critical':30,'high':15,'medium':6,'low':2}; ICON={'critical':'🔴','high':'🟠','medium':'🟡','low':'🔵'}

@dataclass
class Finding:
    rule:str; priority:str; title:str; area:str; path:str; line:int; excerpt:str; description:str; why:str; fix:str; confidence:str='confirmed'; author:str='not determined'; introduced:str='not determined'; fingerprint:str=''
    def finish(self):
        self.fingerprint=hashlib.sha256(f'{self.rule}|{self.path}|{self.line}|{self.title}'.encode()).hexdigest()[:12]; return self

def sh(*a):
    try:return subprocess.check_output(a,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return ''
def files():
    listed=sh('git','ls-files').splitlines() or [str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file()]
    out=[]
    for name in listed:
        p=ROOT/name
        if p.is_file() and p.stat().st_size<1_000_000 and not any(x in SKIP for x in p.parts) and (p.suffix.lower() in TEXT or p.name in {'Dockerfile','Makefile','.env.example'}):out.append(p)
    return out
def read(p):
    try:return p.read_text(encoding='utf-8',errors='replace')
    except Exception:return ''
def line_of(c,m):return c[:m.start()].count('\n')+1
def snippet(lines,n,redact=False):
    s='\n'.join(lines[max(0,n-1):n+2])
    if redact:
        s=re.sub(r'([:=]\s*["\'])[^"\']+(["\'])',r'\1[REDACTED]\2',s)
        s=re.sub(r'(-----BEGIN [^-]+-----).*?(-----END [^-]+-----)',r'\1\n[REDACTED]\n\2',s,flags=re.S)
    return s.strip()
def blame(path,n):
    b=sh('git','blame','-L',f'{n},{n}','--porcelain','--',path); a=re.search(r'^author (.+)$',b,re.M); c=re.match(r'^([0-9a-f]{40})',b)
    return (a.group(1) if a else 'not determined',c.group(1)[:8] if c else 'not determined')
def add(out,**kw):
    f=Finding(**kw).finish()
    if not any(x.fingerprint==f.fingerprint for x in out):out.append(f)
def find(out,rule,priority,title,area,p,content,match,desc,why,fix,redact=False,confidence='confirmed'):
    n=line_of(content,match); rel=str(p.relative_to(ROOT)); a,c=blame(rel,n)
    add(out,rule=rule,priority=priority,title=title,area=area,path=rel,line=n,excerpt=snippet(content.splitlines(),n,redact),description=desc,why=why,fix=fix,confidence=confidence,author=a,introduced=c)

def scan(fs,out,base):
    for p in fs:
        c=read(p); rel=str(p.relative_to(ROOT)); low=rel.lower()
        # Sensitive data scanner
        for title,rx,priority in [
          ('Private key committed',r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----','critical'),
          ('GitHub token committed',r'\bgh[pousr]_[A-Za-z0-9_]{20,}\b','critical'),
          ('AWS access key committed',r'\bAKIA[0-9A-Z]{16}\b','critical'),
          ('Hardcoded credential-like value',r'(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*["\'][^"\']{8,}["\']','high')]:
            m=re.search(rx,c)
            is_test = bool(re.search(r'(^|/)(?:test|tests|__tests__)/|\.(?:test|spec)\.[^/]+$', rel, re.I))
            safe_reference = ('${{ secrets.' in c or re.search(r'\$[A-Za-z_]', (m.group(0) if m else '')) or is_test or 'Sanitizer' in p.name or p.name == '.env.example')
            if m and not safe_reference:find(out,'sensitive-data',priority,title,'Sensitive data scanner',p,c,m,'A value resembling a credential is tracked in source.','Secrets in Git history can be copied, reused or exposed.','Remove it, rotate the real credential, and use deployment/GitHub secrets.',True)
        # Database migration guard
        if p.suffix=='.sql' and '/backups/' not in '/'+rel and re.search(r'(migration|migrations|flyway|liquibase)',low):
            for title,rx,priority,desc,why,fix in [
              ('Random data mutation in migration',r'(?i)\b(random\s*\(|rand\s*\()','critical','A migration generates random values while changing data.','Migrations must be deterministic and recoverable.','Remove random mutation; use explicit reviewed values or a test-data seed.'),
              ('Destructive database operation',r'(?i)\b(drop\s+(?:table|schema|database)|truncate\s+table|delete\s+from)\b','high','A migration contains a destructive operation.','Production data or schema can be removed.','Require an explicit safe scope and document data impact.'),
              ('Unbounded database update',r'(?im)^\s*update\s+[\w."`]+\s*(?:set|\n)','high','A migration updates table data.','Without a restrictive WHERE clause it can change every row.','Add a restrictive WHERE clause or explain and test the full-table rewrite.')]:
                m=re.search(rx,c)
                if m:find(out,'migration-guard',priority,title,'Database migration guard',p,c,m,desc,why,fix,confidence='needs verification' if title=='Unbounded database update' else 'confirmed')
        # Demo detector only runtime
        if re.search(r'(?i)(src|app|lib|features|controllers)',rel) and not re.search(r'(?i)(test|spec|story|example)',rel):
            m=re.search(r'\b(?:mock|fixture|fake|dummy|sample|demo)[A-Z_][A-Za-z0-9_]*\b',c)
            if m:find(out,'demo-data','medium','Demo or mock marker in runtime code','Demo-data detector',p,c,m,'Runtime source contains a demo/mock marker.','A screen can appear complete while using non-shared or non-persistent data.','Confirm intent; connect real API/storage or isolate it behind a development-only adapter.',confidence='needs verification')
        # cleanup
        m=re.search(r'(?i)\b(TODO|FIXME|HACK|XXX)\b',c)
        if m:find(out,'temporary-code','low','Unresolved TODO/FIXME/HACK marker','Dead / temporary code check',p,c,m,'Source declares unfinished or workaround behavior.','Temporary behavior can silently become production behavior.','Create a tracked issue with owner/date or remove obsolete code.',confidence='needs verification')
        # CI / deployment guard
        if '.github/workflows/' in rel:
            m=re.search(r'(?i)(-DskipTests|--skip-tests|test:\s*false|skip\s+tests)',c)
            if m:find(out,'ci-deployment','high','Tests explicitly skipped in workflow','CI / deployment guard',p,c,m,'The workflow explicitly skips tests.','A green build can represent untested code.','Remove the skip or make a separate clearly labelled build-only job.')
            m=re.search(r'(?i)(deploy|production|release)',c)
            if m:find(out,'ci-deployment','medium','Deployment-related workflow needs CI dependency review','CI / deployment guard',p,c,m,'A deployment workflow was detected.','Branch-triggered deploys can bypass an immutable successful quality run.','Confirm deployment requires a successful CI result or protected release tag.',confidence='needs verification')
    # dependency readiness
    names={p.name for p in fs}; manifests={'package.json','pom.xml','composer.json','requirements.txt','pyproject.toml','go.mod'}
    locks={'package-lock.json','pnpm-lock.yaml','yarn.lock','composer.lock','poetry.lock','go.sum'}
    if names & manifests and not names & locks:
        add(out,rule='dependency-lock',priority='medium',title='Dependency manifest has no lockfile',area='Dependency vulnerability scan',path=next(iter(names&manifests)),line=1,excerpt='Manifest is tracked but no supported lockfile was found.',description='Dependencies are not pinned by a lockfile.',why='Builds may resolve different versions over time.',fix='Generate and commit the lockfile used by CI.')
    if not any('.github/workflows/' in str(p.relative_to(ROOT)) for p in fs):
        add(out,rule='ci-guard',priority='high',title='No GitHub Actions workflow found',area='CI / deployment guard',path='.github/workflows',line=1,excerpt='No workflow files found.',description='No visible automated quality gate exists.',why='Broken code can reach the default branch without verification.',fix='Add CI for dependency install, tests, lint/format and build.')
    # document reality check
    runtime='\n'.join(read(p) for p in fs if re.search(r'(?i)(src|app|lib|features)',str(p.relative_to(ROOT))))
    if re.search(r'(?i)\b(mock|fixture|fake|dummy|demo)\b',runtime):
        for p in [x for x in fs if x.suffix=='.md']:
            c=read(p);m=re.search(r'(?i)(production ready|complete|fully implemented|all features)',c)
            if m:find(out,'document-reality','medium','Documentation may overstate runtime completion','Document reality check',p,c,m,'Documentation claims completion while runtime code contains demo/mock markers.','Stakeholders can make release decisions from a misleading status.','State real scope, limitations and verification evidence.',confidence='needs verification')
    # Test gap in PR diff
    if base:
        changed=sh('git','diff','--name-only',f'{base}...HEAD').splitlines(); source=[x for x in changed if re.search(r'(?i)(src|app|lib|modules|features)/',x) and not re.search(r'(?i)(test|spec)',x)]; tests=[x for x in changed if re.search(r'(?i)(test|spec)',x)]
        if source and not tests:add(out,rule='test-gap',priority='medium',title='Production code changed without a matching test change',area='Test-gap detector',path=source[0],line=1,excerpt='\n'.join(source[:12]),description=f'{len(source)} runtime source file(s) changed, but no test file changed.',why='Important behavior can regress without automated proof.',fix='Add/update focused tests or document why testing is unnecessary.',confidence='needs verification')
    # compatibility (single repo heuristic)
    fe=[p for p in fs if p.suffix in {'.ts','.tsx','.js','.jsx'}]; be=[p for p in fs if p.suffix in {'.java','.kt','.php','.py','.cs'}]
    if fe and be:
        calls=set(); routes=set()
        for p in fe:calls|=set(re.findall(r"['\"](/api/[A-Za-z0-9_?=&${}/.-]+)",read(p)))
        for p in be:routes|=set(re.findall(r'@(?:Get|Post|Put|Patch|Delete)Mapping\(\s*"([^"]*)"',read(p)))
        bad=[x for x in calls if not any(x.split('?')[0].endswith(r.strip('/')) or r.strip('/') in x for r in routes)]
        if bad:add(out,rule='be-fe-compatibility',priority='medium',title='Potential frontend/backend API mismatch',area='BE ↔ FE compatibility check',path=str(fe[0].relative_to(ROOT)),line=1,excerpt='\n'.join(sorted(bad)[:10]),description='Frontend paths do not clearly match backend routes found in this repository.',why='A UI can request an endpoint that no backend provides.',fix='Verify the API contract. Configure paired-repository OpenAPI mode for cross-repository projects.',confidence='needs verification')
    # generated temporary assets
    junk=[str(p.relative_to(ROOT)) for p in fs if p.name=='tsconfig.tsbuildinfo' or re.search(r'(?i)(^|/)(\.tmp|tmp-|temp-|screenshot|snapshot).*(\.png|\.txt|\.log)$',str(p.relative_to(ROOT)))]
    if junk:add(out,rule='tracked-artifacts',priority='low',title=f'{len(junk)} generated or temporary files are tracked',area='Dead / temporary code check',path=junk[0],line=1,excerpt='\n'.join(junk[:10]),description='Generated/cache/snapshot files are committed.',why='Review noise and repository size hide meaningful changes.',fix='Keep required assets only; remove generated files and add ignore rules.',confidence='needs verification')

def report(repo,scope,fs,out):
    history=ROOT/'.pmis-security/history.json'; old=set()
    if history.exists():
        try:old=set(json.loads(read(history)).get('fingerprints',[]))
        except Exception:pass
    for f in out:
        if f.fingerprint in old:f.title='Regression: '+f.title;f.area='Regression memory / '+f.area
    out.sort(key=lambda x:(-WEIGHT.get(x.priority,0),x.path,x.line)); counts={p:sum(x.priority==p for x in out) for p in WEIGHT}
    penalty=min(40,counts['critical']*40)+min(25,counts['high']*8)+min(15,counts['medium'])+min(5,counts['low']//2)
    score=max(0,100-penalty); ready=counts['critical']==0 and counts['high']==0 and any('.github/workflows/' in str(p.relative_to(ROOT)) for p in fs)
    lines=[f'# PMIS Security Report — `{repo}`','',f'**Checked:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}  ',f'**Scope:** {scope}  ',f'**Project health score:** **{score}/100**  ',f'**Release readiness:** {"✅ Ready" if ready else "❌ Not ready"}','',f'**Findings:** {counts["critical"]} critical · {counts["high"]} high · {counts["medium"]} medium · {counts["low"]} low','','## Findings','']
    if not out:lines+=['✅ No static findings. Human review and runtime testing are still required.','']
    for f in out:
        lines += [f'### {ICON[f.priority]} {f.priority.upper()} — {f.title}','',f'**Status:** {f.confidence.replace("_"," ")}  ',f'**Area:** {f.area}  ',f'**Location:** `{f.path}:{f.line}`  ',f'**Introduced by:** {f.author} · commit `{f.introduced}`  ',f'**Fingerprint:** `{f.fingerprint}`','','**What was found**','',f.description,'','**Why it matters**','',f.why,'','**Exact relevant source**','',f'```text\n{f.excerpt}\n```','','**Required next step**','',f.fix,'']
    lines += ['---','','## Coverage','','| Check | Result |','|---|---|','| Project health score | Included |','| BE ↔ FE compatibility | Heuristic now; paired-repository OpenAPI mode is configured per project |','| Database migration guard | Included |','| Demo-data detector | Included |','| Sensitive data scanner | Included; values are redacted |','| Dead / temporary code | Included |','| Dependency vulnerability scan | Lockfile readiness now; CVE feed can be added per ecosystem |','| CI / deployment guard | Included |','| Test-gap detector | Included for pull-request comparisons |','| Regression memory | Uses `.pmis-security/history.json` when present |','| Intern progress view | Weekly organization report uses PR/commit metadata |','| Release readiness report | Included |','| Document reality check | Included |','','> “Needs verification” is evidence for review, not an accusation.']
    return '\n'.join(lines)+'\n',{'health_score':score,**counts,'release_ready':ready,'fingerprints':[f.fingerprint for f in out]}
def main():
    a=argparse.ArgumentParser();a.add_argument('--repository',default=os.getenv('GITHUB_REPOSITORY','local/repo'));a.add_argument('--scope',default='full');a.add_argument('--base-ref',default='');a.add_argument('--output',default='pmis-security-report.md');x=a.parse_args();fs=files();out=[];scan(fs,out,x.base_ref);md,meta=report(x.repository,x.scope,fs,out);Path(x.output).write_text(md);Path('pmis-security-summary.json').write_text(json.dumps(meta));Path('pmis-security-state.json').write_text(json.dumps({'fingerprints':meta['fingerprints'],'updated_at':datetime.now(timezone.utc).isoformat()},indent=2));print(json.dumps(meta))
if __name__=='__main__':main()
