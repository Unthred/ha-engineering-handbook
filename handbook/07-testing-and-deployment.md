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
Material dashboard layout or presentation changes also require visual
breakpoint verification in normal view (`HA-TEST-016`, `HA-UX-016`–`HA-UX-018`).

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

In a production-first Home Assistant repository, implementation changes that
affect Home Assistant runtime behaviour MUST NOT be merged into the branch that
represents production-proven state (commonly `develop` in
`Unthred/HomeAssistant`) until the candidate has been deployed to the real
Home Assistant instance and validated there.

Automated tests, configuration checks, review approval, and green CI are
necessary and MUST NOT be treated as substitutes for production validation.

If production deployment is not authorised, the pull request MUST remain open
or draft and unmerged. A repository-first workflow (merge before deploy) is
permitted only when the owner **explicitly** authorises that exception; it MUST
NOT be inferred from phrases such as “implement,” “create a PR,” “merge
normally,” or “do not deploy.”

The integration branch MUST be understood as containing configuration that has
been proven where proof is required — not merely configuration that passed
static validation or CI.

**Why:** Merging runtime configuration before live proof made #249/#251 land on
`develop` while production still lacked the Bedroom Tonight package, inverting
the meaning of the integration branch.

**Verify:** Change records for operational PRs include deployment authorisation,
candidate identity/hash, immediate production validation results, and either
parity with production or an explicit `HA-TEST-013` / owner exception.

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

Preferred correction path during an authorised candidate validation session:

1. Diagnose against the live deployed implementation.
2. Apply the smallest safe live correction and prove it on production.
3. Reproduce that exact proven correction on the candidate branch (or a
   reconciliation branch from current `develop`).
4. Confirm branch content matches the proven production files (hash or
   semantic parity).
5. Only then merge.

Open-ended debugging MUST NOT leave production-managed YAML permanently
divergent from Git. Unreconciled live edits are incomplete work.

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

Natural validations that require bedtime, weather progression, or other
physical/time events MAY remain explicitly pending after safe deployment and
immediate production checks pass — but the immediate checks MUST pass before
merge. A task MUST NOT be called production-proven merely because it merged.

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
- agent-rule / handbook install updates that cannot affect Home Assistant
  runtime
- non-operational templates or examples
- tests that cannot affect production behaviour

Runtime configuration, dashboards, automations, scripts, templates,
integrations, and hardware-facing behaviour REQUIRE production-first
validation.

The change record MUST state which exception applies and why. Ambiguous cases
MUST follow the production-proof path or ask the human.

## HA-TEST-014 — Require a change matrix for multi-surface device work

**Level:** Standard

Issues and pull requests that add or change cameras (or similarly multi-surface
devices) MUST include a change matrix listing each affected surface — inventory,
integration/config, entities/helpers, automations/scripts, settings UI,
other dashboards, documentation, tests/validators, and production verification —
and mark each as changed or verified unchanged. Automated parity checks for the
canonical inventory MUST pass before merge. Validators MUST NOT operate physical
devices or send notifications.

## HA-TEST-015 — Refuse merge-before-deploy prompt conflicts

**Level:** Standard

If instructions simultaneously require merging operational Home Assistant
configuration into the production-proven branch and forbid or withhold
production deployment, the assistant MUST STOP and report the workflow conflict
rather than merging. Generic instructions to “merge normally,” “open a PR and
merge when green,” or “CI is enough” MUST NOT override `HA-TEST-007`.

Before merging operational configuration, record evidence of:

1. deployment authorisation (or an explicit owner exception under
   `HA-TEST-013`);
2. backup or rollback readiness;
3. deployed candidate identity/hash;
4. immediate production validation results;
5. pending natural validations (if any);
6. production-to-branch reconciliation (hashes or semantic parity);
7. owner-authorised exception text, if applicable.

Absence of that gate evidence means the PR MUST stay unmerged.

**Why:** The #248/#250 sequence (“implement → PR → merge → do not deploy”)
merged runtime YAML into `develop` without live proof because prompt wording
overrode the weaker reading of production-first rules.

**Verify:** A hypothetical prompt that says both “merge into develop” and “do
not deploy” for a new package is refused; docs-only PRs still may merge under
`HA-TEST-013`.

## HA-TEST-016 — Visual breakpoint verification

**Level:** Standard

Material dashboard layout or presentation changes MUST be visually verified in
**normal dashboard mode** against the consuming repository's responsive
acceptance matrix (defaults in `handbook/09-visual-design-system.md` and
`examples/dashboard-profile.yaml`). “Checked desktop” without evidence is not
sufficient.

The validation report MUST state:

- the actual viewport widths checked;
- whether normal dashboard mode was used (not editor-only);
- layout and reading order at each width;
- any clipping, overflow, excessive gaps, or awkward spans;
- whether conditional states were tested;
- who performed visual confirmation.

Editor preview, valid JSON/YAML, a successful Lovelace save, and inspection of
storage data are **not** proof of acceptable visual output. If the agent cannot
inspect the authenticated Home Assistant frontend, it MUST obtain human visual
confirmation before merging any material dashboard layout or presentation
change.

Automated linting and rule generation MAY enforce that the responsive contract
exists and propagates; they MUST NOT be treated as substitutes for visual
acceptance.

**Why:** Agents equated configuration validity with visual quality, shipping
desktop holes and editor-only checks.

**Verify:** Change records for material dashboard PRs list matrix widths,
normal-view confirmation, gap/clipping notes, conditional-state checks, and
named visual confirmer when the agent lacked frontend access.

## HA-TEST-018 — Reimplemented-logic tests require parity proof

**Level:** Standard

A test that reimplements production template, script, or configuration logic
in another language or format (a "mirror") MUST NOT be treated as proof the
production artifact itself is correct, no matter how thorough its own
scenario coverage is. Such coverage MUST be paired with either:

- a test that executes the actual production artifact (the real Jinja
  template, script, or config file) through a compatible renderer or
  interpreter, exercising the same scenarios; or
- explicit, documented evidence that the mirror and the real artifact were
  verified to produce identical output for every scenario the mirror covers.

A regression test that claims to catch a specific defect MUST be run once
against the known-bad version of the artifact and shown to fail, before it
is trusted to pass against the fix. A test suite that only ever ran against
the fixed version has not demonstrated it catches anything.

**Why:** A Python mirror of a Jinja helper module silently "fixed" a real
bug the actual template file had (a missing prefix-stripping step) by
implementing the corrected behaviour in the mirror without realising the
real artifact disagreed. Every mirror-based test passed while the deployed
template was broken; the defect was only caught by a live read-only render
of the real artifact during a production candidate deploy, immediately
before a physical test would have exercised the broken path.

**Verify:** Test suites covering reimplemented logic name, for each mirrored
function, either the real-artifact test that proves parity or the reason
none is needed (no artifact exists to mirror). Any test whose commit message
or docstring claims to be a regression test for a specific defect shows, in
the same change record, that it was run against the pre-fix code and failed.

## HA-TEST-019 — Physical verification starts with the least hazardous target and intensity

**Level:** Standard

When a candidate's proof requires exercising real hardware (`HA-TEST-011`),
the first target and intensity exercised MUST be the least hazardous
available — lowest brightness, most reversible action, least sensory-impactful
output — not the first convenient one, and not one selected only for coverage
efficiency. A deployment plan that pauses for physical confirmation MUST name
which target is safest to test first when several are available, and MUST
NOT treat a live, reloaded candidate as "not yet tested" merely because the
agent has not personally triggered it: once a candidate is reloaded, real
triggers (physical switches, schedules, other automations) can exercise it at
any time, so containment and least-hazardous ordering apply from the moment
of reload, not from the moment of an agent-initiated test.

A trace showing an automation fired without error, or a service call that is
syntactically valid, is evidence the *code ran* — it is not evidence the
*physical output was safe*. Deployment-window verification MUST assert the
actual commanded values (colour, brightness, sound level, motion, unlock
state, and similar) against known-safe bounds for the affected space, not only
absence of exceptions.

**Why:** A candidate reload made a new "complete command from off" code path
live at the moment of `automation.reload`. Fifteen minutes later, a genuine
independent household button press — not an agent-initiated test — exercised
that path for the first time and commanded an unrequested near-white colour
into a bedroom belonging to an occupant with documented chronic migraines and
evening light sensitivity. The deployment-window verification already
observed this exact automation firing for real physical gestures during the
window and correctly reported "zero errors" — that report was true and still
missed the safety defect, because it checked for exceptions, not for whether
the commanded output was an acceptable thing to happen to that person in that
room at that hour.

**Verify:** Deployment plans for candidates touching hazard-relevant hardware
(lighting colour/brightness, sound, locks, climate, motorised equipment) name
the least-hazardous first target explicitly, and record the actual commanded
values observed during the verification window — not only that verification
ran without error. Cross-reference `HA-AUTO-008`.
