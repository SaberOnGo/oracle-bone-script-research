#!/usr/bin/env python3
"""Capture candidate-packet metadata for codepoint crosswalk evidence tasks."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


EVIDENCE_CAPTURE_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "044_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-capture-scaffold.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "047_ai-agent-hust-obimd-evobc-codepoint-crosswalk-candidate-packet-capture-results.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "codepoint_crosswalk_candidate_packet_capture_result_not_scholarship"
CANDIDATE_PACKET_ROW_STATUS = "reviewed_candidate_packet_file_found"
CANDIDATE_PACKET_EVIDENCE_STATUS = "metadata_captured_from_reviewed_candidate_packet"
EVIDENCE_COLLECTION_STATUS = "candidate_packet_metadata_captured"
RIGHTS_DECISION_STATUS = "packet_value_captured_no_new_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
DECIPHERMENT_CLAIM_STATUS = "no_claim"
COMPONENT_CLAIM_STATUS = "no_claim"
EVOLUTION_CHAIN_CLAIM_STATUS = "no_claim"
CROSS_SOURCE_REFERENCE_STATUS = "route_refs_recorded_for_later_review_not_identity_claim"
CAPTURE_STATUS = "reviewed_metadata_only"
CAUTION = (
    "This row captures local candidate-packet metadata for later evidence review. "
    "It copies HUST-OBC candidate-packet fields and records the 044 cross-source "
    "route refs only as later-review pointers; it is not an oracle-character "
    "identity decision, not an accepted reading, not a component assignment, not "
    "an evolution-chain assignment, not a new rights decision, not a source "
    "promotion, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "capture_result_id",
    "capture_task_id",
    "route_result_id",
    "review_log_draft_id",
    "codepoint_review_task_id",
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "candidate_packet_path",
    "candidate_packet_row_status",
    "candidate_packet_id_evidence_value",
    "record_type_evidence_value",
    "source_id_evidence_value",
    "preferred_directory_name_evidence_value",
    "primary_external_ref_id_evidence_value",
    "source_candidate_promotion_queue_id_evidence_value",
    "source_candidate_class_id_evidence_value",
    "source_candidate_validation_class_id_evidence_value",
    "source_candidate_source_category_id_evidence_value",
    "source_candidate_source_category_id_padded_evidence_value",
    "source_candidate_label_crosswalk_id_evidence_value",
    "source_candidate_source_category_row_ids_evidence_value",
    "dataset_label_status_evidence_value",
    "dataset_label_source_modern_label_codepoints_evidence_value",
    "dataset_label_component_count_evidence_value",
    "dataset_label_has_multi_component_label_evidence_value",
    "dataset_label_source_category_member_count_evidence_value",
    "decipherment_status_evidence_value",
    "assignment_status_evidence_value",
    "promotion_status_evidence_value",
    "packet_status_evidence_value",
    "required_next_review_evidence_value",
    "external_reference_ids_evidence_value",
    "evidence_download_ids_evidence_value",
    "source_metadata_files_evidence_value",
    "route_file_count_evidence_value",
    "rights_status_evidence_value",
    "review_status_evidence_value",
    "candidate_packet_research_boundary_evidence_value",
    "candidate_packet_caution_evidence_value",
    "packet_updated_at_evidence_value",
    "route_cross_source_refs_evidence_value",
    "candidate_packet_evidence_status",
    "evidence_collection_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "cross_source_reference_status",
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _compact_list(values: list[Any]) -> str:
    return ";".join(str(value) for value in values if value is not None and str(value))


def _external_reference_ids(packet: dict[str, Any]) -> str:
    refs = packet.get("external_references", [])
    return _compact_list(ref.get("external_ref_id", "") for ref in refs)


def _candidate_packet_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = [row for row in rows if row.get("target_evidence_section") == "candidate_packet"]
    tasks.sort(key=lambda row: row["capture_task_id"])
    return tasks


def _summary(parts: dict[str, str]) -> str:
    return ";".join(f"{key}={value}" for key, value in parts.items())


def _capture_row(
    index: int,
    task: dict[str, str],
    packet: dict[str, Any],
) -> dict[str, str]:
    source_candidate = packet["source_candidate"]
    dataset_label = packet["dataset_label"]
    route_files = packet.get("route_files", [])
    return {
        "capture_result_id": f"codepoint-candidate-packet-capture-result-{index:03d}",
        "capture_task_id": task["capture_task_id"],
        "route_result_id": task["route_result_id"],
        "review_log_draft_id": task["review_log_draft_id"],
        "codepoint_review_task_id": task["codepoint_review_task_id"],
        "crosswalk_candidate_id": task["crosswalk_candidate_id"],
        "suggested_oracle_character_id": task["suggested_oracle_character_id"],
        "candidate_packet_path": task["source_route_path"],
        "candidate_packet_row_status": CANDIDATE_PACKET_ROW_STATUS,
        "candidate_packet_id_evidence_value": packet["candidate_packet_id"],
        "record_type_evidence_value": packet["record_type"],
        "source_id_evidence_value": packet["source_id"],
        "preferred_directory_name_evidence_value": packet["preferred_directory_name"],
        "primary_external_ref_id_evidence_value": packet["primary_external_ref_id"],
        "source_candidate_promotion_queue_id_evidence_value": source_candidate["promotion_queue_id"],
        "source_candidate_class_id_evidence_value": source_candidate["candidate_class_id"],
        "source_candidate_validation_class_id_evidence_value": source_candidate["validation_class_id"],
        "source_candidate_source_category_id_evidence_value": source_candidate["source_category_id"],
        "source_candidate_source_category_id_padded_evidence_value": source_candidate[
            "source_category_id_padded"
        ],
        "source_candidate_label_crosswalk_id_evidence_value": source_candidate[
            "candidate_label_crosswalk_id"
        ],
        "source_candidate_source_category_row_ids_evidence_value": _compact_list(
            source_candidate.get("source_category_row_ids", [])
        ),
        "dataset_label_status_evidence_value": dataset_label["status"],
        "dataset_label_source_modern_label_codepoints_evidence_value": dataset_label[
            "source_modern_label_codepoints"
        ],
        "dataset_label_component_count_evidence_value": dataset_label["label_component_count"],
        "dataset_label_has_multi_component_label_evidence_value": dataset_label[
            "has_multi_component_label"
        ],
        "dataset_label_source_category_member_count_evidence_value": dataset_label[
            "source_category_member_count"
        ],
        "decipherment_status_evidence_value": packet["decipherment_status"],
        "assignment_status_evidence_value": packet["assignment_status"],
        "promotion_status_evidence_value": packet["promotion_status"],
        "packet_status_evidence_value": packet["packet_status"],
        "required_next_review_evidence_value": packet["required_next_review"],
        "external_reference_ids_evidence_value": _external_reference_ids(packet),
        "evidence_download_ids_evidence_value": _compact_list(packet.get("evidence_download_ids", [])),
        "source_metadata_files_evidence_value": _compact_list(packet.get("source_metadata_files", [])),
        "route_file_count_evidence_value": str(len(route_files)),
        "rights_status_evidence_value": packet["rights_status"],
        "review_status_evidence_value": packet["review_status"],
        "candidate_packet_research_boundary_evidence_value": packet["research_boundary"],
        "candidate_packet_caution_evidence_value": packet["caution"],
        "packet_updated_at_evidence_value": packet["updated_at"],
        "route_cross_source_refs_evidence_value": task["source_record_refs"],
        "candidate_packet_evidence_status": CANDIDATE_PACKET_EVIDENCE_STATUS,
        "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
        "rights_decision_status": RIGHTS_DECISION_STATUS,
        "source_promotion_status": SOURCE_PROMOTION_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
        "component_claim_status": COMPONENT_CLAIM_STATUS,
        "evolution_chain_claim_status": EVOLUTION_CHAIN_CLAIM_STATUS,
        "cross_source_reference_status": CROSS_SOURCE_REFERENCE_STATUS,
        "capture_status": CAPTURE_STATUS,
        "captured_metadata_summary": _summary(
            {
                "route_result_id": task["route_result_id"],
                "capture_task_id": task["capture_task_id"],
                "candidate_packet_id": packet["candidate_packet_id"],
                "source_candidate_class_id": source_candidate["candidate_class_id"],
                "validation_class_id": source_candidate["validation_class_id"],
                "source_category_id_padded": source_candidate["source_category_id_padded"],
                "dataset_label_codepoints": dataset_label["source_modern_label_codepoints"],
                "packet_status": packet["packet_status"],
                "rights_status": packet["rights_status"],
                "review_status": packet["review_status"],
            }
        ),
        "required_next_checks": (
            "open_candidate_packet;verify_hust_candidate_fields_against_staging;"
            "cross_check_obimd_evobc_source_register_and_download_log_before_evidence_promotion"
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_capture_results(
    capture_scaffold_rows: list[dict[str, str]],
    root: Path,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for task in _candidate_packet_tasks(capture_scaffold_rows):
        packet_path = root / task["source_route_path"]
        if not packet_path.exists():
            raise FileNotFoundError(packet_path)
        packet = read_json(packet_path)
        rows.append(_capture_row(len(rows) + 1, task, packet))
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
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_results(
        read_csv_rows(root / args.capture_scaffold),
        root,
    )
    write_csv(root / args.output, rows)
    print(
        f"capture_result_count={len(rows)} "
        f"candidate_packet_count={len({row['candidate_packet_id_evidence_value'] for row in rows})} "
        f"output={(root / args.output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
