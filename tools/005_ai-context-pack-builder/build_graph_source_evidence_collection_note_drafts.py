#!/usr/bin/env python3
"""Build empty evidence-collection note drafts from source-register tasks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/016_ai-agent-graph-source-evidence-collection-task-queue.csv"
)
GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv"
)

UPDATED_AT = "2026-06-10"
TARGET_EVIDENCE_SECTION = "source_register"
NOTE_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
PROMOTION_STATUS = "not_promoted"
RESEARCH_BOUNDARY = "evidence_collection_note_draft_not_scholarship"
CAUTION_EN = (
    "This draft note is not collected evidence, not a rights decision, not a promotion "
    "decision, not a component or evolution-chain assignment, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿记录不是已收集证据、不是权利决定、不是提升决定、不是构件或演化链判定，"
    "也不是释读结论。"
)

OUTPUT_FIELDS = [
    "evidence_collection_note_draft_id",
    "evidence_collection_task_id",
    "cross_review_result_id",
    "draft_log_id",
    "cross_review_log_id",
    "cross_review_task_id",
    "source_id",
    "primary_review_record_id",
    "primary_external_ref_id",
    "source_record_id",
    "target_evidence_section",
    "note_draft_path",
    "task_queue_source_path",
    "route_files_to_open",
    "counter_source_ids_to_check",
    "note_status",
    "evidence_collection_status",
    "promotion_status",
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


def build_markdown(row: dict[str, str], note_draft_id: str) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    counter_sources = _split_compact(row["counter_source_ids_to_check"])
    lines = [
        "# Evidence Collection Note / 证据收集记录草稿",
        "",
        "## Status / 状态",
        "",
        f"- Evidence collection note draft ID / 证据收集记录草稿 ID: `{note_draft_id}`",
        f"- Evidence collection task ID / 证据收集任务 ID: `{row['evidence_collection_task_id']}`",
        f"- Cross-review result ID / 交叉复核结果 ID: `{row['cross_review_result_id']}`",
        f"- Status / 状态: `{NOTE_STATUS}`",
        f"- Evidence collection status / 证据收集状态: `{EVIDENCE_COLLECTION_STATUS}`",
        f"- Promotion status / 提升状态: `{PROMOTION_STATUS}`",
        f"- Research boundary / 研究边界: `{RESEARCH_BOUNDARY}`",
        f"- Updated at / 更新时间: `{UPDATED_AT}`",
        "",
        "## Source Route / 来源路由",
        "",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Primary review record ID / 主复核记录 ID: `{row['primary_review_record_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Source record ID / 来源记录 ID: `{row['source_record_id']}`",
        f"- Target evidence section / 目标证据章节: `{row['target_evidence_section']}`",
        f"- Collection scope / 收集范围: `{row['collection_scope']}`",
        f"- Expected output path from task queue / 任务队列预期输出路径: `{row['expected_output_path']}`",
        "",
        "## Route Files To Open / 待打开路由文件",
        "",
    ]
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend(
        [
            "",
            "## Counter Sources To Check / 需反查来源",
            "",
        ]
    )
    lines.extend(f"- `{source_id}`" for source_id in counter_sources)
    lines.extend(
        [
            "",
            "## Evidence Collection / 证据收集",
            "",
            "### Source Register / 来源登记",
            "",
            "- Status / 状态: `not_collected`",
            "- Evidence items / 证据条目: none",
            "- Notes / 备注: not collected.",
            "",
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_016_task_queue`",
            "- Note / 备注: Empty draft created for later source-marked evidence collection.",
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


def build_note_manifest_rows(task_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    source_register_rows = [
        row
        for row in task_rows
        if row.get("target_evidence_section") == TARGET_EVIDENCE_SECTION
    ]
    rows: list[dict[str, str]] = []
    for index, row in enumerate(source_register_rows, start=1):
        rows.append(
            {
                "evidence_collection_note_draft_id": f"graph-source-evidence-note-draft-{index:03d}",
                "evidence_collection_task_id": row["evidence_collection_task_id"],
                "cross_review_result_id": row["cross_review_result_id"],
                "draft_log_id": row["draft_log_id"],
                "cross_review_log_id": row["cross_review_log_id"],
                "cross_review_task_id": row["cross_review_task_id"],
                "source_id": row["source_id"],
                "primary_review_record_id": row["primary_review_record_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "source_record_id": row["source_record_id"],
                "target_evidence_section": row["target_evidence_section"],
                "note_draft_path": row["expected_output_path"],
                "task_queue_source_path": GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "counter_source_ids_to_check": row["counter_source_ids_to_check"],
                "note_status": NOTE_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "promotion_status": PROMOTION_STATUS,
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


def write_markdown_drafts(
    root: Path,
    task_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
) -> None:
    task_rows_by_id = {
        row["evidence_collection_task_id"]: row
        for row in task_rows
    }
    for manifest_row in manifest_rows:
        task_row = task_rows_by_id[manifest_row["evidence_collection_task_id"]]
        output_path = root / manifest_row["note_draft_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            build_markdown(task_row, manifest_row["evidence_collection_note_draft_id"]),
            encoding="utf-8",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-queue", default=str(GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE))
    parser.add_argument("--manifest", default=str(GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    task_rows = read_csv_rows(root / args.task_queue)
    manifest_rows = build_note_manifest_rows(task_rows)
    write_markdown_drafts(root, task_rows, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
