#!/usr/bin/env python3
"""Build human-gated follow-up queue for first-wave source-engineering results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
FIRST_WAVE_REVIEW_RESULTS = STAT_DIR / "119_ai-agent-source-engineering-first-wave-review-results.csv"
RESULT_RECORD_MANIFEST = STAT_DIR / "120_ai-agent-source-engineering-first-wave-result-record-manifest.csv"
DEFAULT_OUTPUT = STAT_DIR / "121_ai-agent-source-engineering-first-wave-followup-queue.csv"

UPDATED_AT = "2026-06-19"
FOLLOWUP_STATUS = "pending_human_review"
AUTOMATION_BOUNDARY = "human_gated_metadata_only_followup"
RESEARCH_BOUNDARY = "source_engineering_first_wave_followup_queue_not_scholarship"
CAUTION = (
    "This first-wave follow-up queue routes metadata-only source-engineering "
    "tasks for human review. It is not a new download, not checksum "
    "recalculation, not a rights decision, not source promotion, not corpus "
    "import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)

FOLLOWUP_ACTION_TYPES = {
    "access_boundary_followup": "manual_access_boundary_review",
    "checksum_and_download_status_review": "checksum_absence_boundary_review",
    "metadata_profile_extraction_planning": "metadata_profile_extraction_plan_review",
    "source_field_map_planning": "field_map_semantics_review",
    "package_manifest_or_not_applicable_review": "package_manifest_decision_review",
    "safe_derived_record_decision": "safe_derived_record_decision_review",
}

OUTPUT_FIELDS = [
    "followup_task_id",
    "first_wave_result_id",
    "result_record_manifest_id",
    "handoff_item_id",
    "next_action_id",
    "source_engineering_gap_id",
    "source_id",
    "action_lane",
    "followup_action_type",
    "followup_priority_rank",
    "decision_field",
    "decision_value",
    "followup_objective",
    "followup_status",
    "automation_boundary",
    "first_wave_result_path",
    "result_record_manifest_path",
    "result_record_path",
    "reviewed_evidence_paths",
    "required_next_checks",
    "required_followup",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_by_result_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["first_wave_result_id"]: row for row in rows}


def followup_objective(row: dict[str, str]) -> str:
    parts = [
        row["required_next_checks"],
        row["required_followup"],
        "keep_metadata_only_boundary",
        "record_human_review_before_any_source_promotion_or_import",
    ]
    return ";".join(part for part in parts if part)


def build_followup_rows(
    review_rows: list[dict[str, str]], manifest_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    manifest = manifest_by_result_id(manifest_rows)
    rows: list[dict[str, str]] = []
    for index, row in enumerate(review_rows, start=1):
        result_id = row["first_wave_result_id"]
        if result_id not in manifest:
            raise ValueError(f"missing result record manifest row for {result_id}")
        manifest_row = manifest[result_id]
        action_lane = row["action_lane"]
        if action_lane not in FOLLOWUP_ACTION_TYPES:
            raise ValueError(f"unsupported first-wave action lane: {action_lane}")
        rows.append(
            {
                "followup_task_id": f"source-engineering-first-wave-followup-{index:04d}",
                "first_wave_result_id": result_id,
                "result_record_manifest_id": manifest_row["result_record_manifest_id"],
                "handoff_item_id": row["handoff_item_id"],
                "next_action_id": row["next_action_id"],
                "source_engineering_gap_id": row["source_engineering_gap_id"],
                "source_id": row["source_id"],
                "action_lane": action_lane,
                "followup_action_type": FOLLOWUP_ACTION_TYPES[action_lane],
                "followup_priority_rank": row["priority_rank"],
                "decision_field": row["decision_field"],
                "decision_value": row["decision_value"],
                "followup_objective": followup_objective(row),
                "followup_status": FOLLOWUP_STATUS,
                "automation_boundary": AUTOMATION_BOUNDARY,
                "first_wave_result_path": FIRST_WAVE_REVIEW_RESULTS.as_posix(),
                "result_record_manifest_path": RESULT_RECORD_MANIFEST.as_posix(),
                "result_record_path": manifest_row["result_record_path"],
                "reviewed_evidence_paths": row["reviewed_evidence_paths"],
                "required_next_checks": row["required_next_checks"],
                "required_followup": row["required_followup"],
                "rights_decision_status": row["rights_decision_status"],
                "source_promotion_status": row["source_promotion_status"],
                "corpus_import_status": row["corpus_import_status"],
                "decipherment_claim_status": row["decipherment_claim_status"],
                "identity_claim_status": row["identity_claim_status"],
                "component_claim_status": row["component_claim_status"],
                "evolution_claim_status": row["evolution_claim_status"],
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build first-wave source-engineering follow-up queue.")
    parser.add_argument("--results", default=str(FIRST_WAVE_REVIEW_RESULTS))
    parser.add_argument("--manifest", default=str(RESULT_RECORD_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_followup_rows(
        read_csv_rows(root / args.results),
        read_csv_rows(root / args.manifest),
    )
    write_csv(root / args.output, rows)
    print(
        f"followup_task_count={len(rows)} "
        f"action_type_count={len({row['followup_action_type'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
