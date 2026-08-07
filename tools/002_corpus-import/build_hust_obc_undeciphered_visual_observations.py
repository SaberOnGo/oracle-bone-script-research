#!/usr/bin/env python3
"""Add conservative visual-profile notes for HUST-OBC candidates.

Existing human visual records are preserved.  Candidates without a human
record receive an object-local note containing reproducible pixel facts and
specific questions for a later human image review.  The profile is not a
stroke segmentation, component assignment, reading, or decipherment claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import textwrap
from pathlib import Path

from PIL import Image


CHARACTER_ROOT = Path("corpus/001_oracle-characters")
OBSERVATION_NAME = "14_material-visual-observation.md"
PACKET_GLOB = "01_*packet.json"
PROJECT_ID_RE = re.compile(r"obs-(?:char|unk)-\d{6}")
MAX_LINE_LENGTH = 80
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def wrap(text: str) -> list[str]:
    return textwrap.wrap(
        text,
        width=MAX_LINE_LENGTH,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def bullet(text: str) -> list[str]:
    return textwrap.wrap(
        f"- {text}",
        width=MAX_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=True,
        break_on_hyphens=False,
    ) or ["-"]


def project_id_for(object_dir: Path, packet: dict[str, object]) -> str:
    for key in ("unknown_candidate_id", "suggested_oracle_character_id"):
        value = packet.get(key)
        if isinstance(value, str) and PROJECT_ID_RE.fullmatch(value):
            return value
    match = PROJECT_ID_RE.search(object_dir.name)
    if not match:
        raise ValueError(f"cannot determine project id: {object_dir}")
    return match.group(0)


def first_value(packet: dict[str, object], *names: str) -> str:
    for name in names:
        value = packet.get(name)
        if isinstance(value, str) and value:
            return value
    return "pending"


def read_visual_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def filesystem_path(path: Path) -> str:
    resolved = path.resolve()
    if resolved.drive:
        return "\\\\?\\" + str(resolved)
    return str(resolved)


def local_images(object_dir: Path) -> list[Path]:
    def is_file(path: Path) -> bool:
        if path.is_file():
            return True
        resolved = path.resolve()
        if resolved.drive:
            return Path("\\\\?\\" + str(resolved)).is_file()
        return False

    paths: list[Path] = []
    for dirname in ("03_visual-assets", "07_visual-assets"):
        asset_dir = object_dir / dirname
        if not asset_dir.exists():
            continue
        paths.extend(
            path
            for path in asset_dir.rglob("*")
            if is_file(path) and path.suffix.lower() in IMAGE_SUFFIXES
        )
    return sorted(paths)


def relative_path(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def image_profile(path: Path) -> dict[str, str]:
    """Return reproducible image-level facts without segmenting strokes."""

    with Image.open(filesystem_path(path)) as source:
        source.load()
        width, height = source.size
        gray = source.convert("L")
        pixels = gray.load()
        corners = [
            (0, 0),
            (max(width - 1, 0), 0),
            (0, max(height - 1, 0)),
            (max(width - 1, 0), max(height - 1, 0)),
        ]
        corner_mean = sum(pixels[x, y] for x, y in corners) / len(corners)
        background = "light" if corner_mean >= 128 else "dark"
        marked: list[tuple[int, int]] = []
        for y in range(height):
            for x in range(width):
                value = pixels[x, y]
                if (background == "light" and value < 128) or (
                    background == "dark" and value >= 128
                ):
                    marked.append((x, y))
        total = max(width * height, 1)
        if marked:
            xs = [point[0] for point in marked]
            ys = [point[1] for point in marked]
            x0, x1 = min(xs), max(xs)
            y0, y1 = min(ys), max(ys)
            span_width = x1 - x0 + 1
            span_height = y1 - y0 + 1
            bbox = f"({x0},{y0})–({x1},{y1})"
            span = f"{span_width} × {span_height} px"
            if span_width > span_height * 1.2:
                orientation = "wider than tall"
            elif span_height > span_width * 1.2:
                orientation = "taller than wide"
            else:
                orientation = "roughly square"
        else:
            bbox = "none"
            span = "0 × 0 px"
            orientation = "no thresholded mark field"
        mean_luma = sum(pixels[x, y] for y in range(height) for x in range(width)) / total
        return {
            "pixel_width": str(width),
            "pixel_height": str(height),
            "color_mode": source.mode,
            "background": background,
            "marked_fraction": f"{len(marked) / total:.2%}",
            "marked_bbox": bbox,
            "marked_span": span,
            "orientation": orientation,
            "mean_luma": f"{mean_luma:.2f}",
        }


def ensure_readme_link(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if OBSERVATION_NAME in text:
        return False
    marker = "- Human-readable context dossier / 人类可读语境档案:"
    insertion = [
        "- Human-readable material observation / 人工图像观察:",
        f"  `{OBSERVATION_NAME}`",
    ]
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(marker):
            lines[index:index] = insertion
            path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
            return True
    lines.extend(["", "## Visual Observation / 图像观察", "", *insertion])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return True


def ensure_index_link(path: Path, key: str) -> bool:
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get(key)
    if not isinstance(files, list) or OBSERVATION_NAME in files:
        return False
    insert_at = len(files)
    for index, value in enumerate(files):
        if value == "08_character-context-evidence-dossier.md":
            insert_at = index + 1
            break
    files.insert(insert_at, OBSERVATION_NAME)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return True


def observation_text(
    root: Path,
    object_dir: Path,
    packet: dict[str, object],
    visual_rows: list[dict[str, str]],
    image: Path | None,
) -> str:
    project_id = project_id_for(object_dir, packet)
    external_id = first_value(packet, "primary_external_ref_id")
    source_id = first_value(packet, "source_id")
    download_id = first_value(packet, "evidence_download_id", "download_id")
    row = visual_rows[0] if visual_rows else {}
    source_route = row.get("source_image_reference_path", "pending source image route")
    asset_id = row.get("asset_id", "pending asset id")
    rights = row.get("rights_status", first_value(packet, "rights_status"))
    review = row.get("review_status", "needs_human_visual_review")
    lines = [
        f"# Material Visual Observation / {project_id} 材料图像观察",
        "",
        "English:",
        *wrap(
            "This object-local record adds a reproducible pixel profile for a "
            "source-linked image. It is a preparation-stage routing aid; a "
            "human researcher still needs to inspect the image and record "
            "neutral visible marks."
        ),
        "",
        "简体中文：",
        *wrap(
            "本对象记录为有来源路线的图像补充可复现像素 profile。它只是预处理阶段的路线辅助，"
            "仍需由人类研究者打开图像，记录中性的可见痕迹。"
        ),
        "",
        "## Evidence Opened / 已打开证据",
        "",
        *bullet(f"Project ID / 项目 ID: `{project_id}`"),
        *bullet(f"External reference / 外部参考: `{external_id}`"),
        *bullet(f"Source / 来源: `{source_id}`"),
        *bullet(f"Download route / 下载路线: `{download_id}`"),
        *bullet(f"Source image route / 来源图像路线: `{source_route}`"),
        *bullet(f"Asset ID / 资产 ID: `{asset_id}`"),
        *bullet(
            "Local image / 本地图像: "
            + (f"`{relative_path(root, image)}`" if image else "not found")
        ),
        *bullet(f"Rights status / 权利状态: `{rights}`"),
        *bullet(f"Review status / 复核状态: `{review}`"),
        "",
    ]
    if image is None:
        lines.extend(
            [
                "## Missing Image Route / 缺图路线",
                "",
                *bullet(
                    "No local image was found. This is a source-processing gap, "
                    "not evidence that the source object has no image."
                ),
                *bullet(
                    "当前没有找到本地图像。这是来源预处理缺口，不表示来源对象本身没有图像。"
                ),
            ]
        )
    else:
        profile = image_profile(image)
        orientation_zh = {
            "wider than tall": "宽于高",
            "taller than wide": "高于宽",
            "roughly square": "近方形",
            "no thresholded mark field": "没有阈值痕迹区域",
        }[profile["orientation"]]
        background_zh = {"light": "浅色", "dark": "深色"}[profile["background"]]
        lines.extend(
            [
                "## Pixel Profile / 像素 profile",
                "",
                *bullet(
                    "The profile records pixels only; it does not segment "
                    "individual strokes or establish a glyph shape."
                ),
                *bullet(
                    f"Image profile: {profile['pixel_width']} × "
                    f"{profile['pixel_height']} px, mode {profile['color_mode']}; "
                    f"corner background is {profile['background']}; "
                    f"thresholded marked pixels occupy {profile['marked_fraction']}; "
                    f"mean luma {profile['mean_luma']}."
                ),
                *bullet(
                    f"Marked-pixel bounds: {profile['marked_bbox']}; span "
                    f"{profile['marked_span']}; marked rectangle is "
                    f"{profile['orientation']}."
                ),
                *bullet(
                    f"像素 profile 只记录像素，不分割单独笔画，也不确认字形。图像为 "
                    f"{profile['pixel_width']} × {profile['pixel_height']} 像素，"
                    f"角点背景为{background_zh}，阈值痕迹像素占 {profile['marked_fraction']}，"
                    f"平均灰度 {profile['mean_luma']}。"
                ),
                *bullet(
                    f"痕迹范围为 {profile['marked_bbox']}，跨度 {profile['marked_span']}，"
                    f"标记矩形{orientation_zh}。"
                ),
            ]
        )
    lines.extend(
        [
            "",
            "## Human Review Boundary / 人工复核边界",
            "",
            *bullet(
                "This algorithmic profile is not a human visual observation. "
                "Open the image before recording stroke shape, damage, or "
                "orientation."
            ),
            *bullet(
                "本算法 profile 不是人工图像观察。记录笔画形态、残损或方向前，必须打开图像人工复核。"
            ),
            *bullet(
                "Identity, variant, near form, component, inscription, reading, "
                "period, and evolution remain pending source review."
            ),
            *bullet(
                "身份、异体、近形、构件、卜辞、释读、时期和演变关系仍待来源复核。"
            ),
            "",
            "## Next Checks / 下一步核查",
            "",
            *bullet("Open the local image and 02_visual-source-index.csv together."),
            *bullet("Record visible shape, damage, orientation, contrast, and limits by hand."),
            *bullet("Check for a rubbing, inscription text, plate, catalog number, or second view."),
            *bullet("Compare variants and near forms only after the source route is cited."),
            *bullet("打开图像和 02_visual-source-index.csv，记录可见形态、残损、方向、对比度和边界。"),
            *bullet("核查拓片、卜辞全文、图版、著录号以及是否存在第二视角。"),
            *bullet("来源路线有引文后，再比较异体、近形和后世字形路线。"),
            "",
            "## Boundary / 边界",
            "",
            *wrap(
                "This note is a preprocessing record. It is not a reading, "
                "component assignment, inscription identity, evolution claim, "
                "or decipherment conclusion."
            ),
            *wrap(
                "本记录是预处理档案，不是释读、构件归属、卜辞身份、演变结论或释读结论。"
            ),
        ]
    )
    text = "\n".join(lines) + "\n"
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH:
            raise ValueError(f"line exceeds {MAX_LINE_LENGTH}: {project_id}:{line_number}")
    return text


def build(root: Path, overwrite: bool = False) -> dict[str, int]:
    root = root.resolve()
    created = 0
    skipped = 0
    profiles = 0
    missing_images = 0
    readme_links = 0
    index_links = 0
    for packet_path in sorted((root / CHARACTER_ROOT).rglob(PACKET_GLOB)):
        object_dir = packet_path.parent
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        project_id = project_id_for(object_dir, packet)
        if not project_id.startswith("obs-unk-"):
            continue
        observation_path = object_dir / OBSERVATION_NAME
        existing = observation_path.read_text(encoding="utf-8") if observation_path.exists() else ""
        preserve = bool(existing) and not overwrite
        if not existing or overwrite and "Direct Visual Record" not in existing:
            image = local_images(object_dir)[0] if local_images(object_dir) else None
            if not preserve:
                visual_rows = read_visual_rows(object_dir / "02_visual-source-index.csv")
                observation_path.write_text(
                    observation_text(root, object_dir, packet, visual_rows, image),
                    encoding="utf-8",
                    newline="\n",
                )
                created += 1
                if image is None:
                    missing_images += 1
                else:
                    profiles += 1
            else:
                skipped += 1
        else:
            skipped += 1
        if ensure_readme_link(object_dir / "README.md"):
            readme_links += 1
        for path, key in [
            (object_dir / "07_research-dossier-index.json", "human_files"),
            (object_dir / "09_character-context-evidence-index.json", "human_readable_files"),
            (object_dir / "13_human-research-readiness-index.json", "human_readable_files"),
        ]:
            if ensure_index_link(path, key):
                index_links += 1
    return {
        "created": created,
        "skipped": skipped,
        "created_with_pixel_profile": profiles,
        "created_without_image": missing_images,
        "readme_links_added": readme_links,
        "index_links_added": index_links,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    result = build(args.root, overwrite=args.overwrite)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
