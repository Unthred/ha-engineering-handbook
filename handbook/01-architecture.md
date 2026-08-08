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
