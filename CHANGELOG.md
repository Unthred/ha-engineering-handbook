# Changelog

All notable handbook changes will be recorded here.

## Unreleased

### Added

- Disruptive test isolation: `HA-TEST-017` (structural test-mode /
  production-incident gate; deny-by-default external alerts/sirens; prove the
  call graph; user approval before real-world alert tests; duplicate
  Notification discipline). Cross-linked from `HA-AUTO-007`.
- Disruptive automation corroboration: `HA-AUTO-007` (inferred-state actions
  need confirming evidence, confirmation/grace with deliberate-interaction
  cancel, automatic media transitions must not cancel, playback may be room
  context not permanent veto; fail-safe; non-destructive tests;
  external side-effect isolation pointer to `HA-TEST-017`);
  `HA-AUTO-003` cross-link
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