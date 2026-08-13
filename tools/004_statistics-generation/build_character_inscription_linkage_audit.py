#!/usr/bin/env python3
"""Build a human-readable audit for character-inscription linkage coverage."""

from __future__ import annotations

import argparse
import json
import textwrap
from collections import Counter
from pathlib import Path


PACKET_ROOT = Path("corpus/002_oracle-bone-inscriptions")
GRAPH_ROOT = Path("corpus/008_relationship-graph")
CAMBRIDGE_HOPKINS_GRAPH = (
    "008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl"
)
HUMAN_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "223_character-inscription-linkage-audit.md"
)
INDEX_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "224_character-inscription-linkage-audit-index.json"
)
LINK_FIELDS = (
    "linked_glyphs",
    "linked_characters",
    "character_routes",
    "linked_glyph_candidates",
)
CANDIDATE_EDGE_MARKER = "candidate_not_promoted"
MAX_HUMAN_LINE_LENGTH = 80


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wrap_bullet(text: str) -> str:
    return textwrap.fill(
        f"- {text}",
        width=78,
        subsequent_indent="  ",
        break_long_words=True,
        break_on_hyphens=False,
    )


def graph_edge_rows(
    root: Path,
) -> tuple[int, int, Counter[str], Counter[str]]:
    total = 0
    cambridge_hopkins_total = 0
    promoted_types: Counter[str] = Counter()
    candidate_types: Counter[str] = Counter()
    for path in sorted((root / GRAPH_ROOT).glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                row = json.loads(line)
                total += 1
                if path.name == CAMBRIDGE_HOPKINS_GRAPH:
                    cambridge_hopkins_total += 1
                edge_type = str(row.get("edge_type", ""))
                if "character" in edge_type.lower() and "inscription" in edge_type.lower():
                    if CANDIDATE_EDGE_MARKER in str(row.get("candidate_route_status", "")):
                        candidate_types[edge_type] += 1
                    else:
                        promoted_types[edge_type] += 1
    return total, cambridge_hopkins_total, promoted_types, candidate_types


def build_audit(root: Path) -> tuple[str, dict[str, object]]:
    packet_count = 0
    packets_with_explicit_link_fields = 0
    field_counts: Counter[str] = Counter()
    for path in sorted((root / PACKET_ROOT).rglob("01_*packet.json")):
        with path.open("r", encoding="utf-8-sig") as file:
            packet = json.load(file)
        packet_count += 1
        present = [field for field in LINK_FIELDS if packet.get(field)]
        if present:
            packets_with_explicit_link_fields += 1
            field_counts.update(present)

    (
        graph_total,
        cambridge_hopkins_total,
        character_inscription_edge_types,
        character_inscription_candidate_edge_types,
    ) = graph_edge_rows(root)
    promoted_edge_count = sum(character_inscription_edge_types.values())
    candidate_edge_count = sum(character_inscription_candidate_edge_types.values())
    status = (
        "candidate_only_no_character_inscription_edge_promoted"
        if promoted_edge_count == 0
        else "character_inscription_edges_require_human_review"
    )
    index = {
        "record_type": "character_inscription_linkage_audit_index",
        "human_readable_file": HUMAN_OUTPUT.as_posix(),
        "packet_root": PACKET_ROOT.as_posix(),
        "graph_root": GRAPH_ROOT.as_posix(),
        "packet_count": packet_count,
        "packets_with_explicit_character_link_fields": packets_with_explicit_link_fields,
        "explicit_link_field_counts": dict(sorted(field_counts.items())),
        "graph_edge_count_all_jsonl": graph_total,
        "cambridge_hopkins_graph_edge_count": cambridge_hopkins_total,
        "character_inscription_edge_count": promoted_edge_count,
        "character_inscription_edge_types": dict(sorted(character_inscription_edge_types.items())),
        "character_inscription_candidate_edge_count": candidate_edge_count,
        "character_inscription_candidate_edge_types": dict(
            sorted(character_inscription_candidate_edge_types.items())
        ),
        "review_status": status,
        "claim_boundary": [
            "no character-inscription identity claim",
            "no formal inscription assignment",
            "no transcription or inscription reading",
            "no decipherment conclusion",
        ],
        "updated_at": "2026-08-13",
    }

    field_text = ", ".join(LINK_FIELDS)
    if packets_with_explicit_link_fields:
        evidence_result = (
            f"{packets_with_explicit_link_fields} packet(s) expose one or more "
            f"explicit linkage fields: {field_text}. These values still require "
            "plate, text, position, source, and human review before an edge is "
            "promoted."
        )
    else:
        evidence_result = (
            "No packet exposes an explicit linked-character field. The current "
            "candidate rows contain catalog and period/group routing clues, but "
            "do not identify a character project ID or a character position in a "
            "plate, image, or inscription text."
        )
    if promoted_edge_count:
        edge_result = (
            f"{promoted_edge_count} character-inscription graph edge(s) exist; "
            "each must remain in human review until its evidence route is opened."
        )
    elif candidate_edge_count:
        edge_result = (
            "Zero character-inscription graph edges are promoted. "
            f"{candidate_edge_count} candidate route edge(s) are present, but "
            "they remain dataset-only routes until plate, text, position, and "
            "identity evidence is reviewed."
        )
    else:
        edge_result = (
            "Zero character-inscription graph edges are promoted. Candidate "
            "routes, if present, remain separate from formal relations. This is "
            "an audited evidence gap, not evidence that inscriptions contain no "
            "characters."
        )

    text = "\n".join(
        [
            "# Character-Inscription Linkage Audit / 字形—卜辞关联审计",
            "",
            "## Human Reading Result / 人类阅读结果",
            "",
            wrap_bullet(f"Candidate packet count: {packet_count}"),
            wrap_bullet(
                "Packets with explicit character-link fields: "
                f"{packets_with_explicit_link_fields}"
            ),
            wrap_bullet(f"Graph edges scanned across JSONL files: {graph_total}"),
            wrap_bullet(
                "Cambridge/Hopkins catalog-route graph edges: "
                f"{cambridge_hopkins_total}"
            ),
            wrap_bullet(
                "Character-inscription edges promoted: "
                f"{promoted_edge_count}"
            ),
            wrap_bullet(
                "Character-inscription candidate routes: "
                f"{candidate_edge_count}"
            ),
            wrap_bullet(f"Review state: `{status}`"),
            "",
            "## What The Current Evidence Says / 当前证据说明",
            "",
            textwrap.fill(
                "The raw JSONL row count is used here. The legacy graph summary "
                "may count one edge once per source membership, so its total is "
                "not the same denominator.",
                width=78,
                break_long_words=True,
            ),
            "本审计使用 JSONL 原始行数。旧版图谱统计可能按每个 source membership",
            "重复计数，因此两者的总数分母并不相同。",
            "",
            textwrap.fill(evidence_result, width=78, break_long_words=True),
            "",
            textwrap.fill(edge_result, width=78, break_long_words=True),
            "",
            textwrap.fill(
                f"The {cambridge_hopkins_total:,} Cambridge/Hopkins graph routes "
                "currently describe source, "
                "download, period, group, and catalog references. They do not supply "
                "a plate position or a linked character identity.",
                width=78,
                break_long_words=True,
            ),
            "",
            "当前 Cambridge/Hopkins 图边只描述来源、下载记录、时期、组类和著录路线。",
            "它们没有提供图版位置或已关联的字形身份。",
            "",
            "## Evidence Required Before A Relation Edge / 建边前必须补齐的证据",
            "",
            wrap_bullet(
                "Open the cited plate, rubbing, photograph, or collection image and "
                "record its exact source route and rights status."
            ),
            wrap_bullet(
                "Capture the full inscription or OCR as a source transcription, with "
                "unreadable signs and uncertain positions marked."
            ),
            wrap_bullet(
                "Record the exact plate/image position of each proposed character "
                "occurrence; do not infer it from a filename or catalog number."
            ),
            wrap_bullet(
                "Link the occurrence to an existing character dossier only when the "
                "source evidence and project ID are explicit."
            ),
            wrap_bullet(
                "Record the reviewer, source citation, disagreement, and review "
                "status before changing the edge to a reviewed relation."
            ),
            "",
            "## Human Opening Order / 人类复核顺序",
            "",
            wrap_bullet(
                "Start with each object-local `07_human-inscription-dossier.md` "
                "and `21_character-inscription-linkage-review.md`."
            ),
            wrap_bullet(
                "For the H2 source-record candidate, open its `02_human-"
                "inscription-dossier.md` and `09_character-inscription-"
                "candidate-graph-route.md`."
            ),
            wrap_bullet(
                "Then open `06_plate-text-gallery.md`, `03_catalog-reference-index.csv`, "
                "and `13_text-ocr-quality-review.md`."
            ),
            wrap_bullet(
                "Follow the source object dossier and download/manifest records "
                "before collecting a new image or text route."
            ),
            wrap_bullet(
                "Use `224_character-inscription-linkage-audit-index.json` only as a "
                "machine-readable count supporting this report."
            ),
            "",
            "## Boundary / 边界",
            "",
            textwrap.fill(
                "This audit is preprocessing and review routing only. It does not "
                "make a character-inscription identity claim, assign a formal "
                "`obi-*` ID, accept a transcription, propose a reading, or conclude "
                "decipherment.",
                width=78,
                break_long_words=True,
            ),
            "It is not a formal `obi-*` ID assignment and does not propose a reading.",
            "",
            "本审计只服务于预处理和人工复核路线，不确认字形—卜辞身份关系，",
            "不分配正式 `obi-*` 编号，不接受释文，不提出释读，也不形成破译结论。",
        ]
    )
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(f"{HUMAN_OUTPUT}:{line_number} exceeds 80 characters")
    return text + "\n", index


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
        "packet_count="
        f"{index['packet_count']} "
        "explicit_link_packets="
        f"{index['packets_with_explicit_character_link_fields']} "
        "character_inscription_edges="
        f"{index['character_inscription_edge_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
