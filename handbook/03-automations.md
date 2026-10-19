# Automations

## HA-AUTO-001 — Define trigger semantics

**Level:** Standard

Every automation MUST make clear whether it responds to an edge, a sustained state, a schedule, or an event. Restart behaviour and initial state must be considered.

## HA-AUTO-002 — Make execution mode deliberate

**Level:** Standard

Choose `single`, `restart`, `queued`, or `parallel` based on concurrency semantics; do not accept the default accidentally.

## HA-AUTO-003 — Guard unsafe and noisy actions

**Level:** Standard

Actions that unlock, open, heat, notify repeatedly, or affect security MUST have explicit preconditions and rate limits where appropriate.

## HA-AUTO-004 — Make retries bounded

**Level:** Standard

Retries MUST have a limit, delay, and observable failure outcome. Infinite retry loops are forbidden.

## HA-AUTO-005 — Preserve user intent

**Level:** Principle

Manual intervention SHOULD win for a documented period or until a clear reset condition. An automation MUST NOT immediately undo an occupant's action.

Ordinary re-evaluations, occupancy changes, sensor updates, and the automation's own write echoes MUST NOT cancel a still-valid manual intervention. Occupant- or policy-selected timed override modes (distinct from ambient re-evaluation) MAY stack above schedules and manual holds only where that precedence is explicitly documented.

## HA-AUTO-006 — Use traceable structure

**Level:** Guideline

Give triggers IDs, use descriptive aliases for branches and actions, and keep traces useful enough to explain why a decision occurred.

## HA-AUTO-007 — Honour physical and manual controls

**Level:** Standard

Where hardware exposes a physical or local control (thermostat, wall switch, lock pad, and equivalent Home Assistant entity UIs for the same device):

1. A deliberate human setpoint or state change MUST become a temporary manual override (or an equivalent documented hold), not a race the automation immediately "corrects".
2. Automations MUST distinguish occupant-initiated changes from their own commanded writes before deciding to reassert.
3. Override end conditions MUST be explicit (for example a maximum duration and/or the next genuine schedule or mode transition). When an override ends, recalculate the desired state through the authoritative owner (`HA-ARCH-003`); do not issue an unconditional off/min/reset as the end policy unless that is the recalculated result.
4. Graceful degradation (`HA-ARCH-004`, `HA-PHIL-001`) still applies: unavailable devices hold safely; equipment protections remain in force.

**Why:** Extends `HA-AUTO-005` and `HA-PHIL-005` into enforceable control-plane behaviour for visitor-friendly homes.

**Verify:** Tests or shadow traces cover physical/UI change, automation echo suppression, scheduled handover, expiry, restart recovery, and failure hold.
