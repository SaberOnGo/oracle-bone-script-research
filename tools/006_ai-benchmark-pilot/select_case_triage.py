"""Select bounded AI research cases for human-first review.

This is a deterministic pre-agent triage aid.  It ranks work routes by the
evidence that is already visible in object dossiers; it never estimates a
decipherment probability or creates a benchmark result.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path
from typing import Any


CASE_ROOT = Path(
    "corpus/002_oracle-bone-inscriptions/008_source-record-candidates"
)
HUMAN_FILES = (
    "README.md",
    "02_human-inscription-dossier.md",
    "05_human-research-dossier.md",
)
PLAN_FILES = (
    "06_missing-evidence-plan.md",
    "07_missing-evidence-plan.md",
)
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
PUBLIC_RIGHTS = "public_domain_verified"


def _source_label(source_id: str) -> str:
    labels = {
        "src-british-library-oracle-bone": "BL",
        "src-ihp-museum-oracle-bones": "IHP",
        "src-obimd": "OBIMD",
        "src-wikimedia-ningxia-museum-hyz421": "Ningxia",
        "src-metmuseum-oracle-bone": "Met",
    }
    return labels.get(source_id, source_id or "unknown")


class TriageError(ValueError):
    """Raised when triage input or output boundaries are invalid."""


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _record_path(directory: Path) -> Path:
    path = directory / "90_source-record.json"
    if not path.is_file():
        raise TriageError(f"missing source record: {directory}")
    return path


def _has_source_checksum(record: dict[str, Any]) -> bool:
    for key in ("source_record_sha256", "checksum_sha256"):
        if record.get(key):
            return True
    package = record.get("source_package")
    if isinstance(package, dict) and package.get("sha256"):
        return True
    for route in record.get("image_routes", []):
        if isinstance(route, dict) and route.get("sha256"):
            return True
    return False


def _source_layer(record: dict[str, Any]) -> str:
    availability = str(record.get("text_availability", ""))
    if record.get("source_reported_recto_string") or record.get(
        "source_reported_verso_string"
    ):
        return "source_display_text"
    if "uid_sequence" in availability or "sentence" in availability:
        return "structured_sequence"
    if "description_only" in availability:
        return "source_description_only"
    if availability:
        return "source_layer_recorded"
    return "no_text_layer_recorded"


def inspect_candidate(root: Path, directory: Path) -> dict[str, Any]:
    """Return a review-only triage row for one object directory."""

    root = root.resolve()
    directory = directory.resolve()
    relative = _relative(directory, root)
    record = json.loads(_record_path(directory).read_text(encoding="utf-8"))
    record_type = record.get("record_type")
    if record_type and record_type != "inscription_source_record_candidate":
        raise TriageError(f"unsupported record type: {relative}")

    human_paths = [
        _relative(directory / name, root)
        for name in HUMAN_FILES
        if (directory / name).is_file()
    ]
    if not human_paths:
        raise TriageError(f"no human dossier in: {relative}")

    image_paths = [
        _relative(path, root)
        for path in sorted((directory / "03_visual-assets").glob("*"))
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    source_id = str(record.get("source_id", ""))
    if not source_id:
        if "ihp-item" in directory.name:
            source_id = "src-ihp-museum-oracle-bones"
        elif "bl-or" in directory.name:
            source_id = "src-british-library-oracle-bone"
        elif "obimd" in directory.name:
            source_id = "src-obimd"
    rights_status = str(record.get("rights_status", "not_recorded"))
    source_layer = _source_layer(record)
    has_plan = any((directory / name).is_file() for name in PLAN_FILES)
    has_checksum = _has_source_checksum(record)
    blockers: list[str] = []

    if rights_status != PUBLIC_RIGHTS:
        blockers.append(
            "Resolve effective rights before public image or derivative use."
        )
    if not image_paths:
        blockers.append(
            "Locate a permitted image or keep the case as a route-only record."
        )
    if source_layer in {"source_description_only", "structured_sequence"}:
        blockers.append(
            "Obtain a line-addressable text or OCR layer from an independent source."
        )
    if not record.get("plate_page_locator"):
        blockers.append(
            "Locate an independent plate and page reference before text linkage."
        )
    blockers.append(
        "Keep formal identity, character links, and readings unassigned until review."
    )

    signals = ["human_dossier"]
    if image_paths:
        signals.append("committed_source_image")
    if has_checksum:
        signals.append("source_checksum")
    signals.append(source_layer)
    if has_plan:
        signals.append("concrete_next_checks")

    visible_summary = []
    if image_paths:
        visible_summary.append("image")
    if has_checksum:
        visible_summary.append("hash")
    if source_layer not in {"no_text_layer_recorded", "source_layer_recorded"}:
        visible_summary.append("text")
    if not visible_summary:
        visible_summary.append("route")

    if image_paths and rights_status == PUBLIC_RIGHTS:
        lane = "open_for_deep_review"
    elif rights_status != PUBLIC_RIGHTS:
        lane = "rights_blocked_route_review"
    else:
        lane = "source_route_review"

    return {
        "candidate_id": record.get("candidate_id", ""),
        "source_id": source_id,
        "source_label": _source_label(source_id),
        "source_identifier": next(
            (
                str(record.get(key))
                for key in (
                    "source_identifier",
                    "accession_ref",
                    "accession_recto",
                    "museum_item",
                )
                if record.get(key)
            ),
            "unidentified-source-row",
        ),
        "directory": relative,
        "human_entry": human_paths[0],
        "rights_status": rights_status,
        "source_layer": source_layer,
        "image_paths": image_paths,
        "signals": signals,
        "visible_summary": "+".join(visible_summary),
        "blockers": blockers,
        "lane": lane,
        "triage_basis": (
            "work-order signal from visible evidence; not a probability, "
            "scholarly confidence, or decipherment judgment"
        ),
    }


def select_candidates(root: Path, limit: int | None = None) -> list[dict[str, Any]]:
    """Inspect all inscription source-record candidates in stable work order."""

    root = root.resolve()
    case_root = root / CASE_ROOT
    if not case_root.is_dir():
        raise TriageError(f"missing case root: {case_root}")
    rows = [
        inspect_candidate(root, directory)
        for directory in sorted(case_root.iterdir())
        if directory.is_dir() and (directory / "90_source-record.json").is_file()
    ]
    rows.sort(
        key=lambda row: (
            row["lane"] != "open_for_deep_review",
            row["rights_status"] != PUBLIC_RIGHTS,
            not bool(row["image_paths"]),
            row["source_layer"] == "source_description_only",
            len(row["blockers"]),
            row["candidate_id"],
        )
    )
    for rank, row in enumerate(rows, start=1):
        row["work_order_rank"] = rank
    return rows if limit is None else rows[:limit]


def render_markdown(rows: list[dict[str, Any]]) -> str:
    """Render the human-first triage report."""

    lane_labels = {
        "open_for_deep_review": "open_deep_review",
        "rights_blocked_route_review": "rights_blocked",
        "source_route_review": "route_only",
    }
    lines = [
        "# AI Case Selection Triage / AI 案件选案分诊",
        "",
        "Status / 状态: `triage_only`",
        "",
        "This report is a deterministic work-order aid for opening human",
        "dossiers. A rank is not a probability, confidence, candidate claim,",
        "or decipherment result. It does not open a v2 benchmark channel.",
        "",
        "本报告是打开人类档案前的确定性工作顺序辅助。排名不是概率、",
        "置信度、候选结论或破译结果，也不会打开 v2 基准通道。",
        "",
        "## Selection rule / 选案规则",
        "",
        "The order favors visible human evidence, a permitted committed image,",
        "a bound checksum, and concrete counter-check questions. Rights, plate",
        "locators, OCR, and identity gaps remain explicit blockers.",
        "",
        "排序优先考虑可见人类证据、获准的已提交图像、绑定校验和以及",
        "具体反查问题。权利、图版定位、OCR 和身份缺口仍明确阻断。",
        "",
        "## Work order / 工作顺序",
        "",
        "Each rank is a compact review card; long fields continue on new lines.",
        "每个排名是紧凑复核卡；较长字段会换到下一行。",
        "",
    ]
    for row in rows:
        lines.append(
            f"- Rank / 排名 {row['work_order_rank']}: "
            f"`{row['candidate_id']}`"
        )
        lines.append(
            f"  Source / 来源: `{row['source_label']}`; "
            f"lane / 通道: `{lane_labels.get(row['lane'], row['lane'])}`"
        )
        lines.append(
            f"  Visible / 可见: `{row['visible_summary']}`"
        )
    lines.extend(["", "## Human review cards / 人类复核卡", ""])
    for row in rows:
        card_lines = [
            f"### {row['work_order_rank']}. {row['candidate_id']}",
            "",
            "- Human entry / 人类入口: open `README.md`, then the primary",
            "  human dossier in the object folder.",
            f"- Candidate key / 候选键: `{row['candidate_id']}`",
            "- Folder resolution / 目录定位: use the central source-record",
            "  map with this candidate key.",
            f"- Source / 来源: `{row['source_label']}`; "
            f"`{row['source_identifier']}`",
            f"- Rights / 权利: `{row['rights_status']}`",
            f"- Source layer / 来源层: `{row['source_layer']}`",
        ]
        signal_text = ", ".join(row["signals"])
        signal_lines = textwrap.wrap(signal_text, width=65)
        card_lines.append(f"- Signals / 证据信号: {signal_lines[0]}")
        card_lines.extend(f"  {part}" for part in signal_lines[1:])
        card_lines.append("- Concrete blockers / 具体阻断:")
        for blocker in row["blockers"]:
            wrapped = textwrap.wrap(blocker, width=76)
            card_lines.append(f"  - {wrapped[0]}")
            card_lines.extend(f"    {part}" for part in wrapped[1:])
        card_lines.append("")
        lines.extend(card_lines)
    lines.extend(
        [
            "## Boundary / 边界",
            "",
            "Only the object-local human dossier and its cited source routes may",
            "be used for the next review. This report contains no model output,",
            "no calibrated probability, and no scholarly or decipherment claim.",
            "",
            "下一步只能打开对象内人类档案及其引用的来源路线。本报告不含模型",
            "输出、校准概率或任何学术、释读和破译结论。",
            "",
        ]
    )
    return "\n".join(lines)


def _safe_output(root: Path, output: Path) -> None:
    try:
        relative = output.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise TriageError("triage output must stay inside the repository") from exc
    if ".working" in relative.parts:
        return
    if relative.parts[:4] == ("doc", "public", "user_research", "generated"):
        return
    raise TriageError(
        "triage output must stay under .working or generated user research"
    )


def _exclusive_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        rows = select_candidates(root, args.limit)
        _safe_output(root, args.output)
        _exclusive_write(args.output.resolve(), render_markdown(rows))
        if args.json_output:
            _safe_output(root, args.json_output)
            _exclusive_write(
                args.json_output.resolve(),
                json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            )
        print(f"PASS triage-only case selection ({len(rows)} rows)")
        return 0
    except (OSError, TriageError, json.JSONDecodeError) as exc:
        print(f"FAIL triage-only case selection: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
