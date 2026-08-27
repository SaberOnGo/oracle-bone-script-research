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


class IhpItem1222JoinDatabaseEvidenceTests(unittest.TestCase):
    def test_join_database_dossier_and_index_exist(self):
        self.assertTrue(
            (CANDIDATE / "13_join-database-and-bibliographic-review.md").is_file()
        )
        self.assertTrue((CANDIDATE / "94_join-database-index.csv").is_file())

    def test_human_dossier_separates_the_two_join_stages(self):
        text = (
            CANDIDATE / "13_join-database-and-bibliographic-review.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "R060751",
            "Heji Supplement 00417",
            "Zhuihui 1028",
            "two-stage source record",
            "两阶段来源记录",
            "original plate still unopened",
            "原始图版仍未打开",
            "bibliographic anomaly",
            "书目异常",
        ):
            self.assertIn(marker, flat)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_index_withholds_join_and_identity_promotion(self):
        with (CANDIDATE / "94_join-database-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 4)
        self.assertTrue(all(row["formal_identity"] == "withheld" for row in rows))
        self.assertTrue(all(row["join_verdict"] == "withheld" for row in rows))
        self.assertIn(
            "historical_stage_crosswalk_candidate",
            {row["relation_status"] for row in rows},
        )


if __name__ == "__main__":
    unittest.main()
