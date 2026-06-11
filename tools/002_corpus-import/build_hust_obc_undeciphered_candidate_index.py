#!/usr/bin/env python3
"""Build metadata-only HUST-OBC undeciphered candidate records."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile


SOURCE_ID = "src-hust-obc"
SOURCE_PACKAGE_ID = "large-src-000001"
DOWNLOAD_ID = "dl-hust-obc-figshare-raw"
SOURCE_URL = "https://ndownloader.figshare.com/files/48465988"
SOURCE_REPORTED_UNDECIPHERED_CLASS_COUNT = 9411
FIGSHARE_MD5 = "7138be414ebc8c9262ecda38b7fd9e84"
ZIP_OBSERVED_UNDECIPHERED_CLASS_COUNT = 9408
ZIP_OBSERVED_UNDECIPHERED_IMAGE_COUNT = 62989
RAW_SIZE_BYTES = 607933810
RAW_SHA256 = "0d00a4de8dd9ce7b7495d7b26f3c80098ee9975b91615211dde02e569bf0ad9d"
UPDATED_AT = "2026-06-10"
DOWNLOADED_AT = "2026-06-10T10:25:00+00:00"
DEFAULT_ZIP_PATH = "tmp/source_downloads/dl-hust-obc-figshare-raw.zip"
ARCHIVE_HINT = (
    "external_local_archive/source_packages/hust-obc/"
    "dl-hust-obc-figshare-raw.zip"
)
EXTERNAL_ARCHIVE_PATH = (
    "D:/project/52_oracle-bone-script-research-local-archive/"
    "source_packages/hust-obc/dl-hust-obc-figshare-raw.zip"
)
INDEX_PATH = (
    "corpus/001_oracle-characters/000_character-registers/"
    "003_undeciphered-oracle-characters-index.csv"
)
LARGE_SOURCE_REGISTER = "project_registry/006_large-source-register/001_large-source-register.csv"
DOWNLOAD_LOG = "project_registry/006_large-source-register/002_source-download-log.csv"

GROUP_LABELS = {
    "L": "Oracle Bone Script: Six Digit Numerical Code",
    "X": "New Compilation of Oracle Bone Scripts",
    "Y+H": "YinQiWenYuan + HWOBC",
}
GROUP_ORDER = {"L": 0, "X": 1, "Y+H": 2}
BUCKET_SPECS = [
    {
        "directory_prefix": "017",
        "start": 1,
        "end": 100,
        "materialization_status": "first_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "018",
        "start": 101,
        "end": 200,
        "materialization_status": "second_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "019",
        "start": 201,
        "end": 300,
        "materialization_status": "third_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "020",
        "start": 301,
        "end": 400,
        "materialization_status": "fourth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "021",
        "start": 401,
        "end": 500,
        "materialization_status": "fifth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "022",
        "start": 501,
        "end": 600,
        "materialization_status": "sixth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "023",
        "start": 601,
        "end": 700,
        "materialization_status": "seventh_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "024",
        "start": 701,
        "end": 800,
        "materialization_status": "eighth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "025",
        "start": 801,
        "end": 900,
        "materialization_status": "ninth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "026",
        "start": 901,
        "end": 1000,
        "materialization_status": "tenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "027",
        "start": 1001,
        "end": 1100,
        "materialization_status": "eleventh_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "028",
        "start": 1101,
        "end": 1200,
        "materialization_status": "twelfth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "029",
        "start": 1201,
        "end": 1300,
        "materialization_status": "thirteenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "030",
        "start": 1301,
        "end": 1400,
        "materialization_status": "fourteenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "031",
        "start": 1401,
        "end": 1500,
        "materialization_status": "fifteenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "032",
        "start": 1501,
        "end": 1600,
        "materialization_status": "sixteenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "033",
        "start": 1601,
        "end": 1700,
        "materialization_status": "seventeenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "034",
        "start": 1701,
        "end": 1800,
        "materialization_status": "eighteenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "035",
        "start": 1801,
        "end": 1900,
        "materialization_status": "nineteenth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "036",
        "start": 1901,
        "end": 2000,
        "materialization_status": "twentieth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "037",
        "start": 2001,
        "end": 2100,
        "materialization_status": "twenty_first_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "038",
        "start": 2101,
        "end": 2200,
        "materialization_status": "twenty_second_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "039",
        "start": 2201,
        "end": 2300,
        "materialization_status": "twenty_third_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "040",
        "start": 2301,
        "end": 2400,
        "materialization_status": "twenty_fourth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "041",
        "start": 2401,
        "end": 2500,
        "materialization_status": "twenty_fifth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "042",
        "start": 2501,
        "end": 2600,
        "materialization_status": "twenty_sixth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "043",
        "start": 2601,
        "end": 2700,
        "materialization_status": "twenty_seventh_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "044",
        "start": 2701,
        "end": 2800,
        "materialization_status": "twenty_eighth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "045",
        "start": 2801,
        "end": 2900,
        "materialization_status": "twenty_ninth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "046",
        "start": 2901,
        "end": 3000,
        "materialization_status": "thirtieth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "047",
        "start": 3001,
        "end": 3100,
        "materialization_status": "thirty_first_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "048",
        "start": 3101,
        "end": 3200,
        "materialization_status": "thirty_second_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "049",
        "start": 3201,
        "end": 3300,
        "materialization_status": "thirty_third_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "050",
        "start": 3301,
        "end": 3400,
        "materialization_status": "thirty_fourth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "051",
        "start": 3401,
        "end": 3500,
        "materialization_status": "thirty_fifth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "052",
        "start": 3501,
        "end": 3600,
        "materialization_status": "thirty_sixth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "053",
        "start": 3601,
        "end": 3700,
        "materialization_status": "thirty_seventh_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "054",
        "start": 3701,
        "end": 3800,
        "materialization_status": "thirty_eighth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "055",
        "start": 3801,
        "end": 3900,
        "materialization_status": "thirty_ninth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "056",
        "start": 3901,
        "end": 4000,
        "materialization_status": "fortieth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "057",
        "start": 4001,
        "end": 4100,
        "materialization_status": "forty_first_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "058",
        "start": 4101,
        "end": 4200,
        "materialization_status": "forty_second_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "059",
        "start": 4201,
        "end": 4300,
        "materialization_status": "forty_third_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "060",
        "start": 4301,
        "end": 4400,
        "materialization_status": "forty_fourth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "061",
        "start": 4401,
        "end": 4500,
        "materialization_status": "forty_fifth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "062",
        "start": 4501,
        "end": 4600,
        "materialization_status": "forty_sixth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "063",
        "start": 4601,
        "end": 4700,
        "materialization_status": "forty_seventh_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "064",
        "start": 4701,
        "end": 4800,
        "materialization_status": "forty_eighth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "065",
        "start": 4801,
        "end": 4900,
        "materialization_status": "forty_ninth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "066",
        "start": 4901,
        "end": 5000,
        "materialization_status": "fiftieth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "067",
        "start": 5001,
        "end": 5100,
        "materialization_status": "fifty_first_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "068",
        "start": 5101,
        "end": 5200,
        "materialization_status": "fifty_second_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "069",
        "start": 5201,
        "end": 5300,
        "materialization_status": "fifty_third_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "070",
        "start": 5301,
        "end": 5400,
        "materialization_status": "fifty_fourth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "071",
        "start": 5401,
        "end": 5500,
        "materialization_status": "fifty_fifth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "072",
        "start": 5501,
        "end": 5600,
        "materialization_status": "fifty_sixth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "073",
        "start": 5601,
        "end": 5700,
        "materialization_status": "fifty_seventh_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "074",
        "start": 5701,
        "end": 5800,
        "materialization_status": "fifty_eighth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "075",
        "start": 5801,
        "end": 5900,
        "materialization_status": "fifty_ninth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "076",
        "start": 5901,
        "end": 6000,
        "materialization_status": "sixtieth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "077",
        "start": 6001,
        "end": 6100,
        "materialization_status": "sixty_first_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "078",
        "start": 6101,
        "end": 6200,
        "materialization_status": "sixty_second_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "079",
        "start": 6201,
        "end": 6300,
        "materialization_status": "sixty_third_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "080",
        "start": 6301,
        "end": 6400,
        "materialization_status": "sixty_fourth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "081",
        "start": 6401,
        "end": 6500,
        "materialization_status": "sixty_fifth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "082",
        "start": 6501,
        "end": 6600,
        "materialization_status": "sixty_sixth_bucket_candidate_packet_materialized",
    },
    {
        "directory_prefix": "083",
        "start": 6601,
        "end": 6700,
        "materialization_status": "sixty_seventh_bucket_candidate_packet_materialized",
    },
]

INDEX_FIELDS = [
    "unknown_candidate_id",
    "record_type",
    "source_id",
    "source_package_id",
    "evidence_download_id",
    "primary_external_ref_id",
    "source_group",
    "source_group_label",
    "source_class_id",
    "source_class_path",
    "source_image_count",
    "first_source_image_path",
    "last_source_image_path",
    "filename_source_prefixes",
    "source_reported_undeciphered_class_count",
    "zip_observed_undeciphered_class_count",
    "zip_observed_undeciphered_image_count",
    "materialized_candidate_packet_path",
    "materialization_status",
    "decipherment_status",
    "identity_claim_status",
    "assignment_status",
    "promotion_status",
    "rights_status",
    "risk_note",
    "caution",
    "review_status",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def group_from_zip_path(path: str) -> tuple[str, str] | None:
    parts = path.split("/")
    if len(parts) < 5 or parts[0] != "HUST-OBC" or parts[1] != "undeciphered":
        return None
    group = parts[2]
    if group not in GROUP_ORDER:
        return None
    class_id = parts[3]
    filename = parts[-1]
    if not filename or filename == class_id:
        return None
    if not re.search(r"\.(png|jpg|jpeg|bmp|webp)$", filename, re.IGNORECASE):
        return None
    return group, class_id


def class_sort_key(item: tuple[tuple[str, str], list[str]]) -> tuple[int, int, str]:
    (group, class_id), _paths = item
    numeric = int(class_id) if class_id.isdigit() else 10**12
    return GROUP_ORDER[group], numeric, class_id


def external_ref_id(group: str, sequence: int) -> str:
    ref_group = "YH" if group == "Y+H" else group
    return f"hust-obc-und-{ref_group}-{sequence:06d}"


def packet_dir_name(sequence: int, candidate_id: str, ref_id: str) -> str:
    return f"{sequence:03d}_{candidate_id}_{ref_id}_oracle-character-candidate"


def bucket_directory(spec: dict[str, int | str]) -> str:
    return (
        "corpus/001_oracle-characters/"
        f"{spec['directory_prefix']}_undeciphered-{int(spec['start']):06d}-"
        f"{int(spec['end']):06d}_obs-unk-bucket_oracle-character-candidates"
    )


def bucket_manifest_path(spec: dict[str, int | str]) -> str:
    return (
        f"{bucket_directory(spec)}/"
        "000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
    )


def bucket_for_sequence(sequence: int) -> dict[str, int | str] | None:
    for spec in BUCKET_SPECS:
        if int(spec["start"]) <= sequence <= int(spec["end"]):
            return spec
    return None


def filename_prefixes(paths: list[str]) -> str:
    counts: Counter[str] = Counter()
    for path in paths:
        name = Path(path).name
        prefix = name.split("_", 1)[0]
        counts[prefix] += 1
    return ";".join(f"{key}:{counts[key]}" for key in sorted(counts))


def collect_candidates(zip_path: Path) -> list[dict[str, str]]:
    by_class: dict[tuple[str, str], list[str]] = defaultdict(list)
    with ZipFile(zip_path) as zf:
        for name in zf.namelist():
            parsed = group_from_zip_path(name)
            if parsed is None:
                continue
            by_class[parsed].append(name)

    rows: list[dict[str, str]] = []
    for sequence, ((group, class_id), paths) in enumerate(
        sorted(by_class.items(), key=class_sort_key), start=1
    ):
        sorted_paths = sorted(paths)
        candidate_id = f"obs-unk-{sequence:06d}"
        ref_id = external_ref_id(group, sequence)
        spec = bucket_for_sequence(sequence)
        materialized_path = ""
        materialization_status = "index_only_not_materialized"
        if spec is not None:
            bucket_sequence = sequence - int(spec["start"]) + 1
            materialized_path = (
                f"{bucket_directory(spec)}/"
                f"{packet_dir_name(bucket_sequence, candidate_id, ref_id)}/"
                "01_undeciphered-candidate-packet.json"
            )
            materialization_status = str(spec["materialization_status"])
        caution = (
            "HUST-OBC zip-directory candidate only; not an accepted oracle character, "
            "reading, component, evolution chain, or decipherment conclusion. "
            "Article reports 9411 undeciphered characters, but the inspected zip "
            "directory yielded 9408 candidate class directories; discrepancy needs review."
        )
        rows.append(
            {
                "unknown_candidate_id": candidate_id,
                "record_type": "oracle_character_undeciphered_candidate",
                "source_id": SOURCE_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "evidence_download_id": DOWNLOAD_ID,
                "primary_external_ref_id": ref_id,
                "source_group": group,
                "source_group_label": GROUP_LABELS[group],
                "source_class_id": class_id,
                "source_class_path": f"HUST-OBC/undeciphered/{group}/{class_id}/",
                "source_image_count": str(len(sorted_paths)),
                "first_source_image_path": sorted_paths[0],
                "last_source_image_path": sorted_paths[-1],
                "filename_source_prefixes": filename_prefixes(sorted_paths),
                "source_reported_undeciphered_class_count": str(
                    SOURCE_REPORTED_UNDECIPHERED_CLASS_COUNT
                ),
                "zip_observed_undeciphered_class_count": str(
                    ZIP_OBSERVED_UNDECIPHERED_CLASS_COUNT
                ),
                "zip_observed_undeciphered_image_count": str(
                    ZIP_OBSERVED_UNDECIPHERED_IMAGE_COUNT
                ),
                "materialized_candidate_packet_path": materialized_path,
                "materialization_status": materialization_status,
                "decipherment_status": "undeciphered_dataset_candidate_not_accepted_character",
                "identity_claim_status": "no_identity_claim",
                "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
                "promotion_status": "not_promoted",
                "rights_status": "source_marked_risk_noted",
                "risk_note": (
                    "Figshare package metadata reports CC BY 4.0; Scientific Data article "
                    "page uses CC BY-NC-ND 4.0. Raw package is 607933810 bytes and must "
                    "not be committed to regular Git."
                ),
                "caution": caution,
                "review_status": "reviewed_metadata_only",
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_packet_bucket(root: Path, rows: list[dict[str, str]], spec: dict[str, int | str]) -> None:
    bucket_path = root / bucket_directory(spec)
    if bucket_path.exists():
        for child in bucket_path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            elif child.name == "000_hust-obc-undeciphered-candidate-bucket-manifest.csv":
                child.unlink()
    bucket_path.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, str]] = []
    start = int(spec["start"])
    end = int(spec["end"])
    for bucket_sequence, row in enumerate(rows[start - 1:end], start=1):
        packet_path = root / row["materialized_candidate_packet_path"]
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        packet = {
            "unknown_candidate_id": row["unknown_candidate_id"],
            "record_type": "oracle_character_undeciphered_candidate_packet",
            "source_id": row["source_id"],
            "source_package_id": row["source_package_id"],
            "evidence_download_id": row["evidence_download_id"],
            "primary_external_ref_id": row["primary_external_ref_id"],
            "source_group": row["source_group"],
            "source_group_label": row["source_group_label"],
            "source_class_id": row["source_class_id"],
            "source_class_path": row["source_class_path"],
            "source_image_count": int(row["source_image_count"]),
            "first_source_image_path": row["first_source_image_path"],
            "last_source_image_path": row["last_source_image_path"],
            "filename_source_prefixes": row["filename_source_prefixes"],
            "decipherment_status": row["decipherment_status"],
            "identity_claim_status": row["identity_claim_status"],
            "assignment_status": row["assignment_status"],
            "promotion_status": row["promotion_status"],
            "rights_status": row["rights_status"],
            "risk_note": row["risk_note"],
            "caution": row["caution"],
            "review_status": row["review_status"],
            "updated_at": row["updated_at"],
        }
        packet_path.write_text(
            json.dumps(packet, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest_rows.append(
            {
                "bucket_sequence": f"{bucket_sequence:03d}",
                "unknown_candidate_id": row["unknown_candidate_id"],
                "primary_external_ref_id": row["primary_external_ref_id"],
                "packet_path": row["materialized_candidate_packet_path"],
                "source_group": row["source_group"],
                "source_class_id": row["source_class_id"],
                "source_image_count": row["source_image_count"],
                "review_status": row["review_status"],
                "updated_at": row["updated_at"],
            }
        )
    write_csv(
        root / bucket_manifest_path(spec),
        [
            "bucket_sequence",
            "unknown_candidate_id",
            "primary_external_ref_id",
            "packet_path",
            "source_group",
            "source_class_id",
            "source_image_count",
            "review_status",
            "updated_at",
        ],
        manifest_rows,
    )


def write_packets(root: Path, rows: list[dict[str, str]]) -> None:
    for spec in BUCKET_SPECS:
        write_packet_bucket(root, rows, spec)


def update_large_source_register(root: Path) -> None:
    path = root / LARGE_SOURCE_REGISTER
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
        fieldnames = file.readline()
    fieldnames_list = list(rows[0].keys()) if rows else []
    for row in rows:
        if row["source_package_id"] == SOURCE_PACKAGE_ID:
            row["source_url"] = SOURCE_URL
            row["access_method"] = (
                "Downloaded via figshare ndownloader after source and rights review; "
                "raw package kept outside regular Git."
            )
            row["downloaded_at"] = DOWNLOADED_AT
            row["file_size_bytes"] = str(RAW_SIZE_BYTES)
            row["checksum_sha256"] = RAW_SHA256
            row["storage_status"] = "downloaded_to_external_local_archive_registered"
            row["storage_hint"] = ARCHIVE_HINT
            materialized_end = max(int(spec["end"]) for spec in BUCKET_SPECS)
            row["handling_strategy"] = (
                "Commit only metadata-only undeciphered candidate index and first "
                f"{materialized_end} packet scaffolds; do not commit raw images."
            )
            manifest_paths = ";".join(bucket_manifest_path(spec) for spec in BUCKET_SPECS)
            row["derived_record_paths"] = (
                "corpus/001_oracle-characters/000_character-registers/"
                "003_undeciphered-oracle-characters-index.csv;"
                f"{manifest_paths}"
            )
            row["rights_status"] = "source_marked_risk_noted"
            row["risk_note"] = (
                "Raw package exceeds 40 MiB and is not committed. Figshare metadata "
                "reports CC BY 4.0, while the Scientific Data article page uses "
                "CC BY-NC-ND 4.0. Article reports 9411 undeciphered characters; "
                "zip directory yielded 9408 candidate classes."
            )
            row["review_status"] = "reviewed_metadata_only"
            row["updated_at"] = UPDATED_AT
    if not fieldnames_list:
        return
    write_csv(path, fieldnames_list, rows)


def update_download_log(root: Path) -> None:
    path = root / DOWNLOAD_LOG
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    fieldnames = list(rows[0].keys()) if rows else [
        "download_id",
        "source_id",
        "url",
        "downloaded_at",
        "status",
        "http_status",
        "file_size_bytes",
        "checksum_sha256",
        "local_temp_path",
        "risk_note",
    ]
    rows = [row for row in rows if row.get("download_id") != DOWNLOAD_ID]
    rows.append(
        {
            "download_id": DOWNLOAD_ID,
            "source_id": SOURCE_ID,
            "url": SOURCE_URL,
            "downloaded_at": DOWNLOADED_AT,
            "status": "downloaded",
            "http_status": "200",
            "file_size_bytes": str(RAW_SIZE_BYTES),
            "checksum_sha256": RAW_SHA256,
            "local_temp_path": ARCHIVE_HINT,
            "risk_note": (
                f"Raw zip kept outside regular Git; MD5 {FIGSHARE_MD5} matches "
                "figshare API. Zip directory lists 9408 undeciphered candidate "
                "classes and 62989 undeciphered images, while article reports "
                "9411 undeciphered characters."
            ),
        }
    )
    write_csv(path, fieldnames, rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-path", default=DEFAULT_ZIP_PATH)
    args = parser.parse_args()
    root = repo_root()
    zip_path = Path(args.zip_path)
    if not zip_path.is_absolute():
        zip_path = root / zip_path
    if not zip_path.exists():
        archive_path = Path(EXTERNAL_ARCHIVE_PATH)
        if archive_path.exists():
            zip_path = archive_path
    if not zip_path.exists():
        raise SystemExit(f"missing HUST-OBC raw zip: {zip_path}")
    rows = collect_candidates(zip_path)
    write_csv(root / INDEX_PATH, INDEX_FIELDS, rows)
    write_packets(root, rows)
    update_large_source_register(root)
    update_download_log(root)
    group_counts = Counter(row["source_group"] for row in rows)
    image_count = sum(int(row["source_image_count"]) for row in rows)
    print(
        "wrote "
        f"{len(rows)} undeciphered candidates; groups={dict(group_counts)}; "
        f"images={image_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
