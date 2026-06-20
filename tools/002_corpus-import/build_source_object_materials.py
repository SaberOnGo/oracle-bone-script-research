#!/usr/bin/env python3
"""Build object-local human and AI material bundles for registered sources."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
DOWNLOAD_MANIFEST = Path("corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv")
DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
PACKAGE_MANIFEST = Path("corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv")
METADATA_PROFILE = Path("corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv")
OUTPUT_ROOT = Path("corpus/006_research-sources-and-bibliography/001_source-objects")
UPDATED_AT = "2026-06-20"


DOWNLOAD_ROUTE_FIELDS = [
    "route_id",
    "source_id",
    "download_id",
    "url",
    "artifact_kind",
    "commit_policy",
    "manifest_max_bytes",
    "manifest_notes",
    "download_status",
    "http_status",
    "file_size_bytes",
    "checksum_sha256",
    "local_temp_path",
    "risk_note",
    "review_status",
]

PACKAGE_ROUTE_FIELDS = [
    "package_route_id",
    "source_id",
    "package_file_id",
    "source_package_id",
    "file_name",
    "file_kind",
    "source_url",
    "file_size_bytes",
    "download_id",
    "commit_policy",
    "handling_strategy",
    "rights_status",
    "review_status",
    "updated_at",
]

FIELD_ROUTE_FIELDS = [
    "field_route_id",
    "source_id",
    "map_id",
    "source_level",
    "source_field_or_unit",
    "source_meaning",
    "target_record_type",
    "target_project_field",
    "import_action",
    "rights_boundary",
    "evidence_download_id",
    "review_status",
    "updated_at",
]

METADATA_ROUTE_FIELDS = [
    "metadata_route_id",
    "source_id",
    "profile_id",
    "evidence_download_id",
    "metadata_file",
    "profile_metric",
    "profile_value",
    "profile_unit",
    "import_relevance",
    "caution",
    "review_status",
    "updated_at",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_dir_name(index: int, source_id: str) -> str:
    safe_source_id = "".join(ch if ch.isascii() and (ch.isalnum() or ch in "-_") else "-" for ch in source_id)
    return f"{index:03d}_{safe_source_id}_source-object"


def index_by_source(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_source[row.get("source_id", "")].append(row)
    return dict(by_source)


def build_download_routes(
    source_id: str,
    manifest_rows: list[dict[str, str]],
    log_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    log_by_download_id = {row["download_id"]: row for row in log_rows}
    routes = []
    for index, manifest in enumerate(manifest_rows, start=1):
        log = log_by_download_id.get(manifest["download_id"], {})
        routes.append(
            {
                "route_id": f"{source_id}-download-route-{index:03d}",
                "source_id": source_id,
                "download_id": manifest["download_id"],
                "url": manifest["url"],
                "artifact_kind": manifest["artifact_kind"],
                "commit_policy": manifest["commit_policy"],
                "manifest_max_bytes": manifest["max_bytes"],
                "manifest_notes": manifest["notes"],
                "download_status": log.get("status", "not_logged_yet"),
                "http_status": log.get("http_status", ""),
                "file_size_bytes": log.get("file_size_bytes", ""),
                "checksum_sha256": log.get("checksum_sha256", ""),
                "local_temp_path": log.get("local_temp_path", ""),
                "risk_note": log.get("risk_note", ""),
                "review_status": "metadata_route_needs_human_review",
            }
        )
    return routes


def add_route_ids(source_id: str, rows: list[dict[str, str]], key: str, prefix: str) -> list[dict[str, str]]:
    routed = []
    for index, row in enumerate(rows, start=1):
        routed.append({prefix: f"{source_id}-{key}-{index:03d}", **row})
    return routed


def source_packet(
    source: dict[str, str],
    object_dir: Path,
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "record_type": "source_object_packet",
        "source_id": source["source_id"],
        "source_type": source["source_type"],
        "title": source["title"],
        "provider": source["provider"],
        "authority_tier": source["authority_tier"],
        "source_url": source["source_url"],
        "scope": source["scope"],
        "adoption_status": source["adoption_status"],
        "download_strategy": source["download_strategy"],
        "rights_status": source["rights_status"],
        "risk_note": source["risk_note"],
        "review_status": source["review_status"],
        "object_dir": object_dir.as_posix(),
        "download_route_count": len(download_routes),
        "package_route_count": len(package_routes),
        "field_map_route_count": len(field_routes),
        "metadata_profile_route_count": len(metadata_routes),
        "local_files": [
            "README.md",
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "06_human-source-review-sheet.md",
            "07_material-access-index.md",
        ],
        "research_boundary": (
            "source_object_packet_preprocessing_only; source metadata, routes, "
            "download logs, package manifests, and field maps are not decipherment, "
            "identity, component, inscription, or correspondence conclusions"
        ),
        "decipherment_claim_status": "no_claim",
        "updated_at": UPDATED_AT,
    }


def readme_text(source: dict[str, str], packet: dict[str, object]) -> str:
    return f"""# {source["source_id"]} Source Object / {source["source_id"]} 来源对象

English:
This directory is the co-located human and AI entrance for one registered research source. It keeps the readable summary, route indexes, package manifest links, metadata profile links, field-map links, and AI-readable packet inside the same concrete source object directory.

简体中文：
本目录是一个已登记研究来源的同目录人类/AI 入口。可读摘要、下载路线索引、来源包 manifest 线索、metadata profile 线索、字段映射线索和 AI 可读 packet 都放在同一个具体来源对象目录中。

## Source Summary / 来源摘要

- Source ID / 来源 ID: `{source["source_id"]}`
- Type / 类型: `{source["source_type"]}`
- Title / 标题: `{source["title"]}`
- Provider / 提供方: `{source["provider"]}`
- Authority tier / 权威等级: `{source["authority_tier"]}`
- URL / 链接: {source["source_url"]}
- Adoption status / 采用状态: `{source["adoption_status"]}`
- Rights status / 权利状态: `{source["rights_status"]}`
- Review status / 复核状态: `{source["review_status"]}`

## Local Files / 本目录文件

- AI-readable source packet / AI 可读来源包: `01_source-packet.json`
- Download/access routes / 下载或访问路线: `02_download-route-index.csv`
- Package/file manifest routes / 来源包和文件清单路线: `03_package-route-index.csv`
- Field-map routes / 字段映射路线: `04_field-map-route-index.csv`
- Downloaded metadata profile routes / 已下载 metadata profile 路线: `05_metadata-profile-route-index.csv`
- Human review sheet / 人工复核表: `06_human-source-review-sheet.md`

## Current Route Counts / 当前路线数量

- Download route count / 下载路线数: `{packet["download_route_count"]}`
- Package route count / 来源包路线数: `{packet["package_route_count"]}`
- Field map route count / 字段映射路线数: `{packet["field_map_route_count"]}`
- Metadata profile route count / metadata profile 路线数: `{packet["metadata_profile_route_count"]}`

## Risk And Boundary / 风险与边界

English:
{source["risk_note"]}

These rows are preparation-stage source routes. They are not rights clearance, not a formal import decision, not a confirmed character reading, not a component assignment, not an inscription identity, and not a decipherment conclusion.

简体中文：
{source["risk_note"]}

这些记录只是准备阶段的来源路线。它们不是权利清理结论，不是正式导入决定，不是已确认字义或释读，不是构件归属，不是卜辞身份结论，也不是破译结论。
"""


def status_label(count: int, present_label: str) -> str:
    if count > 0:
        return present_label
    return "not_present_in_current_registers"


def material_access_index_text(
    source: dict[str, str],
    packet: dict[str, object],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> str:
    download_count = len(download_routes)
    package_count = len(package_routes)
    field_count = len(field_routes)
    metadata_count = len(metadata_routes)
    download_statuses = sorted({row.get("download_status", "") for row in download_routes if row.get("download_status")})
    package_kinds = sorted({row.get("file_kind", "") for row in package_routes if row.get("file_kind")})
    target_record_types = sorted({row.get("target_record_type", "") for row in field_routes if row.get("target_record_type")})
    metadata_metrics = sorted({row.get("profile_metric", "") for row in metadata_routes if row.get("profile_metric")})
    return f"""# {source["source_id"]} Material Access Index / {source["source_id"]} 资料访问索引

English:
This object-local index tells a human reviewer what source materials are currently visible in this same source directory and which AI-readable files carry the structured routes. It is a preparation-stage access map, not a rights decision or research conclusion.

简体中文：
本对象内索引说明人工复核者在同一个来源目录里可以看到哪些资料入口，以及哪些 AI 可读文件保存了结构化路线。它只是准备阶段的访问地图，不是权利结论，也不是学术结论。

## Human-Readable Entrances / 人类可读入口

| Material area | Local file | Current status | Count or signal |
| --- | --- | --- | --- |
| Source summary / 来源摘要 | `README.md` | present | source ID `{source["source_id"]}` |
| Human review sheet / 人工复核表 | `06_human-source-review-sheet.md` | present | source provenance and rights checklist |
| Download or access routes / 下载或访问路线 | `02_download-route-index.csv` | {status_label(download_count, "route_rows_present")} | {download_count} route row(s); statuses: {";".join(download_statuses) if download_statuses else "none"} |
| Package or file manifest routes / 来源包或文件清单路线 | `03_package-route-index.csv` | {status_label(package_count, "route_rows_present")} | {package_count} route row(s); kinds: {";".join(package_kinds) if package_kinds else "none"} |
| Field maps / 字段映射 | `04_field-map-route-index.csv` | {status_label(field_count, "field_rows_present")} | {field_count} row(s); target records: {";".join(target_record_types) if target_record_types else "none"} |
| Downloaded metadata profiles / 已下载 metadata profile | `05_metadata-profile-route-index.csv` | {status_label(metadata_count, "profile_rows_present")} | {metadata_count} row(s); metrics: {";".join(metadata_metrics) if metadata_metrics else "none"} |

## AI-Readable Entrances / AI 可读入口

- Source packet / 来源 packet: `01_source-packet.json`
- Download route table / 下载路线表: `02_download-route-index.csv`
- Package route table / 来源包路线表: `03_package-route-index.csv`
- Field-map route table / 字段映射路线表: `04_field-map-route-index.csv`
- Metadata profile route table / metadata profile 路线表: `05_metadata-profile-route-index.csv`

## Next Review Step / 下一步复核入口

- Rights status / 权利状态: `{source["rights_status"]}`
- Review status / 复核状态: `{source["review_status"]}`
- Risk note / 风险提示: {source["risk_note"]}
- Recommended next action / 建议下一步: inspect the route rows above, then decide whether source-safe visual/text derivatives can be added inside the relevant concrete corpus object directories.

## Boundary / 边界

English:
This index does not collect new evidence, clear rights, promote a source, import corpus records, confirm a character identity, assign a component, identify an inscription, confirm an evolution chain, or make a decipherment conclusion.

简体中文：
本索引不采集新证据，不完成权利清理，不提升来源，不导入语料记录，不确认字形身份，不指定构件，不确认卜辞身份，不确认演化链，也不作释读结论。
"""


def review_sheet_text(source: dict[str, str]) -> str:
    return f"""# {source["source_id"]} Human Source Review Sheet / {source["source_id"]} 人工来源复核表

## Review Scope / 复核范围

English:
Review only source provenance, access status, package/file metadata, field mapping, rights status, and whether any raw material is safe to promote into object-local derived records.

简体中文：
这里只复核来源出处、访问状态、来源包/文件 metadata、字段映射、权利状态，以及是否可以把某些原始资料提升为对象内派生记录。

## Checklist / 清单

- [ ] Source register row checked against `01_source-packet.json`
- [ ] Download/access routes checked in `02_download-route-index.csv`
- [ ] Package/file manifest routes checked in `03_package-route-index.csv`
- [ ] Field-map routes checked in `04_field-map-route-index.csv`
- [ ] Metadata profile routes checked in `05_metadata-profile-route-index.csv`
- [ ] Rights status and risk note reviewed before any asset promotion
- [ ] No reading, identity, component, inscription, or correspondence conclusion added

## Status / 状态

- Source ID / 来源 ID: `{source["source_id"]}`
- Rights status / 权利状态: `{source["rights_status"]}`
- Review status / 复核状态: `needs_human_source_review`
- Decipherment claim status / 释读结论状态: `no_claim`
"""


def build_materials(root: Path) -> dict[str, int]:
    root = root.resolve()
    sources = read_csv(root / SOURCE_INDEX)
    downloads_by_source = index_by_source(read_csv(root / DOWNLOAD_MANIFEST))
    download_logs_by_source = index_by_source(read_csv(root / DOWNLOAD_LOG))
    packages_by_source = index_by_source(read_csv(root / PACKAGE_MANIFEST))
    fields_by_source = index_by_source(read_csv(root / FIELD_MAP))
    metadata_by_source = index_by_source(read_csv(root / METADATA_PROFILE))

    for index, source in enumerate(sources, start=1):
        source_id = source["source_id"]
        object_dir = root / OUTPUT_ROOT / source_dir_name(index, source_id)
        object_dir.mkdir(parents=True, exist_ok=True)
        download_routes = build_download_routes(
            source_id,
            downloads_by_source.get(source_id, []),
            download_logs_by_source.get(source_id, []),
        )
        package_routes = add_route_ids(
            source_id, packages_by_source.get(source_id, []), "package-route", "package_route_id"
        )
        field_routes = add_route_ids(source_id, fields_by_source.get(source_id, []), "field-route", "field_route_id")
        metadata_routes = add_route_ids(
            source_id, metadata_by_source.get(source_id, []), "metadata-route", "metadata_route_id"
        )
        packet = source_packet(
            source,
            object_dir.relative_to(root),
            download_routes,
            package_routes,
            field_routes,
            metadata_routes,
        )
        (object_dir / "README.md").write_text(readme_text(source, packet).rstrip() + "\n", encoding="utf-8")
        write_json(object_dir / "01_source-packet.json", packet)
        write_csv(object_dir / "02_download-route-index.csv", download_routes, DOWNLOAD_ROUTE_FIELDS)
        write_csv(object_dir / "03_package-route-index.csv", package_routes, PACKAGE_ROUTE_FIELDS)
        write_csv(object_dir / "04_field-map-route-index.csv", field_routes, FIELD_ROUTE_FIELDS)
        write_csv(object_dir / "05_metadata-profile-route-index.csv", metadata_routes, METADATA_ROUTE_FIELDS)
        (object_dir / "06_human-source-review-sheet.md").write_text(
            review_sheet_text(source).rstrip() + "\n", encoding="utf-8"
        )
        (object_dir / "07_material-access-index.md").write_text(
            material_access_index_text(
                source,
                packet,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ).rstrip()
            + "\n",
            encoding="utf-8",
        )
    return {"source_object_count": len(sources)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    result = build_materials(args.root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
