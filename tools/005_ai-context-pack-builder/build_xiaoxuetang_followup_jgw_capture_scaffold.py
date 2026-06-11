#!/usr/bin/env python3
"""Build a JGW follow-up capture scaffold from the first Xiaoxuetang handoff wave."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


HANDOFF_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "079_ai-agent-xiaoxuetang-followup-wave-handoff-scaffold.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "080_ai-agent-xiaoxuetang-followup-jgw-capture-scaffold.csv"
)
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "xxt_followup_jgw_capture_scaffold_not_scholarship"
OUTPUT_SCOPE = "xiaoxuetang_followup_jgw_capture_scaffold_only"

FIELDNAMES = [
    "capture_row_id",
    "handoff_item_id",
    "assignment_wave_id",
    "assignment_plan_item_id",
    "followup_task_id",
    "followup_family_id",
    "route_source_id",
    "target_source_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "targeted_download_id",
    "targeted_url",
    "review_log_draft_path",
    "source_queue_path",
    "official_access_boundary_status",
    "source_register_row_check_status",
    "download_manifest_row_check_status",
    "download_log_row_check_status",
    "full_inscription_context_note_check_status",
    "route_probe_result_check_status",
    "manual_followup_route_status",
    "catalog_availability_status",
    "catalog_availability_evidence_value",
    "heji_crosswalk_availability_status",
    "heji_crosswalk_evidence_value",
    "collection_match_availability_status",
    "collection_match_evidence_value",
    "inscription_context_availability_status",
    "inscription_context_evidence_value",
    "capture_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_scope_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "updated_at",
    "handoff_scaffold_path",
    "assignment_plan_path",
    "review_route_summary_path",
    "route_pack_path",
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


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(values: object) -> str:
    if not isinstance(values, list):
        return ""
    return ";".join(str(value) for value in values if value)


def _capture_row(index: int, item: dict[str, object]) -> dict[str, str]:
    return {
        "capture_row_id": f"xxt-jgw-followup-capture-{index:03d}",
        "handoff_item_id": str(item["handoff_item_id"]),
        "assignment_wave_id": str(item["assignment_wave_id"]),
        "assignment_plan_item_id": str(item["assignment_plan_item_id"]),
        "followup_task_id": str(item["followup_task_id"]),
        "followup_family_id": str(item["followup_family_id"]),
        "route_source_id": str(item["route_source_id"]),
        "target_source_id": str(item["target_source_id"]),
        "unknown_candidate_id": str(item["unknown_candidate_id"]),
        "primary_external_ref_id": str(item["primary_external_ref_id"]),
        "targeted_download_id": str(item["targeted_download_id"]),
        "targeted_url": str(item["targeted_url"]),
        "review_log_draft_path": str(item["review_log_draft_path"]),
        "source_queue_path": str(item["source_queue_path"]),
        "official_access_boundary_status": str(item["official_access_boundary_status"]),
        "source_register_row_check_status": "not_checked",
        "download_manifest_row_check_status": "not_checked",
        "download_log_row_check_status": "not_checked",
        "full_inscription_context_note_check_status": "not_checked",
        "route_probe_result_check_status": "not_checked",
        "manual_followup_route_status": "manual_browser_or_institutional_export_not_started",
        "catalog_availability_status": "not_checked",
        "catalog_availability_evidence_value": "",
        "heji_crosswalk_availability_status": "not_checked",
        "heji_crosswalk_evidence_value": "",
        "collection_match_availability_status": "not_checked",
        "collection_match_evidence_value": "",
        "inscription_context_availability_status": "not_checked",
        "inscription_context_evidence_value": "",
        "capture_status": "empty_scaffold_not_started",
        "human_review_status": "not_started",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "identity_claim_status": "no_identity_claim",
        "assignment_scope_status": str(item["assignment_scope_status"]),
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
        "updated_at": UPDATED_AT,
        "handoff_scaffold_path": HANDOFF_SCAFFOLD.as_posix(),
        "assignment_plan_path": str(item["assignment_plan_path"]),
        "review_route_summary_path": str(item["review_route_summary_path"]),
        "route_pack_path": str(item["route_pack_path"]),
        "route_files_to_open": _compact(item.get("route_files_to_open", [])),
        "required_review_sections": _compact(item.get("required_review_sections", [])),
        "required_next_checks": _compact(item.get("required_next_checks", [])),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "rights_status": str(item["rights_status"]),
        "risk_note": str(item["risk_note"]),
        "caution": (
            "Empty capture scaffold for first-wave Xiaoxuetang JGW follow-up only. "
            "Fill this row only after opening the handoff row and cited route files; "
            "do not use it as collected evidence, a rights decision, a catalog or "
            "collection match, a formal assignment, or not a decipherment conclusion."
        ),
    }


def build_capture_scaffold(handoff_scaffold: dict[str, object]) -> list[dict[str, str]]:
    items = list(handoff_scaffold.get("handoff_items", []))
    rows = [_capture_row(index, item) for index, item in enumerate(items, start=1)]
    if any(row["followup_family_id"] != "xxt_jgw_tls_access_boundary_followup" for row in rows):
        raise ValueError("capture scaffold only supports first-wave Xiaoxuetang JGW rows")
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff-scaffold", default=str(HANDOFF_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_capture_scaffold(read_json(root / args.handoff_scaffold))
    write_csv(root / args.output, rows)
    print(
        f"capture_row_count={len(rows)} "
        f"target_source_count={len({row['target_source_id'] for row in rows})} "
        "capture_status=empty_scaffold_not_started"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
