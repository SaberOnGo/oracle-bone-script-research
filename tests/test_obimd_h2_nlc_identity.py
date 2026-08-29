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
PAGE = OBJECT / "10_nlc-heji2-identity-and-aggregator-mismatch.md"


class ObimdH2NlcIdentityTests(unittest.TestCase):
    def test_human_page_records_candidate_counterevidence_and_falsifiers(self):
        text = PAGE.read_text(encoding="utf-8")
        for marker in (
            "candidate route to *Jiaguwen Heji* 2",
            "国家图书馆甲骨 14427",
            "text-image mismatch",
            "页面级图文错配",
            "strongest alternative",
            "最强替代解释",
            "Falsifiers / 可推翻条件",
            "No percentage is displayed",
            "decipherment effect: none",
        ):
            self.assertIn(marker, text)

    def test_source_receipts_and_machine_record_are_checksum_bound(self):
        text = PAGE.read_text(encoding="utf-8")
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        identity = record["identity_candidate"]
        nlc = record["national_library_evidence"]
        mismatch = record["public_aggregator_mismatch"]
        self.assertEqual(
            identity["result"],
            "candidate_route_heji2_shared_ancestry_audited",
        )
        self.assertEqual(nlc["object_number"], "14427")
        self.assertEqual(nlc["heji_reference"], "Heji 2")
        self.assertEqual(
            nlc["pdf_sha256"],
            "a675739ec1bd43ed83a7b902baad71667d28c378e122d0ee96baab8199c0d0d8",
        )
        self.assertEqual(
            mismatch["html_sha256"],
            "f30fe2e94c631b2bd2accd37b7efdc879131cd50379361b64eaf65f0665b6b10",
        )
        self.assertEqual(
            mismatch["image_sha256"],
            "df8be7e602be409479f38cab78a5217e2e3e60be90d47bb7f0c803179aedfc8f",
        )
        for digest in (
            nlc["pdf_sha256"],
            mismatch["html_sha256"],
            mismatch["image_sha256"],
        ):
            self.assertIn(digest, text)

    def test_rights_boundary_keeps_downloads_out_of_public_object(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            record["identity_candidate"]["probability_status"],
            "not_displayed_no_task_specific_calibration",
        )
        self.assertIn(
            "raw_pdf_not_committed",
            record["national_library_evidence"]["rights_status"],
        )
        image_suffixes = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
        self.assertEqual(
            [p for p in OBJECT.rglob("*") if p.suffix.lower() in image_suffixes],
            [],
        )

    def test_human_page_is_bilingual_and_within_line_limit(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("## Result / 结果", text)
        self.assertIn("## Boundary / 边界", text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
