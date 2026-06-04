import unittest
import csv

from tools.validation.check_repository_skeleton import (
    check_bilingual_markers,
    check_file_size_limits,
    check_forbidden_policy_text,
    check_forbidden_paths,
    check_forbidden_top_level_dirs,
    check_required_paths,
    check_root_gitignore_patterns,
    check_source_registers,
    check_tracked_temp_artifacts,
    repo_root,
)


class RepositorySkeletonTests(unittest.TestCase):
    def test_required_paths_exist(self) -> None:
        self.assertEqual(check_required_paths(repo_root()), [])

    def test_bilingual_markers_exist(self) -> None:
        self.assertEqual(check_bilingual_markers(repo_root()), [])

    def test_forbidden_path_patterns_absent(self) -> None:
        self.assertEqual(check_forbidden_paths(repo_root()), [])

    def test_forbidden_top_level_dirs_absent(self) -> None:
        self.assertEqual(check_forbidden_top_level_dirs(repo_root()), [])

    def test_forbidden_old_policy_text_absent(self) -> None:
        self.assertEqual(check_forbidden_policy_text(repo_root()), [])

    def test_file_size_limits(self) -> None:
        self.assertEqual(check_file_size_limits(repo_root()), [])

    def test_root_gitignore_patterns(self) -> None:
        self.assertEqual(check_root_gitignore_patterns(repo_root()), [])

    def test_tracked_temp_artifacts_absent(self) -> None:
        self.assertEqual(check_tracked_temp_artifacts(repo_root()), [])

    def test_source_registers(self) -> None:
        self.assertEqual(check_source_registers(repo_root()), [])

    def test_source_field_map_covers_first_stage_sources(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "007_source-field-map.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        source_ids = {row["source_id"] for row in rows}
        expected = {
            "src-hust-obc",
            "src-obimd",
            "src-evobc",
            "src-obid-ancientbooks",
            "src-cambridge-hopkins",
            "src-tsinghua-oracle-bones",
        }
        self.assertTrue(expected.issubset(source_ids))
        self.assertGreaterEqual(len(rows), 20)

    def test_source_package_manifest_covers_large_metadata_boundaries(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "009_source-package-file-manifest.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        file_names = {row["file_name"] for row in rows}
        expected = {
            "HUST-OBC.zip",
            "data.json",
            "facsimile.zip",
            "rubbing.zip",
            "Main-character.json",
            "List_of_EVOBC.json",
        }
        self.assertTrue(expected.issubset(file_names))
        for row in rows:
            file_size = int(row["file_size_bytes"])
            if file_size >= 40 * 1024 * 1024:
                self.assertEqual(row["commit_policy"], "do_not_commit_regular_git")

    def test_downloaded_metadata_profiles_include_core_counts(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "010_downloaded-metadata-profile.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        metrics = {(row["source_id"], row["profile_metric"]): row["profile_value"] for row in rows}
        self.assertEqual(metrics[("src-hust-obc", "validation_label_count")], "1588")
        self.assertEqual(metrics[("src-obimd", "main_character_uid_count")], "3936")
        self.assertEqual(metrics[("src-evobc", "class_count")], "13714")
        self.assertEqual(metrics[("src-evobc", "image_reference_count")], "229170")

    def test_hust_obc_validation_staging_has_1588_candidate_classes(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "005_hust-obc-validation-class-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1588)
        self.assertEqual(rows[0]["candidate_class_id"], "obs-cand-000001")
        self.assertEqual(rows[0]["source_category_id"], "0001")
        self.assertEqual(rows[0]["validation_class_id"], "0")
        self.assertEqual(rows[-1]["source_category_id"], "1781")
        self.assertEqual(rows[-1]["validation_class_id"], "1587")
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"dataset_candidate_not_promoted"},
        )


if __name__ == "__main__":
    unittest.main()
