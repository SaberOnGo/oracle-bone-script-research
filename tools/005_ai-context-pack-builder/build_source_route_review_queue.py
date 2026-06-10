#!/usr/bin/env python3
"""Build a source-route review queue from the AI Agent source coverage context pack."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SOURCE_COVERAGE_CONTEXT_PACK = Path(
    "corpus/009_statistics-and-derived-features/008_ai-agent-source-coverage-context-pack.json"
)
SOURCE_ROUTE_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/009_ai-agent-source-route-review-queue.csv"
)
SOURCE_COVERAGE_SUMMARY = Path("corpus/009_statistics-and-derived-features/007_source-coverage-summary.csv")
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_STATUS_CODEBOOK = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/013_source-download-status-codebook.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
ASSET_RIGHTS_REVIEW_LOG = Path("project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv")
ASSET_IMAGE_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
ASSET_IMAGE_VISUAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
)
RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/001_relationship-graph-edge-type-summary.csv"
)
RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/002_relationship-graph-node-degree-summary.csv"
)
AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK = Path(
    "corpus/009_statistics-and-derived-features/003_ai-agent-relationship-graph-context-pack.json"
)
AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK = Path(
    "corpus/009_statistics-and-derived-features/004_ai-agent-hust-obc-bucket-review-route-pack.json"
)
AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK = Path(
    "corpus/009_statistics-and-derived-features/006_ai-agent-public-domain-asset-context-pack.json"
)
HUST_OBC_OBS_CHAR_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"
)
HUST_OBC_CANDIDATE_GRAPH_EDGES = Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl")
OBIMD_COMPONENT_GRAPH_EDGES = Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl")
EVOBC_EVOLUTION_GRAPH_EDGES = Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")

UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "routing_metadata_only_not_scholarship"
CAUTION = (
    "This source-route task is a routing and provenance review aid only. "
    "Open the cited source rows before making any claim; do not treat coverage, "
    "dataset labels, graph edges, or asset metadata as decipherment conclusions."
)

OUTPUT_FIELDS = [
    "source_route_task_id",
    "context_pack_id",
    "source_id",
    "priority_rank",
    "priority_tags",
    "route",
    "route_zh",
    "coverage_status",
    "rights_status",
    "authority_tier",
    "review_focus",
    "route_files",
    "required_next_checks",
    "research_boundary",
    "assignment_status",
    "review_status",
    "caution",
    "updated_at",
]

PRIORITY_ORDER = [
    "candidate_queue",
    "graph_derivative",
    "public_asset",
    "access_limited_or_error",
    "metadata_profile",
    "download_log",
    "source_register",
]

GRAPH_EDGE_FILES_BY_SOURCE = {
    "src-hust-obc": HUST_OBC_CANDIDATE_GRAPH_EDGES,
    "src-obimd": OBIMD_COMPONENT_GRAPH_EDGES,
    "src-evobc": EVOBC_EVOLUTION_GRAPH_EDGES,
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def int_value(entry: dict[str, object], key: str) -> int:
    value = entry.get(key, 0)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value:
        return int(value)
    return 0


def source_tags(entry: dict[str, object]) -> list[str]:
    tags: list[str] = []
    if int_value(entry, "promotion_queue_candidate_count") > 0:
        tags.append("candidate_queue")
    if int_value(entry, "graph_edge_count") > 0:
        tags.append("graph_derivative")
    if int_value(entry, "committed_asset_count") > 0:
        tags.append("public_asset")
    download_status_counts = str(entry.get("download_status_counts", ""))
    if "access_restricted" in download_status_counts or "http_error" in download_status_counts:
        tags.append("access_limited_or_error")
    if int_value(entry, "metadata_profile_metric_count") > 0:
        tags.append("metadata_profile")
    if int_value(entry, "download_log_count") > 0:
        tags.append("download_log")
    if not tags:
        tags.append("source_register")
    return tags


def priority_rank(tags: list[str]) -> int:
    for index, tag in enumerate(PRIORITY_ORDER, start=1):
        if tag in tags:
            return index
    return len(PRIORITY_ORDER)


def review_focus(tags: list[str]) -> str:
    if "candidate_queue" in tags:
        return "open_candidate_queue_and_graph_routes_before_evidence_pack_work"
    if "graph_derivative" in tags:
        return "open_graph_derivatives_and_source_metadata_before_using_edges"
    if "public_asset" in tags:
        return "open_asset_rights_and_image_metadata_before_visual_review"
    if "access_limited_or_error" in tags:
        return "open_download_logs_and_resolve_access_or_error_boundary"
    if "metadata_profile" in tags:
        return "open_metadata_profile_and_source_register_before_extraction"
    if "download_log" in tags:
        return "open_download_manifest_log_and_package_manifest_before_promotion"
    return "open_source_register_before_any_use"


def route_files(entry: dict[str, object], tags: list[str]) -> list[str]:
    files = [
        SOURCE_COVERAGE_CONTEXT_PACK,
        SOURCE_COVERAGE_SUMMARY,
        SOURCE_INDEX,
    ]
    if "download_log" in tags or "access_limited_or_error" in tags:
        files.extend(
            [
                SOURCE_DOWNLOAD_MANIFEST,
                SOURCE_DOWNLOAD_LOG,
                SOURCE_PACKAGE_FILE_MANIFEST,
                SOURCE_DOWNLOAD_STATUS_CODEBOOK,
            ]
        )
    if "metadata_profile" in tags:
        files.append(DOWNLOADED_METADATA_PROFILE)
    if "public_asset" in tags:
        files.extend(
            [
                ASSET_SOURCE_INDEX,
                ASSET_RIGHTS_REVIEW_LOG,
                ASSET_IMAGE_TECHNICAL_PROFILE,
                ASSET_IMAGE_VISUAL_PROFILE,
                AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK,
            ]
        )
    if "graph_derivative" in tags:
        files.extend(
            [
                RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY,
                RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY,
                AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK,
            ]
        )
        source_id = str(entry["source_id"])
        edge_file = GRAPH_EDGE_FILES_BY_SOURCE.get(source_id)
        if edge_file is not None:
            files.append(edge_file)
    if "candidate_queue" in tags:
        files.extend(
            [
                HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
                AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK,
                AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
            ]
        )
    unique_files: list[str] = []
    for path in files:
        value = path.as_posix()
        if value not in unique_files:
            unique_files.append(value)
    return unique_files


def required_next_checks(tags: list[str]) -> list[str]:
    checks: list[str] = []
    if "candidate_queue" in tags:
        checks.append("verify_candidate_queue_rows_remain_reserved_and_cross_source_review_only")
    if "graph_derivative" in tags:
        checks.append("verify_graph_edges_are_metadata_routes_not_component_or_decipherment_claims")
    if "public_asset" in tags:
        checks.append("verify_asset_rights_checksums_and_visual_profiles_before_image_use")
    if "access_limited_or_error" in tags:
        checks.append("review_download_log_status_and_record_retry_or_metadata_only_decision")
    if "metadata_profile" in tags:
        checks.append("open_metadata_profile_rows_and_keep_extraction_reviewed_metadata_only")
    if "download_log" in tags:
        checks.append("confirm_source_size_checksum_rights_and_risk_before_promoting_derivatives")
    if not checks:
        checks.append("open_source_register_and_define_next_review_artifact")
    return checks


def build_queue_rows(context_pack: dict[str, object]) -> list[dict[str, str]]:
    context_pack_id = str(context_pack["context_pack_id"])
    entries = context_pack.get("source_routes", [])
    if not isinstance(entries, list):
        raise TypeError("source_routes must be a list")
    sorted_entries = sorted(
        (entry for entry in entries if isinstance(entry, dict)),
        key=lambda entry: (
            priority_rank(source_tags(entry)),
            str(entry["source_id"]),
        ),
    )
    rows: list[dict[str, str]] = []
    for index, entry in enumerate(sorted_entries, start=1):
        tags = source_tags(entry)
        rows.append(
            {
                "source_route_task_id": f"source-route-review-{index:03d}",
                "context_pack_id": context_pack_id,
                "source_id": str(entry["source_id"]),
                "priority_rank": str(priority_rank(tags)),
                "priority_tags": ";".join(tags),
                "route": str(entry["route"]),
                "route_zh": str(entry["route_zh"]),
                "coverage_status": str(entry["coverage_status"]),
                "rights_status": str(entry["rights_status"]),
                "authority_tier": str(entry["authority_tier"]),
                "review_focus": review_focus(tags),
                "route_files": ";".join(route_files(entry, tags)),
                "required_next_checks": ";".join(required_next_checks(tags)),
                "research_boundary": RESEARCH_BOUNDARY,
                "assignment_status": "unassigned",
                "review_status": "needs_source_route_review",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-pack", default=str(SOURCE_COVERAGE_CONTEXT_PACK))
    parser.add_argument("--output", default=str(SOURCE_ROUTE_REVIEW_QUEUE))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_queue_rows(read_json(root / args.context_pack))
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
