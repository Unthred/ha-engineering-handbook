# AI handover reader example — “check handover”

This is the reader side of `HA-AI-009`. The project must designate its own
canonical file and stable ref in agent startup instructions. The reader fetches
that file; it does not route through a central dispatcher or require a separate
archive pointer.

## HomeAssistant coordinates

| Item | Value |
|---|---|
| Repository | `Unthred/HomeAssistant` |
| Stable ref | `develop` |
| Canonical file | `docs/ai/CURRENT_HANDOVER.md` |

When the user says **check handover for Home Assistant**, fetch the file through
the authenticated GitHub Contents API or authorized checkout at
`develop:docs/ai/CURRENT_HANDOVER.md`. Record the commit SHA read. Read the full
file, inspect only its linked relevant source, CI, review, and runtime evidence,
and report the current outcome and next action. If the file cannot be read,
state the actual access result and use only authorized alternatives; do not
reconstruct its contents from an older report, a chat transcript, or a central
coordination repository.

A product may retain `latest.json`, immutable reports, or other archives for
historical evidence. Those records do not replace or supersede the canonical
active file. A handover file is not operational permission.

Cursor cannot install instructions into ChatGPT. ChatGPT follows this example
through an already-authorized GitHub connector; private repository access must
be authenticated. Never ask the user to paste a token or repeat secret values.
