#!/usr/bin/env python3
"""Add object-local visual observation notes for OBIMD components.

The existing ten manually reviewed notes are preserved.  For the remaining
objects this script records reproducible image-level facts (dimensions,
contrast mask, and marked-pixel bounds) and keeps stroke shape, component
boundaries, variants, readings, and identity explicitly pending human review.
The generated Markdown is a human opening aid, not a decipherment result.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import textwrap
from pathlib import Path

from PIL import Image


MAX_LINE_LENGTH = 80
COMPONENT_ROOT = Path("corpus/003_graphemic-components")
OBSERVATION_NAME = "18_material-visual-observation.md"
PACKET_NAME = "01_candidate-component-packet.json"
VISUAL_INDEX_NAME = "06_component-visual-index.csv"
PROJECT_ID_RE = re.compile(r"obs-comp-cand-\d{6}")
MANUAL_OBSERVATION_IDS = {
    f"obs-comp-cand-{index:06d}" for index in range(1, 11)
}


def wrap(text: str, width: int = MAX_LINE_LENGTH) -> list[str]:
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def bullet(text: str) -> list[str]:
    lines = textwrap.wrap(
        f"- {text}",
        width=MAX_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )
    return lines or ["-"]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def first_value(packet: dict[str, object], *names: str) -> str:
    for name in names:
        value = packet.get(name)
        if isinstance(value, str) and value:
            return value
    return "pending"


def relative_path(root: Path, value: str, object_dir: Path) -> str:
    if not value:
        return "pending"
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve().relative_to((root / object_dir).resolve()).as_posix()
    except ValueError:
        return value.replace("\\", "/")


def image_path(root: Path, value: str) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    return path if path.is_file() else None


def image_profile(path: Path) -> dict[str, str]:
    """Return conservative, reproducible pixel-level facts for one image."""

    with Image.open(path) as source:
        source.load()
        width, height = source.size
        gray = source.convert("L")
        pixels = gray.load()
        corner_points = [
            (0, 0),
            (max(width - 1, 0), 0),
            (0, max(height - 1, 0)),
            (max(width - 1, 0), max(height - 1, 0)),
        ]
        corner_mean = sum(pixels[x, y] for x, y in corner_points) / len(
            corner_points
        )
        background_polarity = "light" if corner_mean >= 128 else "dark"
        marked: list[tuple[int, int]] = []
        if background_polarity == "light":
            for y in range(height):
                for x in range(width):
                    if pixels[x, y] < 128:
                        marked.append((x, y))
        else:
            for y in range(height):
                for x in range(width):
                    if pixels[x, y] >= 128:
                        marked.append((x, y))
        total = max(width * height, 1)
        if marked:
            x_values = [point[0] for point in marked]
            y_values = [point[1] for point in marked]
            x0, x1 = min(x_values), max(x_values)
            y0, y1 = min(y_values), max(y_values)
            span_width = x1 - x0 + 1
            span_height = y1 - y0 + 1
            if span_width > span_height * 1.2:
                orientation = "wider than tall"
            elif span_height > span_width * 1.2:
                orientation = "taller than wide"
            else:
                orientation = "roughly square"
            bbox = f"({x0},{y0})–({x1},{y1})"
            span = f"{span_width} × {span_height} px"
        else:
            orientation = "no thresholded mark field"
            bbox = "none"
            span = "0 × 0 px"
        return {
            "pixel_width": str(width),
            "pixel_height": str(height),
            "color_mode": source.mode,
            "background_polarity": background_polarity,
            "marked_pixel_fraction": f"{len(marked) / total:.2%}",
            "marked_bbox": bbox,
            "marked_span": span,
            "marked_orientation": orientation,
        }


def observation_text(
    root: Path,
    object_dir: Path,
    packet: dict[str, object],
    visual_rows: list[dict[str, str]],
) -> str:
    project_id = first_value(packet, "candidate_component_id")
    external_id = first_value(packet, "primary_external_ref_id")
    source_id = first_value(packet, "source_id")
    download_id = first_value(
        packet,
        "evidence_download_id",
    )
    if download_id == "pending":
        relation = packet.get("source_relationship")
        if isinstance(relation, dict):
            download_id = first_value(relation, "evidence_download_id")
    image_row = visual_rows[0] if visual_rows else {}
    local_image = relative_path(
        root,
        image_row.get("local_asset_path", ""),
        object_dir,
    )
    source_member = image_row.get("source_zip_member", "pending source member")
    checksum = image_row.get("checksum_sha256", "pending")
    rights = image_row.get("rights_status", "pending rights review")
    review = image_row.get("review_status", "needs_human_visual_review")
    local_path = image_path(root, image_row.get("local_asset_path", ""))
    profile: dict[str, str] | None = None
    profile_error = ""
    if local_path is not None:
        try:
            profile = image_profile(local_path)
        except Exception as exc:  # pragma: no cover - defensive source handling
            profile_error = type(exc).__name__
    lines = [
        f"# Material Visual Observation / {project_id} 实物图像观察",
        "",
        "English:",
        *wrap(
            "This object-local note records a source-linked visual asset or a "
            "specific missing-image route. Pixel facts are reproducible "
            "preprocessing evidence; stroke shape, component boundaries, "
            "variants, readings, and identity remain pending human review."
        ),
        "",
        "简体中文：",
        *wrap(
            "本对象记录一项有来源链接的图像资料，或一条具体的缺图路线。"
            "像素事实是可复现的预处理证据；笔画形态、构件边界、异体、"
            "释读和字形身份仍待人工复核。"
        ),
        "",
        "## Evidence Opened / 已打开证据",
        "",
        *bullet(f"Candidate ID / 候选 ID: `{project_id}`"),
        *bullet(f"External reference / 外部参照: `{external_id}`"),
        *bullet(f"Source / 来源: `{source_id}`"),
        *bullet(f"Download route / 下载路线: `{download_id}`"),
        *bullet(f"Local image / 本地图像: `{local_image}`"),
        *bullet(f"Source zip member / 来源压缩包成员: `{source_member}`"),
        *bullet(f"Checksum / 校验和: `{checksum}`"),
        *bullet(f"Rights status / 权利状态: `{rights}`"),
        *bullet(f"Review status / 复核状态: `{review}`"),
        "",
        "## Direct Visual Record / 直接可见记录",
        "",
    ]
    if profile is not None:
        background_zh = {
            "light": "浅色",
            "dark": "深色",
        }[profile["background_polarity"]]
        orientation_zh = {
            "wider than tall": "宽于高",
            "taller than wide": "高于宽",
            "roughly square": "近方形",
            "no thresholded mark field": "没有阈值痕迹区域",
        }[profile["marked_orientation"]]
        lines.extend(
            bullet(
                "English observation: The opened raster contains a "
                "contrasting mark field. The following profile describes "
                "pixels only and does not segment individual strokes."
            )
        )
        lines.extend(
            bullet(
                f"Image profile: {profile['pixel_width']} × "
                f"{profile['pixel_height']} px, mode {profile['color_mode']}; "
                f"corner background is {profile['background_polarity']}; "
                f"thresholded marked pixels occupy "
                f"{profile['marked_pixel_fraction']}."
            )
        )
        lines.extend(
            bullet(
                f"Marked-pixel bounds: {profile['marked_bbox']}; span "
                f"{profile['marked_span']}; the marked rectangle is "
                f"{profile['marked_orientation']}."
            )
        )
        lines.extend(
            bullet(
                "简体中文观察：已打开栅格图像中存在对比度明显的痕迹区域。"
                "以下 profile 只记录像素，不分割单独笔画。"
            )
        )
        lines.extend(
            bullet(
                f"图像 profile：{profile['pixel_width']} × "
                f"{profile['pixel_height']} 像素，模式 "
                f"{profile['color_mode']}；角点背景为"
                f"{background_zh}；阈值痕迹像素占"
                f"{profile['marked_pixel_fraction']}。"
            )
        )
        lines.extend(
            bullet(
                f"痕迹范围：{profile['marked_bbox']}；跨度"
                f"{profile['marked_span']}；痕迹矩形"
                f"{orientation_zh}。"
            )
        )
        if profile_error:
            lines.extend(
                bullet(
                    f"Image decode warning / 图像解码警告: `{profile_error}`; "
                    "open the local file again before using the profile."
                )
            )
    else:
        lines.extend(
            bullet(
                "English observation: No local PNG/JPEG asset is currently "
                "registered for this candidate; no shape observation is made."
            )
        )
        lines.extend(
            bullet(
                "简体中文观察：当前没有登记的本地 PNG/JPEG 资料；本记录不作"
                "字形观察。"
            )
        )
        lines.extend(
            bullet(
                "The absence is a source-processing gap, not evidence that the "
                "source object has no image."
            )
        )
        lines.extend(
            bullet(
                "缺图是来源预处理缺口，不表示来源对象本身没有图像。"
            )
        )
    lines.extend(
        [
            "",
            "## Next Checks / 下一步核查",
            "",
        ]
    )
    checks = [
        "Open the local asset together with 06_component-visual-index.csv.",
        "Compare the image with independent character and component sources.",
        "Check whether a rubbing, inscription, plate, or second image exists.",
        "Record visible damage, orientation, contrast, and scale limits by hand.",
        "Keep component boundaries, variants, readings, and disputes as pending.",
        "打开本地图像并同时核对 06_component-visual-index.csv。",
        "将图像与独立单字、构件来源进行比较。",
        "核查是否存在拓片、卜辞、图版或第二张图像。",
        "人工记录可见残损、方向、对比度和尺寸限制。",
        "构件边界、异体、释读和争议继续标为待复核。",
    ]
    for item in checks:
        lines.extend(bullet(item))
    lines.extend(
        [
            "",
            "## Boundary / 边界",
            "",
            *wrap(
                "This is a visible-material preprocessing record, not a "
                "confirmed component form or oracle-character identity claim. "
                "It is not a component assignment; it is not a decipherment "
                "conclusion."
            ),
            *wrap(
                "本记录是图像资料预处理档案，不是已确认的构件形体或甲骨单字身份。"
                "本记录不是构件归属，也不是释读结论。"
            ),
            "- Claim boundary: not a component assignment; not a decipherment conclusion.",
            "- 边界标记：不是构件归属；不是释读结论。",
        ]
    )
    text = "\n".join(lines) + "\n"
    for number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH:
            raise ValueError(f"line exceeds {MAX_LINE_LENGTH}: {project_id}:{number}")
    return text


def build(root: Path, overwrite: bool = False) -> dict[str, int]:
    created = 0
    skipped = 0
    with_image = 0
    without_image = 0
    for packet_path in sorted(
        (root / COMPONENT_ROOT).rglob(PACKET_NAME)
    ):
        object_dir = packet_path.parent.relative_to(root)
        match = PROJECT_ID_RE.search(object_dir.name)
        if not match:
            continue
        project_id = match.group(0)
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        visual_rows = read_rows(root / object_dir / VISUAL_INDEX_NAME)
        observation_path = root / object_dir / OBSERVATION_NAME
        if observation_path.exists():
            existing_text = observation_path.read_text(encoding="utf-8")
            # Preserve manually written notes (including the four notes that
            # predate this generator) and explicit no-image gap records.
            if (
                not overwrite
                or project_id in MANUAL_OBSERVATION_IDS
                or (
                    "Image profile:" not in existing_text
                    and "No local PNG/JPEG asset" not in existing_text
                )
            ):
                skipped += 1
                continue
        observation_path.write_text(
            observation_text(root, object_dir, packet, visual_rows),
            encoding="utf-8",
            newline="\n",
        )
        created += 1
        if visual_rows and image_path(root, visual_rows[0].get("local_asset_path", "")):
            with_image += 1
        else:
            without_image += 1
    return {
        "created": created,
        "skipped": skipped,
        "created_with_image": with_image,
        "created_without_image": without_image,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    result = build(args.root.resolve(), overwrite=args.overwrite)
    for key, value in result.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
