# Examples

- `agent-install-manifest.json` declares a consuming repository's generated
  rules, workspace roots, local overlays, capabilities, preservation evidence,
  and supporting assets for `rules.py verify-install`.
- `preservation-matrix.json` is the minimum machine-readable migration evidence.
- `dashboard-profile.yaml` is the copy-and-customise responsive-layout contract
  (`HA-UX-016`–`019`, `HA-DESIGN-007`–`009`, `HA-TEST-016`), including
  `page_header.mode`; schema at `schemas/dashboard-profile.schema.json`.
- `audit-report-template.md` includes the mandatory responsive acceptance table
  and page-header checks.

Examples demonstrate how rules work together in realistic Home Assistant configurations. They are non-normative: when an example and a handbook rule differ, the handbook wins.

Each example should state its goal, assumptions, relevant rule IDs, configuration, verification steps, and failure behaviour.
