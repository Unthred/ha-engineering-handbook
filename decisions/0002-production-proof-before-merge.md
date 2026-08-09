# ADR-0002: Production proof before merge for operational configuration

- **Status:** Accepted
- **Date:** 2026-08-09
- **Decision owners:** Installation maintainers consuming this handbook

## Context

Some Home Assistant installations have no equivalent staging instance. Static
validation and pull-request review are still required, but they do not prove
behaviour against real entities and hardware. Earlier handbook wording
(`HA-TEST-004`) encouraged separating development from production without
defining how to ship safely when production is the only runtime.

Ambiguity allowed agents to treat “validated in CI” or “merged to develop” as
sufficient for operational YAML, or conversely to edit production hosts outside
Git while debugging.

## Decision

For repository-managed **operational** Home Assistant configuration:

1. Open a PR and keep it unmerged until the exact candidate commit is proven.
2. Deploy that immutable candidate selectively to production.
3. Reload narrowly; restart Core only with evidence and approval.
4. Prove behaviour with entity-state evidence and physical confirmation when
   needed.
5. Merge only after proof (or an explicit `HA-TEST-013` exception).
6. Verify repository/production parity after merge.

UI/storage-managed configuration is live-first (`HA-TEST-010`, `HA-UX-014`):
prove on the instance, then record the export in Git.

Production-only testing is an **installation-specific operating constraint**,
not a universal recommendation that every Home Assistant project abandon
staging.

## Alternatives considered

- Require a staging HA for all consumers: rejected as incompatible with
  installations that have deliberately shelved staging.
- Merge after CI only, deploy later: rejected because broken operational YAML
  would land on the integration branch before real-world proof.
- Debug with uncommitted edits on the production host: rejected because it
  destroys candidate identity and rollback clarity.

## Consequences

Handbook rules `HA-TEST-007`–`HA-TEST-013` and `HA-UX-014` are normative.
Consuming repositories MUST reinstall generated assistant rules after adopting
this handbook revision. Local overlays may still describe prod-first standing
orders; they MUST NOT contradict the prove-then-merge gate for operational
configuration.
