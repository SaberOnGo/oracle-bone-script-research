import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "002_coll-obj-cand-00002_ihp-item-1214_collection-object-candidate"
)
GATE = OBJECT / "19_claim-evidence-gate-review.md"


class IhpItem1214ClaimGateTests(unittest.TestCase):
    def setUp(self):
        self.gate_text = GATE.read_text(encoding="utf-8-sig")

    def test_gate_is_linked_from_object_entries(self):
        self.assertTrue(GATE.exists())
        readme = (OBJECT / "README.md").read_text(encoding="utf-8-sig")
        dossier = (OBJECT / "06_human-collection-dossier.md").read_text(
            encoding="utf-8-sig"
        )
        opening = (OBJECT / "16_preformal-research-start-check.md").read_text(
            encoding="utf-8-sig"
        )
        index = json.loads(
            (OBJECT / "07_collection-dossier-index.json").read_text(
                encoding="utf-8-sig"
            )
        )
        for text in (readme, dossier, opening):
            self.assertIn("19_claim-evidence-gate-review.md", text)
        self.assertIn(
            "19_claim-evidence-gate-review.md",
            "\n".join(index["human_readable_files"]),
        )
        self.assertEqual(index["updated_at"], "2026-08-21")

    def test_gate_separates_source_text_image_and_claim_status(self):
        required = (
            "E1",
            "E2",
            "E3",
            "1214",
            "R038861",
            "Jia Bian 0959",
            "今夕又（有）",
            "□子（巳）卜，□□亡。",
            "C1 collection object identity",
            "C2 direct visual surfaces",
            "C4 inscription occurrence and context",
            "C5 transcription or OCR",
            "C6 reading or semantic interpretation",
            "C8 user-facing candidate delivery",
            "source_reported_partial_text",
            "abstain_withhold_candidate",
            "metadata_only_until_verified",
            "破译结果",
        )
        for value in required:
            self.assertIn(value, self.gate_text)
        self.assertNotIn("confirmed reading", self.gate_text.lower())
        self.assertNotIn("probability=1", self.gate_text.lower())

    def test_gate_is_bilingual_and_within_line_width(self):
        self.assertIn("Evidence families", self.gate_text)
        self.assertIn("证据家族", self.gate_text)
        self.assertIn("Claim Dispositions", self.gate_text)
        self.assertIn("命题处置", self.gate_text)
        long_lines = [
            (number, len(line))
            for number, line in enumerate(self.gate_text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], long_lines)


if __name__ == "__main__":
    unittest.main()
