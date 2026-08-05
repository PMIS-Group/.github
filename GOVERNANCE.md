# PMIS GitHub Organization Governance

## 1. Purpose

This document defines the governance expectations for the PMIS GitHub organization.

## 2. Organization ownership

PMIS owns all repositories and technical assets in the organization.

## 3. Organization roles

Organization owners are limited to the CTO/Tech Lead and a trusted backup owner. Ordinary developers are organization members, not owners. Shared accounts are prohibited; members use individual GitHub identities with MFA.

## 4. Team structure

The initial teams are `@PMIS-Group/Leads` and `@PMIS-Group/Developers`. Future teams may include QA, Platform, Security, Product, Support, and Contractors when justified.

## 5. Repository ownership

Each repository must have an accountable technical owner, normally represented through a team or repository-specific CODEOWNERS file. Ownership rules require appropriate repository access.

## 6. Repository creation

Repository creation is restricted to authorized organization owners. New repositories must have a purpose, owner, visibility decision, and appropriate baseline controls.

## 7. Repository visibility

Repositories are private by default. Public repositories require explicit approval and must not expose client, production, or confidential information.

## 8. Access model

Base repository permission remains `None`. Grant access through teams whenever practical and provide only the minimum necessary permissions. Developers should not receive organization-wide administrative roles by default.

## 9. External collaborators

Contractors receive minimum necessary, time-limited access. Their access, repository scope, responsible owner, and review date must be documented.

## 10. Administrative privileges

Administrative privileges are limited to authorized organization owners and must be used only for PMIS business needs.

## 11. GitHub Apps and integrations

GitHub Apps and integrations must be reviewed before installation for necessity, requested permissions, data handling, ownership, and ongoing maintenance.

## 12. Repository archiving and deletion

Repository deletion or transfer requires explicit owner approval. Archive repositories when appropriate and preserve required records, ownership, and recovery considerations.

## 13. Access reviews

Review access periodically and after major staffing changes, paying particular attention to privileged, contractor, and inactive access.

## 14. Offboarding

Remove access immediately during offboarding, including organization membership, team membership, external collaboration, tokens, integrations, and other applicable access paths.

## 15. Exceptions

Document exceptions with the reason, accountable owner, risk, and review date. Exceptions require approval by an authorized organization owner.

## 16. Review cycle

Review this governance document at least every six months and after significant organizational or process changes.
