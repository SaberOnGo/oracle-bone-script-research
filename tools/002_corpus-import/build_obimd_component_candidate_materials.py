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

COMPONENT_VISUAL_OBSERVATIONS = {
    "obs-comp-cand-000001": (
        "The local image shows a pointed, closed outer outline with a short "
        "oblique interior stroke and a narrow tail continuing below the outline.",
        "本地图像有尖顶闭合外轮廓，内部有短斜向笔画，轮廓下方另有窄长尾部。",
    ),
    "obs-comp-cand-000002": (
        "The image shows a horizontal rounded rectangular outline with one short "
        "vertical stroke near the center and no other visible interior marks.",
        "图像有横向圆角矩形外轮廓，中部附近有一道短竖画，内部未见其他明显痕迹。",
    ),
    "obs-comp-cand-000003": (
        "The image shows a thick circular ring surrounding one separate filled "
        "round mark at the center.",
        "图像有粗圆环，中央包围一处分离的实心圆形痕迹。",
    ),
    "obs-comp-cand-000004": (
        "The image has a rounded horizontal central outline with a short inner "
        "stroke, two detached side marks, and short horizontal marks above and below.",
        "图像中央有横向圆弧外轮廓和短内部笔画，两侧有分离痕迹，上下另有短横画。",
    ),
    "obs-comp-cand-000005": (
        "The image shows a small upper rounded rectangle with a short inner bar, "
        "a longer horizontal bar below, and one long stroke descending from it.",
        "图像上部有小型圆角矩形和短内横画，下方有较长横画，并向下延出长笔画。",
    ),
    "obs-comp-cand-000006": (
        "The image shows an upper rounded rectangle with a short inner bar and a "
        "separate square outline below it.",
        "图像上部有圆角矩形和短内横画，下方另有分离的方框轮廓。",
    ),
    "obs-comp-cand-000007": (
        "The upper part contains several short angular strokes in two dense rows; "
        "a separate rounded outline with a short inner mark sits below.",
        "上部有两排密集的短折角笔画，下方另有带短内部痕迹的圆弧外轮廓。",
    ),
    "obs-comp-cand-000008": (
        "The upper part shows crossing diagonal and upright strokes with long lower "
        "tails; a separate rounded square with an inner bar sits below.",
        "上部有交叉斜向和直立笔画，并向下延出长尾；下方另有带内横画的圆角方框。",
    ),
    "obs-comp-cand-000009": (
        "The image shows a long curved outer stroke and a central descending stroke "
        "ending at a rounded enclosure with a filled interior mark.",
        "图像有长弯曲外侧笔画和中央下行笔画，下端接圆弧外框，内部有实心痕迹。",
    ),
    "obs-comp-cand-000010": (
        "The image shows a long curved left stroke and a central descending stroke "
        "ending at a rounded enclosure with a filled interior mark.",
        "图像有左侧长弯曲笔画和中央下行笔画，下端接圆弧外框，内部有实心痕迹。",
    ),
}

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


def has_material_visual_observation(index: int) -> bool:
    return candidate_id(index) in COMPONENT_VISUAL_OBSERVATIONS


def route_files(directory: Path, index: int | None = None) -> list[str]:
    routes = [
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
        (directory / "11_human-component-dossier.md").as_posix(),
        (directory / "12_component-dossier-index.json").as_posix(),
        (directory / "13_component-context-evidence-dossier.md").as_posix(),
        (directory / "14_component-context-evidence-index.json").as_posix(),
        (directory / "15_component-review-fact-matrix.md").as_posix(),
        (directory / "16_component-research-readiness-review.md").as_posix(),
        (directory / "17_component-research-readiness-index.json").as_posix(),
    ]
    if index is not None and has_material_visual_observation(index):
        routes.append((directory / "18_material-visual-observation.md").as_posix())
    return routes


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
        "route_files": route_files(directory, index),
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
        "This directory is the object-local human research entrance for one "
        "OBIMD subcharacter candidate. Start with the human component dossier, "
        "then use the source, visual, route, and structured support files only "
        "to trace and verify the human-readable evidence."
    )
    chinese_intro = wrap_markdown_line(
        "本目录是一个 OBIMD subcharacter 候选对象的对象内人类研究入口。"
        "先阅读人类构件档案，再用来源、图像、路线和结构化辅助文件追溯、"
        "核查人类可读证据。"
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
        "Open 06_component-visual-index.csv and name the source image row.",
        "\u6253\u5f00 06_component-visual-index.csv\uff0c\u5199\u660e"
        "\u6765\u6e90\u56fe\u50cf\u884c\u3002",
        "Open 09_component-visual-route-index.csv and name the missing route row.",
        "\u6253\u5f00 09_component-visual-route-index.csv\uff0c"
        "\u5199\u660e\u7f3a\u5931\u8def\u7ebf\u884c\u3002",
        "Open 03_glyph-codepoint-index.csv and name dataset-only glyph links.",
        "\u6253\u5f00 03_glyph-codepoint-index.csv\uff0c"
        "\u5199\u660e\u4ec5\u5c5e\u6570\u636e\u96c6\u7ebf\u7d22\u7684"
        "\u5b57\u5f62\u5173\u7cfb\u3002",
        "Open 13_component-context-evidence-dossier.md for context routes.",
        "\u6253\u5f00 13_component-context-evidence-dossier.md\uff0c"
        "\u6838\u5bf9\u4e0a\u4e0b\u6587\u8def\u7ebf\u3002",
        "Record whether the missing route is image, near-shape, source, or context.",
        "\u8bb0\u5f55\u7f3a\u53e3\u5c5e\u4e8e\u56fe\u50cf\u3001"
        "\u8fd1\u5f62\u3001\u6765\u6e90\u8fd8\u662f\u4e0a\u4e0b\u6587\u8def\u7ebf\u3002",
    ]
    question_lines = "\n".join(
        line
        for item in concrete_questions
        for line in wrapped_bullet(item)
    )
    local_files = [
        ("01_candidate-component-packet.json", "Structured support packet for this human dossier."),
        ("02_component-source-index.csv", "Source, download, rights, and review index."),
        ("03_glyph-codepoint-index.csv", "OBIMD glyph-codepoint links."),
        ("04_glyph-codepoint-gallery.md", "Human glyph-codepoint gallery."),
        ("05_component-visual-assets/", "Source-marked OBIMD PNG review assets."),
        ("06_component-visual-index.csv", "Structured support index for visual assets."),
        ("07_component-visual-gallery.md", "Human component image gallery."),
        ("08_human-visual-review-sheet.md", "Manual visual review sheet."),
        ("09_component-visual-route-index.csv", "Structured support index for visual routes."),
        ("10_component-visual-route-gallery.md", "Human visual route gallery."),
        ("11_human-component-dossier.md", "Human component candidate dossier."),
        ("12_component-dossier-index.json", "Structured support index for dossier gaps."),
        ("13_component-context-evidence-dossier.md", "Human context evidence dossier."),
        ("14_component-context-evidence-index.json", "Structured support index for context routes."),
        ("15_component-review-fact-matrix.md", "Human component review fact matrix."),
        (
            "16_component-research-readiness-review.md",
            "Human readiness review before formal component research.",
        ),
        (
            "17_component-research-readiness-index.json",
            "Structured support index for readiness slots.",
        ),
    ]
    if has_material_visual_observation(index):
        local_files.append(
            (
                "18_material-visual-observation.md",
                "Direct visible-material observation for this local image.",
            )
        )
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

## Human Component Review Slots / 构件复核槽位

Structured support files only serve the human component dossier.

结构化辅助文件只服务本对象内的人类构件档案。

- Compare the OBIMD subcharacter image with local visual evidence.
- Check near-shape, variant, and component-splitting candidates.
- Link only source-backed character and inscription context routes.
- Record meaning, reading, scholarship, and dispute status as pending.
- Check source, rights, manifest, field map, and extraction evidence.
- Keep every missing item as a concrete question before formal research.
- 比较 OBIMD subcharacter 图像和对象内视觉证据。
- 核查近形、异体、变体和构件拆分候选。
- 只关联有来源支持的单字和卜辞上下文路线。
- 将字义、读法、文献和争议状态标为待查。
- 核对来源、权利、manifest、字段映射和抽取证据。
- 正式研究前，所有缺失项都必须写成具体问题。

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

{chr(10).join(line for path in route_files(directory, index) for line in wrapped_bullet(Path(path).name))}
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
        "Open 06_component-visual-index.csv and name the local image row.",
        "\u6253\u5f00 06_component-visual-index.csv\uff0c\u5199\u660e"
        "\u672c\u5730\u56fe\u50cf\u884c\u3002",
        "Open 09_component-visual-route-index.csv and name the source route row.",
        "\u6253\u5f00 09_component-visual-route-index.csv\uff0c"
        "\u5199\u660e\u6765\u6e90\u8def\u7ebf\u884c\u3002",
        "Open 13_component-context-evidence-dossier.md for character context.",
        "\u6253\u5f00 13_component-context-evidence-dossier.md\uff0c"
        "\u6838\u5bf9\u5355\u5b57\u4e0e\u535c\u8f9e\u4e0a\u4e0b\u6587\u3002",
        "Record the missing image, near-shape, source, or context route.",
        "\u8bb0\u5f55\u7f3a\u5931\u7684\u56fe\u50cf\u3001\u8fd1\u5f62\u3001"
        "\u6765\u6e90\u6216\u4e0a\u4e0b\u6587\u8def\u7ebf\u3002",
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


def compact_inline_sample(values: list[str], max_chars: int) -> str:
    sample = ", ".join(values[:2])
    if len(values) > 2:
        sample = f"{sample}, ..."
    if not sample:
        return "pending review"
    if len(sample) <= max_chars:
        return sample
    return f"{sample[: max_chars - 3].rstrip(' ,;')}..."


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
        "Open 06_component-visual-index.csv and name the source image row.",
        "\u6253\u5f00 06_component-visual-index.csv\uff0c\u5199\u660e"
        "\u6765\u6e90\u56fe\u50cf\u884c\u3002",
        "Open 09_component-visual-route-index.csv and name the missing route row.",
        "\u6253\u5f00 09_component-visual-route-index.csv\uff0c"
        "\u5199\u660e\u7f3a\u5931\u8def\u7ebf\u884c\u3002",
        "Open 03_glyph-codepoint-index.csv and name dataset-only glyph links.",
        "\u6253\u5f00 03_glyph-codepoint-index.csv\uff0c"
        "\u5199\u660e\u4ec5\u5c5e\u6570\u636e\u96c6\u7ebf\u7d22\u7684"
        "\u5b57\u5f62\u5173\u7cfb\u3002",
        "Open 13_component-context-evidence-dossier.md for context routes.",
        "\u6253\u5f00 13_component-context-evidence-dossier.md\uff0c"
        "\u6838\u5bf9\u4e0a\u4e0b\u6587\u8def\u7ebf\u3002",
        "Record whether the missing route is image, near-shape, source, or context.",
        "\u8bb0\u5f55\u7f3a\u53e3\u5c5e\u4e8e\u56fe\u50cf\u3001"
        "\u8fd1\u5f62\u3001\u6765\u6e90\u8fd8\u662f\u4e0a\u4e0b\u6587\u8def\u7ebf\u3002",
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


def material_visual_observation_text(
    index: int,
    main_row: dict[str, str],
    visual_rows: list[dict[str, str]],
    directory: Path,
) -> str:
    component_id = candidate_id(index)
    observation_en, observation_zh = COMPONENT_VISUAL_OBSERVATIONS[component_id]
    image_row = visual_rows[0] if visual_rows else {}
    local_path = Path(image_row.get("local_asset_path", "pending"))
    try:
        local_path_text = local_path.relative_to(directory).as_posix()
    except ValueError:
        local_path_text = local_path.as_posix()
    source_member = image_row.get("source_zip_member", "pending source row")
    lines = [
        f"# Material Visual Observation / {component_id} 实物图像观察",
        "",
        "English:",
        wrap_markdown_line(
            "This note records only visible marks in one local, source-linked "
            "OBIMD review image. It is a preparation-stage observation, not a "
            "component assignment or decipherment conclusion."
        ),
        "",
        "简体中文：",
        wrap_markdown_line(
            "本记录只描述一张有来源链接的本地 OBIMD 复核图像中直接可见的"
            "痕迹，供预处理阶段查阅，不是构件归属或释读结论。"
        ),
        "",
        "## Evidence Opened / 已打开证据",
        "",
        f"- Candidate ID / 候选 ID: `{component_id}`",
        f"- External reference / 外部参照: `{main_row['subcharacter_external_ref_id']}`",
        f"- Source / 来源: `{main_row['source_id']}`",
        f"- Download route / 下载路线: `{main_row['evidence_download_id']}`",
        f"- Asset ID / 资产 ID: `{image_row.get('asset_id', 'pending')}`",
        f"- Local image / 本地图像: `{local_path_text}`",
        "- Source zip member / 来源压缩包成员:",
        f"  `{source_member}`",
        "- Checksum / 校验和:",
        f"  `{image_row.get('checksum_sha256', 'pending')}`",
        f"- Rights status / 权利状态: `{RIGHTS_STATUS}`",
        f"- Review status / 复核状态: `{IMAGE_REVIEW_STATUS}`",
        "",
        "## Direct Visual Record / 直接可见记录",
        "",
        "- English observation:",
        *textwrap.wrap(
            observation_en,
            width=78,
            break_long_words=False,
            break_on_hyphens=False,
            subsequent_indent="  ",
        ),
        "- 中文观察:",
        f"  {observation_zh}",
        "",
        "## Next Checks / 下一步核查",
        "",
        "- Compare the image with independent component and character sources.",
        "- Check whether a second image, rubbing, inscription, or plate exists.",
        "- Record component boundaries, near forms, readings, and disputes only",
        "  after source review; keep them as candidates or pending checks.",
        "- 与独立构件和单字来源比较本地图像。",
        "- 查找是否存在第二张图像、拓片、卜辞或图版。",
        "- 来源复核前，构件边界、近形、释读和争议只能记为候选或待查。",
        "",
        "## Boundary / 边界",
        "",
        wrap_markdown_line(
            "This is a visible-material observation, not a confirmed component "
            "form, component assignment, oracle-character identity claim, or "
            "decipherment conclusion."
        ),
        "- Claim boundary: not a component assignment; not a decipherment conclusion.",
        "- 边界标记：不是构件归属；不是释读结论。",
        "本记录是图像观察，不是已确认构件形体、构件归属、甲骨字身份或释读结论。",
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(text, f"{component_id}/18_material-visual-observation.md")
    return text


def component_dossier_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    directory: Path,
) -> str:
    component_id = candidate_id(index)
    local_status = (
        "source_image_extracted"
        if visual_rows
        else "not_found_in_registered_source_package_route_indexed"
    )
    intro_en = wrap_markdown_line(
        "This human-readable dossier gathers the object-local material needed "
        "before any component review: source identifiers, local images, "
        "glyph-codepoint clues, route files, rights evidence, and concrete "
        "questions still requiring human verification."
    )
    intro_zh = wrap_markdown_line(
        "\u672c\u6863\u6848\u6c47\u603b\u6784\u4ef6\u590d\u6838\u524d"
        "\u9700\u8981\u6253\u5f00\u7684\u5bf9\u8c61\u5185\u6750\u6599\uff1a"
        "\u6765\u6e90\u7f16\u53f7\u3001\u672c\u5730\u56fe\u50cf\u3001"
        "glyph-codepoint \u7ebf\u7d22\u3001\u8def\u7ebf\u6587\u4ef6\u3001"
        "\u6743\u5229\u8bc1\u636e\uff0c\u4ee5\u53ca\u4ecd\u9700"
        "\u4eba\u5de5\u6838\u67e5\u7684\u5177\u4f53\u95ee\u9898\u3002"
    )
    boundary = wrap_markdown_line(
        "This is not a formal component assignment, not a confirmed component "
        "form, not an oracle-character identity claim, and not a decipherment "
        "conclusion."
    )
    glyph_count = str(len(glyph_rows))
    visual_count = str(len(visual_rows))
    glyph_values = sorted({row["glyph_codepoint_uplus"] for row in glyph_rows if row})
    glyph_sample = compact_inline_sample(glyph_values, max_chars=44)
    visual_paths = "\n".join(
        f"| `{row['asset_id']}` | `{Path(row['local_asset_path']).name}` |"
        f" `{row['checksum_sha256']}` |"
        for row in visual_rows
    )
    if not visual_paths:
        visual_paths = (
            "| no_local_image | not_found_in_registered_package | "
            "pending source-package check |"
        )
    questions = [
        "Open 06_component-visual-index.csv and record image evidence.",
        "\u6253\u5f00 06_component-visual-index.csv\uff0c\u8bb0\u5f55"
        "\u56fe\u50cf\u8bc1\u636e\u3002",
        "Which glyph-codepoint links are private-use or font-dependent clues?",
        "\u54ea\u4e9b glyph-codepoint \u5173\u7cfb\u5c5e\u4e8e"
        "\u79c1\u7528\u533a\u6216\u4f9d\u8d56\u5b57\u4f53\u7684\u7ebf\u7d22\uff1f",
        "Open 09_component-visual-route-index.csv for missing-image routes.",
        "\u6253\u5f00 09_component-visual-route-index.csv\uff0c"
        "\u6838\u5bf9\u7f3a\u5931\u56fe\u50cf\u8def\u7ebf\u3002",
        "Open 13_component-context-evidence-dossier.md for character context.",
        "\u6253\u5f00 13_component-context-evidence-dossier.md\uff0c"
        "\u6838\u5bf9\u5355\u5b57\u4e0e\u535c\u8f9e\u4e0a\u4e0b\u6587\u3002",
        "Which source package, checksum, and rights rows prove the images?",
        "\u54ea\u4e9b\u6765\u6e90\u5305\u3001checksum \u4e0e"
        "\u6743\u5229\u8bb0\u5f55\u80fd\u8bc1\u660e\u8fd9\u4e9b\u56fe\u50cf\uff1f",
        "Record whether the missing route is image, near-shape, source, or context.",
        "\u8bb0\u5f55\u7f3a\u53e3\u5c5e\u4e8e\u56fe\u50cf\u3001"
        "\u8fd1\u5f62\u3001\u6765\u6e90\u8fd8\u662f\u4e0a\u4e0b\u6587\u8def\u7ebf\u3002",
    ]
    question_lines = "\n".join(
        line for item in questions for line in wrapped_bullet(item)
    )
    comparison_order = "\n".join(
        line
        for item in human_component_comparison_order_items()
        for line in wrapped_bullet(item)
    )
    lines = [
        (
            "# Human Component Candidate Dossier / "
            f"\u6784\u4ef6\u5019\u9009\u7814\u7a76\u6863\u6848: {component_id}"
        ),
        "",
        "English:",
        intro_en,
        "",
        "\u7b80\u4f53\u4e2d\u6587\uff1a",
        intro_zh,
        "",
        "## Human Comparison Order / \u4eba\u5de5\u6bd4\u8f83\u987a\u5e8f",
        "",
        comparison_order,
        "",
        "## Candidate Identity / \u5019\u9009\u8eab\u4efd",
        "",
        f"- candidate_component_id: `{component_id}`",
        f"- primary_external_ref_id: `{main_row['subcharacter_external_ref_id']}`",
        f"- source_subcharacter_uid: `{main_row['source_subcharacter_uid']}`",
        f"- source_main_character_uid: `{main_row['source_main_character_uid']}`",
        f"- main_character_external_ref_id: `{main_row['main_character_external_ref_id']}`",
        "- object_directory: see `12_component-dossier-index.json`",
        "",
        "## Glyph Image Observation / \u5b57\u5f62\u56fe\u50cf\u89c2\u5bdf",
        "",
        f"- local_image_status: `{local_status}`",
        f"- visual_asset_count: `{visual_count}`",
        f"- glyph_codepoint_count: `{glyph_count}`",
        f"- glyph_codepoint_uplus_sample: `{glyph_sample}`",
        "- full_glyph_codepoint_list: see `03_glyph-codepoint-index.csv`",
        "",
        "| Asset ID | Local image file | SHA-256 |",
        "| --- | --- | --- |",
        visual_paths,
        "",
        (
            "## Near-Shape And Variant Review / "
            "\u8fd1\u5f62\u4e0e\u5f02\u4f53\u590d\u6838"
        ),
        "",
        wrap_markdown_line(
            "No near-shape or variant judgment is made here. Reviewers should "
            "compare the local image, glyph-codepoint clues, and independent "
            "component sources before promoting any relationship."
        ),
        "",
        wrap_markdown_line(
            "\u6b64\u5904\u4e0d\u4f5c\u8fd1\u5f62\u6216\u5f02\u4f53"
            "\u5224\u65ad\u3002\u590d\u6838\u8005\u5e94\u5148\u6bd4\u8f83"
            "\u672c\u5730\u56fe\u50cf\u3001glyph-codepoint \u7ebf\u7d22"
            "\u548c\u72ec\u7acb\u6784\u4ef6\u6765\u6e90\uff0c\u518d\u51b3\u5b9a"
            "\u662f\u5426\u63d0\u5347\u5173\u7cfb\u3002"
        ),
        "",
        (
            "## Character And Inscription Routes / "
            "\u7532\u9aa8\u5355\u5b57\u4e0e\u535c\u8f9e\u8def\u7ebf"
        ),
        "",
        wrap_markdown_line(
            "Open the object-local indexes and graph edges to trace possible "
            "oracle character, inscription, and source routes. These routes "
            "are lookup aids only."
        ),
        "",
        "- `03_glyph-codepoint-index.csv`",
        "- `04_glyph-codepoint-gallery.md`",
        "- `09_component-visual-route-index.csv`",
        "- `10_component-visual-route-gallery.md`",
        "",
        (
            "## Source Evidence And Rights Trail / "
            "\u6765\u6e90\u8bc1\u636e\u4e0e\u6743\u5229\u94fe"
        ),
        "",
        f"- source_id: `{main_row['source_id']}`",
        f"- evidence_download_id: `{main_row['evidence_download_id']}`",
        f"- source_metadata_file: `{main_row['source_metadata_file']}`",
        f"- rights_status: `{RIGHTS_STATUS}`",
        f"- review_status: `{REVIEW_STATUS}`",
        "",
        (
            "## Missing Evidence And Next Checks / "
            "\u7f3a\u5931\u8bc1\u636e\u4e0e\u4e0b\u4e00\u6b65"
        ),
        "",
        "- near_shape_and_variant_comparison",
        "- oracle_character_context",
        "- inscription_occurrence_context",
        "- published_component_history",
        "- reading_history_and_disputes",
        "",
        (
            "## Concrete Questions To Check / "
            "\u5177\u4f53\u5f85\u67e5\u95ee\u9898"
        ),
        "",
        question_lines,
        "",
        "## Review Boundary / \u590d\u6838\u8fb9\u754c",
        "",
        boundary,
    ]
    return "\n".join(lines) + "\n"


def human_component_comparison_order_items() -> list[str]:
    return [
        "Open `11_human-component-dossier.md` before route tables.",
        "Compare glyph images before graph or CSV routes.",
        "Open `13_component-context-evidence-dossier.md` before context use.",
        "Do not promote graph or visual routes into component assignments.",
        (
            "\u5148\u6253\u5f00 11_human-component-dossier.md\uff0c"
            "\u518d\u4f7f\u7528\u8def\u7ebf\u8868\u3002"
        ),
        (
            "\u5148\u6bd4\u8f83\u5b57\u5f62\u56fe\u50cf\uff0c"
            "\u518d\u67e5\u56fe\u8fb9\u6216 CSV \u8def\u7ebf\u3002"
        ),
        (
            "\u4e0d\u5f97\u628a\u56fe\u8fb9\u6216\u56fe\u50cf\u8def\u7ebf"
            "\u63d0\u5347\u4e3a\u6784\u4ef6\u5f52\u5c5e\u3002"
        ),
    ]


def component_dossier_index_payload(
    index: int,
    main_row: dict[str, str],
    directory: Path,
) -> dict[str, object]:
    human_readable_files = [
        (directory / "README.md").as_posix(),
        (directory / "04_glyph-codepoint-gallery.md").as_posix(),
        (directory / "07_component-visual-gallery.md").as_posix(),
        (directory / "08_human-visual-review-sheet.md").as_posix(),
        (directory / "10_component-visual-route-gallery.md").as_posix(),
        (directory / "11_human-component-dossier.md").as_posix(),
        (directory / "13_component-context-evidence-dossier.md").as_posix(),
        (directory / "15_component-review-fact-matrix.md").as_posix(),
        (directory / "16_component-research-readiness-review.md").as_posix(),
    ]
    if has_material_visual_observation(index):
        human_readable_files.append(
            (directory / "18_material-visual-observation.md").as_posix()
        )
    return {
        "candidate_component_id": candidate_id(index),
        "record_type": "graphemic_component_candidate_dossier_index",
        "primary_external_ref_id": main_row["subcharacter_external_ref_id"],
        "human_readable_files": human_readable_files,
        "ai_support_files": [
            (directory / "01_candidate-component-packet.json").as_posix(),
            (directory / "02_component-source-index.csv").as_posix(),
            (directory / "03_glyph-codepoint-index.csv").as_posix(),
            (directory / "06_component-visual-index.csv").as_posix(),
            (directory / "09_component-visual-route-index.csv").as_posix(),
            (directory / "12_component-dossier-index.json").as_posix(),
            (directory / "14_component-context-evidence-index.json").as_posix(),
            (directory / "17_component-research-readiness-index.json").as_posix(),
        ],
        "source_route_files": route_files(directory, index),
        "uncollected_human_research_fields": [
            "near_shape_and_variant_comparison",
            "oracle_character_context",
            "inscription_occurrence_context",
            "published_component_history",
            "reading_history_and_disputes",
        ],
        "claim_boundary": (
            "no formal component assignment; no confirmed component form; "
            "no oracle-character identity; no decipherment conclusion"
        ),
        "rights_status": RIGHTS_STATUS,
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def short_join(values: list[str], limit: int = 2) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return "待查"
    shown = cleaned[:limit]
    suffix = f"; 另有 {len(cleaned) - limit} 项" if len(cleaned) > limit else ""
    return "; ".join(shown) + suffix


def component_context_dossier_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> str:
    component_id = candidate_id(index)
    glyph_values = sorted(
        {row.get("glyph_codepoint_uplus", "") for row in glyph_rows if row}
    )
    visual_assets = sorted(
        {row.get("asset_id", "") for row in visual_rows if row.get("asset_id")}
    )
    zip_members = sorted(
        {
            Path(row.get("source_zip_member", "")).name
            for row in visual_rows
            if row.get("source_zip_member")
        }
    )
    route_types = sorted(
        {row.get("route_type", "") for row in route_rows if row.get("route_type")}
    )
    lines = [
        f"# {component_id} 构件候选上下文复核档案",
        "",
        wrap_markdown_line(
            "本文件是构件候选对象目录内的人类可读复核入口。它把图像、"
            "glyph-codepoint、近形异体比较、单字卜辞上下文、来源权利"
            "和 manifest 待查路线集中到同一个对象目录。"
        ),
        "",
        wrap_markdown_line(
            "This dossier is a context review entrance for one component "
            "candidate. It gathers object-local evidence routes without "
            "promoting any route into a formal component assignment."
        ),
        "",
        wrap_markdown_line(
            "边界提示：这里记录的是候选路线，不是构件归属结论，"
            "不是单字身份结论，也不是释读结论。"
        ),
        "",
        "## 1. 候选身份与来源",
        "",
        f"- 构件候选 ID: `{component_id}`",
        f"- 首选外部 ID: `{main_row['subcharacter_external_ref_id']}`",
        f"- OBIMD subcharacter UID: `{main_row['source_subcharacter_uid']}`",
        f"- OBIMD main character UID: `{main_row['source_main_character_uid']}`",
        f"- 来源 ID: `{main_row['source_id']}`",
        f"- 下载记录: `{main_row['evidence_download_id']}`",
        f"- 复核状态: `{REVIEW_STATUS}`",
        f"- 权利状态: `{RIGHTS_STATUS}`",
        "",
        "## 2. 字形图片与构件观察",
        "",
        f"- 本地图像数: `{len(visual_rows)}`",
        f"- 视觉资产示例: {short_join(visual_assets)}",
        f"- 来源 zip 成员示例: {short_join(zip_members)}",
        "- 图像入口: `07_component-visual-gallery.md`",
        "- 图像索引: `06_component-visual-index.csv`",
        "- 图像路线: `09_component-visual-route-index.csv`",
        "",
        wrap_markdown_line(
            "构件观察必须先回到图像和来源行；任何形体、笔画、残缺、"
            "方向、比例或拆分判断都只能记为待复核观察，不能写成归属。"
        ),
        "",
        "## 3. 近形、异体与变体比较",
        "",
        f"- glyph-codepoint 数: `{len(glyph_rows)}`",
        f"- codepoint 示例: {short_join(glyph_values)}",
        f"- 路线类型: {short_join(route_types)}",
        "- codepoint 入口: `03_glyph-codepoint-index.csv`",
        "- codepoint 图页: `04_glyph-codepoint-gallery.md`",
        "",
        wrap_markdown_line(
            "近形、异体和变体比较需要独立来源互证。OBIMD 子构件关系、"
            "PUA 码位或图像相似性都只是候选线索。"
        ),
        "",
        "## 4. 单字、卜辞与上下文路线",
        "",
        "- 单字路线: 待查，先开 `corpus/001_oracle-characters/` 互证。",
        "- 卜辞路线: 待查，先开 `corpus/002_oracle-bone-inscriptions/`。",
        "- 字位上下文: 待查，先开 `11_human-component-dossier.md` 及卜辞候选档案。",
        "- 图边文件: `006_obimd-component-graph-edges.jsonl`",
        "",
        wrap_markdown_line(
            "构件候选不能单独证明某个甲骨单字的结构。必须先打开相关"
            "单字、卜辞、图版和著录路线，记录证据来源和复核状态。"
        ),
        "",
        "## 5. 来源证据、权利与 manifest",
        "",
        f"- source_metadata_file: `{main_row['source_metadata_file']}`",
        "- source package: `dl-obimd-subcharacter-images`",
        "- checksum: 见 `06_component-visual-index.csv`。",
        "- manifest: 见本 bucket 的 `000_obimd-component-candidate-bucket-manifest.csv`。",
        "- 权利复核: 见 asset rights index 和 review log。",
        "",
        "## 6. 具体待查问题",
        "",
        "- 需要比较哪些近形、异体或变体图像？",
        "- 哪些单字、卜辞、图版或著录路线需要先打开？",
        "- 哪些 glyph-codepoint 只是 PUA 或字体依赖线索？",
        "- 哪个 source zip member、checksum 和 asset 权利记录支持图像？",
        "- 哪些构件候选路线需要与独立来源互证？",
        "- 正式构件归属前还缺哪些图像、卜辞、文献或来源证据？",
        "",
        "## 7. 本目录应先打开的文件",
        "",
        "- `README.md`",
        "- `04_glyph-codepoint-gallery.md`",
        "- `07_component-visual-gallery.md`",
        "- `08_human-visual-review-sheet.md`",
        "- `11_human-component-dossier.md`",
        "- `13_component-context-evidence-dossier.md`",
        "- `01_candidate-component-packet.json`",
        "- `12_component-dossier-index.json`",
        "- `14_component-context-evidence-index.json`",
        "",
        "## 8. 复核边界",
        "",
        wrap_markdown_line(
            "本档案只服务预处理阶段的资料核查。任何构件命名、构件归属、"
            "单字结构、卜辞身份或释读意见，都必须在正式研究阶段另行"
            "人工复核后才能记录为学术说明。"
        ),
    ]
    text = "\n".join(lines).rstrip() + "\n"
    assert_human_line_width(text, f"{component_id}/13_component-context-evidence-dossier.md")
    return text


def component_context_index_payload(
    index: int,
    main_row: dict[str, str],
    directory: Path,
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> dict[str, object]:
    human_readable_files = [
        "README.md",
        "04_glyph-codepoint-gallery.md",
        "07_component-visual-gallery.md",
        "08_human-visual-review-sheet.md",
        "11_human-component-dossier.md",
        "13_component-context-evidence-dossier.md",
        "15_component-review-fact-matrix.md",
        "16_component-research-readiness-review.md",
    ]
    if has_material_visual_observation(index):
        human_readable_files.append("18_material-visual-observation.md")
    return {
        "candidate_component_id": candidate_id(index),
        "record_type": "component_context_evidence_dossier_index",
        "primary_external_ref_id": main_row["subcharacter_external_ref_id"],
        "updated_at": UPDATED_AT,
        "human_readable_files": human_readable_files,
        "ai_support_files": [
            "01_candidate-component-packet.json",
            "03_glyph-codepoint-index.csv",
            "06_component-visual-index.csv",
            "09_component-visual-route-index.csv",
            "12_component-dossier-index.json",
            "14_component-context-evidence-index.json",
            "17_component-research-readiness-index.json",
        ],
        "source_summary": {
            "source_id": main_row["source_id"],
            "evidence_download_id": main_row["evidence_download_id"],
            "source_metadata_file": main_row["source_metadata_file"],
            "source_subcharacter_uid": main_row["source_subcharacter_uid"],
            "source_main_character_uid": main_row["source_main_character_uid"],
        },
        "route_counts": {
            "glyph_codepoint_rows": len(glyph_rows),
            "visual_asset_rows": len(visual_rows),
            "visual_route_rows": len(route_rows),
        },
        "missing_or_review_fields": [
            "near_shape_variant_and_component_comparison_to_check",
            "oracle_character_and_inscription_context_to_check",
            "source_manifest_checksum_and_rights_to_check",
            "published_component_history_and_disputes_to_check",
        ],
        "claim_boundary": (
            "context_routes_only_not_component_assignment_not_decipherment"
        ),
    }


def component_review_fact_matrix_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> str:
    component_id = candidate_id(index)
    local_image_status = (
        "source_image_extracted"
        if visual_rows
        else "not_found_in_registered_source_package_route_indexed"
    )
    codepoint_summary = short_join(
        sorted({row.get("glyph_codepoint_uplus", "") for row in glyph_rows})
    )
    fact_rows = [
        (
            "Component candidate / 构件候选",
            "dataset candidate only; no component assignment",
            "01_candidate-component-packet.json; 11_human-component-dossier.md",
        ),
        (
            "Glyph or codepoint route / 字形或码位路线",
            f"{len(glyph_rows)} OBIMD route rows; examples {codepoint_summary}",
            "03_glyph-codepoint-index.csv; 04_glyph-codepoint-gallery.md",
        ),
        (
            "Local visual evidence / 本地视觉证据",
            f"{len(visual_rows)} local image rows; {local_image_status}",
            "06_component-visual-index.csv; 07_component-visual-gallery.md",
        ),
        (
            "Visual package route / 视觉包路线",
            f"{len(route_rows)} route rows from package and local indexes",
            "09_component-visual-route-index.csv; 10_component-visual-route-gallery.md",
        ),
        (
            "Near-shape and variant review / 近形与异体复核",
            "pending comparison against independent visual evidence",
            "11_human-component-dossier.md; 13_component-context-evidence-dossier.md",
        ),
        (
            "Character and inscription context / 单字与卜辞上下文",
            "pending oracle-character, inscription, and plate context review",
            "13_component-context-evidence-dossier.md; 14_component-context-evidence-index.json",
        ),
        (
            "Meaning or reading status / 字义或释读状态",
            "no confirmed meaning or reading; keep \u91ca\u8bfb as a review question",
            "11_human-component-dossier.md; 13_component-context-evidence-dossier.md",
        ),
        (
            "Scholarship and dispute route / 学术史与争议路线",
            "check \u91ca\u8bfb\u53f2, dispute, and \u4e89\u8bae before any claim",
            "research/; 13_component-context-evidence-dossier.md",
        ),
        (
            "Findspot collection period route / 出土地馆藏时期路线",
            "check findspot, collection, period, \u51fa\u571f, \u9986\u85cf, \u65f6\u671f, and \u7ec4\u7c7b",
            "corpus/005_excavation-sites-periods-and-batches/; project_registry/",
        ),
        (
            "Source and rights trail / 来源与权利链",
            f"{main_row['source_id']}; rights {RIGHTS_STATUS}",
            "02_component-source-index.csv; project_registry/",
        ),
        (
            "Missing evidence route / 缺失证据路线",
            "record whether the gap is image, near-shape, source, or context",
            "08_human-visual-review-sheet.md; 13_component-context-evidence-dossier.md",
        ),
        (
            "Review status / 复核状态",
            REVIEW_STATUS,
            "12_component-dossier-index.json; 14_component-context-evidence-index.json",
        ),
    ]
    table = "\n".join(
        f"| {fact} | {status} | {evidence} |"
        for fact, status, evidence in fact_rows
    )
    intro = wrap_markdown_line(
        "This human-readable matrix gives a compact review order for one "
        "OBIMD component candidate. It keeps glyph-codepoint, image, source, "
        "near-shape, character-context, and rights routes together without "
        "promoting any route into a formal component assignment."
    )
    intro_zh = wrap_markdown_line(
        "\u672c\u77e9\u9635\u4e3a\u4e00\u4e2a OBIMD \u6784\u4ef6"
        "\u5019\u9009\u5bf9\u8c61\u63d0\u4f9b\u7b80\u660e\u7684\u4eba\u5de5"
        "\u590d\u6838\u987a\u5e8f\uff0c\u628a codepoint\u3001\u56fe\u50cf\u3001"
        "\u6765\u6e90\u3001\u8fd1\u5f62\u548c\u4e0a\u4e0b\u6587\u8def\u7ebf"
        "\u653e\u5728\u540c\u4e00\u5bf9\u8c61\u76ee\u5f55\u5185\u3002"
    )
    questions = "\n".join(
        line
        for item in [
            "Open the component dossier before using any CSV route.",
            "Open visual indexes and galleries before comparing shapes.",
            "Check codepoints as dataset routes, not confirmed component forms.",
            "Open context dossiers before linking a character or inscription.",
            "Record the concrete missing route before any formal assignment.",
            (
                "\u5148\u6253\u5f00\u6784\u4ef6\u6863\u6848\uff0c"
                "\u518d\u4f7f\u7528 CSV \u8def\u7ebf\u3002"
            ),
            (
                "\u8054\u7cfb\u5355\u5b57\u6216\u535c\u8f9e\u524d\uff0c"
                "\u5148\u6253\u5f00\u4e0a\u4e0b\u6587\u6863\u6848\u3002"
            ),
        ]
        for line in wrapped_bullet(item)
    )
    comparison_order = "\n".join(
        line
        for item in human_component_comparison_order_items()
        for line in wrapped_bullet(item)
    )
    lines = [
        f"# Component Review Fact Matrix / \u6784\u4ef6\u590d\u6838\u4e8b\u5b9e\u77e9\u9635: {component_id}",
        "",
        "English:",
        intro,
        "",
        "\u7b80\u4f53\u4e2d\u6587\uff1a",
        intro_zh,
        "",
        "## Human Review Order / \u4eba\u5de5\u590d\u6838\u987a\u5e8f",
        "",
        "- Open `15_component-review-fact-matrix.md` first.",
        "- Then open `11_human-component-dossier.md`.",
        "- Open `13_component-context-evidence-dossier.md` before context use.",
        "- Use structured route files only as secondary route support.",
        "- 结构化路线文件只作检索、追溯和复核辅助。",
        "",
        (
            "## Component Candidate Review Fact Matrix / "
            "\u6784\u4ef6\u5019\u9009\u590d\u6838\u77e9\u9635"
        ),
        "",
        "| Fact / 项目 | Current status / 当前状态 | Local evidence to open / 需打开的本地证据 |",
        "| --- | --- | --- |",
        table,
        "",
        "## Human Comparison Order / \u4eba\u5de5\u6bd4\u8f83\u987a\u5e8f",
        "",
        comparison_order,
        "",
        "## Concrete Review Questions / \u5177\u4f53\u590d\u6838\u95ee\u9898",
        "",
        questions,
        "",
        "## Review Boundary / \u590d\u6838\u8fb9\u754c",
        "",
        "- not a confirmed graphemic component",
        "- not a formal component assignment",
        "- not an oracle-character identity",
        "- not a decipherment conclusion",
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(text, f"{component_id}/15_component-review-fact-matrix.md")
    return text


def component_readiness_slots(
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    local_image_status = (
        "source_image_extracted"
        if visual_rows
        else "not_found_in_registered_source_package_route_indexed"
    )
    return [
        {
            "slot": "candidate_identity",
            "status": "dataset_candidate_only",
            "human_file": "11_human-component-dossier.md",
            "question": "Which OBIMD subcharacter route identifies this candidate?",
        },
        {
            "slot": "visual_evidence",
            "status": local_image_status,
            "human_file": "07_component-visual-gallery.md",
            "question": "Which local image row must be opened before comparison?",
        },
        {
            "slot": "glyph_codepoint_routes",
            "status": f"{len(glyph_rows)} glyph-codepoint route rows",
            "human_file": "04_glyph-codepoint-gallery.md",
            "question": "Which codepoint clues are dataset routes only?",
        },
        {
            "slot": "visual_route_integrity",
            "status": f"{len(route_rows)} visual route rows",
            "human_file": "10_component-visual-route-gallery.md",
            "question": "Which package, index, or image route needs review?",
        },
        {
            "slot": "near_shape_variant_context",
            "status": "pending independent comparison",
            "human_file": "13_component-context-evidence-dossier.md",
            "question": "Which near-shape or variant route needs human comparison?",
        },
        {
            "slot": "character_inscription_context",
            "status": "pending character and inscription route review",
            "human_file": "13_component-context-evidence-dossier.md",
            "question": "Which character, inscription, or plate route must be opened?",
        },
        {
            "slot": "source_rights_manifest",
            "status": "source and rights routes present for review",
            "human_file": "15_component-review-fact-matrix.md",
            "question": "Which manifest, checksum, field map, or rights row applies?",
        },
        {
            "slot": "formal_research_blockers",
            "status": "formal component assignment blocked pending review",
            "human_file": "16_component-research-readiness-review.md",
            "question": "What evidence is still missing before formal research?",
        },
    ]


def component_research_readiness_review_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> str:
    component_id = candidate_id(index)
    slots = component_readiness_slots(glyph_rows, visual_rows, route_rows)
    slot_lines = "\n".join(
        line
        for slot in slots
        for line in wrapped_bullet(
            f"{slot['slot']}: {slot['status']} -> {slot['human_file']}"
        )
    )
    questions = [
        "Which source image row can be opened before comparing shape?",
        "Which glyph-codepoint row is only dataset routing metadata?",
        "Which near-shape, variant, or host-character route is still pending?",
        "Which inscription, plate, findspot, collection, or period route is missing?",
        "Which source package, checksum, field map, rights note, and risk note apply?",
        "Which bibliography, proposer, reading history, or dispute remains missing?",
        (
            "\u5148\u6253\u5f00\u54ea\u4e00\u6761\u6765\u6e90\u56fe\u50cf"
            "\u8bb0\u5f55\u540e\u624d\u80fd\u6bd4\u8f83\u5b57\u5f62\uff1f"
        ),
        (
            "\u54ea\u4e00\u6761 glyph-codepoint \u8bb0\u5f55\u53ea\u662f"
            "\u6570\u636e\u96c6\u8def\u7531 metadata\uff1f"
        ),
        (
            "\u54ea\u4e9b\u8fd1\u5f62\u3001\u5f02\u4f53\u6216\u4e3b\u5b57"
            "\u8def\u7ebf\u4ecd\u7136\u5f85\u590d\u6838\uff1f"
        ),
        (
            "\u8fd8\u7f3a\u54ea\u4e00\u6761\u535c\u8f9e\u3001\u56fe\u7248\u3001"
            "\u51fa\u571f\u5730\u3001\u9986\u85cf\u6216\u65f6\u671f\u8def\u7ebf\uff1f"
        ),
    ]
    question_lines = "\n".join(
        line
        for question in questions
        for line in wrapped_bullet(question)
    )
    lines = [
        f"# Component Research Readiness Review / \u6784\u4ef6\u7814\u7a76\u5c31\u7eea\u590d\u6838: {component_id}",
        "",
        "English:",
        wrap_markdown_line(
            "This human-readable review gathers the object-local evidence a "
            "researcher must inspect before any formal component research. "
            "It summarizes images, codepoint routes, context routes, source "
            "provenance, rights evidence, and concrete missing questions."
        ),
        "",
        "\u7b80\u4f53\u4e2d\u6587\uff1a",
        wrap_markdown_line(
            "\u672c\u590d\u6838\u9875\u6c47\u603b\u6b63\u5f0f\u6784\u4ef6"
            "\u7814\u7a76\u524d\u5fc5\u987b\u6253\u5f00\u7684\u5bf9\u8c61\u5185"
            "\u8bc1\u636e\uff1a\u56fe\u50cf\u3001\u7801\u4f4d\u8def\u7ebf\u3001"
            "\u4e0a\u4e0b\u6587\u3001\u6765\u6e90\u3001\u6743\u5229\u8bb0\u5f55"
            "\u548c\u5177\u4f53\u5f85\u67e5\u95ee\u9898\u3002"
        ),
        "",
        "## Human Reading Order / \u4eba\u5de5\u9605\u8bfb\u987a\u5e8f",
        "",
        "- Open `11_human-component-dossier.md` first.",
        "- Open `13_component-context-evidence-dossier.md` before context use.",
        "- Open `15_component-review-fact-matrix.md` for source and rights facts.",
        "- Use JSON and CSV only after the human files are clear.",
        (
            "- \u5148\u8bfb\u4eba\u7c7b\u6863\u6848\uff0c\u518d\u4f7f\u7528"
            "\u7ed3\u6784\u5316\u8def\u7ebf\u6587\u4ef6\u3002"
        ),
        "",
        "## Readiness Slots / \u5c31\u7eea\u590d\u6838\u69fd\u4f4d",
        "",
        slot_lines,
        "",
        "## Concrete Questions Before Formal Research / \u6b63\u5f0f\u7814\u7a76\u524d\u5f85\u67e5\u95ee\u9898",
        "",
        question_lines,
        "",
        "## Boundary / \u8fb9\u754c",
        "",
        "- not a confirmed graphemic component",
        "- not a formal component assignment",
        "- not an oracle-character identity claim",
        "- not a decipherment conclusion",
        (
            "- \u8fd9\u662f\u9884\u5904\u7406\u590d\u6838\u9875\uff0c"
            "\u4e0d\u662f\u5b66\u672f\u7ed3\u8bba\u3002"
        ),
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        text,
        f"{component_id}/16_component-research-readiness-review.md",
    )
    return text


def component_research_readiness_index_payload(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    visual_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> dict[str, object]:
    human_readable_files = [
        "11_human-component-dossier.md",
        "13_component-context-evidence-dossier.md",
        "15_component-review-fact-matrix.md",
        "16_component-research-readiness-review.md",
    ]
    if has_material_visual_observation(index):
        human_readable_files.append("18_material-visual-observation.md")
    return {
        "candidate_component_id": candidate_id(index),
        "record_type": "component_research_readiness_index",
        "primary_external_ref_id": main_row["subcharacter_external_ref_id"],
        "human_entry": "16_component-research-readiness-review.md",
        "human_readable_files": human_readable_files,
        "support_files": [
            "01_candidate-component-packet.json",
            "03_glyph-codepoint-index.csv",
            "06_component-visual-index.csv",
            "09_component-visual-route-index.csv",
            "14_component-context-evidence-index.json",
            "17_component-research-readiness-index.json",
        ],
        "readiness_slots": component_readiness_slots(
            glyph_rows,
            visual_rows,
            route_rows,
        ),
        "claim_boundary": (
            "no confirmed component form; no formal component assignment; "
            "no oracle-character identity claim; no decipherment conclusion"
        ),
        "review_status": REVIEW_STATUS,
        "updated_at": UPDATED_AT,
    }


def assert_human_line_width(text: str, label: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("|") or line.startswith("!["):
            continue
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(f"{label}:{line_number} exceeds 80 chars: {line}")


def build_outputs(root: Path) -> dict[str, dict[str, object]]:
    main_rows = read_csv_rows(root / SUBCHARACTER_MAIN_STAGING)
    glyph_by_uid: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv_rows(root / SUBCHARACTER_GLYPH_STAGING):
        glyph_by_uid[row["source_subcharacter_uid"]].append(row)
    outputs: dict[str, dict[str, object]] = {}
    for index, main_row in enumerate(main_rows, start=1):
        project_id = candidate_id(index)
        directory = object_dir(index, main_row["subcharacter_external_ref_id"])
        full_directory = root / directory
        glyph_rows = glyph_by_uid[main_row["source_subcharacter_uid"]]
        visual_rows = read_csv_rows(full_directory / "06_component-visual-index.csv")
        route_rows = read_csv_rows(full_directory / "09_component-visual-route-index.csv")
        outputs[project_id] = {
            "object_dir": full_directory,
            "context_dossier_path": full_directory / "13_component-context-evidence-dossier.md",
            "context_index_path": full_directory / "14_component-context-evidence-index.json",
            "fact_matrix_path": full_directory / "15_component-review-fact-matrix.md",
            "readiness_review_path": full_directory / "16_component-research-readiness-review.md",
            "readiness_index_path": full_directory / "17_component-research-readiness-index.json",
            "context_dossier_text": component_context_dossier_text(
                index,
                main_row,
                glyph_rows,
                visual_rows,
                route_rows,
            ),
            "fact_matrix_text": component_review_fact_matrix_text(
                index,
                main_row,
                glyph_rows,
                visual_rows,
                route_rows,
            ),
            "context_index": component_context_index_payload(
                index,
                main_row,
                directory,
                glyph_rows,
                visual_rows,
                route_rows,
            ),
            "readiness_review_text": component_research_readiness_review_text(
                index,
                main_row,
                glyph_rows,
                visual_rows,
                route_rows,
            ),
            "readiness_index": component_research_readiness_index_payload(
                index,
                main_row,
                glyph_rows,
                visual_rows,
                route_rows,
            ),
        }
    return outputs


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
            route_rows = visual_route_rows(index, main_row, visual_rows, directory)

            if has_material_visual_observation(index):
                (full_directory / "18_material-visual-observation.md").write_text(
                    material_visual_observation_text(
                        index,
                        main_row,
                        visual_rows,
                        directory,
                    ),
                    encoding="utf-8",
                )
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
                route_rows,
                VISUAL_ROUTE_FIELDS,
            )
            (full_directory / "10_component-visual-route-gallery.md").write_text(
                visual_route_gallery_text(index, main_row, visual_rows, directory),
                encoding="utf-8",
            )
            (full_directory / "11_human-component-dossier.md").write_text(
                component_dossier_text(
                    index,
                    main_row,
                    glyph_rows,
                    visual_rows,
                    directory,
                ),
                encoding="utf-8",
            )
            (full_directory / "12_component-dossier-index.json").write_text(
                json.dumps(
                    component_dossier_index_payload(index, main_row, directory),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            (full_directory / "13_component-context-evidence-dossier.md").write_text(
                component_context_dossier_text(
                    index,
                    main_row,
                    glyph_rows,
                    visual_rows,
                    route_rows,
                ),
                encoding="utf-8",
            )
            (full_directory / "14_component-context-evidence-index.json").write_text(
                json.dumps(
                    component_context_index_payload(
                        index,
                        main_row,
                        directory,
                        glyph_rows,
                        visual_rows,
                        route_rows,
                    ),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            (full_directory / "15_component-review-fact-matrix.md").write_text(
                component_review_fact_matrix_text(
                    index,
                    main_row,
                    glyph_rows,
                    visual_rows,
                    route_rows,
                ),
                encoding="utf-8",
            )
            (full_directory / "16_component-research-readiness-review.md").write_text(
                component_research_readiness_review_text(
                    index,
                    main_row,
                    glyph_rows,
                    visual_rows,
                    route_rows,
                ),
                encoding="utf-8",
            )
            (full_directory / "17_component-research-readiness-index.json").write_text(
                json.dumps(
                    component_research_readiness_index_payload(
                        index,
                        main_row,
                        glyph_rows,
                        visual_rows,
                        route_rows,
                    ),
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
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
