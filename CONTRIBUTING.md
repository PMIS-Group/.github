# Contributing to PMIS Repositories

## 1. Purpose

This standard defines the minimum expectations for changes to PMIS repositories. It supports secure, maintainable delivery for PMIS products, platforms, and client work.

## 2. Scope and precedence

These are organization-wide defaults. Repository-specific contribution files, templates, and documented requirements override them where they are more specific.

## 3. Before starting work

Confirm the business outcome, scope, owner, dependencies, and acceptance criteria. Work must normally be linked to an approved issue or task, using an identifier such as `PMIS-123`.

## 4. Task requirements

Approved work should have clear acceptance criteria and relevant security, data, operational, and documentation considerations. Keep the implementation within the approved scope; obtain approval before expanding it.

## 5. Branch naming

Do not develop directly on `main`. Keep branches short-lived and use one of these patterns:

- `feature/PMIS-123-short-description`
- `fix/PMIS-123-short-description`
- `hotfix/PMIS-123-short-description`
- `chore/PMIS-123-short-description`
- `docs/PMIS-123-short-description`
- `refactor/PMIS-123-short-description`

## 6. Commit guidance

Write clear, understandable commits that describe the change. PMIS does not require one rigid commit-message format at this time. Avoid mixing unrelated changes in a commit or branch.

## 7. Development expectations

Keep changes focused. Do not combine unrelated refactoring with feature work unless explicitly approved. Follow repository conventions, handle failures appropriately, and remove temporary debugging code before review. Generated code, including AI-generated code, must be reviewed and is owned by the submitting developer.

## 8. Testing

Run relevant automated checks and tests locally where practical. Critical workflows require appropriate automated tests. Add or update unit, integration, end-to-end, or manual test evidence as appropriate; automated checks must pass when configured.

## 9. Documentation

Update documentation in the same change where practical, including technical guidance, APIs, runbooks, configuration notes, or release information affected by the work.

## 10. Pull requests

All changes to `main` require a pull request. Link the approved work and explain the business reason, technical change, testing, security impact, deployment impact, and rollback approach. Pull requests should be small enough to review effectively.

## 11. Code review

At least one qualified reviewer must approve each pull request. Authors may self-review, but self-review is not independent approval. Address review feedback and resolve applicable conversations before merging.

## 12. Security and secrets

Never commit production secrets, credentials, access tokens, private keys, or confidential client data. Use approved secret-management systems, GitHub environment secrets, or hosting environment variables. Report exploitable vulnerabilities privately under [SECURITY.md](SECURITY.md).

## 13. Database changes

Use versioned migrations for database schema changes. Manual production schema changes are prohibited except through an approved emergency process. Document data migration, backfill, compatibility, and recovery implications.

## 14. Deployment and rollback

Document deployment effects for production-impacting changes, including configuration, environment variables, workers, scheduled jobs, integrations, and rollout order. Consider and document a rollback plan before release.

## 15. Definition of Done

A change is complete only when acceptance criteria, review, testing, documentation, and applicable release requirements are satisfied.

- [ ] Requirements implemented
- [ ] Acceptance criteria satisfied
- [ ] Code reviewed
- [ ] Automated checks passed
- [ ] Tests completed
- [ ] Security impact reviewed
- [ ] Documentation updated
- [ ] Deployment implications documented
- [ ] Rollback possible
- [ ] Release information prepared when applicable
- [ ] No secrets or sensitive data committed

## 16. Emergency changes

Emergency fixes may use an approved expedited process, but still require documentation and a retrospective review. Follow the approved incident-response process for production incidents.

## 17. Repository-specific requirements

Repository-specific requirements override these defaults when documented. They may add ownership, test, release, architecture, compliance, or operational requirements; they must not weaken applicable PMIS security controls without an approved exception.

## 18. Questions and escalation

Raise repository questions with the maintainers or Engineering Lead. Use the approved PMIS support, incident, and security processes for matters outside normal engineering work.
