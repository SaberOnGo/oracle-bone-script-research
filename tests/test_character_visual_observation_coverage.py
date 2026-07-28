import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools/004_statistics-generation/"
    "build_character_visual_observation_coverage_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
    "build_character_visual_observation_coverage_audit", MODULE_PATH
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CharacterVisualObservationCoverageTests(unittest.TestCase):
    def make_object(
        self,
        root: Path,
        object_name: str,
        packet_name: str,
        packet: dict,
        observation: bool,
    ) -> Path:
        object_dir = (
            root
            / "corpus/001_oracle-characters/001_000001-000100_obs-char-bucket"
            / object_name
        )
        asset_dir = object_dir / "03_visual-assets"
        asset_dir.mkdir(parents=True)
        (asset_dir / "001_asset-test_glyph.png").write_bytes(b"image")
        (object_dir / packet_name).write_text(
            json.dumps(packet), encoding="utf-8"
        )
        (object_dir / "02_visual-source-index.csv").write_text(
            "project_id,review_status,rights_status\n"
            f"{object_name.split('_')[1]},needs_human_visual_review,source_marked_risk_noted\n",
            encoding="utf-8",
        )
        if observation:
            (object_dir / "14_material-visual-observation.md").write_text(
                "# Material Visual Observation\n\n"
                "## Direct Visual Record / 直接可见记录\n",
                encoding="utf-8",
            )
        return object_dir

    def test_build_rows_separates_images_and_direct_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_object(
                root,
                "001_obs-char-000001_test_oracle-character",
                "01_candidate-character-packet.json",
                {"suggested_oracle_character_id": "obs-char-000001"},
                True,
            )
            self.make_object(
                root,
                "002_obs-unk-000001_test_oracle-character-candidate",
                "01_undeciphered-candidate-packet.json",
                {"unknown_candidate_id": "obs-unk-000001"},
                False,
            )
            rows = MODULE.build_rows(root)
            self.assertEqual(len(rows), 2)
            by_id = {row["project_id"]: row for row in rows}
            self.assertEqual(
                by_id["obs-char-000001"]["visual_observation_status"],
                "direct_visual_record_present",
            )
            self.assertEqual(
                by_id["obs-unk-000001"]["visual_observation_status"],
                "missing_direct_visual_record",
            )
            self.assertEqual(by_id["obs-unk-000001"]["asset_count"], "1")

    def test_report_is_human_readable_and_line_wrapped(self) -> None:
        rows = [
            {
                "project_id": "obs-unk-000001",
                "project_id_type": "undeciphered_candidate",
                "asset_count": "1",
                "visual_observation_status": "missing_direct_visual_record",
                "object_dir": "corpus/001_oracle-characters/" + "a" * 160,
            }
        ]
        report = MODULE.build_report(
            rows, "corpus/009_statistics-and-derived-features/227_test.csv"
        )
        self.assertLessEqual(max(len(line) for line in report.splitlines()), 80)
        self.assertIn("needs_human_visual_observation_review", report)
        self.assertIn("有图无观察", report)


if __name__ == "__main__":
    unittest.main()
