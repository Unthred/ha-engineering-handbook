# Documentation and AI assistants

## HA-DOC-001 — Document operational intent

**Level:** Standard

Documentation MUST explain purpose, dependencies, expected behaviour, fallback, and verification for important systems.

## HA-DOC-002 — Keep the handbook authoritative

**Level:** Standard

Assistant-specific instruction files MUST be generated from handbook rules. Conflicts are resolved in favour of the handbook.

## HA-AI-001 — Inspect before editing

**Level:** Standard

An AI assistant MUST inspect relevant files, conventions, dependencies, and current state before proposing or applying changes. Claims that a needed tool, API, host, credential, or other capability is unavailable are governed by `HA-AI-008` and MUST NOT replace that inspection with an unverified limitation.

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

## HA-AI-009 — Publish a durable AI campaign handover

**Level:** Standard

At the end of an engineering campaign, an assistant MUST publish a complete,
persistent handover that another assistant can retrieve from GitHub when a
human says **check handover**. Chat transcripts are not the system of record.

### Mandatory closeout

Publication is **mandatory before** the Implementer declares completion,
parks the work, or returns control to the Overseer. This includes:

- successful work
- partially completed work
- blocked or failed work
- live investigations and acceptance testing
- tasks where no code was changed
- tasks stopped for human intervention

A failed or incomplete campaign still requires a handover. Waiting to “fix
it first” is not a reason to skip publication. If publication fails, the
assistant MUST report **HANDOVER PUBLICATION BLOCKED**, retain the evidence,
and give recovery instructions. The assistant MUST NOT silently skip
publication or claim that Overseer can retrieve a report that was not
pushed to the agreed pointer branch.

Consuming repositories MUST provide a Cursor `publish-handover` skill, a
publisher that writes immutable `docs/ai/handovers/<id>.md` and atomically
updates `docs/ai/latest.json`, and a closeout check (`scripts/ai/` in the
product repo) that validates the pointer. Generated Cursor rules MUST
include this closeout duty. Assistants MUST run the publisher as part of
normal closeout, not only when a human says “publish handover”.

This rule MUST NOT block emergency recovery: operators may still revert,
disarm, or restore from backup without waiting for a handover. The handover
is then published as soon as it is safe, recording the emergency action.

A Markdown skill alone is not sufficient enforcement. Shared generated
Cursor rules, closeout-check tests, and repository docs MUST state the
duty. Cursor cannot intercept end-of-chat; remaining gaps are agent
compliance and Overseer retrieval checks.

The machine contract is protocol version 1 in
`schemas/ai-handover.schema.json`. The conversational reader contract is
`examples/ai-handover-reader.md`. A Cursor publishing skill named
`publish-handover` in the consuming repository MUST implement publication.
This rule does **not** install anything into ChatGPT; it defines the shared
contract ChatGPT can follow through an existing GitHub connector. Consuming
repositories in this house are typically **private**; the reader MUST use the
authenticated GitHub connector, not anonymous raw URLs.

Each handover MUST identify: protocol version; unique handover ID; project
and repository; UTC creation timestamp; source branch and exact commit;
relevant issues and PRs; campaign objective and outcome; independent
development, review, deployment, and merge states; full report path and
supporting evidence; tests, CI, and independent review; production
modifications, backups, and rollback where applicable; remaining risks,
blockers, and human acceptance; recommended next Overseer action.

Reports MUST NOT impose an arbitrary length limit. Failures and reservations
MUST be preserved. Large logs or binary evidence MAY live elsewhere with
immutable references and SHA-256 hashes. Credentials, tokens, cookies,
private keys, and secret values MUST NOT be published.

Publication MUST write an immutable uniquely named Markdown report, update
`docs/ai/latest.json` atomically, validate metadata and links, and never
overwrite a prior handover file. A newer `created_utc` on the canonical
pointer MUST NOT be silently replaced by an older campaign. If publication
fails, the assistant MUST report failure rather than claim the handover is
retrievable.

The canonical `docs/ai/latest.json` pointer MUST be discoverable from the
consuming repository’s **agreed pointer branch** (Home Assistant: `develop`;
fallback: the GitHub default branch) even when the campaign remains on an
unmerged feature branch. Assistants MUST NOT merge unrelated feature
branches solely to publish a handover. Copying the report onto a
docs-only pointer update is the allowed path.

**Why:** Overseer review was blocked when campaign evidence lived only in a
Cursor chat. A GitHub-retrievable pointer lets a human say “check handover”
and get the full report.

**Verify:** Consuming repositories have `docs/ai/latest.json`, immutable
handovers under `docs/ai/handovers/`, a `publish-handover` skill, a closeout
check, and tests for pointer freshness, secret scanning, missing evidence,
and mandatory-closeout phrasing; handbook tests assert `HA-AI-009` plus
`HANDOVER PUBLICATION BLOCKED` in generated Cursor rules.
