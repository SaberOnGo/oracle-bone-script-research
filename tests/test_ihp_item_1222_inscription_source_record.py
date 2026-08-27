from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "010_obs-insc-src-cand-000010_ihp-item-1222_source-record-candidate"
)
PARENT = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches/"
    "002_collection-object-candidates/"
    "008_coll-obj-cand-00008_ihp-item-1222_collection-object-candidate"
)


class IhpItem1222InscriptionSourceRecordTests(unittest.TestCase):
    def test_human_dossier_precedes_machine_support(self):
        human = sorted(CANDIDATE.glob("*.md"))
        support = sorted(CANDIDATE.glob("*.json")) + sorted(
            CANDIDATE.glob("*.csv")
        )
        self.assertGreaterEqual(len(human), 9)
        self.assertEqual(len(support), 3)
        self.assertTrue((CANDIDATE / "02_human-inscription-dossier.md").is_file())
        self.assertTrue((CANDIDATE / "90_source-record.json").is_file())

    def test_human_files_are_bilingual_readable_and_concrete(self):
        required = (
            "metadata_only_until_verified",
            "source-record candidate",
            "来源记录候选",
        )
        joined = ""
        for path in CANDIDATE.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            joined += text
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("not_collected", text)
            for number, line in enumerate(text.splitlines(), 1):
                self.assertLessEqual(
                    len(line), 80, f"{path}:{number}:{len(line)}"
                )
        for marker in required:
            self.assertIn(marker, joined)
        self.assertIn("Yi Bian 4817+5061+5520+5804+6087+R60751", joined)
        self.assertIn("rendered glyph response", joined)
        self.assertIn("页面渲染字形响应", joined)
        self.assertIn("counterevidence", joined)
        self.assertIn("反证", joined)

    def test_support_record_preserves_routes_and_withholds_claims(self):
        packet = json.loads(
            (CANDIDATE / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(packet["candidate_id"], "obs-insc-src-cand-000010")
        self.assertEqual(packet["museum_item"], "1222")
        self.assertEqual(packet["museum_accession"], "ZR038421")
        self.assertEqual(packet["formal_inscription_identity"], "withheld")
        self.assertEqual(packet["character_links"], [])
        self.assertEqual(packet["rights_status"], "metadata_only_until_verified")
        self.assertEqual(packet["delivery_state"], "abstain_withhold_candidate")
        self.assertEqual(len(packet["large_image_routes"]), 2)
        self.assertEqual(len(packet["inline_glyph_response_routes"]), 3)
        for route in packet["inline_glyph_response_routes"]:
            self.assertEqual(route["evidence_type"], "rendered_glyph_response")
            self.assertEqual(route["bone_surface_location"], "unmapped")

    def test_support_index_names_concrete_missing_questions(self):
        with (CANDIDATE / "91_source-record-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["candidate_id"], "obs-insc-src-cand-000010")
        self.assertEqual(row["formal_identity_status"], "withheld")
        self.assertEqual(row["character_link_status"], "withheld_no_mapping")
        self.assertIn("catalog page and plate locators", row["missing_evidence"])
        self.assertNotIn("not_collected", ";".join(row.values()))

    def test_candidate_links_parent_checksum_bound_evidence(self):
        readme = (CANDIDATE / "README.md").read_text(encoding="utf-8")
        parent_evidence = PARENT / "19_official-page-text-evidence.md"
        self.assertTrue(parent_evidence.is_file())
        self.assertIn("19_official-page-text-evidence.md", readme)
        self.assertIn("d59a6cbd401daf184880e58a7aa826e310bc2ee481f71a91a4aa2f3d18ac45bf", readme)


if __name__ == "__main__":
    unittest.main()
