import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/004_graph-edge-schema/graph-edge.schema.json"
GRAPH_README = ROOT / "corpus/008_relationship-graph/README.md"


class GraphConfidenceBoundaryTests(unittest.TestCase):
    def test_schema_separates_route_confidence_and_probability(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        properties = schema["properties"]
        self.assertIn("route_integrity_confidence", properties)
        self.assertIn("hypothesis_probability", properties)
        self.assertIn("hypothesis_probability_status", properties)
        self.assertIn("hypothesis_calibration_ref", properties)
        self.assertEqual(properties["hypothesis_probability"]["minimum"], 0)
        self.assertEqual(properties["hypothesis_probability"]["maximum"], 1)
        self.assertIn("never a", properties["confidence_level"]["description"])
        self.assertIn(
            "calibrated task-specific probability",
            properties["hypothesis_probability"]["description"],
        )

    def test_graph_readme_states_the_same_boundary(self):
        text = GRAPH_README.read_text(encoding="utf-8")
        for marker in (
            "Confidence boundary",
            "route_integrity_confidence",
            "hypothesis_probability",
            "hypothesis_probability_status",
            "不是概率",
            "任务级校准",
        ):
            self.assertIn(marker, text)
        self.assertIn("not a probability", text)


if __name__ == "__main__":
    unittest.main()
