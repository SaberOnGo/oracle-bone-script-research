#!/usr/bin/env python3
"""Build lane-level summary for source-engineering review backlog.

This summary aggregates the 104 next-action checklist and the 105 empty result
scaffold by action lane. It is a preprocessing statistics surface only: it does
not complete source-engineering review, collect evidence, decide rights,
promote sources, import corpus rows, or make scholarly claims.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/104_ai-agent-source-engineering-next-action-checklist.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/106_ai-agent-source-engineering-lane-summary.csv"
)

UPDATED_AT = "2026-06-19"
REVIEW_STATUS = "summary_only_pending_source_engineering_review"
RESEARCH_BOUNDARY = "source_engineering_lane_summary_not_scholarship"
CAUTION = (
    "Source-engineering lane summary only; this does not complete "
    "source-engineering review, collect evidence, decide rights, promote "
    "sources, import corpus rows, confirm identity, or make decipherment claims."
)

OUTPUT_FIELDS = [
    "lane_summary_id",
    "action_lane",
    "action_count",
    "source_count",
    "priority_min",
    "priority_max",
    "gap_type_counts",
    "safe_to_automate_status_counts",
    "result_status_counts",
    "evidence_collection_status_counts",
    "human_review_status_counts",
    "rights_decision_status_counts",
    "source_promotion_status_counts",
    "corpus_import_status_counts",
    "decipherment_claim_status_counts",
    "source_ids",
    "next_action_ids",
    "result_scaffold_ids",
    "blocking_conditions",
    "checklist_path",
    "result_scaffold_path",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter) if key)


def join_unique(values: list[str]) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            output.append(value)
            seen.add(value)
    return ";".join(output)


def int_value(value: str) -> int:
    return int(value) if value.isdigit() else 0


def build_lane_summary_rows(root: Path) -> list[dict[str, str]]:
    checklist_rows = read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
    result_rows = read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD)
    results_by_action = {row["next_action_id"]: row for row in result_rows}
    lanes = sorted({row["action_lane"] for row in checklist_rows})

    output_rows: list[dict[str, str]] = []
    for index, lane in enumerate(lanes, start=1):
        lane_checklist_rows = [row for row in checklist_rows if row["action_lane"] == lane]
        lane_results = [results_by_action[row["next_action_id"]] for row in lane_checklist_rows]
        priorities = [int_value(row["priority_rank"]) for row in lane_checklist_rows]
        output_rows.append(
            {
                "lane_summary_id": f"source-engineering-lane-summary-{index:03d}",
                "action_lane": lane,
                "action_count": str(len(lane_checklist_rows)),
                "source_count": str(len({row["source_id"] for row in lane_checklist_rows})),
                "priority_min": str(min(priorities)),
                "priority_max": str(max(priorities)),
                "gap_type_counts": compact_counter(Counter(row["gap_type"] for row in lane_checklist_rows)),
                "safe_to_automate_status_counts": compact_counter(
                    Counter(row["safe_to_automate_status"] for row in lane_checklist_rows)
                ),
                "result_status_counts": compact_counter(Counter(row["result_status"] for row in lane_results)),
                "evidence_collection_status_counts": compact_counter(
                    Counter(row["evidence_collection_status"] for row in lane_results)
                ),
                "human_review_status_counts": compact_counter(
                    Counter(row["human_review_status"] for row in lane_results)
                ),
                "rights_decision_status_counts": compact_counter(
                    Counter(row["rights_decision_status"] for row in lane_results)
                ),
                "source_promotion_status_counts": compact_counter(
                    Counter(row["source_promotion_status"] for row in lane_results)
                ),
                "corpus_import_status_counts": compact_counter(
                    Counter(row["corpus_import_status"] for row in lane_results)
                ),
                "decipherment_claim_status_counts": compact_counter(
                    Counter(row["decipherment_claim_status"] for row in lane_results)
                ),
                "source_ids": join_unique([row["source_id"] for row in lane_checklist_rows]),
                "next_action_ids": join_unique([row["next_action_id"] for row in lane_checklist_rows]),
                "result_scaffold_ids": join_unique([row["result_scaffold_id"] for row in lane_results]),
                "blocking_conditions": join_unique([row["blocking_condition"] for row in lane_checklist_rows]),
                "checklist_path": SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST.as_posix(),
                "result_scaffold_path": SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD.as_posix(),
                "review_status": REVIEW_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering lane summary.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_lane_summary_rows(root)
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
