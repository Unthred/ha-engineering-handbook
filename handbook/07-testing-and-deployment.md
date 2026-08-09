# Testing and deployment

This chapter covers validation, candidate deployment, behavioural proof, and
merge gates for Home Assistant configuration. Static checks are necessary and
insufficient for operational changes that control a live home.

## Lifecycle overview

For **repository-managed** operational configuration (YAML packages, automations,
scripts, and other Git-owned files that Home Assistant loads):

1. Create a clean feature branch from the intended integration baseline.
2. Prepare a bounded candidate change.
3. Validate it statically (`check_config`, repository tests, and local checks).
4. Commit the candidate so it has an immutable identity.
5. Push it and open a pull request, **keeping the PR unmerged**.
6. Record the exact candidate commit and rollback baseline.
7. Deploy that **exact** candidate selectively to production.
8. Use the narrowest supported reload; restart Core only with explicit approval
   and evidence that reloads are insufficient (`HA-TEST-006`).
9. Test against the real Home Assistant state and physical hardware
   (`HA-TEST-005`, `HA-TEST-011`).
10. If testing finds defects, amend the same branch and repeat from static
    validation — do not debug by editing production-managed YAML outside Git.
11. Merge only after production behaviour is proven (`HA-TEST-008`).
12. Verify repository and production parity after merging (`HA-TEST-012`).

For **UI / storage-managed** configuration (storage-mode Lovelace and other
live UI-owned objects), follow `HA-UX-014` and `HA-TEST-010`: change live state
surgically, prove behaviour, then export the proven representation into Git.

## HA-TEST-001 — Validate before deployment

**Level:** Standard

A candidate MUST pass Home Assistant configuration validation and applicable
repository checks before it is deployed to production. Static validation alone
MUST NOT be treated as permission to merge operational configuration into the
integration branch.

## HA-TEST-002 — Test boundaries and failure paths

**Level:** Standard

Tests or documented verification MUST cover unavailable inputs, threshold edges,
restart behaviour, concurrent triggers, and manual overrides where relevant.

## HA-TEST-003 — Make changes reversible

**Level:** Standard

Changes SHOULD be small enough to review and revert. Risky changes require a
documented rollback path before candidate deployment, including the exact
rollback baseline commit and the files in scope.

## HA-TEST-004 — Prefer isolation when a safe non-production path exists

**Level:** Guideline

When an installation provides an equivalent non-production Home Assistant
environment, experimental logic SHOULD be isolated there or limited to
non-critical entities before it controls the live home.

When an installation has **no** equivalent staging or non-production Home
Assistant (an installation-specific operating constraint, not a general
recommendation for every project), production validation is intentional and
MUST follow `HA-TEST-007` through `HA-TEST-012`: exact-commit based, bounded,
reversible, selectively deployed, minimally reloaded, evidenced by entity
state, and physically confirmed when software state cannot prove real-world
behaviour.

Absence of staging MUST NOT be treated as permission to merge unproven
operational configuration, to broaden deployment scope, or to debug through
uncommitted edits on the production host.

## HA-TEST-005 — Verify the outcome

**Level:** Standard

A successful reload is not proof of correct behaviour. Verify resulting entity
state, traces, logs, notifications, and physical outcome as applicable. Do not
treat a successful service-call HTTP response as behavioural proof.

## HA-TEST-006 — Use the narrowest safe reload

**Level:** Standard

Deployment MUST use the narrowest supported reload or restart that applies the
change. A full Home Assistant Core restart requires a documented reason, impact
check, explicit approval, and post-restart verification when a domain or
integration reload would suffice.

## HA-TEST-007 — Prove operational candidates before merge

**Level:** Standard

Operational Home Assistant configuration that affects runtime behaviour MUST NOT
be merged into the installation's integration branch (commonly `develop`) until
the exact candidate commit has been deployed and behaviourally proven in the
required real environment, or an accepted exception under `HA-TEST-013` applies
and is stated in the change record.

The integration branch MUST be understood as containing configuration that has
been proven where proof is required — not merely configuration that passed
static validation.

## HA-TEST-008 — Deploy an immutable candidate commit

**Level:** Standard

A production candidate deployment of repository-managed configuration MUST
identify and deploy an exact Git commit. The deployment record MUST include:

- exact candidate commit
- exact rollback baseline commit
- files in scope
- deployment mechanism used
- pre-deployment production fingerprints for in-scope files
- post-copy byte-level or semantic verification against the candidate
- minimum reload plan
- expected physical effects
- behavioural test procedure
- rollback procedure
- final repository/production parity result after merge (when merging)

Debugging MUST NOT proceed through uncommitted edits to production-managed YAML
or other Git-owned operational files on the production host. Corrections MUST be
made on the feature branch, re-validated, and redeployed as a new or amended
candidate commit with approval.

## HA-TEST-009 — Keep candidate deployment selective

**Level:** Standard

A candidate deployment MUST copy only the in-scope files from the recorded
candidate commit (or an equivalent selective mechanism that cannot introduce
unrelated content).

If the normal deployment tool would deploy unrelated content — for example a
full-tree `rsync --delete` of an entire checkout, or a branch that is not the
candidate — the agent MUST stop and report the conflict, or use an
already-approved selective mechanism. It MUST NOT silently broaden deployment
scope, overwrite secrets, or modify `.storage` as part of a YAML candidate
deploy.

## HA-TEST-010 — Prove UI-managed state before recording it in Git

**Level:** Standard

For storage-mode dashboards and other live UI-managed objects:

1. Inspect and back up the exact live object.
2. Make the smallest supported surgical production change (`HA-UX-011`,
   `HA-UX-012`).
3. Do not edit `.storage` files directly.
4. Test the resulting live controls and physical behaviour.
5. Export or otherwise reproduce the proven live state in the repository.
6. Verify semantic parity between live state and the repository mirror.
7. Commit and merge the proven representation.

Editing an exported dashboard JSON file in the repository does **not** update
the live storage-mode dashboard. Repository mirrors MUST NOT be imported over
live Lovelace unless that import is an explicitly approved operation with its
own backup and rollback plan.

## HA-TEST-011 — Confirm physical outcomes when state is insufficient

**Level:** Standard

When entity state, traces, or logs cannot prove the real-world outcome (for
example visible light level, sound, motion, or appliance behaviour), the agent
MUST obtain user confirmation of the physical result before treating the
candidate as proven. Physical tests MUST be bounded, reversible where
practical, and limited to the devices in scope.

## HA-TEST-012 — Verify parity after merge

**Level:** Standard

After merging a proven operational candidate, the agent MUST verify that the
integration branch contains the proven change and that production still matches
the in-scope proven content (byte or semantic parity). Merge MUST NOT silently
trigger an additional production deploy unless that deploy is separately
approved.

## HA-TEST-013 — Scoped exceptions to production proof

**Level:** Standard

The production-proof-before-merge requirement (`HA-TEST-007`) MAY be skipped
only for changes that do not depend on Home Assistant runtime behaviour or
physical hardware, such as:

- documentation-only changes
- CI or tooling-only changes
- non-operational templates or examples
- tests that cannot affect production behaviour

The change record MUST state which exception applies and why. Ambiguous cases
MUST follow the production-proof path or ask the human.
