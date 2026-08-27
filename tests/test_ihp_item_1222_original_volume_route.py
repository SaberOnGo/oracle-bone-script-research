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


class IhpItem1222OriginalVolumeRouteTests(unittest.TestCase):
    def test_human_route_and_support_index_exist(self):
        self.assertTrue(
            (CANDIDATE / "15_original-volume-and-errata-route.md").is_file()
        )
        self.assertTrue((CANDIDATE / "96_original-volume-route-index.csv").is_file())

    def test_human_route_preserves_the_unopened_boundary(self):
        text = (
            CANDIDATE / "15_original-volume-and-errata-route.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "9789862544471",
            "9789863222859",
            "Zhuihui 1028",
            "correction-controlled evidence gap",
            "受勘误控制的证据缺口",
            "does not contain plate 1028",
            "不含第 1028 组图版",
            "groups 641 through 646",
            "第 641 至 646 组",
            "pages 20-29",
            "第 20-29 页",
            "Lawful acquisition route",
            "合法取得路线",
        ):
            self.assertIn(marker, flat)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_index_records_checksums_and_withholds_promotion(self):
        with (CANDIDATE / "96_original-volume-route-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 4)
        self.assertTrue(all(row["claim_promotion"] == "withheld" for row in rows))
        self.assertTrue(all(len(row["sha256"]) == 64 for row in rows))
        self.assertIn(
            "sample_visually_reviewed",
            {row["review_status"] for row in rows},
        )

    def test_central_claim_gate_includes_the_original_volume_gate(self):
        text = (CANDIDATE / "08_claim-gate.md").read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "the 2011 plate",
            "separate `Tuban pian kanwu` entry",
            "matching 2013 commentary",
            "the 2018 paper",
            "2011 年图版",
            "独立《图版篇勘误》条目",
            "2013 年对应考释",
            "2018 年论文",
        ):
            self.assertIn(marker, flat)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))


if __name__ == "__main__":
    unittest.main()
