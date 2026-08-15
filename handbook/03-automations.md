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

## HA-AUTO-008 — Treat accessibility and sensory constraints as safety requirements

**Level:** Principle

Documented accessibility needs and sensory sensitivities (light, sound,
motion, or similar) are safety requirements, not preferences to normalise
away or design around only when convenient (see also `HA-REVIEW-005`). An
automation MUST NOT invent, assume, or silently reuse a default colour,
brightness, sound, or other sensory output value the user has never
specified for that purpose — including promoting an existing preset built for
one context (for example, a rarely-hit stale-state fallback) into a
different, more frequently-triggered context (for example, a universal
activation default) without the same explicit approval a new value would
need.

A safety mitigation gated on a manually-toggled, acute-episode-style setting
(for example, a migraine-severity selector defaulting to "off") MUST NOT be
treated as covering a standing, chronic condition the user has separately
documented. Absence of an active acute flag is not evidence that a standing
sensitivity does not apply; the safe default MUST hold whether or not the
user remembered to set an unrelated toggle.

**Why:** A blueprint automation hardcoded a single "day colour" (a
near-white preset originally rated low-risk only for a rare stale-colour
fallback scenario) as the default for every activation-from-off, in every
room, at every hour, with no per-room override. It reached production without
the owner ever being asked whether that colour was an acceptable default, and
its only safety branch depended on a manually-toggled acute migraine-severity
selector that was "off" (its default) at the time — even though the owner's
chronic migraines and evening light sensitivity are a standing condition, not
an occasional flare the owner must remember to flag before every light
activation. The result was an unrequested near-white light in an occupant's
bedroom at night.

**Verify:** Any automation or script that commands a sensory-affecting output
(colour, brightness, sound, etc.) as a default — rather than passing through
a value the user supplied for that specific call — names where that default
came from, whether the owner approved it for this specific use, and whether
any safety branch depends on a toggle the owner would need to actively set
versus a standing condition it should hold for regardless. Cross-reference
`HA-TEST-019` for the matching physical-verification-order requirement.
