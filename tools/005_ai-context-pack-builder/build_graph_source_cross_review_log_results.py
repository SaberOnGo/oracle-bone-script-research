#!/usr/bin/env python3
"""Build metadata-only results from graph-source cross-review log drafts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/014_ai-agent-graph-source-cross-review-log-draft-manifest.csv"
)
GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/015_ai-agent-graph-source-cross-review-log-results.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
HUST_OBC_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"
)
HUST_OBC_BUCKET_MANIFEST = Path(
    "corpus/001_oracle-characters/001_000001-000100_obs-char-bucket_oracle-characters/"
    "000_hust-obc-promotion-bucket-manifest.csv"
)
HUST_OBC_EVIDENCE_REQUEST_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
EVOBC_CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
EVOBC_CODEBOOK_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "002_evobc-era-source-codebook-staging.csv"
)
OBIMD_MAIN_CHARACTER_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv"
)
OBIMD_SUBCHARACTER_MAIN_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/002_obimd-subcharacter-main-staging.csv"
)
OBIMD_SUBCHARACTER_GLYPH_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/003_obimd-subcharacter-glyph-staging.csv"
)
HUST_OBC_CANDIDATE_GRAPH_EDGES = Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl")
OBIMD_COMPONENT_GRAPH_EDGES = Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl")
EVOBC_EVOLUTION_GRAPH_EDGES = Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")

UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "cross_source_review_log_result_metadata_only_not_scholarship"
OUTPUT_SCOPE = "cross_source_review_log_result_only"
CAUTION = (
    "This is a metadata-only cross-source review log result. It records local route evidence "
    "availability only; it is not source evidence by itself, not a rights decision, not a "
    "promotion decision, not a component or evolution-chain assignment, and not a decipherment "
    "conclusion."
)

PRIMARY_GRAPH_FILE_BY_SOURCE = {
    "src-hust-obc": HUST_OBC_CANDIDATE_GRAPH_EDGES,
    "src-evobc": EVOBC_EVOLUTION_GRAPH_EDGES,
    "src-obimd": OBIMD_COMPONENT_GRAPH_EDGES,
}

OUTPUT_FIELDS = [
    "cross_review_result_id",
    "draft_log_id",
    "cross_review_log_id",
    "cross_review_task_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "required_counter_source_count",
    "registered_counter_source_count",
    "counter_source_lookup_status",
    "download_log_count",
    "download_log_review_status",
    "package_manifest_count",
    "package_manifest_review_status",
    "metadata_profile_metric_count",
    "metadata_profile_review_status",
    "graph_route_file_count",
    "graph_edge_route_line_count",
    "primary_graph_edge_count",
    "graph_edge_review_status",
    "staging_row_count",
    "staging_record_refs",
    "staging_row_review_status",
    "draft_log_status",
    "rights_status",
    "rights_risk_review_status",
    "promotion_decision_status",
    "evidence_pack_draft_status",
    "research_boundary",
    "output_scope",
    "review_note",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_jsonl_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as file:
        return sum(1 for line in file if line.strip())


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _source_rows(rows: list[dict[str, str]], source_id: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("source_id") == source_id]


def _one(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one row where {key}={value}, found {len(matches)}")
    return matches[0]


def _registered_counter_source_count(required_ids: list[str], source_index_rows: list[dict[str, str]]) -> int:
    registered = {row.get("source_id", "") for row in source_index_rows}
    return sum(1 for source_id in required_ids if source_id in registered)


def _route_file_status(root: Path, route_files: list[str]) -> tuple[int, str]:
    missing_count = sum(1 for path in route_files if not (root / path).exists())
    status = "reviewed_route_files_exist" if missing_count == 0 else "route_files_missing"
    return missing_count, status


def _review_status_from_count(count: int, present_status: str) -> str:
    return present_status if count > 0 else "missing_metadata_rows"


def _graph_paths(route_files: list[str]) -> list[str]:
    return [path for path in route_files if path.startswith("corpus/008_relationship-graph/")]


def _graph_route_line_count(root: Path, graph_paths: list[str]) -> int:
    return sum(read_jsonl_count(root / path) for path in graph_paths)


def _status_for_draft(root: Path, draft_log_path: str) -> str:
    return "draft_log_exists" if (root / draft_log_path).exists() else "draft_log_missing"


def _hust_staging_refs(
    row: dict[str, str],
    evidence_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    bucket_rows: list[dict[str, str]],
) -> list[str]:
    refs: list[str] = []
    for evidence_row in evidence_rows:
        if evidence_row.get("evidence_request_id") == row["primary_review_record_id"]:
            refs.append(evidence_row["evidence_request_id"])
    for promotion_row in promotion_rows:
        if promotion_row.get("primary_external_ref_id") == row["primary_external_ref_id"]:
            refs.append(promotion_row["promotion_queue_id"])
    for bucket_row in bucket_rows:
        if bucket_row.get("primary_external_ref_id") == row["primary_external_ref_id"]:
            refs.append(bucket_row["bucket_manifest_row_id"])
    return refs


def _evobc_staging_refs(
    row: dict[str, str],
    category_rows: list[dict[str, str]],
    codebook_rows: list[dict[str, str]],
) -> list[str]:
    refs: list[str] = []
    category_row = _one(category_rows, "candidate_evolution_category_id", row["primary_review_record_id"])
    refs.append(category_row["candidate_evolution_category_id"])
    era_codes = [part.split(":", 1)[0] for part in _split_compact(category_row["era_code_counts"])]
    for codebook_row in codebook_rows:
        if codebook_row.get("code_type") == "era" and codebook_row.get("code_value") in era_codes:
            refs.append(codebook_row["codebook_row_id"])
    return refs


def _obimd_staging_refs(
    row: dict[str, str],
    main_rows: list[dict[str, str]],
    sub_rows: list[dict[str, str]],
    glyph_rows: list[dict[str, str]],
) -> list[str]:
    refs: list[str] = []
    source_uid = row["source_record_id"]
    for main_row in main_rows:
        if main_row.get("candidate_main_character_id") == row.get("related_project_id") or main_row.get("source_uid") == source_uid:
            refs.append(main_row["candidate_main_character_id"])
            break
    for sub_row in sub_rows:
        if sub_row.get("candidate_subcharacter_id") == row["primary_review_record_id"]:
            refs.append(sub_row["candidate_subcharacter_id"])
            break
    refs.extend(
        glyph_row["candidate_glyph_link_id"]
        for glyph_row in glyph_rows
        if glyph_row.get("source_subcharacter_uid") == source_uid
    )
    return refs


def _staging_refs(
    row: dict[str, str],
    evidence_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    bucket_rows: list[dict[str, str]],
    evobc_category_rows: list[dict[str, str]],
    evobc_codebook_rows: list[dict[str, str]],
    obimd_main_rows: list[dict[str, str]],
    obimd_sub_rows: list[dict[str, str]],
    obimd_glyph_rows: list[dict[str, str]],
) -> list[str]:
    source_id = row["source_id"]
    if source_id == "src-hust-obc":
        return _hust_staging_refs(row, evidence_rows, promotion_rows, bucket_rows)
    if source_id == "src-evobc":
        return _evobc_staging_refs(row, evobc_category_rows, evobc_codebook_rows)
    if source_id == "src-obimd":
        return _obimd_staging_refs(row, obimd_main_rows, obimd_sub_rows, obimd_glyph_rows)
    raise ValueError(f"unsupported source_id: {source_id}")


def _review_note(row: dict[str, str], route_file_count: int, staging_row_count: int) -> str:
    return (
        f"Metadata-only review opened {route_file_count} local route references for "
        f"{row['source_id']} and found {staging_row_count} matching staging or draft rows. "
        "The result is ready for later evidence collection, but it does not promote dataset "
        "labels, graph edges, staging rows, or draft logs into scholarship."
    )


def build_result_rows(
    draft_rows: list[dict[str, str]],
    source_index_rows: list[dict[str, str]],
    metadata_profile_rows: list[dict[str, str]],
    download_log_rows: list[dict[str, str]],
    package_manifest_rows: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    bucket_rows: list[dict[str, str]],
    evobc_category_rows: list[dict[str, str]],
    evobc_codebook_rows: list[dict[str, str]],
    obimd_main_rows: list[dict[str, str]],
    obimd_sub_rows: list[dict[str, str]],
    obimd_glyph_rows: list[dict[str, str]],
    root: Path,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(draft_rows, start=1):
        source_id = row["source_id"]
        route_files = _split_compact(row["route_files_to_open"])
        required_counter_source_ids = _split_compact(row["required_counter_source_ids"])
        route_missing_count, route_file_status = _route_file_status(root, route_files)
        registered_counter_count = _registered_counter_source_count(required_counter_source_ids, source_index_rows)
        source_index_row = _one(source_index_rows, "source_id", source_id)
        download_count = len(_source_rows(download_log_rows, source_id))
        package_count = len(_source_rows(package_manifest_rows, source_id))
        metadata_count = len(_source_rows(metadata_profile_rows, source_id))
        graph_paths = _graph_paths(route_files)
        primary_graph_count = read_jsonl_count(root / PRIMARY_GRAPH_FILE_BY_SOURCE[source_id])
        graph_route_line_count = _graph_route_line_count(root, graph_paths)
        staging_refs = _staging_refs(
            row,
            evidence_rows,
            promotion_rows,
            bucket_rows,
            evobc_category_rows,
            evobc_codebook_rows,
            obimd_main_rows,
            obimd_sub_rows,
            obimd_glyph_rows,
        )
        staging_count = len(staging_refs)
        rows.append(
            {
                "cross_review_result_id": f"graph-source-cross-review-result-{index:03d}",
                "draft_log_id": row["draft_log_id"],
                "cross_review_log_id": row["cross_review_log_id"],
                "cross_review_task_id": row["cross_review_task_id"],
                "source_id": source_id,
                "primary_review_record_id": row["primary_review_record_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_record_id": row["source_record_id"],
                "route_file_count": str(len(route_files)),
                "missing_route_file_count": str(route_missing_count),
                "route_file_review_status": route_file_status,
                "required_counter_source_count": str(len(required_counter_source_ids)),
                "registered_counter_source_count": str(registered_counter_count),
                "counter_source_lookup_status": (
                    "reviewed_all_required_counter_sources_registered"
                    if registered_counter_count == len(required_counter_source_ids)
                    else "missing_counter_source_registration"
                ),
                "download_log_count": str(download_count),
                "download_log_review_status": _review_status_from_count(download_count, "reviewed_metadata_only"),
                "package_manifest_count": str(package_count),
                "package_manifest_review_status": _review_status_from_count(package_count, "reviewed_metadata_only"),
                "metadata_profile_metric_count": str(metadata_count),
                "metadata_profile_review_status": _review_status_from_count(metadata_count, "reviewed_metadata_only"),
                "graph_route_file_count": str(len(graph_paths)),
                "graph_edge_route_line_count": str(graph_route_line_count),
                "primary_graph_edge_count": str(primary_graph_count),
                "graph_edge_review_status": "reviewed_graph_route_files_metadata_only",
                "staging_row_count": str(staging_count),
                "staging_record_refs": ";".join(staging_refs),
                "staging_row_review_status": "reviewed_metadata_only",
                "draft_log_status": _status_for_draft(root, row["draft_log_path"]),
                "rights_status": source_index_row["rights_status"],
                "rights_risk_review_status": "reviewed_rights_boundary_metadata_only",
                "promotion_decision_status": "not_promoted",
                "evidence_pack_draft_status": "not_started_or_draft_only",
                "research_boundary": RESEARCH_BOUNDARY,
                "output_scope": OUTPUT_SCOPE,
                "review_note": _review_note(row, len(route_files), staging_count),
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
    parser.add_argument("--draft-manifest", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST))
    parser.add_argument("--output", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_result_rows(
        read_csv_rows(root / args.draft_manifest),
        read_csv_rows(root / SOURCE_INDEX),
        read_csv_rows(root / DOWNLOADED_METADATA_PROFILE),
        read_csv_rows(root / SOURCE_DOWNLOAD_LOG),
        read_csv_rows(root / SOURCE_PACKAGE_FILE_MANIFEST),
        read_csv_rows(root / HUST_OBC_EVIDENCE_REQUEST_QUEUE),
        read_csv_rows(root / HUST_OBC_PROMOTION_QUEUE),
        read_csv_rows(root / HUST_OBC_BUCKET_MANIFEST),
        read_csv_rows(root / EVOBC_CATEGORY_STAGING),
        read_csv_rows(root / EVOBC_CODEBOOK_STAGING),
        read_csv_rows(root / OBIMD_MAIN_CHARACTER_STAGING),
        read_csv_rows(root / OBIMD_SUBCHARACTER_MAIN_STAGING),
        read_csv_rows(root / OBIMD_SUBCHARACTER_GLYPH_STAGING),
        root,
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
