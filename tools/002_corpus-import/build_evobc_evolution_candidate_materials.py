#!/usr/bin/env python3
"""Build object-local materials for EVOBC evolution-category candidates.

These outputs are preprocessing infrastructure only. Each object preserves
dataset metadata for later review; it is not a formal paleographic
correspondence or evolution-chain conclusion.
"""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from pathlib import Path


CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
CODEBOOK_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "002_evobc-era-source-codebook-staging.csv"
)
EVOLUTION_GRAPH = Path("corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl")
EVOLUTION_ROOT = Path("corpus/004_bronze-seal-modern-correspondences")
EVOLUTION_ID_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "005_evolution-candidate-id-source-map.csv"
)

UPDATED_AT = "2026-06-20"
MAX_HUMAN_LINE_LENGTH = 80
BUCKET_SIZE = 100
SOURCE_ID = "src-evobc"
RECORD_TYPE = "evolution_correspondence_candidate"
REVIEW_STATUS = "needs_human_evolution_review"
OBJECT_STATUS = "dataset_candidate_not_promoted"
RIGHTS_STATUS = "source_marked_risk_noted"
RESEARCH_BOUNDARY = (
    "evobc_evolution_category_candidate_only_not_formal_correspondence_not_evolution_chain"
)
CAUTION = (
    "EVOBC category and image-reference metadata is useful for routing cross-period "
    "review, but this object is not an accepted paleographic correspondence, not an "
    "evolution-chain conclusion, not a modern-character identification, and not a "
    "decipherment conclusion."
)

MAP_FIELDS = [
    "project_id",
    "record_type",
    "canonical_path",
    "primary_external_ref_id",
    "all_external_ref_ids",
    "source_ids",
    "rights_status",
    "review_status",
    "updated_at",
]

SOURCE_INDEX_FIELDS = [
    "source_index_id",
    "project_id",
    "candidate_evolution_category_id",
    "source_id",
    "evidence_download_id",
    "source_file_path",
    "source_row_id",
    "source_category_id",
    "rights_status",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

CODE_INDEX_FIELDS = [
    "code_index_id",
    "project_id",
    "candidate_evolution_category_id",
    "codebook_row_id",
    "code_type",
    "code_value",
    "observed_token",
    "label_en",
    "label_zh",
    "category_image_reference_count",
    "code_image_reference_count",
    "reference_basis",
    "review_status",
    "caution",
    "updated_at",
]

IMAGE_ROUTE_FIELDS = [
    "image_route_id",
    "project_id",
    "candidate_evolution_category_id",
    "route_type",
    "route_label",
    "source_id",
    "evidence_download_id",
    "route_file_path",
    "route_record_ref",
    "image_reference_count",
    "local_image_status",
    "rights_status",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

MANIFEST_FIELDS = [
    "project_id",
    "record_type",
    "candidate_directory",
    "packet_path",
    "source_index_path",
    "code_index_path",
    "image_reference_route_index_path",
    "image_reference_route_gallery_path",
    "human_review_sheet_path",
    "source_character_label",
    "source_character_codepoints",
    "image_reference_count",
    "review_status",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_counts(value: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not value:
        return counts
    for part in value.split(";"):
        if not part:
            continue
        key, raw_count = part.rsplit(":", 1)
        counts[key] = int(raw_count)
    return counts


def project_id(index: int) -> str:
    return f"obs-evo-cand-{index:06d}"


def primary_external_ref(row: dict[str, str]) -> str:
    return f"evobc-cat-{row['source_category_id']}"


def bucket_dir(index: int) -> Path:
    bucket_index = (index - 1) // BUCKET_SIZE + 1
    start = (bucket_index - 1) * BUCKET_SIZE + 1
    end = min(bucket_index * BUCKET_SIZE, 13714)
    return EVOLUTION_ROOT / (
        f"{bucket_index:03d}_{start:06d}-{end:06d}_"
        "obs-evo-cand-bucket_evolution-candidates"
    )


def object_dir(index: int, row: dict[str, str]) -> Path:
    return bucket_dir(index) / (
        f"{index:03d}_{project_id(index)}_{primary_external_ref(row)}_evolution-candidate"
    )


def codebook_lookup(codebook_rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["code_type"], row["code_value"]): row
        for row in codebook_rows
    }


def code_index_rows(
    index: int,
    row: dict[str, str],
    codebook: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    category_id = row["candidate_evolution_category_id"]
    for code_type, source_field in [
        ("era", "era_code_counts"),
        ("source", "source_code_counts"),
    ]:
        for code_value, count in parse_counts(row[source_field]).items():
            codebook_row = codebook[(code_type, code_value)]
            rows.append(
                {
                    "code_index_id": f"{project_id(index)}-{code_type}-{int(code_value):02d}",
                    "project_id": project_id(index),
                    "candidate_evolution_category_id": category_id,
                    "codebook_row_id": codebook_row["codebook_row_id"],
                    "code_type": code_type,
                    "code_value": code_value,
                    "observed_token": codebook_row["observed_token"],
                    "label_en": codebook_row["label_en"],
                    "label_zh": codebook_row["label_zh"],
                    "category_image_reference_count": row["image_reference_count"],
                    "code_image_reference_count": str(count),
                    "reference_basis": codebook_row["reference_basis"],
                    "review_status": codebook_row["review_status"],
                    "caution": codebook_row["caution"],
                    "updated_at": UPDATED_AT,
                }
            )
    return rows


def source_index_rows(index: int, row: dict[str, str]) -> list[dict[str, str]]:
    candidate_id = row["candidate_evolution_category_id"]
    return [
        {
            "source_index_id": f"{project_id(index)}-source-key-value",
            "project_id": project_id(index),
            "candidate_evolution_category_id": candidate_id,
            "source_id": SOURCE_ID,
            "evidence_download_id": row["evidence_download_id_key_value"],
            "source_file_path": CATEGORY_STAGING.as_posix(),
            "source_row_id": str(index),
            "source_category_id": row["source_category_id"],
            "rights_status": row["rights_status"],
            "review_status": row["review_status"],
            "research_boundary": RESEARCH_BOUNDARY,
            "caution": CAUTION,
            "updated_at": UPDATED_AT,
        },
        {
            "source_index_id": f"{project_id(index)}-source-list",
            "project_id": project_id(index),
            "candidate_evolution_category_id": candidate_id,
            "source_id": SOURCE_ID,
            "evidence_download_id": row["evidence_download_id_list"],
            "source_file_path": CATEGORY_STAGING.as_posix(),
            "source_row_id": str(index),
            "source_category_id": row["source_category_id"],
            "rights_status": row["rights_status"],
            "review_status": row["review_status"],
            "research_boundary": RESEARCH_BOUNDARY,
            "caution": CAUTION,
            "updated_at": UPDATED_AT,
        },
    ]


def route_files(directory: Path) -> list[str]:
    return [
        CATEGORY_STAGING.as_posix(),
        CODEBOOK_STAGING.as_posix(),
        EVOLUTION_GRAPH.as_posix(),
        (directory / "02_evolution-source-index.csv").as_posix(),
        (directory / "03_era-source-code-index.csv").as_posix(),
        (directory / "04_human-review-sheet.md").as_posix(),
        (directory / "05_image-reference-route-index.csv").as_posix(),
        (directory / "06_image-reference-route-gallery.md").as_posix(),
    ]


def wrapped_paragraph(text: str) -> str:
    return textwrap.fill(
        text,
        width=MAX_HUMAN_LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrapped_bullet(text: str) -> list[str]:
    return textwrap.wrap(
        f"- {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def bullet_block(items: list[str]) -> str:
    return "\n".join(line for item in items for line in wrapped_bullet(item))


def code_rows_block(code_rows: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for code in code_rows:
        lines.extend(wrapped_bullet(f"{code['code_type']} `{code['code_value']}`"))
        lines.extend(
            textwrap.wrap(
                f"  token: `{code['observed_token']}`",
                width=MAX_HUMAN_LINE_LENGTH,
                subsequent_indent="  ",
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
        lines.extend(
            textwrap.wrap(
                f"  image references: {code['code_image_reference_count']}",
                width=MAX_HUMAN_LINE_LENGTH,
                subsequent_indent="  ",
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return "\n".join(lines)


def route_cards_block(image_routes: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for route in image_routes:
        lines.extend(wrapped_bullet(f"`{route['image_route_id']}`"))
        for label, key in [
            ("type", "route_type"),
            ("label", "route_label"),
            ("route file", "route_file_path"),
            ("status", "local_image_status"),
        ]:
            value = Path(route[key]).name if key == "route_file_path" else route[key]
            lines.extend(
                textwrap.wrap(
                    f"  {label}: `{value}`",
                    width=MAX_HUMAN_LINE_LENGTH,
                    subsequent_indent="  ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
    return "\n".join(lines)


def image_route_rows(index: int, row: dict[str, str], code_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    pid = project_id(index)
    category_id = row["candidate_evolution_category_id"]
    routes = [
        {
            "image_route_id": f"{pid}-route-category-staging",
            "route_type": "category_metadata_staging",
            "route_label": "EVOBC category row with aggregate image-reference counts",
            "evidence_download_id": row["evidence_download_id_key_value"],
            "route_file_path": CATEGORY_STAGING.as_posix(),
            "route_record_ref": category_id,
            "image_reference_count": row["image_reference_count"],
        },
        {
            "image_route_id": f"{pid}-route-list-staging",
            "route_type": "list_metadata_staging",
            "route_label": "EVOBC list rows summarized into era/source counts",
            "evidence_download_id": row["evidence_download_id_list"],
            "route_file_path": CATEGORY_STAGING.as_posix(),
            "route_record_ref": row["source_category_id"],
            "image_reference_count": row["image_reference_count"],
        },
        {
            "image_route_id": f"{pid}-route-code-index",
            "route_type": "object_local_code_index",
            "route_label": "Object-local era/source code index for locating review buckets",
            "evidence_download_id": row["evidence_download_id_list"],
            "route_file_path": "03_era-source-code-index.csv",
            "route_record_ref": ";".join(code_row["code_index_id"] for code_row in code_rows),
            "image_reference_count": row["image_reference_count"],
        },
        {
            "image_route_id": f"{pid}-route-evolution-graph",
            "route_type": "graph_edge_route",
            "route_label": "EVOBC relationship graph edges that reference this category",
            "evidence_download_id": row["evidence_download_id_list"],
            "route_file_path": EVOLUTION_GRAPH.as_posix(),
            "route_record_ref": category_id,
            "image_reference_count": row["image_reference_count"],
        },
    ]
    shared = {
        "project_id": pid,
        "candidate_evolution_category_id": category_id,
        "source_id": SOURCE_ID,
        "local_image_status": "not_collected_route_indexed",
        "rights_status": RIGHTS_STATUS,
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }
    return [{**shared, **route} for route in routes]


def packet_payload(
    index: int,
    row: dict[str, str],
    directory: Path,
    code_rows: list[dict[str, str]],
    image_routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": RECORD_TYPE,
        "candidate_evolution_category_id": row["candidate_evolution_category_id"],
        "primary_external_ref_id": primary_external_ref(row),
        "source_id": SOURCE_ID,
        "source_category_id": row["source_category_id"],
        "source_character_label": row["source_character_label"],
        "source_character_codepoints": row["source_character_codepoints"],
        "image_reference_count": int(row["image_reference_count"]),
        "era_code_counts": parse_counts(row["era_code_counts"]),
        "era_token_counts": row["era_token_counts"],
        "source_code_counts": parse_counts(row["source_code_counts"]),
        "source_token_counts": row["source_token_counts"],
        "script_stage_flags": {
            "has_oracle_bone_refs": row["has_oracle_bone_refs"] == "true",
            "has_bronze_refs": row["has_bronze_refs"] == "true",
            "has_seal_refs": row["has_seal_refs"] == "true",
            "has_spring_autumn_refs": row["has_spring_autumn_refs"] == "true",
            "has_warring_states_refs": row["has_warring_states_refs"] == "true",
            "has_clerical_refs": row["has_clerical_refs"] == "true",
        },
        "code_index": code_rows,
        "image_reference_routes": image_routes,
        "local_image_status": "not_collected_route_indexed",
        "route_files": route_files(directory),
        "formal_correspondence_status": "not_formal_correspondence",
        "evolution_chain_claim_status": "no_claim",
        "modern_character_identity_status": "not_confirmed",
        "project_import_status": OBJECT_STATUS,
        "rights_status": RIGHTS_STATUS,
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def readme_text(index: int, row: dict[str, str], code_rows: list[dict[str, str]]) -> str:
    intro_en = wrapped_paragraph(
        "This directory is the object-local research entrance for one EVOBC "
        "category. Human-readable notes and AI-readable indexes are stored in "
        "this same concrete corpus object directory."
    )
    intro_zh = wrapped_paragraph(
        "本目录是一个 EVOBC 字形演化类别候选对象的本地研究入口。"
        "人类可读说明、人工复核表和 AI 可读索引放在同一对象目录内。"
    )
    boundary_lines = bullet_block(
        [
            "This is not an accepted paleographic correspondence.",
            "This is not an evolution-chain conclusion.",
            "This is not a confirmed modern-character identity.",
            "This is not a decipherment conclusion.",
            "本对象只是演化或对应候选路线，不是正式古文字对应结论。",
            "本对象不确认演化链、现代字身份或释读结论。",
        ]
    )
    local_file_lines = bullet_block(
        [
            "`01_candidate-evolution-packet.json`: AI-readable candidate packet.",
            "`02_evolution-source-index.csv`: source, download, rights, and route index.",
            "`03_era-source-code-index.csv`: observed era/source code rows.",
            "`04_human-review-sheet.md`: human source-chain review sheet.",
            "`05_image-reference-route-index.csv`: object-local image route index.",
            "`06_image-reference-route-gallery.md`: visual-evidence route gallery.",
        ]
    )
    metadata_lines = bullet_block(
        [
            f"Project ID: `{project_id(index)}`",
            f"EVOBC category candidate ID: `{row['candidate_evolution_category_id']}`",
            f"External category ref: `{primary_external_ref(row)}`",
            f"Source label: `{row['source_character_label']}`",
            f"Source codepoints: `{row['source_character_codepoints']}`",
            f"Image reference count: `{row['image_reference_count']}`",
            f"Era token counts: `{row['era_token_counts']}`",
            f"Source token counts: `{row['source_token_counts']}`",
        ]
    )
    question_lines = bullet_block(
        [
            "Which EVOBC image-reference route should be opened first?",
            "Which source/download/checksum rows prove this candidate route?",
            "Which era or source code labels are only dataset metadata?",
            "Which bronze, seal, or later-script route is only a dataset clue?",
            "Which oracle inscription, collection, or findspot context is missing?",
            "Which Xiaoxuetang, OBIMD, HUST-OBC, IHP, or museum source should be checked?",
            "What evidence is still missing before any formal correspondence claim?",
            "应先打开哪条 EVOBC 图像引用路线？",
            "哪些来源、下载记录或 checksum 行能证明这条候选路线？",
            "哪些时期码、来源码、金文、小篆或后世字形路线只是数据集线索？",
            "还缺哪些卜辞、馆藏、出土地、时期或著录上下文？",
            "正式对应结论前还缺哪些可复核证据？",
        ]
    )
    review_status = wrapped_paragraph(
        f"Current status: `{REVIEW_STATUS}`. Reviewers must compare this "
        "candidate against primary images, source-chain records, dictionaries, "
        "inscription context, and stronger provenance sources before any formal "
        "correspondence or evolution record is created."
    )
    return f"""# {project_id(index)} / EVOBC evolution-category candidate

English:
{intro_en}

Simplified Chinese:
{intro_zh}

## Boundary / 边界

{boundary_lines}

## Local Files / 本目录文件

{local_file_lines}

## Candidate Metadata / 候选 metadata

{metadata_lines}

## Observed Code Rows / 观察到的代码行

{code_rows_block(code_rows)}

## Concrete Questions To Check / 具体待查问题

{question_lines}

## Review Status / 复核状态
{review_status}
"""

    code_lines = "\n".join(
        f"- {code['code_type']} {code['code_value']} / {code['observed_token']}: "
        f"{code['code_image_reference_count']} image references"
        for code in code_rows
    )
    return f"""# {project_id(index)} / EVOBC evolution-category candidate

English:
This directory is the object-local research entrance for one EVOBC category. Human-readable notes and AI-readable indexes are stored in this same concrete `corpus/004_bronze-seal-modern-correspondences` object directory.

Simplified Chinese:
本目录是一个 EVOBC 字形演化类别候选对象的本地研究入口。人类可读说明、人工复核表和 AI 可读索引都放在同一个具体 `corpus/004_bronze-seal-modern-correspondences` 对象目录中，不另建并行的人类资料目录。

## Boundary / 边界

- This is not an accepted paleographic correspondence.
- This is not an evolution-chain conclusion.
- This is not a confirmed modern-character identity.
- This is not a decipherment conclusion.
- 本对象不是已确认的古文字对应关系，不是字形演化链结论，不是现代字身份确认，也不是释读结论。

## Local Files / 本目录文件

- `01_candidate-evolution-packet.json`: AI-readable candidate packet.
- `02_evolution-source-index.csv`: source, download, rights, and route index.
- `03_era-source-code-index.csv`: era/source code rows observed for this category.
- `04_human-review-sheet.md`: human review sheet for source-chain, image, and cross-source checks.
- `05_image-reference-route-index.csv`: object-local image-reference route index for humans and AI agents.
- `06_image-reference-route-gallery.md`: object-local route gallery explaining where visual evidence still needs to be collected.

## Candidate Metadata / 候选 metadata

- Project ID: `{project_id(index)}`
- EVOBC category candidate ID: `{row['candidate_evolution_category_id']}`
- External category ref: `{primary_external_ref(row)}`
- Source label: `{row['source_character_label']}`
- Source codepoints: `{row['source_character_codepoints']}`
- Image reference count: `{row['image_reference_count']}`
- Era token counts: `{row['era_token_counts']}`
- Source token counts: `{row['source_token_counts']}`

## Observed Code Rows / 观察到的代码行

{code_lines}

## Review Status / 复核状态

Current status: `{REVIEW_STATUS}`. Reviewers must compare this candidate against primary images, source-chain records, oracle/bronze/seal dictionaries, inscription context, and stronger provenance sources before any formal correspondence or evolution record is created.
"""


def image_route_gallery_text(index: int, row: dict[str, str], image_routes: list[dict[str, str]]) -> str:
    intro_en = wrapped_paragraph(
        "This object has EVOBC image-reference metadata, but no local source "
        "image is collected here yet. The route cards below guide later visual "
        "evidence review inside the same object directory and registered "
        "source files."
    )
    intro_zh = wrapped_paragraph(
        "本对象保存 EVOBC 图像引用 metadata，目前尚未采集本地图像。"
        "下面条目只是证据路线卡，用来指导后续视觉证据复核。"
    )
    boundary_text = wrapped_paragraph(
        "These route cards are preprocessing infrastructure only. They are not "
        "accepted paleographic correspondences, not evolution-chain "
        "conclusions, not modern-character identity confirmations, and not "
        "decipherment conclusions."
    )
    question_lines = bullet_block(
        [
            "Which EVOBC image-reference route should be opened first?",
            "Which route file and source download record should prove it?",
            "Which bronze, seal, or later-script route is only a dataset clue?",
            "Which local image, rubbing, hand copy, or plate is still missing?",
            "Which oracle inscription, collection, or findspot context is missing?",
            "What evidence is still missing before any visual comparison?",
            "应先打开哪条 EVOBC 图像引用路线？",
            "哪一个路线文件和下载记录能够支撑它？",
            "哪些金文、小篆或后世字形路线只是数据集线索？",
            "还缺哪些本地图像、拓片、摹本或图版？",
            "视觉比较前还缺哪些可复核证据？",
        ]
    )
    return f"""# Image Reference Route Gallery / 图像引用路线图
Project ID: `{project_id(index)}`

EVOBC category candidate ID: `{row['candidate_evolution_category_id']}`

English:
{intro_en}

Simplified Chinese:
{intro_zh}

## Route Cards / 路线卡

{route_cards_block(image_routes)}

## Evidence Boundary / 证据边界

- Local image status: `not_collected_route_indexed`
- Formal correspondence: `not_formal_correspondence`
- Evolution-chain claim: `no_claim`
- Modern-character identity: `not_confirmed`
- Boundary marker: `not accepted paleographic correspondences`
- Boundary marker: `not evolution-chain conclusions`
- Review status: `{REVIEW_STATUS}`

{boundary_text}

## Concrete Questions To Check / 具体待查问题

{question_lines}
"""

    route_lines = "\n".join(
        "- `{image_route_id}` / `{route_type}`: {route_label}; route file `{route_file_path}`; status `{local_image_status}`.".format(**route)
        for route in image_routes
    )
    return f"""# Image Reference Route Gallery / 图像引用路线图

Project ID: `{project_id(index)}`

EVOBC category candidate ID: `{row['candidate_evolution_category_id']}`

English:
This object has EVOBC image-reference metadata, but no local source image is collected here yet. The entries below are route cards for finding and reviewing visual evidence inside this same object directory and its registered source files.

简体中文：
本对象保存的是 EVOBC 图像引用 metadata，当前尚未在此目录内采集本地图像。下面的条目只是证据路线卡，用来指导后续在同一对象目录和已登记来源文件中查找、复核视觉证据。

## Route Cards / 路线卡

{route_lines}

## Evidence Boundary / 证据边界

- Local image status: `not_collected_route_indexed`
- Formal correspondence: `not_formal_correspondence`
- Evolution-chain claim: `no_claim`
- Modern-character identity: `not_confirmed`
- Review status: `{REVIEW_STATUS}`

These route cards are preprocessing infrastructure only. They are not accepted paleographic correspondences, not evolution-chain conclusions, not modern-character identity confirmations, and not decipherment conclusions.
"""


def wrapped_bullet(text: str) -> list[str]:
    return textwrap.wrap(
        f"- {text}",
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def review_sheet_text(index: int, row: dict[str, str]) -> str:
    required_checks = [
        "Open `02_evolution-source-index.csv` and confirm the source, download, "
        "checksum, and rights-status trail.",
        "Open `03_era-source-code-index.csv`; treat era/source codes as dataset "
        "metadata only.",
        "Open `05_image-reference-route-index.csv` and "
        "`06_image-reference-route-gallery.md` before visual review.",
        "Locate or verify primary image references before using visual evidence.",
        "Compare Xiaoxuetang/OBM, OBIMD, HUST-OBC, IHP/museum records, and "
        "inscription context before promotion.",
        "Do not record a formal correspondence, evolution-chain conclusion, "
        "modern-character identity, or decipherment conclusion here.",
    ]
    concrete_questions = [
        "Which EVOBC image-reference route should be opened first?",
        "应先打开哪些 EVOBC 图像引用路线？",
        "Which source/download/checksum rows prove the route?",
        "哪些来源、下载或 checksum 行能证明路线？",
        "Which era or source code labels are only dataset metadata?",
        "哪些时代码或来源码只是数据集 metadata？",
        "Which bronze, seal, or later-script links are only candidates?",
        "哪些金文、小篆或后世字形路线只是候选？",
        "Which oracle inscription, collection, or findspot context is missing?",
        "还缺哪些卜辞、馆藏或出土地上下文？",
        "Which Xiaoxuetang, OBIMD, HUST-OBC, or museum source should be checked?",
        "下一步应核对小学堂、OBIMD、HUST-OBC 还是博物馆来源？",
        "What evidence is still missing before any formal correspondence claim?",
        "正式对应结论前还缺哪些证据？",
    ]
    required_lines = "\n".join(
        line
        for item in required_checks
        for line in wrapped_bullet(item)
    )
    question_lines = "\n".join(
        line
        for item in concrete_questions
        for line in wrapped_bullet(item)
    )
    caution_lines = textwrap.fill(
        CAUTION,
        width=MAX_HUMAN_LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return f"""# Human Review Sheet / 人工复核表

Project ID: `{project_id(index)}`

EVOBC category candidate ID: `{row['candidate_evolution_category_id']}`

## Required Checks / 必须复核

{required_lines}

## Concrete Questions To Check / 具体待查问题

{question_lines}

## Current Evidence Status / 当前证据状态

- Formal correspondence: `not_formal_correspondence`
- Evolution-chain claim: `no_claim`
- Modern-character identity: `not_confirmed`
- Source image evidence: `not_collected_route_indexed`
- Cross-source review: `needs_human_evolution_review`

## Caution / 风险提示

{caution_lines}
"""


def build_outputs(root: Path) -> dict[str, dict[str, object]]:
    category_rows = read_csv_rows(root / CATEGORY_STAGING)
    codebook = codebook_lookup(read_csv_rows(root / CODEBOOK_STAGING))
    outputs: dict[str, dict[str, object]] = {}
    for index, row in enumerate(category_rows, start=1):
        directory = object_dir(index, row)
        code_rows = code_index_rows(index, row, codebook)
        image_routes = image_route_rows(index, row, code_rows)
        pid = project_id(index)
        outputs[pid] = {
            "object_dir": root / directory,
            "relative_object_dir": directory,
            "readme_text": readme_text(index, row, code_rows),
            "packet": packet_payload(index, row, directory, code_rows, image_routes),
            "source_rows": source_index_rows(index, row),
            "code_rows": code_rows,
            "image_route_rows": image_routes,
            "image_route_gallery_text": image_route_gallery_text(index, row, image_routes),
            "review_sheet_text": review_sheet_text(index, row),
            "map_row": {
                "project_id": pid,
                "record_type": RECORD_TYPE,
                "canonical_path": directory.as_posix(),
                "primary_external_ref_id": primary_external_ref(row),
                "all_external_ref_ids": ";".join(
                    [
                        row["candidate_evolution_category_id"],
                        primary_external_ref(row),
                        row["source_category_id"],
                    ]
                ),
                "source_ids": SOURCE_ID,
                "rights_status": RIGHTS_STATUS,
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            },
        }
    return outputs


def write_bucket_manifests(root: Path, outputs: dict[str, dict[str, object]]) -> None:
    buckets: dict[Path, list[dict[str, str]]] = {}
    for pid, output in outputs.items():
        directory = output["relative_object_dir"]
        assert isinstance(directory, Path)
        packet = output["packet"]
        assert isinstance(packet, dict)
        buckets.setdefault(directory.parent, []).append(
            {
                "project_id": pid,
                "record_type": RECORD_TYPE,
                "candidate_directory": directory.as_posix(),
                "packet_path": (directory / "01_candidate-evolution-packet.json").as_posix(),
                "source_index_path": (directory / "02_evolution-source-index.csv").as_posix(),
                "code_index_path": (directory / "03_era-source-code-index.csv").as_posix(),
                "image_reference_route_index_path": (directory / "05_image-reference-route-index.csv").as_posix(),
                "image_reference_route_gallery_path": (directory / "06_image-reference-route-gallery.md").as_posix(),
                "human_review_sheet_path": (directory / "04_human-review-sheet.md").as_posix(),
                "source_character_label": str(packet["source_character_label"]),
                "source_character_codepoints": str(packet["source_character_codepoints"]),
                "image_reference_count": str(packet["image_reference_count"]),
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
    for bucket, rows in buckets.items():
        write_csv(root / bucket / "000_evobc-evolution-candidate-bucket-manifest.csv", rows, MANIFEST_FIELDS)


def write_outputs(root: Path, outputs: dict[str, dict[str, object]]) -> None:
    for output in outputs.values():
        directory = output["object_dir"]
        assert isinstance(directory, Path)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "README.md").write_text(str(output["readme_text"]), encoding="utf-8", newline="\n")
        (directory / "01_candidate-evolution-packet.json").write_text(
            json.dumps(output["packet"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        write_csv(directory / "02_evolution-source-index.csv", output["source_rows"], SOURCE_INDEX_FIELDS)  # type: ignore[arg-type]
        write_csv(directory / "03_era-source-code-index.csv", output["code_rows"], CODE_INDEX_FIELDS)  # type: ignore[arg-type]
        write_csv(directory / "05_image-reference-route-index.csv", output["image_route_rows"], IMAGE_ROUTE_FIELDS)  # type: ignore[arg-type]
        (directory / "06_image-reference-route-gallery.md").write_text(
            str(output["image_route_gallery_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "04_human-review-sheet.md").write_text(
            str(output["review_sheet_text"]),
            encoding="utf-8",
            newline="\n",
        )
    write_csv(root / EVOLUTION_ID_MAP, [output["map_row"] for output in outputs.values()], MAP_FIELDS)  # type: ignore[list-item]
    write_bucket_manifests(root, outputs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    outputs = build_outputs(root)
    write_outputs(root, outputs)
    print(f"evolution_candidate_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
