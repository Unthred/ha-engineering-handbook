# ADR-0003: Work-in-progress discipline for assistants

- **Status:** Accepted
- **Date:** 2026-08-09
- **Decision owners:** Installation maintainers consuming this handbook

## Context

The handbook already constrains production mutation, secrets, and proof-before-
merge, but did not sufficiently constrain **unfinished work**. Assistants could
leave open issues, pull requests, branches, worktrees, evidence, documentation
gaps, or unclear operational state while starting an unrelated implementation.
“Code merged” was easy to confuse with “task complete.”

## Decision

Normative rule `HA-AI-006` requires:

1. One active implementation task per agent and workspace by default.
2. A full definition of done covering implementation, verification, docs,
   issues, PRs, cleanup inventory, and reporting.
3. Formal parking with a complete resumption record when switching is necessary.
4. Explicit interruption exceptions (human reprioritization, emergency,
   blocked dependency, withheld authorization, unsafe/wasteful continuation).
5. Transition checks before starting the next implementation.

Parking and deferred cleanup inventory do **not** authorize destructive cleanup
or unauthorized resumption of deferred work.

## Consequences

- Generated assistant guidance gains an enforceable WIP gate.
- Installations update local workflow checklists to cite `HA-AI-006`.
- Rule count increases by one (for example 89 → 90 when installed from the
  previous production-proof revision).
