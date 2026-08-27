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


class IhpItem1222LiteratureDisputeEvidenceTests(unittest.TestCase):
    def test_human_literature_dossiers_and_support_index_exist(self):
        self.assertTrue(
            (CANDIDATE / "09_literature-join-and-dispute-evidence.md").is_file()
        )
        self.assertTrue(
            (CANDIDATE / "10_literature-source-snapshot-record.md").is_file()
        )
        self.assertTrue((CANDIDATE / "92_literature-source-index.csv").is_file())

    def test_human_record_preserves_candidate_and_counterevidence(self):
        text = (
            CANDIDATE / "09_literature-join-and-dispute-evidence.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "published_source_reported_crosswalk_candidate",
            "Heji 13517",
            "Huibian 1028",
            "𠂤组和宾组卜辞",
            "史语所藏“类家谱”甲骨刻辞新探",
            "R53740",
            "R53840",
            "R54970",
            "R62431",
            "physical inspection",
            "实物目验",
            "counterevidence",
            "反证",
            "20-29",
            "20-30",
            "14-17",
            "21-23",
        ):
            self.assertIn(marker, flat)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_snapshot_record_binds_local_captures_and_rights(self):
        text = (
            CANDIDATE / "10_literature-source-snapshot-record.md"
        ).read_text(encoding="utf-8")
        for marker in (
            "689541bdbcd48483e002fc70e7043a34e885ae59dc36846fbdcb79295e551cc1",
            "82b9678fc13fb4e1dbb0a33d5060bbb2475584311f0f2323c7ddcddba80a27b0",
            "metadata_only_until_verified",
            ".working/ihp-1222-literature-20260827/",
            "PDF parse warning",
            "PDF 解析警告",
        ):
            self.assertIn(marker, text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_machine_index_keeps_claims_withheld(self):
        with (CANDIDATE / "92_literature-source-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 5)
        self.assertTrue(
            all(
                row["claim_status"]
                in {
                    "source_report_only",
                    "crosswalk_candidate_only",
                    "bibliographic_route_only",
                }
                for row in rows
            )
        )
        self.assertTrue(
            all(row["rights_status"] == "metadata_only_until_verified" for row in rows)
        )
        self.assertFalse(any(row["formal_identity"] == "confirmed" for row in rows))


if __name__ == "__main__":
    unittest.main()
