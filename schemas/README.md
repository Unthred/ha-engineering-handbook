# Schemas

`rule.schema.json` describes the generated rule catalog in `generated/rules.json`.
The handbook Markdown remains authoritative; the catalog is a deterministic,
machine-readable representation for tools and assistants.

`dashboard-profile.schema.json` describes the responsive-layout contract recorded
in consuming repositories (see `examples/dashboard-profile.yaml`). The example is
validated structurally by `python scripts/rules.py check` without third-party
JSON Schema libraries; consumers with `jsonschema` MAY validate a JSON encoding
of their profile against this file.
