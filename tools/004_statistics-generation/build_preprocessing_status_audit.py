#!/usr/bin/env python3
"""Build a repository-wide preprocessing status audit.

The audit summarizes source engineering state only. It does not promote
candidate rows into accepted character, inscription, component, or decipherment
records.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/090_preprocessing-status-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/091_preprocessing-status-summary.json")
UPDATED_AT = "2026-06-19"
CAUTION = (
    "Preprocessing audit only; all identity, component, evolution, inscription, "
    "and decipherment-facing rows remain candidates or review routes until "
    "source evidence and human review promote them."
)

SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
CHAR_ID_MAP = Path("project_registry/002_project-id-to-source-reference-map/001_oracle-character-id-source-map.csv")
INSCRIPTION_ID_MAP = Path("project_registry/002_project-id-to-source-reference-map/002_oracle-inscription-id-source-map.csv")
ASSET_ID_MAP = Path("project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv")
COMPONENT_ID_MAP = Path("project_registry/002_project-id-to-source-reference-map/004_component-id-source-map.csv")
ACCEPTED_CHAR_INDEX = Path("corpus/001_oracle-characters/000_character-registers/001_all-oracle-characters-index.csv")
UNDECIPHERED_INDEX = Path("corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv")
HUST_VALIDATION_STAGING = Path("corpus/001_oracle-characters/000_character-registers/005_hust-obc-validation-class-staging.csv")
OBIMD_MAIN_STAGING = Path("corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv")
HUST_LABEL_CROSSWALK = Path("corpus/001_oracle-characters/000_character-registers/007_hust-obc-validation-label-crosswalk-staging.csv")
HUST_SOURCE_CATEGORY = Path("corpus/001_oracle-characters/000_character-registers/008_hust-obc-source-category-staging.csv")
HUST_PROMOTION_QUEUE = Path("corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv")
HUST_CODEPOINT_CROSSWALK = Path("corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv")
REL_GRAPH_DIR = Path("corpus/008_relationship-graph")
STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CAMBRIDGE_HOPKINS_REVIEW_QUEUE = STAT_DIR / "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
SOURCE_ENGINEERING_GAP_QUEUE = STAT_DIR / "099_ai-agent-source-engineering-gap-queue.csv"
SOURCE_ENGINEERING_EXECUTION_MATRIX = STAT_DIR / "100_ai-agent-source-engineering-execution-matrix.csv"
SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST = (
    STAT_DIR / "102_ai-agent-source-engineering-gap-review-log-draft-manifest.csv"
)
SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT = (
    STAT_DIR / "103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = (
    STAT_DIR / "104_ai-agent-source-engineering-next-action-checklist.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = (
    STAT_DIR / "105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
SOURCE_ENGINEERING_LANE_ROUTE_PACK = STAT_DIR / "107_ai-agent-source-engineering-lane-route-pack.json"
SOURCE_FIELD_MAP_SCAFFOLD = STAT_DIR / "108_ai-agent-source-field-map-scaffold.csv"
SOURCE_FIELD_MAP_REVIEW_CHECKLIST = STAT_DIR / "109_ai-agent-source-field-map-review-checklist.csv"
SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD = STAT_DIR / "110_ai-agent-source-field-map-review-result-scaffold.csv"
SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK = STAT_DIR / "111_ai-agent-source-field-map-review-route-pack.json"
SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK = (
    STAT_DIR / "112_ai-agent-source-package-manifest-review-route-pack.json"
)
SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK = (
    STAT_DIR / "113_ai-agent-source-access-boundary-review-route-pack.json"
)
SOURCE_CHECKSUM_REVIEW_ROUTE_PACK = STAT_DIR / "114_ai-agent-source-checksum-review-route-pack.json"
SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK = (
    STAT_DIR / "115_ai-agent-source-metadata-profile-review-route-pack.json"
)
SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK = (
    STAT_DIR / "116_ai-agent-source-safe-derived-record-review-route-pack.json"
)
SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY = (
    STAT_DIR / "117_ai-agent-source-engineering-review-route-summary.json"
)
SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD = (
    STAT_DIR / "118_ai-agent-source-engineering-review-wave-handoff-scaffold.json"
)
SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS = (
    STAT_DIR / "119_ai-agent-source-engineering-first-wave-review-results.csv"
)
SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST = (
    STAT_DIR / "120_ai-agent-source-engineering-first-wave-result-record-manifest.csv"
)
SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE = (
    STAT_DIR / "121_ai-agent-source-engineering-first-wave-followup-queue.csv"
)
SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS = (
    STAT_DIR / "122_ai-agent-source-engineering-first-wave-source-status.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST = (
    STAT_DIR / "123_ai-agent-source-engineering-second-wave-source-checklist.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST = (
    STAT_DIR / "124_ai-agent-source-engineering-second-wave-review-draft-manifest.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD = (
    STAT_DIR / "125_ai-agent-source-engineering-second-wave-result-scaffold.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST = (
    STAT_DIR / "126_ai-agent-source-engineering-second-wave-review-checklist.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD = (
    STAT_DIR / "127_ai-agent-source-engineering-second-wave-review-outcome-scaffold.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK = (
    STAT_DIR / "128_ai-agent-source-engineering-second-wave-outcome-route-pack.json"
)
SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD = (
    STAT_DIR / "129_ai-agent-source-engineering-second-wave-outcome-handoff-scaffold.json"
)
SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST = (
    STAT_DIR / "130_ai-agent-source-engineering-second-wave-handoff-review-checklist.csv"
)
SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "131_ai-agent-source-engineering-second-wave-handoff-route-summary.json"
)
SOURCE_PIPELINE_GAP_MATRIX = STAT_DIR / "132_ai-agent-source-pipeline-gap-matrix.csv"
SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST = STAT_DIR / "133_ai-agent-source-pipeline-gap-review-checklist.csv"
SOURCE_PIPELINE_EVIDENCE_LEDGER = STAT_DIR / "134_ai-agent-source-pipeline-evidence-ledger.csv"
CORE_CORPUS_PHASE_COVERAGE_MATRIX = STAT_DIR / "135_core-corpus-phase-coverage-matrix.csv"
SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX = STAT_DIR / "136_source-pipeline-phase-coverage-matrix.csv"
SOURCE_PIPELINE_PHASE_ACTION_QUEUE = STAT_DIR / "137_source-pipeline-phase-action-queue.csv"
SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD = STAT_DIR / "138_source-pipeline-phase-action-result-scaffold.csv"
SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY = STAT_DIR / "139_source-pipeline-phase-action-route-summary.json"
SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY = STAT_DIR / "140_source-pipeline-phase-action-source-summary.csv"
SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST = STAT_DIR / "141_source-pipeline-phase-action-file-checklist.csv"
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX = (
    STAT_DIR / "142_source-pipeline-phase-action-evidence-presence-matrix.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY = (
    STAT_DIR / "143_source-pipeline-phase-action-evidence-gap-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE = (
    STAT_DIR / "144_source-pipeline-phase-action-missing-evidence-action-queue.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD = (
    STAT_DIR / "145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY = (
    STAT_DIR / "146_source-pipeline-phase-action-missing-evidence-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY = (
    STAT_DIR / "147_source-pipeline-phase-action-missing-evidence-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST = (
    STAT_DIR / "148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD = (
    STAT_DIR / "149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST = (
    STAT_DIR / "150_source-pipeline-phase-action-missing-evidence-review-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK = (
    STAT_DIR / "151_source-pipeline-phase-action-missing-evidence-review-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD = (
    STAT_DIR / "152_source-pipeline-phase-action-missing-evidence-review-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST = (
    STAT_DIR / "153_source-pipeline-phase-action-missing-evidence-review-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "154_source-pipeline-phase-action-missing-evidence-review-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD = (
    STAT_DIR / "155_source-pipeline-phase-action-missing-evidence-review-outcome-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK = (
    STAT_DIR / "156_source-pipeline-phase-action-missing-evidence-review-outcome-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD = (
    STAT_DIR / "157_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST = (
    STAT_DIR / "158_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "159_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN = (
    STAT_DIR / "160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD = (
    STAT_DIR / "161_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST = (
    STAT_DIR / "162_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "163_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN = (
    STAT_DIR / "164_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-plan.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST = (
    STAT_DIR / "165_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD = (
    STAT_DIR / "166_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY = (
    STAT_DIR / "167_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY = (
    STAT_DIR / "168_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST = (
    STAT_DIR / "169_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK = (
    STAT_DIR / "170_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-pack.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD = (
    STAT_DIR / "171_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-scaffold.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST = (
    STAT_DIR / "172_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist.csv"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_ROUTE_SUMMARY = (
    STAT_DIR / "173_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-route-summary.json"
)
SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_SCAFFOLD = (
    STAT_DIR / "174_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-scaffold.csv"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def safe_rows(root: Path, path: Path) -> list[dict[str, str]]:
    full_path = root / path
    if not full_path.exists():
        return []
    return read_csv_rows(full_path)


def count_csv(root: Path, path: Path) -> int:
    return len(safe_rows(root, path))


def count_existing_file(root: Path, path: Path) -> int:
    return 1 if (root / path).exists() else 0


def count_files(root: Path, pattern: str) -> int:
    return sum(1 for _ in root.glob(pattern))


def graph_edge_counts(root: Path) -> tuple[int, Counter[str], Counter[str]]:
    total = 0
    source_counts: Counter[str] = Counter()
    edge_type_counts: Counter[str] = Counter()
    for path in sorted((root / REL_GRAPH_DIR).glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                total += 1
                record = json.loads(line)
                edge_type_counts[record.get("edge_type", "unknown")] += 1
                for source_id in record.get("source_ids", []):
                    source_counts[source_id] += 1
    return total, source_counts, edge_type_counts


def classify_stage(
    discovered: int = 0,
    downloaded: int = 0,
    registered: int = 0,
    unpacked: int = 0,
    extracted: int = 0,
    cleaned: int = 0,
    structured: int = 0,
    linked: int = 0,
    verified: int = 0,
    review_queue: int = 0,
) -> str:
    if verified:
        return "verified"
    if review_queue:
        return "pending_human_review"
    if linked:
        return "linked"
    if structured:
        return "structured"
    if cleaned:
        return "cleaned"
    if extracted:
        return "extracted"
    if unpacked:
        return "unpacked"
    if registered:
        return "registered"
    if downloaded:
        return "downloaded"
    if discovered:
        return "discovered"
    return "not_found"


def make_row(
    area_id: str,
    area_type: str,
    label_en: str,
    label_zh: str,
    stage: str,
    counts: dict[str, int],
    next_entry: str,
    review_status: str,
    caution: str = CAUTION,
) -> dict[str, str]:
    return {
        "audit_row_id": area_id,
        "area_type": area_type,
        "label_en": label_en,
        "label_zh": label_zh,
        "current_stage": stage,
        "count_summary": ";".join(f"{key}:{counts[key]}" for key in sorted(counts)),
        "next_entry_path": next_entry,
        "review_status": review_status,
        "caution": caution,
        "updated_at": UPDATED_AT,
    }


def build_audit_rows(root: Path) -> list[dict[str, str]]:
    source_rows = safe_rows(root, SOURCE_INDEX)
    download_manifest_rows = safe_rows(root, SOURCE_DOWNLOAD_MANIFEST)
    download_log_rows = safe_rows(root, SOURCE_DOWNLOAD_LOG)
    large_rows = safe_rows(root, LARGE_SOURCE_REGISTER)
    asset_rows = safe_rows(root, ASSET_SOURCE_INDEX)
    metadata_profile_rows = safe_rows(root, DOWNLOADED_METADATA_PROFILE)
    package_manifest_rows = safe_rows(root, SOURCE_PACKAGE_FILE_MANIFEST)
    graph_total, graph_source_counts, graph_type_counts = graph_edge_counts(root)

    downloaded = sum(1 for item in download_log_rows if item.get("status", "").startswith("downloaded"))
    download_errors = len(download_log_rows) - downloaded
    review_log_files = count_files(root, "doc/public/user_research/**/*review-log*.md")
    evidence_note_files = count_files(root, "doc/public/user_research/**/*collection-note*.md")
    character_candidate_packet_count = count_files(
        root, "corpus/001_oracle-characters/**/01_candidate-character-packet.json"
    )
    undeciphered_candidate_packet_count = count_files(
        root, "corpus/001_oracle-characters/**/01_undeciphered-candidate-packet.json"
    )

    rows = [
        make_row(
            "pre-audit-001",
            "source_registry",
            "Authoritative and dataset source registry",
            "权威来源与数据集来源登记",
            classify_stage(
                discovered=len(source_rows),
                downloaded=downloaded,
                registered=len(source_rows),
                extracted=len(metadata_profile_rows),
                structured=len(package_manifest_rows),
                verified=len(source_rows),
            ),
            {
                "source_rows": len(source_rows),
                "download_manifest_rows": len(download_manifest_rows),
                "download_log_rows": len(download_log_rows),
                "downloaded_rows": downloaded,
                "download_error_or_boundary_rows": download_errors,
                "metadata_profile_rows": len(metadata_profile_rows),
                "package_manifest_rows": len(package_manifest_rows),
            },
            str(SOURCE_INDEX).replace("\\", "/"),
            "reviewed_metadata_only",
        ),
        make_row(
            "pre-audit-002",
            "large_source_register",
            "Large source packages and local-only raw archives",
            "大型来源包与本地原始归档",
            classify_stage(
                discovered=len(large_rows),
                registered=len(large_rows),
                downloaded=sum(1 for item in large_rows if item.get("storage_status", "").startswith("downloaded")),
                extracted=sum(1 for item in large_rows if item.get("derived_record_paths")),
                verified=len(large_rows),
            ),
            {
                "large_source_rows": len(large_rows),
                "downloaded_large_source_rows": sum(
                    1 for item in large_rows if item.get("storage_status", "").startswith("downloaded")
                ),
                "not_downloaded_registered_rows": sum(
                    1 for item in large_rows if item.get("storage_status") == "not_downloaded_registered"
                ),
            },
            str(LARGE_SOURCE_REGISTER).replace("\\", "/"),
            "reviewed_metadata_only",
        ),
        make_row(
            "pre-audit-003",
            "oracle_character_candidates",
            "HUST-OBC deciphered-class candidate packets",
            "HUST-OBC 已释类别候选包",
            classify_stage(
                discovered=count_csv(root, HUST_VALIDATION_STAGING),
                extracted=count_csv(root, HUST_LABEL_CROSSWALK),
                structured=character_candidate_packet_count,
                linked=count_csv(root, HUST_CODEPOINT_CROSSWALK),
                review_queue=count_csv(root, HUST_PROMOTION_QUEUE),
            ),
            {
                "validation_class_rows": count_csv(root, HUST_VALIDATION_STAGING),
                "label_crosswalk_rows": count_csv(root, HUST_LABEL_CROSSWALK),
                "source_category_rows": count_csv(root, HUST_SOURCE_CATEGORY),
                "promotion_review_queue_rows": count_csv(root, HUST_PROMOTION_QUEUE),
                "candidate_character_packet_json_files": character_candidate_packet_count,
                "accepted_character_index_rows": count_csv(root, ACCEPTED_CHAR_INDEX),
            },
            str(HUST_PROMOTION_QUEUE).replace("\\", "/"),
            "candidate_not_promoted",
        ),
        make_row(
            "pre-audit-004",
            "undeciphered_character_candidates",
            "HUST-OBC undeciphered candidate packets",
            "HUST-OBC 未释字候选包",
            classify_stage(
                discovered=count_csv(root, UNDECIPHERED_INDEX),
                unpacked=count_csv(root, UNDECIPHERED_INDEX),
                extracted=count_csv(root, UNDECIPHERED_INDEX),
                structured=count_csv(root, UNDECIPHERED_INDEX),
                review_queue=count_csv(root, STAT_DIR / "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"),
            ),
            {
                "undeciphered_index_rows": count_csv(root, UNDECIPHERED_INDEX),
                "review_queue_rows": count_csv(root, STAT_DIR / "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"),
                "review_log_draft_rows": count_csv(root, STAT_DIR / "052_ai-agent-hust-obc-undeciphered-candidate-review-log-draft-manifest.csv"),
                "source_image_reference_rows": count_csv(root, STAT_DIR / "068_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-results.csv"),
                "undeciphered_candidate_packet_json_files": undeciphered_candidate_packet_count,
            },
            str(UNDECIPHERED_INDEX).replace("\\", "/"),
            "candidate_not_promoted",
        ),
        make_row(
            "pre-audit-005",
            "components_and_glyph_links",
            "OBIMD component and glyph-codepoint staging",
            "OBIMD 构件与字形码位暂存",
            classify_stage(
                discovered=count_csv(root, OBIMD_MAIN_STAGING),
                extracted=graph_source_counts["src-obimd"],
                structured=count_csv(root, OBIMD_MAIN_STAGING),
                linked=graph_source_counts["src-obimd"],
                review_queue=count_files(root, "doc/public/user_research/002_cross-source-review-queues/obimd/*.md"),
            ),
            {
                "obimd_main_character_rows": count_csv(root, OBIMD_MAIN_STAGING),
                "obimd_graph_edges": graph_source_counts["src-obimd"],
                "obimd_cross_review_logs": count_files(root, "doc/public/user_research/002_cross-source-review-queues/obimd/*.md"),
            },
            "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
            "candidate_graph_edges",
        ),
        make_row(
            "pre-audit-006",
            "evolution_correspondence_candidates",
            "EVOBC evolution and era/source code staging",
            "EVOBC 字形演化与时代/来源码暂存",
            classify_stage(
                discovered=graph_source_counts["src-evobc"],
                extracted=graph_source_counts["src-evobc"],
                structured=graph_type_counts["EVOBC_CATEGORY_HAS_ERA_CODE"],
                linked=graph_source_counts["src-evobc"],
                review_queue=count_files(root, "doc/public/user_research/002_cross-source-review-queues/evobc/*.md"),
            ),
            {
                "evobc_graph_edges": graph_source_counts["src-evobc"],
                "era_code_edges": graph_type_counts["EVOBC_CATEGORY_HAS_ERA_CODE"],
                "source_code_edges": graph_type_counts["EVOBC_CATEGORY_HAS_SOURCE_CODE"],
                "evobc_cross_review_logs": count_files(root, "doc/public/user_research/002_cross-source-review-queues/evobc/*.md"),
            },
            "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl",
            "candidate_graph_edges",
        ),
        make_row(
            "pre-audit-007",
            "inscription_and_collection_staging",
            "Inscription, plate, and collection provenance staging",
            "卜辞、图版与馆藏出处暂存",
            classify_stage(
                discovered=count_csv(root, INSCRIPTION_ID_MAP),
                extracted=count_csv(root, STAT_DIR / "085_ai-agent-xxt-obm-access-boundary-capture-results.csv"),
                structured=count_files(root, "corpus/002_oracle-bone-inscriptions/**/*"),
                review_queue=count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE)
                + count_files(root, "doc/public/user_research/008_xxt-obm-access-boundary-review-queues/**/*.md"),
            ),
            {
                "formal_inscription_id_map_rows": count_csv(root, INSCRIPTION_ID_MAP),
                "cambridge_hopkins_graph_edges": graph_source_counts["src-cambridge-hopkins"],
                "cambridge_hopkins_crosswalk_review_queue_rows": count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE),
                "xxt_obm_access_capture_rows": count_csv(root, STAT_DIR / "085_ai-agent-xxt-obm-access-boundary-capture-results.csv"),
                "xxt_obm_review_logs": count_files(root, "doc/public/user_research/008_xxt-obm-access-boundary-review-queues/**/*.md"),
                "formal_inscription_record_files": count_files(root, "corpus/002_oracle-bone-inscriptions/**/*.json"),
            },
            "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/",
            "metadata_only_pending_review",
        ),
        make_row(
            "pre-audit-008",
            "assets",
            "Committed public-domain or source-marked image assets",
            "已提交的公版或来源标注图像资产",
            classify_stage(
                discovered=len(asset_rows),
                downloaded=len(asset_rows),
                registered=len(asset_rows),
                extracted=count_csv(root, ASSET_ID_MAP),
                verified=len(asset_rows),
            ),
            {
                "asset_source_rows": len(asset_rows),
                "asset_id_map_rows": count_csv(root, ASSET_ID_MAP),
                "technical_profile_rows": count_csv(
                    root, Path("project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv")
                ),
                "visual_profile_rows": count_csv(
                    root, Path("project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv")
                ),
            },
            str(ASSET_SOURCE_INDEX).replace("\\", "/"),
            "reviewed_assets_only",
        ),
        make_row(
            "pre-audit-009",
            "relationship_graph",
            "Candidate relationship graph edges and summaries",
            "候选关系图边与统计",
            classify_stage(
                discovered=graph_total,
                structured=graph_total,
                linked=graph_total,
                verified=count_csv(root, STAT_DIR / "001_relationship-graph-edge-type-summary.csv"),
            ),
            {
                "graph_edge_rows": graph_total,
                "edge_type_count": len(graph_type_counts),
                "edge_type_summary_rows": count_csv(root, STAT_DIR / "001_relationship-graph-edge-type-summary.csv"),
                "node_degree_summary_rows": count_csv(root, STAT_DIR / "002_relationship-graph-node-degree-summary.csv"),
            },
            "corpus/008_relationship-graph/",
            "candidate_graph_edges",
        ),
        make_row(
            "pre-audit-010",
            "review_queues",
            "AI/user review queues and evidence collection drafts",
            "AI/用户复核队列与证据收集草稿",
            classify_stage(
                discovered=review_log_files
                + count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_GAP_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_EXECUTION_MATRIX)
                + count_csv(root, SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT)
                + count_csv(root, SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_ENGINEERING_LANE_ROUTE_PACK)
                + count_csv(root, SOURCE_FIELD_MAP_SCAFFOLD)
                + count_csv(root, SOURCE_FIELD_MAP_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_CHECKSUM_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_GAP_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_EVIDENCE_LEDGER)
                + count_csv(root, CORE_CORPUS_PHASE_COVERAGE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_QUEUE)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD),
                structured=review_log_files
                + evidence_note_files
                + count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_GAP_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_EXECUTION_MATRIX)
                + count_csv(root, SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT)
                + count_csv(root, SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_ENGINEERING_LANE_ROUTE_PACK)
                + count_csv(root, SOURCE_FIELD_MAP_SCAFFOLD)
                + count_csv(root, SOURCE_FIELD_MAP_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_CHECKSUM_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_GAP_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_EVIDENCE_LEDGER)
                + count_csv(root, CORE_CORPUS_PHASE_COVERAGE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_QUEUE)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD),
                review_queue=review_log_files
                + evidence_note_files
                + count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_GAP_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_EXECUTION_MATRIX)
                + count_csv(root, SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT)
                + count_csv(root, SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_ENGINEERING_LANE_ROUTE_PACK)
                + count_csv(root, SOURCE_FIELD_MAP_SCAFFOLD)
                + count_csv(root, SOURCE_FIELD_MAP_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_CHECKSUM_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE)
                + count_csv(root, SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST)
                + count_existing_file(root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_GAP_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_EVIDENCE_LEDGER)
                + count_csv(root, SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX)
                + count_csv(root, CORE_CORPUS_PHASE_COVERAGE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_QUEUE)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST)
                + count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_ROUTE_SUMMARY)
                + count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_SCAFFOLD),
            ),
            {
                "review_log_files": review_log_files,
                "evidence_collection_note_files": evidence_note_files,
                "codepoint_review_queue_rows": count_csv(root, STAT_DIR / "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"),
                "undeciphered_review_queue_rows": count_csv(root, STAT_DIR / "051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv"),
                "cambridge_hopkins_crosswalk_review_queue_rows": count_csv(root, CAMBRIDGE_HOPKINS_REVIEW_QUEUE),
                "source_engineering_gap_queue_rows": count_csv(root, SOURCE_ENGINEERING_GAP_QUEUE),
                "source_engineering_execution_matrix_rows": count_csv(root, SOURCE_ENGINEERING_EXECUTION_MATRIX),
                "source_engineering_gap_review_log_draft_rows": count_csv(
                    root, SOURCE_ENGINEERING_GAP_REVIEW_LOG_DRAFT_MANIFEST
                ),
                "source_engineering_gap_evidence_snapshot_rows": count_csv(
                    root, SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT
                ),
                "source_engineering_next_action_checklist_rows": count_csv(
                    root, SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST
                ),
                "source_engineering_next_action_result_scaffold_rows": count_csv(
                    root, SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD
                ),
                "source_engineering_lane_route_pack_files": count_existing_file(
                    root, SOURCE_ENGINEERING_LANE_ROUTE_PACK
                ),
                "source_field_map_scaffold_rows": count_csv(root, SOURCE_FIELD_MAP_SCAFFOLD),
                "source_field_map_review_checklist_rows": count_csv(
                    root, SOURCE_FIELD_MAP_REVIEW_CHECKLIST
                ),
                "source_field_map_review_result_scaffold_rows": count_csv(
                    root, SOURCE_FIELD_MAP_REVIEW_RESULT_SCAFFOLD
                ),
                "source_field_map_review_route_pack_files": count_existing_file(
                    root, SOURCE_FIELD_MAP_REVIEW_ROUTE_PACK
                ),
                "source_package_manifest_review_route_pack_files": count_existing_file(
                    root, SOURCE_PACKAGE_MANIFEST_REVIEW_ROUTE_PACK
                ),
                "source_access_boundary_review_route_pack_files": count_existing_file(
                    root, SOURCE_ACCESS_BOUNDARY_REVIEW_ROUTE_PACK
                ),
                "source_checksum_review_route_pack_files": count_existing_file(
                    root, SOURCE_CHECKSUM_REVIEW_ROUTE_PACK
                ),
                "source_metadata_profile_review_route_pack_files": count_existing_file(
                    root, SOURCE_METADATA_PROFILE_REVIEW_ROUTE_PACK
                ),
                "source_safe_derived_record_review_route_pack_files": count_existing_file(
                    root, SOURCE_SAFE_DERIVED_RECORD_REVIEW_ROUTE_PACK
                ),
                "source_engineering_review_route_summary_files": count_existing_file(
                    root, SOURCE_ENGINEERING_REVIEW_ROUTE_SUMMARY
                ),
                "source_engineering_review_wave_handoff_scaffold_files": count_existing_file(
                    root, SOURCE_ENGINEERING_REVIEW_WAVE_HANDOFF_SCAFFOLD
                ),
                "source_engineering_first_wave_review_result_rows": count_csv(
                    root, SOURCE_ENGINEERING_FIRST_WAVE_REVIEW_RESULTS
                ),
                "source_engineering_first_wave_result_record_manifest_rows": count_csv(
                    root, SOURCE_ENGINEERING_FIRST_WAVE_RESULT_RECORD_MANIFEST
                ),
                "source_engineering_first_wave_followup_queue_rows": count_csv(
                    root, SOURCE_ENGINEERING_FIRST_WAVE_FOLLOWUP_QUEUE
                ),
                "source_engineering_first_wave_source_status_rows": count_csv(
                    root, SOURCE_ENGINEERING_FIRST_WAVE_SOURCE_STATUS
                ),
                "source_engineering_second_wave_source_checklist_rows": count_csv(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_SOURCE_CHECKLIST
                ),
                "source_engineering_second_wave_review_draft_manifest_rows": count_csv(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_DRAFT_MANIFEST
                ),
                "source_engineering_second_wave_result_scaffold_rows": count_csv(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_RESULT_SCAFFOLD
                ),
                "source_engineering_second_wave_review_checklist_rows": count_csv(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_CHECKLIST
                ),
                "source_engineering_second_wave_review_outcome_scaffold_rows": count_csv(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD
                ),
                "source_engineering_second_wave_outcome_route_pack_files": count_existing_file(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_ROUTE_PACK
                ),
                "source_engineering_second_wave_outcome_handoff_scaffold_files": count_existing_file(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_OUTCOME_HANDOFF_SCAFFOLD
                ),
                "source_engineering_second_wave_handoff_review_checklist_rows": count_csv(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST
                ),
                "source_engineering_second_wave_handoff_route_summary_files": count_existing_file(
                    root, SOURCE_ENGINEERING_SECOND_WAVE_HANDOFF_ROUTE_SUMMARY
                ),
                "source_pipeline_gap_matrix_rows": count_csv(root, SOURCE_PIPELINE_GAP_MATRIX),
                "source_pipeline_gap_review_checklist_rows": count_csv(root, SOURCE_PIPELINE_GAP_REVIEW_CHECKLIST),
                "source_pipeline_evidence_ledger_rows": count_csv(root, SOURCE_PIPELINE_EVIDENCE_LEDGER),
                "core_corpus_phase_coverage_rows": count_csv(root, CORE_CORPUS_PHASE_COVERAGE_MATRIX),
                "source_pipeline_phase_coverage_rows": count_csv(root, SOURCE_PIPELINE_PHASE_COVERAGE_MATRIX),
                "source_pipeline_phase_action_queue_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_QUEUE),
                "source_pipeline_phase_action_result_scaffold_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_RESULT_SCAFFOLD),
                "source_pipeline_phase_action_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_ROUTE_SUMMARY),
                "source_pipeline_phase_action_source_summary_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY),
                "source_pipeline_phase_action_file_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_FILE_CHECKLIST),
                "source_pipeline_phase_action_evidence_presence_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_PRESENCE_MATRIX),
                "source_pipeline_phase_action_evidence_gap_summary_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_EVIDENCE_GAP_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_action_queue_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ACTION_QUEUE),
                "source_pipeline_phase_action_missing_evidence_result_scaffold_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_RESULT_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_ROUTE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_source_summary_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_SOURCE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_draft_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_DRAFT_MANIFEST),
                "source_pipeline_phase_action_missing_evidence_review_result_scaffold_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_RESULT_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_route_pack_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_ROUTE_PACK),
                "source_pipeline_phase_action_missing_evidence_review_handoff_scaffold_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_handoff_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_handoff_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_HANDOFF_ROUTE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_outcome_scaffold_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_outcome_route_pack_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ROUTE_PACK),
                "source_pipeline_phase_action_missing_evidence_review_outcome_handoff_scaffold_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_outcome_handoff_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_outcome_handoff_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_HANDOFF_ROUTE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_outcome_assignment_plan_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_ASSIGNMENT_PLAN),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_scaffold_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ROUTE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_plan_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_PLAN),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_scaffold_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_ROUTE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_summary_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_route_pack_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_ROUTE_PACK),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_scaffold_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_SCAFFOLD),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_checklist_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_CHECKLIST),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_route_summary_files": count_existing_file(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_ROUTE_SUMMARY),
                "source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_handoff_outcome_scaffold_rows": count_csv(root, SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_OUTCOME_WAVE_HANDOFF_ASSIGNMENT_OUTCOME_SOURCE_HANDOFF_OUTCOME_SCAFFOLD),
            },
            "doc/public/user_research/",
            "pending_human_review",
        ),
        make_row(
            "pre-audit-011",
            "formal_project_id_maps",
            "Formal project-local ID maps",
            "正式本项目 ID 映射表",
            classify_stage(
                registered=count_csv(root, ASSET_ID_MAP),
                structured=count_csv(root, CHAR_ID_MAP)
                + count_csv(root, INSCRIPTION_ID_MAP)
                + count_csv(root, ASSET_ID_MAP)
                + count_csv(root, COMPONENT_ID_MAP),
            ),
            {
                "formal_character_map_rows": count_csv(root, CHAR_ID_MAP),
                "formal_inscription_map_rows": count_csv(root, INSCRIPTION_ID_MAP),
                "formal_asset_map_rows": count_csv(root, ASSET_ID_MAP),
                "formal_component_map_rows": count_csv(root, COMPONENT_ID_MAP),
            },
            "project_registry/002_project-id-to-source-reference-map/",
            "mostly_unassigned_by_design",
        ),
    ]
    return rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    stage_counts = Counter(row["current_stage"] for row in rows)
    area_type_counts = Counter(row["area_type"] for row in rows)
    return {
        "summary_id": "preprocessing-status-summary-001",
        "updated_at": UPDATED_AT,
        "audit_csv_path": str(OUTPUT_CSV).replace("\\", "/"),
        "row_count": len(rows),
        "stage_counts": dict(sorted(stage_counts.items())),
        "area_type_counts": dict(sorted(area_type_counts.items())),
        "completion_boundary": (
            "This summary describes preprocessing infrastructure readiness only. "
            "It does not start formal decipherment research or confirm candidate identities."
        ),
        "caution": CAUTION,
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    parser.add_argument("--json-output", default=str(OUTPUT_JSON))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_audit_rows(root)
    write_csv(root / args.csv_output, rows)
    write_json(root / args.json_output, build_summary(rows))
    print(f"preprocessing_audit_rows={len(rows)} csv={args.csv_output} json={args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
