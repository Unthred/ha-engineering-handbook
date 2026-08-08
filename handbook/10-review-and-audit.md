# Review and audit framework

Use this framework before changing an existing Home Assistant system. An audit is evidence gathering, not permission to rewrite the home.

## Required inputs

Inspect the repository structure, configuration entry points, dashboards, themes, custom cards, helpers, automations, scripts, blueprints, secrets boundaries, deployment method, validation tools, and repository-local agent instructions. Obtain actual entity IDs from configuration or the running system; never infer them from friendly names.

## Audit process

1. Inventory the system and identify which files are authoritative versus generated or UI-managed.
2. Record supported displays, household priorities, essential functions, custom frontend dependencies, and known constraints.
3. Evaluate each applicable handbook rule and cite concrete evidence by path and object name.
4. Separate defects from preferences. Do not call a stylistic alternative a violation unless a rule or repository profile requires it.
5. Group findings by risk and dependency, then propose small reversible stages.
6. Validate each stage and state what still requires physical or user verification.

## Finding format

Every finding contains:

- stable finding ID
- severity: critical, high, medium, low, or advisory
- handbook rule ID
- evidence: file, object, and current behaviour
- impact in plain language
- recommendation and expected result
- dependency, risk, validation, and rollback notes

Do not edit while auditing unless the user explicitly requests implementation. Never produce a giant replacement dashboard before confirming the inventory and target displays.

## Remediation order

1. Safety, security, and loss of manual control
2. Broken, unavailable, or misleading behaviour
3. Conflicting automation ownership and fragile dependencies
4. Dashboard state clarity and accessibility
5. Navigation, layout, and reusable components
6. Cosmetic consistency and cleanup

## HA-REVIEW-001 — Gather evidence before judging

**Level:** Standard

An audit MUST cite the actual repository path and configuration object for every violation; assumptions and unavailable runtime evidence must be labelled explicitly.

## HA-REVIEW-002 — Separate audit from implementation

**Level:** Standard

Reviewing a system MUST NOT silently authorise edits. Findings, proposed remediation, and applied changes are separate stages unless the user explicitly combines them.

## HA-REVIEW-003 — Report by rule ID

**Level:** Standard

Every compliance finding MUST reference an applicable handbook rule ID, severity, evidence, impact, recommendation, validation, and rollback consideration.

## HA-REVIEW-004 — Remediate in reversible stages

**Level:** Standard

Remediation plans MUST prioritise safety and correctness, preserve working behaviour, limit each stage to a reviewable concern, and define success and rollback before implementation.

## HA-REVIEW-005 — Preserve user-specific intent

**Level:** Principle

An agent MUST treat documented accessibility needs, household routines, display constraints, and deliberate exceptions as design inputs rather than normalising them away.
