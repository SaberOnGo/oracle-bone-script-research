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
        self.assertIn("not a decipherment conclusion", record["boundaries"])

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
