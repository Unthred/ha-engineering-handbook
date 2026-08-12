# Home Assistant audit

## Scope and evidence

- Repository/ref:
- Home Assistant version:
- Authoritative configuration:
- UI-managed configuration not available in Git:
- Dashboard profile path (or “missing”):
- Target displays / matrix widths used:
- Lovelace mode (storage / YAML):
- Authenticated normal-view access available:
- Constraints and documented exceptions:

## Executive summary

State what is sound, the most important risks, and the recommended first stage. Do not imply runtime verification that was not performed.

## Responsive acceptance (dashboard views)

Complete for every audited dashboard view. “Responsive: yes” without this table is insufficient (`HA-TEST-016`).

| View path | Widths checked (px) | Normal mode? | Mobile order OK? | Desktop gaps/spans OK? | Conditionals checked? | Content hygiene OK? | Confirmer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

### Responsive defect checklist

- [ ] No avoidable empty columns or large holes at desktop/wide widths (`HA-DESIGN-007`)
- [ ] `max_columns`, dense placement, section spans, and `grid_options` considered (`HA-DESIGN-008`)
- [ ] Phone stack preserves task order (`HA-UX-016`)
- [ ] Desktop uses space deliberately — not stretched sparse phone cards (`HA-UX-017`)
- [ ] Not editor-only; normal view confirmed (`HA-TEST-016`)
- [ ] No issue/PR refs, entity IDs, or implementation notes in ordinary cards (`HA-UX-018`)
- [ ] Repository mirror vs live storage divergence labelled (`HA-UX-014`)
- [ ] Page header matches profile mode (`HA-UX-019`); pills relevant and compact (`HA-DESIGN-009`)
- [ ] Header wraps without clipping/overflow; desktop pills stay centred and compact
## Findings

### AUDIT-001 — Short finding title

- **Severity:** medium
- **Rule:** HA-UX-010
- **Evidence:** `dashboards/example.yaml`, card/view name
- **Current behaviour:**
- **Impact:**
- **Recommendation:**
- **Dependencies and risk:**
- **Validation:**
- **Rollback:**

### Example finding shapes

**Structural gap (fail):** Rule `HA-DESIGN-007`; evidence desktop 1280 px normal view; short section stranded beside tall graph; empty column.

**Content hygiene (fail):** Rule `HA-UX-018`; evidence card subtitle contains `(#248)`.

**Missing evidence (fail):** Rule `HA-TEST-016`; PR claims “checked desktop” with no widths or confirmer.

**Missing preferred header (fail):** Rule `HA-UX-019`; profile prefers header but view has none.

**Vague phone failure Notification (fail):** Rule `HA-REL-006` / `HA-REVIEW-006`; evidence message text “One or more switches failed… Action needed.” with no named targets, expected vs actual, or next step.

## Phone Notification checklist (when auditing alerts)

- [ ] Away-from-home question answered yes (`HA-REVIEW-006`)
- [ ] Operation, failed targets (friendly names), expected vs actual, reason, retries, next action present where applicable (`HA-REL-006`)
- [ ] Multi-target failures list only the failed subset; no “one or more” / “some devices” / bare “action needed” when specifics are known
- [ ] Successful retry suppresses the failure phone Notification

**Decorative pills (fail):** Rule `HA-DESIGN-009`; pills exist only for symmetry or include entity IDs.

## Staged remediation plan

| Stage | Scope | Findings | Success check | Rollback |
| --- | --- | --- | --- | --- |
| 1 | Safety/correctness |  |  |  |
| 2 | Structure/reuse/responsive layout |  | Matrix widths + gap-free desktop |  |
| 3 | Visual consistency / content hygiene |  |  |  |

## Decisions required

List only choices that materially change behaviour, risk, cost, or visual direction.
