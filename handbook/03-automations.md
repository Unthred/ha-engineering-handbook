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

Manual intervention SHOULD win for a documented period or until a clear reset condition. An automation must not immediately undo an occupant's action.

A manual-override mechanism MUST define a complete lifecycle, not just a set
condition: what sets or renews it (a repeated deliberate command MUST renew
protection, never toggle it off), what leaves it unchanged (an in-progress
manual adjustment, such as a hold or a colour cycle, MUST NOT cancel its own
protection), what clears it, and what happens under ambiguity. Clearing on
"the controlled equipment went off" MUST be based on a confirmed observed
state per affected physical unit, not assumed from the command that was
sent — a partial, unavailable, or otherwise ambiguous reading MUST fail
closed (leave the override in place) rather than clear it. A mechanism that
can only describe "protected" or "not protected" without naming its clearing
triggers does not satisfy this rule.

## HA-AUTO-006 — Use traceable structure

**Level:** Guideline

Give triggers IDs, use descriptive aliases for branches and actions, and keep traces useful enough to explain why a decision occurred.
