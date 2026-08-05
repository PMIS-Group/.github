# PMIS GitHub Organization Standards

This is the special GitHub organization repository for PMIS. It provides organization-wide default issue forms, pull-request templates, contribution guidance, security guidance, support information, governance rules, and code ownership for repositories that do not define their own versions.

Repository-specific files override these defaults. The organization profile is stored in [profile/README.md](profile/README.md), and issue templates are stored in [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/).

These organization-wide policies are expectations. Technical enforcement is configured separately through GitHub rulesets, repository permissions, branch protection, and required checks.

| File | Purpose |
| --- | --- |
| [.github/ISSUE_TEMPLATE/config.yml](.github/ISSUE_TEMPLATE/config.yml) | Configures the issue chooser and support routes. |
| [.github/ISSUE_TEMPLATE/bug_report.yml](.github/ISSUE_TEMPLATE/bug_report.yml) | Captures reproducible defects. |
| [.github/ISSUE_TEMPLATE/feature_request.yml](.github/ISSUE_TEMPLATE/feature_request.yml) | Captures product improvement requests. |
| [.github/ISSUE_TEMPLATE/technical_task.yml](.github/ISSUE_TEMPLATE/technical_task.yml) | Captures engineering and operational work. |
| [.github/ISSUE_TEMPLATE/documentation.yml](.github/ISSUE_TEMPLATE/documentation.yml) | Captures documentation changes. |
| [.github/ISSUE_TEMPLATE/security_report.yml](.github/ISSUE_TEMPLATE/security_report.yml) | Captures non-confidential security hardening work. |
| [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | Default pull-request template. |
| [CODEOWNERS](CODEOWNERS) | Default ownership guidance. |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Contributor Covenant 2.1 code of conduct. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Organization-wide contribution standard. |
| [SECURITY.md](SECURITY.md) | Private vulnerability reporting and security expectations. |
| [SUPPORT.md](SUPPORT.md) | Support routing guidance. |
| [GOVERNANCE.md](GOVERNANCE.md) | GitHub organization governance. |
| [README.md](README.md) | This repository guide. |
| [profile/README.md](profile/README.md) | Public PMIS organization profile. |

## Maintenance

- Owner: PMIS Engineering Leads
- Review frequency: at least every six months and after significant organizational or process changes
- Approval: PMIS Engineering Lead or authorized organization owner
- Changes: through pull request

## Next configuration steps in GitHub

The following controls should be configured separately; this repository does not technically enforce them.

1. Create an organization ruleset for `main`.
2. Require pull requests.
3. Require at least one approval.
4. Require conversation resolution.
5. Block force pushes.
6. Block branch deletion.
7. Require status checks after CI is introduced.
8. Optionally require CODEOWNERS review after repository ownership is mature.
9. Configure Dependabot and secret scanning where available.
10. Review GitHub App and personal access-token policies.
