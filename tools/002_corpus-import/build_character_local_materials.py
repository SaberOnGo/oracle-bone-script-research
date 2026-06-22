#!/usr/bin/env python3
"""Build co-located human and AI material indexes for character directories."""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from pathlib import Path


MAX_HUMAN_MARKDOWN_LINE_LENGTH = 80
OBS_CHAR_LOCAL_MATERIAL_LIMIT = 1588
EXTRA_TARGET_PROJECT_IDS = ("obs-unk-005708", "obs-unk-006294")
TARGET_PROJECT_IDS = tuple(
    [f"obs-char-{index:06d}" for index in range(1, OBS_CHAR_LOCAL_MATERIAL_LIMIT + 1)]
    + list(EXTRA_TARGET_PROJECT_IDS)
)
IMAGE_REFERENCE_RESULTS = (
    "corpus/009_statistics-and-derived-features/"
    "068_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-results.csv"
)
VISUAL_INDEX_FIELDS = [
    "visual_source_index_id",
    "project_id",
    "primary_external_ref_id",
    "source_id",
    "source_package_id",
    "download_id",
    "visual_material_status",
    "committed_image_path",
    "source_image_reference_path",
    "source_image_sequence_in_candidate",
    "source_image_count_expected",
    "registered_storage_hint",
    "resolved_local_archive_path",
    "local_archive_status",
    "rights_status",
    "risk_note",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def project_id_from_object_dir(path: Path) -> str:
    for part in path.name.split("_"):
        if part.startswith("obs-char-") or part.startswith("obs-unk-"):
            return part
    raise ValueError(f"Cannot find project ID in object directory name: {path}")


def discover_target_dirs(root: Path) -> dict[str, dict[str, Path | str]]:
    target_ids = set(TARGET_PROJECT_IDS)
    object_root = root / "corpus/001_oracle-characters"
    targets: dict[str, dict[str, Path | str]] = {}
    for packet_path in sorted(object_root.glob("*/*/01_*packet.json")):
        object_dir = packet_path.parent
        project_id = project_id_from_object_dir(object_dir)
        if project_id in target_ids:
            targets[project_id] = {
                "object_dir": object_dir,
                "packet": packet_path.name,
            }
    missing_ids = sorted(target_ids - set(targets))
    if missing_ids:
        raise FileNotFoundError(f"Missing target character packet directories: {', '.join(missing_ids)}")
    return {project_id: targets[project_id] for project_id in TARGET_PROJECT_IDS}


def read_image_reference_rows(root: Path) -> dict[str, list[dict[str, str]]]:
    path = root / IMAGE_REFERENCE_RESULTS
    rows_by_candidate: dict[str, list[dict[str, str]]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            rows_by_candidate.setdefault(row["unknown_candidate_id"], []).append(row)
    return rows_by_candidate


def read_existing_visual_rows(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return {
            row["source_image_reference_path"]: row
            for row in csv.DictReader(file)
            if row.get("source_image_reference_path")
        }


def archive_status(row: dict[str, str]) -> str:
    resolved = row.get("resolved_local_archive_path", "")
    if resolved and Path(resolved).exists():
        return "registered_external_archive_available_outside_git"
    if resolved:
        return "registered_external_archive_missing_on_current_disk"
    return "not_applicable_no_archive_path"


def build_visual_rows(
    project_id: str,
    packet: dict,
    image_reference_rows: list[dict[str, str]],
    existing_visual_rows: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    existing_visual_rows = existing_visual_rows or {}
    if image_reference_rows:
        rows = []
        for index, source_row in enumerate(image_reference_rows, start=1):
            existing_row = existing_visual_rows.get(source_row["source_image_path"], {})
            committed_image_path = existing_row.get("committed_image_path", "")
            visual_material_status = (
                "committed_review_image_derivative"
                if committed_image_path
                else "source_image_reference_only_no_committed_glyph_image"
            )
            rows.append(
                {
                    "visual_source_index_id": f"{project_id}-visual-source-{index:03d}",
                    "project_id": project_id,
                    "primary_external_ref_id": source_row["primary_external_ref_id"],
                    "source_id": source_row["source_id"],
                    "source_package_id": source_row["source_package_id"],
                    "download_id": source_row["download_id"],
                    "visual_material_status": visual_material_status,
                    "committed_image_path": committed_image_path,
                    "source_image_reference_path": source_row["source_image_path"],
                    "source_image_sequence_in_candidate": source_row["source_image_sequence_in_candidate"],
                    "source_image_count_expected": source_row["source_image_count_expected"],
                    "registered_storage_hint": source_row["registered_storage_hint"],
                    "resolved_local_archive_path": source_row["resolved_local_archive_path"],
                    "local_archive_status": existing_row.get("local_archive_status") or archive_status(source_row),
                    "rights_status": source_row["source_rights_status"],
                    "risk_note": source_row["risk_note"],
                    "review_status": "needs_human_visual_review",
                    "research_boundary": "co_located_visual_source_index_not_scholarship",
                    "caution": (
                        "Source image path metadata only; not a committed image, not an "
                        "accepted glyph identity, not an accepted reading, and not a "
                        "decipherment conclusion."
                    ),
                    "updated_at": "2026-06-20",
                }
            )
        return rows

    if existing_visual_rows:
        return sorted(existing_visual_rows.values(), key=lambda row: row.get("visual_source_index_id", ""))

    return [
        {
            "visual_source_index_id": f"{project_id}-visual-source-001",
            "project_id": project_id,
            "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
            "source_id": packet.get("source_id", ""),
            "source_package_id": packet.get("source_package_id", ""),
            "download_id": ";".join(packet.get("evidence_download_ids", [])),
            "visual_material_status": "no_source_image_reference_extracted_yet",
            "committed_image_path": "",
            "source_image_reference_path": "",
            "source_image_sequence_in_candidate": "",
            "source_image_count_expected": "",
            "registered_storage_hint": "",
            "resolved_local_archive_path": "",
            "local_archive_status": "not_applicable_no_source_image_reference",
            "rights_status": packet.get("rights_status", ""),
            "risk_note": packet.get("risk_note", ""),
            "review_status": "needs_human_visual_review",
            "research_boundary": "co_located_visual_source_index_not_scholarship",
            "caution": (
                "This object has a local candidate packet but no extracted source-image "
                "reference in the current prepared records; not an accepted reading and "
                "not a decipherment conclusion."
            ),
            "updated_at": "2026-06-20",
        }
    ]


def relative_committed_images(object_dir: Path, committed_images: list[str]) -> str:
    if not committed_images:
        return "none in this directory yet"
    values = []
    for path in committed_images:
        asset_path = Path(path)
        values.append(
            asset_path.relative_to(object_dir).as_posix()
            if asset_path.is_relative_to(object_dir)
            else path
        )
    return "; ".join(values)


def wrap_markdown_text(text: str) -> list[str]:
    return textwrap.wrap(
        text,
        width=MAX_HUMAN_MARKDOWN_LINE_LENGTH,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]


def append_wrapped_paragraph(lines: list[str], text: str) -> None:
    lines.extend(wrap_markdown_text(text))


def append_wrapped_bullet(lines: list[str], label: str, value: object) -> None:
    lines.extend(
        textwrap.wrap(
            f"- {label}: {value}",
            width=MAX_HUMAN_MARKDOWN_LINE_LENGTH,
            subsequent_indent="  ",
            break_long_words=True,
            break_on_hyphens=False,
        )
    )


def build_readme_text(
    project_id: str,
    object_dir: Path,
    packet_name: str,
    packet: dict,
    visual_rows: list[dict[str, str]],
) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    status_counts = sorted({row["visual_material_status"] for row in visual_rows})
    image_ref_count = sum(1 for row in visual_rows if row["source_image_reference_path"])
    committed_images = [row["committed_image_path"] for row in visual_rows if row.get("committed_image_path")]
    packet_record_type = packet.get("record_type", "")
    caution = packet.get("caution", "")
    local_path = object_dir.as_posix()
    status_text = ", ".join(status_counts)
    committed_image_text = relative_committed_images(object_dir, committed_images)
    lines: list[str] = [
        f"# {project_id} Local Object Materials / {project_id} 本地对象资料",
        "",
        "English:",
    ]
    append_wrapped_paragraph(
        lines,
        "This directory is the co-located working folder for this concrete "
        "oracle-character object. Human-readable notes, visual/source "
        "entrances, and AI-readable packet/index files stay together in this "
        "same object directory, not in a parallel human-only directory.",
    )
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "本目录是这个具体甲骨文字对象的同位工作目录。人类可读说明、图像和"
        "来源入口、AI 可读资料包和索引都放在同一具体对象目录中，不另建与 "
        "`corpus` 或对象目录并行的“人类看的目录”。",
    )
    lines.extend(["", "## Local Files / 本地文件", ""])
    append_wrapped_bullet(lines, "Human-readable page / 人类可读页面", "`README.md`")
    append_wrapped_bullet(
        lines,
        "Human-readable visual gallery / 人类可读图像页",
        "`04_visual-gallery.md`",
    )
    append_wrapped_bullet(
        lines,
        "AI-readable candidate packet / AI 可读候选包",
        f"`{packet_name}`",
    )
    append_wrapped_bullet(
        lines,
        "AI-readable visual/source index / AI 可读图像与来源索引",
        "`02_visual-source-index.csv`",
    )
    lines.extend(["", "## Object Summary / 对象摘要", ""])
    append_wrapped_bullet(lines, "Project ID / 项目 ID", f"`{project_id}`")
    append_wrapped_bullet(
        lines,
        "Primary external reference / 首选外部参考",
        f"`{external_id}`",
    )
    append_wrapped_bullet(lines, "Source / 来源", f"`{source_id}`")
    append_wrapped_bullet(
        lines,
        "Packet record type / 资料包类型",
        f"`{packet_record_type}`",
    )
    append_wrapped_bullet(lines, "Directory / 目录", f"`{local_path}`")
    lines.extend(["", "## Visual Material Status / 图像资料状态", ""])
    append_wrapped_bullet(lines, "Status / 状态", f"`{status_text}`")
    append_wrapped_bullet(
        lines,
        "Source image reference rows / 来源图像路径引用行数",
        f"`{image_ref_count}`",
    )
    append_wrapped_bullet(
        lines,
        "Committed glyph image / 已提交字形图像",
        committed_image_text,
    )
    lines.extend(["", "English:"])
    append_wrapped_paragraph(
        lines,
        "If `02_visual-source-index.csv` contains source image paths, those "
        "paths are source-package references only. The raw HUST-OBC package "
        "is registered as a large source and is not committed to normal Git. "
        "If the CSV has no source image path, the next preparation step is to "
        "restore or download the registered source package, extract a "
        "review-safe image derivative, and record rights/provenance before "
        "committing any image asset.",
    )
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "如果 `02_visual-source-index.csv` 中有来源图像路径，它们只是来源包"
        "内部路径引用。HUST-OBC 原始包已经按大型来源登记，不提交到普通 Git。"
        "如果 CSV 中还没有来源图像路径，下一步资料工程应先恢复或下载已登记"
        "来源包，抽取适合复核的图像派生件，并在提交任何图像资产前记录权利、"
        "出处和风险。",
    )
    lines.extend(["", "## Research Boundary / 研究边界", "", "English:"])
    append_wrapped_paragraph(
        lines,
        "This page is a preparation-stage object entrance. It is not an "
        "accepted character record, not an accepted reading, not a component "
        "conclusion, and not a decipherment conclusion.",
    )
    lines.append("This is not a decipherment conclusion.")
    lines.extend(["", "简体中文："])
    append_wrapped_paragraph(
        lines,
        "本页只是准备阶段的对象入口。它不是正式甲骨单字记录，不是已确认释读，"
        "不是构件结论，也不是破译结论。",
    )
    lines.extend(["", "## Review Notes / 复核说明", ""])
    append_wrapped_bullet(
        lines,
        "Review status / 复核状态",
        "`needs_human_visual_review`",
    )
    append_wrapped_bullet(
        lines,
        "Required next step / 下一步",
        "open the packet, visual gallery, and visual/source index in this same "
        "directory, then compare against source registers, source package "
        "manifests, and cross-source evidence.",
    )
    append_wrapped_bullet(lines, "Boundary caution / 边界提示", caution)
    return "\n".join(lines)


def build_gallery_text(project_id: str, packet_name: str, packet: dict, visual_rows: list[dict[str, str]]) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    committed_rows = [row for row in visual_rows if row.get("committed_image_path")]
    sections: list[str] = []
    for row in committed_rows:
        asset_path = Path(row["committed_image_path"])
        asset_name = asset_path.name
        metadata_name = asset_path.with_suffix(".yaml").name
        local_asset_path = f"03_visual-assets/{asset_name}"
        local_metadata_path = f"03_visual-assets/{metadata_name}"
        sections.append(
            f"""## {row["visual_source_index_id"]} / 图像条目

![{project_id} glyph candidate]({local_asset_path})

- Local image / 本地图像: `{local_asset_path}`
- Local metadata / 本地 metadata: `{local_metadata_path}`
- Source image path / 来源图像路径: `{row.get("source_image_reference_path", "")}`
- Source package / 来源包: `{row.get("source_package_id", "")}`
- Download ID / 下载 ID: `{row.get("download_id", "")}`
- Rights status / 权利状态: `{row.get("rights_status", "")}`
- Review status / 复核状态: `{row.get("review_status", "")}`
- Risk note / 风险提示: {row.get("risk_note", "")}
"""
        )
    if not sections:
        sections.append(
            """## No Committed Local Image Yet / 暂无已提交本地图像

English:
This object currently has no committed local glyph image derivative. Use `02_visual-source-index.csv` to inspect source-image references and source-package routing before extracting any review image into this same object directory.

简体中文：
本对象目前还没有已提交的本地字形图像派生件。请先查看 `02_visual-source-index.csv` 中的来源图像引用和来源包路线，再把可复核图像抽取到同一对象目录中。"""
        )
    return f"""# {project_id} Visual Gallery / {project_id} 图像资料页

English:
This human-readable gallery stays inside the same concrete oracle-character object directory as the AI-readable packet and visual/source index. It is a preparation-stage viewing surface for local review images, not a parallel human-only directory.

简体中文：
本图像资料页与 AI 可读资料包、图像和来源索引放在同一具体甲骨文字对象目录内。它只是准备阶段的人类查看入口，不是另建的并行“人类看的目录”。

## Object And Source / 对象与来源

- Project ID / 项目 ID: `{project_id}`
- Primary external reference / 首选外部参考: `{external_id}`
- Source / 来源: `{source_id}`
- AI packet / AI 资料包: `{packet_name}`
- Visual/source index / 图像与来源索引: `02_visual-source-index.csv`
- Committed local review images / 已提交本地复核图像数: `{len(committed_rows)}`

## Research Boundary / 研究边界

English:
Images shown here are source-marked preparation materials for human visual review. Each image is not an accepted glyph identity, not an accepted reading, not a component conclusion, and not a decipherment conclusion.

简体中文：
本页展示的图像只是带来源标记的准备阶段材料，用于人工视觉复核。它们不是已确认字形身份，不是已确认释读，不是构件结论，也不是破译结论。

{chr(10).join(sections)}
"""


def build_gallery_text(project_id: str, packet_name: str, packet: dict, visual_rows: list[dict[str, str]]) -> str:
    external_id = packet.get("primary_external_ref_id", "")
    source_id = packet.get("source_id", "")
    committed_rows = [row for row in visual_rows if row.get("committed_image_path")]
    lines: list[str] = [
        f"# {project_id} Visual Gallery / {project_id} 图像资料页",
        "",
        "English:",
    ]
    append_wrapped_paragraph(
        lines,
        "This human-readable gallery stays inside the same concrete "
        "oracle-character object directory as the AI-readable packet and "
        "visual/source index. It is a preparation-stage viewing surface for "
        "local review images, not a parallel human-only directory.",
    )
    lines.extend(["", "简体中文:"])
    append_wrapped_paragraph(
        lines,
        "本图像资料页与 AI 可读资料包、图像和来源索引放在同一具体甲骨"
        "文字对象目录内。它只是准备阶段的人类查看入口，不是另建的并行"
        "人类目录。",
    )
    lines.extend(["", "## Object And Source / 对象与来源", ""])
    append_wrapped_bullet(lines, "Project ID / 项目 ID", f"`{project_id}`")
    append_wrapped_bullet(
        lines,
        "Primary external reference / 首选外部参考",
        f"`{external_id}`",
    )
    append_wrapped_bullet(lines, "Source / 来源", f"`{source_id}`")
    append_wrapped_bullet(lines, "AI packet / AI 资料包", f"`{packet_name}`")
    append_wrapped_bullet(
        lines,
        "Visual/source index / 图像与来源索引",
        "`02_visual-source-index.csv`",
    )
    append_wrapped_bullet(
        lines,
        "Committed local review images / 已提交本地复核图像数",
        f"`{len(committed_rows)}`",
    )
    lines.extend(["", "## Research Boundary / 研究边界", "", "English:"])
    append_wrapped_paragraph(
        lines,
        "Images shown here are source-marked preparation materials for human "
        "visual review. Each image is not an accepted glyph identity, not an "
        "accepted reading, not a component conclusion, and not a decipherment "
        "conclusion.",
    )
    lines.extend(["", "简体中文:"])
    append_wrapped_paragraph(
        lines,
        "本页展示的图像只是带来源标记的准备阶段材料，用于人工视觉复核。"
        "它们不是已确认字形身份，不是已确认释读，不是构件结论，也不是"
        "破译结论。",
    )

    if committed_rows:
        for row in committed_rows:
            asset_path = Path(row["committed_image_path"])
            asset_name = asset_path.name
            metadata_name = asset_path.with_suffix(".yaml").name
            local_asset_path = f"03_visual-assets/{asset_name}"
            local_metadata_path = f"03_visual-assets/{metadata_name}"
            lines.extend(
                [
                    "",
                    f"## {row['visual_source_index_id']} / 图像条目",
                    "",
                    f"![{project_id} glyph candidate]({local_asset_path})",
                    "",
                ]
            )
            append_wrapped_bullet(lines, "Local image / 本地图像", f"`{local_asset_path}`")
            append_wrapped_bullet(
                lines,
                "Local metadata / 本地 metadata",
                f"`{local_metadata_path}`",
            )
            append_wrapped_bullet(
                lines,
                "Source image path / 来源图像路径",
                f"`{row.get('source_image_reference_path', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Source package / 来源包",
                f"`{row.get('source_package_id', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Download ID / 下载 ID",
                f"`{row.get('download_id', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Rights status / 权利状态",
                f"`{row.get('rights_status', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Review status / 复核状态",
                f"`{row.get('review_status', '')}`",
            )
            append_wrapped_bullet(
                lines,
                "Risk note / 风险提示",
                row.get("risk_note", ""),
            )
    else:
        lines.extend(
            [
                "",
                "## No Committed Local Image Yet / 暂无已提交本地图像",
                "",
                "English:",
            ]
        )
        append_wrapped_paragraph(
            lines,
            "This object currently has no committed local glyph image "
            "derivative. Use `02_visual-source-index.csv` to inspect "
            "source-image references and source-package routing before "
            "extracting any review image into this same object directory.",
        )
        lines.extend(["", "简体中文:"])
        append_wrapped_paragraph(
            lines,
            "本对象目前还没有已提交的本地字形图像派生件。请先查看 "
            "`02_visual-source-index.csv` 中的来源图像引用和来源包路线，"
            "再把可复核图像抽取到同一对象目录中。",
        )
    return "\n".join(lines) + "\n"


def build_outputs(root: Path) -> dict[str, dict]:
    image_rows = read_image_reference_rows(root)
    outputs: dict[str, dict] = {}
    for project_id, target in discover_target_dirs(root).items():
        object_dir = target["object_dir"]
        packet_name = target["packet"]
        packet = read_json(object_dir / packet_name)
        visual_index_path = object_dir / "02_visual-source-index.csv"
        visual_rows = build_visual_rows(
            project_id,
            packet,
            image_rows.get(project_id, []),
            read_existing_visual_rows(visual_index_path),
        )
        outputs[project_id] = {
            "object_dir": object_dir,
            "readme_path": object_dir / "README.md",
            "visual_index_path": visual_index_path,
            "gallery_path": object_dir / "04_visual-gallery.md",
            "readme_text": build_readme_text(project_id, object_dir.relative_to(root), packet_name, packet, visual_rows),
            "gallery_text": build_gallery_text(project_id, packet_name, packet, visual_rows),
            "visual_rows": visual_rows,
        }
    return outputs


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=VISUAL_INDEX_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(outputs: dict[str, dict]) -> None:
    for output in outputs.values():
        output["readme_path"].write_text(output["readme_text"].rstrip() + "\n", encoding="utf-8", newline="\n")
        output["gallery_path"].write_text(output["gallery_text"].rstrip() + "\n", encoding="utf-8", newline="\n")
        write_csv(output["visual_index_path"], output["visual_rows"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    outputs = build_outputs(args.root)
    write_outputs(outputs)
    print(f"Wrote local materials for {len(outputs)} character directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
