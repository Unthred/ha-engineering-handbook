# ADR-0004: Enforceable responsive dashboard visual contract

- **Status:** Accepted
- **Date:** 2026-08-12
- **Decision owners:** Handbook maintainers; installation maintainers consuming this handbook

## Context

Dashboard chapters stated intentions such as “check phone, tablet, and desktop”
and “avoid decorative empty space,” but agents could still ship layouts that:

- treated mobile-first as mobile-only;
- left large desktop structural gaps from Home Assistant Sections defaults;
- exposed development debris (issue numbers, entity IDs, implementation notes)
  in ordinary operational cards;
- treated editor preview or valid Lovelace JSON as visual acceptance.

A live analytics view defect (large desktop holes and GitHub references in
everyday cards) showed that per-task reminders are insufficient; the handbook
needed an enforceable contract.

## Decision

1. Add normative rules `HA-UX-016`–`HA-UX-018`, `HA-DESIGN-007`–`HA-DESIGN-008`,
   and `HA-TEST-016`.
2. Strengthen `HA-UX-005` and `HA-DESIGN-004` to point at the matrix and
   structural-gap rules rather than vague size checks.
3. Expand `examples/dashboard-profile.yaml` into a responsive-layout contract
   with a documented schema.
4. Require audit and change records to capture breakpoint evidence and content
   hygiene; human confirmation when the agent cannot inspect the authenticated
   frontend.
5. Propagate the rules through generated assistant instructions.

Automated checks enforce existence and propagation of the contract. They do
**not** prove that a layout looks good; visual acceptance remains a separate
gate.

## Alternatives considered

- Keep guidance advisory only: rejected; agents omitted it under time pressure.
- Mandate pixel-perfect screenshots in CI: rejected as brittle and
  installation-specific; evidence requirements are enough.
- Encode Temperature Tally-specific layout: rejected; this is a general
  handbook defect.

## Consequences

- Dashboard PRs need matrix evidence and may need a named human confirmer.
- Consuming repositories should adopt profile version 2 fields when they next
  touch dashboard standards.
- Reviewers must fail avoidable structural gaps and operational content debris
  by rule ID.
