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


class IhpItem1222RigidImageControlTests(unittest.TestCase):
    def test_human_review_and_support_index_exist(self):
        self.assertTrue(
            (CANDIDATE / "16_rigid-image-match-and-countercontrol.md").is_file()
        )
        self.assertTrue((CANDIDATE / "97_rigid-match-index.csv").is_file())

    def test_human_review_preserves_diagnostic_boundary(self):
        text = (
            CANDIDATE / "16_rigid-image-match-and-countercontrol.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "similarity transform only",
            "仅使用相似变换",
            "opposite-face countercontrol",
            "异面反向对照",
            "algorithmic inconclusive",
            "算法未定",
            "not a seam verdict",
            "不是接缝裁决",
        ):
            self.assertIn(marker, flat)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_support_index_separates_matches_from_inconclusive_rows(self):
        with (CANDIDATE / "97_rigid-match-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 12)
        statuses = {row["diagnostic_status"] for row in rows}
        self.assertEqual(statuses, {"rigid_match", "algorithmic_inconclusive"})
        matched_members = {
            row["member_id"]
            for row in rows
            if row["diagnostic_status"] == "rigid_match"
        }
        self.assertEqual(matched_members, {"R038421", "R039467", "R060751"})
        self.assertTrue(all(row["join_verdict"] == "withheld" for row in rows))


if __name__ == "__main__":
    unittest.main()
