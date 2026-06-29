#!/usr/bin/env python3
"""Build review-log drafts for source-engineering gap tasks.

These drafts turn the 099 source-engineering gap queue into human/agent review
work surfaces. They materialize existing route metadata from the 103 snapshot
without promoting source, rights, corpus, identity, or decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_ENGINEERING_GAP_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/099_ai-agent-source-engineering-gap-queue.csv"
)
DEFAULT_MANIFEST = Path(
    "corpus/009_statistics-and-derived-features/"
    "102_ai-agent-source-engineering-gap-review-log-draft-manifest.csv"
)
REVIEW_QUEUE_DIR = Path("doc/public/user_research/009_source-engineering-gap-review-queues")
EVIDENCE_SNAPSHOT = Path(
    "corpus/009_statistics-and-derived-features/"
    "103_ai-agent-source-engineering-gap-evidence-snapshot.csv"
)
UPDATED_AT = "2026-06-19"
DRAFT_STATUS = "draft_not_collected"
EVIDENCE_COLLECTION_STATUS = "not_collected"
HUMAN_REVIEW_STATUS = "pending_human_review"
SOURCE_PROMOTION_STATUS = "not_promoted"
RIGHTS_DECISION_STATUS = "no_new_rights_decision"
RESEARCH_BOUNDARY = "source_engineering_gap_review_log_draft_not_scholarship"
COMMIT_POLICY_BOUNDARY = "metadata_review_only_raw_or_temporary_material_stays_outside_regular_git"
CAUTION_EN = (
    "This draft is a source-engineering routing scaffold only. It is not source "
    "evidence, not rights clearance, not a source promotion decision, not a "
    "corpus import, not an oracle-character identity claim, and not a "
    "decipherment conclusion."
)
CAUTION_ZH = (
    "本草稿仅为来源工程复核路线脚手架；不是来源证据，不是权利清除，不是来源提升决定，"
    "不是语料导入，不是甲骨单字身份判断，也不是释读结论。"
)

OUTPUT_FIELDS = [
    "review_log_draft_id",
    "source_engineering_gap_id",
    "source_id",
    "gap_type",
    "priority_rank",
    "current_stage",
    "authority_tier",
    "rights_status",
    "draft_path",
    "source_queue_path",
    "route_files_to_open",
    "observed_gap_evidence",
    "required_next_checks",
    "draft_status",
    "evidence_collection_status",
    "human_review_status",
    "rights_decision_status",
    "source_promotion_status",
    "commit_policy_boundary",
    "research_boundary",
    "caution",
    "updated_at",
]

CHECK_LABELS = {
    "open_download_log_and_status_codebook": (
        "Open the download log and status codebook before retry or access decisions.",
        "在重试或访问判定前打开下载日志和状态码表。",
    ),
    "record_retry_manual_access_or_metadata_only_boundary": (
        "Record whether the next route is retry, manual access, or metadata-only boundary.",
        "记录下一步是重试、人工访问，还是 metadata-only 边界。",
    ),
    "do_not_promote_failed_or_restricted_download_as_source_content": (
        "Do not promote failed or restricted access as source content.",
        "不要把失败或受限访问记录提升为来源内容。",
    ),
    "open_download_log": (
        "Open the download log and distinguish successful rows from boundary rows.",
        "打开下载日志，并区分成功下载行与访问边界行。",
    ),
    "separate_failed_or_restricted_rows_from checksum-bearing downloads": (
        "Separate failed or restricted rows from checksum-bearing downloads.",
        "将失败或受限访问行与带 checksum 的下载行分开。",
    ),
    "record_no_source_package_or_metadata_promotion_without verified checksum": (
        "Record that no package or metadata promotion is allowed without verified checksum evidence.",
        "记录没有经验证 checksum 时不得提升来源包或 metadata。",
    ),
    "open_download_log_and_source_register": (
        "Open download log and source register before metadata profile extraction.",
        "在抽取 metadata profile 前打开下载日志和来源登记表。",
    ),
    "extract_metadata_only_counts_or_scope_from_committed_evidence": (
        "Extract only metadata counts or scope from already committed evidence.",
        "只从已提交证据中抽取 metadata 计数或范围。",
    ),
    "record_review_status_and_no_scholarly_claim": (
        "Record review status and no scholarly claim.",
        "记录复核状态，并明确不形成学术结论。",
    ),
    "open_source_register_and_available_metadata_profile": (
        "Open source register and any available metadata profile before field mapping.",
        "在字段映射前打开来源登记表和已有 metadata profile。",
    ),
    "define_source_fields_or_units_to_project_record_targets": (
        "Define source fields or units against project record targets.",
        "把来源字段或单位映射到项目记录目标。",
    ),
    "record_rights_boundary_for_each mapped field": (
        "Record the rights boundary for each mapped field.",
        "为每个映射字段记录权利边界。",
    ),
    "open_download_manifest_download_log_and_package_manifest": (
        "Open download manifest, download log, and package manifest.",
        "打开下载 manifest、下载日志和 package manifest。",
    ),
    "record_package_file_manifest_rows_or_explicit_not_applicable_decision": (
        "Record package-file manifest rows or an explicit not-applicable decision.",
        "记录 package-file manifest 行，或明确记录不适用判定。",
    ),
    "keep_raw_or_temporary_files_outside_regular_git": (
        "Keep raw or temporary files outside regular Git.",
        "把原始或临时文件留在普通 Git 之外。",
    ),
    "open_metadata_profile_source_route_and_rights_status": (
        "Open metadata profile, source route, and rights status before derivative decisions.",
        "在派生记录决策前打开 metadata profile、来源路线和权利状态。",
    ),
    "decide_next_safe_derivative_staging_or_review_queue": (
        "Decide the next safe derivative staging row or review queue.",
        "决定下一步安全的派生 staging 行或复核队列。",
    ),
    "record_no_corpus_promotion_without_source_marked_review": (
        "Record no corpus promotion without source-marked review.",
        "记录没有带来源标记的复核不得提升为语料。",
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def split_long_value(value: str, limit: int = 68) -> list[str]:
    if ";" in value:
        return [part for part in value.split(";") if part]
    if "/" in value and " " not in value:
        chunks: list[str] = []
        current = ""
        for part in value.split("/"):
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


def paragraph_lines(
    prefix: str, text: str, limit: int = 76, continuation_prefix: str | None = None
) -> list[str]:
    continuation = prefix if continuation_prefix is None else continuation_prefix
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if len(f"{prefix}{candidate}") > limit and current:
            line_prefix = prefix if not lines else continuation
            lines.append(f"{line_prefix}{current}")
            current = word
        else:
            current = candidate
    if current:
        line_prefix = prefix if not lines else continuation
        lines.append(f"{line_prefix}{current}")
    return lines


def snapshot_by_gap_id(root: Path | None = None) -> dict[str, dict[str, str]]:
    base = repo_root() if root is None else root
    path = base / EVIDENCE_SNAPSHOT
    if not path.exists():
        return {}
    return {row["source_engineering_gap_id"]: row for row in read_csv_rows(path)}


def build_draft_manifest_rows(queue_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(queue_rows, start=1):
        rows.append(
            {
                "review_log_draft_id": f"source-engineering-gap-review-log-draft-{index:04d}",
                "source_engineering_gap_id": row["source_engineering_gap_id"],
                "source_id": row["source_id"],
                "gap_type": row["gap_type"],
                "priority_rank": row["priority_rank"],
                "current_stage": row["current_stage"],
                "authority_tier": row["authority_tier"],
                "rights_status": row["rights_status"],
                "draft_path": row["expected_output_path"],
                "source_queue_path": SOURCE_ENGINEERING_GAP_QUEUE.as_posix(),
                "route_files_to_open": row["route_files_to_open"],
                "observed_gap_evidence": row["observed_gap_evidence"],
                "required_next_checks": row["required_next_checks"],
                "draft_status": DRAFT_STATUS,
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "rights_decision_status": RIGHTS_DECISION_STATUS,
                "source_promotion_status": SOURCE_PROMOTION_STATUS,
                "commit_policy_boundary": COMMIT_POLICY_BOUNDARY,
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION_EN,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_markdown(row: dict[str, str]) -> str:
    route_files = split_values(row["route_files_to_open"])
    next_checks = split_values(row["required_next_checks"])
    snapshot = snapshot_by_gap_id().get(row["source_engineering_gap_id"], {})
    lines = [
        "# Source Engineering Gap Review Log Draft / 来源工程缺口复核日志草稿",
        "",
        "## Status / 状态",
        "",
    ]
    for label, field in [
        ("Review log draft ID / 复核日志草稿 ID", "review_log_draft_id"),
        ("Source engineering gap ID / 来源工程缺口 ID", "source_engineering_gap_id"),
        ("Draft status / 草稿状态", "draft_status"),
        ("Evidence collection status / 证据收集状态", "evidence_collection_status"),
        ("Human review status / 人工复核状态", "human_review_status"),
        ("Rights decision status / 权利决策状态", "rights_decision_status"),
        ("Source promotion status / 来源提升状态", "source_promotion_status"),
        ("Commit policy boundary / 提交边界", "commit_policy_boundary"),
        ("Research boundary / 研究边界", "research_boundary"),
        ("Updated at / 更新时间", "updated_at"),
    ]:
        lines.extend(field_lines("- ", label, row[field]))
    lines.extend(["", "## Source Route / 来源路线", ""])
    for label, field in [
        ("Source ID / 来源 ID", "source_id"),
        ("Gap type / 缺口类型", "gap_type"),
        ("Priority rank / 优先级", "priority_rank"),
        ("Current stage / 当前阶段", "current_stage"),
        ("Authority tier / 来源层级", "authority_tier"),
        ("Rights status / 权利状态", "rights_status"),
    ]:
        lines.extend(field_lines("- ", label, row[field]))
    lines.extend(["", "## Observed Gap Evidence / 已观察缺口证据", ""])
    for item in split_values(row["observed_gap_evidence"]):
        lines.extend(field_lines("- ", "Observed item / 已观察项", item))
    lines.extend(["", "## Route Files To Open / 待打开路线文件", ""])
    for route_file in route_files:
        lines.extend(field_lines("- ", "Route file / 路线文件", route_file))
    lines.extend(
        [
            "",
            "## Required Next Checks / 必需下一步检查",
            "",
        ]
    )
    for check in next_checks:
        label_en, label_zh = CHECK_LABELS.get(check, (check, check))
        lines.extend(
            [
                f"- `{check}`",
            ]
        )
        lines.extend(paragraph_lines("  - English: ", label_en, continuation_prefix="    "))
        lines.extend(paragraph_lines("  - 简体中文：", label_zh, continuation_prefix="    "))
    lines.extend(
        [
            "",
            "## Evidence Collection / 证据收集",
            "",
            "English: Existing metadata has been captured from routed records.",
            "It remains metadata-only and does not promote source content.",
            "",
            "简体中文：已从路线记录捕获现有 metadata。",
            "这些内容仍为 metadata-only，不提升为来源正文。",
            "",
            "## Existing Metadata Snapshot / 已有 metadata 快照",
            "",
        ]
    )
    for label, field in [
        ("Evidence snapshot ID / 证据快照 ID", "evidence_snapshot_id"),
        ("Evidence status / 证据状态", "evidence_status"),
        ("Source review status / 来源复核状态", "source_review_status"),
        ("Rights status / 权利状态", "rights_status"),
        ("Download manifest IDs / 下载 manifest ID", "download_manifest_ids"),
        ("Download log IDs / 下载日志 ID", "download_log_ids"),
        ("download_log_status_counts", "download_log_status_counts"),
        ("download_log_http_status_counts", "download_log_http_status_counts"),
        ("download_log_file_size_bytes_total", "download_log_file_size_bytes_total"),
        ("download_log_checksum_present_count", "download_log_checksum_present_count"),
        ("package_file_ids", "package_file_ids"),
        ("metadata_profile_ids", "metadata_profile_ids"),
        ("Route file missing count / 缺失路线文件数", "route_file_missing_count"),
    ]:
        lines.extend(field_lines("- ", label, snapshot.get(field, "")))
    lines.extend(
        [
            "",
            "## Snapshot Boundary / 快照边界",
            "",
        ]
    )
    for label, field in [
        ("Rights decision status / 权利决策状态", "rights_decision_status"),
        ("Source promotion status / 来源提升状态", "source_promotion_status"),
        ("Corpus import status / 语料导入状态", "corpus_import_status"),
    ]:
        lines.extend(field_lines("- ", label, snapshot.get(field, "")))
    lines.extend(
        [
            "- Identity, component, evolution, and decipherment claims:",
            "  - `blocked`",
            "- 身份、构件、演化链和释读结论：",
            "  - `blocked`",
            "",
            "## Review Log / 复核日志",
            "",
            "- Status / 状态: `created_from_099_source_engineering_gap_queue`",
            "- Decision / 决定:",
            "  - no rights clearance, no source promotion, no corpus import,",
            "    no identity claim, and no decipherment conclusion.",
            "",
            "## Caution / 警示",
            "",
            *paragraph_lines("English: ", CAUTION_EN, continuation_prefix="  "),
            "",
            *paragraph_lines("简体中文：", CAUTION_ZH, continuation_prefix="  "),
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
    expected_paths = {row["draft_path"] for row in rows}
    queue_dir = root / REVIEW_QUEUE_DIR
    if queue_dir.exists():
        for path in sorted(queue_dir.glob("*_review-log.md")):
            rel_path = path.relative_to(root).as_posix()
            if rel_path not in expected_paths:
                path.unlink()
    for row in rows:
        draft_path = root / row["draft_path"]
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(build_markdown(row), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-engineering gap review-log drafts.")
    parser.add_argument("--queue", default=str(SOURCE_ENGINEERING_GAP_QUEUE))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    queue_rows = read_csv_rows(root / args.queue)
    manifest_rows = build_draft_manifest_rows(queue_rows)
    write_markdown_drafts(root, manifest_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(f"wrote={len(manifest_rows)} manifest={(root / args.manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
