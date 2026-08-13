# Reliability and observability

## HA-REL-001 — Detect stale and unavailable data

**Level:** Standard

Important decisions MUST distinguish valid readings from `unknown`, `unavailable`, implausible, or stale values.

## HA-REL-002 — Make failure visible

**Level:** Standard

Failures affecting essential or expected behaviour MUST surface through a proportionate persistent notification, dashboard status, log, or alert.

The absence of expected behaviour MUST NOT be the primary failure-detection mechanism for important operational workflows. Occupants MUST NOT have to notice a secondary symptom and reverse-engineer traces to learn that a consequential automation has been failing repeatedly.

**Why:** Silent multi-day aborts of overnight or security-adjacent workflows are operational defects even when the underlying fault is "only" diagnostic.

## HA-REL-003 — Avoid alert fatigue

**Level:** Standard

Notifications SHOULD be actionable, deduplicated, severity-appropriate, and clear about what happened and what the occupant should do.

A single transient failure and a workflow failing repeatedly across nights MAY warrant different escalation. Prefer replaceable HA side notifications for first failures and reserve phone Notifications for actionable or repeated cases per installation policy.

## HA-REL-004 — Observe dependencies

**Level:** Guideline

Critical integrations, batteries, coordinators, storage, backups, and remote endpoints SHOULD have health indicators and documented thresholds.

## HA-REL-005 — Restore safely

**Level:** Standard

After restart or reconnection, logic MUST re-evaluate current reality rather than blindly replaying stale actions.

## HA-REL-007 — Treat failure paths as first-class execution

**Level:** Standard

Important workflows MUST consider what happens when an intermediate action fails.

Safe cleanup, latch restoration, and other recovery operations that remain correct after failure MUST NOT depend solely on the happy path when they can execute after the failure.

Do NOT blindly continue after every error. If proceeding would create an unsafe or misleading state, fail safely and make that failure explicit.

**Why:** Temporary state and latches stranded by an aborted middle step create lasting incorrect household state even when the original fault was only diagnostic.

**Invalid:** Night shutdown fails during verification, leaves a temporary bedtime latch set, skips downstream Good Morning state, and only exposes the problem through traces.

**Valid:** Night shutdown encounters a verification error, records the exact failing stage, performs any safe required cleanup, exposes the degraded or failed execution through the established observability mechanism, and preserves enough evidence to diagnose the problem.

**Verify:** Identify temporary latches and cleanup steps; confirm they still run (or a watchdog recovers them) when an intermediate verification or optional step fails.

## HA-REL-008 — Keep verification from destroying availability

**Level:** Standard

Verification is important, but verification code itself MUST NOT unnecessarily abort an otherwise safe workflow.

Where appropriate, distinguish:

- the operation failed;
- verification failed;
- verification could not run;
- verification found an unexpected state.

Those outcomes are not automatically equivalent and MUST NOT all be treated as a hard abort of unrelated safe cleanup or state management.

**Why:** A type error or diagnostic failure in a verifier must not undo completed shutdown work or skip unrelated latch clearing.

**Verify:** Confirm post-action verifiers are isolated (for example non-blocking invocation or dual-typed inputs) so a verifier fault cannot cancel required follow-on safe steps.

## HA-REL-009 — Evidence of health for important recurring workflows

**Level:** Guideline

Important recurring workflows SHOULD provide enough observability to determine whether they are succeeding without waiting for an occupant to notice a secondary symptom.

Appropriate evidence includes last-success / last-failure state, replaceable persistent notifications, dashboard/system-health indication, and repeated-failure escalation that avoids notification spam.

**Why:** Nightly and other scheduled household workflows need a health signal, not only an on-demand forensic trail.

**Verify:** After a successful run and after a safe simulated failure, confirm an operator can tell which outcome occurred from the established observability surfaces.
