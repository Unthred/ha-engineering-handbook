import tempfile
import unittest
from pathlib import Path

from scripts.rules import HANDBOOK, parse_file


class RuleParserTests(unittest.TestCase):
    def test_extracts_rule_metadata(self):
        with tempfile.TemporaryDirectory(dir=HANDBOOK) as directory:
            path = Path(directory) / "chapter.md"
            path.write_text(
                "# Chapter\n\n"
                "## HA-TEST-999 — Example rule\n\n"
                "**Level:** Standard\n\n"
                "Systems MUST be testable.\n\n"
                "**Why:** Failures happen.\n\n"
                "**Verify:** Exercise the failure path.\n",
                encoding="utf-8",
            )
            rule = parse_file(path)[0]
            self.assertEqual("HA-TEST-999", rule.id)
            self.assertEqual("TEST", rule.area)
            self.assertEqual("Systems MUST be testable.", rule.text)
            self.assertEqual("Failures happen.", rule.rationale)
            self.assertEqual("Exercise the failure path.", rule.verification)

    def test_rejects_missing_level(self):
        with tempfile.TemporaryDirectory(dir=HANDBOOK) as directory:
            path = Path(directory) / "chapter.md"
            path.write_text(
                "## HA-TEST-999 — Broken rule\n\nSystems MUST be testable.\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "has no valid Level"):
                parse_file(path)


if __name__ == "__main__":
    unittest.main()
