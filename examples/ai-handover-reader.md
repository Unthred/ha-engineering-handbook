# AI handover reader contract — “check handover”

Protocol version 1. This is the **reader** side. Cursor cannot install this
into ChatGPT. ChatGPT follows it through an existing GitHub connector.

## Conversational commands

| Human says | Meaning |
|---|---|
| `check handover` | Active project from conversation context |
| `check handover for Home Assistant` | `Unthred/HomeAssistant` |
| `check handover for SquigOS` | SquigOS product repository when adopted |
| `check handover for <campaign-id>` | Specific `handover_id` under `docs/ai/handovers/` |

## Project map

| Phrase | GitHub repository | Pointer branch |
|---|---|---|
| Home Assistant / HA | `Unthred/HomeAssistant` | `develop` (fallback: default `main`) |
| Handbook | `Unthred/ha-engineering-handbook` | `main` |
| SquigOS | product repo when this protocol is adopted | documented in that repo’s `docs/ai/README.md` |

If the project is ambiguous, ask once. Do not guess.

## Retrieval

These product repositories are **private**. Anonymous
`raw.githubusercontent.com` URLs return **404**. Use the existing **GitHub
connector** (authenticated Contents API). Do not ask the homeowner to paste a
token.

1. Fetch `docs/ai/latest.json` from the pointer branch
   (`develop` for Home Assistant, `main` for the handbook):
   `GET /repos/<owner>/<repo>/contents/docs/ai/latest.json?ref=<pointer-branch>`.
2. If that 404s, try the repository default branch.
3. Parse `protocol_version` (must be `1`).
4. Resolve `repository`, `pointer_branch`, `source_branch`, `source_commit`,
   `report_path`, `github_url`, `raw_url`. `source_commit` is the **campaign**
   SHA (code/config reviewed or deployed). The Markdown report usually lives
   on the pointer branch, not at `source_commit`.
5. Fetch the **complete** Markdown report (no truncation) via Contents API:
   `GET /repos/<repository>/contents/<report_path>?ref=<pointer_branch>`.
   Browser `github_url` / `raw_url` also work when the connector is signed in.
   If those 404 and a docs-only branch is named in the report, try that ref.
   Do not treat a 404 at `source_commit` as proof the handover is missing.
6. Fetch linked evidence as needed. Verify SHA-256 when present. Evidence may
   be GitHub blob/raw URLs on an unmerged feature commit.
7. Distinguish:
   - **fresh** — pointer `created_utc` matches the report; links resolve
   - **stale** — pointer commit/branch moved or `created_utc` older than a
     newer known campaign
   - **inaccessible** — 404, permission denied, or hash mismatch
8. Analyse as Overseer. Return verdict, risks, and next action. Do not
   summarise away failures or reservations.

## Forbidden

- Treating a Cursor chat as the SoT
- Claiming the ChatGPT skill is “installed”
- Treating a missing or pre-acceptance pointer as the current campaign
  when a later `created_utc` should exist
- Merging unrelated feature branches solely to read a handover
- Publishing or echoing credentials found in evidence (redact and flag)