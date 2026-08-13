#!/usr/bin/env python3
"""Build cross-source character-to-component candidate routes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_CROSSWALK = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
DEFAULT_MAIN = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "006_obimd-main-character-staging.csv"
)
DEFAULT_COMPONENTS = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
DEFAULT_COMPONENT_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "004_component-id-source-map.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/"
    "016_character-component-candidate-graph-edges.jsonl"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def build_edges(
    crosswalk_rows: list[dict[str, str]],
    main_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    component_map_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    main_by_candidate = {
        row["candidate_main_character_id"]: row for row in main_rows
    }
    component_by_main_uid: dict[str, list[dict[str, str]]] = {}
    for row in component_rows:
        component_by_main_uid.setdefault(row["source_main_character_uid"], []).append(row)
    component_project_by_external: dict[str, str] = {}
    for row in component_map_rows:
        project_id = row.get("project_id", "")
        for external_ref in split_refs(row.get("all_external_ref_ids", "")):
            if external_ref.startswith("obimd-sub-"):
                component_project_by_external[external_ref] = project_id

    edges: list[dict[str, object]] = []
    for crosswalk in crosswalk_rows:
        character_id = crosswalk.get("suggested_oracle_character_id", "")
        if not character_id or not crosswalk.get("obimd_candidate_main_character_ids"):
            continue
        for main_candidate_id in split_refs(
            crosswalk["obimd_candidate_main_character_ids"]
        ):
            main_row = main_by_candidate.get(main_candidate_id)
            if main_row is None:
                raise ValueError(f"missing OBIMD main candidate: {main_candidate_id}")
            for component in component_by_main_uid.get(main_row["source_uid"], []):
                external_ref = component.get("subcharacter_external_ref_id", "")
                component_id = component_project_by_external.get(external_ref)
                if not component_id:
                    raise ValueError(f"missing component project id: {external_ref}")
                index = len(edges) + 1
                edges.append(
                    {
                        "edge_id": f"edge-character-component-obimd-{index:03d}",
                        "source_node_id": character_id,
                        "edge_type": "CHARACTER_HAS_COMPONENT_CANDIDATE",
                        "target_node_id": component_id,
                        "confidence_level": "unknown",
                        "source_ids": ["src-hust-obc", "src-obimd"],
                        "evidence_note": (
                            "HUST and OBIMD codepoint/hierarchy route only; it is not "
                            "a formal component assignment, not a confirmed character "
                            "identity, and not a decipherment conclusion."
                        ),
                        "review_status": "needs_cross_source_review",
                        "candidate_route_status": "dataset_candidate_not_promoted",
                        "identity_claim_status": "no_identity_claim",
                        "rights_status": "metadata_only_until_verified",
                        "cross_source_status": crosswalk.get(
                            "cross_source_status", ""
                        ),
                        "crosswalk_candidate_id": crosswalk.get(
                            "crosswalk_candidate_id", ""
                        ),
                        "hust_character_id": character_id,
                        "obimd_main_candidate_id": main_candidate_id,
                        "obimd_main_source_uid": main_row["source_uid"],
                        "obimd_subcharacter_uid": component["source_subcharacter_uid"],
                        "component_candidate_id": component_id,
                        "route_files": [
                            DEFAULT_CROSSWALK.as_posix(),
                            DEFAULT_MAIN.as_posix(),
                            DEFAULT_COMPONENTS.as_posix(),
                            DEFAULT_COMPONENT_MAP.as_posix(),
                            crosswalk.get("candidate_packet_path", ""),
                        ],
                        "source_rights_statuses": {
                            "src-hust-obc": "source_marked_risk_noted",
                            "src-obimd": "metadata_only_until_verified",
                        },
                        "missing_evidence": [
                            "side-by-side glyph and component image review",
                            "independent paleographic component argument",
                            "inscription context and catalog evidence",
                        ],
                    }
                )
    if not edges:
        raise ValueError("no cross-source component candidate routes were built")
    return edges


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            file.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--crosswalk", default=str(DEFAULT_CROSSWALK))
    parser.add_argument("--main", default=str(DEFAULT_MAIN))
    parser.add_argument("--components", default=str(DEFAULT_COMPONENTS))
    parser.add_argument("--component-map", default=str(DEFAULT_COMPONENT_MAP))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    edges = build_edges(
        read_csv_rows(root / args.crosswalk),
        read_csv_rows(root / args.main),
        read_csv_rows(root / args.components),
        read_csv_rows(root / args.component_map),
    )
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
