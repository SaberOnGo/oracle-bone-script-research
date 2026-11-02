"""Validate repository policy and content gates for Oracle Bone Script Research.

Rebuilt on 2026-11-02 for the architecture reset in
doc/project/007_architecture-reset-and-human-first-knowledge-base/.
The former 37,000-line structure checker is preserved in Git history at
commit f8638e9ea77.
"""

from __future__ import annotations

import sys

import csv

import hashlib

import json

import os

import re

import subprocess

from collections import Counter

from functools import lru_cache

from pathlib import Path

SIZE_LIMIT_BYTES = 30 * 1024 * 1024

HARD_FILE_LIMIT_BYTES = 40 * 1024 * 1024

IGNORED_LOCAL_ARCHIVE_PREFIXES = (
    "external_local_archive/",
    "external_sources_local/",
    "large_sources_local/",
    "local_private_data/",
    "private_data/",
)

SIZE_LIMIT_EXCEPTIONS = "project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv"

ASSET_SOURCE_INDEX = "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"

ASSET_RIGHTS_REVIEW_LOG = "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv"

ASSET_IMAGE_TECHNICAL_PROFILE = "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"

ASSET_IMAGE_VISUAL_PROFILE = "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"

OBIMD_RIGHTS_CONFLICT_REVIEW = (
    "project_registry/004_asset-source-and-rights-index/006_obimd-rights-conflict-review.md"
)

OBIMD_RIGHTS_STATUS_OVERRIDE = (
    "project_registry/004_asset-source-and-rights-index/006_obimd-rights-status-override.csv"
)

ASSET_ID_SOURCE_MAP = "project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv"

SOURCE_INDEX = "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"

LARGE_SOURCE_REGISTER = "project_registry/006_large-source-register/001_large-source-register.csv"

def git_command(root: Path, *args: str) -> list[str]:
    return ["git", "-c", f"safe.directory={root.as_posix()}", *args]

SOURCE_PACKAGE_FILE_MANIFEST = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "009_source-package-file-manifest.csv"
)

AI_AGENT_BENCHMARK_EXPERIMENT_SCHEMA = (
    "schemas/007_ai-agent-benchmark-experiment-schema/"
    "ai-agent-benchmark-experiment-v2.schema.json"
)

OBIMD_SUBCHARACTER_MAIN_STAGING = (
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)

REQUIRED_ROOT_GITIGNORE_PATTERNS = [
    "tmp/*",
    "**/_tmp/",
    "**/tmp/",
    "**/temp/",
    "**/scratch/",
    "**/.working/",
    "**/.cache/",
    "*.ai-tmp",
    "*.tmp",
    "*.bak",
    "external_sources_local/",
    "large_sources_local/",
    "external_local_archive/",
]

FORBIDDEN_TRACKED_TEMP_DIR_NAMES = {
    "_tmp",
    "tmp",
    "temp",
    "scratch",
    ".scratch",
    ".working",
    ".cache",
}

ALLOWED_TRACKED_TEMP_CONTROL_FILES = {
    "tmp/.gitignore",
    "tmp/README.md",
}

FORBIDDEN_TRACKED_TEMP_FILE_SUFFIXES = (
    ".ai-tmp",
    ".bak",
    ".cache",
    ".log",
    ".scratch",
    ".tmp",
)

REQUIRED_BILINGUAL_MARKERS = [
    ("AGENTS.md", ["Mandatory Rules", "强制规则"]),
    ("README.md", ["Mission", "中文摘要"]),
    ("README.zh-CN.md", ["项目使命", "English summary"]),
    ("project_registry/README.md", ["English:", "简体中文："]),
    ("skills/README.md", ["English:", "简体中文："]),
]

FORBIDDEN_PATH_PARTS = [
    "deciphered_ma",
    "deciphered_ren",
    "ma-馬",
    "ren-人",
]

SCAN_IGNORED_DIR_NAMES = {
    ".git",
    ".working",
    ".cache",
    "_tmp",
    "tmp",
    "temp",
    "scratch",
    ".scratch",
    "external_local_archive",
    "external_sources_local",
    "large_sources_local",
    "local_private_data",
    "private_data",
}

FORBIDDEN_TOP_LEVEL_DIRS = ["data", "knowledge_base"]

FORBIDDEN_TEXT_SNIPPETS = [
    "Do not download or commit external oracle bone images",
    "在权利状态和来源政策明确前，不要下载或提交外部甲骨图片",
    "Rights-unclear scans, paper PDFs, large image sets, or commercial publication extracts should not be committed",
    "权利不明的扫描图、论文 PDF、大规模图片和商业出版物整理文本，在权利说明明确前不应提交",
]

RAW_USER_PROMPT_ARCHIVE_PATH_PREFIXES = (
    "doc/public/user_prompt/",
)

def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def check_bilingual_markers(root: Path) -> list[str]:
    issues: list[str] = []
    for relative, markers in REQUIRED_BILINGUAL_MARKERS:
        path = root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                issues.append(f"{relative} missing bilingual marker: {marker}")
    return issues

def check_forbidden_paths(root: Path) -> list[str]:
    issues: list[str] = []
    for relative_path in _repository_candidate_relative_paths(str(root.resolve())):
        path = root / relative_path
        path_text = path.as_posix()
        for forbidden in FORBIDDEN_PATH_PARTS:
            if forbidden in path_text:
                issues.append(f"forbidden path naming pattern: {relative_path}")
    return issues

def check_forbidden_top_level_dirs(root: Path) -> list[str]:
    issues: list[str] = []
    for dirname in FORBIDDEN_TOP_LEVEL_DIRS:
        if (root / dirname).exists():
            issues.append(f"forbidden top-level directory: {dirname}")
    return issues

def check_forbidden_policy_text(root: Path) -> list[str]:
    issues: list[str] = []
    for relative_path in _repository_candidate_relative_paths(str(root.resolve())):
        path = root / relative_path
        if _is_generated_evolution_candidate_material_path(path, root):
            continue
        if _is_raw_user_prompt_archive_path(path, root):
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in {".md", ".txt", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for snippet in FORBIDDEN_TEXT_SNIPPETS:
            if snippet in text:
                issues.append(f"forbidden old policy text in {relative_path}")
    return issues

def _relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()

def _iter_filesystem_candidate_paths(root: Path):
    """Yield non-ignored filesystem paths without descending into archives."""

    for directory, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in SCAN_IGNORED_DIR_NAMES
        ]
        directory_path = Path(directory)
        for filename in filenames:
            yield directory_path / filename

def _iter_repository_candidate_paths(root: Path):
    """Yield tracked and non-ignored files without descending into archives."""

    try:
        result = subprocess.run(
            git_command(
                root,
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ),
            cwd=root,
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError):
        yield from _iter_filesystem_candidate_paths(root)
        return

    for raw_relative in result.stdout.split("\0"):
        if not raw_relative:
            continue
        relative = Path(raw_relative)
        if any(part in SCAN_IGNORED_DIR_NAMES for part in relative.parts[:-1]):
            continue
        path = root / relative
        if path.exists():
            yield path

@lru_cache(maxsize=8)
def _repository_candidate_relative_paths(root_text: str) -> tuple[str, ...]:
    """Return existing, non-ignored candidate paths once per repository root."""

    root = Path(root_text)
    return tuple(
        _relative_posix(path, root)
        for path in _iter_repository_candidate_paths(root)
    )

def _is_generated_evolution_candidate_material_path(path: Path, root: Path) -> bool:
    relative_path = _relative_posix(path, root)
    return (
        relative_path.startswith("corpus/004_bronze-seal-modern-correspondences/")
        and "_obs-evo-cand-bucket_evolution-candidates/" in relative_path
    )

def _is_raw_user_prompt_archive_path(path: Path, root: Path) -> bool:
    relative_path = _relative_posix(path, root)
    return any(relative_path.startswith(prefix) for prefix in RAW_USER_PROMPT_ARCHIVE_PATH_PREFIXES)

def _tracked_files(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            git_command(root, "ls-files"),
            cwd=root,
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            _relative_posix(path, root)
            for path in _iter_filesystem_candidate_paths(root)
            if path.is_file() and ".git" not in path.parts
        ]
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]

def _load_size_limit_exceptions(root: Path) -> tuple[set[str], list[str]]:
    issues: list[str] = []
    exception_path = root / SIZE_LIMIT_EXCEPTIONS
    if not exception_path.exists():
        return set(), [f"missing size-limit exceptions index: {SIZE_LIMIT_EXCEPTIONS}"]

    exceptions: set[str] = set()
    with exception_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if "path" not in (reader.fieldnames or []):
            issues.append(f"{SIZE_LIMIT_EXCEPTIONS} missing required column: path")
            return exceptions, issues
        for line_number, row in enumerate(reader, start=2):
            relative_path = (row.get("path") or "").strip().replace("\\", "/")
            if not relative_path:
                continue
            if relative_path.startswith("/") or "../" in relative_path or relative_path == "..":
                issues.append(f"{SIZE_LIMIT_EXCEPTIONS}:{line_number} has unsafe path: {relative_path}")
                continue
            exceptions.add(relative_path)
    return exceptions, issues

def check_file_size_limits(root: Path) -> list[str]:
    issues: list[str] = []
    exceptions, exception_issues = _load_size_limit_exceptions(root)
    issues.extend(exception_issues)

    for relative_path in _repository_candidate_relative_paths(str(root.resolve())):
        path = root / relative_path
        if not path.is_file():
            continue
        if relative_path.startswith(IGNORED_LOCAL_ARCHIVE_PREFIXES):
            continue
        file_size = path.stat().st_size
        if file_size >= HARD_FILE_LIMIT_BYTES:
            issues.append(
                f"file exceeds hard 40 MiB commit limit: {relative_path} ({file_size} bytes)"
            )
        elif file_size > SIZE_LIMIT_BYTES and relative_path not in exceptions:
            issues.append(
                f"file exceeds SIZE_LIMIT 30 MiB and is not listed in "
                f"{SIZE_LIMIT_EXCEPTIONS}: {relative_path} ({file_size} bytes)"
            )
    return issues

def check_root_gitignore_patterns(root: Path) -> list[str]:
    path = root / ".gitignore"
    if not path.exists():
        return ["missing root .gitignore"]

    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []
    for pattern in REQUIRED_ROOT_GITIGNORE_PATTERNS:
        if pattern not in text:
            issues.append(f".gitignore missing required temporary-artifact pattern: {pattern}")
    return issues

def check_tracked_temp_artifacts(root: Path) -> list[str]:
    issues: list[str] = []
    for relative_path in _tracked_files(root):
        if relative_path in ALLOWED_TRACKED_TEMP_CONTROL_FILES:
            continue
        parts = relative_path.split("/")
        for part in parts[:-1]:
            if part in FORBIDDEN_TRACKED_TEMP_DIR_NAMES:
                issues.append(f"tracked temporary artifact path: {relative_path}")
                break
        else:
            lower_path = relative_path.lower()
            if lower_path.endswith(FORBIDDEN_TRACKED_TEMP_FILE_SUFFIXES):
                issues.append(f"tracked temporary artifact file: {relative_path}")
    return issues

def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def _read_simple_yaml_scalars(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith(" ") or line.startswith("-") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values

def check_asset_records(root: Path) -> list[str]:
    issues: list[str] = []
    asset_rows, asset_issues = _read_csv_rows(root / ASSET_SOURCE_INDEX)
    rights_rows, rights_issues = _read_csv_rows(root / ASSET_RIGHTS_REVIEW_LOG)
    image_profile_rows, image_profile_issues = _read_csv_rows(root / ASSET_IMAGE_TECHNICAL_PROFILE)
    visual_profile_rows, visual_profile_issues = _read_csv_rows(root / ASSET_IMAGE_VISUAL_PROFILE)
    map_rows, map_issues = _read_csv_rows(root / ASSET_ID_SOURCE_MAP)
    issues.extend(asset_issues + rights_issues + image_profile_issues + visual_profile_issues + map_issues)

    asset_ids = {row.get("asset_id", "") for row in asset_rows}
    required_asset_ids = {"asset-000001", "asset-000002", "asset-000003"}
    for asset_id in sorted(required_asset_ids - asset_ids):
        issues.append(f"{ASSET_SOURCE_INDEX} missing asset_id: {asset_id}")

    rights_asset_ids = {row.get("asset_id", "") for row in rights_rows}
    image_profile_asset_ids = {row.get("asset_id", "") for row in image_profile_rows}
    visual_profile_asset_ids = {row.get("asset_id", "") for row in visual_profile_rows}
    map_asset_ids = {row.get("project_id", "") for row in map_rows if row.get("project_id", "").startswith("asset-")}
    for asset_id in sorted(asset_ids - rights_asset_ids):
        issues.append(f"{ASSET_RIGHTS_REVIEW_LOG} missing rights review for asset_id: {asset_id}")
    for asset_id in sorted(asset_ids - map_asset_ids):
        issues.append(f"{ASSET_ID_SOURCE_MAP} missing source map for asset_id: {asset_id}")
    for asset_id in sorted(asset_ids - image_profile_asset_ids):
        issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} missing image profile for asset_id: {asset_id}")
    for asset_id in sorted(asset_ids - visual_profile_asset_ids):
        issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} missing visual profile for asset_id: {asset_id}")

    expected_assets = {
        "asset-000001": {
            "canonical_path": (
                "corpus/005_excavation-sites-periods-and-batches/"
                "001_public-domain-object-image-assets/"
                "001_asset-000001_met-obj-42045_object-image.jpg"
            ),
            "metadata_path": (
                "corpus/005_excavation-sites-periods-and-batches/"
                "001_public-domain-object-image-assets/"
                "001_asset-000001_met-obj-42045_object-image.yaml"
            ),
            "size": 1780568,
            "sha256": "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
            "external_ref": "met-obj-42045",
            "source_id": "src-metmuseum-oracle-bone",
            "image_suffix": "LC-67_43_14_002.jpg",
            "rights_evidence_snippet": "isPublicDomain=true",
            "width": "2667",
            "height": "4000",
            "dpi_x": "",
            "dpi_y": "",
            "icc_profile_bytes": "0",
            "visual_threshold": "140",
            "visual_bbox": ("11", "23", "2233", "3552", "2223", "3530"),
            "foreground_pixel_count": "154404",
            "foreground_pixel_ratio": "0.01447357",
            "mean_luma": "189.3774",
        },
        "asset-000002": {
            "canonical_path": (
                "corpus/005_excavation-sites-periods-and-batches/"
                "001_public-domain-object-image-assets/"
                "002_asset-000002_met-obj-42022_object-image.jpg"
            ),
            "metadata_path": (
                "corpus/005_excavation-sites-periods-and-batches/"
                "001_public-domain-object-image-assets/"
                "002_asset-000002_met-obj-42022_object-image.yaml"
            ),
            "size": 2508142,
            "sha256": "61510f04c8d599e4e5f9bf50ebcb1cb2163ebd7243e4a125ce08e73fdadad8cd",
            "external_ref": "met-obj-42022",
            "source_id": "src-metmuseum-oracle-bone",
            "image_suffix": "LC-18_56_71_002.jpg",
            "rights_evidence_snippet": "isPublicDomain=true",
            "width": "4000",
            "height": "2667",
            "dpi_x": "300",
            "dpi_y": "300",
            "icc_profile_bytes": "3136",
            "visual_threshold": "140",
            "visual_bbox": ("58", "75", "3482", "2535", "3425", "2461"),
            "foreground_pixel_count": "1972665",
            "foreground_pixel_ratio": "0.18491423",
            "mean_luma": "171.9248",
        },
        "asset-000003": {
            "canonical_path": (
                "corpus/005_excavation-sites-periods-and-batches/"
                "001_public-domain-object-image-assets/"
                "003_asset-000003_si-nmaa-fsc-o-26_object-image.jpg"
            ),
            "metadata_path": (
                "corpus/005_excavation-sites-periods-and-batches/"
                "001_public-domain-object-image-assets/"
                "003_asset-000003_si-nmaa-fsc-o-26_object-image.yaml"
            ),
            "size": 633418,
            "sha256": "e4152d2d680234decb8d4b04225c83a59955b69bc4d8b10eebe7a98d54259079",
            "external_ref": "si-nmaa-fsc-o-26",
            "source_id": "src-smithsonian-nmaa-oracle-bone",
            "image_suffix": "FS-FSC-O-26_1/full/full/0/default.jpg",
            "rights_evidence_snippet": "CC0",
            "width": "3000",
            "height": "2000",
            "dpi_x": "72",
            "dpi_y": "72",
            "icc_profile_bytes": "560",
            "visual_threshold": "140",
            "visual_bbox": ("816", "823", "2381", "1762", "1566", "940"),
            "foreground_pixel_count": "208710",
            "foreground_pixel_ratio": "0.03478500",
            "mean_luma": "225.5226",
        },
    }
    rows_by_asset_id = {row.get("asset_id", ""): row for row in asset_rows}
    image_profile_by_asset_id = {row.get("asset_id", ""): row for row in image_profile_rows}
    visual_profile_by_asset_id = {row.get("asset_id", ""): row for row in visual_profile_rows}
    for asset_id, expected in expected_assets.items():
        row = rows_by_asset_id.get(asset_id)
        if not row:
            continue
        if row.get("asset_type") != "museum_object_image":
            issues.append(f"{ASSET_SOURCE_INDEX} asset_type changed: {asset_id}")
        if row.get("canonical_path") != expected["canonical_path"]:
            issues.append(f"{ASSET_SOURCE_INDEX} canonical_path changed: {asset_id}")
        if row.get("primary_external_ref_id") != expected["external_ref"]:
            issues.append(f"{ASSET_SOURCE_INDEX} primary external ref changed: {asset_id}")
        if row.get("source_ids") != expected["source_id"]:
            issues.append(f"{ASSET_SOURCE_INDEX} source_id changed: {asset_id}")
        if row.get("rights_status") != "public_domain_verified":
            issues.append(f"{ASSET_SOURCE_INDEX} rights status must stay public_domain_verified: {asset_id}")
        if row.get("review_status") != "reviewed":
            issues.append(f"{ASSET_SOURCE_INDEX} row must stay reviewed: {asset_id}")
        asset_path = root / expected["canonical_path"]
        if not asset_path.exists():
            issues.append(f"{ASSET_SOURCE_INDEX} asset file missing: {expected['canonical_path']}")
            continue
        if asset_path.stat().st_size != expected["size"]:
            issues.append(f"{ASSET_SOURCE_INDEX} file size changed: {asset_id}")
        if _sha256_file(asset_path) != expected["sha256"]:
            issues.append(f"{ASSET_SOURCE_INDEX} checksum changed: {asset_id}")
        if not row.get("source_url", "").endswith(expected["image_suffix"]):
            issues.append(f"{ASSET_SOURCE_INDEX} source image URL changed: {asset_id}")
        metadata_path = root / expected["metadata_path"]
        if not metadata_path.exists():
            issues.append(f"{ASSET_SOURCE_INDEX} metadata file missing: {expected['metadata_path']}")
            continue
        metadata = _read_simple_yaml_scalars(metadata_path)
        if metadata.get("asset_id") != asset_id:
            issues.append(f"{expected['metadata_path']} asset_id changed")
        if metadata.get("checksum_sha256") != expected["sha256"]:
            issues.append(f"{expected['metadata_path']} checksum changed")
        if metadata.get("rights_status") != "public_domain_verified":
            issues.append(f"{expected['metadata_path']} rights status changed")
        if expected["rights_evidence_snippet"] not in metadata.get("rights_evidence", ""):
            issues.append(f"{expected['metadata_path']} missing public-domain evidence")
        if metadata.get("pixel_width") != expected["width"]:
            issues.append(f"{expected['metadata_path']} pixel_width changed")
        if metadata.get("pixel_height") != expected["height"]:
            issues.append(f"{expected['metadata_path']} pixel_height changed")
        profile = image_profile_by_asset_id.get(asset_id)
        if not profile:
            continue
        if profile.get("image_format") != "JPEG":
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} image format changed: {asset_id}")
        if profile.get("pixel_width") != expected["width"]:
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} width changed: {asset_id}")
        if profile.get("pixel_height") != expected["height"]:
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} height changed: {asset_id}")
        if profile.get("color_mode") != "RGB":
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} color mode changed: {asset_id}")
        if profile.get("dpi_x") != expected["dpi_x"] or profile.get("dpi_y") != expected["dpi_y"]:
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} DPI changed: {asset_id}")
        if profile.get("icc_profile_bytes") != expected["icc_profile_bytes"]:
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} ICC profile byte count changed: {asset_id}")
        if profile.get("checksum_sha256") != expected["sha256"]:
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} checksum changed: {asset_id}")
        if profile.get("analysis_scope") != "image_technical_metadata_only":
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} analysis scope changed: {asset_id}")
        if profile.get("review_status") != "reviewed":
            issues.append(f"{ASSET_IMAGE_TECHNICAL_PROFILE} row must stay reviewed: {asset_id}")
        visual_profile = visual_profile_by_asset_id.get(asset_id)
        if not visual_profile:
            continue
        if visual_profile.get("asset_path") != expected["canonical_path"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} asset_path changed: {asset_id}")
        if visual_profile.get("analysis_tool") != "Pillow":
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} analysis tool changed: {asset_id}")
        if visual_profile.get("analysis_method") != "pillow_luma_threshold_bbox_v1":
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} analysis method changed: {asset_id}")
        if visual_profile.get("luma_threshold") != expected["visual_threshold"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} threshold changed: {asset_id}")
        if visual_profile.get("pixel_width") != expected["width"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} width changed: {asset_id}")
        if visual_profile.get("pixel_height") != expected["height"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} height changed: {asset_id}")
        bbox_values = (
            visual_profile.get("foreground_bbox_x_min", ""),
            visual_profile.get("foreground_bbox_y_min", ""),
            visual_profile.get("foreground_bbox_x_max", ""),
            visual_profile.get("foreground_bbox_y_max", ""),
            visual_profile.get("foreground_bbox_width", ""),
            visual_profile.get("foreground_bbox_height", ""),
        )
        if bbox_values != expected["visual_bbox"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} foreground bbox changed: {asset_id}")
        if visual_profile.get("foreground_pixel_count") != expected["foreground_pixel_count"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} foreground pixel count changed: {asset_id}")
        if visual_profile.get("foreground_pixel_ratio") != expected["foreground_pixel_ratio"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} foreground ratio changed: {asset_id}")
        if visual_profile.get("mean_luma") != expected["mean_luma"]:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} mean luma changed: {asset_id}")
        if visual_profile.get("analysis_scope") != "visual_preprocessing_metadata_only":
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} analysis scope changed: {asset_id}")
        caution = visual_profile.get("caution", "")
        if "not glyph segmentation" not in caution or "paleographic interpretation" not in caution:
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} caution boundary changed: {asset_id}")
        if visual_profile.get("review_status") != "reviewed_algorithmic_metadata":
            issues.append(f"{ASSET_IMAGE_VISUAL_PROFILE} row must stay reviewed algorithmic metadata: {asset_id}")
    return issues

def check_ai_agent_evidence_pack_validator(root: Path) -> list[str]:
    result = subprocess.run(
        [sys.executable, "tools/validation/validate_ai_agent_evidence_packs.py"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode == 0:
        return []
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    return [f"AI Agent evidence-pack validator failed:\n{output}"]

def check_obimd_rights_override(root: Path) -> list[str]:
    """Check the effective OBIMD rights decision without rewriting legacy rows."""
    issues: list[str] = []
    override_path = root / OBIMD_RIGHTS_STATUS_OVERRIDE
    conflict_path = root / OBIMD_RIGHTS_CONFLICT_REVIEW
    if not override_path.exists():
        return [f"{OBIMD_RIGHTS_STATUS_OVERRIDE} missing"]
    if not conflict_path.exists():
        issues.append(f"{OBIMD_RIGHTS_CONFLICT_REVIEW} missing")
    override_rows, override_issues = _read_csv_rows(override_path)
    issues.extend(override_issues)
    if len(override_rows) != 6:
        issues.append(
            f"{OBIMD_RIGHTS_STATUS_OVERRIDE} should contain exactly six active rows"
        )

    expected = {
        "obimd-rights-override-001": (
            "source",
            "src-obimd",
            "metadata_only_until_verified",
            "metadata_only_no_public_redistribution_until_reconciled",
            1,
        ),
        "obimd-rights-override-002": (
            "large_source",
            "large-src-000002;large-src-000004",
            "metadata_only_until_verified",
            "raw_packages_external_archive_metadata_only_until_reconciled",
            2,
        ),
        "obimd-rights-override-003": (
            "package_manifest",
            "src-obimd",
            "metadata_only_until_verified",
            "no_public_derivative_promotion_until_reconciled",
            7,
        ),
        "obimd-rights-override-004": (
            "asset_source_index",
            "source_ids:src-obimd",
            "metadata_only_until_verified",
            "no_public_asset_redistribution_until_reconciled",
            10364,
        ),
        "obimd-rights-override-005": (
            "component_staging",
            "002_obimd-subcharacter-main-staging.csv",
            "metadata_only_until_verified",
            "no_public_component_derivative_promotion_until_reconciled",
            2747,
        ),
        "obimd-rights-override-006": (
            "orphan_rights_log",
            "asset-011000..asset-011049",
            "local_private_only",
            "do_not_publish_or_derive_until_asset_identity_restored",
            50,
        ),
    }
    required_evidence_ids = {"dl-obimd-hf-readme", "dl-obimd-github-readme"}
    required_evidence_urls = {
        "https://huggingface.co/datasets/KLOBIP/OBIMD",
        "https://raw.githubusercontent.com/libang1991/OBIMD/main/README.md",
    }
    required_evidence_checksums = {
        "2ad91fb999e3ea176a2f7dd39cf67b5e8cfb327d9f22f6713aa1d196a61932de",
        "3361eb37c65a01de05d73b57525500eeed6db7c35dcc16c303794a467c4bbd3e",
    }
    seen_ids: set[str] = set()
    for row in override_rows:
        override_id = row.get("override_id", "")
        seen_ids.add(override_id)
        expected_row = expected.get(override_id)
        if expected_row is None:
            issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} unexpected override_id: {override_id}")
            continue
        scope_type, scope_id, effective_status, public_decision, record_count = expected_row
        for field, value in {
            "scope_type": scope_type,
            "scope_id": scope_id,
            "effective_status": effective_status,
            "public_commit_decision": public_decision,
            "record_count": str(record_count),
            "legacy_status": "licensed_for_repository",
            "review_status": "active_conflict_review",
            "research_boundary": "rights_audit_only_not_scholarship",
        }.items():
            if row.get(field, "") != value:
                issues.append(
                    f"{OBIMD_RIGHTS_STATUS_OVERRIDE} {override_id} "
                    f"{field} mismatch: {row.get(field, '')}"
                )
        if not required_evidence_ids.issubset(set(row.get("evidence_download_ids", "").split(";"))):
            issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} {override_id} missing evidence download")
        if not required_evidence_urls.issubset(set(row.get("evidence_urls", "").split(";"))):
            issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} {override_id} missing evidence URL")
        if not required_evidence_checksums.issubset(
            set(row.get("evidence_checksums", "").split(";"))
        ):
            issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} {override_id} missing evidence checksum")
        if row.get("updated_at") != "2026-08-09":
            issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} {override_id} has unexpected updated_at")
        if "rights" not in row.get("caution", "").lower():
            issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} {override_id} missing rights caution")
    missing_ids = sorted(set(expected) - seen_ids)
    for override_id in missing_ids:
        issues.append(f"{OBIMD_RIGHTS_STATUS_OVERRIDE} missing override_id: {override_id}")

    source_rows, source_issues = _read_csv_rows(root / SOURCE_INDEX)
    large_rows, large_issues = _read_csv_rows(root / LARGE_SOURCE_REGISTER)
    package_rows, package_issues = _read_csv_rows(root / SOURCE_PACKAGE_FILE_MANIFEST)
    asset_rows, asset_issues = _read_csv_rows(root / ASSET_SOURCE_INDEX)
    rights_rows, rights_issues = _read_csv_rows(root / ASSET_RIGHTS_REVIEW_LOG)
    component_rows, component_issues = _read_csv_rows(root / OBIMD_SUBCHARACTER_MAIN_STAGING)
    issues.extend(
        source_issues
        + large_issues
        + package_issues
        + asset_issues
        + rights_issues
        + component_issues
    )
    if not any(row.get("source_id") == "src-obimd" for row in source_rows):
        issues.append(f"{SOURCE_INDEX} missing src-obimd")
    large_ids = {row.get("source_package_id") for row in large_rows}
    if not {"large-src-000002", "large-src-000004"}.issubset(large_ids):
        issues.append(f"{LARGE_SOURCE_REGISTER} missing OBIMD package rows")
    package_obimd = [row for row in package_rows if row.get("source_id") == "src-obimd"]
    if len(package_obimd) != 7:
        issues.append(f"{SOURCE_PACKAGE_FILE_MANIFEST} should contain seven OBIMD rows")
    asset_obimd = [
        row for row in asset_rows if "src-obimd" in row.get("source_ids", "").split(";")
    ]
    if len(asset_obimd) != 10364:
        issues.append(f"{ASSET_SOURCE_INDEX} should contain 10364 OBIMD assets")
    asset_obimd_ids = {row.get("asset_id", "") for row in asset_obimd}
    rights_obimd = [row for row in rights_rows if row.get("asset_id", "") in asset_obimd_ids]
    if len(rights_obimd) != 10364:
        issues.append(f"{ASSET_RIGHTS_REVIEW_LOG} should contain 10364 matching OBIMD rights rows")
    expected_orphans = {f"asset-011{i:03d}" for i in range(50)}
    actual_orphans = {
        row.get("asset_id", "") for row in rights_rows if row.get("asset_id", "") in expected_orphans
    }
    if actual_orphans != expected_orphans:
        issues.append(f"{ASSET_RIGHTS_REVIEW_LOG} missing the 50 documented OBIMD orphan rows")
    if len(component_rows) != 2747:
        issues.append(f"{OBIMD_SUBCHARACTER_MAIN_STAGING} should contain 2747 OBIMD rows")

    if conflict_path.exists():
        conflict_text = conflict_path.read_text(encoding="utf-8")
        for marker in [
            "CC BY-NC-ND",
            "academic research only",
            "metadata_only_until_verified",
            "https://huggingface.co/datasets/KLOBIP/OBIMD",
            "https://raw.githubusercontent.com/libang1991/OBIMD/main/README.md",
            "2ad91fb999e3ea176a2f7dd39cf67b5e8cfb327d9f22f6713aa1d196a61932de",
            "3361eb37c65a01de05d73b57525500eeed6db7c35dcc16c303794a467c4bbd3e",
        ]:
            if marker not in conflict_text:
                issues.append(f"{OBIMD_RIGHTS_CONFLICT_REVIEW} missing marker: {marker}")
        if "not scholarship" not in conflict_text.lower():
            issues.append(f"{OBIMD_RIGHTS_CONFLICT_REVIEW} missing non-scholarship boundary")
        if "\ufffd" in conflict_text:
            issues.append(f"{OBIMD_RIGHTS_CONFLICT_REVIEW} contains replacement-character mojibake")
        for line_number, line in enumerate(conflict_text.splitlines(), start=1):
            if len(line) > 80:
                issues.append(f"{OBIMD_RIGHTS_CONFLICT_REVIEW}:{line_number} line exceeds 80 characters")
    return issues

def _read_csv_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    issues: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            return [], [f"{path.name} has no header"]
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                issues.append(f"{path.relative_to(repo_root())}:{line_number} has extra CSV columns")
            rows.append({key: (value or "") for key, value in row.items() if key is not None})
    return rows, issues

def check_ai_agent_benchmark_contract(root: Path) -> list[str]:
    """Check the v2 contract's critical boundary constants and paths."""

    relative = AI_AGENT_BENCHMARK_EXPERIMENT_SCHEMA
    schema_path = root / relative
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{relative} cannot be parsed: {exc}"]

    issues: list[str] = []
    if schema.get("title") != "AI Agent Oracle Bone Candidate Benchmark Experiment v2":
        issues.append(f"{relative} title changed")
    properties = schema.get("properties", {})
    if properties.get("research_boundary", {}).get("const") != (
        "benchmark_experiment_not_scholarship"
    ):
        issues.append(f"{relative} research boundary changed")
    required = set(schema.get("required", []))
    for field in ("benchmark", "protocol", "runs", "adjudication", "evaluation", "human_delivery_package"):
        if field not in required:
            issues.append(f"{relative} missing required field: {field}")
    definitions = schema.get("$defs", {})
    case_definition = definitions.get("case", {})
    case_required = set(case_definition.get("required", []))
    for field in (
        "case_type",
        "blind_alias",
        "evidence_cutoff_at",
        "source_checksums",
        "pretraining_exposure",
        "benchmark_eligibility",
        "dependency_manifest",
    ):
        if field not in case_required:
            issues.append(f"{relative} case missing required field: {field}")
    if (
        definitions.get("sealed_gold", {})
        .get("properties", {})
        .get("storage_class", {})
        .get("enum")
        != ["ignored_local_diagnostic", "external_isolated_scorer"]
    ):
        issues.append(f"{relative} gold storage boundary changed")
    evaluation_properties = definitions.get("evaluation", {}).get("properties", {})
    if "gold_payload_sha256" in evaluation_properties:
        issues.append(f"{relative} must not expose a raw gold payload hash")
    adjudicator_enum = (
        definitions.get("adjudication", {})
        .get("properties", {})
        .get("adjudicator_kind", {})
        .get("enum")
    )
    if adjudicator_enum != ["ai_agent", "agent_panel"]:
        issues.append(f"{relative} adjudicator enum permits non-AI review")
    pilot_path = root / "tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py"
    try:
        pilot_text = pilot_path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(f"{pilot_path.relative_to(root)} cannot be read: {exc}")
    else:
        for marker in (
            "lock-adjudication",
            "ADJUDICATOR_RUNTIME_FIELDS",
            "human_packet_sha256",
        ):
            if marker not in pilot_text:
                issues.append(
                    f"{pilot_path.relative_to(root)} missing {marker}"
                )
    return issues


# ---------------------------------------------------------------------------
# Architecture-reset checks (doc/project/007_*). These replace the former
# per-template structure checks. They enforce policy and content quality,
# not the existence of generated files.
# ---------------------------------------------------------------------------

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    ".gitignore",
    "tmp/.gitignore",
    "tmp/README.md",
    "corpus/README.md",
    "project_registry/README.md",
    "schemas/README.md",
    "skills/README.md",
    "research/README.md",
    "doc/public/user_research/README.md",
    "doc/project/001_project-positioning-and-research-boundaries/README.md",
    "doc/project/002_source-rights-and-provenance-policy/README.md",
    "doc/project/003_record-model-and-id-system/README.md",
    "doc/project/005_ai-agent-research-assistant-design/README.md",
    "doc/project/006_large-source-material-handling/README.md",
    "doc/project/007_architecture-reset-and-human-first-knowledge-base/README.md",
    "doc/project/007_architecture-reset-and-human-first-knowledge-base/"
    "03_object-dossier-standard.md",
    "doc/project/007_architecture-reset-and-human-first-knowledge-base/"
    "05_ai-agent-operating-protocol.md",
    "doc/project/007_architecture-reset-and-human-first-knowledge-base/"
    "06_quality-gates-and-metrics.md",
    SOURCE_INDEX,
    LARGE_SOURCE_REGISTER,
    "project_registry/006_large-source-register/002_source-download-log.csv",
    ASSET_SOURCE_INDEX,
    ASSET_RIGHTS_REVIEW_LOG,
    OBIMD_RIGHTS_STATUS_OVERRIDE,
    "tools/git/check_commit_messages.py",
]

SOURCE_DOWNLOAD_LOG = "project_registry/006_large-source-register/002_source-download-log.csv"

STANDARD_DOSSIER_RECORD = "record.json"
STANDARD_DOSSIER_ROOTS = ("corpus/", "research/")

DISCLAIMER_PATTERNS = [
    re.compile(r"\bnot an? (?:accepted |confirmed |formal )?(?:decipherment|reading)", re.I),
    re.compile(r"不是(?:已确认的?|正式的?)?(?:释读|破译)"),
]
FIXED_PENDING_SNIPPETS = [
    "待查：需核对",
    "待查:需核对",
    "only route record",
    "not_collected",
    "Open first / 先打开的材料",
]
GENERATED_NAME_PATTERN = re.compile(r"scaffold|queue|handoff|route[-_]pack|route[-_]summary", re.I)
GENERATED_NAME_ALLOWLIST = {
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv",
    "tools/002_corpus-import/build_hust_obc_obs_char_promotion_queue.py",
}
MAX_NEW_OBJECT_DIRS_PER_CHANGE = 10
MAX_NEW_NON_CORPUS_FILES_PER_CHANGE = 200
OBJECT_DIR_PATTERN = re.compile(
    r"^(corpus/[^/]+/(?:[^/]+/)?\d{3}_(?:obs|coll|src|lit|case)-[^/]+)/"
)


def check_required_paths(root: Path) -> list[str]:
    return [f"missing required path: {p}" for p in REQUIRED_PATHS if not (root / p).exists()]


def _csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def check_source_register_fields(root: Path) -> list[str]:
    """Every registered source keeps rights, risk, and review status."""
    issues: list[str] = []
    required = {
        SOURCE_INDEX: ("source_id", ["rights_status", "risk_note", "review_status"]),
        LARGE_SOURCE_REGISTER: (
            "source_package_id",
            ["rights_status", "risk_note", "review_status", "storage_hint"],
        ),
        SOURCE_DOWNLOAD_LOG: ("download_id", ["source_id", "status", "risk_note"]),
    }
    for rel, (key, fields) in required.items():
        path = root / rel
        if not path.exists():
            continue
        rows = _csv_dicts(path)
        seen: set[str] = set()
        for index, row in enumerate(rows, 2):
            ident = (row.get(key) or "").strip()
            if not ident:
                issues.append(f"{rel} line {index}: empty {key}")
                continue
            if ident in seen:
                issues.append(f"{rel}: duplicate {key} {ident}")
            seen.add(ident)
            for field in fields:
                if not (row.get(field) or "").strip():
                    issues.append(f"{rel}: {ident} missing {field}")
    return issues


def _tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        git_command(root, "ls-files", "-z"),
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [p for p in result.stdout.decode("utf-8").split("\0") if p]


def check_generated_names(root: Path) -> list[str]:
    """Gate G9: no generated queue / scaffold / handoff / route-pack files."""
    issues = []
    for rel in _tracked_paths(root):
        name = rel.rsplit("/", 1)[-1]
        if GENERATED_NAME_PATTERN.search(name) and rel not in GENERATED_NAME_ALLOWLIST:
            issues.append(f"G9 generated work-queue file is not allowed: {rel}")
    return issues


def _broken_backtick_lines(lines: list[str]) -> list[int]:
    broken = []
    in_fence = False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.count("`") % 2 == 1:
            broken.append(number)
    return broken


def dossier_issues(readme: Path, rel_dir: str) -> list[str]:
    """Gates G2, G3, G5, G6, G11 for one standard dossier directory."""
    issues: list[str] = []
    directory = readme.parent
    extra_md = sorted(
        p.name for p in directory.iterdir() if p.suffix.lower() == ".md" and p.name != "README.md"
    )
    if extra_md:
        issues.append(f"G2 {rel_dir}: extra human Markdown files {extra_md}")
    text = readme.read_text(encoding="utf-8")
    lines = text.splitlines()
    disclaimers = sum(1 for line in lines if any(p.search(line) for p in DISCLAIMER_PATTERNS))
    if disclaimers > 1:
        issues.append(f"G3 {rel_dir}/README.md: {disclaimers} boundary disclaimers (max 1)")
    for snippet in FIXED_PENDING_SNIPPETS:
        if snippet in text:
            issues.append(f"G5 {rel_dir}/README.md: fixed placeholder text {snippet!r}")
    broken = _broken_backtick_lines(lines)
    if broken:
        issues.append(f"G6 {rel_dir}/README.md: identifier or path broken across lines at {broken[:5]}")
    record_path = directory / STANDARD_DOSSIER_RECORD
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return issues + [f"G11 {rel_dir}/record.json unreadable: {error}"]
    object_id = record.get("id", "")
    if not object_id or object_id not in text:
        issues.append(f"G11 {rel_dir}: record id {object_id!r} not shown in README.md")
    for source in record.get("sources", []):
        ref = source.get("source_id", "") if isinstance(source, dict) else str(source)
        if ref and ref not in text:
            issues.append(f"G11 {rel_dir}: source {ref} in record.json not cited in README.md")
    for image in record.get("images", []):
        path = image.get("path", "") if isinstance(image, dict) else str(image)
        if path and not (directory / path).exists():
            issues.append(f"G11 {rel_dir}: image {path} listed in record.json is missing")
    return issues


def check_standard_dossiers(root: Path) -> list[str]:
    """Apply the dossier standard to every directory holding record.json."""
    issues: list[str] = []
    for rel in _tracked_paths(root):
        if not rel.endswith("/" + STANDARD_DOSSIER_RECORD):
            continue
        if not rel.startswith(STANDARD_DOSSIER_ROOTS):
            continue
        rel_dir = rel.rsplit("/", 1)[0]
        readme = root / rel_dir / "README.md"
        if not readme.exists():
            issues.append(f"G2 {rel_dir}: record.json without README.md dossier")
            continue
        issues.extend(dossier_issues(readme, rel_dir))
    return issues


def _staged_changes(root: Path) -> list[tuple[str, str]]:
    result = subprocess.run(
        git_command(root, "diff", "--cached", "--name-status", "--no-renames", "-z"),
        cwd=root,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    parts = [p for p in result.stdout.decode("utf-8").split("\0") if p]
    return list(zip(parts[0::2], parts[1::2]))


def check_change_size(root: Path) -> tuple[list[str], list[str]]:
    """Gates G7 (blocking) and G8 (warning) on the staged change."""
    changes = _staged_changes(root)
    if not changes:
        return [], []
    head = subprocess.run(
        git_command(root, "ls-tree", "-r", "--name-only", "-z", "HEAD"),
        cwd=root,
        capture_output=True,
    )
    head_paths = head.stdout.decode("utf-8").split("\0") if head.returncode == 0 else []
    head_dirs = set()
    for path in head_paths:
        match = OBJECT_DIR_PATTERN.match(path)
        if match:
            head_dirs.add(match.group(1))
    new_dirs = set()
    new_non_corpus = 0
    for status, path in changes:
        if status != "A":
            continue
        match = OBJECT_DIR_PATTERN.match(path)
        if match and match.group(1) not in head_dirs:
            new_dirs.add(match.group(1))
        if not path.startswith("corpus/"):
            new_non_corpus += 1
    issues, warnings = [], []
    if len(new_dirs) > MAX_NEW_OBJECT_DIRS_PER_CHANGE:
        issues.append(
            f"G7 staged change creates {len(new_dirs)} new object directories "
            f"(max {MAX_NEW_OBJECT_DIRS_PER_CHANGE}); batch generation is not allowed"
        )
    if new_non_corpus > MAX_NEW_NON_CORPUS_FILES_PER_CHANGE:
        warnings.append(
            f"G8 staged change adds {new_non_corpus} non-corpus files "
            f"(soft limit {MAX_NEW_NON_CORPUS_FILES_PER_CHANGE})"
        )
    return issues, warnings


def main() -> int:
    root = repo_root()
    issues: list[str] = []
    issues.extend(check_required_paths(root))
    issues.extend(check_bilingual_markers(root))
    issues.extend(check_forbidden_paths(root))
    issues.extend(check_forbidden_top_level_dirs(root))
    issues.extend(check_forbidden_policy_text(root))
    issues.extend(check_file_size_limits(root))
    issues.extend(check_root_gitignore_patterns(root))
    issues.extend(check_tracked_temp_artifacts(root))
    issues.extend(check_source_register_fields(root))
    issues.extend(check_asset_records(root))
    issues.extend(check_obimd_rights_override(root))
    issues.extend(check_ai_agent_evidence_pack_validator(root))
    issues.extend(check_ai_agent_benchmark_contract(root))
    issues.extend(check_generated_names(root))
    issues.extend(check_standard_dossiers(root))
    change_issues, warnings = check_change_size(root)
    issues.extend(change_issues)

    for warning in warnings:
        print(f"WARN {warning}")
    if issues:
        print("FAIL repository skeleton")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS repository skeleton")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
