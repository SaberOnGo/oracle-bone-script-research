import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "003_obs-insc-src-cand-000003_ihp-item-1215_source-record-candidate"
)


class IhpItem1215InscriptionSourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8-sig")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("obs-insc-src-cand-000003", parent)
        for name in (
            "01_object-and-image-routes.md",
            "02_human-inscription-dossier.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_missing-evidence-plan.md",
            "07_visual-observation-and-parent-evidence.md",
            "08_external-catalog-search.md",
        ):
            self.assertTrue((OBJECT / name).exists(), name)
            self.assertIn(name, readme)

    def test_source_text_is_not_promoted_to_reading(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "R044587",
            "Yi Bian 3330+5281+Yi Bian buyi 4936",
            "帚（婦）井示。韋。",
            "source-reported",
            "not assigned",
            "not a project translation",
        ):
            self.assertIn(value, dossier)
        self.assertIn("not collected", dossier)

    def test_machine_record_preserves_candidate_boundary(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8-sig")
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000003")
        self.assertEqual(record["museum_item"], "1215")
        self.assertEqual(record["museum_accession"], "R044587")
        self.assertEqual(
            record["text_availability"],
            "description_only_no_full_text_or_ocr",
        )
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"], "metadata_only_until_verified")
        self.assertIn("no decipherment conclusion", record["boundaries"])
        self.assertEqual(len(record["image_routes"]), 3)

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

    def test_image_routes_match_parent_evidence(self):
        route_text = (OBJECT / "01_object-and-image-routes.md").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "6716755ee8c5a912.jpg",
            "1526755ee906c069.jpg",
            "4936755ee94db0fb.jpg",
            "bceef865308f6ad7351b6d8e7f3dfedf53bb57f4dba05e937452ba54ec819175",
            "c87562d1e2c6f20c5fc5f5ae8ecc4f240862c99f0d93c7ce36aa85132c16a819",
            "f3562d4ce4c61c4fd827c29a04ab000102bc104c805f75777e64bc40a59a3169",
        ):
            self.assertIn(value, route_text)

    def test_visual_page_keeps_parent_and_pixel_boundaries(self):
        path = OBJECT / "07_visual-observation-and-parent-evidence.md"
        text = path.read_text(encoding="utf-8-sig")
        for value in (
            "18_live-source-evidence-review.md",
            "6716755ee8c5a912.jpg",
            "1526755ee906c069.jpg",
            "4936755ee94db0fb.jpg",
            "pixel-level observations only",
            "不能单独证明实物复原",
            "metadata_only_until_verified",
        ):
            self.assertIn(value, text)
        self.assertNotIn("project reading", text)

    def test_external_search_page_keeps_negative_boundary(self):
        path = OBJECT / "08_external-catalog-search.md"
        text = path.read_text(encoding="utf-8-sig")
        for value in (
            "2026-08-21",
            "R044587",
            "Yi Bian 3330",
            "Yi Bian buyi 4936",
            "No independent book",
            "非证据",
            "not proof that no external publication",
            "没有建立新摹写",
            "metadata_only_until_verified",
        ):
            self.assertIn(value, text)

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
