# Review and audit framework

Use this framework before changing an existing Home Assistant system. An audit is evidence gathering, not permission to rewrite the home.

## Required inputs

Inspect the repository structure, configuration entry points, dashboards, themes, custom cards, helpers, automations, scripts, blueprints, secrets boundaries, deployment method, validation tools, and repository-local agent instructions. Obtain actual entity IDs from configuration or the running system; never infer them from friendly names.

For dashboard work, also obtain the repository dashboard profile (or note its absence), target displays, whether Lovelace is storage-mode or YAML-mode, and whether the auditor can open the authenticated normal-view frontend.

## Audit process

1. Inventory the system and identify which files are authoritative versus generated or UI-managed.
2. Record supported displays, household priorities, essential functions, custom frontend dependencies, and known constraints.
3. Evaluate each applicable handbook rule and cite concrete evidence by path and object name.
4. Separate defects from preferences. Do not call a stylistic alternative a violation unless a rule or repository profile requires it.
5. Group findings by risk and dependency, then propose small reversible stages.
6. Validate each stage and state what still requires physical or user verification.
7. For dashboards, complete the responsive and content-hygiene checks below; do not tick “responsive” without matrix evidence.

## Responsive and presentation audit (mandatory for dashboard findings)

Reviewers MUST explicitly inspect responsive quality. Ask or observe:

| Check | Fail when |
| --- | --- |
| Desktop gaps / unused columns | Avoidable empty columns or large holes at desktop/wide widths (`HA-DESIGN-007`) |
| Section spans and packing | Inappropriate full-width bands, ignored `max_columns` / `dense_section_placement` / `grid_options` (`HA-DESIGN-008`) |
| Mobile reading order | Phone stack breaks task order or buries primary actions (`HA-UX-016`) |
| Editor-only testing | Layout checked only in the editor, not normal view (`HA-TEST-016`) |
| Missing normal-view confirmation | No named confirmer when authenticated frontend was unavailable |
| Development debris | Issue/PR refs, entity IDs, implementation notes in ordinary cards (`HA-UX-018`) |
| Conditional states | Visibility states not exercised in normal view |
| Repo vs live storage drift | Repository mirror treated as live, or live layout diverges without parity (`HA-UX-014`) |
| Missing preferred header | Profile `page_header.mode` is `preferred`/`required` but view lacks centred title + relevant pills without exception (`HA-UX-019`) |
| Decorative or excessive pills | Pills lack page purpose, exist only for symmetry, or routinely exceed ~5 (`HA-DESIGN-009`) |
| Header debris / overflow | Issue/PR refs or entity IDs in pills; poor wrap, clipping, desktop stretch, or humour that obscures function (`HA-UX-018`, `HA-DESIGN-009`) |

### Pass / fail examples

**Fail — structural gap:** At 1280 px, a short “status” section sits left of a tall history graph, leaving most of the right column empty for a full viewport height, with `dense_section_placement` off and no max-width policy. Cite `HA-DESIGN-007` / `HA-DESIGN-008`.

**Fail — mobile-only mindset:** Cards look fine at 390 px but at 1440 px a single sparse card stretches edge-to-edge with large side voids and no second column or max-width. Cite `HA-UX-016` / `HA-UX-017`.

**Fail — content hygiene:** An operational card subtitle reads `plant humidity excluded (#248)`. Cite `HA-UX-018`.

**Fail — evidence:** PR says “checked desktop” with no widths, no normal-view note, and no confirmer. Cite `HA-TEST-016` / strengthened `HA-UX-005`.

**Fail — missing preferred header:** Profile sets `page_header.mode: preferred` but an operational analytics view opens with only raw entity rows and no centred title/pills, with no documented exception. Cite `HA-UX-019`.

**Fail — decorative pills:** Six chips showing unrelated system metrics on a room lighting page, including an entity ID string. Cite `HA-DESIGN-009` / `HA-UX-018`.

**Pass:** Profile lists phone 390 and desktop 1280; normal-view screenshots or human confirmation record stacking order, shared desktop row for two short sections, full-width analytics band, no issue numbers in cards, conditional empty-state checked, and a centred characterful title with 3–4 relevant pills that wrap cleanly.

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
5. Navigation, layout, responsive structure, and reusable components
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

## HA-REVIEW-006 — Accept only actionable phone Notifications

**Level:** Standard

Before accepting any new phone Notification (especially a failure alert), the implementer MUST answer:

> If the occupant receives this away from home, does it tell them exactly what happened and what they can do about it?

A “no,” or reliance on logs, entity IDs alone, or vague multi-target wording (“one or more,” “some devices,” “action needed” when specifics are known), is a defect under `HA-REL-006`. Reviewers MUST reject or remediate such Notifications before merge.

### Phone Notification audit checks

| Check | Fail when |
| --- | --- |
| Operation named | Message does not say what failed |
| Failed targets listed | Multi-target failure uses “one or more” / “some” when exact failures are known |
| Expected vs actual | Missing expected or observed result for named targets |
| Retries / recovery | Retries happened but outcome omitted, or success-after-retry still phones a failure |
| Next action | No concrete occupant action or useful diagnostic destination |
| Deep link | Appropriate Companion destination exists but is omitted without reason |
