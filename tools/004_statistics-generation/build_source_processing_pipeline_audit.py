#!/usr/bin/env python3
"""Build a source-level processing pipeline audit.

This audit shows how far each registered source has progressed through
provenance, download/access logging, checksum/size recording, field mapping,
manifesting, derived records, graph links, and review routing. It is a
preprocessing control surface only and does not promote any research claim.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/094_source-processing-pipeline-audit.csv")
OUTPUT_JSON = Path("corpus/009_statistics-and-derived-features/095_source-processing-pipeline-summary.json")
UPDATED_AT = "2026-06-19"
CAUTION = (
    "Source processing pipeline audit only; derived counts and graph links are "
    "provenance and routing infrastructure, not decipherment or identity claims."
)

SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
SOURCE_FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
HUST_PROMOTION_QUEUE = Path("corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv")
UNDECIPHERED_INDEX = Path("corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv")
HUST_CODEPOINT_CROSSWALK = Path("corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv")
SOURCE_ROUTE_REVIEW_QUEUE = Path("corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv")
GRAPH_EDGE_FILES = [
    Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def count_by_field(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row.get(field, "") for row in rows if row.get(field, ""))


def count_assets_by_source(asset_rows: list[dict[str, str]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in asset_rows:
        for source_id in split_values(row.get("source_ids", "")):
            counts[source_id] += 1
    return counts


def graph_counts_by_source(root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in GRAPH_EDGE_FILES:
        with (root / path).open("r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    continue
                edge = json.loads(stripped)
                for source_id in edge.get("source_ids", []):
                    counts[str(source_id)] += 1
    return counts


def downloaded_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("status", "").startswith("downloaded"))


def access_boundary_count(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if "access_restricted" in row.get("status", "") or row.get("status") == "download_error"
    )


def checksum_present_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("checksum_sha256", ""))


def size_recorded_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if row.get("file_size_bytes", "").isdigit())


def stage_for(
    *,
    source_registered: bool,
    download_log_count: int,
    downloaded_rows: int,
    field_map_count: int,
    package_manifest_count: int,
    metadata_profile_count: int,
    asset_count: int,
    candidate_queue_count: int,
    graph_edge_count: int,
    route_review_count: int,
) -> str:
    if route_review_count and (graph_edge_count or candidate_queue_count or asset_count or metadata_profile_count):
        return "pending_human_review"
    if graph_edge_count:
        return "linked"
    if candidate_queue_count or asset_count or metadata_profile_count or package_manifest_count:
        return "structured"
    if field_map_count:
        return "cleaned"
    if downloaded_rows:
        return "downloaded"
    if download_log_count:
        return "discovered_access_boundary_or_error"
    if source_registered:
        return "registered"
    return "not_found"


def next_action_for(row: dict[str, str]) -> str:
    graph_edges = int(row["graph_edge_count"])
    candidate_rows = int(row["candidate_queue_count"])
    access_boundaries = int(row["access_boundary_or_error_count"])
    route_reviews = int(row["source_route_review_queue_count"])
    metadata_profiles = int(row["metadata_profile_count"])
    download_logs = int(row["download_log_count"])
    if graph_edges or candidate_rows:
        return "open_review_route_and_collect_source_marked_evidence_without_promoting_candidates"
    if access_boundaries:
        return "manual_or_institutional_access_followup_keep_metadata_only"
    if metadata_profiles:
        return "review_metadata_profile_and_decide_safe_derived_record_promotion"
    if download_logs:
        return "review_download_log_size_checksum_rights_and_extract_metadata"
    if route_reviews:
        return "open_source_route_review_queue"
    return "prepare_or_refresh_download_manifest_and_field_map"


def build_pipeline_rows(root: Path) -> list[dict[str, str]]:
    source_rows = read_csv_rows(root / SOURCE_INDEX)
    manifest_rows = read_csv_rows(root / SOURCE_DOWNLOAD_MANIFEST)
    download_log_rows = read_csv_rows(root / SOURCE_DOWNLOAD_LOG)
    field_map_rows = read_csv_rows(root / SOURCE_FIELD_MAP)
    package_manifest_rows = read_csv_rows(root / SOURCE_PACKAGE_FILE_MANIFEST)
    metadata_profile_rows = read_csv_rows(root / DOWNLOADED_METADATA_PROFILE)
    asset_rows = read_csv_rows(root / ASSET_SOURCE_INDEX)
    promotion_rows = read_csv_rows(root / HUST_PROMOTION_QUEUE)
    undeciphered_rows = read_csv_rows(root / UNDECIPHERED_INDEX)
    codepoint_rows = read_csv_rows(root / HUST_CODEPOINT_CROSSWALK)
    route_review_rows = read_csv_rows(root / SOURCE_ROUTE_REVIEW_QUEUE)

    manifest_counts = count_by_field(manifest_rows, "source_id")
    field_map_counts = count_by_field(field_map_rows, "source_id")
    package_manifest_counts = count_by_field(package_manifest_rows, "source_id")
    metadata_profile_counts = count_by_field(metadata_profile_rows, "source_id")
    large_source_counts: Counter[str] = Counter()
    large_source_packages_by_source: dict[str, set[str]] = {}
    for row in package_manifest_rows:
        source_id = row.get("source_id", "")
        source_package_id = row.get("source_package_id", "")
        if source_id and source_package_id:
            large_source_packages_by_source.setdefault(source_id, set()).add(source_package_id)
    for source_id, source_package_ids in large_source_packages_by_source.items():
        large_source_counts[source_id] = len(source_package_ids)
    asset_counts = count_assets_by_source(asset_rows)
    graph_counts = graph_counts_by_source(root)
    route_review_counts = count_by_field(route_review_rows, "source_id")

    download_rows_by_source: dict[str, list[dict[str, str]]] = {}
    for row in download_log_rows:
        download_rows_by_source.setdefault(row.get("source_id", ""), []).append(row)

    candidate_counts = Counter(row.get("source_id", "") for row in promotion_rows)
    candidate_counts.update(row.get("source_id", "") for row in undeciphered_rows)
    crosswalk_match_counts = Counter()
    for row in codepoint_rows:
        for source_id in split_values(row.get("matched_source_ids", "")):
            crosswalk_match_counts[source_id] += 1

    output_rows: list[dict[str, str]] = []
    for index, source in enumerate(sorted(source_rows, key=lambda item: item["source_id"]), start=1):
        source_id = source["source_id"]
        source_download_rows = download_rows_by_source.get(source_id, [])
        current_stage = stage_for(
            source_registered=True,
            download_log_count=len(source_download_rows),
            downloaded_rows=downloaded_count(source_download_rows),
            field_map_count=field_map_counts[source_id],
            package_manifest_count=package_manifest_counts[source_id],
            metadata_profile_count=metadata_profile_counts[source_id],
            asset_count=asset_counts[source_id],
            candidate_queue_count=candidate_counts[source_id],
            graph_edge_count=graph_counts[source_id],
            route_review_count=route_review_counts[source_id],
        )
        row = {
            "pipeline_row_id": f"source-pipeline-{index:03d}",
            "source_id": source_id,
            "source_type": source["source_type"],
            "authority_tier": source["authority_tier"],
            "adoption_status": source["adoption_status"],
            "rights_status": source["rights_status"],
            "source_review_status": source["review_status"],
            "download_manifest_count": str(manifest_counts[source_id]),
            "download_log_count": str(len(source_download_rows)),
            "downloaded_count": str(downloaded_count(source_download_rows)),
            "access_boundary_or_error_count": str(access_boundary_count(source_download_rows)),
            "checksum_present_count": str(checksum_present_count(source_download_rows)),
            "size_recorded_count": str(size_recorded_count(source_download_rows)),
            "field_map_count": str(field_map_counts[source_id]),
            "large_source_register_count": str(large_source_counts[source_id]),
            "package_manifest_count": str(package_manifest_counts[source_id]),
            "metadata_profile_count": str(metadata_profile_counts[source_id]),
            "asset_count": str(asset_counts[source_id]),
            "candidate_queue_count": str(candidate_counts[source_id]),
            "cross_source_crosswalk_match_count": str(crosswalk_match_counts[source_id]),
            "graph_edge_count": str(graph_counts[source_id]),
            "source_route_review_queue_count": str(route_review_counts[source_id]),
            "download_status_counts": compact_counter(Counter(row.get("status", "") for row in source_download_rows)),
            "current_stage": current_stage,
            "next_entry_path": "corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv",
            "next_action": "",
            "caution": CAUTION,
            "updated_at": UPDATED_AT,
        }
        row["next_action"] = next_action_for(row)
        output_rows.append(row)
    return output_rows


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    stage_counts = Counter(row["current_stage"] for row in rows)
    authority_counts = Counter(row["authority_tier"] for row in rows)
    rights_counts = Counter(row["rights_status"] for row in rows)
    totals = Counter()
    for row in rows:
        for field in [
            "download_manifest_count",
            "download_log_count",
            "downloaded_count",
            "access_boundary_or_error_count",
            "checksum_present_count",
            "size_recorded_count",
            "field_map_count",
            "large_source_register_count",
            "package_manifest_count",
            "metadata_profile_count",
            "asset_count",
            "candidate_queue_count",
            "cross_source_crosswalk_match_count",
            "graph_edge_count",
            "source_route_review_queue_count",
        ]:
            totals[field] += int(row[field])
    return {
        "summary_id": "source-processing-pipeline-summary-001",
        "updated_at": UPDATED_AT,
        "audit_csv_path": OUTPUT_CSV.as_posix(),
        "source_count": len(rows),
        "stage_counts": dict(sorted(stage_counts.items())),
        "authority_tier_counts": dict(sorted(authority_counts.items())),
        "rights_status_counts": dict(sorted(rights_counts.items())),
        "totals": dict(sorted(totals.items())),
        "completion_boundary": (
            "This summary audits source-level preprocessing only. A source can be "
            "well processed here while its character, component, inscription, or "
            "evolution records still remain candidates pending human review."
        ),
        "caution": CAUTION,
        "rows": rows,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
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
    rows = build_pipeline_rows(root)
    write_csv(root / args.csv_output, rows)
    write_json(root / args.json_output, build_summary(rows))
    print(f"source_pipeline_rows={len(rows)} csv={args.csv_output} json={args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
