# AI campaign handovers

Handbook rule **HA-AI-009**. Protocol version 1.

When the homeowner says **check handover for the handbook**, ChatGPT
(Overseer) fetches this tree from GitHub.

## Canonical pointer

| Item | Value |
|---|---|
| Repository | `Unthred/ha-engineering-handbook` |
| Pointer branch | **`main`** |
| Latest pointer | [`docs/ai/latest.json`](latest.json) |
| Raw latest | https://raw.githubusercontent.com/Unthred/ha-engineering-handbook/main/docs/ai/latest.json |
| Reports | [`docs/ai/handovers/`](handovers/) |
| Schema | [`../../schemas/ai-handover.schema.json`](../../schemas/ai-handover.schema.json) |
| Reader | [`../../examples/ai-handover-reader.md`](../../examples/ai-handover-reader.md) |
| Publisher | `.cursor/skills/publish-handover/` + `scripts/ai/publish_handover.py` |

This repository is the **specification**. Product pilots (Home Assistant first)
publish their own `docs/ai/latest.json` in the product repo. Do not claim
ChatGPT is installed by this documentation.

## Commands

- `check handover` (project from conversation context)
- `check handover for Home Assistant`
- `check handover for SquigOS`
- `check handover for the handbook`
