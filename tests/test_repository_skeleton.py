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


if __name__ == "__main__":
    unittest.main()
