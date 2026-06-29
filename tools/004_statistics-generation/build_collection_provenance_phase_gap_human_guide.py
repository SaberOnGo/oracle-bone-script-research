#!/usr/bin/env python3
"""Build a human guide for collection-provenance phase gaps.

The guide turns the 194 checklist into a human-readable review entrance. It is
navigation only: no evidence collection, rights decision, source promotion,
formal corpus import, collection-object identity claim, or decipherment claim.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STAT_DIR = Path("corpus/009_statistics-and-derived-features")
CHECKLIST = STAT_DIR / "194_collection-provenance-phase-gap-review-checklist.csv"
ACTION_QUEUE = STAT_DIR / "192_core-corpus-phase-gap-action-queue.csv"
COLLECTION_STAGING = Path(
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "001_institutional-collection-provenance-staging.csv"
)
OBJECT_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "006_collection-object-id-source-map.csv"
)
ASSET_SOURCE_INDEX = Path(
    "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
)
ASSET_RIGHTS_LOG = Path(
    "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv"
)
OBM_REVIEW_QUEUE = (
    STAT_DIR / "074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"
)
DEFAULT_OUTPUT = STAT_DIR / "215_collection-provenance-phase-gap-human-guide.md"
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
    phase_statuses = [f"{row['phase_name']}: `{row['phase_status']}`" for row in rows]
    first = rows[0]
    source_ids = sorted(
        unique_values(
            [
                sid
                for row in rows
                for field in [
                    "collection_source_ids",
                    "collection_object_source_ids",
                    "museum_object_asset_source_ids",
                    "obm_followup_source_ids",
                ]
                for sid in split_values(row[field])
            ]
        )
    )

    lines = [
        "# Collection Provenance Phase Gap Human Guide / ",
        "馆藏出土地阶段缺口人工复核指南",
        "",
        "English:",
        "This guide is the human entrance for collection provenance",
        "phase gaps. It sends a reviewer from the phase queue back",
        "to object-local dossiers, collection registers, object maps,",
        "asset source rows, rights logs, and raw-file boundaries.",
        "It is not a rights decision, not a source promotion,",
        "not a collection-object identity claim, not confirmed",
        "scholarship, and not a decipherment conclusion.",
        "",
        "简体中文：",
        "本指南是馆藏、出土地与资料权利阶段缺口的人工入口。",
        "复核者应从阶段缺口回到对象目录内档案、馆藏登记、",
        "对象 ID 映射、资产来源行、权利复核日志和原始文件边界。",
        "它不是权利决定，不是来源提升，不是馆藏对象身份断定，",
        "不是已确认学术结论，也不是释读结论。",
        "",
        "## Summary / 摘要",
        "",
        f"- updated at: {UPDATED_AT}",
        f"- checklist rows: {len(rows)}",
        f"- collection staging rows: {first['collection_staging_count']}",
        f"- collection object candidates: {first['collection_object_map_count']}",
        f"- museum object assets: {first['museum_object_asset_count']}",
        f"- OBM follow-up routes: {first['obm_followup_route_count']}",
    ]
    for source_id in source_ids:
        lines.append(f"- source id: `{source_id}`")
    for status in phase_statuses:
        lines.append(f"- {status}")

    lines.extend(
        [
            "",
            "## Human Review Entry Order / 人工复核入口顺序",
            "",
            "1. Open the object-local collection dossier first.",
            "2. Open `06_human-collection-dossier.md` first.",
            "3. Open `08_collection-provenance-evidence-dossier.md`.",
            "4. Open `10_collection-provenance-fact-matrix.md`.",
            "5. Check institution, object record, accession, or catalog number.",
            "6. Check source system, collection staging row, and ID map row.",
            "7. Check findspot, excavation site, period, batch, or pit context.",
            "8. Check image or object route before any visual comparison.",
            "9. Check file size, checksum, rights status, and risk note.",
            "10. Check components, relations, and scholarship routes.",
            "11. Check whether the raw package stays outside regular Git.",
            "12. Record only reviewed outcomes in the matching review log.",
            "",
            "人工复核时，先打开对象目录内的人类馆藏档案和来源证据档案。",
            "随后核对馆藏机构、对象记录、登记号、著录号、来源系统、",
            "出土地、遗址、时期、坑位或批次、图像路径、文件大小、",
            "checksum、权利状态和风险说明。",
            "缺失项必须写成具体待查问题，不得写成空泛状态。",
            "",
            "## Support Files / 辅助文件",
            "",
            "| File | Path |",
            "| --- | --- |",
            f"| checklist | `{CHECKLIST.as_posix()}` |",
            f"| action queue | `{ACTION_QUEUE.as_posix()}` |",
            f"| collection staging | `{COLLECTION_STAGING.as_posix()}` |",
            f"| object id map | `{OBJECT_MAP.as_posix()}` |",
            f"| asset source index | `{ASSET_SOURCE_INDEX.as_posix()}` |",
            f"| asset rights log | `{ASSET_RIGHTS_LOG.as_posix()}` |",
            f"| OBM review queue | `{OBM_REVIEW_QUEUE.as_posix()}` |",
            "| object root | `corpus/005_excavation-sites-periods-and-batches/` |",
            "",
            "Use these files after opening object-local human dossiers.",
            "They are support routes, not reviewed evidence by themselves.",
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "",
            "- Which collection object candidate is being reviewed?",
            "- Which institution, object record, accession, or catalog number",
            "  identifies it?",
            "- Which collection staging row and source system support it?",
            "- Which collection-object ID map row links it to source IDs?",
            "- Which findspot, excavation site, period, batch, or pit context",
            "  remains missing or uncertain?",
            "- Which image or object route can be opened for review?",
            "- Which asset source row, rights review row, file size, checksum,",
            "  rights status, and risk note limit public use?",
            "- Which raw package or unclear image stays outside regular Git?",
            "- Which components, relations, or scholarship routes need review?",
            "- Which object-local dossier or review sheet must be opened next?",
            "- Which missing item needs a human source check before promotion?",
            "- 正在复核哪一个馆藏对象候选？",
            "- 哪个馆藏机构、对象记录、登记号或著录号能够定位它？",
            "- 哪条馆藏 staging 行和来源系统支持它？",
            "- 哪条馆藏对象 ID 映射行把它连到来源 ID？",
            "- 哪个出土地、遗址、时期、批次或坑位背景仍缺失或不确定？",
            "- 哪条图像或对象路线可以打开复核？",
            "- 哪条资产来源行、权利复核行、文件大小、checksum、",
            "  权利状态和风险说明限制公开使用？",
            "- 哪个原始包或不清楚图像必须留在普通 Git 之外？",
            "- 哪些构件、关系或学术文献路线还需要复核？",
            "- 下一步应打开哪个对象内档案或复核表？",
            "- 哪个缺失项在提升前需要人工来源核查？",
            "",
            "## Boundary / 边界",
            "",
            "Do not import raw or unclear images from this guide.",
            "Do not treat a checklist row, source map, asset row,",
            "rights row, object route, or OBM route as confirmed evidence.",
            "Do not decide rights, promote a source, import corpus records,",
            "or make a collection-object identity claim.",
            "This guide is not confirmed scholarship.",
            "It is not a decipherment conclusion.",
            "",
            "不得根据本指南导入原始或不清楚图像。",
            "不得把清单行、来源映射、资产行、权利行、对象路线或 OBM",
            "路线当作已确认的证据。",
            "不得裁定权利，不得提升来源，不得导入正式语料记录，",
            "也不得作出馆藏对象身份断定。",
            "本指南不是已确认学术结论，也不是释读结论。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the collection provenance phase gap human guide."
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    write_markdown(root / args.output, build_markdown(root))
    print(f"collection_provenance_phase_gap_human_guide={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
