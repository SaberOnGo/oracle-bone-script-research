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
    "human_evolution_dossier_path",
    "evolution_dossier_index_path",
    "cross_period_review_dossier_path",
    "cross_period_review_index_path",
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
        (directory / "07_human-evolution-dossier.md").as_posix(),
        (directory / "08_evolution-dossier-index.json").as_posix(),
        (directory / "09_cross-period-review-dossier.md").as_posix(),
        (directory / "10_cross-period-review-index.json").as_posix(),
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
        lines.extend(
            textwrap.wrap(
                "  pending check: 待查：打开路线文件后核对本地图像、拓片、摹本或图版。",
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


def human_dossier_text(
    index: int,
    row: dict[str, str],
    code_rows: list[dict[str, str]],
    image_routes: list[dict[str, str]],
) -> str:
    pid = project_id(index)
    intro_en = wrapped_paragraph(
        "This dossier is the human-readable working file for one EVOBC "
        "evolution or cross-period correspondence candidate. It records source "
        "routes and concrete checks only; it is not a formal correspondence, "
        "not an evolution-chain conclusion, and not a decipherment conclusion."
    )
    intro_zh = wrapped_paragraph(
        "本档案是一个 EVOBC 字形演化或跨时期对应候选对象的人类可读工作档案。"
        "这里记录来源路线、图像线索和具体待查问题，不作正式对应、演化链或释读结论。"
    )
    identity_lines = bullet_block(
        [
            f"Project ID: `{pid}`",
            f"EVOBC category candidate ID: `{row['candidate_evolution_category_id']}`",
            f"External category reference: `{primary_external_ref(row)}`",
            f"Source category ID: `{row['source_category_id']}`",
            f"Source label: `{row['source_character_label']}`",
            f"Source codepoints: `{row['source_character_codepoints']}`",
            f"Image reference count in source metadata: `{row['image_reference_count']}`",
            f"Review status: `{REVIEW_STATUS}`",
        ]
    )
    route_lines = bullet_block(
        [
            "Open the EVOBC category staging CSV for the source category row.",
            "Open the EVOBC era/source codebook CSV for code labels.",
            "Open `05_image-reference-route-index.csv` before visual review.",
            "Open `06_image-reference-route-gallery.md` for local route cards.",
            "Open the EVOBC graph JSONL only as graph-derived routing.",
            "Check source download records, checksums, rights notes, and manifests "
            "before using any route as evidence.",
        ]
    )
    stage_lines = bullet_block(
        [
            "甲骨 route: check whether the source row only has metadata flags, "
            "or whether a primary oracle image, rubbing, plate, or inscription "
            "context has been separately verified.",
            "金文 route: treat bronze references as candidate route metadata until "
            "a cited image, catalog, vessel context, and bibliography are checked.",
            "小篆 route: treat seal-script links as later-script comparison clues, "
            "not proof of identity or development.",
            "后世字形 route: record only source-provided hints until dictionaries "
            "and published scholarship are opened.",
            "今字 route: codepoints and labels are lookup aids only; they do not "
            "confirm modern-character identity.",
        ]
    )
    code_lines = code_rows_block(code_rows)
    image_route_lines = route_cards_block(image_routes)
    bibliography_lines = bullet_block(
        [
            "Check Xiaoxuetang, OBIMD, HUST-OBC, IHP/Sinica, museum portals, "
            "published catalog notes, and paper bibliography before promotion.",
            "Record proposer, source, page or record ID, and disagreement status "
            "when a published correspondence or variant history is later found.",
            "Until bibliography is opened, keep this object as a route dossier "
            "with no reviewed scholarly conclusion.",
        ]
    )
    missing_lines = bullet_block(
        [
            "Which primary image, rubbing, hand copy, or plate corresponds to "
            "each EVOBC image reference?",
            "Which inscription number, collection number, findspot, period, "
            "batch, or group should be checked for the oracle-side context?",
            "Which bronze, seal, or later-script comparanda are cited by a "
            "reviewed source rather than inferred from dataset labels?",
            "Which modern codepoint route is only a lookup key, and which source "
            "would be needed before recording identity?",
            "Which bibliography, database page, or museum object page records "
            "a reading history, dispute, or alternative opinion?",
            "What evidence remains missing before any formal correspondence "
            "or evolution-chain claim can be reviewed?",
            "具体待查问题：先核对实物、拓片、照片、图版、著录和卜辞上下文，再记录 "
            "金文、小篆、后世字形和今字路线的证据等级。",
        ]
    )
    boundary_lines = bullet_block(
        [
            "No formal correspondence is recorded in this dossier.",
            "This dossier is not an evolution-chain conclusion.",
            "No evolution-chain conclusion is recorded in this dossier.",
            "No modern-character identity is confirmed in this dossier.",
            "No decipherment conclusion is recorded in this dossier.",
            "本档案只服务资料整理和复核路线，不替代正式文字学研究。",
        ]
    )
    return f"""# Human Evolution And Correspondence Dossier / 字形演化与对应候选档案

Project ID: `{pid}`

## Purpose / 用途

{intro_en}

{intro_zh}

## Candidate Identity / 候选身份

{identity_lines}

## Source Image And Route Evidence / 来源图像与路线证据

{route_lines}

## Era And Source-Code Context / 时期与来源代码语境

{code_lines}

## Oracle, Bronze, Seal, And Later-Script Review

{stage_lines}

## Modern Codepoint Route Review / 今字 codepoint 路线复核

{wrapped_paragraph(
        "Modern codepoints, source labels, and category IDs are lookup routes. "
        "They may guide comparison, but they are not accepted identities until "
        "human reviewers verify images, inscriptions, catalogs, and scholarship."
    )}

## Image Reference Route Cards / 图像引用路线卡

{image_route_lines}

## Bibliography, Database, And Web Source Routes

{bibliography_lines}

## Missing Evidence And Next Checks / 缺失证据与下一步

{missing_lines}

## Concrete Questions To Check / 具体待查问题

{missing_lines}

## Review Boundary / 复核边界

{boundary_lines}
"""


def dossier_index_payload(
    index: int,
    row: dict[str, str],
    directory: Path,
    code_rows: list[dict[str, str]],
    image_routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "evolution_correspondence_candidate_dossier_index",
        "candidate_evolution_category_id": row["candidate_evolution_category_id"],
        "source_id": SOURCE_ID,
        "human_readable_files": [
            (directory / "README.md").as_posix(),
            (directory / "04_human-review-sheet.md").as_posix(),
            (directory / "06_image-reference-route-gallery.md").as_posix(),
            (directory / "07_human-evolution-dossier.md").as_posix(),
            (directory / "09_cross-period-review-dossier.md").as_posix(),
        ],
        "ai_support_files": [
            (directory / "01_candidate-evolution-packet.json").as_posix(),
            (directory / "02_evolution-source-index.csv").as_posix(),
            (directory / "03_era-source-code-index.csv").as_posix(),
            (directory / "05_image-reference-route-index.csv").as_posix(),
            (directory / "10_cross-period-review-index.json").as_posix(),
        ],
        "source_route_files": route_files(directory),
        "code_row_count": len(code_rows),
        "image_route_count": len(image_routes),
        "uncollected_human_research_fields": [
            "primary_images",
            "oracle_inscription_context",
            "bronze_seal_later_script_comparanda",
            "modern_codepoint_identity_review",
            "bibliography_database_web_routes",
            "reading_history_and_disputes",
        ],
        "claim_boundary": (
            "no formal correspondence; no evolution-chain conclusion; "
            "no modern-character identity; no decipherment conclusion"
        ),
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def cross_period_review_dossier_text(
    index: int,
    row: dict[str, str],
    code_rows: list[dict[str, str]],
    image_routes: list[dict[str, str]],
) -> str:
    pid = project_id(index)
    intro = wrapped_paragraph(
        "本文件是给人工复核者打开的跨时期字形复核档案。它把 EVOBC "
        "候选路线、图像引用、时期/来源代码和下一步待查证据放在同一对象"
        "目录内；它不是正式对应结论，也不是释读结论。"
    )
    identity_lines = bullet_block(
        [
            f"本项目 ID：`{pid}`",
            f"EVOBC 候选类别 ID：`{row['candidate_evolution_category_id']}`",
            f"外部类别引用：`{primary_external_ref(row)}`",
            f"来源类别 ID：`{row['source_category_id']}`",
            f"来源标签：`{row['source_character_label']}`",
            f"来源 codepoints：`{row['source_character_codepoints']}`",
            f"EVOBC 图像引用数量：`{row['image_reference_count']}`",
            f"复核状态：`{REVIEW_STATUS}`",
        ]
    )
    oracle_lines = bullet_block(
        [
            "先查是否有对应的甲骨实物、拓片、照片、图版或摹本。",
            "再查甲骨侧卜辞编号、全文或 OCR、合集号、著录号和页码。",
            "继续核对馆藏、出土地、时期、组类、批次和关联字形。",
            "若只存在 EVOBC metadata，不得写成已确认甲骨字形对应。",
        ]
    )
    later_script_lines = bullet_block(
        [
            "金文路线只作为待核对比较线索，须另查器物、铭文和著录。",
            "小篆路线只作为后世字形比较线索，须另查字书和释读史。",
            "后世字形或今字路线须记录来源、提出者和不同意见。",
            "任何跨时期对应在人工复核前均保持候选和待查状态。",
        ]
    )
    codepoint_lines = bullet_block(
        [
            "codepoint 和来源标签只是检索键，不确认今字身份。",
            "若要记录今字对应，需先打开可复核字典、数据库或论文来源。",
            "若来源之间有不同意见，应记录争议而不是合并成结论。",
        ]
    )
    source_lines = bullet_block(
        [
            "先打开 `02_evolution-source-index.csv` 查来源与下载路线。",
            "再打开 `03_era-source-code-index.csv` 查时期和来源代码。",
            "再打开 `05_image-reference-route-index.csv` 查图像引用路线。",
            "图边和统计只作检索路线，不作学术结论。",
            "后续应核对小学堂、OBIMD、HUST-OBC、史语所和博物馆来源。",
        ]
    )
    route_lines = route_cards_block(image_routes)
    code_lines = code_rows_block(code_rows)
    missing_lines = bullet_block(
        [
            "哪一条 EVOBC 图像引用路线应先打开？",
            "哪一个甲骨卜辞、馆藏、出土地或时期批次仍未核对？",
            "哪一个金文器物、铭文、著录号或图版仍未核对？",
            "哪一个小篆、字书、数据库或论文来源仍未核对？",
            "哪一个今字 codepoint 只是检索键，尚不能作为对应结论？",
            "是否存在释读史、提出者、不同意见或争议需要记录？",
            "哪一条来源还缺 checksum、manifest、字段映射或权利复核？",
        ]
    )
    boundary_lines = bullet_block(
        [
            "这不是正式对应结论。",
            "这不是演化链结论。",
            "这不是今字身份确认。",
            "这不是释读结论。",
            "所有未打开的一手材料、著录和论文均保持待查状态。",
        ]
    )
    return f"""# {pid} 跨时期字形复核档案

{intro}

## 候选身份

{identity_lines}

## 甲骨侧待查证据

{oracle_lines}

## 金文、小篆与后世字形路线

{later_script_lines}

## 今字与 codepoint 路线

{codepoint_lines}

## 来源证据、争议与释读史路线

{source_lines}

## 已登记时期与来源代码

{code_lines}

## 图像引用路线卡

{route_lines}

## 具体待查问题

{missing_lines}

## 复核边界

{boundary_lines}
"""


def cross_period_review_index_payload(
    index: int,
    row: dict[str, str],
    directory: Path,
    code_rows: list[dict[str, str]],
    image_routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "project_id": project_id(index),
        "record_type": "evolution_cross_period_review_index",
        "candidate_evolution_category_id": row["candidate_evolution_category_id"],
        "source_id": SOURCE_ID,
        "human_readable_files": [
            (directory / "README.md").as_posix(),
            (directory / "04_human-review-sheet.md").as_posix(),
            (directory / "06_image-reference-route-gallery.md").as_posix(),
            (directory / "07_human-evolution-dossier.md").as_posix(),
            (directory / "09_cross-period-review-dossier.md").as_posix(),
        ],
        "ai_support_files": [
            (directory / "01_candidate-evolution-packet.json").as_posix(),
            (directory / "02_evolution-source-index.csv").as_posix(),
            (directory / "03_era-source-code-index.csv").as_posix(),
            (directory / "05_image-reference-route-index.csv").as_posix(),
            (directory / "08_evolution-dossier-index.json").as_posix(),
        ],
        "specific_missing_evidence": [
            "primary_image_rubbing_photo_plate_handcopy",
            "oracle_inscription_collection_findspot_period_batch",
            "bronze_object_inscription_catalog_plate",
            "seal_script_dictionary_database_paper_source",
            "modern_codepoint_identity_review",
            "reading_history_proposer_disagreement_dispute",
            "checksum_manifest_field_map_rights_review",
        ],
        "code_row_count": len(code_rows),
        "image_route_count": len(image_routes),
        "claim_status": {
            "correspondence": "no_formal_correspondence_claim",
            "evolution_chain": "no_evolution_chain_claim",
            "modern_identity": "no_modern_identity_claim",
            "decipherment": "no_decipherment_claim",
        },
        "review_status": REVIEW_STATUS,
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

- Local image evidence: 待查：需要打开路线文件核对本地图像、拓片、摹本或图版。
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

- Local image evidence: 待查：需要打开路线文件核对本地图像、拓片、摹本或图版。
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
- Source image evidence: 待查：需要打开图像路线文件核对来源图像证据。
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
            "human_dossier_text": human_dossier_text(index, row, code_rows, image_routes),
            "dossier_index": dossier_index_payload(index, row, directory, code_rows, image_routes),
            "cross_period_review_dossier_text": cross_period_review_dossier_text(
                index,
                row,
                code_rows,
                image_routes,
            ),
            "cross_period_review_index": cross_period_review_index_payload(
                index,
                row,
                directory,
                code_rows,
                image_routes,
            ),
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
                "human_evolution_dossier_path": (directory / "07_human-evolution-dossier.md").as_posix(),
                "evolution_dossier_index_path": (directory / "08_evolution-dossier-index.json").as_posix(),
                "cross_period_review_dossier_path": (directory / "09_cross-period-review-dossier.md").as_posix(),
                "cross_period_review_index_path": (directory / "10_cross-period-review-index.json").as_posix(),
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
        (directory / "07_human-evolution-dossier.md").write_text(
            str(output["human_dossier_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "08_evolution-dossier-index.json").write_text(
            json.dumps(output["dossier_index"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (directory / "09_cross-period-review-dossier.md").write_text(
            str(output["cross_period_review_dossier_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (directory / "10_cross-period-review-index.json").write_text(
            json.dumps(output["cross_period_review_index"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
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
