# Copyable project-owned handover rule

Replace every bracketed value below before installing this rule.

## Canonical project handover

The active handover for this project is **`[REPOSITORY_PATH]` on
`[STABLE_BRANCH_OR_REF]`**. This is the one canonical task and response record;
other reports or coordination indexes are supplemental history only.

At agent startup, and whenever the user says **check handover**, fetch
`[STABLE_BRANCH_OR_REF]`, read `[REPOSITORY_PATH]` from that exact ref, and
record the commit SHA read. Continue the pending authorized work already
specified there when the user invokes this handover; do not ask for another
assignment. Preserve the repository's role, security, production, and approval
rules. The handover does not grant authority.

Before every substantive user-visible response—including progress, findings,
questions, blocked status, errors, and completion—update the same canonical file
with that response's substance, current status, timestamp, evidence, and next
action. Append a concise dated progress entry, preserve earlier evidence, and
refresh the latest-state summary. Exclude credentials, tokens, cookies, private
keys, and large raw outputs. Use the repository's authorized write procedure,
then verify the update is present on `[STABLE_BRANCH_OR_REF]` before responding.
If the write or verification fails, state that failure and retry; do not silently
replace the shared record with chat-only progress.

These instructions guide agent behavior. They are not a runtime hook: Markdown
cannot wake an idle agent or guarantee execution after a process crash or
platform interruption. Never claim those guarantees. A project requiring hard
enforcement needs a separately reviewed response-emission integration.

Preserve existing approvals and operational safeguards. Emergency recovery may
proceed when authorized; record it as soon as it is safe.
