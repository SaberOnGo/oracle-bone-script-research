import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OBJ = ROOT / (
    "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
)
HUMAN = OBJ / "13_published-reading-history-and-conflict.md"
RECORD = OBJ / "90_source-record.json"


class NingxiaHyz421SourceBaselineTests(unittest.TestCase):
    def test_human_page_records_four_page_closed_chain(self):
        text = HUMAN.read_text(encoding="utf-8")
        for marker in (
            "2003 source-edition closed chain",
            "p. 840 / leaf 173",
            "p. 841 / leaf 174",
            "p. 1452 / leaf 175",
            "p. 1724 / leaf 174",
            "拓片圖版383",
            "摹本圖版383",
            "照片圖版446",
            "421（H3:1325）龜腹甲",
            "21.6×15.1cm",
        ):
            self.assertIn(marker, text)

    def test_human_page_preserves_counterevidence_and_rights_boundary(self):
        text = HUMAN.read_text(encoding="utf-8")
        for marker in (
            "page_1724_has_no_explicit_modern_rain_avoidance_gloss",
            "Han_2007_pp350_354_pending_direct_check",
            "leaf 150",
            "p. 1427",
            "object 398",
            "community mirror",
            "not independent evidence",
            "not authorized for redistribution",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("conflict resolved", text.lower())
        self.assertNotIn("strong counterevidence", text.lower())

    def test_support_record_exposes_baseline_and_keeps_semantics_blocked(self):
        data = json.loads(RECORD.read_text(encoding="utf-8"))
        conflict = data["published_reading_conflict"]
        baseline = conflict["source_edition_2003_baseline"]
        self.assertEqual("direct_checked", baseline["review_status"])
        self.assertEqual("HYZ 421", baseline["catalog_number"])
        self.assertEqual("H3:1325", baseline["excavation_number"])
        self.assertEqual(
            "page_1724_has_no_explicit_modern_rain_avoidance_gloss",
            baseline["counterevidence"],
        )
        self.assertEqual(
            "candidate_counterevidence_pending_Han_2007",
            baseline["semantic_effect"],
        )
        self.assertEqual(
            "Han_2007_pp350_354_pending_direct_check",
            conflict["remaining_hard_gate"],
        )
        self.assertEqual("blocked", conflict["evidence_states"]["C5"])
        self.assertEqual("blocked", conflict["evidence_states"]["C6"])
        self.assertEqual("abstain_withhold", conflict["evidence_states"]["C8"])

    def test_ignored_page_receipts_replay_when_present(self):
        data = json.loads(RECORD.read_text(encoding="utf-8"))
        pages = data["published_reading_conflict"]["source_edition_2003_baseline"][
            "pages"
        ]
        self.assertEqual(4, len(pages))
        for page in pages:
            local = ROOT / page["local_ignored_path"]
            if not local.exists():
                continue
            self.assertEqual(page["size_bytes"], local.stat().st_size)
            self.assertEqual(
                page["sha256"], hashlib.sha256(local.read_bytes()).hexdigest()
            )

    def test_human_markdown_stays_within_eighty_columns(self):
        lines = HUMAN.read_text(encoding="utf-8").splitlines()
        self.assertEqual(
            [],
            [(number, line) for number, line in enumerate(lines, 1) if len(line) > 80],
        )


if __name__ == "__main__":
    unittest.main()
