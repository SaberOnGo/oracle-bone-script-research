import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "006_obs-insc-src-cand-000006_bl-or-1535_source-record-candidate"
)
PAGE = OBJECT / "11_published-opposite-face-plate.md"


class BritishLibrary1535PublishedPlateTests(unittest.TestCase):
    def test_human_page_is_linked_bilingual_and_bounded(self):
        self.assertTrue(PAGE.is_file())
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn(PAGE.name, readme)
        text = PAGE.read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "Published Opposite-Face Plate Review",
            "出版物异面图版复核",
            "Or.7694/1535",
            "printed spread 20--21",
            "印刷页 20--21",
            "opposite-surface compatibility observation",
            "异面轮廓相容观察",
            "没有释读或破译获得晋级",
        ):
            self.assertIn(marker, text)
        self.assertIn("No reading or decipherment is promoted", flat)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_capture_and_rights_boundaries_are_explicit(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("1093393", text)
        self.assertIn(
            "ebc0d151823ff672d86fc86e7800cb7f40eb718fbab02a8810f62a153a0a7446",
            text,
        )
        self.assertIn("certificate produced a hostname-mismatch error", text)
        self.assertIn("did not bypass that certificate check", text)
        self.assertIn(
            "metadata_and_visual_observation_only_until_reuse_terms_verified",
            text,
        )
        self.assertIn("No OpenCV runtime was available", text)
        self.assertNotIn("match probability", text.lower())

    def test_machine_support_matches_the_human_boundary(self):
        data = json.loads((OBJECT / "90_source-record.json").read_text(
            encoding="utf-8"
        ))
        expected = (
            "published_plate_source_reported_object_match_side_unresolved"
        )
        self.assertEqual(data["plate_status"], "not_independently_verified")
        self.assertEqual(data["publication_plate_status"], expected)
        route = data["publication_plate_routes"][0]
        self.assertEqual(route["object_caption"], "British Library Or.7694/1535")
        self.assertEqual(route["face_label_status"], "unresolved")
        self.assertEqual(route["size_bytes"], 1093393)
        self.assertEqual(len(route["sha256"]), 64)
        with (OBJECT / "91_source-record-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            row = next(csv.DictReader(handle))
        self.assertEqual(row["plate_status"], "not_independently_verified")
        self.assertEqual(row["publication_plate_status"], expected)
        self.assertIn("explicit face labels", row["missing_evidence"])

    def test_human_guide_exposes_the_published_plate(self):
        guide = (
            ROOT
            / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
            "005_opened-source-record-candidate-guide.md"
        ).read_text(encoding="utf-8")
        self.assertIn("2019 published opposite-face plate", guide)
        self.assertIn("2019 年出版", guide)
        self.assertTrue(all(len(line) <= 80 for line in guide.splitlines()))


if __name__ == "__main__":
    unittest.main()
