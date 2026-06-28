#!/usr/bin/env python3
"""Build human-readable Markdown drafts from graph-source cross-review routes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD = Path(
    "corpus/009_statistics-and-derived-features/013_ai-agent-graph-source-cross-review-log-scaffold.csv"
)
GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/014_ai-agent-graph-source-cross-review-log-draft-manifest.csv"
)
GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/015_ai-agent-graph-source-cross-review-log-results.csv"
)
UPDATED_AT = "2026-06-10"
RESEARCH_BOUNDARY = "user_research_draft_not_scholarship"
STATUS = "draft_not_collected"
CAUTION_EN = (
    "This draft is not source evidence, not a rights decision, not a promotion decision, "
    "not a component or evolution-chain assignment, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿不是来源证据、不是权利决定、不是提升决定、不是构件或演化链判定，"
    "也不是释读结论。"
)

SECTION_LABELS = {
    "source_register": ("Source Register", "来源登记"),
    "download_log": ("Download Log", "下载日志"),
    "package_manifest": ("Package Manifest", "包 manifest"),
    "metadata_profile": ("Metadata Profile", "metadata 画像"),
    "graph_edges": ("Graph Edges", "图谱边"),
    "staging_row": ("Staging Row", "staging 行"),
    "counter_source_lookup": ("Counter-Source Lookup", "反查来源"),
    "rights_risk_review": ("Rights And Risk Review", "权利与风险复核"),
    "review_log": ("Review Log", "复核日志"),
}

SECTION_NOTES = {
    "source_register": (
        "Compare source ID, external ref, rights, risk, and review status.",
        "核对来源 ID、外部引用、权利、风险和复核状态。",
    ),
    "download_log": (
        "Open access log before treating the route as usable evidence.",
        "先打开访问日志，再判断路线能否作为证据线索。",
    ),
    "package_manifest": (
        "Check package file list, checksum route, extraction note, and gaps.",
        "核对来源包清单、checksum 路线、抽取说明和缺失项。",
    ),
    "metadata_profile": (
        "Verify metadata fields and keep provider labels as source records.",
        "核对 metadata 字段，并把提供方标签保持为来源记录。",
    ),
    "graph_edges": (
        "Use graph edges only as routes; do not treat them as scholarship.",
        "图边只作复核路线，不得当作学术结论。",
    ),
    "staging_row": (
        "Compare staging rows with object-local dossier before any claim.",
        "提出任何判断前，先与对象目录内档案互核 staging 行。",
    ),
    "counter_source_lookup": (
        "Open each counter-source row before writing cross-source evidence.",
        "写跨来源证据前，逐项打开反查来源行。",
    ),
    "rights_risk_review": (
        "Check rights, risk note, size boundary, and public-use limit.",
        "核对权利、风险说明、大小边界和公开使用限制。",
    ),
    "review_log": (
        "Record only source-marked review notes; leave promotion undecided.",
        "只记录带来源标记的复核说明，提升结论保持未定。",
    ),
}

OUTPUT_FIELDS = [
    "draft_log_id",
    "cross_review_log_id",
    "cross_review_task_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "draft_log_path",
    "scaffold_source_path",
    "route_files_to_open",
    "required_counter_source_ids",
    "required_evidence_sections",
    "cross_review_result_id",
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
    "result_research_boundary",
    "result_output_scope",
    "result_review_note",
    "draft_status",
    "evidence_section_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _results_by_draft_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["draft_log_id"]: row for row in rows}


def _slug_for_row(row: dict[str, str]) -> str:
    source_id = row["source_id"]
    if source_id == "src-hust-obc":
        return "hust-obc"
    if source_id == "src-evobc":
        return "evobc"
    if source_id == "src-obimd":
        return "obimd"
    raise ValueError(f"unsupported source_id: {source_id}")


def _draft_path_for_row(row: dict[str, str], index: int) -> str:
    source_slug = _slug_for_row(row)
    return (
        "doc/public/user_research/002_cross-source-review-queues/"
        f"{source_slug}/{index:03d}_{row['primary_review_record_id']}_cross-source-review-log.md"
    )


def _pair_lines(label: str, value: str) -> list[str]:
    if ";" in value:
        return [f"- {label}:"] + [f"  - `{part}`" for part in _split_compact(value)]
    return [f"- {label}: `{value}`"]


def _metadata_snapshot_lines(row: dict[str, str]) -> list[str]:
    pairs = [
        ("Cross-review result ID", row["cross_review_result_id"]),
        ("Result source", GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS.as_posix()),
        ("Route file count", row["route_file_count"]),
        ("Missing route file count", row["missing_route_file_count"]),
        ("Route file review status", row["route_file_review_status"]),
        ("Required counter source count", row["required_counter_source_count"]),
        ("Registered counter source count", row["registered_counter_source_count"]),
        ("Counter-source lookup status", row["counter_source_lookup_status"]),
        ("Download log count", row["download_log_count"]),
        ("Download log review status", row["download_log_review_status"]),
        ("Package manifest count", row["package_manifest_count"]),
        ("Package manifest review status", row["package_manifest_review_status"]),
        ("Metadata profile metric count", row["metadata_profile_metric_count"]),
        ("Metadata profile review status", row["metadata_profile_review_status"]),
        ("Graph route file count", row["graph_route_file_count"]),
        ("Graph edge route line count", row["graph_edge_route_line_count"]),
        ("Primary graph edge count", row["primary_graph_edge_count"]),
        ("Graph edge review status", row["graph_edge_review_status"]),
        ("Staging row count", row["staging_row_count"]),
        ("Staging record refs", row["staging_record_refs"]),
        ("Staging row review status", row["staging_row_review_status"]),
        ("Draft log status", row["draft_log_status"]),
        ("Rights status", row["rights_status"]),
        ("Rights risk review status", row["rights_risk_review_status"]),
        ("Promotion decision status", row["promotion_decision_status"]),
        ("Evidence pack draft status", row["evidence_pack_draft_status"]),
        ("Result research boundary", row["result_research_boundary"]),
        ("Result output scope", row["result_output_scope"]),
    ]
    lines: list[str] = []
    for label, value in pairs:
        lines.extend(_pair_lines(label, value))
    return lines


def _concrete_next_check_lines(row: dict[str, str]) -> list[str]:
    return [
        "- Which source-register row proves the source identity and rights status?",
        "- Which download-log and package-manifest rows prove the access route?",
        "- Which graph edge files should be opened before any cross-source claim?",
        "- Which staging rows or object-local dossiers should be compared first?",
        "- Which counter-source rows still need human review before evidence capture?",
        f"- Does `{row['primary_review_record_id']}` remain unpromoted and undeciphered?",
    ]


def build_markdown(
    row: dict[str, str],
    draft_log_id: str,
    manifest_row: dict[str, str] | None = None,
) -> str:
    manifest_row = manifest_row or {}
    route_files = _split_compact(row["route_files_to_open"])
    counter_sources = _split_compact(row["required_counter_source_ids"])
    evidence_sections = _split_compact(row["required_evidence_sections"])
    lines = [
        "# Graph Source Cross-Review Log / 图谱来源交叉复核日志",
        "",
        "## Status / 状态",
        "",
        f"- Draft log ID / 草稿日志 ID: `{draft_log_id}`",
        f"- Cross-review log ID / 交叉复核日志 ID: `{row['cross_review_log_id']}`",
        f"- Cross-review task ID / 交叉复核任务 ID: `{row['cross_review_task_id']}`",
        f"- Status / 状态: `{STATUS}`",
        f"- Research boundary / 研究边界: `{RESEARCH_BOUNDARY}`",
        "- Evidence section status / 证据章节状态: `not_collected`",
        "- Promotion decision / 提升决定: `not_decided`",
        f"- Updated at / 更新时间: `{UPDATED_AT}`",
        "",
        "## Source Route / 来源路由",
        "",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Target review scope / 目标复核范围: `{row['target_review_scope']}`",
        f"- Primary review record ID / 主复核记录 ID: `{row['primary_review_record_id']}`",
        f"- Related project ID / 相关项目 ID: `{row['related_project_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Source record ID / 来源记录 ID: `{row['source_record_id']}`",
        f"- Expected output path from scaffold / 骨架预期输出路径: `{row['expected_output_path']}`",
        "",
        "## Route Files To Open / 待打开路由文件",
        "",
    ]
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend(
        [
            "",
            "## Required Counter Sources / 必须反查来源",
            "",
        ]
    )
    lines.extend(f"- `{source_id}`" for source_id in counter_sources)
    lines.extend(
        [
            "",
            "## Evidence Sections / 证据章节",
            "",
            "English: These sections record route availability only; they are not source evidence or scholarship.",
            "",
            "简体中文：以下章节只记录路线可用性；不是来源证据，也不是学术结论。",
            "",
            "## Cross-Review Metadata Snapshot / 交叉复核 metadata 快照",
            "",
            *_metadata_snapshot_lines(manifest_row),
            "",
            "## Concrete Next Checks / 具体下一步待查",
            "",
            *_concrete_next_check_lines(row),
            "",
        ]
    )
    for section in evidence_sections:
        label_en, label_zh = SECTION_LABELS.get(section, (section, section))
        lines.extend(
            [
                f"### {label_en} / {label_zh}",
                "",
                "- Status / 状态: `not_collected_metadata_snapshot`",
                "- Metadata snapshot / metadata 快照: see `Cross-Review Metadata Snapshot` above.",
                "- Notes / 备注:",
                f"  - English: {SECTION_NOTES[section][0]}",
                f"  - 简体中文：{SECTION_NOTES[section][1]}",
                "",
            ]
        )
    lines.extend(
        [
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_013_scaffold`",
            "- Note / 备注: Empty draft created for later source-marked review.",
            "",
            "## Caution / 警示",
            "",
            f"English: {CAUTION_EN}",
            "",
            f"简体中文：{CAUTION_ZH}",
            "",
        ]
    )
    return "\n".join(lines)


def build_draft_manifest_rows(
    scaffold_rows: list[dict[str, str]],
    result_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    results_by_draft_id = _results_by_draft_id(result_rows or [])
    rows: list[dict[str, str]] = []
    for index, row in enumerate(scaffold_rows, start=1):
        draft_log_id = f"graph-source-cross-review-draft-{index:03d}"
        draft_log_path = _draft_path_for_row(row, index)
        result_row = results_by_draft_id.get(draft_log_id, {})
        rows.append(
            {
                "draft_log_id": draft_log_id,
                "cross_review_log_id": row["cross_review_log_id"],
                "cross_review_task_id": row["cross_review_task_id"],
                "source_id": row["source_id"],
                "primary_review_record_id": row["primary_review_record_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_record_id": row["source_record_id"],
                "draft_log_path": draft_log_path,
                "scaffold_source_path": GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "required_counter_source_ids": row["required_counter_source_ids"],
                "required_evidence_sections": row["required_evidence_sections"],
                "cross_review_result_id": result_row.get("cross_review_result_id", ""),
                "route_file_count": result_row.get("route_file_count", ""),
                "missing_route_file_count": result_row.get("missing_route_file_count", ""),
                "route_file_review_status": result_row.get("route_file_review_status", ""),
                "required_counter_source_count": result_row.get("required_counter_source_count", ""),
                "registered_counter_source_count": result_row.get("registered_counter_source_count", ""),
                "counter_source_lookup_status": result_row.get("counter_source_lookup_status", ""),
                "download_log_count": result_row.get("download_log_count", ""),
                "download_log_review_status": result_row.get("download_log_review_status", ""),
                "package_manifest_count": result_row.get("package_manifest_count", ""),
                "package_manifest_review_status": result_row.get("package_manifest_review_status", ""),
                "metadata_profile_metric_count": result_row.get("metadata_profile_metric_count", ""),
                "metadata_profile_review_status": result_row.get("metadata_profile_review_status", ""),
                "graph_route_file_count": result_row.get("graph_route_file_count", ""),
                "graph_edge_route_line_count": result_row.get("graph_edge_route_line_count", ""),
                "primary_graph_edge_count": result_row.get("primary_graph_edge_count", ""),
                "graph_edge_review_status": result_row.get("graph_edge_review_status", ""),
                "staging_row_count": result_row.get("staging_row_count", ""),
                "staging_record_refs": result_row.get("staging_record_refs", ""),
                "staging_row_review_status": result_row.get("staging_row_review_status", ""),
                "draft_log_status": result_row.get("draft_log_status", ""),
                "rights_status": result_row.get("rights_status", ""),
                "rights_risk_review_status": result_row.get("rights_risk_review_status", ""),
                "promotion_decision_status": result_row.get("promotion_decision_status", ""),
                "evidence_pack_draft_status": result_row.get("evidence_pack_draft_status", ""),
                "result_research_boundary": result_row.get("research_boundary", ""),
                "result_output_scope": result_row.get("output_scope", ""),
                "result_review_note": result_row.get("review_note", ""),
                "draft_status": STATUS,
                "evidence_section_status": "not_collected",
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION_EN,
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


def write_markdown_drafts(root: Path, scaffold_rows: list[dict[str, str]], manifest_rows: list[dict[str, str]]) -> None:
    for scaffold_row, manifest_row in zip(scaffold_rows, manifest_rows):
        output_path = root / manifest_row["draft_log_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            build_markdown(scaffold_row, manifest_row["draft_log_id"], manifest_row),
            encoding="utf-8",
            newline="\n",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scaffold", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD))
    parser.add_argument("--results", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS))
    parser.add_argument("--manifest", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    scaffold_rows = read_csv_rows(root / args.scaffold)
    result_rows = read_csv_rows(root / args.results)
    manifest_rows = build_draft_manifest_rows(scaffold_rows, result_rows)
    write_markdown_drafts(root, scaffold_rows, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
