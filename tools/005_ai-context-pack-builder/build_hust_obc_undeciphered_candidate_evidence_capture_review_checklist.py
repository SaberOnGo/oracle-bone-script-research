#!/usr/bin/env python3
"""Build a review checklist for HUST-OBC undeciphered evidence-capture rows."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "054_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-scaffold.csv"
)
ROUTE_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "053_ai-agent-hust-obc-undeciphered-candidate-review-route-results.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "055_ai-agent-hust-obc-undeciphered-candidate-evidence-capture-review-checklist.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = (
    "hust_obc_undeciphered_candidate_evidence_capture_review_checklist_not_scholarship"
)
CHECKLIST_STATUS = "not_started"
EVIDENCE_COLLECTION_STATUS = "not_collected"
CAPTURE_STATUS = "empty_scaffold_not_started"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
PROMOTION_STATUS = "not_promoted"
RIGHTS_DECISION_STATUS = "not_decided"
SOURCE_PROMOTION_STATUS = "not_promoted"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
CAUTION = (
    "Checklist row only. Open the capture scaffold, route result, and cited source "
    "route before filling any evidence. This checklist does not contain collected "
    "evidence, a rights decision, source promotion, accepted oracle-character "
    "identity, formal obs-char assignment, reading, component assignment, "
    "evolution-chain assignment, or decipherment conclusion."
)

SECTION_REVIEW_CHECKS = {
    "candidate_packet": (
        "open_capture_scaffold_row;open_candidate_packet;"
        "verify_packet_review_status_and_source_class_path;"
        "block_identity_assignment_reading_component_evolution_and_decipherment_claims"
    ),
    "source_register": (
        "open_capture_scaffold_row;open_source_register;"
        "verify_provider_authority_tier_rights_status_and_risk_note;"
        "block_new_rights_decision_and_source_promotion"
    ),
    "large_source_register": (
        "open_capture_scaffold_row;open_large_source_register;"
        "verify_raw_package_size_checksum_storage_and_rights;"
        "block_raw_package_commit_and_evidence_inference"
    ),
    "download_log": (
        "open_capture_scaffold_row;open_download_log;"
        "verify_download_status_size_checksum_and_temp_path;"
        "block_rights_identity_or_decipherment_inference"
    ),
}

OUTPUT_FIELDS = [
    "checklist_id",
    "capture_task_id",
    "route_result_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "capture_scaffold_path",
    "route_results_path",
    "source_route_path",
    "required_review_checks",
    "required_route_files_to_open",
    "checklist_status",
    "evidence_collection_status",
    "capture_status",
    "identity_claim_status",
    "assignment_status",
    "promotion_status",
    "rights_decision_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _route_files_to_open(row: dict[str, str]) -> str:
    return ";".join(
        [
            CAPTURE_SCAFFOLD.as_posix(),
            ROUTE_RESULTS.as_posix(),
            row["source_route_path"],
        ]
    )


def build_review_checklist(capture_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    checklist: list[dict[str, str]] = []
    for row in capture_rows:
        target_section = row["target_evidence_section"]
        if target_section not in SECTION_REVIEW_CHECKS:
            raise ValueError(f"unsupported target_evidence_section: {target_section}")
        checklist.append(
            {
                "checklist_id": (
                    "hust-obc-undeciphered-capture-review-checklist-"
                    f"{len(checklist) + 1:04d}"
                ),
                "capture_task_id": row["capture_task_id"],
                "route_result_id": row["route_result_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "target_evidence_section": target_section,
                "capture_scaffold_path": CAPTURE_SCAFFOLD.as_posix(),
                "route_results_path": ROUTE_RESULTS.as_posix(),
                "source_route_path": row["source_route_path"],
                "required_review_checks": SECTION_REVIEW_CHECKS[target_section],
                "required_route_files_to_open": _route_files_to_open(row),
                "checklist_status": CHECKLIST_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "capture_status": CAPTURE_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "promotion_status": PROMOTION_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return checklist


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-scaffold", default=str(CAPTURE_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_review_checklist(read_csv_rows(root / args.capture_scaffold))
    write_csv(root / args.output, rows)
    print(
        f"checklist_row_count={len(rows)} "
        "checklist_status=not_started "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
