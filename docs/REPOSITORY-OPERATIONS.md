# .github — Engineering Operations, Automation and Onboarding

**Classification:** Internal engineering | **Review date:** 2026-11-02 | **Maintainer:** PMIS Engineering | **Status:** Verified repository identity; runtime, production and CI claims require release-specific evidence.

## 1. Service/repository charter
**Repository:** `PMIS-Group/.github` · **Default branch:** `main`. **Purpose:** organization governance, default issue/PR templates, CODEOWNERS, shared PMIS Security runner and weekly organization reporting. **Technology/format:** GitHub Actions, GitHub organization configuration, Python-based PMIS Security.

The purpose of this handbook is to explain what this repository owns, how engineering contributors work with it, how automation is operated, what evidence is needed for deployment, and how the next maintainer can recover context without private conversations. This file does not itself claim any release has passed operational readiness.

### Scope and architectural invariants
Shared policy and reusable workflow are the source of organization-wide guidance. Changes require review of all consumer repositories and reusable workflow permission contracts.

Separate authoritative implementation from roadmap: current code/runtime defines the implemented state; approved specifications and ADRs define desired behavior; GitHub Issues/Projects show live work; changelog/tags record prepared releases; production deployment requires independent environment evidence. Documentation must not present old sprint dates as current commitments.

## 2. First-day engineer onboarding
1. Request individual GitHub organization access with MFA and least-privilege team/repository membership; do not share accounts or personal tokens.
2. Read this handbook, the repository root README, `CONTRIBUTING.md` if present, the organization standards and relevant security policy. Follow links in the current docs index, not historical sprint boards.
3. Confirm the default branch, inspect the latest commit and open PRs, and clone with an approved credential method. Record the exact environment you are using.
4. Install required runtime and tools. **Local setup reference:** Review GOVERNANCE.md, SECURITY.md, CONTRIBUTING.md, profile/README.md, pmis-security/README.md and .github/workflows. Validate security engine tests and workflow permissions before publishing.
5. Read the project's module boundaries, data authority, auth/permission rules, failure states, test strategy and migrations (where applicable).
6. Run repository-specific checks locally; keep logs or CI links for review. Never use confidential production datasets in development.
7. Select an issue with clear acceptance criteria, create a focused branch, open PR and respond to review/CI results.
8. Demonstrate ability to locate the deployment guide, known operational alerts, secrets owner (reference only), rollback process, and support escalation path.

## 3. Automation inventory and verification
Audit the repository's `.github/workflows/` before making changes; a YAML file alone does not establish that a job is enabled, green, or has the necessary secret permissions.

| Automation category | What it does | Evidence and safeguards |
|---|---|---|
| Continuous integration | Build, lint, tests and quality evidence on PR and default-branch changes where configured | Verify latest run, exact check names, required branch checks, review requirements and representative test coverage |
| PMIS Security | Organization-shared analysis and advisory security reporting when configured | Validate reusable workflow invocation and least-privilege permissions; triage findings rather than treating a generated report as approval |
| Bootstrap / repository policy | Initialize labels, milestones, Projects and branch settings where applicable | Re-run only after inspecting side effects, default branch, GitHub Project association and authorization scope |
| Issue / PR Project sync | Keep project board linked to execution metadata when configured | Confirm state/priority fields and avoid creating duplicate issues or overwriting human decisions |
| Wiki synchronization | Publish version-controlled `docs/wiki/` to native GitHub Wiki when configured | Verify first Wiki initialization, workflow status and published page content |
| Release and deployment | Prepare tagged releases and/or environment deployment according to project workflows | Require approved SHA, change record, tests, environment approvals, post-deploy check and rollback evidence |
| Scheduled and privileged maintenance | Dependency checks, reports and any infrastructure/DB jobs | Review schedules, secrets, environment restrictions and failure escalation; never treat a destructive job as routine |

**Important:** These categories are an audit checklist; they are not a statement that every category exists or is enabled in this particular repository. Confirm actual workflow paths and triggers from the default branch before changing policy or reporting success.

## 4. Delivery governance
Every change must link to one authoritative GitHub issue or approved exception. A task includes: purpose, user/business impact, acceptance criteria, owner discipline, priority, dependencies, test approach, API/data impact and completion evidence. Keep branches small; link PR to issue; explain user impact and deployment risk. Require independent code review, relevant CI and updated documentation. Freeze/rollback behavior must be explicit for critical production changes.

### GitHub Project workflow
Backlog → Ready → In Progress → In Review → Done. Blocked work records a reason and dependency. GitHub Projects is a status/portfolio view; the issue and PR contain execution evidence. Do not duplicate live issue status in static sprint tables. A closed ticket or merged PR is not automatic evidence of deployment.

### Security and access
Use GitHub environment secrets or a company-approved password manager; no credentials or raw customer production data in docs, tickets, workflow logs, scripts or generated artifacts. Keep permissions scoped to job requirements and avoid privileged execution of untrusted PR code. Periodically review dependency risk, branch protections, workflow action versions, CODEOWNERS validity, and access/offboarding records.

## 5. Release and operational acceptance
Before release, verify applicable acceptance tests, auth and role boundaries, database/migration compatibility, integration contract, CI results, staging or representative environment smoke, backup/restore or safe rollback, and monitored production health. The recorded release should show version, source SHA, approver, deployment environment, date, checks and rollback procedure. Do not infer green checks from absent API results; locate the exact workflow run.

### Recovery and incident handling
Identify incident severity and scope, preserve evidence and stop unsafe automation, open tracked incident record and communicate impact. For source changes inspect exact refs/SHAs before reverting or cherry-picking. For data systems confirm backups and migration state before altering schema. Restore only through approved runbook, validate health, and track action items to closure.

## 6. Documentation maintenance and gap closure
Maintain up-to-date root README, architecture, local development, APIs/data model, testing, environment/deployment, troubleshooting, security, change log/release policy, ownership and onboarding. Publish Wiki content from versioned source if configured; confirm synchronization rather than assuming it. When something cannot be verified, mark **Needs verification** with a tracked owner rather than writing an unsupported implementation claim.

### Project-specific verification register (complete before declaring audit closed)
| Check | Current evidence status |
|---|---|
| Default branch and repository purpose | Verified in GitHub repository inventory |
| Actual workflow list, trigger/permissions and last run | Requires per-workflow verification |
| CODEOWNERS and branch rules active | Requires GitHub settings verification |
| Local commands and tests pass on current SHA | Requires CI or developer-run evidence |
| Published Wiki matches version-controlled source | Requires native Wiki comparison |
| Latest deployed production version and environment owner | Requires deployment evidence |
| Backup, restore, security scan and release approvals | Requires operational evidence |

This register must be refreshed when ownership, workflows, runtime topology or release process changes. It deliberately distinguishes procedure from achieved compliance.
