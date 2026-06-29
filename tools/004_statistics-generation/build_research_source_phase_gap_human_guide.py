#!/usr/bin/env python3
"""Build a human guide for research-source phase gaps.

The guide turns the 193 checklist into a human-readable review entrance. It
does not collect evidence, record outcomes, decide rights, promote sources,
import corpus records, or make decipherment claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CHECKLIST = STAT_DIR / "193_research-source-phase-gap-review-checklist.csv"
ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
ASSIGNMENT_CHECKLIST = (
    STAT_DIR
    / "185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/"
    "000_source-registers/001_all-sources-index.csv"
)
SOURCE_OBJECT_ROOT = Path(
    "corpus/006_research-sources-and-bibliography/001_source-objects"
)
LARGE_SOURCE_REGISTER = Path(
    "project_registry/006_large-source-register/001_large-source-register.csv"
)
DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = STAT_DIR / "216_research-source-phase-gap-human-guide.md"
UPDATED_AT = "2026-06-30"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def unique_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def build_markdown(root: Path) -> str:
    rows = read_csv_rows(root / CHECKLIST)
    first = rows[0]
    phase_statuses = [f"{row['phase_name']}: `{row['phase_status']}`" for row in rows]
    source_ids = split_values(first["source_ids"])
    route_counts = split_values(first["assignment_route_counts"])

    lines = [
        "# Research Source Phase Gap Human Guide /",
        "研究来源阶段缺口人工复核指南",
        "",
        "English:",
        "This guide is the human entrance for research-source",
        "preprocessing phase gaps. It sends reviewers from the phase",
        "queue back to source-object dossiers, source registers,",
        "download logs, package manifests, field maps, extraction",
        "notes, rights notes, risk notes, and safe derived records.",
        "Each source must be checked for the human evidence it can",
        "support: glyph_image, inscription text, components, excavation",
        "context, collection context, relations, and bibliography.",
        "It is not a rights decision, not source promotion,",
        "not corpus import approval, not confirmed scholarship,",
        "and not a decipherment conclusion.",
        "",
        "简体中文：",
        "本指南是研究来源预处理阶段缺口的人工入口。",
        "复核者应从阶段缺口回到来源对象档案、来源登记、",
        "下载日志、package manifest、字段映射、抽取说明、",
        "权利说明、风险提示和安全派生记录。",
        "它不是权利决定，不是来源提升，不是语料导入批准，",
        "不是已确认学术结论，也不是释读结论。",
        "",
        "## Summary / 摘要",
        "",
        f"- updated at: {UPDATED_AT}",
        f"- checklist rows: {len(rows)}",
        f"- assignment groups: {first['assignment_group_count']}",
        f"- assignment source ids: {first['assignment_source_count_total']}",
        "- pipeline gap statuses:",
    ]
    for status in split_values(first["pipeline_gap_statuses"]):
        lines.append(f"  - `{status}`")
    for status in phase_statuses:
        lines.append(f"- {status}")
    for route_count in route_counts:
        if route_count.endswith("-004:7"):
            lines.append(f"- {route_count}")
    for source_id in source_ids:
        lines.append(f"- source id: `{source_id}`")

    lines.extend(
        [
            "",
            "## Human Review Entry Order / 人工复核入口顺序",
            "",
            "1. Open the source-object dossier first.",
            "2. Open the source-object `README.md`.",
            "3. Open `07_material-access-index.md`.",
            "4. Open `01_source-packet.json` only after the human file.",
            "5. Open `193_research-source-phase-gap-review-checklist.csv`.",
            "6. Open the matching 185 assignment checklist row.",
            "7. Open the all-sources index and large-source register.",
            "8. Check access or download record, date, and provider.",
            "9. Check source system, provider, catalog, book, paper, museum, or URL.",
            "10. Check package name, file size and checksum.",
            "11. Check package manifest, field map, extraction note.",
            "12. Check rights status, risk note, and public-commit decision.",
            "13. Check glyph_image, inscription, and collection evidence.",
            "14. Check components, excavation context, relations, literature.",
            "15. Check derived paths and safe derived records.",
            "16. Record reviewed outcomes only in the matching result log.",
            "",
            "人工复核时，先打开来源对象目录内的人类可读说明，",
            "再打开物料访问索引、来源 packet、阶段缺口清单、",
            "185 分配清单、来源总索引和大型来源登记。",
            "缺失项必须写成具体待查问题，不得写成空泛状态。",
            "",
            "## Support Files / 辅助文件",
            "",
            "| File | Path |",
            "| --- | --- |",
            f"| checklist | `{CHECKLIST.as_posix()}` |",
            f"| action queue | `{ACTION_QUEUE.as_posix()}` |",
            f"| assignment checklist | `{ASSIGNMENT_CHECKLIST.as_posix()}` |",
            f"| source index | `{SOURCE_INDEX.as_posix()}` |",
            f"| source objects | `{SOURCE_OBJECT_ROOT.as_posix()}` |",
            f"| large source register | `{LARGE_SOURCE_REGISTER.as_posix()}` |",
            f"| download log | `{DOWNLOAD_LOG.as_posix()}` |",
            "",
            "Use these files after opening a source-object human dossier.",
            "They are support pointers, not reviewed evidence by themselves.",
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
            "- Which source object and source id are being reviewed?",
            "- Which source system, provider, catalog, book, paper, museum,",
            "  or URL supplied the source?",
            "- Which access or download record, access date, package name,",
            "  file size and checksum locate it?",
            "- Which source package, manifest, field map, extraction note,",
            "  and derived paths let a reviewer audit it?",
            "- Which rights status, risk note, and public-commit decision",
            "  are visible beside the source?",
            "- Which glyph_image, inscription text, or plate evidence",
            "  can a human researcher inspect from this source?",
            "- Which components, variants, or near-form comparisons",
            "  can this source support without becoming a conclusion?",
            "- Which excavation, findspot, collection, period, or batch",
            "  evidence is present or still missing?",
            "- Which relations, citation links, bibliography notes,",
            "  proposer records, or disputes can this source support?",
            "- Which safe derived record or object-local dossier can be opened?",
            "- Which missing source, license, checksum, field, or review status",
            "  remains before an outcome can be recorded?",
            "- Which assignment group still has empty outcome slots by design?",
            "- 正在复核哪一个来源对象和来源 ID？",
            "- 哪个来源系统、提供者、著录、图书、论文、博物馆或 URL",
            "  提供了这个来源？",
            "- 哪条访问或下载记录、访问日期、来源包名、文件大小和",
            "  checksum 能够定位它？",
            "- 哪个来源包、manifest、字段映射、抽取说明和派生路径",
            "  能让复核者审计它？",
            "- 来源旁边是否已有权利状态、风险提示和公开提交决定？",
            "- 这个来源能让人检查哪条 glyph_image、卜辞文本或图版证据？",
            "- 这个来源能支持哪些构件、异体或近形比较而不变成结论？",
            "- 哪些出土、地点、馆藏、时期或批次证据存在或仍缺失？",
            "- 这个来源能支持哪些关系、引用、书目、提出者或争议记录？",
            "- 哪条安全派生记录或对象内档案可以直接打开？",
            "- 记录结果前，还缺哪个来源、许可、checksum、字段或状态？",
            "- 哪个分配组按设计仍保留空 outcome 栏位？",
            "",
            "## Boundary / 边界",
            "",
            "Do not record reviewed outcomes in this guide.",
            "Do not treat a checklist row, assignment group, source packet,",
            "manifest pointer, field-map pointer, or graph edge as scholarship.",
            "Do not decide rights, promote sources, or import corpus records.",
            "This guide is not corpus import approval.",
            "This guide is not confirmed scholarship.",
            "It is not a decipherment conclusion.",
            "",
            "不得在本指南中记录复核结论。",
            "不得把清单行、分配组、来源 packet、manifest 路线、",
            "字段映射路线或图路线当作学术结论。",
            "不得裁定权利，不得提升来源，也不得导入正式语料记录。",
            "本指南不是语料导入批准，不是已确认学术结论，",
            "也不是释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the research source phase gap human guide."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    write_markdown(root / args.output, build_markdown(root))
    print(f"research_source_phase_gap_human_guide={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
