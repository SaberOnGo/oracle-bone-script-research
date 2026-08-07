import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools/004_statistics-generation/"
    "build_component_visual_observation_coverage_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
    "build_component_visual_visual_observation_coverage_audit", MODULE_PATH
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ComponentVisualObservationCoverageTests(unittest.TestCase):
    def make_object(
        self,
        root: Path,
        object_name: str,
        image: bool,
        observation: str,
    ) -> None:
        object_dir = (
            root
            / "corpus/003_graphemic-components/001_000001-000100_obs-comp-cand-bucket"
            / object_name
        )
        object_dir.mkdir(parents=True)
        (object_dir / "01_candidate-component-packet.json").write_text(
            json.dumps(
                {
                    "candidate_component_id": object_name.split("_")[1],
                    "rights_status": "licensed_for_repository",
                    "review_status": "needs_human_component_review",
                }
            ),
            encoding="utf-8",
        )
        header = (
            "visual_index_id,candidate_component_id,asset_id,rights_status,"
            "review_status,local_asset_path\n"
        )
        row = (
            "visual-1,obs-comp-cand-000001,asset-1,licensed_for_repository,"
            "needs_human_visual_review,corpus/image.png\n"
            if image
            else ""
        )
        (object_dir / "06_component-visual-index.csv").write_text(
            header + row,
            encoding="utf-8",
        )
        (object_dir / "18_material-visual-observation.md").write_text(
            observation,
            encoding="utf-8",
        )

    def test_rows_separate_pixel_profiles_and_missing_image_routes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_object(
                root,
                "001_obs-comp-cand-000001_test_component-candidate",
                True,
                "# Material Visual Observation\n\n"
                "## Direct Visual Record / 直接可见记录\n\n"
                "Image profile: 10 × 10 px\n"
                "图像 profile：10 × 10 像素\n\n"
                "## Boundary / 边界\n",
            )
            second = (
                root
                / "corpus/003_graphemic-components/001_000001-000100_obs-comp-cand-bucket"
                / "002_obs-comp-cand-000002_test_component-candidate"
            )
            second.mkdir(parents=True)
            (second / "01_candidate-component-packet.json").write_text(
                json.dumps({"candidate_component_id": "obs-comp-cand-000002"}),
                encoding="utf-8",
            )
            (second / "06_component-visual-index.csv").write_text(
                "visual_index_id,candidate_component_id,asset_id,rights_status,"
                "review_status,local_asset_path\n",
                encoding="utf-8",
            )
            (second / "18_material-visual-observation.md").write_text(
                "# Material Visual Observation\n\n"
                "## Direct Visual Record / 直接可见记录\n\n"
                "No local PNG/JPEG asset is currently registered.\n"
                "没有登记的本地 PNG/JPEG 资料。\n\n"
                "## Boundary / 边界\n",
                encoding="utf-8",
            )
            rows = MODULE.build_rows(root)
            by_id = {row["project_id"]: row for row in rows}
            self.assertEqual(
                by_id["obs-comp-cand-000001"]["visual_observation_status"],
                "pixel_profile_and_boundary_present",
            )
            self.assertEqual(
                by_id["obs-comp-cand-000002"]["visual_observation_status"],
                "missing_image_route_and_boundary_present",
            )

    def test_report_is_bilingual_and_wrapped(self) -> None:
        report = MODULE.build_report(
            [
                {
                    "project_id": "obs-comp-cand-000001",
                    "asset_count": "1",
                    "observation_path": "x",
                    "visual_observation_status": "pixel_profile_and_boundary_present",
                }
            ],
            "corpus/009_statistics-and-derived-features/228_component-visual-observation-coverage.csv",
        )
        self.assertLessEqual(max(len(line) for line in report.splitlines()), 80)
        self.assertIn("构件图像观察覆盖审计", report)
        self.assertIn("pixel_profile_and_boundary_present", report)


if __name__ == "__main__":
    unittest.main()
