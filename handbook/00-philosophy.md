# Philosophy

## HA-PHIL-001 — The home must remain operable

**Level:** Principle

Essential functions MUST retain a simple manual path when Home Assistant, the network, or an integration is unavailable.

**Why:** Automation should improve a home, not hold it hostage.

**Verify:** For each essential function, identify the fallback and test it periodically.

## HA-PHIL-002 — Prefer local control

**Level:** Standard

Local, documented interfaces SHOULD be preferred over cloud-only dependencies, especially for lighting, heating, access, safety, and accessibility.

## HA-PHIL-003 — Automate outcomes, not surprises

**Level:** Principle

Behaviour MUST be predictable to occupants. Context-aware behaviour needs clear boundaries, sensible defaults, and an obvious override.

## HA-PHIL-004 — Complexity must earn its keep

**Level:** Guideline

Choose the simplest design that meets reliability and usability needs. Every helper, template, dependency, and abstraction creates maintenance cost.
