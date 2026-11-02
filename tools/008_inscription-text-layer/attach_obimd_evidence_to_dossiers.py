#!/usr/bin/env python3
"""Attach OBIMD inscription examples and distribution to character dossiers.

For every character dossier whose record.json lists OBIMD main-character UIDs
(cross_source_codepoint.obimd_main_uids), this writes section 4 (example
sentences) and section 5 (distribution) into README.md and the same data into
record.json. Running it again replaces the two sections.

Public quoting is limited on purpose: at most two example sentences per
dossier, plus plate numbers for further occurrences. OBIMD rights are
metadata_only_until_verified; the full text stays in the ignored local layer
built by build_obimd_inscription_text_layer.py.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_obimd_inscription_text_layer as layer  # noqa: E402

ROOT = layer.ROOT
CHAR_AREA = ROOT / "corpus/001_oracle-characters"
MAX_EXAMPLES = 2
MAX_PLATES = 10
SECTION_4_5 = re.compile(r"## 4 卜辞例句\n.*?(?=\n## (?:6|7|8|9|10|11) )", re.S)
STATUS_EXAMPLES = re.compile(r"例句：\d+")
OLD_TODO = "- 从 OBIMD 卜辞语料中取出这些 UID 的全部字例，抄录带著录号的例句，统计分期与共现字。\n"
NEW_TODO = ("- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为"
            "同一字，不等于字形相同。\n")


def long_path(path: Path) -> Path:
    text = str(path)
    if sys.platform == "win32" and not text.startswith("\\\\?\\"):
        return Path("\\\\?\\" + text)
    return path


def load_layer():
    data = json.loads(layer.DEFAULT_DATA.read_text(encoding="utf-8"))
    main = layer.load_main_characters()
    groups = layer.build_groups(data, main)
    index = defaultdict(list)
    for group in groups:
        for position, char in enumerate(group["chars"], 1):
            if char["uid"]:
                index[char["uid"]].append((group, position))
    stats = {}
    with (layer.PUBLIC_OUT / "002_obimd-glyph-occurrence-stats.csv").open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            stats[row["obimd_main_uid"]] = row
    return index, stats


def good_example(group: dict) -> bool:
    if group["category"] != "InscriptionSentence":
        return False
    length = len(group["chars"])
    unknown = sum(1 for c in group["chars"] if c["text"] == layer.UNKNOWN)
    return 4 <= length <= 16 and unknown * 4 <= length


def summarize(uids: list[str], index, stats) -> dict:
    hits = [hit for uid in uids for hit in index.get(uid, [])]
    hits.sort(key=lambda h: (layer.plate_sort_key(h[0]["plate"]), h[0]["group_index"], h[1]))
    examples, used = [], set()
    for group, position in hits:
        key = (group["plate"], group["group_index"])
        if key in used or not good_example(group):
            continue
        used.add(key)
        examples.append({
            "plate": group["plate"],
            "heji_candidate": group["heji_candidate"],
            "group_index": group["group_index"],
            "text": layer.display_text(group["text"]),
            "position": position,
            "length": len(group["chars"]),
        })
        if len(examples) == MAX_EXAMPLES:
            break
    plates = []
    for group, _ in hits:
        if group["plate"] not in plates:
            plates.append(group["plate"])
    categories = Counter(group["category"] for group, _ in hits)
    cooccur = Counter()
    for uid in uids:
        row = stats.get(uid)
        if not row or not row["top_cooccurring"]:
            continue
        for item in row["top_cooccurring"].split("|"):
            text, other, count = item.rsplit(":", 2)
            if other not in uids:
                cooccur[(text, other)] += int(count)
    return {
        "obimd_main_uids": uids,
        "occurrences": len(hits),
        "plates": len(plates),
        "plate_list_head": plates[:MAX_PLATES + MAX_EXAMPLES],
        "by_category": {layer.CATEGORY_ZH.get(k, k): v for k, v in categories.most_common()},
        "top_cooccurring": [{"text": t, "uid": u, "count": n} for (t, u), n in cooccur.most_common(6)],
        "examples": examples,
    }


def render(summary: dict) -> str:
    lines = ["## 4 卜辞例句", ""]
    if summary["examples"]:
        lines.append("以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，"
                     "◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片"
                     "核对（见案件 `case-h2-heji2`）。")
        lines.append("")
        lines.append("| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |")
        lines.append("| --- | --- | --- | --- |")
        for ex in summary["examples"]:
            lines.append(f"| {ex['plate']} | {ex['text']} | 第 {ex['position']}/{ex['length']} 字 | "
                         f"src-obimd {ex['plate']} 句组 {ex['group_index']} |")
        lines.append("")
    shown = {ex["plate"] for ex in summary["examples"]}
    others = [p for p in summary["plate_list_head"] if p not in shown][:MAX_PLATES]
    if others:
        lines.append(f"- 其他字例所在甲骨：{'、'.join(others)}"
                     f"{'等' if summary['plates'] > len(others) + len(shown) else ''}"
                     "〔来源 src-obimd〕。")
        lines.append("")
    lines.append("## 5 分布")
    lines.append("")
    cats = "，".join(f"{k} {v}" for k, v in summary["by_category"].items())
    lines.append(f"- OBIMD 中共 {summary['occurrences']} 个字例，见于 {summary['plates']} 片"
                 f"甲骨；按句组类别：{cats}〔来源 src-obimd，统计表 "
                 "`corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。")
    if summary["top_cooccurring"]:
        top = "、".join(f"{c['text']}（{c['count']}）" for c in summary["top_cooccurring"])
        lines.append(f"- 同一句组中最常一起出现的字：{top}。")
    lines.append("- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料"
                 "来源表补入。")
    lines.append("")
    return "\n".join(lines)


def insert_sections(text: str, block: str) -> str:
    if SECTION_4_5.search(text):
        return SECTION_4_5.sub(lambda _: block.rstrip("\n") + "\n", text, count=1)
    for anchor in ("## 6 ", "## 7 ", "## 8 ", "## 10 "):
        position = text.find("\n" + anchor)
        if position != -1:
            return text[: position + 1] + block + "\n" + text[position + 1:]
    return text.rstrip("\n") + "\n\n" + block


def main() -> int:
    index, stats = load_layer()
    updated = skipped = 0
    for record_path in sorted(CHAR_AREA.glob("*/*/record.json")):
        record_path = long_path(record_path)
        record = json.loads(record_path.read_text(encoding="utf-8"))
        uids = record.get("cross_source_codepoint", {}).get("obimd_main_uids", [])
        if not uids:
            continue
        summary = summarize(uids, index, stats)
        if not summary["occurrences"]:
            skipped += 1
            continue
        readme_path = record_path.with_name("README.md")
        text = readme_path.read_text(encoding="utf-8")
        text = insert_sections(text, render(summary))
        text = STATUS_EXAMPLES.sub(f"例句：{len(summary['examples'])}", text, count=1)
        text = text.replace(OLD_TODO, NEW_TODO)
        text = re.sub(r"([^\n])\n(## )", r"\1\n\n\2", text)
        record["inscription_evidence"] = summary
        record["status"]["example_sentences"] = len(summary["examples"])
        readme_path.write_text(text, encoding="utf-8", newline="\n")
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8", newline="\n")
        updated += 1
    print(f"dossiers updated: {updated}; matched UIDs without occurrences: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
