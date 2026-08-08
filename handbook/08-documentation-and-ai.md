# Documentation and AI assistants

## HA-DOC-001 — Document operational intent

**Level:** Standard

Documentation MUST explain purpose, dependencies, expected behaviour, fallback, and verification for important systems.

## HA-DOC-002 — Keep the handbook authoritative

**Level:** Standard

Assistant-specific instruction files MUST be generated from handbook rules. Conflicts are resolved in favour of the handbook.

## HA-AI-001 — Inspect before editing

**Level:** Standard

An AI assistant MUST inspect relevant files, conventions, dependencies, and current state before proposing or applying changes.

## HA-AI-002 — Never invent entity IDs

**Level:** Standard

An assistant MUST obtain entity, device, area, service, and integration identifiers from the actual system or user-provided configuration.

## HA-AI-003 — State assumptions and risk

**Level:** Standard

When facts cannot be verified, an assistant MUST identify assumptions. Consequential or destructive actions require explicit scope and a recovery path.

## HA-AI-004 — Preserve unrelated work

**Level:** Standard

An assistant MUST keep changes focused and must not overwrite, reformat, or remove unrelated user changes.
