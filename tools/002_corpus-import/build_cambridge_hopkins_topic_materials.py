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
        "instructions, source routes, period-count metadata, and crosswalk "
        "routes are the primary review materials. Structured support files "
        "only serve the human topic dossier, source tracing, comparison, and "
        "review."
    )
    chinese_intro = wrapped_paragraph(
        "本目录是 Cambridge/Hopkins 分类表主题候选的对象内入口。人类可读"
        "说明、复核说明、来源路线、分期计数和卜辞互证路线是主体复核"
        "资料。结构化辅助文件只服务人类主题档案、来源追溯、比较和复核。"
    )
    human_research_slots = "\n".join(
        [
            "## Human Research Slots / 人类研究槽位",
            "",
            wrapped_bullet(
                "Glyph and image: no glyph image, rubbing, or photograph is "
                "assigned here; check linked inscription and plate evidence "
                "before any graphic comparison."
            ),
            wrapped_bullet(
                "Inscription and catalog: compare full inscription text, OCR, "
                "plate number, catalog wording, and Heji or OBM references "
                "before any topic claim."
            ),
            wrapped_bullet(
                "Components and variants: no component, variant, near-form, "
                "bronze, seal, modern-character, or relation claim is accepted "
                "without source-backed comparison."
            ),
            wrapped_bullet(
                "Scholarship and dispute: record bibliography, proposer, "
                "disagreement, and dispute only when collected from reviewed "
                "sources."
            ),
            wrapped_bullet(
                "Provenance and period: treat collection, findspot, period, "
                "group, and batch fields as source clues pending human review."
            ),
            "- 字形和图像：本目录不指定字形图片、拓片或照片；需先核对卜辞和图版证据。",
            "- 卜辞和著录：正式归类前，应比较全文、OCR、图版号、著录文字和合集线索。",
            "- 构件和关系：构件、异体、近形、金文、小篆、今字和关系均只是待查槽位。",
            "- 文献和争议：只有来源已收集时，才记录书目、提出者、不同意见和争议。",
            "- 出处和时期：馆藏、出土地、时期、组类和批次都按来源线索待人工复核。",
        ]
    )
    file_entries = "\n".join(
        [
            wrapped_bullet(
                "`01_topic-candidate-packet.json`: structured candidate "
                "support packet."
            ),
            wrapped_bullet("`02_topic-source-index.csv`: source and provenance route."),
            wrapped_bullet("`03_period-count-index.csv`: period-count metadata."),
            wrapped_bullet(
                "`04_inscription-crosswalk-route-index.csv`: inscription "
                "crosswalk route rows."
            ),
            wrapped_bullet("`05_human-topic-review-sheet.md`: human checklist."),
            wrapped_bullet("`06_human-topic-dossier.md`: human topic dossier."),
            wrapped_bullet(
                "`07_topic-dossier-index.json`: structured dossier support index."
            ),
            wrapped_bullet(
                "`08_topic-literature-context-dossier.md`: literature/context "
                "dossier."
            ),
            wrapped_bullet(
                "`09_topic-literature-context-index.json`: structured context index."
            ),
            wrapped_bullet(
                "`10_topic-citation-dispute-review-dossier.md`: citation and "
                "dispute review."
            ),
            wrapped_bullet(
                "`11_topic-citation-dispute-review-index.json`: structured "
                "citation support index."
            ),
            wrapped_bullet(
                "`12_topic-research-use-boundary-review.md`: human review of "
                "research-use limits, promotion blockers, and claim boundaries."
            ),
            wrapped_bullet(
                "`13_topic-research-use-boundary-index.json`: structured "
                "support for the research-use boundary review."
            ),
            wrapped_bullet(
                "`14_topic-research-readiness-review.md`: human readiness "
                "review before formal topic or grammar research."
            ),
            wrapped_bullet(
                "`15_topic-research-readiness-index.json`: structured "
                "support for the readiness review."
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

{human_research_slots}

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
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
            "13_topic-research-use-boundary-index.json",
            "15_topic-research-readiness-index.json",
        ],
        "source_route_files": [
            CLASSIFIED_SUMMARY.as_posix(),
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
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
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
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
            "13_topic-research-use-boundary-index.json",
            "15_topic-research-readiness-index.json",
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
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "04_inscription-crosswalk-route-index.csv",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
            "13_topic-research-use-boundary-index.json",
            "15_topic-research-readiness-index.json",
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


def topic_research_use_boundary_review_text(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> str:
    route_sample = routes[:6]
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
        "This review tells a human researcher what this topic candidate can "
        "support before formal research begins, what evidence must be opened "
        "first, and which claims remain blocked."
    )
    intro_zh = wrapped_paragraph(
        "本复核页说明正式研究开始前，这个主题候选可以支持哪些准备工作、"
        "必须先打开哪些证据，以及哪些结论仍被阻止。"
    )
    allowed_use = "\n".join(
        [
            wrapped_bullet(
                "Use it as a source-classification route for locating "
                "Cambridge/Hopkins rows and linked inscription crosswalks."
            ),
            wrapped_bullet(
                "Use it to plan bibliography, citation, alternate-label, and "
                "disagreement checks."
            ),
            wrapped_bullet(
                "Use period counts only as source-table counts that need "
                "comparison against inscription examples."
            ),
            wrapped_bullet(
                "可把它用作查找 Cambridge/Hopkins 行和相关卜辞互证的来源分类路线。"
            ),
            wrapped_bullet(
                "可用它安排书目、引用关系、替代标签和不同意见的复核。"
            ),
            wrapped_bullet(
                "分期计数只可作为来源表计数，必须再与卜辞实例互相核对。"
            ),
        ]
    )
    blocked_claims = "\n".join(
        [
            wrapped_bullet("Do not treat the label as an accepted topic assignment."),
            wrapped_bullet("Do not treat the row as a grammar analysis."),
            wrapped_bullet("Do not treat the route as a transcription or reading."),
            wrapped_bullet("Do not treat period counts as dating conclusions."),
            wrapped_bullet("Do not treat this as a decipherment conclusion."),
            wrapped_bullet("不得把该标签当作已接受的主题归属。"),
            wrapped_bullet("不得把该行当作语法分析。"),
            wrapped_bullet("不得把该路线当作释文或读法。"),
            wrapped_bullet("不得把分期计数当作断代结论。"),
            wrapped_bullet("这不是释读结论。"),
        ]
    )
    questions = "\n".join(
        [
            wrapped_bullet(
                "Which bibliography note or source page first states this label?"
            ),
            wrapped_bullet(
                "Which linked inscription should be opened before the label is used?"
            ),
            wrapped_bullet(
                "Which alternate label or disagreement could change the scope?"
            ),
            wrapped_bullet(
                "Which evidence is missing before any topic, grammar, or date claim?"
            ),
            wrapped_bullet("哪条书目说明或来源页面最先记录这个标签？"),
            wrapped_bullet("使用该标签前，应该先打开哪条相关卜辞？"),
            wrapped_bullet("哪条替代标签或不同意见可能改变适用范围？"),
            wrapped_bullet("提出主题、语法或断代判断前，还缺哪项证据？"),
        ]
    )
    return f"""# Topic Research Use Boundary Review / 主题研究使用边界复核
Topic candidate ID: `{project_id}`

English:
{intro_en}

简体中文：
{intro_zh}

## Candidate Label And Source Scope / 候选标签与来源范围

| field | value |
| --- | --- |
| source id | {SOURCE_ID} |
| download id | {DOWNLOAD_ID} |
| source summary row | {row["summary_row_id"]} |
| source group | {row["group_number"]} |
| source label en | {row["group_label_en"]} |
| source label zh | {row["group_label_zh"]} |
| linked crosswalk routes | {len(routes)} |

## Evidence To Open First / 必须先打开的证据

| evidence route | review purpose |
| --- | --- |
| 02_topic-source-index.csv | source row, rights status, and group label |
| 03_period-count-index.csv | source-table counts only |
| 04_inscription-crosswalk-route-index.csv | linked inscription routes |
| 08_topic-literature-context-dossier.md | bibliography and scope gaps |
| 10_topic-citation-dispute-review-dossier.md | citation and dispute gaps |

## Sample Inscription Routes / 卜辞路线样例

| crosswalk id | period | Yingguo route | Heji route |
| --- | --- | --- | --- |
{route_lines}

## Allowed Pre-Research Use / 允许的研究前用途

{allowed_use}

## Blocked Claims / 仍被阻止的结论

{blocked_claims}

## Concrete Promotion Blockers / 具体提升阻碍

{questions}

## Review Boundary / 复核边界

- research-use boundary only
- not a grammar conclusion
- not an accepted topic assignment
- not a transcription
- not a reading
- not a dating conclusion
- not a decipherment conclusion
"""


def topic_research_use_boundary_index_payload(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "topic_candidate_id": project_id,
        "record_type": "research_topic_use_boundary_index",
        "human_readable_files": [
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "04_inscription-crosswalk-route-index.csv",
            "13_topic-research-use-boundary-index.json",
            "15_topic-research-readiness-index.json",
        ],
        "boundary_slots": {
            "allowed_use": [
                "source_classification_route",
                "bibliography_review_planning",
                "inscription_crosswalk_review_queue",
                "source_count_comparison",
            ],
            "blocked_claims": [
                "accepted_topic_assignment",
                "grammar_analysis",
                "transcription",
                "reading",
                "dating_conclusion",
                "decipherment_conclusion",
            ],
            "promotion_blockers": [
                "bibliography_note_or_source_page",
                "linked_inscription_context",
                "alternate_label_or_disagreement",
                "topic_grammar_or_date_evidence",
            ],
        },
        "linked_crosswalk_candidate_count": len(routes),
        "claim_boundary": (
            "research_use_boundary_only_not_topic_grammar_reading_dating_or_"
            "decipherment_claim"
        ),
        "review_status": "needs_human_topic_review",
        "updated_at": UPDATED_AT,
    }


def topic_research_readiness_review_text(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> str:
    intro_en = wrapped_paragraph(
        "This review is the last preprocessing gate for this topic candidate. "
        "It tells a human reader what to open before any formal topic, "
        "grammar, dating, reading, or decipherment research begins."
    )
    intro_zh_lines = [
        "本页是该主题候选进入正式研究前的最后资料整理复核。",
        "它只说明研究者应先打开哪些证据、还缺哪些核查。",
        "它不提出主题、语法、断代、释读或破译结论。",
    ]
    reading_order = "\n".join(
        [
            wrapped_bullet("Open `05_human-topic-review-sheet.md` for the first checks."),
            wrapped_bullet("Open `06_human-topic-dossier.md` for the source label scope."),
            wrapped_bullet(
                "Open `08_topic-literature-context-dossier.md` for bibliography "
                "and inscription context."
            ),
            wrapped_bullet(
                "Open `10_topic-citation-dispute-review-dossier.md` for citation, "
                "proposer, and dispute routes."
            ),
            wrapped_bullet(
                "Open `12_topic-research-use-boundary-review.md` for blocked "
                "claims and promotion limits."
            ),
            "- 先读 `05_human-topic-review-sheet.md`，核对最基本检查项。",
            "- 再读 `06_human-topic-dossier.md`，确认来源标签范围。",
            "- 再读 `08_topic-literature-context-dossier.md`，查书目和卜辞语境。",
            "- 再读 `10_topic-citation-dispute-review-dossier.md`，查引用和争议。",
            "- 最后读 `12_topic-research-use-boundary-review.md`，确认禁止结论。",
        ]
    )
    readiness_slots = "\n".join(
        [
            wrapped_bullet(
                "source_classification_route: Cambridge/Hopkins group row is "
                "recorded as a source route only."
            ),
            wrapped_bullet(
                "bibliography_and_source_page: the first source note or page "
                "still needs human confirmation."
            ),
            wrapped_bullet(
                "linked_inscription_context: linked crosswalk rows must be "
                "opened before any topic use."
            ),
            wrapped_bullet(
                "evidence_level: current evidence is metadata and route "
                "evidence only."
            ),
            wrapped_bullet(
                "citation_and_dispute_record: proposer, alternate labels, and "
                "different opinions remain review items."
            ),
            wrapped_bullet(
                "research_use_boundary: allowed use is preprocessing and "
                "source comparison only."
            ),
            wrapped_bullet(
                "source_rights_manifest: source, download, rights status, and "
                "risk note stay visible in local files."
            ),
            wrapped_bullet(
                "formal_topic_research_blockers: missing bibliography, "
                "inscription context, or disputes block formal research."
            ),
            wrapped_bullet(
                "glyph image route: no glyph image, rubbing, or photo is "
                "claimed here; open linked inscription evidence first."
            ),
            wrapped_bullet(
                "component route: no component analysis is claimed here; "
                "compare component clues only after source review."
            ),
            wrapped_bullet(
                "variant and relation route: variant, near-form, bronze, seal, "
                "modern-character, and relation checks remain pending."
            ),
            "- 来源分类路线：Cambridge/Hopkins 分组行只作为来源线索。",
            "- 书目和来源页：最早出处说明仍需人工打开确认。",
            "- 关联卜辞语境：使用主题前必须先看互证路线。",
            "- 证据等级：当前只到 metadata 和路线证据。",
            "- 引用和争议：提出者、异名和不同意见仍待复核。",
            "- 使用边界：只能用于预处理、查找和来源比较。",
            "- 来源权利：source、download、rights 和 risk note 必须可见。",
            "- 正式研究阻塞项：书目、卜辞语境或争议缺口会阻塞研究。",
            "- 字形图像路线：本页不确认 glyph image、拓片或照片。",
            "- 构件路线：本页不做 component 分析，只标出待核查线索。",
            "- 关系路线：variant、近形、金文、小篆和今字关系仍待查。",
        ]
    )
    questions = "\n".join(
        [
            wrapped_bullet(
                "Which source note, page, or finding-list row first supports "
                "this topic label?"
            ),
            wrapped_bullet(
                "Which linked inscription route must be opened before the label "
                "is cited?"
            ),
            wrapped_bullet(
                "Which proposer, alternate label, or disagreement is still "
                "missing?"
            ),
            wrapped_bullet(
                "Which issue blocks formal topic or grammar research?"
            ),
            "- 哪条来源说明、页码或 finding-list 行最先支持该标签？",
            "- 引用该标签前，应先打开哪条关联卜辞路线？",
            "- 哪个提出者、异名或不同意见仍缺来源？",
            "- 哪个问题仍阻塞正式主题或语法研究？",
        ]
    )
    source_status = wrapped_paragraph(
        "Source and rights evidence remains in `02_topic-source-index.csv`, "
        "`03_period-count-index.csv`, `04_inscription-crosswalk-route-index.csv`, "
        "and the Cambridge/Hopkins classified-summary register."
    )
    return f"""# Topic Research Readiness Review / 主题研究就绪复核
Topic candidate ID: `{project_id}`

English:
{intro_en}

简体中文：
{chr(10).join(intro_zh_lines)}

## Candidate And Source Status / 候选项与来源状态

| field | value |
| --- | --- |
| source id | {SOURCE_ID} |
| download id | {DOWNLOAD_ID} |
| source summary row | {row["summary_row_id"]} |
| source group | {row["group_number"]} |
| source label en | {row["group_label_en"]} |
| source label zh | {row["group_label_zh"]} |
| linked crosswalk routes | {len(routes)} |

English:
{source_status}

简体中文：
来源、下载、权利和风险线索仍在本目录索引和总登记中复核。

## Human Reading Order / 人工阅读顺序
{reading_order}

## Readiness Slots / 就绪复核项
{readiness_slots}

## Concrete Questions Before Formal Research / 正式研究前的具体问题
{questions}

## Review Boundary / 复核边界

- preprocessing readiness only
- not a grammar conclusion
- not an accepted topic assignment
- not a transcription
- not a reading
- not a dating conclusion
- not a decipherment conclusion
"""


def topic_research_readiness_index_payload(
    project_id: str,
    row: dict[str, str],
    routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "topic_candidate_id": project_id,
        "record_type": "research_topic_readiness_index",
        "human_entry": "14_topic-research-readiness-review.md",
        "human_readable_files": [
            "05_human-topic-review-sheet.md",
            "06_human-topic-dossier.md",
            "08_topic-literature-context-dossier.md",
            "10_topic-citation-dispute-review-dossier.md",
            "12_topic-research-use-boundary-review.md",
            "14_topic-research-readiness-review.md",
        ],
        "ai_support_files": [
            "01_topic-candidate-packet.json",
            "02_topic-source-index.csv",
            "03_period-count-index.csv",
            "04_inscription-crosswalk-route-index.csv",
            "07_topic-dossier-index.json",
            "09_topic-literature-context-index.json",
            "11_topic-citation-dispute-review-index.json",
            "13_topic-research-use-boundary-index.json",
            "15_topic-research-readiness-index.json",
        ],
        "source_evidence_files": [
            CLASSIFIED_SUMMARY.as_posix(),
            CROSSWALK_STAGING.as_posix(),
            "02_topic-source-index.csv",
            "04_inscription-crosswalk-route-index.csv",
        ],
        "readiness_slots": [
            "source_classification_route",
            "bibliography_and_source_page",
            "linked_inscription_context",
            "evidence_level",
            "citation_and_dispute_record",
            "research_use_boundary",
            "source_rights_manifest",
            "formal_topic_research_blockers",
        ],
        "formal_research_blockers": [
            "missing_confirmed_bibliography_or_source_page",
            "linked_inscription_context_not_opened",
            "proposer_alternate_label_or_dispute_not_reviewed",
            "topic_grammar_reading_or_dating_claim_still_blocked",
        ],
        "linked_crosswalk_candidate_count": len(routes),
        "claim_boundary": [
            "no grammar conclusion",
            "no accepted topic assignment",
            "no transcription",
            "no reading",
            "no dating conclusion",
            "no decipherment conclusion",
        ],
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
        (output_dir / "12_topic-research-use-boundary-review.md").write_text(
            topic_research_use_boundary_review_text(project_id, row, routes),
            encoding="utf-8",
            newline="\n",
        )
        write_json(
            output_dir / "13_topic-research-use-boundary-index.json",
            topic_research_use_boundary_index_payload(project_id, row, routes),
        )
        (output_dir / "14_topic-research-readiness-review.md").write_text(
            topic_research_readiness_review_text(project_id, row, routes),
            encoding="utf-8",
            newline="\n",
        )
        write_json(
            output_dir / "15_topic-research-readiness-index.json",
            topic_research_readiness_index_payload(project_id, row, routes),
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
