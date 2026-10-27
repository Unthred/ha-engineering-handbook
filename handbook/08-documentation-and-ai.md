# Documentation and AI assistants

## HA-DOC-001 — Document operational intent

**Level:** Standard

Documentation MUST explain purpose, dependencies, expected behaviour, fallback, and verification for important systems.

## HA-DOC-002 — Keep the handbook authoritative

**Level:** Standard

Assistant-specific instruction files MUST be generated from handbook rules. Conflicts are resolved in favour of the handbook.

## HA-DOC-003 — Maintain and consult domain behaviour specifications

**Level:** Standard

An Implementer MUST maintain and consult domain behaviour specifications in the consuming Home Assistant repository before changing occupant-facing behaviour. Shared handbook rules own the obligation; instance-specific behaviour tables MUST remain in the product repository, not this handbook (`HA-DOC-002`, ADR-0005, ADR-0007).

Production YAML, live entity state, and audit notes that equate “intended” with “what the current files do” are evidence of current implementation. They MUST NOT be treated as the intended specification unless a specification requirement records that alignment with confirmation provenance.

Each individual requirement in a domain specification MUST have a status of confirmed, proposed, or unknown, and MUST record confirmation provenance (who confirmed it, which artefact records the confirmation, or why the status is not confirmed).

When no relevant specification exists, the Implementer MUST record a documented specification gap and obtain an explicit review decision before treating current YAML as intended occupant-facing behaviour. Missing specifications MUST NOT unconditionally block urgent repairs: an urgent repair MAY proceed when that review decision records the gap and the repair scope.

Do not invent specifications for domains that have not been confirmed. A recorded gap is preferable to a fabricated contract.

**Why:** Occupant-facing behaviour drifted because Implementers inferred intent from YAML and room-by-room history; equivalent devices then diverged without a labelled exception.

**Verify:** Occupant-facing change records cite the domain specification or a recorded gap plus review decision; each requirement has status and provenance; generated assistant instructions include `HA-DOC-003`; handbook tests assert the rule ID, status vocabulary, evidence-not-spec language, and urgent-repair exception.

## HA-AI-001 — Inspect before editing

**Level:** Standard

An AI assistant MUST inspect relevant files, conventions, dependencies, current state, and — when the change is occupant-facing — the relevant domain behaviour specification (`HA-DOC-003`) before proposing or applying changes. If no specification exists, the assistant MUST record a specification gap rather than inferring intent solely from production YAML. Claims that a needed tool, API, host, credential, or other capability is unavailable are governed by `HA-AI-008` and MUST NOT replace that inspection with an unverified limitation.

## HA-AI-002 — Never invent entity IDs

**Level:** Standard

An assistant MUST obtain entity, device, area, service, and integration identifiers from the actual system or user-provided configuration.

## HA-AI-003 — State assumptions and risk

**Level:** Standard

When facts cannot be verified, an assistant MUST identify assumptions. Consequential or destructive actions require explicit scope and a recovery path. An assumption about the assistant’s environment or capabilities MUST remain labelled as an assumption (`HA-AI-003`) and MUST NOT be restated as a categorical unavailability claim without the evidence required by `HA-AI-008`.

## HA-AI-004 — Preserve unrelated work

**Level:** Standard

An assistant MUST keep changes focused and must not overwrite, reformat, or remove unrelated user changes.

## HA-AI-005 — Check references after structural changes

**Level:** Standard

After moving, renaming, replacing, or removing an instruction, skill, script, file, entity, or reusable dashboard object, an assistant MUST search for and validate inbound references, discovery pointers, and documented invocation paths.

## HA-AI-006 — Finish, close, or formally park before starting another implementation

**Level:** Standard

An assistant MUST treat **one active implementation task per agent and
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
- a GitHub-retrievable campaign handover (`HA-AI-009`) when the work is an
  engineering campaign that Overseer may later **check handover**

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

**Why:** Unfinished implementation left behind as open issues, stale pull
requests, dirty worktrees, or unclear production state causes silent loss of
work and unsafe handoffs.

**Verify:** Active-task inventory shows at most one implementation; completed
tasks have accurate issue/PR/closeout records; parked tasks have a complete
parking record; transition checks appear before a second implementation starts.

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

**Level:** Standard

**Principle.** Claims about the assistant’s environment or capabilities are
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

**Why:** Invented capability limits stop useful work, hide real defects
(credential, hook, or classifier issues), and teach humans to distrust
assistant status reports. The Home Assistant “API blocked” incident was a
tooling false block that had not been tested.

**Verify:** Capability-unavailability statements in assistant output cite a
probe that was attempted; generated assistant instructions include
`HA-AI-008` and the evidence requirement; handbook tests assert the rule ID,
level, and key normative phrases in `rules.json`, Cursor rules, AGENTS.md,
and CLAUDE.md.

## HA-AI-009 — Maintain one canonical project handover

**Level:** Standard

Each adopting project MUST designate exactly one canonical handover file and
its agreed stable repository/ref in instructions loaded by the Implementer and
reader. A project-specific file on the project repository's stable working
branch SHOULD be used; a central dispatcher MUST NOT replace per-project task
records.

At task startup, and whenever a human says **check handover**, the assistant
MUST fetch the agreed ref and read that exact file before selecting or reporting
work. It MUST continue the pending authorized work recorded there when the
current request invokes that handover, and MUST preserve project, role,
security, production, and approval boundaries. A handover records authority; it
does not grant authority.

Before each substantive user-visible response during the campaign—including
progress, findings, questions, blocked status, errors, and completion—the
assistant MUST update the same canonical file with the response's substance,
current status, timestamp, evidence, and next action. Progress history MUST be
preserved (for example, append dated entries and refresh a short latest-state
section). Credentials, secret values, cookies, tokens, and private keys MUST
NOT be recorded. The assistant MUST verify that the update reached the agreed
ref before claiming that response was mirrored; on failure it MUST state the
write failure and retry rather than silently substituting chat-only progress.

An immutable report archive MAY supplement the canonical file when a project
or operator requires it. Such an archive MUST NOT dispatch work, supersede the
active file, or require a second report for each progress response. Existing
archives and their schemas MAY be retained as historical records.

These repository instructions guide agent behavior but are not, by themselves,
a runtime interceptor. Markdown rules cannot wake an idle agent or guarantee
execution after a process crash or platform interruption. Implementations MUST
NOT claim those guarantees. If hard enforcement is required, it needs a
separately reviewed runtime hook integrated with response emission and a
fail-safe recovery path; that mechanism is outside this rule.

This rule MUST NOT block emergency recovery: an authorized safety action may
proceed without waiting for a handover write, which MUST be recorded as soon as
it is safe. Reports MUST preserve failures and reservations, link bounded
evidence where useful, and state remaining risks honestly.

The generic copyable rule is `examples/canonical-agent-handover-rule.md`.
`examples/ai-handover-reader.md` describes the GitHub reader pattern for
HomeAssistant's private repository; readers MUST use an authorized connector
or checkout, not anonymous raw URLs. Legacy archive metadata and publisher
schemas remain available for historical reports, not active dispatch.

**Why:** Work and important evidence were lost when instructions pointed at
different handovers or when progress lived only in chat. One stable,
project-owned file lets the Implementer and Overseer resume from the same
verified state without creating a central dispatcher.

**Verify:** Each consuming repository's normal startup path names its canonical
file/ref; a dry-run confirms the assistant can fetch/read it; a harmless
response is written and the resulting ref is inspected. Tests assert the
required path, write-through duty, secret exclusion, authorization boundary,
and explicit limitation that Markdown cannot wake or intercept an agent.
