#!/usr/bin/env python3
"""Fill blank asset ID source-map fields from the asset provenance index.

This synchronizes routing metadata only. It does not add images, change rights
decisions, promote character records, or make decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


ASSET_ID_SOURCE_MAP = Path("project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv")
ASSET_SOURCE_INDEX = Path("project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv")
UPDATED_AT = "2026-06-20"
HUST_OBC_PACKAGE_REFS = ("large-src-000001", "dl-hust-obc-figshare-raw")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.replace(",", ";").split(";") if item.strip()]


def build_external_ref_list(map_row: dict[str, str], asset_row: dict[str, str]) -> str:
    existing = map_row.get("all_external_ref_ids", "")
    if existing:
        return existing
    refs = []
    primary = map_row.get("primary_external_ref_id", "") or asset_row.get("primary_external_ref_id", "")
    if primary:
        refs.append(primary)
    source_ids = split_values(map_row.get("source_ids", "") or asset_row.get("source_ids", ""))
    if "src-hust-obc" in source_ids and asset_row.get("source_url", "").endswith("48465988"):
        refs.extend(HUST_OBC_PACKAGE_REFS)
    return ";".join(dict.fromkeys(refs))


def sync_asset_map_rows(
    map_rows: list[dict[str, str]],
    asset_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], Counter[str]]:
    asset_by_id = {row.get("asset_id", ""): row for row in asset_rows}
    changes: Counter[str] = Counter()
    synced_rows: list[dict[str, str]] = []
    fill_fields = {
        "record_type": "asset_type",
        "canonical_path": "canonical_path",
        "primary_external_ref_id": "primary_external_ref_id",
        "source_ids": "source_ids",
        "rights_status": "rights_status",
        "review_status": "review_status",
    }
    for row in map_rows:
        synced = dict(row)
        asset_row = asset_by_id.get(row.get("project_id", ""), {})
        if asset_row:
            for map_field, asset_field in fill_fields.items():
                if not synced.get(map_field, "") and asset_row.get(asset_field, ""):
                    synced[map_field] = asset_row[asset_field]
                    changes[f"{map_field}_filled"] += 1
            if not synced.get("all_external_ref_ids", ""):
                refs = build_external_ref_list(synced, asset_row)
                if refs:
                    synced["all_external_ref_ids"] = refs
                    changes["all_external_ref_ids_filled"] += 1
            if synced != row:
                synced["updated_at"] = UPDATED_AT
                changes["rows_updated"] += 1
        synced_rows.append(synced)
    return synced_rows, changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-map", default=str(ASSET_ID_SOURCE_MAP))
    parser.add_argument("--asset-index", default=str(ASSET_SOURCE_INDEX))
    args = parser.parse_args(argv)

    root = repo_root()
    asset_map_path = root / args.asset_map
    map_rows = read_csv_rows(asset_map_path)
    asset_rows = read_csv_rows(root / args.asset_index)
    synced_rows, changes = sync_asset_map_rows(map_rows, asset_rows)
    if changes["rows_updated"]:
        fieldnames = list(map_rows[0])
        write_csv_rows(asset_map_path, synced_rows, fieldnames)
    print(
        f"asset_id_source_map_sync rows_scanned={len(map_rows)} "
        + " ".join(f"{key}={changes[key]}" for key in sorted(changes))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
