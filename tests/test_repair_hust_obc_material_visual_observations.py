import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools/002_corpus-import/"
    "repair_hust_obc_material_visual_observations.py"
)
SPEC = importlib.util.spec_from_file_location(
    "repair_hust_obc_material_visual_observations", MODULE_PATH
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RepairHustObcMaterialVisualObservationTests(unittest.TestCase):
    def test_normalizes_existing_follow_up_and_boundary_sections(self) -> None:
        source = (
            "# Record\n\n"
            "Direct Visual Record / 直接可见记录\n\n"
            "- A source-linked image path is deliberately very long and must "
            "be wrapped without losing its route or changing the visible "
            "description.\n\n"
            "Concrete follow-up questions / 具体待查问题：\n"
            "- Which plate contains it?\n\n"
            "Research Boundary / 研究边界\n"
            "- No reading is assigned.\n"
        )
        repaired, details = MODULE.repair_text(source)
        self.assertFalse(details["added_next"])
        self.assertFalse(details["added_boundary"])
        self.assertIn(
            "## Direct Visual Record / 直接可见记录",
            repaired,
        )
        self.assertIn("## Next Checks / 下一步核查", repaired)
        self.assertIn("## Boundary / 边界", repaired)
        self.assertNotIn("Concrete follow-up questions", repaired)
        self.assertNotIn("Research Boundary", repaired)
        self.assertLessEqual(
            max(len(line) for line in repaired.splitlines()),
            80,
        )

    def test_adds_concrete_sections_when_missing(self) -> None:
        source = "# Record\n\n- " + ("visible mark " * 10) + "\n"
        repaired, details = MODULE.repair_text(source)
        self.assertTrue(details["added_next"])
        self.assertTrue(details["added_boundary"])
        self.assertIn("Which catalog entry", repaired)
        self.assertIn("## Boundary / 边界", repaired)
        self.assertLessEqual(
            max(len(line) for line in repaired.splitlines()),
            80,
        )

    def test_repair_scans_only_hust_object_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            object_dir = (
                root
                / "corpus/001_oracle-characters/001_bucket/001_hust-obc-und-X-000001"
            )
            object_dir.mkdir(parents=True)
            note = object_dir / "14_material-visual-observation.md"
            note.write_text("# Record\n", encoding="utf-8")
            result = MODULE.repair(root)
            self.assertEqual(result["scanned"], 1)
            self.assertEqual(result["changed"], 1)
            self.assertIn("Next Checks", note.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
