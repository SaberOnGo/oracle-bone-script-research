import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate"
)


class BritishLibraryOr1595SourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("obs-insc-src-cand-000005", parent)
        self.assertIn("[bl-1595-candidate]", parent)
        for name in (
            "01_object-and-image-routes.md",
            "02_human-inscription-dossier.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_literature-and-dispute-review.md",
            "07_missing-evidence-plan.md",
            "10_secondary-dissemination-and-rights.md",
        ):
            self.assertTrue((OBJECT / name).exists(), name)
            self.assertIn(name, readme)

    def test_source_strings_and_catalog_routes_remain_unconfirmed(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8"
        )
        for value in (
            "Or. 7694/1595r",
            "Or. 7694/1595v",
            "Heji 40610r/v",
            "已未庚申月㞢[食]",
            "七日己未斲庚申月又食",
            "source-reported",
            "not assigned",
            "not an independent transcription",
        ):
            self.assertIn(value, dossier)
        self.assertIn("not independently verified", dossier)

    def test_machine_record_keeps_image_and_candidate_boundaries(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000005")
        self.assertEqual(record["source_id"], "src-british-library-oracle-bone")
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"], "public_domain_verified")
        self.assertEqual(len(record["image_routes"]), 2)
        self.assertEqual(
            record["image_routes"][0]["sha256"],
            "ddecad64f5b958ec3c4425bad53dbe90c7f782b41622a672b7ec6d971ddf9c19",
        )
        self.assertEqual(
            record["image_routes"][1]["sha256"],
            "5833d7fc96d0d5a2878bd6981c0110c5919613cd4d382ad45f93f3451bf342f4",
        )
        self.assertIn("no decipherment conclusion", record["boundaries"])

    def test_machine_record_keeps_literature_routes_as_unresolved(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            record["literature_status"],
            "named_astronomical_date_dispute_route_only",
        )
        self.assertEqual(len(record["literature_routes"]), 2)
        self.assertEqual(
            {item["project_use"] for item in record["literature_routes"]},
            {"source_report_only", "dispute_route_only"},
        )
        for item in record["literature_routes"]:
            self.assertEqual(item["snapshot_status"], "not_downloaded")
            self.assertEqual(
                item["checksum_status"], "not_applicable_not_stored"
            )
            self.assertEqual(
                item["rights_status"], "copyright_review_required"
            )

    def test_index_and_rights_route_are_explicit(self):
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8"
        )
        for value in (
            "source_display_only_without_project_transcription",
            "not_collected",
            "not_independently_verified",
            "public_direct_route_local_private_snapshot_only",
            "public_domain_verified",
            "stable BL item record",
        ):
            self.assertIn(value, index)
        evidence = (OBJECT / "03_source-evidence-review.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("CC0 1.0 Universal Public Domain Dedication", evidence)
        self.assertIn("Page text and structured metadata", evidence)

    def test_related_routes_keep_aggregation_and_noai_boundaries(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(record["related_routes"]), 2)
        by_id = {item["route_id"]: item for item in record["related_routes"]}
        self.assertEqual(
            by_id["gac-bl-or-1595"]["independence"],
            "same_source_family_not_independent",
        )
        self.assertEqual(
            by_id["sketchfab-bl-or-1595"]["rights_status"],
            "noai_restricted_do_not_ingest",
        )
        self.assertTrue(by_id["sketchfab-bl-or-1595"]["noai_restriction"])
        route_text = (
            OBJECT / "10_secondary-dissemination-and-rights.md"
        ).read_text(encoding="utf-8")
        for marker in (
            "Google Arts & Culture",
            "same source family",
            "Sketchfab",
            "NoAI",
            "noai_restricted_do_not_ingest",
            "used for model training",
        ):
            self.assertIn(marker, route_text)

    def test_markdown_files_are_utf8_and_within_80_columns(self):
        for path in OBJECT.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            long_lines = [
                (line_no, len(line))
                for line_no, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ]
            self.assertEqual([], long_lines, str(path))


if __name__ == "__main__":
    unittest.main()
