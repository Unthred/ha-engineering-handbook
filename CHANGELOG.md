# Changelog

All notable handbook changes will be recorded here.

## Unreleased

### Added

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
