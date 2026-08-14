import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "006_obs-insc-src-cand-000006_bl-or-1535_source-record-candidate"
)


class BritishLibraryOr1535SourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("obs-insc-src-cand-000006", parent)
        self.assertIn("[bl-1535-candidate]", parent)
        for name in (
            "01_object-and-image-routes.md",
            "02_human-inscription-dossier.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_literature-and-dispute-review.md",
            "07_missing-evidence-plan.md",
            "08_british-library-catalog-record.md",
        ):
            self.assertTrue((OBJECT / name).exists(), name)
            self.assertIn(name, readme)

    def test_source_routes_remain_candidate_only(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8"
        )
        for value in (
            "Or. 7694/1535v",
            "Heji 39498v",
            "Yingcang 1117v",
            "Source-reported",
            "not_assigned",
            "not a project transcription",
        ):
            self.assertIn(value, dossier)
        self.assertIn("not independently", dossier)
        self.assertIn("matched in this snapshot", dossier)

    def test_catalog_record_is_source_reported_and_bounded(self):
        path = OBJECT / "08_british-library-catalog-record.md"
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Or 7694/1535",
            "Shang dynasty oracle bone",
            "Couling-Chalfant",
            "Oriental Manuscripts",
            "1300 BC-1050 BC",
            "Images currently unavailable",
            "source-reported",
            "item-level JSON",
            "no project OCR",
            "or decipherment result",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("twentieth century", text)
        self.assertNotIn("project translation", text)

    def test_machine_record_keeps_image_and_identity_boundaries(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000006")
        self.assertEqual(record["source_id"], "src-british-library-oracle-bone")
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"], "public_domain_verified")
        self.assertEqual(len(record["image_routes"]), 1)
        route = record["image_routes"][0]
        self.assertEqual(route["size_bytes"], 975908)
        self.assertEqual(route["pixels"], "1670x1714")
        self.assertEqual(
            route["sha256"],
            "88e5337e29035d70c89a2ba6339f1973d0e808865b312dd0131fd9f4ddb96ca6",
        )
        self.assertIn("no decipherment conclusion", record["boundaries"])

    def test_index_and_rights_route_are_explicit(self):
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8"
        )
        for value in (
            "not_available_in_checked_snapshot",
            "not_independently_verified",
            "public_direct_route_local_private_snapshot_only",
            "public_domain_verified",
            "stable BL object record",
        ):
            self.assertIn(value, index)
        evidence = (OBJECT / "03_source-evidence-review.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("CC0 1.0 Universal Public Domain Dedication", evidence)
        self.assertIn("31453308", evidence)

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
