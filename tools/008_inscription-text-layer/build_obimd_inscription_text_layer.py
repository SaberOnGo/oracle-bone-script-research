#!/usr/bin/env python3
"""Build the OBIMD inscription text layer (architecture reset step 4).

Reads the registered OBIMD annotation file (large-src-000002, data.json) and
the OBIMD main-character register, and reconstructs every sentence group in
reading order.

Outputs
  Local only (ignored, personal research; OBIMD rights are
  metadata_only_until_verified):
    external_local_archive/derived/obimd-inscriptions/inscriptions.jsonl
    external_local_archive/derived/obimd-inscriptions/plates-NNNNN-NNNNN.md
  Public (statistics and identifiers only):
    corpus/002_oracle-bone-inscriptions/010_inscription-texts/
      001_obimd-plate-index.csv
      002_obimd-glyph-occurrence-stats.csv

Usage:
  python tools/008_inscription-text-layer/build_obimd_inscription_text_layer.py \
      [--data external_local_archive/source_packages/obimd/data.json]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "external_local_archive/source_packages/obimd/data.json"
MAIN_REGISTER = ROOT / "corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv"
LOCAL_OUT = ROOT / "external_local_archive/derived/obimd-inscriptions"
PUBLIC_OUT = ROOT / "corpus/002_oracle-bone-inscriptions/010_inscription-texts"
UNKNOWN = "□"
PRIVATE_USE = "◇"


def display_text(text: str) -> str:
    """Replace OBIMD non-standard codepoints, which render as garbage, with ◇.

    OBIMD encodes characters without a standard Unicode form either in the
    private-use areas or in unassigned planes 4--14.
    """
    out = []
    for ch in text:
        cp = ord(ch)
        private = 0xE000 <= cp <= 0xF8FF or cp >= 0x40000
        out.append(PRIVATE_USE if private else ch)
    return "".join(out)
CATEGORY_ZH = {
    "InscriptionSentence": "卜辞句",
    "OracleSequence": "兆序",
    "OracleOutcome": "验辞",
    "Uncertain": "未定",
}


def load_main_characters(path: Path = MAIN_REGISTER) -> dict[str, str]:
    """Map OBIMD main-character UID to one normalized transcription."""
    table = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            values = [v for v in row["transcription_values"].split("|") if v]
            table[row["source_uid"]] = row["codepoint"] or (values[0] if values else UNKNOWN)
    return table


def plate_sort_key(name: str) -> tuple[int, str]:
    match = re.match(r"H(\d+)", name)
    return (int(match.group(1)) if match else 10**9, name)


def build_groups(data: list[dict], main: dict[str, str]) -> list[dict]:
    """Return one record per sentence group, characters in reading order."""
    groups = []
    for plate in data:
        name = plate["RubbingName"]
        for index, group in enumerate(plate["RecordUtilSentenceGroupVoList"], 1):
            category = re.sub(r"\d+$", "", group["GroupCategory"])
            chars = []
            for char in group["RecordUtilOracleCharVoList"]:
                uid = char.get("Label")
                chars.append({
                    "order": int(char.get("OrderNumber", 0)),
                    "uid": uid,
                    "text": main.get(uid, UNKNOWN) if uid else UNKNOWN,
                    "bbox_xywh": char.get("Position", ""),
                    "placeholder": char.get("SeatFont") in (1, "1"),
                    "mark": char.get("Mark"),
                })
            chars.sort(key=lambda c: c["order"])
            groups.append({
                "plate": name,
                "heji_candidate": name[1:] if name.startswith("H") else "",
                "group_index": index,
                "group_label": group["GroupCategory"],
                "category": category,
                "text": "".join(c["text"] for c in chars),
                "chars": chars,
                "rubbing_member": plate.get("Rubbing", ""),
                "facsimile_member": plate.get("Facsimile", ""),
            })
    groups.sort(key=lambda g: (plate_sort_key(g["plate"]), g["group_index"]))
    return groups


def glyph_statistics(groups: list[dict], main: dict[str, str]) -> list[dict]:
    occurrences = Counter()
    plates = defaultdict(set)
    by_category = defaultdict(Counter)
    cooccur = defaultdict(Counter)
    for group in groups:
        uids = [c["uid"] for c in group["chars"] if c["uid"]]
        for uid in uids:
            occurrences[uid] += 1
            plates[uid].add(group["plate"])
            by_category[uid][group["category"]] += 1
        for uid in set(uids):
            for other in set(uids) - {uid}:
                cooccur[uid][other] += 1
    rows = []
    for uid, count in occurrences.most_common():
        top = cooccur[uid].most_common(8)
        rows.append({
            "obimd_main_uid": uid,
            "transcription": display_text(main.get(uid, "")),
            "occurrences": count,
            "plates": len(plates[uid]),
            "inscription_sentence": by_category[uid]["InscriptionSentence"],
            "oracle_sequence": by_category[uid]["OracleSequence"],
            "oracle_outcome": by_category[uid]["OracleOutcome"],
            "uncertain": by_category[uid]["Uncertain"],
            "top_cooccurring": "|".join(f"{display_text(main.get(o, o))}:{o}:{n}" for o, n in top),
            "source_id": "src-obimd",
            "rights_status": "metadata_only_until_verified",
        })
    return rows


def plate_index(groups: list[dict]) -> list[dict]:
    plates = defaultdict(lambda: {"groups": 0, "chars": 0, "unknown": 0, "categories": Counter()})
    for group in groups:
        entry = plates[group["plate"]]
        entry["groups"] += 1
        entry["chars"] += len(group["chars"])
        entry["unknown"] += sum(1 for c in group["chars"] if c["text"] == UNKNOWN)
        entry["categories"][group["category"]] += 1
    rows = []
    for name in sorted(plates, key=plate_sort_key):
        entry = plates[name]
        rows.append({
            "obimd_plate": name,
            "heji_number_candidate": name[1:] if name.startswith("H") else "",
            "sentence_groups": entry["groups"],
            "character_occurrences": entry["chars"],
            "unidentified_or_placeholder": entry["unknown"],
            "group_categories": "|".join(f"{k}:{v}" for k, v in sorted(entry["categories"].items())),
            "source_id": "src-obimd",
            "identity_note": "H-number to Heji number is a candidate mapping; see case-h2-heji2",
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_local(groups: list[dict]) -> None:
    LOCAL_OUT.mkdir(parents=True, exist_ok=True)
    with (LOCAL_OUT / "inscriptions.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for group in groups:
            handle.write(json.dumps(group, ensure_ascii=False) + "\n")
    buckets = defaultdict(list)
    for group in groups:
        number = plate_sort_key(group["plate"])[0]
        start = (number - 1) // 1000 * 1000 + 1
        buckets[start].append(group)
    for start, items in buckets.items():
        lines = [f"# OBIMD 卜辞释文 H{start}--H{start + 999}", "",
                 "本地研究用，不随仓库公开。字序按 OBIMD 阅读顺序；□ 为未识别或占位字，"
                 "◇ 为 OBIMD 私用区自造字（原码位见 inscriptions.jsonl）。", "",
                 "| 片号 | 句组 | 类别 | 释文 |", "| --- | --- | --- | --- |"]
        for group in items:
            lines.append(f"| {group['plate']} | {group['group_index']} | "
                         f"{CATEGORY_ZH.get(group['category'], group['category'])} | {display_text(group['text'])} |")
        (LOCAL_OUT / f"plates-{start:05d}-{start + 999:05d}.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    raw = args.data.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    main_table = load_main_characters()
    groups = build_groups(data, main_table)
    write_local(groups)
    write_csv(PUBLIC_OUT / "001_obimd-plate-index.csv", plate_index(groups))
    write_csv(PUBLIC_OUT / "002_obimd-glyph-occurrence-stats.csv", glyph_statistics(groups, main_table))
    chars = sum(len(g["chars"]) for g in groups)
    unknown = sum(1 for g in groups for c in g["chars"] if c["text"] == UNKNOWN)
    print(f"data.json sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}")
    print(f"plates={len(data)} groups={len(groups)} characters={chars} unidentified={unknown}")
    print(f"local corpus: {LOCAL_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
