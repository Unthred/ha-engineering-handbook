---
name: publish-handover
description: >-
  Publish an immutable GitHub-retrievable AI campaign handover
  (docs/ai/handovers/* and docs/ai/latest.json). Mandatory at every
  campaign closeout (success, fail, partial, blocked, live acceptance,
  no-code, paused for a human) under HA-AI-009. Also when the user says
  publish handover or check handover (publisher side).
---

# Publish handover

Protocol: handbook `HA-AI-009` / `schemas/ai-handover.schema.json` v1.

ChatGPT is **not** installed by this skill. After a successful push, give the
human the GitHub URL and tell them to say **check handover**.

## When

Before declaring completion or returning control to Overseer. Includes
failed, partial, blocked, live-acceptance, no-code, and human-paused work.
Do not skip because a PR is still unmerged or because a defect is unfixed.
If this publisher fails, report **HANDOVER PUBLICATION BLOCKED**.

## Steps

1. Write the **full** campaign report (no length cap; keep failures).
   Required headings:
   - Campaign objective
   - Outcome
   - States
   - Tests
   - Independent review
   - Remaining risks
   - Recommended next Overseer action
2. Never include credentials, tokens, cookies, private keys, or secret values.
3. Run from the product repo root:

```bash
python3 scripts/ai/publish_handover.py \
  --report /path/to/report.md \
  --slug short-kebab-slug \
  --project handbook \
  --repository Unthred/ha-engineering-handbook \
  --pointer-branch main \
  --source-branch "$(git rev-parse --abbrev-ref HEAD)" \
  --source-commit "$(git rev-parse HEAD)" \
  --objective "..." \
  --outcome "..." \
  --development complete \
  --review pass_with_nits \
  --deployment not_applicable \
  --merge unmerged \
  --recommended-next "..."
```

If the host has no `python3`:

```bash
git cat-file -t "$SOURCE_COMMIT"
bash /boot/config/scripts/docker-run-limited.sh run --rm \
  -v "$PWD":/src -w /src python:3.12-slim-bookworm \
  python scripts/ai/publish_handover.py ...same args...
```

4. If the script prints `FAIL:`, **stop**. Do not claim the handover is live.
5. Commit `docs/ai/handovers/<id>.md` and `docs/ai/latest.json` (never overwrite
   an existing handover file).
6. Push. Pointer branch for this repository is **`main`**.
7. Return the `github_url` from the script output.

## Pointer safety

Never replace a newer `created_utc` in `docs/ai/latest.json` with an older
campaign. The publisher refuses that.

## Reader

[docs/ai/README.md](../../../docs/ai/README.md)
[examples/ai-handover-reader.md](../../../examples/ai-handover-reader.md)
