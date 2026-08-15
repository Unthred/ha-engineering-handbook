# Changelog

All notable handbook changes will be recorded here.

## Unreleased

### Added

- `HA-AUTO-008` — treat accessibility and sensory constraints as safety
  requirements (no invented/reused default colour, brightness, or other
  sensory output; a standing documented sensitivity is not covered by a
  toggle-gated acute-episode setting defaulting to off). Note: `HA-AUTO-007`
  is reserved by open PR #16 (automation corroboration standard) and is not
  on `main` yet — this rule therefore uses `HA-AUTO-008`.
- `HA-TEST-019` — physical verification starts with the least hazardous
  target and intensity; a candidate is live to real triggers from the moment
  of reload, not from the moment of an agent-initiated test; "fired without
  error" is not evidence of a safe physical outcome
- `HA-TEST-018` — reimplemented-logic tests require parity proof (a Python/
  other-language mirror of production template/script/config logic is not
  proof the real artifact is correct; pair it with a real-artifact-executing
  test or documented parity evidence; regression tests must be shown to fail
  against the known-bad version). Note: `HA-TEST-017` is reserved elsewhere
  and is not used here.
- Extended `HA-ARCH-003` (Define ownership) — canonical physical-scope
  mapping required when multiple entities can address overlapping hardware,
  so two entities describing the same equipment cannot silently disagree
  about who is responsible for it.
- Extended `HA-AUTO-005` (Preserve user intent) — a manual-override mechanism
  must define its full lifecycle (set/renew, unchanged-while-in-progress,
  clear, ambiguity handling); clearing on "went off" must be a confirmed
  per-unit observation, not assumed from the command sent, and must fail
  closed on ambiguity.
- Extended `HA-REVIEW-005` (Preserve user-specific intent) — once the user
  settles a previously open decision, every document/test/finding in the
  same body of work that still frames it as open must be corrected in the
  same pass, not only the location the user pointed at.
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