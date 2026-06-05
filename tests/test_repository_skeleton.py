import unittest
import csv
import importlib.util
import json
from collections import Counter

from tools.validation.check_repository_skeleton import (
    check_bilingual_markers,
    check_file_size_limits,
    check_forbidden_policy_text,
    check_forbidden_paths,
    check_forbidden_top_level_dirs,
    check_ai_context_packs,
    check_ai_agent_evidence_pack_validator,
    check_required_paths,
    check_relationship_graph_edges,
    check_relationship_graph_statistics,
    check_root_gitignore_patterns,
    check_source_registers,
    check_tracked_temp_artifacts,
    repo_root,
)


def load_download_source_manifest_module():
    path = repo_root() / "tools/002_corpus-import/download_source_manifest.py"
    spec = importlib.util.spec_from_file_location("download_source_manifest", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_label_crosswalk_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_validation_label_crosswalk.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_validation_label_crosswalk", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_source_category_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_source_category_staging.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_source_category_staging", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_obs_char_promotion_queue_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_obs_char_promotion_queue.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_obs_char_promotion_queue", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_promotion_bucket_manifests_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_promotion_bucket_manifests.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_promotion_bucket_manifests", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_candidate_graph_edges_module():
    path = repo_root() / "tools/003_graph-generation/build_hust_obc_candidate_graph_edges.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_candidate_graph_edges", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_obimd_component_graph_edges_module():
    path = repo_root() / "tools/003_graph-generation/build_obimd_component_graph_edges.py"
    spec = importlib.util.spec_from_file_location("build_obimd_component_graph_edges", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_evobc_evolution_graph_edges_module():
    path = repo_root() / "tools/003_graph-generation/build_evobc_evolution_graph_edges.py"
    spec = importlib.util.spec_from_file_location("build_evobc_evolution_graph_edges", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_relationship_graph_statistics_module():
    path = repo_root() / "tools/004_statistics-generation/build_relationship_graph_statistics.py"
    spec = importlib.util.spec_from_file_location("build_relationship_graph_statistics", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_relationship_graph_context_pack_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_relationship_graph_context_pack.py"
    spec = importlib.util.spec_from_file_location("build_relationship_graph_context_pack", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_bucket_review_route_pack_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_hust_obc_bucket_review_route_pack.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_bucket_review_route_pack", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_candidate_evidence_pack_request_queue_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_hust_obc_candidate_evidence_pack_request_queue.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_candidate_evidence_pack_request_queue", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_evidence_pack_draft_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_hust_obc_evidence_pack_draft.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_evidence_pack_draft", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_ai_agent_evidence_pack_validator_module():
    path = repo_root() / "tools/validation/validate_ai_agent_evidence_packs.py"
    spec = importlib.util.spec_from_file_location("validate_ai_agent_evidence_packs", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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

    def test_relationship_graph_edges(self) -> None:
        self.assertEqual(check_relationship_graph_edges(repo_root()), [])

    def test_relationship_graph_statistics(self) -> None:
        self.assertEqual(check_relationship_graph_statistics(repo_root()), [])

    def test_ai_context_packs(self) -> None:
        self.assertEqual(check_ai_context_packs(repo_root()), [])

    def test_ai_agent_evidence_pack_validator(self) -> None:
        self.assertEqual(check_ai_agent_evidence_pack_validator(repo_root()), [])

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
            "src-xiaoxuetang-jiaguwen",
            "src-xiaoxuetang-obm",
            "src-ihp-oracle-rubbings",
            "src-hust-obc",
            "src-obimd",
            "src-evobc",
            "src-obid-ancientbooks",
            "src-cambridge-hopkins",
            "src-tsinghua-oracle-bones",
        }
        self.assertTrue(expected.issubset(source_ids))
        self.assertGreaterEqual(len(rows), 30)

    def test_core_institutional_access_profile_preserves_main_source_contracts(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "011_core-institutional-access-profile.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertGreaterEqual(len(rows), 15)
        by_source = {}
        for row in rows:
            by_source.setdefault(row["source_id"], []).append(row)
        self.assertTrue(
            {
                "src-xiaoxuetang-jiaguwen",
                "src-xiaoxuetang-obm",
                "src-ihp-oracle-rubbings",
            }.issubset(by_source)
        )
        text = " ".join(" ".join(row.values()) for row in rows)
        self.assertIn("character_heads=2548", text)
        self.assertIn("glyph_forms=24701", text)
        self.assertIn("jiaguwen_bian_primary_basis", text)
        self.assertIn("heji_range=1-41956", text)
        self.assertIn("old_catalog_book_abbrev_count=90", text)
        self.assertIn("holding_abbrev_count=211", text)
        self.assertIn("old_catalog_book_abbrev_rows_staged=90", text)
        self.assertIn("holding_abbrev_rows_staged=211", text)
        self.assertIn("digitized_searchable_records=21556", text)
        self.assertIn("collection_number_cross_reference", text)
        self.assertIn("site_policy_required", text)
        self.assertEqual(
            {row["review_status"] for row in rows},
            {"reviewed_metadata_only"},
        )

    def test_obm_abbreviation_staging_preserves_appendix_boundaries(self) -> None:
        path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "012_obm-abbreviation-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 301)
        by_kind = {}
        for row in rows:
            by_kind.setdefault(row["abbreviation_kind"], []).append(row)
        self.assertEqual(len(by_kind["old_catalog_book_abbreviation"]), 90)
        self.assertEqual(len(by_kind["holding_abbreviation"]), 211)
        self.assertEqual(by_kind["old_catalog_book_abbreviation"][0]["source_abbreviation"], "鐵")
        self.assertEqual(by_kind["old_catalog_book_abbreviation"][0]["source_label"], "鐵雲藏龜")
        self.assertEqual(by_kind["holding_abbreviation"][0]["source_abbreviation"], "八木")
        self.assertEqual(by_kind["holding_abbreviation"][-1]["source_abbreviation"], "簠拓")
        self.assertEqual(
            {row["evidence_download_id"] for row in by_kind["old_catalog_book_abbreviation"]},
            {"dl-xxt-obm-appendix01"},
        )
        self.assertEqual(
            {row["evidence_download_id"] for row in by_kind["holding_abbreviation"]},
            {"dl-xxt-obm-appendix02"},
        )
        self.assertEqual(
            {row["rights_status"] for row in rows},
            {"metadata_only_until_verified"},
        )
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"abbreviation_metadata_not_promoted"},
        )
        self.assertEqual(
            {row["review_status"] for row in rows},
            {"reviewed_metadata_only"},
        )

    def test_download_source_manifest_can_merge_targeted_log_rows(self) -> None:
        module = load_download_source_manifest_module()
        existing_rows = [
            {"download_id": "dl-a", "status": "old-a"},
            {"download_id": "dl-b", "status": "old-b"},
        ]
        updated_rows = [
            {"download_id": "dl-b", "status": "new-b"},
            {"download_id": "dl-c", "status": "new-c"},
        ]
        merged = module.merge_log_rows(existing_rows, updated_rows)
        self.assertEqual(
            [(row["download_id"], row["status"]) for row in merged],
            [("dl-a", "old-a"), ("dl-b", "new-b"), ("dl-c", "new-c")],
        )

    def test_external_prefixes_cover_staging_id_families(self) -> None:
        path = (
            repo_root()
            / "project_registry/003_external-source-prefixes/"
            / "003_external-source-prefixes.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        prefixes = {row["prefix"]: row for row in rows}
        expected = {
            "cam-hopkins-y",
            "cam-hopkins-c",
            "cam-hopkins-h",
            "cam-hopkins-j",
            "hust-obc-cat",
            "ihp-mus-obj",
            "obimd-main",
            "obimd-sub",
            "obimd-glyph-link",
            "evobc-cat",
            "evobc-code",
            "collection-prov",
        }
        self.assertTrue(expected.issubset(prefixes))
        self.assertEqual(prefixes["hust-obc-cat"]["source_id"], "src-hust-obc")
        self.assertEqual(prefixes["obimd-main"]["source_id"], "src-obimd")
        self.assertEqual(prefixes["cam-hopkins-j"]["source_id"], "src-cambridge-hopkins")
        self.assertEqual(prefixes["ihp-mus-obj"]["source_id"], "src-ihp-museum-oracle-bones")
        self.assertEqual(prefixes["evobc-cat"]["source_id"], "src-evobc")
        self.assertIn("not an accepted oracle-character ID", prefixes["hust-obc-cat"]["notes_en"])

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
        self.assertEqual(metrics[("src-hust-obc", "validation_label_crosswalk_count")], "1588")
        self.assertEqual(metrics[("src-hust-obc", "validation_label_single_component_count")], "1415")
        self.assertEqual(metrics[("src-hust-obc", "validation_label_multi_component_count")], "173")
        self.assertEqual(metrics[("src-hust-obc", "validation_source_category_count")], "1781")
        self.assertEqual(metrics[("src-hust-obc", "validation_source_category_multi_member_count")], "366")
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

    def test_hust_obc_validation_label_crosswalk_preserves_1588_label_candidates(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "007_hust-obc-validation-label-crosswalk-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1588)
        self.assertEqual(rows[0]["candidate_label_crosswalk_id"], "hust-obc-label-xwalk-0001")
        self.assertEqual(rows[0]["candidate_class_id"], "obs-cand-000001")
        self.assertEqual(rows[0]["source_category_id"], "0001")
        self.assertEqual(rows[0]["source_category_id_padded"], "00001")
        self.assertEqual(rows[0]["source_modern_label_candidate"], "\u2e80")
        self.assertEqual(rows[0]["source_modern_label_codepoints"], "U+2E80")
        self.assertEqual(rows[10]["source_category_id"], "0011_0012_0013")
        self.assertEqual(rows[10]["source_category_id_padded"], "00011;00012;00013")
        self.assertEqual(rows[10]["label_component_count"], "3")
        self.assertEqual(rows[10]["has_multi_component_label"], "true")
        self.assertEqual(rows[-1]["candidate_label_crosswalk_id"], "hust-obc-label-xwalk-1588")
        self.assertEqual(rows[-1]["candidate_class_id"], "obs-cand-001588")
        self.assertEqual(rows[-1]["source_category_id"], "1781")
        self.assertEqual(rows[-1]["source_modern_label_candidate"], "\u3aeb")
        self.assertEqual(rows[-1]["source_modern_label_codepoints"], "U+3AEB")
        self.assertEqual(
            sum(1 for row in rows if row["has_multi_component_label"] == "true"),
            173,
        )
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"dataset_label_candidate_not_promoted"},
        )
        self.assertEqual(
            {row["review_status"] for row in rows},
            {"reviewed_metadata_only"},
        )

    def test_hust_obc_label_crosswalk_builder_pads_source_ids(self) -> None:
        module = load_hust_obc_label_crosswalk_module()
        rows = module.build_rows(
            [
                {
                    "candidate_class_id": "obs-cand-000001",
                    "source_category_id": "0011_0012",
                    "validation_class_id": "10",
                }
            ],
            {"00011": "\u3401", "00012": "\u3402"},
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source_category_id_padded"], "00011;00012")
        self.assertEqual(rows[0]["source_modern_label_candidate"], "\u3401\u3402")
        self.assertEqual(rows[0]["source_modern_label_codepoints"], "U+3401;U+3402")
        self.assertEqual(rows[0]["label_component_count"], "2")
        self.assertEqual(rows[0]["has_multi_component_label"], "true")

    def test_hust_obc_source_category_staging_preserves_1781_categories(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "008_hust-obc-source-category-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1781)
        self.assertEqual(rows[0]["source_category_row_id"], "hust-obc-src-cat-0001")
        self.assertEqual(rows[0]["source_category_id"], "0001")
        self.assertEqual(rows[0]["source_category_id_padded"], "00001")
        self.assertEqual(rows[0]["source_modern_label_candidate"], "\u2e80")
        self.assertEqual(rows[0]["source_modern_label_codepoint"], "U+2E80")
        self.assertEqual(rows[10]["source_category_row_id"], "hust-obc-src-cat-0011")
        self.assertEqual(rows[10]["source_category_id"], "0011")
        self.assertEqual(rows[10]["linked_candidate_class_id"], "obs-cand-000011")
        self.assertEqual(rows[10]["linked_label_crosswalk_id"], "hust-obc-label-xwalk-0011")
        self.assertEqual(rows[10]["is_part_of_multi_category_class"], "true")
        self.assertEqual(rows[-1]["source_category_row_id"], "hust-obc-src-cat-1781")
        self.assertEqual(rows[-1]["source_category_id"], "1781")
        self.assertEqual(rows[-1]["source_modern_label_candidate"], "\u3aeb")
        self.assertEqual(rows[-1]["source_modern_label_codepoint"], "U+3AEB")
        self.assertEqual(
            sum(1 for row in rows if row["is_part_of_multi_category_class"] == "true"),
            366,
        )
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"dataset_source_category_not_promoted"},
        )
        self.assertEqual(
            {row["review_status"] for row in rows},
            {"reviewed_metadata_only"},
        )

    def test_hust_obc_source_category_builder_expands_multi_category_classes(self) -> None:
        module = load_hust_obc_source_category_module()
        rows = module.build_rows(
            [
                {
                    "candidate_class_id": "obs-cand-000011",
                    "source_category_id": "0011_0012",
                    "validation_class_id": "10",
                }
            ],
            {"00011": "\u3401", "00012": "\u3402"},
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["source_category_row_id"], "hust-obc-src-cat-0011")
        self.assertEqual(rows[0]["linked_candidate_class_id"], "obs-cand-000011")
        self.assertEqual(rows[0]["linked_label_crosswalk_id"], "hust-obc-label-xwalk-0001")
        self.assertEqual(rows[0]["is_part_of_multi_category_class"], "true")
        self.assertEqual(rows[1]["source_category_id"], "0012")
        self.assertEqual(rows[1]["source_modern_label_codepoint"], "U+3402")

    def test_hust_obc_obs_char_promotion_queue_preserves_review_boundary(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "009_hust-obc-obs-char-promotion-review-queue.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1588)
        self.assertEqual(rows[0]["promotion_queue_id"], "hust-obc-obs-char-promo-000001")
        self.assertEqual(rows[0]["suggested_oracle_character_id"], "obs-char-000001")
        self.assertEqual(
            rows[0]["suggested_bucket_directory"],
            "001_000001-000100_obs-char-bucket_oracle-characters",
        )
        self.assertEqual(rows[0]["candidate_class_id"], "obs-cand-000001")
        self.assertEqual(rows[0]["source_modern_label_codepoints"], "U+2E80")
        self.assertEqual(rows[10]["source_category_member_count"], "3")
        self.assertEqual(
            rows[10]["source_category_row_ids"],
            "hust-obc-src-cat-0011;hust-obc-src-cat-0012;hust-obc-src-cat-0013",
        )
        self.assertEqual(rows[12]["source_category_member_count"], "2")
        self.assertEqual(rows[-1]["promotion_queue_id"], "hust-obc-obs-char-promo-001588")
        self.assertEqual(rows[-1]["suggested_oracle_character_id"], "obs-char-001588")
        self.assertEqual(
            rows[-1]["suggested_bucket_directory"],
            "016_001501-001600_obs-char-bucket_oracle-characters",
        )
        self.assertEqual(rows[-1]["source_modern_label_codepoints"], "U+3AEB")
        self.assertEqual(sum(1 for row in rows if row["has_multi_component_label"] == "true"), 173)
        self.assertEqual({row["assignment_status"] for row in rows}, {"reserved_candidate_not_assigned"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"needs_cross_source_review"})
        self.assertEqual({row["review_status"] for row in rows}, {"needs_review"})

    def test_hust_obc_obs_char_promotion_queue_builder_assigns_reserved_ids_only(self) -> None:
        module = load_hust_obc_obs_char_promotion_queue_module()
        rows = module.build_rows(
            [
                {
                    "candidate_class_id": "obs-cand-000011",
                    "source_id": "src-hust-obc",
                    "primary_external_ref_id": "hust-obc-cat-0011_0012",
                    "source_category_id": "0011_0012",
                    "validation_class_id": "10",
                    "reported_decipherment_scope": "deciphered_dataset_category",
                }
            ],
            [
                {
                    "candidate_label_crosswalk_id": "hust-obc-label-xwalk-0001",
                    "candidate_class_id": "obs-cand-000011",
                    "source_category_id_padded": "00011;00012",
                    "source_modern_label_candidate": "\u3401\u3402",
                    "source_modern_label_codepoints": "U+3401;U+3402",
                    "label_component_count": "2",
                    "has_multi_component_label": "true",
                }
            ],
            [
                {
                    "source_category_row_id": "hust-obc-src-cat-0011",
                    "linked_candidate_class_id": "obs-cand-000011",
                    "source_category_id": "0011",
                },
                {
                    "source_category_row_id": "hust-obc-src-cat-0012",
                    "linked_candidate_class_id": "obs-cand-000011",
                    "source_category_id": "0012",
                },
            ],
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["suggested_oracle_character_id"], "obs-char-000001")
        self.assertEqual(rows[0]["source_category_member_count"], "2")
        self.assertEqual(rows[0]["assignment_status"], "reserved_candidate_not_assigned")
        self.assertEqual(rows[0]["suggested_decipherment_status"], "unknown_until_cross_source_review")
        self.assertIn("not assigned", rows[0]["caution"])

    def test_hust_obc_promotion_bucket_manifests_cover_full_queue(self) -> None:
        base = repo_root() / "corpus/001_oracle-characters"
        rows_by_queue_id = {}
        bucket_counts = []
        for bucket_number in range(1, 17):
            bucket_start = (bucket_number - 1) * 100 + 1
            bucket_end = bucket_start + 99
            bucket_directory = (
                f"{bucket_number:03d}_{bucket_start:06d}-{bucket_end:06d}"
                "_obs-char-bucket_oracle-characters"
            )
            path = base / bucket_directory / "000_hust-obc-promotion-bucket-manifest.csv"
            with path.open("r", encoding="utf-8-sig", newline="") as file:
                rows = list(csv.DictReader(file))
            bucket_counts.append(len(rows))
            self.assertEqual(
                rows[0]["bucket_manifest_row_id"],
                f"hust-obc-bucket-{bucket_number:03d}-row-001",
            )
            self.assertEqual(rows[0]["suggested_bucket_directory"], bucket_directory)
            for row in rows:
                rows_by_queue_id[row["promotion_queue_id"]] = row

        self.assertEqual(bucket_counts[:15], [100] * 15)
        self.assertEqual(bucket_counts[15], 88)
        self.assertEqual(len(rows_by_queue_id), 1588)
        self.assertEqual(
            set(rows_by_queue_id),
            {f"hust-obc-obs-char-promo-{index:06d}" for index in range(1, 1589)},
        )
        self.assertEqual(
            rows_by_queue_id["hust-obc-obs-char-promo-000001"]["suggested_oracle_character_id"],
            "obs-char-000001",
        )
        self.assertEqual(
            rows_by_queue_id["hust-obc-obs-char-promo-001588"]["suggested_bucket_directory"],
            "016_001501-001600_obs-char-bucket_oracle-characters",
        )
        self.assertEqual(
            {row["assignment_status"] for row in rows_by_queue_id.values()},
            {"reserved_candidate_not_assigned"},
        )
        self.assertEqual(
            {row["review_status"] for row in rows_by_queue_id.values()},
            {"needs_review"},
        )

    def test_hust_obc_promotion_bucket_summary_routes_review_batches(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "010_hust-obc-promotion-bucket-review-summary.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 16)
        self.assertEqual(rows[0]["bucket_summary_id"], "hust-obc-bucket-summary-001")
        self.assertEqual(rows[0]["suggested_oracle_character_id_start"], "obs-char-000001")
        self.assertEqual(rows[0]["suggested_oracle_character_id_end"], "obs-char-000100")
        self.assertEqual(rows[0]["row_count"], "100")
        self.assertEqual(rows[0]["multi_component_label_count"], "10")
        self.assertEqual(rows[0]["source_category_row_count"], "111")
        self.assertEqual(rows[-1]["bucket_summary_id"], "hust-obc-bucket-summary-016")
        self.assertEqual(rows[-1]["suggested_oracle_character_id_start"], "obs-char-001501")
        self.assertEqual(rows[-1]["suggested_oracle_character_id_end"], "obs-char-001588")
        self.assertEqual(rows[-1]["row_count"], "88")
        self.assertEqual(sum(int(row["row_count"]) for row in rows), 1588)
        self.assertEqual(sum(int(row["multi_component_label_count"]) for row in rows), 173)
        self.assertEqual(sum(int(row["source_category_row_count"]) for row in rows), 1781)
        self.assertEqual({row["source_id_set"] for row in rows}, {"src-hust-obc"})
        self.assertEqual(
            {row["assignment_status_set"] for row in rows},
            {"reserved_candidate_not_assigned"},
        )
        self.assertEqual({row["review_status_set"] for row in rows}, {"needs_review"})
        self.assertIn("not assigned", rows[0]["caution"])

    def test_hust_obc_promotion_bucket_manifest_builder_partitions_rows(self) -> None:
        module = load_hust_obc_promotion_bucket_manifests_module()
        queue_rows = [
            {
                "promotion_queue_id": "hust-obc-obs-char-promo-000001",
                "suggested_oracle_character_id": "obs-char-000001",
                "suggested_bucket_directory": "001_000001-000100_obs-char-bucket_oracle-characters",
                "candidate_class_id": "obs-cand-000001",
                "source_id": "src-hust-obc",
                "has_multi_component_label": "false",
                "source_category_member_count": "1",
                "assignment_status": "reserved_candidate_not_assigned",
            },
            {
                "promotion_queue_id": "hust-obc-obs-char-promo-000101",
                "suggested_oracle_character_id": "obs-char-000101",
                "suggested_bucket_directory": "002_000101-000200_obs-char-bucket_oracle-characters",
                "candidate_class_id": "obs-cand-000101",
                "source_id": "src-hust-obc",
                "has_multi_component_label": "true",
                "source_category_member_count": "2",
                "assignment_status": "reserved_candidate_not_assigned",
            },
        ]
        manifests = module.build_bucket_manifests(queue_rows)
        self.assertEqual(
            sorted(manifests),
            [
                "001_000001-000100_obs-char-bucket_oracle-characters",
                "002_000101-000200_obs-char-bucket_oracle-characters",
            ],
        )
        self.assertEqual(
            manifests["001_000001-000100_obs-char-bucket_oracle-characters"][0][
                "bucket_manifest_row_id"
            ],
            "hust-obc-bucket-001-row-001",
        )
        self.assertEqual(
            manifests["002_000101-000200_obs-char-bucket_oracle-characters"][0][
                "bucket_manifest_row_id"
            ],
            "hust-obc-bucket-002-row-001",
        )
        summary_rows = module.build_bucket_summary_rows(manifests, module.DEFAULT_OUTPUT_ROOT)
        self.assertEqual(len(summary_rows), 2)
        self.assertEqual(summary_rows[0]["bucket_summary_id"], "hust-obc-bucket-summary-001")
        self.assertEqual(summary_rows[0]["row_count"], "1")
        self.assertEqual(summary_rows[0]["suggested_oracle_character_id_start"], "obs-char-000001")
        self.assertEqual(summary_rows[1]["bucket_summary_id"], "hust-obc-bucket-summary-002")
        self.assertEqual(summary_rows[1]["manifest_path"], (
            "corpus/001_oracle-characters/"
            "002_000101-000200_obs-char-bucket_oracle-characters/"
            "000_hust-obc-promotion-bucket-manifest.csv"
        ))

    def test_hust_obc_candidate_graph_edges_preserve_metadata_relationships(self) -> None:
        path = repo_root() / "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3562)
        self.assertEqual(
            Counter(row["edge_type"] for row in rows),
            Counter(
                {
                    "HAS_HUST_OBC_SOURCE_CATEGORY": 1781,
                    "HAS_HUST_OBC_OCR_LABEL_CANDIDATE": 1781,
                }
            ),
        )
        self.assertEqual(rows[0]["edge_id"], "edge-hust-obc-class-src-cat-0001")
        self.assertEqual(rows[0]["source_node_id"], "obs-cand-000001")
        self.assertEqual(rows[0]["target_node_id"], "hust-obc-src-cat-0001")
        self.assertEqual(rows[1780]["edge_id"], "edge-hust-obc-class-src-cat-1781")
        self.assertEqual(rows[1780]["source_node_id"], "obs-cand-001588")
        self.assertEqual(rows[1780]["target_node_id"], "hust-obc-src-cat-1781")
        self.assertEqual(rows[1781]["edge_id"], "edge-hust-obc-src-cat-label-0001")
        self.assertEqual(rows[1781]["source_node_id"], "hust-obc-src-cat-0001")
        self.assertEqual(rows[1781]["target_node_id"], "hust-obc-ocr-label-u2e80")
        self.assertEqual(rows[-1]["edge_id"], "edge-hust-obc-src-cat-label-1781")
        self.assertEqual(rows[-1]["target_node_id"], "hust-obc-ocr-label-u3aeb")
        self.assertEqual({tuple(row["source_ids"]) for row in rows}, {("src-hust-obc",)})
        self.assertEqual({row["confidence_level"] for row in rows}, {"high"})
        self.assertEqual({row["review_status"] for row in rows}, {"reviewed"})

    def test_hust_obc_candidate_graph_edges_builder_keeps_dataset_boundary(self) -> None:
        module = load_hust_obc_candidate_graph_edges_module()
        rows = module.build_edges(
            [
                {"candidate_class_id": "obs-cand-000011"},
            ],
            [
                {
                    "source_category_row_id": "hust-obc-src-cat-0011",
                    "linked_candidate_class_id": "obs-cand-000011",
                    "source_modern_label_codepoint": "U+3401",
                },
                {
                    "source_category_row_id": "hust-obc-src-cat-0012",
                    "linked_candidate_class_id": "obs-cand-000011",
                    "source_modern_label_codepoint": "U+3402",
                },
            ],
        )
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["edge_id"], "edge-hust-obc-class-src-cat-0001")
        self.assertEqual(rows[0]["source_node_id"], "obs-cand-000011")
        self.assertEqual(rows[0]["target_node_id"], "hust-obc-src-cat-0011")
        self.assertEqual(rows[2]["edge_type"], "HAS_HUST_OBC_OCR_LABEL_CANDIDATE")
        self.assertEqual(rows[2]["target_node_id"], "hust-obc-ocr-label-u3401")
        self.assertIn("not a formal oracle-character identity claim", rows[0]["evidence_note"])
        self.assertIn("not accepted paleographic readings", rows[2]["evidence_note"])

    def test_obimd_component_graph_edges_preserve_component_and_glyph_mappings(self) -> None:
        path = repo_root() / "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl"
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 44433)
        self.assertEqual(
            Counter(row["edge_type"] for row in rows),
            Counter(
                {
                    "OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER": 2747,
                    "OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT": 41686,
                }
            ),
        )
        self.assertEqual(rows[0]["edge_id"], "edge-obimd-sub-main-000001")
        self.assertEqual(rows[0]["source_node_id"], "obimd-sub-cand-000001")
        self.assertEqual(rows[0]["target_node_id"], "obimd-main-p8w7ujqanz")
        self.assertEqual(rows[2746]["edge_id"], "edge-obimd-sub-main-002747")
        self.assertEqual(rows[2746]["source_node_id"], "obimd-sub-cand-002747")
        self.assertEqual(rows[2746]["target_node_id"], "obimd-main-bt5y2iq3kp")
        self.assertEqual(rows[2747]["edge_id"], "edge-obimd-sub-glyph-000001")
        self.assertEqual(rows[2747]["source_node_id"], "obimd-sub-cand-000001")
        self.assertEqual(rows[2747]["target_node_id"], "obimd-glyph-codepoint-u65e5-uf0000")
        self.assertEqual(rows[-1]["edge_id"], "edge-obimd-sub-glyph-041686")
        self.assertEqual(rows[-1]["source_node_id"], "obimd-sub-cand-002747")
        self.assertEqual(rows[-1]["target_node_id"], "obimd-glyph-codepoint-uff9e1")
        self.assertEqual({tuple(row["source_ids"]) for row in rows}, {("src-obimd",)})
        self.assertEqual({row["confidence_level"] for row in rows}, {"high"})
        self.assertEqual({row["review_status"] for row in rows}, {"reviewed"})

    def test_obimd_component_graph_edges_builder_keeps_external_main_refs(self) -> None:
        module = load_obimd_component_graph_edges_module()
        rows = module.build_edges(
            [],
            [
                {
                    "candidate_subcharacter_id": "obimd-sub-cand-000001",
                    "source_subcharacter_uid": "sub-uid-a",
                    "source_main_character_uid": "main-uid-not-in-main-table",
                    "main_character_external_ref_id": "obimd-main-main-uid-not-in-main-table",
                }
            ],
            [
                {
                    "source_subcharacter_uid": "sub-uid-a",
                    "glyph_codepoint_uplus": "U+65E5;U+F0000",
                }
            ],
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["edge_type"], "OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER")
        self.assertEqual(rows[0]["target_node_id"], "obimd-main-main-uid-not-in-main-table")
        self.assertEqual(rows[1]["edge_type"], "OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT")
        self.assertEqual(rows[1]["target_node_id"], "obimd-glyph-codepoint-u65e5-uf0000")
        self.assertIn("not a formal component analysis", rows[0]["evidence_note"])
        self.assertIn("private-use code points", rows[1]["evidence_note"])

    def test_evobc_evolution_graph_edges_preserve_era_and_source_counts(self) -> None:
        path = repo_root() / "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl"
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 51679)
        self.assertEqual(
            Counter(row["edge_type"] for row in rows),
            Counter(
                {
                    "EVOBC_CATEGORY_HAS_ERA_CODE": 26378,
                    "EVOBC_CATEGORY_HAS_SOURCE_CODE": 25301,
                }
            ),
        )
        self.assertEqual(rows[0]["edge_id"], "edge-evobc-cat-era-00001-00")
        self.assertEqual(rows[0]["source_node_id"], "evobc-evo-cat-00001")
        self.assertEqual(rows[0]["target_node_id"], "evobc-code-001")
        self.assertIn("edge_image_reference_count=35", rows[0]["evidence_note"])
        self.assertEqual(rows[1]["edge_id"], "edge-evobc-cat-era-00001-03")
        self.assertEqual(rows[1]["target_node_id"], "evobc-code-004")
        self.assertEqual(rows[2]["edge_id"], "edge-evobc-cat-source-00001-00")
        self.assertEqual(rows[2]["target_node_id"], "evobc-code-007")
        self.assertIn("source-code labels are dataset tokens", rows[2]["evidence_note"])
        self.assertEqual(rows[7]["edge_id"], "edge-evobc-cat-source-00001-07")
        self.assertEqual(rows[7]["target_node_id"], "evobc-code-014")
        self.assertEqual(rows[8]["edge_id"], "edge-evobc-cat-era-00002-04")
        self.assertEqual(rows[8]["target_node_id"], "evobc-code-005")
        self.assertEqual(rows[-1]["edge_id"], "edge-evobc-cat-source-13713-05")
        self.assertEqual(rows[-1]["source_node_id"], "evobc-evo-cat-13713")
        self.assertEqual(rows[-1]["target_node_id"], "evobc-code-012")
        self.assertEqual({tuple(row["source_ids"]) for row in rows}, {("src-evobc",)})
        self.assertEqual({row["confidence_level"] for row in rows}, {"high"})
        self.assertEqual({row["review_status"] for row in rows}, {"reviewed"})

    def test_evobc_evolution_graph_edges_builder_expands_compact_counts(self) -> None:
        module = load_evobc_evolution_graph_edges_module()
        rows = module.build_edges(
            [
                {
                    "candidate_evolution_category_id": "evobc-evo-cat-00001",
                    "source_category_id": "00001",
                    "image_reference_count": "37",
                    "era_code_counts": "0:35;3:2",
                    "source_code_counts": "0:1;7:2",
                },
                {
                    "candidate_evolution_category_id": "evobc-evo-cat-13714",
                    "source_category_id": "13714",
                    "image_reference_count": "0",
                    "era_code_counts": "",
                    "source_code_counts": "",
                },
            ],
            [
                {"code_type": "era", "code_value": "0", "codebook_row_id": "evobc-code-001"},
                {"code_type": "era", "code_value": "3", "codebook_row_id": "evobc-code-004"},
                {"code_type": "source", "code_value": "0", "codebook_row_id": "evobc-code-007"},
                {"code_type": "source", "code_value": "7", "codebook_row_id": "evobc-code-014"},
            ],
        )
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["edge_id"], "edge-evobc-cat-era-00001-00")
        self.assertEqual(rows[1]["target_node_id"], "evobc-code-004")
        self.assertEqual(rows[2]["edge_type"], "EVOBC_CATEGORY_HAS_SOURCE_CODE")
        self.assertEqual(rows[3]["edge_id"], "edge-evobc-cat-source-00001-07")
        self.assertIn("category_image_reference_count=37", rows[0]["evidence_note"])
        self.assertIn("not an accepted paleographic correspondence", rows[0]["evidence_note"])

    def test_relationship_graph_edge_type_summary_preserves_current_edge_totals(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "001_relationship-graph-edge-type-summary.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 6)
        by_edge_type = {row["edge_type"]: row for row in rows}
        self.assertEqual(by_edge_type["HAS_HUST_OBC_SOURCE_CATEGORY"]["edge_count"], "1781")
        self.assertEqual(by_edge_type["HAS_HUST_OBC_SOURCE_CATEGORY"]["unique_source_node_count"], "1588")
        self.assertEqual(by_edge_type["OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT"]["edge_count"], "41686")
        self.assertEqual(by_edge_type["OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER"]["unique_target_node_count"], "1730")
        self.assertEqual(by_edge_type["EVOBC_CATEGORY_HAS_ERA_CODE"]["edge_count"], "26378")
        self.assertEqual(by_edge_type["EVOBC_CATEGORY_HAS_SOURCE_CODE"]["unique_target_node_count"], "8")
        self.assertEqual(sum(int(row["edge_count"]) for row in rows), 99674)
        self.assertEqual({row["generated_from"] for row in rows}, {"relationship_graph_jsonl"})

    def test_relationship_graph_node_degree_summary_preserves_degree_totals(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "002_relationship-graph-node-degree-summary.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 65039)
        self.assertEqual(sum(int(row["out_degree"]) for row in rows), 99674)
        self.assertEqual(sum(int(row["in_degree"]) for row in rows), 99674)
        self.assertEqual(rows[0]["node_id"], "evobc-code-008")
        self.assertEqual(rows[0]["total_degree"], "10158")
        self.assertEqual(rows[0]["incoming_edge_type_counts"], "EVOBC_CATEGORY_HAS_SOURCE_CODE:10158")
        self.assertEqual(rows[1]["node_id"], "evobc-code-003")
        self.assertEqual(rows[1]["total_degree"], "9147")
        self.assertEqual(rows[-1]["node_id"], "obs-cand-001588")
        self.assertEqual(rows[-1]["outgoing_edge_type_counts"], "HAS_HUST_OBC_SOURCE_CATEGORY:1")
        self.assertEqual({row["generated_from"] for row in rows}, {"relationship_graph_jsonl"})

    def test_relationship_graph_statistics_builder_summarizes_small_graph(self) -> None:
        module = load_relationship_graph_statistics_module()
        rows = [
            {
                "edge_id": "edge-a",
                "source_node_id": "node-a",
                "edge_type": "RELATES_TO",
                "target_node_id": "node-b",
                "confidence_level": "high",
                "source_ids": ["src-test"],
                "review_status": "reviewed",
            },
            {
                "edge_id": "edge-b",
                "source_node_id": "node-a",
                "edge_type": "RELATES_TO",
                "target_node_id": "node-c",
                "confidence_level": "high",
                "source_ids": ["src-test"],
                "review_status": "reviewed",
            },
        ]
        original_reader = module.read_jsonl_edges
        try:
            module.read_jsonl_edges = lambda _path: rows
            graph_files = [module.Path("example.jsonl")]
            edge_summary = module.build_edge_type_summary(graph_files, repo_root())
            degree_summary = module.build_node_degree_summary(graph_files, repo_root())
        finally:
            module.read_jsonl_edges = original_reader
        self.assertEqual(edge_summary[0]["edge_count"], "2")
        self.assertEqual(edge_summary[0]["unique_source_node_count"], "1")
        self.assertEqual(edge_summary[0]["unique_target_node_count"], "2")
        by_node = {row["node_id"]: row for row in degree_summary}
        self.assertEqual(by_node["node-a"]["out_degree"], "2")
        self.assertEqual(by_node["node-b"]["in_degree"], "1")
        self.assertEqual(by_node["node-c"]["incoming_edge_type_counts"], "RELATES_TO:1")

    def test_ai_agent_relationship_graph_context_pack_preserves_routing_summary(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "003_ai-agent-relationship-graph-context-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["context_pack_id"], "ai-context-relationship-graph-001")
        self.assertEqual(data["status"], "reviewed_metadata_only")
        self.assertEqual(data["coverage"]["total_edge_count"], 99674)
        self.assertEqual(data["coverage"]["node_count"], 65039)
        self.assertEqual(data["coverage"]["source_count"], 3)
        self.assertEqual(data["coverage"]["edge_type_count"], 6)
        by_source = {row["source_id"]: row for row in data["source_summaries"]}
        self.assertEqual(by_source["src-hust-obc"]["edge_count"], 3562)
        self.assertEqual(by_source["src-obimd"]["edge_count"], 44433)
        self.assertEqual(by_source["src-evobc"]["edge_count"], 51679)
        self.assertEqual(data["top_degree_nodes"][0]["node_id"], "evobc-code-008")
        self.assertEqual(data["top_degree_nodes"][0]["total_degree"], 10158)
        self.assertIn("routing and coverage summary", " ".join(data["agent_use_rules"]))
        self.assertIn("不得把 OCR 标签", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_relationship_graph_context_pack_builder_keeps_cautions(self) -> None:
        module = load_relationship_graph_context_pack_module()
        edge_summary_rows = [
            {
                "graph_file": "example.jsonl",
                "source_id": "src-hust-obc",
                "edge_type": "HAS_TEST_EDGE",
                "edge_count": "2",
                "unique_source_node_count": "1",
                "unique_target_node_count": "2",
            }
        ]
        node_degree_rows = [
            {
                "node_id": "node-a",
                "total_degree": "2",
                "out_degree": "2",
                "in_degree": "0",
                "outgoing_edge_type_counts": "HAS_TEST_EDGE:2",
                "incoming_edge_type_counts": "",
                "source_ids": "src-hust-obc",
                "graph_files": "example.jsonl",
            }
        ]
        data = module.build_context_pack(edge_summary_rows, node_degree_rows, top_node_limit=1)
        self.assertEqual(data["coverage"]["total_edge_count"], 2)
        self.assertEqual(data["coverage"]["top_node_limit"], 1)
        self.assertEqual(data["source_summaries"][0]["label"], "HUST-OBC dataset metadata")
        self.assertEqual(data["top_degree_nodes"][0]["node_id"], "node-a")
        self.assertIn("does not contain decipherment claims", data["purpose"])
        self.assertIn("Open the cited CSV/JSONL source rows", data["agent_use_rules"][1])

    def test_ai_agent_hust_obc_bucket_review_route_pack_preserves_batch_routes(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "004_ai-agent-hust-obc-bucket-review-route-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["context_pack_id"], "ai-context-hust-obc-bucket-review-001")
        self.assertEqual(data["status"], "reviewed_metadata_only")
        self.assertEqual(data["coverage"]["bucket_count"], 16)
        self.assertEqual(data["coverage"]["candidate_count"], 1588)
        self.assertEqual(data["coverage"]["multi_component_label_count"], 173)
        self.assertEqual(data["coverage"]["source_category_row_count"], 1781)
        self.assertEqual(data["coverage"]["source_route_requirement_count"], 6)
        self.assertEqual(data["coverage"]["evidence_gap_type_count"], 9)
        source_ids = {row["source_id"] for row in data["source_route_requirements"]}
        self.assertTrue(
            {
                "src-hust-obc",
                "src-xiaoxuetang-jiaguwen",
                "src-xiaoxuetang-obm",
                "src-obimd",
                "src-evobc",
                "src-ihp-oracle-rubbings",
            }.issubset(source_ids)
        )
        self.assertEqual(len(data["bucket_routes"]), 16)
        first_route = data["bucket_routes"][0]
        self.assertEqual(first_route["bucket_summary_id"], "hust-obc-bucket-summary-001")
        self.assertEqual(first_route["candidate_count"], 100)
        self.assertEqual(first_route["assignment_status"], "reserved_candidate_not_assigned")
        self.assertIn("source_provenance", first_route["evidence_gap_types"])
        self.assertIn("primary_inscription_context", first_route["evidence_gap_types"])
        self.assertIn(
            "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl",
            first_route["route_files"],
        )
        self.assertEqual(data["bucket_routes"][-1]["bucket_summary_id"], "hust-obc-bucket-summary-016")
        self.assertEqual(data["bucket_routes"][-1]["candidate_count"], 88)
        self.assertIn("reserved candidates", " ".join(data["agent_use_rules"]))
        self.assertIn("doc/public/user_research", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_hust_obc_bucket_review_route_pack_builder_keeps_draft_boundary(self) -> None:
        module = load_hust_obc_bucket_review_route_pack_module()
        data = module.build_route_pack(
            [
                {
                    "bucket_summary_id": "hust-obc-bucket-summary-001",
                    "bucket_number": "001",
                    "bucket_directory": "001_000001-000100_obs-char-bucket_oracle-characters",
                    "manifest_path": (
                        "corpus/001_oracle-characters/"
                        "001_000001-000100_obs-char-bucket_oracle-characters/"
                        "000_hust-obc-promotion-bucket-manifest.csv"
                    ),
                    "suggested_oracle_character_id_start": "obs-char-000001",
                    "suggested_oracle_character_id_end": "obs-char-000100",
                    "promotion_queue_id_start": "hust-obc-obs-char-promo-000001",
                    "promotion_queue_id_end": "hust-obc-obs-char-promo-000100",
                    "candidate_class_id_start": "obs-cand-000001",
                    "candidate_class_id_end": "obs-cand-000100",
                    "row_count": "100",
                    "multi_component_label_count": "10",
                    "source_category_row_count": "111",
                    "assignment_status_set": "reserved_candidate_not_assigned",
                    "review_status_set": "needs_review",
                    "required_next_review": "compare_xiaoxuetang_obm_obimd_evobc_and_primary_inscription_context",
                }
            ]
        )
        self.assertEqual(data["coverage"]["candidate_count"], 100)
        self.assertEqual(data["bucket_routes"][0]["assignment_status"], "reserved_candidate_not_assigned")
        self.assertIn("does not contain decipherment claims", data["purpose"])
        self.assertIn("doc/public/user_research", data["bucket_routes"][0]["agent_batch_steps"][3])

    def test_ai_agent_hust_obc_candidate_evidence_request_queue_covers_all_candidates(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1588)
        self.assertEqual(rows[0]["evidence_request_id"], "hust-obc-evidence-request-000001")
        self.assertEqual(rows[0]["route_pack_id"], "ai-context-hust-obc-bucket-review-001")
        self.assertEqual(rows[0]["promotion_queue_id"], "hust-obc-obs-char-promo-000001")
        self.assertEqual(rows[0]["bucket_summary_id"], "hust-obc-bucket-summary-001")
        self.assertEqual(rows[0]["draft_status"], "not_started")
        self.assertTrue(rows[0]["draft_output_path"].startswith("doc/public/user_research/"))
        self.assertIn("primary_inscription_context", rows[0]["evidence_gap_types"])
        self.assertIn("full_inscription_context", rows[0]["required_evidence_pack_sections"])
        self.assertIn(
            "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl",
            rows[0]["route_files"],
        )
        self.assertEqual(rows[-1]["evidence_request_id"], "hust-obc-evidence-request-001588")
        self.assertEqual(rows[-1]["suggested_oracle_character_id"], "obs-char-001588")
        self.assertEqual(rows[-1]["bucket_summary_id"], "hust-obc-bucket-summary-016")
        self.assertEqual(
            rows[-1]["draft_output_path"],
            "doc/public/user_research/001_ai-agent-evidence-packs/hust-obc/"
            "016_001501-001600_obs-char-bucket/"
            "016_obs-char-001588_hust-obc-cat-1781_evidence-pack-draft.json",
        )
        self.assertEqual(sum(1 for row in rows if row["has_multi_component_label"] == "true"), 173)
        self.assertEqual({row["assignment_status"] for row in rows}, {"reserved_candidate_not_assigned"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"needs_cross_source_review"})
        self.assertEqual({row["review_status"] for row in rows}, {"needs_evidence_pack"})
        self.assertTrue(all(not row["draft_output_path"].startswith("research/") for row in rows))
        self.assertTrue(all("not be treated as a decipherment result" in row["caution"] for row in rows))

    def test_ai_agent_hust_obc_candidate_evidence_request_queue_builder_keeps_boundaries(self) -> None:
        module = load_hust_obc_candidate_evidence_pack_request_queue_module()
        route_pack = {
            "context_pack_id": "ai-context-hust-obc-bucket-review-001",
            "source_route_requirements": [
                {"source_id": "src-hust-obc"},
                {"source_id": "src-obimd"},
            ],
            "bucket_routes": [
                {
                    "bucket_directory": "001_000001-000100_obs-char-bucket_oracle-characters",
                    "bucket_summary_id": "hust-obc-bucket-summary-001",
                    "manifest_path": (
                        "corpus/001_oracle-characters/"
                        "001_000001-000100_obs-char-bucket_oracle-characters/"
                        "000_hust-obc-promotion-bucket-manifest.csv"
                    ),
                    "route_files": ["manifest.csv", "graph.jsonl"],
                    "evidence_gap_types": ["source_provenance", "opposing_evidence"],
                }
            ],
        }
        rows = module.build_request_rows(
            [
                {
                    "promotion_queue_id": "hust-obc-obs-char-promo-000001",
                    "suggested_oracle_character_id": "obs-char-000001",
                    "suggested_bucket_directory": "001_000001-000100_obs-char-bucket_oracle-characters",
                    "candidate_class_id": "obs-cand-000001",
                    "primary_external_ref_id": "hust-obc-cat-0001",
                    "source_category_id": "0001",
                    "source_modern_label_codepoints": "U+2E80",
                    "has_multi_component_label": "false",
                    "source_category_member_count": "1",
                    "assignment_status": "reserved_candidate_not_assigned",
                    "promotion_status": "needs_cross_source_review",
                }
            ],
            route_pack,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["evidence_request_id"], "hust-obc-evidence-request-000001")
        self.assertEqual(rows[0]["draft_status"], "not_started")
        self.assertEqual(rows[0]["review_status"], "needs_evidence_pack")
        self.assertTrue(rows[0]["draft_output_path"].startswith("doc/public/user_research/"))
        self.assertIn("source_references_and_asset_metadata", rows[0]["required_evidence_pack_sections"])
        self.assertIn("not be treated as a decipherment result", rows[0]["caution"])

    def test_ai_agent_evidence_pack_schema_keeps_draft_contract(self) -> None:
        path = (
            repo_root()
            / "schemas/006_ai-agent-evidence-pack-schema/"
            / "ai-agent-evidence-pack.schema.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["title"], "AI Agent Oracle Bone Script Evidence Pack")
        required = set(data["required"])
        expected = {
            "evidence_pack_id",
            "evidence_request_id",
            "status",
            "research_boundary",
            "assignment_status",
            "source_references_and_asset_metadata",
            "full_inscription_context",
            "neighboring_characters",
            "component_breakdown_and_variant_notes",
            "excavation_period_and_catalog_provenance",
            "bronze_seal_or_modern_comparanda",
            "supporting_evidence",
            "opposing_evidence",
            "open_questions_and_next_checks",
            "review_log",
            "caution",
        }
        self.assertTrue(expected.issubset(required))
        self.assertEqual(data["properties"]["research_boundary"]["const"], "draft_not_scholarship")
        self.assertIn(
            "reserved_candidate_not_assigned",
            data["properties"]["assignment_status"]["enum"],
        )

    def test_ai_agent_first_evidence_pack_draft_is_empty_scaffold(self) -> None:
        path = (
            repo_root()
            / "doc/public/user_research/001_ai-agent-evidence-packs/hust-obc/"
            / "001_000001-000100_obs-char-bucket/"
            / "001_obs-char-000001_hust-obc-cat-0001_evidence-pack-draft.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["evidence_pack_id"], "hust-obc-evidence-pack-000001")
        self.assertEqual(data["evidence_request_id"], "hust-obc-evidence-request-000001")
        self.assertEqual(data["status"], "draft")
        self.assertEqual(data["research_boundary"], "draft_not_scholarship")
        self.assertEqual(data["assignment_status"], "reserved_candidate_not_assigned")
        self.assertEqual(data["suggested_oracle_character_id"], "obs-char-000001")
        self.assertEqual(data["primary_external_ref_id"], "hust-obc-cat-0001")
        self.assertIn("not a decipherment result", data["caution"])
        evidence_sections = [
            "character_or_unknown_glyph_id",
            "source_references_and_asset_metadata",
            "full_inscription_context",
            "neighboring_characters",
            "component_breakdown_and_variant_notes",
            "excavation_period_and_catalog_provenance",
            "bronze_seal_or_modern_comparanda",
            "supporting_evidence",
            "opposing_evidence",
        ]
        for section in evidence_sections:
            self.assertEqual(data[section]["status"], "not_collected")
            self.assertEqual(data[section]["items"], [])
        self.assertTrue(data["open_questions_and_next_checks"])
        self.assertTrue(data["review_log"])

    def test_ai_agent_evidence_pack_draft_builder_creates_scaffold_only(self) -> None:
        module = load_hust_obc_evidence_pack_draft_module()
        row = {
            "evidence_request_id": "hust-obc-evidence-request-000001",
            "assignment_status": "reserved_candidate_not_assigned",
            "suggested_oracle_character_id": "obs-char-000001",
            "candidate_class_id": "obs-cand-000001",
            "primary_external_ref_id": "hust-obc-cat-0001",
            "route_pack_id": "ai-context-hust-obc-bucket-review-001",
            "bucket_manifest_path": "manifest.csv",
            "route_files": "manifest.csv;graph.jsonl",
            "source_route_requirement_ids": "src-hust-obc;src-obimd",
            "evidence_gap_types": "source_provenance;opposing_evidence",
        }
        data = module.build_draft(row)
        self.assertEqual(data["evidence_pack_id"], "hust-obc-evidence-pack-000001")
        self.assertEqual(data["research_boundary"], "draft_not_scholarship")
        self.assertEqual(data["route_files"], ["manifest.csv", "graph.jsonl"])
        self.assertEqual(data["source_route_requirement_ids"], ["src-hust-obc", "src-obimd"])
        self.assertEqual(data["supporting_evidence"]["status"], "not_collected")
        self.assertEqual(data["supporting_evidence"]["items"], [])
        self.assertIn("not a decipherment result", data["caution"])

    def test_ai_agent_evidence_pack_validator_catches_boundary_errors(self) -> None:
        builder = load_hust_obc_evidence_pack_draft_module()
        validator = load_ai_agent_evidence_pack_validator_module()
        row = {
            "evidence_request_id": "hust-obc-evidence-request-000001",
            "assignment_status": "reserved_candidate_not_assigned",
            "suggested_oracle_character_id": "obs-char-000001",
            "candidate_class_id": "obs-cand-000001",
            "primary_external_ref_id": "hust-obc-cat-0001",
            "route_pack_id": "ai-context-hust-obc-bucket-review-001",
            "bucket_manifest_path": "manifest.csv",
            "route_files": "manifest.csv;graph.jsonl",
            "source_route_requirement_ids": "src-hust-obc;src-obimd",
            "evidence_gap_types": "source_provenance;opposing_evidence",
        }
        data = builder.build_draft(row)
        self.assertEqual(validator.validate_pack(data, root=repo_root()), [])
        data["research_boundary"] = "published_scholarship"
        data["caution"] = "This is a decipherment result."
        issues = validator.validate_pack(data, root=repo_root())
        self.assertTrue(any("research_boundary" in issue for issue in issues))
        self.assertTrue(any("not a decipherment result" in issue for issue in issues))

    def test_obimd_main_character_staging_has_3936_candidate_uids(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "006_obimd-main-character-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3936)
        self.assertEqual(rows[0]["candidate_main_character_id"], "obimd-main-cand-000001")
        self.assertEqual(rows[0]["source_uid"], "p8w7ujqanz")
        self.assertEqual(rows[0]["codepoint"], "日")
        self.assertEqual(rows[0]["transcription_values"], "日")
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(
            sum(1 for row in rows if row["has_empty_transcription"] == "true"),
            1159,
        )

    def test_obimd_subcharacter_staging_preserves_hierarchy_and_glyph_links(self) -> None:
        main_path = (
            repo_root()
            / "corpus/003_graphemic-components/000_component-registers/"
            / "002_obimd-subcharacter-main-staging.csv"
        )
        glyph_path = (
            repo_root()
            / "corpus/003_graphemic-components/000_component-registers/"
            / "003_obimd-subcharacter-glyph-staging.csv"
        )
        with main_path.open("r", encoding="utf-8-sig", newline="") as file:
            main_rows = list(csv.DictReader(file))
        with glyph_path.open("r", encoding="utf-8-sig", newline="") as file:
            glyph_rows = list(csv.DictReader(file))
        self.assertEqual(len(main_rows), 2747)
        self.assertEqual(len(glyph_rows), 41686)
        self.assertEqual(main_rows[0]["candidate_subcharacter_id"], "obimd-sub-cand-000001")
        self.assertEqual(main_rows[0]["source_subcharacter_uid"], "p8w7ujqanz")
        self.assertEqual(main_rows[0]["source_main_character_uid"], "p8w7ujqanz")
        self.assertEqual(glyph_rows[0]["candidate_glyph_link_id"], "obimd-glyph-link-000001")
        self.assertEqual(glyph_rows[0]["source_subcharacter_uid"], "p8w7ujqanz")
        self.assertEqual(glyph_rows[0]["glyph_codepoint_uplus"], "U+65E5;U+F0000")
        self.assertEqual(
            {row["project_import_status"] for row in main_rows + glyph_rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(len({row["source_subcharacter_uid"] for row in main_rows}), 2747)
        self.assertEqual(len({row["source_main_character_uid"] for row in main_rows}), 1730)
        self.assertEqual(len({row["glyph_codepoint"] for row in glyph_rows}), 41686)

    def test_evobc_evolution_staging_preserves_dataset_scale(self) -> None:
        category_path = (
            repo_root()
            / "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            / "001_evobc-evolution-category-staging.csv"
        )
        codebook_path = (
            repo_root()
            / "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            / "002_evobc-era-source-codebook-staging.csv"
        )
        with category_path.open("r", encoding="utf-8-sig", newline="") as file:
            category_rows = list(csv.DictReader(file))
        with codebook_path.open("r", encoding="utf-8-sig", newline="") as file:
            codebook_rows = list(csv.DictReader(file))
        self.assertEqual(len(category_rows), 13714)
        self.assertEqual(category_rows[0]["candidate_evolution_category_id"], "evobc-evo-cat-00001")
        self.assertEqual(category_rows[0]["source_category_id"], "00001")
        self.assertEqual(category_rows[0]["source_character_codepoints"], "U+3401")
        self.assertEqual(category_rows[0]["era_code_counts"], "0:35;3:2")
        self.assertEqual(category_rows[-1]["source_category_id"], "13714")
        self.assertEqual(category_rows[-1]["image_reference_count"], "0")
        self.assertEqual(sum(int(row["image_reference_count"]) for row in category_rows), 229170)
        self.assertEqual(sum(1 for row in category_rows if row["image_reference_count"] == "0"), 2)
        self.assertEqual(
            {row["project_import_status"] for row in category_rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(len(codebook_rows), 14)
        era_counts = {
            row["code_value"]: row["image_reference_count"]
            for row in codebook_rows
            if row["code_type"] == "era"
        }
        self.assertEqual(
            era_counts,
            {
                "0": "75681",
                "1": "47314",
                "2": "13434",
                "3": "9131",
                "4": "80042",
                "5": "3568",
            },
        )
        source_counts = {
            row["code_value"]: row["image_reference_count"]
            for row in codebook_rows
            if row["code_type"] == "source"
        }
        self.assertEqual(source_counts["1"], "106010")
        self.assertEqual(
            {row["review_status"] for row in codebook_rows},
            {"reviewed_metadata_only"},
        )

    def test_cambridge_hopkins_crosswalk_preserves_official_references(self) -> None:
        crosswalk_path = (
            repo_root()
            / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
            / "002_cambridge-hopkins-crosswalk-staging.csv"
        )
        summary_path = (
            repo_root()
            / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
            / "003_cambridge-hopkins-classified-summary.csv"
        )
        with crosswalk_path.open("r", encoding="utf-8-sig", newline="") as file:
            crosswalk_rows = list(csv.DictReader(file))
        with summary_path.open("r", encoding="utf-8-sig", newline="") as file:
            summary_rows = list(csv.DictReader(file))
        self.assertEqual(len(crosswalk_rows), 612)
        self.assertEqual(crosswalk_rows[0]["yingguo_ref_id"], "y1")
        self.assertEqual(crosswalk_rows[0]["cul_ref_id"], "45")
        self.assertEqual(crosswalk_rows[0]["chalfant_ref_id"], "459")
        self.assertEqual(crosswalk_rows[0]["heji_ref_id"], "39502")
        self.assertEqual(crosswalk_rows[-1]["yingguo_ref_id"], "ybu04")
        self.assertEqual(
            {row["project_import_status"] for row in crosswalk_rows},
            {"dataset_candidate_not_promoted"},
        )
        self.assertEqual(sum(1 for row in crosswalk_rows if row["has_missing_cul_ref"] == "true"), 6)
        self.assertEqual(sum(1 for row in crosswalk_rows if row["has_missing_chalfant_ref"] == "true"), 171)
        self.assertEqual(sum(1 for row in crosswalk_rows if row["has_missing_heji_ref"] == "true"), 316)
        self.assertEqual(
            sum(1 for row in crosswalk_rows if row["yingguo_ref_id"] == "y2402"),
            2,
        )
        self.assertEqual(len(summary_rows), 25)
        group_rows = [row for row in summary_rows if row["summary_kind"] == "classified_table_group"]
        self.assertEqual(len(group_rows), 20)
        grand_total = [
            row for row in summary_rows
            if row["summary_kind"] == "classified_table_grand_total"
        ][0]
        self.assertEqual(grand_total["total_count"], "609")

    def test_institutional_collection_provenance_staging_preserves_source_facts(self) -> None:
        path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "001_institutional-collection-provenance-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 4)
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(
            set(by_source),
            {
                "src-tsinghua-oracle-bones",
                "src-ihp-oracle-rubbings",
                "src-ihp-museum-oracle-bones",
                "src-cambridge-hopkins",
            },
        )
        self.assertIn("over 1,750", by_source["src-tsinghua-oracle-bones"]["holding_count_statement"])
        self.assertIn("1,495", by_source["src-tsinghua-oracle-bones"]["inscribed_count_statement"])
        self.assertIn("Hu Houxuan", by_source["src-tsinghua-oracle-bones"]["named_provenance_people"])
        self.assertIn("over 40,000", by_source["src-ihp-oracle-rubbings"]["holding_count_statement"])
        self.assertIn("21,556", by_source["src-ihp-oracle-rubbings"]["digitized_record_count_statement"])
        self.assertIn("more than 25,000", by_source["src-ihp-museum-oracle-bones"]["holding_count_statement"])
        self.assertIn("Hsiao-tun Village", by_source["src-ihp-museum-oracle-bones"]["excavation_or_source_context"])
        self.assertIn("grand total 609", by_source["src-cambridge-hopkins"]["holding_count_statement"])
        self.assertIn("50 bones", by_source["src-cambridge-hopkins"]["digitized_record_count_statement"])
        self.assertEqual(
            {row["review_status"] for row in rows},
            {"reviewed_metadata_only"},
        )

    def test_ihp_museum_object_staging_preserves_official_item_links(self) -> None:
        path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "002_ihp-museum-oracle-bone-object-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 52)
        self.assertEqual(rows[0]["candidate_collection_object_id"], "ihp-mus-obj-00001")
        self.assertEqual(rows[0]["source_collection_item_id"], "1212")
        self.assertEqual(rows[0]["catalog_reference_text"], "Jia Bian 3333+3361")
        self.assertEqual(rows[-1]["source_collection_item_id"], "273")
        self.assertEqual(rows[-1]["catalog_reference_text"], "Ping 0264")
        self.assertEqual(len({row["source_collection_item_id"] for row in rows}), 52)
        self.assertTrue(
            all(
                row["object_page_url"].startswith(
                    "https://museum.sinica.edu.tw/en/collection/32/item/"
                )
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["thumbnail_url"].startswith(
                    "https://museum.sinica.edu.tw/_upload/image/collection_item/thumbnail/"
                )
                for row in rows
            )
        )
        self.assertEqual(
            {row["thumbnail_download_status"] for row in rows},
            {"not_downloaded_metadata_only"},
        )
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"object_metadata_not_promoted"},
        )


if __name__ == "__main__":
    unittest.main()
