import csv
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate"
)


EXPECTED_IMAGES = {
    "recto": (
        "03_visual-assets/001_asset-000001_bl-1595r.png",
        942112,
        "ddecad64f5b958ec3c4425bad53dbe90c7f782b41622a672b7ec6d971ddf9c19",
        (681, 898),
    ),
    "verso": (
        "03_visual-assets/002_asset-000002_bl-1595v.png",
        933246,
        "5833d7fc96d0d5a2878bd6981c0110c5919613cd4d382ad45f93f3451bf342f4",
        (610, 905),
    ),
}

EXPECTED_REGIONS = {
    "R-01": ("recto", "x112..575;y60..405", "upper_incised_field", "not_mapped_to_source_string"),
    "R-02": ("recto", "x105..322;y260..520", "middle_surface_and_damage", "not_mapped_to_source_string"),
    "R-03": ("recto", "x285..465;y388..545", "paper_label_and_obscured_area", "not_inscription_evidence"),
    "R-04": ("recto", "x111..325;y500..842", "lower_left_incised_field", "not_mapped_to_source_string"),
    "R-05": ("recto", "x400..586;y480..782", "lower_right_incised_field", "not_mapped_to_source_string"),
    "V-01": ("verso", "x145..525;y50..240", "upper_cut_edge", "not_inscription_evidence"),
    "V-02": ("verso", "x105..440;y235..630", "central_drill_hole_field", "not_inscription_evidence"),
    "V-03": ("verso", "x460..578;y170..835", "right_margin_incised_field", "not_mapped_to_source_string"),
    "V-04": ("verso", "x40..315;y315..790", "left_surface", "not_mapped_to_source_string"),
    "V-05": ("verso", "x60..530;y690..885", "lower_edge_and_damage", "not_inscription_evidence"),
}


class BritishLibrary1595VisualRegionTests(unittest.TestCase):
    def test_human_region_page_is_linked_and_bounded(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        page = OBJECT / "11_visual-region-review.md"
        self.assertTrue(page.is_file())
        self.assertIn("11_visual-region-review.md", readme)
        self.assertIn("92_visual-region-register.csv", readme)
        index = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("provisional_boxes_not_text_mapping", index)
        self.assertIn("92_visual-region-register.csv", index)
        text = page.read_text(encoding="utf-8")
        for marker in (
            "R-01",
            "R-05",
            "V-01",
            "V-05",
            "not_mapped_to_source_string",
            "not a transcription",
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

    def test_region_register_matches_committed_source_images(self):
        with (OBJECT / "92_visual-region-register.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 10)
        self.assertEqual({row["region_id"] for row in rows}, set(EXPECTED_REGIONS))
        self.assertEqual({row["side"] for row in rows}, {"recto", "verso"})
        for row in rows:
            side, bbox, observation, relation = EXPECTED_REGIONS[row["region_id"]]
            self.assertEqual(
                (row["side"], row["bbox_xyxy_px"], row["observation_code"],
                 row["source_string_relation"]),
                (side, bbox, observation, relation),
            )
        for side, (relative, size, digest, dimensions) in EXPECTED_IMAGES.items():
            image = OBJECT / relative
            self.assertTrue(image.is_file(), image)
            self.assertEqual(image.stat().st_size, size)
            self.assertEqual(
                hashlib.sha256(image.read_bytes()).hexdigest(), digest
            )
            for row in [item for item in rows if item["side"] == side]:
                self.assertEqual(row["asset_path"], relative)
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

    def test_region_register_keeps_text_and_reading_boundaries(self):
        text = (OBJECT / "92_visual-region-register.csv").read_text(
            encoding="utf-8-sig"
        )
        self.assertNotIn("transcription", text.lower())
        self.assertNotIn("translation", text.lower())
        self.assertNotIn("decipherment", text.lower())
        self.assertEqual(text.count("not_mapped_to_source_string"), 6)
        self.assertEqual(text.count("not_inscription_evidence"), 4)


if __name__ == "__main__":
    unittest.main()
