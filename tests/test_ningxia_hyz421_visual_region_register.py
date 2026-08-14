import csv
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
)
IMAGE = "03_visual-assets/001_asset-000001_ningxia-hyz421_h3-1325.jpg"
EXPECTED_IMAGE = (
    2302630,
    "b4f44b4a325d0a24c605ce84ae3c8180177407e59709e69892185fb66398adaa",
    (3001, 3345),
)
EXPECTED_REGIONS = {
    "H-01": (
        "x430..2530;y90..1030", "upper_shell_surface",
        "not_mapped_to_source_string",
    ),
    "H-02": (
        "x1660..2920;y240..1180", "upper_right_marked_field",
        "not_mapped_to_source_string",
    ),
    "H-03": (
        "x170..1280;y930..1900", "central_left_marked_field",
        "not_mapped_to_source_string",
    ),
    "H-04": (
        "x1320..2780;y1000..2050", "central_right_surface",
        "not_mapped_to_source_string",
    ),
    "L-01": (
        "x210..1170;y1850..2880", "lower_left_marked_field",
        "not_mapped_to_source_string",
    ),
    "L-02": (
        "x950..2070;y2050..3150", "lower_center_surface",
        "not_mapped_to_source_string",
    ),
    "L-03": (
        "x1980..2910;y1900..3050", "lower_right_marked_field",
        "not_mapped_to_source_string",
    ),
    "L-04": (
        "x540..2460;y2920..3344", "lower_edge_and_opening",
        "not_inscription_evidence",
    ),
}


class NingxiaHyz421VisualRegionTests(unittest.TestCase):
    def test_page_is_linked_and_human_bounded(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        page = OBJECT / "08_visual-region-review.md"
        self.assertTrue(page.is_file())
        self.assertIn("08_visual-region-review.md", readme)
        self.assertIn("92_visual-region-register.csv", readme)
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("provisional_boxes_not_text_mapping", index)
        self.assertIn("92_visual-region-register.csv", index)
        text = page.read_text(encoding="utf-8")
        for marker in (
            "H-01",
            "L-04",
            "not_mapped_to_source_string",
            "not OCR",
            "No OCR",
            "not a formal inscription record",
            "具体下一步待查",
        ):
            self.assertIn(marker, text)
        self.assertEqual(
            [],
            [
                (number, len(line))
                for number, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ],
        )

    def test_register_binds_image_and_boxes(self):
        image = OBJECT / IMAGE
        self.assertTrue(image.is_file(), image)
        size, digest, dimensions = EXPECTED_IMAGE
        self.assertEqual(image.stat().st_size, size)
        self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), digest)
        from PIL import Image

        with Image.open(image) as opened:
            self.assertEqual(opened.size, dimensions)
        with (OBJECT / "92_visual-region-register.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 8)
        self.assertEqual(
            {row["region_id"] for row in rows}, set(EXPECTED_REGIONS)
        )
        for row in rows:
            bbox, observation, relation = EXPECTED_REGIONS[row["region_id"]]
            self.assertEqual(row["asset_path"], IMAGE)
            self.assertEqual(
                (row["bbox_xyxy_px"], row["observation_code"],
                 row["source_string_relation"]),
                (bbox, observation, relation),
            )
            self.assertEqual(
                row["review_status"],
                "visual_region_candidate_pending_human_check",
            )
            self.assertEqual(
                row["rights_status"],
                "source_marked_risk_noted_uploaded_photo",
            )
            values = row["bbox_xyxy_px"].replace("x", "").replace("y", "")
            x_part, y_part = values.split(";")
            x1, x2 = [int(value) for value in x_part.split("..")]
            y1, y2 = [int(value) for value in y_part.split("..")]
            self.assertLess(x1, x2)
            self.assertLess(y1, y2)
            self.assertGreaterEqual(x1, 0)
            self.assertGreaterEqual(y1, 0)
            self.assertLessEqual(x2, dimensions[0])
            self.assertLessEqual(y2, dimensions[1])

    def test_register_keeps_text_and_rights_boundaries(self):
        text = (OBJECT / "92_visual-region-register.csv").read_text(
            encoding="utf-8-sig"
        )
        self.assertNotIn("transcription", text.lower())
        self.assertNotIn("translation", text.lower())
        self.assertNotIn("decipherment", text.lower())
        self.assertEqual(text.count("not_mapped_to_source_string"), 7)
        self.assertEqual(text.count("not_inscription_evidence"), 1)
        self.assertIn("source_marked_risk_noted_uploaded_photo", text)


if __name__ == "__main__":
    unittest.main()
