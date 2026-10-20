#!/usr/bin/env python3
"""Validate docs/ai/latest.json for HA-AI-009 closeout.

Exits 0 when the pointer and report exist and hashes match.
Exits 2 with HANDOVER PUBLICATION BLOCKED when they do not.
Does not call Home Assistant or change production.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai.publish_handover import PublishError, sha256_text, validate_latest  # noqa: E402

BLOCKED = "HANDOVER PUBLICATION BLOCKED"


def check(repo_root: Path) -> dict:
    latest_path = repo_root / "docs/ai/latest.json"
    if not latest_path.is_file():
        raise PublishError(f"{BLOCKED}: missing docs/ai/latest.json")
    latest = json.loads(latest_path.read_text(encoding="utf-8"))
    validate_latest(latest)
    report = repo_root / latest["report_path"]
    if not report.is_file():
        raise PublishError(f"{BLOCKED}: missing report {latest['report_path']}")
    digest = sha256_text(report.read_text(encoding="utf-8"))
    if digest != latest["report_sha256"]:
        raise PublishError(f"{BLOCKED}: report_sha256 mismatch")
    return latest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        latest = check(args.repo_root)
    except (PublishError, json.JSONDecodeError, OSError) as error:
        print(f"{BLOCKED}: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "ok": True,
                "handover_id": latest["handover_id"],
                "created_utc": latest["created_utc"],
                "report_path": latest["report_path"],
                "github_url": latest.get("github_url"),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
