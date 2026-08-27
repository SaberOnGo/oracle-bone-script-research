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


class IhpItem1222LibraryHoldingsTests(unittest.TestCase):
    def test_human_holdings_review_is_bilingual_and_bounded(self):
        path = CANDIDATE / "17_early-plate-holdings-and-copy-request.md"
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Minimal reproducible copy request",
            "最小可复跑复制请求",
            "Tuban pian kanwu",
            "图版篇勘误",
            "pages unopened",
            "目标页仍未打开",
        ):
            self.assertIn(marker, text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_holdings_index_names_all_six_target_requests(self):
        path = CANDIDATE / "98_library-holdings-route-index.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 6)
        self.assertEqual(
            {row["target"] for row in rows},
            {
                "zhuihui-1028-plate",
                "zhuihui-1028-errata",
                "zhuihui-1028-commentary",
                "zhang-song-2018-article",
                "yinxu-wenzi-zhuihe-295",
                "yan-1989-group-165",
            },
        )
        self.assertTrue(
            all(row["access_state"] == "holding_verified_pages_unopened"
                for row in rows)
        )

    def test_claim_gate_requires_separate_errata_part(self):
        claim_gate = (CANDIDATE / "08_claim-gate.md").read_text(
            encoding="utf-8"
        )
        volume_gate = (
            CANDIDATE / "15_original-volume-and-errata-route.md"
        ).read_text(encoding="utf-8")
        for text in (claim_gate, volume_gate):
            self.assertIn("Tuban pian kanwu", text)
            self.assertIn("图版篇勘误", text)


if __name__ == "__main__":
    unittest.main()
