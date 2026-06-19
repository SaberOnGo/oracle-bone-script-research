#!/usr/bin/env python3
"""Build a route pack for source-level missing-evidence review checklists.

The route pack indexes the 150 checklist rows so a later human reviewer can
open the right draft, source files, and route IDs before filling any reviewed
outcome. It does not collect evidence, decide rights, promote sources, import
corpus rows, or make identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST = Path(
    "corpus/009_statistics-and-derived-features/"
    "150_source-pipeline-phase-action-missing-evidence-review-checklist.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "151_source-pipeline-phase-action-missing-evidence-review-route-pack.json"
)

UPDATED_AT = "2026-06-19"
ROUTE_STATUS = "not_started"
AUTOMATION_BOUNDARY = "routing_only_no_missing_evidence_outcome_capture"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_missing_evidence_review_route_pack_not_scholarship"
CAUTION = (
    "This source pipeline missing-evidence review route pack is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights "
    "decision, not source promotion, not a corpus import, not an identity "
    "claim, not a component assignment, not an evolution-chain assignment, "
    "and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def route_from_row(index: int, row: dict[str, str]) -> dict[str, object]:
    return {
        "route_id": f"source-pipeline-missing-evidence-review-route-{index:03d}",
        "review_checklist_path": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST.as_posix(),
        "review_checklist_id": row["review_checklist_id"],
        "result_scaffold_id": row["result_scaffold_id"],
        "review_draft_id": row["review_draft_id"],
        "source_summary_id": row["source_summary_id"],
        "source_id": row["source_id"],
        "source_type": row["source_type"],
        "rights_status": row["rights_status"],
        "pipeline_gap_status": row["pipeline_gap_status"],
        "missing_route_count": row["missing_route_count"],
        "missing_file_role_count": row["missing_file_role_count"],
        "missing_file_roles": split_semicolon(row["missing_file_roles"]),
        "priority_rank": row["priority_rank"],
        "priority_tags": split_semicolon(row["priority_tags"]),
        "required_review_steps": split_semicolon(row["required_review_steps"]),
        "blocking_condition": row["blocking_condition"],
        "result_scaffold_path": row["result_scaffold_path"],
        "result_update_target_path": row["result_update_target_path"],
        "review_draft_manifest_path": row["review_draft_manifest_path"],
        "draft_path": row["draft_path"],
        "source_summary_path": row["source_summary_path"],
        "route_summary_path": row["route_summary_path"],
        "route_ids": split_semicolon(row["route_ids"]),
        "missing_evidence_action_ids": split_semicolon(row["missing_evidence_action_ids"]),
        "missing_evidence_result_scaffold_ids": split_semicolon(row["missing_evidence_result_scaffold_ids"]),
        "evidence_presence_row_ids": split_semicolon(row["evidence_presence_row_ids"]),
        "files_to_open": split_semicolon(row["files_to_open"]),
        "required_review_actions": split_semicolon(row["required_review_actions"]),
        "route_status": ROUTE_STATUS,
        "assignment_status": row["assignment_status"],
        "review_status": row["review_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "reviewed_evidence_paths": "",
        "reviewed_outcome_summary": "",
        "human_review_status": row["human_review_status"],
        "rights_decision_status": row["rights_decision_status"],
        "source_promotion_status": row["source_promotion_status"],
        "corpus_import_status": row["corpus_import_status"],
        "decipherment_claim_status": row["decipherment_claim_status"],
        "identity_claim_status": row["identity_claim_status"],
        "component_claim_status": row["component_claim_status"],
        "evolution_claim_status": row["evolution_claim_status"],
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def build_route_pack(checklist_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(checklist_rows, start=1)]
    return {
        "route_pack_id": "source-pipeline-missing-evidence-review-route-pack-001",
        "updated_at": UPDATED_AT,
        "source_paths": {
            "review_checklist": SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST.as_posix(),
            "route_pack": DEFAULT_OUTPUT.as_posix(),
        },
        "route_count": len(routes),
        "source_count": len({route["source_id"] for route in routes}),
        "pipeline_gap_status_counts": dict(sorted(Counter(route["pipeline_gap_status"] for route in routes).items())),
        "route_status_counts": dict(sorted(Counter(route["route_status"] for route in routes).items())),
        "review_status_counts": dict(sorted(Counter(route["review_status"] for route in routes).items())),
        "human_review_status_counts": dict(sorted(Counter(route["human_review_status"] for route in routes).items())),
        "rights_decision_status_counts": dict(
            sorted(Counter(route["rights_decision_status"] for route in routes).items())
        ),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source pipeline missing-evidence review route pack.")
    parser.add_argument("--checklist", default=str(SOURCE_PIPELINE_PHASE_ACTION_MISSING_EVIDENCE_REVIEW_CHECKLIST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_pack(read_csv_rows(root / args.checklist))
    write_json(root / args.output, data)
    print(f"missing_evidence_review_routes={data['route_count']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
