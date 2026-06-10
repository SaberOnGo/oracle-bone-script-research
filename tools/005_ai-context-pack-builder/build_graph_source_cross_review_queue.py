#!/usr/bin/env python3
"""Build graph-derived cross-source review tasks for AI Agent preparation."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_ROUTE_REVIEW_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/011_ai-agent-source-route-review-results.csv"
)
GRAPH_SOURCE_CROSS_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/012_ai-agent-graph-source-cross-review-queue.csv"
)
HUST_OBC_OBS_CHAR_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv"
)
AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
EVOBC_EVOLUTION_CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
EVOBC_ERA_SOURCE_CODEBOOK_STAGING = Path(
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
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)

UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "cross_source_review_queue_metadata_only_not_scholarship"
TASK_STATUS = "needs_cross_source_review"
PROMOTION_STATUS = "not_promoted"
REQUIRED_EVIDENCE_SECTIONS = (
    "source_register;download_log;package_manifest;metadata_profile;graph_edges;staging_row;"
    "counter_source_lookup;rights_risk_review;review_log"
)
COMMON_ROUTE_FILES = [
    SOURCE_ROUTE_REVIEW_RESULTS,
    SOURCE_INDEX,
    DOWNLOADED_METADATA_PROFILE,
    SOURCE_DOWNLOAD_LOG,
    SOURCE_PACKAGE_FILE_MANIFEST,
]
CAUTION = (
    "This is an AI Agent cross-source review queue row only. It is not source evidence by "
    "itself, not a decipherment result, not a component assignment, not an evolution-chain "
    "assignment, not a rights clearance, and must not promote dataset labels, graph edges, "
    "staging rows, or raw source packages into scholarship."
)

OUTPUT_FIELDS = [
    "cross_review_task_id",
    "source_route_result_id",
    "source_route_task_id",
    "context_pack_id",
    "source_id",
    "target_review_scope",
    "primary_review_record_id",
    "related_project_id",
    "primary_external_ref_id",
    "source_record_id",
    "candidate_or_staging_row_count",
    "graph_edge_count",
    "rights_status",
    "source_review_status",
    "required_counter_source_ids",
    "required_evidence_sections",
    "route_files_to_open",
    "review_basis_files",
    "expected_output_path",
    "task_status",
    "promotion_status",
    "research_boundary",
    "review_note",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _one(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one row where {key}={value}, found {len(matches)}")
    return matches[0]


def _paths(values: list[Path | str]) -> str:
    return ";".join(str(value).replace("\\", "/") for value in values)


def _base_row(
    task_number: int,
    source_route_result: dict[str, str],
    target_review_scope: str,
    primary_review_record_id: str,
    related_project_id: str,
    primary_external_ref_id: str,
    source_record_id: str,
    candidate_or_staging_row_count: int,
    required_counter_source_ids: str,
    route_files: list[Path | str],
    expected_output_path: str,
    review_note: str,
) -> dict[str, str]:
    all_route_files = COMMON_ROUTE_FILES + route_files
    return {
        "cross_review_task_id": f"graph-source-cross-review-{task_number:03d}",
        "source_route_result_id": source_route_result["source_route_result_id"],
        "source_route_task_id": source_route_result["source_route_task_id"],
        "context_pack_id": source_route_result["context_pack_id"],
        "source_id": source_route_result["source_id"],
        "target_review_scope": target_review_scope,
        "primary_review_record_id": primary_review_record_id,
        "related_project_id": related_project_id,
        "primary_external_ref_id": primary_external_ref_id,
        "source_record_id": source_record_id,
        "candidate_or_staging_row_count": str(candidate_or_staging_row_count),
        "graph_edge_count": source_route_result["graph_edge_count"],
        "rights_status": source_route_result["rights_status"],
        "source_review_status": source_route_result["source_review_status"],
        "required_counter_source_ids": required_counter_source_ids,
        "required_evidence_sections": REQUIRED_EVIDENCE_SECTIONS,
        "route_files_to_open": _paths(all_route_files),
        "review_basis_files": _paths(all_route_files),
        "expected_output_path": expected_output_path,
        "task_status": TASK_STATUS,
        "promotion_status": PROMOTION_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "review_note": review_note,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_cross_review_rows(
    source_route_review_results: list[dict[str, str]],
    hust_evidence_requests: list[dict[str, str]],
    hust_promotion_rows: list[dict[str, str]],
    evobc_category_rows: list[dict[str, str]],
    evobc_codebook_rows: list[dict[str, str]],
    obimd_main_rows: list[dict[str, str]],
    obimd_subcharacter_rows: list[dict[str, str]],
    obimd_glyph_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_results = {row["source_id"]: row for row in source_route_review_results}

    hust_evidence = hust_evidence_requests[0]
    hust_promotion = _one(hust_promotion_rows, "promotion_queue_id", hust_evidence["promotion_queue_id"])
    evobc_category = evobc_category_rows[0]
    evobc_codebook = evobc_codebook_rows[0]
    obimd_main = obimd_main_rows[0]
    obimd_sub = obimd_subcharacter_rows[0]
    obimd_glyph = obimd_glyph_rows[0]

    return [
        _base_row(
            1,
            source_results["src-hust-obc"],
            "hust_obc_first_candidate_evidence_pack_cross_source_review",
            hust_evidence["evidence_request_id"],
            hust_evidence["suggested_oracle_character_id"],
            hust_evidence["primary_external_ref_id"],
            hust_evidence["source_category_id"],
            len(hust_evidence_requests),
            hust_evidence["source_route_requirement_ids"],
            [
                AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
                HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
                hust_evidence["bucket_manifest_path"],
                HUST_OBC_CANDIDATE_GRAPH_EDGES,
                OBIMD_COMPONENT_GRAPH_EDGES,
                EVOBC_EVOLUTION_GRAPH_EDGES,
            ],
            hust_evidence["draft_output_path"],
            (
                "Open the first HUST-OBC evidence request and promotion queue row, then "
                "cross-check source category 0001 against Xiaoxuetang/OBM, OBIMD, EVOBC, "
                "and inscription context before any evidence-pack draft. The suggested "
                f"project ID {hust_promotion['suggested_oracle_character_id']} remains reserved only."
            ),
        ),
        _base_row(
            2,
            source_results["src-evobc"],
            "evobc_first_evolution_category_cross_source_review",
            evobc_category["candidate_evolution_category_id"],
            "",
            f"evobc-cat-{evobc_category['source_category_id']}",
            evobc_category["source_category_id"],
            len(evobc_category_rows),
            "src-xiaoxuetang-jiaguwen;src-xiaoxuetang-obm;src-hust-obc;src-obimd;src-ihp-oracle-rubbings",
            [
                EVOBC_EVOLUTION_CATEGORY_STAGING,
                EVOBC_ERA_SOURCE_CODEBOOK_STAGING,
                EVOBC_EVOLUTION_GRAPH_EDGES,
            ],
            (
                "doc/public/user_research/002_cross-source-review-queues/evobc/"
                "001_evobc-evo-cat-00001_cross-source-review-log.md"
            ),
            (
                "Open the first EVOBC category staging row and era/source codebook row, then "
                "treat codepoints and era/source codes as dataset metadata only. First category "
                f"has source_category_id={evobc_category['source_category_id']}, "
                f"source_character_codepoints={evobc_category['source_character_codepoints']}, "
                f"image_reference_count={evobc_category['image_reference_count']}, "
                f"era_code_counts={evobc_category['era_code_counts']}, and first codebook row "
                f"{evobc_codebook['codebook_row_id']}."
            ),
        ),
        _base_row(
            3,
            source_results["src-obimd"],
            "obimd_first_component_glyph_route_cross_source_review",
            obimd_sub["candidate_subcharacter_id"],
            obimd_main["candidate_main_character_id"],
            obimd_sub["subcharacter_external_ref_id"],
            obimd_sub["source_subcharacter_uid"],
            len(obimd_subcharacter_rows),
            "src-xiaoxuetang-jiaguwen;src-xiaoxuetang-obm;src-hust-obc;src-evobc;src-ihp-oracle-rubbings",
            [
                OBIMD_MAIN_CHARACTER_STAGING,
                OBIMD_SUBCHARACTER_MAIN_STAGING,
                OBIMD_SUBCHARACTER_GLYPH_STAGING,
                OBIMD_COMPONENT_GRAPH_EDGES,
            ],
            (
                "doc/public/user_research/002_cross-source-review-queues/obimd/"
                "001_obimd-sub-cand-000001_cross-source-review-log.md"
            ),
            (
                "Open the first OBIMD main-character, subcharacter, and glyph-codepoint rows. "
                f"Main candidate {obimd_main['candidate_main_character_id']} and subcharacter "
                f"{obimd_sub['candidate_subcharacter_id']} share source UID "
                f"{obimd_sub['source_subcharacter_uid']}; first glyph link "
                f"{obimd_glyph['candidate_glyph_link_id']} has glyph_codepoint_uplus="
                f"{obimd_glyph['glyph_codepoint_uplus']}. Treat all as dataset metadata only."
            ),
        ),
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-route-review-results", default=str(SOURCE_ROUTE_REVIEW_RESULTS))
    parser.add_argument("--hust-evidence-request-queue", default=str(AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE))
    parser.add_argument("--hust-promotion-queue", default=str(HUST_OBC_OBS_CHAR_PROMOTION_QUEUE))
    parser.add_argument("--evobc-category-staging", default=str(EVOBC_EVOLUTION_CATEGORY_STAGING))
    parser.add_argument("--evobc-codebook-staging", default=str(EVOBC_ERA_SOURCE_CODEBOOK_STAGING))
    parser.add_argument("--obimd-main-staging", default=str(OBIMD_MAIN_CHARACTER_STAGING))
    parser.add_argument("--obimd-subcharacter-staging", default=str(OBIMD_SUBCHARACTER_MAIN_STAGING))
    parser.add_argument("--obimd-glyph-staging", default=str(OBIMD_SUBCHARACTER_GLYPH_STAGING))
    parser.add_argument("--output", default=str(GRAPH_SOURCE_CROSS_REVIEW_QUEUE))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_cross_review_rows(
        read_csv_rows(root / args.source_route_review_results),
        read_csv_rows(root / args.hust_evidence_request_queue),
        read_csv_rows(root / args.hust_promotion_queue),
        read_csv_rows(root / args.evobc_category_staging),
        read_csv_rows(root / args.evobc_codebook_staging),
        read_csv_rows(root / args.obimd_main_staging),
        read_csv_rows(root / args.obimd_subcharacter_staging),
        read_csv_rows(root / args.obimd_glyph_staging),
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
