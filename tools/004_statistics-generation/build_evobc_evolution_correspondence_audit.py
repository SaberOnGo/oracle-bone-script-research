#!/usr/bin/env python3
"""Build the human audit for EVOBC evolution-route candidates."""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from collections import Counter
from pathlib import Path


CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/"
    "000_evolution-registers/001_evobc-evolution-category-staging.csv"
)
GRAPH_PATH = Path(
    "corpus/008_relationship-graph/"
    "017_evobc-evolution-correspondence-candidate-graph-edges.jsonl"
)
HUMAN_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "234_evobc-evolution-correspondence-audit.md"
)
INDEX_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "235_evobc-evolution-correspondence-audit-index.json"
)
MAX_LINE_LENGTH = 80


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wrap(value: str) -> str:
    return textwrap.fill(
        value,
        width=78,
        break_long_words=True,
        break_on_hyphens=False,
    )


def read_categories(root: Path) -> list[dict[str, str]]:
    with (root / CATEGORY_STAGING).open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


def parse_counts(value: str) -> dict[int, int]:
    result: dict[int, int] = {}
    for token in value.split(";"):
        if token:
            code, count = token.rsplit(":", 1)
            result[int(code)] = int(count)
    return result


def read_graph_rows(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with (root / GRAPH_PATH).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_audit(root: Path) -> tuple[str, dict[str, object]]:
    categories = read_categories(root)
    graph_rows = read_graph_rows(root)
    mixed_categories: set[str] = set()
    later_code_counts: Counter[int] = Counter()
    expected_candidate_edges = 0
    for row in categories:
        era_counts = parse_counts(row.get("era_code_counts", ""))
        later_codes = sorted(code for code in era_counts if code > 0)
        if 0 not in era_counts or not later_codes:
            continue
        mixed_categories.add(row["candidate_evolution_category_id"])
        expected_candidate_edges += len(later_codes)
        later_code_counts.update(later_codes)

    graph_candidate_edges = [
        row
        for row in graph_rows
        if row.get("candidate_correspondence_status")
        == "candidate_evolution_correspondence_route"
    ]
    formal_correspondence_count = sum(
        1
        for row in graph_rows
        if row.get("candidate_correspondence_status")
        == "accepted_paleographic_correspondence"
    )
    index: dict[str, object] = {
        "record_type": "evobc_evolution_correspondence_audit_index",
        "human_readable_file": HUMAN_OUTPUT.as_posix(),
        "graph_file": GRAPH_PATH.as_posix(),
        "category_staging_file": CATEGORY_STAGING.as_posix(),
        "mixed_era_category_count": len(mixed_categories),
        "candidate_evolution_correspondence_edge_count": expected_candidate_edges,
        "graph_candidate_field_count": len(graph_candidate_edges),
        "later_era_code_counts": {
            str(code): later_code_counts[code]
            for code in sorted(later_code_counts)
        },
        "formal_correspondence_count": formal_correspondence_count,
        "route_integrity_confidence": "high",
        "hypothesis_probability": None,
        "candidate_route_status": "dataset_candidate_not_promoted",
        "review_status": "reviewed_metadata_only",
        "rights_status": "source_marked_risk_noted",
        "claim_boundary": [
            "dataset category co-membership only",
            "not a confirmed later-form correspondence",
            "not a decipherment conclusion",
        ],
        "required_next_checks": [
            "open original image references for each category",
            "verify catalog, period, and source provenance",
            "write an independent paleographic comparison",
            "compare inscription context and opposing evidence",
        ],
        "updated_at": "2026-08-13",
    }
    if expected_candidate_edges != len(graph_candidate_edges):
        raise ValueError(
            "staging and graph candidate counts disagree: "
            f"{expected_candidate_edges} != {len(graph_candidate_edges)}"
        )

    paragraphs = [
        "# EVOBC Evolution-Correspondence Audit / "
        "EVOBC 演化—对应关系审计",
        "",
        "## Human Reading Result / 人类阅读结果",
        "",
        wrap(
            f"The EVOBC staging table contains {len(mixed_categories):,} categories "
            f"with both an Oracle Bone Characters code and at least one later-era "
            f"code. They yield {expected_candidate_edges:,} candidate category-to-era "
            "routes."
        ),
        wrap(
            f"EVOBC 暂存表中有 {len(mixed_categories)} 个类别同时含甲骨文字代码和至少一个后世时代代码，"
            f"共形成 {expected_candidate_edges:,} 条类别—时代候选路线。"
        ),
        "",
        wrap(
            "These counts describe dataset co-membership. They do not show that "
            "the same written form, reading, meaning, or historical object was "
            "carried across eras."
        ),
        wrap(
            "这些数量只说明数据集类别的共同收录，不证明同一字形、读音、意义或历史对象跨时代延续。"
        ),
        "",
        "- Formal paleographic correspondences recorded: 0.",
        "- 已记录的正式文字学对应关系：0。",
        "- Candidate probabilities: not estimated.",
        "- 候选概率：未估计。",
        "",
        "## Later-Era Route Counts / 后世时代路线数量",
        "",
        *[
            f"- Era code {code}: {later_code_counts[code]} candidate routes."
            for code in sorted(later_code_counts)
        ],
        *[
            f"- 时代代码 {code}：{later_code_counts[code]} 条候选路线。"
            for code in sorted(later_code_counts)
        ],
        "",
        wrap(
            "The graph field candidate_correspondence_status marks these rows as "
            "candidate_evolution_correspondence_route. Its route integrity "
            "confidence is high because the CSV and codebook join is reproducible; "
            "that is not a semantic probability."
        ),
        wrap(
            "图边字段 candidate_correspondence_status 将这些行标为候选演化对应路线。"
            "路线完整性置信度为 high，只表示 CSV 与代码表连接可复跑，不是语义概率。"
        ),
        "",
        "## Source Route / 来源路线",
        "",
        wrap(
            f"Start with `{CATEGORY_STAGING.as_posix()}` and the EVOBC codebook "
            "used by the graph builder. Then open the EVOBC source dossier and "
            "the cited original image or book/web route for the category."
        ),
        wrap(
            f"先打开 `{CATEGORY_STAGING.as_posix()}` 和图边生成器使用的 EVOBC 代码表，"
            "再打开 EVOBC 来源档案，并按类别追查原始图像或书籍、网页路线。"
        ),
        "",
        "## Evidence Still Required / 仍需补齐的证据",
        "",
        wrap(
            "For each proposed route, record the original image member, catalog "
            "or page, period attribution, source provenance, and any competing "
            "classification before making a paleographic comparison."
        ),
        wrap(
            "每条候选路线都必须补充原始图像成员、著录或页码、时期归属、来源证据和不同分类，"
            "之后才可以进行文字学比较。"
        ),
        "",
        "- Do not turn a modern label into a reading or meaning.",
        "- 不要把今字标签改写成释读或字义。",
        "- Do not treat a dataset era token as a historical date.",
        "- 不要把数据集时代代码当成已核定的历史年代。",
        "- Keep missing image, catalog, and inscription evidence explicit.",
        "- 图像、著录和卜辞证据缺失时，必须具体写出待查项。",
        "",
        "## Boundary / 边界",
        "",
        wrap(
            "This page is a human research route for preprocessing. It is not an "
            "accepted evolution chain, not a decipherment conclusion, and not "
            "scholarly confirmation."
        ),
        wrap(
            "本页只是面向人类研究的预处理路线，不记录已接受的演化链，不构成释读或破译，"
            "也不构成学术确认。"
        ),
        "",
    ]
    text = "\n".join(paragraphs)
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH:
            raise ValueError(f"{HUMAN_OUTPUT}:{line_number} exceeds 80 characters")
    return text, index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    text, index = build_audit(root)
    (root / HUMAN_OUTPUT).write_text(text, encoding="utf-8", newline="\n")
    (root / INDEX_OUTPUT).write_text(
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"mixed_categories={index['mixed_era_category_count']} "
        f"candidate_edges={index['candidate_evolution_correspondence_edge_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
