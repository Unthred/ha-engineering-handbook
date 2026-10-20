# ADR-0006: Durable AI campaign handover

- **Status:** Accepted
- **Date:** 2026-10-20
- **Decision owners:** Homeowner (campaign authorised); handbook maintainers

## Context

Campaign evidence lived in Cursor chats. ChatGPT (Overseer) could not retrieve
a complete report when the homeowner said “check handover”. Transcripts are
not durable, not hashed, and not independently fetchable.

## Decision

1. Add **HA-AI-009**: publish a GitHub-retrievable handover at campaign close.
2. Version the machine contract as protocol 1 (`schemas/ai-handover.schema.json`).
3. Keep `docs/ai/latest.json` on the consuming repo’s agreed pointer branch
   (`develop` for Home Assistant) without merging unrelated feature work.
4. Provide a Cursor `publish-handover` skill in consuming repos. Document a
   ChatGPT **reader contract**; do not claim ChatGPT installation.

## Alternatives considered

- Wiki or gist: rejected — not tied to commit SHAs or product git history.
- Merge the feature PR to publish docs: rejected — operational proof gates
  (`HA-TEST-007`+) must not be bypassed for chat convenience.
- ChatGPT-only custom GPT files: rejected — not the git SoT and not reusable
  across SquigOS / Unraid.

## Consequences

- Consuming repositories add `docs/ai/`, a publisher script, and the skill.
- Pointer updates are docs-only when the campaign branch stays unmerged.
- Handbook generate/check must include `HA-AI-009`.

## Follow-up

- Home Assistant pilot: PR #341 lighting deployment handover.
- SquigOS adoption after the HA pointer is proven retrievable.
