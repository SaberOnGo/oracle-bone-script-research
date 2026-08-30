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
RECORD = OBJECT / "90_source-record.json"


class ObimdH2NlcCustodialPublicationTests(unittest.TestCase):
    def record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def test_nlc_evidence_is_classified_as_custodial_publication(self):
        nlc = self.record()["national_library_evidence"]
        self.assertEqual(nlc["publication_author"], "Zhao Aixue")
        self.assertEqual(
            nlc["institution_role"],
            "object_custodian_and_official_publication_provider",
        )
        self.assertEqual(
            nlc["direct_custodial_fact"],
            "NLC_oracle_bone_14427_is_Heji_2_and_is_shown_in_figure_3",
        )
        self.assertEqual(
            nlc["claim_effect"],
            "institution_bearing_anchor_strengthens_C1_but_does_not_promote_it",
        )
        self.assertEqual(
            nlc["remaining_blocker"],
            "physical_object_item_identifier_dimensions_material_and_collection_history_missing",
        )
        self.assertEqual(nlc["image_commit_status"], "not_committed_rights_restricted")

    def test_c1_contract_replaces_obsolete_institution_blocker(self):
        record = self.record()
        c1 = record["per_claim_contract"]["C1"]
        self.assertEqual(c1["state"], "candidate_route")
        items = {item["id"]: item for item in c1["evidence_items"]}
        self.assertEqual(
            items["ev-h2-nlc-fig3"]["evidence_role"],
            "institution_custodial_publication_object_image_and_catalog_mapping",
        )
        self.assertIn("item-level", c1["blocker"])
        self.assertNotIn("no institution-bearing", c1["blocker"])
        self.assertEqual(c1["delivery_state"], "withhold")

        contract = record["claim_recording_contract"]
        self.assertIn("item-level", contract["blocker"])
        self.assertNotIn("no institution-bearing", contract["blocker"])
        self.assertIn("14427", contract["next_source"])

    def test_human_adjudication_is_linked_and_keeps_rights_boundary(self):
        page = PAGE.read_text(encoding="utf-8")
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn(PAGE.name, readme)
        for marker in (
            "custodial publication",
            "保管机构出版物",
            "国图甲骨 14427",
            "《甲骨文合集》2",
            "figure 3",
            "图 3",
            "C1",
            "candidate_route",
            "not commit",
            "不提交",
        ):
            self.assertIn(marker, page)

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
