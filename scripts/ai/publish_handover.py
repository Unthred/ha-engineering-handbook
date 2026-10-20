#!/usr/bin/env python3
"""Publish an immutable AI campaign handover (HA-AI-009 protocol v1)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL_VERSION = 1
HANDOVER_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[a-z0-9][a-z0-9-]{1,80}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret_id|role_id|client_secret|private_key)\s*[:=]\s*\S+"),
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]{20,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)password\s*[:=]\s*(?!['\"]?\*+|['\"]?redacted)[^\s'\"]{8,}"),
]

STATES = {
    "development": {"not_started", "in_progress", "complete", "blocked"},
    "review": {"not_started", "pass", "pass_with_nits", "fail", "blocked"},
    "deployment": {
        "not_applicable",
        "not_started",
        "candidate_deployed",
        "rolled_back",
        "blocked",
    },
    "merge": {"unmerged", "merged_develop", "merged_main", "not_applicable"},
}


class PublishError(Exception):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            if not content.endswith("\n"):
                handle.write("\n")
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def secret_scan(text: str, *, label: str) -> None:
    for pattern in SECRET_PATTERNS:
        match = pattern.search(text)
        if match:
            raise PublishError(f"secret-scan failed in {label}: pattern {pattern.pattern}")


def parse_handover_id(slug: str, when: datetime) -> str:
    slug = slug.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,80}", slug):
        raise PublishError("slug must be lowercase letters, digits, hyphen")
    return f"{when.strftime('%Y%m%dT%H%M%SZ')}-{slug}"


def should_replace_latest(existing: dict | None, candidate: dict) -> None:
    if not existing:
        return
    old = existing.get("created_utc") or ""
    new = candidate.get("created_utc") or ""
    if old > new:
        raise PublishError(
            f"refusing to replace newer latest.json ({old}) with older campaign ({new})"
        )


def required_report_headings(text: str) -> None:
    needed = [
        "## Campaign objective",
        "## Outcome",
        "## States",
        "## Tests",
        "## Independent review",
        "## Remaining risks",
        "## Recommended next Overseer action",
    ]
    missing = [h for h in needed if h not in text]
    if missing:
        raise PublishError("report missing required headings: " + ", ".join(missing))


def validate_latest(obj: dict) -> None:
    if obj.get("protocol_version") != PROTOCOL_VERSION:
        raise PublishError("protocol_version must be 1")
    if not HANDOVER_ID_RE.fullmatch(str(obj.get("handover_id", ""))):
        raise PublishError("invalid handover_id")
    if not COMMIT_RE.fullmatch(str(obj.get("source_commit", ""))):
        raise PublishError("source_commit must be a 40-char SHA")
    states = obj.get("states") or {}
    for key, allowed in STATES.items():
        if states.get(key) not in allowed:
            raise PublishError(f"invalid states.{key}")
    path = str(obj.get("report_path", ""))
    if not path.startswith("docs/ai/handovers/") or not path.endswith(".md"):
        raise PublishError("report_path must be docs/ai/handovers/*.md")
    digest = str(obj.get("report_sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise PublishError("invalid report_sha256")
    if not obj.get("github_url"):
        raise PublishError("github_url required")
    if not obj.get("recommended_next_overseer_action"):
        raise PublishError("recommended_next_overseer_action required")


def validate_evidence(repo_root: Path, evidence: list[dict]) -> None:
    for item in evidence:
        path = str(item.get("path") or "")
        if not path:
            raise PublishError("evidence entry missing path")
        if not item.get("note"):
            raise PublishError(f"evidence entry missing note: {path}")
        if path.startswith("https://") or path.startswith("http://"):
            continue
        full = repo_root / path
        if not full.is_file():
            raise PublishError(f"missing evidence: {path}")
        expected = item.get("sha256")
        if expected:
            actual = hashlib.sha256(full.read_bytes()).hexdigest()
            if actual != expected:
                raise PublishError(f"evidence hash mismatch: {path}")


def verify_source_commit(repo_root: Path, source_commit: str) -> None:
    if not (repo_root / ".git").exists():
        return
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "cat-file", "-t", source_commit],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return
    if result.returncode != 0 or result.stdout.strip() != "commit":
        raise PublishError(f"source_commit not found in this repository: {source_commit}")


def github_blob_url(repository: str, ref: str, path: str) -> str:
    return f"https://github.com/{repository}/blob/{ref}/{path}"


def github_raw_url(repository: str, ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repository}/{ref}/{path}"


def publish(
    *,
    repo_root: Path,
    report_text: str,
    slug: str,
    project: str,
    repository: str,
    source_branch: str,
    source_commit: str,
    pointer_branch: str,
    objective: str,
    outcome: str,
    states: dict[str, str],
    issues: list[str],
    pull_requests: list[str],
    tests: str,
    independent_review: str,
    production: str,
    risks: str,
    human_acceptance: str,
    recommended_next: str,
    evidence: list[dict],
    created: datetime | None = None,
    existing_latest: dict | None = None,
) -> dict:
    when = created or utc_now()
    handover_id = parse_handover_id(slug, when)
    required_report_headings(report_text)
    secret_scan(report_text, label="report")
    if not COMMIT_RE.fullmatch(source_commit):
        raise PublishError("source_commit must be a 40-char SHA")
    verify_source_commit(repo_root, source_commit)
    validate_evidence(repo_root, evidence)
    rel_path = f"docs/ai/handovers/{handover_id}.md"
    dest = repo_root / rel_path
    if dest.exists():
        raise PublishError(f"handover already exists: {rel_path}")
    digest = sha256_text(report_text if report_text.endswith("\n") else report_text + "\n")
    latest = {
        "protocol_version": PROTOCOL_VERSION,
        "handover_id": handover_id,
        "project": project,
        "repository": repository,
        "created_utc": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_branch": source_branch,
        "source_commit": source_commit,
        "pointer_branch": pointer_branch,
        "pointer_commit": None,
        "issues": issues,
        "pull_requests": pull_requests,
        "objective": objective,
        "outcome": outcome,
        "states": states,
        "report_path": rel_path,
        "report_sha256": digest,
        "github_url": github_blob_url(repository, pointer_branch, rel_path),
        "raw_url": github_raw_url(repository, pointer_branch, rel_path),
        "evidence": evidence,
        "tests": tests,
        "independent_review": independent_review,
        "production": production,
        "risks": risks,
        "human_acceptance": human_acceptance,
        "recommended_next_overseer_action": recommended_next,
    }
    validate_latest(latest)
    secret_scan(json.dumps(latest), label="latest.json")
    should_replace_latest(existing_latest, latest)
    atomic_write(dest, report_text if report_text.endswith("\n") else report_text + "\n")
    latest_path = repo_root / "docs/ai/latest.json"
    atomic_write(latest_path, json.dumps(latest, indent=2, ensure_ascii=False) + "\n")
    return latest


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--project", default="home-assistant")
    parser.add_argument("--repository", default="Unthred/HomeAssistant")
    parser.add_argument("--source-branch", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--pointer-branch", default="develop")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--development", default="complete")
    parser.add_argument("--review", default="pass_with_nits")
    parser.add_argument("--deployment", default="not_applicable")
    parser.add_argument("--merge", default="unmerged")
    parser.add_argument("--issues", default="")
    parser.add_argument("--pull-requests", default="")
    parser.add_argument("--tests", default="")
    parser.add_argument("--independent-review", default="")
    parser.add_argument("--production", default="")
    parser.add_argument("--risks", default="")
    parser.add_argument("--human-acceptance", default="")
    parser.add_argument("--recommended-next", required=True)
    parser.add_argument("--evidence-json", default="[]")
    parser.add_argument("--evidence-file", type=Path, default=None)
    args = parser.parse_args(argv)

    report_text = args.report.read_text(encoding="utf-8")
    existing = load_json(args.repo_root / "docs/ai/latest.json")
    try:
        latest = publish(
            repo_root=args.repo_root,
            report_text=report_text,
            slug=args.slug,
            project=args.project,
            repository=args.repository,
            source_branch=args.source_branch,
            source_commit=args.source_commit,
            pointer_branch=args.pointer_branch,
            objective=args.objective,
            outcome=args.outcome,
            states={
                "development": args.development,
                "review": args.review,
                "deployment": args.deployment,
                "merge": args.merge,
            },
            issues=[x for x in args.issues.split(",") if x],
            pull_requests=[x for x in args.pull_requests.split(",") if x],
            tests=args.tests,
            independent_review=args.independent_review,
            production=args.production,
            risks=args.risks,
            human_acceptance=args.human_acceptance,
            recommended_next=args.recommended_next,
            evidence=json.loads(
                args.evidence_file.read_text(encoding="utf-8")
                if args.evidence_file
                else args.evidence_json
            ),
            existing_latest=existing,
        )
    except PublishError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "handover_id": latest["handover_id"], "github_url": latest["github_url"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
