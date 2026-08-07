#!/usr/bin/env python3
"""Audit human-readable visual observations for every OBIMD component object.

The audit distinguishes a local image, a reproducible pixel profile, and a
manually described shape.  None of these states is a component assignment or a
decipherment result.
"""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from collections import Counter
from pathlib import Path


COMPONENT_ROOT = Path("corpus/003_graphemic-components")
CSV_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/228_component-visual-observation-coverage.csv"
)
REPORT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/229_component-visual-observation-coverage-audit.md"
)
PACKET_NAME = "01_candidate-component-packet.json"
OBSERVATION_NAME = "18_material-visual-observation.md"
VISUAL_INDEX_NAME = "06_component-visual-index.csv"
MAX_LINE_LENGTH = 80
CSV_FIELDS = [
    "coverage_id",
    "project_id",
    "object_dir",
    "asset_count",
    "local_image_status",
    "observation_path",
    "visual_observation_status",
    "pixel_profile_status",
    "rights_status",
    "review_status",
    "next_human_action",
]


def wrap(text: str) -> list[str]:
    return textwrap.wrap(
        text,
        width=MAX_LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def bullet(label: str, value: str) -> list[str]:
    return textwrap.wrap(
        f"- {label}: {value}",
        width=MAX_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    ) or [f"- {label}: {value}"]


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def observation_status(path: Path) -> tuple[str, str]:
    if not path.exists():
        return "missing_direct_visual_record", "missing"
    text = path.read_text(encoding="utf-8")
    required = (
        "Direct Visual Record",
        "直接可见记录",
        "Boundary",
        "边界",
    )
    if any(marker not in text for marker in required):
        return "observation_file_without_boundary_markers", "missing"
    if "Image profile:" in text and "图像 profile" in text:
        return "pixel_profile_and_boundary_present", "present"
    if "No local PNG/JPEG asset" in text and "没有登记的本地 PNG/JPEG" in text:
        return "missing_image_route_and_boundary_present", "not_applicable"
    return "manual_shape_observation_and_boundary_present", "not_applicable"


def build_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    packet_paths = sorted((root / COMPONENT_ROOT).rglob(PACKET_NAME))
    for packet_path in packet_paths:
        object_dir = packet_path.parent
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        project_id = str(packet.get("candidate_component_id", ""))
        if not project_id.startswith("obs-comp-cand-"):
            continue
        visual_rows = read_rows(object_dir / VISUAL_INDEX_NAME)
        observation_path = object_dir / OBSERVATION_NAME
        visual_status, profile_status = observation_status(observation_path)
        local_image_status = (
            "source_image_extracted" if visual_rows else "not_found_in_registered_source_package"
        )
        if visual_rows and visual_status == "pixel_profile_and_boundary_present":
            action = "open image and add human stroke-level observations"
        elif visual_rows:
            action = "open image and verify the neutral visual record"
        else:
            action = "follow source route and resolve the missing image question"
        image_row = visual_rows[0] if visual_rows else {}
        rows.append(
            {
                "coverage_id": f"component-visual-observation-{len(rows) + 1:05d}",
                "project_id": project_id,
                "object_dir": relative(object_dir, root),
                "asset_count": str(len(visual_rows)),
                "local_image_status": local_image_status,
                "observation_path": (
                    relative(observation_path, root)
                    if observation_path.exists()
                    else ""
                ),
                "visual_observation_status": visual_status,
                "pixel_profile_status": profile_status,
                "rights_status": image_row.get(
                    "rights_status", str(packet.get("rights_status", ""))
                ),
                "review_status": image_row.get(
                    "review_status", str(packet.get("review_status", ""))
                ),
                "next_human_action": action,
            }
        )
    return rows


def build_report(rows: list[dict[str, str]], csv_path: str) -> str:
    status_counts = Counter(row["visual_observation_status"] for row in rows)
    image_count = sum(row["asset_count"] != "0" for row in rows)
    lines = [
        "# Component Visual Observation Coverage / 构件图像观察覆盖审计",
        "",
        *wrap(
            "This report separates a local OBIMD image, a reproducible pixel "
            "profile, and a human-readable observation. It is preprocessing "
            "evidence, not a component assignment or decipherment claim."
        ),
        "",
        "简体中文：",
        *wrap(
            "本报告区分 OBIMD 本地图像、可复现像素 profile 和人类可读观察。"
            "它是预处理证据，不是构件归属或释读结论。"
        ),
        "",
        "## Coverage Result / 覆盖结果",
        "",
        *bullet("Component object directories / 构件对象目录", str(len(rows))),
        *bullet("Objects with local image routes / 有本地图像路线", str(image_count)),
        *bullet(
            "Observation files / 观察文件",
            str(sum(bool(row["observation_path"]) for row in rows)),
        ),
        *bullet(
            "Human shape notes / 人工形态记录",
            str(status_counts["manual_shape_observation_and_boundary_present"]),
        ),
        *bullet(
            "Pixel profile records / 像素 profile 记录",
            str(status_counts["pixel_profile_and_boundary_present"]),
        ),
        *bullet(
            "Missing-image routes / 缺图路线记录",
            str(status_counts["missing_image_route_and_boundary_present"]),
        ),
        "",
        "## Human Reading Order / 人工阅读顺序",
        "",
    ]
    for item in [
        "Open the object README and 18_material-visual-observation.md.",
        "Open the image and 06_component-visual-index.csv together.",
        "Treat pixel bounds as routing facts, not stroke segmentation.",
        "Add human notes for damage, orientation, and visible stroke relations.",
        "Compare independent character, inscription, rubbing, and plate sources.",
        "Keep component boundaries, variants, readings, and disputes pending.",
        "先打开对象 README 和 18_material-visual-observation.md。",
        "同时打开图像和 06_component-visual-index.csv。",
        "像素范围只作路线事实，不作笔画分割。",
        "人工补充残损、方向和可见笔画关系。",
        "比较独立单字、卜辞、拓片和图版来源。",
        "构件边界、异体、释读和争议继续保持待复核。",
    ]:
        lines.extend(wrap(f"- {item}"))
    lines.extend(
        [
            "",
            "## Status Counts / 状态计数",
            "",
        ]
    )
    for status, count in sorted(status_counts.items()):
        lines.extend(bullet(status, str(count)))
    lines.extend(
        [
            "",
            "## Concrete Follow-up / 具体待查",
            "",
            *wrap(
                "The 28 objects without a local image remain source-processing "
                "gaps. Their object-local notes name the package route and ask "
                "whether extraction, rights review, or source availability is "
                "the unresolved issue."
            ),
            *wrap(
                "没有本地图像的 28 个对象仍是来源预处理缺口。对象内记录已经写明"
                "压缩包路线，并要求核查抽取、权利审查或来源可用性究竟是哪一项未完成。"
            ),
            "",
            "Complete row-level audit:",
            "- CSV directory:",
            "  `corpus/009_statistics-and-derived-features/`",
            "- CSV filename:",
            "  `228_component-visual-observation-coverage.csv`",
            "",
            "## Boundary / 边界",
            "",
            *wrap(
                "This audit does not convert image metadata or pixel profiles into "
                "component forms, component assignments, readings, evolution, "
                "or decipherment conclusions."
            ),
            *wrap(
                "本审计不把图像 metadata 或像素 profile 转成构件形体、构件归属、"
                "释读、演化或破译结论。"
            ),
        ]
    )
    text = "\n".join(lines) + "\n"
    if max(map(len, text.splitlines()), default=0) > MAX_LINE_LENGTH:
        raise ValueError("component visual audit report exceeds 80 characters")
    return text


def write_outputs(root: Path, rows: list[dict[str, str]]) -> tuple[Path, Path]:
    csv_path = root / CSV_OUTPUT
    report_path = root / REPORT_OUTPUT
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    report_path.write_text(
        build_report(rows, CSV_OUTPUT.as_posix()),
        encoding="utf-8",
        newline="\n",
    )
    return csv_path, report_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    csv_path, report_path = write_outputs(root, build_rows(root))
    print(f"component_visual_observation_rows={sum(1 for _ in csv_path.open(encoding='utf-8')) - 1}")
    print(f"csv={csv_path}")
    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
