#!/usr/bin/env python3
"""Build review tasks for HUST/OBIMD/EVOBC codepoint crosswalk matches."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


CODEPOINT_CROSSWALK_CONTEXT_PACK = Path(
    "corpus/009_statistics-and-derived-features/"
    "040_ai-agent-hust-obimd-evobc-codepoint-crosswalk-context-pack.json"
)
HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "codepoint_crosswalk_review_queue_metadata_only_not_scholarship"
TASK_STATUS = "needs_codepoint_cross_source_review"
PROMOTION_STATUS = "not_promoted"
ASSIGNMENT_STATUS = "unassigned"
CAUTION = (
    "This row is a codepoint cross-source review task only. Exact Unicode codepoint matches "
    "from dataset labels are lookup routes, not confirmed oracle-character identity, not "
    "accepted readings, not component assignments, not evolution-chain assignments, and not "
    "decipherment conclusions."
)

OUTPUT_FIELDS = [
    "codepoint_review_task_id",
    "context_pack_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "promotion_queue_id",
    "priority_rank",
    "priority_bucket",
    "cross_source_status",
    "matched_source_ids",
    "hust_primary_external_ref_id",
    "hust_label_codepoints",
    "obimd_match_count",
    "obimd_candidate_main_character_ids",
    "evobc_match_count",
    "evobc_candidate_evolution_category_ids",
    "evobc_image_reference_count_total",
    "evobc_has_oracle_bone_refs_any",
    "candidate_packet_path",
    "required_evidence_sections",
    "required_next_checks",
    "route_files_to_open",
    "expected_output_path",
    "identity_claim_status",
    "promotion_status",
    "assignment_status",
    "task_status",
    "research_boundary",
    "caution",
    "updated_at",
]

PRIORITY_BY_STATUS = {
    "matched_obimd_and_evobc_by_codepoint": (1, "both_obimd_and_evobc_codepoint_match"),
    "matched_obimd_by_codepoint": (2, "obimd_only_codepoint_match"),
    "matched_evobc_by_codepoint": (3, "evobc_only_codepoint_match"),
}

REQUIRED_EVIDENCE_SECTIONS = [
    "crosswalk_row",
    "hust_candidate_packet",
    "source_register",
    "download_log",
    "rights_risk_boundary",
    "review_log",
]

COMMON_NEXT_CHECKS = [
    "open_codepoint_crosswalk_row",
    "open_hust_candidate_packet",
    "verify_source_register_and_download_log_rights_risk",
    "record_no_identity_or_decipherment_claim",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _priority(row: dict[str, str]) -> tuple[int, str]:
    return PRIORITY_BY_STATUS[row["cross_source_status"]]


def _evidence_sections(row: dict[str, str]) -> list[str]:
    sections = list(REQUIRED_EVIDENCE_SECTIONS)
    if int(row["obimd_match_count"]) > 0:
        sections.insert(2, "obimd_main_character_staging_row")
    if int(row["evobc_match_count"]) > 0:
        insert_at = 3 if "obimd_main_character_staging_row" in sections else 2
        sections.insert(insert_at, "evobc_evolution_category_staging_row")
    return sections


def _next_checks(row: dict[str, str]) -> list[str]:
    checks = list(COMMON_NEXT_CHECKS)
    if int(row["obimd_match_count"]) > 0:
        checks.insert(2, "open_obimd_main_character_staging_row")
    if int(row["evobc_match_count"]) > 0:
        insert_at = 3 if "open_obimd_main_character_staging_row" in checks else 2
        checks.insert(insert_at, "open_evobc_evolution_category_staging_row")
    return checks


def _expected_output_path(index: int, row: dict[str, str]) -> str:
    priority_rank, priority_bucket = _priority(row)
    return (
        "doc/public/user_research/004_codepoint-crosswalk-review-queues/"
        f"{priority_rank:03d}_{priority_bucket}/"
        f"{index:03d}_{row['crosswalk_candidate_id']}_review-log.md"
    )


def _route_files(row: dict[str, str]) -> list[str]:
    files = [
        CODEPOINT_CROSSWALK_CONTEXT_PACK.as_posix(),
        HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK.as_posix(),
    ]
    files.extend(_split_values(row["route_files"]))
    unique_files: list[str] = []
    for file_path in files:
        if file_path not in unique_files:
            unique_files.append(file_path)
    return unique_files


def build_review_rows(
    context_pack: dict[str, object],
    crosswalk_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    context_pack_id = str(context_pack["context_pack_id"])
    matched_rows = [
        row
        for row in crosswalk_rows
        if row["cross_source_status"] in PRIORITY_BY_STATUS
    ]
    matched_rows.sort(
        key=lambda row: (
            _priority(row)[0],
            row["crosswalk_candidate_id"],
        )
    )

    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(matched_rows, start=1):
        priority_rank, priority_bucket = _priority(row)
        output_rows.append(
            {
                "codepoint_review_task_id": f"codepoint-crosswalk-review-{index:03d}",
                "context_pack_id": context_pack_id,
                "crosswalk_candidate_id": row["crosswalk_candidate_id"],
                "suggested_oracle_character_id": row["suggested_oracle_character_id"],
                "promotion_queue_id": row["promotion_queue_id"],
                "priority_rank": str(priority_rank),
                "priority_bucket": priority_bucket,
                "cross_source_status": row["cross_source_status"],
                "matched_source_ids": row["matched_source_ids"],
                "hust_primary_external_ref_id": row["hust_primary_external_ref_id"],
                "hust_label_codepoints": row["hust_label_codepoints"],
                "obimd_match_count": row["obimd_match_count"],
                "obimd_candidate_main_character_ids": row["obimd_candidate_main_character_ids"],
                "evobc_match_count": row["evobc_match_count"],
                "evobc_candidate_evolution_category_ids": row[
                    "evobc_candidate_evolution_category_ids"
                ],
                "evobc_image_reference_count_total": row["evobc_image_reference_count_total"],
                "evobc_has_oracle_bone_refs_any": row["evobc_has_oracle_bone_refs_any"],
                "candidate_packet_path": row["candidate_packet_path"],
                "required_evidence_sections": ";".join(_evidence_sections(row)),
                "required_next_checks": ";".join(_next_checks(row)),
                "route_files_to_open": ";".join(_route_files(row)),
                "expected_output_path": _expected_output_path(index, row),
                "identity_claim_status": row["identity_claim_status"],
                "promotion_status": PROMOTION_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "task_status": TASK_STATUS,
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-pack", default=str(CODEPOINT_CROSSWALK_CONTEXT_PACK))
    parser.add_argument("--crosswalk", default=str(HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_rows(
        read_json(root / args.context_pack),
        read_csv_rows(root / args.crosswalk),
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
