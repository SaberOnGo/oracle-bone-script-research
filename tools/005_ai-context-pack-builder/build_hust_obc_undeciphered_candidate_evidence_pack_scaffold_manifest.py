#!/usr/bin/env python3
"""Build empty evidence-pack scaffold manifest rows for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


READINESS_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv"
)
REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "052_ai-agent-hust-obc-undeciphered-candidate-review-log-draft-manifest.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "061_ai-agent-hust-obc-undeciphered-candidate-evidence-pack-scaffold-manifest.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_evidence_pack_scaffold_manifest_not_scholarship"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
EVIDENCE_PACK_STATUS = "empty_scaffold_not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "not_started"
METADATA_CAPTURE_STATUS = "ready_metadata_only"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
REQUIRED_EVIDENCE_SECTIONS = [
    "character_or_unknown_glyph_id",
    "source_references_and_asset_metadata",
    "full_inscription_context",
    "neighboring_characters",
    "component_breakdown_and_variant_notes",
    "excavation_period_and_catalog_provenance",
    "bronze_seal_or_modern_comparanda",
    "supporting_evidence",
    "opposing_evidence",
    "open_questions_and_next_checks",
    "review_log",
]
CAUTION = (
    "This row is an empty metadata-only evidence-pack scaffold for a HUST-OBC "
    "undeciphered candidate. It is not compatible with the formal obs-char "
    "evidence-pack schema until a human review promotes the candidate into a "
    "formal obs-char assignment path. It records route readiness only; do not infer "
    "identity, reading, component, evolution chain, rights decision, source "
    "promotion, or decipherment conclusion from it."
)

OUTPUT_FIELDS = [
    "evidence_pack_scaffold_id",
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "review_log_draft_path",
    "candidate_packet_path",
    "bucket_manifest_path",
    "source_id_captured",
    "source_package_id_captured",
    "download_id_captured",
    "source_class_path_captured",
    "source_image_count_captured",
    "metadata_capture_status",
    "evidence_pack_status",
    "evidence_collection_status",
    "evidence_section_statuses",
    "required_evidence_sections",
    "human_review_status",
    "formal_schema_compatibility_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "rights_decision_status",
    "source_promotion_status",
    "research_boundary",
    "required_next_checks",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _by_review_log(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row["review_log_draft_id"]
        if key in result:
            raise ValueError(f"duplicate review_log_draft_id: {key}")
        result[key] = row
    return result


def _require_ready(row: dict[str, str]) -> None:
    if row["overall_readiness_status"] != "ready_for_human_evidence_pack_review_metadata_only":
        raise ValueError(f"readiness row is not ready: {row['readiness_check_id']}")
    if row["captured_section_count"] != row["required_section_count"]:
        raise ValueError(f"incomplete metadata capture: {row['readiness_check_id']}")
    if row["missing_required_sections"] != "none":
        raise ValueError(f"missing sections in readiness row: {row['readiness_check_id']}")


def _section_statuses() -> str:
    return ";".join(f"{section}=not_collected" for section in REQUIRED_EVIDENCE_SECTIONS)


def _sections() -> str:
    return ";".join(REQUIRED_EVIDENCE_SECTIONS)


def _review_log_path(row: dict[str, str], review_rows_by_id: dict[str, dict[str, str]]) -> str:
    draft = review_rows_by_id.get(row["review_log_draft_id"])
    if draft is None:
        raise ValueError(f"missing 052 draft row for {row['review_log_draft_id']}")
    for field in ["unknown_candidate_id", "primary_external_ref_id", "undeciphered_review_task_id"]:
        if row[field] != draft[field]:
            raise ValueError(f"052/060 mismatch for {field}: {row['readiness_check_id']}")
    return draft["draft_path"]


def build_scaffold_manifest_rows(
    readiness_rows: list[dict[str, str]],
    review_log_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    review_rows_by_id = _by_review_log(review_log_rows)
    rows: list[dict[str, str]] = []
    for index, row in enumerate(readiness_rows, start=1):
        _require_ready(row)
        rows.append(
            {
                "evidence_pack_scaffold_id": f"hust-obc-undeciphered-evidence-pack-scaffold-{index:04d}",
                "readiness_check_id": row["readiness_check_id"],
                "route_result_id": row["route_result_id"],
                "review_log_draft_id": row["review_log_draft_id"],
                "undeciphered_review_task_id": row["undeciphered_review_task_id"],
                "context_pack_id": row["context_pack_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "candidate_packet_capture_result_id": row["candidate_packet_capture_result_id"],
                "source_register_capture_result_id": row["source_register_capture_result_id"],
                "download_log_capture_result_id": row["download_log_capture_result_id"],
                "large_source_register_capture_result_id": row["large_source_register_capture_result_id"],
                "review_log_draft_path": _review_log_path(row, review_rows_by_id),
                "candidate_packet_path": row["candidate_packet_path"],
                "bucket_manifest_path": row["bucket_manifest_path"],
                "source_id_captured": row["source_id_captured"],
                "source_package_id_captured": row["source_package_id_captured"],
                "download_id_captured": row["download_id_captured"],
                "source_class_path_captured": row["source_class_path_captured"],
                "source_image_count_captured": row["source_image_count_captured"],
                "metadata_capture_status": METADATA_CAPTURE_STATUS,
                "evidence_pack_status": EVIDENCE_PACK_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "evidence_section_statuses": _section_statuses(),
                "required_evidence_sections": _sections(),
                "human_review_status": HUMAN_REVIEW_STATUS,
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "decipherment_claim_status": NO_CLAIM,
                "component_claim_status": NO_CLAIM,
                "evolution_chain_claim_status": NO_CLAIM,
                "rights_decision_status": row["rights_decision_status"],
                "source_promotion_status": row["source_promotion_status"],
                "research_boundary": RESEARCH_BOUNDARY,
                "required_next_checks": (
                    "open_060_readiness_row;open_052_review_log_draft;"
                    "open_056_057_058_059_capture_rows;open_candidate_packet_and_bucket_manifest;"
                    "collect_source_marked_evidence_before_any_formal_schema_promotion"
                ),
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
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
    parser.add_argument("--readiness-checklist", default=str(READINESS_CHECKLIST))
    parser.add_argument("--review-log-draft-manifest", default=str(REVIEW_LOG_DRAFT_MANIFEST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_scaffold_manifest_rows(
        read_csv_rows(root / args.readiness_checklist),
        read_csv_rows(root / args.review_log_draft_manifest),
    )
    write_csv(root / args.output, rows)
    print(
        f"evidence_pack_scaffold_count={len(rows)} "
        f"not_collected_count={sum(row['evidence_collection_status'] == EVIDENCE_COLLECTION_STATUS for row in rows)} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
