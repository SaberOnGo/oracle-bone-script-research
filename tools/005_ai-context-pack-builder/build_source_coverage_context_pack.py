#!/usr/bin/env python3
"""Build an AI Agent source coverage context pack from source coverage statistics."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SOURCE_COVERAGE_SUMMARY = Path("corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv")
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
DEFAULT_OUTPUT = Path("corpus/009_statistics-and-derived-features/008_ai-agent-source-coverage-context-pack.json")
UPDATED_AT = "2026-06-10"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def int_value(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    if value == "":
        return 0
    return int(value)


def source_route(row: dict[str, str]) -> str:
    status = row["coverage_status"]
    if status == "has_relationship_graph_derivatives":
        return "open_graph_and_metadata_derivatives"
    if status == "has_committed_public_asset_or_metadata":
        return "open_asset_and_rights_records"
    if status == "has_downloaded_metadata_profile":
        return "open_metadata_profile_and_source_register"
    if status == "has_download_log_only":
        return "open_download_log_and_source_register"
    if status == "has_download_plan_only":
        return "open_download_manifest_before_fetching"
    return "open_source_register_first"


def source_route_zh(row: dict[str, str]) -> str:
    status = row["coverage_status"]
    if status == "has_relationship_graph_derivatives":
        return "先打开关系图谱派生记录和来源 metadata"
    if status == "has_committed_public_asset_or_metadata":
        return "先打开资产登记和权利复核记录"
    if status == "has_downloaded_metadata_profile":
        return "先打开 metadata profile 和来源登记"
    if status == "has_download_log_only":
        return "先打开下载日志和来源登记"
    if status == "has_download_plan_only":
        return "下载前先打开 download manifest"
    return "先打开来源登记"


def source_entry(row: dict[str, str]) -> dict[str, object]:
    return {
        "source_id": row["source_id"],
        "source_type": row["source_type"],
        "authority_tier": row["authority_tier"],
        "adoption_status": row["adoption_status"],
        "rights_status": row["rights_status"],
        "coverage_status": row["coverage_status"],
        "route": source_route(row),
        "route_zh": source_route_zh(row),
        "download_manifest_count": int_value(row, "download_manifest_count"),
        "download_log_count": int_value(row, "download_log_count"),
        "download_status_counts": row["download_status_counts"],
        "metadata_profile_metric_count": int_value(row, "metadata_profile_metric_count"),
        "committed_asset_count": int_value(row, "committed_asset_count"),
        "committed_asset_bytes": int_value(row, "committed_asset_bytes"),
        "asset_rights_status_counts": row["asset_rights_status_counts"],
        "graph_edge_count": int_value(row, "graph_edge_count"),
        "graph_edge_type_count": int_value(row, "graph_edge_type_count"),
        "promotion_queue_candidate_count": int_value(row, "promotion_queue_candidate_count"),
    }


def build_context_pack(coverage_rows: list[dict[str, str]]) -> dict[str, object]:
    entries = [source_entry(row) for row in sorted(coverage_rows, key=lambda item: item["source_id"])]
    status_counts: dict[str, int] = {}
    authority_counts: dict[str, int] = {}
    rights_counts: dict[str, int] = {}
    for row in coverage_rows:
        status_counts[row["coverage_status"]] = status_counts.get(row["coverage_status"], 0) + 1
        authority_counts[row["authority_tier"]] = authority_counts.get(row["authority_tier"], 0) + 1
        rights_counts[row["rights_status"]] = rights_counts.get(row["rights_status"], 0) + 1

    graph_sources = [
        entry
        for entry in entries
        if entry["graph_edge_count"] > 0
    ]
    asset_sources = [
        entry
        for entry in entries
        if entry["committed_asset_count"] > 0
    ]
    candidate_queue_sources = [
        entry
        for entry in entries
        if entry["promotion_queue_candidate_count"] > 0
    ]
    access_limited_sources = [
        entry
        for entry in entries
        if "access_restricted" in entry["download_status_counts"]
        or "http_error" in entry["download_status_counts"]
    ]

    return {
        "context_pack_id": "ai-context-source-coverage-001",
        "title": "Source Coverage Routing Context Pack",
        "title_zh": "来源覆盖路由上下文包",
        "status": "reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": [
            SOURCE_COVERAGE_SUMMARY.as_posix(),
            SOURCE_INDEX.as_posix(),
            SOURCE_DOWNLOAD_MANIFEST.as_posix(),
            SOURCE_DOWNLOAD_LOG.as_posix(),
            DOWNLOADED_METADATA_PROFILE.as_posix(),
            ASSET_SOURCE_INDEX.as_posix(),
            RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY.as_posix(),
            HUST_OBC_OBS_CHAR_PROMOTION_QUEUE.as_posix(),
        ],
        "purpose": (
            "Entry-point routing context for AI Agents choosing which reviewed "
            "source registers, download logs, metadata profiles, asset records, "
            "graph derivatives, or promotion queues to open before collecting evidence."
        ),
        "purpose_zh": (
            "供 AI Agent 选择下一步应打开哪些已复核来源登记、下载日志、metadata profile、"
            "资产记录、图谱派生或 promotion queue 的入口路由上下文。"
        ),
        "coverage": {
            "source_count": len(entries),
            "download_manifest_count": sum(entry["download_manifest_count"] for entry in entries),
            "download_log_count": sum(entry["download_log_count"] for entry in entries),
            "metadata_profile_metric_count": sum(entry["metadata_profile_metric_count"] for entry in entries),
            "committed_asset_count": sum(entry["committed_asset_count"] for entry in entries),
            "committed_asset_bytes": sum(entry["committed_asset_bytes"] for entry in entries),
            "graph_edge_count": sum(entry["graph_edge_count"] for entry in entries),
            "promotion_queue_candidate_count": sum(entry["promotion_queue_candidate_count"] for entry in entries),
            "coverage_status_counts": dict(sorted(status_counts.items())),
            "authority_tier_counts": dict(sorted(authority_counts.items())),
            "rights_status_counts": dict(sorted(rights_counts.items())),
        },
        "priority_routes": {
            "graph_derivative_sources": graph_sources,
            "public_asset_sources": asset_sources,
            "candidate_queue_sources": candidate_queue_sources,
            "access_limited_or_error_sources": access_limited_sources,
        },
        "source_routes": entries,
        "agent_use_rules": [
            "Use this pack as a source-routing and coverage summary, not as evidence by itself.",
            "Open the cited source register and source-specific rows before making any research claim.",
            "Treat dataset-derived rows as candidates or metadata until cross-source review.",
            "Do not infer decipherment, component analysis, provenance facts, or rights status from coverage counts alone.",
            "Keep new downloads in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本上下文包只作为来源路由和覆盖范围摘要使用，不能单独当作证据。",
            "提出任何研究判断前，必须打开被引用的来源登记和对应来源派生记录行。",
            "数据集派生记录在跨来源复核前都只能视为候选或 metadata。",
            "不得仅凭覆盖数量推断释读、构件分析、provenance 事实或权利状态。",
            "新增下载在记录来源、大小、checksum、权利和风险前必须留在已忽略临时目录。",
        ],
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-coverage-summary", default=str(SOURCE_COVERAGE_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    coverage_rows = read_csv_rows(root / args.source_coverage_summary)
    context_pack = build_context_pack(coverage_rows)
    write_json(root / args.output, context_pack)
    print(
        f"context_pack_id={context_pack['context_pack_id']} "
        f"source_count={context_pack['coverage']['source_count']} "
        f"graph_edge_count={context_pack['coverage']['graph_edge_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
