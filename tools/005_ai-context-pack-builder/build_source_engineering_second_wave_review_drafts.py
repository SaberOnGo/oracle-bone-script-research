#!/usr/bin/env python3
"""Materialize second-wave source-engineering review drafts from 123.

These drafts are human-review work surfaces for source-level continuation
tasks. They summarize existing first-wave source-status metadata without
making a rights decision, promoting a source, importing a corpus row, or making
identity, component, evolution, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
FIRST_WAVE_SOURCE_STATUS = (
    STAT_DIR / "122_ai-agent-source-engineering-first-wave-source-status.csv"
)
SECOND_WAVE_SOURCE_CHECKLIST = (
    STAT_DIR / "123_ai-agent-source-engineering-second-wave-source-checklist.csv"
)
DEFAULT_MANIFEST = (
    STAT_DIR / "124_ai-agent-source-engineering-second-wave-review-draft-manifest.csv"
)

UPDATED_AT = "2026-06-19"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
SOURCE_PROMOTION_STATUS = "not_promoted"
CORPUS_IMPORT_STATUS = "not_imported"
DECIPHERMENT_CLAIM_STATUS = "no_decipherment_claim"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
COMPONENT_CLAIM_STATUS = "no_component_claim"
EVOLUTION_CLAIM_STATUS = "no_evolution_chain_claim"
RESEARCH_BOUNDARY = "source_engineering_second_wave_review_draft_metadata-only_not_scholarship"
CAUTION = (
    "Second-wave source review draft only; this is metadata-only routing, not "
    "collected evidence, not a rights decision, not source promotion, not a "
    "corpus import, not an identity claim, not a component assignment, not an "
    "evolution-chain assignment, and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "review_draft_id",
    "continuation_task_id",
    "source_status_id",
    "source_id",
    "source_action_lane",
    "source_first_wave_status",
    "draft_path",
    "source_checklist_path",
    "source_status_path",
    "required_inputs",
    "result_record_paths",
    "reviewed_evidence_paths",
    "source_level_objective",
    "blocker_summary",
    "draft_status",
    "evidence_collection_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "identity_claim_status",
    "component_claim_status",
    "evolution_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def split_long_value(value: str, limit: int = 68) -> list[str]:
    if ";" in value:
        return [part for part in value.split(";") if part]
    if "/" in value and " " not in value:
        chunks: list[str] = []
        current = ""
        for part in value.split("/"):
            if len(part) > limit:
                if current:
                    chunks.append(current.rstrip("/"))
                    current = ""
                chunks.extend(split_long_value(part, limit))
                continue
            token = f"{part}/"
            candidate = f"{current}{token}"
            if len(candidate) > limit and current:
                chunks.append(current.rstrip("/"))
                current = token
            else:
                current = candidate
        if current:
            chunks.append(current.rstrip("/"))
        return chunks
    words = value.split()
    if len(words) <= 1:
        for separator in ["_", "-"]:
            if separator in value:
                chunks: list[str] = []
                current = ""
                for part in value.split(separator):
                    token = f"{part}{separator}"
                    candidate = f"{current}{token}"
                    if len(candidate) > limit and current:
                        chunks.append(current.rstrip(separator))
                        current = token
                    else:
                        current = candidate
                if current:
                    chunks.append(current.rstrip(separator))
                return chunks
        return [value]
    chunks: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > limit and current:
            chunks.append(current)
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def field_lines(prefix: str, field: str, value: str) -> list[str]:
    display = value if value else "none"
    line = f"{prefix}{field}: `{display}`"
    if len(line) <= 80:
        return [line]
    lines = [f"{prefix}{field}:"]
    lines.extend(f"{prefix}  - `{part}`" for part in split_long_value(display))
    return lines


def paragraph_lines(prefix: str, text: str, limit: int = 76) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if len(f"{prefix}{candidate}") > limit and current:
            line_prefix = prefix if not lines else "  "
            lines.append(f"{line_prefix}{current}")
            current = word
        else:
            current = candidate
    if current:
        line_prefix = prefix if not lines else "  "
        lines.append(f"{line_prefix}{current}")
    return lines


def source_status_by_id(root: Path | None = None) -> dict[str, dict[str, str]]:
    base = repo_root() if root is None else root
    path = base / FIRST_WAVE_SOURCE_STATUS
    if not path.exists():
        return {}
    return {row["source_status_id"]: row for row in read_csv_rows(path)}


def build_manifest_rows(checklist_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(checklist_rows, start=1):
        rows.append(
            {
                "review_draft_id": f"source-engineering-second-wave-review-draft-{index:04d}",
                "continuation_task_id": row["continuation_task_id"],
                "source_status_id": row["source_status_id"],
                "source_id": row["source_id"],
                "source_action_lane": row["source_action_lane"],
                "source_first_wave_status": row["source_first_wave_status"],
                "draft_path": row["expected_review_output_path"],
                "source_checklist_path": SECOND_WAVE_SOURCE_CHECKLIST.as_posix(),
                "source_status_path": row["source_status_path"],
                "required_inputs": row["required_inputs"],
                "result_record_paths": row["result_record_paths"],
                "reviewed_evidence_paths": row["reviewed_evidence_paths"],
                "source_level_objective": row["source_level_objective"],
                "blocker_summary": row["blocker_summary"],
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "corpus_import_status": CORPUS_IMPORT_STATUS,
                "decipherment_claim_status": DECIPHERMENT_CLAIM_STATUS,
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "component_claim_status": COMPONENT_CLAIM_STATUS,
                "evolution_claim_status": EVOLUTION_CLAIM_STATUS,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def bullet_list(values: list[str]) -> list[str]:
    if not values:
        return ["- none"]
    lines: list[str] = []
    for value in values:
        lines.extend(field_lines("- ", "Path / 路径", value))
    return lines


def value_bullet_list(values: list[str], label: str) -> list[str]:
    if not values:
        return ["- none"]
    lines: list[str] = []
    for value in values:
        lines.extend(field_lines("- ", label, value))
    return lines


def next_review_questions(row: dict[str, str]) -> list[str]:
    lane = row["source_action_lane"]
    questions = [
        "Which source-status and result records prove this boundary?",
        "Which rights, checksum, manifest, or field-map item remains pending?",
        "What exact human decision is required before source promotion?",
    ]
    if lane == "access_and_checksum_boundary_resolution":
        questions.append("Which access route explains the HTTP or checksum boundary?")
    elif lane == "metadata_profile_and_package_manifest_decision":
        questions.append("Which metadata profile and package manifest scope is usable?")
    elif lane == "field_map_semantics_review":
        questions.append("Which field-map semantics are safe for metadata-only review?")
    elif lane == "safe_derived_record_decision":
        questions.append("Which derived rows can stay public as reviewed metadata?")
    return questions


def build_markdown(checklist_row: dict[str, str], manifest_row: dict[str, str]) -> str:
    del checklist_row
    status_snapshot = source_status_by_id().get(manifest_row["source_status_id"], {})
    lines = [
        "# Source Engineering Second-Wave Review Draft / 来源工程第二波复核草稿",
        "",
        "## Status / 状态",
        "",
    ]
    for label, field in [
        ("Review draft ID / 复核草稿 ID", "review_draft_id"),
        ("Continuation task ID / 后续任务 ID", "continuation_task_id"),
        ("Source status ID / 来源状态 ID", "source_status_id"),
        ("Draft status / 草稿状态", "draft_status"),
        ("Evidence collection status / 证据收集状态", "evidence_collection_status"),
        ("Human review status / 人工复核状态", "human_review_status"),
        ("Research boundary / 研究边界", "research_boundary"),
        ("Updated at / 更新时间", "updated_at"),
    ]:
        lines.extend(field_lines("- ", label, manifest_row[field]))
    lines.extend(["", "## Source / 来源", ""])
    for label, field in [
        ("Source ID / 来源 ID", "source_id"),
        ("First-wave status / 第一波状态", "source_first_wave_status"),
        ("Source action lane / 来源动作泳道", "source_action_lane"),
    ]:
        lines.extend(field_lines("- ", label, manifest_row[field]))
    lines.extend(["", "## Objective / 目标", ""])
    lines.extend(
        value_bullet_list(split_values(manifest_row["source_level_objective"]), "Objective / 目标")
    )
    lines.extend(["", "## Blockers / 阻断项", ""])
    lines.extend(value_bullet_list(split_values(manifest_row["blocker_summary"]), "Blocker / 阻断项"))
    lines.extend(["", "## Required Inputs / 必须打开的输入", ""])
    lines.extend(bullet_list(split_values(manifest_row["required_inputs"])))
    lines.extend(["", "## Result Records / 结果记录", ""])
    lines.extend(bullet_list(split_values(manifest_row["result_record_paths"])))
    lines.extend(["", "## Reviewed Evidence Paths / 已复核证据路径", ""])
    lines.extend(bullet_list(split_values(manifest_row["reviewed_evidence_paths"])))
    lines.extend(["", "## First-Wave Source Status Snapshot / 第一波来源状态快照", ""])
    for label, field in [
        ("first_wave_result_count", "first_wave_result_count"),
        ("followup_task_count", "followup_task_count"),
        ("decision_values", "decision_values"),
        ("pipeline_current_stages", "pipeline_current_stages"),
        ("download_log_ids", "download_log_ids"),
        ("download_log_status_counts", "download_log_status_counts"),
        ("download_log_http_status_counts", "download_log_http_status_counts"),
        (
            "download_log_checksum_present_count_total",
            "download_log_checksum_present_count_total",
        ),
        ("metadata_profile_ids", "metadata_profile_ids"),
        ("metadata_profile_metric_count_total", "metadata_profile_metric_count_total"),
        ("package_manifest_row_count_total", "package_manifest_row_count_total"),
        ("field_map_scaffold_ids", "field_map_scaffold_ids"),
        ("rights_statuses", "rights_statuses"),
        ("remaining_blockers", "remaining_blockers"),
        ("next_recommended_action", "next_recommended_action"),
    ]:
        lines.extend(field_lines("- ", label, status_snapshot.get(field, "")))
    lines.extend(["", "## Concrete Next Review Questions / 具体下一步复核问题", ""])
    lines.extend(value_bullet_list(next_review_questions(manifest_row), "Question / 问题"))
    lines.extend(["", "## Boundary Status / 边界状态", ""])
    for label, field in [
        ("Rights decision status / 权利决定状态", "rights_decision_status"),
        ("Source promotion status / 来源提升状态", "source_promotion_status"),
        ("Corpus import status / 语料导入状态", "corpus_import_status"),
        ("Decipherment claim status / 释读结论状态", "decipherment_claim_status"),
        ("Identity claim status / 身份判断状态", "identity_claim_status"),
        ("Component claim status / 构件判断状态", "component_claim_status"),
        ("Evolution claim status / 演化链判断状态", "evolution_claim_status"),
    ]:
        lines.extend(field_lines("- ", label, manifest_row[field]))
    lines.extend(
        [
            "",
            "## Review Notes / 复核记录",
            "",
            "English: Existing first-wave metadata is summarized here.",
            "It remains metadata-only until human source review records",
            "a decision in the routed result files.",
            "",
            "简体中文：这里汇总的是第一波 metadata。",
            "在人工来源复核写入路线结果文件前，仍保持 metadata-only。",
            "",
            "- Review outcome / 复核结果: `pending_human_review`",
            "- Rights outcome / 权利结果: `no_new_rights_decision`",
            "- Promotion outcome / 提升结果: `not_promoted`",
            "- Import outcome / 导入结果: `not_imported`",
            "- Boundary phrase / 边界短语: `not a decipherment conclusion`",
            "",
            "## Caution / 警示",
            "",
        ]
    )
    lines.extend(paragraph_lines("English: ", CAUTION))
    lines.extend(
        [
            "",
            "简体中文：本第二波来源复核草稿仅用于 metadata-only 路由；",
            "不是权利决定，不是来源提升，不是语料导入，不是身份判断，",
            "不是构件归属，不是演化链归属，也不是释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown_drafts(
    root: Path, checklist_rows: list[dict[str, str]], manifest_rows: list[dict[str, str]]
) -> None:
    for checklist_row, manifest_row in zip(checklist_rows, manifest_rows, strict=True):
        path = root / manifest_row["draft_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(build_markdown(checklist_row, manifest_row), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build second-wave source-engineering review drafts.")
    parser.add_argument("--checklist", default=str(SECOND_WAVE_SOURCE_CHECKLIST))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    checklist_rows = read_csv_rows(root / args.checklist)
    manifest_rows = build_manifest_rows(checklist_rows)
    write_markdown_drafts(root, checklist_rows, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"review_draft_count={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
