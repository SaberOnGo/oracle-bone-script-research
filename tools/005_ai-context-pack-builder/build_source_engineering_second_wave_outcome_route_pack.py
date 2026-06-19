#!/usr/bin/env python3
"""Build a routing pack for second-wave source-engineering outcome scaffolds.

The route pack indexes the 127 outcome scaffold rows so a later reviewer can
open the right route files before filling human-reviewed outcomes. It does not
collect evidence, decide rights, promote sources, import corpus rows, or make
identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD = (
    STAT_DIR / "127_ai-agent-source-engineering-second-wave-review-outcome-scaffold.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "128_ai-agent-source-engineering-second-wave-outcome-route-pack.json"

UPDATED_AT = "2026-06-19"
ROUTE_STATUS = "not_started"
AUTOMATION_BOUNDARY = "routing_only_no_outcome_capture"
RESEARCH_BOUNDARY = "source_engineering_second_wave_outcome_route_pack_not_scholarship"
CAUTION = (
    "This second-wave source-engineering route pack is routing-only. It is not "
    "collected evidence, not a rights decision, not source promotion, not a "
    "corpus import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
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
        "route_id": f"source-engineering-second-wave-outcome-route-{index:04d}",
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
        "blocking_condition": row["blocking_condition"],
        "outcome_scaffold_path": SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD.as_posix(),
        "review_checklist_path": row["review_checklist_path"],
        "result_scaffold_path": row["result_scaffold_path"],
        "source_review_draft_manifest_path": row["source_review_draft_manifest_path"],
        "source_checklist_path": row["source_checklist_path"],
        "source_status_path": row["source_status_path"],
        "draft_path": row["draft_path"],
        "route_files_to_open": split_semicolon(row["route_files_to_open"]),
        "reserved_review_fields": split_semicolon(row["reserved_review_fields"]),
        "reserved_outcome_fields": split_semicolon(row["reserved_outcome_fields"]),
        "route_status": ROUTE_STATUS,
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


def build_route_pack(outcome_rows: list[dict[str, str]]) -> dict[str, object]:
    routes = [route_from_row(index, row) for index, row in enumerate(outcome_rows, start=1)]
    lane_counts = Counter(route["source_action_lane"] for route in routes)
    return {
        "route_pack_id": "source-engineering-second-wave-outcome-route-pack-001",
        "updated_at": UPDATED_AT,
        "outcome_scaffold_path": SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD.as_posix(),
        "route_count": len(routes),
        "source_count": len({route["source_id"] for route in routes}),
        "lane_counts": dict(sorted(lane_counts.items())),
        "route_status_counts": dict(sorted(Counter(route["route_status"] for route in routes).items())),
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
    parser = argparse.ArgumentParser(description="Build second-wave source-engineering outcome route pack.")
    parser.add_argument("--outcome-scaffold", default=str(SECOND_WAVE_REVIEW_OUTCOME_SCAFFOLD))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_route_pack(read_csv_rows(root / args.outcome_scaffold))
    write_json(root / args.output, data)
    print(f"routes={data['route_count']} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
