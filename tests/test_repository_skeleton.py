import unittest
import csv
import hashlib
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
    check_asset_records,
    check_required_paths,
    check_relationship_graph_edges,
    check_relationship_graph_statistics,
    check_root_gitignore_patterns,
    check_hust_obc_undeciphered_candidates,
    check_source_coverage_statistics,
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


def load_hust_obc_first_bucket_candidate_packets_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_first_bucket_candidate_packets.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_first_bucket_candidate_packets", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_candidate_packets_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_candidate_packets.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_candidate_packets", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obc_undeciphered_candidate_index_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obc_undeciphered_candidate_index.py"
    spec = importlib.util.spec_from_file_location("build_hust_obc_undeciphered_candidate_index", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_module():
    path = repo_root() / "tools/002_corpus-import/build_hust_obimd_evobc_codepoint_crosswalk.py"
    spec = importlib.util.spec_from_file_location("build_hust_obimd_evobc_codepoint_crosswalk", path)
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


def load_asset_image_visual_profiles_module():
    path = repo_root() / "tools/004_statistics-generation/build_asset_image_visual_profiles.py"
    spec = importlib.util.spec_from_file_location("build_asset_image_visual_profiles", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_coverage_statistics_module():
    path = repo_root() / "tools/004_statistics-generation/build_source_coverage_statistics.py"
    spec = importlib.util.spec_from_file_location("build_source_coverage_statistics", path)
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


def load_public_domain_asset_context_pack_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_public_domain_asset_context_pack.py"
    spec = importlib.util.spec_from_file_location("build_public_domain_asset_context_pack", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_coverage_context_pack_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_source_coverage_context_pack.py"
    spec = importlib.util.spec_from_file_location("build_source_coverage_context_pack", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_context_pack_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_context_pack.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_context_pack", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_review_queue_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_review_queue.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_review_queue", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_review_route_results_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_review_route_results.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_review_route_results", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_evidence_capture_scaffold_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_evidence_capture_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_evidence_capture_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_source_register_capture_results_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_source_register_capture_results.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_source_register_capture_results",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_download_log_capture_results_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_download_log_capture_results.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_download_log_capture_results",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_candidate_packet_capture_results_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_candidate_packet_capture_results.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_candidate_packet_capture_results",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_evidence_readiness_checklist_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_evidence_readiness_checklist.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_evidence_readiness_checklist",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_hust_obimd_evobc_codepoint_crosswalk_route_availability_snapshot_module():
    path = (
        repo_root()
        / "tools/005_ai-context-pack-builder/"
        / "build_hust_obimd_evobc_codepoint_crosswalk_route_availability_snapshot.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_hust_obimd_evobc_codepoint_crosswalk_route_availability_snapshot",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_route_review_queue_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_source_route_review_queue.py"
    spec = importlib.util.spec_from_file_location("build_source_route_review_queue", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_route_review_result_scaffold_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_source_route_review_result_scaffold.py"
    spec = importlib.util.spec_from_file_location("build_source_route_review_result_scaffold", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_source_route_review_results_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_source_route_review_results.py"
    spec = importlib.util.spec_from_file_location("build_source_route_review_results", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_cross_review_queue_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_cross_review_queue.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_cross_review_queue", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_cross_review_log_scaffold_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_cross_review_log_scaffold.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_cross_review_log_scaffold", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_cross_review_log_drafts_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_cross_review_log_drafts.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_cross_review_log_drafts", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_cross_review_log_results_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_cross_review_log_results.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_cross_review_log_results", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_task_queue_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_task_queue.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_evidence_collection_task_queue", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_note_drafts_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_note_drafts.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_evidence_collection_note_drafts", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_route_pack_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_route_pack.py"
    spec = importlib.util.spec_from_file_location("build_graph_source_evidence_collection_route_pack", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_result_scaffold_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_result_scaffold.py"
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_evidence_collection_result_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_review_queue_module():
    path = repo_root() / "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_review_queue.py"
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_evidence_collection_review_queue", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_review_route_summary_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_evidence_collection_review_route_summary.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_evidence_collection_review_route_summary", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_assignment_plan_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_evidence_collection_assignment_plan.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_evidence_collection_assignment_plan", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_wave_handoff_scaffold_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_evidence_collection_wave_handoff_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_evidence_collection_wave_handoff_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_download_log_wave_handoff_scaffold_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_download_log_wave_handoff_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_download_log_wave_handoff_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_package_manifest_wave_handoff_scaffold_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_package_manifest_wave_handoff_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_package_manifest_wave_handoff_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_package_manifest_capture_scaffold_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_package_manifest_capture_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_package_manifest_capture_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_package_manifest_capture_review_checklist_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_package_manifest_capture_review_checklist.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_package_manifest_capture_review_checklist", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_download_log_capture_scaffold_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_download_log_capture_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_download_log_capture_scaffold", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_download_log_capture_review_checklist_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_download_log_capture_review_checklist.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_download_log_capture_review_checklist", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_evidence_collection_source_register_capture_scaffold_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_evidence_collection_source_register_capture_scaffold.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_evidence_collection_source_register_capture_scaffold",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_graph_source_source_register_capture_review_checklist_module():
    path = repo_root() / (
        "tools/005_ai-context-pack-builder/"
        "build_graph_source_source_register_capture_review_checklist.py"
    )
    spec = importlib.util.spec_from_file_location(
        "build_graph_source_source_register_capture_review_checklist",
        path,
    )
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

    def test_public_domain_asset_records(self) -> None:
        self.assertEqual(check_asset_records(repo_root()), [])

        asset_index_path = repo_root() / "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
        rights_log_path = repo_root() / "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv"
        technical_profile_path = (
            repo_root() / "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
        )
        visual_profile_path = (
            repo_root() / "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
        )
        asset_map_path = repo_root() / "project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv"
        with asset_index_path.open("r", encoding="utf-8-sig", newline="") as file:
            assets = {row["asset_id"]: row for row in csv.DictReader(file)}
        with rights_log_path.open("r", encoding="utf-8-sig", newline="") as file:
            rights_rows = {row["asset_id"]: row for row in csv.DictReader(file)}
        with technical_profile_path.open("r", encoding="utf-8-sig", newline="") as file:
            profile_rows = {row["asset_id"]: row for row in csv.DictReader(file)}
        with visual_profile_path.open("r", encoding="utf-8-sig", newline="") as file:
            visual_rows = {row["asset_id"]: row for row in csv.DictReader(file)}
        with asset_map_path.open("r", encoding="utf-8-sig", newline="") as file:
            map_rows = {row["project_id"]: row for row in csv.DictReader(file)}

        expected = {
            "asset-000001": (
                "001_asset-000001_met-obj-42045_object-image.jpg",
                1780568,
                "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
                "met-obj-42045",
            ),
            "asset-000002": (
                "002_asset-000002_met-obj-42022_object-image.jpg",
                2508142,
                "61510f04c8d599e4e5f9bf50ebcb1cb2163ebd7243e4a125ce08e73fdadad8cd",
                "met-obj-42022",
            ),
            "asset-000003": (
                "003_asset-000003_si-nmaa-fsc-o-26_object-image.jpg",
                633418,
                "e4152d2d680234decb8d4b04225c83a59955b69bc4d8b10eebe7a98d54259079",
                "si-nmaa-fsc-o-26",
            ),
        }
        for asset_id, (filename, size, checksum, external_ref) in expected.items():
            self.assertIn(asset_id, assets)
            self.assertIn(asset_id, rights_rows)
            self.assertIn(asset_id, profile_rows)
            self.assertIn(asset_id, visual_rows)
            self.assertIn(asset_id, map_rows)
            row = assets[asset_id]
            self.assertEqual(row["rights_status"], "public_domain_verified")
            self.assertEqual(row["primary_external_ref_id"], external_ref)
            image_path = repo_root() / row["canonical_path"]
            self.assertEqual(image_path.name, filename)
            self.assertEqual(image_path.stat().st_size, size)
            with image_path.open("rb") as file:
                self.assertEqual(hashlib.sha256(file.read()).hexdigest(), checksum)
            metadata_path = image_path.with_suffix(".yaml")
            metadata_text = metadata_path.read_text(encoding="utf-8")
            self.assertIn(f"asset_id: {asset_id}", metadata_text)
            self.assertIn(f"checksum_sha256: {checksum}", metadata_text)
            self.assertIn("rights_status: public_domain_verified", metadata_text)
            profile = profile_rows[asset_id]
            self.assertEqual(profile["image_format"], "JPEG")
            self.assertEqual(profile["color_mode"], "RGB")
            self.assertEqual(profile["checksum_sha256"], checksum)
            self.assertEqual(profile["analysis_scope"], "image_technical_metadata_only")
            visual = visual_rows[asset_id]
            self.assertEqual(visual["asset_path"], row["canonical_path"])
            self.assertEqual(visual["analysis_tool"], "Pillow")
            self.assertEqual(visual["analysis_method"], "pillow_luma_threshold_bbox_v1")
            self.assertEqual(visual["luma_threshold"], "140")
            self.assertEqual(visual["analysis_scope"], "visual_preprocessing_metadata_only")
            self.assertEqual(visual["review_status"], "reviewed_algorithmic_metadata")
            self.assertIn("not glyph segmentation", visual["caution"])
        self.assertEqual(profile_rows["asset-000001"]["pixel_width"], "2667")
        self.assertEqual(profile_rows["asset-000001"]["pixel_height"], "4000")
        self.assertEqual(profile_rows["asset-000001"]["icc_profile_bytes"], "0")
        self.assertEqual(visual_rows["asset-000001"]["foreground_bbox_width"], "2223")
        self.assertEqual(visual_rows["asset-000001"]["foreground_bbox_height"], "3530")
        self.assertEqual(visual_rows["asset-000001"]["foreground_pixel_ratio"], "0.01447357")
        self.assertEqual(visual_rows["asset-000001"]["mean_luma"], "189.3774")
        self.assertEqual(profile_rows["asset-000002"]["pixel_width"], "4000")
        self.assertEqual(profile_rows["asset-000002"]["pixel_height"], "2667")
        self.assertEqual(profile_rows["asset-000002"]["dpi_x"], "300")
        self.assertEqual(profile_rows["asset-000002"]["dpi_y"], "300")
        self.assertEqual(profile_rows["asset-000002"]["icc_profile_bytes"], "3136")
        self.assertEqual(visual_rows["asset-000002"]["foreground_bbox_width"], "3425")
        self.assertEqual(visual_rows["asset-000002"]["foreground_bbox_height"], "2461")
        self.assertEqual(visual_rows["asset-000002"]["foreground_pixel_ratio"], "0.18491423")
        self.assertEqual(visual_rows["asset-000002"]["mean_luma"], "171.9248")
        self.assertEqual(profile_rows["asset-000003"]["pixel_width"], "3000")
        self.assertEqual(profile_rows["asset-000003"]["pixel_height"], "2000")
        self.assertEqual(profile_rows["asset-000003"]["dpi_x"], "72")
        self.assertEqual(profile_rows["asset-000003"]["dpi_y"], "72")
        self.assertEqual(profile_rows["asset-000003"]["icc_profile_bytes"], "560")
        self.assertEqual(visual_rows["asset-000003"]["foreground_bbox_width"], "1566")
        self.assertEqual(visual_rows["asset-000003"]["foreground_bbox_height"], "940")
        self.assertEqual(visual_rows["asset-000003"]["foreground_pixel_ratio"], "0.03478500")
        self.assertEqual(visual_rows["asset-000003"]["mean_luma"], "225.5226")

    def test_source_registers(self) -> None:
        self.assertEqual(check_source_registers(repo_root()), [])

    def test_hust_obc_undeciphered_candidates(self) -> None:
        self.assertEqual(check_hust_obc_undeciphered_candidates(repo_root()), [])

        index_path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "003_undeciphered-oracle-characters-index.csv"
        )
        with index_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 9408)
        self.assertEqual(
            Counter(row["source_group"] for row in rows),
            {"L": 4444, "X": 2288, "Y+H": 2676},
        )
        self.assertEqual(sum(int(row["source_image_count"]) for row in rows), 62989)
        self.assertEqual(rows[0]["unknown_candidate_id"], "obs-unk-000001")
        self.assertEqual(rows[0]["primary_external_ref_id"], "hust-obc-und-L-000001")
        self.assertEqual(rows[-1]["unknown_candidate_id"], "obs-unk-009408")
        self.assertEqual(rows[-1]["primary_external_ref_id"], "hust-obc-und-YH-009408")
        self.assertTrue(all(not row["unknown_candidate_id"].startswith("obs-char-") for row in rows))
        self.assertEqual(
            {row["identity_claim_status"] for row in rows},
            {"no_identity_claim"},
        )
        self.assertEqual(
            {row["assignment_status"] for row in rows},
            {"unknown_candidate_id_not_formal_obs_char_assignment"},
        )
        self.assertEqual(
            sum(
                1
                for row in rows
                if row["materialization_status"]
                in {
                    "first_bucket_candidate_packet_materialized",
                    "second_bucket_candidate_packet_materialized",
                    "third_bucket_candidate_packet_materialized",
                    "fourth_bucket_candidate_packet_materialized",
                    "fifth_bucket_candidate_packet_materialized",
                    "sixth_bucket_candidate_packet_materialized",
                    "seventh_bucket_candidate_packet_materialized",
                    "eighth_bucket_candidate_packet_materialized",
                    "ninth_bucket_candidate_packet_materialized",
                    "tenth_bucket_candidate_packet_materialized",
                    "eleventh_bucket_candidate_packet_materialized",
                    "twelfth_bucket_candidate_packet_materialized",
                    "thirteenth_bucket_candidate_packet_materialized",
                    "fourteenth_bucket_candidate_packet_materialized",
                    "fifteenth_bucket_candidate_packet_materialized",
                    "sixteenth_bucket_candidate_packet_materialized",
                    "seventeenth_bucket_candidate_packet_materialized",
                    "eighteenth_bucket_candidate_packet_materialized",
                    "nineteenth_bucket_candidate_packet_materialized",
                    "twentieth_bucket_candidate_packet_materialized",
                    "twenty_first_bucket_candidate_packet_materialized",
                    "twenty_second_bucket_candidate_packet_materialized",
                    "twenty_third_bucket_candidate_packet_materialized",
                    "twenty_fourth_bucket_candidate_packet_materialized",
                    "twenty_fifth_bucket_candidate_packet_materialized",
                    "twenty_sixth_bucket_candidate_packet_materialized",
                    "twenty_seventh_bucket_candidate_packet_materialized",
                    "twenty_eighth_bucket_candidate_packet_materialized",
                    "twenty_ninth_bucket_candidate_packet_materialized",
                    "thirtieth_bucket_candidate_packet_materialized",
                    "thirty_first_bucket_candidate_packet_materialized",
                    "thirty_second_bucket_candidate_packet_materialized",
                    "thirty_third_bucket_candidate_packet_materialized",
                    "thirty_fourth_bucket_candidate_packet_materialized",
                    "thirty_fifth_bucket_candidate_packet_materialized",
                    "thirty_sixth_bucket_candidate_packet_materialized",
                    "thirty_seventh_bucket_candidate_packet_materialized",
                    "thirty_eighth_bucket_candidate_packet_materialized",
                    "thirty_ninth_bucket_candidate_packet_materialized",
                    "fortieth_bucket_candidate_packet_materialized",
                    "forty_first_bucket_candidate_packet_materialized",
                    "forty_second_bucket_candidate_packet_materialized",
                    "forty_third_bucket_candidate_packet_materialized",
                    "forty_fourth_bucket_candidate_packet_materialized",
                    "forty_fifth_bucket_candidate_packet_materialized",
                    "forty_sixth_bucket_candidate_packet_materialized",
                    "forty_seventh_bucket_candidate_packet_materialized",
                    "forty_eighth_bucket_candidate_packet_materialized",
                    "forty_ninth_bucket_candidate_packet_materialized",
                    "fiftieth_bucket_candidate_packet_materialized",
                    "fifty_first_bucket_candidate_packet_materialized",
                    "fifty_second_bucket_candidate_packet_materialized",
                    "fifty_third_bucket_candidate_packet_materialized",
                    "fifty_fourth_bucket_candidate_packet_materialized",
                    "fifty_fifth_bucket_candidate_packet_materialized",
                    "fifty_sixth_bucket_candidate_packet_materialized",
                    "fifty_seventh_bucket_candidate_packet_materialized",
                    "fifty_eighth_bucket_candidate_packet_materialized",
                    "fifty_ninth_bucket_candidate_packet_materialized",
                    "sixtieth_bucket_candidate_packet_materialized",
                    "sixty_first_bucket_candidate_packet_materialized",
                    "sixty_second_bucket_candidate_packet_materialized",
                    "sixty_third_bucket_candidate_packet_materialized",
                    "sixty_fourth_bucket_candidate_packet_materialized",
                    "sixty_fifth_bucket_candidate_packet_materialized",
                    "sixty_sixth_bucket_candidate_packet_materialized",
                    "sixty_seventh_bucket_candidate_packet_materialized",
                    "sixty_eighth_bucket_candidate_packet_materialized",
                    "sixty_ninth_bucket_candidate_packet_materialized",
                    "seventieth_bucket_candidate_packet_materialized",
                    "seventy_first_bucket_candidate_packet_materialized",
                    "seventy_second_bucket_candidate_packet_materialized",
                    "seventy_third_bucket_candidate_packet_materialized",
                    "seventy_fourth_bucket_candidate_packet_materialized",
                    "seventy_fifth_bucket_candidate_packet_materialized",
                    "seventy_sixth_bucket_candidate_packet_materialized",
                }
            ),
            7600,
        )
        self.assertTrue(all("9411" in row["caution"] and "9408" in row["caution"] for row in rows))

        first_packet_path = repo_root() / rows[0]["materialized_candidate_packet_path"]
        first_packet = json.loads(first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(first_packet["unknown_candidate_id"], "obs-unk-000001")
        self.assertEqual(first_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(first_packet["identity_claim_status"], "no_identity_claim")
        self.assertEqual(first_packet["source_id"], "src-hust-obc")
        self.assertIn("not an accepted oracle character", first_packet["caution"])

        second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "018_undeciphered-000101-000200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(second_manifest_rows), 100)
        self.assertEqual(second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000101")
        self.assertEqual(second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000200")
        second_packet_path = repo_root() / rows[100]["materialized_candidate_packet_path"]
        second_packet = json.loads(second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(second_packet["unknown_candidate_id"], "obs-unk-000101")
        self.assertEqual(second_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(second_packet["assignment_status"], "unknown_candidate_id_not_formal_obs_char_assignment")

        third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "019_undeciphered-000201-000300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(third_manifest_rows), 100)
        self.assertEqual(third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000201")
        self.assertEqual(third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000300")
        third_packet_path = repo_root() / rows[200]["materialized_candidate_packet_path"]
        third_packet = json.loads(third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(third_packet["unknown_candidate_id"], "obs-unk-000201")
        self.assertEqual(third_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(third_packet["identity_claim_status"], "no_identity_claim")

        fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "020_undeciphered-000301-000400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fourth_manifest_rows), 100)
        self.assertEqual(fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000301")
        self.assertEqual(fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000400")
        fourth_packet_path = repo_root() / rows[300]["materialized_candidate_packet_path"]
        fourth_packet = json.loads(fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fourth_packet["unknown_candidate_id"], "obs-unk-000301")
        self.assertEqual(fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(fourth_packet["identity_claim_status"], "no_identity_claim")

        fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "021_undeciphered-000401-000500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifth_manifest_rows), 100)
        self.assertEqual(fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000401")
        self.assertEqual(fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000500")
        fifth_packet_path = repo_root() / rows[400]["materialized_candidate_packet_path"]
        fifth_packet = json.loads(fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifth_packet["unknown_candidate_id"], "obs-unk-000401")
        self.assertEqual(fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(fifth_packet["identity_claim_status"], "no_identity_claim")

        sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "022_undeciphered-000501-000600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixth_manifest_rows), 100)
        self.assertEqual(sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000501")
        self.assertEqual(sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000600")
        sixth_packet_path = repo_root() / rows[500]["materialized_candidate_packet_path"]
        sixth_packet = json.loads(sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixth_packet["unknown_candidate_id"], "obs-unk-000501")
        self.assertEqual(sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(sixth_packet["identity_claim_status"], "no_identity_claim")

        seventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "023_undeciphered-000601-000700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventh_manifest_rows), 100)
        self.assertEqual(seventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000601")
        self.assertEqual(seventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000700")
        seventh_packet_path = repo_root() / rows[600]["materialized_candidate_packet_path"]
        seventh_packet = json.loads(seventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventh_packet["unknown_candidate_id"], "obs-unk-000601")
        self.assertEqual(seventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(seventh_packet["identity_claim_status"], "no_identity_claim")

        eighth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "024_undeciphered-000701-000800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with eighth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            eighth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(eighth_manifest_rows), 100)
        self.assertEqual(eighth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000701")
        self.assertEqual(eighth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000800")
        eighth_packet_path = repo_root() / rows[700]["materialized_candidate_packet_path"]
        eighth_packet = json.loads(eighth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(eighth_packet["unknown_candidate_id"], "obs-unk-000701")
        self.assertEqual(eighth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(eighth_packet["identity_claim_status"], "no_identity_claim")

        ninth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "025_undeciphered-000801-000900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with ninth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            ninth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(ninth_manifest_rows), 100)
        self.assertEqual(ninth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000801")
        self.assertEqual(ninth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-000900")
        ninth_packet_path = repo_root() / rows[800]["materialized_candidate_packet_path"]
        ninth_packet = json.loads(ninth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(ninth_packet["unknown_candidate_id"], "obs-unk-000801")
        self.assertEqual(ninth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(ninth_packet["identity_claim_status"], "no_identity_claim")

        tenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "026_undeciphered-000901-001000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with tenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            tenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(tenth_manifest_rows), 100)
        self.assertEqual(tenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-000901")
        self.assertEqual(tenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001000")
        tenth_packet_path = repo_root() / rows[900]["materialized_candidate_packet_path"]
        tenth_packet = json.loads(tenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(tenth_packet["unknown_candidate_id"], "obs-unk-000901")
        self.assertEqual(tenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(tenth_packet["identity_claim_status"], "no_identity_claim")

        eleventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "027_undeciphered-001001-001100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with eleventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            eleventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(eleventh_manifest_rows), 100)
        self.assertEqual(eleventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001001")
        self.assertEqual(eleventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001100")
        eleventh_packet_path = repo_root() / rows[1000]["materialized_candidate_packet_path"]
        eleventh_packet = json.loads(eleventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(eleventh_packet["unknown_candidate_id"], "obs-unk-001001")
        self.assertEqual(eleventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(eleventh_packet["identity_claim_status"], "no_identity_claim")
        twelfth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "028_undeciphered-001101-001200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twelfth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twelfth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twelfth_manifest_rows), 100)
        self.assertEqual(twelfth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001101")
        self.assertEqual(twelfth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001200")
        twelfth_packet_path = repo_root() / rows[1100]["materialized_candidate_packet_path"]
        twelfth_packet = json.loads(twelfth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twelfth_packet["unknown_candidate_id"], "obs-unk-001101")
        self.assertEqual(twelfth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twelfth_packet["identity_claim_status"], "no_identity_claim")
        thirteenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "029_undeciphered-001201-001300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirteenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirteenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirteenth_manifest_rows), 100)
        self.assertEqual(thirteenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001201")
        self.assertEqual(thirteenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001300")
        thirteenth_packet_path = repo_root() / rows[1200]["materialized_candidate_packet_path"]
        thirteenth_packet = json.loads(thirteenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirteenth_packet["unknown_candidate_id"], "obs-unk-001201")
        self.assertEqual(thirteenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirteenth_packet["identity_claim_status"], "no_identity_claim")
        fourteenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "030_undeciphered-001301-001400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fourteenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fourteenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fourteenth_manifest_rows), 100)
        self.assertEqual(fourteenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001301")
        self.assertEqual(fourteenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001400")
        fourteenth_packet_path = repo_root() / rows[1300]["materialized_candidate_packet_path"]
        fourteenth_packet = json.loads(fourteenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fourteenth_packet["unknown_candidate_id"], "obs-unk-001301")
        self.assertEqual(fourteenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(fourteenth_packet["identity_claim_status"], "no_identity_claim")
        fifteenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "031_undeciphered-001401-001500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifteenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifteenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifteenth_manifest_rows), 100)
        self.assertEqual(fifteenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001401")
        self.assertEqual(fifteenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001500")
        fifteenth_packet_path = repo_root() / rows[1400]["materialized_candidate_packet_path"]
        fifteenth_packet = json.loads(fifteenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifteenth_packet["unknown_candidate_id"], "obs-unk-001401")
        self.assertEqual(fifteenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(fifteenth_packet["identity_claim_status"], "no_identity_claim")
        sixteenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "032_undeciphered-001501-001600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixteenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixteenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixteenth_manifest_rows), 100)
        self.assertEqual(sixteenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001501")
        self.assertEqual(sixteenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001600")
        sixteenth_packet_path = repo_root() / rows[1500]["materialized_candidate_packet_path"]
        sixteenth_packet = json.loads(sixteenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixteenth_packet["unknown_candidate_id"], "obs-unk-001501")
        self.assertEqual(sixteenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(sixteenth_packet["identity_claim_status"], "no_identity_claim")
        seventeenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "033_undeciphered-001601-001700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventeenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventeenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventeenth_manifest_rows), 100)
        self.assertEqual(seventeenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001601")
        self.assertEqual(seventeenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001700")
        seventeenth_packet_path = repo_root() / rows[1600]["materialized_candidate_packet_path"]
        seventeenth_packet = json.loads(seventeenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventeenth_packet["unknown_candidate_id"], "obs-unk-001601")
        self.assertEqual(seventeenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(seventeenth_packet["identity_claim_status"], "no_identity_claim")
        eighteenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "034_undeciphered-001701-001800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with eighteenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            eighteenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(eighteenth_manifest_rows), 100)
        self.assertEqual(eighteenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001701")
        self.assertEqual(eighteenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001800")
        eighteenth_packet_path = repo_root() / rows[1700]["materialized_candidate_packet_path"]
        eighteenth_packet = json.loads(eighteenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(eighteenth_packet["unknown_candidate_id"], "obs-unk-001701")
        self.assertEqual(eighteenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(eighteenth_packet["identity_claim_status"], "no_identity_claim")
        nineteenth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "035_undeciphered-001801-001900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with nineteenth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            nineteenth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(nineteenth_manifest_rows), 100)
        self.assertEqual(nineteenth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001801")
        self.assertEqual(nineteenth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-001900")
        nineteenth_packet_path = repo_root() / rows[1800]["materialized_candidate_packet_path"]
        nineteenth_packet = json.loads(nineteenth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(nineteenth_packet["unknown_candidate_id"], "obs-unk-001801")
        self.assertEqual(nineteenth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(nineteenth_packet["identity_claim_status"], "no_identity_claim")
        twentieth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "036_undeciphered-001901-002000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twentieth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twentieth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twentieth_manifest_rows), 100)
        self.assertEqual(twentieth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-001901")
        self.assertEqual(twentieth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002000")
        twentieth_packet_path = repo_root() / rows[1900]["materialized_candidate_packet_path"]
        twentieth_packet = json.loads(twentieth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twentieth_packet["unknown_candidate_id"], "obs-unk-001901")
        self.assertEqual(twentieth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twentieth_packet["identity_claim_status"], "no_identity_claim")
        twenty_first_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "037_undeciphered-002001-002100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_first_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_first_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_first_manifest_rows), 100)
        self.assertEqual(twenty_first_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002001")
        self.assertEqual(twenty_first_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002100")
        twenty_first_packet_path = repo_root() / rows[2000]["materialized_candidate_packet_path"]
        twenty_first_packet = json.loads(twenty_first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_first_packet["unknown_candidate_id"], "obs-unk-002001")
        self.assertEqual(twenty_first_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_first_packet["identity_claim_status"], "no_identity_claim")
        twenty_second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "038_undeciphered-002101-002200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_second_manifest_rows), 100)
        self.assertEqual(twenty_second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002101")
        self.assertEqual(twenty_second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002200")
        twenty_second_packet_path = repo_root() / rows[2100]["materialized_candidate_packet_path"]
        twenty_second_packet = json.loads(twenty_second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_second_packet["unknown_candidate_id"], "obs-unk-002101")
        self.assertEqual(twenty_second_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_second_packet["identity_claim_status"], "no_identity_claim")
        twenty_third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "039_undeciphered-002201-002300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_third_manifest_rows), 100)
        self.assertEqual(twenty_third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002201")
        self.assertEqual(twenty_third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002300")
        twenty_third_packet_path = repo_root() / rows[2200]["materialized_candidate_packet_path"]
        twenty_third_packet = json.loads(twenty_third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_third_packet["unknown_candidate_id"], "obs-unk-002201")
        self.assertEqual(twenty_third_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_third_packet["identity_claim_status"], "no_identity_claim")
        twenty_fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "040_undeciphered-002301-002400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_fourth_manifest_rows), 100)
        self.assertEqual(twenty_fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002301")
        self.assertEqual(twenty_fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002400")
        twenty_fourth_packet_path = repo_root() / rows[2300]["materialized_candidate_packet_path"]
        twenty_fourth_packet = json.loads(twenty_fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_fourth_packet["unknown_candidate_id"], "obs-unk-002301")
        self.assertEqual(twenty_fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_fourth_packet["identity_claim_status"], "no_identity_claim")
        twenty_fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "041_undeciphered-002401-002500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_fifth_manifest_rows), 100)
        self.assertEqual(twenty_fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002401")
        self.assertEqual(twenty_fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002500")
        twenty_fifth_packet_path = repo_root() / rows[2400]["materialized_candidate_packet_path"]
        twenty_fifth_packet = json.loads(twenty_fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_fifth_packet["unknown_candidate_id"], "obs-unk-002401")
        self.assertEqual(twenty_fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_fifth_packet["identity_claim_status"], "no_identity_claim")
        twenty_sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "042_undeciphered-002501-002600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_sixth_manifest_rows), 100)
        self.assertEqual(twenty_sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002501")
        self.assertEqual(twenty_sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002600")
        twenty_sixth_packet_path = repo_root() / rows[2500]["materialized_candidate_packet_path"]
        twenty_sixth_packet = json.loads(twenty_sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_sixth_packet["unknown_candidate_id"], "obs-unk-002501")
        self.assertEqual(twenty_sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_sixth_packet["identity_claim_status"], "no_identity_claim")
        twenty_seventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "043_undeciphered-002601-002700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_seventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_seventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_seventh_manifest_rows), 100)
        self.assertEqual(twenty_seventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002601")
        self.assertEqual(twenty_seventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002700")
        twenty_seventh_packet_path = repo_root() / rows[2600]["materialized_candidate_packet_path"]
        twenty_seventh_packet = json.loads(twenty_seventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_seventh_packet["unknown_candidate_id"], "obs-unk-002601")
        self.assertEqual(twenty_seventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_seventh_packet["identity_claim_status"], "no_identity_claim")
        twenty_eighth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "044_undeciphered-002701-002800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_eighth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_eighth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_eighth_manifest_rows), 100)
        self.assertEqual(twenty_eighth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002701")
        self.assertEqual(twenty_eighth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002800")
        twenty_eighth_packet_path = repo_root() / rows[2700]["materialized_candidate_packet_path"]
        twenty_eighth_packet = json.loads(twenty_eighth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_eighth_packet["unknown_candidate_id"], "obs-unk-002701")
        self.assertEqual(twenty_eighth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_eighth_packet["identity_claim_status"], "no_identity_claim")
        twenty_ninth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "045_undeciphered-002801-002900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with twenty_ninth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            twenty_ninth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(twenty_ninth_manifest_rows), 100)
        self.assertEqual(twenty_ninth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002801")
        self.assertEqual(twenty_ninth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-002900")
        twenty_ninth_packet_path = repo_root() / rows[2800]["materialized_candidate_packet_path"]
        twenty_ninth_packet = json.loads(twenty_ninth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(twenty_ninth_packet["unknown_candidate_id"], "obs-unk-002801")
        self.assertEqual(twenty_ninth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(twenty_ninth_packet["identity_claim_status"], "no_identity_claim")
        thirtieth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "046_undeciphered-002901-003000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirtieth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirtieth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirtieth_manifest_rows), 100)
        self.assertEqual(thirtieth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-002901")
        self.assertEqual(thirtieth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003000")
        thirtieth_packet_path = repo_root() / rows[2900]["materialized_candidate_packet_path"]
        thirtieth_packet = json.loads(thirtieth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirtieth_packet["unknown_candidate_id"], "obs-unk-002901")
        self.assertEqual(thirtieth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirtieth_packet["identity_claim_status"], "no_identity_claim")
        thirty_first_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "047_undeciphered-003001-003100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_first_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_first_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_first_manifest_rows), 100)
        self.assertEqual(thirty_first_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003001")
        self.assertEqual(thirty_first_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003100")
        thirty_first_packet_path = repo_root() / rows[3000]["materialized_candidate_packet_path"]
        thirty_first_packet = json.loads(thirty_first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_first_packet["unknown_candidate_id"], "obs-unk-003001")
        self.assertEqual(thirty_first_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_first_packet["identity_claim_status"], "no_identity_claim")
        thirty_second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "048_undeciphered-003101-003200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_second_manifest_rows), 100)
        self.assertEqual(thirty_second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003101")
        self.assertEqual(thirty_second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003200")
        thirty_second_packet_path = repo_root() / rows[3100]["materialized_candidate_packet_path"]
        thirty_second_packet = json.loads(thirty_second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_second_packet["unknown_candidate_id"], "obs-unk-003101")
        self.assertEqual(thirty_second_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_second_packet["identity_claim_status"], "no_identity_claim")
        thirty_third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "049_undeciphered-003201-003300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_third_manifest_rows), 100)
        self.assertEqual(thirty_third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003201")
        self.assertEqual(thirty_third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003300")
        thirty_third_packet_path = repo_root() / rows[3200]["materialized_candidate_packet_path"]
        thirty_third_packet = json.loads(thirty_third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_third_packet["unknown_candidate_id"], "obs-unk-003201")
        self.assertEqual(thirty_third_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_third_packet["identity_claim_status"], "no_identity_claim")
        thirty_fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "050_undeciphered-003301-003400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_fourth_manifest_rows), 100)
        self.assertEqual(thirty_fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003301")
        self.assertEqual(thirty_fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003400")
        thirty_fourth_packet_path = repo_root() / rows[3300]["materialized_candidate_packet_path"]
        thirty_fourth_packet = json.loads(thirty_fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_fourth_packet["unknown_candidate_id"], "obs-unk-003301")
        self.assertEqual(thirty_fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_fourth_packet["identity_claim_status"], "no_identity_claim")
        thirty_fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "051_undeciphered-003401-003500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_fifth_manifest_rows), 100)
        self.assertEqual(thirty_fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003401")
        self.assertEqual(thirty_fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003500")
        thirty_fifth_packet_path = repo_root() / rows[3400]["materialized_candidate_packet_path"]
        thirty_fifth_packet = json.loads(thirty_fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_fifth_packet["unknown_candidate_id"], "obs-unk-003401")
        self.assertEqual(thirty_fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_fifth_packet["identity_claim_status"], "no_identity_claim")
        thirty_sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "052_undeciphered-003501-003600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_sixth_manifest_rows), 100)
        self.assertEqual(thirty_sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003501")
        self.assertEqual(thirty_sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003600")
        thirty_sixth_packet_path = repo_root() / rows[3500]["materialized_candidate_packet_path"]
        thirty_sixth_packet = json.loads(thirty_sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_sixth_packet["unknown_candidate_id"], "obs-unk-003501")
        self.assertEqual(thirty_sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_sixth_packet["identity_claim_status"], "no_identity_claim")
        thirty_seventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "053_undeciphered-003601-003700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_seventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_seventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_seventh_manifest_rows), 100)
        self.assertEqual(thirty_seventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003601")
        self.assertEqual(thirty_seventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003700")
        thirty_seventh_packet_path = repo_root() / rows[3600]["materialized_candidate_packet_path"]
        thirty_seventh_packet = json.loads(thirty_seventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_seventh_packet["unknown_candidate_id"], "obs-unk-003601")
        self.assertEqual(thirty_seventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_seventh_packet["identity_claim_status"], "no_identity_claim")
        thirty_eighth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "054_undeciphered-003701-003800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_eighth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_eighth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_eighth_manifest_rows), 100)
        self.assertEqual(thirty_eighth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003701")
        self.assertEqual(thirty_eighth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003800")
        thirty_eighth_packet_path = repo_root() / rows[3700]["materialized_candidate_packet_path"]
        thirty_eighth_packet = json.loads(thirty_eighth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_eighth_packet["unknown_candidate_id"], "obs-unk-003701")
        self.assertEqual(thirty_eighth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_eighth_packet["identity_claim_status"], "no_identity_claim")
        thirty_ninth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "055_undeciphered-003801-003900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with thirty_ninth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            thirty_ninth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(thirty_ninth_manifest_rows), 100)
        self.assertEqual(thirty_ninth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003801")
        self.assertEqual(thirty_ninth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-003900")
        thirty_ninth_packet_path = repo_root() / rows[3800]["materialized_candidate_packet_path"]
        thirty_ninth_packet = json.loads(thirty_ninth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(thirty_ninth_packet["unknown_candidate_id"], "obs-unk-003801")
        self.assertEqual(thirty_ninth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(thirty_ninth_packet["identity_claim_status"], "no_identity_claim")
        fortieth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "056_undeciphered-003901-004000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fortieth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fortieth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fortieth_manifest_rows), 100)
        self.assertEqual(fortieth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-003901")
        self.assertEqual(fortieth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004000")
        fortieth_packet_path = repo_root() / rows[3900]["materialized_candidate_packet_path"]
        fortieth_packet = json.loads(fortieth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fortieth_packet["unknown_candidate_id"], "obs-unk-003901")
        self.assertEqual(fortieth_packet["record_type"], "oracle_character_undeciphered_candidate_packet")
        self.assertEqual(fortieth_packet["identity_claim_status"], "no_identity_claim")
        forty_first_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "057_undeciphered-004001-004100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_first_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_first_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_first_manifest_rows), 100)
        self.assertEqual(forty_first_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004001")
        self.assertEqual(forty_first_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004100")
        forty_first_packet_path = repo_root() / rows[4000]["materialized_candidate_packet_path"]
        forty_first_packet = json.loads(forty_first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_first_packet["unknown_candidate_id"], "obs-unk-004001")
        self.assertEqual(
            forty_first_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_first_packet["identity_claim_status"], "no_identity_claim")
        forty_second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "058_undeciphered-004101-004200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_second_manifest_rows), 100)
        self.assertEqual(forty_second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004101")
        self.assertEqual(forty_second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004200")
        forty_second_packet_path = repo_root() / rows[4100]["materialized_candidate_packet_path"]
        forty_second_packet = json.loads(forty_second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_second_packet["unknown_candidate_id"], "obs-unk-004101")
        self.assertEqual(
            forty_second_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_second_packet["identity_claim_status"], "no_identity_claim")
        forty_third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "059_undeciphered-004201-004300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_third_manifest_rows), 100)
        self.assertEqual(forty_third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004201")
        self.assertEqual(forty_third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004300")
        forty_third_packet_path = repo_root() / rows[4200]["materialized_candidate_packet_path"]
        forty_third_packet = json.loads(forty_third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_third_packet["unknown_candidate_id"], "obs-unk-004201")
        self.assertEqual(
            forty_third_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_third_packet["identity_claim_status"], "no_identity_claim")
        forty_fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "060_undeciphered-004301-004400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_fourth_manifest_rows), 100)
        self.assertEqual(forty_fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004301")
        self.assertEqual(forty_fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004400")
        forty_fourth_packet_path = repo_root() / rows[4300]["materialized_candidate_packet_path"]
        forty_fourth_packet = json.loads(forty_fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_fourth_packet["unknown_candidate_id"], "obs-unk-004301")
        self.assertEqual(
            forty_fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_fourth_packet["identity_claim_status"], "no_identity_claim")
        forty_fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "061_undeciphered-004401-004500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_fifth_manifest_rows), 100)
        self.assertEqual(forty_fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004401")
        self.assertEqual(forty_fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004500")
        forty_fifth_packet_path = repo_root() / rows[4400]["materialized_candidate_packet_path"]
        forty_fifth_packet = json.loads(forty_fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_fifth_packet["unknown_candidate_id"], "obs-unk-004401")
        self.assertEqual(
            forty_fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_fifth_packet["identity_claim_status"], "no_identity_claim")
        forty_sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "062_undeciphered-004501-004600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_sixth_manifest_rows), 100)
        self.assertEqual(forty_sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004501")
        self.assertEqual(forty_sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004600")
        forty_sixth_packet_path = repo_root() / rows[4500]["materialized_candidate_packet_path"]
        forty_sixth_packet = json.loads(forty_sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_sixth_packet["unknown_candidate_id"], "obs-unk-004501")
        self.assertEqual(
            forty_sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_sixth_packet["identity_claim_status"], "no_identity_claim")
        forty_seventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "063_undeciphered-004601-004700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_seventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_seventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_seventh_manifest_rows), 100)
        self.assertEqual(forty_seventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004601")
        self.assertEqual(forty_seventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004700")
        forty_seventh_packet_path = repo_root() / rows[4600]["materialized_candidate_packet_path"]
        forty_seventh_packet = json.loads(forty_seventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_seventh_packet["unknown_candidate_id"], "obs-unk-004601")
        self.assertEqual(
            forty_seventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_seventh_packet["identity_claim_status"], "no_identity_claim")
        forty_eighth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "064_undeciphered-004701-004800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_eighth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_eighth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_eighth_manifest_rows), 100)
        self.assertEqual(forty_eighth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004701")
        self.assertEqual(forty_eighth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004800")
        forty_eighth_packet_path = repo_root() / rows[4700]["materialized_candidate_packet_path"]
        forty_eighth_packet = json.loads(forty_eighth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_eighth_packet["unknown_candidate_id"], "obs-unk-004701")
        self.assertEqual(
            forty_eighth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_eighth_packet["identity_claim_status"], "no_identity_claim")
        forty_ninth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "065_undeciphered-004801-004900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with forty_ninth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            forty_ninth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(forty_ninth_manifest_rows), 100)
        self.assertEqual(forty_ninth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004801")
        self.assertEqual(forty_ninth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-004900")
        forty_ninth_packet_path = repo_root() / rows[4800]["materialized_candidate_packet_path"]
        forty_ninth_packet = json.loads(forty_ninth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(forty_ninth_packet["unknown_candidate_id"], "obs-unk-004801")
        self.assertEqual(
            forty_ninth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(forty_ninth_packet["identity_claim_status"], "no_identity_claim")
        fiftieth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "066_undeciphered-004901-005000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fiftieth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fiftieth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fiftieth_manifest_rows), 100)
        self.assertEqual(fiftieth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-004901")
        self.assertEqual(fiftieth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005000")
        fiftieth_packet_path = repo_root() / rows[4900]["materialized_candidate_packet_path"]
        fiftieth_packet = json.loads(fiftieth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fiftieth_packet["unknown_candidate_id"], "obs-unk-004901")
        self.assertEqual(
            fiftieth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fiftieth_packet["identity_claim_status"], "no_identity_claim")
        fifty_first_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "067_undeciphered-005001-005100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_first_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_first_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_first_manifest_rows), 100)
        self.assertEqual(fifty_first_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005001")
        self.assertEqual(fifty_first_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005100")
        fifty_first_packet_path = repo_root() / rows[5000]["materialized_candidate_packet_path"]
        fifty_first_packet = json.loads(fifty_first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_first_packet["unknown_candidate_id"], "obs-unk-005001")
        self.assertEqual(
            fifty_first_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_first_packet["identity_claim_status"], "no_identity_claim")
        fifty_second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "068_undeciphered-005101-005200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_second_manifest_rows), 100)
        self.assertEqual(fifty_second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005101")
        self.assertEqual(fifty_second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005200")
        fifty_second_packet_path = repo_root() / rows[5100]["materialized_candidate_packet_path"]
        fifty_second_packet = json.loads(fifty_second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_second_packet["unknown_candidate_id"], "obs-unk-005101")
        self.assertEqual(
            fifty_second_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_second_packet["identity_claim_status"], "no_identity_claim")
        fifty_third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "069_undeciphered-005201-005300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_third_manifest_rows), 100)
        self.assertEqual(fifty_third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005201")
        self.assertEqual(fifty_third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005300")
        fifty_third_packet_path = repo_root() / rows[5200]["materialized_candidate_packet_path"]
        fifty_third_packet = json.loads(fifty_third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_third_packet["unknown_candidate_id"], "obs-unk-005201")
        self.assertEqual(
            fifty_third_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_third_packet["identity_claim_status"], "no_identity_claim")
        fifty_fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "070_undeciphered-005301-005400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_fourth_manifest_rows), 100)
        self.assertEqual(fifty_fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005301")
        self.assertEqual(fifty_fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005400")
        fifty_fourth_packet_path = repo_root() / rows[5300]["materialized_candidate_packet_path"]
        fifty_fourth_packet = json.loads(fifty_fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_fourth_packet["unknown_candidate_id"], "obs-unk-005301")
        self.assertEqual(
            fifty_fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_fourth_packet["identity_claim_status"], "no_identity_claim")
        fifty_fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "071_undeciphered-005401-005500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_fifth_manifest_rows), 100)
        self.assertEqual(fifty_fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005401")
        self.assertEqual(fifty_fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005500")
        fifty_fifth_packet_path = repo_root() / rows[5400]["materialized_candidate_packet_path"]
        fifty_fifth_packet = json.loads(fifty_fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_fifth_packet["unknown_candidate_id"], "obs-unk-005401")
        self.assertEqual(
            fifty_fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_fifth_packet["identity_claim_status"], "no_identity_claim")
        fifty_sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "072_undeciphered-005501-005600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_sixth_manifest_rows), 100)
        self.assertEqual(fifty_sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005501")
        self.assertEqual(fifty_sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005600")
        fifty_sixth_packet_path = repo_root() / rows[5500]["materialized_candidate_packet_path"]
        fifty_sixth_packet = json.loads(fifty_sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_sixth_packet["unknown_candidate_id"], "obs-unk-005501")
        self.assertEqual(
            fifty_sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_sixth_packet["identity_claim_status"], "no_identity_claim")
        fifty_seventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "073_undeciphered-005601-005700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_seventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_seventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_seventh_manifest_rows), 100)
        self.assertEqual(fifty_seventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005601")
        self.assertEqual(fifty_seventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005700")
        fifty_seventh_packet_path = repo_root() / rows[5600]["materialized_candidate_packet_path"]
        fifty_seventh_packet = json.loads(fifty_seventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_seventh_packet["unknown_candidate_id"], "obs-unk-005601")
        self.assertEqual(
            fifty_seventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_seventh_packet["identity_claim_status"], "no_identity_claim")
        fifty_eighth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "074_undeciphered-005701-005800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_eighth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_eighth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_eighth_manifest_rows), 100)
        self.assertEqual(fifty_eighth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005701")
        self.assertEqual(fifty_eighth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005800")
        fifty_eighth_packet_path = repo_root() / rows[5700]["materialized_candidate_packet_path"]
        fifty_eighth_packet = json.loads(fifty_eighth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_eighth_packet["unknown_candidate_id"], "obs-unk-005701")
        self.assertEqual(
            fifty_eighth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_eighth_packet["identity_claim_status"], "no_identity_claim")
        fifty_ninth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "075_undeciphered-005801-005900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with fifty_ninth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            fifty_ninth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(fifty_ninth_manifest_rows), 100)
        self.assertEqual(fifty_ninth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005801")
        self.assertEqual(fifty_ninth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-005900")
        fifty_ninth_packet_path = repo_root() / rows[5800]["materialized_candidate_packet_path"]
        fifty_ninth_packet = json.loads(fifty_ninth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(fifty_ninth_packet["unknown_candidate_id"], "obs-unk-005801")
        self.assertEqual(
            fifty_ninth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(fifty_ninth_packet["identity_claim_status"], "no_identity_claim")
        sixtieth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "076_undeciphered-005901-006000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixtieth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixtieth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixtieth_manifest_rows), 100)
        self.assertEqual(sixtieth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-005901")
        self.assertEqual(sixtieth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006000")
        sixtieth_packet_path = repo_root() / rows[5900]["materialized_candidate_packet_path"]
        sixtieth_packet = json.loads(sixtieth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixtieth_packet["unknown_candidate_id"], "obs-unk-005901")
        self.assertEqual(
            sixtieth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixtieth_packet["identity_claim_status"], "no_identity_claim")
        sixty_first_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "077_undeciphered-006001-006100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_first_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_first_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_first_manifest_rows), 100)
        self.assertEqual(sixty_first_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006001")
        self.assertEqual(sixty_first_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006100")
        sixty_first_packet_path = repo_root() / rows[6000]["materialized_candidate_packet_path"]
        sixty_first_packet = json.loads(sixty_first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_first_packet["unknown_candidate_id"], "obs-unk-006001")
        self.assertEqual(
            sixty_first_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_first_packet["identity_claim_status"], "no_identity_claim")
        sixty_second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "078_undeciphered-006101-006200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_second_manifest_rows), 100)
        self.assertEqual(sixty_second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006101")
        self.assertEqual(sixty_second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006200")
        sixty_second_packet_path = repo_root() / rows[6100]["materialized_candidate_packet_path"]
        sixty_second_packet = json.loads(sixty_second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_second_packet["unknown_candidate_id"], "obs-unk-006101")
        self.assertEqual(
            sixty_second_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_second_packet["identity_claim_status"], "no_identity_claim")
        sixty_third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "079_undeciphered-006201-006300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_third_manifest_rows), 100)
        self.assertEqual(sixty_third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006201")
        self.assertEqual(sixty_third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006300")
        sixty_third_packet_path = repo_root() / rows[6200]["materialized_candidate_packet_path"]
        sixty_third_packet = json.loads(sixty_third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_third_packet["unknown_candidate_id"], "obs-unk-006201")
        self.assertEqual(
            sixty_third_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_third_packet["identity_claim_status"], "no_identity_claim")
        sixty_fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "080_undeciphered-006301-006400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_fourth_manifest_rows), 100)
        self.assertEqual(sixty_fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006301")
        self.assertEqual(sixty_fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006400")
        sixty_fourth_packet_path = repo_root() / rows[6300]["materialized_candidate_packet_path"]
        sixty_fourth_packet = json.loads(sixty_fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_fourth_packet["unknown_candidate_id"], "obs-unk-006301")
        self.assertEqual(
            sixty_fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_fourth_packet["identity_claim_status"], "no_identity_claim")
        sixty_fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "081_undeciphered-006401-006500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_fifth_manifest_rows), 100)
        self.assertEqual(sixty_fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006401")
        self.assertEqual(sixty_fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006500")
        sixty_fifth_packet_path = repo_root() / rows[6400]["materialized_candidate_packet_path"]
        sixty_fifth_packet = json.loads(sixty_fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_fifth_packet["unknown_candidate_id"], "obs-unk-006401")
        self.assertEqual(
            sixty_fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_fifth_packet["identity_claim_status"], "no_identity_claim")
        sixty_sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "082_undeciphered-006501-006600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_sixth_manifest_rows), 100)
        self.assertEqual(sixty_sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006501")
        self.assertEqual(sixty_sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006600")
        sixty_sixth_packet_path = repo_root() / rows[6500]["materialized_candidate_packet_path"]
        sixty_sixth_packet = json.loads(sixty_sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_sixth_packet["unknown_candidate_id"], "obs-unk-006501")
        self.assertEqual(
            sixty_sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_sixth_packet["identity_claim_status"], "no_identity_claim")
        sixty_seventh_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "083_undeciphered-006601-006700_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_seventh_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_seventh_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_seventh_manifest_rows), 100)
        self.assertEqual(sixty_seventh_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006601")
        self.assertEqual(sixty_seventh_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006700")
        sixty_seventh_packet_path = repo_root() / rows[6600]["materialized_candidate_packet_path"]
        sixty_seventh_packet = json.loads(sixty_seventh_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_seventh_packet["unknown_candidate_id"], "obs-unk-006601")
        self.assertEqual(
            sixty_seventh_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_seventh_packet["identity_claim_status"], "no_identity_claim")
        sixty_eighth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "084_undeciphered-006701-006800_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_eighth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_eighth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_eighth_manifest_rows), 100)
        self.assertEqual(sixty_eighth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006701")
        self.assertEqual(sixty_eighth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006800")
        sixty_eighth_packet_path = repo_root() / rows[6700]["materialized_candidate_packet_path"]
        sixty_eighth_packet = json.loads(sixty_eighth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_eighth_packet["unknown_candidate_id"], "obs-unk-006701")
        self.assertEqual(
            sixty_eighth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_eighth_packet["identity_claim_status"], "no_identity_claim")
        sixty_ninth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "085_undeciphered-006801-006900_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with sixty_ninth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            sixty_ninth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(sixty_ninth_manifest_rows), 100)
        self.assertEqual(sixty_ninth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006801")
        self.assertEqual(sixty_ninth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-006900")
        sixty_ninth_packet_path = repo_root() / rows[6800]["materialized_candidate_packet_path"]
        sixty_ninth_packet = json.loads(sixty_ninth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(sixty_ninth_packet["unknown_candidate_id"], "obs-unk-006801")
        self.assertEqual(
            sixty_ninth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(sixty_ninth_packet["identity_claim_status"], "no_identity_claim")
        seventieth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "086_undeciphered-006901-007000_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventieth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventieth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventieth_manifest_rows), 100)
        self.assertEqual(seventieth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-006901")
        self.assertEqual(seventieth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007000")
        seventieth_packet_path = repo_root() / rows[6900]["materialized_candidate_packet_path"]
        seventieth_packet = json.loads(seventieth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventieth_packet["unknown_candidate_id"], "obs-unk-006901")
        self.assertEqual(
            seventieth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventieth_packet["identity_claim_status"], "no_identity_claim")
        seventy_first_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "087_undeciphered-007001-007100_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventy_first_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventy_first_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventy_first_manifest_rows), 100)
        self.assertEqual(seventy_first_manifest_rows[0]["unknown_candidate_id"], "obs-unk-007001")
        self.assertEqual(seventy_first_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007100")
        seventy_first_packet_path = repo_root() / rows[7000]["materialized_candidate_packet_path"]
        seventy_first_packet = json.loads(seventy_first_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventy_first_packet["unknown_candidate_id"], "obs-unk-007001")
        self.assertEqual(
            seventy_first_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventy_first_packet["identity_claim_status"], "no_identity_claim")
        seventy_second_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "088_undeciphered-007101-007200_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventy_second_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventy_second_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventy_second_manifest_rows), 100)
        self.assertEqual(seventy_second_manifest_rows[0]["unknown_candidate_id"], "obs-unk-007101")
        self.assertEqual(seventy_second_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007200")
        seventy_second_packet_path = repo_root() / rows[7100]["materialized_candidate_packet_path"]
        seventy_second_packet = json.loads(seventy_second_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventy_second_packet["unknown_candidate_id"], "obs-unk-007101")
        self.assertEqual(
            seventy_second_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventy_second_packet["identity_claim_status"], "no_identity_claim")
        seventy_third_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "089_undeciphered-007201-007300_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventy_third_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventy_third_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventy_third_manifest_rows), 100)
        self.assertEqual(seventy_third_manifest_rows[0]["unknown_candidate_id"], "obs-unk-007201")
        self.assertEqual(seventy_third_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007300")
        seventy_third_packet_path = repo_root() / rows[7200]["materialized_candidate_packet_path"]
        seventy_third_packet = json.loads(seventy_third_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventy_third_packet["unknown_candidate_id"], "obs-unk-007201")
        self.assertEqual(
            seventy_third_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventy_third_packet["identity_claim_status"], "no_identity_claim")
        seventy_fourth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "090_undeciphered-007301-007400_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventy_fourth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventy_fourth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventy_fourth_manifest_rows), 100)
        self.assertEqual(seventy_fourth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-007301")
        self.assertEqual(seventy_fourth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007400")
        seventy_fourth_packet_path = repo_root() / rows[7300]["materialized_candidate_packet_path"]
        seventy_fourth_packet = json.loads(seventy_fourth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventy_fourth_packet["unknown_candidate_id"], "obs-unk-007301")
        self.assertEqual(
            seventy_fourth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventy_fourth_packet["identity_claim_status"], "no_identity_claim")
        seventy_fifth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "091_undeciphered-007401-007500_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventy_fifth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventy_fifth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventy_fifth_manifest_rows), 100)
        self.assertEqual(seventy_fifth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-007401")
        self.assertEqual(seventy_fifth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007500")
        seventy_fifth_packet_path = repo_root() / rows[7400]["materialized_candidate_packet_path"]
        seventy_fifth_packet = json.loads(seventy_fifth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventy_fifth_packet["unknown_candidate_id"], "obs-unk-007401")
        self.assertEqual(
            seventy_fifth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventy_fifth_packet["identity_claim_status"], "no_identity_claim")
        seventy_sixth_bucket_manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "092_undeciphered-007501-007600_obs-unk-bucket_oracle-character-candidates/"
            / "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
        )
        with seventy_sixth_bucket_manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            seventy_sixth_manifest_rows = list(csv.DictReader(file))
        self.assertEqual(len(seventy_sixth_manifest_rows), 100)
        self.assertEqual(seventy_sixth_manifest_rows[0]["unknown_candidate_id"], "obs-unk-007501")
        self.assertEqual(seventy_sixth_manifest_rows[-1]["unknown_candidate_id"], "obs-unk-007600")
        seventy_sixth_packet_path = repo_root() / rows[7500]["materialized_candidate_packet_path"]
        seventy_sixth_packet = json.loads(seventy_sixth_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(seventy_sixth_packet["unknown_candidate_id"], "obs-unk-007501")
        self.assertEqual(
            seventy_sixth_packet["record_type"], "oracle_character_undeciphered_candidate_packet"
        )
        self.assertEqual(seventy_sixth_packet["identity_claim_status"], "no_identity_claim")
        self.assertEqual(rows[7600]["materialization_status"], "index_only_not_materialized")

    def test_hust_obc_undeciphered_candidate_index_builder_parses_zip_paths(self) -> None:
        module = load_hust_obc_undeciphered_candidate_index_module()
        self.assertEqual(
            module.group_from_zip_path("HUST-OBC/undeciphered/L/1/L00001.png"),
            ("L", "1"),
        )
        self.assertEqual(
            module.group_from_zip_path("HUST-OBC/undeciphered/Y+H/7/Y00007.png"),
            ("Y+H", "7"),
        )
        self.assertIsNone(module.group_from_zip_path("HUST-OBC/deciphered/1/0001.png"))
        self.assertEqual(module.external_ref_id("Y+H", 9408), "hust-obc-und-YH-009408")

    def test_relationship_graph_edges(self) -> None:
        self.assertEqual(check_relationship_graph_edges(repo_root()), [])

    def test_relationship_graph_statistics(self) -> None:
        self.assertEqual(check_relationship_graph_statistics(repo_root()), [])

    def test_source_coverage_statistics(self) -> None:
        self.assertEqual(check_source_coverage_statistics(repo_root()), [])

    def test_asset_image_visual_profile_builder_preserves_boundary(self) -> None:
        module = load_asset_image_visual_profiles_module()
        asset_index_path = repo_root() / "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
        with asset_index_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        visual_rows = module.build_visual_profiles(rows, repo_root())
        self.assertEqual(len(visual_rows), 3)
        self.assertEqual(visual_rows[0]["visual_profile_id"], "asset-visual-profile-000001")
        self.assertEqual(visual_rows[0]["luma_threshold"], "140")
        self.assertEqual(visual_rows[0]["foreground_pixel_count"], "154404")
        self.assertEqual(visual_rows[1]["foreground_pixel_count"], "1972665")
        self.assertEqual(visual_rows[2]["foreground_pixel_count"], "208710")
        self.assertEqual(
            {row["analysis_scope"] for row in visual_rows},
            {"visual_preprocessing_metadata_only"},
        )
        self.assertTrue(
            all("not glyph segmentation" in row["caution"] for row in visual_rows)
        )

    def test_ai_context_packs(self) -> None:
        self.assertEqual(check_ai_context_packs(repo_root()), [])

    def test_public_domain_asset_context_pack_preserves_asset_routes(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "006_ai-agent-public-domain-asset-context-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["context_pack_id"], "ai-context-public-domain-assets-001")
        self.assertEqual(data["status"], "reviewed_metadata_only")
        self.assertEqual(data["coverage"]["asset_count"], 3)
        self.assertEqual(
            data["coverage"]["source_ids"],
            ["src-metmuseum-oracle-bone", "src-smithsonian-nmaa-oracle-bone"],
        )
        self.assertEqual(data["coverage"]["rights_statuses"], ["public_domain_verified"])
        self.assertEqual(
            data["coverage"]["analysis_scopes"],
            ["image_technical_metadata_only", "visual_preprocessing_metadata_only"],
        )
        self.assertEqual(
            [asset["asset_id"] for asset in data["assets"]],
            ["asset-000001", "asset-000002", "asset-000003"],
        )
        self.assertEqual(data["assets"][0]["primary_external_ref_id"], "met-obj-42045")
        self.assertEqual(data["assets"][1]["primary_external_ref_id"], "met-obj-42022")
        self.assertEqual(data["assets"][2]["primary_external_ref_id"], "si-nmaa-fsc-o-26")
        self.assertEqual(data["assets"][0]["technical_profile"]["file_size_bytes"], 1780568)
        self.assertEqual(data["assets"][1]["technical_profile"]["icc_profile_bytes"], 3136)
        self.assertEqual(data["assets"][2]["technical_profile"]["icc_profile_bytes"], 560)
        self.assertEqual(data["assets"][0]["visual_profile"]["foreground_pixel_count"], 154404)
        self.assertEqual(data["assets"][1]["visual_profile"]["foreground_pixel_count"], 1972665)
        self.assertEqual(data["assets"][2]["visual_profile"]["foreground_pixel_count"], 208710)
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("not as a decipherment result", rules)
        self.assertIn("not glyph segmentation", rules)

    def test_public_domain_asset_context_pack_builder_merges_asset_records(self) -> None:
        module = load_public_domain_asset_context_pack_module()
        base = repo_root() / "project_registry/004_asset-source-and-rights-index"
        with (base / "001_asset-source-index.csv").open("r", encoding="utf-8-sig", newline="") as file:
            asset_rows = list(csv.DictReader(file))
        with (base / "002_asset-rights-review-log.csv").open("r", encoding="utf-8-sig", newline="") as file:
            rights_rows = list(csv.DictReader(file))
        with (base / "004_asset-image-technical-profile.csv").open("r", encoding="utf-8-sig", newline="") as file:
            technical_rows = list(csv.DictReader(file))
        with (base / "005_asset-image-visual-profile.csv").open("r", encoding="utf-8-sig", newline="") as file:
            visual_rows = list(csv.DictReader(file))
        data = module.build_context_pack(asset_rows, rights_rows, technical_rows, visual_rows)
        self.assertEqual(data["coverage"]["asset_count"], 3)
        self.assertEqual(data["assets"][0]["rights_review"]["rights_status_after"], "public_domain_verified")
        self.assertEqual(
            data["assets"][0]["technical_profile"]["checksum_sha256"],
            "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
        )
        self.assertEqual(data["assets"][1]["visual_profile"]["foreground_bbox"]["width"], 3425)
        self.assertEqual(data["assets"][2]["source_ids"], ["src-smithsonian-nmaa-oracle-bone"])
        self.assertEqual(
            data["assets"][2]["technical_profile"]["checksum_sha256"],
            "e4152d2d680234decb8d4b04225c83a59955b69bc4d8b10eebe7a98d54259079",
        )
        self.assertIn("资产索引", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_source_coverage_context_pack_preserves_routes(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "008_ai-agent-source-coverage-context-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["context_pack_id"], "ai-context-source-coverage-001")
        self.assertEqual(data["status"], "reviewed_metadata_only")
        self.assertEqual(data["coverage"]["source_count"], 21)
        self.assertEqual(data["coverage"]["download_manifest_count"], 44)
        self.assertEqual(data["coverage"]["download_log_count"], 44)
        self.assertEqual(data["coverage"]["metadata_profile_metric_count"], 48)
        self.assertEqual(data["coverage"]["committed_asset_count"], 3)
        self.assertEqual(data["coverage"]["committed_asset_bytes"], 4922128)
        self.assertEqual(data["coverage"]["graph_edge_count"], 99674)
        self.assertEqual(data["coverage"]["promotion_queue_candidate_count"], 1588)
        self.assertEqual(
            data["coverage"]["coverage_status_counts"],
            {
                "has_committed_public_asset_or_metadata": 2,
                "has_download_log_only": 12,
                "has_downloaded_metadata_profile": 4,
                "has_relationship_graph_derivatives": 3,
            },
        )
        source_routes = {
            entry["source_id"]: entry
            for entry in data["source_routes"]
        }
        self.assertEqual(len(source_routes), 21)
        self.assertEqual(source_routes["src-hust-obc"]["graph_edge_count"], 3562)
        self.assertEqual(source_routes["src-hust-obc"]["promotion_queue_candidate_count"], 1588)
        self.assertEqual(source_routes["src-obimd"]["graph_edge_count"], 44433)
        self.assertEqual(source_routes["src-evobc"]["graph_edge_count"], 51679)
        self.assertEqual(source_routes["src-metmuseum-oracle-bone"]["committed_asset_count"], 2)
        self.assertEqual(source_routes["src-smithsonian-nmaa-oracle-bone"]["committed_asset_count"], 1)
        self.assertEqual(
            [
                entry["source_id"]
                for entry in data["priority_routes"]["graph_derivative_sources"]
            ],
            ["src-evobc", "src-hust-obc", "src-obimd"],
        )
        self.assertEqual(
            [
                entry["source_id"]
                for entry in data["priority_routes"]["public_asset_sources"]
            ],
            ["src-metmuseum-oracle-bone", "src-smithsonian-nmaa-oracle-bone"],
        )
        self.assertEqual(
            [
                entry["source_id"]
                for entry in data["priority_routes"]["access_limited_or_error_sources"]
            ],
            [
                "src-british-museum-oracle-bone",
                "src-smithsonian-nmaa-oracle-bone",
                "src-xiaoxuetang-jiaguwen",
                "src-xiaoxuetang-obm",
            ],
        )
        rules = " ".join(data["agent_use_rules"])
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("not as evidence by itself", rules)
        self.assertIn("dataset-derived rows as candidates", rules)
        self.assertIn("Do not infer decipherment", rules)
        self.assertIn("已忽略临时目录", rules_zh)

    def test_ai_agent_source_coverage_context_pack_builder_keeps_boundaries(self) -> None:
        module = load_source_coverage_context_pack_module()
        path = repo_root() / "corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        data = module.build_context_pack(rows)
        source_routes = {
            entry["source_id"]: entry
            for entry in data["source_routes"]
        }
        self.assertEqual(data["coverage"]["source_count"], 21)
        self.assertEqual(data["coverage"]["graph_edge_count"], 99674)
        self.assertEqual(data["coverage"]["promotion_queue_candidate_count"], 1588)
        self.assertEqual(source_routes["src-hust-obc"]["route"], "open_graph_and_metadata_derivatives")
        self.assertEqual(source_routes["src-smithsonian-nmaa-oracle-bone"]["route"], "open_asset_and_rights_records")
        self.assertEqual(source_routes["src-smithsonian-nmaa-oracle-bone"]["committed_asset_count"], 1)
        self.assertEqual(
            source_routes["src-xiaoxuetang-jiaguwen"]["download_status_counts"],
            "downloaded_access_restricted_page:2",
        )
        rules = " ".join(data["agent_use_rules"])
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("source-routing and coverage summary", rules)
        self.assertIn("not as evidence by itself", rules)
        self.assertIn("Keep new downloads in ignored temporary directories", rules)
        self.assertIn("数据集派生记录", rules_zh)
        self.assertNotIn("confirmed scholarship", rules)

    def test_hust_obimd_evobc_codepoint_crosswalk_context_pack_preserves_lookup_boundaries(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "040_ai-agent-hust-obimd-evobc-codepoint-crosswalk-context-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            data["context_pack_id"],
            "ai-context-hust-obimd-evobc-codepoint-crosswalk-001",
        )
        self.assertEqual(data["status"], "reviewed_metadata_only")
        self.assertEqual(data["coverage"]["total_crosswalk_rows"], 1588)
        self.assertEqual(data["coverage"]["rows_with_any_obimd_or_evobc_codepoint_match"], 134)
        self.assertEqual(data["coverage"]["rows_with_obimd_codepoint_match"], 22)
        self.assertEqual(data["coverage"]["rows_with_evobc_codepoint_match"], 127)
        self.assertEqual(data["coverage"]["rows_with_both_obimd_and_evobc_codepoint_match"], 15)
        self.assertEqual(data["coverage"]["rows_without_obimd_or_evobc_codepoint_match"], 1454)
        self.assertEqual(data["coverage"]["total_obimd_match_count"], 22)
        self.assertEqual(data["coverage"]["total_evobc_match_count"], 127)
        self.assertEqual(data["coverage"]["evobc_image_reference_count_total"], 1518)
        self.assertEqual(data["coverage"]["evobc_oracle_ref_candidate_row_count"], 32)
        self.assertEqual(data["coverage"]["multi_component_label_row_count"], 173)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 1609)
        self.assertEqual(data["coverage"]["identity_claim_status_counts"], {"no_identity_claim": 1588})
        self.assertEqual(data["coverage"]["promotion_status_counts"], {"not_promoted": 1588})
        self.assertEqual(data["coverage"]["review_status_counts"], {"needs_cross_source_review": 1588})
        self.assertEqual(
            data["coverage"]["cross_source_status_counts"],
            {
                "matched_evobc_by_codepoint": 112,
                "matched_obimd_and_evobc_by_codepoint": 15,
                "matched_obimd_by_codepoint": 7,
                "no_obimd_or_evobc_codepoint_match": 1454,
            },
        )
        self.assertEqual(
            [row["source_id"] for row in data["source_routes"]],
            ["src-hust-obc", "src-obimd", "src-evobc"],
        )
        self.assertEqual(set(data["sample_rows_by_status"]), {
            "matched_evobc_by_codepoint",
            "matched_obimd_and_evobc_by_codepoint",
            "matched_obimd_by_codepoint",
            "no_obimd_or_evobc_codepoint_match",
        })
        three_source_sample = data["sample_rows_by_status"]["matched_obimd_and_evobc_by_codepoint"]
        self.assertEqual(three_source_sample["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(three_source_sample["hust_label_codepoints"], "U+342D")
        self.assertEqual(three_source_sample["identity_claim_status"], "no_identity_claim")
        self.assertIn("not decipherment conclusions", three_source_sample["caution"])
        rules = " ".join(data["agent_use_rules"])
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("codepoint lookup route", rules)
        self.assertIn("do not confirm oracle-character identity", rules)
        self.assertIn("current routing gap", rules)
        self.assertIn("codepoint 反查路由", rules_zh)
        self.assertIn("不等于确认甲骨字身份", rules_zh)

    def test_hust_obimd_evobc_codepoint_crosswalk_context_pack_builder_keeps_boundaries(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_context_pack_module()
        root = repo_root()
        data = module.build_context_pack(
            module.read_csv_rows(root / module.HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK),
            module.read_csv_rows(root / module.SOURCE_INDEX),
        )

        self.assertEqual(data["coverage"]["total_crosswalk_rows"], 1588)
        self.assertEqual(data["coverage"]["rows_with_any_obimd_or_evobc_codepoint_match"], 134)
        self.assertEqual(data["coverage"]["total_obimd_match_count"], 22)
        self.assertEqual(data["coverage"]["total_evobc_match_count"], 127)
        self.assertEqual(data["coverage"]["evobc_image_reference_count_total"], 1518)
        self.assertEqual(data["coverage"]["matched_source_set_counts"]["src-hust-obc;src-obimd;src-evobc"], 15)
        self.assertEqual(data["status_routes"][0]["claim_boundary"], "lookup_route_only_no_identity_or_decipherment_claim")
        self.assertEqual(data["source_routes"][1]["source_id"], "src-obimd")
        self.assertIn(
            module.OBIMD_MAIN_CHARACTER_STAGING.as_posix(),
            data["source_routes"][1]["route_files"],
        )
        self.assertIn(
            module.EVOBC_EVOLUTION_CATEGORY_STAGING.as_posix(),
            data["source_routes"][2]["route_files"],
        )
        self.assertIn("does not contain identity", data["purpose"])
        self.assertNotIn("confirmed scholarship", " ".join(data["agent_use_rules"]))

    def test_hust_obimd_evobc_codepoint_crosswalk_review_queue_prioritizes_matches(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 134)
        self.assertEqual(
            Counter(row["priority_bucket"] for row in rows),
            {
                "both_obimd_and_evobc_codepoint_match": 15,
                "obimd_only_codepoint_match": 7,
                "evobc_only_codepoint_match": 112,
            },
        )
        self.assertEqual(
            Counter(row["cross_source_status"] for row in rows),
            {
                "matched_obimd_and_evobc_by_codepoint": 15,
                "matched_obimd_by_codepoint": 7,
                "matched_evobc_by_codepoint": 112,
            },
        )
        self.assertEqual(rows[0]["codepoint_review_task_id"], "codepoint-crosswalk-review-001")
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[0]["priority_rank"], "1")
        self.assertEqual(rows[0]["matched_source_ids"], "src-hust-obc;src-obimd;src-evobc")
        self.assertEqual(rows[0]["hust_label_codepoints"], "U+342D")
        self.assertIn("obimd_main_character_staging_row", rows[0]["required_evidence_sections"])
        self.assertIn("evobc_evolution_category_staging_row", rows[0]["required_evidence_sections"])
        self.assertIn("040_ai-agent-hust-obimd-evobc-codepoint-crosswalk-context-pack.json", rows[0]["route_files_to_open"])
        self.assertTrue(rows[0]["expected_output_path"].startswith("doc/public/user_research/"))
        self.assertEqual(rows[0]["identity_claim_status"], "no_identity_claim")
        self.assertEqual(rows[0]["promotion_status"], "not_promoted")
        self.assertEqual(rows[0]["assignment_status"], "unassigned")
        self.assertEqual(rows[0]["task_status"], "needs_codepoint_cross_source_review")
        self.assertIn("not confirmed oracle-character identity", rows[0]["caution"])
        self.assertIn("not decipherment conclusions", rows[0]["caution"])
        self.assertEqual(rows[14]["codepoint_review_task_id"], "codepoint-crosswalk-review-015")
        self.assertEqual(rows[14]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001550")
        self.assertEqual(rows[15]["codepoint_review_task_id"], "codepoint-crosswalk-review-016")
        self.assertEqual(rows[15]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000057")
        self.assertEqual(rows[15]["priority_rank"], "2")
        self.assertEqual(rows[-1]["codepoint_review_task_id"], "codepoint-crosswalk-review-134")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001570")
        self.assertEqual(rows[-1]["priority_rank"], "3")
        self.assertTrue(all(row["research_boundary"].endswith("not_scholarship") for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_review_queue_builder_keeps_boundaries(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_review_queue_module()
        root = repo_root()
        rows = module.build_review_rows(
            module.read_json(root / module.CODEPOINT_CROSSWALK_CONTEXT_PACK),
            module.read_csv_rows(root / module.HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK),
        )

        self.assertEqual(len(rows), 134)
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[0]["priority_bucket"], "both_obimd_and_evobc_codepoint_match")
        self.assertEqual(rows[15]["priority_bucket"], "obimd_only_codepoint_match")
        self.assertEqual(rows[-1]["priority_bucket"], "evobc_only_codepoint_match")
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"not_promoted"})
        self.assertTrue(
            all("record_no_identity_or_decipherment_claim" in row["required_next_checks"] for row in rows)
        )
        self.assertTrue(
            all(module.CODEPOINT_CROSSWALK_CONTEXT_PACK.as_posix() in row["route_files_to_open"] for row in rows)
        )
        self.assertFalse(any(row["expected_output_path"].startswith("research/") for row in rows))
        self.assertIn("not component assignments", rows[0]["caution"])

    def test_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "042_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-log-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 15)
        self.assertEqual(
            {row["priority_bucket"] for row in rows},
            {"both_obimd_and_evobc_codepoint_match"},
        )
        self.assertEqual(
            {row["cross_source_status"] for row in rows},
            {"matched_obimd_and_evobc_by_codepoint"},
        )
        self.assertEqual(rows[0]["review_log_draft_id"], "codepoint-crosswalk-review-log-draft-001")
        self.assertEqual(rows[0]["codepoint_review_task_id"], "codepoint-crosswalk-review-001")
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[0]["draft_status"], "draft_not_collected")
        self.assertEqual(rows[0]["evidence_collection_status"], "not_collected")
        self.assertEqual(rows[0]["identity_claim_status"], "no_identity_claim")
        self.assertEqual(rows[0]["promotion_status"], "not_promoted")
        self.assertEqual(
            rows[0]["research_boundary"],
            "codepoint_crosswalk_review_log_draft_not_scholarship",
        )
        self.assertEqual(rows[-1]["codepoint_review_task_id"], "codepoint-crosswalk-review-015")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001550")
        self.assertTrue(all(row["draft_path"].startswith("doc/public/user_research/") for row in rows))
        self.assertFalse(any(row["draft_path"].startswith("research/") for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))

        draft_text = (repo_root() / rows[0]["draft_path"]).read_text(encoding="utf-8")
        for snippet in [
            "Codepoint Crosswalk Review Log Draft",
            "codepoint 交叉复核日志草稿",
            "draft_not_collected",
            "not_collected",
            "no_identity_claim",
            "not_promoted",
            "Route Files To Open",
            "Required Next Checks",
            "not a decipherment conclusion",
            "不是释读结论",
            "hust-obimd-evobc-xwalk-000047",
        ]:
            self.assertIn(snippet, draft_text)
        self.assertIn(rows[0]["route_files_to_open"].split(";")[0], draft_text)

    def test_hust_obimd_evobc_codepoint_crosswalk_review_log_draft_builder_links_queue(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts_module()
        root = repo_root()
        queue_rows = module.read_csv_rows(root / module.CODEPOINT_CROSSWALK_REVIEW_QUEUE)
        rows = module.build_draft_manifest_rows(queue_rows)

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["review_log_draft_id"], "codepoint-crosswalk-review-log-draft-001")
        self.assertEqual(rows[0]["codepoint_review_task_id"], "codepoint-crosswalk-review-001")
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[-1]["codepoint_review_task_id"], "codepoint-crosswalk-review-015")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001550")
        self.assertEqual({row["draft_status"] for row in rows}, {"draft_not_collected"})
        self.assertEqual({row["evidence_collection_status"] for row in rows}, {"not_collected"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"not_promoted"})
        self.assertTrue(all(row["source_queue_path"] == module.CODEPOINT_CROSSWALK_REVIEW_QUEUE.as_posix() for row in rows))
        self.assertFalse(any(row["draft_path"].startswith("research/") for row in rows))

        markdown = module.build_markdown(rows[0])
        self.assertIn("Route Files To Open", markdown)
        self.assertIn("Evidence Sections", markdown)
        self.assertIn("Required Next Checks", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)
        self.assertIn("不是释读结论", markdown)

    def test_hust_obimd_evobc_codepoint_crosswalk_review_route_results_are_metadata_only(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "043_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-route-results.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["review_log_draft_id"], "codepoint-crosswalk-review-log-draft-001")
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[0]["hust_candidate_packet_id"], "hust-obc-candidate-packet-000047")
        self.assertEqual(rows[0]["obimd_candidate_main_character_id"], "obimd-main-cand-002255")
        self.assertEqual(rows[0]["evobc_candidate_evolution_category_id"], "evobc-evo-cat-00005")
        self.assertEqual(rows[0]["route_file_count"], "9")
        self.assertEqual(rows[0]["missing_route_file_count"], "0")
        self.assertEqual(rows[0]["route_file_review_status"], "reviewed_route_files_exist")
        self.assertEqual(rows[0]["draft_log_status"], "draft_log_exists")
        self.assertEqual(rows[0]["source_register_match_count"], "3")
        self.assertEqual(rows[0]["download_log_match_count"], "5")
        self.assertEqual(rows[0]["download_checksum_present_count"], "5")
        self.assertGreater(int(rows[0]["download_total_file_size_bytes"]), 0)
        self.assertEqual(rows[0]["evidence_collection_status"], "not_collected")
        self.assertEqual(rows[0]["identity_claim_status"], "no_identity_claim")
        self.assertEqual(rows[0]["promotion_status"], "not_promoted")
        self.assertEqual(
            rows[0]["research_boundary"],
            "codepoint_crosswalk_review_route_result_metadata_only_not_scholarship",
        )
        self.assertIn("src-hust-obc=", rows[0]["source_register_rights_statuses"])
        self.assertIn("src-obimd=", rows[0]["source_register_rights_statuses"])
        self.assertIn("src-evobc=", rows[0]["source_register_rights_statuses"])
        self.assertIn("not a decipherment conclusion", rows[0]["caution"])
        self.assertEqual(rows[-1]["route_result_id"], "codepoint-crosswalk-route-result-015")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001550")
        self.assertTrue(all(row["research_boundary"].endswith("not_scholarship") for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_review_route_result_builder_links_routes(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_review_route_results_module()
        root = repo_root()
        rows = module.build_result_rows(
            module.read_csv_rows(root / module.CODEPOINT_REVIEW_LOG_DRAFT_MANIFEST),
            module.read_csv_rows(root / module.SOURCE_INDEX),
            module.read_csv_rows(root / module.SOURCE_DOWNLOAD_LOG),
            module.read_csv_rows(root / module.OBIMD_MAIN_CHARACTER_STAGING),
            module.read_csv_rows(root / module.EVOBC_EVOLUTION_CATEGORY_STAGING),
            root,
        )

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["hust_candidate_packet_id"], "hust-obc-candidate-packet-000047")
        self.assertEqual(rows[0]["hust_packet_review_status"], "needs_cross_source_review")
        self.assertEqual(rows[0]["obimd_codepoint_uplus"], "U+342D")
        self.assertEqual(rows[0]["evobc_source_character_codepoints"], "U+342D")
        self.assertEqual({row["route_file_review_status"] for row in rows}, {"reviewed_route_files_exist"})
        self.assertEqual(
            {row["source_register_review_status"] for row in rows},
            {"reviewed_required_sources_registered"},
        )
        self.assertEqual(
            {row["download_log_review_status"] for row in rows},
            {"reviewed_required_download_logs_registered"},
        )
        self.assertEqual({row["evidence_collection_status"] for row in rows}, {"not_collected"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"not_promoted"})
        self.assertTrue(all("not source evidence by itself" in row["caution"] for row in rows))
        self.assertFalse(any("accepted reading" in row["review_note"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_evidence_capture_scaffold_routes_sections(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "044_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-capture-scaffold.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 45)
        self.assertEqual(
            Counter(row["target_evidence_section"] for row in rows),
            {"candidate_packet": 15, "source_register": 15, "download_log": 15},
        )
        self.assertEqual(rows[0]["capture_task_id"], "codepoint-evidence-capture-001")
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[0]["target_evidence_section"], "candidate_packet")
        self.assertIn("hust-obc-candidate-packet-000047", rows[0]["source_record_refs"])
        self.assertIn("obimd-main-cand-002255", rows[0]["source_record_refs"])
        self.assertIn("evobc-evo-cat-00005", rows[0]["source_record_refs"])
        self.assertIn("hust_candidate_packet_id", rows[0]["capturable_field_names"])
        self.assertIn("route_result_id=codepoint-crosswalk-route-result-001", rows[0]["captured_metadata_summary"])
        self.assertEqual(rows[1]["target_evidence_section"], "source_register")
        self.assertEqual(rows[1]["source_record_refs"], "src-hust-obc;src-obimd;src-evobc")
        self.assertIn("source_register_rights_statuses", rows[1]["capturable_field_names"])
        self.assertIn("src-hust-obc=source_marked_risk_noted", rows[1]["captured_metadata_summary"])
        self.assertEqual(rows[2]["target_evidence_section"], "download_log")
        self.assertEqual(rows[2]["source_record_refs"].count("dl-"), 5)
        self.assertIn("download_total_file_size_bytes", rows[2]["capturable_field_names"])
        self.assertIn("download_checksum_present_count=5", rows[2]["captured_metadata_summary"])
        self.assertEqual({row["evidence_collection_status"] for row in rows}, {"not_collected"})
        self.assertEqual({row["capture_status"] for row in rows}, {"not_started"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"not_promoted"})
        self.assertTrue(all(row["research_boundary"].endswith("not_scholarship") for row in rows))
        self.assertTrue(all(not row["source_route_path"].startswith("research/") for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        self.assertEqual(rows[-1]["capture_task_id"], "codepoint-evidence-capture-045")
        self.assertEqual(rows[-1]["route_result_id"], "codepoint-crosswalk-route-result-015")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001550")

    def test_hust_obimd_evobc_codepoint_crosswalk_evidence_capture_scaffold_builder_links_route_results(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_evidence_capture_scaffold_module()
        root = repo_root()
        route_rows = module.read_csv_rows(root / module.ROUTE_RESULTS)
        rows = module.build_capture_rows(route_rows)

        self.assertEqual(len(rows), 45)
        self.assertEqual(rows[0]["capture_task_id"], "codepoint-evidence-capture-001")
        self.assertEqual(rows[0]["source_route_path"], route_rows[0]["hust_candidate_packet_path"])
        self.assertEqual(rows[1]["source_route_path"], module.SOURCE_REGISTER_PATH)
        self.assertEqual(rows[2]["source_route_path"], module.SOURCE_DOWNLOAD_LOG_PATH)
        self.assertEqual(
            [row["target_evidence_section"] for row in rows[:3]],
            ["candidate_packet", "source_register", "download_log"],
        )
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"codepoint_crosswalk_evidence_capture_scaffold_not_scholarship"},
        )
        self.assertEqual({row["evidence_collection_status"] for row in rows}, {"not_collected"})
        self.assertEqual({row["capture_status"] for row in rows}, {"not_started"})
        self.assertTrue(all("not collected source evidence" in row["caution"] for row in rows))
        self.assertFalse(any("accepted reading" in row["required_review_actions"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_source_register_capture_results_record_sources(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "045_ai-agent-hust-obimd-evobc-codepoint-crosswalk-source-register-capture-results.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 45)
        self.assertEqual(
            Counter(row["source_id"] for row in rows),
            {"src-hust-obc": 15, "src-obimd": 15, "src-evobc": 15},
        )
        self.assertEqual(rows[0]["capture_result_id"], "codepoint-source-register-capture-result-001")
        self.assertEqual(rows[0]["capture_task_id"], "codepoint-evidence-capture-002")
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[0]["authority_tier_evidence_value"], "peer_reviewed_dataset")
        self.assertEqual(rows[0]["rights_status_evidence_value"], "source_marked_risk_noted")
        self.assertEqual(rows[0]["review_status_evidence_value"], "reviewed")
        self.assertIn("Huazhong University", rows[0]["provider_evidence_value"])
        self.assertEqual(rows[1]["source_id"], "src-obimd")
        self.assertEqual(rows[1]["rights_status_evidence_value"], "licensed_for_repository")
        self.assertEqual(rows[2]["source_id"], "src-evobc")
        self.assertEqual(rows[2]["authority_tier_evidence_value"], "peer_reviewed_or_preprint_dataset")
        self.assertEqual(
            {row["source_register_evidence_status"] for row in rows},
            {"metadata_captured_from_reviewed_source_register"},
        )
        self.assertEqual(
            {row["evidence_collection_status"] for row in rows},
            {"source_register_metadata_captured"},
        )
        self.assertEqual(
            {row["rights_decision_status"] for row in rows},
            {"register_value_captured_no_new_decision"},
        )
        self.assertEqual({row["source_promotion_status"] for row in rows}, {"not_promoted"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["decipherment_claim_status"] for row in rows}, {"no_claim"})
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        self.assertEqual(rows[-1]["capture_result_id"], "codepoint-source-register-capture-result-045")
        self.assertEqual(rows[-1]["capture_task_id"], "codepoint-evidence-capture-044")
        self.assertEqual(rows[-1]["route_result_id"], "codepoint-crosswalk-route-result-015")
        self.assertEqual(rows[-1]["source_id"], "src-evobc")

    def test_hust_obimd_evobc_codepoint_crosswalk_source_register_capture_builder_uses_source_index(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_source_register_capture_results_module()
        root = repo_root()
        rows = module.build_capture_results(
            module.read_csv_rows(root / module.EVIDENCE_CAPTURE_SCAFFOLD),
            module.read_csv_rows(root / module.SOURCE_INDEX),
        )

        self.assertEqual(len(rows), 45)
        self.assertEqual(
            [row["source_id"] for row in rows[:3]],
            ["src-hust-obc", "src-obimd", "src-evobc"],
        )
        self.assertEqual(rows[0]["source_register_path"], module.SOURCE_INDEX.as_posix())
        self.assertEqual(rows[0]["source_type_evidence_value"], "open_research_dataset")
        self.assertEqual(rows[0]["rights_status_evidence_value"], "source_marked_risk_noted")
        self.assertEqual(rows[1]["rights_status_evidence_value"], "licensed_for_repository")
        self.assertEqual(rows[2]["rights_status_evidence_value"], "source_marked_risk_noted")
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"codepoint_crosswalk_source_register_capture_result_not_scholarship"},
        )
        self.assertTrue(all("not a new rights decision" in row["caution"] for row in rows))
        self.assertFalse(any("accepted reading" in row["required_next_checks"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_download_log_capture_results_record_downloads(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "046_ai-agent-hust-obimd-evobc-codepoint-crosswalk-download-log-capture-results.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 75)
        self.assertEqual(
            Counter(row["download_id"] for row in rows),
            {
                "dl-hust-obc-validation-label": 15,
                "dl-hust-obc-ocr-id-to-chinese": 15,
                "dl-obimd-main-character-json": 15,
                "dl-evobc-key-value-json": 15,
                "dl-evobc-list-json": 15,
            },
        )
        self.assertEqual(rows[0]["capture_result_id"], "codepoint-download-log-capture-result-001")
        self.assertEqual(rows[0]["capture_task_id"], "codepoint-evidence-capture-003")
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["download_id"], "dl-hust-obc-validation-label")
        self.assertEqual(rows[0]["source_id_evidence_value"], "src-hust-obc")
        self.assertEqual(rows[0]["status_evidence_value"], "downloaded")
        self.assertEqual(rows[0]["http_status_evidence_value"], "200")
        self.assertEqual(rows[0]["file_size_bytes_evidence_value"], "22087")
        self.assertEqual(
            rows[0]["checksum_sha256_evidence_value"],
            "406ad244008502401d6c0a690c7e0699896fbcb1b67cd09b36e5dc354158bd8f",
        )
        self.assertEqual(rows[4]["download_id"], "dl-evobc-list-json")
        self.assertEqual(rows[4]["file_size_bytes_evidence_value"], "23254733")
        self.assertEqual(
            {row["download_log_evidence_status"] for row in rows},
            {"metadata_captured_from_reviewed_download_log"},
        )
        self.assertEqual(
            {row["evidence_collection_status"] for row in rows},
            {"download_log_metadata_captured"},
        )
        self.assertEqual(
            {row["checksum_review_status"] for row in rows},
            {"checksum_value_captured_no_recalculation"},
        )
        self.assertEqual(
            {row["size_review_status"] for row in rows},
            {"size_value_captured_no_new_file_review"},
        )
        self.assertEqual(
            {row["access_review_status"] for row in rows},
            {"download_status_captured_no_new_access"},
        )
        self.assertEqual(
            {row["rights_decision_status"] for row in rows},
            {"download_log_value_captured_no_new_decision"},
        )
        self.assertEqual({row["source_promotion_status"] for row in rows}, {"not_promoted"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["decipherment_claim_status"] for row in rows}, {"no_claim"})
        self.assertTrue(all("not a new download" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        self.assertEqual(rows[-1]["capture_result_id"], "codepoint-download-log-capture-result-075")
        self.assertEqual(rows[-1]["capture_task_id"], "codepoint-evidence-capture-045")
        self.assertEqual(rows[-1]["route_result_id"], "codepoint-crosswalk-route-result-015")
        self.assertEqual(rows[-1]["download_id"], "dl-evobc-list-json")

    def test_hust_obimd_evobc_codepoint_crosswalk_download_log_capture_builder_uses_download_log(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_download_log_capture_results_module()
        root = repo_root()
        rows = module.build_capture_results(
            module.read_csv_rows(root / module.EVIDENCE_CAPTURE_SCAFFOLD),
            module.read_csv_rows(root / module.SOURCE_DOWNLOAD_LOG),
        )

        self.assertEqual(len(rows), 75)
        self.assertEqual(
            [row["download_id"] for row in rows[:5]],
            [
                "dl-hust-obc-validation-label",
                "dl-hust-obc-ocr-id-to-chinese",
                "dl-obimd-main-character-json",
                "dl-evobc-key-value-json",
                "dl-evobc-list-json",
            ],
        )
        self.assertEqual(rows[0]["download_log_path"], module.SOURCE_DOWNLOAD_LOG.as_posix())
        self.assertEqual(rows[0]["status_evidence_value"], "downloaded")
        self.assertEqual(rows[0]["file_size_bytes_evidence_value"], "22087")
        self.assertIn("checksum_sha256_present=true", rows[0]["captured_metadata_summary"])
        self.assertEqual(rows[4]["source_id_evidence_value"], "src-evobc")
        self.assertEqual(rows[4]["file_size_bytes_evidence_value"], "23254733")
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"codepoint_crosswalk_download_log_capture_result_not_scholarship"},
        )
        self.assertTrue(all("not a checksum recalculation" in row["caution"] for row in rows))
        self.assertFalse(any("accepted reading" in row["required_next_checks"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_candidate_packet_capture_results_record_packets(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "047_ai-agent-hust-obimd-evobc-codepoint-crosswalk-candidate-packet-capture-results.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["capture_result_id"], "codepoint-candidate-packet-capture-result-001")
        self.assertEqual(rows[0]["capture_task_id"], "codepoint-evidence-capture-001")
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["candidate_packet_id_evidence_value"], "hust-obc-candidate-packet-000047")
        self.assertEqual(rows[0]["source_candidate_class_id_evidence_value"], "obs-cand-000047")
        self.assertEqual(rows[0]["source_candidate_validation_class_id_evidence_value"], "46")
        self.assertEqual(rows[0]["source_candidate_source_category_id_padded_evidence_value"], "00055")
        self.assertEqual(rows[0]["dataset_label_status_evidence_value"], "dataset_label_candidate_not_accepted_reading")
        self.assertEqual(rows[0]["dataset_label_source_modern_label_codepoints_evidence_value"], "U+342D")
        self.assertEqual(rows[0]["rights_status_evidence_value"], "source_marked_risk_noted")
        self.assertEqual(rows[0]["review_status_evidence_value"], "needs_cross_source_review")
        self.assertIn("obimd-main-cand-002255", rows[0]["route_cross_source_refs_evidence_value"])
        self.assertIn("evobc-evo-cat-00005", rows[0]["route_cross_source_refs_evidence_value"])
        self.assertEqual(
            {row["candidate_packet_evidence_status"] for row in rows},
            {"metadata_captured_from_reviewed_candidate_packet"},
        )
        self.assertEqual(
            {row["evidence_collection_status"] for row in rows},
            {"candidate_packet_metadata_captured"},
        )
        self.assertEqual(
            {row["rights_decision_status"] for row in rows},
            {"packet_value_captured_no_new_decision"},
        )
        self.assertEqual(
            {row["cross_source_reference_status"] for row in rows},
            {"route_refs_recorded_for_later_review_not_identity_claim"},
        )
        self.assertEqual({row["source_promotion_status"] for row in rows}, {"not_promoted"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["decipherment_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["component_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["evolution_chain_claim_status"] for row in rows}, {"no_claim"})
        self.assertTrue(all("not an accepted reading" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        self.assertEqual(rows[-1]["capture_result_id"], "codepoint-candidate-packet-capture-result-015")
        self.assertEqual(rows[-1]["capture_task_id"], "codepoint-evidence-capture-043")
        self.assertEqual(rows[-1]["route_result_id"], "codepoint-crosswalk-route-result-015")
        self.assertEqual(rows[-1]["candidate_packet_id_evidence_value"], "hust-obc-candidate-packet-001550")
        self.assertEqual(rows[-1]["dataset_label_source_modern_label_codepoints_evidence_value"], "U+3AC3")

    def test_hust_obimd_evobc_codepoint_crosswalk_candidate_packet_capture_builder_uses_packets(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_candidate_packet_capture_results_module()
        root = repo_root()
        rows = module.build_capture_results(
            module.read_csv_rows(root / module.EVIDENCE_CAPTURE_SCAFFOLD),
            root,
        )

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["candidate_packet_id_evidence_value"], "hust-obc-candidate-packet-000047")
        self.assertEqual(rows[0]["record_type_evidence_value"], "oracle_character_candidate_packet")
        self.assertEqual(rows[0]["source_id_evidence_value"], "src-hust-obc")
        self.assertEqual(rows[0]["external_reference_ids_evidence_value"], "hust-obc-cat-0055;obs-cand-000047")
        self.assertEqual(
            rows[0]["evidence_download_ids_evidence_value"],
            "dl-hust-obc-validation-label;dl-hust-obc-ocr-id-to-chinese",
        )
        self.assertEqual(rows[0]["route_file_count_evidence_value"], "8")
        self.assertIn("candidate_packet_id=hust-obc-candidate-packet-000047", rows[0]["captured_metadata_summary"])
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"codepoint_crosswalk_candidate_packet_capture_result_not_scholarship"},
        )
        self.assertTrue(all("044 cross-source route refs only" in row["caution"] for row in rows))
        self.assertFalse(any("accepted reading" in row["required_next_checks"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_evidence_readiness_checklist_links_captures(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "048_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-readiness-checklist.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["readiness_check_id"], "codepoint-evidence-readiness-001")
        self.assertEqual(rows[0]["route_result_id"], "codepoint-crosswalk-route-result-001")
        self.assertEqual(rows[0]["candidate_packet_id"], "hust-obc-candidate-packet-000047")
        self.assertEqual(rows[0]["source_ids_captured"], "src-hust-obc;src-obimd;src-evobc")
        self.assertEqual(
            rows[0]["download_ids_captured"],
            "dl-hust-obc-validation-label;dl-hust-obc-ocr-id-to-chinese;"
            "dl-obimd-main-character-json;dl-evobc-key-value-json;dl-evobc-list-json",
        )
        self.assertEqual(rows[0]["candidate_packet_capture_count"], "1")
        self.assertEqual(rows[0]["source_register_capture_count"], "3")
        self.assertEqual(rows[0]["download_log_capture_count"], "5")
        self.assertEqual(rows[0]["captured_section_count"], "3")
        self.assertEqual(rows[0]["missing_required_sections"], "none")
        self.assertIn("src-obimd=licensed_for_repository", rows[0]["source_register_rights_statuses"])
        self.assertIn("dl-evobc-list-json=downloaded:200", rows[0]["download_log_access_statuses"])
        self.assertEqual(
            {row["overall_readiness_status"] for row in rows},
            {"ready_for_human_evidence_pack_review_metadata_only"},
        )
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["decipherment_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["component_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["evolution_chain_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["source_promotion_status"] for row in rows}, {"not_promoted"})
        self.assertEqual({row["rights_decision_status"] for row in rows}, {"no_new_rights_decision"})
        self.assertTrue(all("not source evidence by itself" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        self.assertEqual(rows[-1]["readiness_check_id"], "codepoint-evidence-readiness-015")
        self.assertEqual(rows[-1]["route_result_id"], "codepoint-crosswalk-route-result-015")
        self.assertEqual(rows[-1]["candidate_packet_id"], "hust-obc-candidate-packet-001550")

    def test_hust_obimd_evobc_codepoint_crosswalk_evidence_readiness_builder_uses_capture_rows(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_evidence_readiness_checklist_module()
        root = repo_root()
        rows = module.build_readiness_rows(
            module.read_csv_rows(root / module.CANDIDATE_PACKET_CAPTURE_RESULTS),
            module.read_csv_rows(root / module.SOURCE_REGISTER_CAPTURE_RESULTS),
            module.read_csv_rows(root / module.DOWNLOAD_LOG_CAPTURE_RESULTS),
        )

        self.assertEqual(len(rows), 15)
        self.assertEqual(rows[0]["candidate_packet_capture_result_id"], "codepoint-candidate-packet-capture-result-001")
        self.assertEqual(
            rows[0]["source_register_capture_result_ids"],
            "codepoint-source-register-capture-result-001;codepoint-source-register-capture-result-002;"
            "codepoint-source-register-capture-result-003",
        )
        self.assertEqual(
            rows[0]["download_log_capture_result_ids"],
            "codepoint-download-log-capture-result-001;codepoint-download-log-capture-result-002;"
            "codepoint-download-log-capture-result-003;codepoint-download-log-capture-result-004;"
            "codepoint-download-log-capture-result-005",
        )
        self.assertEqual(rows[0]["source_register_evidence_statuses"], "metadata_captured_from_reviewed_source_register=3")
        self.assertEqual(rows[0]["download_log_evidence_statuses"], "metadata_captured_from_reviewed_download_log=5")
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"codepoint_crosswalk_evidence_readiness_checklist_not_scholarship"},
        )
        self.assertTrue(all("verify_candidate_packet_source_register_download_log_rows" in row["required_next_checks"] for row in rows))
        self.assertFalse(any("accepted reading" in row["required_next_checks"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_route_availability_snapshot_covers_review_queue(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "049_ai-agent-hust-obimd-evobc-codepoint-crosswalk-route-availability-snapshot.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 134)
        self.assertEqual(
            Counter(row["priority_bucket"] for row in rows),
            Counter(
                {
                    "both_obimd_and_evobc_codepoint_match": 15,
                    "obimd_only_codepoint_match": 7,
                    "evobc_only_codepoint_match": 112,
                }
            ),
        )
        self.assertEqual(
            Counter(row["review_log_materialization_status"] for row in rows),
            Counter({"draft_log_exists": 15, "draft_log_not_materialized": 119}),
        )
        self.assertEqual(rows[0]["route_availability_id"], "codepoint-route-availability-001")
        self.assertEqual(rows[0]["codepoint_review_task_id"], "codepoint-crosswalk-review-001")
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[0]["obimd_row_count"], "1")
        self.assertEqual(rows[0]["evobc_row_count"], "1")
        self.assertEqual(rows[0]["download_log_match_count"], "5")
        self.assertEqual(rows[15]["route_availability_id"], "codepoint-route-availability-016")
        self.assertEqual(rows[15]["priority_bucket"], "obimd_only_codepoint_match")
        self.assertEqual(rows[15]["obimd_row_count"], "1")
        self.assertEqual(rows[15]["evobc_row_count"], "0")
        self.assertEqual(rows[15]["download_log_match_count"], "3")
        self.assertEqual(rows[-1]["route_availability_id"], "codepoint-route-availability-134")
        self.assertEqual(rows[-1]["priority_bucket"], "evobc_only_codepoint_match")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001570")
        self.assertEqual(rows[-1]["obimd_row_count"], "0")
        self.assertEqual(rows[-1]["evobc_row_count"], "1")
        self.assertEqual(rows[-1]["download_log_match_count"], "4")
        self.assertEqual({row["route_file_review_status"] for row in rows}, {"reviewed_route_files_exist"})
        self.assertEqual({row["missing_route_file_count"] for row in rows}, {"0"})
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["decipherment_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["component_claim_status"] for row in rows}, {"no_claim"})
        self.assertEqual({row["evolution_chain_claim_status"] for row in rows}, {"no_claim"})
        self.assertTrue(all("not source evidence by itself" in row["caution"] for row in rows))

    def test_hust_obimd_evobc_codepoint_crosswalk_route_availability_builder_rebuilds_snapshot(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_route_availability_snapshot_module()
        root = repo_root()
        rows = module.build_availability_rows(
            module.read_csv_rows(root / module.CODEPOINT_REVIEW_QUEUE),
            module.read_csv_rows(root / module.SOURCE_INDEX),
            module.read_csv_rows(root / module.SOURCE_DOWNLOAD_LOG),
            module.read_csv_rows(root / module.OBIMD_MAIN_CHARACTER_STAGING),
            module.read_csv_rows(root / module.EVOBC_EVOLUTION_CATEGORY_STAGING),
            root,
        )

        self.assertEqual(len(rows), 134)
        self.assertEqual(rows[0]["hust_candidate_packet_id"], "hust-obc-candidate-packet-000047")
        self.assertEqual(rows[0]["download_ids_required"], "dl-hust-obc-validation-label;dl-hust-obc-ocr-id-to-chinese;dl-obimd-main-character-json;dl-evobc-key-value-json;dl-evobc-list-json")
        self.assertEqual(rows[15]["download_ids_required"], "dl-hust-obc-validation-label;dl-hust-obc-ocr-id-to-chinese;dl-obimd-main-character-json")
        self.assertEqual(rows[-1]["download_ids_required"], "dl-hust-obc-validation-label;dl-hust-obc-ocr-id-to-chinese;dl-evobc-key-value-json;dl-evobc-list-json")
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"codepoint_crosswalk_route_availability_snapshot_not_scholarship"},
        )
        self.assertEqual(
            {row["evidence_collection_status"] for row in rows},
            {"availability_metadata_captured_not_evidence"},
        )
        self.assertTrue(all("verify_matched_source_staging_rows" in row["required_next_checks"] for row in rows))
        self.assertFalse(any("accepted reading" in row["required_next_checks"] for row in rows))

    def test_ai_agent_source_route_review_queue_prioritizes_safe_next_checks(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "009_ai-agent-source-route-review-queue.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 21)
        self.assertEqual(rows[0]["source_route_task_id"], "source-route-review-001")
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[0]["priority_rank"], "1")
        self.assertEqual(
            rows[0]["priority_tags"],
            "candidate_queue;graph_derivative;metadata_profile;download_log",
        )
        self.assertIn(
            "corpus/001_oracle-characters/000_character-registers/"
            "009_hust-obc-obs-char-promotion-review-queue.csv",
            rows[0]["route_files"],
        )
        self.assertIn(
            "verify_candidate_queue_rows_remain_reserved_and_cross_source_review_only",
            rows[0]["required_next_checks"],
        )
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(by_source["src-evobc"]["priority_rank"], "2")
        self.assertIn(
            "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl",
            by_source["src-evobc"]["route_files"],
        )
        self.assertEqual(by_source["src-metmuseum-oracle-bone"]["priority_rank"], "3")
        self.assertIn(
            "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv",
            by_source["src-metmuseum-oracle-bone"]["route_files"],
        )
        self.assertEqual(
            by_source["src-smithsonian-nmaa-oracle-bone"]["priority_tags"],
            "public_asset;access_limited_or_error;metadata_profile;download_log",
        )
        self.assertIn(
            "review_download_log_status_and_record_retry_or_metadata_only_decision",
            by_source["src-smithsonian-nmaa-oracle-bone"]["required_next_checks"],
        )
        self.assertEqual(by_source["src-british-museum-oracle-bone"]["priority_rank"], "4")
        self.assertEqual(by_source["src-nlc-oracle-world"]["priority_rank"], "5")
        self.assertEqual(by_source["src-yinqi-wenyuan"]["priority_rank"], "6")
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"routing_metadata_only_not_scholarship"},
        )
        self.assertTrue(
            all("decipherment conclusions" in row["caution"] for row in rows)
        )

    def test_ai_agent_source_route_review_queue_builder_keeps_boundary(self) -> None:
        module = load_source_route_review_queue_module()
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "008_ai-agent-source-coverage-context-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = module.build_queue_rows(data)
        self.assertEqual(len(rows), 21)
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[0]["context_pack_id"], "ai-context-source-coverage-001")
        self.assertEqual(rows[0]["research_boundary"], "routing_metadata_only_not_scholarship")
        self.assertEqual(rows[1]["source_id"], "src-evobc")
        self.assertEqual(rows[2]["source_id"], "src-obimd")
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(
            by_source["src-xiaoxuetang-jiaguwen"]["review_focus"],
            "open_download_logs_and_resolve_access_or_error_boundary",
        )
        self.assertIn(
            "corpus/006_research-sources-and-bibliography/000_source-registers/"
            "013_source-download-status-codebook.csv",
            by_source["src-xiaoxuetang-jiaguwen"]["route_files"],
        )
        self.assertIn(
            "confirm_source_size_checksum_rights_and_risk_before_promoting_derivatives",
            by_source["src-yinqi-wenyuan"]["required_next_checks"],
        )
        self.assertNotIn("confirmed scholarship", rows[0]["caution"])

    def test_ai_agent_source_route_review_result_scaffold_is_empty(self) -> None:
        queue_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "009_ai-agent-source-route-review-queue.csv"
        )
        result_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "010_ai-agent-source-route-review-result-scaffold.csv"
        )
        with queue_path.open("r", encoding="utf-8-sig", newline="") as file:
            queue_rows = list(csv.DictReader(file))
        with result_path.open("r", encoding="utf-8-sig", newline="") as file:
            result_rows = list(csv.DictReader(file))
        self.assertEqual(len(result_rows), 21)
        self.assertEqual(len(result_rows), len(queue_rows))
        self.assertEqual(result_rows[0]["source_route_result_id"], "source-route-result-001")
        self.assertEqual(result_rows[0]["source_route_task_id"], "source-route-review-001")
        self.assertEqual(result_rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(result_rows[0]["route_files_to_open"], queue_rows[0]["route_files"])
        self.assertEqual(result_rows[0]["required_next_checks"], queue_rows[0]["required_next_checks"])
        self.assertEqual(
            {row["result_status"] for row in result_rows},
            {"not_started"},
        )
        self.assertEqual(
            {row["source_register_review_status"] for row in result_rows},
            {"not_collected"},
        )
        self.assertEqual(
            {row["rights_and_risk_review_status"] for row in result_rows},
            {"not_collected"},
        )
        self.assertEqual(
            {row["derivative_promotion_status"] for row in result_rows},
            {"not_decided"},
        )
        self.assertEqual(
            {row["research_boundary"] for row in result_rows},
            {"review_result_scaffold_not_scholarship"},
        )
        self.assertTrue(
            all("Do not use it as source evidence" in row["caution"] for row in result_rows)
        )
        self.assertTrue(
            all("decipherment conclusion" in row["caution"] for row in result_rows)
        )

    def test_ai_agent_source_route_review_result_scaffold_builder_keeps_empty_sections(self) -> None:
        module = load_source_route_review_result_scaffold_module()
        queue_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "009_ai-agent-source-route-review-queue.csv"
        )
        with queue_path.open("r", encoding="utf-8-sig", newline="") as file:
            queue_rows = list(csv.DictReader(file))
        result_rows = module.build_result_rows(queue_rows)
        self.assertEqual(len(result_rows), 21)
        self.assertEqual(result_rows[0]["source_route_result_id"], "source-route-result-001")
        self.assertEqual(result_rows[0]["source_route_task_id"], queue_rows[0]["source_route_task_id"])
        self.assertEqual(result_rows[4]["source_id"], "src-smithsonian-nmaa-oracle-bone")
        self.assertEqual(result_rows[4]["priority_tags"], queue_rows[4]["priority_tags"])
        self.assertEqual(result_rows[4]["route_files_to_open"], queue_rows[4]["route_files"])
        self.assertEqual(result_rows[4]["result_status"], "not_started")
        self.assertEqual(result_rows[4]["evidence_gap_status"], "not_collected")
        self.assertEqual(result_rows[4]["next_artifact_recommendation"], "not_collected")
        self.assertEqual(result_rows[4]["output_scope"], "source_route_review_scaffold_only")
        self.assertNotIn("confirmed scholarship", result_rows[4]["caution"])
        self.assertNotIn("public_domain_verified", result_rows[4]["derivative_promotion_status"])

    def test_ai_agent_source_route_review_results_record_graph_derived_metadata_reviews(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "011_ai-agent-source-route-review-results.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(by_source["src-hust-obc"]["source_route_result_id"], "source-route-result-001")
        self.assertEqual(by_source["src-hust-obc"]["source_route_task_id"], "source-route-review-001")
        self.assertEqual(by_source["src-hust-obc"]["candidate_queue_count"], "1588")
        self.assertEqual(by_source["src-hust-obc"]["evidence_request_count"], "1588")
        self.assertEqual(by_source["src-hust-obc"]["graph_edge_count"], "3562")
        self.assertEqual(by_source["src-hust-obc"]["raw_package_file_size_bytes"], "607933810")
        self.assertIn(
            "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl",
            by_source["src-hust-obc"]["route_files_opened"],
        )
        self.assertIn("dataset labels remain candidates", by_source["src-hust-obc"]["review_note"])
        self.assertEqual(by_source["src-evobc"]["source_route_result_id"], "source-route-result-002")
        self.assertEqual(by_source["src-evobc"]["source_route_task_id"], "source-route-review-002")
        self.assertEqual(by_source["src-evobc"]["metadata_profile_metric_count"], "7")
        self.assertEqual(by_source["src-evobc"]["download_log_count"], "5")
        self.assertEqual(by_source["src-evobc"]["source_package_file_manifest_count"], "3")
        self.assertEqual(by_source["src-evobc"]["graph_edge_count"], "51679")
        self.assertEqual(by_source["src-evobc"]["raw_package_file_size_bytes"], "23254733")
        self.assertIn("EVOBC category, era-code", by_source["src-evobc"]["review_note"])
        self.assertIn(
            "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl",
            by_source["src-evobc"]["route_files_opened"],
        )
        self.assertEqual(by_source["src-obimd"]["source_route_result_id"], "source-route-result-003")
        self.assertEqual(by_source["src-obimd"]["source_route_task_id"], "source-route-review-003")
        self.assertEqual(by_source["src-obimd"]["metadata_profile_metric_count"], "5")
        self.assertEqual(by_source["src-obimd"]["download_log_count"], "6")
        self.assertEqual(by_source["src-obimd"]["source_package_file_manifest_count"], "7")
        self.assertEqual(by_source["src-obimd"]["graph_edge_count"], "44433")
        self.assertEqual(by_source["src-obimd"]["raw_package_file_size_bytes"], "558367972")
        self.assertIn("OBIMD main-character, subcharacter", by_source["src-obimd"]["review_note"])
        self.assertIn(
            "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
            by_source["src-obimd"]["route_files_opened"],
        )
        self.assertEqual(
            {row["result_status"] for row in rows},
            {"reviewed_metadata_routes_only"},
        )
        self.assertEqual(
            {row["derivative_promotion_status"] for row in rows},
            {"no_raw_asset_or_dataset_claim_promotion"},
        )
        self.assertTrue(all("not a decipherment result" in row["caution"] for row in rows))
        self.assertTrue(all("not a rights clearance" in row["caution"] for row in rows))
        self.assertTrue(all("graph edges" in row["caution"] for row in rows))

    def test_ai_agent_source_route_review_results_builder_reads_graph_derived_routes(self) -> None:
        module = load_source_route_review_results_module()
        root = repo_root()
        rows = module.build_review_rows(
            module.read_csv_rows(root / module.SOURCE_ROUTE_REVIEW_QUEUE),
            module.read_csv_rows(root / module.SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD),
            module.read_csv_rows(root / module.SOURCE_COVERAGE_SUMMARY),
            module.read_csv_rows(root / module.SOURCE_INDEX),
            module.read_csv_rows(root / module.DOWNLOADED_METADATA_PROFILE),
            module.read_csv_rows(root / module.SOURCE_DOWNLOAD_LOG),
            module.read_csv_rows(root / module.SOURCE_PACKAGE_FILE_MANIFEST),
            module.read_csv_rows(root / module.HUST_OBC_OBS_CHAR_PROMOTION_QUEUE),
            module.read_csv_rows(root / module.AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE),
            {
                source_id: module.read_jsonl_count(root / graph_file)
                for source_id, graph_file in module.GRAPH_EDGE_FILES_BY_SOURCE.items()
            },
            root=root,
        )
        self.assertEqual(len(rows), 3)
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(by_source["src-hust-obc"]["route_file_review_status"], "reviewed_route_files_exist")
        self.assertEqual(by_source["src-hust-obc"]["candidate_queue_count"], "1588")
        self.assertEqual(by_source["src-hust-obc"]["graph_edge_count"], "3562")
        self.assertEqual(by_source["src-evobc"]["candidate_queue_count"], "0")
        self.assertEqual(by_source["src-evobc"]["graph_edge_count"], "51679")
        self.assertEqual(
            by_source["src-evobc"]["size_checksum_review_status"],
            "downloaded_metadata_files_logged_tmp_only",
        )
        self.assertEqual(by_source["src-obimd"]["candidate_queue_count"], "0")
        self.assertEqual(by_source["src-obimd"]["graph_edge_count"], "44433")
        self.assertEqual(by_source["src-obimd"]["raw_package_commit_policy"], "do_not_commit_regular_git")
        self.assertTrue(all("confirmed scholarship" not in row["caution"] for row in rows))
        self.assertTrue(
            all(row["derivative_promotion_status"] != "public_domain_verified" for row in rows)
        )

    def test_ai_agent_graph_source_cross_review_queue_records_first_review_tasks(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "012_ai-agent-graph-source-cross-review-queue.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(
            by_source["src-hust-obc"]["cross_review_task_id"],
            "graph-source-cross-review-001",
        )
        self.assertEqual(
            by_source["src-hust-obc"]["primary_review_record_id"],
            "hust-obc-evidence-request-000001",
        )
        self.assertEqual(by_source["src-hust-obc"]["related_project_id"], "obs-char-000001")
        self.assertEqual(by_source["src-hust-obc"]["candidate_or_staging_row_count"], "1588")
        self.assertIn("source category 0001", by_source["src-hust-obc"]["review_note"])
        self.assertIn(
            "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv",
            by_source["src-hust-obc"]["route_files_to_open"],
        )
        self.assertEqual(
            by_source["src-evobc"]["primary_review_record_id"],
            "evobc-evo-cat-00001",
        )
        self.assertEqual(by_source["src-evobc"]["primary_external_ref_id"], "evobc-cat-00001")
        self.assertEqual(by_source["src-evobc"]["candidate_or_staging_row_count"], "13714")
        self.assertIn("source_character_codepoints=U+3401", by_source["src-evobc"]["review_note"])
        self.assertIn(
            "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            "001_evobc-evolution-category-staging.csv",
            by_source["src-evobc"]["route_files_to_open"],
        )
        self.assertEqual(
            by_source["src-obimd"]["primary_review_record_id"],
            "obimd-sub-cand-000001",
        )
        self.assertEqual(by_source["src-obimd"]["related_project_id"], "obimd-main-cand-000001")
        self.assertEqual(by_source["src-obimd"]["primary_external_ref_id"], "obimd-sub-p8w7ujqanz")
        self.assertEqual(by_source["src-obimd"]["candidate_or_staging_row_count"], "2747")
        self.assertIn("glyph_codepoint_uplus=U+65E5;U+F0000", by_source["src-obimd"]["review_note"])
        self.assertIn(
            "corpus/003_graphemic-components/000_component-registers/"
            "003_obimd-subcharacter-glyph-staging.csv",
            by_source["src-obimd"]["route_files_to_open"],
        )
        self.assertEqual(
            {row["task_status"] for row in rows},
            {"needs_cross_source_review"},
        )
        self.assertEqual({row["promotion_status"] for row in rows}, {"not_promoted"})
        self.assertTrue(all("not a decipherment result" in row["caution"] for row in rows))
        self.assertTrue(all("not a rights clearance" in row["caution"] for row in rows))
        self.assertTrue(all("staging rows" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_cross_review_queue_builder_reads_first_review_tasks(self) -> None:
        module = load_graph_source_cross_review_queue_module()
        root = repo_root()
        rows = module.build_cross_review_rows(
            module.read_csv_rows(root / module.SOURCE_ROUTE_REVIEW_RESULTS),
            module.read_csv_rows(root / module.AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE),
            module.read_csv_rows(root / module.HUST_OBC_OBS_CHAR_PROMOTION_QUEUE),
            module.read_csv_rows(root / module.EVOBC_EVOLUTION_CATEGORY_STAGING),
            module.read_csv_rows(root / module.EVOBC_ERA_SOURCE_CODEBOOK_STAGING),
            module.read_csv_rows(root / module.OBIMD_MAIN_CHARACTER_STAGING),
            module.read_csv_rows(root / module.OBIMD_SUBCHARACTER_MAIN_STAGING),
            module.read_csv_rows(root / module.OBIMD_SUBCHARACTER_GLYPH_STAGING),
        )
        self.assertEqual(len(rows), 3)
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(by_source["src-hust-obc"]["source_route_result_id"], "source-route-result-001")
        self.assertEqual(by_source["src-hust-obc"]["primary_external_ref_id"], "hust-obc-cat-0001")
        self.assertEqual(by_source["src-hust-obc"]["graph_edge_count"], "3562")
        self.assertEqual(by_source["src-evobc"]["source_route_result_id"], "source-route-result-002")
        self.assertEqual(by_source["src-evobc"]["source_record_id"], "00001")
        self.assertEqual(by_source["src-evobc"]["graph_edge_count"], "51679")
        self.assertEqual(by_source["src-obimd"]["source_route_result_id"], "source-route-result-003")
        self.assertEqual(by_source["src-obimd"]["source_record_id"], "p8w7ujqanz")
        self.assertEqual(by_source["src-obimd"]["graph_edge_count"], "44433")
        self.assertTrue(all("confirmed scholarship" not in row["caution"] for row in rows))
        self.assertTrue(all(row["research_boundary"].endswith("not_scholarship") for row in rows))

    def test_ai_agent_graph_source_cross_review_log_scaffold_is_empty(self) -> None:
        queue_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "012_ai-agent-graph-source-cross-review-queue.csv"
        )
        scaffold_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "013_ai-agent-graph-source-cross-review-log-scaffold.csv"
        )
        with queue_path.open("r", encoding="utf-8-sig", newline="") as file:
            queue_rows = list(csv.DictReader(file))
        with scaffold_path.open("r", encoding="utf-8-sig", newline="") as file:
            scaffold_rows = list(csv.DictReader(file))
        self.assertEqual(len(scaffold_rows), 3)
        self.assertEqual(len(scaffold_rows), len(queue_rows))
        self.assertEqual(
            [row["source_id"] for row in scaffold_rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual(scaffold_rows[0]["cross_review_log_id"], "graph-source-cross-review-log-001")
        self.assertEqual(scaffold_rows[0]["cross_review_task_id"], queue_rows[0]["cross_review_task_id"])
        self.assertEqual(scaffold_rows[0]["expected_output_path"], queue_rows[0]["expected_output_path"])
        self.assertEqual(scaffold_rows[1]["primary_review_record_id"], "evobc-evo-cat-00001")
        self.assertEqual(scaffold_rows[2]["primary_review_record_id"], "obimd-sub-cand-000001")
        self.assertEqual({row["result_status"] for row in scaffold_rows}, {"not_started"})
        self.assertEqual(
            {row["source_register_review_status"] for row in scaffold_rows},
            {"not_collected"},
        )
        self.assertEqual(
            {row["counter_source_lookup_status"] for row in scaffold_rows},
            {"not_collected"},
        )
        self.assertEqual(
            {row["promotion_decision_status"] for row in scaffold_rows},
            {"not_decided"},
        )
        self.assertEqual(
            {row["research_boundary"] for row in scaffold_rows},
            {"cross_source_review_log_scaffold_not_scholarship"},
        )
        self.assertTrue(all("Do not use it as source evidence" in row["caution"] for row in scaffold_rows))
        self.assertTrue(all("decipherment conclusion" in row["caution"] for row in scaffold_rows))

    def test_ai_agent_graph_source_cross_review_log_scaffold_builder_keeps_empty_sections(self) -> None:
        module = load_graph_source_cross_review_log_scaffold_module()
        root = repo_root()
        queue_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_CROSS_REVIEW_QUEUE)
        scaffold_rows = module.build_log_scaffold_rows(queue_rows)
        self.assertEqual(len(scaffold_rows), 3)
        self.assertEqual(scaffold_rows[0]["cross_review_log_id"], "graph-source-cross-review-log-001")
        self.assertEqual(scaffold_rows[0]["cross_review_task_id"], queue_rows[0]["cross_review_task_id"])
        self.assertEqual(scaffold_rows[0]["route_files_to_open"], queue_rows[0]["route_files_to_open"])
        self.assertEqual(scaffold_rows[1]["source_id"], "src-evobc")
        self.assertEqual(scaffold_rows[1]["expected_output_path"], queue_rows[1]["expected_output_path"])
        self.assertEqual(scaffold_rows[2]["source_id"], "src-obimd")
        self.assertEqual(scaffold_rows[2]["output_scope"], "cross_source_review_log_scaffold_only")
        self.assertEqual(
            {row["graph_edge_review_status"] for row in scaffold_rows},
            {"not_collected"},
        )
        self.assertTrue(all("confirmed scholarship" not in row["caution"] for row in scaffold_rows))
        self.assertTrue(all(row["promotion_decision_status"] != "promoted" for row in scaffold_rows))

    def test_ai_agent_graph_source_cross_review_log_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "014_ai-agent-graph-source-cross-review-log-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual(rows[0]["draft_log_id"], "graph-source-cross-review-draft-001")
        self.assertEqual(rows[0]["cross_review_log_id"], "graph-source-cross-review-log-001")
        self.assertEqual(rows[0]["draft_status"], "draft_not_collected")
        self.assertEqual(rows[0]["evidence_section_status"], "not_collected")
        self.assertEqual(rows[0]["research_boundary"], "user_research_draft_not_scholarship")
        self.assertEqual(
            rows[0]["draft_log_path"],
            "doc/public/user_research/002_cross-source-review-queues/hust-obc/"
            "001_hust-obc-evidence-request-000001_cross-source-review-log.md",
        )
        self.assertEqual(
            rows[1]["draft_log_path"],
            "doc/public/user_research/002_cross-source-review-queues/evobc/"
            "002_evobc-evo-cat-00001_cross-source-review-log.md",
        )
        self.assertEqual(
            rows[2]["draft_log_path"],
            "doc/public/user_research/002_cross-source-review-queues/obimd/"
            "003_obimd-sub-cand-000001_cross-source-review-log.md",
        )
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        draft_text = (repo_root() / rows[0]["draft_log_path"]).read_text(encoding="utf-8")
        for snippet in [
            "Graph Source Cross-Review Log",
            "draft_not_collected",
            "user_research_draft_not_scholarship",
            "not_collected",
            "not_decided",
            "created_from_013_scaffold",
            "not a decipherment conclusion",
        ]:
            self.assertIn(snippet, draft_text)

    def test_ai_agent_graph_source_cross_review_log_draft_builder_links_scaffold(self) -> None:
        module = load_graph_source_cross_review_log_drafts_module()
        root = repo_root()
        scaffold_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD)
        rows = module.build_draft_manifest_rows(scaffold_rows)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["draft_log_id"], "graph-source-cross-review-draft-001")
        self.assertEqual(rows[0]["cross_review_log_id"], scaffold_rows[0]["cross_review_log_id"])
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[1]["source_id"], "src-evobc")
        self.assertEqual(rows[2]["source_id"], "src-obimd")
        self.assertEqual(rows[0]["draft_status"], "draft_not_collected")
        self.assertEqual(rows[0]["evidence_section_status"], "not_collected")
        self.assertEqual(rows[0]["research_boundary"], "user_research_draft_not_scholarship")
        self.assertEqual(
            rows[0]["draft_log_path"],
            "doc/public/user_research/002_cross-source-review-queues/hust-obc/"
            "001_hust-obc-evidence-request-000001_cross-source-review-log.md",
        )
        self.assertEqual(
            rows[0]["route_files_to_open"],
            scaffold_rows[0]["route_files_to_open"],
        )
        self.assertTrue(all("confirmed scholarship" not in row["caution"] for row in rows))
        markdown = module.build_markdown(scaffold_rows[0], rows[0]["draft_log_id"])
        self.assertIn("hust-obc-evidence-request-000001", markdown)
        self.assertIn("Route Files To Open", markdown)
        self.assertIn("Required Counter Sources", markdown)
        self.assertIn("Evidence Sections", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_cross_review_log_results_are_metadata_only(self) -> None:
        results_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "015_ai-agent-graph-source-cross-review-log-results.csv"
        )
        with results_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(by_source["src-hust-obc"]["route_file_count"], "11")
        self.assertEqual(by_source["src-hust-obc"]["missing_route_file_count"], "0")
        self.assertEqual(by_source["src-hust-obc"]["registered_counter_source_count"], "6")
        self.assertEqual(by_source["src-hust-obc"]["primary_graph_edge_count"], "3562")
        self.assertEqual(by_source["src-hust-obc"]["staging_row_count"], "3")
        self.assertIn("hust-obc-bucket-001-row-001", by_source["src-hust-obc"]["staging_record_refs"])
        self.assertEqual(by_source["src-evobc"]["route_file_count"], "8")
        self.assertEqual(by_source["src-evobc"]["primary_graph_edge_count"], "51679")
        self.assertEqual(by_source["src-evobc"]["staging_row_count"], "3")
        self.assertIn("evobc-code-004", by_source["src-evobc"]["staging_record_refs"])
        self.assertEqual(by_source["src-obimd"]["route_file_count"], "9")
        self.assertEqual(by_source["src-obimd"]["primary_graph_edge_count"], "44433")
        self.assertEqual(by_source["src-obimd"]["staging_row_count"], "52")
        self.assertIn("obimd-glyph-link-000050", by_source["src-obimd"]["staging_record_refs"])
        self.assertEqual({row["route_file_review_status"] for row in rows}, {"reviewed_route_files_exist"})
        self.assertEqual(
            {row["counter_source_lookup_status"] for row in rows},
            {"reviewed_all_required_counter_sources_registered"},
        )
        self.assertEqual({row["promotion_decision_status"] for row in rows}, {"not_promoted"})
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"cross_source_review_log_result_metadata_only_not_scholarship"},
        )
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_cross_review_log_result_builder_counts_routes(self) -> None:
        module = load_graph_source_cross_review_log_results_module()
        root = repo_root()
        rows = module.build_result_rows(
            module.read_csv_rows(root / module.GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST),
            module.read_csv_rows(root / module.SOURCE_INDEX),
            module.read_csv_rows(root / module.DOWNLOADED_METADATA_PROFILE),
            module.read_csv_rows(root / module.SOURCE_DOWNLOAD_LOG),
            module.read_csv_rows(root / module.SOURCE_PACKAGE_FILE_MANIFEST),
            module.read_csv_rows(root / module.HUST_OBC_EVIDENCE_REQUEST_QUEUE),
            module.read_csv_rows(root / module.HUST_OBC_PROMOTION_QUEUE),
            module.read_csv_rows(root / module.HUST_OBC_BUCKET_MANIFEST),
            module.read_csv_rows(root / module.EVOBC_CATEGORY_STAGING),
            module.read_csv_rows(root / module.EVOBC_CODEBOOK_STAGING),
            module.read_csv_rows(root / module.OBIMD_MAIN_CHARACTER_STAGING),
            module.read_csv_rows(root / module.OBIMD_SUBCHARACTER_MAIN_STAGING),
            module.read_csv_rows(root / module.OBIMD_SUBCHARACTER_GLYPH_STAGING),
            root,
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["cross_review_result_id"], "graph-source-cross-review-result-001")
        self.assertEqual(rows[0]["draft_log_id"], "graph-source-cross-review-draft-001")
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[0]["graph_edge_route_line_count"], "99674")
        self.assertEqual(rows[1]["source_id"], "src-evobc")
        self.assertIn("evobc-evo-cat-00001", rows[1]["staging_record_refs"])
        self.assertEqual(rows[2]["source_id"], "src-obimd")
        self.assertIn("obimd-main-cand-000001", rows[2]["staging_record_refs"])
        self.assertTrue(all(row["draft_log_status"] == "draft_log_exists" for row in rows))
        self.assertTrue(all(row["promotion_decision_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("confirmed scholarship" not in row["caution"] for row in rows))

    def test_ai_agent_graph_source_evidence_collection_task_queue_is_not_collected(self) -> None:
        task_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "016_ai-agent-graph-source-evidence-collection-task-queue.csv"
        )
        with task_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 27)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-001")
        self.assertEqual(rows[-1]["evidence_collection_task_id"], "graph-source-evidence-task-027")
        self.assertEqual(
            {row["source_id"] for row in rows},
            {"src-hust-obc", "src-evobc", "src-obimd"},
        )
        self.assertEqual(
            [row["target_evidence_section"] for row in rows[:9]],
            [
                "source_register",
                "download_log",
                "package_manifest",
                "metadata_profile",
                "graph_edges",
                "staging_row",
                "counter_source_lookup",
                "rights_risk_review",
                "review_log",
            ],
        )
        self.assertEqual(
            {row["target_evidence_section"] for row in rows},
            {
                "source_register",
                "download_log",
                "package_manifest",
                "metadata_profile",
                "graph_edges",
                "staging_row",
                "counter_source_lookup",
                "rights_risk_review",
                "review_log",
            },
        )
        self.assertEqual(rows[4]["route_file_count"], "3")
        self.assertEqual(rows[5]["route_file_count"], "3")
        self.assertEqual(rows[13]["route_file_count"], "1")
        self.assertEqual(rows[14]["route_file_count"], "2")
        self.assertEqual(rows[22]["route_file_count"], "1")
        self.assertEqual(rows[23]["route_file_count"], "3")
        self.assertTrue(all(row["prerequisite_status"] == "ready_from_015_metadata_review" for row in rows))
        self.assertTrue(all(row["task_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_evidence_collection_task_queue_builder_splits_sections(self) -> None:
        module = load_graph_source_evidence_collection_task_queue_module()
        root = repo_root()
        rows = module.build_task_rows(
            module.read_csv_rows(root / module.GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST),
            module.read_csv_rows(root / module.GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS),
        )
        self.assertEqual(len(rows), 27)
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[0]["target_evidence_section"], "source_register")
        self.assertEqual(rows[0]["route_file_count"], "1")
        self.assertEqual(rows[4]["target_evidence_section"], "graph_edges")
        self.assertEqual(rows[4]["route_file_count"], "3")
        self.assertEqual(rows[9]["source_id"], "src-evobc")
        self.assertEqual(rows[14]["target_evidence_section"], "staging_row")
        self.assertEqual(rows[14]["route_file_count"], "2")
        self.assertEqual(rows[18]["source_id"], "src-obimd")
        self.assertEqual(rows[23]["target_evidence_section"], "staging_row")
        self.assertEqual(rows[23]["route_file_count"], "3")
        self.assertTrue(all(row["expected_output_path"].startswith("doc/public/user_research/") for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all("confirmed scholarship" not in row["caution"] for row in rows))

    def test_ai_agent_graph_source_evidence_collection_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_note_draft_id"] for row in rows],
            [
                "graph-source-evidence-note-draft-001",
                "graph-source-evidence-note-draft-002",
                "graph-source-evidence-note-draft-003",
            ],
        )
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-001",
                "graph-source-evidence-task-010",
                "graph-source-evidence-task-019",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"source_register"})
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("Route Files To Open", text)
            self.assertIn("created_from_016_task_queue", text)
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_evidence_collection_note_draft_builder_links_tasks(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_note_draft_id"], "graph-source-evidence-note-draft-001")
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-001")
        self.assertEqual(rows[0]["note_draft_path"], task_rows[0]["expected_output_path"])
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-010")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-019")
        self.assertTrue(all(row["target_evidence_section"] == "source_register" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        markdown = module.build_markdown(task_rows[0], rows[0]["evidence_collection_note_draft_id"])
        self.assertIn("Evidence Collection Note", markdown)
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)
        self.assertIn("不是释读结论", markdown)

    def test_ai_agent_graph_source_download_log_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "018_ai-agent-graph-source-download-log-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-002",
                "graph-source-evidence-task-011",
                "graph-source-evidence-task-020",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"download_log"})
        self.assertEqual(
            {row["route_files_to_open"] for row in rows},
            {"project_registry/006_large-source-register/002_source-download-log.csv"},
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a rights decision" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("download_log", text)
            self.assertIn("Download Log", text)
            self.assertIn("下载日志", text)
            self.assertIn("project_registry/006_large-source-register/002_source-download-log.csv", text)
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_download_log_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="download_log")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-002")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-011")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-020")
        self.assertTrue(all(row["target_evidence_section"] == "download_log" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-002"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Download Log", markdown)
        self.assertIn("下载日志", markdown)
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_package_manifest_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "019_ai-agent-graph-source-package-manifest-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-003",
                "graph-source-evidence-task-012",
                "graph-source-evidence-task-021",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"package_manifest"})
        self.assertEqual(
            {row["route_files_to_open"] for row in rows},
            {"corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"},
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a promotion decision" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("package_manifest", text)
            self.assertIn("Package Manifest", text)
            self.assertIn("包 manifest", text)
            self.assertIn(
                "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv",
                text,
            )
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_package_manifest_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="package_manifest")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-003")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-012")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-021")
        self.assertTrue(all(row["target_evidence_section"] == "package_manifest" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-003"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Package Manifest", markdown)
        self.assertIn("包 manifest", markdown)
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_metadata_profile_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "020_ai-agent-graph-source-metadata-profile-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-004",
                "graph-source-evidence-task-013",
                "graph-source-evidence-task-022",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"metadata_profile"})
        self.assertEqual(
            {row["route_files_to_open"] for row in rows},
            {"corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"},
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a rights decision" in row["caution"] for row in rows))
        self.assertTrue(all("not a promotion decision" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("metadata_profile", text)
            self.assertIn("Metadata Profile", text)
            self.assertIn("metadata 画像", text)
            self.assertIn(
                "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv",
                text,
            )
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_metadata_profile_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="metadata_profile")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-004")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-013")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-022")
        self.assertTrue(all(row["target_evidence_section"] == "metadata_profile" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-004"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Metadata Profile", markdown)
        self.assertIn("metadata 画像", markdown)
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_graph_edges_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "021_ai-agent-graph-source-graph-edges-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-005",
                "graph-source-evidence-task-014",
                "graph-source-evidence-task-023",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"graph_edges"})
        self.assertIn(
            "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl",
            rows[0]["route_files_to_open"],
        )
        self.assertIn(
            "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl",
            rows[1]["route_files_to_open"],
        )
        self.assertIn(
            "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
            rows[2]["route_files_to_open"],
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a component or evolution-chain assignment" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("graph_edges", text)
            self.assertIn("Graph Edges", text)
            self.assertIn("图谱边", text)
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)
            for route_file in row["route_files_to_open"].split(";"):
                self.assertIn(route_file, text)

    def test_ai_agent_graph_source_graph_edges_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="graph_edges")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-005")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-014")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-023")
        self.assertTrue(all(row["target_evidence_section"] == "graph_edges" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-005"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Graph Edges", markdown)
        self.assertIn("图谱边", markdown)
        self.assertIn("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl", markdown)
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_staging_row_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "022_ai-agent-graph-source-staging-row-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-006",
                "graph-source-evidence-task-015",
                "graph-source-evidence-task-024",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"staging_row"})
        self.assertIn(
            "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv",
            rows[0]["route_files_to_open"],
        )
        self.assertIn(
            "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/001_evobc-evolution-category-staging.csv",
            rows[1]["route_files_to_open"],
        )
        self.assertIn(
            "corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv",
            rows[2]["route_files_to_open"],
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a promotion decision" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("staging_row", text)
            self.assertIn("Staging Row", text)
            self.assertIn("staging 行", text)
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)
            for route_file in row["route_files_to_open"].split(";"):
                self.assertIn(route_file, text)

    def test_ai_agent_graph_source_staging_row_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="staging_row")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-006")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-015")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-024")
        self.assertTrue(all(row["target_evidence_section"] == "staging_row" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-006"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Staging Row", markdown)
        self.assertIn("staging 行", markdown)
        self.assertIn(
            "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv",
            markdown,
        )
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_counter_source_lookup_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "023_ai-agent-graph-source-counter-source-lookup-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-007",
                "graph-source-evidence-task-016",
                "graph-source-evidence-task-025",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"counter_source_lookup"})
        self.assertEqual(
            {row["route_files_to_open"] for row in rows},
            {"corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"},
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a rights decision" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("counter_source_lookup", text)
            self.assertIn("Counter-Source Lookup", text)
            self.assertIn("反查来源", text)
            self.assertIn(
                "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv",
                text,
            )
            self.assertIn("not_collected", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_counter_source_lookup_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="counter_source_lookup")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-007")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-016")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-025")
        self.assertTrue(all(row["target_evidence_section"] == "counter_source_lookup" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-007"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Counter-Source Lookup", markdown)
        self.assertIn("反查来源", markdown)
        self.assertIn(
            "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv",
            markdown,
        )
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_rights_risk_review_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "024_ai-agent-graph-source-rights-risk-review-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-008",
                "graph-source-evidence-task-017",
                "graph-source-evidence-task-026",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"rights_risk_review"})
        expected_route_files = (
            "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv;"
            "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv;"
            "project_registry/006_large-source-register/002_source-download-log.csv;"
            "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
        )
        self.assertEqual({row["route_files_to_open"] for row in rows}, {expected_route_files})
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a rights decision" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("rights_risk_review", text)
            self.assertIn("Rights And Risk Review", text)
            self.assertIn("权利与风险复核", text)
            for route_file in expected_route_files.split(";"):
                self.assertIn(route_file, text)
            self.assertIn("not_collected", text)
            self.assertIn("not a rights decision", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是权利决定", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_rights_risk_review_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="rights_risk_review")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-008")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-017")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-026")
        self.assertTrue(all(row["target_evidence_section"] == "rights_risk_review" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-008"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Rights And Risk Review", markdown)
        self.assertIn("权利与风险复核", markdown)
        self.assertIn("collect_rights_risk_and_size_boundary_notes", markdown)
        self.assertIn(
            "project_registry/006_large-source-register/002_source-download-log.csv",
            markdown,
        )
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a rights decision", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_review_log_note_drafts_are_empty(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "025_ai-agent-graph-source-review-log-note-draft-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["evidence_collection_task_id"] for row in rows],
            [
                "graph-source-evidence-task-009",
                "graph-source-evidence-task-018",
                "graph-source-evidence-task-027",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"review_log"})
        expected_route_files_by_task = {
            "graph-source-evidence-task-009": (
                "corpus/009_statistics-and-derived-features/015_ai-agent-graph-source-cross-review-log-results.csv;"
                "doc/public/user_research/002_cross-source-review-queues/hust-obc/"
                "001_hust-obc-evidence-request-000001_cross-source-review-log.md"
            ),
            "graph-source-evidence-task-018": (
                "corpus/009_statistics-and-derived-features/015_ai-agent-graph-source-cross-review-log-results.csv;"
                "doc/public/user_research/002_cross-source-review-queues/evobc/"
                "002_evobc-evo-cat-00001_cross-source-review-log.md"
            ),
            "graph-source-evidence-task-027": (
                "corpus/009_statistics-and-derived-features/015_ai-agent-graph-source-cross-review-log-results.csv;"
                "doc/public/user_research/002_cross-source-review-queues/obimd/"
                "003_obimd-sub-cand-000001_cross-source-review-log.md"
            ),
        }
        self.assertEqual(
            [row["route_files_to_open"] for row in rows],
            [expected_route_files_by_task[row["evidence_collection_task_id"]] for row in rows],
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all("not a rights decision" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))
        for row in rows:
            note_path = repo_root() / row["note_draft_path"]
            text = note_path.read_text(encoding="utf-8")
            self.assertIn("Evidence Collection Note", text)
            self.assertIn("review_log", text)
            self.assertIn("Review Log", text)
            self.assertIn("复核日志", text)
            for route_file in expected_route_files_by_task[row["evidence_collection_task_id"]].split(";"):
                self.assertIn(route_file, text)
            self.assertIn("not_collected", text)
            self.assertIn("not a rights decision", text)
            self.assertIn("not a decipherment conclusion", text)
            self.assertIn("不是权利决定", text)
            self.assertIn("不是释读结论", text)

    def test_ai_agent_graph_source_review_log_note_draft_builder_selects_section(self) -> None:
        module = load_graph_source_evidence_collection_note_drafts_module()
        root = repo_root()
        task_rows = module.read_csv_rows(root / module.GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE)
        rows = module.build_note_manifest_rows(task_rows, target_section="review_log")
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-009")
        self.assertEqual(rows[1]["evidence_collection_task_id"], "graph-source-evidence-task-018")
        self.assertEqual(rows[2]["evidence_collection_task_id"], "graph-source-evidence-task-027")
        self.assertTrue(all(row["target_evidence_section"] == "review_log" for row in rows))
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in rows))
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in rows))
        task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
        markdown = module.build_markdown(
            task_rows_by_id["graph-source-evidence-task-009"],
            rows[0]["evidence_collection_note_draft_id"],
        )
        self.assertIn("Review Log", markdown)
        self.assertIn("复核日志", markdown)
        self.assertIn("collect_human_or_agent_review_log_notes_under_user_research", markdown)
        self.assertIn(
            "doc/public/user_research/002_cross-source-review-queues/hust-obc/"
            "001_hust-obc-evidence-request-000001_cross-source-review-log.md",
            markdown,
        )
        self.assertIn("created_from_016_task_queue", markdown)
        self.assertIn("not_collected", markdown)
        self.assertIn("not a rights decision", markdown)
        self.assertIn("not a decipherment conclusion", markdown)

    def test_ai_agent_graph_source_evidence_collection_route_pack_preserves_routes(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "026_ai-agent-graph-source-evidence-collection-route-pack.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        expected_sources = ["src-hust-obc", "src-evobc", "src-obimd"]
        expected_sections = [
            "source_register",
            "download_log",
            "package_manifest",
            "metadata_profile",
            "graph_edges",
            "staging_row",
            "counter_source_lookup",
            "rights_risk_review",
            "review_log",
        ]
        expected_manifests = [
            "corpus/009_statistics-and-derived-features/"
            "017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "018_ai-agent-graph-source-download-log-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "019_ai-agent-graph-source-package-manifest-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "020_ai-agent-graph-source-metadata-profile-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "021_ai-agent-graph-source-graph-edges-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "022_ai-agent-graph-source-staging-row-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "023_ai-agent-graph-source-counter-source-lookup-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "024_ai-agent-graph-source-rights-risk-review-note-draft-manifest.csv",
            "corpus/009_statistics-and-derived-features/"
            "025_ai-agent-graph-source-review-log-note-draft-manifest.csv",
        ]

        self.assertEqual(data["context_pack_id"], "ai-context-graph-source-evidence-collection-001")
        self.assertEqual(data["status"], "draft_route_pack_not_collected")
        self.assertEqual(data["updated_at"], "2026-06-10")
        self.assertEqual(data["generated_from"], expected_manifests)
        self.assertEqual(
            data["coverage"],
            {
                "counter_source_reference_count": 144,
                "evidence_collection_status_counts": {"not_collected": 27},
                "manifest_count": 9,
                "note_draft_count": 27,
                "note_status_counts": {"draft_not_collected": 27},
                "promotion_status_counts": {"not_promoted": 27},
                "research_boundary_counts": {
                    "evidence_collection_note_draft_not_scholarship": 27
                },
                "route_file_reference_count": 46,
                "section_counts": {section: 3 for section in expected_sections},
                "source_count": 3,
                "source_counts": {"src-evobc": 9, "src-hust-obc": 9, "src-obimd": 9},
                "target_evidence_section_count": 9,
            },
        )
        self.assertEqual([row["source_id"] for row in data["source_routes"]], expected_sources)
        self.assertTrue(all(row["note_draft_count"] == 9 for row in data["source_routes"]))
        self.assertTrue(
            all(row["target_evidence_sections"] == expected_sections for row in data["source_routes"])
        )
        self.assertEqual(
            [row["target_evidence_section"] for row in data["section_routes"]],
            expected_sections,
        )
        self.assertTrue(all(row["source_ids"] == expected_sources for row in data["section_routes"]))
        self.assertEqual(len(data["note_routes"]), 27)
        self.assertEqual(
            data["note_routes"][0]["evidence_collection_task_id"],
            "graph-source-evidence-task-001",
        )
        self.assertEqual(
            data["note_routes"][-1]["evidence_collection_task_id"],
            "graph-source-evidence-task-027",
        )
        self.assertTrue(
            all(
                row["note_draft_path"].startswith("doc/public/user_research/")
                and not row["note_draft_path"].startswith("research/")
                for row in data["note_routes"]
            )
        )
        self.assertTrue(
            all(row["evidence_collection_status"] == "not_collected" for row in data["note_routes"])
        )
        self.assertTrue(all(row["promotion_status"] == "not_promoted" for row in data["note_routes"]))
        self.assertTrue(
            all(
                row["research_boundary"] == "evidence_collection_note_draft_not_scholarship"
                for row in data["note_routes"]
            )
        )
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("not-collected", rules)
        self.assertIn("Do not treat this pack as collected evidence", rules)
        self.assertIn("ignored temporary directories", rules)
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("未收集", rules_zh)
        self.assertIn("不得把本包当作已收集证据", rules_zh)
        self.assertIn("已忽略临时目录", rules_zh)

    def test_ai_agent_graph_source_evidence_collection_route_pack_builder_collects_manifests(self) -> None:
        module = load_graph_source_evidence_collection_route_pack_module()
        root = repo_root()
        data = module.build_route_pack(
            [
                (manifest_path, module.read_csv_rows(root / manifest_path))
                for manifest_path in module.MANIFEST_PATHS
            ]
        )
        self.assertEqual(data["coverage"]["manifest_count"], 9)
        self.assertEqual(data["coverage"]["note_draft_count"], 27)
        self.assertEqual(data["coverage"]["route_file_reference_count"], 46)
        self.assertEqual(data["coverage"]["counter_source_reference_count"], 144)
        self.assertEqual(
            {row["source_id"]: row["note_draft_count"] for row in data["source_routes"]},
            {"src-hust-obc": 9, "src-evobc": 9, "src-obimd": 9},
        )
        self.assertEqual(
            {row["target_evidence_section"]: row["note_draft_count"] for row in data["section_routes"]},
            {
                "source_register": 3,
                "download_log": 3,
                "package_manifest": 3,
                "metadata_profile": 3,
                "graph_edges": 3,
                "staging_row": 3,
                "counter_source_lookup": 3,
                "rights_risk_review": 3,
                "review_log": 3,
            },
        )
        self.assertEqual(
            data["note_routes"][0]["evidence_collection_task_id"],
            "graph-source-evidence-task-001",
        )
        self.assertEqual(
            data["note_routes"][-1]["evidence_collection_task_id"],
            "graph-source-evidence-task-027",
        )
        self.assertTrue(all(row["note_status"] == "draft_not_collected" for row in data["note_routes"]))
        self.assertTrue(
            all("not a decipherment conclusion" in row["caution"] for row in data["note_routes"])
        )
        self.assertIn("or a decipherment conclusion", " ".join(data["agent_use_rules"]))

    def test_ai_agent_graph_source_evidence_collection_result_scaffold_is_empty(self) -> None:
        route_pack_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "026_ai-agent-graph-source-evidence-collection-route-pack.json"
        )
        result_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
        )
        route_pack = json.loads(route_pack_path.read_text(encoding="utf-8"))
        with result_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 27)
        self.assertEqual(len(rows), len(route_pack["note_routes"]))
        self.assertEqual(rows[0]["evidence_collection_result_id"], "graph-source-evidence-result-001")
        self.assertEqual(rows[0]["evidence_collection_task_id"], "graph-source-evidence-task-001")
        self.assertEqual(rows[-1]["evidence_collection_result_id"], "graph-source-evidence-result-027")
        self.assertEqual(rows[-1]["evidence_collection_task_id"], "graph-source-evidence-task-027")
        self.assertEqual([row["source_id"] for row in rows[:9]], ["src-hust-obc"] * 9)
        self.assertEqual([row["source_id"] for row in rows[9:18]], ["src-evobc"] * 9)
        self.assertEqual([row["source_id"] for row in rows[18:]], ["src-obimd"] * 9)
        self.assertEqual(
            [row["target_evidence_section"] for row in rows[:9]],
            [
                "source_register",
                "download_log",
                "package_manifest",
                "metadata_profile",
                "graph_edges",
                "staging_row",
                "counter_source_lookup",
                "rights_risk_review",
                "review_log",
            ],
        )
        self.assertEqual(
            {row["result_status"] for row in rows},
            {"not_started"},
        )
        self.assertEqual(
            {row["evidence_collection_status"] for row in rows},
            {"not_collected"},
        )
        self.assertEqual(
            {row["source_promotion_status"] for row in rows},
            {"not_promoted"},
        )
        self.assertEqual(
            {row["decipherment_claim_status"] for row in rows},
            {"no_claim"},
        )
        self.assertEqual(
            {row["research_boundary"] for row in rows},
            {"evidence_collection_result_scaffold_not_scholarship"},
        )
        self.assertTrue(all("Do not use it as collected evidence" in row["caution"] for row in rows))
        self.assertTrue(all("decipherment conclusion" in row["caution"] for row in rows))
        self.assertEqual(
            rows[0]["route_files_to_open"],
            ";".join(route_pack["note_routes"][0]["route_files_to_open"]),
        )
        self.assertEqual(
            rows[0]["counter_source_ids_to_check"],
            ";".join(route_pack["note_routes"][0]["counter_source_ids_to_check"]),
        )

    def test_ai_agent_graph_source_evidence_collection_result_scaffold_builder_keeps_empty_sections(
        self,
    ) -> None:
        module = load_graph_source_evidence_collection_result_scaffold_module()
        route_pack = module.read_json(
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "026_ai-agent-graph-source-evidence-collection-route-pack.json"
        )
        rows = module.build_result_rows(route_pack)
        self.assertEqual(len(rows), 27)
        self.assertEqual(rows[0]["evidence_collection_result_id"], "graph-source-evidence-result-001")
        self.assertEqual(rows[0]["required_collection_action"], "collect_source_register_provenance_fields")
        self.assertEqual(
            rows[7]["required_collection_action"],
            "collect_rights_risk_notes_without_rights_decision",
        )
        self.assertEqual(
            rows[26]["required_collection_action"],
            "collect_review_log_notes_without_promotion_decision",
        )
        self.assertEqual(
            {row["note_draft_open_status"] for row in rows},
            {"not_opened"},
        )
        self.assertEqual(
            {row["route_files_open_status"] for row in rows},
            {"not_opened"},
        )
        self.assertEqual(
            {row["source_register_evidence_status"] for row in rows},
            {"not_collected"},
        )
        self.assertEqual(
            {row["rights_risk_review_status"] for row in rows},
            {"not_collected"},
        )
        self.assertTrue(all(row["output_scope"].endswith("_scaffold_only") for row in rows))
        self.assertTrue(all("source promotion decision" in row["caution"] for row in rows))
        self.assertTrue(all("component or evolution-chain assignment" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_evidence_collection_review_queue_routes_scaffolds(self) -> None:
        result_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
        )
        queue_path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
        )
        with result_path.open("r", encoding="utf-8-sig", newline="") as file:
            result_rows = list(csv.DictReader(file))
        with queue_path.open("r", encoding="utf-8-sig", newline="") as file:
            queue_rows = list(csv.DictReader(file))

        self.assertEqual(len(queue_rows), 27)
        self.assertEqual(len(queue_rows), len(result_rows))
        self.assertEqual(
            queue_rows[0]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-001",
        )
        self.assertEqual(queue_rows[0]["evidence_collection_result_id"], "graph-source-evidence-result-001")
        self.assertEqual(queue_rows[-1]["evidence_collection_result_id"], "graph-source-evidence-result-027")
        self.assertEqual(
            [row["target_evidence_section"] for row in queue_rows[:9]],
            [
                "source_register",
                "download_log",
                "package_manifest",
                "metadata_profile",
                "graph_edges",
                "staging_row",
                "counter_source_lookup",
                "rights_risk_review",
                "review_log",
            ],
        )
        self.assertEqual(queue_rows[0]["priority_rank"], "1")
        self.assertEqual(queue_rows[7]["priority_rank"], "5")
        self.assertEqual(queue_rows[-1]["priority_rank"], "9")
        self.assertTrue(all(row["assignment_status"] == "unassigned" for row in queue_rows))
        self.assertTrue(
            all(row["review_status"] == "needs_evidence_collection_review" for row in queue_rows)
        )
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in queue_rows))
        self.assertTrue(all(row["source_promotion_status"] == "not_promoted" for row in queue_rows))
        self.assertTrue(all(row["decipherment_claim_status"] == "no_claim" for row in queue_rows))
        self.assertTrue(
            all(row["research_boundary"] == "evidence_collection_review_queue_not_scholarship" for row in queue_rows)
        )
        self.assertTrue(
            all("keep_result_row_not_collected_until_evidence_is_source_marked" in row["required_review_checks"] for row in queue_rows)
        )
        self.assertTrue(
            all("do_not_write_ai_hypothesis_as_scholarship" in row["required_review_checks"] for row in queue_rows)
        )
        self.assertIn(queue_rows[0]["note_draft_path"], queue_rows[0]["route_files_to_open"])
        self.assertIn(queue_rows[0]["route_pack_path"], queue_rows[0]["route_files_to_open"])
        self.assertIn(queue_rows[0]["manifest_path"], queue_rows[0]["route_files_to_open"])
        self.assertTrue(all("Do not use this queue as collected evidence" in row["caution"] for row in queue_rows))
        self.assertTrue(all("decipherment conclusion" in row["caution"] for row in queue_rows))

    def test_ai_agent_graph_source_evidence_collection_review_queue_builder_preserves_boundary(
        self,
    ) -> None:
        module = load_graph_source_evidence_collection_review_queue_module()
        result_rows = module.read_csv_rows(
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
        )
        rows = module.build_review_rows(result_rows)
        self.assertEqual(len(rows), 27)
        self.assertEqual(rows[0]["evidence_collection_review_task_id"], "graph-source-evidence-review-001")
        self.assertEqual(rows[0]["priority_tags"], "section:source_register;source:src-hust-obc;provenance_first")
        self.assertIn("rights_boundary", rows[7]["priority_tags"])
        self.assertIn("cross_source_candidate_check", rows[6]["priority_tags"])
        self.assertIn("review_trace", rows[8]["priority_tags"])
        self.assertIn(
            "open_source_register_row_before_copying_provenance",
            rows[0]["required_review_checks"],
        )
        self.assertIn(
            "do_not_turn_review_queue_into_rights_decision",
            rows[7]["required_review_checks"],
        )
        self.assertIn(
            "do_not_promote_review_notes_without_source_marked_evidence",
            rows[8]["required_review_checks"],
        )
        self.assertTrue(all(row["result_scaffold_path"].endswith("027_ai-agent-graph-source-evidence-collection-result-scaffold.csv") for row in rows))
        self.assertTrue(all(row["result_update_target_path"] == row["result_scaffold_path"] for row in rows))
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["decipherment_claim_status"] == "no_claim" for row in rows))
        self.assertTrue(all("component or evolution-chain assignment" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_evidence_collection_review_route_summary_groups_routes(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "029_ai-agent-graph-source-evidence-collection-review-route-summary.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        expected_sections = [
            "source_register",
            "download_log",
            "package_manifest",
            "metadata_profile",
            "graph_edges",
            "staging_row",
            "counter_source_lookup",
            "rights_risk_review",
            "review_log",
        ]

        self.assertEqual(
            data["context_pack_id"],
            "ai-context-graph-source-evidence-collection-review-summary-001",
        )
        self.assertEqual(data["status"], "draft_review_route_summary_not_collected")
        self.assertEqual(data["updated_at"], "2026-06-10")
        self.assertEqual(
            data["research_boundary"],
            "evidence_collection_review_route_summary_not_scholarship",
        )
        self.assertEqual(
            data["generated_from"],
            [
                "corpus/009_statistics-and-derived-features/"
                "028_ai-agent-graph-source-evidence-collection-review-queue.csv",
                "corpus/009_statistics-and-derived-features/"
                "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv",
                "corpus/009_statistics-and-derived-features/"
                "026_ai-agent-graph-source-evidence-collection-route-pack.json",
            ],
        )
        self.assertEqual(data["coverage"]["review_task_count"], 27)
        self.assertEqual(
            data["coverage"]["source_counts"],
            {"src-hust-obc": 9, "src-evobc": 9, "src-obimd": 9},
        )
        self.assertEqual(
            data["coverage"]["section_counts"],
            {section: 3 for section in expected_sections},
        )
        self.assertEqual(data["coverage"]["route_file_reference_count"], 154)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 57)
        self.assertEqual(data["coverage"]["counter_source_reference_count"], 144)
        self.assertEqual(data["coverage"]["unique_counter_source_count"], 6)
        self.assertEqual(data["coverage"]["assignment_status_counts"], {"unassigned": 27})
        self.assertEqual(
            data["coverage"]["review_status_counts"],
            {"needs_evidence_collection_review": 27},
        )
        self.assertEqual(
            data["coverage"]["evidence_collection_status_counts"],
            {"not_collected": 27},
        )
        self.assertEqual(
            data["coverage"]["source_promotion_status_counts"],
            {"not_promoted": 27},
        )
        self.assertEqual(
            data["coverage"]["decipherment_claim_status_counts"],
            {"no_claim": 27},
        )
        self.assertEqual(
            data["coverage"]["priority_rank_counts"],
            {str(rank): 3 for rank in range(1, 10)},
        )
        self.assertEqual(
            [row["source_id"] for row in data["source_summaries"]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(
            all(row["target_evidence_sections"] == expected_sections for row in data["source_summaries"])
        )
        self.assertEqual(
            {row["source_id"]: row["route_file_count"] for row in data["source_summaries"]},
            {"src-hust-obc": 32, "src-evobc": 29, "src-obimd": 30},
        )
        self.assertEqual(
            [row["target_evidence_section"] for row in data["section_summaries"]],
            expected_sections,
        )
        self.assertTrue(
            all(row["source_ids"] == ["src-hust-obc", "src-evobc", "src-obimd"] for row in data["section_summaries"])
        )
        self.assertTrue(
            all(row["required_review_check_count"] == 12 for row in data["section_summaries"])
        )
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("Open the 028 queue row", rules)
        self.assertIn("Do not treat this summary as collected evidence", rules)
        self.assertIn("ignored temporary directories", rules)
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("必须打开 028 队列行", rules_zh)
        self.assertIn("不得把本摘要当作已收集证据", rules_zh)

    def test_ai_agent_graph_source_evidence_collection_review_route_summary_builder(
        self,
    ) -> None:
        module = load_graph_source_evidence_collection_review_route_summary_module()
        rows = module.read_csv_rows(
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
        )
        data = module.build_route_summary(rows)
        self.assertEqual(data["coverage"]["review_task_count"], 27)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 57)
        self.assertEqual(data["coverage"]["unique_counter_source_count"], 6)
        self.assertEqual(data["source_summaries"][0]["review_task_count"], 9)
        self.assertEqual(data["source_summaries"][0]["min_priority_rank"], 1)
        self.assertEqual(data["source_summaries"][0]["max_priority_rank"], 9)
        self.assertEqual(
            data["section_summaries"][7]["target_evidence_section"],
            "rights_risk_review",
        )
        self.assertEqual(data["section_summaries"][7]["priority_rank"], "5")
        self.assertTrue(
            all(
                row["source_ids"] == ["src-hust-obc", "src-evobc", "src-obimd"]
                for row in data["section_summaries"]
            )
        )
        self.assertIn("component or evolution-chain assignment", " ".join(data["agent_use_rules"]))
        self.assertIn("释读结论", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_graph_source_evidence_collection_assignment_plan_orders_waves(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        expected_priority_sections = [
            "source_register",
            "download_log",
            "package_manifest",
            "metadata_profile",
            "rights_risk_review",
            "graph_edges",
            "staging_row",
            "counter_source_lookup",
            "review_log",
        ]

        self.assertEqual(
            data["context_pack_id"],
            "ai-context-graph-source-evidence-collection-assignment-plan-001",
        )
        self.assertEqual(data["status"], "draft_assignment_plan_not_started")
        self.assertEqual(data["updated_at"], "2026-06-10")
        self.assertEqual(
            data["research_boundary"],
            "evidence_collection_assignment_plan_not_scholarship",
        )
        self.assertEqual(
            data["output_scope"],
            "graph_source_evidence_collection_assignment_plan_only",
        )
        self.assertEqual(
            data["upstream_context_pack_id"],
            "ai-context-graph-source-evidence-collection-review-summary-001",
        )
        self.assertEqual(
            data["generated_from"],
            [
                "corpus/009_statistics-and-derived-features/"
                "029_ai-agent-graph-source-evidence-collection-review-route-summary.json",
                "corpus/009_statistics-and-derived-features/"
                "028_ai-agent-graph-source-evidence-collection-review-queue.csv",
                "corpus/009_statistics-and-derived-features/"
                "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv",
                "corpus/009_statistics-and-derived-features/"
                "026_ai-agent-graph-source-evidence-collection-route-pack.json",
            ],
        )
        self.assertEqual(data["coverage"]["assignment_item_count"], 27)
        self.assertEqual(data["coverage"]["assignment_wave_count"], 9)
        self.assertEqual(data["coverage"]["source_workstream_count"], 3)
        self.assertEqual(data["coverage"]["route_file_reference_count"], 154)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 57)
        self.assertEqual(data["coverage"]["counter_source_reference_count"], 144)
        self.assertEqual(data["coverage"]["unique_counter_source_count"], 6)
        self.assertEqual(
            data["coverage"]["assignment_status_counts"],
            {"planned_not_assigned": 27},
        )
        self.assertEqual(
            data["coverage"]["review_status_counts"],
            {"needs_evidence_collection_review": 27},
        )
        self.assertEqual(
            data["coverage"]["evidence_collection_status_counts"],
            {"not_collected": 27},
        )
        self.assertEqual(
            data["coverage"]["source_promotion_status_counts"],
            {"not_promoted": 27},
        )
        self.assertEqual(
            data["coverage"]["decipherment_claim_status_counts"],
            {"no_claim": 27},
        )
        self.assertEqual(
            [row["target_evidence_section"] for row in data["assignment_waves"]],
            expected_priority_sections,
        )
        self.assertTrue(
            all(row["assignment_item_count"] == 3 for row in data["assignment_waves"])
        )
        self.assertTrue(
            all(row["source_ids"] == ["src-hust-obc", "src-evobc", "src-obimd"] for row in data["assignment_waves"])
        )
        self.assertEqual(
            [row["source_id"] for row in data["source_workstreams"]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(
            all(row["target_evidence_sections"] == expected_priority_sections for row in data["source_workstreams"])
        )
        self.assertEqual(
            {row["source_id"]: row["route_file_count"] for row in data["source_workstreams"]},
            {"src-hust-obc": 32, "src-evobc": 29, "src-obimd": 30},
        )
        self.assertEqual(len(data["assignment_items"]), 27)
        self.assertEqual(
            data["assignment_items"][0]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-001",
        )
        self.assertEqual(
            data["assignment_items"][1]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-010",
        )
        self.assertEqual(
            data["assignment_items"][2]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-019",
        )
        self.assertEqual(
            data["assignment_items"][-1]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-027",
        )
        self.assertTrue(
            all(row["assignment_status"] == "planned_not_assigned" for row in data["assignment_items"])
        )
        self.assertTrue(
            all(row["evidence_collection_status"] == "not_collected" for row in data["assignment_items"])
        )
        self.assertTrue(
            all(row["source_promotion_status"] == "not_promoted" for row in data["assignment_items"])
        )
        self.assertTrue(
            all(row["decipherment_claim_status"] == "no_claim" for row in data["assignment_items"])
        )
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("Open the 030 plan item", rules)
        self.assertIn("planned_not_assigned", rules)
        self.assertIn("Do not treat this plan as collected evidence", rules)
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("必须打开 030 计划项", rules_zh)
        self.assertIn("不得把本计划当作已收集证据", rules_zh)

    def test_ai_agent_graph_source_evidence_collection_assignment_plan_builder(
        self,
    ) -> None:
        module = load_graph_source_evidence_collection_assignment_plan_module()
        root = repo_root()
        data = module.build_assignment_plan(
            module.read_csv_rows(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
            ),
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "029_ai-agent-graph-source-evidence-collection-review-route-summary.json"
            ),
        )
        self.assertEqual(data["coverage"]["assignment_item_count"], 27)
        self.assertEqual(data["coverage"]["assignment_wave_count"], 9)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 57)
        self.assertEqual(
            data["assignment_waves"][4]["target_evidence_section"],
            "rights_risk_review",
        )
        self.assertEqual(data["assignment_waves"][4]["priority_rank"], "5")
        self.assertEqual(
            data["assignment_items"][4]["target_evidence_section"],
            "download_log",
        )
        self.assertEqual(
            data["assignment_items"][4]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-011",
        )
        self.assertTrue(
            all(row["assignment_status"] == "planned_not_assigned" for row in data["assignment_items"])
        )
        self.assertIn("rights decision", " ".join(data["agent_use_rules"]))
        self.assertIn("释读结论", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_graph_source_evidence_collection_wave_handoff_scaffold(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "031_ai-agent-graph-source-evidence-collection-wave-handoff-scaffold.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            data["context_pack_id"],
            "ai-context-graph-source-evidence-collection-wave-handoff-001",
        )
        self.assertEqual(data["status"], "draft_wave_handoff_scaffold_not_started")
        self.assertEqual(data["updated_at"], "2026-06-10")
        self.assertEqual(
            data["research_boundary"],
            "evidence_collection_wave_handoff_scaffold_not_scholarship",
        )
        self.assertEqual(
            data["output_scope"],
            "graph_source_evidence_collection_wave_handoff_scaffold_only",
        )
        self.assertEqual(
            data["generated_from"],
            [
                "corpus/009_statistics-and-derived-features/"
                "030_ai-agent-graph-source-evidence-collection-assignment-plan.json",
                "corpus/009_statistics-and-derived-features/"
                "029_ai-agent-graph-source-evidence-collection-review-route-summary.json",
                "corpus/009_statistics-and-derived-features/"
                "028_ai-agent-graph-source-evidence-collection-review-queue.csv",
                "corpus/009_statistics-and-derived-features/"
                "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv",
                "corpus/009_statistics-and-derived-features/"
                "026_ai-agent-graph-source-evidence-collection-route-pack.json",
            ],
        )
        self.assertEqual(
            data["handoff_scope"]["assignment_wave_id"],
            "graph-source-evidence-assignment-wave-001",
        )
        self.assertEqual(data["handoff_scope"]["target_evidence_section"], "source_register")
        self.assertEqual(
            data["handoff_scope"]["source_ids"],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual(data["coverage"]["handoff_item_count"], 3)
        self.assertEqual(data["coverage"]["assignment_wave_count"], 1)
        self.assertEqual(data["coverage"]["route_file_reference_count"], 15)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 7)
        self.assertEqual(data["coverage"]["counter_source_reference_count"], 16)
        self.assertEqual(data["coverage"]["unique_counter_source_count"], 6)
        self.assertEqual(data["coverage"]["required_review_check_reference_count"], 12)
        self.assertEqual(data["coverage"]["unique_required_review_check_count"], 4)
        self.assertEqual(
            data["coverage"]["handoff_status_counts"],
            {"ready_for_source_register_evidence_collection_not_started": 3},
        )
        self.assertEqual(
            data["coverage"]["rights_decision_status_counts"],
            {"not_decided": 3},
        )
        self.assertEqual(
            data["coverage"]["source_register_evidence_status_counts"],
            {"not_collected": 3},
        )
        self.assertEqual(
            [row["source_id"] for row in data["handoff_items"]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual(
            [row["evidence_collection_review_task_id"] for row in data["handoff_items"]],
            [
                "graph-source-evidence-review-001",
                "graph-source-evidence-review-010",
                "graph-source-evidence-review-019",
            ],
        )
        self.assertTrue(
            all(row["target_evidence_section"] == "source_register" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["evidence_collection_status"] == "not_collected" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["rights_decision_status"] == "not_decided" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["decipherment_claim_status"] == "no_claim" for row in data["handoff_items"])
        )
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("Open the 031 handoff row", rules)
        self.assertIn("Do not treat this scaffold as collected evidence", rules)
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("必须打开 031 交接行", rules_zh)
        self.assertIn("不得把本脚手架当作已收集证据", rules_zh)

    def test_ai_agent_graph_source_evidence_collection_wave_handoff_builder(
        self,
    ) -> None:
        module = load_graph_source_evidence_collection_wave_handoff_scaffold_module()
        root = repo_root()
        data = module.build_wave_handoff_scaffold(
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
            )
        )
        self.assertEqual(data["coverage"]["handoff_item_count"], 3)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 7)
        self.assertEqual(data["handoff_scope"]["target_evidence_section"], "source_register")
        self.assertEqual(
            data["handoff_items"][0]["assignment_plan_item_id"],
            "graph-source-evidence-assignment-001",
        )
        self.assertEqual(
            data["handoff_items"][1]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-010",
        )
        self.assertEqual(
            data["handoff_items"][2]["note_draft_path"],
            "doc/public/user_research/003_evidence-collection-tasks/obimd/"
            "graph-source-evidence-task-019_source-register_collection-note.md",
        )
        self.assertTrue(
            all(row["source_register_evidence_status"] == "not_collected" for row in data["handoff_items"])
        )
        self.assertIn("rights decision", " ".join(data["agent_use_rules"]))
        self.assertIn("释读结论", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_graph_source_download_log_wave_handoff_scaffold(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "034_ai-agent-graph-source-download-log-wave-handoff-scaffold.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            data["context_pack_id"],
            "ai-context-graph-source-download-log-wave-handoff-001",
        )
        self.assertEqual(data["status"], "draft_download_log_wave_handoff_scaffold_not_started")
        self.assertEqual(data["updated_at"], "2026-06-10")
        self.assertEqual(
            data["research_boundary"],
            "evidence_collection_download_log_wave_handoff_scaffold_not_scholarship",
        )
        self.assertEqual(
            data["output_scope"],
            "graph_source_evidence_collection_download_log_wave_handoff_scaffold_only",
        )
        self.assertEqual(
            data["handoff_scope"]["assignment_wave_id"],
            "graph-source-evidence-assignment-wave-002",
        )
        self.assertEqual(data["handoff_scope"]["target_evidence_section"], "download_log")
        self.assertEqual(
            data["handoff_scope"]["assignment_plan_item_ids"],
            [
                "graph-source-evidence-assignment-004",
                "graph-source-evidence-assignment-005",
                "graph-source-evidence-assignment-006",
            ],
        )
        self.assertEqual(
            data["handoff_scope"]["review_task_ids"],
            [
                "graph-source-evidence-review-002",
                "graph-source-evidence-review-011",
                "graph-source-evidence-review-020",
            ],
        )
        self.assertEqual(data["coverage"]["handoff_item_count"], 3)
        self.assertEqual(data["coverage"]["route_file_reference_count"], 15)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 7)
        self.assertEqual(data["coverage"]["counter_source_reference_count"], 16)
        self.assertEqual(data["coverage"]["required_review_check_reference_count"], 12)
        self.assertEqual(
            data["coverage"]["handoff_status_counts"],
            {"ready_for_download_log_evidence_collection_not_started": 3},
        )
        self.assertEqual(
            data["coverage"]["download_log_evidence_status_counts"],
            {"not_collected": 3},
        )
        self.assertEqual(
            data["coverage"]["checksum_review_status_counts"],
            {"not_started": 3},
        )
        self.assertEqual(
            data["coverage"]["size_review_status_counts"],
            {"not_started": 3},
        )
        self.assertEqual(
            data["coverage"]["access_review_status_counts"],
            {"not_started": 3},
        )
        self.assertIn(
            "project_registry/006_large-source-register/002_source-download-log.csv",
            data["route_files_to_open"],
        )
        self.assertEqual(
            [row["source_id"] for row in data["handoff_items"]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual(
            [row["handoff_item_id"] for row in data["handoff_items"]],
            [
                "graph-source-evidence-download-log-handoff-004",
                "graph-source-evidence-download-log-handoff-005",
                "graph-source-evidence-download-log-handoff-006",
            ],
        )
        self.assertTrue(
            all(row["target_evidence_section"] == "download_log" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["download_log_evidence_status"] == "not_collected" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["checksum_review_status"] == "not_started" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["size_review_status"] == "not_started" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["access_review_status"] == "not_started" for row in data["handoff_items"])
        )
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("Open the 034 handoff row", rules)
        self.assertIn("checksum review", rules)
        self.assertIn("ignored temporary directories", rules)
        rules_zh = " ".join(data["agent_use_rules_zh"])
        self.assertIn("必须打开 034 交接行", rules_zh)
        self.assertIn("checksum 复核", rules_zh)
        self.assertIn("已忽略临时目录", rules_zh)

    def test_ai_agent_graph_source_download_log_wave_handoff_builder(
        self,
    ) -> None:
        module = load_graph_source_download_log_wave_handoff_scaffold_module()
        root = repo_root()
        data = module.build_download_log_wave_handoff_scaffold(
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
            )
        )
        self.assertEqual(data["coverage"]["handoff_item_count"], 3)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 7)
        self.assertEqual(data["handoff_scope"]["target_evidence_section"], "download_log")
        self.assertEqual(
            data["handoff_items"][0]["assignment_plan_item_id"],
            "graph-source-evidence-assignment-004",
        )
        self.assertEqual(
            data["handoff_items"][1]["evidence_collection_review_task_id"],
            "graph-source-evidence-review-011",
        )
        self.assertEqual(
            data["handoff_items"][2]["note_draft_path"],
            "doc/public/user_research/003_evidence-collection-tasks/obimd/"
            "graph-source-evidence-task-020_download-log_collection-note.md",
        )
        self.assertTrue(
            all(row["download_log_evidence_status"] == "not_collected" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["checksum_review_status"] == "not_started" for row in data["handoff_items"])
        )
        self.assertIn("checksum review", " ".join(data["agent_use_rules"]))
        self.assertIn("释读结论", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_graph_source_package_manifest_wave_handoff_scaffold(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "037_ai-agent-graph-source-package-manifest-wave-handoff-scaffold.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            data["context_pack_id"],
            "ai-context-graph-source-package-manifest-wave-handoff-001",
        )
        self.assertEqual(data["status"], "draft_package_manifest_wave_handoff_scaffold_not_started")
        self.assertEqual(
            data["research_boundary"],
            "evidence_collection_package_manifest_wave_handoff_scaffold_not_scholarship",
        )
        self.assertEqual(
            data["output_scope"],
            "graph_source_evidence_collection_package_manifest_wave_handoff_scaffold_only",
        )
        self.assertEqual(
            data["handoff_scope"]["assignment_wave_id"],
            "graph-source-evidence-assignment-wave-003",
        )
        self.assertEqual(data["handoff_scope"]["target_evidence_section"], "package_manifest")
        self.assertEqual(
            data["handoff_scope"]["assignment_plan_item_ids"],
            [
                "graph-source-evidence-assignment-007",
                "graph-source-evidence-assignment-008",
                "graph-source-evidence-assignment-009",
            ],
        )
        self.assertEqual(
            data["handoff_scope"]["review_task_ids"],
            [
                "graph-source-evidence-review-003",
                "graph-source-evidence-review-012",
                "graph-source-evidence-review-021",
            ],
        )
        self.assertEqual(data["coverage"]["handoff_item_count"], 3)
        self.assertEqual(data["coverage"]["unique_route_file_count"], 7)
        self.assertEqual(data["coverage"]["package_manifest_evidence_status_counts"], {"not_collected": 3})
        self.assertEqual(data["coverage"]["file_size_review_status_counts"], {"not_started": 3})
        self.assertEqual(data["coverage"]["checksum_review_status_counts"], {"not_started": 3})
        self.assertEqual(data["coverage"]["storage_boundary_review_status_counts"], {"not_started": 3})
        self.assertIn(
            "corpus/006_research-sources-and-bibliography/000_source-registers/"
            "009_source-package-file-manifest.csv",
            data["route_files_to_open"],
        )
        self.assertEqual(
            data["required_review_checks"],
            [
                "do_not_write_ai_hypothesis_as_scholarship",
                "keep_raw_package_storage_boundary_explicit",
                "keep_result_row_not_collected_until_evidence_is_source_marked",
                "open_package_manifest_before_recording_file_size_or_checksum",
            ],
        )
        self.assertEqual(
            [row["handoff_item_id"] for row in data["handoff_items"]],
            [
                "graph-source-evidence-package-manifest-handoff-007",
                "graph-source-evidence-package-manifest-handoff-008",
                "graph-source-evidence-package-manifest-handoff-009",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in data["handoff_items"]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(
            all(row["target_evidence_section"] == "package_manifest" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["package_manifest_evidence_status"] == "not_collected" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["file_size_review_status"] == "not_started" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["storage_boundary_review_status"] == "not_started" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["rights_decision_status"] == "not_decided" for row in data["handoff_items"])
        )
        rules = " ".join(data["agent_use_rules"])
        self.assertIn("file-size review", rules)
        self.assertIn("40 MiB", rules)
        self.assertIn("释读结论", " ".join(data["agent_use_rules_zh"]))

    def test_ai_agent_graph_source_package_manifest_wave_handoff_builder(
        self,
    ) -> None:
        module = load_graph_source_package_manifest_wave_handoff_scaffold_module()
        root = repo_root()
        data = module.build_package_manifest_wave_handoff_scaffold(
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
            )
        )

        self.assertEqual(data["handoff_scope"]["assignment_wave_id"], "graph-source-evidence-assignment-wave-003")
        self.assertEqual(data["handoff_scope"]["target_evidence_section"], "package_manifest")
        self.assertEqual(data["coverage"]["handoff_item_count"], 3)
        self.assertEqual(
            [row["evidence_collection_review_task_id"] for row in data["handoff_items"]],
            [
                "graph-source-evidence-review-003",
                "graph-source-evidence-review-012",
                "graph-source-evidence-review-021",
            ],
        )
        self.assertEqual(data["handoff_items"][0]["source_id"], "src-hust-obc")
        self.assertEqual(data["handoff_items"][1]["source_id"], "src-evobc")
        self.assertEqual(data["handoff_items"][2]["source_id"], "src-obimd")
        self.assertTrue(
            all(row["package_manifest_evidence_status"] == "not_collected" for row in data["handoff_items"])
        )
        self.assertTrue(
            all(row["checksum_review_status"] == "not_started" for row in data["handoff_items"])
        )
        self.assertIn("037_ai-agent", module.DEFAULT_OUTPUT.as_posix())
        self.assertIn("source package file manifest", " ".join(data["agent_use_rules"]))

    def test_ai_agent_graph_source_package_manifest_capture_scaffold(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "038_ai-agent-graph-source-package-manifest-evidence-capture-scaffold.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["capture_row_id"] for row in rows],
            [
                "graph-source-evidence-package-manifest-capture-001",
                "graph-source-evidence-package-manifest-capture-002",
                "graph-source-evidence-package-manifest-capture-003",
            ],
        )
        self.assertEqual(
            [row["handoff_item_id"] for row in rows],
            [
                "graph-source-evidence-package-manifest-handoff-007",
                "graph-source-evidence-package-manifest-handoff-008",
                "graph-source-evidence-package-manifest-handoff-009",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(all(row["target_evidence_section"] == "package_manifest" for row in rows))
        self.assertTrue(
            all(
                row["source_package_file_manifest_path"]
                == "corpus/006_research-sources-and-bibliography/000_source-registers/"
                "009_source-package-file-manifest.csv"
                for row in rows
            )
        )
        self.assertTrue(
            all(row["source_package_file_manifest_row_status"] == "not_checked" for row in rows)
        )
        self.assertTrue(all(row["package_manifest_evidence_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["file_size_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["checksum_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["storage_boundary_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["rights_decision_status"] == "not_decided" for row in rows))
        self.assertTrue(all(row["source_promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all(row["decipherment_claim_status"] == "no_claim" for row in rows))
        self.assertTrue(all(row["capture_status"] == "empty_scaffold_not_started" for row in rows))
        empty_fields = [
            "package_file_id_evidence_value",
            "source_package_id_evidence_value",
            "source_id_evidence_value",
            "file_name_evidence_value",
            "file_kind_evidence_value",
            "source_url_evidence_value",
            "file_size_bytes_evidence_value",
            "download_id_evidence_value",
            "checksum_sha256_evidence_value",
            "commit_policy_evidence_value",
            "handling_strategy_evidence_value",
            "rights_status_evidence_value",
            "review_status_evidence_value",
        ]
        for row in rows:
            for field in empty_fields:
                self.assertEqual(row[field], "")
            self.assertEqual(
                row["handoff_scaffold_path"],
                "corpus/009_statistics-and-derived-features/"
                "037_ai-agent-graph-source-package-manifest-wave-handoff-scaffold.json",
            )
            self.assertIn(
                "corpus/006_research-sources-and-bibliography/000_source-registers/"
                "009_source-package-file-manifest.csv",
                row["route_files_to_open"],
            )
            self.assertIn(
                "open_package_manifest_before_recording_file_size_or_checksum",
                row["required_review_checks"],
            )
            self.assertIn("keep_raw_package_storage_boundary_explicit", row["required_review_checks"])
            self.assertIn("storage boundary", row["caution"])
            self.assertIn("collected evidence", row["caution"])

    def test_ai_agent_graph_source_package_manifest_capture_scaffold_builder(
        self,
    ) -> None:
        module = load_graph_source_package_manifest_capture_scaffold_module()
        root = repo_root()
        rows = module.build_capture_scaffold(
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "037_ai-agent-graph-source-package-manifest-wave-handoff-scaffold.json"
            )
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["capture_row_id"], "graph-source-evidence-package-manifest-capture-001")
        self.assertEqual(rows[1]["source_id"], "src-evobc")
        self.assertEqual(rows[2]["evidence_collection_review_task_id"], "graph-source-evidence-review-021")
        self.assertTrue(all(row["target_evidence_section"] == "package_manifest" for row in rows))
        self.assertTrue(all(row["package_manifest_evidence_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["package_file_id_evidence_value"] == "" for row in rows))
        self.assertTrue(all(row["file_size_bytes_evidence_value"] == "" for row in rows))
        self.assertTrue(all(row["checksum_sha256_evidence_value"] == "" for row in rows))
        self.assertIn("keep_raw_package_storage_boundary_explicit", rows[0]["required_review_checks"])
        self.assertIn("038_ai-agent", module.DEFAULT_OUTPUT.as_posix())

    def test_ai_agent_graph_source_package_manifest_capture_review_checklist(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "039_ai-agent-graph-source-package-manifest-capture-review-checklist.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        expected_check_keys = [
            "open_capture_row",
            "open_package_manifest_row",
            "verify_package_file_and_source_package_ids",
            "verify_file_name_kind_and_url",
            "verify_file_size_and_download_id",
            "verify_checksum_boundary",
            "verify_commit_policy_and_handling_strategy",
            "verify_rights_and_review_status_boundary",
            "block_source_promotion",
            "block_decipherment_claim",
        ]
        self.assertEqual(len(rows), 30)
        self.assertEqual(rows[0]["checklist_item_id"], "graph-source-evidence-package-manifest-check-001")
        self.assertEqual(rows[-1]["checklist_item_id"], "graph-source-evidence-package-manifest-check-030")
        self.assertEqual([row["check_key"] for row in rows[:10]], expected_check_keys)
        self.assertEqual(
            [row["capture_row_id"] for row in rows[::10]],
            [
                "graph-source-evidence-package-manifest-capture-001",
                "graph-source-evidence-package-manifest-capture-002",
                "graph-source-evidence-package-manifest-capture-003",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows[::10]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(all(row["target_evidence_section"] == "package_manifest" for row in rows))
        self.assertTrue(all(row["check_status"] == "not_started" for row in rows))
        self.assertTrue(
            all(row["review_status"] == "needs_package_manifest_capture_review" for row in rows)
        )
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["package_manifest_evidence_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["file_size_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["checksum_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["storage_boundary_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["rights_decision_status"] == "not_decided" for row in rows))
        self.assertTrue(all(row["source_promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all(row["decipherment_claim_status"] == "no_claim" for row in rows))
        self.assertTrue(
            all(
                row["source_package_file_manifest_path"]
                == "corpus/006_research-sources-and-bibliography/000_source-registers/"
                "009_source-package-file-manifest.csv"
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["capture_scaffold_path"].endswith(
                    "038_ai-agent-graph-source-package-manifest-evidence-capture-scaffold.csv"
                )
                for row in rows
            )
        )
        self.assertTrue(
            all(
                "corpus/006_research-sources-and-bibliography/000_source-registers/"
                "009_source-package-file-manifest.csv"
                in row["route_files_to_open"]
                for row in rows
            )
        )
        self.assertTrue(
            all(
                "keep_raw_package_storage_boundary_explicit" in row["required_review_checks"]
                for row in rows
            )
        )
        self.assertTrue(any("file size" in row["instruction"] for row in rows))
        self.assertTrue(any("checksum" in row["instruction"] for row in rows))
        self.assertTrue(any("不得仅凭文件大小" in row["instruction_zh"] for row in rows))
        self.assertTrue(all("Checklist item only" in row["caution"] for row in rows))
        self.assertTrue(all("storage-boundary review" in row["caution"] for row in rows))
        self.assertTrue(all("decipherment conclusion" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_package_manifest_capture_review_checklist_builder(
        self,
    ) -> None:
        module = load_graph_source_package_manifest_capture_review_checklist_module()
        root = repo_root()
        rows = module.build_review_checklist(
            module.read_csv_rows(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "038_ai-agent-graph-source-package-manifest-evidence-capture-scaffold.csv"
            )
        )

        self.assertEqual(len(rows), 30)
        self.assertEqual(rows[0]["check_key"], "open_capture_row")
        self.assertEqual(rows[1]["check_key"], "open_package_manifest_row")
        self.assertEqual(rows[5]["check_key"], "verify_checksum_boundary")
        self.assertEqual(rows[6]["check_key"], "verify_commit_policy_and_handling_strategy")
        self.assertEqual(rows[7]["check_key"], "verify_rights_and_review_status_boundary")
        self.assertEqual(rows[-1]["check_key"], "block_decipherment_claim")
        self.assertEqual(rows[0]["review_status"], "needs_package_manifest_capture_review")
        self.assertEqual(rows[0]["evidence_collection_status"], "not_collected")
        self.assertEqual(rows[0]["package_manifest_evidence_status"], "not_collected")
        self.assertEqual(rows[0]["file_size_review_status"], "not_started")
        self.assertEqual(rows[0]["checksum_review_status"], "not_started")
        self.assertEqual(rows[0]["rights_decision_status"], "not_decided")
        self.assertIn("039_ai-agent", module.DEFAULT_OUTPUT.as_posix())
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"package_manifest"})

    def test_ai_agent_graph_source_download_log_capture_scaffold(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "035_ai-agent-graph-source-download-log-evidence-capture-scaffold.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["capture_row_id"] for row in rows],
            [
                "graph-source-evidence-download-log-capture-001",
                "graph-source-evidence-download-log-capture-002",
                "graph-source-evidence-download-log-capture-003",
            ],
        )
        self.assertEqual(
            [row["handoff_item_id"] for row in rows],
            [
                "graph-source-evidence-download-log-handoff-004",
                "graph-source-evidence-download-log-handoff-005",
                "graph-source-evidence-download-log-handoff-006",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(all(row["target_evidence_section"] == "download_log" for row in rows))
        self.assertTrue(
            all(
                row["source_download_log_path"]
                == "project_registry/006_large-source-register/002_source-download-log.csv"
                for row in rows
            )
        )
        self.assertTrue(all(row["source_download_log_row_status"] == "not_checked" for row in rows))
        self.assertTrue(all(row["download_log_evidence_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["checksum_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["size_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["access_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["rights_decision_status"] == "not_decided" for row in rows))
        self.assertTrue(all(row["source_promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all(row["decipherment_claim_status"] == "no_claim" for row in rows))
        self.assertTrue(all(row["capture_status"] == "empty_scaffold_not_started" for row in rows))
        empty_fields = [
            "download_id_evidence_value",
            "source_id_evidence_value",
            "url_evidence_value",
            "downloaded_at_evidence_value",
            "download_status_evidence_value",
            "http_status_evidence_value",
            "file_size_bytes_evidence_value",
            "checksum_sha256_evidence_value",
            "local_temp_path_evidence_value",
            "risk_note_evidence_value",
        ]
        for row in rows:
            for field in empty_fields:
                self.assertEqual(row[field], "")
            self.assertEqual(
                row["handoff_scaffold_path"],
                "corpus/009_statistics-and-derived-features/"
                "034_ai-agent-graph-source-download-log-wave-handoff-scaffold.json",
            )
            self.assertIn(
                "project_registry/006_large-source-register/002_source-download-log.csv",
                row["route_files_to_open"],
            )
            self.assertIn(
                "open_download_log_before_recording_access_or_checksum_status",
                row["required_review_checks"],
            )
            self.assertIn("do_not_infer_rights_from_download_success", row["required_review_checks"])
            self.assertIn("do not infer rights", row["caution"])
            self.assertIn("collected evidence", row["caution"])

    def test_ai_agent_graph_source_download_log_capture_scaffold_builder(
        self,
    ) -> None:
        module = load_graph_source_download_log_capture_scaffold_module()
        root = repo_root()
        rows = module.build_capture_scaffold(
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "034_ai-agent-graph-source-download-log-wave-handoff-scaffold.json"
            )
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["capture_row_id"], "graph-source-evidence-download-log-capture-001")
        self.assertEqual(rows[1]["source_id"], "src-evobc")
        self.assertEqual(rows[2]["evidence_collection_review_task_id"], "graph-source-evidence-review-020")
        self.assertTrue(all(row["target_evidence_section"] == "download_log" for row in rows))
        self.assertTrue(all(row["download_log_evidence_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["checksum_sha256_evidence_value"] == "" for row in rows))
        self.assertTrue(all(row["file_size_bytes_evidence_value"] == "" for row in rows))
        self.assertIn("do_not_infer_rights_from_download_success", rows[0]["required_review_checks"])
        self.assertIn("035_ai-agent", module.DEFAULT_OUTPUT.as_posix())

    def test_ai_agent_graph_source_download_log_capture_review_checklist(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "036_ai-agent-graph-source-download-log-capture-review-checklist.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        expected_check_keys = [
            "open_capture_row",
            "open_download_log_row",
            "verify_download_id_and_url",
            "verify_download_and_http_status",
            "verify_file_size",
            "verify_checksum",
            "verify_local_temp_path_and_risk",
            "block_rights_inference",
            "block_source_promotion",
            "block_decipherment_claim",
        ]
        self.assertEqual(len(rows), 30)
        self.assertEqual(rows[0]["checklist_item_id"], "graph-source-evidence-download-log-check-001")
        self.assertEqual(rows[-1]["checklist_item_id"], "graph-source-evidence-download-log-check-030")
        self.assertEqual([row["check_key"] for row in rows[:10]], expected_check_keys)
        self.assertEqual(
            [row["capture_row_id"] for row in rows[::10]],
            [
                "graph-source-evidence-download-log-capture-001",
                "graph-source-evidence-download-log-capture-002",
                "graph-source-evidence-download-log-capture-003",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows[::10]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(all(row["target_evidence_section"] == "download_log" for row in rows))
        self.assertTrue(all(row["check_status"] == "not_started" for row in rows))
        self.assertTrue(
            all(row["review_status"] == "needs_download_log_capture_review" for row in rows)
        )
        self.assertTrue(all(row["evidence_collection_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["download_log_evidence_status"] == "not_collected" for row in rows))
        self.assertTrue(all(row["checksum_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["size_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["access_review_status"] == "not_started" for row in rows))
        self.assertTrue(all(row["rights_decision_status"] == "not_decided" for row in rows))
        self.assertTrue(all(row["source_promotion_status"] == "not_promoted" for row in rows))
        self.assertTrue(all(row["decipherment_claim_status"] == "no_claim" for row in rows))
        self.assertTrue(
            all(
                row["source_download_log_path"]
                == "project_registry/006_large-source-register/002_source-download-log.csv"
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["capture_scaffold_path"].endswith(
                    "035_ai-agent-graph-source-download-log-evidence-capture-scaffold.csv"
                )
                for row in rows
            )
        )
        self.assertTrue(
            all(
                "project_registry/006_large-source-register/002_source-download-log.csv"
                in row["route_files_to_open"]
                for row in rows
            )
        )
        self.assertTrue(
            all(
                "do_not_infer_rights_from_download_success" in row["required_review_checks"]
                for row in rows
            )
        )
        self.assertTrue(any("HTTP status" in row["instruction"] for row in rows))
        self.assertTrue(any("checksum" in row["instruction"] for row in rows))
        self.assertTrue(any("不得从下载成功" in row["instruction_zh"] for row in rows))
        self.assertTrue(all("Checklist item only" in row["caution"] for row in rows))
        self.assertTrue(all("checksum review" in row["caution"] for row in rows))
        self.assertTrue(all("decipherment conclusion" in row["caution"] for row in rows))

    def test_ai_agent_graph_source_download_log_capture_review_checklist_builder(
        self,
    ) -> None:
        module = load_graph_source_download_log_capture_review_checklist_module()
        root = repo_root()
        rows = module.build_review_checklist(
            module.read_csv_rows(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "035_ai-agent-graph-source-download-log-evidence-capture-scaffold.csv"
            )
        )

        self.assertEqual(len(rows), 30)
        self.assertEqual(rows[0]["check_key"], "open_capture_row")
        self.assertEqual(rows[1]["check_key"], "open_download_log_row")
        self.assertEqual(rows[6]["check_key"], "verify_local_temp_path_and_risk")
        self.assertEqual(rows[7]["check_key"], "block_rights_inference")
        self.assertEqual(rows[-1]["check_key"], "block_decipherment_claim")
        self.assertEqual(rows[0]["review_status"], "needs_download_log_capture_review")
        self.assertEqual(rows[0]["evidence_collection_status"], "not_collected")
        self.assertEqual(rows[0]["download_log_evidence_status"], "not_collected")
        self.assertEqual(rows[0]["checksum_review_status"], "not_started")
        self.assertEqual(rows[0]["rights_decision_status"], "not_decided")
        self.assertIn("036_ai-agent", module.DEFAULT_OUTPUT.as_posix())
        self.assertEqual({row["target_evidence_section"] for row in rows}, {"download_log"})

    def test_ai_agent_graph_source_source_register_capture_scaffold(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "032_ai-agent-graph-source-source-register-evidence-capture-scaffold.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["capture_row_id"] for row in rows],
            [
                "graph-source-evidence-source-register-capture-001",
                "graph-source-evidence-source-register-capture-002",
                "graph-source-evidence-source-register-capture-003",
            ],
        )
        self.assertEqual(
            [row["handoff_item_id"] for row in rows],
            [
                "graph-source-evidence-handoff-001",
                "graph-source-evidence-handoff-002",
                "graph-source-evidence-handoff-003",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertEqual(
            [row["evidence_collection_review_task_id"] for row in rows],
            [
                "graph-source-evidence-review-001",
                "graph-source-evidence-review-010",
                "graph-source-evidence-review-019",
            ],
        )
        self.assertTrue(
            all(row["target_evidence_section"] == "source_register" for row in rows)
        )
        self.assertTrue(
            all(row["source_register_row_status"] == "not_checked" for row in rows)
        )
        self.assertTrue(
            all(row["evidence_collection_status"] == "not_collected" for row in rows)
        )
        self.assertTrue(
            all(row["source_register_evidence_status"] == "not_collected" for row in rows)
        )
        self.assertTrue(
            all(row["rights_decision_status"] == "not_decided" for row in rows)
        )
        self.assertTrue(
            all(row["source_promotion_status"] == "not_promoted" for row in rows)
        )
        self.assertTrue(
            all(row["decipherment_claim_status"] == "no_claim" for row in rows)
        )
        self.assertTrue(
            all(row["capture_status"] == "empty_scaffold_not_started" for row in rows)
        )
        empty_fields = [
            "source_id_evidence_value",
            "primary_external_ref_evidence_value",
            "source_title_evidence_value",
            "source_type_evidence_value",
            "rights_status_evidence_value",
            "risk_note_evidence_value",
            "review_status_evidence_value",
        ]
        self.assertTrue(all(row[fieldname] == "" for row in rows for fieldname in empty_fields))
        self.assertTrue(
            all(
                "corpus/006_research-sources-and-bibliography/000_source-registers/"
                "001_all-sources-index.csv" in row["route_files_to_open"]
                for row in rows
            )
        )
        self.assertTrue(
            all(
                "open_source_register_row_before_copying_provenance"
                in row["required_review_checks"]
                for row in rows
            )
        )
        self.assertTrue(
            all("do not use it as collected evidence" in row["caution"] for row in rows)
        )

    def test_ai_agent_graph_source_source_register_capture_scaffold_builder(
        self,
    ) -> None:
        module = (
            load_graph_source_evidence_collection_source_register_capture_scaffold_module()
        )
        root = repo_root()
        rows = module.build_capture_scaffold(
            module.read_json(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "031_ai-agent-graph-source-evidence-collection-wave-handoff-scaffold.json"
            )
        )

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["source_id"], "src-hust-obc")
        self.assertEqual(rows[1]["source_id"], "src-evobc")
        self.assertEqual(rows[2]["source_id"], "src-obimd")
        self.assertEqual(rows[0]["capture_status"], "empty_scaffold_not_started")
        self.assertEqual(rows[1]["source_register_row_status"], "not_checked")
        self.assertEqual(rows[2]["source_register_evidence_status"], "not_collected")
        self.assertEqual(
            rows[0]["handoff_scaffold_path"],
            "corpus/009_statistics-and-derived-features/"
            "031_ai-agent-graph-source-evidence-collection-wave-handoff-scaffold.json",
        )
        self.assertIn(
            "corpus/006_research-sources-and-bibliography/000_source-registers/"
            "001_all-sources-index.csv",
            rows[0]["route_files_to_open"],
        )
        self.assertIn("decipherment conclusion", rows[0]["caution"])

    def test_ai_agent_graph_source_source_register_capture_review_checklist(
        self,
    ) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "033_ai-agent-graph-source-source-register-capture-review-checklist.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        expected_check_keys = [
            "open_capture_row",
            "open_source_register_row",
            "verify_primary_external_ref",
            "verify_title_and_type",
            "verify_rights_and_risk",
            "keep_capture_boundary",
            "block_source_promotion",
            "block_decipherment_claim",
        ]
        self.assertEqual(len(rows), 24)
        self.assertEqual(rows[0]["checklist_item_id"], "graph-source-evidence-source-register-check-001")
        self.assertEqual(rows[-1]["checklist_item_id"], "graph-source-evidence-source-register-check-024")
        self.assertEqual(
            [row["check_key"] for row in rows[:8]],
            expected_check_keys,
        )
        self.assertEqual(
            [row["capture_row_id"] for row in rows[::8]],
            [
                "graph-source-evidence-source-register-capture-001",
                "graph-source-evidence-source-register-capture-002",
                "graph-source-evidence-source-register-capture-003",
            ],
        )
        self.assertEqual(
            [row["source_id"] for row in rows[::8]],
            ["src-hust-obc", "src-evobc", "src-obimd"],
        )
        self.assertTrue(all(row["check_status"] == "not_started" for row in rows))
        self.assertTrue(
            all(row["review_status"] == "needs_source_register_capture_review" for row in rows)
        )
        self.assertTrue(
            all(row["evidence_collection_status"] == "not_collected" for row in rows)
        )
        self.assertTrue(
            all(row["rights_decision_status"] == "not_decided" for row in rows)
        )
        self.assertTrue(
            all(row["source_promotion_status"] == "not_promoted" for row in rows)
        )
        self.assertTrue(
            all(row["decipherment_claim_status"] == "no_claim" for row in rows)
        )
        self.assertTrue(
            all(
                row["capture_scaffold_path"].endswith(
                    "032_ai-agent-graph-source-source-register-evidence-capture-scaffold.csv"
                )
                for row in rows
            )
        )
        self.assertTrue(
            all(
                "corpus/006_research-sources-and-bibliography/000_source-registers/"
                "001_all-sources-index.csv" in row["route_files_to_open"]
                for row in rows
            )
        )
        self.assertTrue(all(row["instruction"] and row["instruction_zh"] for row in rows))
        self.assertTrue(
            any(row["check_key"] == "block_decipherment_claim" for row in rows)
        )
        self.assertTrue(
            all("does not contain collected evidence" in row["caution"] for row in rows)
        )

    def test_ai_agent_graph_source_source_register_capture_review_checklist_builder(
        self,
    ) -> None:
        module = load_graph_source_source_register_capture_review_checklist_module()
        root = repo_root()
        rows = module.build_review_checklist(
            module.read_csv_rows(
                root
                / "corpus/009_statistics-and-derived-features/"
                / "032_ai-agent-graph-source-source-register-evidence-capture-scaffold.csv"
            )
        )

        self.assertEqual(len(rows), 24)
        self.assertEqual(rows[0]["check_key"], "open_capture_row")
        self.assertEqual(rows[7]["check_key"], "block_decipherment_claim")
        self.assertEqual(rows[8]["source_id"], "src-evobc")
        self.assertEqual(rows[16]["source_id"], "src-obimd")
        self.assertEqual(rows[0]["check_status"], "not_started")
        self.assertEqual(rows[0]["evidence_collection_status"], "not_collected")
        self.assertEqual(rows[0]["rights_decision_status"], "not_decided")
        self.assertIn("source-register row", rows[1]["instruction"])
        self.assertIn("不得从本 checklist 提升来源", rows[6]["instruction_zh"])
        self.assertIn("decipherment conclusion", rows[0]["caution"])

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
        self.assertIn("nlc_oracle_world_objects=2964", text)
        self.assertIn("object_images=5932", text)
        self.assertIn("rubbings=2975", text)
        self.assertIn("rubbing_images=3177", text)
        self.assertIn("nlc_oracle_bone_holding_count=35651", text)
        self.assertIn("nlc_field_contract=holding_number", text)
        self.assertIn("nlc_heji_refs_over_8000", text)
        self.assertIn("nlc_yinqi_cuibian_refs=1595", text)
        self.assertIn("smithsonian_nmaa_accession=FSC-O-26", text)
        self.assertIn("rights=CC0", text)
        self.assertIn("iiif_source_image_id=FS-FSC-O-26_1", text)
        self.assertIn("smithsonian_nmaa_provenance_john_hadley_cox_xiaotun_anyang", text)
        self.assertIn("penn_museum_object_number=49-14-7A", text)
        self.assertIn("provenience=Anyang", text)
        self.assertIn("period=Shang_Dynasty", text)
        self.assertIn("penn_museum_materials=Bone;Shell", text)
        self.assertIn("credit_line_julia_morgan_hugh_morgan_1949", text)
        self.assertIn("metmuseum_object_id=42045", text)
        self.assertIn("accession=67.43.14", text)
        self.assertIn("metmuseum_object_id=42022", text)
        self.assertIn("accession=18.56.71", text)
        self.assertIn("metmuseum_primary_image_urls_available_for_public_domain_objects", text)
        self.assertIn("xiaoxuetang_portal_scope=glyphs_over_180000", text)
        self.assertIn("phonology_over_1000000", text)
        self.assertIn("dictionary_indexes_over_250000", text)
        self.assertIn("covers_oracle_bone_bronze_warring_states_seal_regular", text)
        self.assertIn("xiaoxuetang_portal_rights_holders=ntu_chinese_ihp_iis", text)
        self.assertIn("yinshang_oracle_vocab_pieces=52486", text)
        self.assertIn("characters_about_1000000", text)
        self.assertIn("major_corpora=heji_xiaotun_nandi_yingguo_tokyo_whitney", text)
        self.assertIn("yinshang_oracle_vocab_topics=astronomy_calendar_weather_geography_polities", text)
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

    def test_source_download_status_codebook_defines_log_statuses(self) -> None:
        codebook_path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "013_source-download-status-codebook.csv"
        )
        log_path = repo_root() / "project_registry/006_large-source-register/002_source-download-log.csv"
        with codebook_path.open("r", encoding="utf-8-sig", newline="") as file:
            status_rows = {row["status_code"]: row for row in csv.DictReader(file)}
        with log_path.open("r", encoding="utf-8-sig", newline="") as file:
            log_statuses = {row["status"] for row in csv.DictReader(file)}

        expected = {
            "downloaded",
            "downloaded_access_restricted_page",
            "downloaded_client_challenge_page",
            "download_error",
            "http_error",
            "skipped_exceeds_manifest_limit",
        }
        self.assertTrue(expected.issubset(status_rows))
        self.assertTrue(log_statuses.issubset(status_rows))
        self.assertEqual(status_rows["downloaded"]["can_support_payload_extracted"], "true")
        self.assertEqual(status_rows["download_error"]["can_support_payload_extracted"], "false")
        self.assertEqual(status_rows["downloaded_access_restricted_page"]["can_support_payload_extracted"], "false")
        self.assertIn("Do not treat download_error as proof", status_rows["download_error"]["caution_en"])

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
            "met-obj",
            "sinica-da-xxt",
            "sinica-lachnoracle",
        }
        self.assertTrue(expected.issubset(prefixes))
        self.assertEqual(prefixes["hust-obc-cat"]["source_id"], "src-hust-obc")
        self.assertEqual(prefixes["obimd-main"]["source_id"], "src-obimd")
        self.assertEqual(prefixes["cam-hopkins-j"]["source_id"], "src-cambridge-hopkins")
        self.assertEqual(prefixes["ihp-mus-obj"]["source_id"], "src-ihp-museum-oracle-bones")
        self.assertEqual(prefixes["evobc-cat"]["source_id"], "src-evobc")
        self.assertEqual(prefixes["met-obj"]["source_id"], "src-metmuseum-oracle-bone")
        self.assertEqual(prefixes["sinica-da-xxt"]["source_id"], "src-sinica-da-xiaoxuetang-site")
        self.assertEqual(
            prefixes["sinica-lachnoracle"]["source_id"],
            "src-sinica-yinshang-oracle-vocabulary",
        )
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
        self.assertEqual(metrics[("src-nlc-oracle-world", "oracle_world_object_record_count")], "2964")
        self.assertEqual(metrics[("src-nlc-oracle-world", "oracle_world_object_image_count")], "5932")
        self.assertEqual(metrics[("src-nlc-oracle-world", "oracle_world_rubbing_record_count")], "2975")
        self.assertEqual(metrics[("src-nlc-oracle-world", "oracle_world_rubbing_image_count")], "3177")
        self.assertEqual(metrics[("src-nlc-oracle-world", "nlc_oracle_bone_holding_count")], "35651")
        self.assertEqual(metrics[("src-nlc-oracle-world", "nlc_yinqi_cuibian_cataloged_count")], "1595")
        self.assertEqual(metrics[("src-smithsonian-nmaa-oracle-bone", "accession_number")], "FSC-O-26")
        self.assertEqual(metrics[("src-smithsonian-nmaa-oracle-bone", "rights_status")], "CC0")
        self.assertEqual(metrics[("src-smithsonian-nmaa-oracle-bone", "iiif_source_image_id")], "FS-FSC-O-26_1")
        self.assertEqual(metrics[("src-penn-museum-oracle-bone", "object_number")], "49-14-7A")
        self.assertEqual(metrics[("src-penn-museum-oracle-bone", "provenience")], "Anyang")
        self.assertEqual(metrics[("src-penn-museum-oracle-bone", "period")], "Shang Dynasty")
        self.assertEqual(metrics[("src-penn-museum-oracle-bone", "current_location")], "Asia Galleries - On Display")
        self.assertEqual(metrics[("src-metmuseum-oracle-bone", "object_id")], "42022")
        self.assertEqual(metrics[("src-metmuseum-oracle-bone", "accession_number")], "18.56.71")
        self.assertEqual(metrics[("src-metmuseum-oracle-bone", "is_public_domain")], "true")
        self.assertEqual(metrics[("src-sinica-da-xiaoxuetang-site", "xiaoxuetang_glyph_total_over")], "180000")
        self.assertEqual(
            metrics[("src-sinica-da-xiaoxuetang-site", "xiaoxuetang_phonology_total_over")],
            "1000000",
        )
        self.assertEqual(
            metrics[("src-sinica-da-xiaoxuetang-site", "xiaoxuetang_dictionary_index_total_over")],
            "250000",
        )
        self.assertEqual(
            metrics[("src-sinica-yinshang-oracle-vocabulary", "yinshang_oracle_bone_piece_count")],
            "52486",
        )
        self.assertEqual(
            metrics[("src-sinica-yinshang-oracle-vocabulary", "yinshang_oracle_character_count_about")],
            "1000000",
        )

    def test_nlc_oracle_world_source_is_official_scope_confirmed(self) -> None:
        source_path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "001_all-sources-index.csv"
        )
        download_log_path = repo_root() / "project_registry/006_large-source-register/002_source-download-log.csv"
        field_map_path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "007_source-field-map.csv"
        )
        with source_path.open("r", encoding="utf-8-sig", newline="") as file:
            sources = {row["source_id"]: row for row in csv.DictReader(file)}
        with download_log_path.open("r", encoding="utf-8-sig", newline="") as file:
            log_rows = {row["download_id"]: row for row in csv.DictReader(file)}
        with field_map_path.open("r", encoding="utf-8-sig", newline="") as file:
            field_rows = [
                row for row in csv.DictReader(file)
                if row["source_id"] == "src-nlc-oracle-world"
            ]

        nlc = sources["src-nlc-oracle-world"]
        self.assertEqual(nlc["adoption_status"], "candidate_institutional_official_scope_confirmed")
        self.assertEqual(nlc["review_status"], "reviewed")
        self.assertIn("35651", nlc["scope"])
        self.assertIn("not a stable current bulk endpoint", nlc["risk_note"])
        self.assertIn("dl-nlc-oracle-world-note", log_rows)
        self.assertIn("dl-nlc-oracle-database-design", log_rows)
        self.assertEqual(log_rows["dl-nlc-oracle-database-design"]["status"], "downloaded")
        self.assertTrue(log_rows["dl-nlc-oracle-database-design"]["local_temp_path"].startswith("tmp/"))
        self.assertGreater(int(log_rows["dl-nlc-oracle-database-design"]["file_size_bytes"]), 0)
        field_names = {row["source_field_or_unit"] for row in field_rows}
        self.assertTrue({"馆藏号", "来源号", "著录情况"}.issubset(field_names))
        joined_target_fields = " ".join(row["target_project_field"] for row in field_rows)
        self.assertIn("nlc_holding_number", joined_target_fields)
        self.assertIn("heji_ref_id", joined_target_fields)

    def test_smithsonian_nmaa_public_domain_sample_staging(self) -> None:
        source_path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "001_all-sources-index.csv"
        )
        download_log_path = repo_root() / "project_registry/006_large-source-register/002_source-download-log.csv"
        staging_path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "003_smithsonian-nmaa-oracle-bone-object-staging.csv"
        )
        with source_path.open("r", encoding="utf-8-sig", newline="") as file:
            sources = {row["source_id"]: row for row in csv.DictReader(file)}
        with download_log_path.open("r", encoding="utf-8-sig", newline="") as file:
            log_rows = {row["download_id"]: row for row in csv.DictReader(file)}
        with staging_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        source = sources["src-smithsonian-nmaa-oracle-bone"]
        self.assertEqual(source["adoption_status"], "adopted_public_domain_sample_source")
        self.assertEqual(source["rights_status"], "public_domain_verified")
        self.assertIn("FSC-O-26", source["scope"])
        self.assertIn("request verification", source["risk_note"])
        self.assertIn("dl-smithsonian-nmaa-fsc-o-26-archive", log_rows)
        self.assertEqual(log_rows["dl-smithsonian-nmaa-fsc-o-26-archive"]["status"], "downloaded")
        self.assertTrue(log_rows["dl-smithsonian-nmaa-fsc-o-26-archive"]["local_temp_path"].startswith("tmp/"))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["candidate_collection_object_id"], "si-nmaa-obj-00001")
        self.assertEqual(row["source_collection_item_id"], "FSC-O-26")
        self.assertEqual(row["accession_number"], "FSC-O-26")
        self.assertEqual(row["iiif_source_image_id"], "FS-FSC-O-26_1")
        self.assertEqual(row["rights_status"], "public_domain_verified")
        self.assertEqual(row["iiif_manifest_status"], "public_domain_image_committed_as_asset_000003")
        self.assertIn("John Hadley Cox", row["provenance_note"])
        self.assertIn("CC0 IIIF image is committed as asset-000003", row["caution"])

    def test_penn_museum_oracle_bone_object_staging(self) -> None:
        source_path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "001_all-sources-index.csv"
        )
        download_log_path = repo_root() / "project_registry/006_large-source-register/002_source-download-log.csv"
        staging_path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "004_penn-museum-oracle-bone-object-staging.csv"
        )
        with source_path.open("r", encoding="utf-8-sig", newline="") as file:
            sources = {row["source_id"]: row for row in csv.DictReader(file)}
        with download_log_path.open("r", encoding="utf-8-sig", newline="") as file:
            log_rows = {row["download_id"]: row for row in csv.DictReader(file)}
        with staging_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        source = sources["src-penn-museum-oracle-bone"]
        self.assertEqual(source["adoption_status"], "adopted_collection_reference")
        self.assertEqual(source["rights_status"], "metadata_only_until_verified")
        self.assertIn("49-14-7A", source["scope"])
        self.assertIn("object-level review", source["risk_note"])
        self.assertIn("dl-penn-museum-49-14-7a", log_rows)
        self.assertEqual(log_rows["dl-penn-museum-49-14-7a"]["status"], "downloaded")
        self.assertTrue(log_rows["dl-penn-museum-49-14-7a"]["local_temp_path"].startswith("tmp/"))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["candidate_collection_object_id"], "penn-mus-obj-00001")
        self.assertEqual(row["source_collection_item_id"], "49-14-7A")
        self.assertEqual(row["provenience"], "Anyang")
        self.assertEqual(row["historical_period"], "Shang Dynasty")
        self.assertEqual(row["materials"], "Bone;Shell")
        self.assertEqual(row["dimensions"], "height_cm=2.3;width_cm=2.5")
        self.assertEqual(row["rights_status"], "metadata_only_until_verified")
        self.assertIn("raw object images are not downloaded", row["caution"].lower())

    def test_metmuseum_public_domain_oracle_bone_object_staging(self) -> None:
        source_path = (
            repo_root()
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            / "001_all-sources-index.csv"
        )
        download_log_path = repo_root() / "project_registry/006_large-source-register/002_source-download-log.csv"
        staging_path = (
            repo_root()
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "005_metmuseum-oracle-bone-object-staging.csv"
        )
        with source_path.open("r", encoding="utf-8-sig", newline="") as file:
            sources = {row["source_id"]: row for row in csv.DictReader(file)}
        with download_log_path.open("r", encoding="utf-8-sig", newline="") as file:
            log_rows = {row["download_id"]: row for row in csv.DictReader(file)}
        with staging_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        source = sources["src-metmuseum-oracle-bone"]
        self.assertEqual(source["adoption_status"], "adopted_public_domain_sample_source")
        self.assertEqual(source["rights_status"], "public_domain_verified")
        self.assertIn("42045", source["scope"])
        self.assertIn("42022", source["scope"])
        for download_id in ["dl-metmuseum-object-42045", "dl-metmuseum-object-42022"]:
            self.assertIn(download_id, log_rows)
            self.assertEqual(log_rows[download_id]["status"], "downloaded")
            self.assertTrue(log_rows[download_id]["local_temp_path"].startswith("tmp/"))

        self.assertEqual(len(rows), 2)
        by_id = {row["candidate_collection_object_id"]: row for row in rows}
        first = by_id["met-obj-00001"]
        second = by_id["met-obj-00002"]
        self.assertEqual(first["source_collection_item_id"], "42045")
        self.assertEqual(first["accession_number"], "67.43.14")
        self.assertEqual(first["is_public_domain"], "true")
        self.assertEqual(first["rights_status"], "public_domain_verified")
        self.assertTrue(first["primary_image_url"].endswith("LC-67_43_14_002.jpg"))
        self.assertEqual(second["source_collection_item_id"], "42022")
        self.assertEqual(second["accession_number"], "18.56.71")
        self.assertEqual(second["is_public_domain"], "true")
        self.assertEqual(second["object_date"], "13th-11th century BCE")
        self.assertTrue(second["primary_image_url"].endswith("LC-18_56_71_002.jpg"))
        self.assertEqual(
            {row["project_import_status"] for row in rows},
            {"object_metadata_not_promoted"},
        )
        self.assertTrue(all("raw image files are not committed" in row["caution"] for row in rows))

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

    def test_hust_obc_first_bucket_candidate_packets_materialize_100_candidates(self) -> None:
        manifest_path = (
            repo_root()
            / "corpus/001_oracle-characters/"
            / "001_000001-000100_obs-char-bucket_oracle-characters/"
            / "001_hust-obc-candidate-packet-manifest.csv"
        )
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 100)
        self.assertEqual(rows[0]["candidate_packet_id"], "hust-obc-candidate-packet-000001")
        self.assertEqual(rows[-1]["candidate_packet_id"], "hust-obc-candidate-packet-000100")
        self.assertEqual(rows[0]["suggested_oracle_character_id"], "obs-char-000001")
        self.assertEqual(rows[-1]["suggested_oracle_character_id"], "obs-char-000100")
        self.assertEqual({row["source_id"] for row in rows}, {"src-hust-obc"})
        self.assertEqual(
            {row["decipherment_status"] for row in rows},
            {"unknown_until_cross_source_review"},
        )
        self.assertEqual(
            {row["dataset_label_status"] for row in rows},
            {"dataset_label_candidate_not_accepted_reading"},
        )
        self.assertEqual({row["assignment_status"] for row in rows}, {"reserved_candidate_not_assigned"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"needs_cross_source_review"})
        self.assertEqual({row["review_status"] for row in rows}, {"needs_cross_source_review"})
        self.assertTrue(all("not an accepted reading" in row["caution"] for row in rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in rows))

        first_packet_path = repo_root() / rows[0]["candidate_packet_path"]
        last_packet_path = repo_root() / rows[-1]["candidate_packet_path"]
        first_packet = json.loads(first_packet_path.read_text(encoding="utf-8"))
        last_packet = json.loads(last_packet_path.read_text(encoding="utf-8"))
        self.assertEqual(first_packet["record_type"], "oracle_character_candidate_packet")
        self.assertEqual(first_packet["source_candidate"]["promotion_queue_id"], "hust-obc-obs-char-promo-000001")
        self.assertEqual(last_packet["source_candidate"]["promotion_queue_id"], "hust-obc-obs-char-promo-000100")
        self.assertEqual(first_packet["dataset_label"]["status"], "dataset_label_candidate_not_accepted_reading")
        self.assertEqual(first_packet["dataset_label"]["source_modern_label_codepoints"], "U+2E80")
        self.assertIn("dl-hust-obc-validation-label", first_packet["evidence_download_ids"])
        self.assertIn(
            "corpus/001_oracle-characters/000_character-registers/"
            "009_hust-obc-obs-char-promotion-review-queue.csv",
            first_packet["route_files"],
        )
        self.assertIn("not an accepted oracle character record", first_packet["caution"])

    def test_hust_obc_candidate_packets_materialize_all_1588_candidates(self) -> None:
        root = repo_root()
        all_rows: list[dict[str, str]] = []
        bucket_counts: list[int] = []
        for bucket_number in range(1, 17):
            bucket_start = (bucket_number - 1) * 100 + 1
            bucket_end = bucket_start + 99
            bucket_directory = (
                f"{bucket_number:03d}_{bucket_start:06d}-{bucket_end:06d}"
                "_obs-char-bucket_oracle-characters"
            )
            manifest_path = (
                root
                / "corpus/001_oracle-characters"
                / bucket_directory
                / "001_hust-obc-candidate-packet-manifest.csv"
            )
            with manifest_path.open("r", encoding="utf-8-sig", newline="") as file:
                rows = list(csv.DictReader(file))
            bucket_counts.append(len(rows))
            all_rows.extend(rows)

        self.assertEqual(bucket_counts, [100] * 15 + [88])
        self.assertEqual(len(all_rows), 1588)
        self.assertEqual(all_rows[0]["candidate_packet_id"], "hust-obc-candidate-packet-000001")
        self.assertEqual(all_rows[-1]["candidate_packet_id"], "hust-obc-candidate-packet-001588")
        self.assertEqual(all_rows[0]["suggested_oracle_character_id"], "obs-char-000001")
        self.assertEqual(all_rows[-1]["suggested_oracle_character_id"], "obs-char-001588")
        self.assertEqual({row["source_id"] for row in all_rows}, {"src-hust-obc"})
        self.assertEqual(
            {row["decipherment_status"] for row in all_rows},
            {"unknown_until_cross_source_review"},
        )
        self.assertEqual(
            {row["dataset_label_status"] for row in all_rows},
            {"dataset_label_candidate_not_accepted_reading"},
        )
        self.assertEqual({row["assignment_status"] for row in all_rows}, {"reserved_candidate_not_assigned"})
        self.assertEqual({row["promotion_status"] for row in all_rows}, {"needs_cross_source_review"})
        self.assertEqual({row["review_status"] for row in all_rows}, {"needs_cross_source_review"})
        self.assertTrue(all("not an accepted reading" in row["caution"] for row in all_rows))
        self.assertTrue(all("not a decipherment conclusion" in row["caution"] for row in all_rows))

        first_packet = json.loads((root / all_rows[0]["candidate_packet_path"]).read_text(encoding="utf-8"))
        last_packet = json.loads((root / all_rows[-1]["candidate_packet_path"]).read_text(encoding="utf-8"))
        self.assertEqual(first_packet["record_type"], "oracle_character_candidate_packet")
        self.assertEqual(first_packet["source_candidate"]["promotion_queue_id"], "hust-obc-obs-char-promo-000001")
        self.assertEqual(last_packet["source_candidate"]["promotion_queue_id"], "hust-obc-obs-char-promo-001588")
        self.assertEqual(first_packet["dataset_label"]["status"], "dataset_label_candidate_not_accepted_reading")
        self.assertEqual(last_packet["dataset_label"]["status"], "dataset_label_candidate_not_accepted_reading")
        self.assertIn("dl-hust-obc-validation-label", first_packet["evidence_download_ids"])
        self.assertIn("dl-hust-obc-ocr-id-to-chinese", last_packet["evidence_download_ids"])
        self.assertIn("not an accepted oracle character record", first_packet["caution"])
        self.assertIn("not a decipherment conclusion", last_packet["caution"])

    def test_hust_obc_first_bucket_candidate_packet_builder_keeps_candidate_boundary(self) -> None:
        module = load_hust_obc_first_bucket_candidate_packets_module()
        root = repo_root()
        promotion_rows = module.read_csv_rows(
            root
            / "corpus/001_oracle-characters/000_character-registers/"
            / "009_hust-obc-obs-char-promotion-review-queue.csv"
        )
        packets, manifest_rows = module.build_candidate_packets(promotion_rows, limit=3)

        self.assertEqual(len(packets), 3)
        self.assertEqual(len(manifest_rows), 3)
        self.assertEqual(manifest_rows[0]["candidate_packet_id"], "hust-obc-candidate-packet-000001")
        self.assertEqual(manifest_rows[2]["suggested_oracle_character_id"], "obs-char-000003")
        self.assertEqual(manifest_rows[0]["dataset_label_status"], "dataset_label_candidate_not_accepted_reading")
        self.assertEqual(manifest_rows[0]["review_status"], "needs_cross_source_review")
        self.assertTrue(packets[0][0].as_posix().endswith("01_candidate-character-packet.json"))
        self.assertEqual(packets[0][1]["record_type"], "oracle_character_candidate_packet")
        self.assertEqual(packets[0][1]["decipherment_status"], "unknown_until_cross_source_review")
        self.assertEqual(packets[0][1]["dataset_label"]["status"], "dataset_label_candidate_not_accepted_reading")
        self.assertIn("not a decipherment conclusion", packets[0][1]["caution"])

    def test_hust_obc_candidate_packet_builder_groups_all_buckets(self) -> None:
        module = load_hust_obc_candidate_packets_module()
        root = repo_root()
        promotion_rows = module.read_csv_rows(root / module.PROMOTION_QUEUE)
        packets_by_manifest, manifest_rows_by_manifest = module.build_candidate_packets(promotion_rows)

        self.assertEqual(len(packets_by_manifest), 16)
        self.assertEqual(len(manifest_rows_by_manifest), 16)
        self.assertEqual(sum(len(packets) for packets in packets_by_manifest.values()), 1588)
        self.assertEqual(sum(len(rows) for rows in manifest_rows_by_manifest.values()), 1588)
        manifest_counts = [len(rows) for _, rows in sorted(manifest_rows_by_manifest.items())]
        self.assertEqual(manifest_counts, [100] * 15 + [88])

        first_manifest = sorted(manifest_rows_by_manifest)[0]
        last_manifest = sorted(manifest_rows_by_manifest)[-1]
        first_row = manifest_rows_by_manifest[first_manifest][0]
        last_row = manifest_rows_by_manifest[last_manifest][-1]
        self.assertEqual(first_row["candidate_packet_id"], "hust-obc-candidate-packet-000001")
        self.assertEqual(last_row["candidate_packet_id"], "hust-obc-candidate-packet-001588")
        self.assertEqual(first_row["dataset_label_status"], "dataset_label_candidate_not_accepted_reading")
        self.assertEqual(last_row["review_status"], "needs_cross_source_review")

        first_packet = packets_by_manifest[first_manifest][0][1]
        last_packet = packets_by_manifest[last_manifest][-1][1]
        self.assertEqual(first_packet["record_type"], "oracle_character_candidate_packet")
        self.assertEqual(last_packet["source_candidate"]["promotion_queue_id"], "hust-obc-obs-char-promo-001588")
        self.assertEqual(last_packet["decipherment_status"], "unknown_until_cross_source_review")
        self.assertIn("not a decipherment conclusion", last_packet["caution"])

    def test_hust_obimd_evobc_codepoint_crosswalk_records_lookup_routes_only(self) -> None:
        path = (
            repo_root()
            / "corpus/001_oracle-characters/000_character-registers/"
            / "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 1588)
        self.assertEqual(rows[0]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000001")
        self.assertEqual(rows[-1]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-001588")
        self.assertEqual(rows[0]["promotion_queue_id"], "hust-obc-obs-char-promo-000001")
        self.assertEqual(rows[-1]["promotion_queue_id"], "hust-obc-obs-char-promo-001588")
        self.assertEqual({row["identity_claim_status"] for row in rows}, {"no_identity_claim"})
        self.assertEqual({row["promotion_status"] for row in rows}, {"not_promoted"})
        self.assertEqual({row["review_status"] for row in rows}, {"needs_cross_source_review"})
        self.assertEqual(
            {row["match_basis"] for row in rows},
            {"exact_unicode_codepoint_sequence_from_dataset_labels"},
        )
        status_counts = Counter(row["cross_source_status"] for row in rows)
        self.assertEqual(
            status_counts,
            {
                "matched_evobc_by_codepoint": 112,
                "matched_obimd_and_evobc_by_codepoint": 15,
                "matched_obimd_by_codepoint": 7,
                "no_obimd_or_evobc_codepoint_match": 1454,
            },
        )
        self.assertEqual(sum(int(row["obimd_match_count"]) for row in rows), 22)
        self.assertEqual(sum(int(row["evobc_match_count"]) for row in rows), 127)
        self.assertTrue(all("not confirmed oracle-character identity" in row["caution"] for row in rows))
        self.assertTrue(all("not decipherment conclusions" in row["caution"] for row in rows))

        three_source_row = next(row for row in rows if row["cross_source_status"] == "matched_obimd_and_evobc_by_codepoint")
        self.assertEqual(three_source_row["matched_source_ids"], "src-hust-obc;src-obimd;src-evobc")
        self.assertEqual(three_source_row["hust_label_codepoints"], "U+342D")
        self.assertEqual(three_source_row["obimd_match_count"], "1")
        self.assertEqual(three_source_row["evobc_match_count"], "1")
        self.assertEqual(three_source_row["evobc_has_oracle_bone_refs_any"], "true")
        self.assertIn(
            "corpus/001_oracle-characters/000_character-registers/"
            "006_obimd-main-character-staging.csv",
            three_source_row["route_files"],
        )
        self.assertIn(
            "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            "001_evobc-evolution-category-staging.csv",
            three_source_row["route_files"],
        )

    def test_hust_obimd_evobc_codepoint_crosswalk_builder_matches_current_staging(self) -> None:
        module = load_hust_obimd_evobc_codepoint_crosswalk_module()
        root = repo_root()
        rows = module.build_crosswalk_rows(
            module.read_csv_rows(root / module.HUST_OBC_PROMOTION_QUEUE),
            module.read_csv_rows(root / module.OBIMD_MAIN_CHARACTER_STAGING),
            module.read_csv_rows(root / module.EVOBC_EVOLUTION_CATEGORY_STAGING),
        )

        self.assertEqual(len(rows), 1588)
        status_counts = Counter(row["cross_source_status"] for row in rows)
        self.assertEqual(status_counts["matched_obimd_and_evobc_by_codepoint"], 15)
        self.assertEqual(status_counts["matched_obimd_by_codepoint"], 7)
        self.assertEqual(status_counts["matched_evobc_by_codepoint"], 112)
        self.assertEqual(status_counts["no_obimd_or_evobc_codepoint_match"], 1454)
        self.assertEqual(sum(int(row["obimd_match_count"]) for row in rows), 22)
        self.assertEqual(sum(int(row["evobc_match_count"]) for row in rows), 127)
        self.assertEqual(rows[46]["crosswalk_candidate_id"], "hust-obimd-evobc-xwalk-000047")
        self.assertEqual(rows[46]["hust_label_codepoints"], "U+342D")
        self.assertEqual(rows[46]["matched_source_ids"], "src-hust-obc;src-obimd;src-evobc")
        self.assertEqual(rows[46]["identity_claim_status"], "no_identity_claim")
        self.assertIn("not evolution-chain assignments", rows[46]["caution"])

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

    def test_source_coverage_summary_preserves_current_source_totals(self) -> None:
        path = (
            repo_root()
            / "corpus/009_statistics-and-derived-features/"
            / "007_source-coverage-summary.csv"
        )
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 21)
        self.assertEqual(sum(int(row["download_manifest_count"]) for row in rows), 44)
        self.assertEqual(sum(int(row["download_log_count"]) for row in rows), 44)
        self.assertEqual(sum(int(row["metadata_profile_metric_count"]) for row in rows), 48)
        self.assertEqual(sum(int(row["committed_asset_count"]) for row in rows), 3)
        self.assertEqual(sum(int(row["committed_asset_bytes"]) for row in rows), 4922128)
        self.assertEqual(sum(int(row["graph_edge_count"]) for row in rows), 99674)
        self.assertEqual(sum(int(row["promotion_queue_candidate_count"]) for row in rows), 1588)
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(by_source["src-hust-obc"]["promotion_queue_candidate_count"], "1588")
        self.assertEqual(by_source["src-hust-obc"]["graph_edge_count"], "3562")
        self.assertEqual(by_source["src-obimd"]["graph_edge_count"], "44433")
        self.assertEqual(by_source["src-evobc"]["graph_edge_count"], "51679")
        self.assertEqual(by_source["src-metmuseum-oracle-bone"]["committed_asset_count"], "2")
        self.assertEqual(by_source["src-smithsonian-nmaa-oracle-bone"]["committed_asset_bytes"], "633418")
        self.assertEqual(
            by_source["src-xiaoxuetang-jiaguwen"]["download_status_counts"],
            "downloaded_access_restricted_page:2",
        )
        self.assertTrue(all("Coverage statistics only" in row["caution"] for row in rows))

    def test_source_coverage_statistics_builder_merges_source_rows(self) -> None:
        module = load_source_coverage_statistics_module()
        rows = module.build_source_coverage_summary(repo_root())
        by_source = {row["source_id"]: row for row in rows}
        self.assertEqual(len(rows), 21)
        self.assertEqual(by_source["src-hust-obc"]["metadata_profile_metric_count"], "11")
        self.assertEqual(by_source["src-hust-obc"]["coverage_status"], "has_relationship_graph_derivatives")
        self.assertEqual(by_source["src-obimd"]["graph_edge_type_count"], "2")
        self.assertEqual(by_source["src-metmuseum-oracle-bone"]["asset_rights_status_counts"], "public_domain_verified:2")
        self.assertEqual(
            by_source["src-smithsonian-nmaa-oracle-bone"]["coverage_status"],
            "has_committed_public_asset_or_metadata",
        )
        self.assertEqual(by_source["src-xiaoxuetang-jiaguwen"]["coverage_status"], "has_download_log_only")
        self.assertIn("source_registers", rows[0]["generated_from"])

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
