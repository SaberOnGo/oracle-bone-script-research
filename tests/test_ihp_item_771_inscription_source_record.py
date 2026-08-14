import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "004_obs-insc-src-cand-000004_ihp-item-771_source-record-candidate"
)


class IhpItem771InscriptionSourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8-sig")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("obs-insc-src-cand-000004", parent)
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

    def test_source_proposal_is_not_promoted_to_reading(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "R039275+R043001",
            "I 5867+8202",
            "ting-wei",
            "hsin-hai",
            "source-reported",
            "not a project transcription or translation",
            "not assigned",
        ):
            self.assertIn(value, dossier)
        self.assertIn("not collected", dossier)

    def test_machine_record_preserves_candidate_boundary(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8-sig")
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000004")
        self.assertEqual(record["museum_item"], "771")
        self.assertEqual(record["museum_accession"], "R039275+R043001")
        self.assertEqual(
            record["text_availability"],
            "source_reported_proposed_translation_without_independent_review",
        )
        self.assertEqual(
            record["formal_inscription_identity"],
            "not_assigned",
        )
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"], "metadata_only_until_verified")
        self.assertIn("no decipherment conclusion", record["boundaries"])
        self.assertEqual(len(record["image_routes"]), 3)
        self.assertEqual(len(record["page_snapshots"]), 2)

    def test_index_keeps_missing_fields_explicit(self):
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8-sig"
        )
        for value in (
            "source_reported_proposal_only",
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
            "thumbnail-115f488d1fb39b0.jpg",
            "large-115f488d1fb39b0.jpg",
            "hd-115f488d1fb39b0.jpg",
            "46d6239db5a26c9ce349332df8ee61b3eddb7937be7b9f9ad9880c9405777f66",
            "b8d7bb2be97271ee3a6d7abdd2c082c246c58d2e954b4ceae451eb98a781ec93",
            "2d7d4147f4c977f8c7cd816d9f1fbcca0713e65252ceb41ebf6a6f53025a07",
        ):
            self.assertIn(value, route_text)

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
