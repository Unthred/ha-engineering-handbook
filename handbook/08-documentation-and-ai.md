# Documentation and AI assistants

## HA-DOC-001 — Document operational intent

**Level:** Standard

Documentation MUST explain purpose, dependencies, expected behaviour, fallback, and verification for important systems.

## HA-DOC-002 — Keep the handbook authoritative

**Level:** Standard

Assistant-specific instruction files MUST be generated from handbook rules. Conflicts are resolved in favour of the handbook.

## HA-AI-001 — Inspect before editing

**Level:** Standard

An AI assistant MUST inspect relevant files, conventions, dependencies, and current state before proposing or applying changes.

## HA-AI-002 — Never invent entity IDs

**Level:** Standard

An assistant MUST obtain entity, device, area, service, and integration identifiers from the actual system or user-provided configuration.

## HA-AI-003 — State assumptions and risk

**Level:** Standard

When facts cannot be verified, an assistant MUST identify assumptions. Consequential or destructive actions require explicit scope and a recovery path.

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
- required pull-request CI for the exact head SHA green, or an evidenced
  external blocker recorded (`HA-AI-007`)
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

## HA-AI-007 — Own pull-request CI through green or evidenced blocker

**Level:** Standard

**Scope:** This standard applies to **every repository** that installs this
handbook. It is not Home Assistant-specific. A consuming project MAY add a
local overlay that names its required check IDs or `gh` helpers; that overlay
MUST NOT weaken, replace, or substitute for this rule. Installing only a
project-local CI-ownership note without the generated handbook rule is
**not** compliance.

An agent that creates or updates a pull request MUST retain ownership of
required checks for the **exact pushed head SHA** through a **terminal
result**: success for every required check, or a clearly evidenced external
blocker reported with URLs and inspected evidence. Ownership includes
monitoring, failure inspection, repair of failures caused by the agent’s
changes, re-push, and re-check of the new head.

### Forbidden handoff (the defect this rule forbids)

The unacceptable behaviour is **not** merely that CI failed. It is that the
agent pushed a pull request, failed to retain ownership of its checks, and
handed the work back while the latest head was **failing** or **unverified**.

The following are forbidden as completed handoffs after an agent push:

- “CI should pass,” “checks started,” “pending at last check,” or equivalent
- reporting an older SHA’s green result while a newer head remains unmonitored
- leaving required checks red or pending and asking the human to watch them
- treating a local parse, config reload, or workflow trigger as CI completion

### After every push

1. Record the pushed commit SHA.
2. Confirm the pull-request head matches that SHA.
3. Wait for required checks to appear for that SHA (not a superseded run).
4. Monitor those checks to a terminal state (success, failure, cancelled, or
   timed-out).
5. If a GitHub Actions check fails:
   - retrieve the job log and annotations with `gh` (for example `gh pr checks`,
     `gh run view`, and failed-job logs)
   - identify the failing command and root cause
   - implement the smallest correct fix (or prove the failure is unrelated /
     external)
   - run the closest local equivalent where practical
   - push the correction
   - restart monitoring against the **new** head SHA
6. If a check stays pending for an unusually long time, inspect the workflow or
   run instead of silently abandoning it.
7. If a check is cancelled or superseded, follow the newest head SHA.
8. If an external check fails, report its URL and evidence; do not pretend its
   logs were inspected.
9. Never merge unless the human separately authorises merging.

### Boundaries

- Do not blindly re-run a deterministic failing workflow without changing
  anything. One re-run is acceptable only when evidence indicates infrastructure
  or transient failure.
- Do not modify application behaviour merely to appease a broken test; determine
  which is wrong.
- Do not weaken, skip, or disable checks to make the pull request green.
- Do not add broad exclusions or `continue-on-error` to hide failures.
- Never expose secrets from Actions logs.
- If a failure appears unrelated to the pull-request diff, prove that by
  checking the base branch or a previous successful run before changing
  unrelated code.
- After three materially different attempted fixes without success, stop,
  preserve evidence, and report the blocker rather than looping indefinitely.

### Completion report (mandatory)

When handing work back after a pull-request update, the agent MUST include:

- pull-request URL
- final head SHA
- every required check and its terminal result for **that** SHA
- failing commands and root causes encountered
- fixes made
- local verification performed
- links to any remaining failed or externally blocked checks

If required checks are still pending, the agent’s work is still in progress.
Pushing code, a local parse, a Home Assistant reload, or triggering a workflow
is not completion.

**Why:** Failure emails and abandoned red or unverified CI shift recovery onto
the human. The agent that owns the push must own the checks for that push
through a terminal result.

**Verify:** After an agent push, required checks for the reported head SHA are
green, or the handoff names an evidenced external blocker with URLs and logs.
Sample invalid handoffs (“should pass”, “pending”, “older SHA was green”) are
rejected in review. Consuming installs include the generated handbook rule, not
only a local overlay.
