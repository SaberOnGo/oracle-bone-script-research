#!/usr/bin/env python3
"""Build object-local candidate materials for OBIMD subcharacters.

The output is preprocessing infrastructure only. Each object is a dataset
candidate package, not a formal component record or component assignment.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import textwrap
import zipfile
from collections import defaultdict
from io import BytesIO
from pathlib import Path

from PIL import Image


SUBCHARACTER_MAIN_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
SUBCHARACTER_GLYPH_STAGING = Path(
    "corpus/003_graphemic-components/000_component-registers/"
    "003_obimd-subcharacter-glyph-staging.csv"
)
COMPONENT_ROOT = Path("corpus/003_graphemic-components")
COMPONENT_ID_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/004_component-id-source-map.csv"
)
ASSET_ID_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv"
)
ASSET_SOURCE_INDEX = Path(
    "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
)
ASSET_RIGHTS_REVIEW_LOG = Path(
    "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv"
)
ASSET_TECHNICAL_PROFILE = Path(
    "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
)
OBIMD_SUBCHARACTER_IMAGES_ZIP = Path(
    "external_local_archive/source_packages/obimd/dl-obimd-subcharacter-images.zip"
)
OBIMD_IMAGE_SOURCE_URL = (
    "https://huggingface.co/datasets/KLOBIP/OBIMD/resolve/main/"
    "Hierarchical%20Character%20Metadata%20Supplement/"
    "Sub-character%20Images.zip"
)
UPDATED_AT = "2026-06-20"
MAX_HUMAN_LINE_LENGTH = 80
BUCKET_SIZE = 100
RECORD_TYPE = "graphemic_component_candidate"
OBJECT_STATUS = "dataset_candidate_not_promoted"
REVIEW_STATUS = "needs_human_component_review"
IMAGE_REVIEW_STATUS = "needs_human_visual_review"
RIGHTS_STATUS = "licensed_for_repository"
IMAGE_DOWNLOAD_ID = "dl-obimd-subcharacter-images"
RESEARCH_BOUNDARY = (
    "dataset_component_candidate_only_not_formal_component_record_not_component_assignment"
)
CAUTION = (
    "OBIMD subcharacter metadata is useful for routing component review, but this "
    "object is not a confirmed graphemic component, not a component breakdown, and "
    "not a decipherment or oracle-character identity claim."
)
IMAGE_CAUTION = (
    "OBIMD subcharacter image is a source-marked review asset only; it is not a "
    "confirmed component form, component assignment, or decipherment conclusion."
)

MANIFEST_FIELDS = [
    "candidate_component_id",
    "candidate_subcharacter_id",
    "candidate_directory",
    "primary_external_ref_id",
    "source_subcharacter_uid",
    "source_main_character_uid",
    "main_character_external_ref_id",
    "glyph_codepoint_count",
    "rights_status",
    "object_status",
    "review_status",
    "research_boundary",
    "updated_at",
]

SOURCE_INDEX_FIELDS = [
    "source_index_id",
    "candidate_component_id",
    "source_id",
    "evidence_download_id",
    "source_metadata_file",
    "external_ref_id",
    "relationship_type",
    "rights_status",
    "review_status",
    "caution",
    "updated_at",
]

GLYPH_INDEX_FIELDS = [
    "glyph_index_id",
    "candidate_component_id",
    "candidate_glyph_link_id",
    "source_id",
    "evidence_download_id",
    "subcharacter_external_ref_id",
    "glyph_codepoint",
    "glyph_codepoint_uplus",
    "relationship_type",
    "rights_status",
    "review_status",
    "caution",
    "updated_at",
]

VISUAL_INDEX_FIELDS = [
    "visual_index_id",
    "candidate_component_id",
    "asset_id",
    "source_id",
    "evidence_download_id",
    "subcharacter_external_ref_id",
    "source_zip_member",
    "local_asset_path",
    "file_size_bytes",
    "image_format",
    "pixel_width",
    "pixel_height",
    "color_mode",
    "dpi_x",
    "dpi_y",
    "icc_profile_bytes",
    "checksum_sha256",
    "rights_status",
    "review_status",
    "caution",
    "updated_at",
]

VISUAL_ROUTE_FIELDS = [
    "visual_route_id",
    "candidate_component_id",
    "source_id",
    "evidence_download_id",
    "subcharacter_external_ref_id",
    "source_package_path",
    "source_package_url",
    "source_subcharacter_uid",
    "local_image_status",
    "route_type",
    "route_path",
    "rights_status",
    "review_status",
    "caution",
    "updated_at",
]

COMPONENT_MAP_FIELDS = [
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

ASSET_MAP_FIELDS = [
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

ASSET_SOURCE_FIELDS = [
    "asset_id",
    "asset_type",
    "canonical_path",
    "file_size_bytes",
    "related_project_ids",
    "primary_external_ref_id",
    "source_ids",
    "source_url",
    "rights_status",
    "risk_note",
    "review_status",
    "updated_at",
]

ASSET_RIGHTS_FIELDS = [
    "review_id",
    "asset_id",
    "reviewer",
    "rights_status_before",
    "rights_status_after",
    "evidence",
    "reviewed_at",
    "notes",
]

ASSET_TECHNICAL_FIELDS = [
    "profile_id",
    "asset_id",
    "asset_path",
    "image_format",
    "pixel_width",
    "pixel_height",
    "color_mode",
    "dpi_x",
    "dpi_y",
    "icc_profile_bytes",
    "file_size_bytes",
    "checksum_sha256",
    "analysis_tool",
    "analysis_scope",
    "caution",
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def max_numeric_id(rows: list[dict[str, str]], field: str, prefix: str) -> int:
    max_id = 0
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    for row in rows:
        match = pattern.match(row.get(field, ""))
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id


def asset_id(number: int) -> str:
    return f"asset-{number:06d}"


def bucket_dir(index: int) -> Path:
    bucket_index = (index - 1) // BUCKET_SIZE + 1
    start = (bucket_index - 1) * BUCKET_SIZE + 1
    end = bucket_index * BUCKET_SIZE
    return COMPONENT_ROOT / (
        f"{bucket_index:03d}_{start:06d}-{end:06d}_"
        "obs-comp-cand-bucket_component-candidates"
    )


def candidate_id(index: int) -> str:
    return f"obs-comp-cand-{index:06d}"


def object_dir(index: int, external_ref_id: str) -> Path:
    return bucket_dir(index) / (
        f"{index:03d}_{candidate_id(index)}_{external_ref_id}_component-candidate"
    )


def route_files(directory: Path) -> list[str]:
    return [
        SUBCHARACTER_MAIN_STAGING.as_posix(),
        SUBCHARACTER_GLYPH_STAGING.as_posix(),
        COMPONENT_ID_MAP.as_posix(),
        ASSET_ID_MAP.as_posix(),
        ASSET_SOURCE_INDEX.as_posix(),
        ASSET_RIGHTS_REVIEW_LOG.as_posix(),
        "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
        (directory / "02_component-source-index.csv").as_posix(),
        (directory / "03_glyph-codepoint-index.csv").as_posix(),
        (directory / "04_glyph-codepoint-gallery.md").as_posix(),
        (directory / "06_component-visual-index.csv").as_posix(),
        (directory / "07_component-visual-gallery.md").as_posix(),
        (directory / "08_human-visual-review-sheet.md").as_posix(),
        (directory / "09_component-visual-route-index.csv").as_posix(),
        (directory / "10_component-visual-route-gallery.md").as_posix(),
    ]


def packet_payload(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    directory: Path,
) -> dict[str, object]:
    component_id = candidate_id(index)
    return {
        "candidate_component_id": component_id,
        "record_type": RECORD_TYPE,
        "candidate_subcharacter_id": main_row["candidate_subcharacter_id"],
        "preferred_directory_name": directory.name,
        "source_id": main_row["source_id"],
        "primary_external_ref_id": main_row["subcharacter_external_ref_id"],
        "source_subcharacter_uid": main_row["source_subcharacter_uid"],
        "source_main_character_uid": main_row["source_main_character_uid"],
        "main_character_external_ref_id": main_row["main_character_external_ref_id"],
        "source_relationship": {
            "relationship_type": main_row["relationship_type"],
            "evidence_download_id": main_row["evidence_download_id"],
            "source_metadata_file": main_row["source_metadata_file"],
            "status": main_row["project_import_status"],
        },
        "glyph_codepoint_links": [
            {
                "candidate_glyph_link_id": row["candidate_glyph_link_id"],
                "glyph_codepoint": row["glyph_codepoint"],
                "glyph_codepoint_uplus": row["glyph_codepoint_uplus"],
                "relationship_type": row["relationship_type"],
                "evidence_download_id": row["evidence_download_id"],
            }
            for row in glyph_rows
        ],
        "component_visual_assets": [
            {
                "asset_id": row["asset_id"],
                "source_zip_member": row["source_zip_member"],
                "local_asset_path": row["local_asset_path"],
                "checksum_sha256": row["checksum_sha256"],
                "review_status": row["review_status"],
            }
            for row in visual_rows
        ],
        "local_image_status": (
            "source_image_extracted"
            if visual_rows
            else "not_found_in_registered_source_package_route_indexed"
        ),
        "route_files": route_files(directory),
        "rights_status": RIGHTS_STATUS,
        "object_status": OBJECT_STATUS,
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def source_index_rows(index: int, main_row: dict[str, str]) -> list[dict[str, str]]:
    component_id = candidate_id(index)
    return [
        {
            "source_index_id": f"{component_id}-source-main",
            "candidate_component_id": component_id,
            "source_id": main_row["source_id"],
            "evidence_download_id": main_row["evidence_download_id"],
            "source_metadata_file": main_row["source_metadata_file"],
            "external_ref_id": main_row["subcharacter_external_ref_id"],
            "relationship_type": main_row["relationship_type"],
            "rights_status": main_row["rights_status"],
            "review_status": main_row["review_status"],
            "caution": main_row["caution"],
            "updated_at": UPDATED_AT,
        }
    ]


def glyph_index_rows(index: int, glyph_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    component_id = candidate_id(index)
    rows: list[dict[str, str]] = []
    for glyph_index, row in enumerate(glyph_rows, start=1):
        rows.append(
            {
                "glyph_index_id": f"{component_id}-glyph-{glyph_index:04d}",
                "candidate_component_id": component_id,
                "candidate_glyph_link_id": row["candidate_glyph_link_id"],
                "source_id": row["source_id"],
                "evidence_download_id": row["evidence_download_id"],
                "subcharacter_external_ref_id": row["subcharacter_external_ref_id"],
                "glyph_codepoint": row["glyph_codepoint"],
                "glyph_codepoint_uplus": row["glyph_codepoint_uplus"],
                "relationship_type": row["relationship_type"],
                "rights_status": row["rights_status"],
                "review_status": row["review_status"],
                "caution": row["caution"],
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def visual_route_rows(
    index: int,
    main_row: dict[str, str],
    visual_rows: list[dict[str, str]],
    directory: Path,
) -> list[dict[str, str]]:
    component_id = candidate_id(index)
    local_status = (
        "source_image_extracted"
        if visual_rows
        else "not_found_in_registered_source_package_route_indexed"
    )
    route_specs = [
        (
            "source_package",
            OBIMD_SUBCHARACTER_IMAGES_ZIP.as_posix(),
        ),
        (
            "source_metadata_staging",
            SUBCHARACTER_MAIN_STAGING.as_posix(),
        ),
        (
            "glyph_metadata_staging",
            SUBCHARACTER_GLYPH_STAGING.as_posix(),
        ),
        (
            "object_local_visual_index",
            (directory / "06_component-visual-index.csv").as_posix(),
        ),
    ]
    return [
        {
            "visual_route_id": f"{component_id}-visual-route-{route_index:02d}",
            "candidate_component_id": component_id,
            "source_id": "src-obimd",
            "evidence_download_id": IMAGE_DOWNLOAD_ID,
            "subcharacter_external_ref_id": main_row["subcharacter_external_ref_id"],
            "source_package_path": OBIMD_SUBCHARACTER_IMAGES_ZIP.as_posix(),
            "source_package_url": OBIMD_IMAGE_SOURCE_URL,
            "source_subcharacter_uid": main_row["source_subcharacter_uid"],
            "local_image_status": local_status,
            "route_type": route_type,
            "route_path": route_path,
            "rights_status": RIGHTS_STATUS,
            "review_status": IMAGE_REVIEW_STATUS,
            "caution": (
                "Visual route metadata only; this records where to inspect the "
                "OBIMD source package and object-local indexes, not a confirmed "
                "component form, component assignment, or decipherment conclusion."
            ),
            "updated_at": UPDATED_AT,
        }
        for route_index, (route_type, route_path) in enumerate(route_specs, start=1)
    ]


def readme_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    directory: Path,
) -> str:
    component_id = candidate_id(index)
    english_intro = wrap_markdown_line(
        "This directory is the object-local research entrance for one OBIMD "
        "subcharacter candidate. It keeps human-readable notes and AI-readable "
        "indexes in the same concrete corpus object directory."
    )
    chinese_intro = wrap_markdown_line(
        "本目录是一个 OBIMD subcharacter 候选对象的本地研究入口；"
        "人类可读资料和 AI 可读索引放在同一个具体 corpus 对象目录中。"
    )
    english_boundary = wrap_markdown_line(
        "This is not a confirmed graphemic component, not a component "
        "breakdown, not an oracle-character identity claim, and not a "
        "decipherment conclusion. It is a source-marked dataset candidate "
        "awaiting human component review."
    )
    chinese_boundary = wrap_markdown_line(
        "这不是已确认构件，不是构件拆分结论，不是甲骨字身份判断，"
        "也不是释读结论；它只是带来源标记、等待人工复核的数据库"
        "候选对象。"
    )
    english_review = wrap_markdown_line(
        "Review the OBIMD hierarchy, local images, source routes, and "
        "glyph-codepoint links against independent component, character, and "
        "inscription evidence before promoting any formal component record or "
        "graph relation."
    )
    chinese_review = wrap_markdown_line(
        "在提升为正式构件记录或正式图谱关系前，需要把 OBIMD 层级、"
        "本地图像、来源路线和 glyph-codepoint 线索同独立的构件、"
        "单字和卜辞证据交叉复核。"
    )
    concrete_questions = [
        "Which OBIMD source image or route should be opened first?",
        "应先打开哪一张 OBIMD 来源图像或哪条来源路线？",
        "Which glyph-codepoint links are only dataset clues?",
        "哪些 glyph-codepoint 关系只是数据集线索？",
        "Which local image, source zip member, or checksum needs review?",
        "需要核对哪张本地图像、source zip member 或 checksum？",
        "Which oracle character, inscription, or component source is relevant?",
        "哪些甲骨单字、卜辞或构件来源与本候选有关？",
        "Which near-shape or variant comparison is still missing?",
        "还缺哪些近形或异体比较？",
        "What evidence is still missing before any formal component assignment?",
        "正式构件归属前还缺哪些证据？",
    ]
    question_lines = "\n".join(
        line
        for item in concrete_questions
        for line in wrapped_bullet(item)
    )
    local_files = [
        ("01_candidate-component-packet.json", "AI-readable candidate packet."),
        ("02_component-source-index.csv", "Source, download, rights, and review index."),
        ("03_glyph-codepoint-index.csv", "OBIMD glyph-codepoint links."),
        ("04_glyph-codepoint-gallery.md", "Human glyph-codepoint gallery."),
        ("05_component-visual-assets/", "Source-marked OBIMD PNG review assets."),
        ("06_component-visual-index.csv", "AI-readable visual asset index."),
        ("07_component-visual-gallery.md", "Human component image gallery."),
        ("08_human-visual-review-sheet.md", "Manual visual review sheet."),
        ("09_component-visual-route-index.csv", "AI-readable visual route index."),
        ("10_component-visual-route-gallery.md", "Human visual route gallery."),
    ]
    local_file_lines = "\n".join(
        line
        for filename, note in local_files
        for line in wrapped_bullet(f"`{filename}`: {note}")
    )
    return f"""# {component_id} / OBIMD Subcharacter Candidate

English:
{english_intro}

Simplified Chinese:
{chinese_intro}

## Boundary / 边界

English:
{english_boundary}

简体中文：
{chinese_boundary}

## Source Snapshot / 来源快照

- candidate_component_id: `{component_id}`
- candidate_subcharacter_id: `{main_row["candidate_subcharacter_id"]}`
- primary_external_ref_id: `{main_row["subcharacter_external_ref_id"]}`
- source_subcharacter_uid: `{main_row["source_subcharacter_uid"]}`
- source_main_character_uid: `{main_row["source_main_character_uid"]}`
- main_character_external_ref_id: `{main_row["main_character_external_ref_id"]}`
- glyph_codepoint_link_count: `{len(glyph_rows)}`
- component_visual_asset_count: `{len(visual_rows)}`
- rights_status: `{RIGHTS_STATUS}`
- review_status: `{REVIEW_STATUS}`

## Local Files / 本地文件

{local_file_lines}

## Concrete Questions To Check / 具体待查问题

Use these specific component-review questions before recording conclusions.

{question_lines}

## Next Review / 下一步复核

English:
{english_review}

简体中文：
{chinese_review}

Route files / 路由文件:

{chr(10).join(line for path in route_files(directory) for line in wrapped_bullet(Path(path).name))}
"""


def gallery_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
) -> str:
    component_id = candidate_id(index)
    english_note = wrap_markdown_line(
        "This page is a human-readable review surface for OBIMD "
        "glyph-codepoint metadata. Some codepoints are private-use values and "
        "may not render in every font."
    )
    chinese_note = wrap_markdown_line(
        "本页用于人工查看 OBIMD glyph-codepoint metadata。部分码位属于"
        "私用区，可能无法在所有字体中正确显示。"
    )
    boundary_note = wrap_markdown_line(
        "dataset candidate only; not a confirmed component image, component "
        "assignment, or decipherment claim."
    )
    questions = [
        "Which glyph-codepoint links are only dataset clues?",
        "哪些 glyph-codepoint 关系只是数据集线索？",
        "Which codepoints are private-use or font-dependent?",
        "哪些码位属于私用区或依赖特定字体显示？",
        "Which glyph text must be compared with a source image?",
        "哪些 glyph text 必须回到来源图像比对？",
        "What evidence is missing before a component assignment?",
        "正式构件归属前还缺哪些证据？",
    ]
    question_lines = "\n".join(
        line
        for item in questions
        for line in wrapped_bullet(item)
    )
    lines = [
        f"# Glyph Codepoint Gallery / 字形码位查看: {component_id}",
        "",
        "English:",
        english_note,
        "",
        "简体中文：",
        chinese_note,
        "",
        "Boundary / 边界：",
        boundary_note,
        "- not a confirmed component form",
        "- not a component assignment",
        "- not a decipherment claim",
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "",
        question_lines,
        "",
        "| Link ID | Glyph text | U+ codepoints | Review status |",
        "| --- | --- | --- | --- |",
    ]
    for row in glyph_rows:
        glyph_text = row["glyph_codepoint"].replace("|", "\\|")
        lines.append(
            f"| `{row['candidate_glyph_link_id']}` | {glyph_text} | "
            f"`{row['glyph_codepoint_uplus']}` | `{row['review_status']}` |"
        )
    return "\n".join(lines) + "\n"


def visual_gallery_text(index: int, visual_rows: list[dict[str, str]]) -> str:
    component_id = candidate_id(index)
    english_note = wrap_markdown_line(
        "This page displays OBIMD subcharacter PNG assets extracted into this "
        "concrete corpus object directory for human review."
    )
    chinese_note = wrap_markdown_line(
        "本页展示抽取到当前具体 corpus 对象目录内的 OBIMD subcharacter "
        "PNG 资料，供人工复核使用。"
    )
    boundary_note = wrap_markdown_line(
        "dataset image candidate only; not a confirmed component form, not a "
        "component assignment, and not a decipherment claim."
    )
    questions = [
        "Which local image should be opened first?",
        "应先打开哪一张本地构件图像？",
        "Which source zip member anchors this image?",
        "哪一个 source zip member 能定位这张图像？",
        "Which near-shape or variant comparison is still missing?",
        "还缺哪些近形或异体比较？",
        "Which character or inscription context should be checked next?",
        "下一步应核对哪些单字或卜辞上下文？",
        "What evidence is missing before a component assignment?",
        "正式构件归属前还缺哪些证据？",
    ]
    question_lines = "\n".join(
        line
        for item in questions
        for line in wrapped_bullet(item)
    )
    lines = [
        f"# Component Visual Gallery / 构件图像查看: {component_id}",
        "",
        "English:",
        english_note,
        "",
        "简体中文：",
        chinese_note,
        "",
        "Boundary / 边界：",
        boundary_note,
        "- not a confirmed component form",
        "- not a component assignment",
        "- not a decipherment claim",
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "",
        question_lines,
        "",
    ]
    if not visual_rows:
        lines.extend(
            [
                wrap_markdown_line(
                    "No local OBIMD subcharacter image was found for this "
                    "candidate in the registered source package."
                ),
                "",
                "未在已登记来源包中找到此候选对应的本地图像。",
            ]
        )
        return "\n".join(lines) + "\n"

    for row in visual_rows:
        local_path = row["local_asset_path"]
        rel = local_path.split("/")[-2] + "/" + local_path.split("/")[-1]
        lines.extend(
            [
                f"## {row['asset_id']}",
                "",
                f"![{row['asset_id']}]({rel})",
                "",
                f"- source_zip_member: `{row['source_zip_member']}`",
                "- checksum_sha256: see `06_component-visual-index.csv`.",
                f"- review_status: `{row['review_status']}`",
                "- caution: source-marked review image only.",
                "",
            ]
        )
    return "\n".join(lines)


def wrap_markdown_line(text: str) -> str:
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


def visual_review_sheet_text(index: int, visual_rows: list[dict[str, str]]) -> str:
    component_id = candidate_id(index)
    rows = "\n".join(
        f"| `{row['asset_id']}` | `{row['source_zip_member']}` | pending | pending | pending | |"
        for row in visual_rows
    )
    if not rows:
        rows = "| no_local_image | not_found_in_registered_package | n/a | n/a | n/a | |"
    english_note = wrap_markdown_line(
        "Use this sheet to review the local OBIMD subcharacter images before any "
        "later component or relationship promotion."
    )
    chinese_note = wrap_markdown_line(
        "本表用于在后续提升为构件记录或关系前，人工复核本地 OBIMD "
        "subcharacter 图像。"
    )
    boundary_note = wrap_markdown_line(
        "These rows are review tasks only. They do not confirm a component form, "
        "component assignment, or decipherment."
    )
    concrete_questions = [
        "Which OBIMD component image or route should be opened first?",
        "应先打开哪些 OBIMD 构件图像或路线？",
        "Which source zip member and checksum prove the local image?",
        "哪些 source zip member 和 checksum 能证明本地图像？",
        "Which glyph-codepoint links are only dataset clues?",
        "哪些 glyph-codepoint 关系只是数据集线索？",
        "Which oracle character, inscription, or component source needs checking?",
        "需要核对哪些甲骨单字、卜辞或构件来源？",
        "Which near-shape or variant comparison is still missing?",
        "还缺哪些近形或异体比较？",
        "What evidence is still missing before any formal component assignment?",
        "正式构件归属前还缺哪些证据？",
    ]
    question_lines = "\n".join(
        line
        for item in concrete_questions
        for line in wrapped_bullet(item)
    )
    return f"""# Human Visual Review Sheet / 人工图像复核表: {component_id}

English:
{english_note}

简体中文：
{chinese_note}

Boundary / 边界：
{boundary_note}

## Concrete Questions To Check / 具体待查问题

{question_lines}

| Asset ID | Source zip member | Image legible? | Matches candidate UID? | Reuse acceptable? | Notes |
| --- | --- | --- | --- | --- | --- |
{rows}
"""


def visual_route_gallery_text(
    index: int,
    main_row: dict[str, str],
    visual_rows: list[dict[str, str]],
    directory: Path,
) -> str:
    component_id = candidate_id(index)
    local_status = (
        "source_image_extracted"
        if visual_rows
        else "not_found_in_registered_source_package_route_indexed"
    )
    route_rows = visual_route_rows(index, main_row, visual_rows, directory)
    english_note = wrap_markdown_line(
        "This object-local page records where a human or AI Agent should "
        "inspect OBIMD visual source material for this component candidate."
    )
    chinese_note = wrap_markdown_line(
        "本对象内页面记录人工或 AI Agent 应到哪里检查此构件候选的 "
        "OBIMD 图像来源材料。"
    )
    boundary_note = wrap_markdown_line(
        "Visual route metadata only; not a confirmed component form, not a "
        "component assignment, and not a decipherment conclusion."
    )
    questions = [
        "Which source package route should be opened first?",
        "应先打开哪一条来源包路线？",
        "Which missing-image status needs human confirmation?",
        "哪一项缺图状态需要人工确认？",
        "Which object-local visual index should be checked next?",
        "下一步应核对哪个对象内视觉索引？",
        "Which rights or source-package record must be reviewed?",
        "还要复核哪些权利或来源包记录？",
        "What evidence is missing before a component assignment?",
        "正式构件归属前还缺哪些证据？",
    ]
    question_lines = "\n".join(
        line
        for item in questions
        for line in wrapped_bullet(item)
    )
    lines = [
        f"# Component Visual Route Gallery / 构件图像路线图: {component_id}",
        "",
        "English:",
        english_note,
        "",
        "简体中文：",
        chinese_note,
        "",
        f"- local_image_status: `{local_status}`",
        "- source_package_path: see route table below.",
        "- source_package_url: see `09_component-visual-route-index.csv`.",
        f"- source_subcharacter_uid: `{main_row['source_subcharacter_uid']}`",
        f"- subcharacter_external_ref_id: `{main_row['subcharacter_external_ref_id']}`",
        "",
        "Boundary / 边界：",
        boundary_note,
        "- not a confirmed component form",
        "- not a component assignment",
        "- not a decipherment conclusion",
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "",
        question_lines,
        "",
        "| Route type | Route path | Review status |",
        "| --- | --- | --- |",
    ]
    for row in route_rows:
        lines.append(
            f"| `{row['route_type']}` | `{row['route_path']}` | `{row['review_status']}` |"
        )
    if not visual_rows:
        lines.extend(
            [
                "",
                wrap_markdown_line(
                    "No local PNG asset was found for this candidate in the "
                    "registered OBIMD source package during preprocessing."
                ),
                "",
                "预处理期间未在已登记的 OBIMD 来源包中找到此候选对应的本地 PNG 资产。",
            ]
        )
    return "\n".join(lines) + "\n"


def manifest_row(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    directory: Path,
) -> dict[str, str]:
    return {
        "candidate_component_id": candidate_id(index),
        "candidate_subcharacter_id": main_row["candidate_subcharacter_id"],
        "candidate_directory": directory.as_posix(),
        "primary_external_ref_id": main_row["subcharacter_external_ref_id"],
        "source_subcharacter_uid": main_row["source_subcharacter_uid"],
        "source_main_character_uid": main_row["source_main_character_uid"],
        "main_character_external_ref_id": main_row["main_character_external_ref_id"],
        "glyph_codepoint_count": str(len(glyph_rows)),
        "rights_status": RIGHTS_STATUS,
        "object_status": OBJECT_STATUS,
        "review_status": REVIEW_STATUS,
        "research_boundary": RESEARCH_BOUNDARY,
        "updated_at": UPDATED_AT,
    }


def component_map_row(index: int, main_row: dict[str, str], directory: Path) -> dict[str, str]:
    return {
        "project_id": candidate_id(index),
        "record_type": RECORD_TYPE,
        "canonical_path": directory.as_posix(),
        "primary_external_ref_id": main_row["subcharacter_external_ref_id"],
        "all_external_ref_ids": ";".join(
            [
                main_row["subcharacter_external_ref_id"],
                main_row["main_character_external_ref_id"],
            ]
        ),
        "source_ids": main_row["source_id"],
        "rights_status": RIGHTS_STATUS,
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def zip_images_by_subcharacter(zip_path: Path) -> dict[str, list[zipfile.ZipInfo]]:
    images: dict[str, list[zipfile.ZipInfo]] = defaultdict(list)
    if not zip_path.exists():
        return images
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if info.is_dir() or not info.filename.lower().endswith(".png"):
                continue
            parts = info.filename.split("/")
            if len(parts) >= 4 and parts[0] == "Sub-character Images":
                sub_uid = parts[2]
                images[sub_uid].append(info)
    for sub_uid in images:
        images[sub_uid].sort(key=lambda item: item.filename)
    return images


def existing_visual_asset_ids(root: Path) -> dict[str, str]:
    existing: dict[str, str] = {}
    for path in COMPONENT_ROOT.glob("*/*/06_component-visual-index.csv"):
        full_path = root / path
        if not full_path.exists():
            continue
        for row in read_csv_rows(full_path):
            key = f"{row.get('candidate_component_id')}|{row.get('source_zip_member')}"
            if row.get("asset_id"):
                existing[key] = row["asset_id"]
    return existing


def visual_asset_rows(
    root: Path,
    index: int,
    main_row: dict[str, str],
    directory: Path,
    image_infos: list[zipfile.ZipInfo],
    archive: zipfile.ZipFile | None,
    assigned_ids: dict[str, str],
    next_asset_number: list[int],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    component_id = candidate_id(index)
    asset_dir = root / directory / "05_component-visual-assets"
    asset_dir.mkdir(parents=True, exist_ok=True)

    for visual_index, info in enumerate(image_infos, start=1):
        key = f"{component_id}|{info.filename}"
        if key not in assigned_ids:
            assigned_ids[key] = asset_id(next_asset_number[0])
            next_asset_number[0] += 1
        current_asset_id = assigned_ids[key]
        asset_path = (
            directory
            / "05_component-visual-assets"
            / f"{visual_index:03d}_{current_asset_id}_img.png"
        )
        full_asset_path = root / asset_path
        assert archive is not None
        data = archive.read(info)
        full_asset_path.parent.mkdir(parents=True, exist_ok=True)
        full_asset_path.write_bytes(data)
        checksum = sha256_bytes(data)
        with Image.open(BytesIO(data)) as image:
            image_format = image.format or "PNG"
            pixel_width, pixel_height = image.size
            color_mode = image.mode
            dpi = image.info.get("dpi") or ("", "")
            dpi_x = str(dpi[0]) if dpi and dpi[0] else ""
            dpi_y = str(dpi[1]) if dpi and dpi[1] else ""
            icc_profile_bytes = str(len(image.info.get("icc_profile", b"")))
        yaml_path = full_asset_path.with_suffix(".yaml")
        yaml_path.write_text(
            "\n".join(
                [
                    f"asset_id: {current_asset_id}",
                    "asset_type: obimd_component_candidate_image",
                    f"candidate_component_id: {component_id}",
                    "source_id: src-obimd",
                    f"evidence_download_id: {IMAGE_DOWNLOAD_ID}",
                    f"subcharacter_external_ref_id: {main_row['subcharacter_external_ref_id']}",
                    f"source_zip_member: {info.filename}",
                    f"file_size_bytes: {len(data)}",
                    f"image_format: {image_format}",
                    f"pixel_width: {pixel_width}",
                    f"pixel_height: {pixel_height}",
                    f"color_mode: {color_mode}",
                    f"checksum_sha256: {checksum}",
                    f"rights_status: {RIGHTS_STATUS}",
                    f"review_status: {IMAGE_REVIEW_STATUS}",
                    f"updated_at: {UPDATED_AT}",
                    f"caution: {IMAGE_CAUTION}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        rows.append(
            {
                "visual_index_id": f"{component_id}-visual-{visual_index:04d}",
                "candidate_component_id": component_id,
                "asset_id": current_asset_id,
                "source_id": "src-obimd",
                "evidence_download_id": IMAGE_DOWNLOAD_ID,
                "subcharacter_external_ref_id": main_row["subcharacter_external_ref_id"],
                "source_zip_member": info.filename,
                "local_asset_path": asset_path.as_posix(),
                "file_size_bytes": str(len(data)),
                "image_format": image_format,
                "pixel_width": str(pixel_width),
                "pixel_height": str(pixel_height),
                "color_mode": color_mode,
                "dpi_x": dpi_x,
                "dpi_y": dpi_y,
                "icc_profile_bytes": icc_profile_bytes,
                "checksum_sha256": checksum,
                "rights_status": RIGHTS_STATUS,
                "review_status": IMAGE_REVIEW_STATUS,
                "caution": IMAGE_CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def obimd_asset_source_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "asset_id": row["asset_id"],
        "asset_type": "obimd_component_candidate_image",
        "canonical_path": row["local_asset_path"],
        "file_size_bytes": row["file_size_bytes"],
        "related_project_ids": row["candidate_component_id"],
        "primary_external_ref_id": row["subcharacter_external_ref_id"],
        "source_ids": row["source_id"],
        "source_url": OBIMD_IMAGE_SOURCE_URL,
        "rights_status": row["rights_status"],
        "risk_note": row["caution"],
        "review_status": row["review_status"],
        "updated_at": UPDATED_AT,
    }


def obimd_asset_map_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "project_id": row["asset_id"],
        "record_type": "obimd_component_candidate_image",
        "canonical_path": row["local_asset_path"],
        "primary_external_ref_id": row["subcharacter_external_ref_id"],
        "all_external_ref_ids": row["subcharacter_external_ref_id"],
        "source_ids": row["source_id"],
        "rights_status": row["rights_status"],
        "review_status": row["review_status"],
        "updated_at": UPDATED_AT,
    }


def obimd_asset_rights_row(row: dict[str, str]) -> dict[str, str]:
    numeric = row["asset_id"].split("-")[-1]
    return {
        "review_id": f"asset-rights-review-{numeric}",
        "asset_id": row["asset_id"],
        "reviewer": "codex-agent",
        "rights_status_before": "unreviewed",
        "rights_status_after": row["rights_status"],
        "evidence": (
            "OBIMD dataset card and source register mark repository use as "
            f"{RIGHTS_STATUS}; raw source package is registered and kept outside Git."
        ),
        "reviewed_at": UPDATED_AT,
        "notes": row["caution"],
    }


def obimd_asset_technical_row(index: int, row: dict[str, str]) -> dict[str, str]:
    return {
        "profile_id": f"asset-image-profile-{index:06d}",
        "asset_id": row["asset_id"],
        "asset_path": row["local_asset_path"],
        "image_format": row["image_format"],
        "pixel_width": row["pixel_width"],
        "pixel_height": row["pixel_height"],
        "color_mode": row["color_mode"],
        "dpi_x": row["dpi_x"],
        "dpi_y": row["dpi_y"],
        "icc_profile_bytes": row["icc_profile_bytes"],
        "file_size_bytes": row["file_size_bytes"],
        "checksum_sha256": row["checksum_sha256"],
        "analysis_tool": "Pillow",
        "analysis_scope": "image_technical_metadata_only",
        "caution": (
            "Technical profile records file properties only; it is not glyph "
            "segmentation, component analysis, or paleographic interpretation."
        ),
        "review_status": IMAGE_REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def build_materials(root: Path) -> tuple[int, int]:
    main_rows = read_csv_rows(root / SUBCHARACTER_MAIN_STAGING)
    glyph_by_uid: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv_rows(root / SUBCHARACTER_GLYPH_STAGING):
        glyph_by_uid[row["source_subcharacter_uid"]].append(row)

    manifest_by_bucket: dict[Path, list[dict[str, str]]] = defaultdict(list)
    component_map_rows: list[dict[str, str]] = []
    asset_map_rows_existing = read_csv_rows(root / ASSET_ID_MAP)
    asset_source_rows_existing = read_csv_rows(root / ASSET_SOURCE_INDEX)
    asset_rights_rows_existing = read_csv_rows(root / ASSET_RIGHTS_REVIEW_LOG)
    asset_technical_rows_existing = read_csv_rows(root / ASSET_TECHNICAL_PROFILE)
    assigned_ids = existing_visual_asset_ids(root)
    next_asset_number = [
        max_numeric_id(asset_map_rows_existing, "project_id", "asset-") + 1
    ]
    image_infos_by_uid = zip_images_by_subcharacter(root / OBIMD_SUBCHARACTER_IMAGES_ZIP)
    archive: zipfile.ZipFile | None = None
    if (root / OBIMD_SUBCHARACTER_IMAGES_ZIP).exists():
        archive = zipfile.ZipFile(root / OBIMD_SUBCHARACTER_IMAGES_ZIP)
    all_visual_rows: list[dict[str, str]] = []

    try:
        for index, main_row in enumerate(main_rows, start=1):
            glyph_rows = glyph_by_uid[main_row["source_subcharacter_uid"]]
            directory = object_dir(index, main_row["subcharacter_external_ref_id"])
            full_directory = root / directory
            full_directory.mkdir(parents=True, exist_ok=True)
            image_infos = image_infos_by_uid.get(main_row["source_subcharacter_uid"], [])
            visual_rows = visual_asset_rows(
                root,
                index,
                main_row,
                directory,
                image_infos,
                archive,
                assigned_ids,
                next_asset_number,
            )
            all_visual_rows.extend(visual_rows)

            (full_directory / "README.md").write_text(
                readme_text(index, main_row, glyph_rows, visual_rows, directory),
                encoding="utf-8",
            )
            (full_directory / "01_candidate-component-packet.json").write_text(
                json.dumps(
                    packet_payload(index, main_row, glyph_rows, visual_rows, directory),
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            write_csv(
                full_directory / "02_component-source-index.csv",
                source_index_rows(index, main_row),
                SOURCE_INDEX_FIELDS,
            )
            write_csv(
                full_directory / "03_glyph-codepoint-index.csv",
                glyph_index_rows(index, glyph_rows),
                GLYPH_INDEX_FIELDS,
            )
            (full_directory / "04_glyph-codepoint-gallery.md").write_text(
                gallery_text(index, main_row, glyph_rows),
                encoding="utf-8",
            )
            write_csv(
                full_directory / "06_component-visual-index.csv",
                visual_rows,
                VISUAL_INDEX_FIELDS,
            )
            (full_directory / "07_component-visual-gallery.md").write_text(
                visual_gallery_text(index, visual_rows),
                encoding="utf-8",
            )
            (full_directory / "08_human-visual-review-sheet.md").write_text(
                visual_review_sheet_text(index, visual_rows),
                encoding="utf-8",
            )
            write_csv(
                full_directory / "09_component-visual-route-index.csv",
                visual_route_rows(index, main_row, visual_rows, directory),
                VISUAL_ROUTE_FIELDS,
            )
            (full_directory / "10_component-visual-route-gallery.md").write_text(
                visual_route_gallery_text(index, main_row, visual_rows, directory),
                encoding="utf-8",
            )
            manifest_by_bucket[bucket_dir(index)].append(
                manifest_row(index, main_row, glyph_rows, directory)
            )
            component_map_rows.append(component_map_row(index, main_row, directory))
    finally:
        if archive is not None:
            archive.close()

    for bucket, rows in manifest_by_bucket.items():
        write_csv(root / bucket / "000_obimd-component-candidate-bucket-manifest.csv", rows, MANIFEST_FIELDS)
    write_csv(root / COMPONENT_ID_MAP, component_map_rows, COMPONENT_MAP_FIELDS)
    non_obimd_asset_map = [
        row
        for row in asset_map_rows_existing
        if row.get("record_type") != "obimd_component_candidate_image"
    ]
    non_obimd_asset_source = [
        row
        for row in asset_source_rows_existing
        if row.get("asset_type") != "obimd_component_candidate_image"
    ]
    non_obimd_asset_rights = [
        row
        for row in asset_rights_rows_existing
        if row.get("asset_id") not in {visual["asset_id"] for visual in all_visual_rows}
    ]
    non_obimd_asset_technical = [
        row
        for row in asset_technical_rows_existing
        if row.get("asset_id") not in {visual["asset_id"] for visual in all_visual_rows}
    ]
    write_csv(
        root / ASSET_ID_MAP,
        non_obimd_asset_map + [obimd_asset_map_row(row) for row in all_visual_rows],
        ASSET_MAP_FIELDS,
    )
    write_csv(
        root / ASSET_SOURCE_INDEX,
        non_obimd_asset_source
        + [obimd_asset_source_row(row) for row in all_visual_rows],
        ASSET_SOURCE_FIELDS,
    )
    write_csv(
        root / ASSET_RIGHTS_REVIEW_LOG,
        non_obimd_asset_rights
        + [obimd_asset_rights_row(row) for row in all_visual_rows],
        ASSET_RIGHTS_FIELDS,
    )
    write_csv(
        root / ASSET_TECHNICAL_PROFILE,
        non_obimd_asset_technical
        + [
            obimd_asset_technical_row(index, row)
            for index, row in enumerate(
                all_visual_rows,
                start=len(non_obimd_asset_technical) + 1,
            )
        ],
        ASSET_TECHNICAL_FIELDS,
    )
    return len(main_rows), len(manifest_by_bucket)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else repo_root()
    candidate_count, bucket_count = build_materials(root)
    print(f"component_candidate_count={candidate_count} bucket_count={bucket_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
