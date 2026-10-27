# PMIS Security

PMIS Security is an organization-wide, read-only review engine. It scans source,
configuration, workflows, migrations and documentation. It never executes project
code, database migrations, package install hooks or deploy scripts.

## Included checks

- health and release-readiness score
- database migration guard
- sensitive-data scanner with redacted evidence
- demo/mock-data detector
- temporary/dead-code signals
- dependency lockfile readiness
- CI and deployment guard
- pull-request test-gap detector
- regression memory through `.pmis-security/history.json`
- document-reality signals
- frontend/backend route heuristic; project-specific OpenAPI pairing is the next enhancement

## Report policy

A finding always includes priority, exact relevant source, plain-language impact,
recommended next action and Git author/commit attribution when Git history is available.
`Needs verification` means the scanner found evidence, not that it proved wrongdoing.

Reports are artifacts on pull requests. Scheduled or manually published reports are
written to `security-reports/latest.md` through a separate review-only pull request.
