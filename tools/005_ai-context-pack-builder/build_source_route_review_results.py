#!/usr/bin/env python3
"""Build reviewed metadata-only source-route review results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_ROUTE_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv"
)
SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/010_ai-agent-source-route-review-result-scaffold.csv"
)
SOURCE_ROUTE_REVIEW_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/011_ai-agent-source-route-review-results.csv"
)
SOURCE_COVERAGE_SUMMARY = Path("corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv")
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
HUST_OBC_OBS_CHAR_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"
)
AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
HUST_OBC_CANDIDATE_GRAPH_EDGES = Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl")
OBIMD_COMPONENT_GRAPH_EDGES = Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl")
EVOBC_EVOLUTION_GRAPH_EDGES = Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")

TARGET_SOURCE_IDS = ["src-hust-obc", "src-evobc", "src-obimd"]
GRAPH_EDGE_FILES_BY_SOURCE = {
    "src-hust-obc": HUST_OBC_CANDIDATE_GRAPH_EDGES,
    "src-evobc": EVOBC_EVOLUTION_GRAPH_EDGES,
    "src-obimd": OBIMD_COMPONENT_GRAPH_EDGES,
}
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "source_route_review_metadata_only_not_scholarship"
OUTPUT_SCOPE = "source_route_review_result_only"
CAUTION = (
    "This is a metadata-only source-route review result. It is not source evidence by itself, "
    "not a decipherment result, not a character/component/evolution-chain assignment, not a "
    "rights clearance, and does not promote raw images, dataset labels, graph edges, or staging "
    "rows into scholarship."
)

OUTPUT_FIELDS = [
    "source_route_result_id",
    "source_route_task_id",
    "context_pack_id",
    "source_id",
    "priority_tags",
    "review_focus",
    "result_status",
    "source_register_review_status",
    "route_file_review_status",
    "rights_and_risk_review_status",
    "size_checksum_review_status",
    "derivative_promotion_status",
    "evidence_gap_status",
    "source_index_row_count",
    "metadata_profile_metric_count",
    "download_log_count",
    "source_package_file_manifest_count",
    "candidate_queue_count",
    "evidence_request_count",
    "graph_edge_count",
    "raw_package_file_size_bytes",
    "raw_package_commit_policy",
    "rights_status",
    "source_review_status",
    "route_files_opened",
    "review_basis_files",
    "next_artifact_recommendation",
    "research_boundary",
    "output_scope",
    "review_note",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_jsonl_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as file:
        return sum(1 for line in file if line.strip())


def _one(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one row where {key}={value}, found {len(matches)}")
    return matches[0]


def _source_rows(rows: list[dict[str, str]], source_id: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("source_id") == source_id]


def _primary_package_row(rows: list[dict[str, str]], source_id: str) -> dict[str, str]:
    source_rows = _source_rows(rows, source_id)
    if not source_rows:
        return {}
    return max(source_rows, key=lambda row: int(row.get("file_size_bytes") or "0"))


def _size_checksum_review_status(package_rows: list[dict[str, str]]) -> str:
    if not package_rows:
        return "not_applicable_no_package_manifest_rows"
    if any(row.get("commit_policy") == "do_not_commit_regular_git" for row in package_rows):
        return "raw_package_over_git_limit_manifested"
    return "downloaded_metadata_files_logged_tmp_only"


def _candidate_queue_count(source_id: str, promotion_queue_rows: list[dict[str, str]]) -> int:
    if source_id != "src-hust-obc":
        return 0
    return len(promotion_queue_rows)


def _evidence_request_count(source_id: str, evidence_request_rows: list[dict[str, str]]) -> int:
    if source_id != "src-hust-obc":
        return 0
    return len(evidence_request_rows)


def _next_artifact_recommendation(source_id: str) -> str:
    recommendations = {
        "src-hust-obc": "open_first_hust_obc_candidate_or_bucket_route_for_cross_source_review",
        "src-evobc": "open_first_evobc_evolution_category_route_for_cross_source_review",
        "src-obimd": "open_first_obimd_component_or_glyph_route_for_cross_source_review",
    }
    return recommendations[source_id]


def _review_note(source_id: str) -> str:
    notes = {
        "src-hust-obc": (
            "Metadata-only review confirms the HUST-OBC source-route files and derived counts "
            "are internally consistent. HUST dataset labels remain candidates, and raw images "
            "or the raw zip are not promoted."
        ),
        "src-evobc": (
            "Metadata-only review confirms the EVOBC source-route files and derived counts are "
            "internally consistent. EVOBC category, era-code, and source-code graph edges remain "
            "dataset metadata; raw images and large JSON files are not promoted."
        ),
        "src-obimd": (
            "Metadata-only review confirms the OBIMD source-route files and derived counts are "
            "internally consistent. OBIMD main-character, subcharacter, and glyph-codepoint graph "
            "edges remain dataset metadata; raw annotation and image packages are not promoted."
        ),
    }
    return notes[source_id]


def build_review_rows(
    queue_rows: list[dict[str, str]],
    scaffold_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    source_index_rows: list[dict[str, str]],
    metadata_profile_rows: list[dict[str, str]],
    download_log_rows: list[dict[str, str]],
    package_file_rows: list[dict[str, str]],
    promotion_queue_rows: list[dict[str, str]],
    evidence_request_rows: list[dict[str, str]],
    graph_edge_counts: dict[str, int],
    root: Path | None = None,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id in TARGET_SOURCE_IDS:
        queue_row = _one(queue_rows, "source_id", source_id)
        scaffold_row = _one(scaffold_rows, "source_id", source_id)
        coverage_row = _one(coverage_rows, "source_id", source_id)
        source_index_row = _one(source_index_rows, "source_id", source_id)
        metadata_rows = _source_rows(metadata_profile_rows, source_id)
        download_rows = _source_rows(download_log_rows, source_id)
        package_rows = _source_rows(package_file_rows, source_id)
        primary_package = _primary_package_row(package_file_rows, source_id)
        route_files = scaffold_row["route_files_to_open"]
        route_file_list = [value for value in route_files.split(";") if value]
        route_files_exist = True
        if root is not None:
            route_files_exist = all((root / value).exists() for value in route_file_list)

        rows.append(
            {
                "source_route_result_id": scaffold_row["source_route_result_id"],
                "source_route_task_id": queue_row["source_route_task_id"],
                "context_pack_id": queue_row["context_pack_id"],
                "source_id": source_id,
                "priority_tags": queue_row["priority_tags"],
                "review_focus": queue_row["review_focus"],
                "result_status": "reviewed_metadata_routes_only",
                "source_register_review_status": "reviewed_metadata_only",
                "route_file_review_status": (
                    "reviewed_route_files_exist" if route_files_exist else "route_files_missing"
                ),
                "rights_and_risk_review_status": coverage_row["rights_status"],
                "size_checksum_review_status": _size_checksum_review_status(package_rows),
                "derivative_promotion_status": "no_raw_asset_or_dataset_claim_promotion",
                "evidence_gap_status": "needs_cross_source_review_before_evidence_pack",
                "source_index_row_count": "1",
                "metadata_profile_metric_count": str(len(metadata_rows)),
                "download_log_count": str(len(download_rows)),
                "source_package_file_manifest_count": str(len(package_rows)),
                "candidate_queue_count": str(_candidate_queue_count(source_id, promotion_queue_rows)),
                "evidence_request_count": str(_evidence_request_count(source_id, evidence_request_rows)),
                "graph_edge_count": str(graph_edge_counts[source_id]),
                "raw_package_file_size_bytes": primary_package.get("file_size_bytes", ""),
                "raw_package_commit_policy": primary_package.get("commit_policy", ""),
                "rights_status": source_index_row["rights_status"],
                "source_review_status": source_index_row["review_status"],
                "route_files_opened": route_files,
                "review_basis_files": route_files,
                "next_artifact_recommendation": _next_artifact_recommendation(source_id),
                "research_boundary": RESEARCH_BOUNDARY,
                "output_scope": OUTPUT_SCOPE,
                "review_note": _review_note(source_id),
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-route-queue", default=str(SOURCE_ROUTE_REVIEW_QUEUE))
    parser.add_argument("--result-scaffold", default=str(SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD))
    parser.add_argument("--source-coverage-summary", default=str(SOURCE_COVERAGE_SUMMARY))
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--metadata-profile", default=str(DOWNLOADED_METADATA_PROFILE))
    parser.add_argument("--source-download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--source-package-file-manifest", default=str(SOURCE_PACKAGE_FILE_MANIFEST))
    parser.add_argument("--promotion-queue", default=str(HUST_OBC_OBS_CHAR_PROMOTION_QUEUE))
    parser.add_argument("--evidence-request-queue", default=str(AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE))
    parser.add_argument("--graph-edges", default=str(HUST_OBC_CANDIDATE_GRAPH_EDGES))
    parser.add_argument("--output", default=str(SOURCE_ROUTE_REVIEW_RESULTS))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_rows(
        read_csv_rows(root / args.source_route_queue),
        read_csv_rows(root / args.result_scaffold),
        read_csv_rows(root / args.source_coverage_summary),
        read_csv_rows(root / args.source_index),
        read_csv_rows(root / args.metadata_profile),
        read_csv_rows(root / args.source_download_log),
        read_csv_rows(root / args.source_package_file_manifest),
        read_csv_rows(root / args.promotion_queue),
        read_csv_rows(root / args.evidence_request_queue),
        {
            source_id: read_jsonl_count(root / graph_file)
            for source_id, graph_file in GRAPH_EDGE_FILES_BY_SOURCE.items()
        },
        root=root,
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
