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
    / "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)
PAGE = OBJECT / "12_heji-volume1-plate2-local-visual-receipt.md"
RECORD = OBJECT / "90_source-record.json"


class ObimdH2Plate2LocalVisualReceiptTests(unittest.TestCase):
    def record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def test_human_receipt_is_bilingual_and_linked(self):
        page = PAGE.read_text(encoding="utf-8")
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        for marker in (
            "Heji volume 1 plate 2 local visual receipt",
            "《合集》第一册图版二本地目视回执",
            "clearly printed `2`",
            "清楚印有数字 `2`",
            "local_private_only",
            "metadata_only_until_verified",
            "C1` remains `candidate_route",
            "C8` remains `withhold",
            "not a calibrated probability",
        ):
            self.assertIn(marker, page)
        self.assertIn(PAGE.name, readme)

    def test_machine_receipt_binds_local_derivative(self):
        receipt = self.record()["heji_plate2_local_visual_receipt"]
        self.assertEqual(receipt["printed_object_number"], "2")
        self.assertEqual(receipt["printed_page_number"], "1")
        self.assertEqual(receipt["size_bytes"], 1167146)
        self.assertEqual(receipt["pixel_dimensions"], [2889, 4338])
        self.assertEqual(
            receipt["sha256"],
            "fa64aa17b2d018b974529f710c9f4d53d3b75c5633a56a46a6e436fb5854d6c2",
        )
        local_path = ROOT / receipt["local_ignored_path"]
        if local_path.is_file():
            self.assertEqual(local_path.stat().st_size, receipt["size_bytes"])
            self.assertEqual(
                hashlib.sha256(local_path.read_bytes()).hexdigest(),
                receipt["sha256"],
            )

    def test_rights_and_probability_boundaries_are_explicit(self):
        receipt = self.record()["heji_plate2_local_visual_receipt"]
        self.assertEqual(receipt["rights_status"], "metadata_only_until_verified")
        self.assertEqual(
            receipt["public_visibility"],
            "local_private_only_no_image_committed",
        )
        self.assertEqual(
            receipt["probability_status"],
            "not_a_probability_routing_aid_only",
        )
        self.assertEqual(receipt["claim_effect"], "C1_remains_candidate_route")

    def test_c1_contract_records_new_fact_without_promotion(self):
        record = self.record()
        c1 = record["per_claim_contract"]["C1"]
        self.assertEqual(c1["state"], "candidate_route")
        items = {item["id"]: item for item in c1["evidence_items"]}
        item = items["ev-h2-ia-heji-vol1-plate2"]
        self.assertEqual(item["state"], "direct_checked")
        self.assertEqual(item["family_id"], "family-ia-unlicensed-heji-scan")
        self.assertIn("item-level", c1["blocker"])
        self.assertEqual(c1["delivery_state"], "withhold")

        contract = record["claim_recording_contract"]
        self.assertIn(item["id"], contract["evidence_items"])
        self.assertIn(item["family_id"], contract["evidence_families"])
        family_note = contract["evidence_families"][item["family_id"]]
        self.assertIn("not independent", family_note)
        self.assertIn("Internet Archive", contract["shared_ancestor_warning"])
        self.assertIn("item-level", contract["blocker"])
        self.assertIn("14427", contract["next_source"])

    def test_per_claim_items_and_families_are_globally_registered(self):
        record = self.record()
        contract = record["claim_recording_contract"]
        global_items = set(contract["evidence_items"])
        global_families = set(contract["evidence_families"])
        for claim in record["per_claim_contract"].values():
            for item in claim["evidence_items"]:
                self.assertIn(item["id"], global_items)
                self.assertIn(item["family_id"], global_families)
            self.assertTrue(set(claim["family_ids"]) <= global_families)

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
