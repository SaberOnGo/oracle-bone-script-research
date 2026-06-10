#!/usr/bin/env python3
"""Build empty log scaffolds for graph-source cross-review tasks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


GRAPH_SOURCE_CROSS_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/012_ai-agent-graph-source-cross-review-queue.csv"
)
GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/013_ai-agent-graph-source-cross-review-log-scaffold.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "cross_source_review_log_scaffold_not_scholarship"
OUTPUT_SCOPE = "cross_source_review_log_scaffold_only"
CAUTION = (
    "This row is an empty graph-source cross-review log scaffold only. All review sections "
    "remain not_collected until an agent opens the cited route files and records source-marked "
    "evidence. Do not use it as source evidence, a rights decision, a promotion decision, "
    "a component or evolution-chain assignment, or a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "cross_review_log_id",
    "cross_review_task_id",
    "source_route_result_id",
    "source_route_task_id",
    "context_pack_id",
    "source_id",
    "target_review_scope",
    "primary_review_record_id",
    "related_project_id",
    "primary_external_ref_id",
    "source_record_id",
    "expected_output_path",
    "route_files_to_open",
    "required_counter_source_ids",
    "required_evidence_sections",
    "result_status",
    "source_register_review_status",
    "download_log_review_status",
    "package_manifest_review_status",
    "metadata_profile_review_status",
    "graph_edge_review_status",
    "staging_row_review_status",
    "counter_source_lookup_status",
    "rights_risk_review_status",
    "review_log_status",
    "evidence_pack_draft_status",
    "promotion_decision_status",
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


def build_log_scaffold_rows(cross_review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(cross_review_rows, start=1):
        rows.append(
            {
                "cross_review_log_id": f"graph-source-cross-review-log-{index:03d}",
                "cross_review_task_id": row["cross_review_task_id"],
                "source_route_result_id": row["source_route_result_id"],
                "source_route_task_id": row["source_route_task_id"],
                "context_pack_id": row["context_pack_id"],
                "source_id": row["source_id"],
                "target_review_scope": row["target_review_scope"],
                "primary_review_record_id": row["primary_review_record_id"],
                "related_project_id": row["related_project_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_record_id": row["source_record_id"],
                "expected_output_path": row["expected_output_path"],
                "route_files_to_open": row["route_files_to_open"],
                "required_counter_source_ids": row["required_counter_source_ids"],
                "required_evidence_sections": row["required_evidence_sections"],
                "result_status": "not_started",
                "source_register_review_status": "not_collected",
                "download_log_review_status": "not_collected",
                "package_manifest_review_status": "not_collected",
                "metadata_profile_review_status": "not_collected",
                "graph_edge_review_status": "not_collected",
                "staging_row_review_status": "not_collected",
                "counter_source_lookup_status": "not_collected",
                "rights_risk_review_status": "not_collected",
                "review_log_status": "not_collected",
                "evidence_pack_draft_status": "not_started",
                "promotion_decision_status": "not_decided",
                "research_boundary": RESEARCH_BOUNDARY,
                "output_scope": OUTPUT_SCOPE,
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
    parser.add_argument("--cross-review-queue", default=str(GRAPH_SOURCE_CROSS_REVIEW_QUEUE))
    parser.add_argument("--output", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_log_scaffold_rows(read_csv_rows(root / args.cross_review_queue))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
