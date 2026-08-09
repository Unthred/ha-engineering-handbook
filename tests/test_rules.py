import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.rules import GENERATED, HANDBOOK, parse_file, verify_install


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


class InstallVerificationTests(unittest.TestCase):
    def make_target(self, directory: str) -> Path:
        target = Path(directory)
        subprocess.run(["git", "init", "-q", str(target)], check=True)
        installed = target / ".cursor/rules/home-assistant-engineering.mdc"
        installed.parent.mkdir(parents=True)
        installed.write_text(
            (GENERATED / ".cursor/rules/home-assistant-engineering.mdc").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        overlay = target / ".cursor/rules/local/secrets.mdc"
        overlay.parent.mkdir(parents=True)
        overlay.write_text("Secrets workflow without values.\n", encoding="utf-8")
        matrix = target / ".cursor/handbook/preservation-matrix.json"
        matrix.parent.mkdir(parents=True)
        matrix.write_text(json.dumps({"entries": [{"status": "preserved-equivalently"}]}), encoding="utf-8")
        manifest = {
            "schema_version": 1,
            "handbook_revision": "0" * 40,
            "installed_generated_files": [{
                "source": ".cursor/rules/home-assistant-engineering.mdc",
                "destination": ".cursor/rules/home-assistant-engineering.mdc",
            }],
            "workspace_roots": ["."],
            "local_overlays": [".cursor/rules/local"],
            "required_capabilities": [{
                "name": "secrets management", "owner": "local overlay",
                "instruction": ".cursor/rules/local/secrets.mdc",
            }],
            "preservation_matrix": ".cursor/handbook/preservation-matrix.json",
            "required_assets": [".cursor/rules/local/secrets.mdc"],
        }
        (target / ".ha-handbook-install.json").write_text(json.dumps(manifest), encoding="utf-8")
        return target

    def test_accepts_complete_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(verify_install(self.make_target(directory)))

    def test_rejects_unresolved_preservation_gap(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(directory)
            matrix = target / ".cursor/handbook/preservation-matrix.json"
            matrix.write_text(json.dumps({"entries": [{"status": "missing"}]}), encoding="utf-8")
            self.assertFalse(verify_install(target))


if __name__ == "__main__":
    unittest.main()
