#!/usr/bin/env python3
"""Build source coverage statistics from reviewed registry and derived rows."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/001_relationship-graph-edge-type-summary.csv"
)
HUST_OBC_OBS_CHAR_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"
)
DEFAULT_OUTPUT = Path("corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv")
UPDATED_AT = "2026-06-10"
GENERATED_FROM = (
    "source_registers;download_manifest;download_log;metadata_profiles;"
    "asset_source_index;relationship_graph_statistics;hust_obc_promotion_queue"
)
CAUTION = (
    "Coverage statistics only; inspect source register rows and source-specific "
    "derived records before reuse or research interpretation."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def compact_counter(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def split_source_ids(value: str) -> list[str]:
    return [source_id for source_id in value.split(";") if source_id]


def coverage_status(row: dict[str, str]) -> str:
    if int(row["committed_asset_count"]) > 0:
        return "has_committed_public_asset_or_metadata"
    if int(row["graph_edge_count"]) > 0:
        return "has_relationship_graph_derivatives"
    if int(row["promotion_queue_candidate_count"]) > 0:
        return "has_candidate_review_queue"
    if int(row["metadata_profile_metric_count"]) > 0:
        return "has_downloaded_metadata_profile"
    if int(row["download_log_count"]) > 0:
        return "has_download_log_only"
    if int(row["download_manifest_count"]) > 0:
        return "has_download_plan_only"
    return "registered_source_only"


def build_source_coverage_summary(root: Path) -> list[dict[str, str]]:
    source_rows = read_csv_rows(root / SOURCE_INDEX)
    download_manifest_rows = read_csv_rows(root / SOURCE_DOWNLOAD_MANIFEST)
    download_log_rows = read_csv_rows(root / SOURCE_DOWNLOAD_LOG)
    metadata_profile_rows = read_csv_rows(root / DOWNLOADED_METADATA_PROFILE)
    asset_rows = read_csv_rows(root / ASSET_SOURCE_INDEX)
    graph_edge_rows = read_csv_rows(root / RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY)
    promotion_queue_rows = read_csv_rows(root / HUST_OBC_OBS_CHAR_PROMOTION_QUEUE)

    manifest_count = Counter(row["source_id"] for row in download_manifest_rows)
    download_log_count = Counter(row["source_id"] for row in download_log_rows)
    download_status_counts: dict[str, Counter[str]] = defaultdict(Counter)
    download_bytes = Counter()
    for row in download_log_rows:
        source_id = row["source_id"]
        download_status_counts[source_id][row["status"]] += 1
        file_size = row.get("file_size_bytes", "")
        if file_size.isdigit():
            download_bytes[source_id] += int(file_size)

    metadata_metric_count = Counter(row["source_id"] for row in metadata_profile_rows)
    metadata_review_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in metadata_profile_rows:
        metadata_review_counts[row["source_id"]][row["review_status"]] += 1

    asset_count: Counter[str] = Counter()
    asset_bytes: Counter[str] = Counter()
    asset_rights_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in asset_rows:
        for source_id in split_source_ids(row["source_ids"]):
            asset_count[source_id] += 1
            file_size = row.get("file_size_bytes", "")
            if file_size.isdigit():
                asset_bytes[source_id] += int(file_size)
            asset_rights_counts[source_id][row["rights_status"]] += 1

    graph_edge_count: Counter[str] = Counter()
    graph_edge_type_count: dict[str, set[str]] = defaultdict(set)
    for row in graph_edge_rows:
        source_id = row["source_id"]
        edge_count = row.get("edge_count", "")
        if edge_count.isdigit():
            graph_edge_count[source_id] += int(edge_count)
        graph_edge_type_count[source_id].add(row["edge_type"])

    promotion_candidate_count = Counter(row["source_id"] for row in promotion_queue_rows)

    output_rows: list[dict[str, str]] = []
    for index, source in enumerate(sorted(source_rows, key=lambda row: row["source_id"]), start=1):
        source_id = source["source_id"]
        row = {
            "coverage_row_id": f"source-coverage-{index:03d}",
            "source_id": source_id,
            "source_type": source["source_type"],
            "authority_tier": source["authority_tier"],
            "adoption_status": source["adoption_status"],
            "rights_status": source["rights_status"],
            "source_review_status": source["review_status"],
            "download_manifest_count": str(manifest_count[source_id]),
            "download_log_count": str(download_log_count[source_id]),
            "download_status_counts": compact_counter(download_status_counts[source_id]),
            "downloaded_file_bytes": str(download_bytes[source_id]),
            "metadata_profile_metric_count": str(metadata_metric_count[source_id]),
            "metadata_profile_review_status_counts": compact_counter(metadata_review_counts[source_id]),
            "committed_asset_count": str(asset_count[source_id]),
            "committed_asset_bytes": str(asset_bytes[source_id]),
            "asset_rights_status_counts": compact_counter(asset_rights_counts[source_id]),
            "graph_edge_count": str(graph_edge_count[source_id]),
            "graph_edge_type_count": str(len(graph_edge_type_count[source_id])),
            "promotion_queue_candidate_count": str(promotion_candidate_count[source_id]),
            "coverage_status": "",
            "generated_from": GENERATED_FROM,
            "caution": CAUTION,
            "updated_at": UPDATED_AT,
        }
        row["coverage_status"] = coverage_status(row)
        output_rows.append(row)
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_source_coverage_summary(root)
    write_csv(root / args.output, rows)
    print(f"source_coverage_rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
