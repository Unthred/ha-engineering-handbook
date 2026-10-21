# ADR-0007: Domain behaviour specifications

- **Status:** Proposed
- **Date:** 2026-10-20
- **Decision owners:** Homeowner (campaign authorised); handbook maintainers

## Context

Occupant-facing lighting behaviour drifted because Implementers treated
production YAML and “intended = what the current files do” audits as the
contract. Equivalent wall switches then diverged without a labelled exception.
Handbook rules already require predictable behaviour (`HA-PHIL-003`),
human-first physical controls (`HA-PHIL-005`, `HA-AUTO-007`), and operational
intent docs (`HA-DOC-001`), but they do not require a consultable per-domain
specification, do not forbid inferring intent from YAML, and do not bind
equivalent physical devices the way `HA-UX-008` binds dashboard controls.

ADR-0005 already forbids copying instance-specific tables (for example Heating
V2 setpoints) into the handbook.

## Decision

1. Add **HA-DOC-003**: Implementers MUST maintain and consult domain behaviour
   specifications in the consuming Home Assistant repository before changing
   occupant-facing behaviour.
2. Add **HA-ARCH-008**: equivalent devices MUST behave consistently unless an
   explicit, justified exception is recorded in that specification.
3. Keep instance-specific behaviour in the product repository. The handbook
   owns the obligation only.
4. Treat production YAML as evidence, not automatically the intended
   specification.
5. Require each individual requirement to have status `confirmed`,
   `proposed`, or `unknown`, with confirmation provenance.
6. Missing specifications trigger a documented gap and an explicit review
   decision. They MUST NOT unconditionally block urgent repairs.

## Alternatives considered

- Put house-specific gesture tables in the handbook: rejected — violates
  ADR-0005 / `HA-DOC-002`.
- Fail closed on any occupant-facing change without a complete specification:
  rejected — would block urgent repairs; Overseer required a documented gap
  plus review decision instead of an unconditional block.
- Rely on `HA-UX-008` and `HA-DOC-001` only: rejected — Lovelace-only
  equivalence and generic intent docs did not stop wall-switch divergence.

## Consequences

- Generated assistant rules must be regenerated (`scripts/rules.py generate`).
- Consuming repositories add `docs/behaviour/` (or equivalent) content
  independently of this handbook PR.
- Urgent repairs may proceed with a recorded gap; they must not silently
  treat current YAML as the occupant contract.

## Follow-up

- Homeowner / Overseer review of this ADR and PR.
- First product-repository catalogue: lighting only; do not invent heating,
  doors, blinds, or other domain specifications in the same campaign.
