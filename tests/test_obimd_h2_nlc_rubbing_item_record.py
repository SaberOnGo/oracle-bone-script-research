import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OBJ = ROOT / (
    "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)
HUMAN = OBJ / "13_nlc-rubbing-item-record-and-broken-object-link.md"
RECORD = OBJ / "90_source-record.json"
IMAGE = ROOT / (
    "tmp/source_downloads/"
    "dl-nlc-oracle-rubbing-14427T-20260830.jpg"
)


class ObimdH2NlcRubbingItemRecordTests(unittest.TestCase):
    def test_human_page_is_linked_bilingual_and_readable(self):
        text = HUMAN.read_text(encoding="utf-8")
        readme = (OBJ / "README.md").read_text(encoding="utf-8")
        self.assertIn(HUMAN.name, readme)
        self.assertIn("## English", text)
        self.assertIn("## 简体中文", text)
        long_lines = [
            (number, line)
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], long_lines)

    def test_human_page_preserves_source_text_and_scope_boundary(self):
        text = HUMAN.read_text(encoding="utf-8")
        for marker in (
            "2022JGTP0627",
            "北圖14427",
            "善9025",
            "合集2",
            "■[王大令眾人]曰： 04114[田]，其受年。[十]一[月]。",
            "rubbing_record_dimensions_not_physical_object_dimensions",
            "broken_physical_object_link",
            "7.7×7.2cm",
            "甲骨14427T",
        ):
            self.assertIn(marker, text)

    def test_support_record_keeps_identity_and_reading_withheld(self):
        data = json.loads(RECORD.read_text(encoding="utf-8"))
        item = data["national_library_rubbing_item_record"]
        self.assertEqual("direct_checked", item["review_status"])
        self.assertEqual(
            "rubbing_record_dimensions_not_physical_object_dimensions",
            item["dimension_scope"],
        )
        self.assertEqual("broken_physical_object_link", item["object_link_status"])
        self.assertEqual("candidate_route", data["claim_gate_decision"]["C1"])
        self.assertEqual("blocked", data["claim_gate_decision"]["C5"])
        self.assertEqual("blocked", data["claim_gate_decision"]["C6"])
        self.assertEqual("withhold", data["claim_gate_decision"]["C8"])
        self.assertEqual("abstain", data["claim_gate_decision"]["delivery_action"])
        c1_items = {
            item["id"]: item
            for item in data["per_claim_contract"]["C1"]["evidence_items"]
        }
        self.assertEqual(
            c1_items["ev-h2-nlc-fig3"]["family_id"],
            c1_items["ev-h2-nlc-rubbing-item-2022JGTP0627"]["family_id"],
        )
        self.assertNotIn(
            "family-nlc-rubbing-catalog",
            data["claim_recording_contract"]["evidence_families"],
        )

    def test_ignored_image_receipt_replays_when_present(self):
        data = json.loads(RECORD.read_text(encoding="utf-8"))
        item = data["national_library_rubbing_item_record"]
        self.assertEqual(323056, item["image_size_bytes"])
        self.assertEqual([945, 1417], item["image_pixel_dimensions"])
        self.assertEqual(
            "314c76798a617ec425e2191ef035c1cdd0dc84b47892455f7ccb1c8f5a1b0f08",
            item["image_sha256"],
        )
        if IMAGE.exists():
            self.assertEqual(item["image_size_bytes"], IMAGE.stat().st_size)
            self.assertEqual(
                item["image_sha256"],
                hashlib.sha256(IMAGE.read_bytes()).hexdigest(),
            )

        for prefix in ("html", "api"):
            local = ROOT / item[f"{prefix}_local_ignored_path"]
            if local.exists():
                self.assertEqual(item[f"{prefix}_size_bytes"], local.stat().st_size)
                self.assertEqual(
                    item[f"{prefix}_sha256"],
                    hashlib.sha256(local.read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
