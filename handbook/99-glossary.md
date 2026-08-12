# Glossary

**ADR** — Architecture Decision Record; a durable record of context, decision, and consequences.

**Essential function** — A household capability whose loss affects safety, access, accessibility, sleep, heating, or other significant needs.

**Generated rule** — Assistant-specific guidance derived mechanically from normative handbook rules.

**Helper** — A Home Assistant entity used to store policy, state, thresholds, selections, or user overrides.

**Manual override** — An occupant action that temporarily or persistently takes precedence over automation.

**Normative rule** — A rule with a stable `HA-<AREA>-NNN` identifier and declared level.

**Active implementation task** — The single in-flight change lifecycle an assistant
is executing in a workspace, spanning investigation through closeout—not merely
the act of editing files.

**Parked task** — An implementation deliberately paused with a complete formal
parking record so it can be resumed safely without guessing; parking is not
authorization to resume.

**Source of truth** — The authoritative location from which derivative configuration or documentation is produced.

**Dashboard profile** — Repository-owned YAML that records responsive layout
policy, viewport validation widths, Sections packing choices, visual
confirmation requirements, and content-hygiene expectations. It is not loaded
by Home Assistant at runtime.

**Responsive acceptance matrix** — The set of viewport widths and required
outcomes used to accept a dashboard layout (`HA-TEST-016`). Handbook defaults
may be overridden by the dashboard profile.

**Structural layout gap** — An avoidable empty region caused by section
placement, spans, or packing—not purposeful separation or a documented maximum
content width (`HA-DESIGN-007`).

**Dense section placement** — Home Assistant Sections option that packs shorter
sections into leftover horizontal space; helpful for reclaiming empty columns,
harmful when it confuses reading order (`HA-DESIGN-008`).

**Page header pattern** — Preferred operational page identity: a centred
characterful title, optional compact subtitle, and a centred wrapping row of
page-relevant status pills (`HA-UX-019`, `HA-DESIGN-009`). Profile
`page_header.mode` may be `preferred`, `required`, `optional`, or `disabled`.
