# Generated assistant rules

This directory contains deterministic outputs for:

- generic assistants: `AGENTS.md`
- Claude: `CLAUDE.md`
- GitHub Copilot: `.github/copilot-instructions.md`
- Cursor: `.cursor/rules/home-assistant-engineering.mdc`
- Windsurf: `.windsurfrules`
- other tooling: `rules.json`

Copy the required file to the corresponding path in a Home Assistant repository.
Do not edit generated files directly. Change the source rule in `handbook/`, then
run `python scripts/rules.py generate`.

For an existing workspace, do not replace active instructions blindly. Follow
`handbook/11-agent-rule-migration.md`: back up the current instruction chain,
preserve project-specific capabilities in a local overlay, prove discovery from
every supported workspace root, and resolve every preservation gap before commit.
