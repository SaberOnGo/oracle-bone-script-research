#!/usr/bin/env python3
"""Build an OBM access-boundary capture scaffold from the queue and draft manifest."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FOLLOWUP_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"
)
REVIEW_LOG_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "075_ai-agent-xxt-obm-access-boundary-review-log-draft-manifest.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "083_ai-agent-xxt-obm-access-boundary-capture-scaffold.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "xxt_obm_access_boundary_capture_scaffold_not_scholarship"
OUTPUT_SCOPE = "xxt_obm_access_boundary_capture_scaffold_only"

FIELDNAMES = [
    "capture_row_id",
    "review_log_draft_id",
    "followup_task_id",
    "source_id",
    "targeted_download_id",
    "targeted_url",
    "artifact_kind",
    "priority_bucket",
    "followup_method",
    "source_queue_path",
    "review_log_draft_path",
    "official_access_boundary_status",
    "route_file_review_status",
    "profile_match_count",
    "profile_ids",
    "profile_areas",
    "profile_normalized_values",
    "staging_row_count",
    "staging_row_kind_counts",
    "access_profile_availability_status",
    "access_profile_evidence_value",
    "staging_availability_status",
    "staging_evidence_value",
    "manual_followup_route_status",
    "capture_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "updated_at",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
    "research_boundary",
    "output_scope",
    "rights_status",
    "risk_note",
    "caution",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _compact(value: str) -> str:
    return value.strip()


def _by_id(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if key in result:
            raise ValueError(f"duplicate {field}: {key}")
        result[key] = row
    return result


def _capture_row(
    index: int,
    queue_row: dict[str, str],
    draft_row: dict[str, str],
) -> dict[str, str]:
    if queue_row["targeted_download_id"] != draft_row["targeted_download_id"]:
        raise ValueError("queue/draft targeted_download_id mismatch")
    if queue_row["targeted_url"] != draft_row["targeted_url"]:
        raise ValueError("queue/draft targeted_url mismatch")

    return {
        "capture_row_id": f"xxt-obm-access-capture-{index:03d}",
        "review_log_draft_id": draft_row["review_log_draft_id"],
        "followup_task_id": queue_row["obm_followup_review_task_id"],
        "source_id": queue_row["source_id"],
        "targeted_download_id": queue_row["targeted_download_id"],
        "targeted_url": queue_row["targeted_url"],
        "artifact_kind": queue_row["artifact_kind"],
        "priority_bucket": queue_row["priority_bucket"],
        "followup_method": queue_row["followup_method"],
        "source_queue_path": FOLLOWUP_REVIEW_QUEUE.as_posix(),
        "review_log_draft_path": draft_row["draft_path"],
        "official_access_boundary_status": queue_row["download_status"],
        "route_file_review_status": queue_row["route_file_review_status"],
        "profile_match_count": queue_row["profile_match_count"],
        "profile_ids": queue_row["profile_ids"],
        "profile_areas": queue_row["profile_areas"],
        "profile_normalized_values": queue_row["profile_normalized_values"],
        "staging_row_count": queue_row["staging_row_count"],
        "staging_row_kind_counts": queue_row["staging_row_kind_counts"],
        "access_profile_availability_status": "not_checked",
        "access_profile_evidence_value": "",
        "staging_availability_status": "not_checked",
        "staging_evidence_value": "",
        "manual_followup_route_status": "manual_browser_or_institutional_export_not_started",
        "capture_status": "empty_scaffold_not_started",
        "human_review_status": "not_started",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "assignment_status": "not_applicable_source_level_followup_only",
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "updated_at": UPDATED_AT,
        "route_files_to_open": _compact(queue_row["route_files_to_open"]),
        "required_review_sections": _compact(queue_row["required_review_sections"]),
        "required_next_checks": _compact(queue_row["required_next_checks"]),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "rights_status": queue_row["rights_status"],
        "risk_note": queue_row["risk_note"],
        "caution": (
            "Empty capture scaffold for Xiaoxuetang OBM access-boundary follow-up only. "
            "Fill this row only after opening the queue row, review-log draft, and cited "
            "route files; do not use it as source evidence, an old-catalog confirmation, "
            "a holding or collection match, a formal assignment, or not a decipherment conclusion."
        ),
    }


def build_capture_scaffold(
    queue_rows: list[dict[str, str]],
    draft_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    draft_by_task = _by_id(draft_rows, "obm_followup_review_task_id")
    rows: list[dict[str, str]] = []
    for queue_row in queue_rows:
        rows.append(
            _capture_row(
                len(rows) + 1,
                queue_row,
                draft_by_task[queue_row["obm_followup_review_task_id"]],
            )
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--followup-review-queue", default=str(FOLLOWUP_REVIEW_QUEUE))
    parser.add_argument("--review-log-manifest", default=str(REVIEW_LOG_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_scaffold(
        read_csv_rows(root / args.followup_review_queue),
        read_csv_rows(root / args.review_log_manifest),
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_row_count={len(rows)} "
        f"targeted_download_count={len({row['targeted_download_id'] for row in rows})} "
        "capture_status=empty_scaffold_not_started"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
