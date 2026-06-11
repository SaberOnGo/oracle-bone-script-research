#!/usr/bin/env python3
"""Build empty collection-note drafts for HUST-OBC undeciphered candidate tasks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


TASK_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "062_ai-agent-hust-obc-undeciphered-candidate-evidence-collection-task-queue.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "063_ai-agent-hust-obc-undeciphered-candidate-evidence-collection-note-draft-manifest.csv"
)
UPDATED_AT = "2026-06-11"
NOTE_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_candidate_evidence_collection_note_draft_not_scholarship"
CAUTION_EN = (
    "This draft note is a route scaffold only. It is not collected evidence, not an "
    "accepted glyph identity, not a formal obs-char assignment, not a reading, not a "
    "component or evolution-chain assignment, not a rights decision, not a source "
    "promotion, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿记录只是路由脚手架；不是已收集证据，不是已接受字形身份，不是正式 "
    "obs-char 分配，不是释读，不是构件或演化链判定，不是权利决定，不是来源提升，"
    "也不是破译或释读结论。"
)

SECTION_LABELS = {
    "character_or_unknown_glyph_id": ("Character Or Unknown Glyph ID", "甲骨字或未知字 ID"),
    "source_references_and_asset_metadata": ("Source References And Asset Metadata", "来源引用与资产 metadata"),
    "full_inscription_context": ("Full Inscription Context", "卜辞全文上下文"),
    "neighboring_characters": ("Neighboring Characters", "周边字"),
    "component_breakdown_and_variant_notes": ("Component Breakdown And Variant Notes", "构件拆分与变体笔记"),
    "excavation_period_and_catalog_provenance": (
        "Excavation, Period, And Catalog Provenance",
        "出土、时代与著录来源",
    ),
    "bronze_seal_or_modern_comparanda": (
        "Bronze, Seal, Or Modern Comparanda",
        "金文、小篆或今文比较材料",
    ),
    "supporting_evidence": ("Supporting Evidence", "支持证据"),
    "opposing_evidence": ("Opposing Evidence", "反对证据"),
    "open_questions_and_next_checks": ("Open Questions And Next Checks", "未决问题和下一步检查"),
    "review_log": ("Review Log", "复核日志"),
}

OUTPUT_FIELDS = [
    "evidence_collection_note_draft_id",
    "evidence_collection_task_id",
    "evidence_pack_scaffold_id",
    "readiness_check_id",
    "route_result_id",
    "review_log_draft_id",
    "undeciphered_review_task_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "target_evidence_section",
    "note_draft_path",
    "task_queue_source_path",
    "route_hints",
    "route_files_to_open",
    "candidate_packet_capture_result_id",
    "source_register_capture_result_id",
    "download_log_capture_result_id",
    "large_source_register_capture_result_id",
    "note_status",
    "evidence_collection_status",
    "human_review_status",
    "formal_schema_compatibility_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "rights_decision_status",
    "source_promotion_status",
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


def _require_task(row: dict[str, str]) -> None:
    required = {
        "task_status": "not_started",
        "evidence_collection_status": "not_collected",
        "formal_schema_compatibility_status": "not_formal_obs_char_schema",
        "identity_claim_status": "no_identity_claim",
        "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
        "decipherment_claim_status": "no_claim",
        "component_claim_status": "no_claim",
        "evolution_chain_claim_status": "no_claim",
    }
    for field, expected in required.items():
        if row[field] != expected:
            raise ValueError(f"unexpected {field} for {row['evidence_collection_task_id']}: {row[field]}")


def build_markdown(row: dict[str, str], note_draft_id: str) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    route_hints = _split_compact(row["route_hints"])
    section_label_en, section_label_zh = SECTION_LABELS[row["target_evidence_section"]]
    lines = [
        "# HUST-OBC Undeciphered Candidate Evidence Collection Note Draft / HUST-OBC 未释读候选证据收集记录草稿",
        "",
        "## Status / 状态",
        "",
        f"- Evidence collection note draft ID / 证据收集记录草稿 ID: `{note_draft_id}`",
        f"- Evidence collection task ID / 证据收集任务 ID: `{row['evidence_collection_task_id']}`",
        f"- Evidence pack scaffold ID / evidence-pack 脚手架 ID: `{row['evidence_pack_scaffold_id']}`",
        f"- Note status / 记录状态: `{NOTE_STATUS}`",
        f"- Evidence collection status / 证据收集状态: `{EVIDENCE_COLLECTION_STATUS}`",
        f"- Human review status / 人工复核状态: `{HUMAN_REVIEW_STATUS}`",
        f"- Formal schema compatibility / 正式 schema 兼容状态: `{FORMAL_SCHEMA_COMPATIBILITY_STATUS}`",
        f"- Identity claim status / 身份声明状态: `{IDENTITY_CLAIM_STATUS}`",
        f"- Assignment status / 分配状态: `{ASSIGNMENT_STATUS}`",
        f"- Decipherment claim status / 释读声明状态: `{NO_CLAIM}`",
        f"- Component claim status / 构件声明状态: `{NO_CLAIM}`",
        f"- Evolution-chain claim status / 演化链声明状态: `{NO_CLAIM}`",
        f"- Research boundary / 研究边界: `{RESEARCH_BOUNDARY}`",
        f"- Updated at / 更新时间: `{UPDATED_AT}`",
        "",
        "## Candidate Route / 候选路由",
        "",
        f"- Unknown candidate ID / 未知候选 ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Readiness check ID / readiness check ID: `{row['readiness_check_id']}`",
        f"- Route result ID / 路由结果 ID: `{row['route_result_id']}`",
        f"- Review log draft ID / 复核日志草稿 ID: `{row['review_log_draft_id']}`",
        f"- Context pack ID / 上下文包 ID: `{row['context_pack_id']}`",
        f"- Target evidence section / 目标证据章节: `{row['target_evidence_section']}`",
        f"- Collection scope / 收集范围: `{row['collection_scope']}`",
        "",
        "## Route Hints / 路由提示",
        "",
    ]
    lines.extend(f"- `{hint}`" for hint in route_hints)
    lines.extend(["", "## Route Files To Open / 待打开路由文件", ""])
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend(
        [
            "",
            "## Capture Row Links / 捕获行链接",
            "",
            f"- Candidate packet capture result ID / 候选 packet 捕获结果 ID: `{row['candidate_packet_capture_result_id']}`",
            f"- Source register capture result ID / 来源登记捕获结果 ID: `{row['source_register_capture_result_id']}`",
            f"- Download log capture result ID / 下载日志捕获结果 ID: `{row['download_log_capture_result_id']}`",
            f"- Large source register capture result ID / 大型来源登记捕获结果 ID: `{row['large_source_register_capture_result_id']}`",
            "",
            "## Evidence Collection / 证据收集",
            "",
            f"### {section_label_en} / {section_label_zh}",
            "",
            "- Status / 状态: `not_collected`",
            "- Evidence items / 证据条目: none",
            "- Source-marked notes / 带来源标记备注: not collected.",
            "",
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_062_task_queue`",
            "- Decision / 决定: no evidence collected and no identity, reading, formal assignment, component, evolution-chain, rights, source-promotion, or decipherment decision.",
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
    rows: list[dict[str, str]] = []
    for index, row in enumerate(task_rows, start=1):
        _require_task(row)
        rows.append(
            {
                "evidence_collection_note_draft_id": (
                    f"hust-obc-undeciphered-evidence-note-draft-{index:04d}"
                ),
                "evidence_collection_task_id": row["evidence_collection_task_id"],
                "evidence_pack_scaffold_id": row["evidence_pack_scaffold_id"],
                "readiness_check_id": row["readiness_check_id"],
                "route_result_id": row["route_result_id"],
                "review_log_draft_id": row["review_log_draft_id"],
                "undeciphered_review_task_id": row["undeciphered_review_task_id"],
                "context_pack_id": row["context_pack_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "target_evidence_section": row["target_evidence_section"],
                "note_draft_path": row["expected_output_path"],
                "task_queue_source_path": TASK_QUEUE.as_posix(),
                "route_hints": row["route_hints"],
                "route_files_to_open": row["route_files_to_open"],
                "candidate_packet_capture_result_id": row["candidate_packet_capture_result_id"],
                "source_register_capture_result_id": row["source_register_capture_result_id"],
                "download_log_capture_result_id": row["download_log_capture_result_id"],
                "large_source_register_capture_result_id": row["large_source_register_capture_result_id"],
                "note_status": NOTE_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
                "decipherment_claim_status": NO_CLAIM,
                "component_claim_status": NO_CLAIM,
                "evolution_chain_claim_status": NO_CLAIM,
                "rights_decision_status": row["rights_decision_status"],
                "source_promotion_status": row["source_promotion_status"],
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION_EN,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_drafts(root: Path, task_rows: list[dict[str, str]], manifest_rows: list[dict[str, str]]) -> None:
    task_rows_by_id = {row["evidence_collection_task_id"]: row for row in task_rows}
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
    parser.add_argument("--task-queue", default=str(TASK_QUEUE))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
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
