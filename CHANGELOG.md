# Changelog

All notable handbook changes will be recorded here.

## Unreleased

### Added

- `HA-DOC-003` — maintain and consult domain behaviour specifications in the
  consuming Home Assistant repository. Production YAML is evidence, not
  automatically the intended specification. Each requirement has status
  confirmed, proposed, or unknown, with confirmation provenance. Missing
  specifications trigger a documented gap and explicit review decision; they
  MUST NOT unconditionally block urgent repairs. Instance tables stay in the
  product repository (`ADR-0007`).
- `HA-ARCH-008` — equivalent devices should behave consistently unless an
  explicit, justified exception exists in the domain specification.
- `HA-AI-009` — publish a durable AI campaign handover (`docs/ai/latest.json`
  + immutable reports) so Overseer can `check handover` from GitHub. Protocol
  v1 schema, reader contract, ADR-0006. `HA-AI-007` remains reserved (PR #14).
- `HA-AI-009` mandatory closeout — every substantive Implementer campaign
  (success, partial, fail, live acceptance, no-code, paused for a human)
  MUST publish before returning to Overseer; report
  `HANDOVER PUBLICATION BLOCKED` rather than skip. Does not block emergency
  recovery.

- Human-first control contract: `HA-PHIL-005` (human-first operation),
  `HA-AUTO-007` (honour physical and manual controls); clarify `HA-AUTO-005`
  (ordinary re-evals and write echoes must not cancel valid manual intent);
  ADR-0005
- `HA-REL-007` — treat failure paths as first-class execution (safe cleanup /
  latch restoration must not depend solely on happy-path return)
- `HA-REL-008` — keep verification from destroying availability (verifiers
  must not abort primary workflow cleanup)
- `HA-REL-009` — evidence of health for important recurring workflows
  (stranded-latch / silent-abort detection)
- `HA-AI-008` — verify capability claims with evidence before declaring
  unavailability (forbid invented “blocked / missing / inaccessible”
  statements without a safe probe; report observed evidence; distinguish
  auth vs network vs not-attempted). Complements `HA-AI-001` / `HA-AI-003`.
  Note: `HA-AI-007` is reserved by open PR #14 (CI ownership) and is not on
  `main` yet — this rule therefore uses `HA-AI-008`.
- Responsive dashboard visual contract: `HA-UX-016` (mobile-first progressive
  enhancement), `HA-UX-017` (deliberate responsive space use), `HA-UX-018`
  (operational UI content hygiene), `HA-DESIGN-007` (structural layout-gap
  prevention), `HA-DESIGN-008` (section span and packing behaviour),
  `HA-TEST-016` (visual breakpoint verification)
- Preferred page-header pattern: `HA-UX-019` (characterful title + status
  pills), `HA-DESIGN-009` (header composition and pill behaviour); profile
  `page_header.mode` (`preferred` | `required` | `optional` | `disabled`)
- ADR-0004: enforceable responsive dashboard visual contract
- Dashboard profile v2 example + `schemas/dashboard-profile.schema.json`
- Audit template responsive acceptance table and pass/fail examples
- Example native/Mushroom-shaped page-header snippet (non-normative)
- `HA-TEST-015` — refuse merge-before-deploy prompt conflicts; require recorded
  pre-merge production-proof gate evidence
- One-active-implementation work-in-progress discipline (`HA-AI-006`): finish,
  close, or formally park before starting another implementation
- ADR-0003: work-in-progress discipline for assistants
- Production-validation-before-merge lifecycle for operational configuration
  (`HA-TEST-007`–`HA-TEST-013`)
- Storage-mode / UI-managed dashboard live-first rule (`HA-UX-014`)
- ADR-0002: production proof before merge

### Changed

- Proposed one-time `HA-AI-006` exception for campaign `2026-10-25-campaign-workflow-repair-multiworkstream-delivery`: concurrent isolated packages; preserve lifecycle and all safety gates; expires at closeout.

- `HA-AI-001` / `HA-AI-003` — cross-reference `HA-AI-008` so capability
  limitations cannot silently replace inspection or labelled assumptions
- `HA-UX-005` — require profile matrix validation; phone/desktop each insufficient alone
- `HA-DESIGN-004` — purposeless empty space; cross-ref structural gap and packing rules
- Visual design system — default responsive matrix and Home Assistant Sections mechanics
- Review framework — mandatory responsive and content-hygiene inspection
- `HA-TEST-007` — explicit production-first wording: green CI is not production
  proof; “merge normally” / “do not deploy” cannot authorise merge-before-deploy
- `HA-TEST-008` — allow minimal live correction during authorised validation,
  then exact Git reconciliation before merge
- `HA-TEST-011` — pending natural validations allowed after immediate checks;
  merge alone is not “production-proven”
- `HA-TEST-013` — agent-rule installs are exceptions; runtime YAML is not
- `HA-TEST-001` — static validation gates deploy, not merge of operational config
- `HA-TEST-004` — isolation when staging exists; exact-candidate production
  proof when it does not

### Added (historical)

- Initial repository structure
- Source-of-truth and rule taxonomy
- Foundational engineering chapters
- ADR process and first architecture decision
- Machine-readable rule schema and catalog
- Dependency-free rule generator and validation workflow
- Generated instructions for Cursor, Claude, Copilot, Windsurf, and generic assistants
- Calm, semantic visual design system with standard dashboard layouts
- Repository dashboard profile and audit report templates
- Evidence-based review and staged remediation framework