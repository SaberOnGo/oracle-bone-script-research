#!/usr/bin/env python3
"""Build empty result scaffolds for source-route review tasks."""

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
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "review_result_scaffold_not_scholarship"
CAUTION = (
    "This row is an empty source-route review result scaffold only. "
    "All review sections remain not_collected until an agent opens the cited route files. "
    "Do not use it as source evidence, a rights decision, a promotion decision, "
    "or a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "source_route_result_id",
    "source_route_task_id",
    "context_pack_id",
    "source_id",
    "priority_tags",
    "review_focus",
    "route_files_to_open",
    "required_next_checks",
    "result_status",
    "source_register_review_status",
    "route_file_review_status",
    "rights_and_risk_review_status",
    "size_checksum_review_status",
    "derivative_promotion_status",
    "evidence_gap_status",
    "next_artifact_recommendation",
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


def build_result_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(queue_rows, start=1):
        rows.append(
            {
                "source_route_result_id": f"source-route-result-{index:03d}",
                "source_route_task_id": row["source_route_task_id"],
                "context_pack_id": row["context_pack_id"],
                "source_id": row["source_id"],
                "priority_tags": row["priority_tags"],
                "review_focus": row["review_focus"],
                "route_files_to_open": row["route_files"],
                "required_next_checks": row["required_next_checks"],
                "result_status": "not_started",
                "source_register_review_status": "not_collected",
                "route_file_review_status": "not_collected",
                "rights_and_risk_review_status": "not_collected",
                "size_checksum_review_status": "not_collected",
                "derivative_promotion_status": "not_decided",
                "evidence_gap_status": "not_collected",
                "next_artifact_recommendation": "not_collected",
                "research_boundary": RESEARCH_BOUNDARY,
                "output_scope": "source_route_review_scaffold_only",
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
    parser.add_argument("--output", default=str(SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_rows(read_csv_rows(root / args.source_route_queue))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
