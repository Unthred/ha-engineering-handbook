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
        revision = subprocess.run(
            ["git", "-C", str(HANDBOOK.parent), "rev-parse", "HEAD"],
            check=True, text=True, stdout=subprocess.PIPE,
        ).stdout.strip()
        manifest = {
            "schema_version": 1,
            "handbook_revision": revision,
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

    def test_rejects_different_handbook_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(directory)
            manifest_path = target / ".ha-handbook-install.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["handbook_revision"] = "0" * 40
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertFalse(verify_install(target))


class ProductionProofGateTests(unittest.TestCase):
    def test_ha_test_015_blocks_merge_without_deploy_prompt(self):
        chapter = (HANDBOOK / "07-testing-and-deployment.md").read_text(encoding="utf-8")
        self.assertIn("## HA-TEST-015 — Refuse merge-before-deploy prompt conflicts", chapter)
        self.assertIn("MUST STOP and report the workflow conflict", chapter)
        self.assertIn("merge normally", chapter)
        self.assertIn("do not deploy", chapter)
        self.assertIn("deployment authorisation", chapter)
        # Strengthened HA-TEST-007 language that would have blocked #248/#250
        self.assertIn("green CI", chapter)
        self.assertIn("inferred from phrases", chapter)
        self.assertIn("production-proven state", chapter)

    def test_generated_cursor_and_claude_include_ha_test_015(self):
        subprocess.run(
            ["python", "scripts/rules.py", "generate"],
            cwd=HANDBOOK.parent,
            check=True,
        )
        cursor = (
            GENERATED / ".cursor/rules/home-assistant-engineering.mdc"
        ).read_text(encoding="utf-8")
        claude = (GENERATED / "CLAUDE.md").read_text(encoding="utf-8")
        for blob in (cursor, claude):
            self.assertIn("HA-TEST-015", blob)
            self.assertIn("MUST STOP and report the workflow conflict", blob)
            self.assertIn("green CI", blob)


if __name__ == "__main__":
    unittest.main()
