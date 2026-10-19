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

## HA-PHIL-005 — Human-first operation

**Level:** Principle

Anyone SHOULD be able to enter the house and operate essential functions as an ordinary home, using physical controls and obvious local interfaces, without needing Home Assistant, dashboards, voice assistants, or special modes. Advanced automation remains an optional homeowner extra, subject to hardware capability.

**Why:** Guests and distracted occupants must not be blocked by opaque smart-home behaviour. Physical controls that silently reverse themselves train people not to trust the house. This complements `HA-PHIL-001` (fallback when HA is unavailable): human-first applies while automation is running.

**Verify:** For heating, lighting, access, and similar essential functions, confirm a visitor can achieve a sensible outcome from the room's physical control alone, and that automation does not immediately undo that action (`HA-AUTO-005`, `HA-AUTO-007`).
