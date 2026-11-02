"""Tests for the scholarly relationship graph (architecture reset step 6)."""

import csv
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "corpus/008_relationship-graph/100_scholarly-graph"
TOOL = ROOT / "tools/009_scholarly-graph/build_scholarly_graph.py"

spec = importlib.util.spec_from_file_location("scholarly_graph", TOOL)
graph = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(graph)

REQUIRED = {"edge_type", "source", "target", "source_ref", "status", "note", "edge_id"}
PUBLIC_TYPES = {"dataset_label", "same_character_candidate", "catalog_clue", "co_occurs"}


def read_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


class EdgeShapeTests(unittest.TestCase):
    def test_edge_helper_sets_required_fields(self):
        record = graph.edge("co_occurs", "a", "b", "ref", "candidate", "n", count=3)
        self.assertTrue(REQUIRED <= set(record))
        self.assertEqual(record["edge_id"], "co_occurs:a->b")
        self.assertEqual(record["count"], 3)


class PublicGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identity = read_jsonl(GRAPH / "001_character-identity-edges.jsonl")
        cls.cooccur = read_jsonl(GRAPH / "002_glyph-cooccurrence-edges.jsonl")

    def test_every_public_edge_has_source_and_status(self):
        for record in self.identity + self.cooccur:
            self.assertTrue(REQUIRED <= set(record), record)
            self.assertTrue(record["source_ref"], record)
            self.assertIn(record["edge_type"], PUBLIC_TYPES)

    def test_public_graph_has_no_position_level_occurrences(self):
        for record in self.identity + self.cooccur:
            self.assertNotEqual(record["edge_type"], "occurs_in")
            self.assertNotIn("position", record)

    def test_dataset_labels_come_from_the_official_table(self):
        labels = {r["hust_category"]: r["target"] for r in self.identity if r["edge_type"] == "dataset_label"}
        self.assertEqual(labels.get("0111"), "九")
        self.assertEqual(labels.get("0001"), "㐁")
        self.assertNotIn("⺀", labels.values())

    def test_cooccurrence_respects_minimum_and_has_counts(self):
        self.assertTrue(self.cooccur)
        self.assertTrue(all(r["count"] >= 5 for r in self.cooccur))
        top = self.cooccur[0]
        self.assertEqual({top["source_text"], top["target_text"]}, {"貞", "卜"})

    def test_candidate_edges_are_not_marked_confirmed(self):
        for record in self.identity:
            if record["edge_type"] == "same_character_candidate":
                self.assertEqual(record["status"], "candidate")
                self.assertIn("unchecked", record["note"])

    def test_summary_matches_edge_files(self):
        with (GRAPH / "000_edge-summary.csv").open(encoding="utf-8") as handle:
            rows = {(r["edge_type"], r["status"]): int(r["count"]) for r in csv.DictReader(handle)}
        self.assertEqual(rows[("co_occurs", "source_derived_count")], len(self.cooccur))
        identity_total = sum(v for (k, _), v in rows.items() if k in PUBLIC_TYPES - {"co_occurs"})
        self.assertEqual(identity_total, len(self.identity))

    def test_invalid_legacy_edges_are_removed(self):
        legacy = ROOT / "corpus/008_relationship-graph"
        self.assertFalse((legacy / "005_hust-obc-candidate-graph-edges.jsonl").exists())
        self.assertFalse((legacy / "010_cross-source-id-graph-edges.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
