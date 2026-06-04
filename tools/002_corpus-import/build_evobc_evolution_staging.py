#!/usr/bin/env python3
"""Build reviewed EVOBC evolution-chain staging records from downloaded metadata."""

from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path


SOURCE_ID = "src-evobc"
KEY_VALUE_DOWNLOAD_ID = "dl-evobc-key-value-json"
LIST_DOWNLOAD_ID = "dl-evobc-list-json"
RIGHTS_STATUS = "source_marked_risk_noted"
REVIEW_STATUS = "reviewed_metadata_only"
IMPORT_STATUS = "dataset_candidate_not_promoted"
UPDATED_AT = "2026-06-04"

ERA_CODEBOOK = {
    0: ("OBC", "Oracle Bone Characters", "\u7532\u9aa8\u6587\u5b57"),
    1: ("BI", "Bronze Inscriptions", "\u91d1\u6587"),
    2: ("SS", "Seal Script", "\u7bc6\u4e66"),
    3: ("SAC", "Spring and Autumn period Characters", "\u6625\u79cb\u6587\u5b57"),
    4: ("WSC", "Warring States period Characters", "\u6218\u56fd\u6587\u5b57"),
    5: ("CS", "Clerical Script", "\u96b6\u4e66"),
}

CATEGORY_COLUMNS = [
    "candidate_evolution_category_id",
    "source_id",
    "evidence_download_id_key_value",
    "evidence_download_id_list",
    "source_category_id",
    "source_character_label",
    "source_character_codepoints",
    "image_reference_count",
    "era_code_counts",
    "era_token_counts",
    "source_code_counts",
    "source_token_counts",
    "has_oracle_bone_refs",
    "has_bronze_refs",
    "has_seal_refs",
    "has_spring_autumn_refs",
    "has_warring_states_refs",
    "has_clerical_refs",
    "project_import_status",
    "rights_status",
    "caution",
    "review_status",
    "updated_at",
]

CODEBOOK_COLUMNS = [
    "codebook_row_id",
    "source_id",
    "evidence_download_id",
    "code_type",
    "code_value",
    "observed_token",
    "label_en",
    "label_zh",
    "reference_basis",
    "image_reference_count",
    "caution",
    "review_status",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def compact_counts(counter: collections.Counter[object]) -> str:
    parts = []
    for key in sorted(counter, key=lambda value: (str(type(value)), str(value))):
        if key is None:
            label = "unknown"
        else:
            label = str(key).strip() or "blank"
        parts.append(f"{label}:{counter[key]}")
    return ";".join(parts)


def codepoints(text: str) -> str:
    return ";".join(f"U+{ord(char):04X}" for char in text)


def filename_tokens(file_name: str) -> tuple[str, str]:
    parts = file_name.split("_")
    source_token = parts[1].strip() if len(parts) > 1 else "unknown"
    era_token = parts[2].strip() if len(parts) > 2 else "unknown"
    return source_token or "blank", era_token or "blank"


def load_metadata(key_value_path: Path, list_path: Path) -> tuple[dict[str, str], list[dict[str, object]]]:
    key_value = json.loads(key_value_path.read_text(encoding="utf-8"))
    records = json.loads(list_path.read_text(encoding="utf-8"))
    if not isinstance(key_value, dict) or not isinstance(records, list):
        raise ValueError("Unexpected EVOBC metadata shape")
    return key_value, records


def build_category_rows(key_value: dict[str, str], records: list[dict[str, object]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        source_category_id = str(record.get("ID", ""))
        character_label = str(record.get("Character", ""))
        key_value_label = key_value.get(source_category_id, "")
        if key_value_label and key_value_label != character_label:
            raise ValueError(f"EVOBC label mismatch for {source_category_id}")

        images = record.get("images") or []
        if not isinstance(images, list):
            raise ValueError(f"EVOBC images field is not a list for {source_category_id}")

        era_codes: collections.Counter[object] = collections.Counter()
        source_codes: collections.Counter[object] = collections.Counter()
        era_tokens: collections.Counter[str] = collections.Counter()
        source_tokens: collections.Counter[str] = collections.Counter()

        for image in images:
            if not isinstance(image, dict):
                raise ValueError(f"EVOBC image entry is not an object for {source_category_id}")
            era_codes[image.get("era")] += 1
            source_codes[image.get("source")] += 1
            source_token, era_token = filename_tokens(str(image.get("file", "")))
            source_tokens[source_token] += 1
            era_tokens[era_token] += 1

        rows.append(
            {
                "candidate_evolution_category_id": f"evobc-evo-cat-{index:05d}",
                "source_id": SOURCE_ID,
                "evidence_download_id_key_value": KEY_VALUE_DOWNLOAD_ID,
                "evidence_download_id_list": LIST_DOWNLOAD_ID,
                "source_category_id": source_category_id,
                "source_character_label": character_label,
                "source_character_codepoints": codepoints(character_label),
                "image_reference_count": str(len(images)),
                "era_code_counts": compact_counts(era_codes),
                "era_token_counts": compact_counts(era_tokens),
                "source_code_counts": compact_counts(source_codes),
                "source_token_counts": compact_counts(source_tokens),
                "has_oracle_bone_refs": str(era_codes[0] > 0).lower(),
                "has_bronze_refs": str(era_codes[1] > 0).lower(),
                "has_seal_refs": str(era_codes[2] > 0).lower(),
                "has_spring_autumn_refs": str(era_codes[3] > 0).lower(),
                "has_warring_states_refs": str(era_codes[4] > 0).lower(),
                "has_clerical_refs": str(era_codes[5] > 0).lower(),
                "project_import_status": IMPORT_STATUS,
                "rights_status": RIGHTS_STATUS,
                "caution": (
                    "EVOBC category and image-reference metadata is not an accepted "
                    "paleographic correspondence until cross-source review is complete."
                ),
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def build_codebook_rows(category_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    era_totals: collections.Counter[int] = collections.Counter()

    for row in category_rows:
        for part in row["era_code_counts"].split(";"):
            if not part:
                continue
            key, value = part.split(":", 1)
            if key.isdigit():
                era_totals[int(key)] += int(value)

    rows: list[dict[str, str]] = []
    row_index = 1
    for code, (token, label_en, label_zh) in ERA_CODEBOOK.items():
        rows.append(
            {
                "codebook_row_id": f"evobc-code-{row_index:03d}",
                "source_id": SOURCE_ID,
                "evidence_download_id": LIST_DOWNLOAD_ID,
                "code_type": "era",
                "code_value": str(code),
                "observed_token": token,
                "label_en": label_en,
                "label_zh": label_zh,
                "reference_basis": "EVOBC README shorthand table and List_of_EVOBC filename tokens.",
                "image_reference_count": str(era_totals[code]),
                "caution": "Era labels are EVOBC dataset labels and still require source-chain review.",
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
        row_index += 1

    return rows


def add_source_codebook_rows(
    codebook_rows: list[dict[str, str]],
    records: list[dict[str, object]],
) -> None:
    source_totals: collections.Counter[int] = collections.Counter()
    token_by_code: dict[int, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for record in records:
        for image in record.get("images") or []:
            if not isinstance(image, dict):
                continue
            code = image.get("source")
            if not isinstance(code, int):
                continue
            source_totals[code] += 1
            source_token, _ = filename_tokens(str(image.get("file", "")))
            token_by_code[code][source_token] += 1

    next_index = len(codebook_rows) + 1
    for code in sorted(source_totals):
        codebook_rows.append(
            {
                "codebook_row_id": f"evobc-code-{next_index:03d}",
                "source_id": SOURCE_ID,
                "evidence_download_id": LIST_DOWNLOAD_ID,
                "code_type": "source",
                "code_value": str(code),
                "observed_token": compact_counts(token_by_code[code]),
                "label_en": "",
                "label_zh": "",
                "reference_basis": (
                    "Observed from List_of_EVOBC filename tokens; not an official "
                    "source-name mapping."
                ),
                "image_reference_count": str(source_totals[code]),
                "caution": "Source code labels are not documented in the README and must not be overinterpreted.",
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
        next_index += 1


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--key-value",
        type=Path,
        default=root / "tmp/source_downloads/dl-evobc-key-value-json.json",
    )
    parser.add_argument(
        "--list-json",
        type=Path,
        default=root / "tmp/source_downloads/dl-evobc-list-json.json",
    )
    parser.add_argument(
        "--category-output",
        type=Path,
        default=(
            root
            / "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            / "001_evobc-evolution-category-staging.csv"
        ),
    )
    parser.add_argument(
        "--codebook-output",
        type=Path,
        default=(
            root
            / "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
            / "002_evobc-era-source-codebook-staging.csv"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    key_value, records = load_metadata(args.key_value, args.list_json)
    category_rows = build_category_rows(key_value, records)
    codebook_rows = build_codebook_rows(category_rows)
    add_source_codebook_rows(codebook_rows, records)
    write_csv(args.category_output, CATEGORY_COLUMNS, category_rows)
    write_csv(args.codebook_output, CODEBOOK_COLUMNS, codebook_rows)
    print(f"Wrote {len(category_rows)} EVOBC category staging rows")
    print(f"Wrote {len(codebook_rows)} EVOBC codebook staging rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
