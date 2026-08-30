import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    / "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate"
)


class Bl1595EclipseDisputeAdjudicationTests(unittest.TestCase):
    def test_human_dossier_separates_object_scope_and_timing_constraints(self):
        path = OBJECT / "13_eclipse-date-evidence-and-falsification.md"
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Or. 7694/1595 / Yingcang 886",
            "Yingcang 885/886",
            "1192 BCE",
            "1166 BCE",
            "DE422",
            "28,837",
            "1,042",
            "21:50:46",
            "23:33:29",
            "00:50:20",
            "07:14:32",
            "not the same tested proposition",
            "不是同一个受检命题",
            "astronomical year",
            "twentieth-century addition",
            "withhold",
            "Current source-route observation",
        ):
            self.assertIn(marker, text)

        self.assertIn("strongest alternative", text)
        self.assertIn("最强替代解释", text)
        self.assertNotIn("Confirmed finding", text)
        self.assertNotIn("已确认的资料发现", text)
        self.assertNotIn("hypothesis_probability=", text)
        self.assertNotIn("date_is_confirmed", text)

    def test_network_receipts_are_bound_without_claiming_full_article(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        routes = {row["source_id"]: row for row in record["literature_routes"]}

        de422 = routes["literature-ma-et-al-de422-2021"]
        self.assertEqual(de422["snapshot_size_bytes"], 56776)
        self.assertEqual(
            de422["snapshot_sha256"],
            "959635a3fa40b7ac376f75da3fbe828d4e4f12217a46f1f16a1f0880ff832bed",
        )
        self.assertEqual(de422["project_use"], "timing_countercheck_only")

        scroll = routes["literature-scroll-bl-1595-2016"]
        self.assertEqual(scroll["snapshot_size_bytes"], 135946)
        self.assertEqual(
            scroll["snapshot_sha256"],
            "7cbe34af8de639913e3146ce3ba0fd99e559efc510158d36088ba6e16460a25b",
        )
        self.assertEqual(scroll["first_checked_at"], "2026-08-14")
        self.assertEqual(scroll["snapshot_retrieved_at"], "2026-08-30")
        self.assertEqual(scroll["http_status"], 200)
        self.assertEqual(scroll["content_type"], "text/html")

        liu = routes["literature-liu-early-china-2014"]
        self.assertEqual(liu["snapshot_status"], "http_429_no_local_snapshot")
        self.assertEqual(liu["evidence_level"], "abstract_and_notes_route")
        self.assertEqual(liu["first_checked_at"], "2026-08-14")
        self.assertIsNone(liu["snapshot_retrieved_at"])
        self.assertEqual(liu["last_attempt_at"], "2026-08-30")
        self.assertEqual(liu["http_status"], 429)
        self.assertIsNone(liu["content_type"])
        self.assertIn("not full article", liu["risk_note"])

    def test_human_dossier_is_bilingual_and_within_line_limit(self):
        text = (OBJECT / "13_eclipse-date-evidence-and-falsification.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Decision / 裁决", text)
        violations = [
            (number, len(line))
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
