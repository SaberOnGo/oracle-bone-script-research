#!/usr/bin/env python3
"""Build a route summary for second-wave handoff review checklists.

The summary indexes the 130 checklist rows by source and lane for later human
review. It does not collect evidence, record outcomes, decide rights, promote
sources, import corpus rows, or make identity, component, evolution, or
decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST = (
    STAT_DIR / "130_ai-agent-source-engineering-second-wave-handoff-review-checklist.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "131_ai-agent-source-engineering-second-wave-handoff-route-summary.json"

UPDATED_AT = "2026-06-19"
AUTOMATION_BOUNDARY = "route_summary_only_no_outcome_capture"
RESEARCH_BOUNDARY = "source_engineering_second_wave_handoff_route_summary_not_scholarship"
CAUTION = (
    "This second-wave source-engineering handoff route summary is routing-only. "
    "It is not collected evidence, not a reviewed outcome, not a rights decision, "
    "not source promotion, not a corpus import, not an identity claim, not a "
    "component assignment, not an evolution-chain assignment, and not a "
    "decipherment conclusion."
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
        "summary_route_id": f"source-engineering-second-wave-handoff-summary-route-{index:04d}",
        "handoff_review_checklist_path": SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST.as_posix(),
        "handoff_review_checklist_id": row["handoff_review_checklist_id"],
        "handoff_id": row["handoff_id"],
        "route_id": row["route_id"],
        "second_wave_review_outcome_scaffold_id": row["second_wave_review_outcome_scaffold_id"],
        "second_wave_review_checklist_id": row["second_wave_review_checklist_id"],
        "second_wave_result_scaffold_id": row["second_wave_result_scaffold_id"],
        "review_draft_id": row["review_draft_id"],
        "continuation_task_id": row["continuation_task_id"],
        "source_status_id": row["source_status_id"],
        "source_id": row["source_id"],
        "source_action_lane": row["source_action_lane"],
        "source_first_wave_status": row["source_first_wave_status"],
        "priority_rank": row["priority_rank"],
        "priority_tags": split_semicolon(row["priority_tags"]),
        "required_result_action": row["required_result_action"],
        "required_review_steps": split_semicolon(row["required_review_steps"]),
        "required_precheck_steps": split_semicolon(row["required_precheck_steps"]),
        "blocking_condition": row["blocking_condition"],
        "handoff_scaffold_path": row["handoff_scaffold_path"],
        "route_pack_path": row["route_pack_path"],
        "outcome_scaffold_path": row["outcome_scaffold_path"],
        "review_checklist_path": row["review_checklist_path"],
        "result_scaffold_path": row["result_scaffold_path"],
        "source_review_draft_manifest_path": row["source_review_draft_manifest_path"],
        "source_checklist_path": row["source_checklist_path"],
        "source_status_path": row["source_status_path"],
        "draft_path": row["draft_path"],
        "route_files_to_open": split_semicolon(row["route_files_to_open"]),
        "reserved_review_fields": split_semicolon(row["reserved_review_fields"]),
        "reserved_outcome_fields": split_semicolon(row["reserved_outcome_fields"]),
        "checklist_status": row["checklist_status"],
        "assignment_status": row["assignment_status"],
        "handoff_status": row["handoff_status"],
        "route_status": row["route_status"],
        "review_outcome_status": row["review_outcome_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "reviewed_evidence_paths": row["reviewed_evidence_paths"],
        "reviewed_outcome_summary": row["reviewed_outcome_summary"],
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


def build_route_summary(checklist_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(checklist_rows, start=1)]
    lane_counts = Counter(route["source_action_lane"] for route in routes)
    source_counts = Counter(route["source_id"] for route in routes)
    return {
        "route_summary_id": "source-engineering-second-wave-handoff-route-summary-001",
        "updated_at": UPDATED_AT,
        "handoff_review_checklist_path": SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST.as_posix(),
        "route_count": len(routes),
        "source_count": len(source_counts),
        "lane_counts": dict(sorted(lane_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "checklist_status_counts": dict(sorted(Counter(route["checklist_status"] for route in routes).items())),
        "assignment_status_counts": dict(sorted(Counter(route["assignment_status"] for route in routes).items())),
        "handoff_status_counts": dict(sorted(Counter(route["handoff_status"] for route in routes).items())),
        "review_outcome_status_counts": dict(
            sorted(Counter(route["review_outcome_status"] for route in routes).items())
        ),
        "human_review_status_counts": dict(sorted(Counter(route["human_review_status"] for route in routes).items())),
        "automation_boundary": AUTOMATION_BOUNDARY,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "routes": routes,
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build second-wave handoff route summary.")
    parser.add_argument("--checklist", default=str(SECOND_WAVE_HANDOFF_REVIEW_CHECKLIST))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_summary(read_csv_rows(root / args.checklist))
    write_json(root / args.output, data)
    print(f"handoff_summary_routes={data['route_count']} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
