"""Build a human-readable audit of character image observations.

The presence of a local image is not evidence that a person has inspected it.
This audit keeps those states separate and routes missing observations back to
the concrete object-local dossier.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


PROJECT_RE = re.compile(r"obs-(?:char|unk)-\d{6}")
CSV_FIELDS = [
    "coverage_id",
    "project_id",
    "project_id_type",
    "object_dir",
    "asset_count",
    "observation_path",
    "visual_observation_status",
    "review_status",
    "rights_status",
    "next_human_action",
]


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def project_id_for(object_dir: Path, packet: dict) -> str:
    match = PROJECT_RE.search(object_dir.name)
    if match:
        return match.group(0)
    raise ValueError(f"cannot determine project id: {object_dir}")


def image_paths(object_dir: Path) -> list[Path]:
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
            if is_file(path) and path.suffix.lower() in
            {".png", ".jpg", ".jpeg", ".webp", ".gif"}
        )
    return sorted(paths)


def visual_index_facts(object_dir: Path) -> tuple[str, str]:
    path = object_dir / "02_visual-source-index.csv"
    if not path.exists():
        return "", ""
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        return "", ""
    return rows[0].get("review_status", ""), rows[0].get("rights_status", "")


def observation_status(object_dir: Path, root: Path) -> tuple[str, str]:
    path = object_dir / "14_material-visual-observation.md"
    if not path.exists():
        return "missing_direct_visual_record", ""
    text = path.read_text(encoding="utf-8")
    relative_path = relative(path, root)
    if "Direct Visual Record" in text and "直接可见记录" in text:
        return "direct_visual_record_present", relative_path
    if "Pixel Profile" in text and "像素 profile" in text:
        return "pixel_profile_and_boundary_present", relative_path
    if "Missing Image Route" in text and "缺图路线" in text:
        return "missing_image_route_and_boundary_present", relative_path
    return "observation_file_without_direct_record", relative_path


def build_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for packet_path in sorted((root / "corpus/001_oracle-characters").rglob("01_*packet.json")):
        object_dir = packet_path.parent
        try:
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            project_id = project_id_for(object_dir, packet)
        except (json.JSONDecodeError, ValueError):
            continue
        if not project_id.startswith(("obs-char-", "obs-unk-")):
            continue
        status, observation_path = observation_status(object_dir, root)
        review_status, rights_status = visual_index_facts(object_dir)
        asset_count = len(image_paths(object_dir))
        if status == "direct_visual_record_present":
            action = "check source cross-links and inscription context"
        elif status == "pixel_profile_and_boundary_present":
            action = "open the local image and record neutral visible marks"
        elif status == "missing_image_route_and_boundary_present":
            action = "follow the source image route before visual observation"
        elif asset_count:
            action = "open the local image and record neutral visible marks"
        else:
            action = "follow the source image route before visual observation"
        rows.append(
            {
                "coverage_id": f"character-visual-observation-{len(rows) + 1:05d}",
                "project_id": project_id,
                "project_id_type": "oracle_character" if project_id.startswith("obs-char-") else "undeciphered_candidate",
                "object_dir": relative(object_dir, root),
                "asset_count": str(asset_count),
                "observation_path": observation_path,
                "visual_observation_status": status,
                "review_status": review_status,
                "rights_status": rights_status,
                "next_human_action": action,
            }
        )
    return rows


def wrap_bullet(label: str, value: str, width: int = 80) -> list[str]:
    prefix = f"- {label}: "
    lines: list[str] = []
    current = prefix
    for char in value:
        if len(current) >= width:
            lines.append(current.rstrip())
            current = "  "
        current += char
    lines.append(current.rstrip())
    return lines


def wrap_plain_bullet(value: str, width: int = 80) -> list[str]:
    lines: list[str] = []
    current = "-"
    for char in value:
        if len(current) >= width:
            lines.append(current.rstrip())
            current = "  "
        if current == "-":
            current += " "
        current += char
    lines.append(current.rstrip())
    return lines


def build_report(rows: list[dict[str, str]], csv_path: str) -> str:
    total = len(rows)
    by_type = Counter(row["project_id_type"] for row in rows)
    by_status = Counter(row["visual_observation_status"] for row in rows)
    with_assets = sum(row["asset_count"] != "0" for row in rows)
    direct = by_status["direct_visual_record_present"]
    profiles = by_status["pixel_profile_and_boundary_present"]
    lines = [
        "# Character Visual Observation Coverage / 单字图像观察覆盖审计",
        "",
        "This report separates a local image from a human visual observation.",
        "It is a preprocessing audit, not a character identity or reading claim.",
        "本报告区分本地图像和人工图像观察，属于预处理审计，不确认字形身份或释读。",
        "",
        "## Human Reading Result / 人类阅读结果",
        "",
    ]
    lines += wrap_bullet("Character object directories / 单字对象目录", str(total))
    lines += wrap_bullet("Objects with local images / 有本地图像", str(with_assets))
    lines += wrap_bullet("Direct visual records / 有直接观察记录", str(direct))
    lines += wrap_bullet("Pixel profile records / 像素 profile 记录", str(profiles))
    lines += wrap_bullet(
        "Images without direct records / 有图无人工观察",
        str(with_assets - direct),
    )
    lines += wrap_bullet("Objects without local images / 无本地图像", str(total - with_assets))
    lines += wrap_bullet("Status / 状态", "needs_human_visual_observation_review")
    lines += ["", "## Counts By Object Type / 按对象类型计数", ""]
    for kind in ("oracle_character", "undeciphered_candidate"):
        subset = [row for row in rows if row["project_id_type"] == kind]
        direct_count = sum(row["visual_observation_status"] == "direct_visual_record_present" for row in subset)
        profile_count = sum(row["visual_observation_status"] == "pixel_profile_and_boundary_present" for row in subset)
        image_count = sum(row["asset_count"] != "0" for row in subset)
        lines += wrap_bullet(
            kind,
            f"{len(subset)} objects; {image_count} with images; "
            f"{direct_count} direct records; {profile_count} pixel profiles",
        )
    lines += ["", "## What The Gap Means / 缺口含义", ""]
    lines += wrap_bullet(
        "English",
        "A local derivative proves only that an image was extracted. "
        "A pixel profile is still not a human visual observation; the "
        "object-local note routes the next image review.",
    )
    lines += wrap_bullet(
        "中文",
        "本地派生件只能证明图像已经抽取。像素 profile 不是人工观察，"
        "对象内档案只负责引导下一次图像复核。",
    )
    lines += ["", "## Human Opening Order / 人工开包顺序", ""]
    for item in [
        "Open the concrete object README and 04_visual-gallery.md.",
        "Open the image and 02_visual-source-index.csv together.",
        "Treat a pixel profile as routing evidence, not a human observation.",
        "Record only visible shape, damage, orientation, contrast, and limits.",
        "Keep identity, component, reading, and inscription links pending.",
        "Record the reviewer, date, image path, source route, rights, and risk.",
        "先打开具体对象 README 和 04_visual-gallery.md。",
        "同时打开图像和 02_visual-source-index.csv。",
        "像素 profile 只作路线证据，不等于人工图像观察。",
        "只记录形态、残损、方向、对比度和观察边界。",
        "字形身份、构件、释读和卜辞关联继续保持待复核。",
        "记录复核人、日期、图像路径、来源路线、权利和风险。",
    ]:
        lines += wrap_plain_bullet(item)
    lines += ["", "## Representative Missing Routes / 代表性缺口路线", ""]
    missing_rows = [row for row in rows if row["visual_observation_status"] != "direct_visual_record_present"]
    for row in missing_rows[:12]:
        lines += wrap_bullet(row["project_id"], row["object_dir"])
    lines += [
        "",
        "The complete object list is in:",
        "",
        "## Boundary / 边界",
        "",
        "This audit does not convert image metadata into human observations, identity,",
        "component assignments, readings, evolution, or decipherment.",
        "本审计不把图像 metadata 转成观察、身份、构件、释读、演化或破译结论。",
        "",
    ]
    insertion = lines.index("The complete object list is in:") + 1
    lines[insertion:insertion] = wrap_plain_bullet(f"`{csv_path}`")
    return "\n".join(lines)


def write_outputs(root: Path, rows: list[dict[str, str]]) -> tuple[Path, Path]:
    out_dir = root / "corpus/009_statistics-and-derived-features"
    csv_path = out_dir / "227_character-visual-observation-coverage.csv"
    report_path = out_dir / "226_character-visual-observation-coverage-audit.md"
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    report_path.write_text(
        build_report(rows, csv_path.relative_to(root).as_posix()),
        encoding="utf-8",
        newline="\n",
    )
    return report_path, csv_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    report_path, csv_path = write_outputs(root, build_rows(root))
    print(f"rows={sum(1 for _ in csv_path.open(encoding='utf-8')) - 1}")
    print(f"report={report_path}")
    print(f"csv={csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
