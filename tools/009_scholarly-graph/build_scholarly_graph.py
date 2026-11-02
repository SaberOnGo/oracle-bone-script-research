#!/usr/bin/env python3
"""Build the scholarly relationship graph (architecture reset step 6).

Edges describe scholarly relations, not file routes. Every edge carries
source_ref, status, and note.

Public edges (corpus/008_relationship-graph/100_scholarly-graph/):
  dataset_label             obs-char -> character   HUST-OBC official table
  same_character_candidate  obs-char -> OBIMD glyph same transcription
  same_character_candidate  obs-char -> EvoBC class same label
  catalog_clue              obs-char -> Heji number from sample file name
  co_occurs                 OBIMD glyph <-> glyph    aggregated counts only
Local edges (ignored; they would reconstruct OBIMD text):
  occurs_in                 OBIMD glyph -> plate sentence group, position

Usage: python tools/009_scholarly-graph/build_scholarly_graph.py [--min-cooccur 5]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "008_inscription-text-layer"))
import build_obimd_inscription_text_layer as layer  # noqa: E402

CHAR_AREA = ROOT / "corpus/001_oracle-characters"
OUT = ROOT / "corpus/008_relationship-graph/100_scholarly-graph"
LOCAL_OUT = ROOT / "external_local_archive/derived/graph"
LABEL_REGISTER = "corpus/001_oracle-characters/000_character-registers/012_hust-obc-official-deciphered-labels.csv"
STATS = "corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv"


def long_path(path: Path) -> Path:
    text = str(path)
    if sys.platform == "win32" and not text.startswith("\\\\?\\"):
        return Path("\\\\?\\" + text)
    return path


def edge(kind, source, target, source_ref, status, note, **extra):
    record = {"edge_type": kind, "source": source, "target": target,
              "source_ref": source_ref, "status": status, "note": note}
    record.update(extra)
    record["edge_id"] = f"{kind}:{source}->{target}"
    return record


def dossier_edges():
    edges = []
    for record_path in sorted(CHAR_AREA.glob("*/*/record.json")):
        record = json.loads(long_path(record_path).read_text(encoding="utf-8"))
        node = record["id"]
        label = record.get("dataset_label")
        if label:
            for category, char in label.get("labels_by_category", {}).items():
                edges.append(edge("dataset_label", node, char, f"{LABEL_REGISTER}#{category}",
                                  "source_reported", "HUST-OBC official label; not a reviewed reading",
                                  hust_category=category))
        cross = record.get("cross_source_codepoint", {})
        for uid in cross.get("obimd_main_uids", []):
            edges.append(edge("same_character_candidate", node, f"obimd-main-{uid}",
                              "corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv",
                              "candidate", "same transcription in HUST-OBC and OBIMD; glyph identity unchecked"))
        for category in cross.get("evobc_category_ids", []):
            edges.append(edge("same_character_candidate", node, category,
                              "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/001_evobc-evolution-category-staging.csv",
                              "candidate", "same label in HUST-OBC and EvoBC; glyph identity unchecked"))
        clue = record.get("filename_catalog_clue", {})
        if clue.get("heji"):
            edges.append(edge("catalog_clue", node, f"heji-{clue['heji'].lstrip('合補')}",
                              f"sample file name {clue.get('file_name', '')}", "filename_clue",
                              "parsed from the HUST-OBC sample file name; not checked in the catalog"))
    return edges


def cooccur_and_occurs(min_count):
    data = json.loads(layer.DEFAULT_DATA.read_text(encoding="utf-8"))
    main = layer.load_main_characters()
    groups = layer.build_groups(data, main)
    pairs = Counter()
    occurs = []
    for group in groups:
        uids = sorted({c["uid"] for c in group["chars"] if c["uid"]})
        for i, a in enumerate(uids):
            for b in uids[i + 1:]:
                pairs[(a, b)] += 1
        for position, char in enumerate(group["chars"], 1):
            if char["uid"]:
                occurs.append(edge("occurs_in", f"obimd-main-{char['uid']}",
                                   f"{group['plate']}#{group['group_index']}",
                                   f"src-obimd data.json {group['plate']}", "source_reported",
                                   "OBIMD annotation", position=position, category=group["category"]))
    cooccur = [
        edge("co_occurs", f"obimd-main-{a}", f"obimd-main-{b}", STATS, "source_derived_count",
             "same OBIMD sentence group", count=n,
             source_text=layer.display_text(main.get(a, "")), target_text=layer.display_text(main.get(b, "")))
        for (a, b), n in pairs.most_common() if n >= min_count
    ]
    return cooccur, occurs


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--min-cooccur", type=int, default=5)
    args = parser.parse_args()
    dossier = dossier_edges()
    cooccur, occurs = cooccur_and_occurs(args.min_cooccur)
    write_jsonl(OUT / "001_character-identity-edges.jsonl", dossier)
    write_jsonl(OUT / "002_glyph-cooccurrence-edges.jsonl", cooccur)
    write_jsonl(LOCAL_OUT / "occurs_in.jsonl", occurs)
    summary = Counter(e["edge_type"] + "|" + e["status"] for e in dossier + cooccur)
    summary.update({"occurs_in|source_reported (local only)": len(occurs)})
    with (OUT / "000_edge-summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["edge_type", "status", "count"])
        for key, count in sorted(summary.items()):
            kind, status = key.split("|", 1)
            writer.writerow([kind, status, count])
    for key, count in sorted(summary.items()):
        print(f"{key}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
