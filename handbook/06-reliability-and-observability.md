# Reliability and observability

## HA-REL-001 — Detect stale and unavailable data

**Level:** Standard

Important decisions MUST distinguish valid readings from `unknown`, `unavailable`, implausible, or stale values.

## HA-REL-002 — Make failure visible

**Level:** Standard

Failures affecting essential or expected behaviour MUST surface through a proportionate persistent notification, dashboard status, log, or alert.

## HA-REL-003 — Avoid alert fatigue

**Level:** Standard

Notifications SHOULD be actionable, deduplicated, severity-appropriate, and clear about what happened and what the occupant should do. Phone failure Notifications MUST also satisfy `HA-REL-006`.

## HA-REL-004 — Observe dependencies

**Level:** Guideline

Critical integrations, batteries, coordinators, storage, backups, and remote endpoints SHOULD have health indicators and documented thresholds.

## HA-REL-005 — Restore safely

**Level:** Standard

After restart or reconnection, logic MUST re-evaluate current reality rather than blindly replaying stale actions.

## HA-REL-006 — Make phone failure Notifications actionable

**Level:** Standard

A Notification sent to the user’s phone MUST contain enough information to understand and act on the failure without searching logs or guessing which device failed.

Where applicable, every failure Notification MUST include:

- what operation failed
- which exact devices or entities failed, using human-readable friendly names (raw entity IDs only as secondary diagnostic detail when no friendly name exists)
- expected state or result
- actual state or observed result
- known failure reason (for example unavailable, unknown, timeout, service error, or wrong state)
- recovery or retries already attempted and their outcome
- the concrete action the occupant should take
- a relevant Companion-app deep link when an appropriate destination exists

For operations involving multiple targets:

- calculate and report **only** the failed subset
- NEVER use vague wording such as “one or more,” “some devices,” or “action needed” when exact failure information is available
- use correct singular and plural wording
- if details cannot be determined, say what evidence is unavailable and provide the most useful diagnostic destination
- suppress the failure Notification when verification or retry shows that all targets ultimately reached the desired state (record recovery as log-only or a non-phone status surface only when genuinely useful)

Successful status announcements (for example “monitoring on”) remain separate from failure Notifications and MUST NOT inherit failure-message requirements.

### Examples (CCTV-style multi-target apply)

**Bad:**

> Desired indoor CCTV state: disabled. One or more switches failed to follow. Action needed.

**Good:**

> Indoor CCTV failed to disable:
>
> - Kitchen Camera Motion remained on; expected off.
> - Under-bed Camera Detect is unavailable; expected off.
>
> Two retries failed. Check power or connectivity for the listed cameras.

**Why:** Away-from-home phone alerts are useless when they force log diving or guessing. Vague multi-target wording hides which controls need attention.

**Verify:** Before accepting any new phone Notification, answer: “If the occupant receives this away from home, does it tell them exactly what happened and what they can do about it?” (`HA-REVIEW-006`). Exercise failure and recovery paths; confirm suppressed Notifications after successful retry.
