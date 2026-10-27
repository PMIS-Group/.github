# PMIS Security

PMIS Security is an organization-wide, read-only GitHub review engine. It scans source,
configuration, workflows, migrations and documentation. It never runs project code,
database migrations, package-install hooks or deployment scripts.

## What every pull request receives

- a project health score and release-readiness result
- findings grouped by critical, high, medium and low priority
- exact relevant source, with values redacted where needed
- a plain-language explanation, impact and required next step
- Git author and commit attribution when history is available
- a Markdown artifact and a short pull-request review comment

## Included checks

1. health and release-readiness score
2. frontend/backend static route comparison, including optional paired repositories
3. database migration guard
4. demo/mock-data signals in runtime code
5. sensitive-data scanning with redacted evidence
6. TODO, FIXME, HACK and tracked temporary-artifact signals
7. GitHub Dependabot advisories and dependency lockfile readiness
8. CI and deployment guard
9. pull-request test-gap detector
10. regression memory through `.pmis-security/history.json`
11. weekly organization contributor activity report
12. release-readiness report
13. document-reality signals

## Caller workflow

Each project needs a small workflow that calls:

```yaml
jobs:
  audit:
    uses: PMIS-Group/.github/.github/workflows/pmis-security.yml@main
    permissions:
      contents: write
      pull-requests: write
      issues: write
      security-events: read
    with:
      scope: ${{ github.event_name == 'pull_request' && 'pull-request' || 'full' }}
      base_ref: ${{ github.event.pull_request.base.sha || '' }}
      publish_report: ${{ github.event_name == 'schedule' }}
```

For a separate frontend and backend repository, add:

```yaml
      paired_repository: PMIS-Group/example-backend
    secrets: inherit
```

The caller must pass an organization secret named `PMIS_PROJECT_TOKEN` with **read**
access to both repositories. This is only needed for paired-repository comparison and
the weekly organization progress report; it must not have write or administration access.

## Report policy

A finding can be **confirmed** or **needs verification**. The latter means that the
scanner found evidence worth reviewing; it is never a statement of fault or intent.
Attribution identifies the commit that introduced the current line.

Reports are artifacts on pull requests. Scheduled or manually published scans create a
separate report-only pull request that updates `security-reports/latest.md` and
`.pmis-security/history.json`. The weekly organization workflow creates
`security-reports/weekly-latest.md` in the central repository.
