<!-- GENERATED FILE: edit handbook sources, then run python scripts/rules.py generate -->
# Home Assistant engineering rules

Apply these rules when changing a Home Assistant repository.

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

## HA-ARCH-006 — Preserve registry metadata

**Standard.** Changes to entities, devices, automations, scripts, areas, or labels MUST preserve intentional area and label assignments unless the approved change explicitly updates that classification.

## HA-ARCH-007 — Own multi-surface device inventories

**Standard.** When a device class (for example cameras) appears across integrations, packages,
dashboards, notification policy, and tests, the repository MUST maintain one
canonical inventory that declares identity, classification, capabilities, and
notification policy. Downstream surfaces MUST derive from or be parity-checked
against that inventory. Hand-maintained duplicate lists without automated
parity checks are forbidden for new work.

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

**Standard.** Views MUST be validated in normal dashboard mode against the repository dashboard profile's responsive acceptance matrix (`HA-TEST-016`), including at least one phone width and one desktop width. Editor preview alone is not validation. Passing a phone check does not excuse a poor desktop layout, and passing a desktop check does not excuse a compromised phone layout.

## HA-UX-006 — Use the design system

**Standard.** Dashboard changes MUST use the tokens, components, state treatments, and layouts in `handbook/09-visual-design-system.md`; local one-off styling requires a documented reason.

## HA-UX-007 — Reserve colour for meaning

**Standard.** Colour MUST communicate state, severity, or a deliberate accent. Decorative colour must not compete with warnings, active controls, or unavailable states.

## HA-UX-008 — Keep interaction behaviour consistent

**Standard.** Equivalent controls MUST use the same tap, hold, and more-info behaviour. Consequential actions require confirmation or an interaction that makes accidental activation unlikely.

## HA-UX-009 — Prefer progressive disclosure

**Guideline.** Primary views SHOULD show current state and frequent actions; detail, history, settings, and diagnostics should be revealed through subviews or more-info rather than shown permanently.

## HA-UX-010 — Make exceptional states explicit

**Standard.** Unknown, unavailable, stale, warning, and critical states MUST be visually distinguishable without relying on colour alone and must not masquerade as a normal off state.

## HA-UX-011 — Prefer surgical dashboard edits

**Standard.** An existing dashboard MUST be changed by the smallest reliable merge. An assistant MUST NOT replace a complete view, section, or card collection when the requested outcome can be achieved by editing the affected objects.

## HA-UX-012 — Preserve storage-mode properties

**Standard.** Dashboard edits MUST preserve `grid_options`, layout metadata, and unknown storage-mode properties unless their removal is an explicit part of the approved change. A serializer's inability to interpret a property is not permission to discard it.

## HA-UX-013 — Avoid duplicate navigation

**Standard.** An assistant MUST inspect existing dashboard, view, kiosk, and browser navigation before adding back, home, or menu controls. Equivalent navigation MUST NOT be duplicated.

## HA-UX-014 — Treat storage-mode dashboards as live-first

**Standard.** Storage-mode Lovelace and other UI-managed dashboard state live on the Home
Assistant instance. Repository JSON exports are mirrors for review and backup,
not the runtime source, unless the installation has explicitly adopted a
YAML-mode dashboard.

An assistant MUST NOT assume that editing `dashboards/*.json` (or similar
exports) updates the live UI. Live repairs follow `HA-TEST-010`: backup the
live object, apply a surgical UI change, prove behaviour, then refresh the
repository mirror and verify semantic parity. Direct edits to `.storage` files
are forbidden.

## HA-UX-015 — Keep settings UIs aligned with device capability

**Standard.** Operational settings views for a device class MUST present consistent
user-facing controls for every inventoried device. Detection capability and
notification preference MUST be shown as distinct concepts. Disabled or retired
notification paths MUST NOT appear as working toggles. Issue numbers and
internal automation names MUST NOT replace the established primary control
label. Missing devices, stale labels, or capability chips that contradict the
canonical inventory are defects.

## HA-UX-016 — Mobile-first progressive enhancement

**Standard.** Dashboard work MUST begin with a coherent single-column phone hierarchy and
progressively enhance wider displays. Tablet and desktop layouts MUST use
available space deliberately without changing task order, creating substantial
structural gaps, stretching sparse content, or impairing the phone experience.
“Mobile-first” does **not** mean “mobile-only”: desktop quality is part of the
definition of done. Passing mobile validation does not excuse a poor desktop
layout, and passing desktop validation does not excuse a compromised phone
layout.

Required outcomes:

- a logical single-column mobile reading and interaction order;
- progressive enhancement at wider widths;
- preservation of information hierarchy and task order across breakpoints;
- deliberate use of additional desktop width;
- no desktop layout that simply stretches phone cards excessively;
- no desktop layout that leaves large avoidable holes or half the viewport unused;
- no desktop optimisation that damages mobile stacking or usability.

## HA-UX-017 — Deliberate responsive space use

**Standard.** At tablet and desktop widths, additional space MUST be used intentionally:
balanced columns, shared rows for shorter operational sections, deliberate
full-width analytical sections, or an explicit maximum content width. A layout
that merely scales a sparse phone composition across a wide viewport is
defective. Home Assistant Sections mechanics (`max_columns`,
`dense_section_placement`, section `column_span`, card `grid_options`) MUST be
chosen deliberately for the view (`HA-DESIGN-008`).

## HA-UX-018 — Operational UI content hygiene

**Standard.** Normal operational UI MUST help the occupant understand state or decide what to
do. Ordinary user-facing cards MUST NOT expose development or implementation
debris unless explicitly requested or necessary for safe operation. Keep the
following out of everyday operational cards:

- GitHub issue and pull-request references;
- internal entity IDs;
- internal automation, script, or helper names;
- implementation notes and debugging comments;
- model mechanics and source-code terminology;
- historical development explanations;
- caveats that belong in documentation or diagnostics.

Examples of defective everyday copy: `plant humidity excluded (#248)`,
`not sun-exposed gate/garden sensors`, or prose that describes exactly how a
calculation is implemented.

Retain useful detail in documentation, diagnostics, or an explicitly technical
view. Do **not** hide meaningful uncertainty, stale-data warnings, safety
information, data provenance needed for trust, or reasons an automation cannot
act.

## HA-UX-019 — Prefer a characterful page header with status pills

**Guideline.** Operational dashboard pages SHOULD use the standard page-header pattern from
`handbook/09-visual-design-system.md` when the repository dashboard profile
sets `page_header.mode` to `preferred` or `required`: a centred title with
personality, an optional compact subtitle only when it adds context, and a
centred wrapping row of page-relevant status pills.

This is the project's preferred visual signature, not an inflexible requirement
for every possible view. Agents SHOULD preserve or create the pattern when
working on a dashboard that already uses it or whose profile prefers it. Agents
MUST NOT mechanically add a header where it would reduce clarity, consume
excessive mobile height, or invent decorative pills with no task value.

When `page_header.mode` is `required`, absence of the pattern on covered views
is a defect unless the profile lists an explicit exception. When `optional` or
`disabled`, do not force the pattern.

Title humour MUST remain understandable, non-offensive, and appropriate.
Safety-critical or operationally urgent information MUST use clear language
rather than jokes. Pills MUST follow `HA-UX-018` content hygiene and the pill
rules in `HA-DESIGN-009`.

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

**Standard.** A candidate MUST pass Home Assistant configuration validation and applicable
repository checks before it is deployed to production. Static validation alone
MUST NOT be treated as permission to merge operational configuration into the
integration branch.

## HA-TEST-002 — Test boundaries and failure paths

**Standard.** Tests or documented verification MUST cover unavailable inputs, threshold edges,
restart behaviour, concurrent triggers, and manual overrides where relevant.

## HA-TEST-003 — Make changes reversible

**Standard.** Changes SHOULD be small enough to review and revert. Risky changes require a
documented rollback path before candidate deployment, including the exact
rollback baseline commit and the files in scope.

## HA-TEST-004 — Prefer isolation when a safe non-production path exists

**Guideline.** When an installation provides an equivalent non-production Home Assistant
environment, experimental logic SHOULD be isolated there or limited to
non-critical entities before it controls the live home.

When an installation has **no** equivalent staging or non-production Home
Assistant (an installation-specific operating constraint, not a general
recommendation for every project), production validation is intentional and
MUST follow `HA-TEST-007` through `HA-TEST-012`: exact-commit based, bounded,
reversible, selectively deployed, minimally reloaded, evidenced by entity
state, and physically confirmed when software state cannot prove real-world
behaviour.

Absence of staging MUST NOT be treated as permission to merge unproven
operational configuration, to broaden deployment scope, or to debug through
uncommitted edits on the production host.

## HA-TEST-005 — Verify the outcome

**Standard.** A successful reload is not proof of correct behaviour. Verify resulting entity
state, traces, logs, notifications, and physical outcome as applicable. Do not
treat a successful service-call HTTP response as behavioural proof.

## HA-TEST-006 — Use the narrowest safe reload

**Standard.** Deployment MUST use the narrowest supported reload or restart that applies the
change. A full Home Assistant Core restart requires a documented reason, impact
check, explicit approval, and post-restart verification when a domain or
integration reload would suffice.

## HA-TEST-007 — Prove operational candidates before merge

**Standard.** In a production-first Home Assistant repository, implementation changes that
affect Home Assistant runtime behaviour MUST NOT be merged into the branch that
represents production-proven state (commonly `develop` in
`Unthred/HomeAssistant`) until the candidate has been deployed to the real
Home Assistant instance and validated there.

Automated tests, configuration checks, review approval, and green CI are
necessary and MUST NOT be treated as substitutes for production validation.

If production deployment is not authorised, the pull request MUST remain open
or draft and unmerged. A repository-first workflow (merge before deploy) is
permitted only when the owner **explicitly** authorises that exception; it MUST
NOT be inferred from phrases such as “implement,” “create a PR,” “merge
normally,” or “do not deploy.”

The integration branch MUST be understood as containing configuration that has
been proven where proof is required — not merely configuration that passed
static validation or CI.

## HA-TEST-008 — Deploy an immutable candidate commit

**Standard.** A production candidate deployment of repository-managed configuration MUST
identify and deploy an exact Git commit. The deployment record MUST include:

- exact candidate commit
- exact rollback baseline commit
- files in scope
- deployment mechanism used
- pre-deployment production fingerprints for in-scope files
- post-copy byte-level or semantic verification against the candidate
- minimum reload plan
- expected physical effects
- behavioural test procedure
- rollback procedure
- final repository/production parity result after merge (when merging)

Preferred correction path during an authorised candidate validation session:

1. Diagnose against the live deployed implementation.
2. Apply the smallest safe live correction and prove it on production.
3. Reproduce that exact proven correction on the candidate branch (or a
   reconciliation branch from current `develop`).
4. Confirm branch content matches the proven production files (hash or
   semantic parity).
5. Only then merge.

Open-ended debugging MUST NOT leave production-managed YAML permanently
divergent from Git. Unreconciled live edits are incomplete work.

## HA-TEST-009 — Keep candidate deployment selective

**Standard.** A candidate deployment MUST copy only the in-scope files from the recorded
candidate commit (or an equivalent selective mechanism that cannot introduce
unrelated content).

If the normal deployment tool would deploy unrelated content — for example a
full-tree `rsync --delete` of an entire checkout, or a branch that is not the
candidate — the agent MUST stop and report the conflict, or use an
already-approved selective mechanism. It MUST NOT silently broaden deployment
scope, overwrite secrets, or modify `.storage` as part of a YAML candidate
deploy.

## HA-TEST-010 — Prove UI-managed state before recording it in Git

**Standard.** For storage-mode dashboards and other live UI-managed objects:

1. Inspect and back up the exact live object.
2. Make the smallest supported surgical production change (`HA-UX-011`,
   `HA-UX-012`).
3. Do not edit `.storage` files directly.
4. Test the resulting live controls and physical behaviour.
5. Export or otherwise reproduce the proven live state in the repository.
6. Verify semantic parity between live state and the repository mirror.
7. Commit and merge the proven representation.

Editing an exported dashboard JSON file in the repository does **not** update
the live storage-mode dashboard. Repository mirrors MUST NOT be imported over
live Lovelace unless that import is an explicitly approved operation with its
own backup and rollback plan.

## HA-TEST-011 — Confirm physical outcomes when state is insufficient

**Standard.** When entity state, traces, or logs cannot prove the real-world outcome (for
example visible light level, sound, motion, or appliance behaviour), the agent
MUST obtain user confirmation of the physical result before treating the
candidate as proven. Physical tests MUST be bounded, reversible where
practical, and limited to the devices in scope.

Natural validations that require bedtime, weather progression, or other
physical/time events MAY remain explicitly pending after safe deployment and
immediate production checks pass — but the immediate checks MUST pass before
merge. A task MUST NOT be called production-proven merely because it merged.

## HA-TEST-012 — Verify parity after merge

**Standard.** After merging a proven operational candidate, the agent MUST verify that the
integration branch contains the proven change and that production still matches
the in-scope proven content (byte or semantic parity). Merge MUST NOT silently
trigger an additional production deploy unless that deploy is separately
approved.

## HA-TEST-013 — Scoped exceptions to production proof

**Standard.** The production-proof-before-merge requirement (`HA-TEST-007`) MAY be skipped
only for changes that do not depend on Home Assistant runtime behaviour or
physical hardware, such as:

- documentation-only changes
- CI or tooling-only changes
- agent-rule / handbook install updates that cannot affect Home Assistant
  runtime
- non-operational templates or examples
- tests that cannot affect production behaviour

Runtime configuration, dashboards, automations, scripts, templates,
integrations, and hardware-facing behaviour REQUIRE production-first
validation.

The change record MUST state which exception applies and why. Ambiguous cases
MUST follow the production-proof path or ask the human.

## HA-TEST-014 — Require a change matrix for multi-surface device work

**Standard.** Issues and pull requests that add or change cameras (or similarly multi-surface
devices) MUST include a change matrix listing each affected surface — inventory,
integration/config, entities/helpers, automations/scripts, settings UI,
other dashboards, documentation, tests/validators, and production verification —
and mark each as changed or verified unchanged. Automated parity checks for the
canonical inventory MUST pass before merge. Validators MUST NOT operate physical
devices or send notifications.

## HA-TEST-015 — Refuse merge-before-deploy prompt conflicts

**Standard.** If instructions simultaneously require merging operational Home Assistant
configuration into the production-proven branch and forbid or withhold
production deployment, the assistant MUST STOP and report the workflow conflict
rather than merging. Generic instructions to “merge normally,” “open a PR and
merge when green,” or “CI is enough” MUST NOT override `HA-TEST-007`.

Before merging operational configuration, record evidence of:

1. deployment authorisation (or an explicit owner exception under
   `HA-TEST-013`);
2. backup or rollback readiness;
3. deployed candidate identity/hash;
4. immediate production validation results;
5. pending natural validations (if any);
6. production-to-branch reconciliation (hashes or semantic parity);
7. owner-authorised exception text, if applicable.

Absence of that gate evidence means the PR MUST stay unmerged.

## HA-TEST-016 — Visual breakpoint verification

**Standard.** Material dashboard layout or presentation changes MUST be visually verified in
**normal dashboard mode** against the consuming repository's responsive
acceptance matrix (defaults in `handbook/09-visual-design-system.md` and
`examples/dashboard-profile.yaml`). “Checked desktop” without evidence is not
sufficient.

The validation report MUST state:

- the actual viewport widths checked;
- whether normal dashboard mode was used (not editor-only);
- layout and reading order at each width;
- any clipping, overflow, excessive gaps, or awkward spans;
- whether conditional states were tested;
- who performed visual confirmation.

Editor preview, valid JSON/YAML, a successful Lovelace save, and inspection of
storage data are **not** proof of acceptable visual output. If the agent cannot
inspect the authenticated Home Assistant frontend, it MUST obtain human visual
confirmation before merging any material dashboard layout or presentation
change.

Automated linting and rule generation MAY enforce that the responsive contract
exists and propagates; they MUST NOT be treated as substitutes for visual
acceptance.

## HA-DOC-001 — Document operational intent

**Standard.** Documentation MUST explain purpose, dependencies, expected behaviour, fallback, and verification for important systems.

## HA-DOC-002 — Keep the handbook authoritative

**Standard.** Assistant-specific instruction files MUST be generated from handbook rules. Conflicts are resolved in favour of the handbook.

## HA-AI-001 — Inspect before editing

**Standard.** An AI assistant MUST inspect relevant files, conventions, dependencies, and current state before proposing or applying changes. Claims that a needed tool, API, host, credential, or other capability is unavailable are governed by `HA-AI-008` and MUST NOT replace that inspection with an unverified limitation.

## HA-AI-002 — Never invent entity IDs

**Standard.** An assistant MUST obtain entity, device, area, service, and integration identifiers from the actual system or user-provided configuration.

## HA-AI-003 — State assumptions and risk

**Standard.** When facts cannot be verified, an assistant MUST identify assumptions. Consequential or destructive actions require explicit scope and a recovery path. An assumption about the assistant’s environment or capabilities MUST remain labelled as an assumption (`HA-AI-003`) and MUST NOT be restated as a categorical unavailability claim without the evidence required by `HA-AI-008`.

## HA-AI-004 — Preserve unrelated work

**Standard.** An assistant MUST keep changes focused and must not overwrite, reformat, or remove unrelated user changes.

## HA-AI-005 — Check references after structural changes

**Standard.** After moving, renaming, replacing, or removing an instruction, skill, script, file, entity, or reusable dashboard object, an assistant MUST search for and validate inbound references, discovery pointers, and documented invocation paths.

## HA-AI-006 — Finish, close, or formally park before starting another implementation

**Standard.** An assistant MUST treat **one active implementation task per agent and
workspace** as the default. Investigation, implementation, deployment,
verification, documentation, and closeout belong to the **same task
lifecycle**. Writing code or opening a pull request MUST NOT be treated as
task completion when deployment, verification, documentation, issue cleanup,
or an accurate operational record remains outstanding.

**“Merged” is not a synonym for “complete”** when required proof, documentation,
issue closure, cleanup inventory, or parity checks remain undone
(`HA-TEST-007`–`HA-TEST-012` still govern operational merge gates).

A large feature MAY contain explicitly documented subtasks. Labelling work a
“subtask” MUST NOT be used to evade the one-active-implementation limit or to
start unrelated implementation in the same workspace.

### Definition of done

Before declaring a task complete, the assistant MUST reconcile, where
applicable:

- requested implementation and success criteria
- tests and verification (including production or physical proof when
  authorized and required)
- repository state and changelog / durable documentation
- issue status (completed, duplicate, superseded, or separately recorded
  follow-up)
- pull request status and review threads
- branch and worktree status
- temporary evidence and fixtures (retain vs disposable)
- known defects and deliberately recorded remaining work
- rollback or recovery information
- a final report to the human that matches repository and operational reality

A task MAY be called complete only when its success criteria are satisfied,
repository and operational reality agree, related issues accurately reflect
the result, superseded attempts are clearly identified, remaining work is
absent or separately and deliberately recorded, and cleanup has been completed
or explicitly listed as **safe deferred cleanup**.

### Formal parking

When a task cannot reasonably be completed before switching, the assistant
MUST create a **formal parking record** before starting another
implementation. A vague note such as “come back later” is **not** a valid
parked state. Labelling unfinished work “parked” without this record is
forbidden.

The parking record MUST include:

- task and scope
- current status
- completed work
- remaining work
- exact blocker or reason for pausing
- last known-good commit, pull request, deployment, or production state
- tests and verification already performed
- outstanding authorization needed
- open issues, pull requests, branches, and worktrees
- uncommitted or unpublished changes
- temporary evidence and its location
- known risks
- cleanup status
- exact next action and resumption point
- conditions that must be rechecked because they may become stale

Parking MUST preserve evidence and make safe resumption possible without
repeating the investigation or guessing what happened. Parking a deferred
task MUST NOT be treated as authorization to resume it.

### Interruptions and exceptions

Task switching is allowed only when:

- the human explicitly changes priority
- urgent safety, security, outage, or data-loss work intervenes
- an external dependency blocks useful progress
- required authorization is withheld or pending
- continuing would be unsafe or wasteful

Before switching, the interrupted task MUST still be formally parked unless
immediate emergency response makes that impossible. In that exceptional case,
the parking record MUST be created as soon as the immediate danger is
contained.

Waiting for CI, review, or human approval does **not** automatically justify
starting another implementation. The task MAY be parked when the wait is
material and its state is properly recorded.

A documentation query or small read-only check does **not** necessarily become
a competing implementation task, but it MUST NOT mutate or obscure the active
task.

### Cleanup discipline

During closeout or parking, the assistant MUST:

- close or accurately update completed and superseded issues
- resolve or record review threads
- identify merged, abandoned, and still-needed pull requests
- identify branches and worktrees safe for later removal
- distinguish disposable temporary material from evidence that must be retained
- avoid deleting branches, worktrees, or evidence without authorization where
  deletion is not already clearly authorized
- ensure closeout records truthfully distinguish completed work, deferred
  cleanup, and unresolved defects

Accurate inventory and authorized cleanup are distinct. This rule MUST NOT be
read as authorizing destructive cleanup.

### Starting the next implementation

Before beginning another implementation, the assistant MUST confirm:

- the previous task is completed or formally parked
- its repository, issue, pull request, and operational state are recorded
- no uncommitted work will be lost or mixed into the new task
- the new task has a distinct scope, branch or worktree, and authorization
  boundary
- any dependency between the tasks is explicit

If those conditions are not met, the assistant MUST close or park the previous
task first.

### Examples

**Valid complete:** Feature branch merged after required proof; issues closed or
updated to match reality; superseded attempts labelled; deferred cleanup listed
explicitly; final report given; workspace ready for a new scope.

**Valid parked:** Human reprioritizes; agent writes a parking record with known-
good commit, open PR/issue IDs, remaining steps, blockers, evidence path, and
exact resume action; then starts the new authorized implementation in a
separate worktree.

**Invalid handoff:** “Mostly done, will finish later,” with open issues, an
unmerged PR, and no parking record, while starting unrelated implementation in
the same workspace.

## HA-AI-008 — Verify capability claims with evidence before declaring unavailability

**Standard.** **Principle.** Claims about the assistant’s environment or capabilities are
**facts** and require evidence.

An assistant MUST NOT claim that a tool, API, network resource, credential,
command, integration, repository, filesystem path, service, remote host, or
other capability is unavailable, inaccessible, unsupported, blocked, missing,
or broken without first performing an appropriate **safe / non-destructive
probe** when such a probe is possible.

This rule is complementary to `HA-AI-001` (inspect before editing) and
`HA-AI-003` (label unverified assumptions). Those rules alone do not reliably
prevent invented capability limitations: `HA-AI-001` is too general, and
`HA-AI-003` only helps when the assistant recognises that it is assuming.
`HA-AI-008` is independently enforceable.

### Required behaviour

1. Attempt the simplest safe operation capable of proving or disproving the
   supposed limitation (for example a harmless authenticated GET, `which`
   / path check, read-only `gh` / API call, or existence check).
2. Distinguish clearly among outcomes:
   - not attempted
   - attempted and failed
   - authentication or authorization denied
   - configuration or credentials missing
   - network or service failure
   - capability genuinely unavailable
3. Report the **observed error or evidence**, rather than inventing a cause.
4. When safe and appropriate, try an already-available reasonable alternative
   access path (different URL, host, CLI, token file, or transport) before
   declaring the capability unusable.
5. Never convert uncertainty or an assumption into a categorical capability
   statement.
6. Treat remembered limitations, previous-session behaviour, sandbox
   expectations, documentation, and tool descriptions as **hypotheses** until
   verified against the current environment where verification is possible.
7. Re-probe capabilities when the result may be session-specific or stale
   (including after a challenge, a changed working directory, or a new shell
   / approval context).

Destructive, mutating, or production-impacting probes are **not** required
and MUST NOT be invented as “verification.” Prefer read-only checks.

### Invalid

- “HA API calls are blocked in this session,” when no Home Assistant API
  request has actually been attempted.
- “GitHub isn’t accessible from here,” without attempting the configured
  GitHub access mechanism (for example `gh`).
- “curl isn’t installed,” without checking for it.
- Inferring “network access is blocked” from an authentication failure
  (HTTP 401/403) against a reachable endpoint.

### Valid

- Attempt a harmless authenticated Home Assistant `GET /api/states/<entity>`.
  If it succeeds, use the live state.
- If it fails, report evidence such as: “I attempted
  `GET /api/states/<entity>` and received HTTP 401, so the endpoint is
  reachable but the current credentials were rejected.”
- If a first path is refused by a local command hook or policy, try a safe
  alternative already available in the environment, then report what was
  attempted and what was observed.

## HA-DESIGN-001 — Centralise visual tokens

**Standard.** Colours, spacing, radii, typography, and reusable card styling MUST be defined centrally through the theme, dashboard profile, or reusable templates rather than repeated as card-local literals.

## HA-DESIGN-002 — Prefer native components

**Guideline.** Native Home Assistant cards and features SHOULD be preferred. Every custom frontend dependency must have a named benefit, documented installation source, fallback impact, and maintenance owner.

## HA-DESIGN-003 — Follow standard view hierarchy

**Standard.** Overview, room, security, and system-status views MUST follow the information hierarchy in this design system unless the consuming repository documents a user-specific reason to differ.

## HA-DESIGN-004 — Keep density purposeful

**Standard.** Dashboards MUST avoid both entity-dump density and purposeless empty space. Each visible item needs a task, status, or navigation purpose appropriate to that view. Decorative or accidental whitespace that creates avoidable structural gaps is governed by `HA-DESIGN-007`; density packing and spans are governed by `HA-DESIGN-008`. Do not mandate dense packing universally — choose and justify the packing behaviour for the view in the dashboard profile.

## HA-DESIGN-005 — Preserve accessibility

**Standard.** Dashboards MUST retain readable contrast, 44 by 44 pixel touch targets, text or icon reinforcement for meaningful colour, and understandable labels for icon-only actions.

## HA-DESIGN-006 — Define interaction contracts

**Standard.** Reusable components MUST document their displayed state and tap, hold, double-tap, confirmation, and navigation behaviour; undefined gestures should do nothing rather than surprise the user.

## HA-DESIGN-007 — Structural layout-gap prevention

**Standard.** A dashboard layout MUST fail review when it contains avoidable structural defects, including:

- large vertical or horizontal holes;
- empty columns caused by section placement;
- short sections stranded beside substantially taller sections;
- unused desktop width without a deliberate maximum-width design;
- inappropriate full-width cards or sections;
- sparse content stretched across excessive width;
- awkward spans caused by unsuitable grid settings;
- gaps produced by unequal section heights where dense placement or a different span would solve them.

Purposeful whitespace that separates tasks or respects a documented maximum content width is allowed. Accidental empty regions created by Sections defaults are not.

## HA-DESIGN-008 — Section span and packing behaviour

**Standard.** Home Assistant Sections layouts MUST explicitly consider `max_columns`, `dense_section_placement`, section `column_span`, card `grid_options`, unequal section heights, and mobile stacking order. A desktop layout with avoidable empty columns or substantial placement holes is defective.

Designers MUST choose and record (in the dashboard profile or change record) whether dense placement is on or off and why; which sections stay full-width; which shorter sections share a desktop row; and the expected mobile stacking order. Dense packing MUST NOT be enabled merely to silence a gap if it produces a confusing reading order.

## HA-DESIGN-009 — Page-header composition and pill behaviour

**Standard.** When a view uses the standard page-header pattern (`HA-UX-019`), the header MUST
comprise a centred characterful title, an optional compact subtitle only when
useful, and a centred wrapping collection of status pills selected for that
page’s purpose. The complete header MUST establish identity and useful context
without dominating the viewport.

Pills MUST be relevant, concise, readable on narrow phones, and explicit about
unavailable, unknown, and stale states. They MUST NOT expose implementation
debris (`HA-UX-018`), duplicate the next prominent card without purpose, or
stretch into a sparse full-viewport band on desktop. Prefer 2–5 pills; permit
fewer or none when no useful summary exists. Do not add pills for symmetry.

Title humour MUST NOT obscure the page’s function. Safety-critical or
operationally urgent facts MUST use clear language. Header layout MUST wrap
cleanly across the responsive acceptance matrix without horizontal scrolling,
clipping, tiny text, large empty gaps, or an avoidable orphaned final pill.

## HA-REVIEW-001 — Gather evidence before judging

**Standard.** An audit MUST cite the actual repository path and configuration object for every violation; assumptions and unavailable runtime evidence must be labelled explicitly.

## HA-REVIEW-002 — Separate audit from implementation

**Standard.** Reviewing a system MUST NOT silently authorise edits. Findings, proposed remediation, and applied changes are separate stages unless the user explicitly combines them.

## HA-REVIEW-003 — Report by rule ID

**Standard.** Every compliance finding MUST reference an applicable handbook rule ID, severity, evidence, impact, recommendation, validation, and rollback consideration.

## HA-REVIEW-004 — Remediate in reversible stages

**Standard.** Remediation plans MUST prioritise safety and correctness, preserve working behaviour, limit each stage to a reviewable concern, and define success and rollback before implementation.

## HA-REVIEW-005 — Preserve user-specific intent

**Principle.** An agent MUST treat documented accessibility needs, household routines, display constraints, and deliberate exceptions as design inputs rather than normalising them away.

## HA-MIGRATE-001 — Back up active instructions

**Standard.** Before an agent changes repository or workspace instructions, it MUST create a restorable backup with original relative paths, filenames, and a manifest. The backup MUST exclude secret values and MUST NOT overwrite an earlier backup.

## HA-MIGRATE-002 — Inventory capabilities, not filenames

**Standard.** A migration MUST inventory every substantive capability, restriction, workflow, safety control, skill, script dependency, and authority boundary in the previous active instruction chain. Moving or renaming a file is not evidence that its behaviour was preserved.

## HA-MIGRATE-003 — Keep shared and local authority separate

**Standard.** Generated handbook rules MUST provide shared engineering standards. Repository-specific operational knowledge MUST live in a clearly identified local overlay whose authority and conflict policy are documented.

## HA-MIGRATE-004 — Preserve secrets-manager workflows

**Standard.** If a project uses an external secrets manager, migration MUST preserve the discoverable workflow for authentication, lookup, creation, update, rotation, naming, and safe handling without copying secret values into instructions, repositories, logs, reports, or chat output.

## HA-MIGRATE-005 — Preserve operational access

**Standard.** Migration MUST preserve documented production access, deployment, validation, reload, restart, rollback, infrastructure, container, and repository-boundary procedures unless an authorised decision explicitly retires or replaces them.

## HA-MIGRATE-006 — Prove discovery from every workspace root

**Standard.** Every required rule and local capability MUST be demonstrably discoverable when the agent is opened from each supported workspace root. A parent-workspace rule, symlink, pointer, or README mention is insufficient unless the normal agent-loading path is verified.

## HA-MIGRATE-007 — Produce a preservation matrix

**Standard.** Before removing or superseding old instructions, the migration MUST map each substantive instruction to preserved verbatim, preserved equivalently, intentionally superseded by named handbook rule IDs, weakened, missing, or undiscoverable.

## HA-MIGRATE-008 — Block unresolved gaps

**Standard.** A migration MUST NOT be committed while any instruction is weakened, missing, undiscoverable, ambiguously conflicting, or dependent on an unverified loading path. The stricter rule governs security, production safety, access control, deployment, and destructive actions.

## HA-MIGRATE-009 — Validate skills and supporting assets

**Standard.** Migration MUST verify that required skills, helper scripts, templates, documentation, symlink targets, and referenced files still exist and remain invocable through their documented paths.

## HA-MIGRATE-010 — Verify generated instruction integrity

**Standard.** Installed generated instructions MUST match the output produced from the recorded handbook revision. Generated files MUST NOT be edited to hold repository-local policy.

## HA-MIGRATE-011 — Preserve unrelated workspace state

**Standard.** Rule installation MUST preserve unrelated tracked and untracked work, MUST NOT expose credentials, and MUST report the exact changed files and repository status before approval.

## HA-MIGRATE-012 — Separate installation from system changes

**Standard.** Installing or migrating agent instructions MUST NOT implicitly authorise an audit, configuration edit, deployment, commit, push, or pull request. Each later stage requires its own explicit scope or approval.

## HA-MIGRATE-013 — Make installation self-verifying

**Standard.** An installed handbook MUST provide a repeatable, non-interactive verification command which exits non-zero when generated instructions drift, required roots or overlays are absent, capabilities lack owners, preservation gaps remain, supporting assets break, or tracked secret-bearing files are detected. A migration MUST pass both the handbook verifier and any repository-local verifier before commit.
