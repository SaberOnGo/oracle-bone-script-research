#!/usr/bin/env python3
"""Build a route pack for source checksum/download-status review.

The pack filters the 104 source-engineering checklist to the
checksum_and_download_status_review lane and pairs each task with the 105 empty
result scaffold. It is routing metadata only: no download is retried, no
checksum is recalculated, no source package is promoted, and no rights,
corpus-import, identity, or decipherment decision is made.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT = Path(
    "corpus/009_statistics-and-derived-features/103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/104_ai-agent-source-engineering-next-action-checklist.csv"
)
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
SOURCE_ENGINEERING_LANE_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/107_ai-agent-source-engineering-lane-route-pack.json"
)
SOURCE_PROCESSING_PIPELINE_AUDIT = Path(
    "corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv"
)
SOURCE_DOWNLOAD_STATUS_CODEBOOK = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/013_source-download-status-codebook.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/114_ai-agent-source-checksum-review-route-pack.json"
)

UPDATED_AT = "2026-06-19"
ACTION_LANE = "checksum_and_download_status_review"
ROUTE_PACK_ID = "source-checksum-review-route-pack-001"
REVIEW_STATUS = "route_pack_pending_checksum_review"
RESEARCH_BOUNDARY = "source_checksum_review_route_pack_not_download_or_checksum_decision"
CAUTION = (
    "Source checksum/download-status review route pack only; it does not retry "
    "downloads, does not recalculate checksums, is not a corpus import, not "
    "source promotion, not a rights decision, and not an identity or "
    "decipherment claim."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def route_from_rows(checklist_row: dict[str, str], result_row: dict[str, str]) -> dict[str, Any]:
    return {
        "next_action_id": checklist_row["next_action_id"],
        "result_scaffold_id": result_row["result_scaffold_id"],
        "evidence_snapshot_id": checklist_row["evidence_snapshot_id"],
        "source_engineering_gap_id": checklist_row["source_engineering_gap_id"],
        "review_log_draft_id": checklist_row["review_log_draft_id"],
        "source_id": checklist_row["source_id"],
        "gap_type": checklist_row["gap_type"],
        "priority_rank": int(checklist_row["priority_rank"]),
        "action_lane": checklist_row["action_lane"],
        "automation_scope": checklist_row["automation_scope"],
        "human_gate": checklist_row["human_gate"],
        "primary_input_path": checklist_row["primary_input_path"],
        "secondary_input_paths": split_values(checklist_row["secondary_input_paths"]),
        "source_checklist_path": result_row["source_checklist_path"],
        "lane_route_pack_path": SOURCE_ENGINEERING_LANE_ROUTE_PACK.as_posix(),
        "source_processing_pipeline_audit_path": SOURCE_PROCESSING_PIPELINE_AUDIT.as_posix(),
        "download_log_path": SOURCE_DOWNLOAD_LOG.as_posix(),
        "download_status_codebook_path": SOURCE_DOWNLOAD_STATUS_CODEBOOK.as_posix(),
        "review_log_path": checklist_row["review_log_path"],
        "expected_result_path": checklist_row["expected_result_path"],
        "result_record_path": result_row["result_record_path"],
        "checklist_items": split_values(checklist_row["checklist_items"]),
        "blocking_condition": checklist_row["blocking_condition"],
        "safe_to_automate_status": checklist_row["safe_to_automate_status"],
        "action_status": checklist_row["action_status"],
        "result_status": result_row["result_status"],
        "evidence_collection_status": result_row["evidence_collection_status"],
        "checksum_outcome": result_row["checksum_outcome"],
        "remaining_blockers": result_row["remaining_blockers"],
        "required_followup": split_values(result_row["required_followup"]),
        "human_review_status": result_row["human_review_status"],
        "rights_decision_status": result_row["rights_decision_status"],
        "source_promotion_status": result_row["source_promotion_status"],
        "corpus_import_status": result_row["corpus_import_status"],
        "decipherment_claim_status": result_row["decipherment_claim_status"],
    }


def build_route_pack(root: Path) -> dict[str, Any]:
    checklist_rows = [
        row
        for row in read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST)
        if row["action_lane"] == ACTION_LANE
    ]
    result_rows = read_csv_rows(root / SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD)
    results_by_action = {row["next_action_id"]: row for row in result_rows}
    routes = [route_from_rows(row, results_by_action[row["next_action_id"]]) for row in checklist_rows]

    return {
        "route_pack_id": ROUTE_PACK_ID,
        "updated_at": UPDATED_AT,
        "action_lane": ACTION_LANE,
        "source_paths": {
            "evidence_snapshot": SOURCE_ENGINEERING_GAP_EVIDENCE_SNAPSHOT.as_posix(),
            "next_action_checklist": SOURCE_ENGINEERING_NEXT_ACTION_CHECKLIST.as_posix(),
            "next_action_result_scaffold": SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD.as_posix(),
            "lane_route_pack": SOURCE_ENGINEERING_LANE_ROUTE_PACK.as_posix(),
            "source_processing_pipeline_audit": SOURCE_PROCESSING_PIPELINE_AUDIT.as_posix(),
            "source_download_log": SOURCE_DOWNLOAD_LOG.as_posix(),
            "source_download_status_codebook": SOURCE_DOWNLOAD_STATUS_CODEBOOK.as_posix(),
        },
        "source_count": len({route["source_id"] for route in routes}),
        "route_count": len(routes),
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source checksum/download-status review route pack.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_pack(root)
    write_json(root / args.output, data)
    print(f"routes={data['route_count']} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
