#!/usr/bin/env python3
"""Build a human-readable audit for candidate variant routes."""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from collections import Counter
from pathlib import Path


STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
GRAPH = Path("corpus/008_relationship-graph/014_character-variant-graph-edges.jsonl")
HUMAN_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "225_character-variant-linkage-audit.md"
)
INDEX_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "226_character-variant-linkage-audit-index.json"
)
MAX_HUMAN_LINE_LENGTH = 80


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wrap(text: str) -> str:
    return textwrap.fill(text, width=78, break_long_words=True,
                         break_on_hyphens=False)


def read_rows(root: Path) -> list[dict[str, str]]:
    with (root / STAGING).open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_edges(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with (root / GRAPH).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build(root: Path) -> tuple[str, dict[str, object]]:
    staging_rows = read_rows(root)
    edges = read_edges(root)
    relations = Counter(row.get("relation_type", "") for row in staging_rows)
    statuses = Counter(str(row.get("promotion_status", "")) for row in staging_rows)
    main_refs = {row.get("main_character_external_ref_id", "") for row in staging_rows}
    sub_refs = {row.get("subcharacter_external_ref_id", "") for row in staging_rows}
    review_statuses = Counter(str(edge.get("review_status", "")) for edge in edges)
    index = {
        "record_type": "character_variant_linkage_audit_index",
        "human_readable_file": HUMAN_OUTPUT.as_posix(),
        "staging_file": STAGING.as_posix(),
        "graph_file": GRAPH.as_posix(),
        "source_id": "src-obimd",
        "staging_row_count": len(staging_rows),
        "graph_edge_count": len(edges),
        "unique_subcharacter_count": len(sub_refs - {""}),
        "unique_main_character_count": len(main_refs - {""}),
        "relation_type_counts": dict(sorted(relations.items())),
        "promotion_status_counts": dict(sorted(statuses.items())),
        "graph_review_status_counts": dict(sorted(review_statuses.items())),
        "review_status": "candidate_variant_routes_require_human_review",
        "claim_boundary": [
            "no formal variant judgment",
            "no oracle-character identity claim",
            "no accepted reading",
            "no decipherment conclusion",
        ],
        "updated_at": "2026-07-29",
    }
    relation_text = "; ".join(
        f"{key or 'blank'}={value}" for key, value in sorted(relations.items())
    )
    status_text = "; ".join(
        f"{key or 'blank'}={value}" for key, value in sorted(statuses.items())
    )
    lines = [
        "# Character-Variant Linkage Audit / 字形—异体关联审计",
        "",
        "## Human Reading Result / 人类阅读结果",
        "",
        f"- OBIMD staging rows: {len(staging_rows)}",
        f"- Candidate variant graph edges: {len(edges)}",
        f"- Unique sub-character references: {len(sub_refs - {''})}",
        f"- Unique main-character references: {len(main_refs - {''})}",
        f"- Relation types: {relation_text}",
        f"- Promotion statuses: {status_text}",
        "- Graph review status: all rows remain `needs_cross_source_review`.",
        "",
        "## What The Current Evidence Says / 当前证据说明",
        "",
        wrap(
            "The rows reproduce the relation recorded by the OBIMD staging "
            "table. They are source metadata and a review route, not a "
            "paleographic decision that two forms are variants."
        ),
        "",
        wrap(
            "The project-local source node is an OBIMD sub-character candidate "
            "and the target is an OBIMD main-character reference. It does not "
            "confirm an identity, variant relation, or specific oracle-bone sign."
        ),
        "",
        "## Evidence Required Before Promotion / 提升关系前必须补齐的证据",
        "",
        "- Open both glyph images and record a neutral side-by-side observation.",
        "- Check the source workbook row, checksum, rights note, and manifest.",
        "- Compare the forms against HUST-OBC, Xiaoxuetang, and other sources.",
        "- Record period, findspot, inscription context, and catalog references.",
        "- Record published proposals, dissent, reviewer, and review date.",
        "- Keep the edge candidate-only when any of these checks is missing.",
        "",
        "## Human Opening Order / 人类复核顺序",
        "",
        "- Start with the component-candidate human dossier and visual gallery.",
        "- Open `002_obimd-subcharacter-main-staging.csv` for the source row.",
        "- Follow the co-located image, rights, and source-manifest routes.",
        "- Compare the candidate with character dossiers only after visual review.",
        "- Use `226_character-variant-linkage-audit-index.json` for counts only.",
        "",
        "## Boundary / 边界",
        "",
        wrap(
            "This audit and its graph edges support preprocessing and human "
            "review only. They do not confirm an identity, variant relation, "
            "reading, inscription assignment, or decipherment conclusion."
        ),
        "",
        "本审计及图边只服务于预处理和人工复核，不确认字形身份、异体关系、",
        "释读、卜辞归属或破译结论。",
    ]
    text = "\n".join(lines) + "\n"
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(f"{HUMAN_OUTPUT}:{line_number} exceeds 80 characters")
    return text, index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    text, index = build(root)
    (root / HUMAN_OUTPUT).write_text(text, encoding="utf-8", newline="\n")
    (root / INDEX_OUTPUT).write_text(
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(f"staging_rows={index['staging_row_count']} graph_edges={index['graph_edge_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
