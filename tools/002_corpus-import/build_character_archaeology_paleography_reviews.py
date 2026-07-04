#!/usr/bin/env python3
"""Build archaeology and paleography review files for character objects.

The generated files are human-first, object-local preparation materials.
They turn existing packet, visual, source, and graph routes into a concise
review surface for archaeologists and paleographers. They do not add readings,
component assignments, inscription identities, or decipherment conclusions.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


OBJECT_ROOT = Path("corpus/001_oracle-characters")
GRAPH_FILES = [
    Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/009_character-asset-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/010_cross-source-id-graph-edges.jsonl"),
]
UPDATED_AT = "2026-07-04"
REVIEW_FILE = "10_archaeology-paleography-review.md"
INDEX_FILE = "11_archaeology-paleography-index.json"
READINESS_FILE = "12_human-research-readiness-review.md"
READINESS_INDEX_FILE = "13_human-research-readiness-index.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def project_id_from_dir(path: Path) -> str:
    for part in path.name.split("_"):
        if part.startswith("obs-char-") or part.startswith("obs-unk-"):
            return part
    raise ValueError(f"Cannot find project id in {path}")


def discover_packet_dirs(root: Path) -> list[dict[str, Any]]:
    packet_paths = [
        *(root / OBJECT_ROOT).glob("*/*/01_candidate-character-packet.json"),
        *(root / OBJECT_ROOT).glob("*/*/01_undeciphered-candidate-packet.json"),
    ]
    records: list[dict[str, Any]] = []
    for packet_path in sorted(packet_paths):
        object_dir = packet_path.parent
        records.append(
            {
                "project_id": project_id_from_dir(object_dir),
                "object_dir": object_dir,
                "packet_path": packet_path,
                "packet_name": packet_path.name,
            }
        )
    return records


def graph_edges_by_source(root: Path) -> dict[str, list[dict[str, Any]]]:
    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relative in GRAPH_FILES:
        for edge in read_jsonl(root / relative):
            source = str(edge.get("source_node_id", ""))
            if source.startswith(("obs-char-", "obs-unk-")):
                copied = dict(edge)
                copied["graph_file"] = relative.as_posix()
                edges[source].append(copied)
    return edges


def dataset_label(packet: dict[str, Any]) -> dict[str, str]:
    label = packet.get("dataset_label")
    if isinstance(label, dict):
        return {str(key): str(value) for key, value in label.items()}
    return {}


def packet_download_ids(packet: dict[str, Any]) -> list[str]:
    values = packet.get("evidence_download_ids")
    if isinstance(values, list):
        return [str(value) for value in values]
    value = packet.get("evidence_download_id")
    return [str(value)] if value else []


def packet_routes(packet: dict[str, Any]) -> list[str]:
    routes = packet.get("route_files")
    if isinstance(routes, list):
        return [str(value) for value in routes]
    return []


def packet_metadata_files(packet: dict[str, Any]) -> list[str]:
    values = packet.get("source_metadata_files")
    if isinstance(values, list):
        return [str(value) for value in values]
    return []


def visual_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    committed = [row.get("committed_image_path", "") for row in rows]
    refs = [row.get("source_image_reference_path", "") for row in rows]
    rights = sorted({row.get("rights_status", "") for row in rows if row.get("rights_status")})
    review = sorted({row.get("review_status", "") for row in rows if row.get("review_status")})
    return {
        "row_count": str(len(rows)),
        "committed_image_count": str(sum(1 for value in committed if value)),
        "source_image_route_count": str(sum(1 for value in refs if value)),
        "first_committed_image": next((Path(value).name for value in committed if value), ""),
        "first_source_image_route": next((Path(value).name for value in refs if value), ""),
        "rights_status": ";".join(rights),
        "review_status": ";".join(review),
    }


def edge_summary(edges: list[dict[str, Any]]) -> dict[str, Any]:
    type_counts = Counter(str(edge.get("edge_type", "unknown")) for edge in edges)
    route_files: list[str] = []
    graph_files: list[str] = []
    codepoints: list[str] = []
    statuses: list[str] = []
    for edge in edges:
        graph_file = str(edge.get("graph_file", ""))
        if graph_file and graph_file not in graph_files:
            graph_files.append(graph_file)
        codepoint = str(edge.get("hust_label_codepoints", ""))
        if codepoint and codepoint not in codepoints:
            codepoints.append(codepoint)
        status = str(edge.get("cross_source_status", ""))
        if status and status not in statuses:
            statuses.append(status)
        for route_file in edge.get("route_files", []) or []:
            route_file = str(route_file)
            if route_file and route_file not in route_files:
                route_files.append(route_file)
    return {
        "edge_count": len(edges),
        "edge_type_counts": dict(sorted(type_counts.items())),
        "route_files": route_files,
        "graph_files": graph_files,
        "codepoint_routes": codepoints,
        "cross_source_statuses": statuses,
    }


def short(value: str, fallback: str) -> str:
    return value if value else fallback


def compact(value: str, limit: int = 52) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def names(values: list[str], limit: int = 4) -> str:
    cleaned = [compact(Path(value).name) for value in values if value]
    shown = cleaned[:limit]
    if not shown:
        return "pending: check packet, source register, or graph route"
    while len("; ".join(shown)) > 58 and len(shown) > 1:
        shown = shown[:-1]
    extra = len(cleaned) - len(shown)
    suffix = f"; plus {extra} more" if extra > 0 else ""
    return "; ".join(shown) + suffix


def bullet(label: str, value: str) -> str:
    text = f"- {label}: {value}"
    if len(text) > 80:
        return f"- {label}:\n  {value}"
    return text


def review_text(
    project_id: str,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
) -> str:
    label = dataset_label(packet)
    visual = visual_summary(visual_rows)
    edge = edge_summary(edges)
    routes = packet_routes(packet)
    metadata = packet_metadata_files(packet)
    downloads = packet_download_ids(packet)
    lines = [
        f"# {project_id} Archaeology Paleography Review",
        "",
        f"# {project_id} 考古文字复核档案",
        "",
        "English:",
        "This file is an object-local human review surface.",
        "It starts from image, source, inscription, catalog, and provenance",
        "routes before any formal oracle-bone research claim.",
        "",
        "简体中文：",
        "本文件是对象目录内的人类复核档案。",
        "它先整理图像、来源、卜辞、著录和出处路线，",
        "再进入任何正式甲骨文研究判断。",
        "",
        "Boundary:",
        "This is not a decipherment conclusion.",
        "No reading, component, inscription identity, or later-script link is",
        "accepted here.",
        "",
        "边界：",
        "本文件不是释读结论。",
        "读法、构件、卜辞身份和后世字形对应在这里都只作待复核路线。",
        "",
        "## 1. Object Identity / 对象身份",
        "",
        bullet("project id", f"`{project_id}`"),
        bullet("primary external id", f"`{packet.get('primary_external_ref_id', '')}`"),
        bullet("source id", f"`{packet.get('source_id', '')}`"),
        bullet("packet", f"`{packet_name}`"),
        bullet("record type", f"`{packet.get('record_type', '')}`"),
        bullet("review status", f"`{packet.get('review_status', '')}`"),
        bullet("decipherment status", f"`{packet.get('decipherment_status', '')}`"),
        "",
        "## 2. Open First / 先打开的材料",
        "",
        "- `04_visual-gallery.md`",
        "- `05_human-research-dossier.md`",
        "- `06_human-review-sheet.md`",
        "- `08_character-context-evidence-dossier.md`",
        "- `02_visual-source-index.csv`",
        "- `07_research-dossier-index.json`",
        "- `09_character-context-evidence-index.json`",
        "",
        "## 3. Glyph Image And Observation / 字形图像与观察",
        "",
        bullet("visual index rows", f"`{visual['row_count']}`"),
        bullet("local review images", f"`{visual['committed_image_count']}`"),
        bullet("source image routes", f"`{visual['source_image_route_count']}`"),
        bullet("first local image", f"`{short(visual['first_committed_image'], 'pending')}`"),
        bullet("first source image", f"`{short(visual['first_source_image_route'], 'pending')}`"),
        bullet("image rights status", f"`{short(visual['rights_status'], 'pending')}`"),
        bullet("image review status", f"`{short(visual['review_status'], 'pending')}`"),
        "",
        "Questions:",
        "- Which strokes, outlines, damage, or uncertain marks are visible?",
        "- Which exact image row supports each observation?",
        "- Which observation remains only a source record?",
        "",
        "待查问题：",
        "- 哪些笔画、轮廓、残缺或不确定痕迹可以直接看见？",
        "- 每条观察由哪一行图像或来源记录支持？",
        "- 哪些观察仍只是来源记录，不能写成释读判断？",
        "",
        "## 4. Variants Near Forms Components / 异体近形构件线索",
        "",
        bullet("graph edge count", f"`{edge['edge_count']}`"),
        bullet("graph edge types", names(list(edge["edge_type_counts"].keys()))),
        bullet("codepoint routes", names(edge["codepoint_routes"])),
        bullet("cross-source status", names(edge["cross_source_statuses"])),
        "",
        "Questions:",
        "- Which variants or same-plate alternatives should be checked?",
        "- Which near forms need side-by-side visual review?",
        "- Which component route is only a candidate route?",
        "",
        "待查问题：",
        "- 哪些异体或同版异写需要继续核对？",
        "- 哪些近形字需要并排图像比较？",
        "- 哪些构件线索仍只是候选路线？",
        "",
        "## 5. Inscription Plate Catalog / 卜辞图版著录",
        "",
        bullet("route files", names(routes)),
        bullet("graph route files", names(edge["route_files"])),
        bullet("graph files", names(edge["graph_files"])),
        "",
        "Questions:",
        "- Which inscription number contains this glyph?",
        "- Which full text or OCR route preserves the surrounding context?",
        "- Which plate, page, catalog number, Heji number, or old number applies?",
        "",
        "待查问题：",
        "- 哪个卜辞编号包含这个字形？",
        "- 哪条全文或 OCR 路线保存了上下文？",
        "- 哪些图版、页码、著录号、合集号或旧著录号相关？",
        "",
        "## 6. Provenance Collection Period / 出土馆藏时期",
        "",
        bullet("source package", f"`{packet.get('source_package_id', '')}`"),
        bullet("download or access ids", names(downloads)),
        bullet("source metadata files", names(metadata)),
        bullet("rights status", f"`{packet.get('rights_status', '')}`"),
        bullet("risk note", compact(short(str(packet.get("risk_note", "")), "pending"))),
        "",
        "Questions:",
        "- Which findspot, collection, museum item, period, or group applies?",
        "- Which checksum, manifest, and rights note must be opened first?",
        "- Which raw source stays outside normal Git?",
        "",
        "待查问题：",
        "- 哪些出土地、馆藏、藏品、时期或组类记录相关？",
        "- 应先打开哪些 checksum、manifest 和权利说明？",
        "- 哪些原始来源必须留在普通 Git 之外？",
        "",
        "## 7. Reading History Disputes Later Forms",
        "",
        "## 7. 释读史争议与后世字形",
        "",
        bullet("source label status", f"`{label.get('status', '')}`"),
        bullet("source label text", f"`{label.get('source_modern_label_candidate', '')}`"),
        bullet("source label codepoints", f"`{label.get('source_modern_label_codepoints', '')}`"),
        "",
        "The source label is a lookup clue, not the oracle character identity.",
        "Later-script, bronze, seal, and modern-form routes are candidates only.",
        "",
        "来源标签只是检索线索，不是甲骨字身份。",
        "金文、小篆、后世字形和今字路线都只作候选线索。",
        "",
        "Questions:",
        "- Which bibliography discusses reading history or disputes?",
        "- Which scholar, database, or catalog proposed each route?",
        "- Which disagreement must stay pending before formal research?",
        "",
        "待查问题：",
        "- 哪些文献讨论释读史或争议？",
        "- 每条路线由哪位学者、数据库或著录提出？",
        "- 哪些分歧在正式研究前必须继续标为待复核？",
        "",
        "## 8. Review State / 复核状态",
        "",
        "- accepted reading: `not_reviewed`",
        "- accepted meaning: `not_reviewed`",
        "- component assignment: `not_reviewed`",
        "- inscription identity: `not_reviewed`",
        "- later-script correspondence: `not_reviewed`",
        "- decipherment conclusion: `no_claim`",
        "",
        "## 9. Next Source Checks / 下一步来源核查",
        "",
        "- Open visual rows before writing glyph observations.",
        "- Open inscription and plate routes before citing context.",
        "- Open source registry, manifest, checksum, and rights notes.",
        "- Open bibliography before recording reading history or disputes.",
        "- Keep every unresolved item as pending, candidate, or needs review.",
        "",
        "- 写字形观察前先打开图像行。",
        "- 引用上下文前先打开卜辞和图版路线。",
        "- 先打开来源登记、manifest、checksum 和权利说明。",
        "- 记录释读史或争议前先打开书目和文献路线。",
        "- 未解决事项都保留为待查、候选或待复核。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def index_data(
    project_id: str,
    object_dir: Path,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
    root: Path,
) -> dict[str, Any]:
    return {
        "record_type": "character_archaeology_paleography_review_index",
        "project_id": project_id,
        "updated_at": UPDATED_AT,
        "object_dir": object_dir.relative_to(root).as_posix(),
        "human_readable_files": [
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
            "08_character-context-evidence-dossier.md",
            REVIEW_FILE,
            READINESS_FILE,
        ],
        "ai_support_files": [
            packet_name,
            "02_visual-source-index.csv",
            "07_research-dossier-index.json",
            "09_character-context-evidence-index.json",
            INDEX_FILE,
            READINESS_INDEX_FILE,
        ],
        "source_route_summary": {
            "source_id": packet.get("source_id", ""),
            "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
            "source_package_id": packet.get("source_package_id", ""),
            "download_or_access_ids": packet_download_ids(packet),
            "source_metadata_files": packet_metadata_files(packet),
            "route_files": packet_routes(packet),
        },
        "visual_route_summary": visual_summary(visual_rows),
        "graph_route_summary": edge_summary(edges),
        "review_slots": [
            "glyph_image",
            "glyph_observation",
            "variant_forms",
            "near_forms",
            "component_clues",
            "inscription_occurrence",
            "inscription_context",
            "plate_catalog_number",
            "heji_or_collection_number",
            "findspot_collection_period_group",
            "source_evidence",
            "decipherment_history",
            "dispute_record",
            "later_script_routes",
            "missing_items",
            "next_sources_to_check",
        ],
        "claim_boundary": "archaeology_paleography_review_no_decipherment_claim",
    }


def readiness_text(
    project_id: str,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
) -> str:
    label = dataset_label(packet)
    visual = visual_summary(visual_rows)
    edge = edge_summary(edges)
    routes = packet_routes(packet)
    metadata = packet_metadata_files(packet)
    downloads = packet_download_ids(packet)
    lines = [
        f"# {project_id} Human Research Readiness Review",
        "",
        f"# {project_id} 人类研究准备度复核",
        "",
        "English:",
        "This file is the final object-local readiness sheet before formal",
        "oracle-character research. It names the evidence a human reviewer",
        "must open before recording observations, readings, components,",
        "inscription context, or later-script relations.",
        "",
        "简体中文：",
        "本文件是正式单字研究前的对象内准备度复核表。",
        "它列出人工复核者在记录字形观察、释读、构件、卜辞语境",
        "或后世字形关系前必须先打开的证据。",
        "",
        "## 1. Formal Research Status / 正式研究状态",
        "",
        bullet("project id", f"`{project_id}`"),
        bullet("primary external id", f"`{packet.get('primary_external_ref_id', '')}`"),
        bullet("source id", f"`{packet.get('source_id', '')}`"),
        bullet("packet", f"`{packet_name}`"),
        bullet("review status", f"`{packet.get('review_status', '')}`"),
        bullet("decipherment status", f"`{packet.get('decipherment_status', '')}`"),
        bullet("dataset label status", f"`{label.get('status', 'pending')}`"),
        "",
        "Current decision:",
        "- accepted reading: `not_reviewed`",
        "- glyph observation: `needs_human_visual_review`",
        "- component assignment: `not_reviewed`",
        "- inscription occurrence: `candidate_route_only`",
        "- later-script correspondence: `candidate_route_only`",
        "- decipherment conclusion: `no_claim`",
        "",
        "当前判断：",
        "- 已接受释读：`not_reviewed`",
        "- 字形观察：`needs_human_visual_review`",
        "- 构件归属：`not_reviewed`",
        "- 卜辞出现：`candidate_route_only`",
        "- 后世字形对应：`candidate_route_only`",
        "- 释读结论：`no_claim`",
        "",
        "## 2. Readiness Routes To Open / 需要打开的准备路线",
        "",
        "- Visual gallery: `04_visual-gallery.md`",
        "- Human dossier: `05_human-research-dossier.md`",
        "- Human review sheet: `06_human-review-sheet.md`",
        "- Context evidence: `08_character-context-evidence-dossier.md`",
        "- Archaeology review: `10_archaeology-paleography-review.md`",
        "- Visual source index: `02_visual-source-index.csv`",
        "- Dossier support index: `07_research-dossier-index.json`",
        "- Context support index: `09_character-context-evidence-index.json`",
        "- Archaeology support index: `11_archaeology-paleography-index.json`",
        "",
        "Structured support files only route the reviewer back to images,",
        "source rows, graph routes, and object-local dossiers.",
        "They do not replace the human record.",
        "",
        "结构化辅助文件只把复核者带回图像、来源行、图边路线和对象内档案。",
        "它们不能替代人类研究记录。",
        "",
        "## 3. Evidence State / 证据状态",
        "",
        bullet("visual index rows", f"`{visual['row_count']}`"),
        bullet("local review images", f"`{visual['committed_image_count']}`"),
        bullet("source image routes", f"`{visual['source_image_route_count']}`"),
        bullet("image rights status", f"`{short(visual['rights_status'], 'pending')}`"),
        bullet("image review status", f"`{short(visual['review_status'], 'pending')}`"),
        bullet("graph edge count", f"`{edge['edge_count']}`"),
        bullet("graph edge types", names(list(edge["edge_type_counts"].keys()))),
        bullet("route files", names(routes)),
        bullet("download or access ids", names(downloads)),
        bullet("source metadata files", names(metadata)),
        bullet("source label text", f"`{label.get('source_modern_label_candidate', '')}`"),
        bullet("source label codepoints", f"`{label.get('source_modern_label_codepoints', '')}`"),
        "",
        "The source label is lookup metadata only.",
        "It is not the oracle-character identity or accepted reading.",
        "",
        "来源标签只是检索 metadata，不是甲骨字身份或已接受释读。",
        "",
        "## 4. Formal-Research Blockers / 正式研究阻断项",
        "",
        "- Glyph image observation has not been written from opened images.",
        "- Variant and near-form comparison remains a route, not a review.",
        "- Component clues are not assigned to a formal component structure.",
        "- Inscription occurrence and context are not tied to an opened text.",
        "- Plate, catalog, Heji, collection, findspot, period, and group",
        "  evidence remain source routes or graph routes.",
        "- Decipherment history, proposer, bibliography, and disputes are",
        "  not yet reviewed as scholarship notes.",
        "- Later-script, bronze, seal, and modern-form routes remain candidates.",
        "- Source manifest, checksum, field map, rights note, and risk note",
        "  must be checked before formal use.",
        "",
        "## 5. Concrete Missing Evidence Questions / 具体缺证问题",
        "",
        "- Which opened image row supports the first glyph observation?",
        "- Which stroke, outline, damage, or uncertain mark remains pending?",
        "- Which variant or near-form image must be compared side by side?",
        "- Which component clue is only a candidate route?",
        "- Which inscription number and full text contain this glyph?",
        "- Which plate, page, catalog number, Heji number, or old number applies?",
        "- Which findspot, collection, period, group, or batch source applies?",
        "- Which bibliography records reading history, proposer, or dispute?",
        "- Which bronze, seal, later-script, or modern-form route is only lookup?",
        "- Which manifest, checksum, field map, rights note, and risk note apply?",
        "",
        "- 哪一行已打开图像支持第一条字形观察？",
        "- 哪些笔画、轮廓、残损或不确定痕迹仍待查？",
        "- 哪个异体或近形图像需要并排比较？",
        "- 哪条构件线索仍只是候选路线？",
        "- 哪个卜辞编号和全文包含这个字形？",
        "- 哪个图版、页码、著录号、合集号或旧号适用？",
        "- 哪个出土地、馆藏、时期、组类或批次来源适用？",
        "- 哪些书目记录释读史、提出者或争议？",
        "- 哪条金文、小篆、后世字形或今字路线只是检索线索？",
        "- 哪些 manifest、checksum、字段映射、权利说明和风险提示适用？",
        "",
        "## 6. Boundary / 边界",
        "",
        "- not a formal oracle-character record promotion",
        "- not an accepted reading",
        "- not a glyph observation already reviewed from images",
        "- not a component assignment",
        "- not an inscription identity claim",
        "- not a later-script correspondence",
        "- not a decipherment conclusion",
        "- 不是正式单字记录提升",
        "- 不是已接受释读",
        "- 不是已从图像复核的字形观察",
        "- 不是构件归属",
        "- 不是卜辞身份结论",
        "- 不是后世字形对应",
        "- 不是释读结论",
    ]
    return "\n".join(lines).rstrip() + "\n"


def readiness_index_data(
    project_id: str,
    object_dir: Path,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
    root: Path,
) -> dict[str, Any]:
    return {
        "record_type": "character_human_research_readiness_index",
        "project_id": project_id,
        "updated_at": UPDATED_AT,
        "object_dir": object_dir.relative_to(root).as_posix(),
        "human_readable_files": [
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
            "08_character-context-evidence-dossier.md",
            REVIEW_FILE,
            READINESS_FILE,
        ],
        "ai_support_files": [
            packet_name,
            "02_visual-source-index.csv",
            "07_research-dossier-index.json",
            "09_character-context-evidence-index.json",
            INDEX_FILE,
        ],
        "readiness_slots": [
            "opened_glyph_image_observation",
            "variant_near_form_comparison",
            "component_candidate_boundary",
            "inscription_occurrence_full_text_context",
            "plate_catalog_heji_collection_route",
            "findspot_period_group_batch_route",
            "decipherment_history_proposer_dispute",
            "later_script_correspondence_boundary",
            "source_manifest_checksum_field_map_risk",
        ],
        "missing_evidence_questions": [
            "which opened image row supports the first glyph observation",
            "which stroke outline damage or uncertain mark remains pending",
            "which variant or near form image must be compared side by side",
            "which component clue is only a candidate route",
            "which inscription number and full text contain this glyph",
            "which plate page catalog heji or old number applies",
            "which findspot collection period group or batch source applies",
            "which bibliography records reading history proposer or dispute",
            "which later script route is only lookup metadata",
            "which manifest checksum field map rights note and risk note apply",
        ],
        "quality_blockers": [
            "glyph_observation_not_reviewed_from_opened_image",
            "variant_near_form_comparison_pending",
            "component_assignment_not_reviewed",
            "inscription_context_not_tied_to_opened_text",
            "provenance_collection_period_group_pending",
            "bibliography_reading_history_disputes_unreviewed",
            "later_script_correspondence_candidate_only",
            "source_manifest_checksum_field_map_risk_unreviewed",
        ],
        "source_route_summary": {
            "source_id": packet.get("source_id", ""),
            "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
            "source_package_id": packet.get("source_package_id", ""),
            "download_or_access_ids": packet_download_ids(packet),
            "source_metadata_files": packet_metadata_files(packet),
            "route_files": packet_routes(packet),
        },
        "visual_route_summary": visual_summary(visual_rows),
        "graph_route_summary": edge_summary(edges),
        "claim_boundary": [
            "no formal oracle-character record promotion",
            "no accepted reading",
            "no reviewed glyph observation claim",
            "no component assignment",
            "no inscription identity claim",
            "no later-script correspondence",
            "no decipherment conclusion",
        ],
    }


def assert_human_line_width(text: str, label: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > 80 and not line.startswith("!["):
            raise ValueError(f"{label}:{line_number} exceeds 80 chars: {line}")


def build_outputs(root: Path) -> dict[str, dict[str, Any]]:
    edges_by_source = graph_edges_by_source(root)
    outputs: dict[str, dict[str, Any]] = {}
    for record in discover_packet_dirs(root):
        project_id = str(record["project_id"])
        object_dir = record["object_dir"]
        packet_name = str(record["packet_name"])
        packet = read_json(record["packet_path"])
        visual_rows = read_csv_rows(object_dir / "02_visual-source-index.csv")
        edges = edges_by_source.get(project_id, [])
        text = review_text(project_id, packet_name, packet, visual_rows, edges)
        readiness = readiness_text(project_id, packet_name, packet, visual_rows, edges)
        assert_human_line_width(text, project_id)
        assert_human_line_width(readiness, f"{project_id} readiness")
        outputs[project_id] = {
            "object_dir": object_dir,
            "review_path": object_dir / REVIEW_FILE,
            "index_path": object_dir / INDEX_FILE,
            "readiness_path": object_dir / READINESS_FILE,
            "readiness_index_path": object_dir / READINESS_INDEX_FILE,
            "review_text": text,
            "readiness_text": readiness,
            "index_data": index_data(
                project_id,
                object_dir,
                packet_name,
                packet,
                visual_rows,
                edges,
                root,
            ),
            "readiness_index_data": readiness_index_data(
                project_id,
                object_dir,
                packet_name,
                packet,
                visual_rows,
                edges,
                root,
            ),
        }
    return outputs


def write_outputs(outputs: dict[str, dict[str, Any]]) -> None:
    for output in outputs.values():
        output["review_path"].write_text(
            output["review_text"], encoding="utf-8", newline="\n"
        )
        output["index_path"].write_text(
            json.dumps(output["index_data"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        output["readiness_path"].write_text(
            output["readiness_text"], encoding="utf-8", newline="\n"
        )
        output["readiness_index_path"].write_text(
            json.dumps(output["readiness_index_data"], ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
            newline="\n",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    outputs = build_outputs(root)
    if not args.check_only:
        write_outputs(outputs)
    print(f"character_archaeology_paleography_review_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
