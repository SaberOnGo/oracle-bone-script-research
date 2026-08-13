import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_README = ROOT / "corpus/008_relationship-graph/README.md"
OVERRIDE = (
    ROOT
    / "project_registry/004_asset-source-and-rights-index/"
    / "006_obimd-rights-status-override.csv"
)
DECISION = (
    ROOT
    / "corpus/006_research-sources-and-bibliography/001_source-objects/"
    / "016_src-obimd_source-object/25_effective-rights-decision.md"
)


class GraphEffectiveRightsBoundaryTests(unittest.TestCase):
    def test_graph_entry_points_resolve_legacy_obimd_rights(self):
        text = GRAPH_README.read_text(encoding="utf-8")
        for marker in (
            "OBIMD Rights Resolution / OBIMD 权利状态解析",
            "licensed_for_repository",
            "obimd-rights-resolution.md",
            "metadata_only_until_verified",
            "not a redistribution grant",
            "不能授权复制图像",
        ):
            self.assertIn(marker, text)

    def test_active_override_covers_graph_consumers(self):
        with OVERRIDE.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        by_scope = {row["scope_type"]: row for row in rows}
        for scope in ("asset_source_index", "component_staging"):
            self.assertIn(scope, by_scope)
            self.assertEqual(
                by_scope[scope]["effective_status"],
                "metadata_only_until_verified",
            )
        self.assertGreaterEqual(
            DECISION.read_text(encoding="utf-8").count(
                "metadata_only_until_verified"
            ),
            1,
        )

    def test_graph_edges_remain_candidate_routes(self):
        for relative in (
            "corpus/008_relationship-graph/"
            "006_obimd-component-graph-edges.jsonl",
            "corpus/008_relationship-graph/"
            "014_character-variant-graph-edges.jsonl",
            "corpus/008_relationship-graph/"
            "011_component-asset-graph-edges.jsonl",
        ):
            path = ROOT / relative
            rows = [
                line
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertTrue(rows, relative)
            self.assertTrue(
                all(
                    "not" in line.lower()
                    and (
                        "component" in line.lower()
                        or "variant" in line.lower()
                        or "decipherment" in line.lower()
                    )
                    for line in rows[:20]
                ),
                relative,
            )


if __name__ == "__main__":
    unittest.main()
