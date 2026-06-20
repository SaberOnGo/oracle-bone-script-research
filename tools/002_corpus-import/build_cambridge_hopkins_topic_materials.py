#!/usr/bin/env python3
"""Build object-local topic candidate materials from Cambridge/Hopkins metadata."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


CLASSIFIED_SUMMARY = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "003_cambridge-hopkins-classified-summary.csv"
)
CROSSWALK_STAGING = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "002_cambridge-hopkins-crosswalk-staging.csv"
)
OUTPUT_ROOT = Path("corpus/007_research-topics-and-grammar")
TOPIC_REGISTER_DIR = OUTPUT_ROOT / "000_topic-registers"
TOPIC_OBJECT_ROOT = OUTPUT_ROOT / "001_topic-candidates"
TOPIC_INDEX = TOPIC_REGISTER_DIR / "001_cambridge-hopkins-topic-candidate-index.csv"
TOPIC_CROSSWALK_LINKS = TOPIC_REGISTER_DIR / "002_cambridge-hopkins-topic-crosswalk-link-staging.csv"
UNROUTED_CROSSWALK_LINKS = TOPIC_REGISTER_DIR / "003_cambridge-hopkins-unrouted-crosswalk-staging.csv"
SOURCE_ID = "src-cambridge-hopkins"
DOWNLOAD_ID = "dl-cambridge-hopkins-finding-list"
UPDATED_AT = "2026-06-20"

TOPIC_INDEX_FIELDS = [
    "topic_candidate_id",
    "record_type",
    "canonical_path",
    "primary_external_ref_id",
    "source_id",
    "evidence_download_id",
    "source_summary_row_id",
    "source_group_number",
    "topic_label_en",
    "topic_label_zh",
    "period_i_count",
    "period_ii_count",
    "period_iii_count",
    "period_iv_count",
    "period_v_count",
    "total_count",
    "linked_crosswalk_candidate_count",
    "rights_status",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

TOPIC_SOURCE_FIELDS = [
    "topic_source_index_id",
    "topic_candidate_id",
    "source_id",
    "evidence_download_id",
    "source_file_path",
    "source_summary_row_id",
    "source_group_number",
    "source_summary_kind",
    "rights_status",
    "review_status",
    "research_boundary",
    "caution",
]

PERIOD_COUNT_FIELDS = [
    "period_count_id",
    "topic_candidate_id",
    "period_label",
    "source_count_value",
    "count_status",
    "review_status",
    "caution",
]

ROUTE_FIELDS = [
    "topic_crosswalk_route_id",
    "topic_candidate_id",
    "candidate_inscription_crosswalk_id",
    "inscription_crosswalk_project_id",
    "source_group_number",
    "period_label",
    "yingguo_ref_id",
    "cul_ref_id",
    "chalfant_ref_id",
    "heji_ref_id",
    "route_status",
    "review_status",
    "caution",
]

LINK_FIELDS = ROUTE_FIELDS + [
    "source_id",
    "evidence_download_id",
    "research_boundary",
    "updated_at",
]

UNROUTED_FIELDS = [
    "candidate_inscription_crosswalk_id",
    "inscription_crosswalk_project_id",
    "source_id",
    "evidence_download_id",
    "period_label",
    "group_number",
    "yingguo_ref_id",
    "cul_ref_id",
    "chalfant_ref_id",
    "heji_ref_id",
    "route_status",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

RESEARCH_BOUNDARY = "cambridge_hopkins_topic_candidate_preprocessing_only_not_scholarship"
CAUTION = (
    "Cambridge/Hopkins classified-table topic candidate only; not a grammar "
    "analysis result, not an accepted inscription topic assignment, not a "
    "transcription, not a reading, and not a decipherment conclusion."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def safe_token(value: str) -> str:
    token = re.sub(r"[^0-9A-Za-z]+", "-", value).strip("-").lower()
    return token or "unassigned"


def topic_id(index: int) -> str:
    return f"obs-topic-cand-{index:06d}"


def primary_external_ref(row: dict[str, str]) -> str:
    return f"cam-hopkins-group-{int(row['group_number']):02d}"


def object_dir(index: int, row: dict[str, str]) -> Path:
    project_id = topic_id(index)
    external_ref = primary_external_ref(row)
    return TOPIC_OBJECT_ROOT / f"{index:03d}_{project_id}_{external_ref}_topic-candidate"


def crosswalk_project_id(crosswalk_id: str) -> str:
    number = int(crosswalk_id.rsplit("-", 1)[1])
    return f"obs-insc-cw-cand-{number:06d}"


def group_crosswalks(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["group_number"]].append(row)
    return dict(grouped)


def period_rows(project_id: str, row: dict[str, str]) -> list[dict[str, str]]:
    specs = [
        ("I", "period_i_count"),
        ("II", "period_ii_count"),
        ("III", "period_iii_count"),
        ("IV", "period_iv_count"),
        ("V", "period_v_count"),
    ]
    rows = []
    for index, (period_label, field_name) in enumerate(specs, start=1):
        raw_value = row[field_name]
        rows.append(
            {
                "period_count_id": f"{project_id}-period-count-{index:02d}",
                "topic_candidate_id": project_id,
                "period_label": period_label,
                "source_count_value": raw_value,
                "count_status": "reported_count_present" if raw_value.isdigit() else "reported_blank_or_dash",
                "review_status": "reviewed_metadata_only",
                "caution": "Reported classified-table count only; not a verified topic or grammar assignment.",
            }
        )
    return rows


def source_rows(project_id: str, row: dict[str, str]) -> list[dict[str, str]]:
    return [
        {
            "topic_source_index_id": f"{project_id}-source-01",
            "topic_candidate_id": project_id,
            "source_id": SOURCE_ID,
            "evidence_download_id": DOWNLOAD_ID,
            "source_file_path": CLASSIFIED_SUMMARY.as_posix(),
            "source_summary_row_id": row["summary_row_id"],
            "source_group_number": row["group_number"],
            "source_summary_kind": row["summary_kind"],
            "rights_status": "metadata_only_until_verified",
            "review_status": "reviewed_metadata_only",
            "research_boundary": RESEARCH_BOUNDARY,
            "caution": CAUTION,
        }
    ]


def route_rows(
    project_id: str,
    row: dict[str, str],
    crosswalk_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    routes = []
    for index, crosswalk in enumerate(crosswalk_rows, start=1):
        routes.append(
            {
                "topic_crosswalk_route_id": f"{project_id}-crosswalk-route-{index:03d}",
                "topic_candidate_id": project_id,
                "candidate_inscription_crosswalk_id": crosswalk["candidate_inscription_crosswalk_id"],
                "inscription_crosswalk_project_id": crosswalk_project_id(
                    crosswalk["candidate_inscription_crosswalk_id"]
                ),
                "source_group_number": row["group_number"],
                "period_label": crosswalk["period_label"],
                "yingguo_ref_id": crosswalk["yingguo_ref_id"],
                "cul_ref_id": crosswalk["cul_ref_id"],
                "chalfant_ref_id": crosswalk["chalfant_ref_id"],
                "heji_ref_id": crosswalk["heji_ref_id"],
                "route_status": "topic_to_crosswalk_route_metadata_only",
                "review_status": "needs_human_topic_review",
                "caution": CAUTION,
            }
        )
    return routes


def unrouted_rows(
    crosswalk_rows: list[dict[str, str]],
    routed_groups: set[str],
) -> list[dict[str, str]]:
    rows = []
    for crosswalk in crosswalk_rows:
        if crosswalk["group_number"] in routed_groups:
            continue
        rows.append(
            {
                "candidate_inscription_crosswalk_id": crosswalk["candidate_inscription_crosswalk_id"],
                "inscription_crosswalk_project_id": crosswalk_project_id(
                    crosswalk["candidate_inscription_crosswalk_id"]
                ),
                "source_id": SOURCE_ID,
                "evidence_download_id": DOWNLOAD_ID,
                "period_label": crosswalk["period_label"],
                "group_number": crosswalk["group_number"],
                "yingguo_ref_id": crosswalk["yingguo_ref_id"],
                "cul_ref_id": crosswalk["cul_ref_id"],
                "chalfant_ref_id": crosswalk["chalfant_ref_id"],
                "heji_ref_id": crosswalk["heji_ref_id"],
                "route_status": "not_routed_to_topic_candidate_unclassified_source_group",
                "review_status": "needs_human_topic_review",
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def packet(
    project_id: str,
    row: dict[str, str],
    relative_object_dir: Path,
    routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "topic_candidate_id": project_id,
        "record_type": "research_topic_candidate",
        "canonical_path": relative_object_dir.as_posix(),
        "primary_external_ref_id": primary_external_ref(row),
        "source_id": SOURCE_ID,
        "evidence_download_id": DOWNLOAD_ID,
        "source_summary_row_id": row["summary_row_id"],
        "source_group_number": row["group_number"],
        "topic_label_en": row["group_label_en"],
        "topic_label_zh": row["group_label_zh"],
        "period_counts": {
            "I": row["period_i_count"],
            "II": row["period_ii_count"],
            "III": row["period_iii_count"],
            "IV": row["period_iv_count"],
            "V": row["period_v_count"],
        },
        "total_count": row["total_count"],
        "linked_crosswalk_candidate_count": len(routes),
        "topic_assignment_status": "candidate_source_classification_not_reviewed",
        "grammar_analysis_status": "not_started",
        "inscription_topic_claim_status": "no_claim",
        "rights_status": "metadata_only_until_verified",
        "review_status": "needs_human_topic_review",
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def readme_text(project_id: str, row: dict[str, str], route_count: int) -> str:
    return f"""# {project_id} Topic Candidate / {project_id} 主题候选

English:
This directory is the object-local entrance for a Cambridge/Hopkins classified-table topic candidate. Human-readable notes, review instructions, source routes, period-count metadata, crosswalk routes, and the AI-readable packet are kept together in this same `corpus/007_research-topics-and-grammar` object directory.

简体中文：
本目录是 Cambridge/Hopkins 分类表主题候选的对象内入口。人类可读说明、复核说明、来源路线、分期计数 metadata、crosswalk 路线和 AI 可读 packet 都放在同一个 `corpus/007_research-topics-and-grammar` 对象目录中。

## Local Files / 本目录文件
- `01_topic-candidate-packet.json`: AI-readable topic candidate packet.
- `02_topic-source-index.csv`: source and provenance route.
- `03_period-count-index.csv`: period-count metadata from the classified table.
- `04_inscription-crosswalk-route-index.csv`: route rows to inscription crosswalk candidates.
- `05_human-topic-review-sheet.md`: human review checklist.

## Candidate Summary / 候选摘要
- Topic candidate ID / 主题候选 ID: `{project_id}`
- Source group / 来源分组: `{row["group_number"]}`
- English source label / 英文来源标签: `{row["group_label_en"]}`
- Chinese source label / 中文来源标签: `{row["group_label_zh"]}`
- Reported total / 来源表合计: `{row["total_count"]}`
- Linked crosswalk candidate routes / 已关联 crosswalk 候选路线: `{route_count}`

## Boundary / 边界

English:
This is only a source-classification candidate from a Cambridge/Hopkins metadata table. It is not a grammar analysis result, not an accepted inscription topic assignment, not a transcription, not a reading, and not a decipherment conclusion.

简体中文：
这只是来自 Cambridge/Hopkins metadata 表的来源分类候选。它不是语法分析结果，不是已确认卜辞主题归属，不是释文，不是读法，也不是破译结论。
"""


def review_sheet_text(project_id: str, row: dict[str, str]) -> str:
    return f"""# {project_id} Human Topic Review Sheet / {project_id} 人工主题复核表

## Review Scope / 复核范围

English:
Review whether the Cambridge/Hopkins classified-table group is useful as a controlled vocabulary candidate for later inscription analysis. Do not confirm grammar, topic assignments, readings, or decipherment here.

简体中文：
这里仅复核 Cambridge/Hopkins 分类表分组是否适合作为后续卜辞分析的受控词表候选。不要在这里确认语法、主题归属、读法或破译结论。

## Checklist / 清单

- [ ] Source summary row checked in `02_topic-source-index.csv`
- [ ] Period counts checked in `03_period-count-index.csv`
- [ ] Crosswalk routes checked in `04_inscription-crosswalk-route-index.csv`
- [ ] Label wording reviewed as source metadata only
- [ ] No grammar analysis or inscription-topic conclusion added
- [ ] No transcription, reading, or decipherment conclusion added

## Current Status / 当前状态
- Source group / 来源分组: `{row["group_number"]}`
- Review status / 复核状态: `needs_human_topic_review`
- Grammar analysis status / 语法分析状态: `not_started`
- Inscription topic claim status / 卜辞主题结论状态: `no_claim`
"""


def build_materials(root: Path) -> dict[str, int]:
    summary_rows = [
        row
        for row in read_csv(root / CLASSIFIED_SUMMARY)
        if row["summary_kind"] == "classified_table_group"
    ]
    crosswalk_rows = read_csv(root / CROSSWALK_STAGING)
    crosswalks_by_group = group_crosswalks(crosswalk_rows)
    topic_index_rows = []
    link_rows = []
    routed_groups = {row["group_number"] for row in summary_rows}
    for index, row in enumerate(summary_rows, start=1):
        project_id = topic_id(index)
        relative_object_dir = object_dir(index, row)
        output_dir = root / relative_object_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        routes = route_rows(project_id, row, crosswalks_by_group.get(row["group_number"], []))
        topic_packet = packet(project_id, row, relative_object_dir, routes)
        write_json(output_dir / "01_topic-candidate-packet.json", topic_packet)
        write_csv(output_dir / "02_topic-source-index.csv", TOPIC_SOURCE_FIELDS, source_rows(project_id, row))
        write_csv(output_dir / "03_period-count-index.csv", PERIOD_COUNT_FIELDS, period_rows(project_id, row))
        write_csv(output_dir / "04_inscription-crosswalk-route-index.csv", ROUTE_FIELDS, routes)
        (output_dir / "README.md").write_text(readme_text(project_id, row, len(routes)), encoding="utf-8")
        (output_dir / "05_human-topic-review-sheet.md").write_text(
            review_sheet_text(project_id, row), encoding="utf-8"
        )
        topic_index_rows.append(
            {
                "topic_candidate_id": project_id,
                "record_type": "research_topic_candidate",
                "canonical_path": relative_object_dir.as_posix(),
                "primary_external_ref_id": primary_external_ref(row),
                "source_id": SOURCE_ID,
                "evidence_download_id": DOWNLOAD_ID,
                "source_summary_row_id": row["summary_row_id"],
                "source_group_number": row["group_number"],
                "topic_label_en": row["group_label_en"],
                "topic_label_zh": row["group_label_zh"],
                "period_i_count": row["period_i_count"],
                "period_ii_count": row["period_ii_count"],
                "period_iii_count": row["period_iii_count"],
                "period_iv_count": row["period_iv_count"],
                "period_v_count": row["period_v_count"],
                "total_count": row["total_count"],
                "linked_crosswalk_candidate_count": str(len(routes)),
                "rights_status": "metadata_only_until_verified",
                "review_status": "needs_human_topic_review",
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
        for route in routes:
            link_rows.append(
                {
                    **route,
                    "source_id": SOURCE_ID,
                    "evidence_download_id": DOWNLOAD_ID,
                    "research_boundary": RESEARCH_BOUNDARY,
                    "updated_at": UPDATED_AT,
                }
            )
    unrouted = unrouted_rows(crosswalk_rows, routed_groups)
    write_csv(root / TOPIC_INDEX, TOPIC_INDEX_FIELDS, topic_index_rows)
    write_csv(root / TOPIC_CROSSWALK_LINKS, LINK_FIELDS, link_rows)
    write_csv(root / UNROUTED_CROSSWALK_LINKS, UNROUTED_FIELDS, unrouted)
    return {
        "topic_candidate_count": len(topic_index_rows),
        "topic_crosswalk_link_count": len(link_rows),
        "unrouted_crosswalk_link_count": len(unrouted),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    result = build_materials(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
