#!/usr/bin/env python3
"""Extract, validate, and render handbook rules without third-party packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT / "handbook"
GENERATED = ROOT / "generated"
RULE_HEADING = re.compile(r"^## (HA-([A-Z]+)-\d{3}) — (.+)$", re.MULTILINE)
LEVEL = re.compile(r"^\*\*Level:\*\* (Principle|Standard|Guideline|Example)\s*$", re.MULTILINE)
FIELD = re.compile(r"^\*\*(Why|Verify):\*\*\s*(.+)$", re.MULTILINE)
INSTALL_MANIFEST = ".ha-handbook-install.json"


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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _target_path(target: Path, value: str, errors: list[str]) -> Path | None:
    path = (target / value).resolve()
    try:
        path.relative_to(target.resolve())
    except ValueError:
        errors.append(f"path escapes target repository: {value}")
        return None
    return path


def verify_install(target: Path) -> bool:
    target = target.resolve()
    errors: list[str] = []
    manifest_path = target / INSTALL_MANIFEST
    if not manifest_path.is_file():
        print(f"Installation verification failed: missing {manifest_path}", file=sys.stderr)
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Installation verification failed: invalid manifest: {error}", file=sys.stderr)
        return False

    if manifest.get("schema_version") != 1:
        errors.append("manifest schema_version must be 1")
    revision = manifest.get("handbook_revision")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        errors.append("handbook_revision must be a full 40-character Git commit SHA")

    installed = manifest.get("installed_generated_files")
    if not isinstance(installed, list) or not installed:
        errors.append("installed_generated_files must be a non-empty list")
    else:
        generated_by_name = {
            path.relative_to(GENERATED).as_posix(): content
            for path, content in outputs(extract()).items()
        }
        for item in installed:
            if not isinstance(item, dict):
                errors.append("each installed_generated_files entry must be an object")
                continue
            source, destination = item.get("source"), item.get("destination")
            if source not in generated_by_name or not isinstance(destination, str):
                errors.append(f"invalid generated-file mapping: {item!r}")
                continue
            path = _target_path(target, destination, errors)
            if path is None or not path.is_file():
                errors.append(f"installed generated file missing: {destination}")
            elif path.read_text(encoding="utf-8") != generated_by_name[source]:
                errors.append(f"installed generated file differs from handbook output: {destination}")

    roots = manifest.get("workspace_roots")
    if not isinstance(roots, list) or not roots:
        errors.append("workspace_roots must be a non-empty list")
    else:
        for value in roots:
            if not isinstance(value, str):
                errors.append("workspace root paths must be strings")
                continue
            path = _target_path(target, value, errors)
            if path is None or not path.is_dir():
                errors.append(f"workspace root missing: {value}")

    overlays = manifest.get("local_overlays")
    if not isinstance(overlays, list) or not overlays:
        errors.append("local_overlays must be a non-empty list")
    else:
        for value in overlays:
            if not isinstance(value, str):
                errors.append("local overlay paths must be strings")
                continue
            path = _target_path(target, value, errors)
            if path is None or not path.exists():
                errors.append(f"local overlay missing: {value}")

    capabilities = manifest.get("required_capabilities")
    if not isinstance(capabilities, list):
        errors.append("required_capabilities must be a list")
    else:
        for item in capabilities:
            if not isinstance(item, dict) or not item.get("name") or not item.get("owner"):
                errors.append(f"capability lacks a name or owner: {item!r}")
                continue
            path_value = item.get("instruction")
            if not isinstance(path_value, str):
                errors.append(f"capability lacks an instruction path: {item.get('name')}")
                continue
            path = _target_path(target, path_value, errors)
            if path is None or not path.is_file():
                errors.append(f"capability instruction missing: {item.get('name')} -> {path_value}")

    matrix_value = manifest.get("preservation_matrix")
    if not isinstance(matrix_value, str):
        errors.append("preservation_matrix must name a JSON file")
    else:
        matrix_path = _target_path(target, matrix_value, errors)
        if matrix_path is None or not matrix_path.is_file():
            errors.append(f"preservation matrix missing: {matrix_value}")
        else:
            try:
                matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
                entries = matrix.get("entries")
                if not isinstance(entries, list) or not entries:
                    errors.append("preservation matrix entries must be a non-empty list")
                else:
                    blocked = {"weakened", "missing", "undiscoverable", "unresolved"}
                    for entry in entries:
                        status = entry.get("status") if isinstance(entry, dict) else None
                        if status in blocked or not status:
                            errors.append(f"preservation matrix has blocking entry: {entry!r}")
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"invalid preservation matrix: {error}")

    for value in manifest.get("required_assets", []):
        if not isinstance(value, str):
            errors.append("required asset paths must be strings")
            continue
        path = _target_path(target, value, errors)
        if path is None or not path.exists():
            errors.append(f"required asset missing: {value}")
        elif path.is_symlink() and not path.resolve().exists():
            errors.append(f"broken required symlink: {value}")

    try:
        tracked = subprocess.run(
            ["git", "-C", str(target), "ls-files"], check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.splitlines()
        secret_names = re.compile(r"(^|/)(\.env($|\.)|.*\.(pem|key|p12|pfx)|id_rsa|secrets\.ya?ml$)", re.I)
        for value in tracked:
            if secret_names.search(value):
                errors.append(f"tracked file has a secret-bearing filename: {value}")
    except (OSError, subprocess.CalledProcessError):
        errors.append("target must be a readable Git working tree")

    if errors:
        print("Installation verification failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return False
    digest = _sha256(manifest_path)[:12]
    print(f"Installation verified for {target} (manifest {digest}, revision {revision}).")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("generate", "check", "verify-install"))
    parser.add_argument("--target", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "verify-install":
            if args.target is None:
                parser.error("verify-install requires --target")
            return 0 if verify_install(args.target) else 1
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
