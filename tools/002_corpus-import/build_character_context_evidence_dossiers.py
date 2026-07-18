#!/usr/bin/env python3
"""Build readable context evidence dossiers for oracle-character objects.

The generated files are object-local preparation materials. They collect
source routes, visual routes, inscription-context gaps, and concrete next
checks for human review. They do not add readings, component assignments,
inscription identities, or decipherment conclusions.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import textwrap
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


OBJECT_ROOT = Path("corpus/001_oracle-characters")
SOURCE_OBJECT_ROOT = Path(
    "corpus/006_research-sources-and-bibliography/001_source-objects"
)
EVOLUTION_OBJECT_ROOT = Path(
    "corpus/004_bronze-seal-modern-correspondences"
)
GRAPH_FILES = [
    Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/009_character-asset-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/010_cross-source-id-graph-edges.jsonl"),
]
CROSSWALK_FILE = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
UPDATED_AT = "2026-06-23"
WIDTH = 78


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def source_object_routes(root: Path, source_id: str) -> list[str]:
    if not source_id:
        return []
    candidates = sorted(
        (root / SOURCE_OBJECT_ROOT).glob(f"*_{source_id}_source-object")
    )
    if not candidates:
        return []
    object_dir = candidates[0]
    return [
        (object_dir / name).relative_to(root).as_posix()
        for name in (
            "README.md",
            "10_source-evidence-dossier.md",
            "20_source-presearch-readiness-review.md",
        )
        if (object_dir / name).exists()
    ]


def crosswalk_rows_by_character(root: Path) -> dict[str, list[dict[str, str]]]:
    rows_by_character: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv_rows(root / CROSSWALK_FILE):
        project_id = str(row.get("suggested_oracle_character_id", ""))
        if project_id:
            rows_by_character[project_id].append(row)
    return rows_by_character


def evolution_object_routes_by_category(root: Path) -> dict[str, list[str]]:
    """Index object-local EVOBC human files by candidate category ID."""
    routes: dict[str, list[str]] = {}
    pattern = re.compile(r"_evobc-cat-(\d+)_evolution-candidate$")
    for object_dir in sorted(
        (root / EVOLUTION_OBJECT_ROOT).glob(
            "*/*_evobc-cat-*_evolution-candidate"
        )
    ):
        match = pattern.search(object_dir.name)
        if not match:
            continue
        category_id = f"evobc-evo-cat-{match.group(1)}"
        routes[category_id] = [
            (object_dir / name).relative_to(root).as_posix()
            for name in (
                "README.md",
                "07_human-evolution-dossier.md",
                "09_cross-period-review-dossier.md",
                "11_evolution-review-fact-matrix.md",
                "12_modern-label-caution-review.md",
            )
            if (object_dir / name).exists()
        ]
    return routes


def evolution_human_routes(
    category_ids: list[str],
    routes_by_category: dict[str, list[str]],
) -> list[str]:
    routes: list[str] = []
    for category_id in category_ids:
        for route in routes_by_category.get(category_id, []):
            if route not in routes:
                routes.append(route)
    return routes


def cross_source_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    def values(field: str) -> list[str]:
        result: list[str] = []
        for row in rows:
            for value in str(row.get(field, "")).split(";"):
                value = value.strip()
                if value and value not in result:
                    result.append(value)
        return result

    return {
        "row_count": len(rows),
        "cross_source_statuses": values("cross_source_status"),
        "matched_source_ids": values("matched_source_ids"),
        "obimd_candidate_ids": values("obimd_candidate_main_character_ids"),
        "obimd_external_refs": values("obimd_primary_external_ref_ids"),
        "obimd_transcriptions": values("obimd_transcription_values"),
        "evobc_category_ids": values("evobc_candidate_evolution_category_ids"),
        "evobc_external_refs": values("evobc_primary_external_ref_ids"),
        "evobc_image_references": values("evobc_image_reference_count_total"),
        "evobc_oracle_bone_refs": values("evobc_has_oracle_bone_refs_any"),
        "review_statuses": values("review_status"),
        "rights_statuses": values("rights_status"),
        "route_files": values("route_files"),
    }


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
    records: list[dict[str, Any]] = []
    packet_paths = [
        *(root / OBJECT_ROOT).glob("*/*/01_candidate-character-packet.json"),
        *(root / OBJECT_ROOT).glob("*/*/01_undeciphered-candidate-packet.json"),
    ]
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


def wrap(text: str, width: int = WIDTH) -> list[str]:
    if not text:
        return [""]
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def para(text: str) -> str:
    return "\n".join(wrap(text))


def bullet(label: str, value: str) -> str:
    prefix = f"- {label}: "
    text = value if value else concrete_pending("需核对对象 packet、来源路线或图边记录")
    if len(prefix) + len(text) > WIDTH and " " not in text:
        return f"- {label}:\n  {text}"
    lines = textwrap.wrap(
        text,
        width=WIDTH - 2,
        initial_indent=prefix,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(lines)


def code(value: str) -> str:
    return f"`{value}`" if value else concrete_pending("需核对对象 packet、来源路线或图边记录")


def concrete_pending(text: str) -> str:
    return f"待查：{text}"


def short_list(values: list[str], limit: int = 4) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return concrete_pending("需核对对象目录内索引、来源路线或统计图边记录")
    shown = cleaned[:limit]
    suffix = f"; plus {len(cleaned) - limit} more" if len(cleaned) > limit else ""
    return "; ".join(shown) + suffix


def route_bullets(label: str, routes: list[str]) -> list[str]:
    """Render long object-local routes without hiding their exact path."""
    if not routes:
        return [bullet(label, concrete_pending("需核对 EvoBC 对象目录"))]
    lines = [f"- {label}:"]
    for route in routes:
        remaining = route
        while remaining:
            chunk = remaining[: WIDTH - 2]
            lines.append(f"  {chunk}")
            remaining = remaining[len(chunk) :]
    return lines


def dataset_label(packet: dict[str, Any]) -> dict[str, str]:
    label = packet.get("dataset_label")
    if isinstance(label, dict):
        return {str(key): str(value) for key, value in label.items()}
    return {}


def filename_catalog_route_clues(
    visual_rows: list[dict[str, str]],
) -> list[str]:
    """Extract catalog-like strings from source filenames as review routes."""
    clues: list[str] = []
    seen: set[str] = set()
    patterns = (
        (re.compile(r"合\d+"), "Heji-like filename clue"),
        (re.compile(r"(?:YH|H)[-_]?\d+", re.IGNORECASE), "catalog-like filename clue"),
    )
    for row in visual_rows:
        route = str(row.get("source_image_reference_path", ""))
        if not route:
            continue
        name = Path(route).name
        for pattern, label in patterns:
            for match in pattern.findall(name):
                clue = f"{label}: {match} ({name})"
                if clue not in seen:
                    seen.add(clue)
                    clues.append(clue)
    return clues


def packet_download_ids(packet: dict[str, Any]) -> list[str]:
    if isinstance(packet.get("evidence_download_ids"), list):
        return [str(value) for value in packet["evidence_download_ids"]]
    if packet.get("evidence_download_id"):
        return [str(packet["evidence_download_id"])]
    return []


def route_files_from_packet(packet: dict[str, Any]) -> list[str]:
    routes = packet.get("route_files")
    if isinstance(routes, list):
        return [str(value) for value in routes]
    return []


def visual_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    rights = sorted({row.get("rights_status", "") for row in rows if row.get("rights_status")})
    review = sorted({row.get("review_status", "") for row in rows if row.get("review_status")})
    source_refs = [row.get("source_image_reference_path", "") for row in rows]
    committed = [row.get("committed_image_path", "") for row in rows if row.get("committed_image_path")]
    return {
        "row_count": str(len(rows)),
        "source_ref_count": str(sum(1 for value in source_refs if value)),
        "committed_image_count": str(len(committed)),
        "first_source_ref": next((Path(value).name for value in source_refs if value), ""),
        "first_committed_image": next((Path(value).name for value in committed if value), ""),
        "rights_status": ";".join(rights),
        "review_status": ";".join(review),
    }


def edge_summary(edges: list[dict[str, Any]]) -> dict[str, Any]:
    type_counts = Counter(str(edge.get("edge_type", "unknown")) for edge in edges)
    codepoints: list[str] = []
    statuses: list[str] = []
    route_files: list[str] = []
    graph_files: list[str] = []
    for edge in edges:
        codepoint = str(edge.get("hust_label_codepoints", ""))
        if codepoint and codepoint not in codepoints:
            codepoints.append(codepoint)
        status = str(edge.get("cross_source_status", ""))
        if status and status not in statuses:
            statuses.append(status)
        graph_file = str(edge.get("graph_file", ""))
        if graph_file and graph_file not in graph_files:
            graph_files.append(graph_file)
        for route_file in edge.get("route_files", []) or []:
            route_file = str(route_file)
            if route_file and route_file not in route_files:
                route_files.append(route_file)
    return {
        "edge_count": len(edges),
        "edge_type_counts": dict(sorted(type_counts.items())),
        "codepoints": codepoints,
        "cross_source_statuses": statuses,
        "route_files": route_files,
        "graph_files": graph_files,
    }


def graph_evidence_route_lines(
    edges: list[dict[str, Any]],
    limit: int = 4,
) -> list[str]:
    if not edges:
        return [
            "### Graph Evidence Routes",
            "",
            bullet(
                "route status",
                "待查：需生成或核对 character-source、character-asset、"
                "character-inscription 等图边路线",
            ),
        ]

    lines = [
        "### Graph Evidence Routes",
        "",
        para(
            "These graph rows are evidence routes for human review. They do "
            "not confirm a reading, component assignment, inscription "
            "identity, or later-script correspondence."
        ),
    ]
    for index, edge in enumerate(edges[:limit], start=1):
        route_files = [
            Path(str(value)).name for value in edge.get("route_files", []) or []
        ]
        graph_file = Path(str(edge.get("graph_file", ""))).name
        source_ids = [str(value) for value in edge.get("source_ids", []) or []]
        lines.extend(
            [
                "",
                f"#### Graph Evidence Route {index}",
                "",
                bullet("edge type", code(str(edge.get("edge_type", "")))),
                bullet("target node", code(str(edge.get("target_node_id", "")))),
                bullet("graph file", code(graph_file)),
                bullet("review status", code(str(edge.get("review_status", "")))),
                bullet("source ids", short_list(source_ids)),
                bullet("route files", short_list(route_files)),
                bullet("evidence note", str(edge.get("evidence_note", ""))),
            ]
        )
    if len(edges) > limit:
        lines.extend(
            [
                "",
                bullet(
                    "more graph routes",
                    f"{len(edges) - limit} route(s) omitted here; "
                    "open the graph files listed above.",
                ),
            ]
        )
    return lines


def source_object_route_lines(
    source_id: str,
    routes: list[str],
) -> list[str]:
    return [
        "### Source Object Human Routes / 来源对象人类入口",
        "",
        bullet("Source object id / 来源对象 ID", code(source_id)),
        bullet(
            "Human files / 人类文件",
            short_list([Path(value).name for value in routes])
            if routes
            else concrete_pending("需打开 source_id 对应的来源对象 README 和证据 dossier"),
        ),
        para(
            "Open these source-object files before treating packet metadata as "
            "human research evidence."
        ),
        para(
            "在把 packet 元数据当作人类研究证据之前，应先打开这些来源对象文件。"
        ),
        "",
    ]


def context_dossier_text(
    project_id: str,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
    crosswalk_rows: list[dict[str, str]],
    evolution_routes_by_category: dict[str, list[str]],
    root: Path,
) -> str:
    label = dataset_label(packet)
    visual = visual_summary(visual_rows)
    edge = edge_summary(edges)
    cross_source = cross_source_summary(crosswalk_rows)
    evolution_routes = evolution_human_routes(
        cross_source["evobc_category_ids"],
        evolution_routes_by_category,
    )
    catalog_route_clues = filename_catalog_route_clues(visual_rows)
    route_files = route_files_from_packet(packet)
    downloads = packet_download_ids(packet)
    first_visual = visual_rows[0] if visual_rows else {}
    source_package = str(
        packet.get("source_package_id", "")
        or first_visual.get("source_package_id", "")
    )
    source_id = str(
        packet.get("source_id", "") or first_visual.get("source_id", "")
    )
    source_routes = source_object_routes(root, source_id)
    if not downloads:
        downloads = sorted(
            {
                str(row.get("download_id", ""))
                for row in visual_rows
                if row.get("download_id")
            }
        )
    visual_risk = "; ".join(
        sorted({
            str(row.get("risk_note", ""))
            for row in visual_rows
            if row.get("risk_note")
        })
    )
    risk_value = str(packet.get("risk_note", "") or visual_risk)
    source_metadata = [
        str(value)
        for value in packet.get("source_metadata_files", [])
        if isinstance(value, str)
    ]
    lines = [
        f"# {project_id} 单字考古文字上下文档案",
        "",
        para(
            "本文件是单字对象目录内的人类可读上下文档案。它把已经存在的"
            "图片入口、来源路线、图边线索和待查问题集中到同一目录，供甲骨"
            "文学、考古学和人类研究者继续核查。"
        ),
        "",
        "结构化辅助文件只作为检索、追溯、比较和审计工具。",
        "",
        para(
            "This dossier is a human-readable context entrance for the same "
            "object directory. Structured support files remain secondary "
            "tools for search, tracing, comparison, and audit."
        ),
        "",
        para(
            "边界提示：本文件只整理预处理阶段证据路线，不是释读结论，"
            "不是构件归属结论，不是卜辞身份确认，也不是后世字形对应结论。"
        ),
        "",
        "## 1. Object Identity And Review Status / 对象身份与复核状态",
        "",
        bullet("Project ID / 项目 ID", code(project_id)),
        bullet(
            "Primary external ID / 首选外部 ID",
            code(str(packet.get("primary_external_ref_id", ""))),
        ),
        bullet("Source ID / 来源 ID", code(str(packet.get("source_id", "")))),
        bullet("Packet file / packet 文件", code(packet_name)),
        bullet("Record type / 记录类型", code(str(packet.get("record_type", "")))),
        bullet(
            "Decipherment status / 释读状态",
            code(str(packet.get("decipherment_status", ""))),
        ),
        bullet("Review status / 复核状态", code(str(packet.get("review_status", "")))),
        bullet("Rights status / 权利状态", code(str(packet.get("rights_status", "")))),
        "",
        "## 2. Glyph Image And Observation Entrance / 字形图片与观察入口",
        "",
        bullet("Image index / 图像索引", code("02_visual-source-index.csv")),
        bullet("Image page / 图像页", code("04_visual-gallery.md")),
        bullet("Index row count / 索引行数", code(visual["row_count"])),
        bullet("Source image route count / 来源图像路线数", code(visual["source_ref_count"])),
        bullet(
            "Local review image count / 本地复核图像数",
            code(visual["committed_image_count"]),
        ),
        bullet("Source image / 来源图", code(visual["first_source_ref"])),
        bullet("Image / 图像", code(visual["first_committed_image"])),
        bullet("Image rights status / 图像权利状态", code(visual["rights_status"])),
        bullet("Image review status / 图像复核状态", code(visual["review_status"])),
        "",
        para(
            "观察记录应从实物图像、拓片或照片路线开始；每条笔画、残缺、"
            "疑似描摹差异或不确定痕迹都需要绑定到具体图像或来源行。"
        ),
        "",
        "## 3. 异体、近形与构件线索",
        "",
        bullet("异体路线", "待查：需连接已复核的异体、同版异写或来源分组记录"),
        bullet("近形路线", "待查：需核对近形字、误分组和图像相似路线"),
        bullet("构件线索", "待查：只可记录候选构件路线，不能写成构件归属"),
        bullet("当前图边数", code(str(edge["edge_count"]))),
        bullet("图边类型", short_list(list(edge["edge_type_counts"].keys()))),
        "",
        "## 4. Inscription Plate And Catalog Routes / 卜辞、图版与著录路线",
        "",
        bullet(
            "Inscription occurrence / 卜辞出现",
            "待查：需核对卜辞编号、全文或 OCR、上下文和字位",
        ),
        bullet(
            "Plate and page / 图版与页码",
            "待查：需核对图版号、页码、著录来源和影像路线",
        ),
        bullet(
            "Heji or old catalog number / 合集或旧著录号",
            "待查：需核对合集号、旧著录号和目录互证记录",
        ),
        bullet(
            "Filename catalog route clues / 文件名著录线索",
            code("; ".join(catalog_route_clues))
            if catalog_route_clues
            else concrete_pending("需从来源图像文件名和原始著录路线继续核对"),
        ),
        bullet(
            "Catalog clue boundary / 著录线索边界",
            "文件名线索只能定位待查著录，不确认卜辞身份或合集号",
        ),
        bullet(
            "Route files / route 文件",
            short_list([Path(value).name for value in route_files]),
        ),
        bullet(
            "Graph files / 图边文件",
            short_list([Path(value).name for value in edge["route_files"]]),
        ),
        "",
        *graph_evidence_route_lines(edges),
        *source_object_route_lines(source_id, source_routes),
        "### Concrete Cross-Source Candidate Routes / 具体跨来源候选路线",
        "",
        bullet("Crosswalk staging / crosswalk 文件", code(CROSSWALK_FILE.name)),
        bullet("Registered rows / 登记行数", code(str(cross_source["row_count"]))),
        bullet(
            "Matched source ids / 匹配来源 ID",
            code("; ".join(cross_source["matched_source_ids"]) or "none"),
        ),
        bullet(
            "OBIMD candidate ids / OBIMD 候选 ID",
            code("; ".join(cross_source["obimd_candidate_ids"]) or "none"),
        ),
        bullet(
            "OBIMD external refs / OBIMD 外部引用",
            code("; ".join(cross_source["obimd_external_refs"]) or "none"),
        ),
        bullet(
            "OBIMD transcription field / OBIMD 转写字段",
            code("; ".join(cross_source["obimd_transcriptions"]) or "none"),
        ),
        bullet(
            "EvoBC evolution category ids / EvoBC 演化类别 ID",
            code("; ".join(cross_source["evobc_category_ids"]) or "none"),
        ),
        bullet(
            "EvoBC external refs / EvoBC 外部引用",
            code("; ".join(cross_source["evobc_external_refs"]) or "none"),
        ),
        bullet(
            "EvoBC image references / EvoBC 图像引用数",
            code("; ".join(cross_source["evobc_image_references"]) or "0"),
        ),
        bullet(
            "EvoBC oracle-bone refs / EvoBC 甲骨来源标记",
            code("; ".join(cross_source["evobc_oracle_bone_refs"]) or "false"),
        ),
        bullet(
            "Route review status / 路线复核状态",
            code("; ".join(cross_source["review_statuses"]) or "needs_cross_source_review"),
        ),
        "### EvoBC Object-Local Human Routes / EvoBC 对象内人类档案路线",
        "",
        bullet(
            "Matched candidate folders / 匹配候选目录",
            code("; ".join(cross_source["evobc_category_ids"]) or "none"),
        ),
        *route_bullets(
            "Human review files / 人类复核文件",
            evolution_routes,
        ),
        para(
            "These routes point to object-local EVOBC human dossiers. They are "
            "candidate comparison material only; open the cited images, source "
            "codes, bibliography, and dispute records before any correspondence "
            "statement."
        ),
        para(
            "这些路线指向对象目录内的 EVOBC 人类档案。它们只能作为候选比较材料；"
            "在写任何对应说明前，必须打开所列图像、来源代码、书目和争议记录。"
        ),
        para(
            "Boundary: these are exact dataset-codepoint lookup routes only. "
            "They do not confirm identity, reading, meaning, component, "
            "variant, evolution correspondence, or decipherment."
        ),
        para(
            "边界：这些只是数据集码位精确匹配路线，不能确认单字身份、释读、意义、"
            "构件、异体、演化对应关系或破译结论。"
        ),
        "",
        "## 5. 出土地、馆藏、时期与组类",
        "",
        bullet("出土地", "待查：需从来源著录、馆藏对象或考古批次记录追溯"),
        bullet("馆藏", "待查：需核对馆藏号、对象记录和公开数据库路线"),
        bullet("时期与组类", "待查：需记录来源中的分期、组类和批次，不作新判断"),
        bullet(
            "来源包",
            code(source_package)
            if source_package
            else concrete_pending("需核对 01_*packet.json、来源登记和来源包清单"),
        ),
        bullet("下载或访问记录", short_list(downloads)),
        bullet("来源 metadata", short_list(source_metadata)),
        "",
        "## 6. Source Evidence Rights And Risk / 来源证据、权利与风险",
        "",
        bullet("Source trail / 来源追溯", short_list([Path(value).name for value in route_files])),
        bullet(
            "Checksum and manifest / checksum 与 manifest",
            "待查：需打开来源登记、下载日志和来源包清单",
        ),
        bullet(
            "Rights risk / 权利风险",
            code(risk_value)
            if risk_value
            else concrete_pending("需核对 rights_status、risk_note、来源登记和公开提交边界"),
        ),
        bullet("Public commit boundary / 公开提交边界", "元数据和小型派生图像需保留权利状态与风险提示"),
        "",
        "## 7. Decipherment History Dispute And Later Forms / 释读史、争议与后世字形",
        "",
        para(
            "Dataset labels below are not an accepted reading, not the glyph "
            "itself, and not a decipherment conclusion."
        ),
        "",
        bullet("Source label status / 来源标签状态", code(label.get("status", ""))),
        bullet(
            "Source label text / 来源标签文字",
            code(label.get("source_modern_label_candidate", "")),
        ),
        bullet(
            "Source label codepoint / 来源标签 codepoint",
            code(label.get("source_modern_label_codepoints", "")),
        ),
        bullet("Cross-source status / 跨来源状态", short_list(edge["cross_source_statuses"])),
        bullet("Later-form route / 后世字形路线", "待查：金文、小篆、今字路线只能作为候选线索"),
        bullet(
            "Dispute and bibliography route / 争议与文献路线",
            "待查：需记录释读史、提出者、文献来源和不同意见",
        ),
        "",
        "## 8. 具体待查问题",
        "",
        "- 需要核对哪些卜辞、图版、著录号或合集号？",
        "- 哪些全文、OCR 或图版影像能补足该字所在上下文？",
        "- 哪些字形观察能绑定到具体图像、拓片、照片或来源行？",
        "- 哪些异体、近形或构件候选仍只是复核路线？",
        "- 哪些馆藏、出土地、时期、组类或批次记录与本对象有关？",
        "- 哪些文献讨论了释读史、提出者、不同意见或争议？",
        "- 哪些金文、小篆、今字或字形演化路线仍只是候选？",
        "- 需要打开哪些来源、checksum、manifest 或权利记录？",
        "",
        "## 9. 本目录应先打开的文件",
        "",
        "- `README.md`",
        "- `04_visual-gallery.md`",
        "- `05_human-research-dossier.md`",
        "- `06_human-review-sheet.md`",
        "- `08_character-context-evidence-dossier.md`",
        "- `01_*packet.json`",
        "- `02_visual-source-index.csv`",
        "- `07_research-dossier-index.json`",
        "- `09_character-context-evidence-index.json`",
        "",
        "## 10. 复核边界",
        "",
        para(
            "本档案记录可打开、可追溯、可继续核查的资料路线。任何读音、"
            "今字、构件、卜辞身份或演化对应，都必须在正式研究阶段另行"
            "人工复核后才能写成学术说明。"
        ),
    ]
    return "\n".join(lines).rstrip() + "\n"


def context_index(
    project_id: str,
    object_dir: Path,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
    cross_source: dict[str, Any],
    evolution_routes_by_category: dict[str, list[str]],
    root: Path,
) -> dict[str, Any]:
    visual = visual_summary(visual_rows)
    edge = edge_summary(edges)
    source_routes = source_object_routes(
        root,
        str(packet.get("source_id", "")),
    )
    return {
        "record_type": "character_context_evidence_dossier_index",
        "project_id": project_id,
        "updated_at": UPDATED_AT,
        "object_dir": object_dir.relative_to(root).as_posix(),
        "human_readable_files": [
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
            "08_character-context-evidence-dossier.md",
        ],
        "ai_support_files": [
            "01_*packet.json",
            "02_visual-source-index.csv",
            "07_research-dossier-index.json",
            "09_character-context-evidence-index.json",
        ],
        "packet_file": packet_name,
        "source_route_summary": {
            "source_id": packet.get("source_id", ""),
            "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
            "source_package_id": packet.get("source_package_id", ""),
            "download_or_access_ids": packet_download_ids(packet),
            "source_metadata_files": packet.get("source_metadata_files", []),
            "route_files": route_files_from_packet(packet),
            "source_object_routes": source_routes,
        },
        "visual_route_summary": visual,
        "graph_route_summary": edge,
        "cross_source_route_summary": cross_source,
        "evolution_object_human_routes": evolution_human_routes(
            cross_source["evobc_category_ids"],
            evolution_routes_by_category,
        ),
        "human_context_sections": [
            "glyph_image_and_observation_routes",
            "variant_near_shape_and_component_clues",
            "inscription_plate_catalog_and_heji_routes",
            "findspot_collection_period_and_group_routes",
            "source_rights_risk_and_manifest_routes",
            "decipherment_history_dispute_and_later_script_routes",
        ],
        "missing_or_review_fields": [
            "glyph_observation_notes_to_review",
            "variant_and_near_shape_routes_to_check",
            "component_candidate_routes_to_check",
            "inscription_text_context_to_check",
            "plate_catalog_heji_and_old_number_to_check",
            "findspot_collection_period_group_to_check",
            "bibliography_decipherment_history_and_disputes_to_check",
            "later_script_evolution_correspondence_to_check",
            "source_manifest_checksum_and_rights_to_check",
        ],
        "claim_boundary": "context_routes_only_not_decipherment_conclusion",
    }


def assert_human_line_width(text: str, label: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > 80 and not line.startswith("!["):
            raise ValueError(f"{label}:{line_number} exceeds 80 chars: {line}")


def build_outputs(root: Path) -> dict[str, dict[str, Any]]:
    edges_by_source = graph_edges_by_source(root)
    crosswalk_by_character = crosswalk_rows_by_character(root)
    evolution_routes_by_category = evolution_object_routes_by_category(root)
    outputs: dict[str, dict[str, Any]] = {}
    for record in discover_packet_dirs(root):
        project_id = str(record["project_id"])
        object_dir = record["object_dir"]
        packet_name = str(record["packet_name"])
        packet = read_json(record["packet_path"])
        visual_rows = read_csv_rows(object_dir / "02_visual-source-index.csv")
        edges = edges_by_source.get(project_id, [])
        crosswalk_rows = crosswalk_by_character.get(project_id, [])
        dossier = context_dossier_text(
            project_id,
            packet_name,
            packet,
            visual_rows,
            edges,
            crosswalk_rows,
            evolution_routes_by_category,
            root,
        )
        assert_human_line_width(dossier, project_id)
        outputs[project_id] = {
            "object_dir": object_dir,
            "dossier_path": object_dir / "08_character-context-evidence-dossier.md",
            "index_path": object_dir / "09_character-context-evidence-index.json",
            "dossier_text": dossier,
            "index_data": context_index(
                project_id,
                object_dir,
                packet_name,
                packet,
                visual_rows,
                edges,
                cross_source_summary(crosswalk_rows),
                evolution_routes_by_category,
                root,
            ),
        }
    return outputs


def write_outputs(outputs: dict[str, dict[str, Any]]) -> None:
    for output in outputs.values():
        output["dossier_path"].write_text(
            output["dossier_text"], encoding="utf-8", newline="\n"
        )
        output["index_path"].write_text(
            json.dumps(output["index_data"], ensure_ascii=False, indent=2) + "\n",
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
    print(f"character_context_evidence_dossier_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
