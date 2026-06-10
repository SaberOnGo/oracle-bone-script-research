#!/usr/bin/env python3
"""Build a source-register evidence capture scaffold from the first handoff wave."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


HANDOFF_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/"
    "031_ai-agent-graph-source-evidence-collection-wave-handoff-scaffold.json"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "032_ai-agent-graph-source-source-register-evidence-capture-scaffold.csv"
)
SOURCE_REGISTER_PATH = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-evobc", "src-obimd"]
RESEARCH_BOUNDARY = "evidence_collection_source_register_capture_scaffold_not_scholarship"
OUTPUT_SCOPE = "graph_source_evidence_collection_source_register_capture_scaffold_only"

FIELDNAMES = [
    "capture_row_id",
    "handoff_item_id",
    "assignment_wave_id",
    "assignment_plan_item_id",
    "evidence_collection_review_task_id",
    "evidence_collection_result_id",
    "evidence_collection_task_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "target_evidence_section",
    "source_register_path",
    "source_register_row_status",
    "source_id_evidence_value",
    "primary_external_ref_evidence_value",
    "source_title_evidence_value",
    "source_type_evidence_value",
    "rights_status_evidence_value",
    "risk_note_evidence_value",
    "review_status_evidence_value",
    "evidence_collection_status",
    "source_register_evidence_status",
    "rights_decision_status",
    "source_promotion_status",
    "decipherment_claim_status",
    "capture_status",
    "updated_at",
    "result_update_target_path",
    "note_draft_path",
    "route_pack_path",
    "manifest_path",
    "task_queue_source_path",
    "handoff_scaffold_path",
    "route_files_to_open",
    "required_review_checks",
    "counter_source_ids_to_check",
    "research_boundary",
    "output_scope",
    "caution",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_index(source_id: str) -> int:
    try:
        return SOURCE_ORDER.index(source_id)
    except ValueError:
        return len(SOURCE_ORDER)


def _compact(values: object) -> str:
    if not isinstance(values, list):
        return ""
    return ";".join(str(value) for value in values if value)


def _capture_row(index: int, item: dict[str, object]) -> dict[str, str]:
    return {
        "capture_row_id": f"graph-source-evidence-source-register-capture-{index:03d}",
        "handoff_item_id": str(item["handoff_item_id"]),
        "assignment_wave_id": str(item["assignment_wave_id"]),
        "assignment_plan_item_id": str(item["assignment_plan_item_id"]),
        "evidence_collection_review_task_id": str(
            item["evidence_collection_review_task_id"]
        ),
        "evidence_collection_result_id": str(item["evidence_collection_result_id"]),
        "evidence_collection_task_id": str(item["evidence_collection_task_id"]),
        "source_id": str(item["source_id"]),
        "primary_review_record_id": str(item["primary_review_record_id"]),
        "primary_external_ref_id": str(item["primary_external_ref_id"]),
        "source_record_id": str(item["source_record_id"]),
        "target_evidence_section": str(item["target_evidence_section"]),
        "source_register_path": SOURCE_REGISTER_PATH,
        "source_register_row_status": "not_checked",
        "source_id_evidence_value": "",
        "primary_external_ref_evidence_value": "",
        "source_title_evidence_value": "",
        "source_type_evidence_value": "",
        "rights_status_evidence_value": "",
        "risk_note_evidence_value": "",
        "review_status_evidence_value": "",
        "evidence_collection_status": "not_collected",
        "source_register_evidence_status": "not_collected",
        "rights_decision_status": "not_decided",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
        "capture_status": "empty_scaffold_not_started",
        "updated_at": UPDATED_AT,
        "result_update_target_path": str(item["result_update_target_path"]),
        "note_draft_path": str(item["note_draft_path"]),
        "route_pack_path": str(item["route_pack_path"]),
        "manifest_path": str(item["manifest_path"]),
        "task_queue_source_path": str(item["task_queue_source_path"]),
        "handoff_scaffold_path": HANDOFF_SCAFFOLD.as_posix(),
        "route_files_to_open": _compact(item.get("route_files_to_open", [])),
        "required_review_checks": _compact(item.get("required_review_checks", [])),
        "counter_source_ids_to_check": _compact(
            item.get("counter_source_ids_to_check", [])
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "output_scope": OUTPUT_SCOPE,
        "caution": (
            "Empty capture scaffold for source-register evidence only. Fill this "
            "row only after opening the source register and cited route files; do "
            "not use it as collected evidence, a rights decision, source "
            "promotion, or a decipherment conclusion."
        ),
    }


def build_capture_scaffold(handoff_scaffold: dict[str, object]) -> list[dict[str, str]]:
    items = list(handoff_scaffold.get("handoff_items", []))
    items.sort(key=lambda item: _source_index(str(item.get("source_id", ""))))
    rows = [_capture_row(index, item) for index, item in enumerate(items, start=1)]
    if any(row["target_evidence_section"] != "source_register" for row in rows):
        raise ValueError("capture scaffold only supports source_register rows")
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
        f"source_count={len({row['source_id'] for row in rows})} "
        "capture_status=empty_scaffold_not_started"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
