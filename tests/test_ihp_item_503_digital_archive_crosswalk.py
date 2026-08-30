import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    / "002_obs-insc-src-cand-000002_ihp-item-503_source-record-candidate"
)


class IhpItem503DigitalArchiveCrosswalkTests(unittest.TestCase):
    def test_human_dossier_keeps_crosswalk_and_measurement_boundaries(self):
        text = (OBJECT / "10_digital-archive-rubbing-crosswalk.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "188493-0529",
            "R044498",
            "《丙》0529",
            "19.23 x 13.79 cm",
            "17.4 x 13.8 cm",
            "not a dimension conflict",
            "不是尺寸冲突",
            "institution-internal candidate route only",
            "机构内交叉候选",
            "帝令雨",
            "not a full transcription",
            "公开访问不等于再分发许可",
            "TLS certificate",
            "withhold",
        ):
            self.assertIn(marker, text)

        self.assertIn("same evidence family", text)
        self.assertIn("同一证据家族", text)
        self.assertIn("C1 object crosswalk: blocked", text)
        self.assertIn("separately opened in one acquisition attempt", text)
        self.assertNotIn("independently opened", text)
        self.assertNotIn("identity_confirmed", text)

    def test_machine_support_records_success_and_failed_rerun(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        routes = record["digital_archive_routes"]
        self.assertEqual(routes["rubbing_record"]["size_bytes"], 27015)
        self.assertEqual(
            routes["rubbing_record"]["sha256"],
            "00921964c0bbf0e391830f53bbc82c4b5bec50b36fc6243984462a6a9b0919e2",
        )
        self.assertEqual(routes["rubbing_image"]["size_bytes"], 69781)
        self.assertEqual(routes["rubbing_image"]["pixels"], "366x500")
        self.assertEqual(
            routes["rubbing_image"]["sha256"],
            "1264db7947ec39474d3c76a19ff58dc5f9ab7bf55499834fbebfcc4ffadb6b48",
        )
        self.assertEqual(routes["crosswalk_status"], "candidate_not_confirmed")
        self.assertEqual(routes["root_rerun"]["response_scope"], "access_block_page")
        self.assertEqual(record["claim_gate_review"]["c1_object_identity"], "blocked")

    def test_human_dossier_is_within_line_limit(self):
        text = (OBJECT / "10_digital-archive-rubbing-crosswalk.md").read_text(
            encoding="utf-8"
        )
        violations = [
            (number, len(line))
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
