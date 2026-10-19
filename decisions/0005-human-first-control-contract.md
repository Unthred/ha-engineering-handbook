# ADR-0005: Human-first control contract

- **Status:** Proposed
- **Date:** 2026-10-19
- **Decision owners:** Homeowner (approval pending); handbook maintainers

## Context

Household policy requires that visitors can operate essential functions as an ordinary home. Existing rules (`HA-PHIL-001`, `HA-PHIL-003`, `HA-AUTO-005`, glossary "Manual override") already forbid immediate undo of occupant actions, but do not fully cover visitor-first framing, write-echo discrimination, override end conditions, or recalculate-on-release. Domain controllers (heating, lighting, access, and similar) need shared language without embedding instance-specific setpoints in the handbook.

## Decision

1. Add **HA-PHIL-005** (human-first operation) as a durable principle.
2. Clarify **HA-AUTO-005** so ordinary re-evaluations and automation write echoes do not cancel valid manual intervention.
3. Add **HA-AUTO-007** (honour physical and manual controls) as the enforceable standard for temporary overrides and release-via-recalculate.

Do not duplicate heating-specific setpoints in the handbook; consuming repositories keep room policy in local design docs while citing these IDs.

## Alternatives considered

- Rely only on `HA-AUTO-005` without new IDs: rejected — homeowner contract needs discoverable visitor-first and physical-control language.
- Put the full Heating V2 precedence table in the handbook: rejected — too instance-specific; violates handbook vs local overlay split (`HA-DOC-002` / migration rules).

## Consequences

- Generated assistant rules must be regenerated (`scripts/rules.py generate`).
- Consuming installs (for example HomeAssistant) re-install at the new handbook revision when approved.
- Consuming controllers cite `HA-PHIL-005` / `HA-AUTO-005` / `HA-AUTO-007` instead of inventing parallel private doctrine.

## Follow-up

- Homeowner approval of this ADR and PR.
- Regenerate + CI check; then install into each consuming repository via the normal handbook migration path.
