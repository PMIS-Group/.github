# Security Policy

## 1. Security commitment

PMIS is committed to protecting its products, services, technical assets, and client information. Security concerns are assessed and handled through PMIS internal processes.

## 2. Reporting a vulnerability

Do not open public issues for exploitable vulnerabilities. Report them privately to [office@pmis.com](mailto:office@pmis.com). PMIS will acknowledge and assess reports through its internal process. Do not disclose a vulnerability publicly until disclosure is coordinated with PMIS.

## 3. What not to disclose publicly

Do not include credentials, private keys, tokens, production connection details, personal information, confidential client data, exploit steps, or other sensitive vulnerability details in issues, pull requests, discussions, or public channels.

## 4. Information to include in a private report

Provide a concise description, affected repository or component, impact, safe reproduction details, supporting evidence, and any recommended mitigation. Share sensitive material only through a PMIS-approved private channel.

## 5. Response process

PMIS will triage, assess, prioritize, remediate, validate, and coordinate communication through its internal process. Response timing depends on severity, impact, and operational circumstances; no fixed response time is promised here.

## 6. Supported repositories and versions

Security support applies to actively maintained PMIS repositories and supported deployed versions. The responsible Engineering Lead determines maintenance status and remediation approach.

## 7. Secret handling

Secrets belong in approved secret-management systems, GitHub environment secrets, or hosting environment variables. Development, staging, and production credentials must be separated. Production secrets must never be committed to source control.

## 8. Secure development expectations

Changes should apply appropriate authentication, authorization, input validation, data protection, logging, dependency, testing, and review controls. Production-impacting changes must consider deployment and rollback.

## 9. Dependency and vulnerability management

Maintain dependencies responsibly, review security advisories, and remediate confirmed vulnerabilities according to risk and operational impact. Use available repository security tooling where approved.

## 10. AI-assisted development

AI tools must not receive confidential client data or production credentials. AI-generated code receives the same ownership, review, testing, and security controls as human-written code.

## 11. Security ownership

The Engineering Lead coordinates security ownership with authorized PMIS stakeholders. Repository-specific ownership may define additional responsibilities.

## 12. Non-security support

For normal engineering, repository, access, client-support, or documentation questions, follow [SUPPORT.md](SUPPORT.md).
