#!/usr/bin/env python3
"""Build object-local topic candidate materials from Cambridge/Hopkins metadata."""

from __future__ import annotations

import argparse
import csv
import json
import re
import textwrap
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
MAX_HUMAN_LINE_LENGTH = 80


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


def wrapped_bullet(text: str) -> str:
    return textwrap.fill(
        f"- {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrapped_check(text: str) -> str:
    return textwrap.fill(
        f"- [ ] {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrapped_paragraph(text: str) -> str:
    return textwrap.fill(
        text,
        width=MAX_HUMAN_LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
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
    english_intro = wrapped_paragraph(
        "This directory is the object-local entrance for a Cambridge/Hopkins "
        "classified-table topic candidate. Human-readable notes, review "
        "instructions, source routes, period-count metadata, crosswalk routes, "
        "and the AI-readable packet are kept together in this same corpus "
        "object directory."
    )
    chinese_intro = wrapped_paragraph(
        "本目录是 Cambridge/Hopkins 分类表主题候选的对象内入口。人类可读"
        "说明、复核说明、来源路线、分期计数、卜辞互证路线和 AI 辅助"
        "packet 都放在同一个 corpus 对象目录中。"
    )
    file_entries = "\n".join(
        [
            wrapped_bullet("`01_topic-candidate-packet.json`: AI-readable packet."),
            wrapped_bullet("`02_topic-source-index.csv`: source and provenance route."),
            wrapped_bullet("`03_period-count-index.csv`: period-count metadata."),
            wrapped_bullet(
                "`04_inscription-crosswalk-route-index.csv`: inscription "
                "crosswalk route rows."
            ),
            wrapped_bullet("`05_human-topic-review-sheet.md`: human checklist."),
            wrapped_bullet("`06_human-topic-dossier.md`: human topic dossier."),
            wrapped_bullet("`07_topic-dossier-index.json`: AI support index."),
            wrapped_bullet(
                "`08_topic-literature-context-dossier.md`: literature/context "
                "dossier."
            ),
            wrapped_bullet("`09_topic-literature-context-index.json`: AI index."),
            wrapped_bullet(
                "`10_topic-citation-dispute-review-dossier.md`: citation and "
                "dispute review."
            ),
            wrapped_bullet(
                "`11_topic-citation-dispute-review-index.json`: AI support index."
            ),
        ]
    )
    english_boundary = wrapped_paragraph(
        "This is only a source-classification candidate from a "
        "Cambridge/Hopkins metadata table. It is not a grammar analysis "
        "result, not an accepted inscription topic assignment, not a "
        "transcription, not a reading, and not a decipherment conclusion."
    )
    chinese_boundary = wrapped_paragraph(
        "这只是来自 Cambridge/Hopkins metadata 表的来源分类候选。它不是"
        "语法分析结果，不是已接受的卜辞主题归属，不是释文，不是读法，"
        "也不是破译结论。"
    )
    return f"""# {project_id} Topic Candidate / {project_id} 主题候选
English:
{english_intro}

简体中文：
{chinese_intro}

## Local Files / 本目录文件
{file_entries}

## Candidate Summary / 候选摘要
- Topic candidate ID / 主题候选 ID: `{project_id}`
- Source group / 来源分组: `{row["group_number"]}`
- English source label / 英文来源标签: `{row["group_label_en"]}`
- Chinese source label / 中文来源标签: `{row["group_label_zh"]}`
- Reported total / 来源表合计: `{row["total_count"]}`
- Linked crosswalk candidate routes / 已关联 crosswalk 候选路线: `{route_count}`

## Boundary / 边界

English:
{english_boundary}

简体中文：
{chinese_boundary}
"""


def review_sheet_text(project_id: str, row: dict[str, str]) -> str:
    english_scope = wrapped_paragraph(
        "Review whether the Cambridge/Hopkins classified-table group is useful "
        "as a controlled vocabulary candidate for later inscription analysis. "
        "Do not confirm grammar, topic assignments, readings, or decipherment "
        "here."
    )
    chinese_scope = wrapped_paragraph(
        "这里只复核 Cambridge/Hopkins 分类表分组是否适合作为后续卜辞分析"
        "的受控词表候选。不要在这里确认语法、主题归属、读法或破译结论。"
    )
    checklist = "\n".join(
        [
            wrapped_check("Source summary row checked in `02_topic-source-index.csv`"),
            wrapped_check("Period counts checked in `03_period-count-index.csv`"),
            wrapped_check(
                "Crosswalk routes checked in `04_inscription-crosswalk-route-index.csv`"
            ),
            wrapped_check("Label wording reviewed as source metadata only"),
            wrapped_check("No grammar analysis or inscription-topic conclusion added"),
            wrapped_check("No transcription, reading, or decipherment conclusion added"),
        ]
    )
    concrete_questions = "\n".join(
        [
            wrapped_bullet(
                "Open `02_topic-source-index.csv` and name the Cambridge/Hopkins "
                "source group row and original label."
            ),
            wrapped_bullet(
                "Open `03_period-count-index.csv` and list which period counts are "
                "only source-table counts."
            ),
            wrapped_bullet(
                "Open `04_inscription-crosswalk-route-index.csv` and name the first "
                "crosswalk route that needs inscription-context review."
            ),
            wrapped_bullet(
                "Open `06_human-topic-dossier.md` and record which label wording "
                "could mislead readers if treated as a confirmed topic."
            ),
            wrapped_bullet(
                "Open `08_topic-literature-context-dossier.md` and name missing "
                "bibliography, proposer, alternate-label, or disagreement routes."
            ),
            wrapped_bullet(
                "打开 `02_topic-source-index.csv`，写明 Cambridge/Hopkins 来源分组行"
                "和原始标签。"
            ),
            wrapped_bullet(
                "打开 `03_period-count-index.csv`，列出哪些分期计数只是来源表"
                "计数，仍待人工复核。"
            ),
            wrapped_bullet(
                "打开 `04_inscription-crosswalk-route-index.csv`，写明第一条需要"
                "回到卜辞语境复核的 crosswalk 路线。"
            ),
            wrapped_bullet(
                "打开 `06_human-topic-dossier.md`，记录哪些标签措辞若被当成"
                "已确认主题会误导读者。"
            ),
            wrapped_bullet(
                "打开 `08_topic-literature-context-dossier.md`，写明仍缺的书目、"
                "提出者、替代标签或不同意见路线。"
            ),
        ]
    )
    return f"""# {project_id} Human Topic Review Sheet / {project_id} 人工主题复核表
## Review Scope / 复核范围

English:
{english_scope}

简体中文：
{chinese_scope}

## Checklist / 清单

{checklist}

## Concrete Questions To Check / 具体待查问题

{concrete_questions}

## Current Status / 当前状态
- Source group / 来源分组: `{row["group_number"]}`
- Review status / 复核状态: `needs_human_topic_review`
- Grammar analysis status / 语法分析状态: `not_started`
- Inscription topic claim status / 卜辞主题结论状态: `no_claim`
"""


def topic_dossier_text(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> str:
    period_lines = "\n".join(
        [
            f"| I | {row['period_i_count']} |",
            f"| II | {row['period_ii_count']} |",
            f"| III | {row['period_iii_count']} |",
            f"| IV | {row['period_iv_count']} |",
            f"| V | {row['period_v_count']} |",
        ]
    )
    first_routes = routes[:5]
    route_lines = "\n".join(
        [
            "| {route_id} | {crosswalk_id} | {period} | {heji} |".format(
                route_id=route["topic_crosswalk_route_id"],
                crosswalk_id=route["inscription_crosswalk_project_id"],
                period=route["period_label"],
                heji=route["heji_ref_id"]
                or "待查: check 04_inscription-crosswalk-route-index.csv Heji route",
            )
            for route in first_routes
        ]
    )
    if not first_routes:
        route_lines = "| 待查: check 04_inscription-crosswalk-route-index.csv route | 待查: check 04_inscription-crosswalk-route-index.csv crosswalk | 待查: check 04_inscription-crosswalk-route-index.csv period | 待查: check 04_inscription-crosswalk-route-index.csv Heji |"
    questions = "\n".join(
        [
            wrapped_bullet(
                "Open `02_topic-source-index.csv` and verify the source id, "
                "download id, group number, and rights status."
            ),
            wrapped_bullet(
                "Open `03_period-count-index.csv` and record which reported "
                "counts need comparison with inscription examples."
            ),
            wrapped_bullet(
                "Open `04_inscription-crosswalk-route-index.csv` before any "
                "topic or grammar discussion starts."
            ),
            wrapped_bullet(
                "Open `08_topic-literature-context-dossier.md` for bibliography, "
                "scope, proposer, and disagreement gaps."
            ),
            wrapped_bullet(
                "Open `10_topic-citation-dispute-review-dossier.md` before using "
                "this label in a research note."
            ),
            wrapped_bullet(
                "打开 `02_topic-source-index.csv`，核对来源 ID、下载记录 ID、"
                "分组号和权利状态。"
            ),
            wrapped_bullet(
                "打开 `03_period-count-index.csv`，记录哪些来源计数需要与卜辞"
                "实例互相核对。"
            ),
            wrapped_bullet(
                "讨论任何主题或语法问题前，先打开 "
                "`04_inscription-crosswalk-route-index.csv`。"
            ),
            wrapped_bullet(
                "打开 `08_topic-literature-context-dossier.md`，检查书目、适用"
                "范围、提出者和不同意见缺口。"
            ),
            wrapped_bullet(
                "在研究笔记中使用该标签前，先打开 "
                "`10_topic-citation-dispute-review-dossier.md`。"
            ),
        ]
    )
    intro_en = wrapped_paragraph(
        "This dossier records a Cambridge/Hopkins classified-table topic "
        "candidate as a source route for later human review. It does not add a "
        "grammar analysis or a topic conclusion."
    )
    intro_zh = wrapped_paragraph(
        "本档案把 Cambridge/Hopkins 分类表主题候选整理成后续人工复核的"
        "来源路线。它不新增语法分析，也不新增主题结论。"
    )
    source_note = "待查: open Cambridge/Hopkins source summary row and 02_topic-source-index.csv"
    label_note = "待查: compare 02_topic-source-index.csv with later bibliography labels"
    return f"""# Human Topic Dossier / 主题候选研究档案
- Topic candidate ID / 主题候选 ID: `{project_id}`

English:
{intro_en}

简体中文：
{intro_zh}

## Bibliography And Source Route / 书目与来源路线
| field | value |
| --- | --- |
| source id | {SOURCE_ID} |
| download id | {DOWNLOAD_ID} |
| source file | {CLASSIFIED_SUMMARY.as_posix()} |
| source summary row | {row["summary_row_id"]} |
| source group | {row["group_number"]} |
| rights status | metadata_only_until_verified |

## Topic Label And Scope / 主题标签与范围
| field | value |
| --- | --- |
| English source label | {row["group_label_en"]} |
| Chinese source label | {row["group_label_zh"]} |
| current scope | source-classification candidate for review |
| claim status | no grammar or inscription-topic claim |

## Period Counts And Inscription Routes / 分期计数与卜辞路线
| period | source-table count |
| --- | --- |
{period_lines}

| route id | crosswalk id | period | Heji route |
| --- | --- | --- | --- |
{route_lines}

## Evidence Level And Review Status / 证据等级与复核状态
| field | value |
| --- | --- |
| evidence level | metadata and crosswalk route only |
| review status | needs_human_topic_review |
| grammar analysis status | not_started |
| inscription topic claim status | no_claim |

## Citation And Disagreement Notes / 引用与分歧记录
| field | current status |
| --- | --- |
| citation relationship | {source_note} |
| alternate labels | {label_note} |
| different opinions | 待查: review Cambridge/Hopkins label against scholarship notes |

## Concrete Questions To Check / 具体待查问题
{questions}

## Review Boundary / 复核边界

- candidate topic route only
- not a grammar conclusion
- not an inscription-topic assignment
- not a transcription
- not a reading
- not a decipherment conclusion
"""

def topic_dossier_index_payload(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "topic_candidate_id": project_id,
        "record_type": "research_topic_dossier_index",
        "human_readable_files": [
            "README.md",
            "05_human-topic-review-sheet.md",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
        ],
        "source_route_files": [
            CLASSIFIED_SUMMARY.as_posix(),
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
        ],
        "source_group_number": row["group_number"],
        "linked_crosswalk_candidate_count": len(routes),
        "uncollected_human_research_fields": [
            "topic_label_scope_review",
            "bibliographic_citation_relationships",
            "later_scholarship_discussion",
            "different_opinions_or_alternate_classifications",
            "inscription_context_review",
            "grammar_analysis_review",
        ],
        "claim_boundary": [
            "no grammar conclusion",
            "no inscription-topic assignment",
            "no transcription",
            "no reading",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_topic_review",
        "updated_at": UPDATED_AT,
    }




def topic_literature_context_dossier_text(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> str:
    route_sample = routes[:8]
    route_lines = "\n".join(
        [
            "| {crosswalk} | {period} | {yingguo} | {heji} |".format(
                crosswalk=route["inscription_crosswalk_project_id"],
                period=route["period_label"],
                yingguo=route["yingguo_ref_id"]
                or "待查: check 04_inscription-crosswalk-route-index.csv Yingguo route",
                heji=route["heji_ref_id"]
                or "待查: check 04_inscription-crosswalk-route-index.csv Heji route",
            )
            for route in route_sample
        ]
    )
    if not route_lines:
        route_lines = "| 待查: check 04_inscription-crosswalk-route-index.csv crosswalk | 待查: check 04_inscription-crosswalk-route-index.csv period | 待查: check 04_inscription-crosswalk-route-index.csv Yingguo | 待查: check 04_inscription-crosswalk-route-index.csv Heji |"
    intro_en = wrapped_paragraph(
        "This human-readable dossier records the bibliography, citation, "
        "applicable-scope, evidence-level, inscription-context, proposer, "
        "disagreement, and alternate-label checks needed before this topic "
        "candidate can support later research."
    )
    intro_zh = wrapped_paragraph(
        "本档案记录主题候选进入后续研究前需要复核的书目、引用、适用"
        "范围、证据等级、卜辞语境、提出者、不同意见和替代标签问题。"
    )
    questions = "\n".join(
        [
            wrapped_bullet(
                "Open the Cambridge/Hopkins finding-list source summary row "
                "and record which bibliography note supports the label."
            ),
            wrapped_bullet(
                "Open `04_inscription-crosswalk-route-index.csv` and name the "
                "first cited inscription route to inspect."
            ),
            wrapped_bullet(
                "Open `02_topic-source-index.csv` and compare the source label "
                "with later bibliography labels."
            ),
            wrapped_bullet(
                "Record whether the missing evidence is bibliography, cited "
                "inscription, proposer, alternate label, or disagreement."
            ),
            wrapped_bullet(
                "打开 Cambridge/Hopkins finding-list 来源摘要行，记录哪条书目"
                "说明支持该标签。"
            ),
            wrapped_bullet(
                "打开 `04_inscription-crosswalk-route-index.csv`，写明第一条"
                "需要查看的被引卜辞路线。"
            ),
            wrapped_bullet(
                "打开 `02_topic-source-index.csv`，把来源标签与后出书目标签"
                "进行比较。"
            ),
            wrapped_bullet(
                "记录缺失证据属于书目、被引卜辞、提出者、替代标签还是"
                "不同意见。"
            ),
        ]
    )
    boundary_zh = wrapped_paragraph(
        "当前证据只支持查找路线、核对计数和复核书目，不建立语法类别、"
        "历史事实或已接受的主题归属。"
    )
    return f"""# Topic Literature And Inscription Context Dossier / 主题文献与卜辞语境档案
Topic candidate ID: `{project_id}`

English:
{intro_en}

简体中文：
{intro_zh}

## Bibliography And Citation Route / 书目与引用路线
| field | value |
| --- | --- |
| source id | {SOURCE_ID} |
| download id | {DOWNLOAD_ID} |
| source file | {CLASSIFIED_SUMMARY.as_posix()} |
| source summary row | {row["summary_row_id"]} |
| source group | {row["group_number"]} |
| source label en | {row["group_label_en"]} |
| source label zh | {row["group_label_zh"]} |

## Applicable Scope And Evidence Level / 适用范围与证据等级
| field | value |
| --- | --- |
| applicable scope | source-classification route for review |
| evidence level | metadata and crosswalk route only |
| review status | needs_human_topic_review |
| grammar analysis status | not_started |
| inscription topic claim status | no_claim |

English:
{wrapped_paragraph("The current evidence supports route finding, count checking, and bibliography review only. It does not establish a controlled grammar category, historical fact, or accepted topic assignment.")}

简体中文：
{boundary_zh}

## Inscription Context Routes / 卜辞语境路线

| field | value |
| --- | --- |
| linked crosswalk route count | {len(routes)} |
| route index | 04_inscription-crosswalk-route-index.csv |
| sampled route count below | {len(route_sample)} |

| crosswalk id | period | Yingguo route | Heji route |
| --- | --- | --- | --- |
{route_lines}

## Proposer Disagreement And Alternate Labels / 提出者、不同意见与替代标签

| field | current status |
| --- | --- |
| proposer or classifier | Cambridge/Hopkins source table |
| citation relationship | 待查: open Cambridge/Hopkins finding-list source summary row |
| different opinions | 待查: review Cambridge/Hopkins label against scholarship notes |
| alternate labels | 待查: compare 02_topic-source-index.csv with source labels |
| applicability note | candidate literature context only |

## Concrete Missing Literature Questions / 具体缺失文献问题

{questions}

## Review Boundary / 复核边界

- candidate literature context only
- not a grammar conclusion
- not an inscription-topic assignment
- not a transcription
- not a reading
- not a decipherment conclusion
"""

def topic_literature_context_index_payload(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "topic_candidate_id": project_id,
        "record_type": "research_topic_literature_context_index",
        "human_readable_files": [
            "README.md",
            "05_human-topic-review-sheet.md",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
        ],
        "source_evidence_files": [
            CLASSIFIED_SUMMARY.as_posix(),
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
        ],
        "source_group_number": row["group_number"],
        "linked_crosswalk_candidate_count": len(routes),
        "literature_context_status": {
            "bibliography_route": "source_table_recorded_needs_review",
            "citation_relationship": "needs_bibliography_review",
            "applicable_scope": "candidate_route_only",
            "evidence_level": "metadata_and_crosswalk_route_only",
            "proposer": "cambridge_hopkins_source_table",
            "different_opinions": "needs_later_scholarship_review",
            "alternate_labels": "needs_source_comparison_review",
        },
        "missing_literature_questions": [
            "which bibliography note, source page, or finding-list row supports the label",
            "which cited inscription route should be opened first",
            "which period, Heji, Yingguo, CUL, or Chalfant reference needs source checking",
            "who proposed the label, and is the proposer only a source table",
            "which alternate labels or disagreements remain uncollected",
            "what evidence is missing before any grammar, topic, or historical claim",
        ],
        "claim_boundary": (
            "candidate literature context only; no grammar conclusion; no "
            "inscription-topic assignment; no transcription; no reading; no "
            "decipherment conclusion"
        ),
        "review_status": "needs_human_topic_review",
        "updated_at": UPDATED_AT,
    }




def topic_citation_dispute_review_dossier_text(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> str:
    route_sample = routes[:6]
    route_lines = "\n".join(
        [
            "| {crosswalk} | {period} | {yingguo} | {chalfant} |".format(
                crosswalk=route["inscription_crosswalk_project_id"],
                period=route["period_label"],
                yingguo=route["yingguo_ref_id"]
                or "待查: check 04_inscription-crosswalk-route-index.csv Yingguo route",
                chalfant=route["chalfant_ref_id"]
                or "待查: check 04_inscription-crosswalk-route-index.csv Chalfant route",
            )
            for route in route_sample
        ]
    )
    if not route_lines:
        route_lines = "| 待查: check 04_inscription-crosswalk-route-index.csv crosswalk | 待查: check 04_inscription-crosswalk-route-index.csv period | 待查: check 04_inscription-crosswalk-route-index.csv Yingguo | 待查: check 04_inscription-crosswalk-route-index.csv Chalfant |"
    intro_en = wrapped_paragraph(
        "This dossier is a human review map for citation relationships, "
        "proposer/classifier evidence, disagreements, and alternate labels. "
        "It keeps those checks next to the topic candidate before any formal "
        "grammar or inscription-topic study begins."
    )
    intro_zh = wrapped_paragraph(
        "本档案是主题候选的引用关系、提出者或分类者、不同意见和替代"
        "标签复核地图。它只为正式语法或卜辞主题研究前的资料整理服务。"
    )
    questions = "\n".join(
        [
            wrapped_bullet(
                "Open the Cambridge/Hopkins source note or finding-list page "
                "that first states this label."
            ),
            wrapped_bullet(
                "Open `04_inscription-crosswalk-route-index.csv` and name "
                "which Yingguo, CUL, Chalfant, or Heji route cites the label."
            ),
            wrapped_bullet(
                "Open later bibliography notes and record whether they repeat, "
                "narrow, reject, or rename the source classification."
            ),
            wrapped_bullet(
                "Open `08_topic-literature-context-dossier.md` and name "
                "alternate labels to compare before research use."
            ),
            wrapped_bullet(
                "打开最早记录该标签的 Cambridge/Hopkins 来源说明或 finding-list 页。"
            ),
            wrapped_bullet(
                "打开 `04_inscription-crosswalk-route-index.csv`，写明哪条"
                "英粹、CUL、Chalfant 或合集路线引用该标签。"
            ),
            wrapped_bullet(
                "打开后出书目笔记，记录其重复、缩小、反对还是改称该来源分类。"
            ),
            wrapped_bullet(
                "打开 `08_topic-literature-context-dossier.md`，写明研究使用前"
                "需要比较的替代标签。"
            ),
        ]
    )
    return f"""# Topic Citation And Dispute Review Dossier / 主题引用与争议复核档案
Topic candidate ID: `{project_id}`

English:
{intro_en}

简体中文：
{intro_zh}

## Citation Relationship Checks / 引用关系核查

| field | value |
| --- | --- |
| source id | {SOURCE_ID} |
| download id | {DOWNLOAD_ID} |
| source summary row | {row["summary_row_id"]} |
| source group | {row["group_number"]} |
| source label en | {row["group_label_en"]} |
| source label zh | {row["group_label_zh"]} |

## Proposer And Classification Trail / 提出者与分类链
| field | value |
| --- | --- |
| proposer or classifier | Cambridge/Hopkins source table |
| current evidence level | metadata and route evidence only |
| bibliography route | 待查: open Cambridge/Hopkins finding-list source summary row |
| classification route | 待查: check 04_inscription-crosswalk-route-index.csv rows |
| review status | needs_human_topic_review |

## Disagreements And Alternate Labels / 不同意见与替代标签
| field | value |
| --- | --- |
| different opinions | 待查: review Cambridge/Hopkins label against scholarship notes |
| alternate labels | 待查: compare 02_topic-source-index.csv with bibliography labels |
| applicability risk | label may overstate a source classification |
| claim status | no grammar or inscription-topic claim |

## Crosswalk Citation Sample / 互证引用样例

| crosswalk id | period | Yingguo route | Chalfant route |
| --- | --- | --- | --- |
{route_lines}

## Specific Next Source Checks / 具体下一步来源核查
{questions}

## Review Boundary / 复核边界

- citation and dispute routes only
- not a grammar conclusion
- not an inscription-topic assignment
- not a transcription
- not a reading
- not a decipherment conclusion
"""

def topic_citation_dispute_review_index_payload(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "topic_candidate_id": project_id,
        "record_type": "research_topic_citation_dispute_review_index",
        "human_readable_files": [
            "README.md",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "04_inscription-crosswalk-route-index.csv",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
        ],
        "source_evidence_files": [
            CLASSIFIED_SUMMARY.as_posix(),
            CROSSWALK_STAGING.as_posix(),
            "02_topic-source-index.csv",
            "04_inscription-crosswalk-route-index.csv",
        ],
        "source_group_number": row["group_number"],
        "linked_crosswalk_candidate_count": len(routes),
        "review_questions": [
            "which source note or finding-list page first states this label",
            "which crosswalk rows cite the label through catalog routes",
            "which later publication repeats narrows rejects or renames it",
            "which alternate labels must be compared before research use",
        ],
        "claim_boundary": (
            "citation_and_dispute_routes_only_not_topic_or_decipherment_claim"
        ),
        "review_status": "needs_human_topic_review",
        "updated_at": UPDATED_AT,
    }


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
        (output_dir / "README.md").write_text(
            readme_text(project_id, row, len(routes)), encoding="utf-8", newline="\n"
        )
        (output_dir / "05_human-topic-review-sheet.md").write_text(
            review_sheet_text(project_id, row), encoding="utf-8", newline="\n"
        )
        (output_dir / "06_human-topic-dossier.md").write_text(
            topic_dossier_text(project_id, row, routes), encoding="utf-8", newline="\n"
        )
        write_json(
            output_dir / "07_topic-dossier-index.json",
            topic_dossier_index_payload(project_id, row, routes),
        )
        (output_dir / "08_topic-literature-context-dossier.md").write_text(
            topic_literature_context_dossier_text(project_id, row, routes),
            encoding="utf-8",
            newline="\n",
        )
        write_json(
            output_dir / "09_topic-literature-context-index.json",
            topic_literature_context_index_payload(project_id, row, routes),
        )
        (output_dir / "10_topic-citation-dispute-review-dossier.md").write_text(
            topic_citation_dispute_review_dossier_text(project_id, row, routes),
            encoding="utf-8",
            newline="\n",
        )
        write_json(
            output_dir / "11_topic-citation-dispute-review-index.json",
            topic_citation_dispute_review_index_payload(project_id, row, routes),
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
