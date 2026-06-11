#!/usr/bin/env python3
"""Build empty review-log drafts for Xiaoxuetang OBM access-boundary follow-up tasks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FOLLOWUP_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "075_ai-agent-xxt-obm-access-boundary-review-log-draft-manifest.csv"
)
UPDATED_AT = "2026-06-11"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_inscription_or_obs_char_schema"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "xxt_obm_access_boundary_review_log_draft_not_scholarship"
CAUTION_EN = (
    "This draft is a routing scaffold only for Xiaoxuetang OBM access-boundary follow-up. It is "
    "not source evidence, not a Heji row import, not an old-catalog confirmation, not a holding "
    "or collection match, not a formal inscription assignment, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿只是小學堂 OBM 访问边界后续复核的路由脚手架；不是来源证据，不是《合集》行导入，"
    "不是旧著录确认，不是馆藏/拓藏匹配，不是正式卜辞分配，也不是释读结论。"
)

OUTPUT_FIELDS = [
    "review_log_draft_id",
    "obm_followup_review_task_id",
    "source_id",
    "targeted_download_id",
    "targeted_url",
    "artifact_kind",
    "draft_path",
    "source_queue_path",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
    "draft_status",
    "evidence_collection_status",
    "human_review_status",
    "formal_schema_compatibility_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "rights_status",
    "risk_note",
    "caution",
    "updated_at",
]

SECTION_LABELS = {
    "source_register_row": ("Source Register Row", "来源登记行"),
    "source_download_manifest_row": ("Source Download Manifest Row", "来源下载 manifest 行"),
    "download_log_row": ("Download Log Row", "下载日志行"),
    "access_profile_rows": ("Access Profile Rows", "访问画像行"),
    "staging_rows_when_available": ("Staging Rows When Available", "已存在的 staging 行"),
    "official_access_boundary": ("Official Access Boundary", "官方访问边界"),
    "review_log": ("Review Log", "复核日志"),
}

NEXT_CHECK_LABELS = {
    "open_registered_source_and_download_rows": (
        "Open the registered source row, download-manifest row, and download-log row.",
        "打开已登记的来源行、下载 manifest 行和下载日志行。",
    ),
    "open_access_profile_rows": (
        "Open the cited OBM access-profile rows.",
        "打开被引用的 OBM 访问画像行。",
    ),
    "open_staging_rows_before_old_catalog_or_holding_claims": (
        "Open staged abbreviation rows before any old-catalog or holding claim.",
        "在提出旧著录或拓藏/馆藏主张前先打开已分期的简称行。",
    ),
    "review_access_boundary_before_manual_followup": (
        "Review the access boundary before any manual follow-up.",
        "在任何人工后续操作前先复核访问边界。",
    ),
    "use_manual_browser_or_institutional_export_before_any_row_level_claim": (
        "Use a manual browser or institutional export path before any row-level claim.",
        "在提出任何行级主张前，先使用人工浏览或机构导出路径。",
    ),
    "record_no_identity_assignment_or_decipherment_claim": (
        "Record that this follow-up makes no identity, assignment, or decipherment claim.",
        "记录本后续复核不提出身份、分配或释读结论。",
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def build_draft_manifest_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(queue_rows, start=1):
        rows.append(
            {
                "review_log_draft_id": f"xxt-obm-access-review-log-draft-{index:04d}",
                "obm_followup_review_task_id": row["obm_followup_review_task_id"],
                "source_id": row["source_id"],
                "targeted_download_id": row["targeted_download_id"],
                "targeted_url": row["targeted_url"],
                "artifact_kind": row["artifact_kind"],
                "draft_path": row["expected_output_path"],
                "source_queue_path": FOLLOWUP_REVIEW_QUEUE.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "required_review_sections": row["required_review_sections"],
                "required_next_checks": row["required_next_checks"],
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": row["human_review_status"],
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "rights_decision_status": row["rights_decision_status"],
                "source_promotion_status": row["source_promotion_status"],
                "identity_claim_status": row["identity_claim_status"],
                "assignment_status": row["assignment_status"],
                "decipherment_claim_status": NO_CLAIM,
                "component_claim_status": NO_CLAIM,
                "evolution_chain_claim_status": NO_CLAIM,
                "research_boundary": RESEARCH_BOUNDARY,
                "rights_status": row["rights_status"],
                "risk_note": row["risk_note"],
                "caution": CAUTION_EN,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_markdown(row: dict[str, str]) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    review_sections = _split_compact(row["required_review_sections"])
    next_checks = _split_compact(row["required_next_checks"])
    lines = [
        "# Xiaoxuetang OBM Access Boundary Review Log Draft / 小學堂 OBM 访问边界复核日志草稿",
        "",
        "## Status / 状态",
        "",
        f"- Review log draft ID / 复核日志草稿 ID: `{row['review_log_draft_id']}`",
        f"- Follow-up review task ID / 后续复核任务 ID: `{row['obm_followup_review_task_id']}`",
        f"- Draft status / 草稿状态: `{row['draft_status']}`",
        f"- Evidence collection status / 证据收集状态: `{row['evidence_collection_status']}`",
        f"- Human review status / 人工复核状态: `{row['human_review_status']}`",
        f"- Formal schema compatibility / 正式 schema 兼容状态: `{row['formal_schema_compatibility_status']}`",
        f"- Research boundary / 研究边界: `{row['research_boundary']}`",
        f"- Updated at / 更新时间: `{row['updated_at']}`",
        "",
        "## Route / 路由",
        "",
        f"- Source ID / 来源 ID: `{row['source_id']}`",
        f"- Targeted download ID / 目标下载 ID: `{row['targeted_download_id']}`",
        f"- Targeted URL / 目标 URL: `{row['targeted_url']}`",
        f"- Artifact kind / 资料类型: `{row['artifact_kind']}`",
        "",
        "## Route Files To Open / 待打开路由文件",
        "",
    ]
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend(
        [
            "",
            "## Review Sections / 复核章节",
            "",
            "English: Keep every section empty until source-marked evidence is collected through a permitted route.",
            "",
            "简体中文：在通过允许路径收集到带来源标记的证据前，所有章节都必须保持为空。",
            "",
        ]
    )
    for section in review_sections:
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
    lines.extend(["## Required Next Checks / 必需下一步检查", ""])
    for check in next_checks:
        label_en, label_zh = NEXT_CHECK_LABELS.get(check, (check, check))
        lines.extend(
            [
                f"- `{check}`",
                f"  - English: {label_en}",
                f"  - 简体中文：{label_zh}",
            ]
        )
    lines.extend(
        [
            "",
            "## Rights And Risk / 权利与风险",
            "",
            f"- Rights status / 权利状态: `{row['rights_status']}`",
            f"- Risk note / 风险说明: {row['risk_note']}",
            "",
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_074_followup_review_queue`",
            "- Evidence collection / 证据收集: `not_collected`",
            "- Decision / 决定: no row-level import, no old-catalog confirmation, no holding match, no inscription assignment, and no decipherment conclusion.",
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_drafts(root: Path, rows: list[dict[str, str]]) -> None:
    for row in rows:
        output_path = root / row["draft_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(build_markdown(row), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=str(FOLLOWUP_REVIEW_QUEUE))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = repo_root()
    manifest_rows = build_draft_manifest_rows(read_csv_rows(root / args.queue))
    write_markdown_drafts(root, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
