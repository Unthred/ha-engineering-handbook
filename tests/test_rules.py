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


class ResponsiveDashboardContractTests(unittest.TestCase):
    REQUIRED_RULES = {
        "HA-UX-016": "Mobile-first progressive enhancement",
        "HA-UX-017": "Deliberate responsive space use",
        "HA-UX-018": "Operational UI content hygiene",
        "HA-UX-019": "Prefer a characterful page header with status pills",
        "HA-DESIGN-007": "Structural layout-gap prevention",
        "HA-DESIGN-008": "Section span and packing behaviour",
        "HA-DESIGN-009": "Page-header composition and pill behaviour",
        "HA-TEST-016": "Visual breakpoint verification",
    }

    def test_rule_ids_unique_and_present(self):
        catalog = json.loads((GENERATED / "rules.json").read_text(encoding="utf-8"))
        ids = [rule["id"] for rule in catalog["rules"]]
        self.assertEqual(len(ids), len(set(ids)))
        for rule_id, title in self.REQUIRED_RULES.items():
            self.assertIn(rule_id, ids)
            match = next(rule for rule in catalog["rules"] if rule["id"] == rule_id)
            self.assertEqual(title, match["title"])

    def test_normative_language_not_diluted(self):
        ux = (HANDBOOK / "04-dashboards-and-ux.md").read_text(encoding="utf-8")
        design = (HANDBOOK / "09-visual-design-system.md").read_text(encoding="utf-8")
        testing = (HANDBOOK / "07-testing-and-deployment.md").read_text(encoding="utf-8")
        review = (HANDBOOK / "10-review-and-audit.md").read_text(encoding="utf-8")
        self.assertIn("progressively enhance wider displays", ux)
        self.assertIn("does **not** mean “mobile-only”", ux)
        self.assertIn("GitHub issue and pull-request references", ux)
        self.assertIn("characterful page header with status pills", ux)
        self.assertIn("MUST NOT mechanically add a header", ux)
        self.assertIn("avoidable empty columns or substantial placement holes is defective", design)
        self.assertIn("dense_section_placement", design)
        self.assertIn("centred wrapping collection of status pills", design)
        self.assertIn("normal dashboard mode", testing)
        self.assertIn("who performed visual confirmation", testing)
        self.assertIn("Development debris", review)
        self.assertIn("Fail — structural gap", review)
        self.assertIn("Fail — missing preferred header", review)

    def test_ha_ux_005_requires_matrix_not_vague_sizes(self):
        ux = (HANDBOOK / "04-dashboards-and-ux.md").read_text(encoding="utf-8")
        self.assertIn("responsive acceptance matrix", ux)
        self.assertIn("HA-TEST-016", ux)
        self.assertNotIn(
            "Views MUST be checked at their intended phone, tablet, desktop, or wall-panel sizes.",
            ux,
        )

    def test_generated_outputs_include_responsive_contract(self):
        subprocess.run(
            ["python", "scripts/rules.py", "generate"],
            cwd=HANDBOOK.parent,
            check=True,
        )
        cursor = (
            GENERATED / ".cursor/rules/home-assistant-engineering.mdc"
        ).read_text(encoding="utf-8")
        claude = (GENERATED / "CLAUDE.md").read_text(encoding="utf-8")
        agents = (GENERATED / "AGENTS.md").read_text(encoding="utf-8")
        for blob in (cursor, claude, agents):
            for rule_id in self.REQUIRED_RULES:
                self.assertIn(rule_id, blob)
            self.assertIn("progressively enhance wider displays", blob)
            self.assertIn("avoidable empty columns or substantial placement holes is defective", blob)
            self.assertIn("GitHub issue and pull-request references", blob)
            self.assertIn("normal dashboard mode", blob)
            self.assertIn("MUST NOT mechanically add a header", blob)
            self.assertIn("centred wrapping collection of status pills", blob)

    def test_dashboard_profile_contract_markers(self):
        result = subprocess.run(
            ["python", "scripts/rules.py", "check"],
            cwd=HANDBOOK.parent,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        self.assertIn("dashboard profile OK", result.stdout)
        profile = (HANDBOOK.parent / "examples" / "dashboard-profile.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("validation_widths_px: [390, 1280]", profile)
        self.assertIn("column_span: full", profile)
        self.assertIn("forbid_in_ordinary_operational_cards:", profile)
        self.assertIn("page_header:", profile)
        self.assertIn("mode: preferred", profile)
        self.assertEqual(profile.count("page_header:"), 2)  # top-level + example_view
        self.assertIn("example_page_header_cards:", profile)
        self.assertIn("mushroom-title-card", profile)


class AgentCiOwnershipTests(unittest.TestCase):
    def test_ha_ai_007_present_with_mandatory_workflow(self):
        chapter = (HANDBOOK / "08-documentation-and-ai.md").read_text(encoding="utf-8")
        self.assertIn("## HA-AI-007 — Own pull-request CI through green or evidenced blocker", chapter)
        self.assertIn("exact pushed head SHA", chapter)
        self.assertIn("Forbidden handoff", chapter)
        self.assertIn("failing** or **unverified", chapter)
        self.assertIn("every repository", chapter)
        self.assertIn("project-local CI-ownership note without the generated handbook rule", chapter)
        self.assertIn("CI should pass", chapter)
        self.assertIn("pending at last check", chapter)
        self.assertIn("three materially different attempted fixes", chapter)
        self.assertIn("Never merge unless the human separately authorises merging", chapter)
        # Cross-link from HA-AI-006 definition of done
        self.assertIn("HA-AI-007", chapter.split("## HA-AI-006", 1)[1].split("## HA-AI-007", 1)[0])

    def test_generated_outputs_include_ha_ai_007(self):
        subprocess.run(
            ["python", "scripts/rules.py", "generate"],
            cwd=HANDBOOK.parent,
            check=True,
        )
        catalog = json.loads((GENERATED / "rules.json").read_text(encoding="utf-8"))
        ids = {rule["id"] for rule in catalog["rules"]}
        self.assertIn("HA-AI-007", ids)
        rule = next(r for r in catalog["rules"] if r["id"] == "HA-AI-007")
        self.assertIn("exact pushed head SHA", rule["text"])
        self.assertIn("Forbidden handoff", rule["text"])
        self.assertIn("every repository", rule["text"])

        cursor = (
            GENERATED / ".cursor/rules/home-assistant-engineering.mdc"
        ).read_text(encoding="utf-8")
        claude = (GENERATED / "CLAUDE.md").read_text(encoding="utf-8")
        for blob in (cursor, claude):
            self.assertIn("HA-AI-007", blob)
            self.assertIn("CI should pass", blob)
            self.assertIn("Forbidden handoff", blob)
            self.assertIn("gh pr checks", blob)


if __name__ == "__main__":
    unittest.main()
