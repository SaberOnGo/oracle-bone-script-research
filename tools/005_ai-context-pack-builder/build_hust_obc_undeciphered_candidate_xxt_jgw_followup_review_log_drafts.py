#!/usr/bin/env python3
"""Build metadata-backed follow-up review-log drafts for Xiaoxuetang route probes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FOLLOWUP_REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "072_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-followup-review-queue.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "073_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-followup-review-log-draft-manifest.csv"
)
FOLLOWUP_ROUTE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/"
    "077_ai-agent-xiaoxuetang-followup-review-route-summary.json"
)
UPDATED_AT = "2026-06-11"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
ASSIGNMENT_STATUS = "unknown_candidate_id_not_formal_obs_char_assignment"
NO_CLAIM = "no_claim"
RESEARCH_BOUNDARY = "hust_obc_xxt_jgw_followup_review_log_draft_not_scholarship"
CAUTION_EN = (
    "This draft is a routing scaffold only for an official Xiaoxuetang route follow-up. It is "
    "not source evidence, not catalog confirmation, not a Heji crosswalk, not a collection "
    "match, not a formal obs-char assignment, and not a decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿只是小學堂官方 route 后续复核的路由脚手架；不是来源证据，不是著录确认，"
    "不是《合集》交叉索引，不是馆藏匹配，不是正式 obs-char 分配，也不是释读结论。"
)

OUTPUT_FIELDS = [
    "review_log_draft_id",
    "xxt_followup_review_task_id",
    "route_probe_result_id",
    "note_update_result_id",
    "context_pack_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "targeted_download_id",
    "targeted_url",
    "candidate_filename_number_probe_token",
    "note_draft_path",
    "draft_path",
    "source_queue_path",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
    "followup_family_id",
    "followup_family_label",
    "followup_method",
    "target_source_id",
    "artifact_kind",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "official_access_boundary_status",
    "family_review_task_count",
    "family_route_file_count",
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
    "route_probe_result": ("Route Probe Result", "route probe 结果"),
    "note_update_result": ("Note Update Result", "note update 结果"),
    "full_inscription_context_note": ("Full Inscription Context Note", "完整卜辞上下文草稿"),
    "source_register_row": ("Source Register Row", "来源登记行"),
    "source_download_manifest_row": ("Source Download Manifest Row", "来源下载 manifest 行"),
    "download_log_row": ("Download Log Row", "下载日志行"),
    "official_access_boundary": ("Official Access Boundary", "官方访问边界"),
    "review_log": ("Review Log", "复核日志"),
}

SECTION_NOTES = {
    "route_probe_result": (
        "Open the 071 route-probe row and record the exact access failure.",
        "打开 071 route-probe 行，记录具体访问失败原因。",
    ),
    "note_update_result": (
        "Open the 070 note-update row before editing context notes.",
        "修改上下文备注前，先打开 070 note-update 行。",
    ),
    "full_inscription_context_note": (
        "Check the linked note draft; keep missing context as questions.",
        "核对关联备注草稿；缺失上下文写成具体问题。",
    ),
    "source_register_row": (
        "Verify Xiaoxuetang source identity, scope, rights, and risk note.",
        "核对小学堂来源身份、范围、权利和风险说明。",
    ),
    "source_download_manifest_row": (
        "Verify manifest row, targeted URL, file size, and checksum route.",
        "核对 manifest 行、目标 URL、文件大小和 checksum 路线。",
    ),
    "download_log_row": (
        "Verify download log status before treating the page as reachable.",
        "把页面视为可访问前，先核对下载日志状态。",
    ),
    "official_access_boundary": (
        "Use manual browser or institutional export before catalog claims.",
        "提出著录主张前，先用人工浏览或机构导出路线。",
    ),
    "review_log": (
        "Record no identity, assignment, or decipherment claim in this log.",
        "本日志只记录不作身份、分配或释读结论。",
    ),
}

NEXT_CHECK_LABELS = {
    "open_071_route_probe_result": (
        "Open the cited 071 route-probe result row.",
        "打开被引用的 071 route-probe 结果行。",
    ),
    "open_070_note_update_result": (
        "Open the cited 070 note-update result row.",
        "打开被引用的 070 note-update 结果行。",
    ),
    "open_full_inscription_context_note_draft": (
        "Open the linked full-inscription-context note draft.",
        "打开关联的完整卜辞上下文草稿。",
    ),
    "verify_registered_xxt_source_and_download_rows": (
        "Verify the Xiaoxuetang source, manifest, and download-log rows.",
        "复核已登记的小學堂来源行、下载 manifest 行和下载日志行。",
    ),
    "use_manual_browser_or_institutional_export_before_any_catalog_claim": (
        "Use manual browser or export before any catalog claim.",
        "在提出任何著录或卜辞上下文主张前，先使用人工浏览或机构导出路径。",
    ),
    "record_no_identity_assignment_or_decipherment_claim": (
        "Record no identity, assignment, or decipherment claim.",
        "记录本后续复核不提出身份、分配或释读结论。",
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_compact(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _family_summaries_by_id(summary: dict[str, object]) -> dict[str, dict[str, object]]:
    rows = summary.get("family_summaries", [])
    return {str(row["followup_family_id"]): row for row in rows}  # type: ignore[index]


def build_draft_manifest_rows(
    queue_rows: list[dict[str, str]],
    route_summary: dict[str, object],
) -> list[dict[str, str]]:
    family_summaries = _family_summaries_by_id(route_summary)
    rows: list[dict[str, str]] = []
    for index, row in enumerate(queue_rows, start=1):
        followup_family_id = row["priority_bucket"]
        family = family_summaries[followup_family_id]
        artifact_kinds = family.get("artifact_kinds", [])
        artifact_kind = str(artifact_kinds[0]) if artifact_kinds else ""
        rows.append(
            {
                "review_log_draft_id": f"hust-obc-xxt-followup-review-log-draft-{index:04d}",
                "xxt_followup_review_task_id": row["xxt_followup_review_task_id"],
                "route_probe_result_id": row["route_probe_result_id"],
                "note_update_result_id": row["note_update_result_id"],
                "context_pack_id": row["context_pack_id"],
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "targeted_download_id": row["targeted_download_id"],
                "targeted_url": row["targeted_url"],
                "candidate_filename_number_probe_token": row["candidate_filename_number_probe_token"],
                "note_draft_path": row["note_draft_path"],
                "draft_path": row["expected_output_path"],
                "source_queue_path": FOLLOWUP_REVIEW_QUEUE.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "required_review_sections": row["required_review_sections"],
                "required_next_checks": row["required_next_checks"],
                "followup_family_id": followup_family_id,
                "followup_family_label": str(family["followup_family_label"]),
                "followup_method": row["followup_method"],
                "target_source_id": row["target_source_id"],
                "artifact_kind": artifact_kind,
                "route_file_count": row["route_file_count"],
                "missing_route_file_count": row["missing_route_file_count"],
                "route_file_review_status": row["route_file_review_status"],
                "official_access_boundary_status": row["official_access_boundary_status"],
                "family_review_task_count": str(family["review_task_count"]),
                "family_route_file_count": str(family["route_file_count"]),
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": row["human_review_status"],
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "rights_decision_status": row["rights_decision_status"],
                "source_promotion_status": row["source_promotion_status"],
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": ASSIGNMENT_STATUS,
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
        "# Xiaoxuetang Route Follow-up Review Log Draft / 小學堂 route 后续复核日志草稿",
        "",
        "## Status / 状态",
        "",
        f"- Review log draft ID / 复核日志草稿 ID: `{row['review_log_draft_id']}`",
        f"- Follow-up review task ID / 后续复核任务 ID: `{row['xxt_followup_review_task_id']}`",
        f"- Draft status / 草稿状态: `{row['draft_status']}`",
        f"- Evidence collection status / 证据收集状态: `{row['evidence_collection_status']}`",
        f"- Human review status / 人工复核状态: `{row['human_review_status']}`",
        f"- Formal schema compatibility / 正式 schema 兼容状态: `{row['formal_schema_compatibility_status']}`",
        f"- Identity claim status / 身份声明状态: `{row['identity_claim_status']}`",
        f"- Assignment status / 分配状态: `{row['assignment_status']}`",
        f"- Research boundary / 研究边界: `{row['research_boundary']}`",
        f"- Updated at / 更新时间: `{row['updated_at']}`",
        "",
        "## Route / 路由",
        "",
        f"- Route probe result ID / route probe 结果 ID: `{row['route_probe_result_id']}`",
        f"- Note update result ID / note update 结果 ID: `{row['note_update_result_id']}`",
        f"- Context pack ID / 上下文包 ID: `{row['context_pack_id']}`",
        f"- Unknown candidate ID / 未知候选 ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID / 首选外部引用 ID: `{row['primary_external_ref_id']}`",
        f"- Targeted download ID / 目标下载 ID: `{row['targeted_download_id']}`",
        f"- Targeted URL / 目标 URL: `{row['targeted_url']}`",
        f"- Filename probe token / 文件名检索 token: `{row['candidate_filename_number_probe_token']}`",
        f"- Linked note draft / 关联草稿路径: `{row['note_draft_path']}`",
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
            "简体中文：在通过允许的路径收集到带来源标记的证据前，所有章节都必须保持为空。",
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
                "- Notes / 备注:",
                f"  - English: {SECTION_NOTES[section][0]}",
                f"  - 简体中文：{SECTION_NOTES[section][1]}",
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
            "- Status / 状态: `created_from_072_followup_review_queue`",
            "- Evidence collection / 证据收集: `not_collected`",
            "- Decision / 决定: no catalog confirmation, no Heji crosswalk, no collection match, no obs-char assignment, and no decipherment conclusion.",
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


SNAPSHOT_FIELDS = [
    "followup_family_id",
    "followup_family_label",
    "followup_method",
    "target_source_id",
    "artifact_kind",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "official_access_boundary_status",
    "family_review_task_count",
    "family_route_file_count",
]


def _field_lines(row: dict[str, str], fields: list[str]) -> list[str]:
    return [f"- `{field}`: `{row.get(field, '')}`" for field in fields]


def build_markdown(row: dict[str, str]) -> str:
    route_files = _split_compact(row["route_files_to_open"])
    review_sections = _split_compact(row["required_review_sections"])
    next_checks = _split_compact(row["required_next_checks"])
    lines = [
        "# Xiaoxuetang Route Follow-up Review Log Draft / Xiaoxuetang 后续复核日志草稿",
        "",
        "## Status / Status",
        "",
        f"- Review log draft ID: `{row['review_log_draft_id']}`",
        f"- Follow-up review task ID: `{row['xxt_followup_review_task_id']}`",
        f"- Draft status: `{row['draft_status']}`",
        f"- Evidence collection status: `{row['evidence_collection_status']}`",
        f"- Human review status: `{row['human_review_status']}`",
        f"- Formal schema compatibility: `{row['formal_schema_compatibility_status']}`",
        f"- Identity claim status: `{row['identity_claim_status']}`",
        f"- Assignment status: `{row['assignment_status']}`",
        f"- Research boundary: `{row['research_boundary']}`",
        f"- Updated at: `{row['updated_at']}`",
        "",
        "## Route / Route",
        "",
        f"- Route probe result ID: `{row['route_probe_result_id']}`",
        f"- Note update result ID: `{row['note_update_result_id']}`",
        f"- Context pack ID: `{row['context_pack_id']}`",
        f"- Unknown candidate ID: `{row['unknown_candidate_id']}`",
        f"- Primary external ref ID: `{row['primary_external_ref_id']}`",
        f"- Targeted download ID: `{row['targeted_download_id']}`",
        f"- Targeted URL: `{row['targeted_url']}`",
        f"- Filename probe token: `{row['candidate_filename_number_probe_token']}`",
        f"- Linked note draft: `{row['note_draft_path']}`",
        "",
        "## Xiaoxuetang Follow-up Route Snapshot / Xiaoxuetang Follow-up Route Snapshot",
        "",
        "These values summarize the 072 task row and 077 family route summary for human review.",
        "",
    ]
    lines.extend(_field_lines(row, SNAPSHOT_FIELDS))
    lines.extend(
        [
            "",
            "## Route Files To Open / Route Files To Open",
            "",
        ]
    )
    lines.extend(f"- `{route_file}`" for route_file in route_files)
    lines.extend(
        [
            "",
            "## Review Sections / Review Sections",
            "",
            "English: Each section records what a human reviewer should verify next.",
            "",
            "简体中文：每一节只记录下一步人工应核查的来源路线。",
            "",
        ]
    )
    for section in review_sections:
        label_en, label_zh = SECTION_LABELS.get(section, (section, section))
        note_en, note_zh = SECTION_NOTES[section]
        lines.extend(
            [
                f"### {label_en} / {label_zh}",
                "",
                "- Status: `not_collected_metadata_snapshot`",
                "- Metadata snapshot: route and access-boundary values are listed above.",
                "- Human review task:",
                f"  - English: {note_en}",
                f"  - 简体中文：{note_zh}",
                "",
            ]
        )
    lines.extend(["## Concrete Next Checks / Concrete Next Checks", ""])
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
            "## Rights And Risk / Rights And Risk",
            "",
            f"- Rights status: `{row['rights_status']}`",
            f"- Risk note: {row['risk_note']}",
            "",
            "## Review Log / Review Log",
            "",
            "- Status: `created_from_072_followup_review_queue`",
            "- Evidence collection: `not_collected`",
            "- Decision: no catalog confirmation, no Heji crosswalk, no collection match, no obs-char assignment, and no decipherment conclusion.",
            "",
            "## Caution / Caution",
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
    parser.add_argument("--route-summary", default=str(FOLLOWUP_ROUTE_SUMMARY))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = repo_root()
    manifest_rows = build_draft_manifest_rows(
        read_csv_rows(root / args.queue),
        read_json(root / args.route_summary),
    )
    write_markdown_drafts(root, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
