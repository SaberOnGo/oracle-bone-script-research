#!/usr/bin/env python3
"""Capture source-register metadata for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


EVIDENCE_CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "054_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-scaffold.csv"
)
CAPTURE_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "055_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-review-checklist.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "056_ai-agent-hust-obc-undeciphered-candidate-source-register-capture-results.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_source_register_capture_result_not_scholarship"
SOURCE_REGISTER_ROW_STATUS = "reviewed_source_register_row_found"
SOURCE_REGISTER_EVIDENCE_STATUS = "metadata_captured_from_reviewed_source_register"
EVIDENCE_COLLECTION_STATUS = "source_register_metadata_captured"
RIGHTS_DECISION_STATUS = "register_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
COMPONENT_CLAIM_STATUS = "no_claim"
EVOLUTION_CHAIN_CLAIM_STATUS = "no_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures source-register metadata for later undeciphered-candidate "
    "evidence review. It copies registered source, URL, rights, risk, and review "
    "fields only; it is not an accepted oracle-character identity, not a formal "
    "obs-char assignment, not an accepted reading, not a component assignment, "
    "not an evolution-chain assignment, not a new rights decision, not source "
    "promotion, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "capture_result_id",
    "checklist_id",
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "source_id",
    "source_register_path",
    "source_register_row_status",
    "source_type_evidence_value",
    "title_evidence_value",
    "provider_evidence_value",
    "authority_tier_evidence_value",
    "source_url_evidence_value",
    "scope_evidence_value",
    "adoption_status_evidence_value",
    "download_strategy_evidence_value",
    "rights_status_evidence_value",
    "risk_note_evidence_value",
    "review_status_evidence_value",
    "source_updated_at_evidence_value",
    "source_register_evidence_status",
    "evidence_collection_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "capture_status",
    "captured_metadata_summary",
    "required_next_checks",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _source_register_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "source_register"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _checklist_by_capture_task(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    source_rows = _source_register_tasks(rows)
    for row in source_rows:
        if row["checklist_status"] != "not_started":
            raise ValueError(f"unexpected checklist_status for {row['capture_task_id']}")
        if row["evidence_collection_status"] != "not_collected":
            raise ValueError(f"unexpected evidence_collection_status for {row['capture_task_id']}")
        if "open_source_register" not in row["required_review_checks"]:
            raise ValueError(f"missing source-register review check for {row['capture_task_id']}")
    return {row["capture_task_id"]: row for row in source_rows}


def _capture_row(
    index: int,
    task: dict[str, str],
    checklist_row: dict[str, str],
    source_row: dict[str, str],
) -> dict[str, str]:
    source_id = task["source_record_refs"]
    return {
        "capture_result_id": f"hust-obc-undeciphered-source-register-capture-result-{index:04d}",
        "checklist_id": checklist_row["checklist_id"],
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "undeciphered_review_task_id": task["undeciphered_review_task_id"],
        "context_pack_id": task["context_pack_id"],
        "unknown_candidate_id": task["unknown_candidate_id"],
        "primary_external_ref_id": task["primary_external_ref_id"],
        "source_id": source_id,
        "source_register_path": task["source_route_path"],
        "source_register_row_status": SOURCE_REGISTER_ROW_STATUS,
        "source_type_evidence_value": source_row["source_type"],
        "title_evidence_value": source_row["title"],
        "provider_evidence_value": source_row["provider"],
        "authority_tier_evidence_value": source_row["authority_tier"],
        "source_url_evidence_value": source_row["source_url"],
        "scope_evidence_value": source_row["scope"],
        "adoption_status_evidence_value": source_row["adoption_status"],
        "download_strategy_evidence_value": source_row["download_strategy"],
        "rights_status_evidence_value": source_row["rights_status"],
        "risk_note_evidence_value": source_row["risk_note"],
        "review_status_evidence_value": source_row["review_status"],
        "source_updated_at_evidence_value": source_row["updated_at"],
        "source_register_evidence_status": SOURCE_REGISTER_EVIDENCE_STATUS,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "rights_decision_status": RIGHTS_DECISION_STATUS,
        "source_promotion_status": SOURCE_PROMOTION_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "assignment_status": ASSIGNMENT_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "component_claim_status": COMPONENT_CLAIM_STATUS,
        "evolution_chain_claim_status": EVOLUTION_CHAIN_CLAIM_STATUS,
        "capture_status": CAPTURE_STATUS,
        "captured_metadata_summary": _summary(
            {
                "route_result_id": task["route_result_id"],
                "capture_task_id": task["capture_task_id"],
                "checklist_id": checklist_row["checklist_id"],
                "source_id": source_id,
                "source_type": source_row["source_type"],
                "authority_tier": source_row["authority_tier"],
                "rights_status": source_row["rights_status"],
                "review_status": source_row["review_status"],
            }
        ),
        "required_next_checks": (
            "open_056_source_register_capture_result;cross_check_against_057_download_log;"
            "do_not_promote_unknown_candidate_identity_or_decipherment"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    checklist_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_by_id = {row["source_id"]: row for row in source_rows}
    checklist_by_task = _checklist_by_capture_task(checklist_rows)
    rows: list[dict[str, str]] = []
    for task in _source_register_tasks(capture_scaffold_rows):
        source_id = task["source_record_refs"]
        if source_id not in source_by_id:
            raise ValueError(f"missing source register row for {source_id}")
        if task["capture_task_id"] not in checklist_by_task:
            raise ValueError(f"missing checklist row for {task['capture_task_id']}")
        rows.append(
            _capture_row(
                len(rows) + 1,
                task,
                checklist_by_task[task["capture_task_id"]],
                source_by_id[source_id],
            )
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-scaffold", default=str(EVIDENCE_CAPTURE_SCAFFOLD))
    parser.add_argument("--capture-review-checklist", default=str(CAPTURE_REVIEW_CHECKLIST))
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        read_csv_rows(root / args.capture_review_checklist),
        read_csv_rows(root / args.source_index),
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"source_count={len({row['source_id'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
