#!/usr/bin/env python3
"""Lint helpers for actionable phone failure Notifications (HA-REL-006).

Consuming repositories MAY call ``scan_failure_notification`` on candidate
message templates. The handbook tests use the same helpers against bad/good
examples so vague multi-target wording is caught where practical.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# Phrases forbidden when exact failure details are (or should be) available.
VAGUE_MULTI_TARGET_PHRASES = (
    "one or more",
    "some devices",
    "some switches",
    "some cameras",
    "some entities",
    "action needed",
)

# Soft signals that a message is a multi-target failure report.
FAILURE_CONTEXT_MARKERS = (
    "failed",
    "failure",
    "did not follow",
    "could not",
    "unable to",
)


@dataclass(frozen=True)
class LintFinding:
    code: str
    detail: str


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def looks_like_failure_notification(text: str) -> bool:
    lowered = _normalise(text)
    return any(marker in lowered for marker in FAILURE_CONTEXT_MARKERS)


def scan_failure_notification(
    text: str,
    *,
    treat_as_failure: bool | None = None,
) -> list[LintFinding]:
    """Return actionability defects for a candidate phone failure message.

    When ``treat_as_failure`` is None, failure context is inferred from wording.
    Non-failure status messages return no findings.
    """
    if not text or not text.strip():
        return [LintFinding("empty", "message is empty")]

    is_failure = (
        looks_like_failure_notification(text)
        if treat_as_failure is None
        else treat_as_failure
    )
    if not is_failure:
        return []

    lowered = _normalise(text)
    findings: list[LintFinding] = []

    for phrase in VAGUE_MULTI_TARGET_PHRASES:
        if phrase in lowered:
            findings.append(
                LintFinding(
                    "vague_multi_target",
                    f"forbidden vague wording when specifics should be known: {phrase!r}",
                )
            )

    # Expected vs actual signals (friendly heuristic — not a full grammar).
    has_expected = "expected" in lowered or "should be" in lowered or "wanted" in lowered
    has_actual = any(
        token in lowered
        for token in (
            "remained",
            "stayed",
            "was ",
            "is unavailable",
            "unavailable",
            "unknown",
            "timed out",
            "timeout",
            "actual",
        )
    )
    if not has_expected:
        findings.append(
            LintFinding("missing_expected", "no expected state/result wording found")
        )
    if not has_actual:
        findings.append(
            LintFinding("missing_actual", "no actual/observed state wording found")
        )

    # Named target bullet/line heuristic: at least one list-ish line or camera/device name pair.
    has_named_target = bool(
        re.search(r"(?m)^\s*[-•*]\s+\S+", text)
        or re.search(
            r"\b(camera|switch|sensor|lock|cover|light|device)\b.+\b(on|off|unavailable|unknown)\b",
            lowered,
        )
    )
    if not has_named_target and any(
        f.code == "vague_multi_target" for f in findings
    ):
        findings.append(
            LintFinding(
                "missing_named_targets",
                "multi-target failure lacks named targets with friendly names",
            )
        )

    return findings


def assert_actionable_or_raise(text: str, *, treat_as_failure: bool = True) -> None:
    findings = scan_failure_notification(text, treat_as_failure=treat_as_failure)
    if findings:
        joined = "; ".join(f"{f.code}: {f.detail}" for f in findings)
        raise AssertionError(f"HA-REL-006 actionability defects: {joined}")
