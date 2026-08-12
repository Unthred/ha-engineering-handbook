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

Dashboard layout is a **mobile-first progressive enhancement** contract (`HA-UX-016`, `HA-UX-017`). Phone defines the reading and task order; wider displays enhance that order without rewriting it.

### Default responsive acceptance matrix

Consuming repositories SHOULD copy and customise `examples/dashboard-profile.yaml`. Unless the profile overrides them, validate at least these default widths in **normal dashboard mode** (not editor-only):

| Target | Default validation width | Required outcome |
| --- | ---: | --- |
| Small phone | 360 px | One-column hierarchy, usable controls, no clipping |
| Typical phone | 390–430 px | Comfortable card and control sizing |
| Tablet | 768–1024 px | Intentional use of additional width |
| Desktop | 1280 px | Balanced layout without major holes |
| Wide desktop | 1440–1920 px | Purposeful columns or deliberate maximum width |

These are defaults, not unexplained universal magic numbers. A dashboard profile MAY narrow, widen, or rename targets, but MUST record the widths actually used for acceptance (`HA-TEST-016`).

### Home Assistant Sections mechanics

Home Assistant Sections layouts MUST explicitly consider `max_columns`, `dense_section_placement`, section spans, card `grid_options`, unequal section heights, and mobile stacking order. A desktop layout with avoidable empty columns or substantial placement holes is defective (`HA-DESIGN-007`, `HA-DESIGN-008`).

| Mechanism | What to decide |
| --- | --- |
| `max_columns` | How many section columns the view may occupy at desktop width |
| `dense_section_placement` | Whether shorter sections may pack into leftover horizontal space |
| Section `column_span` | Full-width analytical bands versus shared operational columns |
| Card `grid_options` | Per-card width within a section; preserve in storage-mode edits (`HA-UX-012`) |
| Full-width vs single-column sections | Which bands must remain full width on every breakpoint |
| Unequal section heights | Whether adjacent sections leave tall empty regions that denser packing or different spans would fix |
| Section order / mobile stacking | Desktop left-to-right order becomes phone top-to-bottom; order MUST remain a coherent story |
| Storage-mode preservation | Live Lovelace is authoritative; repository mirrors can drift (`HA-UX-014`) |
| Conditional cards | Editor preview can show cards that are hidden in normal view — validate both |

**When dense placement helps:** shorter status or control sections sharing a row beside a taller neighbour, reclaiming an otherwise empty column without changing task order.

**When dense placement harms:** packing that produces a confusing reading order, interleaves unrelated tasks, or makes the phone stack jump between topics unpredictably. Prefer explicit section order and justified spans over automatic packing when narrative clarity matters more than density.

Horizontal scrolling is forbidden for primary content. Minimum interactive target is 44 by 44 CSS pixels. Test light and dark themes, long labels, unavailable entities, conditional states, and the smallest supported display.

## Visual definition of done

Successful rendering alone is insufficient. A dashboard change is not complete until it has been checked for:

- correct content and interaction;
- clear information hierarchy and understandable labels;
- mobile usability and deliberate tablet/desktop layout;
- absence of avoidable structural gaps, clipping, and overflow;
- sensible section and card spans;
- correct conditional states in **normal view**;
- operational UI content hygiene (`HA-UX-018`);
- consistency with this design system.

Valid JSON/YAML, a successful Lovelace save, editor preview, and inspection of storage data are **not** proof of acceptable visual output. If the agent cannot inspect the authenticated Home Assistant frontend, human visual confirmation is required before merging any material dashboard layout or presentation change (`HA-TEST-016`).

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

Dashboards MUST avoid both entity-dump density and purposeless empty space. Each visible item needs a task, status, or navigation purpose appropriate to that view. Decorative or accidental whitespace that creates avoidable structural gaps is governed by `HA-DESIGN-007`; density packing and spans are governed by `HA-DESIGN-008`. Do not mandate dense packing universally — choose and justify the packing behaviour for the view in the dashboard profile.

## HA-DESIGN-005 — Preserve accessibility

**Level:** Standard

Dashboards MUST retain readable contrast, 44 by 44 pixel touch targets, text or icon reinforcement for meaningful colour, and understandable labels for icon-only actions.

## HA-DESIGN-006 — Define interaction contracts

**Level:** Standard

Reusable components MUST document their displayed state and tap, hold, double-tap, confirmation, and navigation behaviour; undefined gestures should do nothing rather than surprise the user.

## HA-DESIGN-007 — Structural layout-gap prevention

**Level:** Standard

A dashboard layout MUST fail review when it contains avoidable structural defects, including:

- large vertical or horizontal holes;
- empty columns caused by section placement;
- short sections stranded beside substantially taller sections;
- unused desktop width without a deliberate maximum-width design;
- inappropriate full-width cards or sections;
- sparse content stretched across excessive width;
- awkward spans caused by unsuitable grid settings;
- gaps produced by unequal section heights where dense placement or a different span would solve them.

Purposeful whitespace that separates tasks or respects a documented maximum content width is allowed. Accidental empty regions created by Sections defaults are not.

**Why:** “Avoid decorative empty space” was too weak; agents treated large placement holes as acceptable as long as cards rendered.

**Verify:** At desktop and wide-desktop matrix widths, no avoidable empty column or substantial hole remains unless the dashboard profile documents a deliberate max-width or packing exception.

## HA-DESIGN-008 — Section span and packing behaviour

**Level:** Standard

Home Assistant Sections layouts MUST explicitly consider `max_columns`, `dense_section_placement`, section `column_span`, card `grid_options`, unequal section heights, and mobile stacking order. A desktop layout with avoidable empty columns or substantial placement holes is defective.

Designers MUST choose and record (in the dashboard profile or change record) whether dense placement is on or off and why; which sections stay full-width; which shorter sections share a desktop row; and the expected mobile stacking order. Dense packing MUST NOT be enabled merely to silence a gap if it produces a confusing reading order.

**Why:** Sections defaults and indiscriminate full-width spans are a common source of desktop holes and phone-order surprises.

**Verify:** Profile or change record states packing policy and spans; normal-view phone stack matches the intended order; desktop shows justified shared rows or full-width bands without empty columns.
