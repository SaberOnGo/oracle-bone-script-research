from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / (
    "corpus/008_relationship-graph/"
    "017_evobc-evolution-correspondence-candidate-graph-edges.jsonl"
)
CATEGORY = ROOT / (
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
CODEBOOK = ROOT / (
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "002_evobc-era-source-codebook-staging.csv"
)


def load_module(relative_path: str, name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EvoBCEvolutionCorrespondenceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [
            json.loads(line)
            for line in GRAPH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_candidate_route_count_and_category_count(self):
        rows = [
            row
            for row in self.rows
            if row.get("candidate_correspondence_status")
            == "candidate_evolution_correspondence_route"
        ]
        self.assertEqual(len(rows), 5387)
        self.assertEqual(len({row["source_node_id"] for row in rows}), 1583)

    def test_candidate_edges_keep_route_and_scholarship_boundaries(self):
        for row in self.rows:
            self.assertEqual(row["candidate_route_status"], "dataset_candidate_not_promoted")
            self.assertEqual(
                row["confidence_semantics"],
                "hypothesis_probability_not_estimated",
            )
            self.assertEqual(row["identity_claim_status"], "no_identity_claim")
            self.assertEqual(row["rights_status"], "source_marked_risk_noted")
            self.assertIn(
                row["candidate_correspondence_status"],
                {
                    "candidate_evolution_correspondence_route",
                    "dataset_era_metadata_route_only",
                    "dataset_source_metadata_route_only",
                },
            )
            self.assertIn(
                "not a confirmed later-form correspondence",
                row["evidence_note"],
            )

    def test_builder_reproduces_committed_graph(self):
        module = load_module(
            "tools/003_graph-generation/"
            "build_evobc_evolution_correspondence_candidate_graph_edges.py",
            "evobc_evolution_correspondence_graph_builder",
        )
        with CATEGORY.open(encoding="utf-8-sig", newline="") as file:
            category_rows = list(csv.DictReader(file))
        with CODEBOOK.open(encoding="utf-8-sig", newline="") as file:
            codebook_rows = list(csv.DictReader(file))
        self.assertEqual(module.build_edges(category_rows, codebook_rows), self.rows)

    def test_human_audit_index_is_explicitly_non_promoted(self):
        audit = ROOT / (
            "corpus/009_statistics-and-derived-features/"
            "234_evobc-evolution-correspondence-audit.md"
        )
        index = ROOT / (
            "corpus/009_statistics-and-derived-features/"
            "235_evobc-evolution-correspondence-audit-index.json"
        )
        text = audit.read_text(encoding="utf-8")
        data = json.loads(index.read_text(encoding="utf-8"))
        self.assertIn("Formal paleographic correspondences recorded: 0", text)
        self.assertIn("Candidate probabilities: not estimated.", text)
        self.assertEqual(data["mixed_era_category_count"], 1583)
        self.assertEqual(data["candidate_evolution_correspondence_edge_count"], 5387)
        self.assertEqual(data["formal_correspondence_count"], 0)
        self.assertIsNone(data["hypothesis_probability"])
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_repository_audits_pass(self):
        validator = load_module(
            "tools/validation/check_repository_skeleton.py",
            "repository_skeleton_evobc_audit",
        )
        self.assertEqual(
            validator.check_evobc_evolution_correspondence_graph(ROOT), []
        )
        self.assertEqual(
            validator.check_evobc_evolution_correspondence_audit(ROOT), []
        )


if __name__ == "__main__":
    unittest.main()
