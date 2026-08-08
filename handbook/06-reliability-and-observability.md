# Reliability and observability

## HA-REL-001 — Detect stale and unavailable data

**Level:** Standard

Important decisions MUST distinguish valid readings from `unknown`, `unavailable`, implausible, or stale values.

## HA-REL-002 — Make failure visible

**Level:** Standard

Failures affecting essential or expected behaviour MUST surface through a proportionate persistent notification, dashboard status, log, or alert.

## HA-REL-003 — Avoid alert fatigue

**Level:** Standard

Notifications SHOULD be actionable, deduplicated, severity-appropriate, and clear about what happened and what the occupant should do.

## HA-REL-004 — Observe dependencies

**Level:** Guideline

Critical integrations, batteries, coordinators, storage, backups, and remote endpoints SHOULD have health indicators and documented thresholds.

## HA-REL-005 — Restore safely

**Level:** Standard

After restart or reconnection, logic MUST re-evaluate current reality rather than blindly replaying stale actions.
