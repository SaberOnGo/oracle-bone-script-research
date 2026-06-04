#!/usr/bin/env python3
"""Validate the repository skeleton for Oracle Bone Script Research."""

from __future__ import annotations

import sys
import csv
import json
import subprocess
from pathlib import Path


SIZE_LIMIT_BYTES = 30 * 1024 * 1024
HARD_FILE_LIMIT_BYTES = 40 * 1024 * 1024
SIZE_LIMIT_EXCEPTIONS = "project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv"
EXTERNAL_SOURCE_PREFIXES = "project_registry/003_external-source-prefixes/003_external-source-prefixes.csv"
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
SOURCE_FIELD_MAP = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "007_source-field-map.csv"
)
IMPORT_READINESS_NOTES = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "008_first-stage-import-readiness-notes.md"
)
SOURCE_PACKAGE_FILE_MANIFEST = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "009_source-package-file-manifest.csv"
)
DOWNLOADED_METADATA_PROFILE = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "010_downloaded-metadata-profile.csv"
)
CORE_INSTITUTIONAL_ACCESS_PROFILE = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "011_core-institutional-access-profile.csv"
)
OBM_ABBREVIATION_STAGING = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "012_obm-abbreviation-staging.csv"
)
HUST_OBC_VALIDATION_CLASS_STAGING = (
    "corpus/001_oracle-characters/000_character-registers/"
    "005_hust-obc-validation-class-staging.csv"
)
HUST_OBC_VALIDATION_LABEL_CROSSWALK = (
    "corpus/001_oracle-characters/000_character-registers/"
    "007_hust-obc-validation-label-crosswalk-staging.csv"
)
HUST_OBC_SOURCE_CATEGORY_STAGING = (
    "corpus/001_oracle-characters/000_character-registers/"
    "008_hust-obc-source-category-staging.csv"
)
HUST_OBC_OBS_CHAR_PROMOTION_QUEUE = (
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)
HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY = (
    "corpus/001_oracle-characters/000_character-registers/"
    "010_hust-obc-promotion-bucket-review-summary.csv"
)
HUST_OBC_PROMOTION_BUCKET_MANIFEST_FILENAME = "000_hust-obc-promotion-bucket-manifest.csv"
HUST_OBC_CANDIDATE_GRAPH_EDGES = (
    "corpus/008_relationship-graph/"
    "005_hust-obc-candidate-graph-edges.jsonl"
)
OBIMD_COMPONENT_GRAPH_EDGES = (
    "corpus/008_relationship-graph/"
    "006_obimd-component-graph-edges.jsonl"
)
EVOBC_EVOLUTION_GRAPH_EDGES = (
    "corpus/008_relationship-graph/"
    "007_evobc-evolution-graph-edges.jsonl"
)
RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "001_relationship-graph-edge-type-summary.csv"
)
RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "002_relationship-graph-node-degree-summary.csv"
)
AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "003_ai-agent-relationship-graph-context-pack.json"
)
OBIMD_MAIN_CHARACTER_STAGING = (
    "corpus/001_oracle-characters/000_character-registers/"
    "006_obimd-main-character-staging.csv"
)
OBIMD_SUBCHARACTER_MAIN_STAGING = (
    "corpus/003_graphemic-components/000_component-registers/"
    "002_obimd-subcharacter-main-staging.csv"
)
OBIMD_SUBCHARACTER_GLYPH_STAGING = (
    "corpus/003_graphemic-components/000_component-registers/"
    "003_obimd-subcharacter-glyph-staging.csv"
)
CAMBRIDGE_HOPKINS_CROSSWALK_STAGING = (
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "002_cambridge-hopkins-crosswalk-staging.csv"
)
CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY = (
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "003_cambridge-hopkins-classified-summary.csv"
)
COLLECTION_PROVENANCE_STAGING = (
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "001_institutional-collection-provenance-staging.csv"
)
IHP_MUSEUM_OBJECT_STAGING = (
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "002_ihp-museum-oracle-bone-object-staging.csv"
)
EVOBC_EVOLUTION_CATEGORY_STAGING = (
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
EVOBC_ERA_SOURCE_CODEBOOK_STAGING = (
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "002_evobc-era-source-codebook-staging.csv"
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

REQUIRED_EXTERNAL_PREFIXES = {
    "cam-hopkins-y",
    "cam-hopkins-c",
    "cam-hopkins-h",
    "cam-hopkins-j",
    "hust-obc-cat",
    "ihp-mus-obj",
    "obimd-main",
    "obimd-sub",
    "obimd-glyph-link",
    "evobc-cat",
    "evobc-code",
    "collection-prov",
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
    EXTERNAL_SOURCE_PREFIXES,
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
    SOURCE_FIELD_MAP,
    IMPORT_READINESS_NOTES,
    SOURCE_PACKAGE_FILE_MANIFEST,
    DOWNLOADED_METADATA_PROFILE,
    CORE_INSTITUTIONAL_ACCESS_PROFILE,
    OBM_ABBREVIATION_STAGING,
    HUST_OBC_VALIDATION_CLASS_STAGING,
    HUST_OBC_VALIDATION_LABEL_CROSSWALK,
    HUST_OBC_SOURCE_CATEGORY_STAGING,
    HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
    HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY,
    HUST_OBC_CANDIDATE_GRAPH_EDGES,
    OBIMD_COMPONENT_GRAPH_EDGES,
    EVOBC_EVOLUTION_GRAPH_EDGES,
    RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY,
    RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY,
    AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK,
    OBIMD_MAIN_CHARACTER_STAGING,
    OBIMD_SUBCHARACTER_MAIN_STAGING,
    OBIMD_SUBCHARACTER_GLYPH_STAGING,
    EVOBC_EVOLUTION_CATEGORY_STAGING,
    EVOBC_ERA_SOURCE_CODEBOOK_STAGING,
    CAMBRIDGE_HOPKINS_CROSSWALK_STAGING,
    CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY,
    COLLECTION_PROVENANCE_STAGING,
    IHP_MUSEUM_OBJECT_STAGING,
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/README.md",
    "tmp/.gitignore",
    "tmp/README.md",
    "tools/git/check_commit_messages.py",
    "tools/002_corpus-import/download_source_manifest.py",
    "tools/002_corpus-import/build_evobc_evolution_staging.py",
    "tools/002_corpus-import/build_hust_obc_validation_label_crosswalk.py",
    "tools/002_corpus-import/build_hust_obc_source_category_staging.py",
    "tools/002_corpus-import/build_hust_obc_obs_char_promotion_queue.py",
    "tools/002_corpus-import/build_hust_obc_promotion_bucket_manifests.py",
    "tools/002_corpus-import/build_ihp_museum_object_staging.py",
    "tools/003_graph-generation/build_hust_obc_candidate_graph_edges.py",
    "tools/003_graph-generation/build_obimd_component_graph_edges.py",
    "tools/003_graph-generation/build_evobc_evolution_graph_edges.py",
    "tools/004_statistics-generation/build_relationship_graph_statistics.py",
    "tools/005_ai-context-pack-builder/build_relationship_graph_context_pack.py",
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


def hust_obc_promotion_bucket_directories() -> list[str]:
    directories = []
    for bucket_number in range(1, 17):
        bucket_start = (bucket_number - 1) * 100 + 1
        bucket_end = bucket_start + 99
        directories.append(
            f"{bucket_number:03d}_{bucket_start:06d}-{bucket_end:06d}"
            "_obs-char-bucket_oracle-characters"
        )
    return directories


def hust_obc_promotion_bucket_manifest_paths() -> list[str]:
    return [
        "corpus/001_oracle-characters/"
        f"{bucket_directory}/{HUST_OBC_PROMOTION_BUCKET_MANIFEST_FILENAME}"
        for bucket_directory in hust_obc_promotion_bucket_directories()
    ]


REQUIRED_PATHS.extend(hust_obc_promotion_bucket_manifest_paths())

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


def _read_jsonl_rows(path: Path) -> tuple[list[dict[str, object]], list[str]]:
    issues: list[str] = []
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                issues.append(f"{path.relative_to(repo_root())}:{line_number} invalid JSON: {exc.msg}")
                continue
            if not isinstance(value, dict):
                issues.append(f"{path.relative_to(repo_root())}:{line_number} must be a JSON object")
                continue
            rows.append(value)
    return rows, issues


def check_relationship_graph_edges(root: Path) -> list[str]:
    issues: list[str] = []
    edge_rows, edge_issues = _read_jsonl_rows(root / HUST_OBC_CANDIDATE_GRAPH_EDGES)
    obimd_edge_rows, obimd_edge_issues = _read_jsonl_rows(root / OBIMD_COMPONENT_GRAPH_EDGES)
    evobc_edge_rows, evobc_edge_issues = _read_jsonl_rows(root / EVOBC_EVOLUTION_GRAPH_EDGES)
    source_category_rows, source_category_issues = _read_csv_rows(root / HUST_OBC_SOURCE_CATEGORY_STAGING)
    validation_rows, validation_issues = _read_csv_rows(root / HUST_OBC_VALIDATION_CLASS_STAGING)
    obimd_subchar_main_rows, obimd_subchar_main_issues = _read_csv_rows(
        root / OBIMD_SUBCHARACTER_MAIN_STAGING
    )
    obimd_subchar_glyph_rows, obimd_subchar_glyph_issues = _read_csv_rows(
        root / OBIMD_SUBCHARACTER_GLYPH_STAGING
    )
    evobc_category_rows, evobc_category_issues = _read_csv_rows(
        root / EVOBC_EVOLUTION_CATEGORY_STAGING
    )
    evobc_codebook_rows, evobc_codebook_issues = _read_csv_rows(
        root / EVOBC_ERA_SOURCE_CODEBOOK_STAGING
    )
    issues.extend(edge_issues)
    issues.extend(obimd_edge_issues)
    issues.extend(evobc_edge_issues)
    issues.extend(source_category_issues)
    issues.extend(validation_issues)
    issues.extend(obimd_subchar_main_issues)
    issues.extend(obimd_subchar_glyph_issues)
    issues.extend(evobc_category_issues)
    issues.extend(evobc_codebook_issues)

    if len(edge_rows) != 3562:
        issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} should contain exactly 3562 edges")

    required_fields = {
        "edge_id",
        "source_node_id",
        "edge_type",
        "target_node_id",
        "confidence_level",
        "source_ids",
        "evidence_note",
        "review_status",
    }
    edge_ids: set[str] = set()
    edge_type_counts: dict[str, int] = {}
    for row in edge_rows:
        edge_id = str(row.get("edge_id", ""))
        if not required_fields.issubset(row):
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} edge missing required fields: {edge_id}")
        if edge_id in edge_ids:
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} duplicate edge_id: {edge_id}")
        edge_ids.add(edge_id)
        edge_type = str(row.get("edge_type", ""))
        edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1
        if row.get("confidence_level") != "high":
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} edge must stay high confidence metadata edge: {edge_id}")
        if row.get("source_ids") != ["src-hust-obc"]:
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} edge must reference only src-hust-obc: {edge_id}")
        if row.get("review_status") != "reviewed":
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} edge must stay reviewed: {edge_id}")
        note = str(row.get("evidence_note", ""))
        if "not" not in note.lower():
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} edge evidence note must preserve caution: {edge_id}")

    expected_type_counts = {
        "HAS_HUST_OBC_SOURCE_CATEGORY": 1781,
        "HAS_HUST_OBC_OCR_LABEL_CANDIDATE": 1781,
    }
    if edge_rows and edge_type_counts != expected_type_counts:
        issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} edge type counts changed")

    validation_candidate_ids = {row.get("candidate_class_id", "") for row in validation_rows}
    expected_class_edges: list[dict[str, object]] = []
    expected_label_edges: list[dict[str, object]] = []
    for index, row in enumerate(source_category_rows, start=1):
        candidate_id = row.get("linked_candidate_class_id", "")
        if candidate_id not in validation_candidate_ids:
            issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} source category links unknown candidate: {candidate_id}")
        source_category_row_id = row.get("source_category_row_id", "")
        expected_class_edges.append(
            {
                "edge_id": f"edge-hust-obc-class-src-cat-{index:04d}",
                "source_node_id": candidate_id,
                "edge_type": "HAS_HUST_OBC_SOURCE_CATEGORY",
                "target_node_id": source_category_row_id,
            }
        )
        label_node_id = (
            "hust-obc-ocr-label-"
            f"{row.get('source_modern_label_codepoint', '').lower().replace('+', '')}"
        )
        expected_label_edges.append(
            {
                "edge_id": f"edge-hust-obc-src-cat-label-{index:04d}",
                "source_node_id": source_category_row_id,
                "edge_type": "HAS_HUST_OBC_OCR_LABEL_CANDIDATE",
                "target_node_id": label_node_id,
            }
        )

    compact_edge_rows = [
        {
            "edge_id": row.get("edge_id"),
            "source_node_id": row.get("source_node_id"),
            "edge_type": row.get("edge_type"),
            "target_node_id": row.get("target_node_id"),
        }
        for row in edge_rows
    ]
    if edge_rows and compact_edge_rows[:1781] != expected_class_edges:
        issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} class-to-category edge sequence changed")
    if edge_rows and compact_edge_rows[1781:] != expected_label_edges:
        issues.append(f"{HUST_OBC_CANDIDATE_GRAPH_EDGES} category-to-label edge sequence changed")

    if len(obimd_edge_rows) != 44433:
        issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} should contain exactly 44433 edges")

    obimd_required_fields = required_fields
    obimd_edge_ids: set[str] = set()
    obimd_edge_type_counts: dict[str, int] = {}
    for row in obimd_edge_rows:
        edge_id = str(row.get("edge_id", ""))
        if not obimd_required_fields.issubset(row):
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} edge missing required fields: {edge_id}")
        if edge_id in obimd_edge_ids:
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} duplicate edge_id: {edge_id}")
        obimd_edge_ids.add(edge_id)
        edge_type = str(row.get("edge_type", ""))
        obimd_edge_type_counts[edge_type] = obimd_edge_type_counts.get(edge_type, 0) + 1
        if row.get("confidence_level") != "high":
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} edge must stay high confidence metadata edge: {edge_id}")
        if row.get("source_ids") != ["src-obimd"]:
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} edge must reference only src-obimd: {edge_id}")
        if row.get("review_status") != "reviewed":
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} edge must stay reviewed: {edge_id}")
        note = str(row.get("evidence_note", ""))
        if "not" not in note.lower():
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} edge evidence note must preserve caution: {edge_id}")

    expected_obimd_type_counts = {
        "OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER": 2747,
        "OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT": 41686,
    }
    if obimd_edge_rows and obimd_edge_type_counts != expected_obimd_type_counts:
        issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} edge type counts changed")

    subcandidate_by_uid = {
        row.get("source_subcharacter_uid", ""): row.get("candidate_subcharacter_id", "")
        for row in obimd_subchar_main_rows
    }
    expected_obimd_sub_main_edges: list[dict[str, object]] = []
    for index, row in enumerate(obimd_subchar_main_rows, start=1):
        expected_obimd_sub_main_edges.append(
            {
                "edge_id": f"edge-obimd-sub-main-{index:06d}",
                "source_node_id": row.get("candidate_subcharacter_id", ""),
                "edge_type": "OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER",
                "target_node_id": row.get("main_character_external_ref_id", ""),
            }
        )
    expected_obimd_sub_glyph_edges: list[dict[str, object]] = []
    for index, row in enumerate(obimd_subchar_glyph_rows, start=1):
        sub_uid = row.get("source_subcharacter_uid", "")
        if sub_uid not in subcandidate_by_uid:
            issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} glyph edge source UID missing: {sub_uid}")
        target_codepoints = row.get("glyph_codepoint_uplus", "").lower().replace("+", "").replace(";", "-")
        expected_obimd_sub_glyph_edges.append(
            {
                "edge_id": f"edge-obimd-sub-glyph-{index:06d}",
                "source_node_id": subcandidate_by_uid.get(sub_uid, ""),
                "edge_type": "OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT",
                "target_node_id": f"obimd-glyph-codepoint-{target_codepoints}",
            }
        )

    compact_obimd_edge_rows = [
        {
            "edge_id": row.get("edge_id"),
            "source_node_id": row.get("source_node_id"),
            "edge_type": row.get("edge_type"),
            "target_node_id": row.get("target_node_id"),
        }
        for row in obimd_edge_rows
    ]
    if obimd_edge_rows and compact_obimd_edge_rows[:2747] != expected_obimd_sub_main_edges:
        issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} subcharacter-to-main edge sequence changed")
    if obimd_edge_rows and compact_obimd_edge_rows[2747:] != expected_obimd_sub_glyph_edges:
        issues.append(f"{OBIMD_COMPONENT_GRAPH_EDGES} subcharacter-to-glyph edge sequence changed")

    if len(evobc_edge_rows) != 51679:
        issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} should contain exactly 51679 edges")

    evobc_edge_ids: set[str] = set()
    evobc_edge_type_counts: dict[str, int] = {}
    for row in evobc_edge_rows:
        edge_id = str(row.get("edge_id", ""))
        if not required_fields.issubset(row):
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge missing required fields: {edge_id}")
        if edge_id in evobc_edge_ids:
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} duplicate edge_id: {edge_id}")
        evobc_edge_ids.add(edge_id)
        edge_type = str(row.get("edge_type", ""))
        evobc_edge_type_counts[edge_type] = evobc_edge_type_counts.get(edge_type, 0) + 1
        if row.get("confidence_level") != "high":
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge must stay high confidence metadata edge: {edge_id}")
        if row.get("source_ids") != ["src-evobc"]:
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge must reference only src-evobc: {edge_id}")
        if row.get("review_status") != "reviewed":
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge must stay reviewed: {edge_id}")
        note = str(row.get("evidence_note", ""))
        if "not" not in note.lower():
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge evidence note must preserve caution: {edge_id}")

    expected_evobc_type_counts = {
        "EVOBC_CATEGORY_HAS_ERA_CODE": 26378,
        "EVOBC_CATEGORY_HAS_SOURCE_CODE": 25301,
    }
    if evobc_edge_rows and evobc_edge_type_counts != expected_evobc_type_counts:
        issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge type counts changed")

    evobc_codebook_by_type_value = {
        (row.get("code_type", ""), row.get("code_value", "")): row.get("codebook_row_id", "")
        for row in evobc_codebook_rows
    }
    expected_evobc_edges: list[dict[str, object]] = []
    for row in evobc_category_rows:
        candidate_id = row.get("candidate_evolution_category_id", "")
        category_id = row.get("source_category_id", "")
        if not category_id.isdigit():
            issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} category ID not numeric: {candidate_id}")
            continue
        category_value = int(category_id)
        for era_code in _parse_compact_counts(row.get("era_code_counts", "")):
            codebook_row_id = evobc_codebook_by_type_value.get(("era", era_code), "")
            if not codebook_row_id:
                issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} missing era codebook row: {era_code}")
            expected_evobc_edges.append(
                {
                    "edge_id": f"edge-evobc-cat-era-{category_value:05d}-{int(era_code):02d}",
                    "source_node_id": candidate_id,
                    "edge_type": "EVOBC_CATEGORY_HAS_ERA_CODE",
                    "target_node_id": codebook_row_id,
                }
            )
        for source_code in _parse_compact_counts(row.get("source_code_counts", "")):
            codebook_row_id = evobc_codebook_by_type_value.get(("source", source_code), "")
            if not codebook_row_id:
                issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} missing source codebook row: {source_code}")
            expected_evobc_edges.append(
                {
                    "edge_id": f"edge-evobc-cat-source-{category_value:05d}-{int(source_code):02d}",
                    "source_node_id": candidate_id,
                    "edge_type": "EVOBC_CATEGORY_HAS_SOURCE_CODE",
                    "target_node_id": codebook_row_id,
                }
            )

    compact_evobc_edge_rows = [
        {
            "edge_id": row.get("edge_id"),
            "source_node_id": row.get("source_node_id"),
            "edge_type": row.get("edge_type"),
            "target_node_id": row.get("target_node_id"),
        }
        for row in evobc_edge_rows
    ]
    if evobc_edge_rows and compact_evobc_edge_rows != expected_evobc_edges:
        issues.append(f"{EVOBC_EVOLUTION_GRAPH_EDGES} edge sequence changed")

    return issues


def check_relationship_graph_statistics(root: Path) -> list[str]:
    issues: list[str] = []
    edge_summary_rows, edge_summary_issues = _read_csv_rows(
        root / RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY
    )
    node_degree_rows, node_degree_issues = _read_csv_rows(
        root / RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY
    )
    issues.extend(edge_summary_issues)
    issues.extend(node_degree_issues)

    if len(edge_summary_rows) != 6:
        issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} should contain exactly 6 rows")
    if len(node_degree_rows) != 65039:
        issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} should contain exactly 65039 rows")

    expected_edge_counts = {
        (
            "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl",
            "src-hust-obc",
            "HAS_HUST_OBC_OCR_LABEL_CANDIDATE",
        ): ("1781", "1781", "1781"),
        (
            "corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl",
            "src-hust-obc",
            "HAS_HUST_OBC_SOURCE_CATEGORY",
        ): ("1781", "1588", "1781"),
        (
            "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
            "src-obimd",
            "OBIMD_SUBCHARACTER_HAS_GLYPH_CODEPOINT",
        ): ("41686", "2747", "41686"),
        (
            "corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl",
            "src-obimd",
            "OBIMD_SUBCHARACTER_OF_MAIN_CHARACTER",
        ): ("2747", "2747", "1730"),
        (
            "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl",
            "src-evobc",
            "EVOBC_CATEGORY_HAS_ERA_CODE",
        ): ("26378", "13712", "6"),
        (
            "corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl",
            "src-evobc",
            "EVOBC_CATEGORY_HAS_SOURCE_CODE",
        ): ("25301", "13712", "8"),
    }
    observed_edge_counts = {}
    total_edge_count = 0
    for row in edge_summary_rows:
        key = (row.get("graph_file", ""), row.get("source_id", ""), row.get("edge_type", ""))
        observed_edge_counts[key] = (
            row.get("edge_count", ""),
            row.get("unique_source_node_count", ""),
            row.get("unique_target_node_count", ""),
        )
        edge_count = row.get("edge_count", "")
        if edge_count.isdigit():
            total_edge_count += int(edge_count)
        else:
            issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} edge_count not numeric: {key}")
        if row.get("generated_from") != "relationship_graph_jsonl":
            issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} generated_from changed: {key}")
        if row.get("updated_at") != "2026-06-04":
            issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} updated_at changed: {key}")
        if not row.get("review_status_counts", "").startswith("reviewed:"):
            issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} review status not reviewed-only: {key}")
        if not row.get("confidence_level_counts", "").startswith("high:"):
            issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} confidence not high-only: {key}")
    if observed_edge_counts != expected_edge_counts:
        issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} edge count summary changed")
    if total_edge_count != 99674:
        issues.append(f"{RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY} total edge count should be 99674")

    total_out_degree = 0
    total_in_degree = 0
    for row in node_degree_rows:
        node_id = row.get("node_id", "")
        if row.get("generated_from") != "relationship_graph_jsonl":
            issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} generated_from changed: {node_id}")
        if row.get("updated_at") != "2026-06-04":
            issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} updated_at changed: {node_id}")
        out_degree = row.get("out_degree", "")
        in_degree = row.get("in_degree", "")
        total_degree = row.get("total_degree", "")
        if not out_degree.isdigit() or not in_degree.isdigit() or not total_degree.isdigit():
            issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} non-numeric degree: {node_id}")
            continue
        out_value = int(out_degree)
        in_value = int(in_degree)
        total_value = int(total_degree)
        if total_value != out_value + in_value:
            issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} total degree mismatch: {node_id}")
        total_out_degree += out_value
        total_in_degree += in_value
    if total_out_degree != 99674:
        issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} total out-degree should be 99674")
    if total_in_degree != 99674:
        issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} total in-degree should be 99674")

    if node_degree_rows:
        expected_first = {
            "node_degree_row_id": "graph-node-degree-000001",
            "node_id": "evobc-code-008",
            "total_degree": "10158",
            "out_degree": "0",
            "in_degree": "10158",
            "incoming_edge_type_counts": "EVOBC_CATEGORY_HAS_SOURCE_CODE:10158",
            "source_ids": "src-evobc",
        }
        for key, value in expected_first.items():
            if node_degree_rows[0].get(key) != value:
                issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} first row {key} changed")
        expected_last = {
            "node_degree_row_id": "graph-node-degree-065039",
            "node_id": "obs-cand-001588",
            "total_degree": "1",
            "out_degree": "1",
            "in_degree": "0",
            "outgoing_edge_type_counts": "HAS_HUST_OBC_SOURCE_CATEGORY:1",
            "source_ids": "src-hust-obc",
        }
        for key, value in expected_last.items():
            if node_degree_rows[-1].get(key) != value:
                issues.append(f"{RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY} last row {key} changed")

    return issues


def check_ai_context_packs(root: Path) -> list[str]:
    issues: list[str] = []
    path = root / AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK
    try:
        context_pack = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} invalid JSON: {exc.msg}"]

    if context_pack.get("context_pack_id") != "ai-context-relationship-graph-001":
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} context_pack_id changed")
    if context_pack.get("status") != "reviewed_metadata_only":
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} status must stay reviewed_metadata_only")
    if context_pack.get("updated_at") != "2026-06-04":
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} updated_at changed")
    generated_from = context_pack.get("generated_from", [])
    if generated_from != [
        RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY,
        RELATIONSHIP_GRAPH_NODE_DEGREE_SUMMARY,
    ]:
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} generated_from changed")

    coverage = context_pack.get("coverage", {})
    expected_coverage = {
        "graph_file_count": 3,
        "source_count": 3,
        "edge_type_count": 6,
        "total_edge_count": 99674,
        "node_count": 65039,
        "top_node_limit": 20,
    }
    for key, value in expected_coverage.items():
        if coverage.get(key) != value:
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} coverage {key} changed")
    expected_graph_files = [
        HUST_OBC_CANDIDATE_GRAPH_EDGES,
        OBIMD_COMPONENT_GRAPH_EDGES,
        EVOBC_EVOLUTION_GRAPH_EDGES,
    ]
    if coverage.get("graph_files") != expected_graph_files:
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} graph file list changed")

    source_summaries = context_pack.get("source_summaries", [])
    if not isinstance(source_summaries, list) or len(source_summaries) != 3:
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} must contain 3 source summaries")
    else:
        edge_counts_by_source = {
            row.get("source_id"): row.get("edge_count")
            for row in source_summaries
        }
        if edge_counts_by_source != {
            "src-evobc": 51679,
            "src-hust-obc": 3562,
            "src-obimd": 44433,
        }:
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} source edge counts changed")

    top_nodes = context_pack.get("top_degree_nodes", [])
    if not isinstance(top_nodes, list) or len(top_nodes) != 20:
        issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} must contain 20 top nodes")
    else:
        first_node = top_nodes[0]
        if first_node.get("node_id") != "evobc-code-008":
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} first top node changed")
        if first_node.get("total_degree") != 10158:
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} first top node degree changed")
        if first_node.get("incoming_edge_type_counts") != "EVOBC_CATEGORY_HAS_SOURCE_CODE:10158":
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} first top node edge count changed")

    rules = " ".join(context_pack.get("agent_use_rules", []))
    rules_zh = " ".join(context_pack.get("agent_use_rules_zh", []))
    for required_snippet in [
        "routing and coverage summary",
        "Open the cited CSV/JSONL source rows",
        "Do not present OCR labels",
    ]:
        if required_snippet not in rules:
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} missing agent rule: {required_snippet}")
    for required_snippet in [
        "只作为检索路由",
        "必须打开被引用的 CSV/JSONL 来源行",
        "不得把 OCR 标签",
    ]:
        if required_snippet not in rules_zh:
            issues.append(f"{AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK} missing Chinese agent rule: {required_snippet}")

    return issues


def _parse_compact_counts(value: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not value:
        return counts
    for part in value.split(";"):
        if not part:
            continue
        if ":" not in part:
            counts[part] = -1
            continue
        key, raw_count = part.rsplit(":", 1)
        if not raw_count.isdigit():
            counts[key] = -1
            continue
        counts[key] = int(raw_count)
    return counts


def check_source_registers(root: Path) -> list[str]:
    issues: list[str] = []
    prefix_rows, prefix_issues = _read_csv_rows(root / EXTERNAL_SOURCE_PREFIXES)
    source_rows, source_issues = _read_csv_rows(root / SOURCE_INDEX)
    inventory_rows, inventory_issues = _read_csv_rows(root / SOURCE_INVENTORY)
    manifest_rows, manifest_issues = _read_csv_rows(root / SOURCE_DOWNLOAD_MANIFEST)
    field_map_rows, field_map_issues = _read_csv_rows(root / SOURCE_FIELD_MAP)
    package_file_rows, package_file_issues = _read_csv_rows(root / SOURCE_PACKAGE_FILE_MANIFEST)
    metadata_profile_rows, metadata_profile_issues = _read_csv_rows(root / DOWNLOADED_METADATA_PROFILE)
    core_access_rows, core_access_issues = _read_csv_rows(root / CORE_INSTITUTIONAL_ACCESS_PROFILE)
    obm_abbreviation_rows, obm_abbreviation_issues = _read_csv_rows(root / OBM_ABBREVIATION_STAGING)
    hust_validation_rows, hust_validation_issues = _read_csv_rows(
        root / HUST_OBC_VALIDATION_CLASS_STAGING
    )
    hust_label_crosswalk_rows, hust_label_crosswalk_issues = _read_csv_rows(
        root / HUST_OBC_VALIDATION_LABEL_CROSSWALK
    )
    hust_source_category_rows, hust_source_category_issues = _read_csv_rows(
        root / HUST_OBC_SOURCE_CATEGORY_STAGING
    )
    hust_promotion_queue_rows, hust_promotion_queue_issues = _read_csv_rows(
        root / HUST_OBC_OBS_CHAR_PROMOTION_QUEUE
    )
    hust_bucket_summary_rows, hust_bucket_summary_issues = _read_csv_rows(
        root / HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY
    )
    obimd_main_rows, obimd_main_issues = _read_csv_rows(root / OBIMD_MAIN_CHARACTER_STAGING)
    obimd_subchar_main_rows, obimd_subchar_main_issues = _read_csv_rows(
        root / OBIMD_SUBCHARACTER_MAIN_STAGING
    )
    obimd_subchar_glyph_rows, obimd_subchar_glyph_issues = _read_csv_rows(
        root / OBIMD_SUBCHARACTER_GLYPH_STAGING
    )
    evobc_category_rows, evobc_category_issues = _read_csv_rows(
        root / EVOBC_EVOLUTION_CATEGORY_STAGING
    )
    evobc_codebook_rows, evobc_codebook_issues = _read_csv_rows(
        root / EVOBC_ERA_SOURCE_CODEBOOK_STAGING
    )
    cambridge_crosswalk_rows, cambridge_crosswalk_issues = _read_csv_rows(
        root / CAMBRIDGE_HOPKINS_CROSSWALK_STAGING
    )
    cambridge_summary_rows, cambridge_summary_issues = _read_csv_rows(
        root / CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY
    )
    collection_provenance_rows, collection_provenance_issues = _read_csv_rows(
        root / COLLECTION_PROVENANCE_STAGING
    )
    ihp_museum_object_rows, ihp_museum_object_issues = _read_csv_rows(
        root / IHP_MUSEUM_OBJECT_STAGING
    )
    log_rows, log_issues = _read_csv_rows(root / SOURCE_DOWNLOAD_LOG)
    large_rows, large_issues = _read_csv_rows(root / LARGE_SOURCE_REGISTER)
    issues.extend(
        prefix_issues
        + source_issues
        + inventory_issues
        + manifest_issues
        + field_map_issues
        + package_file_issues
        + metadata_profile_issues
        + core_access_issues
        + obm_abbreviation_issues
        + hust_validation_issues
        + hust_label_crosswalk_issues
        + hust_source_category_issues
        + hust_promotion_queue_issues
        + hust_bucket_summary_issues
        + obimd_main_issues
        + obimd_subchar_main_issues
        + obimd_subchar_glyph_issues
        + evobc_category_issues
        + evobc_codebook_issues
        + cambridge_crosswalk_issues
        + cambridge_summary_issues
        + collection_provenance_issues
        + ihp_museum_object_issues
        + log_issues
        + large_issues
    )

    source_ids = {row.get("source_id", "") for row in source_rows}
    prefix_values = [row.get("prefix", "") for row in prefix_rows]
    duplicate_prefixes = sorted(
        prefix for prefix in set(prefix_values) if prefix and prefix_values.count(prefix) > 1
    )
    for prefix in duplicate_prefixes:
        issues.append(f"{EXTERNAL_SOURCE_PREFIXES} duplicate prefix: {prefix}")
    for prefix in sorted(REQUIRED_EXTERNAL_PREFIXES - set(prefix_values)):
        issues.append(f"{EXTERNAL_SOURCE_PREFIXES} missing required staging prefix: {prefix}")
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

    field_map_sources = {row.get("source_id", "") for row in field_map_rows}
    for source_id in sorted(field_map_sources - source_ids):
        issues.append(f"{SOURCE_FIELD_MAP} references unknown source_id: {source_id}")
    field_map_download_ids = {row.get("evidence_download_id", "") for row in field_map_rows}
    for download_id in sorted(field_map_download_ids - log_ids):
        issues.append(f"{SOURCE_FIELD_MAP} references missing download log id: {download_id}")
    reviewed_field_maps = [
        row for row in field_map_rows if row.get("review_status") == "reviewed_metadata_only"
    ]
    if len(reviewed_field_maps) < 20:
        issues.append(f"{SOURCE_FIELD_MAP} should contain at least 20 reviewed metadata field maps")

    large_source_ids = {row.get("source_package_id", "") for row in large_rows}
    for row in package_file_rows:
        source_id = row.get("source_id", "")
        package_id = row.get("source_package_id", "")
        download_id = row.get("download_id", "")
        file_size = row.get("file_size_bytes", "")
        commit_policy = row.get("commit_policy", "")
        if source_id not in source_ids:
            issues.append(f"{SOURCE_PACKAGE_FILE_MANIFEST} references unknown source_id: {source_id}")
        if package_id not in large_source_ids:
            issues.append(f"{SOURCE_PACKAGE_FILE_MANIFEST} references unknown source_package_id: {package_id}")
        if download_id and download_id not in log_ids:
            issues.append(f"{SOURCE_PACKAGE_FILE_MANIFEST} references missing download log id: {download_id}")
        if file_size and file_size.isdigit() and int(file_size) >= HARD_FILE_LIMIT_BYTES:
            if commit_policy != "do_not_commit_regular_git":
                issues.append(
                    f"{SOURCE_PACKAGE_FILE_MANIFEST} large file must be do_not_commit_regular_git: "
                    f"{row.get('package_file_id', '')}"
                )
    if len(package_file_rows) < 10:
        issues.append(f"{SOURCE_PACKAGE_FILE_MANIFEST} should contain at least 10 package file rows")

    metadata_profile_sources = {row.get("source_id", "") for row in metadata_profile_rows}
    for source_id in sorted(metadata_profile_sources - source_ids):
        issues.append(f"{DOWNLOADED_METADATA_PROFILE} references unknown source_id: {source_id}")
    for row in metadata_profile_rows:
        download_id = row.get("evidence_download_id", "")
        if download_id and download_id not in log_ids:
            issues.append(f"{DOWNLOADED_METADATA_PROFILE} references missing download log id: {download_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(
                f"{DOWNLOADED_METADATA_PROFILE} profile row not reviewed_metadata_only: "
                f"{row.get('profile_id', '')}"
            )
    if len(metadata_profile_rows) < 15:
        issues.append(f"{DOWNLOADED_METADATA_PROFILE} should contain at least 15 metadata profile rows")

    core_access_sources = {row.get("source_id", "") for row in core_access_rows}
    expected_core_access_sources = {
        "src-xiaoxuetang-jiaguwen",
        "src-xiaoxuetang-obm",
        "src-ihp-oracle-rubbings",
    }
    missing_core_access_sources = sorted(expected_core_access_sources - core_access_sources)
    for source_id in missing_core_access_sources:
        issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} missing core source: {source_id}")
    for row in core_access_rows:
        profile_id = row.get("profile_id", "")
        source_id = row.get("source_id", "")
        download_id = row.get("evidence_download_id", "")
        if not profile_id.startswith("source-access-"):
            issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} profile ID must use source-access-*: {profile_id}")
        if source_id not in source_ids:
            issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} references unknown source_id: {source_id}")
        if download_id not in log_ids:
            issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} references missing download log id: {download_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} row not reviewed_metadata_only: {profile_id}")
        if not row.get("official_url", "").startswith("https://"):
            issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} official_url must be HTTPS: {profile_id}")
    if len(core_access_rows) < 15:
        issues.append(f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} should contain at least 15 access profile rows")
    core_access_text = " ".join(" ".join(row.values()) for row in core_access_rows)
    for required_snippet in [
        "character_heads=2548",
        "glyph_forms=24701",
        "jiaguwen_bian_primary_basis",
        "heji_range=1-41956",
        "old_catalog_book_abbrev_count=90",
        "holding_abbrev_count=211",
        "old_catalog_book_abbrev_rows_staged=90",
        "holding_abbrev_rows_staged=211",
        "digitized_searchable_records=21556",
        "collection_number_cross_reference",
        "site_policy_required",
    ]:
        if required_snippet not in core_access_text:
            issues.append(
                f"{CORE_INSTITUTIONAL_ACCESS_PROFILE} missing expected access fact: "
                f"{required_snippet}"
            )

    if len(obm_abbreviation_rows) != 301:
        issues.append(f"{OBM_ABBREVIATION_STAGING} should contain exactly 301 abbreviation rows")
    obm_abbreviation_counts: dict[str, int] = {}
    obm_abbreviation_ids: set[str] = set()
    expected_obm_download_ids = {
        "old_catalog_book_abbreviation": "dl-xxt-obm-appendix01",
        "holding_abbreviation": "dl-xxt-obm-appendix02",
    }
    for row in obm_abbreviation_rows:
        row_id = row.get("abbrev_row_id", "")
        kind = row.get("abbreviation_kind", "")
        download_id = row.get("evidence_download_id", "")
        if not row_id.startswith(("obm-oldcat-abbrev-", "obm-holding-abbrev-")):
            issues.append(f"{OBM_ABBREVIATION_STAGING} row ID has wrong prefix: {row_id}")
        if row_id in obm_abbreviation_ids:
            issues.append(f"{OBM_ABBREVIATION_STAGING} duplicate row ID: {row_id}")
        obm_abbreviation_ids.add(row_id)
        obm_abbreviation_counts[kind] = obm_abbreviation_counts.get(kind, 0) + 1
        if row.get("source_id") != "src-xiaoxuetang-obm":
            issues.append(f"{OBM_ABBREVIATION_STAGING} row must reference src-xiaoxuetang-obm: {row_id}")
        if download_id != expected_obm_download_ids.get(kind, ""):
            issues.append(f"{OBM_ABBREVIATION_STAGING} row has wrong appendix download id: {row_id}")
        if download_id not in log_ids:
            issues.append(f"{OBM_ABBREVIATION_STAGING} references missing download log id: {download_id}")
        if row.get("rights_status") != "metadata_only_until_verified":
            issues.append(f"{OBM_ABBREVIATION_STAGING} row must stay metadata_only_until_verified: {row_id}")
        if row.get("project_import_status") != "abbreviation_metadata_not_promoted":
            issues.append(f"{OBM_ABBREVIATION_STAGING} row must stay abbreviation_metadata_not_promoted: {row_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{OBM_ABBREVIATION_STAGING} row not reviewed_metadata_only: {row_id}")
        if not row.get("browser_verified_url", "").startswith("https://xiaoxue.iis.sinica.edu.tw/obm/Home/Appendix"):
            issues.append(f"{OBM_ABBREVIATION_STAGING} row must cite official OBM appendix URL: {row_id}")
        if not row.get("source_abbreviation", "") or not row.get("source_label", ""):
            issues.append(f"{OBM_ABBREVIATION_STAGING} row missing abbreviation or label: {row_id}")
    expected_obm_counts = {
        "old_catalog_book_abbreviation": 90,
        "holding_abbreviation": 211,
    }
    if obm_abbreviation_rows and obm_abbreviation_counts != expected_obm_counts:
        issues.append(f"{OBM_ABBREVIATION_STAGING} abbreviation kind counts changed")

    if len(hust_validation_rows) != 1588:
        issues.append(
            f"{HUST_OBC_VALIDATION_CLASS_STAGING} should contain exactly 1588 candidate rows"
        )
    validation_class_ids: set[int] = set()
    for row in hust_validation_rows:
        candidate_class_id = row.get("candidate_class_id", "")
        if not candidate_class_id.startswith("obs-cand-"):
            issues.append(
                f"{HUST_OBC_VALIDATION_CLASS_STAGING} candidate ID must use obs-cand-*: "
                f"{candidate_class_id}"
            )
        if row.get("source_id") != "src-hust-obc":
            issues.append(
                f"{HUST_OBC_VALIDATION_CLASS_STAGING} row must reference src-hust-obc: "
                f"{candidate_class_id}"
            )
        if row.get("evidence_download_id") != "dl-hust-obc-validation-label":
            issues.append(
                f"{HUST_OBC_VALIDATION_CLASS_STAGING} row must cite dl-hust-obc-validation-label: "
                f"{candidate_class_id}"
            )
        if row.get("project_import_status") != "dataset_candidate_not_promoted":
            issues.append(
                f"{HUST_OBC_VALIDATION_CLASS_STAGING} row must stay dataset_candidate_not_promoted: "
                f"{candidate_class_id}"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(
                f"{HUST_OBC_VALIDATION_CLASS_STAGING} row not reviewed_metadata_only: "
                f"{candidate_class_id}"
            )
        validation_id = row.get("validation_class_id", "")
        if not validation_id.isdigit():
            issues.append(
                f"{HUST_OBC_VALIDATION_CLASS_STAGING} validation_class_id not numeric: "
                f"{candidate_class_id}"
            )
        else:
            validation_class_ids.add(int(validation_id))
    if validation_class_ids and validation_class_ids != set(range(1588)):
        issues.append(
            f"{HUST_OBC_VALIDATION_CLASS_STAGING} validation_class_id range must be 0..1587"
        )

    if len(hust_label_crosswalk_rows) != 1588:
        issues.append(
            f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} should contain exactly 1588 label rows"
        )
    label_crosswalk_ids: set[str] = set()
    label_crosswalk_candidate_ids: set[str] = set()
    label_crosswalk_validation_ids: set[int] = set()
    multi_component_label_count = 0
    for row in hust_label_crosswalk_rows:
        crosswalk_id = row.get("candidate_label_crosswalk_id", "")
        candidate_id = row.get("candidate_class_id", "")
        if not crosswalk_id.startswith("hust-obc-label-xwalk-"):
            issues.append(
                f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row ID must use "
                f"hust-obc-label-xwalk-*: {crosswalk_id}"
            )
        if crosswalk_id in label_crosswalk_ids:
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} duplicate row ID: {crosswalk_id}")
        label_crosswalk_ids.add(crosswalk_id)
        label_crosswalk_candidate_ids.add(candidate_id)
        if row.get("source_id") != "src-hust-obc":
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row must reference src-hust-obc: {crosswalk_id}")
        if row.get("evidence_download_id_validation") != "dl-hust-obc-validation-label":
            issues.append(
                f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row must cite "
                f"dl-hust-obc-validation-label: {crosswalk_id}"
            )
        if row.get("evidence_download_id_id_to_chinese") != "dl-hust-obc-ocr-id-to-chinese":
            issues.append(
                f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row must cite "
                f"dl-hust-obc-ocr-id-to-chinese: {crosswalk_id}"
            )
        if row.get("evidence_download_id_validation", "") not in log_ids:
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} validation download id missing in log")
        if row.get("evidence_download_id_id_to_chinese", "") not in log_ids:
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} ID_to_Chinese download id missing in log")
        source_category_id = row.get("source_category_id", "")
        padded_ids = row.get("source_category_id_padded", "").split(";")
        category_parts = source_category_id.split("_") if source_category_id else []
        if len(category_parts) != len(padded_ids):
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} padded ID count mismatch: {crosswalk_id}")
        for category_part, padded_id in zip(category_parts, padded_ids):
            if padded_id != category_part.zfill(5):
                issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} padded ID mismatch: {crosswalk_id}")
        label = row.get("source_modern_label_candidate", "")
        label_codepoints = row.get("source_modern_label_codepoints", "")
        if not label or not label_codepoints:
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} missing label or codepoints: {crosswalk_id}")
        expected_codepoints = ";".join(f"U+{ord(character):04X}" for character in label)
        if label_codepoints != expected_codepoints:
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} codepoint sequence mismatch: {crosswalk_id}")
        component_count = row.get("label_component_count", "")
        if not component_count.isdigit():
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} label_component_count not numeric: {crosswalk_id}")
        elif int(component_count) != len(label):
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} component count mismatch: {crosswalk_id}")
        if row.get("has_multi_component_label") == "true":
            multi_component_label_count += 1
        elif row.get("has_multi_component_label") != "false":
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} invalid multi-component flag: {crosswalk_id}")
        validation_id = row.get("validation_class_id", "")
        if validation_id.isdigit():
            label_crosswalk_validation_ids.add(int(validation_id))
        else:
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} validation_class_id not numeric: {crosswalk_id}")
        if row.get("project_import_status") != "dataset_label_candidate_not_promoted":
            issues.append(
                f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row must stay "
                f"dataset_label_candidate_not_promoted: {crosswalk_id}"
            )
        if row.get("rights_status") != "source_marked_risk_noted":
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row must stay source_marked_risk_noted: {crosswalk_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} row not reviewed_metadata_only: {crosswalk_id}")
    if hust_label_crosswalk_rows and label_crosswalk_validation_ids != set(range(1588)):
        issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} validation_class_id range must be 0..1587")
    if hust_label_crosswalk_rows and multi_component_label_count != 173:
        issues.append(f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} multi-component label count must be 173")
    hust_validation_candidate_ids = {row.get("candidate_class_id", "") for row in hust_validation_rows}
    if hust_label_crosswalk_rows and label_crosswalk_candidate_ids != hust_validation_candidate_ids:
        issues.append(
            f"{HUST_OBC_VALIDATION_LABEL_CROSSWALK} candidate_class_id set must match "
            f"{HUST_OBC_VALIDATION_CLASS_STAGING}"
        )

    if len(hust_source_category_rows) != 1781:
        issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} should contain exactly 1781 source-category rows")
    source_category_ids: set[int] = set()
    source_category_candidate_ids: set[str] = set()
    source_category_multi_count = 0
    for row in hust_source_category_rows:
        row_id = row.get("source_category_row_id", "")
        category_id = row.get("source_category_id", "")
        padded_id = row.get("source_category_id_padded", "")
        if not row_id.startswith("hust-obc-src-cat-"):
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row ID must use hust-obc-src-cat-*: {row_id}")
        if not category_id.isdigit():
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} source_category_id not numeric: {row_id}")
            category_value = -1
        else:
            category_value = int(category_id)
            source_category_ids.add(category_value)
            if row_id != f"hust-obc-src-cat-{category_value:04d}":
                issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row ID does not match source_category_id: {row_id}")
        if padded_id != category_id.zfill(5):
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} padded ID mismatch: {row_id}")
        if row.get("source_id") != "src-hust-obc":
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row must reference src-hust-obc: {row_id}")
        if row.get("evidence_download_id_validation") != "dl-hust-obc-validation-label":
            issues.append(
                f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row must cite dl-hust-obc-validation-label: {row_id}"
            )
        if row.get("evidence_download_id_id_to_chinese") != "dl-hust-obc-ocr-id-to-chinese":
            issues.append(
                f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row must cite dl-hust-obc-ocr-id-to-chinese: {row_id}"
            )
        if row.get("evidence_download_id_validation", "") not in log_ids:
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} validation download id missing in log")
        if row.get("evidence_download_id_id_to_chinese", "") not in log_ids:
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} ID_to_Chinese download id missing in log")
        label = row.get("source_modern_label_candidate", "")
        if len(label) != 1:
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} source label must be exactly one character: {row_id}")
        expected_codepoint = f"U+{ord(label):04X}" if label else ""
        if row.get("source_modern_label_codepoint", "") != expected_codepoint:
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} codepoint mismatch: {row_id}")
        candidate_id = row.get("linked_candidate_class_id", "")
        source_category_candidate_ids.add(candidate_id)
        if candidate_id not in hust_validation_candidate_ids:
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} linked candidate class missing: {row_id}")
        crosswalk_id = row.get("linked_label_crosswalk_id", "")
        if crosswalk_id not in label_crosswalk_ids:
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} linked label crosswalk missing: {row_id}")
        if row.get("is_part_of_multi_category_class") == "true":
            source_category_multi_count += 1
        elif row.get("is_part_of_multi_category_class") != "false":
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} invalid multi-category flag: {row_id}")
        if row.get("project_import_status") != "dataset_source_category_not_promoted":
            issues.append(
                f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row must stay dataset_source_category_not_promoted: {row_id}"
            )
        if row.get("rights_status") != "source_marked_risk_noted":
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row must stay source_marked_risk_noted: {row_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} row not reviewed_metadata_only: {row_id}")
    if hust_source_category_rows and source_category_ids != set(range(1, 1782)):
        issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} source_category_id range must be 1..1781")
    if hust_source_category_rows and source_category_multi_count != 366:
        issues.append(f"{HUST_OBC_SOURCE_CATEGORY_STAGING} multi-category member count must be 366")
    if hust_source_category_rows and not hust_validation_candidate_ids.issubset(source_category_candidate_ids):
        issues.append(
            f"{HUST_OBC_SOURCE_CATEGORY_STAGING} must link back to every HUST validation candidate class"
        )

    if len(hust_promotion_queue_rows) != 1588:
        issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} should contain exactly 1588 rows")
    queue_candidate_ids: set[str] = set()
    queue_ids: set[str] = set()
    queue_suggested_ids: set[str] = set()
    queue_multi_component_count = 0
    all_character_index_rows, all_character_index_issues = _read_csv_rows(
        root / "corpus/001_oracle-characters/000_character-registers/001_all-oracle-characters-index.csv"
    )
    issues.extend(all_character_index_issues)
    if all_character_index_rows:
        issues.append(
            "001_all-oracle-characters-index.csv must stay empty while HUST promotion queue is unreviewed"
        )
    source_category_row_ids = {row.get("source_category_row_id", "") for row in hust_source_category_rows}
    for index, row in enumerate(hust_promotion_queue_rows, start=1):
        queue_id = row.get("promotion_queue_id", "")
        expected_queue_id = f"hust-obc-obs-char-promo-{index:06d}"
        if queue_id != expected_queue_id:
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} queue ID sequence changed: {queue_id}")
        queue_ids.add(queue_id)
        suggested_id = row.get("suggested_oracle_character_id", "")
        if suggested_id != f"obs-char-{index:06d}":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} suggested obs-char ID changed: {queue_id}")
        if suggested_id in queue_suggested_ids:
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} duplicate suggested obs-char ID: {suggested_id}")
        queue_suggested_ids.add(suggested_id)
        candidate_id = row.get("candidate_class_id", "")
        queue_candidate_ids.add(candidate_id)
        if candidate_id not in hust_validation_candidate_ids:
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} references unknown candidate: {candidate_id}")
        if row.get("source_id") != "src-hust-obc":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} row must reference src-hust-obc: {queue_id}")
        if row.get("candidate_label_crosswalk_id", "") not in label_crosswalk_ids:
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} crosswalk link missing: {queue_id}")
        for source_category_row_id in row.get("source_category_row_ids", "").split(";"):
            if source_category_row_id and source_category_row_id not in source_category_row_ids:
                issues.append(
                    f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} source category row missing: "
                    f"{source_category_row_id}"
                )
        member_count = row.get("source_category_member_count", "")
        member_ids = [value for value in row.get("source_category_row_ids", "").split(";") if value]
        if not member_count.isdigit() or int(member_count) != len(member_ids):
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} member count mismatch: {queue_id}")
        component_count = row.get("label_component_count", "")
        label = row.get("source_modern_label_candidate", "")
        if not component_count.isdigit() or int(component_count) != len(label):
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} label component count mismatch: {queue_id}")
        if row.get("has_multi_component_label") == "true":
            queue_multi_component_count += 1
        elif row.get("has_multi_component_label") != "false":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} invalid multi-component flag: {queue_id}")
        if row.get("suggested_decipherment_status") != "unknown_until_cross_source_review":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} must keep unknown suggested status: {queue_id}")
        if row.get("assignment_status") != "reserved_candidate_not_assigned":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} must stay reserved_candidate_not_assigned: {queue_id}")
        if row.get("promotion_status") != "needs_cross_source_review":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} must stay needs_cross_source_review: {queue_id}")
        if row.get("rights_status") != "source_marked_risk_noted":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} row must stay source_marked_risk_noted: {queue_id}")
        if row.get("review_status") != "needs_review":
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} row must stay needs_review: {queue_id}")
        if "not assigned" not in row.get("caution", ""):
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} caution must preserve not-assigned warning: {queue_id}")
    if hust_promotion_queue_rows and queue_candidate_ids != hust_validation_candidate_ids:
        issues.append(
            f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} candidate_class_id set must match "
            f"{HUST_OBC_VALIDATION_CLASS_STAGING}"
        )
    if hust_promotion_queue_rows and queue_suggested_ids != {
        f"obs-char-{index:06d}" for index in range(1, 1589)
    }:
        issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} suggested obs-char range must be 000001..001588")
    if hust_promotion_queue_rows and queue_multi_component_count != 173:
        issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} multi-component label count must be 173")
    if hust_promotion_queue_rows:
        first_queue_row = hust_promotion_queue_rows[0]
        last_queue_row = hust_promotion_queue_rows[-1]
        if first_queue_row.get("suggested_bucket_directory") != (
            "001_000001-000100_obs-char-bucket_oracle-characters"
        ):
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} first bucket changed")
        if last_queue_row.get("suggested_bucket_directory") != (
            "016_001501-001600_obs-char-bucket_oracle-characters"
        ):
            issues.append(f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE} last bucket changed")

    bucket_manifest_queue_ids: set[str] = set()
    bucket_manifest_rows_by_directory: dict[str, list[dict[str, str]]] = {}
    for bucket_number, bucket_directory in enumerate(
        hust_obc_promotion_bucket_directories(),
        start=1,
    ):
        manifest_relative_path = (
            "corpus/001_oracle-characters/"
            f"{bucket_directory}/{HUST_OBC_PROMOTION_BUCKET_MANIFEST_FILENAME}"
        )
        bucket_rows, bucket_issues = _read_csv_rows(root / manifest_relative_path)
        issues.extend(bucket_issues)
        bucket_manifest_rows_by_directory[bucket_directory] = bucket_rows
        bucket_start = (bucket_number - 1) * 100 + 1
        bucket_end = min(bucket_start + 99, 1588)
        expected_count = bucket_end - bucket_start + 1
        if len(bucket_rows) != expected_count:
            issues.append(
                f"{manifest_relative_path} should contain exactly {expected_count} rows"
            )
        for bucket_row_index, row in enumerate(bucket_rows, start=1):
            global_index = bucket_start + bucket_row_index - 1
            queue_id = row.get("promotion_queue_id", "")
            expected_queue_id = f"hust-obc-obs-char-promo-{global_index:06d}"
            if queue_id != expected_queue_id:
                issues.append(f"{manifest_relative_path} queue ID sequence changed: {queue_id}")
            bucket_manifest_queue_ids.add(queue_id)
            expected_bucket_row_id = (
                f"hust-obc-bucket-{bucket_number:03d}-row-{bucket_row_index:03d}"
            )
            if row.get("bucket_manifest_row_id", "") != expected_bucket_row_id:
                issues.append(
                    f"{manifest_relative_path} bucket row ID changed: "
                    f"{row.get('bucket_manifest_row_id', '')}"
                )
            if row.get("suggested_oracle_character_id", "") != f"obs-char-{global_index:06d}":
                issues.append(f"{manifest_relative_path} suggested obs-char ID changed: {queue_id}")
            if row.get("suggested_bucket_directory", "") != bucket_directory:
                issues.append(f"{manifest_relative_path} bucket directory mismatch: {queue_id}")
            if row.get("source_id") != "src-hust-obc":
                issues.append(f"{manifest_relative_path} row must reference src-hust-obc: {queue_id}")
            if row.get("suggested_decipherment_status") != "unknown_until_cross_source_review":
                issues.append(f"{manifest_relative_path} must keep unknown suggested status: {queue_id}")
            if row.get("assignment_status") != "reserved_candidate_not_assigned":
                issues.append(f"{manifest_relative_path} must stay reserved_candidate_not_assigned: {queue_id}")
            if row.get("promotion_status") != "needs_cross_source_review":
                issues.append(f"{manifest_relative_path} must stay needs_cross_source_review: {queue_id}")
            if row.get("rights_status") != "source_marked_risk_noted":
                issues.append(f"{manifest_relative_path} row must stay source_marked_risk_noted: {queue_id}")
            if row.get("review_status") != "needs_review":
                issues.append(f"{manifest_relative_path} row must stay needs_review: {queue_id}")
            if "not assigned" not in row.get("caution", ""):
                issues.append(f"{manifest_relative_path} caution must preserve not-assigned warning: {queue_id}")
    if hust_promotion_queue_rows and bucket_manifest_queue_ids != queue_ids:
        issues.append("HUST-OBC bucket manifests must cover the full promotion queue exactly once")

    if len(hust_bucket_summary_rows) != 16:
        issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} should contain exactly 16 rows")
    summary_bucket_directories: set[str] = set()
    total_summary_rows = 0
    total_summary_multi_component = 0
    total_summary_source_category_rows = 0
    for bucket_number, row in enumerate(hust_bucket_summary_rows, start=1):
        bucket_directory = row.get("bucket_directory", "")
        summary_bucket_directories.add(bucket_directory)
        bucket_rows = bucket_manifest_rows_by_directory.get(bucket_directory, [])
        expected_summary_id = f"hust-obc-bucket-summary-{bucket_number:03d}"
        if row.get("bucket_summary_id", "") != expected_summary_id:
            issues.append(
                f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} summary ID changed: "
                f"{row.get('bucket_summary_id', '')}"
            )
        if row.get("bucket_number", "") != f"{bucket_number:03d}":
            issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} bucket number changed")
        expected_bucket_directory = hust_obc_promotion_bucket_directories()[bucket_number - 1]
        if bucket_directory != expected_bucket_directory:
            issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} bucket directory changed")
        expected_manifest_path = (
            "corpus/001_oracle-characters/"
            f"{bucket_directory}/{HUST_OBC_PROMOTION_BUCKET_MANIFEST_FILENAME}"
        )
        if row.get("manifest_path", "") != expected_manifest_path:
            issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} manifest path changed")
        if not bucket_rows:
            continue
        expected_row_count = len(bucket_rows)
        expected_multi_component = sum(
            1 for bucket_row in bucket_rows if bucket_row.get("has_multi_component_label") == "true"
        )
        expected_single_component = sum(
            1 for bucket_row in bucket_rows if bucket_row.get("has_multi_component_label") == "false"
        )
        expected_multi_source_category = sum(
            1
            for bucket_row in bucket_rows
            if bucket_row.get("source_category_member_count", "").isdigit()
            and int(bucket_row["source_category_member_count"]) > 1
        )
        expected_source_category_rows = sum(
            int(bucket_row["source_category_member_count"])
            for bucket_row in bucket_rows
            if bucket_row.get("source_category_member_count", "").isdigit()
        )
        expected_values = {
            "suggested_oracle_character_id_start": bucket_rows[0].get("suggested_oracle_character_id", ""),
            "suggested_oracle_character_id_end": bucket_rows[-1].get("suggested_oracle_character_id", ""),
            "promotion_queue_id_start": bucket_rows[0].get("promotion_queue_id", ""),
            "promotion_queue_id_end": bucket_rows[-1].get("promotion_queue_id", ""),
            "candidate_class_id_start": bucket_rows[0].get("candidate_class_id", ""),
            "candidate_class_id_end": bucket_rows[-1].get("candidate_class_id", ""),
            "row_count": str(expected_row_count),
            "single_component_label_count": str(expected_single_component),
            "multi_component_label_count": str(expected_multi_component),
            "multi_source_category_candidate_count": str(expected_multi_source_category),
            "source_category_row_count": str(expected_source_category_rows),
            "source_id_set": "src-hust-obc",
            "assignment_status_set": "reserved_candidate_not_assigned",
            "promotion_status_set": "needs_cross_source_review",
            "suggested_decipherment_status_set": "unknown_until_cross_source_review",
            "rights_status_set": "source_marked_risk_noted",
            "review_status_set": "needs_review",
            "required_next_review": "compare_xiaoxuetang_obm_obimd_evobc_and_primary_inscription_context",
            "ai_agent_batch_action": (
                "review_manifest_rows_against_xiaoxuetang_obm_obimd_evobc_and_primary_inscription_context"
            ),
        }
        for field, expected_value in expected_values.items():
            if row.get(field, "") != expected_value:
                issues.append(
                    f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} {field} mismatch: "
                    f"{row.get('bucket_summary_id', '')}"
                )
        if "not assigned" not in row.get("caution", ""):
            issues.append(
                f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} caution must preserve not-assigned warning: "
                f"{row.get('bucket_summary_id', '')}"
            )
        if not row.get("row_count", "").isdigit():
            issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} row_count not numeric")
        else:
            total_summary_rows += int(row["row_count"])
        if row.get("multi_component_label_count", "").isdigit():
            total_summary_multi_component += int(row["multi_component_label_count"])
        if row.get("source_category_row_count", "").isdigit():
            total_summary_source_category_rows += int(row["source_category_row_count"])
    if hust_bucket_summary_rows and summary_bucket_directories != set(hust_obc_promotion_bucket_directories()):
        issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} bucket set changed")
    if hust_bucket_summary_rows and total_summary_rows != 1588:
        issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} total row count must be 1588")
    if hust_bucket_summary_rows and total_summary_multi_component != 173:
        issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} multi-component total must be 173")
    if hust_bucket_summary_rows and total_summary_source_category_rows != 1781:
        issues.append(f"{HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY} source-category total must be 1781")

    if len(obimd_main_rows) != 3936:
        issues.append(f"{OBIMD_MAIN_CHARACTER_STAGING} should contain exactly 3936 candidate rows")
    obimd_uids: set[str] = set()
    empty_transcription_count = 0
    for row in obimd_main_rows:
        candidate_id = row.get("candidate_main_character_id", "")
        if not candidate_id.startswith("obimd-main-cand-"):
            issues.append(
                f"{OBIMD_MAIN_CHARACTER_STAGING} candidate ID must use obimd-main-cand-*: "
                f"{candidate_id}"
            )
        if row.get("source_id") != "src-obimd":
            issues.append(f"{OBIMD_MAIN_CHARACTER_STAGING} row must reference src-obimd: {candidate_id}")
        if row.get("evidence_download_id") != "dl-obimd-main-character-json":
            issues.append(
                f"{OBIMD_MAIN_CHARACTER_STAGING} row must cite dl-obimd-main-character-json: "
                f"{candidate_id}"
            )
        source_uid = row.get("source_uid", "")
        if not source_uid:
            issues.append(f"{OBIMD_MAIN_CHARACTER_STAGING} row missing source_uid: {candidate_id}")
        elif source_uid in obimd_uids:
            issues.append(f"{OBIMD_MAIN_CHARACTER_STAGING} duplicate source_uid: {source_uid}")
        obimd_uids.add(source_uid)
        if row.get("project_import_status") != "dataset_candidate_not_promoted":
            issues.append(
                f"{OBIMD_MAIN_CHARACTER_STAGING} row must stay dataset_candidate_not_promoted: "
                f"{candidate_id}"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{OBIMD_MAIN_CHARACTER_STAGING} row not reviewed_metadata_only: {candidate_id}")
        if row.get("has_empty_transcription") == "true":
            empty_transcription_count += 1
    if obimd_main_rows and empty_transcription_count != 1159:
        issues.append(
            f"{OBIMD_MAIN_CHARACTER_STAGING} should preserve 1159 empty transcription rows"
        )

    if len(obimd_subchar_main_rows) != 2747:
        issues.append(
            f"{OBIMD_SUBCHARACTER_MAIN_STAGING} should contain exactly 2747 relationship rows"
        )
    obimd_subchar_uids: set[str] = set()
    obimd_main_relation_uids: set[str] = set()
    for row in obimd_subchar_main_rows:
        candidate_id = row.get("candidate_subcharacter_id", "")
        if not candidate_id.startswith("obimd-sub-cand-"):
            issues.append(
                f"{OBIMD_SUBCHARACTER_MAIN_STAGING} candidate ID must use obimd-sub-cand-*: "
                f"{candidate_id}"
            )
        if row.get("source_id") != "src-obimd":
            issues.append(f"{OBIMD_SUBCHARACTER_MAIN_STAGING} row must reference src-obimd: {candidate_id}")
        if row.get("evidence_download_id") != "dl-obimd-subchar-main-mapping":
            issues.append(
                f"{OBIMD_SUBCHARACTER_MAIN_STAGING} row must cite dl-obimd-subchar-main-mapping: "
                f"{candidate_id}"
            )
        sub_uid = row.get("source_subcharacter_uid", "")
        main_uid = row.get("source_main_character_uid", "")
        if not sub_uid or not main_uid:
            issues.append(f"{OBIMD_SUBCHARACTER_MAIN_STAGING} row missing UID: {candidate_id}")
        if sub_uid in obimd_subchar_uids:
            issues.append(f"{OBIMD_SUBCHARACTER_MAIN_STAGING} duplicate subcharacter UID: {sub_uid}")
        obimd_subchar_uids.add(sub_uid)
        obimd_main_relation_uids.add(main_uid)
        if row.get("project_import_status") != "dataset_candidate_not_promoted":
            issues.append(
                f"{OBIMD_SUBCHARACTER_MAIN_STAGING} row must stay dataset_candidate_not_promoted: "
                f"{candidate_id}"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{OBIMD_SUBCHARACTER_MAIN_STAGING} row not reviewed_metadata_only: {candidate_id}")
    if obimd_subchar_main_rows and len(obimd_main_relation_uids) != 1730:
        issues.append(f"{OBIMD_SUBCHARACTER_MAIN_STAGING} should preserve 1730 unique main UIDs")

    if len(obimd_subchar_glyph_rows) != 41686:
        issues.append(
            f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} should contain exactly 41686 glyph rows"
        )
    glyph_codepoints: set[str] = set()
    glyph_sub_uids: set[str] = set()
    for row in obimd_subchar_glyph_rows:
        candidate_id = row.get("candidate_glyph_link_id", "")
        if not candidate_id.startswith("obimd-glyph-link-"):
            issues.append(
                f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} candidate ID must use obimd-glyph-link-*: "
                f"{candidate_id}"
            )
        if row.get("source_id") != "src-obimd":
            issues.append(f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} row must reference src-obimd: {candidate_id}")
        if row.get("evidence_download_id") != "dl-obimd-subchar-glyph-mapping":
            issues.append(
                f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} row must cite dl-obimd-subchar-glyph-mapping: "
                f"{candidate_id}"
            )
        sub_uid = row.get("source_subcharacter_uid", "")
        glyph = row.get("glyph_codepoint", "")
        if not sub_uid or not glyph:
            issues.append(f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} row missing UID or glyph: {candidate_id}")
        glyph_sub_uids.add(sub_uid)
        if glyph in glyph_codepoints:
            issues.append(f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} duplicate glyph codepoint: {candidate_id}")
        glyph_codepoints.add(glyph)
        if not row.get("glyph_codepoint_uplus", ""):
            issues.append(f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} row missing U+ form: {candidate_id}")
        if row.get("project_import_status") != "dataset_candidate_not_promoted":
            issues.append(
                f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} row must stay dataset_candidate_not_promoted: "
                f"{candidate_id}"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} row not reviewed_metadata_only: {candidate_id}")
    if glyph_sub_uids and glyph_sub_uids != obimd_subchar_uids:
        issues.append(
            f"{OBIMD_SUBCHARACTER_GLYPH_STAGING} subcharacter UID set must match "
            f"{OBIMD_SUBCHARACTER_MAIN_STAGING}"
        )

    expected_evobc_era_counts = {
        "0": 75681,
        "1": 47314,
        "2": 13434,
        "3": 9131,
        "4": 80042,
        "5": 3568,
    }
    expected_evobc_source_counts = {
        "0": 1633,
        "1": 106010,
        "2": 17600,
        "3": 21681,
        "4": 9131,
        "5": 32794,
        "6": 30645,
        "7": 9676,
    }
    if len(evobc_category_rows) != 13714:
        issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} should contain exactly 13714 rows")
    evobc_source_category_ids: set[str] = set()
    evobc_total_images = 0
    evobc_zero_image_rows = 0
    evobc_era_counts: dict[str, int] = {}
    evobc_source_counts: dict[str, int] = {}
    for row in evobc_category_rows:
        candidate_id = row.get("candidate_evolution_category_id", "")
        if not candidate_id.startswith("evobc-evo-cat-"):
            issues.append(
                f"{EVOBC_EVOLUTION_CATEGORY_STAGING} candidate ID must use "
                f"evobc-evo-cat-*: {candidate_id}"
            )
        if row.get("source_id") != "src-evobc":
            issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} row must reference src-evobc: {candidate_id}")
        if row.get("evidence_download_id_key_value") != "dl-evobc-key-value-json":
            issues.append(
                f"{EVOBC_EVOLUTION_CATEGORY_STAGING} row must cite dl-evobc-key-value-json: "
                f"{candidate_id}"
            )
        if row.get("evidence_download_id_list") != "dl-evobc-list-json":
            issues.append(
                f"{EVOBC_EVOLUTION_CATEGORY_STAGING} row must cite dl-evobc-list-json: "
                f"{candidate_id}"
            )
        source_category_id = row.get("source_category_id", "")
        if len(source_category_id) != 5 or not source_category_id.isdigit():
            issues.append(
                f"{EVOBC_EVOLUTION_CATEGORY_STAGING} source_category_id must be five digits: "
                f"{candidate_id}"
            )
        if source_category_id in evobc_source_category_ids:
            issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} duplicate source_category_id: {source_category_id}")
        evobc_source_category_ids.add(source_category_id)
        image_count = row.get("image_reference_count", "")
        if not image_count.isdigit():
            issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} image_reference_count not numeric: {candidate_id}")
            image_count_value = 0
        else:
            image_count_value = int(image_count)
        evobc_total_images += image_count_value
        if image_count_value == 0:
            evobc_zero_image_rows += 1
        era_counts = _parse_compact_counts(row.get("era_code_counts", ""))
        source_counts = _parse_compact_counts(row.get("source_code_counts", ""))
        if any(count < 0 for count in era_counts.values()):
            issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} malformed era counts: {candidate_id}")
        if any(count < 0 for count in source_counts.values()):
            issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} malformed source counts: {candidate_id}")
        for key, value in era_counts.items():
            evobc_era_counts[key] = evobc_era_counts.get(key, 0) + value
        for key, value in source_counts.items():
            evobc_source_counts[key] = evobc_source_counts.get(key, 0) + value
        expected_flags = {
            "has_oracle_bone_refs": "0",
            "has_bronze_refs": "1",
            "has_seal_refs": "2",
            "has_spring_autumn_refs": "3",
            "has_warring_states_refs": "4",
            "has_clerical_refs": "5",
        }
        for flag, era_code in expected_flags.items():
            if row.get(flag) != str(era_counts.get(era_code, 0) > 0).lower():
                issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} {flag} mismatch: {candidate_id}")
        if row.get("project_import_status") != "dataset_candidate_not_promoted":
            issues.append(
                f"{EVOBC_EVOLUTION_CATEGORY_STAGING} row must stay dataset_candidate_not_promoted: "
                f"{candidate_id}"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} row not reviewed_metadata_only: {candidate_id}")
    if evobc_category_rows and evobc_source_category_ids != {f"{index:05d}" for index in range(1, 13715)}:
        issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} source_category_id range must be 00001..13714")
    if evobc_category_rows and evobc_total_images != 229170:
        issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} image-reference total must be 229170")
    if evobc_category_rows and evobc_zero_image_rows != 2:
        issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} zero-image category count must be 2")
    if evobc_category_rows and evobc_era_counts != expected_evobc_era_counts:
        issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} era-code totals changed")
    if evobc_category_rows and evobc_source_counts != expected_evobc_source_counts:
        issues.append(f"{EVOBC_EVOLUTION_CATEGORY_STAGING} source-code totals changed")

    if len(evobc_codebook_rows) != 14:
        issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} should contain exactly 14 rows")
    era_codebook_counts: dict[str, int] = {}
    source_codebook_counts: dict[str, int] = {}
    for row in evobc_codebook_rows:
        codebook_row_id = row.get("codebook_row_id", "")
        if not codebook_row_id.startswith("evobc-code-"):
            issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} row ID must use evobc-code-*: {codebook_row_id}")
        if row.get("source_id") != "src-evobc":
            issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} row must reference src-evobc: {codebook_row_id}")
        if row.get("evidence_download_id") != "dl-evobc-list-json":
            issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} row must cite dl-evobc-list-json: {codebook_row_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} row not reviewed_metadata_only: {codebook_row_id}")
        image_count = row.get("image_reference_count", "")
        if not image_count.isdigit():
            issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} image_reference_count not numeric: {codebook_row_id}")
            continue
        if row.get("code_type") == "era":
            era_codebook_counts[row.get("code_value", "")] = int(image_count)
        elif row.get("code_type") == "source":
            source_codebook_counts[row.get("code_value", "")] = int(image_count)
        else:
            issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} unknown code_type: {codebook_row_id}")
    if evobc_codebook_rows and era_codebook_counts != expected_evobc_era_counts:
        issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} era-code totals changed")
    if evobc_codebook_rows and source_codebook_counts != expected_evobc_source_counts:
        issues.append(f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING} source-code totals changed")

    if len(cambridge_crosswalk_rows) != 612:
        issues.append(
            f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} should contain exactly 612 crosswalk rows"
        )
    missing_cul_count = 0
    missing_chalfant_count = 0
    missing_heji_count = 0
    for row in cambridge_crosswalk_rows:
        candidate_id = row.get("candidate_inscription_crosswalk_id", "")
        if not candidate_id.startswith("cam-hopkins-crosswalk-"):
            issues.append(
                f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} candidate ID must use "
                f"cam-hopkins-crosswalk-*: {candidate_id}"
            )
        if row.get("source_id") != "src-cambridge-hopkins":
            issues.append(
                f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} row must reference src-cambridge-hopkins: "
                f"{candidate_id}"
            )
        if row.get("evidence_download_id") != "dl-cambridge-hopkins-finding-list":
            issues.append(
                f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} row must cite "
                f"dl-cambridge-hopkins-finding-list: {candidate_id}"
            )
        if row.get("project_import_status") != "dataset_candidate_not_promoted":
            issues.append(
                f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} row must stay "
                f"dataset_candidate_not_promoted: {candidate_id}"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(
                f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} row not reviewed_metadata_only: "
                f"{candidate_id}"
            )
        y_ref = row.get("yingguo_ref_id", "")
        if not y_ref:
            issues.append(f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} row missing y ref: {candidate_id}")
        if row.get("has_missing_cul_ref") == "true":
            missing_cul_count += 1
        if row.get("has_missing_chalfant_ref") == "true":
            missing_chalfant_count += 1
        if row.get("has_missing_heji_ref") == "true":
            missing_heji_count += 1
    if cambridge_crosswalk_rows and (missing_cul_count, missing_chalfant_count, missing_heji_count) != (6, 171, 316):
        issues.append(
            f"{CAMBRIDGE_HOPKINS_CROSSWALK_STAGING} missing-reference counts changed"
        )

    if len(cambridge_summary_rows) != 25:
        issues.append(f"{CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY} should contain exactly 25 rows")
    cambridge_group_rows = [
        row for row in cambridge_summary_rows if row.get("summary_kind") == "classified_table_group"
    ]
    if len(cambridge_group_rows) != 20:
        issues.append(f"{CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY} should contain 20 group rows")
    grand_total_rows = [
        row for row in cambridge_summary_rows
        if row.get("summary_kind") == "classified_table_grand_total"
    ]
    if not grand_total_rows or grand_total_rows[0].get("total_count") != "609":
        issues.append(f"{CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY} grand total must be 609")
    for row in cambridge_summary_rows:
        if row.get("source_id") != "src-cambridge-hopkins":
            issues.append(f"{CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY} row must reference src-cambridge-hopkins")
        if row.get("evidence_download_id") != "dl-cambridge-hopkins-finding-list":
            issues.append(
                f"{CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY} row must cite "
                f"dl-cambridge-hopkins-finding-list"
            )
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY} row not reviewed_metadata_only")

    if len(collection_provenance_rows) != 4:
        issues.append(f"{COLLECTION_PROVENANCE_STAGING} should contain exactly 4 rows")
    expected_collection_sources = {
        "src-tsinghua-oracle-bones",
        "src-ihp-oracle-rubbings",
        "src-ihp-museum-oracle-bones",
        "src-cambridge-hopkins",
    }
    collection_sources = {row.get("source_id", "") for row in collection_provenance_rows}
    if collection_sources != expected_collection_sources:
        issues.append(f"{COLLECTION_PROVENANCE_STAGING} source set changed")
    for row in collection_provenance_rows:
        source_id = row.get("source_id", "")
        download_id = row.get("evidence_download_id", "")
        if source_id not in source_ids:
            issues.append(f"{COLLECTION_PROVENANCE_STAGING} references unknown source_id: {source_id}")
        if download_id not in log_ids:
            issues.append(f"{COLLECTION_PROVENANCE_STAGING} references missing download log id: {download_id}")
        if row.get("rights_status") != "metadata_only_until_verified":
            issues.append(f"{COLLECTION_PROVENANCE_STAGING} row must stay metadata_only_until_verified")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{COLLECTION_PROVENANCE_STAGING} row not reviewed_metadata_only")
    collection_text = " ".join(
        " ".join(row.values()) for row in collection_provenance_rows
    )
    for required_snippet in [
        "over 1,750",
        "1,495",
        "over 40,000",
        "21,556",
        "more than 25,000",
        "grand total 609",
        "50 bones",
    ]:
        if required_snippet not in collection_text:
            issues.append(
                f"{COLLECTION_PROVENANCE_STAGING} missing expected collection fact: "
                f"{required_snippet}"
            )

    if len(ihp_museum_object_rows) != 52:
        issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} should contain exactly 52 rows")
    ihp_item_ids: set[str] = set()
    for row in ihp_museum_object_rows:
        candidate_id = row.get("candidate_collection_object_id", "")
        if not candidate_id.startswith("ihp-mus-obj-"):
            issues.append(
                f"{IHP_MUSEUM_OBJECT_STAGING} candidate ID must use ihp-mus-obj-*: "
                f"{candidate_id}"
            )
        if row.get("source_id") != "src-ihp-museum-oracle-bones":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} row must reference src-ihp-museum-oracle-bones")
        if row.get("evidence_download_id") != "dl-ihp-museum-oracle-bones":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} row must cite dl-ihp-museum-oracle-bones")
        source_item_id = row.get("source_collection_item_id", "")
        if not source_item_id.isdigit():
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} source_collection_item_id not numeric: {candidate_id}")
        if source_item_id in ihp_item_ids:
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} duplicate source_collection_item_id: {source_item_id}")
        ihp_item_ids.add(source_item_id)
        if not row.get("object_page_url", "").startswith(
            "https://museum.sinica.edu.tw/en/collection/32/item/"
        ):
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} object_page_url outside official item path")
        if not row.get("thumbnail_url", "").startswith(
            "https://museum.sinica.edu.tw/_upload/image/collection_item/thumbnail/"
        ):
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} thumbnail_url outside official thumbnail path")
        if row.get("thumbnail_download_status") != "not_downloaded_metadata_only":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} thumbnail must stay metadata-only")
        if row.get("project_import_status") != "object_metadata_not_promoted":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} row must stay object_metadata_not_promoted")
        if row.get("rights_status") != "metadata_only_until_verified":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} row must stay metadata_only_until_verified")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} row not reviewed_metadata_only")
    if ihp_museum_object_rows:
        first_row = ihp_museum_object_rows[0]
        last_row = ihp_museum_object_rows[-1]
        if first_row.get("source_collection_item_id") != "1212":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} first item ID changed")
        if first_row.get("catalog_reference_text") != "Jia Bian 3333+3361":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} first catalog reference changed")
        if last_row.get("source_collection_item_id") != "273":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} last item ID changed")
        if last_row.get("catalog_reference_text") != "Ping 0264":
            issues.append(f"{IHP_MUSEUM_OBJECT_STAGING} last catalog reference changed")

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
    issues.extend(check_relationship_graph_edges(root))
    issues.extend(check_relationship_graph_statistics(root))
    issues.extend(check_ai_context_packs(root))

    if issues:
        print("FAIL repository skeleton")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS repository skeleton")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
