#!/usr/bin/env python3
"""Build not-collected evidence-collection tasks from cross-source review results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/014_ai-agent-graph-source-cross-review-log-draft-manifest.csv"
)
GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/015_ai-agent-graph-source-cross-review-log-results.csv"
)
GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/016_ai-agent-graph-source-evidence-collection-task-queue.csv"
)

UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "evidence_collection_task_queue_not_scholarship"
OUTPUT_SCOPE = "route_to_future_evidence_collection_only"
CAUTION = (
    "This row is an evidence-collection task only. It is not collected evidence, not a rights "
    "decision, not a promotion decision, not a component or evolution-chain assignment, and "
    "not a decipherment conclusion."
)

SECTION_SCOPES = {
    "source_register": "collect_source_register_rows_for_primary_and_counter_sources",
    "download_log": "collect_download_log_rows_and_access_or_checksum_notes",
    "package_manifest": "collect_package_manifest_rows_and_commit_policy_notes",
    "metadata_profile": "collect_metadata_profile_metrics_and_cautions",
    "graph_edges": "collect_graph_edge_rows_or_counts_as_metadata_only",
    "staging_row": "collect_candidate_or_staging_rows_for_primary_record",
    "counter_source_lookup": "collect_counter_source_lookup_plan_without_claiming_identity",
    "rights_risk_review": "collect_rights_risk_and_size_boundary_notes",
    "review_log": "collect_human_or_agent_review_log_notes_under_user_research",
}

OUTPUT_FIELDS = [
    "evidence_collection_task_id",
    "cross_review_result_id",
    "draft_log_id",
    "cross_review_log_id",
    "cross_review_task_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "target_evidence_section",
    "collection_scope",
    "route_files_to_open",
    "counter_source_ids_to_check",
    "expected_output_path",
    "route_file_count",
    "prerequisite_status",
    "task_status",
    "evidence_collection_status",
    "promotion_status",
    "research_boundary",
    "output_scope",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _source_slug(source_id: str) -> str:
    if source_id == "src-hust-obc":
        return "hust-obc"
    if source_id == "src-evobc":
        return "evobc"
    if source_id == "src-obimd":
        return "obimd"
    raise ValueError(f"unsupported source_id: {source_id}")


def _section_slug(section: str) -> str:
    return section.replace("_", "-")


def _one(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one row where {key}={value}, found {len(matches)}")
    return matches[0]


def _route_files_for_section(draft_row: dict[str, str], result_row: dict[str, str], section: str) -> list[str]:
    route_files = _split_compact(draft_row["route_files_to_open"])
    if section == "source_register":
        return [path for path in route_files if path.endswith("001_all-sources-index.csv")]
    if section == "download_log":
        return [path for path in route_files if path.endswith("002_source-download-log.csv")]
    if section == "package_manifest":
        return [path for path in route_files if path.endswith("009_source-package-file-manifest.csv")]
    if section == "metadata_profile":
        return [path for path in route_files if path.endswith("010_downloaded-metadata-profile.csv")]
    if section == "graph_edges":
        return [path for path in route_files if path.startswith("corpus/008_relationship-graph/")]
    if section == "staging_row":
        return [
            path
            for path in route_files
            if (
                "staging.csv" in path
                or "promotion-review-queue.csv" in path
                or "promotion-bucket-manifest.csv" in path
                or "evidence-pack-request-queue.csv" in path
            )
        ]
    if section == "counter_source_lookup":
        return [path for path in route_files if path.endswith("001_all-sources-index.csv")]
    if section == "rights_risk_review":
        return [
            path
            for path in route_files
            if (
                path.endswith("001_all-sources-index.csv")
                or path.endswith("010_downloaded-metadata-profile.csv")
                or path.endswith("002_source-download-log.csv")
                or path.endswith("009_source-package-file-manifest.csv")
            )
        ]
    if section == "review_log":
        return [
            GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS.as_posix(),
            draft_row["draft_log_path"],
        ]
    raise ValueError(f"unsupported evidence section: {section}")


def _expected_output_path(source_id: str, task_id: str, section: str) -> str:
    return (
        "doc/public/user_research/003_evidence-collection-tasks/"
        f"{_source_slug(source_id)}/{task_id}_{_section_slug(section)}_collection-note.md"
    )


def _prerequisite_status(result_row: dict[str, str]) -> str:
    required = {
        "route_file_review_status": "reviewed_route_files_exist",
        "counter_source_lookup_status": "reviewed_all_required_counter_sources_registered",
        "promotion_decision_status": "not_promoted",
    }
    if all(result_row.get(key) == value for key, value in required.items()):
        return "ready_from_015_metadata_review"
    return "blocked_pending_route_review"


def build_task_rows(
    draft_rows: list[dict[str, str]],
    result_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    task_index = 1
    for draft_row in draft_rows:
        result_row = _one(result_rows, "draft_log_id", draft_row["draft_log_id"])
        sections = _split_compact(draft_row["required_evidence_sections"])
        for section in sections:
            task_id = f"graph-source-evidence-task-{task_index:03d}"
            route_files = _route_files_for_section(draft_row, result_row, section)
            rows.append(
                {
                    "evidence_collection_task_id": task_id,
                    "cross_review_result_id": result_row["cross_review_result_id"],
                    "draft_log_id": draft_row["draft_log_id"],
                    "cross_review_log_id": draft_row["cross_review_log_id"],
                    "cross_review_task_id": draft_row["cross_review_task_id"],
                    "source_id": draft_row["source_id"],
                    "primary_review_record_id": draft_row["primary_review_record_id"],
                    "primary_external_ref_id": draft_row["primary_external_ref_id"],
                    "source_record_id": draft_row["source_record_id"],
                    "target_evidence_section": section,
                    "collection_scope": SECTION_SCOPES[section],
                    "route_files_to_open": ";".join(route_files),
                    "counter_source_ids_to_check": draft_row["required_counter_source_ids"],
                    "expected_output_path": _expected_output_path(draft_row["source_id"], task_id, section),
                    "route_file_count": str(len(route_files)),
                    "prerequisite_status": _prerequisite_status(result_row),
                    "task_status": "not_started",
                    "evidence_collection_status": "not_collected",
                    "promotion_status": "not_promoted",
                    "research_boundary": RESEARCH_BOUNDARY,
                    "output_scope": OUTPUT_SCOPE,
                    "caution": CAUTION,
                    "updated_at": UPDATED_AT,
                }
            )
            task_index += 1
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-manifest", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST))
    parser.add_argument("--review-results", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS))
    parser.add_argument("--output", default=str(GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_task_rows(
        read_csv_rows(root / args.draft_manifest),
        read_csv_rows(root / args.review_results),
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
