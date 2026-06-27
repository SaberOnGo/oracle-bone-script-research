#!/usr/bin/env python3
"""Build a shape/component/evolution verification gap review checklist.

This bridges verified-missing core-corpus gaps for codepoint routes, OBIMD
component candidates, and EVOBC evolution/correspondence candidates to existing
staging, graph, map, and review-route files. It is navigation only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CORE_CORPUS_PHASE_GAP_ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
OUTPUT_CSV = STAT_DIR / "196_shape-component-evolution-verification-gap-review-checklist.csv"

CODEPOINT_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
CODEPOINT_REVIEW_QUEUE = STAT_DIR / "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"
CODEPOINT_READINESS_CHECKLIST = (
    STAT_DIR / "048_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-readiness-checklist.csv"
)
HUST_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)

COMPONENT_MAIN_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/002_obimd-subcharacter-main-staging.csv"
)
COMPONENT_GLYPH_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/003_obimd-subcharacter-glyph-staging.csv"
)
COMPONENT_ID_SOURCE_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/004_component-id-source-map.csv"
)
COMPONENT_GRAPH_EDGES = Path("corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl")
COMPONENT_REVIEW_LOG_DIR = Path("doc/public/user_research/002_cross-source-review-queues/obimd")

EVOLUTION_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
EVOLUTION_ID_SOURCE_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/005_evolution-candidate-id-source-map.csv"
)
EVOLUTION_GRAPH_EDGES = Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")
EVOLUTION_REVIEW_LOG_DIR = Path("doc/public/user_research/002_cross-source-review-queues/evobc")

UPDATED_AT = "2026-06-20"
TARGET_AREAS = [
    "cross_source_codepoint_routes",
    "graphemic_components",
    "evolution_correspondences",
]
CLAIM_BOUNDARY = "shape_component_evolution_verification_gap_review_checklist_not_review_outcome_not_scholarship"
CAUTION = (
    "This shape component evolution verification gap review checklist only routes "
    "codepoint, component, and evolution/correspondence candidates to existing "
    "staging, graph, source-map, object-local, and review files for later human "
    "verification. It does not collect new evidence, decide rights, promote "
    "sources, import corpus records, confirm identity, confirm components, "
    "confirm evolution chains, or make decipherment claims."
)
REQUIRED_REVIEW_STEPS = (
    "open_196_shape_component_evolution_verification_gap_review_checklist;"
    "open_192_core_corpus_phase_gap_action_queue;"
    "open_area_primary_staging;"
    "open_area_project_id_map_or_review_queue;"
    "open_area_graph_edges_or_readiness_routes;"
    "confirm_no_new_evidence_collection;"
    "confirm_no_rights_decision;"
    "confirm_no_source_promotion;"
    "confirm_no_corpus_import;"
    "confirm_no_identity_claim;"
    "confirm_no_component_claim;"
    "confirm_no_evolution_chain_claim;"
    "confirm_no_decipherment_claim"
)
SOURCE_CONTEXT_FIELDS_TO_VERIFY = (
    "source_id;"
    "source_register_row;"
    "external_reference;"
    "rights_status;"
    "risk_note;"
    "review_status"
)
AREA_REVIEW_FIELDS = {
    "cross_source_codepoint_routes": {
        "required_verification_slots": (
            "source_codepoint;"
            "source_character_id;"
            "matched_project_character_route;"
            "matched_source_ids;"
            "readiness_route;"
            "promotion_review_route;"
            "missing_evidence;"
            "review_status"
        ),
        "concrete_next_checks": (
            "Which source codepoint route is being compared?;"
            "Which project character route is the match candidate?;"
            "Which HUST, OBIMD, or EVOBC source row supports the route?;"
            "Which readiness or promotion review route must be opened?;"
            "What missing evidence or review status remains before identity review?"
        ),
    },
    "graphemic_components": {
        "required_verification_slots": (
            "component_candidate_id;"
            "component_shape_label;"
            "glyph_image_route;"
            "host_character_route;"
            "subcharacter_source_row;"
            "component_graph_edge_route;"
            "missing_visual_evidence;"
            "review_status"
        ),
        "concrete_next_checks": (
            "Which component candidate and source row are being checked?;"
            "Which glyph image or visual route supports the component candidate?;"
            "Which host character or object-local route must be opened?;"
            "Which graph edge is only a route and not a component claim?;"
            "What missing visual evidence or review status remains?"
        ),
    },
    "evolution_correspondences": {
        "required_verification_slots": (
            "evolution_candidate_id;"
            "oracle_source_route;"
            "bronze_seal_modern_route;"
            "correspondence_category;"
            "source_category_row;"
            "evolution_graph_edge_route;"
            "missing_comparison_evidence;"
            "review_status"
        ),
        "concrete_next_checks": (
            "Which evolution candidate and source category row are being checked?;"
            "Which bronze, seal, or modern correspondence route supports the candidate?;"
            "Which oracle-source route must be opened before comparison?;"
            "Which graph edge is only a route and not an accepted correspondence?;"
            "What missing comparison evidence or review status remains?"
        ),
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_join(values: list[str]) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        value = value.rstrip("/")
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(value)
    return ";".join(output)


def path_text(path: Path) -> str:
    return path.as_posix()


def count_jsonl_rows(root: Path, path: Path) -> int:
    with (root / path).open("r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def count_files(root: Path, pattern: str) -> int:
    return sum(1 for path in root.glob(pattern) if path.is_file())


def source_ids_from_rows(rows: list[dict[str, str]], field: str = "source_id") -> str:
    return ";".join(sorted({source_id for row in rows for source_id in split_values(row.get(field, ""))}))


def build_area_metrics(root: Path) -> dict[str, dict[str, str]]:
    codepoint_rows = read_csv_rows(root / CODEPOINT_STAGING)
    codepoint_review_rows = read_csv_rows(root / CODEPOINT_REVIEW_QUEUE)
    codepoint_readiness_rows = read_csv_rows(root / CODEPOINT_READINESS_CHECKLIST)
    component_main_rows = read_csv_rows(root / COMPONENT_MAIN_STAGING)
    component_glyph_rows = read_csv_rows(root / COMPONENT_GLYPH_STAGING)
    component_map_rows = read_csv_rows(root / COMPONENT_ID_SOURCE_MAP)
    evolution_rows = read_csv_rows(root / EVOLUTION_STAGING)
    evolution_map_rows = read_csv_rows(root / EVOLUTION_ID_SOURCE_MAP)
    return {
        "cross_source_codepoint_routes": {
            "primary_staging_count": str(len(codepoint_rows)),
            "supporting_staging_count": "0",
            "project_id_map_count": "0",
            "primary_review_route_count": str(len(codepoint_review_rows)),
            "supporting_readiness_count": str(len(codepoint_readiness_rows)),
            "graph_edge_count": "0",
            "object_packet_count": "0",
            "review_log_count": "0",
            "source_ids": source_ids_from_rows(codepoint_rows, "matched_source_ids"),
            **AREA_REVIEW_FIELDS["cross_source_codepoint_routes"],
            "files_to_open": unique_join(
                [
                    path_text(OUTPUT_CSV),
                    path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
                    path_text(CODEPOINT_STAGING),
                    path_text(CODEPOINT_REVIEW_QUEUE),
                    path_text(CODEPOINT_READINESS_CHECKLIST),
                    path_text(HUST_PROMOTION_QUEUE),
                ]
            ),
        },
        "graphemic_components": {
            "primary_staging_count": str(len(component_main_rows)),
            "supporting_staging_count": str(len(component_glyph_rows)),
            "project_id_map_count": str(len(component_map_rows)),
            "primary_review_route_count": "0",
            "supporting_readiness_count": "0",
            "graph_edge_count": str(count_jsonl_rows(root, COMPONENT_GRAPH_EDGES)),
            "object_packet_count": str(
                count_files(root, "corpus/003_graphemic-components/**/01_candidate-component-packet.json")
            ),
            "review_log_count": str(count_files(root, path_text(COMPONENT_REVIEW_LOG_DIR / "*.md"))),
            "source_ids": source_ids_from_rows(component_main_rows),
            **AREA_REVIEW_FIELDS["graphemic_components"],
            "files_to_open": unique_join(
                [
                    path_text(OUTPUT_CSV),
                    path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
                    path_text(COMPONENT_MAIN_STAGING),
                    path_text(COMPONENT_GLYPH_STAGING),
                    path_text(COMPONENT_ID_SOURCE_MAP),
                    path_text(COMPONENT_GRAPH_EDGES),
                    path_text(COMPONENT_REVIEW_LOG_DIR),
                    "corpus/003_graphemic-components",
                ]
            ),
        },
        "evolution_correspondences": {
            "primary_staging_count": str(len(evolution_rows)),
            "supporting_staging_count": "0",
            "project_id_map_count": str(len(evolution_map_rows)),
            "primary_review_route_count": "0",
            "supporting_readiness_count": "0",
            "graph_edge_count": str(count_jsonl_rows(root, EVOLUTION_GRAPH_EDGES)),
            "object_packet_count": str(
                count_files(
                    root,
                    "corpus/004_bronze-seal-modern-correspondences/**/01_candidate-evolution-packet.json",
                )
            ),
            "review_log_count": str(count_files(root, path_text(EVOLUTION_REVIEW_LOG_DIR / "*.md"))),
            "source_ids": source_ids_from_rows(evolution_rows),
            **AREA_REVIEW_FIELDS["evolution_correspondences"],
            "files_to_open": unique_join(
                [
                    path_text(OUTPUT_CSV),
                    path_text(CORE_CORPUS_PHASE_GAP_ACTION_QUEUE),
                    path_text(EVOLUTION_STAGING),
                    path_text(EVOLUTION_ID_SOURCE_MAP),
                    path_text(EVOLUTION_GRAPH_EDGES),
                    path_text(EVOLUTION_REVIEW_LOG_DIR),
                    "corpus/004_bronze-seal-modern-correspondences",
                ]
            ),
        },
    }


def build_checklist_rows(root: Path) -> list[dict[str, str]]:
    gap_rows = [
        row
        for row in read_csv_rows(root / CORE_CORPUS_PHASE_GAP_ACTION_QUEUE)
        if row["corpus_area"] in TARGET_AREAS and row["phase_name"] == "verified"
    ]
    metrics = build_area_metrics(root)
    rows: list[dict[str, str]] = []
    for gap_row in gap_rows:
        area_metrics = metrics[gap_row["corpus_area"]]
        rows.append(
            {
                "review_checklist_id": f"shape-component-evolution-verification-gap-review-{len(rows) + 1:03d}",
                "gap_queue_id": gap_row["gap_queue_id"],
                "source_phase_row_id": gap_row["source_phase_row_id"],
                "corpus_area": gap_row["corpus_area"],
                "phase_name": gap_row["phase_name"],
                "phase_status": gap_row["phase_status"],
                "gap_type": gap_row["gap_type"],
                "review_priority": gap_row["review_priority"],
                "review_status": "needs_human_review",
                **area_metrics,
                "required_review_steps": REQUIRED_REVIEW_STEPS,
                "source_context_fields_to_verify": SOURCE_CONTEXT_FIELDS_TO_VERIFY,
                "recommended_action": gap_row["recommended_action"],
                "candidate_or_staging_boundary": gap_row["candidate_or_staging_boundary"],
                "claim_boundary": CLAIM_BOUNDARY,
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "no_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "identity_claim_status": "no_identity_claim",
                "component_claim_status": "no_component_claim",
                "evolution_chain_claim_status": "no_evolution_chain_claim",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_checklist_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"shape_component_evolution_verification_gap_review_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
