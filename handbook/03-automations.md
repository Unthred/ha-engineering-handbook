# Automations

## HA-AUTO-001 — Define trigger semantics

**Level:** Standard

Every automation MUST make clear whether it responds to an edge, a sustained state, a schedule, or an event. Restart behaviour and initial state must be considered.

## HA-AUTO-002 — Make execution mode deliberate

**Level:** Standard

Choose `single`, `restart`, `queued`, or `parallel` based on concurrency semantics; do not accept the default accidentally.

## HA-AUTO-003 — Guard unsafe and noisy actions

**Level:** Standard

Actions that unlock, open, heat, notify repeatedly, affect security, or
disrupt occupied living spaces (room shutdown, media power-off, Night/Away
mode, alarm arming) MUST have explicit preconditions and rate limits where
appropriate. Disruptive shutdown and sleep paths MUST also satisfy
`HA-AUTO-007`.

## HA-AUTO-004 — Make retries bounded

**Level:** Standard

Retries MUST have a limit, delay, and observable failure outcome. Infinite retry loops are forbidden.

## HA-AUTO-005 — Preserve user intent

**Level:** Principle

Manual intervention SHOULD win for a documented period or until a clear reset condition. An automation must not immediately undo an occupant's action.

## HA-AUTO-006 — Use traceable structure

**Level:** Guideline

Give triggers IDs, use descriptive aliases for branches and actions, and keep traces useful enough to explain why a decision occurred.

## HA-AUTO-007 — Corroborate before disruptive home actions

**Level:** Standard

Automations or scripts that automatically shut down rooms, power off media
equipment, change house mode to Night/Away, arm alarms, or otherwise disrupt
occupied living spaces MUST NOT act on a single transient sensor reading.

They MUST:

1. Require **corroborated evidence** appropriate to the outcome (for example
   sustained sleep confidence plus room evidence), not a brief spike.
2. **Fail safe** when required inputs are `unknown`, `unavailable`, stale, or
   mutually contradictory — skip the disruptive action.
3. **Debounce** flaky signals with a sustained `for` duration or equivalent.
4. Treat active viewing or recent occupied activity in the affected area as a
   **hard veto** (for example TV/Shield/receiver playback or a powered living-
   room viewing session must block sleep-triggered living-room shutdown).
5. **Re-validate** every safety condition immediately before each destructive
   step, not only at first trigger.
6. **Cancel** pending delayed shutdowns when contradictory awake activity
   resumes.
7. Use an explicit concurrency mode (`single` unless a documented reason for
   another mode exists) so overlapping runs cannot stack destructive actions.
8. Avoid latching “already processed” helpers until a genuine disruptive
   sequence begins or completes as designed.
9. When skipping because the occupant appears awake, **log the reason only** —
   do not send a phone notification for a successful veto.
10. Validate behaviour with traces, template evaluation, or controlled helper
    tests — **not** by shutting down a room the occupant is actively using.

**Why:** A false sleep or presence signal must not black out a room while
someone is awake and using it. Disruptive automation without corroboration is
a reliability defect, not an acceptable edge case.

**Verify:** Review of disruptive automations shows sustained triggers, viewing/
activity vetoes, last-moment rechecks, cancel-on-awake behaviour, and
documented non-destructive test evidence. Sample invalid design (act on one
confidence sample while media is playing) is rejected in review.
