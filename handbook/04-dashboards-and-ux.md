# Dashboards and UX

## HA-UX-001 — Design around tasks

**Level:** Principle

A dashboard SHOULD prioritise what an occupant needs to understand or do, not expose every available entity.

## HA-UX-002 — Show state before control

**Level:** Standard

Controls MUST communicate the current state, pending transitions, unavailable states, and important consequences.

## HA-UX-003 — Keep common actions close

**Level:** Guideline

Frequent actions SHOULD require minimal navigation. Diagnostic and rare controls belong in secondary views.

## HA-UX-004 — Use consistent visual language

**Level:** Standard

The same colour, icon, label, and interaction pattern MUST mean the same thing across dashboards.

## HA-UX-005 — Build for the actual displays

**Level:** Standard

Views MUST be checked at their intended phone, tablet, desktop, or wall-panel sizes. Do not rely on editor preview alone.

## HA-UX-006 — Use the design system

**Level:** Standard

Dashboard changes MUST use the tokens, components, state treatments, and layouts in `handbook/09-visual-design-system.md`; local one-off styling requires a documented reason.

## HA-UX-007 — Reserve colour for meaning

**Level:** Standard

Colour MUST communicate state, severity, or a deliberate accent. Decorative colour must not compete with warnings, active controls, or unavailable states.

## HA-UX-008 — Keep interaction behaviour consistent

**Level:** Standard

Equivalent controls MUST use the same tap, hold, and more-info behaviour. Consequential actions require confirmation or an interaction that makes accidental activation unlikely.

## HA-UX-009 — Prefer progressive disclosure

**Level:** Guideline

Primary views SHOULD show current state and frequent actions; detail, history, settings, and diagnostics should be revealed through subviews or more-info rather than shown permanently.

## HA-UX-010 — Make exceptional states explicit

**Level:** Standard

Unknown, unavailable, stale, warning, and critical states MUST be visually distinguishable without relying on colour alone and must not masquerade as a normal off state.
