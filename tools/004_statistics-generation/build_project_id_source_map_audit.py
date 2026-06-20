#!/usr/bin/env python3
"""Audit project-local ID to source-reference maps.

This is a preprocessing route audit only. It checks whether existing map rows
have source IDs, external references, rights/review statuses, and reachable
canonical paths; it does not validate identity, reading, component, evolution,
or inscription claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/190_project-id-source-map-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/191_project-id-source-map-summary.json")
UPDATED_AT = "2026-06-20"
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")

RESEARCH_BOUNDARY = (
    "project_id_source_map_audit_not_scholarship; map rows are provenance and "
    "routing infrastructure only, not identity, component, inscription, "
    "evolution, reading, or decipherment conclusions"
)

MAP_SPECS = [
    {
        "map_id": "oracle_character_id_source_map",
        "record_family": "oracle_character",
        "path": Path("project_registry/002_project-id-to-source-reference-map/001_oracle-character-id-source-map.csv"),
    },
    {
        "map_id": "oracle_inscription_id_source_map",
        "record_family": "oracle_inscription_or_crosswalk_candidate",
        "path": Path("project_registry/002_project-id-to-source-reference-map/002_oracle-inscription-id-source-map.csv"),
    },
    {
        "map_id": "asset_id_source_map",
        "record_family": "asset",
        "path": Path("project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv"),
    },
    {
        "map_id": "component_id_source_map",
        "record_family": "component_candidate",
        "path": Path("project_registry/002_project-id-to-source-reference-map/004_component-id-source-map.csv"),
    },
    {
        "map_id": "evolution_candidate_id_source_map",
        "record_family": "evolution_candidate",
        "path": Path("project_registry/002_project-id-to-source-reference-map/005_evolution-candidate-id-source-map.csv"),
    },
    {
        "map_id": "collection_object_id_source_map",
        "record_family": "collection_object_candidate",
        "path": Path("project_registry/002_project-id-to-source-reference-map/006_collection-object-id-source-map.csv"),
    },
]

FIELDNAMES = [
    "map_audit_id",
    "map_id",
    "record_family",
    "map_path",
    "row_count",
    "nonempty_map_status",
    "missing_canonical_path_count",
    "unknown_source_id_count",
    "missing_primary_external_ref_count",
    "missing_all_external_refs_count",
    "missing_source_ids_count",
    "missing_rights_status_count",
    "missing_review_status_count",
    "rights_status_counts",
    "review_status_counts",
    "source_id_counts",
    "current_stage",
    "next_entry_path",
    "next_action",
    "research_boundary",
    "decipherment_claim_status",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", ";").split(";") if item.strip()]


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def load_registered_source_ids(root: Path) -> set[str]:
    return {row.get("source_id", "") for row in read_csv_rows(root / SOURCE_INDEX) if row.get("source_id", "")}


def canonical_path_exists(root: Path, value: str) -> bool:
    if not value:
        return False
    normalized = value.replace("\\", "/")
    if normalized.startswith(("external_", "tmp/", "_tmp/", "scratch/", ".working/", ".cache/")):
        return True
    return (root / normalized).exists()


def status_for(row_count: int, issue_count: int) -> tuple[str, str, str]:
    if row_count == 0:
        return (
            "empty_by_design_or_pending_promotion",
            "registered_empty_map",
            "keep_empty_until_candidate_promotion_is_human_reviewed",
        )
    if issue_count:
        return (
            "has_rows_with_map_integrity_gaps",
            "needs_map_review",
            "repair_missing_paths_or_source_refs_before_reuse",
        )
    return (
        "has_candidate_or_asset_routes",
        "validated_route_map",
        "use_map_as_object_local_route_index_and_continue_human_review",
    )


def build_map_rows(root: Path) -> list[dict[str, str]]:
    registered_source_ids = load_registered_source_ids(root)
    audit_rows: list[dict[str, str]] = []
    for index, spec in enumerate(MAP_SPECS, start=1):
        rows = read_csv_rows(root / spec["path"])
        rights_counts = Counter(row.get("rights_status", "") for row in rows if row.get("rights_status", ""))
        review_counts = Counter(row.get("review_status", "") for row in rows if row.get("review_status", ""))
        source_counts: Counter[str] = Counter()
        missing_canonical_path_count = 0
        unknown_source_id_count = 0
        missing_primary_external_ref_count = 0
        missing_all_external_refs_count = 0
        missing_source_ids_count = 0
        missing_rights_status_count = 0
        missing_review_status_count = 0

        for row in rows:
            if not canonical_path_exists(root, row.get("canonical_path", "")):
                missing_canonical_path_count += 1
            if not row.get("primary_external_ref_id", ""):
                missing_primary_external_ref_count += 1
            if not row.get("all_external_ref_ids", ""):
                missing_all_external_refs_count += 1
            source_ids = split_values(row.get("source_ids", ""))
            if not source_ids:
                missing_source_ids_count += 1
            for source_id in source_ids:
                source_counts[source_id] += 1
                if source_id not in registered_source_ids:
                    unknown_source_id_count += 1
            if not row.get("rights_status", ""):
                missing_rights_status_count += 1
            if not row.get("review_status", ""):
                missing_review_status_count += 1

        issue_count = (
            missing_canonical_path_count
            + unknown_source_id_count
            + missing_primary_external_ref_count
            + missing_all_external_refs_count
            + missing_source_ids_count
            + missing_rights_status_count
            + missing_review_status_count
        )
        nonempty_map_status, current_stage, next_action = status_for(len(rows), issue_count)
        audit_rows.append(
            {
                "map_audit_id": f"project-id-source-map-audit-{index:03d}",
                "map_id": str(spec["map_id"]),
                "record_family": str(spec["record_family"]),
                "map_path": spec["path"].as_posix(),
                "row_count": str(len(rows)),
                "nonempty_map_status": nonempty_map_status,
                "missing_canonical_path_count": str(missing_canonical_path_count),
                "unknown_source_id_count": str(unknown_source_id_count),
                "missing_primary_external_ref_count": str(missing_primary_external_ref_count),
                "missing_all_external_refs_count": str(missing_all_external_refs_count),
                "missing_source_ids_count": str(missing_source_ids_count),
                "missing_rights_status_count": str(missing_rights_status_count),
                "missing_review_status_count": str(missing_review_status_count),
                "rights_status_counts": compact_counter(rights_counts),
                "review_status_counts": compact_counter(review_counts),
                "source_id_counts": compact_counter(source_counts),
                "current_stage": current_stage,
                "next_entry_path": spec["path"].as_posix(),
                "next_action": next_action,
                "research_boundary": RESEARCH_BOUNDARY,
                "decipherment_claim_status": "no_claim",
                "updated_at": UPDATED_AT,
            }
        )
    return audit_rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    stage_counts = Counter(row["current_stage"] for row in rows)
    record_family_counts = Counter(row["record_family"] for row in rows)
    totals = {
        "row_count": sum(int(row["row_count"]) for row in rows),
        "missing_canonical_path_count": sum(int(row["missing_canonical_path_count"]) for row in rows),
        "unknown_source_id_count": sum(int(row["unknown_source_id_count"]) for row in rows),
        "missing_primary_external_ref_count": sum(int(row["missing_primary_external_ref_count"]) for row in rows),
        "missing_all_external_refs_count": sum(int(row["missing_all_external_refs_count"]) for row in rows),
        "missing_source_ids_count": sum(int(row["missing_source_ids_count"]) for row in rows),
        "missing_rights_status_count": sum(int(row["missing_rights_status_count"]) for row in rows),
        "missing_review_status_count": sum(int(row["missing_review_status_count"]) for row in rows),
    }
    return {
        "summary_id": "project-id-source-map-summary-001",
        "updated_at": UPDATED_AT,
        "audit_csv_path": OUTPUT_CSV.as_posix(),
        "map_count": len(rows),
        "total_row_count": totals["row_count"],
        "stage_counts": dict(sorted(stage_counts.items())),
        "record_family_counts": dict(sorted(record_family_counts.items())),
        "totals": totals,
        "completion_boundary": (
            "This summary validates preprocessing route-map integrity only. "
            "It does not start formal decipherment research, promote source rows, "
            "or confirm candidate identities."
        ),
        "research_boundary": RESEARCH_BOUNDARY,
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    parser.add_argument("--json-output", default=str(OUTPUT_JSON))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_map_rows(root)
    write_csv(root / args.csv_output, rows)
    write_json(root / args.json_output, build_summary(rows))
    print(f"project_id_source_map_audit_rows={len(rows)} csv={args.csv_output} json={args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
