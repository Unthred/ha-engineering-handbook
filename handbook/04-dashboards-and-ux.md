# Dashboards and UX

## HA-UX-001 — Design around tasks

**Level:** Principle

A dashboard SHOULD prioritise what an occupant needs to understand or do, not expose every available entity.

## HA-UX-002 — Show state before control

**Level:** Standard

Controls MUST communicate the current state, pending transitions, unavailable states, and important consequences.

## HA-UX-003 — Keep common actions close

**Level:** Guideline

Frequent actions SHOULD require minimal navigation. Diagnostic and rare controls belong in secondary views.

## HA-UX-004 — Use consistent visual language

**Level:** Standard

The same colour, icon, label, and interaction pattern MUST mean the same thing across dashboards.

## HA-UX-005 — Build for the actual displays

**Level:** Standard

Views MUST be validated in normal dashboard mode against the repository dashboard profile's responsive acceptance matrix (`HA-TEST-016`), including at least one phone width and one desktop width. Editor preview alone is not validation. Passing a phone check does not excuse a poor desktop layout, and passing a desktop check does not excuse a compromised phone layout.

## HA-UX-006 — Use the design system

**Level:** Standard

Dashboard changes MUST use the tokens, components, state treatments, and layouts in `handbook/09-visual-design-system.md`; local one-off styling requires a documented reason.

## HA-UX-007 — Reserve colour for meaning

**Level:** Standard

Colour MUST communicate state, severity, or a deliberate accent. Decorative colour must not compete with warnings, active controls, or unavailable states.

## HA-UX-008 — Keep interaction behaviour consistent

**Level:** Standard

Equivalent controls MUST use the same tap, hold, and more-info behaviour. Consequential actions require confirmation or an interaction that makes accidental activation unlikely.

## HA-UX-009 — Prefer progressive disclosure

**Level:** Guideline

Primary views SHOULD show current state and frequent actions; detail, history, settings, and diagnostics should be revealed through subviews or more-info rather than shown permanently.

## HA-UX-010 — Make exceptional states explicit

**Level:** Standard

Unknown, unavailable, stale, warning, and critical states MUST be visually distinguishable without relying on colour alone and must not masquerade as a normal off state.

## HA-UX-011 — Prefer surgical dashboard edits

**Level:** Standard

An existing dashboard MUST be changed by the smallest reliable merge. An assistant MUST NOT replace a complete view, section, or card collection when the requested outcome can be achieved by editing the affected objects.

## HA-UX-012 — Preserve storage-mode properties

**Level:** Standard

Dashboard edits MUST preserve `grid_options`, layout metadata, and unknown storage-mode properties unless their removal is an explicit part of the approved change. A serializer's inability to interpret a property is not permission to discard it.

## HA-UX-013 — Avoid duplicate navigation

**Level:** Standard

An assistant MUST inspect existing dashboard, view, kiosk, and browser navigation before adding back, home, or menu controls. Equivalent navigation MUST NOT be duplicated.

## HA-UX-014 — Treat storage-mode dashboards as live-first

**Level:** Standard

Storage-mode Lovelace and other UI-managed dashboard state live on the Home
Assistant instance. Repository JSON exports are mirrors for review and backup,
not the runtime source, unless the installation has explicitly adopted a
YAML-mode dashboard.

An assistant MUST NOT assume that editing `dashboards/*.json` (or similar
exports) updates the live UI. Live repairs follow `HA-TEST-010`: backup the
live object, apply a surgical UI change, prove behaviour, then refresh the
repository mirror and verify semantic parity. Direct edits to `.storage` files
are forbidden.

## HA-UX-015 — Keep settings UIs aligned with device capability

**Level:** Standard

Operational settings views for a device class MUST present consistent
user-facing controls for every inventoried device. Detection capability and
notification preference MUST be shown as distinct concepts. Disabled or retired
notification paths MUST NOT appear as working toggles. Issue numbers and
internal automation names MUST NOT replace the established primary control
label. Missing devices, stale labels, or capability chips that contradict the
canonical inventory are defects.

## HA-UX-016 — Mobile-first progressive enhancement

**Level:** Standard

Dashboard work MUST begin with a coherent single-column phone hierarchy and
progressively enhance wider displays. Tablet and desktop layouts MUST use
available space deliberately without changing task order, creating substantial
structural gaps, stretching sparse content, or impairing the phone experience.
“Mobile-first” does **not** mean “mobile-only”: desktop quality is part of the
definition of done. Passing mobile validation does not excuse a poor desktop
layout, and passing desktop validation does not excuse a compromised phone
layout.

Required outcomes:

- a logical single-column mobile reading and interaction order;
- progressive enhancement at wider widths;
- preservation of information hierarchy and task order across breakpoints;
- deliberate use of additional desktop width;
- no desktop layout that simply stretches phone cards excessively;
- no desktop layout that leaves large avoidable holes or half the viewport unused;
- no desktop optimisation that damages mobile stacking or usability.

**Why:** Vague “check phone and desktop” guidance allowed agents to ship
phone-shaped layouts that left large empty regions on desktop, or to “fix”
desktop at the expense of mobile stacking.

**Verify:** Normal-view checks at profile phone and desktop widths show the
same task order, usable controls on phone, and deliberate column use on
desktop without avoidable holes (`HA-TEST-016`, `HA-DESIGN-007`).

## HA-UX-017 — Deliberate responsive space use

**Level:** Standard

At tablet and desktop widths, additional space MUST be used intentionally:
balanced columns, shared rows for shorter operational sections, deliberate
full-width analytical sections, or an explicit maximum content width. A layout
that merely scales a sparse phone composition across a wide viewport is
defective. Home Assistant Sections mechanics (`max_columns`,
`dense_section_placement`, section `column_span`, card `grid_options`) MUST be
chosen deliberately for the view (`HA-DESIGN-008`).

**Why:** Default Sections packing often produces empty columns and stranded
short sections beside tall ones when agents accept UI defaults.

**Verify:** Desktop and wide-desktop matrix checks show purposeful columns or a
documented max-width; empty columns and large placement holes are absent or
justified in the dashboard profile.

## HA-UX-018 — Operational UI content hygiene

**Level:** Standard

Normal operational UI MUST help the occupant understand state or decide what to
do. Ordinary user-facing cards MUST NOT expose development or implementation
debris unless explicitly requested or necessary for safe operation. Keep the
following out of everyday operational cards:

- GitHub issue and pull-request references;
- internal entity IDs;
- internal automation, script, or helper names;
- implementation notes and debugging comments;
- model mechanics and source-code terminology;
- historical development explanations;
- caveats that belong in documentation or diagnostics.

Examples of defective everyday copy: `plant humidity excluded (#248)`,
`not sun-exposed gate/garden sensors`, or prose that describes exactly how a
calculation is implemented.

Retain useful detail in documentation, diagnostics, or an explicitly technical
view. Do **not** hide meaningful uncertainty, stale-data warnings, safety
information, data provenance needed for trust, or reasons an automation cannot
act.

**Why:** Development notes left in cards train occupants to ignore the UI and
leak internal process into the living space.

**Verify:** Review every new or changed user-visible string on the view; reject
issue/PR markers, raw entity IDs, and implementation narration in ordinary
cards.
