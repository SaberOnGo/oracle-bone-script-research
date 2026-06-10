#!/usr/bin/env python3
"""Capture source-register rows for codepoint crosswalk evidence tasks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


EVIDENCE_CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "044_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-capture-scaffold.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "045_ai-agent-hust-obimd-evobc-codepoint-crosswalk-source-register-capture-results.csv"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-obimd", "src-evobc"]
RESEARCH_BOUNDARY = "codepoint_crosswalk_source_register_capture_result_not_scholarship"
EVIDENCE_COLLECTION_STATUS = "source_register_metadata_captured"
SOURCE_REGISTER_EVIDENCE_STATUS = "metadata_captured_from_reviewed_source_register"
SOURCE_REGISTER_ROW_STATUS = "reviewed_source_register_row_found"
RIGHTS_DECISION_STATUS = "register_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures source-register metadata for later evidence review. It copies "
    "registered source, URL, rights, risk, and review fields only; it is not an "
    "oracle-character identity decision, not an accepted reading, not a component "
    "assignment, not an evolution-chain assignment, not a new rights decision, and "
    "not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "capture_result_id",
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "codepoint_review_task_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
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
    "decipherment_claim_status",
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


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _source_sort_key(source_id: str) -> int:
    try:
        return SOURCE_ORDER.index(source_id)
    except ValueError:
        return len(SOURCE_ORDER)


def _source_register_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "source_register"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _capture_row(
    index: int,
    task: dict[str, str],
    source_id: str,
    source_row: dict[str, str],
) -> dict[str, str]:
    return {
        "capture_result_id": f"codepoint-source-register-capture-result-{index:03d}",
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "codepoint_review_task_id": task["codepoint_review_task_id"],
        "crosswalk_candidate_id": task["crosswalk_candidate_id"],
        "suggested_oracle_character_id": task["suggested_oracle_character_id"],
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
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "capture_status": CAPTURE_STATUS,
        "captured_metadata_summary": _summary(
            {
                "route_result_id": task["route_result_id"],
                "capture_task_id": task["capture_task_id"],
                "source_id": source_id,
                "source_type": source_row["source_type"],
                "authority_tier": source_row["authority_tier"],
                "rights_status": source_row["rights_status"],
                "review_status": source_row["review_status"],
                "source_updated_at": source_row["updated_at"],
            }
        ),
        "required_next_checks": (
            "open_source_register_row;verify_source_url_provider_rights_and_risk;"
            "cross_check_against_download_log_before_asset_or_evidence_promotion"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_by_id = {row["source_id"]: row for row in source_rows}
    rows: list[dict[str, str]] = []
    for task in _source_register_tasks(capture_scaffold_rows):
        source_ids = sorted(_split_compact(task["source_record_refs"]), key=_source_sort_key)
        for source_id in source_ids:
            if source_id not in source_by_id:
                raise ValueError(f"missing source register row for {source_id}")
            rows.append(_capture_row(len(rows) + 1, task, source_id, source_by_id[source_id]))
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
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
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
