#!/usr/bin/env python3
"""Build a summary over source-engineering review route packs.

The summary indexes the six lane-specific route packs (111-116) so later
reviewers can choose the next source-engineering lane before recording outcomes
back into the 105 result scaffold. It is routing metadata only: no reviewed
outcomes are recorded, no rights decision is made, no source is promoted, no
corpus record is imported, and no identity or decipherment claim is made.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SOURCE_ENGINEERING_LANE_ROUTE_PACK = STAT_DIR / "107_ai-agent-source-engineering-lane-route-pack.json"
SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD = (
    STAT_DIR / "105_ai-agent-source-engineering-next-action-result-scaffold.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "117_ai-agent-source-engineering-review-route-summary.json"

ROUTE_PACK_SPECS = [
    {
        "action_lane": "access_boundary_followup",
        "path": STAT_DIR / "113_ai-agent-source-access-boundary-review-route-pack.json",
        "decision_field": "access_outcome",
    },
    {
        "action_lane": "checksum_and_download_status_review",
        "path": STAT_DIR / "114_ai-agent-source-checksum-review-route-pack.json",
        "decision_field": "checksum_outcome",
    },
    {
        "action_lane": "metadata_profile_extraction_planning",
        "path": STAT_DIR / "115_ai-agent-source-metadata-profile-review-route-pack.json",
        "decision_field": "metadata_profile_decision",
    },
    {
        "action_lane": "source_field_map_planning",
        "path": STAT_DIR / "111_ai-agent-source-field-map-review-route-pack.json",
        "decision_field": "field_map_decision",
    },
    {
        "action_lane": "package_manifest_or_not_applicable_review",
        "path": STAT_DIR / "112_ai-agent-source-package-manifest-review-route-pack.json",
        "decision_field": "manifest_decision",
    },
    {
        "action_lane": "safe_derived_record_decision",
        "path": STAT_DIR / "116_ai-agent-source-safe-derived-record-review-route-pack.json",
        "decision_field": "safe_derived_record_decision",
    },
]

SUMMARY_ID = "source-engineering-review-route-summary-001"
UPDATED_AT = "2026-06-19"
REVIEW_STATUS = "route_summary_pending_source_engineering_review"
RESEARCH_BOUNDARY = "source_engineering_review_route_summary_not_review_result"
CAUTION = (
    "Source-engineering review route summary only; it does not record reviewed "
    "outcomes, is not a corpus import, not source promotion, not a rights "
    "decision, and not an identity or decipherment claim."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def status_counts(routes: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(route_value(route, field)) for route in routes).items()))


def route_value(route: dict[str, Any], field: str) -> Any:
    if field == "result_status":
        return route.get("result_status") or route.get("field_map_result_status", "")
    if field == "evidence_collection_status":
        return route.get("evidence_collection_status") or "not_collected"
    return route.get(field, "")


def summarize_route_pack(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    data = read_json(root / spec["path"])
    routes = data.get("routes", [])
    decision_field = spec["decision_field"]
    first_route = routes[0] if routes else {}
    decision_filled_count = sum(1 for route in routes if route.get(decision_field))
    result_started_count = sum(1 for route in routes if route_value(route, "result_status") != "not_started")
    return {
        "action_lane": spec["action_lane"],
        "route_pack_id": data.get("route_pack_id", ""),
        "route_pack_path": spec["path"].as_posix(),
        "decision_field": decision_field,
        "route_count": len(routes),
        "source_count": len({route.get("source_id", "") for route in routes}),
        "priority_min": min((int(route.get("priority_rank", 0)) for route in routes), default=0),
        "priority_max": max((int(route.get("priority_rank", 0)) for route in routes), default=0),
        "gap_type_counts": status_counts(routes, "gap_type"),
        "result_status_counts": status_counts(routes, "result_status"),
        "evidence_collection_status_counts": status_counts(routes, "evidence_collection_status"),
        "human_review_status_counts": status_counts(routes, "human_review_status"),
        "rights_decision_status_counts": status_counts(routes, "rights_decision_status"),
        "source_promotion_status_counts": status_counts(routes, "source_promotion_status"),
        "corpus_import_status_counts": status_counts(routes, "corpus_import_status"),
        "decipherment_claim_status_counts": status_counts(routes, "decipherment_claim_status"),
        "decision_filled_count": decision_filled_count,
        "result_started_count": result_started_count,
        "blocking_conditions": sorted({route.get("blocking_condition", "") for route in routes if route.get("blocking_condition")}),
        "first_next_action_id": first_route.get("next_action_id", ""),
        "first_source_id": first_route.get("source_id", ""),
        "first_review_log_path": first_route.get("review_log_path", ""),
        "first_result_record_path": first_route.get("result_record_path", ""),
        "review_status": data.get("review_status", ""),
        "research_boundary": data.get("research_boundary", ""),
    }


def build_summary(root: Path) -> dict[str, Any]:
    lanes = [summarize_route_pack(root, spec) for spec in ROUTE_PACK_SPECS]
    return {
        "summary_id": SUMMARY_ID,
        "updated_at": UPDATED_AT,
        "source_paths": {
            "lane_route_pack": SOURCE_ENGINEERING_LANE_ROUTE_PACK.as_posix(),
            "next_action_result_scaffold": SOURCE_ENGINEERING_NEXT_ACTION_RESULT_SCAFFOLD.as_posix(),
            "access_boundary_route_pack": ROUTE_PACK_SPECS[0]["path"].as_posix(),
            "checksum_route_pack": ROUTE_PACK_SPECS[1]["path"].as_posix(),
            "metadata_profile_route_pack": ROUTE_PACK_SPECS[2]["path"].as_posix(),
            "field_map_route_pack": ROUTE_PACK_SPECS[3]["path"].as_posix(),
            "package_manifest_route_pack": ROUTE_PACK_SPECS[4]["path"].as_posix(),
            "safe_derived_record_route_pack": ROUTE_PACK_SPECS[5]["path"].as_posix(),
        },
        "lane_count": len(lanes),
        "route_pack_count": len(ROUTE_PACK_SPECS),
        "total_route_count": sum(lane["route_count"] for lane in lanes),
        "total_decision_filled_count": sum(lane["decision_filled_count"] for lane in lanes),
        "total_result_started_count": sum(lane["result_started_count"] for lane in lanes),
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "lanes": lanes,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering review route summary.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    data = build_summary(root)
    write_json(root / args.output, data)
    print(f"lanes={data['lane_count']} routes={data['total_route_count']} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
