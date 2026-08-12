import importlib.util
import os
import shutil
import tempfile
import unittest
import csv
from pathlib import Path

from tools.validation import check_repository_skeleton


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_dossier_builder():
    path = (
        REPO_ROOT
        / "tools/002_corpus-import/build_character_human_research_dossiers.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_character_human_research_dossiers_local_image_truth",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CharacterDossierLocalImageTruthTests(unittest.TestCase):
    def test_repository_external_file_is_not_a_local_image(self) -> None:
        module = load_dossier_builder()
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            root = workspace / "repository"
            root.mkdir()
            outside_image = workspace / "outside.png"
            outside_image.write_bytes(b"not-a-repository-image")

            self.assertFalse(
                module.local_asset_exists(root, str(outside_image)),
                "An absolute file outside the repository is a source route, "
                "not an object-local image.",
            )

    def test_missing_image_route_has_explicit_route_only_status(self) -> None:
        module = load_dossier_builder()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            route = "corpus/example/03_visual-assets/missing.png"

            self.assertEqual(
                module.local_visual_status(root, route),
                "source_route_only_local_file_missing",
            )

    def test_source_reference_without_committed_route_is_route_only(self) -> None:
        module = load_dossier_builder()
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(
                module.local_visual_status(
                    Path(temp_dir),
                    "",
                    "HUST-OBC/undeciphered/example.png",
                ),
                "source_route_only_local_file_missing",
            )

    @unittest.skipUnless(os.name == "nt", "Windows long-path regression")
    def test_long_repository_path_is_still_a_local_image(self) -> None:
        module = load_dossier_builder()
        temp_dir = tempfile.mkdtemp()
        try:
            root = Path(temp_dir)
            image = (
                root
                / ("bucket-" + "a" * 70)
                / ("object-" + "b" * 70)
                / ("assets-" + "c" * 70)
                / "glyph.png"
            )
            prefixed = Path("\\\\?\\" + str(image))
            prefixed.parent.mkdir(parents=True)
            prefixed.write_bytes(b"local-image")
            self.assertGreater(len(str(image)), 260)

            route = image.relative_to(root).as_posix()
            self.assertEqual(
                module.local_visual_status(root, route),
                "local_file_present",
            )
        finally:
            shutil.rmtree("\\\\?\\" + temp_dir)

    def test_repository_gate_rejects_false_local_image_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            object_dir = (
                root
                / "corpus/001_oracle-characters/001_bucket"
                / "001_obs-unk-000001_example"
            )
            object_dir.mkdir(parents=True)
            route = (
                "corpus/001_oracle-characters/001_bucket/"
                "001_obs-unk-000001_example/03_visual-assets/missing.png"
            )
            with (object_dir / "02_visual-source-index.csv").open(
                "w", encoding="utf-8", newline=""
            ) as file:
                writer = csv.DictWriter(file, fieldnames=["committed_image_path"])
                writer.writeheader()
                writer.writerow({"committed_image_path": route})
            dossier = object_dir / "05_human-research-dossier.md"
            dossier.write_text(
                "- local image status: `local_file_present`\n"
                "- glyph image: `local_file_present`\n",
                encoding="utf-8",
            )

            issues = (
                check_repository_skeleton
                .check_character_dossier_local_image_truth(root)
            )
            self.assertEqual(len(issues), 2)
            self.assertTrue(all("obs-unk-000001" in issue for issue in issues))

            dossier.write_text(
                "- local image status: `source_route_only_local_file_missing`\n"
                "- glyph image: `source_route_only_local_file_missing`\n",
                encoding="utf-8",
            )
            self.assertEqual(
                check_repository_skeleton
                .check_character_dossier_local_image_truth(root),
                [],
            )


if __name__ == "__main__":
    unittest.main()
