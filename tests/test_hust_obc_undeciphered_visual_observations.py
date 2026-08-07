import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools/002_corpus-import/"
    "build_hust_obc_undeciphered_visual_observations.py"
)
SPEC = importlib.util.spec_from_file_location(
    "build_hust_obc_undeciphered_visual_observations", MODULE_PATH
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class HustObcUndecipheredVisualObservationTests(unittest.TestCase):
    def test_profile_is_pixel_only_and_wrapped(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            object_dir = root / "object"
            object_dir.mkdir()
            image_path = object_dir / "glyph.png"
            Image.new("L", (8, 12), 255).save(image_path)
            packet = {
                "unknown_candidate_id": "obs-unk-000001",
                "primary_external_ref_id": "hust-obc-und-X-000001",
                "source_id": "src-hust-obc",
                "evidence_download_id": "dl-hust-obc-figshare-raw",
                "rights_status": "source_marked_risk_noted",
            }
            text = MODULE.observation_text(root, object_dir, packet, [], image_path)
            self.assertIn("Pixel Profile / 像素 profile", text)
            self.assertIn("not a human visual observation", text)
            self.assertNotIn("Direct Visual Record", text)
            self.assertLessEqual(max(len(line) for line in text.splitlines()), 80)

    def test_readme_and_indexes_add_the_observation_route(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            readme = root / "README.md"
            readme.write_text(
                "- Human-readable context dossier / 人类可读语境档案:\n"
                "  `08_character-context-evidence-dossier.md`\n",
                encoding="utf-8",
            )
            self.assertTrue(MODULE.ensure_readme_link(readme))
            self.assertIn("14_material-visual-observation.md", readme.read_text(encoding="utf-8"))
            index = root / "index.json"
            index.write_text(
                json.dumps(
                    {"human_files": ["08_character-context-evidence-dossier.md"]},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            self.assertTrue(MODULE.ensure_index_link(index, "human_files"))
            data = json.loads(index.read_text(encoding="utf-8"))
            self.assertIn("14_material-visual-observation.md", data["human_files"])


if __name__ == "__main__":
    unittest.main()
