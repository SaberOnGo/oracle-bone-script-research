"""Tests for the OBIMD inscription text layer tools (architecture reset step 4)."""

import csv
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools" / "008_inscription-text-layer"
sys.path.insert(0, str(TOOLS))


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


layer = load("build_obimd_inscription_text_layer")
attach = load("attach_obimd_evidence_to_dossiers")

FIXTURE = [
    {
        "Facsimile": "facsimile/h00007.jpg",
        "Rubbing": "rubbing/h00007.jpg",
        "RubbingName": "H7",
        "RecordUtilSentenceGroupVoList": [
            {
                "GroupCategory": "InscriptionSentence1",
                "RecordUtilOracleCharVoList": [
                    {"Position": "1,1,1,1", "OrderNumber": "2", "SeatFont": 0, "Mark": -1, "Label": "u-zhen"},
                    {"Position": "1,1,1,1", "OrderNumber": "0", "SeatFont": 0, "Mark": -1, "Label": "u-gui"},
                    {"Position": "1,1,1,1", "OrderNumber": "1", "SeatFont": 0, "Mark": -1, "Label": "u-bu"},
                    {"Position": "1,1,1,1", "OrderNumber": "3", "SeatFont": 1, "Mark": -1, "Label": None},
                    {"Position": "1,1,1,1", "OrderNumber": "4", "SeatFont": 0, "Mark": -1, "Label": "u-wang"},
                ],
            },
            {
                "GroupCategory": "OracleSequence1",
                "RecordUtilOracleCharVoList": [
                    {"Position": "1,1,1,1", "OrderNumber": "0", "SeatFont": 0, "Mark": -1, "Label": "u-yi"},
                ],
            },
        ],
    },
    {
        "Facsimile": "facsimile/h00002.jpg",
        "Rubbing": "rubbing/h00002.jpg",
        "RubbingName": "H2",
        "RecordUtilSentenceGroupVoList": [
            {
                "GroupCategory": "InscriptionSentence1",
                "RecordUtilOracleCharVoList": [
                    {"Position": "1,1,1,1", "OrderNumber": "0", "SeatFont": 0, "Mark": -1, "Label": "u-wang"},
                    {"Position": "1,1,1,1", "OrderNumber": "1", "SeatFont": 0, "Mark": -1, "Label": "u-zhen"},
                    {"Position": "1,1,1,1", "OrderNumber": "2", "SeatFont": 0, "Mark": -1, "Label": "u-pua"},
                    {"Position": "1,1,1,1", "OrderNumber": "3", "SeatFont": 0, "Mark": -1, "Label": "u-bu"},
                ],
            },
        ],
    },
]
MAIN = {"u-gui": "癸", "u-bu": "卜", "u-zhen": "貞", "u-wang": "王", "u-yi": "一", "u-pua": "\U000FFB45"}


class TextLayerTests(unittest.TestCase):
    def test_groups_follow_reading_order_and_plate_order(self):
        groups = layer.build_groups(FIXTURE, MAIN)
        self.assertEqual([g["plate"] for g in groups], ["H2", "H7", "H7"])
        self.assertEqual(groups[1]["text"], "癸卜貞□王")
        self.assertEqual(groups[1]["category"], "InscriptionSentence")
        self.assertEqual(groups[2]["category"], "OracleSequence")
        self.assertTrue(groups[1]["chars"][3]["placeholder"])
        self.assertEqual(groups[0]["heji_candidate"], "2")

    def test_plate_sort_key_is_numeric(self):
        names = sorted(["H100", "H20", "H3"], key=layer.plate_sort_key)
        self.assertEqual(names, ["H3", "H20", "H100"])

    def test_display_text_hides_nonstandard_codepoints(self):
        self.assertEqual(layer.display_text("王\U000FFB45\U000BEBB7貞"), "王◇◇貞◇")
        self.assertEqual(layer.display_text("癸未卜"), "癸未卜")

    def test_statistics_count_occurrences_and_cooccurrence(self):
        groups = layer.build_groups(FIXTURE, MAIN)
        rows = {r["obimd_main_uid"]: r for r in layer.glyph_statistics(groups, MAIN)}
        self.assertEqual(rows["u-zhen"]["occurrences"], 2)
        self.assertEqual(rows["u-zhen"]["plates"], 2)
        self.assertIn("王:u-wang:2", rows["u-zhen"]["top_cooccurring"])
        self.assertEqual(rows["u-pua"]["transcription"], "◇")
        self.assertEqual(rows["u-yi"]["oracle_sequence"], 1)

    def test_plate_index_counts_placeholders(self):
        groups = layer.build_groups(FIXTURE, MAIN)
        rows = {r["obimd_plate"]: r for r in layer.plate_index(groups)}
        self.assertEqual(rows["H7"]["sentence_groups"], 2)
        self.assertEqual(rows["H7"]["unidentified_or_placeholder"], 1)


class AttachTests(unittest.TestCase):
    def test_examples_skip_short_groups_and_limit_count(self):
        groups = layer.build_groups(FIXTURE, MAIN)
        index = {}
        for group in groups:
            for position, char in enumerate(group["chars"], 1):
                if char["uid"]:
                    index.setdefault(char["uid"], []).append((group, position))
        summary = attach.summarize(["u-zhen"], index, {})
        self.assertEqual(summary["occurrences"], 2)
        self.assertEqual([e["plate"] for e in summary["examples"]], ["H2", "H7"])
        self.assertLessEqual(len(summary["examples"]), attach.MAX_EXAMPLES)
        self.assertEqual(summary["examples"][0]["text"], "王貞◇卜")

    def test_render_and_insert_sections_are_idempotent(self):
        summary = {
            "occurrences": 3, "plates": 2, "plate_list_head": ["H2", "H7"],
            "by_category": {"卜辞句": 3}, "top_cooccurring": [{"text": "卜", "uid": "u", "count": 2}],
            "examples": [{"plate": "H2", "group_index": 1, "text": "王貞卜", "position": 2, "length": 3}],
        }
        base = "# x\n\n## 2 隶定与今字候选\n\n- a\n\n## 10 来源与权利\n\n- b\n"
        once = attach.insert_sections(base, attach.render(summary))
        twice = attach.insert_sections(once, attach.render(summary))
        self.assertEqual(once, twice)
        self.assertLess(once.index("## 4 卜辞例句"), once.index("## 5 分布"))
        self.assertLess(once.index("## 5 分布"), once.index("## 10 来源与权利"))


class PublicOutputTests(unittest.TestCase):
    STATS = ROOT / "corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv"

    def test_public_statistics_carry_no_sentence_text(self):
        with self.STATS.open(encoding="utf-8") as handle:
            header = next(csv.reader(handle))
        self.assertNotIn("text", header)
        self.assertIn("rights_status", header)

    def test_local_corpus_is_ignored_by_git(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("external_local_archive/", gitignore)

    def test_dossiers_quote_at_most_two_examples(self):
        checked = 0
        for path in sorted((ROOT / "corpus/001_oracle-characters").glob("00[1-3]_*/*/record.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            evidence = record.get("inscription_evidence")
            if evidence:
                checked += 1
                self.assertLessEqual(len(evidence["examples"]), attach.MAX_EXAMPLES)
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()
