import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHARACTER_IDS = ("000209", "000412", "000621", "000791", "000852", "000963")


class MaterialDepthIntegrationTests(unittest.TestCase):
    def test_character_human_entrances_link_filename_evidence(self):
        matches = []
        for readme in (ROOT / "corpus/001_oracle-characters").rglob("README.md"):
            if any(f"obs-char-{identifier}_" in str(readme) for identifier in CHARACTER_IDS):
                matches.append(readme)
        self.assertEqual(len(matches), 6)
        for readme in matches:
            text = readme.read_text(encoding="utf-8")
            self.assertIn("15_source-filename-evidence-review.md", text)
            self.assertIn("人类可读文件名证据", text)

    def test_inscription_candidate_has_stable_map_and_human_entrance(self):
        map_path = (
            ROOT
            / "project_registry/002_project-id-to-source-reference-map/"
            "008_oracle-inscription-source-record-candidate-map.csv"
        )
        with map_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 10)
        expected = {
            "obs-insc-src-cand-000001": "obimd-h2",
            "obs-insc-src-cand-000002": "IHP-item-503;R044498",
            "obs-insc-src-cand-000003": "IHP-item-1215;R044587",
            "obs-insc-src-cand-000004": "IHP-item-771;R039275+R043001",
            "obs-insc-src-cand-000005": "BL-Or.7694/1595r;Heji-40610r/v",
            "obs-insc-src-cand-000006": "BL-Or.7694/1535v;Heji-39498v",
            "obs-insc-src-cand-000007": "HYZ-421;H3:1325",
            "obs-insc-src-cand-000008": "Met-42045;67.43.14",
            "obs-insc-src-cand-000009": "Met-42022;18.56.71",
            "obs-insc-src-cand-000010": "IHP-item-1222;ZR038421",
        }
        for row in rows:
            project_id = row["project_id"]
            self.assertIn(project_id, expected)
            self.assertEqual(row["primary_external_ref_id"], expected[project_id])
            expected_rights = {
                "obs-insc-src-cand-000005": "public_domain_verified",
                "obs-insc-src-cand-000006": "public_domain_verified",
                "obs-insc-src-cand-000007": (
                    "source_marked_risk_noted;metadata_only_until_verified"
                ),
                "obs-insc-src-cand-000008": "public_domain_verified",
                "obs-insc-src-cand-000009": "public_domain_verified",
            }.get(project_id, "metadata_only_until_verified")
            self.assertEqual(row["rights_status"], expected_rights)
            if project_id == "obs-insc-src-cand-000007":
                self.assertEqual(
                    row["source_ids"],
                    "src-wikimedia-ningxia-museum-hyz421;src-obimd",
                )
            self.assertTrue((ROOT / row["canonical_path"]).is_dir())

        text = (ROOT / "corpus/002_oracle-bone-inscriptions/README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("[h2-candidate]", text)
        self.assertIn("H2 is not a confirmed Heji 2", text)
        self.assertIn("[ihp-503-candidate]", text)
        self.assertIn("[ihp-1215-candidate]", text)
        self.assertIn("[ihp-771-candidate]", text)
        self.assertIn("[bl-1595-candidate]", text)
        self.assertIn("[bl-1535-candidate]", text)
        self.assertIn("[met-42045-candidate]", text)
        self.assertIn("[met-42022-candidate]", text)
        self.assertIn("[ihp-1222-candidate]", text)

    def test_literature_index_links_item_level_human_dossier(self):
        text = (
            ROOT / "research/001_published-scholarship-index/README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("[hust-paper]", text)
        self.assertIn("94.6%", text)
        self.assertIn("不是释读概率", text)

    def test_current_audit_records_material_gain_without_false_closure(self):
        text = (
            ROOT
            / "corpus/009_statistics-and-derived-features/"
            "231_preprocessing-completion-audit-2026-08-12.md"
        ).read_text(encoding="utf-8")
        for marker in (
            "six selected character objects",
            "93 HUST `G_` source members",
            "one OBIMD H2 inscription source-record candidate",
            "one HUST-OBC 2024 item-level paper dossier",
            "Requirements 8, 9, and 10 therefore remain incomplete",
            "Audit result / 审计结论: `not_complete`",
        ):
            self.assertIn(marker, text)

    def test_changed_human_markdown_is_readable_and_within_line_limit(self):
        paths = [
            ROOT / "corpus/002_oracle-bone-inscriptions/README.md",
            ROOT / "research/001_published-scholarship-index/README.md",
            ROOT / "doc/project/003_record-model-and-id-system/README.md",
            ROOT / "project_registry/002_project-id-to-source-reference-map/README.md",
            ROOT
            / "corpus/009_statistics-and-derived-features/"
            "231_preprocessing-completion-audit-2026-08-12.md",
        ]
        violations = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("中文", text)
            self.assertNotIn("\ufffd", text)
            for number, line in enumerate(text.splitlines(), 1):
                if len(line) > 80:
                    violations.append(f"{path}:{number}:{len(line)}")
        self.assertEqual(violations, [])

    def test_human_gate_scores_primary_inscription_dossier_not_every_page(self):
        from tools.validation import check_human_research_material_gate as gate

        prefix = (
            "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
            "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate/"
        )
        self.assertTrue(gate.human_markdown_path(prefix + "02_human-inscription-dossier.md"))
        for supporting in (
            "README.md",
            "01_rubbing-facsimile-routes.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_missing-evidence-plan.md",
        ):
            self.assertFalse(gate.human_markdown_path(prefix + supporting))


if __name__ == "__main__":
    unittest.main()
