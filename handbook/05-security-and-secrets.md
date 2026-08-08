# Security and secrets

## HA-SEC-001 — Never commit secrets

**Level:** Standard

Passwords, tokens, private keys, webhook identifiers, precise sensitive locations, and recoverable credentials MUST NOT enter version control.

## HA-SEC-002 — Grant least privilege

**Level:** Standard

Accounts, tokens, add-ons, integrations, and network paths MUST receive only the access needed for their function.

## HA-SEC-003 — Treat external input as untrusted

**Level:** Standard

Webhook data, MQTT payloads, voice text, calendar content, and AI output MUST be validated before they can trigger consequential actions.

## HA-SEC-004 — Separate networks by trust

**Level:** Guideline

IoT devices SHOULD be isolated where practical, with explicit routes to required services and no assumed internet access.

## HA-SEC-005 — Review exposure

**Level:** Standard

Entities exposed to voice assistants, remote access, or third-party services MUST be intentionally selected and periodically reviewed.
