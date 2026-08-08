<!-- GENERATED FILE: edit handbook sources, then run python scripts/rules.py generate -->
# Home Assistant engineering rules

Follow these project instructions for all Home Assistant work.

## HA-PHIL-001 — The home must remain operable

**Principle.** Essential functions MUST retain a simple manual path when Home Assistant, the network, or an integration is unavailable.

## HA-PHIL-002 — Prefer local control

**Standard.** Local, documented interfaces SHOULD be preferred over cloud-only dependencies, especially for lighting, heating, access, safety, and accessibility.

## HA-PHIL-003 — Automate outcomes, not surprises

**Principle.** Behaviour MUST be predictable to occupants. Context-aware behaviour needs clear boundaries, sensible defaults, and an obvious override.

## HA-PHIL-004 — Complexity must earn its keep

**Guideline.** Choose the simplest design that meets reliability and usability needs. Every helper, template, dependency, and abstraction creates maintenance cost.

## HA-ARCH-001 — Separate concerns

**Standard.** Inputs, decision logic, and actions SHOULD be distinguishable. Reusable behaviour belongs in scripts; reusable calculations belong in helpers or template entities.

## HA-ARCH-002 — Use stable interfaces

**Standard.** Automations MUST depend on stable entity semantics rather than device IDs or transient implementation details when an entity or helper can express the intent.

## HA-ARCH-003 — Define ownership

**Standard.** Each behaviour MUST have one authoritative owner. Avoid overlapping automations that compete to control the same outcome without an explicit arbitration design.

## HA-ARCH-004 — Design for degraded operation

**Standard.** Critical flows MUST define what happens when a sensor is unavailable, data is stale, a service call fails, or Home Assistant restarts mid-flow.

## HA-ARCH-005 — Minimise hidden coupling

**Guideline.** Dependencies between packages, helpers, scripts, dashboards, and external systems SHOULD be documented close to the controlling logic.

## HA-YAML-001 — Name by purpose

**Standard.** IDs and aliases MUST describe intent, not merely location or implementation. Prefer `bedroom_blackout_close` to `blind_automation_2`.

## HA-YAML-002 — Use consistent identifiers

**Standard.** Use lowercase `snake_case` for YAML IDs and helper names. Entity-friendly display names MAY use natural language.

## HA-YAML-003 — Optimise for review

**Guideline.** Keep YAML explicit, consistently formatted, and locally understandable. Avoid clever templates where a straightforward condition or helper is clearer.

## HA-YAML-004 — Explain the reason

**Standard.** Comments SHOULD document constraints, unusual device behaviour, or rationale. Do not narrate syntax that the YAML already makes obvious.

## HA-YAML-005 — Avoid copied constants

**Guideline.** Values that represent household policy or are reused across behaviours SHOULD live in an appropriately named helper or shared variable.

## HA-AUTO-001 — Define trigger semantics

**Standard.** Every automation MUST make clear whether it responds to an edge, a sustained state, a schedule, or an event. Restart behaviour and initial state must be considered.

## HA-AUTO-002 — Make execution mode deliberate

**Standard.** Choose `single`, `restart`, `queued`, or `parallel` based on concurrency semantics; do not accept the default accidentally.

## HA-AUTO-003 — Guard unsafe and noisy actions

**Standard.** Actions that unlock, open, heat, notify repeatedly, or affect security MUST have explicit preconditions and rate limits where appropriate.

## HA-AUTO-004 — Make retries bounded

**Standard.** Retries MUST have a limit, delay, and observable failure outcome. Infinite retry loops are forbidden.

## HA-AUTO-005 — Preserve user intent

**Principle.** Manual intervention SHOULD win for a documented period or until a clear reset condition. An automation must not immediately undo an occupant's action.

## HA-AUTO-006 — Use traceable structure

**Guideline.** Give triggers IDs, use descriptive aliases for branches and actions, and keep traces useful enough to explain why a decision occurred.

## HA-UX-001 — Design around tasks

**Principle.** A dashboard SHOULD prioritise what an occupant needs to understand or do, not expose every available entity.

## HA-UX-002 — Show state before control

**Standard.** Controls MUST communicate the current state, pending transitions, unavailable states, and important consequences.

## HA-UX-003 — Keep common actions close

**Guideline.** Frequent actions SHOULD require minimal navigation. Diagnostic and rare controls belong in secondary views.

## HA-UX-004 — Use consistent visual language

**Standard.** The same colour, icon, label, and interaction pattern MUST mean the same thing across dashboards.

## HA-UX-005 — Build for the actual displays

**Standard.** Views MUST be checked at their intended phone, tablet, desktop, or wall-panel sizes. Do not rely on editor preview alone.

## HA-SEC-001 — Never commit secrets

**Standard.** Passwords, tokens, private keys, webhook identifiers, precise sensitive locations, and recoverable credentials MUST NOT enter version control.

## HA-SEC-002 — Grant least privilege

**Standard.** Accounts, tokens, add-ons, integrations, and network paths MUST receive only the access needed for their function.

## HA-SEC-003 — Treat external input as untrusted

**Standard.** Webhook data, MQTT payloads, voice text, calendar content, and AI output MUST be validated before they can trigger consequential actions.

## HA-SEC-004 — Separate networks by trust

**Guideline.** IoT devices SHOULD be isolated where practical, with explicit routes to required services and no assumed internet access.

## HA-SEC-005 — Review exposure

**Standard.** Entities exposed to voice assistants, remote access, or third-party services MUST be intentionally selected and periodically reviewed.

## HA-REL-001 — Detect stale and unavailable data

**Standard.** Important decisions MUST distinguish valid readings from `unknown`, `unavailable`, implausible, or stale values.

## HA-REL-002 — Make failure visible

**Standard.** Failures affecting essential or expected behaviour MUST surface through a proportionate persistent notification, dashboard status, log, or alert.

## HA-REL-003 — Avoid alert fatigue

**Standard.** Notifications SHOULD be actionable, deduplicated, severity-appropriate, and clear about what happened and what the occupant should do.

## HA-REL-004 — Observe dependencies

**Guideline.** Critical integrations, batteries, coordinators, storage, backups, and remote endpoints SHOULD have health indicators and documented thresholds.

## HA-REL-005 — Restore safely

**Standard.** After restart or reconnection, logic MUST re-evaluate current reality rather than blindly replaying stale actions.

## HA-TEST-001 — Validate before deployment

**Standard.** Configuration MUST pass Home Assistant configuration validation and repository checks before production use.

## HA-TEST-002 — Test boundaries and failure paths

**Standard.** Tests or documented verification MUST cover unavailable inputs, threshold edges, restart behaviour, concurrent triggers, and manual overrides where relevant.

## HA-TEST-003 — Make changes reversible

**Standard.** Changes SHOULD be small enough to review and revert. Risky changes require a rollback path before deployment.

## HA-TEST-004 — Separate development from production

**Guideline.** Experimental logic SHOULD be isolated and disabled by default or tested against non-critical entities before controlling the live home.

## HA-TEST-005 — Verify the outcome

**Standard.** A successful reload is not proof of correct behaviour. Verify resulting state, traces, logs, notifications, and physical outcome as applicable.

## HA-DOC-001 — Document operational intent

**Standard.** Documentation MUST explain purpose, dependencies, expected behaviour, fallback, and verification for important systems.

## HA-DOC-002 — Keep the handbook authoritative

**Standard.** Assistant-specific instruction files MUST be generated from handbook rules. Conflicts are resolved in favour of the handbook.

## HA-AI-001 — Inspect before editing

**Standard.** An AI assistant MUST inspect relevant files, conventions, dependencies, and current state before proposing or applying changes.

## HA-AI-002 — Never invent entity IDs

**Standard.** An assistant MUST obtain entity, device, area, service, and integration identifiers from the actual system or user-provided configuration.

## HA-AI-003 — State assumptions and risk

**Standard.** When facts cannot be verified, an assistant MUST identify assumptions. Consequential or destructive actions require explicit scope and a recovery path.

## HA-AI-004 — Preserve unrelated work

**Standard.** An assistant MUST keep changes focused and must not overwrite, reformat, or remove unrelated user changes.
