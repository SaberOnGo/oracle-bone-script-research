#!/usr/bin/env python3
"""Validate the repository skeleton for Oracle Bone Script Research."""

from __future__ import annotations

import sys
import csv
import subprocess
from pathlib import Path


SIZE_LIMIT_BYTES = 30 * 1024 * 1024
HARD_FILE_LIMIT_BYTES = 40 * 1024 * 1024
SIZE_LIMIT_EXCEPTIONS = "project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv"
SOURCE_INDEX = "corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv"
SOURCE_INVENTORY = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "002_authoritative-online-source-inventory.csv"
)
SOURCE_DOWNLOAD_MANIFEST = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "003_source-download-manifest.csv"
)
SOURCE_DOWNLOAD_LOG = "project_registry/006_large-source-register/002_source-download-log.csv"
LARGE_SOURCE_REGISTER = "project_registry/006_large-source-register/001_large-source-register.csv"
OPEN_ORACLE_STRATEGY_REVIEW = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "005_open-oracle-strategy-review.md"
)
AUTHORITATIVE_SOURCE_EXPANSION_NOTES = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "006_authoritative-source-expansion-notes.md"
)

ADOPTED_PROFESSIONAL_SOURCE_IDS = {
    "src-xiaoxuetang-jiaguwen",
    "src-xiaoxuetang-obm",
    "src-ihp-oracle-rubbings",
    "src-ihp-museum-oracle-bones",
    "src-yinqi-wenyuan",
    "src-obid-ancientbooks",
    "src-tsinghua-oracle-bones",
    "src-cambridge-hopkins",
    "src-british-museum-oracle-bone",
    "src-smithsonian-nmaa-oracle-bone",
}

ADOPTED_PROJECT_INDEX_SOURCE_IDS = {
    "src-open-oracle",
}

REQUIRED_TOP_LEVEL_GITIGNORE_DIRS = [
    "apps",
    "corpus",
    "database",
    "doc",
    "license",
    "project_registry",
    "readme",
    "research",
    "schemas",
    "skills",
    "tests",
    "tmp",
    "tools",
]

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

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE.md",
    ".gitignore",
    "doc/README.md",
    "doc/project/001_project-positioning-and-research-boundaries/README.md",
    "doc/project/002_source-rights-and-provenance-policy/README.md",
    "doc/project/003_record-model-and-id-system/README.md",
    "doc/project/004_oracle-bone-script-research-methods/README.md",
    "doc/project/005_ai-agent-research-assistant-design/README.md",
    "doc/project/006_large-source-material-handling/README.md",
    "doc/public/user_plan/README.md",
    "doc/public/user_plan/001_project-architecture-and-corpus-organization-plan.zh-CN.md",
    "doc/public/user_plan/001_project-architecture-and-corpus-organization-plan.en.md",
    "doc/public/user_research/README.md",
    "doc/public/user_research/.gitignore",
    "doc/public/user_prompt/README.md",
    "doc/public/user_prompt/任务计划prompt.md",
    "project_registry/README.md",
    "project_registry/001_repository-structure-and-naming-rules/README.md",
    "project_registry/002_project-id-to-source-reference-map/README.md",
    "project_registry/003_external-source-prefixes/003_external-source-prefixes.csv",
    "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv",
    "project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv",
    "project_registry/005_bilingual-project-glossary/001_terms.zh-CN.md",
    "project_registry/005_bilingual-project-glossary/002_terms.en.md",
    "project_registry/006_large-source-register/README.md",
    "project_registry/006_large-source-register/001_large-source-register.csv",
    SOURCE_DOWNLOAD_LOG,
    "research/README.md",
    "skills/README.md",
    "skills/oracle-character-record-curation/SKILL.md",
    "skills/source-provenance-review/SKILL.md",
    "skills/ai-agent-evidence-pack-review/SKILL.md",
    "schemas/README.md",
    "corpus/README.md",
    "corpus/006_research-sources-and-bibliography/000_source-registers/README.md",
    SOURCE_INDEX,
    SOURCE_INVENTORY,
    SOURCE_DOWNLOAD_MANIFEST,
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "004_first-stage-source-adoption-notes.md",
    OPEN_ORACLE_STRATEGY_REVIEW,
    AUTHORITATIVE_SOURCE_EXPANSION_NOTES,
    "tmp/.gitignore",
    "tmp/README.md",
    "tools/git/check_commit_messages.py",
    "tools/002_corpus-import/download_source_manifest.py",
    "tools/validation/check_repository_skeleton.py",
    "tests/test_check_commit_messages.py",
    "tests/test_repository_skeleton.py",
]

REQUIRED_PATHS.extend(f"{dirname}/.gitignore" for dirname in REQUIRED_TOP_LEVEL_GITIGNORE_DIRS)

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


def check_required_paths(root: Path) -> list[str]:
    issues: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            issues.append(f"missing required path: {relative}")
    return issues


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
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        path_text = path.as_posix()
        for forbidden in FORBIDDEN_PATH_PARTS:
            if forbidden in path_text:
                issues.append(f"forbidden path naming pattern: {path.relative_to(root)}")
    return issues


def check_forbidden_top_level_dirs(root: Path) -> list[str]:
    issues: list[str] = []
    for dirname in FORBIDDEN_TOP_LEVEL_DIRS:
        if (root / dirname).exists():
            issues.append(f"forbidden top-level directory: {dirname}")
    return issues


def check_forbidden_policy_text(root: Path) -> list[str]:
    issues: list[str] = []
    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
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
                issues.append(f"forbidden old policy text in {path.relative_to(root)}")
    return issues


def _relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_raw_user_prompt_archive_path(path: Path, root: Path) -> bool:
    relative_path = _relative_posix(path, root)
    return any(relative_path.startswith(prefix) for prefix in RAW_USER_PROMPT_ARCHIVE_PATH_PREFIXES)


def _tracked_files(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            _relative_posix(path, root)
            for path in root.rglob("*")
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

    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative_path = _relative_posix(path, root)
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


def check_source_registers(root: Path) -> list[str]:
    issues: list[str] = []
    source_rows, source_issues = _read_csv_rows(root / SOURCE_INDEX)
    inventory_rows, inventory_issues = _read_csv_rows(root / SOURCE_INVENTORY)
    manifest_rows, manifest_issues = _read_csv_rows(root / SOURCE_DOWNLOAD_MANIFEST)
    log_rows, log_issues = _read_csv_rows(root / SOURCE_DOWNLOAD_LOG)
    large_rows, large_issues = _read_csv_rows(root / LARGE_SOURCE_REGISTER)
    issues.extend(source_issues + inventory_issues + manifest_issues + log_issues + large_issues)

    source_ids = {row.get("source_id", "") for row in source_rows}
    missing_adopted = sorted(ADOPTED_PROFESSIONAL_SOURCE_IDS - source_ids)
    for source_id in missing_adopted:
        issues.append(f"missing adopted professional source: {source_id}")
    missing_project_indexes = sorted(ADOPTED_PROJECT_INDEX_SOURCE_IDS - source_ids)
    for source_id in missing_project_indexes:
        issues.append(f"missing adopted project-index source: {source_id}")

    source_by_id = {row.get("source_id", ""): row for row in source_rows}
    for source_id in sorted(ADOPTED_PROFESSIONAL_SOURCE_IDS):
        row = source_by_id.get(source_id)
        if not row:
            continue
        if not row.get("adoption_status", "").startswith("adopted_"):
            issues.append(f"{SOURCE_INDEX} source not marked adopted: {source_id}")
        if row.get("review_status") != "reviewed":
            issues.append(f"{SOURCE_INDEX} source not reviewed: {source_id}")
    for source_id in sorted(ADOPTED_PROJECT_INDEX_SOURCE_IDS):
        row = source_by_id.get(source_id)
        if not row:
            continue
        if row.get("adoption_status") != "adopted_project_index":
            issues.append(f"{SOURCE_INDEX} project index not marked adopted_project_index: {source_id}")
        if row.get("review_status") != "reviewed":
            issues.append(f"{SOURCE_INDEX} project index not reviewed: {source_id}")

    inventory_source_ids = {row.get("source_id", "") for row in inventory_rows}
    for source_id in sorted(source_ids - inventory_source_ids):
        issues.append(f"{SOURCE_INVENTORY} missing source_id: {source_id}")

    manifest_ids = {row.get("download_id", "") for row in manifest_rows}
    log_ids = {row.get("download_id", "") for row in log_rows}
    for source_id in sorted({row.get("source_id", "") for row in manifest_rows} - source_ids):
        issues.append(f"{SOURCE_DOWNLOAD_MANIFEST} references unknown source_id: {source_id}")
    for download_id in sorted(manifest_ids - log_ids):
        issues.append(f"{SOURCE_DOWNLOAD_LOG} missing download_id from manifest: {download_id}")
    for row in log_rows:
        local_temp_path = row.get("local_temp_path", "")
        if local_temp_path and not local_temp_path.startswith("tmp/"):
            issues.append(f"{SOURCE_DOWNLOAD_LOG} local_temp_path must stay under tmp/: {local_temp_path}")

    for row in large_rows:
        if row.get("file_size_bytes") and row.get("storage_status") == "not_downloaded_registered":
            issues.append(f"{LARGE_SOURCE_REGISTER} not-downloaded package should not claim file_size_bytes")
    return issues


def main() -> int:
    root = repo_root()
    issues = []
    issues.extend(check_required_paths(root))
    issues.extend(check_bilingual_markers(root))
    issues.extend(check_forbidden_paths(root))
    issues.extend(check_forbidden_top_level_dirs(root))
    issues.extend(check_forbidden_policy_text(root))
    issues.extend(check_file_size_limits(root))
    issues.extend(check_root_gitignore_patterns(root))
    issues.extend(check_tracked_temp_artifacts(root))
    issues.extend(check_source_registers(root))

    if issues:
        print("FAIL repository skeleton")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS repository skeleton")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
