# Architecture

## HA-ARCH-001 — Separate concerns

**Level:** Standard

Inputs, decision logic, and actions SHOULD be distinguishable. Reusable behaviour belongs in scripts; reusable calculations belong in helpers or template entities.

## HA-ARCH-002 — Use stable interfaces

**Level:** Standard

Automations MUST depend on stable entity semantics rather than device IDs or transient implementation details when an entity or helper can express the intent.

## HA-ARCH-003 — Define ownership

**Level:** Standard

Each behaviour MUST have one authoritative owner. Avoid overlapping automations that compete to control the same outcome without an explicit arbitration design.

When multiple entities can address overlapping physical scope (for example a
combined-group wrapper and its individual-member wrappers controlling the
same underlying hardware), any state that models "this equipment was just
deliberately commanded" MUST be tracked against a canonical mapping to the
finest addressable physical unit, not against whichever entity happened to
receive the command. Two entities describing the same hardware MUST NOT be
able to silently disagree about who is responsible for it, or about whether
it was just deliberately touched. A change that adds a new wrapper over
existing physical scope MUST update that canonical mapping in the same
change, not as a follow-up.

## HA-ARCH-004 — Design for degraded operation

**Level:** Standard

Critical flows MUST define what happens when a sensor is unavailable, data is stale, a service call fails, or Home Assistant restarts mid-flow.

## HA-ARCH-005 — Minimise hidden coupling

**Level:** Guideline

Dependencies between packages, helpers, scripts, dashboards, and external systems SHOULD be documented close to the controlling logic.

## HA-ARCH-006 — Preserve registry metadata

**Level:** Standard

Changes to entities, devices, automations, scripts, areas, or labels MUST preserve intentional area and label assignments unless the approved change explicitly updates that classification.

## HA-ARCH-007 — Own multi-surface device inventories

**Level:** Standard

When a device class (for example cameras) appears across integrations, packages,
dashboards, notification policy, and tests, the repository MUST maintain one
canonical inventory that declares identity, classification, capabilities, and
notification policy. Downstream surfaces MUST derive from or be parity-checked
against that inventory. Hand-maintained duplicate lists without automated
parity checks are forbidden for new work.
