#!/usr/bin/env python3
"""Build a human-readable audit for component candidate routes."""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path


GRAPH_PATH = Path(
    "corpus/008_relationship-graph/"
    "016_character-component-candidate-graph-edges.jsonl"
)
HUMAN_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "232_character-component-linkage-audit.md"
)
INDEX_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "233_character-component-linkage-audit-index.json"
)
MAX_HUMAN_LINE_LENGTH = 80


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wrap(text: str) -> str:
    return textwrap.fill(
        text,
        width=78,
        break_long_words=True,
        break_on_hyphens=False,
    )


def read_rows(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with (root / GRAPH_PATH).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_audit(root: Path) -> tuple[str, dict[str, object]]:
    rows = read_rows(root)
    character_ids = sorted({str(row["source_node_id"]) for row in rows})
    component_ids = sorted({str(row["target_node_id"]) for row in rows})
    promoted_count = sum(
        1
        for row in rows
        if row.get("candidate_route_status") != "dataset_candidate_not_promoted"
    )
    index: dict[str, object] = {
        "record_type": "character_component_linkage_audit_index",
        "human_readable_file": HUMAN_OUTPUT.as_posix(),
        "graph_file": GRAPH_PATH.as_posix(),
        "candidate_edge_count": len(rows),
        "candidate_edge_type": "CHARACTER_HAS_COMPONENT_CANDIDATE",
        "character_candidate_count": len(character_ids),
        "component_candidate_count": len(component_ids),
        "promoted_formal_relation_count": promoted_count,
        "source_ids": ["src-hust-obc", "src-obimd"],
        "review_status": "needs_cross_source_review",
        "rights_status": "metadata_only_until_verified",
        "claim_boundary": [
            "not a formal component assignment",
            "not a confirmed character identity",
            "not a decipherment conclusion",
        ],
        "required_next_checks": [
            "side-by-side glyph and component image review",
            "independent paleographic component argument",
            "inscription context and catalog evidence",
        ],
        "updated_at": "2026-08-13",
    }

    paragraphs = [
        "# Character-Component Linkage Audit / "
        "\u5b57\u5f62\u2014\u6784\u4ef6\u5173\u8054\u5ba1\u8ba1",
        "",
        "## Human Reading Result / \u4eba\u7c7b\u9605\u8bfb\u7ed3\u679c",
        "",
        wrap(
            f"The graph contains {len(rows)} explicit cross-source candidate "
            f"routes, joining {len(character_ids)} HUST character candidates "
            f"to {len(component_ids)} OBIMD component candidates."
        ),
        wrap(
            f"\u56fe\u4e2d\u6709 {len(rows)} \u6761\u8de8\u6765\u6e90\u6784\u4ef6\u5019\u9009\u8def\u7ebf\uff0c\u8fde\u63a5 "
            f"{len(character_ids)} \u4e2a HUST \u5b57\u5f62\u5019\u9009\u548c "
            f"{len(component_ids)} \u4e2a OBIMD \u6784\u4ef6\u5019\u9009\u3002"
        ),
        "",
        wrap("Every row is a dataset and crosswalk route only."),
        "It is not a formal component assignment.",
        "It is not a confirmed character identity.",
        "It is not a decipherment conclusion.",
        wrap(
            "\u6bcf\u4e00\u884c\u90fd\u53ea\u662f\u6570\u636e\u96c6\u548c\u8de8\u8868\u8def\u7ebf\uff0c\u4e0d\u662f\u6b63\u5f0f\u6784\u4ef6\u5f52\u5c5e\uff0c"
            "\u4e0d\u786e\u8ba4\u7532\u9aa8\u5b57\u8eab\u4efd\uff0c\u4e5f\u4e0d\u662f\u91ca\u8bfb\u6216\u7834\u8bd1\u7ed3\u8bba\u3002"
        ),
        "",
        wrap(
            f"Promoted formal character-component relations: {promoted_count}. "
            "The current value must remain zero until independent evidence is "
            "opened and reviewed."
        ),
        wrap(
            f"\u5df2\u63d0\u5347\u4e3a\u6b63\u5f0f\u5b57\u5f62\u2014\u6784\u4ef6\u5173\u7cfb\uff1a{promoted_count}\u3002\u5728\u72ec\u7acb\u8bc1\u636e\u6253\u5f00\u5e76\u590d\u6838\u524d\uff0c"
            "\u8be5\u6570\u503c\u5fc5\u987b\u4fdd\u6301\u4e3a\u96f6\u3002"
        ),
        "",
        "## Source Route / \u6765\u6e90\u8def\u7ebf",
        "",
        wrap(
            "The route starts with the HUST-OBIMD-EvoBC codepoint crosswalk, "
            "joins OBIMD main-character staging, then follows the OBIMD "
            "sub-character mapping and the project component-ID map."
        ),
        wrap(
            "\u8def\u7ebf\u4ece HUST\u2014OBIMD\u2014EvoBC \u5b57\u7801\u4ea4\u53c9\u8868\u5f00\u59cb\uff0c\u63a5\u5165 OBIMD \u4e3b\u5b57\u5f62\u6682\u5b58\u8868\uff0c"
            "\u518d\u6cbf OBIMD \u5b50\u5b57\u5f62\u6620\u5c04\u548c\u9879\u76ee\u6784\u4ef6 ID \u5bf9\u7167\u8868\u8ffd\u8e2a\u3002"
        ),
        "",
        wrap(
            f"Machine support: `{GRAPH_PATH.as_posix()}`. The JSONL is an "
            "index for tracing; the human dossier remains the research entry."
        ),
        wrap(
            "\u673a\u5668\u8f85\u52a9\u6587\u4ef6\u53ea\u7528\u4e8e\u8ffd\u6eaf\u548c\u68c0\u7d22\uff1b\u4eba\u7c7b\u6863\u6848\u4ecd\u662f\u7814\u7a76\u5165\u53e3\uff0c\u4e0d\u80fd\u7531 JSONL \u66ff\u4ee3\u3002"
        ),
        "",
        "## Evidence Still Required / \u4ecd\u9700\u8865\u9f50\u7684\u8bc1\u636e",
        "",
        "- Open side-by-side glyph and component images with rights notes.",
        "- \u6253\u5f00\u5e76\u6392\u5b57\u5f62\u4e0e\u6784\u4ef6\u56fe\u50cf\uff0c\u5e76\u8bb0\u5f55\u6743\u5229\u72b6\u6001\u3002",
        "- Add an independent paleographic component argument for each route.",
        "- \u4e3a\u6bcf\u6761\u8def\u7ebf\u8865\u5145\u72ec\u7acb\u7684\u6587\u5b57\u5b66\u6784\u4ef6\u8bba\u8bc1\u3002",
        "- Link inscription context, catalog identity, and exact source locators.",
        "- \u8865\u5145\u535c\u8f9e\u4e0a\u4e0b\u6587\u3001\u8457\u5f55\u8eab\u4efd\u548c\u7cbe\u786e\u6765\u6e90\u5b9a\u4f4d\u3002",
        "- Record disagreement, reviewer, and a reproducible review decision.",
        "- \u8bb0\u5f55\u5206\u6b67\u3001\u590d\u6838\u8005\u548c\u53ef\u590d\u8dd1\u7684\u590d\u6838\u51b3\u5b9a\u3002",
        "",
        "## Boundary / \u8fb9\u754c",
        "",
        wrap(
            "This is preprocessing and review routing. It does not assign a "
            "reading, establish a component etymology, or publish scholarship."
        ),
        wrap(
            "\u672c\u9875\u53ea\u670d\u52a1\u4e8e\u9884\u5904\u7406\u548c\u590d\u6838\u8def\u7ebf\uff0c\u4e0d\u5206\u914d\u91ca\u8bfb\uff0c\u4e0d\u5efa\u7acb\u6784\u4ef6\u5b57\u6e90\uff0c\u4e5f\u4e0d\u53d1\u5e03\u5b66\u672f\u7ed3\u8bba\u3002"
        ),
        "",
    ]
    text = "\n".join(paragraphs)
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(f"{HUMAN_OUTPUT}:{line_number} exceeds 80 characters")
    return text, index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    text, index = build_audit(root)
    (root / HUMAN_OUTPUT).write_text(text, encoding="utf-8", newline="\n")
    (root / INDEX_OUTPUT).write_text(
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"candidate_edges={index['candidate_edge_count']} "
        f"characters={index['character_candidate_count']} "
        f"components={index['component_candidate_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
