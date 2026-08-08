# Testing and deployment

## HA-TEST-001 — Validate before deployment

**Level:** Standard

Configuration MUST pass Home Assistant configuration validation and repository checks before production use.

## HA-TEST-002 — Test boundaries and failure paths

**Level:** Standard

Tests or documented verification MUST cover unavailable inputs, threshold edges, restart behaviour, concurrent triggers, and manual overrides where relevant.

## HA-TEST-003 — Make changes reversible

**Level:** Standard

Changes SHOULD be small enough to review and revert. Risky changes require a rollback path before deployment.

## HA-TEST-004 — Separate development from production

**Level:** Guideline

Experimental logic SHOULD be isolated and disabled by default or tested against non-critical entities before controlling the live home.

## HA-TEST-005 — Verify the outcome

**Level:** Standard

A successful reload is not proof of correct behaviour. Verify resulting state, traces, logs, notifications, and physical outcome as applicable.
