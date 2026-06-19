#!/usr/bin/env python3
"""Build a metadata-only review queue for Cambridge/Hopkins inscription crosswalk rows."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


CAMBRIDGE_HOPKINS_CROSSWALK_STAGING = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "002_cambridge-hopkins-crosswalk-staging.csv"
)
CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "003_cambridge-hopkins-classified-summary.csv"
)
CAMBRIDGE_HOPKINS_GRAPH_EDGES = Path(
    "corpus/008_relationship-graph/008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_ROUTE_REVIEW_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/011_ai-agent-source-route-review-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
)

UPDATED_AT = "2026-06-19"
TASK_STATUS = "needs_catalog_crosswalk_review"
RESEARCH_BOUNDARY = "cambridge_hopkins_inscription_crosswalk_review_metadata_only_not_scholarship"
CAUTION = (
    "This row is an inscription catalog-crosswalk review task only. It preserves "
    "Cambridge/Hopkins finding-list metadata and routes reviewers to source-marked "
    "references; it is not a formal obi-* assignment, not an object identity claim, "
    "not an inscription reading, not a Heji/OBM confirmation, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "cambridge_hopkins_review_task_id",
    "candidate_inscription_crosswalk_id",
    "source_id",
    "evidence_download_id",
    "priority_rank",
    "priority_bucket",
    "period_label",
    "group_number",
    "group_declared_count",
    "period_group_observed_row_count",
    "period_group_count_status",
    "yingguo_ref_id",
    "cul_ref_id",
    "chalfant_ref_id",
    "heji_ref_id",
    "missing_reference_count",
    "missing_reference_types",
    "required_next_checks",
    "route_files_to_open",
    "expected_output_path",
    "formal_inscription_assignment_status",
    "catalog_identity_claim_status",
    "image_evidence_status",
    "text_transcription_status",
    "collection_object_match_status",
    "task_status",
    "research_boundary",
    "rights_status",
    "review_status",
    "caution",
    "updated_at",
]

COMMON_NEXT_CHECKS = [
    "open_cambridge_hopkins_crosswalk_row",
    "verify_source_download_log_checksum_size_and_rights_boundary",
    "compare_yingguo_cul_chalfant_heji_refs_against_primary_catalog_or_object_record",
    "record_no_formal_obi_assignment_no_reading_no_object_identity_claim",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def bool_field(row: dict[str, str], key: str) -> bool:
    return row.get(key, "").strip().lower() == "true"


def missing_reference_types(row: dict[str, str]) -> list[str]:
    missing = []
    if bool_field(row, "has_missing_cul_ref"):
        missing.append("cul_ref")
    if bool_field(row, "has_missing_chalfant_ref"):
        missing.append("chalfant_ref")
    if bool_field(row, "has_missing_heji_ref"):
        missing.append("heji_ref")
    return missing


def priority_bucket(row: dict[str, str]) -> tuple[int, str]:
    missing = set(missing_reference_types(row))
    if {"cul_ref", "chalfant_ref", "heji_ref"}.issubset(missing):
        return (1, "missing_cul_chalfant_heji_refs")
    if {"chalfant_ref", "heji_ref"}.issubset(missing):
        return (2, "missing_chalfant_heji_refs")
    if {"cul_ref", "heji_ref"}.issubset(missing):
        return (3, "missing_cul_heji_refs")
    if "heji_ref" in missing:
        return (4, "missing_heji_ref")
    if "chalfant_ref" in missing:
        return (5, "missing_chalfant_ref")
    if "cul_ref" in missing:
        return (6, "missing_cul_ref")
    return (7, "crosswalk_refs_present_needs_external_review")


def sort_key(row: dict[str, str]) -> tuple[int, str, int, str]:
    rank, _bucket = priority_bucket(row)
    group_number = row.get("group_number", "")
    group_sort = 999 if group_number == "unclassified" else int(group_number)
    return (rank, row.get("period_label", ""), group_sort, row["candidate_inscription_crosswalk_id"])


def period_group_key(row: dict[str, str]) -> str:
    return f"{row['period_label']}|{row['group_number']}"


def period_group_count_status(row: dict[str, str], period_group_counts: Counter[str]) -> str:
    declared = row.get("group_declared_count", "")
    if not declared or declared == "-":
        return "no_declared_group_count"
    return (
        "matches_declared_period_group_count"
        if int(declared) == period_group_counts[period_group_key(row)]
        else "differs_from_declared_period_group_count"
    )


def route_files(row: dict[str, str]) -> list[str]:
    return [
        CAMBRIDGE_HOPKINS_CROSSWALK_STAGING.as_posix(),
        CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY.as_posix(),
        CAMBRIDGE_HOPKINS_GRAPH_EDGES.as_posix(),
        SOURCE_INDEX.as_posix(),
        SOURCE_DOWNLOAD_LOG.as_posix(),
        SOURCE_ROUTE_REVIEW_RESULTS.as_posix(),
    ]


def required_next_checks(row: dict[str, str]) -> list[str]:
    checks = list(COMMON_NEXT_CHECKS)
    for missing_type in missing_reference_types(row):
        checks.append(f"locate_or_confirm_missing_{missing_type}")
    if not missing_reference_types(row):
        checks.append("verify_complete_crosswalk_refs_still_do_not_promote_without_image_object_obm_review")
    return checks


def expected_output_path(index: int, row: dict[str, str], bucket: str) -> str:
    return (
        "doc/public/user_research/007_inscription-crosswalk-review-queues/"
        f"{index:04d}_{row['candidate_inscription_crosswalk_id']}_{bucket}_review-log.md"
    )


def build_review_queue_rows(crosswalk_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    period_group_counts = Counter(period_group_key(row) for row in crosswalk_rows)
    output_rows = []
    for index, row in enumerate(sorted(crosswalk_rows, key=sort_key), start=1):
        rank, bucket = priority_bucket(row)
        missing = missing_reference_types(row)
        output_rows.append(
            {
                "cambridge_hopkins_review_task_id": f"cam-hopkins-crosswalk-review-{index:04d}",
                "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
                "source_id": row["source_id"],
                "evidence_download_id": row["evidence_download_id"],
                "priority_rank": str(rank),
                "priority_bucket": bucket,
                "period_label": row["period_label"],
                "group_number": row["group_number"],
                "group_declared_count": row["group_declared_count"],
                "period_group_observed_row_count": str(period_group_counts[period_group_key(row)]),
                "period_group_count_status": period_group_count_status(row, period_group_counts),
                "yingguo_ref_id": row["yingguo_ref_id"],
                "cul_ref_id": row["cul_ref_id"],
                "chalfant_ref_id": row["chalfant_ref_id"],
                "heji_ref_id": row["heji_ref_id"],
                "missing_reference_count": str(len(missing)),
                "missing_reference_types": ";".join(missing) if missing else "none",
                "required_next_checks": ";".join(required_next_checks(row)),
                "route_files_to_open": ";".join(route_files(row)),
                "expected_output_path": expected_output_path(index, row, bucket),
                "formal_inscription_assignment_status": "not_assigned_formal_obi_id",
                "catalog_identity_claim_status": "not_confirmed_catalog_identity",
                "image_evidence_status": "not_collected",
                "text_transcription_status": "not_collected",
                "collection_object_match_status": "not_collected",
                "task_status": TASK_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "rights_status": row["rights_status"],
                "review_status": "needs_human_review",
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Cambridge/Hopkins inscription crosswalk metadata review queue."
    )
    parser.add_argument("--repo-root", type=Path, default=repo_root())
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    crosswalk_rows = read_csv_rows(root / CAMBRIDGE_HOPKINS_CROSSWALK_STAGING)
    rows = build_review_queue_rows(crosswalk_rows)
    output_path = args.output if args.output.is_absolute() else root / args.output
    write_csv(output_path, rows)
    print(f"wrote={len(rows)} {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
