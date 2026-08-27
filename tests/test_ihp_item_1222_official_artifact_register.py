from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "010_obs-insc-src-cand-000010_ihp-item-1222_source-record-candidate"
)


class IhpItem1222OfficialArtifactRegisterTests(unittest.TestCase):
    def test_human_register_review_and_support_index_exist(self):
        self.assertTrue(
            (CANDIDATE / "14_official-artifact-register-and-images.md").is_file()
        )
        self.assertTrue((CANDIDATE / "95_artifact-register-index.csv").is_file())

    def test_human_review_records_membership_and_preserves_join_gate(self):
        text = (
            CANDIDATE / "14_official-artifact-register-and-images.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "ZR038421",
            "ZR053740",
            "R038421",
            "R039467",
            "R053740",
            "R053840",
            "R054970",
            "R060751",
            "R062431",
            "13.0.13027",
            "Yi Supplement 5369",
            "official composite membership",
            "正式合编成员关系",
            "join geometry still withheld",
            "缀合几何仍暂缓裁定",
        ):
            self.assertIn(marker, flat)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_support_index_binds_images_and_withholds_geometry(self):
        with (CANDIDATE / "95_artifact-register-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 12)
        self.assertTrue(all(row["join_geometry"] == "withheld" for row in rows))
        self.assertIn(
            "official_composite_membership",
            {row["relation_status"] for row in rows},
        )
        self.assertIn(
            "scale_bearing_object_image",
            {row["evidence_scope"] for row in rows},
        )


if __name__ == "__main__":
    unittest.main()
