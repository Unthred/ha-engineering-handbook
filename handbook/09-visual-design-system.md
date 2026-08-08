# Visual design system

This chapter defines the default visual language for dashboards. It is deliberately calm and operational: state is easy to scan, common actions are close, and decoration never outranks information. A household may replace theme values centrally, but component meaning and layout rules remain stable.

## Design tokens

Use Home Assistant semantic theme variables wherever possible. Do not scatter literal colours, radii, or shadows through individual cards.

| Token | Default | Use |
| --- | --- | --- |
| spacing-1 | 4 px | icon/label micro-gap |
| spacing-2 | 8 px | internal card gap |
| spacing-3 | 12 px | compact card padding |
| spacing-4 | 16 px | normal card padding and grid gap |
| spacing-6 | 24 px | section separation |
| radius-card | 12 px | cards and dialogs |
| radius-control | 10 px | buttons and compact controls |
| elevation-card | none or theme default | ordinary cards |
| elevation-overlay | theme default | dialogs and popups only |

Typography uses the Home Assistant theme font. Use the standard page title, section title, primary label, secondary label, and caption hierarchy; do not introduce arbitrary font sizes or weights. Keep labels short, sentence case, and human-readable.

Semantic colour roles are `accent`, `active`, `success`, `warning`, `critical`, `muted`, and `unavailable`. Map these roles through theme variables. State colour must be accompanied by an icon, label, or both when the distinction matters.

## Card and control language

- Prefer native Home Assistant cards and features. A custom card is acceptable only when it provides a material capability or density improvement and is listed in the consuming repository's dashboard profile.
- Use one card treatment per information level: ordinary cards are flat; overlays alone receive extra elevation.
- A room summary uses the room name, a meaningful environmental or occupancy summary, and no more than four frequent controls.
- Entity rows use the same icon and friendly-name vocabulary everywhere.
- Tap opens the most common safe action or more-info. Hold is reserved for secondary or consequential actions and must be documented in the dashboard profile.
- Do not hide essential state behind an icon-only control. Icon-only buttons require an accessible name and an icon whose meaning is already established.
- Animation is brief and functional. Avoid continuous decorative animation; respect reduced-motion preferences where supported.

## State treatment

| State | Treatment |
| --- | --- |
| Normal/off | neutral surface, normal label |
| Active/on | active icon plus semantic active colour |
| Pending | explicit progress label or spinner; control cannot imply completion |
| Success | brief confirmation; do not leave the whole dashboard green |
| Warning | warning icon, label, and semantic warning colour |
| Critical | critical icon, direct wording, and the required action |
| Unavailable | unavailable icon, `Unavailable` label, muted treatment |
| Unknown | question/unknown icon and `Unknown`; never render as off |
| Stale | last-updated context plus stale label or badge |

## Standard views

### Overview

Order content as: exceptional household status, presence and security summary, rooms, climate/energy summary, then low-priority information. Healthy diagnostics stay hidden. The first screenful must answer “is anything wrong?” and “what do I use most?”

### Room

Order content as: room header and environment, frequent controls, media or climate, covers, then sensors and diagnostics. Do not show an entity twice unless the second representation serves a different task.

### Security

Show the current armed state, open or breached entries, locks, cameras, and recent relevant events. Arming, disarming, unlocking, and opening must be hard to trigger accidentally and must clearly show pending and failed transitions.

### System status

Lead with actionable failures, then degraded dependencies, batteries, updates, backups, storage, and detailed diagnostics. Healthy rows should collapse or remain visually quiet.

## Responsive layout

- Phone: one primary column; two columns only for compact controls with adequate touch targets.
- Tablet and wall panel: two or three balanced columns; keep primary status in the upper-left reading path.
- Desktop: cap content width or use three/four purposeful columns; never stretch sparse cards across the viewport.
- Minimum interactive target is 44 by 44 CSS pixels.
- Horizontal scrolling is forbidden for primary content.
- Test light and dark themes, long labels, unavailable entities, and the smallest supported display.

## HA-DESIGN-001 — Centralise visual tokens

**Level:** Standard

Colours, spacing, radii, typography, and reusable card styling MUST be defined centrally through the theme, dashboard profile, or reusable templates rather than repeated as card-local literals.

## HA-DESIGN-002 — Prefer native components

**Level:** Guideline

Native Home Assistant cards and features SHOULD be preferred. Every custom frontend dependency must have a named benefit, documented installation source, fallback impact, and maintenance owner.

## HA-DESIGN-003 — Follow standard view hierarchy

**Level:** Standard

Overview, room, security, and system-status views MUST follow the information hierarchy in this design system unless the consuming repository documents a user-specific reason to differ.

## HA-DESIGN-004 — Keep density purposeful

**Level:** Standard

Dashboards MUST avoid both entity-dump density and decorative empty space. Each visible item needs a task, status, or navigation purpose appropriate to that view.

## HA-DESIGN-005 — Preserve accessibility

**Level:** Standard

Dashboards MUST retain readable contrast, 44 by 44 pixel touch targets, text or icon reinforcement for meaningful colour, and understandable labels for icon-only actions.

## HA-DESIGN-006 — Define interaction contracts

**Level:** Standard

Reusable components MUST document their displayed state and tap, hold, double-tap, confirmation, and navigation behaviour; undefined gestures should do nothing rather than surprise the user.
