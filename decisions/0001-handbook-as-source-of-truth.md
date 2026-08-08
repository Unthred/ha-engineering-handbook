# ADR-0001: Handbook as the source of truth

- **Status:** Accepted
- **Date:** 2026-08-08
- **Decision owners:** Project maintainers

## Context

Different AI assistants consume different instruction formats. Hand-maintaining each format would cause duplication, drift, and contradictory policy.

## Decision

Normative engineering rules live only in `handbook/` with stable identifiers. Assistant-specific files in `generated/` are build artifacts produced from those rules and are never edited directly.

## Alternatives considered

- Maintain each assistant's rules manually: rejected because drift is inevitable.
- Use one generic prompt only: rejected because tools have different loading and scoping mechanisms.

## Consequences

Rule extraction and generation must be deterministic and validated. Handbook changes are reviewed as policy changes; generated diffs make their downstream effects visible.
