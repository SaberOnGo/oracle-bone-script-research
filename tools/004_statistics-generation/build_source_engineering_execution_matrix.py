#!/usr/bin/env python3
"""Build a source-level execution matrix from source-engineering gaps.

The matrix condenses the gap queue into one row per registered source so the
preprocessing stage has a clear source-by-source work surface. It is metadata
only: it does not download raw material, import corpus records, clear rights, or
promote candidate scholarship.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


SOURCE_PROCESSING_PIPELINE_AUDIT = Path(
    "corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv"
)
SOURCE_ENGINEERING_GAP_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/099_ai-agent-source-engineering-gap-queue.csv"
)
OUTPUT_CSV = Path(
    "corpus/009_statistics-and-derived-features/100_ai-agent-source-engineering-execution-matrix.csv"
)
OUTPUT_JSON = Path(
    "corpus/009_statistics-and-derived-features/101_source-engineering-execution-summary.json"
)

UPDATED_AT = "2026-06-19"
RESEARCH_BOUNDARY = "source_engineering_execution_matrix_metadata_only_not_scholarship"
COMMIT_POLICY_BOUNDARY = "metadata_review_only_raw_or_temporary_material_stays_outside_regular_git"
CAUTION = (
    "This source-engineering execution row is a preprocessing work index only. "
    "It records source-level gaps and routes for provenance, manifest, field-map, "
    "metadata-profile, and safe-derivative review; it is not rights clearance, "
    "not a corpus import, not a source promotion decision, not an identity claim, "
    "and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "source_execution_id",
    "source_id",
    "current_stage",
    "authority_tier",
    "rights_status",
    "download_status_counts",
    "gap_count",
    "highest_priority_rank",
    "gap_type_counts",
    "required_next_checks",
    "route_files_to_open",
    "expected_review_log_paths",
    "safe_derivative_route_status",
    "source_promotion_status",
    "commit_policy_boundary",
    "research_boundary",
    "review_status",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def unique_semicolon_values(rows: list[dict[str, str]], field: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for value in row.get(field, "").split(";"):
            value = value.strip()
            if value and value not in seen:
                values.append(value)
                seen.add(value)
    return values


def safe_derivative_status(source_gaps: list[dict[str, str]], pipeline_row: dict[str, str]) -> str:
    gap_types = {row.get("gap_type", "") for row in source_gaps}
    if "safe_derived_record_decision_needed" in gap_types:
        return "safe_derivative_decision_needed"
    if int(pipeline_row.get("graph_edge_count", "0")) > 0:
        return "graph_derivative_exists_review_before_promotion"
    if int(pipeline_row.get("candidate_queue_count", "0")) > 0:
        return "candidate_queue_exists_review_before_promotion"
    if int(pipeline_row.get("asset_count", "0")) > 0:
        return "asset_derivative_exists_review_before_reuse"
    if int(pipeline_row.get("metadata_profile_count", "0")) > 0:
        return "metadata_profile_exists_needs_derivative_decision"
    return "no_safe_derivative_route_recorded_yet"


def build_execution_rows(
    pipeline_rows: list[dict[str, str]],
    gap_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    gaps_by_source: dict[str, list[dict[str, str]]] = {}
    for row in gap_rows:
        gaps_by_source.setdefault(row["source_id"], []).append(row)

    output_rows: list[dict[str, str]] = []
    for index, pipeline_row in enumerate(sorted(pipeline_rows, key=lambda item: item["source_id"]), start=1):
        source_id = pipeline_row["source_id"]
        source_gaps = sorted(
            gaps_by_source.get(source_id, []),
            key=lambda item: (int(item["priority_rank"]), item["gap_type"]),
        )
        gap_type_counts = Counter(row["gap_type"] for row in source_gaps)
        priority_values = [int(row["priority_rank"]) for row in source_gaps if row.get("priority_rank", "").isdigit()]
        review_status = "needs_source_engineering_review" if source_gaps else "no_current_source_engineering_gap"
        output_rows.append(
            {
                "source_execution_id": f"source-engineering-exec-{index:03d}",
                "source_id": source_id,
                "current_stage": pipeline_row["current_stage"],
                "authority_tier": pipeline_row["authority_tier"],
                "rights_status": pipeline_row["rights_status"],
                "download_status_counts": pipeline_row["download_status_counts"],
                "gap_count": str(len(source_gaps)),
                "highest_priority_rank": str(min(priority_values)) if priority_values else "0",
                "gap_type_counts": compact_counter(gap_type_counts),
                "required_next_checks": ";".join(unique_semicolon_values(source_gaps, "required_next_checks")),
                "route_files_to_open": ";".join(unique_semicolon_values(source_gaps, "route_files_to_open")),
                "expected_review_log_paths": ";".join(
                    row["expected_output_path"] for row in source_gaps if row.get("expected_output_path")
                ),
                "safe_derivative_route_status": safe_derivative_status(source_gaps, pipeline_row),
                "source_promotion_status": "not_promoted",
                "commit_policy_boundary": COMMIT_POLICY_BOUNDARY,
                "research_boundary": RESEARCH_BOUNDARY,
                "review_status": review_status,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    review_status_counts = Counter(row["review_status"] for row in rows)
    safe_derivative_status_counts = Counter(row["safe_derivative_route_status"] for row in rows)
    gap_type_counts: Counter[str] = Counter()
    total_gap_count = 0
    for row in rows:
        total_gap_count += int(row["gap_count"])
        for item in row["gap_type_counts"].split(";"):
            if not item:
                continue
            gap_type, count = item.rsplit(":", 1)
            gap_type_counts[gap_type] += int(count)
    return {
        "summary_id": "source-engineering-execution-summary-001",
        "updated_at": UPDATED_AT,
        "matrix_csv_path": OUTPUT_CSV.as_posix(),
        "source_count": len(rows),
        "source_with_gap_count": sum(1 for row in rows if int(row["gap_count"]) > 0),
        "total_gap_count": total_gap_count,
        "gap_type_counts": dict(sorted(gap_type_counts.items())),
        "review_status_counts": dict(sorted(review_status_counts.items())),
        "safe_derivative_route_status_counts": dict(sorted(safe_derivative_status_counts.items())),
        "completion_boundary": (
            "This summary is a source-engineering execution index only. It does not "
            "download raw material, import corpus records, clear rights, or promote "
            "candidate scholarship."
        ),
        "caution": CAUTION,
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering execution matrix.")
    parser.add_argument("--repo-root", type=Path, default=repo_root())
    parser.add_argument("--csv-output", type=Path, default=OUTPUT_CSV)
    parser.add_argument("--json-output", type=Path, default=OUTPUT_JSON)
    args = parser.parse_args(argv)

    root = args.repo_root.resolve()
    rows = build_execution_rows(
        read_csv_rows(root / SOURCE_PROCESSING_PIPELINE_AUDIT),
        read_csv_rows(root / SOURCE_ENGINEERING_GAP_QUEUE),
    )
    csv_output = args.csv_output if args.csv_output.is_absolute() else root / args.csv_output
    json_output = args.json_output if args.json_output.is_absolute() else root / args.json_output
    write_csv(csv_output, rows)
    write_json(json_output, build_summary(rows))
    print(f"source_engineering_execution_rows={len(rows)} csv={csv_output} json={json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
