# Naming and YAML

## HA-YAML-001 — Name by purpose

**Level:** Standard

IDs and aliases MUST describe intent, not merely location or implementation. Prefer `bedroom_blackout_close` to `blind_automation_2`.

## HA-YAML-002 — Use consistent identifiers

**Level:** Standard

Use lowercase `snake_case` for YAML IDs and helper names. Entity-friendly display names MAY use natural language.

## HA-YAML-003 — Optimise for review

**Level:** Guideline

Keep YAML explicit, consistently formatted, and locally understandable. Avoid clever templates where a straightforward condition or helper is clearer.

## HA-YAML-004 — Explain the reason

**Level:** Standard

Comments SHOULD document constraints, unusual device behaviour, or rationale. Do not narrate syntax that the YAML already makes obvious.

## HA-YAML-005 — Avoid copied constants

**Level:** Guideline

Values that represent household policy or are reused across behaviours SHOULD live in an appropriately named helper or shared variable.
