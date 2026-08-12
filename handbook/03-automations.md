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
occupied living spaces MUST NOT act on a single transient inferred-state
reading (for example one high sleep-confidence sample).

Inferred human states such as **asleep**, **absent**, or **inactive** MUST NOT
directly trigger disruptive actions without corroboration appropriate to the
outcome, a cancellation opportunity where practical, and final revalidation.

They MUST:

1. Treat probabilistic sensors as **candidate** evidence only. Prefer a
   confirming sample or equivalent debounce that respects the sensor’s real
   update cadence — do not invent certainty with an arbitrary long `for`
   duration on a stale sticky reading.
2. **Fail safe** when required inputs are `unknown`, `unavailable`, stale, or
   mutually contradictory — skip the disruptive action.
3. Where the occupant may be present and using the space, offer a **short
   confirmation / grace window** with a clear warning when a practical display
   channel exists, so deliberate human interaction can cancel before shutdown.
4. Distinguish **deliberate human interaction** (remote command, manual volume,
   UI/`user_id` context, wall-switch events, intentional Assist, companion
   actions) from **automatic device transitions** (programme end, idle,
   screensaver, autoplay, CEC, automation-generated changes). Only deliberate
   interaction cancels a pending sleep-style confirmation; automatic media
   transitions MUST NOT.
5. Understand that **active playback or powered media may be room context**
   (where to warn / what to shut down) without being permanent proof of awake
   or asleep. Whether active use is a hard veto or merely context depends on
   the automation’s purpose and MUST be documented.
6. **Re-validate** every safety condition immediately before each destructive
   step, not only at first trigger.
7. **Cancel** pending delayed shutdowns when deliberate awake evidence appears
   or confidence falls / goes stale.
8. Use an explicit concurrency mode (`single` unless a documented reason for
   another mode exists) so overlapping runs cannot stack destructive actions;
   at most one confirmation countdown at a time.
9. Avoid latching “already processed” helpers until a genuine disruptive
   sequence begins or completes as designed. Cancellation MUST NOT set that
   latch.
10. When skipping or cancelling because the occupant appears awake, **log the
    reason only** — do not send a phone notification merely for cancellation.
11. If a required warning cannot be delivered during confirmation-based
    rollout, fail safe (cancel / skip) rather than silently powering off.
12. Validate behaviour with traces, template evaluation, or controlled helper
    tests — **not** by shutting down a room the occupant is actively using
    during development.
13. When a disruptive automation also owns **external side effects** (phone /
    watch Notifications, critical notification channels, sirens, alarm audio,
    emergency/security notify pools, camera security responses, or delayed
    cleanup against real devices), development and capture/restore tests MUST
    use a **structural test-mode / production-incident gate** (`HA-TEST-017`).
    Panel state alone (for example “alarm remained disarmed”) is **not** proof
    that those channels were unreachable.

**Why:** A false sleep or presence signal must not black out a room without
giving a present occupant a chance to cancel through ordinary interaction.
Mistaking autoplay or screensaver for “awake” (or treating any playback as
permanent veto) both defeat the purpose of sleep wind-down. Separately, a
“harmless” light capture/restore that still shares production notify/siren
scripts can wake a watch even when the alarm panel stays disarmed.

**Verify:** Review shows corroborating/debounce logic matched to sensor
cadence, deliberate-vs-automatic cancel rules, grace/warning where practical,
last-moment rechecks, and non-destructive test evidence. Sample invalid
designs (act on one confidence sample with no confirmation; cancel because
media went idle; treat playing media as permanent veto when the goal is
falling-asleep-on-the-sofa; prove harmlessness from panel state while still
calling `notify.mobile_app_*` / siren scripts) are rejected in review.
