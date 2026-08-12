# Tooling

`rules.py` extracts normative rules directly from the handbook Markdown. It uses
only the Python standard library.

```shell
python scripts/rules.py generate
python scripts/rules.py check
```

`generate` writes the canonical JSON catalog and assistant-specific files under
`generated/`. `check` validates rule IDs and required fields, fails if an
output is missing or stale, and structurally validates
`examples/dashboard-profile.yaml` against the responsive-layout contract markers
plus `schemas/dashboard-profile.schema.json` shape. CI runs the check for every
pull request and push to `main`.

Run the parser tests with `python -m unittest discover -s tests`.

`notify_actionability.py` provides lightweight lint helpers for phone failure
Notification wording (`HA-REL-006`). Handbook tests exercise the CCTV-style
bad/good examples; consuming repositories may import `scan_failure_notification`
to reject vague multi-target templates where practical.
