# PMIS-Group — GitHub Actions, Workflows and Organization Governance Review

**Review:** 2026-11-02 | **Classification:** Internal | **Owner:** Technology Lead | **Evidence boundary:** Source inspection of selected workflow files and repository inventory. This is not a verification of every run, every ruleset or every production configuration.

## Organization inventory
Twelve repositories were visible: `.github`, `pmis-engineering`, `pmis-backend-template-java`, `pmis-frontend-template-nextjs`, `planner`, `pmis-time-keeping-be`, `pmis-time-keeping-fe`, `pmis-time-keeping-old`, `pmis-sales-be`, `pmis-sales-fe`, `pmis-sales-3d`, and `pmis-anlife-fe`.

The only approved FE/BE application templates are `pmis-frontend-template-nextjs` and `pmis-backend-template-java`. The 3D repository is a product workstream, not a third template. `pmis-time-keeping-old` has default branch `master`; `pmis-sales-3d` uses `building-map`; others in the inventory use `main`. Branch-sensitive automations must not blindly assume `main`.

## Confirmed source patterns and risks
| Area | Source observation | Engineering action |
|---|---|---|
| Shared PMIS Security engine | `.github/workflows/pmis-security.yml` is reusable, reads dependency advisories, creates artifacts, comments on PRs, and can open report PRs. Several callers use it. | Define pinned reviewed engine release, validate caller token boundary, permissions and missing-advisory handling; monitor actual run/coverage. |
| Organization weekly activity | `pmis-security-weekly.yml` schedules weekly reporting, uploads an artifact and opens a report PR. | Verify reports run, avoid using commit volume as a personnel productivity metric, establish reader/triage owner and retention policy. |
| Frontend template bootstrap | On new project, creates labels, issues, milestones and tries to copy a canonical Scrum Project using `PMIS_PROJECT_TOKEN`. | Test fresh repository lifecycle, token scopes, idempotency, permissions and Project visibility. Maintain recovery steps for failed bootstrap. |
| Template policy workflow | Configures main branch required status (`quality` FE, `test` BE) and PR review policy. | Verify actual default branch/rulesets, whether reviewers and required checks exist; avoid reusable forced policy on non-main special repos. |
| Project status synchronization | Frontend template Project sync maps closed PRs to Done even without checking `merged`; reopened issues return to Backlog. | Review board semantics and update workflow to distinguish merged vs abandoned PRs before relying on automatic Done counts. |
| Wiki publication | Workflow copies `docs/wiki` into a separate native Wiki Git repository; requires native Wiki initialization. | Verify source-to-published parity, error handling and that manual Wiki edits do not become an untracked alternate source of truth. |
| Prepared release flow | Templates verify version file/application metadata/changelog and publish GitHub Releases; no automatic production deployment implied. | Add clear release and deployment evidence linking; consider reviewed release evidence manifest and environment approvals. |
| Sales production reset | `pmis-sales-be/.github/workflows/reset-production-after-backup.yml` can run through manual confirmation **or a branch push with an authorization marker**, on a self-hosted production runner, and executes schema destruction after backups. `prepare-final-database-reset.yml` captures a new baseline. | **P0 governance review:** if one-time migration has finished, disable/archive obsolete reset workflows via reviewed PR; require manual break-glass approval and independent backup restore evidence for any future destructive operation. Do not trigger or change without operational authorization. |
| Anlife project identity | `pmis-anlife-fe` README still describes Sales Frontend. | Record source-fork relationship, actual client/product ownership, and deployed artifact identity before rewriting architecture claims. |

## Prioritized governance backlog
### P0 — prevent accidental destructive changes
1. Audit and, after owner approval, retire one-time production database reset triggers. Restrict self-hosted production runners to approved protected workflows and environments, verify runner isolation and cleanup.
2. Require environment-level approval, audited named operator and immutable deployment source for production mutations. Never rely solely on a confirmation string as authorization.
3. Confirm backups are recent, encrypted, stored separately and restorable before destructive migration; verify rollback behavior against a nonproduction rehearsal.

### P1 — trustworthy automation and releases
1. Formalize CI required-check naming (`quality` frontend and `test` backend) and verify rulesets match actual latest workflow jobs.
2. Version/pin shared PMIS Security engine and third-party Actions (reviewed SHAs for high-privilege jobs), limit tokens to job scope and prefer GitHub App credentials where available.
3. Correct Project sync closed-without-merge behavior; ensure duplicate/abandoned project items do not count as Done.
4. Add cross-repo documentation freshness checks, protected environment deployment verification and links between releases, changelog and deployed SHAs.
5. Confirm native Wiki publication on every active repository; warn on missing Wiki initialization and track actual source-to-Wiki drift.

### P2 — scalable engineering operations
1. Keep exactly two official application templates; treat other repos as products, legacy reference or company infrastructure.
2. Define a project bootstrap acceptance test using temporary private repositories, validating labels, Projects, Wiki, protections, CI, release and cleanup before upgrading templates.
3. Create an organization software catalogue: project/business owner, technical owner, stack, repo, service level, environments, DB/backup, incident contacts and release status.
4. Establish a quarterly access/repository audit: outside collaborators, dormant branches, tokens, workflows, billing, branch rules and critical credentials.
5. Maintain one authoritative backlog per product and a lightweight company-wide portfolio view. Don't duplicate state in stale Markdown sprint boards.

## Validation checklist for every repository
Record default branch; list workflows and trigger matrix; inspect Actions permissions, secrets and environments; sample latest success/failure runs; verify CODEOWNERS and required status checks; compare Wiki to `docs/wiki`; inspect release version vs tag/deployed SHA; identify backups and operational owner. Label unverified results **Pending evidence** and create owner-linked issues.

## Change policy
This review creates no production execution, disables no workflows and changes no application code. Implement risky fixes through independent reviewed changes with explicit rollback plans, especially for database and infrastructure actions.
