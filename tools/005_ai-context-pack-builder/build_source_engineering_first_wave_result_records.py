#!/usr/bin/env python3
"""Materialize first-wave source-engineering result records from 119 rows."""

from __future__ import annotations

import argparse
import csv
import textwrap
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
FIRST_WAVE_REVIEW_RESULTS = STAT_DIR / "119_ai-agent-source-engineering-first-wave-review-results.csv"
DEFAULT_MANIFEST = STAT_DIR / "120_ai-agent-source-engineering-first-wave-result-record-manifest.csv"

UPDATED_AT = "2026-06-19"
RESULT_RECORD_STATUS = "metadata_result_record_materialized"
RESEARCH_BOUNDARY = "source_engineering_first_wave_result_record_metadata_only_not_scholarship"
CAUTION = (
    "This result record materializes metadata already captured in 119. It is "
    "not a new download, not checksum recalculation, not a rights decision, "
    "not source promotion, not corpus import, not an oracle-character identity "
    "claim, not a component assignment, not an evolution-chain assignment, "
    "and not a decipherment conclusion."
)

OUTPUT_FIELDS = [
    "result_record_manifest_id",
    "first_wave_result_id",
    "handoff_item_id",
    "next_action_id",
    "source_engineering_gap_id",
    "source_id",
    "action_lane",
    "decision_field",
    "decision_value",
    "result_record_path",
    "result_record_status",
    "source_result_path",
    "reviewed_evidence_paths",
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


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def wrap_code_value(prefix: str, value: str, *, width: int = 80) -> list[str]:
    if not value:
        return [f"{prefix}`none`"]
    if len(f"{prefix}`{value}`") > width and len(f"  - `{value}`") <= width:
        return [prefix.rstrip(), f"  - `{value}`"]
    first_limit = max(8, width - len(prefix) - 2)
    chunks = textwrap.wrap(
        value,
        width=first_limit,
        break_long_words=True,
        break_on_hyphens=True,
    )
    if not chunks:
        return [f"{prefix}`none`"]
    lines = [f"{prefix}`{chunks[0]}`"]
    remainder = value[len(chunks[0]) :].lstrip("-_/; ")
    for chunk in textwrap.wrap(
        remainder,
        width=width - 4,
        break_long_words=True,
        break_on_hyphens=True,
    ):
        lines.append(f"  `{chunk}`")
    return lines


def kv_lines(label: str, value: str) -> list[str]:
    return wrap_code_value(f"- {label}: ", value)


def path_value_lines(value: str) -> list[str]:
    if len(f"- `{value}`") <= 80:
        return [f"- `{value}`"]
    path = Path(value)
    parent = path.parent.as_posix()
    name = path.name
    lines: list[str] = []
    if parent and parent != ".":
        lines.extend(wrap_code_value("- ", f"{parent}/"))
        lines.extend(wrap_code_value("  ", name))
    else:
        lines.extend(wrap_code_value("- ", name))
    return lines


def paragraph_lines(
    text: str,
    *,
    prefix: str = "",
    continuation_prefix: str = "  ",
    width: int = 76,
) -> list[str]:
    first_width = width - len(prefix)
    continuation_width = width - len(continuation_prefix)
    words = text.split()
    lines: list[str] = []
    current = ""
    current_width = first_width
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > current_width and current:
            line_prefix = prefix if not lines else continuation_prefix
            lines.append(f"{line_prefix}{current}")
            current = word
            current_width = continuation_width
        else:
            current = candidate
    if current:
        line_prefix = prefix if not lines else continuation_prefix
        lines.append(f"{line_prefix}{current}")
    return lines


def build_manifest_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(source_rows, start=1):
        rows.append(
            {
                "result_record_manifest_id": f"source-engineering-first-wave-result-record-{index:04d}",
                "first_wave_result_id": row["first_wave_result_id"],
                "handoff_item_id": row["handoff_item_id"],
                "next_action_id": row["next_action_id"],
                "source_engineering_gap_id": row["source_engineering_gap_id"],
                "source_id": row["source_id"],
                "action_lane": row["action_lane"],
                "decision_field": row["decision_field"],
                "decision_value": row["decision_value"],
                "result_record_path": row["result_record_path"],
                "result_record_status": RESULT_RECORD_STATUS,
                "source_result_path": FIRST_WAVE_REVIEW_RESULTS.as_posix(),
                "reviewed_evidence_paths": row["reviewed_evidence_paths"],
                "human_review_status": row["human_review_status"],
                "rights_decision_status": row["rights_decision_status"],
                "source_promotion_status": row["source_promotion_status"],
                "corpus_import_status": row["corpus_import_status"],
                "decipherment_claim_status": row["decipherment_claim_status"],
                "identity_claim_status": row["identity_claim_status"],
                "component_claim_status": row["component_claim_status"],
                "evolution_claim_status": row["evolution_claim_status"],
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_markdown(row: dict[str, str]) -> str:
    evidence_paths = split_semicolon(row["reviewed_evidence_paths"])
    required_next_checks = split_semicolon(row["required_next_checks"])
    required_followup = split_semicolon(row["required_followup"])
    lines = [
        "# Source Engineering First-Wave Result Record / 来源工程第一波结果记录",
        "",
        "## Status / 状态",
        "",
    ]
    for label, value in [
        ("First-wave result ID / 第一波结果 ID", row["first_wave_result_id"]),
        ("Handoff item ID / 交接项 ID", row["handoff_item_id"]),
        ("Next action ID / 下一动作 ID", row["next_action_id"]),
        ("Source engineering gap ID / 来源工程缺口 ID", row["source_engineering_gap_id"]),
        ("Evidence snapshot ID / 证据快照 ID", row["evidence_snapshot_id"]),
        ("Result status / 结果状态", row["result_status"]),
        ("Evidence collection status / 证据收集状态", row["evidence_collection_status"]),
        ("Human review status / 人工复核状态", row["human_review_status"]),
        ("Research boundary / 研究边界", RESEARCH_BOUNDARY),
        ("Updated at / 更新时间", UPDATED_AT),
    ]:
        lines.extend(kv_lines(label, value))
    lines.extend(
        [
            "",
            *paragraph_lines(
                "This is a metadata-only review result materialized from "
                "existing local records.",
                prefix="English: ",
            ),
            "",
            "简体中文：本记录仅把本地已有记录中的元数据复核结果实体化。",
            "",
            "## Source / 来源",
            "",
        ]
    )
    for label, value in [
        ("Source ID / 来源 ID", row["source_id"]),
        ("Title / 标题", row["source_title"]),
        ("Provider / 提供方", row["provider"]),
        ("Source URL / 来源 URL", row["source_url"]),
        ("Authority tier / 来源层级", row["authority_tier"]),
        ("Rights status / 权利状态", row["rights_status"]),
    ]:
        lines.extend(kv_lines(label, value))
    lines.extend(paragraph_lines(row["risk_note"], prefix="- Risk note / 风险提示: "))
    lines.extend(["", "## Metadata Result / 元数据结果", ""])
    for label, value in [
        ("Action lane / 动作线", row["action_lane"]),
        ("Gap type / 缺口类型", row["gap_type"]),
        ("Pipeline current stage / 流水线当前阶段", row["pipeline_current_stage"]),
        ("Decision field / 决策字段", row["decision_field"]),
        ("Decision value / 决策值", row["decision_value"]),
        ("Download manifest IDs / 下载 manifest ID", row["download_manifest_ids"]),
        ("Download log IDs / 下载日志 ID", row["download_log_ids"]),
        ("download_log_status_counts", row["download_log_status_counts"]),
        ("download_log_http_status_counts", row["download_log_http_status_counts"]),
        ("download_log_file_size_bytes_total", row["download_log_file_size_bytes_total"]),
        ("download_log_checksum_present_count", row["download_log_checksum_present_count"]),
        ("package_manifest_row_count", row["package_manifest_row_count"]),
        ("metadata_profile_metric_count", row["metadata_profile_metric_count"]),
        ("metadata_profile_ids", row["metadata_profile_ids"]),
        ("field_map_scaffold_id", row["field_map_scaffold_id"]),
        ("field_map_review_status", row["field_map_review_status"]),
    ]:
        lines.extend(kv_lines(label, value))
    lines.extend(["", "## Boundary Status / 边界状态", ""])
    for label, value in [
        ("Rights decision status / 权利决策状态", row["rights_decision_status"]),
        ("Source promotion status / 来源提升状态", row["source_promotion_status"]),
        ("Corpus import status / 语料导入状态", row["corpus_import_status"]),
        ("Decipherment claim status / 释读结论状态", row["decipherment_claim_status"]),
        ("Identity claim status / 身份判断状态", row["identity_claim_status"]),
        ("Component claim status / 构件判断状态", row["component_claim_status"]),
        ("Evolution claim status / 演化链判断状态", row["evolution_claim_status"]),
    ]:
        lines.extend(kv_lines(label, value))
    lines.extend(["", "## Reviewed Evidence Paths / 已复核证据路径", ""])
    for path in evidence_paths:
        lines.extend(path_value_lines(path))
    lines.extend(
        [
            "",
            "## Required Next Checks / 后续必检项",
            "",
        ]
    )
    for value in required_next_checks:
        lines.extend(wrap_code_value("- ", value))
    lines.extend(
        [
            "",
            "## Required Followup / 后续动作",
            "",
        ]
    )
    for value in required_followup:
        lines.extend(wrap_code_value("- ", value))
    lines.extend(
        [
            "",
            "## Caution / 警示",
            "",
            "- Rights decision boundary / 权利决策边界: not a rights decision",
            "",
        ]
    )
    lines.extend(paragraph_lines(CAUTION, prefix="English: "))
    lines.extend(
        [
            "",
            "简体中文：本记录只实体化 119 中已经捕获的元数据；",
            "它不是新的下载，不是 checksum 复算，不是权利裁定，",
            "不是来源提升，不是语料导入，不是甲骨单字身份判断，",
            "不是构件判断，不是演化链判断，也不是释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown_records(root: Path, rows: list[dict[str, str]]) -> None:
    for row in rows:
        path = root / row["result_record_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(build_markdown(row), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build first-wave source-engineering result records.")
    parser.add_argument("--results", default=str(FIRST_WAVE_REVIEW_RESULTS))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    source_rows = read_csv_rows(root / args.results)
    write_markdown_records(root, source_rows)
    manifest_rows = build_manifest_rows(source_rows)
    write_csv(root / args.manifest, manifest_rows)
    print(
        f"result_record_count={len(manifest_rows)} "
        f"manifest={(root / args.manifest).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
