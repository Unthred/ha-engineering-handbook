# Home Assistant Engineering Handbook

An opinionated, tool-agnostic handbook for designing, building, reviewing, and maintaining reliable Home Assistant systems.

## Purpose

Home Assistant can grow from a handful of automations into critical household infrastructure. This handbook captures the engineering principles, standards, and review criteria needed to keep that infrastructure understandable, resilient, secure, and pleasant to use.

The handbook is the source of truth. Rules for Cursor, Claude, Copilot, Windsurf, and other assistants are generated from it; they must not become independent policy.

## Structure

- `handbook/` — normative principles, standards, and guidelines
- `decisions/` — architecture decision records
- `examples/` — worked examples that demonstrate the standards
- `schemas/` — machine-readable rule and metadata schemas
- `scripts/` — validation and generation tooling
- `generated/` — generated assistant-specific rules; do not edit manually
- `.github/` — contribution templates and automated checks

The visual baseline and audit workflow live in `handbook/09-visual-design-system.md` and `handbook/10-review-and-audit.md`. Controlled installation into an existing agent workspace is defined by `handbook/11-agent-rule-migration.md`; it requires a preservation matrix and a discoverable repository-local overlay. Testing, candidate deployment, and prove-before-merge gates live in `handbook/07-testing-and-deployment.md`. Responsive dashboard acceptance (`HA-UX-016`–`018`, `HA-DESIGN-007`–`008`, `HA-TEST-016`) is an enforceable contract: copy `examples/dashboard-profile.yaml`, validate layouts against its viewport matrix in normal view, and use `examples/audit-report-template.md` for rules-based review.

After installation, copy and complete `examples/agent-install-manifest.json`,
then verify the consuming repository with `python scripts/rules.py verify-install
--target /path/to/project`. The command is safe for CI and never reads secret
values.

## Rule language

Each normative rule has a stable identifier such as `HA-ARCH-001` and a level:

- **Principle** — durable reasoning and values
- **Standard** — mandatory unless an accepted exception exists
- **Guideline** — recommended default
- **Example** — non-normative illustration

The words **MUST**, **SHOULD**, and **MAY** follow RFC 2119-style meanings.

## Status

The initial chapters establish the handbook's scope, architecture, conventions, and contribution model. Machine-readable and assistant-specific rules are generated directly from those chapters and checked in CI.

## Generate assistant rules

Python 3.10 or newer is sufficient; there are no third-party dependencies.

```shell
python scripts/rules.py generate
python scripts/rules.py check
```

See [`generated/README.md`](generated/README.md) for the output paths and installation targets.

## Licence

[MIT](LICENSE)
