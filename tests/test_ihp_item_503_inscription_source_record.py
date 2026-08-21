import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "002_obs-insc-src-cand-000002_ihp-item-503_source-record-candidate"
)


class IhpItem503InscriptionSourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8-sig")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("obs-insc-src-cand-000002", parent)
        for name in (
            "01_object-and-image-routes.md",
            "02_human-inscription-dossier.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_missing-evidence-plan.md",
            "07_visual-observation-and-parent-evidence.md",
            "08_claim-evidence-gate-review.md",
        ):
            self.assertTrue((OBJECT / name).exists(), name)
            self.assertIn(name, readme)

    def test_source_description_is_not_promoted_to_text_or_reading(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "R044498",
            "Ping 0529",
            "《丙》0529",
            "帝令雨",
            "source-reported only",
            "not assigned",
            "not a translation supplied by this project",
        ):
            self.assertIn(value, dossier)
        self.assertIn("not collected", dossier)

    def test_live_official_recheck_keeps_source_boundary(self):
        text = (OBJECT / "03_source-evidence-review.md").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "2026-08-21",
            "https://museum.sinica.edu.tw/en/collection/32/item/503/",
            "https://museum.sinica.edu.tw/collection/32/item/503/",
            "帝令雨",
            "not a new byte snapshot",
            "可复现记录",
        ):
            self.assertIn(value, text)

    def test_machine_record_preserves_candidate_boundary(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(
                encoding="utf-8-sig"
            )
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000002")
        self.assertEqual(record["museum_item"], "503")
        self.assertEqual(record["museum_accession"], "R044498")
        self.assertEqual(record["text_availability"],
                         "description_only_no_full_text_or_ocr")
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"],
                         "metadata_only_until_verified")
        self.assertEqual(record["claim_gate_review"]["c1_object_identity"],
                         "blocked")
        self.assertEqual(record["claim_gate_review"]["c8_user_delivery"],
                         "withheld")
        self.assertIn("not a decipherment conclusion", record["boundaries"])

    def test_claim_gate_page_preserves_candidate_boundary(self):
        page = (OBJECT / "08_claim-evidence-gate-review.md").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "C1 object identity",
            "C2 direct glyph observation",
            "C4 inscription occurrence and context",
            "C8 complete proposition and user delivery",
            "C1 对象身份",
            "C8 完整命题与用户交付",
            "帝令雨",
            "no user-facing",
            "候选",
        ):
            self.assertIn(value, page)

    def test_index_keeps_missing_fields_explicit(self):
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "source_description_only",
            "not_collected",
            "local_private_route_only",
            "metadata_only_until_verified",
            "source_record_candidate_needs_catalog_and_text_review",
        ):
            self.assertIn(value, index)

    def test_visual_page_keeps_parent_and_pixel_boundaries(self):
        path = OBJECT / "07_visual-observation-and-parent-evidence.md"
        text = path.read_text(encoding="utf-8-sig")
        for value in (
            "18_live-source-evidence-review.md",
            "hd-77859e83b1f6f4f0.jpg",
            "753,936",
            "1431 x 1920",
            "febc5c14cd855f9cca4ae314233ffff718a51ae7808aadf4e4d9ba020dbf21c9",
            "pixel-level observations",
            "不能证明实物或编辑拼合",
            "metadata_only_until_verified",
        ):
            self.assertIn(value, text)
        self.assertNotIn("project reading", text)

    def test_markdown_files_are_utf8_and_within_80_columns(self):
        for path in OBJECT.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            long_lines = [
                (line_no, len(line))
                for line_no, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ]
            self.assertEqual([], long_lines, str(path))


if __name__ == "__main__":
    unittest.main()
