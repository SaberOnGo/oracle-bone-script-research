from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GRAPH_FILE = (
    ROOT
    / "corpus/008_relationship-graph/"
    "016_character-component-candidate-graph-edges.jsonl"
)


def load_builder():
    path = ROOT / "tools/003_graph-generation/"
    path = path / "build_character_component_candidate_graph_edges.py"
    spec = importlib.util.spec_from_file_location("component_graph_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load component graph builder")
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


class CharacterComponentCandidateGraphTests(unittest.TestCase):
    def _rows(self):
        return [
            json.loads(line)
            for line in GRAPH_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_graph_has_nineteen_cross_source_candidate_routes(self):
        rows = self._rows()
        self.assertEqual(len(rows), 19)
        self.assertEqual(
            rows[0]["source_node_id"],
            "obs-char-000047",
        )
        self.assertEqual(rows[-1]["source_node_id"], "obs-char-001550")
        self.assertEqual(len({row["target_node_id"] for row in rows}), 19)

    def test_edges_keep_component_and_identity_boundaries(self):
        for row in self._rows():
            self.assertEqual(row["edge_type"], "CHARACTER_HAS_COMPONENT_CANDIDATE")
            self.assertEqual(row["candidate_route_status"], "dataset_candidate_not_promoted")
            self.assertEqual(row["identity_claim_status"], "no_identity_claim")
            self.assertEqual(row["review_status"], "needs_cross_source_review")
            self.assertEqual(row["confidence_level"], "unknown")
            self.assertEqual(row["rights_status"], "metadata_only_until_verified")
            self.assertIn("not a formal component assignment", row["evidence_note"])
            self.assertIn("not a decipherment conclusion", row["evidence_note"])
            self.assertEqual(row["source_ids"], ["src-hust-obc", "src-obimd"])

    def test_builder_reproduces_committed_routes(self):
        module = load_builder()
        crosswalk = list(
            csv.DictReader(
                (
                    ROOT
                    / "corpus/001_oracle-characters/000_character-registers/"
                    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
                ).open(encoding="utf-8-sig", newline="")
            )
        )
        main = list(
            csv.DictReader(
                (
                    ROOT
                    / "corpus/001_oracle-characters/000_character-registers/"
                    "006_obimd-main-character-staging.csv"
                ).open(encoding="utf-8-sig", newline="")
            )
        )
        components = list(
            csv.DictReader(
                (
                    ROOT
                    / "corpus/003_graphemic-components/000_component-registers/"
                    "002_obimd-subcharacter-main-staging.csv"
                ).open(encoding="utf-8-sig", newline="")
            )
        )
        component_map = list(
            csv.DictReader(
                (
                    ROOT
                    / "project_registry/002_project-id-to-source-reference-map/"
                    "004_component-id-source-map.csv"
                ).open(encoding="utf-8-sig", newline="")
            )
        )
        rebuilt = module.build_edges(crosswalk, main, components, component_map)
        self.assertEqual(rebuilt, self._rows())

    def test_repository_gate_validates_the_component_graph(self):
        validator = load_skeleton_validator()
        self.assertEqual(
            validator.check_character_component_candidate_graph(ROOT), []
        )

    def test_human_component_audit_keeps_candidate_boundary(self):
        human_path = (
            ROOT
            / "corpus/009_statistics-and-derived-features/"
            "232_character-component-linkage-audit.md"
        )
        index_path = (
            ROOT
            / "corpus/009_statistics-and-derived-features/"
            "233_character-component-linkage-audit-index.json"
        )
        text = human_path.read_text(encoding="utf-8")
        index = json.loads(index_path.read_text(encoding="utf-8"))
        self.assertIn("19 explicit cross-source candidate", text)
        self.assertIn("not a formal component assignment", text)
        self.assertIn("not a decipherment conclusion", text)
        self.assertEqual(index["candidate_edge_count"], 19)
        self.assertEqual(index["character_candidate_count"], 9)
        self.assertEqual(index["component_candidate_count"], 19)
        self.assertEqual(index["promoted_formal_relation_count"], 0)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))


if __name__ == "__main__":
    unittest.main()
