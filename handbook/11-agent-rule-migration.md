# Agent rule installation and migration

Installing generated handbook instructions into an established repository is a controlled migration, not a file replacement. Existing rules may encode credentials-vault workflows, deployment procedures, infrastructure access, repository boundaries, safety restrictions, user needs, and agent skills that a shared handbook cannot know.

The handbook remains vendor-neutral. Projects may use OpenBao, Vault, Infisical, 1Password, or another secrets manager; the repository-local overlay identifies the actual system and its safe operating procedure. Secret values never belong in either layer.

## Required migration evidence

Before changing active instructions:

1. Identify every supported workspace root and every instruction-loading mechanism.
2. Back up the active rules with their paths and a manifest.
3. Inventory substantive capabilities and prohibitions, not only filenames.
4. Map every old instruction to its destination or explicit retirement decision.
5. Install generated rules and a clearly separated local overlay.
6. Validate generated-file integrity, discovery, references, skills, scripts, and repository status.
7. Keep the migration uncommitted until no unresolved preservation gap remains.

The preservation matrix classifies each substantive instruction as: preserved verbatim; preserved equivalently; intentionally superseded by named handbook rules; weakened; missing; or present but undiscoverable. The final three classifications block approval.

## HA-MIGRATE-001 — Back up active instructions

**Level:** Standard

Before an agent changes repository or workspace instructions, it MUST create a restorable backup with original relative paths, filenames, and a manifest. The backup MUST exclude secret values and MUST NOT overwrite an earlier backup.

## HA-MIGRATE-002 — Inventory capabilities, not filenames

**Level:** Standard

A migration MUST inventory every substantive capability, restriction, workflow, safety control, skill, script dependency, and authority boundary in the previous active instruction chain. Moving or renaming a file is not evidence that its behaviour was preserved.

## HA-MIGRATE-003 — Keep shared and local authority separate

**Level:** Standard

Generated handbook rules MUST provide shared engineering standards. Repository-specific operational knowledge MUST live in a clearly identified local overlay whose authority and conflict policy are documented.

## HA-MIGRATE-004 — Preserve secrets-manager workflows

**Level:** Standard

If a project uses an external secrets manager, migration MUST preserve the discoverable workflow for authentication, lookup, creation, update, rotation, naming, and safe handling without copying secret values into instructions, repositories, logs, reports, or chat output.

## HA-MIGRATE-005 — Preserve operational access

**Level:** Standard

Migration MUST preserve documented production access, deployment, validation, reload, restart, rollback, infrastructure, container, and repository-boundary procedures unless an authorised decision explicitly retires or replaces them.

## HA-MIGRATE-006 — Prove discovery from every workspace root

**Level:** Standard

Every required rule and local capability MUST be demonstrably discoverable when the agent is opened from each supported workspace root. A parent-workspace rule, symlink, pointer, or README mention is insufficient unless the normal agent-loading path is verified.

## HA-MIGRATE-007 — Produce a preservation matrix

**Level:** Standard

Before removing or superseding old instructions, the migration MUST map each substantive instruction to preserved verbatim, preserved equivalently, intentionally superseded by named handbook rule IDs, weakened, missing, or undiscoverable.

## HA-MIGRATE-008 — Block unresolved gaps

**Level:** Standard

A migration MUST NOT be committed while any instruction is weakened, missing, undiscoverable, ambiguously conflicting, or dependent on an unverified loading path. The stricter rule governs security, production safety, access control, deployment, and destructive actions.

## HA-MIGRATE-009 — Validate skills and supporting assets

**Level:** Standard

Migration MUST verify that required skills, helper scripts, templates, documentation, symlink targets, and referenced files still exist and remain invocable through their documented paths.

## HA-MIGRATE-010 — Verify generated instruction integrity

**Level:** Standard

Installed generated instructions MUST match the output produced from the recorded handbook revision. Generated files MUST NOT be edited to hold repository-local policy.

## HA-MIGRATE-011 — Preserve unrelated workspace state

**Level:** Standard

Rule installation MUST preserve unrelated tracked and untracked work, MUST NOT expose credentials, and MUST report the exact changed files and repository status before approval.

## HA-MIGRATE-012 — Separate installation from system changes

**Level:** Standard

Installing or migrating agent instructions MUST NOT implicitly authorise an audit, configuration edit, deployment, commit, push, or pull request. Each later stage requires its own explicit scope or approval.
