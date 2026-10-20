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

## HA-ARCH-008 — Equivalent devices should behave consistently unless an explicit, justified exception exists

**Level:** Standard

Equivalent occupant-facing devices of the same class MUST present the same behaviour for the same gesture or control, wherever the hardware can support that gesture, unless an explicit justified exception is recorded in the domain behaviour specification (`HA-DOC-003`).

Historical accretion, copy-paste differences, and undocumented special cases are defects, not exceptions. Hardware that cannot emit a gesture (for example a two-button device with no hold payload) MAY be a justified exception when the domain specification records the limitation.

Dashboard-equivalent controls remain governed by `HA-UX-008`. This rule covers physical and other occupant-facing device classes, including wall switches. Device identity inventories remain governed by `HA-ARCH-007`; this rule governs interaction behaviour, not merely identity.

**Why:** House-wide predictability fails when equivalent controls mean different things in different rooms without a labelled reason.

**Verify:** Domain specifications list shared behaviour and justified exceptions separately; occupant-facing device-class changes either match the shared contract or cite a recorded exception; generated assistant instructions include `HA-ARCH-008`.
