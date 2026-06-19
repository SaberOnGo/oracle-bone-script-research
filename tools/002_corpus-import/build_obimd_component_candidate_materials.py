#!/usr/bin/env python3
"""Build object-local candidate materials for OBIMD subcharacters.

The output is preprocessing infrastructure only. Each object is a dataset
candidate package, not a formal component record or component assignment.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


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
UPDATED_AT = "2026-06-20"
BUCKET_SIZE = 100
RECORD_TYPE = "graphemic_component_candidate"
OBJECT_STATUS = "dataset_candidate_not_promoted"
REVIEW_STATUS = "needs_human_component_review"
RIGHTS_STATUS = "licensed_for_repository"
RESEARCH_BOUNDARY = (
    "dataset_component_candidate_only_not_formal_component_record_not_component_assignment"
)
CAUTION = (
    "OBIMD subcharacter metadata is useful for routing component review, but this "
    "object is not a confirmed graphemic component, not a component breakdown, and "
    "not a decipherment or oracle-character identity claim."
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
        "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
        (directory / "02_component-source-index.csv").as_posix(),
        (directory / "03_glyph-codepoint-index.csv").as_posix(),
        (directory / "04_glyph-codepoint-gallery.md").as_posix(),
    ]


def packet_payload(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
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


def readme_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
    directory: Path,
) -> str:
    component_id = candidate_id(index)
    return f"""# {component_id} / OBIMD Subcharacter Candidate

English:
This directory is the object-local research entrance for one OBIMD subcharacter candidate. It contains human-readable notes and AI-readable indexes in the same concrete corpus object directory.

Simplified Chinese:
本目录是一个 OBIMD subcharacter 候选对象的本地研究入口；人类可读资料和 AI 可读索引放在同一个具体 corpus 对象目录中。

## Boundary / 边界

English:
This is not a confirmed graphemic component, not a component breakdown, not an oracle-character identity claim, and not a decipherment conclusion. It is a source-marked dataset candidate awaiting human component review.

简体中文：
这不是已确认构件，不是构件拆分结论，不是甲骨字身份判断，也不是释读结论；它只是带来源标记、等待人工复核的数据库候选对象。

## Source Snapshot / 来源快照

- candidate_component_id: `{component_id}`
- candidate_subcharacter_id: `{main_row["candidate_subcharacter_id"]}`
- primary_external_ref_id: `{main_row["subcharacter_external_ref_id"]}`
- source_subcharacter_uid: `{main_row["source_subcharacter_uid"]}`
- source_main_character_uid: `{main_row["source_main_character_uid"]}`
- main_character_external_ref_id: `{main_row["main_character_external_ref_id"]}`
- glyph_codepoint_link_count: `{len(glyph_rows)}`
- rights_status: `{RIGHTS_STATUS}`
- review_status: `{REVIEW_STATUS}`

## Local Files / 本地文件

- `01_candidate-component-packet.json`: AI-readable candidate packet.
- `02_component-source-index.csv`: source, download, rights, and review index.
- `03_glyph-codepoint-index.csv`: OBIMD glyph-codepoint links for review.
- `04_glyph-codepoint-gallery.md`: human-readable glyph/codepoint gallery.

## Next Review / 下一步复核

English:
Review the OBIMD hierarchy and glyph-codepoint links against independent component, character, and inscription evidence before promoting any formal component record or graph relation.

简体中文：
在提升为正式构件记录或正式图谱关系前，需要把 OBIMD 层级和 glyph codepoint 线索同独立的构件、单字和卜辞证据交叉复核。

Route files / 路由文件:

{chr(10).join(f"- `{path}`" for path in route_files(directory))}
"""


def gallery_text(
    index: int,
    main_row: dict[str, str],
    glyph_rows: list[dict[str, str]],
) -> str:
    component_id = candidate_id(index)
    lines = [
        f"# Glyph Codepoint Gallery / 字形码位查看: {component_id}",
        "",
        "English:",
        "This page is a human-readable review surface for OBIMD glyph-codepoint metadata. Some codepoints are private-use values and may not render in every font.",
        "",
        "简体中文：",
        "本页用于人工查看 OBIMD glyph-codepoint metadata。部分码位属于私用区，可能无法在所有字体中正确显示。",
        "",
        "Boundary / 边界：dataset candidate only; not a confirmed component image, component assignment, or decipherment claim.",
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


def build_materials(root: Path) -> tuple[int, int]:
    main_rows = read_csv_rows(root / SUBCHARACTER_MAIN_STAGING)
    glyph_by_uid: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv_rows(root / SUBCHARACTER_GLYPH_STAGING):
        glyph_by_uid[row["source_subcharacter_uid"]].append(row)

    manifest_by_bucket: dict[Path, list[dict[str, str]]] = defaultdict(list)
    component_map_rows: list[dict[str, str]] = []

    for index, main_row in enumerate(main_rows, start=1):
        glyph_rows = glyph_by_uid[main_row["source_subcharacter_uid"]]
        directory = object_dir(index, main_row["subcharacter_external_ref_id"])
        full_directory = root / directory
        full_directory.mkdir(parents=True, exist_ok=True)

        (full_directory / "README.md").write_text(
            readme_text(index, main_row, glyph_rows, directory),
            encoding="utf-8",
        )
        (full_directory / "01_candidate-component-packet.json").write_text(
            json.dumps(
                packet_payload(index, main_row, glyph_rows, directory),
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
        manifest_by_bucket[bucket_dir(index)].append(
            manifest_row(index, main_row, glyph_rows, directory)
        )
        component_map_rows.append(component_map_row(index, main_row, directory))

    for bucket, rows in manifest_by_bucket.items():
        write_csv(root / bucket / "000_obimd-component-candidate-bucket-manifest.csv", rows, MANIFEST_FIELDS)
    write_csv(root / COMPONENT_ID_MAP, component_map_rows, COMPONENT_MAP_FIELDS)
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
