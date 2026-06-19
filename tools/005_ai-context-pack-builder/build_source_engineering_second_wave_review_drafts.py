#!/usr/bin/env python3
"""Materialize second-wave source-engineering review drafts from 123.

These drafts are human-review work surfaces for source-level continuation
tasks. They are empty metadata-only scaffolds: no evidence is collected, no
rights decision is made, no source is promoted, no corpus row is imported, and
no identity, component, evolution, or decipherment claim is made.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
SECOND_WAVE_SOURCE_CHECKLIST = STAT_DIR / "123_ai-agent-source-engineering-second-wave-source-checklist.csv"
DEFAULT_MANIFEST = STAT_DIR / "124_ai-agent-source-engineering-second-wave-review-draft-manifest.csv"

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
    return [f"- `{value}`" for value in values] if values else ["- none"]


def build_markdown(checklist_row: dict[str, str], manifest_row: dict[str, str]) -> str:
    lines = [
        "# Source Engineering Second-Wave Review Draft / 来源工程第二波复核草稿",
        "",
        "## Status / 状态",
        "",
        f"- Review draft ID / 复核草稿 ID: `{manifest_row['review_draft_id']}`",
        f"- Continuation task ID / 后续任务 ID: `{manifest_row['continuation_task_id']}`",
        f"- Source status ID / 来源状态 ID: `{manifest_row['source_status_id']}`",
        f"- Draft status / 草稿状态: `{manifest_row['draft_status']}`",
        f"- Evidence collection status / 证据收集状态: `{manifest_row['evidence_collection_status']}`",
        f"- Human review status / 人工复核状态: `{manifest_row['human_review_status']}`",
        f"- Research boundary / 研究边界: `{manifest_row['research_boundary']}`",
        f"- Updated at / 更新时间: `{manifest_row['updated_at']}`",
        "",
        "## Source / 来源",
        "",
        f"- Source ID / 来源 ID: `{manifest_row['source_id']}`",
        f"- First-wave status / 第一波状态: `{manifest_row['source_first_wave_status']}`",
        f"- Source action lane / 来源动作泳道: `{manifest_row['source_action_lane']}`",
        "",
        "## Objective / 目标",
        "",
        f"`{manifest_row['source_level_objective']}`",
        "",
        "## Blockers / 阻断项",
        "",
    ]
    lines.extend(bullet_list(split_values(manifest_row["blocker_summary"])))
    lines.extend(
        [
            "",
            "## Required Inputs / 必须打开的输入",
            "",
        ]
    )
    lines.extend(bullet_list(split_values(manifest_row["required_inputs"])))
    lines.extend(
        [
            "",
            "## Result Records / 结果记录",
            "",
        ]
    )
    lines.extend(bullet_list(split_values(manifest_row["result_record_paths"])))
    lines.extend(
        [
            "",
            "## Reviewed Evidence Paths / 已复核证据路径",
            "",
        ]
    )
    lines.extend(bullet_list(split_values(manifest_row["reviewed_evidence_paths"])))
    lines.extend(
        [
            "",
            "## Boundary Status / 边界状态",
            "",
            f"- Rights decision status / 权利决定状态: `{manifest_row['rights_decision_status']}`",
            f"- Source promotion status / 来源提升状态: `{manifest_row['source_promotion_status']}`",
            f"- Corpus import status / 语料导入状态: `{manifest_row['corpus_import_status']}`",
            f"- Decipherment claim status / 释读结论状态: `{manifest_row['decipherment_claim_status']}`",
            f"- Identity claim status / 身份判断状态: `{manifest_row['identity_claim_status']}`",
            f"- Component claim status / 构件判断状态: `{manifest_row['component_claim_status']}`",
            f"- Evolution claim status / 演化链判断状态: `{manifest_row['evolution_claim_status']}`",
            "",
            "## Review Notes / 复核记录",
            "",
            "English: This draft intentionally contains no collected evidence yet. Record reviewed evidence only after opening the required inputs and preserving source, rights, checksum/access, manifest, field-map, or derivative-record boundaries.",
            "",
            "简体中文：本草稿暂不包含已收集证据。只有在打开必须输入并保留来源、权利、checksum/访问、manifest、field-map 或派生记录边界后，才可记录复核证据。",
            "",
            "- Review outcome / 复核结果: not decided",
            "- Rights outcome / 权利结果: no_new_rights_decision",
            "- Promotion outcome / 提升结果: not_promoted",
            "- Import outcome / 导入结果: not_imported",
            "",
            "## Caution / 警示",
            "",
            f"English: {CAUTION}",
            "",
            "简体中文：本第二波来源复核草稿仅用于 metadata-only 路由；不是已收集证据，不是权利决定，不是来源提升，不是语料导入，不是身份判断，不是构件归属，不是演化链归属，也不是释读结论。",
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
