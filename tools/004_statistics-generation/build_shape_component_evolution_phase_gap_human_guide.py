#!/usr/bin/env python3
"""Build a human guide for shape/component/evolution phase gaps.

The guide turns the 196 checklist into a researcher-facing entrance for
codepoint-route, component-candidate, and evolution-correspondence gaps. It
does not confirm identity, assign components, accept evolution chains, or make
decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CHECKLIST = STAT_DIR / "196_shape-component-evolution-verification-gap-review-checklist.csv"
ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
CODEPOINT_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
CODEPOINT_REVIEW_QUEUE = (
    STAT_DIR / "041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv"
)
CODEPOINT_READINESS = (
    STAT_DIR
    / "048_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-readiness-checklist.csv"
)
HUST_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)
COMPONENT_MAIN_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
COMPONENT_GLYPH_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "003_obimd-subcharacter-glyph-staging.csv"
)
COMPONENT_ID_SOURCE_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "004_component-id-source-map.csv"
)
COMPONENT_GRAPH_EDGES = Path(
    "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl"
)
COMPONENT_REVIEW_DIR = Path(
    "doc/public/user_research/002_cross-source-review-queues/obimd"
)
COMPONENT_OBJECT_DIR = Path("corpus/003_graphemic-components")
EVOLUTION_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
EVOLUTION_ID_SOURCE_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "005_evolution-candidate-id-source-map.csv"
)
EVOLUTION_GRAPH_EDGES = Path(
    "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl"
)
EVOLUTION_REVIEW_DIR = Path(
    "doc/public/user_research/002_cross-source-review-queues/evobc"
)
EVOLUTION_OBJECT_DIR = Path("corpus/004_bronze-seal-modern-correspondences")
DEFAULT_OUTPUT = STAT_DIR / "219_shape-component-evolution-phase-gap-human-guide.md"
UPDATED_AT = "2026-06-30"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def append_wrapped_bullet(lines: list[str], text: str) -> None:
    if len(text) <= 78:
        lines.append(f"- {text}")
        return
    words = text.split(" ")
    current = "- "
    for word in words:
        next_value = f"{current}{word}" if current == "- " else f"{current} {word}"
        if len(next_value) <= 78:
            current = next_value
            continue
        lines.append(current)
        current = f"  {word}"
    if current.strip():
        lines.append(current)


def build_markdown(root: Path) -> str:
    rows = read_csv_rows(root / CHECKLIST)
    codepoint = next(row for row in rows if row["corpus_area"] == "cross_source_codepoint_routes")
    component = next(row for row in rows if row["corpus_area"] == "graphemic_components")
    evolution = next(row for row in rows if row["corpus_area"] == "evolution_correspondences")
    phase_statuses = [
        f"{row['corpus_area']}: {row['phase_name']} `{row['phase_status']}`"
        for row in rows
    ]
    slots = unique_values(
        [
            slot
            for row in rows
            for slot in split_values(row["required_verification_slots"])
        ]
    )
    source_fields = unique_values(
        [
            field
            for row in rows
            for field in split_values(row["source_context_fields_to_verify"])
        ]
    )
    next_checks = unique_values(
        [
            check
            for row in rows
            for check in split_values(row["concrete_next_checks"])
        ]
    )

    slot_labels = {
        "source_codepoint": "source codepoint",
        "source_character_id": "source character id",
        "matched_project_character_route": "matched project character route",
        "matched_source_ids": "matched source ids",
        "readiness_route": "readiness route",
        "promotion_review_route": "promotion review route",
        "missing_evidence": "missing evidence",
        "review_status": "review status",
        "component_candidate_id": "component candidate",
        "component_shape_label": "component shape label",
        "glyph_image_route": "glyph image route",
        "host_character_route": "host character route",
        "subcharacter_source_row": "subcharacter source row",
        "component_graph_edge_route": "component graph edge route",
        "missing_visual_evidence": "missing visual evidence",
        "evolution_candidate_id": "evolution candidate",
        "oracle_source_route": "oracle source route",
        "bronze_seal_modern_route": "bronze, seal, or modern route",
        "correspondence_category": "correspondence category",
        "source_category_row": "source category row",
        "evolution_graph_edge_route": "evolution graph edge route",
        "missing_comparison_evidence": "missing comparison evidence",
    }

    lines = [
        "# Shape Component Evolution Phase Gap Human Guide /",
        "形体构件演化阶段缺口人工复核指南",
        "",
        "English:",
        "This guide is the human entrance for codepoint-route,",
        "component-candidate, and evolution-correspondence phase gaps.",
        "Reviewers should open concrete object folders and visual evidence",
        "before using CSV rows, graph edges, or JSON packets as pointers.",
        "It is not an identity confirmation, not a component assignment,",
        "not an accepted evolution correspondence,",
        "not confirmed scholarship, and not a decipherment conclusion.",
        "",
        "简体中文：",
        "本指南是跨来源 codepoint、构件候选和演化对应阶段缺口的",
        "人工复核入口。",
        "复核者应先打开具体对象目录和可视证据，",
        "再把 CSV 行、图边或 JSON 包当作辅助路线使用。",
        "它不是字形身份确认，不是构件归属，",
        "不是已接受的演化对应，",
        "不是已确认学术结论，也不是释读结论。",
        "",
        "## Summary / 摘要",
        "",
        f"- updated at: {UPDATED_AT}",
        f"- checklist rows: {len(rows)}",
        f"- codepoint staging rows: {codepoint['primary_staging_count']}",
        f"- component candidate rows: {component['primary_staging_count']}",
        f"- component glyph rows: {component['supporting_staging_count']}",
        f"- evolution candidate rows: {evolution['primary_staging_count']}",
        f"- component graph edges: {component['graph_edge_count']}",
        f"- evolution graph edges: {evolution['graph_edge_count']}",
        "- source ids:",
    ]
    for source_id in split_values(";".join(row["source_ids"] for row in rows)):
        lines.append(f"  - `{source_id}`")
    lines.append("- phase gap statuses:")
    for status in phase_statuses:
        lines.append(f"  - {status}")

    lines.extend(
        [
            "",
            "## Human Review Entry Order / 人工复核入口顺序",
            "",
            "1. Open the concrete character, component, or evolution object first.",
            "2. Open an `obs-char-*`, component, or evolution folder.",
            "3. Inspect glyph images, rubbings, photos, or visual routes.",
            "4. Compare variants, near forms, and component clues.",
            "5. Check the source codepoint and source character id.",
            "6. Check HUST, OBIMD, or EvoBC source rows.",
            "7. Check the host character and object-local dossier.",
            "8. Check bronze, seal, or modern correspondence routes.",
            "9. Check source provenance, rights status, and risk note.",
            "10. Record missing items as concrete next-source questions.",
            "11. Open graph edges only as routes, not as conclusions.",
            "12. Do not confirm a component from this guide.",
            "13. Do not accept an evolution chain from this guide.",
            "",
            "人工复核时，先打开具体单字、构件或演化对象目录，",
            "再看图像、拓片、照片、异体、近形、构件线索和出处。",
            "结构化清单只能帮助定位，不得替代人类可读档案。",
            "",
            "## Support Files / 辅助文件",
            "",
            "| File | Path |",
            "| --- | --- |",
            f"| checklist | `{CHECKLIST.as_posix()}` |",
            f"| action queue | `{ACTION_QUEUE.as_posix()}` |",
            f"| codepoint staging | `{CODEPOINT_STAGING.as_posix()}` |",
            f"| codepoint review queue | `{CODEPOINT_REVIEW_QUEUE.as_posix()}` |",
            f"| codepoint readiness | `{CODEPOINT_READINESS.as_posix()}` |",
            f"| HUST promotion queue | `{HUST_PROMOTION_QUEUE.as_posix()}` |",
            f"| component staging | `{COMPONENT_MAIN_STAGING.as_posix()}` |",
            f"| component glyph staging | `{COMPONENT_GLYPH_STAGING.as_posix()}` |",
            f"| component ID source map | `{COMPONENT_ID_SOURCE_MAP.as_posix()}` |",
            f"| component graph edges | `{COMPONENT_GRAPH_EDGES.as_posix()}` |",
            f"| component review route | `{COMPONENT_REVIEW_DIR.as_posix()}` |",
            f"| component object folders | `{COMPONENT_OBJECT_DIR.as_posix()}` |",
            f"| evolution staging | `{EVOLUTION_STAGING.as_posix()}` |",
            f"| evolution ID source map | `{EVOLUTION_ID_SOURCE_MAP.as_posix()}` |",
            f"| evolution graph edges | `{EVOLUTION_GRAPH_EDGES.as_posix()}` |",
            f"| evolution review route | `{EVOLUTION_REVIEW_DIR.as_posix()}` |",
            f"| evolution object folders | `{EVOLUTION_OBJECT_DIR.as_posix()}` |",
            "",
            "Open these files after object-local human materials.",
            "They are route and provenance aids, not accepted readings.",
            "",
            "## Required Verification Slots / 必查复核槽位",
            "",
        ]
    )
    for slot in slots:
        lines.append(f"- {slot_labels.get(slot, slot)}")
    lines.extend(
        [
            "- variant and near-form comparison",
            "- component visual evidence",
            "- bronze, seal, and modern-script comparison",
            "- source provenance and risk note",
            "- unresolved dispute or missing evidence",
            "",
            "Each slot should point back to a visible source, object folder,",
            "or review note before any later human reviewer decides status.",
            "每个槽位都应指回可见来源、对象目录或复核记录，",
            "等待后续人工判断状态。",
            "",
            "## Source Context Fields / 来源语境字段",
            "",
        ]
    )
    for field in source_fields:
        lines.append(f"- `{field}`")
    lines.extend(
        [
            "",
            "These fields support provenance review only.",
            "They do not confirm identity, component, or correspondence.",
            "这些字段只服务来源复核，",
            "不确认身份、构件或对应关系。",
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
        ]
    )
    for check in next_checks:
        append_wrapped_bullet(lines, check)
    lines.extend(
        [
            "- Which glyph image or visual route can be opened directly?",
            "- Which variant, near form, or component clue must be compared?",
            "- Which bronze, seal, or modern correspondence is only a route?",
            "- Which source row, field map, or extraction note is missing?",
            "- Which review note records disagreement or uncertainty?",
            "- 哪一张字形图片或可视路线可以直接打开？",
            "- 哪一个异体、近形或构件线索必须比较？",
            "- 哪一条金文、小篆或今字对应还只是路线？",
            "- 哪一条来源行、字段映射或抽取说明仍然缺失？",
            "- 哪一条复核记录写有分歧或不确定性？",
            "",
            "## Boundary / 边界",
            "",
            "Do not record reviewed outcomes in this guide.",
            "Do not treat a checklist row as evidence by itself.",
            "Do not treat a graph edge as a component claim.",
            "Do not treat an EvoBC route as an evolution conclusion.",
            "Do not confirm identity from a codepoint route.",
            "Do not confirm a component from this guide.",
            "Do not accept an evolution chain from this guide.",
            "Do not write any candidate as confirmed scholarship.",
            "Do not write any candidate as a decipherment conclusion.",
            "",
            "不得在本指南中记录复核结论。",
            "不得把清单行本身当作证据。",
            "不得把图边当作构件结论。",
            "不得把 EvoBC 路线当作演化结论。",
            "不得根据 codepoint 路线确认字形身份。",
            "不得从本指南确认构件。",
            "不得从本指南接受演化链。",
            "不得把任何候选写成已确认学术结论。",
            "不得把任何候选写成释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the shape component evolution phase gap human guide."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    write_markdown(root / args.output, build_markdown(root))
    print(f"shape_component_evolution_phase_gap_human_guide={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
