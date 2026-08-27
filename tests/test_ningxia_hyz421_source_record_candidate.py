import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
)
IMAGE = OBJECT / "03_visual-assets/001_asset-000001_ningxia-hyz421_h3-1325.jpg"


class NingxiaHyz421SourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("obs-insc-src-cand-000007", parent)
        self.assertIn("[ningxia-hyz421-candidate]", parent)
        for name in (
            "01_object-and-image-routes.md",
            "02_human-inscription-dossier.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_literature-and-dispute-review.md",
            "07_missing-evidence-plan.md",
            "09_schwartz-2019-entry-and-identity-conflict.md",
            "10_dpm-2024-morphology-crosscheck.md",
            "11_obimd-hd421-plate-match.md",
        ):
            self.assertTrue((OBJECT / name).is_file(), name)
            self.assertIn(name, readme)

    def test_image_bytes_match_human_and_machine_receipts(self):
        self.assertTrue(IMAGE.is_file(), IMAGE)
        data = IMAGE.read_bytes()
        self.assertEqual(len(data), 2302630)
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "b4f44b4a325d0a24c605ce84ae3c8180177407e59709e69892185fb66398adaa",
        )
        self.assertEqual(
            hashlib.sha1(data).hexdigest(),
            "30a8c1000ea08df01199e4ae20d90053cc434802",
        )
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (3001, 3345))
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.mode, "RGB")
        route = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )["image_route"]
        self.assertEqual(route["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(route["sha1"], hashlib.sha1(data).hexdigest())
        self.assertEqual(route["size_bytes"], len(data))
        self.assertEqual(route["pixels"], "3001x3345")

    def test_source_text_and_context_remain_source_reported(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8"
        )
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        for marker in (
            "HYZ 421, H3:1325",
            "Huayuanzhuang",
            "壬辰夕卜：其宜（俎）一于，若?用。",
            "not an independent transcription",
            "not assigned",
            "Components and relations",
            "Scholarship and dispute trail",
            "Next relation checks",
        ):
            self.assertIn(marker, dossier)
        self.assertEqual(
            record["text_status"],
            "edition_has_two_entries_commons_display_is_incomplete",
        )
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"], "source_marked_risk_noted")
        self.assertIn("no decipherment conclusion", record["boundaries"])

    def test_literature_and_rights_routes_are_explicit(self):
        literature = (OBJECT / "06_literature-and-dispute-review.md").read_text(
            encoding="utf-8"
        )
        evidence = (OBJECT / "03_source-evidence-review.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "Schwartz",
            "347",
            "561",
            "10.1515/9781501505294",
            "Page-level verification",
            "CC BY-NC-ND 3.0",
            "edition_entry_and_raw_data_checked",
            "21.6",
        ):
            self.assertIn(marker, literature)
        self.assertIn("CC BY-SA 3.0", evidence)
        self.assertIn("museum object", evidence)
        self.assertIn("2026-08-21", evidence)
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        publisher_routes = [
            item
            for item in record["literature_routes"]
            if item.get("doi") == "10.1515/9781501505294"
        ]
        self.assertEqual(len(publisher_routes), 1)
        self.assertEqual(
            publisher_routes[0]["status"],
            "publisher_metadata_and_open_access_routes_checked",
        )
        self.assertEqual(
            publisher_routes[0]["effective_project_rights"],
            "no_derivative_pages_or_extracts_committed",
        )

    def test_edition_identity_candidate_and_dimension_conflict_are_explicit(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        identity = record["edition_identity"]
        self.assertEqual(identity["catalog_number"], "HYZ 421")
        self.assertEqual(identity["excavation_number"], "H3:1325")
        self.assertEqual(identity["entry_count"], 2)
        self.assertEqual(identity["printed_entry_page"], 347)
        self.assertEqual(identity["printed_raw_data_page"], 426)
        self.assertEqual(identity["edition_dimensions_cm"], "21.6 x 15.1")
        self.assertEqual(identity["commons_dimensions_cm"], "28.3 x 20.0")
        self.assertEqual(
            identity["photograph_identity"],
            "high_confidence_candidate_plate_visual_match",
        )
        self.assertIn("dimension_conflict_open", record["dispute_status"])

    def test_obimd_plate_match_is_checksum_bound_and_non_numeric(self):
        page = (OBJECT / "11_obimd-hd421-plate-match.md").read_text(
            encoding="utf-8"
        )
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        plate = record["obimd_plate_evidence"]
        for marker in (
            "Rubbing plate 383",
            "H3:1325",
            "high_confidence_candidate_plate_visual_match",
            "No percentage is displayed",
            "metadata_only_until_verified",
            "HTTP 500",
        ):
            self.assertIn(marker, page)
        self.assertEqual(plate["rubbing_name"], "HD421")
        self.assertEqual(plate["annotation_group_count"], 4)
        self.assertEqual(
            plate["rubbing_sha256"],
            "ca546645ddac768b3e96a1b112f1054c6f8bd6edd5299c386a55b50401253a74",
        )
        self.assertEqual(
            plate["facsimile_sha256"],
            "7d594c69affdec1e56f1b4384788d6c7b9b48d410bd50da9aa6db798ef612f98",
        )
        self.assertEqual(
            plate["probability_status"],
            "not_displayed_no_task_specific_calibration",
        )
        self.assertEqual(list(OBJECT.rglob("hd421.jpg")), [])

    def test_morphology_route_is_compatible_but_not_diagnostic(self):
        page = (OBJECT / "10_dpm-2024-morphology-crosscheck.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "printed page 36",
            "blunt-rounded",
            "low_specificity",
            "cannot choose",
            "f67a269954a649ce69ac4f75156e35481a5b42f4f39f1ca69f73015a257f48f7",
        ):
            self.assertIn(marker, page)
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        routes = [
            route
            for route in record["literature_routes"]
            if "李延彦" in route["citation"]
        ]
        self.assertEqual(len(routes), 1)
        self.assertEqual(
            routes[0]["identity_effect"],
            "low_specificity_compatible_not_diagnostic",
        )

    def test_human_markdown_is_utf8_and_within_80_columns(self):
        for path in OBJECT.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            for line_number, line in enumerate(text.splitlines(), 1):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
