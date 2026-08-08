# Contributing

Changes should improve the handbook as a coherent engineering system, not merely add personal preferences.

## Workflow

1. Explain the problem and intended outcome.
2. Identify affected rule IDs and chapters.
3. Add or update rationale, consequences, and examples.
4. Record a significant or difficult-to-reverse decision as an ADR.
5. Run `python scripts/rules.py generate` and `python scripts/rules.py check`.
6. Submit a focused pull request.

Normative rules require a stable ID, level, rationale, and verification method. Generated files must never be edited directly.
