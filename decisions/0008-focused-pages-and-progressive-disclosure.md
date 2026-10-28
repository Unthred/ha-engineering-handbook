# ADR-0008: Focused pages and progressive disclosure

- **Status:** Accepted
- **Date:** 2026-10-28
- **Decision owners:** Handbook maintainers; installation maintainers consuming this handbook

## Context

A household heating "settings" view was delivered that rendered correctly,
saved successfully and passed automated checks, yet put every room's
schedules, ownership, safety-gate and commissioning controls on one long page.
The occupant rejected it as unusable. Existing rules (`HA-UX-001`, `-003`,
`-009`) encouraged task focus and progressive disclosure only as principles or
guidelines, and nothing said that usability is part of "done", so an agent could
reasonably believe the work was finished.

## Decision

1. Add normative rules `HA-UX-020`–`HA-UX-024`: one focused task per page;
   separation of everyday and engineering controls; overview/detail/advanced
   navigation; one template for like items; and usability as part of done.
2. Record page-focus choices in the dashboard profile (`page_focus`).
3. Extend the review audit and the visual definition of done.
4. Keep the rules general to Home Assistant; they name no product feature.

## Consequences

Agents must split overloaded pages, keep engineering controls out of everyday
pages, and treat occupant feedback about usability as a defect. Automated checks
verify the rules exist and propagate; they do not prove a page is pleasant to
use, so human confirmation (`HA-TEST-016`) remains required.
