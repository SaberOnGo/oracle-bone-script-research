#!/usr/bin/env python3
"""Add package-manifest rows for lightweight downloaded source files.

The large package manifest already covers HUST-OBC, OBIMD, and EVOBC raw
packages. This builder records small downloaded pages, API JSON files, PDFs, or
access-restricted page captures as source-package evidence when a source has no
package manifest yet. It only reads committed provenance logs and does not open
ignored tmp downloads, redownload sources, or promote source content.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import unquote, urlparse


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_PACKAGE_FILE_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv"
)
UPDATED_AT = "2026-06-20"
REVIEW_STATUS = "reviewed_metadata_only"

OUTPUT_FIELDS = [
    "package_file_id",
    "source_package_id",
    "source_id",
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


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def next_package_file_number(rows: list[dict[str, str]]) -> int:
    numbers: list[int] = []
    for row in rows:
        package_file_id = row.get("package_file_id", "")
        if package_file_id.startswith("pkg-file-"):
            numbers.append(int(package_file_id.rsplit("-", 1)[1]))
    return max(numbers, default=0) + 1


def file_name_for(download_row: dict[str, str]) -> str:
    local_temp = download_row.get("local_temp_path", "")
    if local_temp:
        return Path(local_temp).name
    url_path = unquote(urlparse(download_row.get("url", "")).path)
    name = Path(url_path).name
    return name or f"{download_row['download_id']}.download"


def file_kind_for(file_name: str, status: str) -> str:
    suffix = Path(file_name).suffix.lower().lstrip(".")
    if status == "downloaded_access_restricted_page":
        return "access_restricted_page_capture"
    if suffix in {"html", "htm"}:
        return "lightweight_html_page"
    if suffix == "json":
        return "lightweight_api_json"
    if suffix == "pdf":
        return "lightweight_pdf"
    if suffix in {"md", "txt"}:
        return f"lightweight_{suffix}_text"
    return "lightweight_downloaded_file"


def source_package_id_for(source_id: str) -> str:
    return f"light-src-{source_id.removeprefix('src-')}"


def build_rows(
    source_rows: list[dict[str, str]],
    download_log_rows: list[dict[str, str]],
    existing_manifest_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = list(existing_manifest_rows)
    source_by_id = {row["source_id"]: row for row in source_rows}
    sources_with_manifest = {row.get("source_id", "") for row in existing_manifest_rows}
    existing_download_ids = {row.get("download_id", "") for row in existing_manifest_rows if row.get("download_id", "")}
    package_file_number = next_package_file_number(rows)

    for download_row in sorted(download_log_rows, key=lambda item: (item["source_id"], item["download_id"])):
        source_id = download_row["source_id"]
        status = download_row.get("status", "")
        if source_id in sources_with_manifest:
            continue
        if download_row["download_id"] in existing_download_ids:
            continue
        if not status.startswith("downloaded"):
            continue
        file_name = file_name_for(download_row)
        rows.append(
            {
                "package_file_id": f"pkg-file-{package_file_number:06d}",
                "source_package_id": source_package_id_for(source_id),
                "source_id": source_id,
                "file_name": file_name,
                "file_kind": file_kind_for(file_name, status),
                "source_url": download_row["url"],
                "file_size_bytes": download_row.get("file_size_bytes", ""),
                "download_id": download_row["download_id"],
                "commit_policy": "download_to_tmp_log_checksum_only",
                "handling_strategy": (
                    "Lightweight source evidence is represented by committed provenance, "
                    "size, checksum, and derived metadata only; ignored tmp downloads are "
                    "not committed as source content."
                ),
                "rights_status": source_by_id[source_id]["rights_status"],
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
        existing_download_ids.add(download_row["download_id"])
        package_file_number += 1
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--source-download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--package-manifest", default=str(SOURCE_PACKAGE_FILE_MANIFEST))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_rows(
        read_csv_rows(root / args.source_index),
        read_csv_rows(root / args.source_download_log),
        read_csv_rows(root / args.package_manifest),
    )
    write_csv(root / args.package_manifest, rows)
    print(f"wrote={len(rows)} output={(root / args.package_manifest).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
