#!/usr/bin/env python3
"""Build empty Markdown drafts from graph-source cross-review log scaffolds."""

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


def build_markdown(row: dict[str, str], draft_log_id: str) -> str:
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
            "English: All sections are intentionally empty until source-marked evidence is collected.",
            "",
            "简体中文：所有章节在收集带来源标记的证据前都必须保持为空。",
            "",
        ]
    )
    for section in evidence_sections:
        label_en, label_zh = SECTION_LABELS.get(section, (section, section))
        lines.extend(
            [
                f"### {label_en} / {label_zh}",
                "",
                "- Status / 状态: `not_collected`",
                "- Evidence items / 证据条目: none",
                "- Notes / 备注: not collected.",
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


def build_draft_manifest_rows(scaffold_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(scaffold_rows, start=1):
        draft_log_id = f"graph-source-cross-review-draft-{index:03d}"
        draft_log_path = _draft_path_for_row(row, index)
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
            build_markdown(scaffold_row, manifest_row["draft_log_id"]),
            encoding="utf-8",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scaffold", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD))
    parser.add_argument("--manifest", default=str(GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    scaffold_rows = read_csv_rows(root / args.scaffold)
    manifest_rows = build_draft_manifest_rows(scaffold_rows)
    write_markdown_drafts(root, scaffold_rows, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
