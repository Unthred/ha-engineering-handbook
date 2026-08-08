#!/usr/bin/env python3
"""Extract, validate, and render handbook rules without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT / "handbook"
GENERATED = ROOT / "generated"
RULE_HEADING = re.compile(r"^## (HA-([A-Z]+)-\d{3}) — (.+)$", re.MULTILINE)
LEVEL = re.compile(r"^\*\*Level:\*\* (Principle|Standard|Guideline|Example)\s*$", re.MULTILINE)
FIELD = re.compile(r"^\*\*(Why|Verify):\*\*\s*(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    area: str
    level: str
    text: str
    source: str
    rationale: str | None = None
    verification: str | None = None


def _paragraphs(body: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]


def parse_file(path: Path) -> list[Rule]:
    content = path.read_text(encoding="utf-8")
    matches = list(RULE_HEADING.finditer(content))
    rules: list[Rule] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        body = content[match.end():end].strip()
        level_match = LEVEL.search(body)
        if not level_match:
            raise ValueError(f"{path}: {match.group(1)} has no valid Level")
        fields = {name: value.strip() for name, value in FIELD.findall(body)}
        text_parts = [
            p for p in _paragraphs(body)
            if not p.startswith("**Level:**")
            and not p.startswith("**Why:**")
            and not p.startswith("**Verify:**")
        ]
        if not text_parts:
            raise ValueError(f"{path}: {match.group(1)} has no normative text")
        rules.append(Rule(
            id=match.group(1), title=match.group(3).strip(), area=match.group(2),
            level=level_match.group(1), text="\n\n".join(text_parts),
            rationale=fields.get("Why"), verification=fields.get("Verify"),
            source=path.relative_to(ROOT).as_posix(),
        ))
    return rules


def extract() -> list[Rule]:
    rules: list[Rule] = []
    for path in sorted(HANDBOOK.glob("*.md")):
        rules.extend(parse_file(path))
    seen: dict[str, str] = {}
    for rule in rules:
        if rule.id in seen:
            raise ValueError(f"duplicate {rule.id}: {seen[rule.id]} and {rule.source}")
        seen[rule.id] = rule.source
    if not rules:
        raise ValueError("no handbook rules found")
    return rules


def render_markdown(rules: list[Rule], assistant: str) -> str:
    preambles = {
        "generic": "Apply these rules when changing a Home Assistant repository.",
        "claude": "Follow these project instructions for all Home Assistant work.",
        "copilot": "Use these instructions when suggesting Home Assistant changes.",
        "windsurf": "Follow these rules for all Home Assistant engineering work.",
    }
    lines = [
        "<!-- GENERATED FILE: edit handbook sources, then run python scripts/rules.py generate -->",
        "# Home Assistant engineering rules", "", preambles[assistant], "",
    ]
    for rule in rules:
        lines.extend([f"## {rule.id} — {rule.title}", "", f"**{rule.level}.** {rule.text}", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_cursor(rules: list[Rule]) -> str:
    body = render_markdown(rules, "generic").split("\n", 1)[1]
    return "---\ndescription: Home Assistant engineering standards\nglobs: \"**/*.{yaml,yml,md,json,jinja}\"\nalwaysApply: true\n---\n" + body


def outputs(rules: list[Rule]) -> dict[Path, str]:
    catalog = {"schema_version": 1, "rules": [asdict(rule) for rule in rules]}
    return {
        GENERATED / "rules.json": json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        GENERATED / "AGENTS.md": render_markdown(rules, "generic"),
        GENERATED / "CLAUDE.md": render_markdown(rules, "claude"),
        GENERATED / ".github/copilot-instructions.md": render_markdown(rules, "copilot"),
        GENERATED / ".cursor/rules/home-assistant-engineering.mdc": render_cursor(rules),
        GENERATED / ".windsurfrules": render_markdown(rules, "windsurf"),
    }


def generate(rules: list[Rule]) -> None:
    for path, content in outputs(rules).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def check(rules: list[Rule]) -> bool:
    stale = []
    for path, expected in outputs(rules).items():
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            stale.append(path.relative_to(ROOT).as_posix())
    if stale:
        print("Generated files are missing or stale:", file=sys.stderr)
        for path in stale:
            print(f"  - {path}", file=sys.stderr)
        print("Run: python scripts/rules.py generate", file=sys.stderr)
        return False
    print(f"Validated {len(rules)} rules; generated files are current.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("generate", "check"))
    args = parser.parse_args()
    try:
        rules = extract()
        if args.command == "generate":
            generate(rules)
            print(f"Generated {len(outputs(rules))} files from {len(rules)} rules.")
            return 0
        return 0 if check(rules) else 1
    except ValueError as error:
        print(f"Rule validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
