import csv
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "006_obs-insc-src-cand-000006_bl-or-1535_source-record-candidate"
)
IMAGE = "03_visual-assets/001_asset-000001_bl-1535v.jpg"
EXPECTED_IMAGE = (
    975908,
    "88e5337e29035d70c89a2ba6339f1973d0e808865b312dd0131fd9f4ddb96ca6",
    (1670, 1714),
)
EXPECTED_REGIONS = {
    "M-01": (
        "x210..540;y160..1530", "left_vertical_strip",
        "not_mapped_to_source_string",
    ),
    "M-02": (
        "x470..820;y60..1270", "central_upper_strip",
        "not_mapped_to_source_string",
    ),
    "M-03": (
        "x760..1120;y160..1180", "central_right_pit_field",
        "not_mapped_to_source_string",
    ),
    "M-04": (
        "x980..1580;y160..1430", "right_broad_surface",
        "not_mapped_to_source_string",
    ),
    "M-05": (
        "x400..1140;y600..1120", "middle_marked_band",
        "not_mapped_to_source_string",
    ),
    "M-06": (
        "x270..720;y1080..1600", "lower_left_fragment_field",
        "not_mapped_to_source_string",
    ),
    "M-07": (
        "x580..1210;y1180..1660", "lower_central_opening",
        "not_inscription_evidence",
    ),
    "M-08": (
        "x1120..1590;y1100..1690", "lower_right_porous_edge",
        "not_inscription_evidence",
    ),
}


class BritishLibrary1535VisualRegionTests(unittest.TestCase):
    def test_page_is_linked_and_human_bounded(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        page = OBJECT / "10_visual-region-review.md"
        self.assertTrue(page.is_file())
        self.assertIn("10_visual-region-review.md", readme)
        self.assertIn("92_visual-region-register.csv", readme)
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("provisional_boxes_not_text_mapping", index)
        self.assertIn("92_visual-region-register.csv", index)
        text = page.read_text(encoding="utf-8")
        for marker in (
            "M-01",
            "M-08",
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
                "public_domain_verified_image_only",
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
        self.assertEqual(text.count("not_mapped_to_source_string"), 6)
        self.assertEqual(text.count("not_inscription_evidence"), 2)
        self.assertIn("public_domain_verified_image_only", text)


if __name__ == "__main__":
    unittest.main()
