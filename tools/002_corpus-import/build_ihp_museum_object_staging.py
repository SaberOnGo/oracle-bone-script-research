#!/usr/bin/env python3
"""Build IHP Museum oracle-bone object staging records from the logged collection page."""

from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path
from urllib.parse import urljoin


SOURCE_ID = "src-ihp-museum-oracle-bones"
EVIDENCE_DOWNLOAD_ID = "dl-ihp-museum-oracle-bones"
BASE_URL = "https://museum.sinica.edu.tw/en/"
SITE_ROOT_URL = "https://museum.sinica.edu.tw/"
RIGHTS_STATUS = "metadata_only_until_verified"
REVIEW_STATUS = "reviewed_metadata_only"
IMPORT_STATUS = "object_metadata_not_promoted"
UPDATED_AT = "2026-06-04"

FIELDNAMES = [
    "candidate_collection_object_id",
    "source_id",
    "evidence_download_id",
    "provider",
    "collection_name",
    "source_collection_item_id",
    "object_page_url",
    "object_title_en",
    "catalog_reference_text",
    "thumbnail_source_path",
    "thumbnail_url",
    "thumbnail_download_status",
    "project_import_status",
    "rights_status",
    "caution",
    "review_status",
    "updated_at",
]

ITEM_PATTERN = re.compile(
    r'<a href="(collection/32/item/(\d+)/)"><img data-src="([^"]+)" alt="([^"]*)"',
    re.DOTALL,
)

CATALOG_TOKEN_PATTERN = re.compile(
    r"\b((?:Jia Bian|Yi Bian buyi|Yi Bian|Bing Bian|Chia|Ping|I)\b\s*[0-9A-Za-z+&;.\-\s]+)",
    re.IGNORECASE,
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def clean_html_text(value: str) -> str:
    previous = value
    while True:
        current = html.unescape(previous)
        if current == previous:
            break
        previous = current
    current = re.sub(r"<[^>]+>", "", current)
    current = current.replace("\xa0", " ")
    current = re.sub(r"\s+", " ", current)
    return current.strip()


def extract_catalog_reference(title: str) -> str:
    matches = [match.group(1).strip() for match in CATALOG_TOKEN_PATTERN.finditer(title)]
    cleaned = []
    for match in matches:
        match = re.sub(r"\s+", " ", match).strip(" ,;")
        if match and match not in cleaned:
            cleaned.append(match)
    return ";".join(cleaned)


def build_rows(html_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen_item_ids: set[str] = set()
    for index, match in enumerate(ITEM_PATTERN.finditer(html_text), start=1):
        href, item_id, thumbnail_path, raw_title = match.groups()
        if item_id in seen_item_ids:
            raise ValueError(f"Duplicate IHP Museum collection item ID: {item_id}")
        seen_item_ids.add(item_id)

        title = clean_html_text(raw_title)
        rows.append(
            {
                "candidate_collection_object_id": f"ihp-mus-obj-{index:05d}",
                "source_id": SOURCE_ID,
                "evidence_download_id": EVIDENCE_DOWNLOAD_ID,
                "provider": "Museum of the Institute of History and Philology, Academia Sinica",
                "collection_name": "Oracle Bones",
                "source_collection_item_id": item_id,
                "object_page_url": urljoin(BASE_URL, href),
                "object_title_en": title,
                "catalog_reference_text": extract_catalog_reference(title),
                "thumbnail_source_path": thumbnail_path,
                "thumbnail_url": urljoin(SITE_ROOT_URL, thumbnail_path),
                "thumbnail_download_status": "not_downloaded_metadata_only",
                "project_import_status": IMPORT_STATUS,
                "rights_status": RIGHTS_STATUS,
                "caution": (
                    "Object and thumbnail metadata comes from the official IHP Museum "
                    "Oracle Bones collection page; images are not downloaded and item-level "
                    "rights must be reviewed before asset import."
                ),
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-html",
        type=Path,
        default=root / "tmp/source_downloads/dl-ihp-museum-oracle-bones.html",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            root
            / "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
            / "002_ihp-museum-oracle-bone-object-staging.csv"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_text = args.input_html.read_text(encoding="utf-8", errors="replace")
    rows = build_rows(html_text)
    write_csv(args.output, rows)
    print(f"Wrote {len(rows)} IHP Museum object staging rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
