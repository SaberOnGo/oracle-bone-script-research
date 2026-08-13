from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)
GRAPH = ROOT / "corpus/008_relationship-graph/"
GRAPH_FILE = GRAPH / "015_character-inscription-candidate-graph-edges.jsonl"


def load_builder():
    path = ROOT / "tools/003_graph-generation/"
    path = path / "build_character_inscription_candidate_graph_edges.py"
    spec = importlib.util.spec_from_file_location("h2_graph_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load H2 graph builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_skeleton_validator():
    path = ROOT / "tools/validation/check_repository_skeleton.py"
    spec = importlib.util.spec_from_file_location("repository_skeleton", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load repository skeleton validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CharacterInscriptionCandidateGraphTests(unittest.TestCase):
    def test_h2_graph_file_has_one_route_per_ordered_occurrence(self):
        rows = [
            json.loads(line)
            for line in GRAPH_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        with (OBJECT / "91_character-occurrence-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as file:
            occurrences = list(csv.DictReader(file))

        self.assertEqual(len(rows), len(occurrences))
        self.assertEqual(
            [row["source_uid"] for row in rows],
            [row["source_uid"] for row in occurrences],
        )
        self.assertEqual(
            [row["source_node_id"] for row in rows],
            [row["candidate_project_id"] for row in occurrences],
        )
        self.assertTrue(
            all(
                row["target_node_id"] == "obs-insc-src-cand-000001"
                for row in rows
            )
        )

    def test_h2_edges_keep_candidate_and_rights_boundaries(self):
        rows = [
            json.loads(line)
            for line in GRAPH_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in rows:
            self.assertEqual(
                row["edge_type"],
                "CHARACTER_HAS_INSCRIPTION_SOURCE_RECORD_CANDIDATE",
            )
            self.assertEqual(row["candidate_route_status"], "dataset_candidate_not_promoted")
            self.assertEqual(row["identity_claim_status"], "no_identity_claim")
            self.assertEqual(row["review_status"], "needs_human_inscription_review")
            self.assertEqual(row["confidence_level"], "unknown")
            self.assertEqual(row["rights_status"], "metadata_only_until_verified")
            self.assertIn("not a decipherment conclusion", row["evidence_note"])
            self.assertIn("not a confirmed character identity", row["evidence_note"])
            self.assertIn("source_record_path", row)
            self.assertTrue(
                str(row["source_record_path"]).endswith("90_source-record.json")
            )

    def test_builder_reproduces_committed_routes(self):
        module = load_builder()
        record = json.loads((OBJECT / "90_source-record.json").read_text(encoding="utf-8"))
        with (OBJECT / "91_character-occurrence-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as file:
            occurrences = list(csv.DictReader(file))
        rebuilt = module.build_edges(record, occurrences)
        committed = [
            json.loads(line)
            for line in GRAPH_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(rebuilt, committed)

    def test_h2_readme_exposes_the_human_graph_route(self):
        text = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("09_character-inscription-candidate-graph-route.md", text)

    def test_repository_gate_validates_the_candidate_graph(self):
        validator = load_skeleton_validator()
        self.assertEqual(
            validator.check_character_inscription_candidate_graph(ROOT), []
        )


if __name__ == "__main__":
    unittest.main()
