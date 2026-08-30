import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
)
PAGE = OBJECT / "13_published-reading-history-and-conflict.md"
RECORD = OBJECT / "90_source-record.json"


class NingxiaHyz421PublishedReadingConflictTests(unittest.TestCase):
    def record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def test_conflict_contract_preserves_source_ancestry_and_blockers(self):
        conflict = self.record()["published_reading_conflict"]
        self.assertEqual(conflict["target_locator"], "H3:421")
        self.assertEqual(conflict["source_doi"], "10.18212/cccs.2013..23.010")
        self.assertEqual(conflict["printed_page"], 221)
        self.assertEqual(
            conflict["source_url"],
            "https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001834863",
        )
        self.assertEqual(
            conflict["source_reported_scope"],
            "being_at_an_untranscribed_place_and_avoiding_rain",
        )
        self.assertEqual(
            conflict["immediate_claim_ancestor"],
            "Han_Jiangsu_2007_printed_pages_351_353",
        )
        self.assertEqual(
            conflict["independence_status"],
            "published_reception_route_not_independent_plate_or_reading_witness",
        )
        self.assertEqual(
            conflict["adjudication_status"],
            "high_value_conflict_candidate_pending_primary_source_check",
        )
        self.assertEqual(conflict["evidence_states"]["C4"], "candidate_route")
        self.assertEqual(conflict["evidence_states"]["C5"], "blocked")
        self.assertEqual(conflict["evidence_states"]["C6"], "blocked")
        self.assertEqual(conflict["evidence_states"]["C8"], "abstain_withhold")
        semantic = conflict["semantic_dispute_route"]
        self.assertEqual(
            semantic["url"], "https://www.fdgwz.org.cn/Web/Show/1770"
        )
        self.assertEqual(semantic["target_scope"], "comparative_not_direct_HYZ421")

    def test_conflict_is_checksum_bound_when_local_pdf_is_present(self):
        conflict = self.record()["published_reading_conflict"]
        self.assertEqual(conflict["pdf_size_bytes"], 803095)
        self.assertEqual(
            conflict["pdf_sha256"],
            "ce7c7bf5fe5f989793c4072f06cce709280b2b27a6260035fa3f995d9254aa0e",
        )
        path = ROOT / conflict["local_ignored_path"]
        if path.is_file():
            self.assertEqual(path.stat().st_size, conflict["pdf_size_bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                conflict["pdf_sha256"],
            )

    def test_human_page_is_linked_bilingual_and_non_promotional(self):
        page = PAGE.read_text(encoding="utf-8")
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn(PAGE.name, readme)
        for marker in (
            "Published reading history and conflict",
            "公开释读史与冲突",
            "10.18212/cccs.2013..23.010",
            "H3:421",
            "Han Jiangsu",
            "韩江苏",
            "not an independent",
            "不是独立",
            "C5",
            "C6",
            "abstain",
        ):
            self.assertIn(marker, page)
        self.assertNotIn("high_confidence", page)
        self.assertNotIn("高置信", page)

    def test_human_markdown_stays_within_eighty_columns(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertNotIn("\ufffd", text)
        for line_number, line in enumerate(text.splitlines(), 1):
            self.assertLessEqual(
                len(line),
                80,
                f"{PAGE}:{line_number}: {len(line)} characters",
            )


if __name__ == "__main__":
    unittest.main()
