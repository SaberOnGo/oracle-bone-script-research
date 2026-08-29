import csv
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
DOSSIER = OBJECT / "11_text-scope-and-box-alignment-adjudication.md"
INDEX = OBJECT / "91_character-occurrence-index.csv"
RECORD = OBJECT / "90_source-record.json"
EXPECTED_LABELS = ["曰", "協", "田", "其", "受", "年", "U+FFB45"]
EXPECTED_SOURCE_VALUES = ["曰", "𫩻|򧅇|協", "田", "其", "受", "年", "十一月"]


class ObimdH2TextScopeAdjudicationTests(unittest.TestCase):
    def test_occurrence_index_preserves_source_label_routes_and_withholding(self):
        rows = list(csv.DictReader(INDEX.read_text(encoding="utf-8").splitlines()))
        self.assertEqual(
            [row["source_reported_label_route"] for row in rows],
            EXPECTED_LABELS,
        )
        self.assertEqual(
            [row["source_reference_modern_values"] for row in rows],
            EXPECTED_SOURCE_VALUES,
        )
        self.assertTrue(
            all(row["raw_source_field_name"] == "transcription_values" for row in rows)
        )
        self.assertTrue(
            all(
                row["reading_delivery_status"].startswith("withheld_")
                for row in rows
            )
        )
        self.assertEqual(
            rows[-1]["alignment_status"],
            "pua_glyph_codepoint_multi_character_reference_warning_withheld",
        )

    def test_machine_record_keeps_catalog_paper_and_claim_gate_boundaries(self):
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        catalog = record["heji_material_source_evidence"]
        self.assertEqual(catalog["heji_plate"], "2")
        self.assertEqual(catalog["earliest_catalog_route"], "粹866")
        self.assertEqual(catalog["selected_route"], "善9025")
        self.assertEqual(catalog["holding_route"], "北圖")
        paper = record["published_same_text_evidence"]
        self.assertIn("Heji 2 and Heji 5", paper["claim"])
        self.assertIn("not Heji 2", paper["scope_boundary"])
        route_evidence = record["box_label_route_evidence"]
        self.assertEqual(
            [row["download_id"] for row in route_evidence["downloads"]],
            ["dl-obimd-subchar-main-mapping", "dl-obimd-main-character-json"],
        )
        self.assertEqual(
            record["box_label_alignment"][-1]["source_reference_modern_values"],
            "十一月",
        )
        decision = record["claim_gate_decision"]
        self.assertEqual(decision["C1"], "candidate_route")
        self.assertEqual(decision["C2"], "direct_checked")
        self.assertEqual(decision["C3"], "not_asserted_not_applicable")
        self.assertEqual(decision["C4"], "candidate_route")
        self.assertEqual(decision["C5"], "blocked")
        self.assertEqual(decision["C6"], "blocked")
        self.assertEqual(decision["C6_blocked_by"], "C5")
        self.assertEqual(
            decision["C7"], "not_applicable_no_diachronic_proposition"
        )
        self.assertEqual(decision["C8"], "withhold")
        self.assertEqual(decision["delivery_action"], "abstain")
        self.assertIn("no_task_specific_calibration", decision["probability_status"])

        contract = record["per_claim_contract"]
        self.assertEqual(set(contract), {"C1", "C2", "C4", "C5", "C6", "C8"})
        required = {
            "state",
            "evidence_items",
            "family_ids",
            "shared_ancestor",
            "blocker",
            "impact",
            "next_source_question",
            "alternative",
            "falsifier",
            "abstention_reason",
            "delivery_state",
            "version",
            "adjudication_path",
        }
        allowed_states = {
            "route_only",
            "source_reported",
            "direct_checked",
            "independently_corroborated",
            "calibrated_support",
        }
        evidence_states = {}
        for claim_id, claim in contract.items():
            self.assertTrue(required <= set(claim), claim_id)
            self.assertEqual(claim["delivery_state"], "withhold", claim_id)
            self.assertEqual(claim["version"], "2026-08-30-h2-text-scope-v1")
            self.assertIn("#claim-recording-contract", claim["adjudication_path"])
            for field in (
                "shared_ancestor",
                "blocker",
                "impact",
                "next_source_question",
                "alternative",
                "falsifier",
                "abstention_reason",
            ):
                self.assertTrue(claim[field], f"{claim_id}:{field}")
            for evidence in claim["evidence_items"]:
                self.assertEqual(
                    set(evidence),
                    {"id", "state", "family_id", "evidence_role"},
                )
                self.assertTrue(evidence["id"], claim_id)
                self.assertIn(evidence["state"], allowed_states)
                self.assertTrue(evidence["evidence_role"], claim_id)
                self.assertIn(evidence["family_id"], claim["family_ids"])
                previous = evidence_states.setdefault(
                    evidence["id"], evidence["state"]
                )
                self.assertEqual(previous, evidence["state"], evidence["id"])

    def test_object_local_record_binds_all_three_source_captures(self):
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        catalog = record["heji_material_source_evidence"]
        self.assertEqual(catalog["response_size_bytes"], 2337)
        self.assertEqual(
            catalog["response_sha256"],
            "3181ca77e710c733f7c9b1c81e83f1d69935b2076560f92c62c21b8c825cacba",
        )
        self.assertTrue(catalog["url"].startswith("https://xiaoxue."))
        paper = record["published_same_text_evidence"]
        self.assertEqual(paper["page_22_size_bytes"], 644706)
        self.assertEqual(paper["page_23_size_bytes"], 616833)
        self.assertTrue(paper["page_22_url"].startswith("https://img.dpm.org.cn/"))
        self.assertTrue(paper["page_23_url"].startswith("https://img.dpm.org.cn/"))
        self.assertEqual(paper["provider"], "The Palace Museum")
        self.assertEqual(paper["access_date"], "2026-08-28")
        self.assertEqual(
            paper["source_registration_status"],
            "object_local_pending_global_source_registration",
        )
        self.assertIn("tmp/source_downloads/", paper["page_22_local_ignored_path"])
        self.assertIn("tmp/source_downloads/", paper["page_23_local_ignored_path"])
        self.assertIn("checksum", paper["public_commit_decision"])
        nlc = record["national_library_evidence"]
        self.assertEqual(nlc["access_date"], "2026-08-28")
        self.assertIn("tmp/source_downloads/", nlc["local_ignored_path"])
        self.assertEqual(catalog["access_date"], "2026-08-28")
        self.assertIn("tmp/source_downloads/", catalog["local_ignored_path"])
        bibliography = record["bibliographic_locator_evidence"]
        self.assertEqual(bibliography["source_name"], "CiNii Books")
        self.assertEqual(bibliography["ncid"], "BN05177578")
        self.assertEqual(
            bibliography["evidence_state"],
            "source_reported_bibliographic_metadata",
        )

    def test_nlc_and_xiaoxuetang_downloads_join_manifest_and_log(self):
        manifest_path = (
            ROOT
            / "corpus/006_research-sources-and-bibliography/"
            "000_source-registers/003_source-download-manifest.csv"
        )
        log_path = (
            ROOT
            / "project_registry/006_large-source-register/"
            "002_source-download-log.csv"
        )
        manifest = {
            row["download_id"]: row
            for row in csv.DictReader(
                manifest_path.read_text(encoding="utf-8-sig").splitlines()
            )
        }
        log = {
            row["download_id"]: row
            for row in csv.DictReader(
                log_path.read_text(encoding="utf-8-sig").splitlines()
            )
        }
        for download_id in (
            "dl-nlc-wenjin-heji2-20260828",
            "dl-xxt-obm-heji2-query-20260828",
        ):
            self.assertIn(download_id, manifest)
            self.assertIn(download_id, log)
            self.assertEqual(manifest[download_id]["source_id"], log[download_id]["source_id"])
            self.assertEqual(manifest[download_id]["url"], log[download_id]["url"])

    def test_human_dossier_is_bilingual_bounded_and_readable(self):
        text = DOSSIER.read_text(encoding="utf-8")
        for phrase in (
            "## English",
            "## 简体中文",
            "source-metadata alignment\ncandidate",
            "数据集元数据对齐",
            "same-text inscriptions",
            "同文卜辞",
            "U+FFB45",
            "十一月",
            "delivery is `withhold`; action is `abstain`",
            "Claim recording contract",
            "主张记录合同",
            "2026-08-30-h2-text-scope-v1",
            "不显示\n任何数值概率",
            "plate 2, not an invented page number",
            "不得编造页码",
        ):
            self.assertIn(phrase, text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), start=1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
