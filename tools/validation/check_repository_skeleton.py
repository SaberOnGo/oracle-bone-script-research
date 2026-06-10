#!/usr/bin/env python3
"""Validate the repository skeleton for Oracle Bone Script Research."""

from __future__ import annotations

import sys
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


SIZE_LIMIT_BYTES = 30 * 1024 * 1024
HARD_FILE_LIMIT_BYTES = 40 * 1024 * 1024
SIZE_LIMIT_EXCEPTIONS = "project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv"
ASSET_SOURCE_INDEX = "project_registry/004_asset-source-and-rights-index/001_asset-source-index.csv"
ASSET_RIGHTS_REVIEW_LOG = "project_registry/004_asset-source-and-rights-index/002_asset-rights-review-log.csv"
ASSET_IMAGE_TECHNICAL_PROFILE = "project_registry/004_asset-source-and-rights-index/004_asset-image-technical-profile.csv"
ASSET_IMAGE_VISUAL_PROFILE = "project_registry/004_asset-source-and-rights-index/005_asset-image-visual-profile.csv"
EXTERNAL_SOURCE_PREFIXES = "project_registry/003_external-source-prefixes/003_external-source-prefixes.csv"
ASSET_ID_SOURCE_MAP = "project_registry/002_project-id-to-source-reference-map/003_asset-id-source-map.csv"
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
SOURCE_DOWNLOAD_STATUS_CODEBOOK = (
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "013_source-download-status-codebook.csv"
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
AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "004_ai-agent-hust-obc-bucket-review-route-pack.json"
)
AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)
AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "006_ai-agent-public-domain-asset-context-pack.json"
)
SOURCE_COVERAGE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "007_source-coverage-summary.csv"
)
AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "008_ai-agent-source-coverage-context-pack.json"
)
AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "009_ai-agent-source-route-review-queue.csv"
)
AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "010_ai-agent-source-route-review-result-scaffold.csv"
)
AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS = (
    "corpus/009_statistics-and-derived-features/"
    "011_ai-agent-source-route-review-results.csv"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "012_ai-agent-graph-source-cross-review-queue.csv"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "013_ai-agent-graph-source-cross-review-log-scaffold.csv"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "014_ai-agent-graph-source-cross-review-log-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS = (
    "corpus/009_statistics-and-derived-features/"
    "015_ai-agent-graph-source-cross-review-log-results.csv"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "016_ai-agent-graph-source-evidence-collection-task-queue.csv"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "018_ai-agent-graph-source-download-log-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "019_ai-agent-graph-source-package-manifest-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "020_ai-agent-graph-source-metadata-profile-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "021_ai-agent-graph-source-graph-edges-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "022_ai-agent-graph-source-staging-row-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "023_ai-agent-graph-source-counter-source-lookup-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "024_ai-agent-graph-source-rights-risk-review-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST = (
    "corpus/009_statistics-and-derived-features/"
    "025_ai-agent-graph-source-review-log-note-draft-manifest.csv"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK = (
    "corpus/009_statistics-and-derived-features/"
    "026_ai-agent-graph-source-evidence-collection-route-pack.json"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "027_ai-agent-graph-source-evidence-collection-result-scaffold.csv"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE = (
    "corpus/009_statistics-and-derived-features/"
    "028_ai-agent-graph-source-evidence-collection-review-queue.csv"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY = (
    "corpus/009_statistics-and-derived-features/"
    "029_ai-agent-graph-source-evidence-collection-review-route-summary.json"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN = (
    "corpus/009_statistics-and-derived-features/"
    "030_ai-agent-graph-source-evidence-collection-assignment-plan.json"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "031_ai-agent-graph-source-evidence-collection-wave-handoff-scaffold.json"
)
AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD = (
    "corpus/009_statistics-and-derived-features/"
    "032_ai-agent-graph-source-source-register-evidence-capture-scaffold.csv"
)
AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST = (
    "corpus/009_statistics-and-derived-features/"
    "033_ai-agent-graph-source-source-register-capture-review-checklist.csv"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_HUST_DRAFT = (
    "doc/public/user_research/002_cross-source-review-queues/hust-obc/"
    "001_hust-obc-evidence-request-000001_cross-source-review-log.md"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_EVOBC_DRAFT = (
    "doc/public/user_research/002_cross-source-review-queues/evobc/"
    "002_evobc-evo-cat-00001_cross-source-review-log.md"
)
AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_OBIMD_DRAFT = (
    "doc/public/user_research/002_cross-source-review-queues/obimd/"
    "003_obimd-sub-cand-000001_cross-source-review-log.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_SOURCE_REGISTER_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-001_source-register_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_SOURCE_REGISTER_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-010_source-register_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_SOURCE_REGISTER_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-019_source-register_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_DOWNLOAD_LOG_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-002_download-log_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_DOWNLOAD_LOG_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-011_download-log_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_DOWNLOAD_LOG_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-020_download-log_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_PACKAGE_MANIFEST_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-003_package-manifest_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_PACKAGE_MANIFEST_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-012_package-manifest_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_PACKAGE_MANIFEST_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-021_package-manifest_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_METADATA_PROFILE_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-004_metadata-profile_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_METADATA_PROFILE_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-013_metadata-profile_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_METADATA_PROFILE_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-022_metadata-profile_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_GRAPH_EDGES_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-005_graph-edges_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_GRAPH_EDGES_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-014_graph-edges_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_GRAPH_EDGES_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-023_graph-edges_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_STAGING_ROW_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-006_staging-row_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_STAGING_ROW_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-015_staging-row_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_STAGING_ROW_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-024_staging-row_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_COUNTER_SOURCE_LOOKUP_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-007_counter-source-lookup_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_COUNTER_SOURCE_LOOKUP_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-016_counter-source-lookup_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_COUNTER_SOURCE_LOOKUP_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-025_counter-source-lookup_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_RIGHTS_RISK_REVIEW_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-008_rights-risk-review_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_RIGHTS_RISK_REVIEW_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-017_rights-risk-review_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_RIGHTS_RISK_REVIEW_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-026_rights-risk-review_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_REVIEW_LOG_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/hust-obc/"
    "graph-source-evidence-task-009_review-log_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_REVIEW_LOG_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/evobc/"
    "graph-source-evidence-task-018_review-log_collection-note.md"
)
AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_REVIEW_LOG_DRAFT = (
    "doc/public/user_research/003_evidence-collection-tasks/obimd/"
    "graph-source-evidence-task-027_review-log_collection-note.md"
)
AI_AGENT_EVIDENCE_PACK_SCHEMA = (
    "schemas/006_ai-agent-evidence-pack-schema/"
    "ai-agent-evidence-pack.schema.json"
)
AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT = (
    "doc/public/user_research/001_ai-agent-evidence-packs/hust-obc/"
    "001_000001-000100_obs-char-bucket/"
    "001_obs-char-000001_hust-obc-cat-0001_evidence-pack-draft.json"
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
SMITHSONIAN_NMAA_OBJECT_STAGING = (
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "003_smithsonian-nmaa-oracle-bone-object-staging.csv"
)
PENN_MUSEUM_OBJECT_STAGING = (
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "004_penn-museum-oracle-bone-object-staging.csv"
)
METMUSEUM_OBJECT_STAGING = (
    "corpus/005_excavation-sites-periods-and-batches/000_collection-registers/"
    "005_metmuseum-oracle-bone-object-staging.csv"
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
    "src-metmuseum-oracle-bone",
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
    "met-obj",
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
    ASSET_SOURCE_INDEX,
    ASSET_RIGHTS_REVIEW_LOG,
    "project_registry/004_asset-source-and-rights-index/003_size-limit-exceptions.csv",
    ASSET_IMAGE_TECHNICAL_PROFILE,
    ASSET_IMAGE_VISUAL_PROFILE,
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
    "schemas/006_ai-agent-evidence-pack-schema/README.md",
    AI_AGENT_EVIDENCE_PACK_SCHEMA,
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
    SOURCE_DOWNLOAD_STATUS_CODEBOOK,
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
    AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK,
    AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
    AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK,
    SOURCE_COVERAGE_SUMMARY,
    AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK,
    AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE,
    AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD,
    AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD,
    AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD,
    AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_HUST_DRAFT,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_EVOBC_DRAFT,
    AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_OBIMD_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_SOURCE_REGISTER_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_SOURCE_REGISTER_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_SOURCE_REGISTER_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_DOWNLOAD_LOG_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_DOWNLOAD_LOG_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_DOWNLOAD_LOG_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_PACKAGE_MANIFEST_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_PACKAGE_MANIFEST_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_PACKAGE_MANIFEST_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_METADATA_PROFILE_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_METADATA_PROFILE_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_METADATA_PROFILE_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_GRAPH_EDGES_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_GRAPH_EDGES_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_GRAPH_EDGES_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_STAGING_ROW_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_STAGING_ROW_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_STAGING_ROW_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_COUNTER_SOURCE_LOOKUP_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_COUNTER_SOURCE_LOOKUP_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_COUNTER_SOURCE_LOOKUP_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_RIGHTS_RISK_REVIEW_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_RIGHTS_RISK_REVIEW_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_RIGHTS_RISK_REVIEW_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_REVIEW_LOG_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_REVIEW_LOG_DRAFT,
    AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_REVIEW_LOG_DRAFT,
    OBIMD_MAIN_CHARACTER_STAGING,
    OBIMD_SUBCHARACTER_MAIN_STAGING,
    OBIMD_SUBCHARACTER_GLYPH_STAGING,
    EVOBC_EVOLUTION_CATEGORY_STAGING,
    EVOBC_ERA_SOURCE_CODEBOOK_STAGING,
    CAMBRIDGE_HOPKINS_CROSSWALK_STAGING,
    CAMBRIDGE_HOPKINS_CLASSIFIED_SUMMARY,
    COLLECTION_PROVENANCE_STAGING,
    IHP_MUSEUM_OBJECT_STAGING,
    SMITHSONIAN_NMAA_OBJECT_STAGING,
    PENN_MUSEUM_OBJECT_STAGING,
    METMUSEUM_OBJECT_STAGING,
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/README.md",
    "corpus/005_excavation-sites-periods-and-batches/001_public-domain-object-image-assets/README.md",
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
    "tools/004_statistics-generation/build_asset_image_visual_profiles.py",
    "tools/004_statistics-generation/build_source_coverage_statistics.py",
    "tools/005_ai-context-pack-builder/build_relationship_graph_context_pack.py",
    "tools/005_ai-context-pack-builder/build_hust_obc_bucket_review_route_pack.py",
    "tools/005_ai-context-pack-builder/build_hust_obc_candidate_evidence_pack_request_queue.py",
    "tools/005_ai-context-pack-builder/build_hust_obc_evidence_pack_draft.py",
    "tools/005_ai-context-pack-builder/build_public_domain_asset_context_pack.py",
    "tools/005_ai-context-pack-builder/build_source_coverage_context_pack.py",
    "tools/005_ai-context-pack-builder/build_source_route_review_queue.py",
    "tools/005_ai-context-pack-builder/build_source_route_review_result_scaffold.py",
    "tools/005_ai-context-pack-builder/build_source_route_review_results.py",
    "tools/005_ai-context-pack-builder/build_graph_source_cross_review_queue.py",
    "tools/005_ai-context-pack-builder/build_graph_source_cross_review_log_scaffold.py",
    "tools/005_ai-context-pack-builder/build_graph_source_cross_review_log_drafts.py",
    "tools/005_ai-context-pack-builder/build_graph_source_cross_review_log_results.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_task_queue.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_note_drafts.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_route_pack.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_result_scaffold.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_review_queue.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_review_route_summary.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_assignment_plan.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_wave_handoff_scaffold.py",
    "tools/005_ai-context-pack-builder/build_graph_source_evidence_collection_source_register_capture_scaffold.py",
    "tools/005_ai-context-pack-builder/build_graph_source_source_register_capture_review_checklist.py",
    "tools/validation/check_repository_skeleton.py",
    "tools/validation/validate_ai_agent_evidence_packs.py",
    "tests/test_check_commit_messages.py",
    "tests/test_repository_skeleton.py",
    AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT,
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
    map_asset_ids = {row.get("project_id", "") for row in map_rows if row.get("record_type") == "museum_object_image"}
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


def check_source_coverage_statistics(root: Path) -> list[str]:
    issues: list[str] = []
    source_rows, source_issues = _read_csv_rows(root / SOURCE_INDEX)
    coverage_rows, coverage_issues = _read_csv_rows(root / SOURCE_COVERAGE_SUMMARY)
    issues.extend(source_issues)
    issues.extend(coverage_issues)

    if len(coverage_rows) != len(source_rows):
        issues.append(f"{SOURCE_COVERAGE_SUMMARY} row count must match source index")
    if len(coverage_rows) != 21:
        issues.append(f"{SOURCE_COVERAGE_SUMMARY} should contain exactly 21 rows")

    source_ids = {row.get("source_id", "") for row in source_rows}
    coverage_source_ids = {row.get("source_id", "") for row in coverage_rows}
    if coverage_source_ids != source_ids:
        issues.append(f"{SOURCE_COVERAGE_SUMMARY} source_id coverage changed")

    totals = Counter()
    status_counts = Counter()
    by_source_id = {}
    for row in coverage_rows:
        source_id = row.get("source_id", "")
        by_source_id[source_id] = row
        if row.get("generated_from") != (
            "source_registers;download_manifest;download_log;metadata_profiles;"
            "asset_source_index;relationship_graph_statistics;hust_obc_promotion_queue"
        ):
            issues.append(f"{SOURCE_COVERAGE_SUMMARY} generated_from changed: {source_id}")
        if row.get("updated_at") != "2026-06-10":
            issues.append(f"{SOURCE_COVERAGE_SUMMARY} updated_at changed: {source_id}")
        if "Coverage statistics only" not in row.get("caution", ""):
            issues.append(f"{SOURCE_COVERAGE_SUMMARY} caution changed: {source_id}")
        for field in [
            "download_manifest_count",
            "download_log_count",
            "downloaded_file_bytes",
            "metadata_profile_metric_count",
            "committed_asset_count",
            "committed_asset_bytes",
            "graph_edge_count",
            "graph_edge_type_count",
            "promotion_queue_candidate_count",
        ]:
            value = row.get(field, "")
            if not value.isdigit():
                issues.append(f"{SOURCE_COVERAGE_SUMMARY} non-numeric {field}: {source_id}")
            else:
                totals[field] += int(value)
        status_counts[row.get("coverage_status", "")] += 1

    expected_totals = {
        "download_manifest_count": 44,
        "download_log_count": 44,
        "downloaded_file_bytes": 37363373,
        "metadata_profile_metric_count": 48,
        "committed_asset_count": 3,
        "committed_asset_bytes": 4922128,
        "graph_edge_count": 99674,
        "promotion_queue_candidate_count": 1588,
    }
    for field, expected_value in expected_totals.items():
        if totals[field] != expected_value:
            issues.append(f"{SOURCE_COVERAGE_SUMMARY} total {field} changed")

    expected_status_counts = {
        "has_committed_public_asset_or_metadata": 2,
        "has_download_log_only": 12,
        "has_downloaded_metadata_profile": 4,
        "has_relationship_graph_derivatives": 3,
    }
    if dict(status_counts) != expected_status_counts:
        issues.append(f"{SOURCE_COVERAGE_SUMMARY} coverage status counts changed")

    expected_source_values = {
        "src-hust-obc": {
            "graph_edge_count": "3562",
            "graph_edge_type_count": "2",
            "promotion_queue_candidate_count": "1588",
            "coverage_status": "has_relationship_graph_derivatives",
        },
        "src-obimd": {
            "graph_edge_count": "44433",
            "graph_edge_type_count": "2",
            "coverage_status": "has_relationship_graph_derivatives",
        },
        "src-evobc": {
            "graph_edge_count": "51679",
            "graph_edge_type_count": "2",
            "coverage_status": "has_relationship_graph_derivatives",
        },
        "src-metmuseum-oracle-bone": {
            "committed_asset_count": "2",
            "committed_asset_bytes": "4288710",
            "asset_rights_status_counts": "public_domain_verified:2",
            "coverage_status": "has_committed_public_asset_or_metadata",
        },
        "src-smithsonian-nmaa-oracle-bone": {
            "committed_asset_count": "1",
            "committed_asset_bytes": "633418",
            "asset_rights_status_counts": "public_domain_verified:1",
            "coverage_status": "has_committed_public_asset_or_metadata",
        },
        "src-xiaoxuetang-jiaguwen": {
            "download_status_counts": "downloaded_access_restricted_page:2",
            "coverage_status": "has_download_log_only",
        },
    }
    for source_id, expected_values in expected_source_values.items():
        row = by_source_id.get(source_id)
        if not row:
            issues.append(f"{SOURCE_COVERAGE_SUMMARY} missing source row: {source_id}")
            continue
        for field, expected_value in expected_values.items():
            if row.get(field) != expected_value:
                issues.append(f"{SOURCE_COVERAGE_SUMMARY} {source_id} {field} changed")

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

    route_path = root / AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK
    try:
        route_pack = json.loads(route_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return issues + [f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} invalid JSON: {exc.msg}"]

    if route_pack.get("context_pack_id") != "ai-context-hust-obc-bucket-review-001":
        issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} context_pack_id changed")
    if route_pack.get("status") != "reviewed_metadata_only":
        issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} status must stay reviewed_metadata_only")
    if route_pack.get("updated_at") != "2026-06-04":
        issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} updated_at changed")
    if route_pack.get("generated_from") != [HUST_OBC_PROMOTION_BUCKET_REVIEW_SUMMARY]:
        issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} generated_from changed")

    route_coverage = route_pack.get("coverage", {})
    expected_route_coverage = {
        "bucket_count": 16,
        "candidate_count": 1588,
        "multi_component_label_count": 173,
        "source_category_row_count": 1781,
        "route_file_count_per_bucket": 5,
        "source_route_requirement_count": 6,
        "evidence_gap_type_count": 9,
    }
    for key, value in expected_route_coverage.items():
        if route_coverage.get(key) != value:
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} coverage {key} changed")
    source_route_requirements = route_pack.get("source_route_requirements", [])
    source_route_ids = {row.get("source_id", "") for row in source_route_requirements}
    expected_source_route_ids = {
        "src-hust-obc",
        "src-xiaoxuetang-jiaguwen",
        "src-xiaoxuetang-obm",
        "src-obimd",
        "src-evobc",
        "src-ihp-oracle-rubbings",
    }
    if source_route_ids != expected_source_route_ids:
        issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} source route set changed")
    bucket_routes = route_pack.get("bucket_routes", [])
    if not isinstance(bucket_routes, list) or len(bucket_routes) != 16:
        issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} must contain 16 bucket routes")
    else:
        first_route = bucket_routes[0]
        last_route = bucket_routes[-1]
        if first_route.get("bucket_summary_id") != "hust-obc-bucket-summary-001":
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} first bucket route changed")
        if first_route.get("candidate_count") != 100:
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} first bucket count changed")
        if first_route.get("assignment_status") != "reserved_candidate_not_assigned":
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} first bucket assignment status changed")
        first_route_files = first_route.get("route_files", [])
        for required_route_file in [
            HUST_OBC_CANDIDATE_GRAPH_EDGES,
            OBIMD_COMPONENT_GRAPH_EDGES,
            EVOBC_EVOLUTION_GRAPH_EDGES,
            SOURCE_INDEX,
        ]:
            if required_route_file not in first_route_files:
                issues.append(
                    f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} first route missing file: "
                    f"{required_route_file}"
                )
        if last_route.get("bucket_summary_id") != "hust-obc-bucket-summary-016":
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} last bucket route changed")
        if last_route.get("candidate_count") != 88:
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} last bucket count changed")
    route_rules = " ".join(route_pack.get("agent_use_rules", []))
    route_rules_zh = " ".join(route_pack.get("agent_use_rules_zh", []))
    for required_snippet in [
        "routing HUST-OBC bucket review",
        "Open the bucket manifest",
        "reserved candidates",
        "doc/public/user_research",
    ]:
        if required_snippet not in route_rules:
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} missing agent rule: {required_snippet}")
    for required_snippet in [
        "HUST-OBC 分桶复核",
        "必须打开 bucket manifest",
        "只是保留候选",
        "doc/public/user_research",
    ]:
        if required_snippet not in route_rules_zh:
            issues.append(f"{AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK} missing Chinese agent rule: {required_snippet}")

    request_rows, request_issues = _read_csv_rows(
        root / AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE
    )
    issues.extend(request_issues)
    if len(request_rows) != 1588:
        issues.append(
            f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} should contain exactly 1588 rows"
        )
    request_multi_component_count = 0
    request_bucket_numbers: set[str] = set()
    required_sections = {
        "character_or_unknown_glyph_id",
        "source_references_and_asset_metadata",
        "full_inscription_context",
        "neighboring_characters",
        "component_breakdown_and_variant_notes",
        "excavation_period_and_catalog_provenance",
        "bronze_seal_or_modern_comparanda",
        "supporting_evidence",
        "opposing_evidence",
        "open_questions_and_next_checks",
    }
    required_gap_types = {
        "source_provenance",
        "primary_inscription_context",
        "neighboring_characters",
        "component_breakdown",
        "variant_chain",
        "bronze_seal_modern_correspondence",
        "cooccurrence_distribution",
        "supporting_evidence",
        "opposing_evidence",
    }
    required_route_source_ids = {
        "src-hust-obc",
        "src-xiaoxuetang-jiaguwen",
        "src-xiaoxuetang-obm",
        "src-obimd",
        "src-evobc",
        "src-ihp-oracle-rubbings",
    }
    for index, row in enumerate(request_rows, start=1):
        request_id = row.get("evidence_request_id", "")
        if request_id != f"hust-obc-evidence-request-{index:06d}":
            issues.append(
                f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} request ID sequence changed: "
                f"{request_id}"
            )
        if row.get("route_pack_id") != "ai-context-hust-obc-bucket-review-001":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} route pack ID changed: {request_id}")
        if row.get("promotion_queue_id") != f"hust-obc-obs-char-promo-{index:06d}":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} promotion queue link changed: {request_id}")
        if row.get("suggested_oracle_character_id") != f"obs-char-{index:06d}":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} suggested obs-char changed: {request_id}")
        expected_bucket_number = f"{((index - 1) // 100) + 1:03d}"
        request_bucket_numbers.add(row.get("bucket_number", ""))
        if row.get("bucket_number") != expected_bucket_number:
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} bucket number changed: {request_id}")
        if row.get("bucket_summary_id") != f"hust-obc-bucket-summary-{int(expected_bucket_number):03d}":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} bucket summary link changed: {request_id}")
        draft_output_path = row.get("draft_output_path", "")
        if not draft_output_path.startswith("doc/public/user_research/001_ai-agent-evidence-packs/hust-obc/"):
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} draft path outside user_research: {request_id}")
        if draft_output_path.startswith("research/"):
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} draft path must not use research/: {request_id}")
        if not draft_output_path.endswith("_evidence-pack-draft.json"):
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} draft path suffix changed: {request_id}")
        if row.get("draft_status") != "not_started":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} draft status changed: {request_id}")
        if row.get("assignment_status") != "reserved_candidate_not_assigned":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} assignment status changed: {request_id}")
        if row.get("promotion_status") != "needs_cross_source_review":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} promotion status changed: {request_id}")
        if row.get("review_status") != "needs_evidence_pack":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} review status changed: {request_id}")
        if "not be treated as a decipherment result" not in row.get("caution", ""):
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} caution changed: {request_id}")
        if row.get("updated_at") != "2026-06-04":
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} updated_at changed: {request_id}")
        if row.get("has_multi_component_label") == "true":
            request_multi_component_count += 1
        route_files = set(filter(None, row.get("route_files", "").split(";")))
        for required_file in [
            HUST_OBC_CANDIDATE_GRAPH_EDGES,
            OBIMD_COMPONENT_GRAPH_EDGES,
            EVOBC_EVOLUTION_GRAPH_EDGES,
            SOURCE_INDEX,
        ]:
            if required_file not in route_files:
                issues.append(
                    f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} missing route file: "
                    f"{required_file}"
                )
        if set(filter(None, row.get("source_route_requirement_ids", "").split(";"))) != required_route_source_ids:
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} source route requirements changed: {request_id}")
        if set(filter(None, row.get("evidence_gap_types", "").split(";"))) != required_gap_types:
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} evidence gap types changed: {request_id}")
        if set(filter(None, row.get("required_evidence_pack_sections", "").split(";"))) != required_sections:
            issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} required sections changed: {request_id}")
    if request_rows and request_multi_component_count != 173:
        issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} multi-component total must be 173")
    if request_rows and request_bucket_numbers != {f"{index:03d}" for index in range(1, 17)}:
        issues.append(f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE} bucket set changed")

    try:
        evidence_pack_schema = json.loads(
            (root / AI_AGENT_EVIDENCE_PACK_SCHEMA).read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        return issues + [f"{AI_AGENT_EVIDENCE_PACK_SCHEMA} invalid JSON: {exc.msg}"]
    schema_required = set(evidence_pack_schema.get("required", []))
    expected_schema_required = required_sections | {
        "evidence_pack_id",
        "evidence_request_id",
        "status",
        "research_boundary",
        "assignment_status",
        "suggested_oracle_character_id",
        "candidate_class_id",
        "primary_external_ref_id",
        "draft_source_queue_path",
        "route_pack_id",
        "bucket_manifest_path",
        "route_files",
        "source_route_requirement_ids",
        "evidence_gap_types",
        "review_log",
        "caution",
        "updated_at",
    }
    if evidence_pack_schema.get("title") != "AI Agent Oracle Bone Script Evidence Pack":
        issues.append(f"{AI_AGENT_EVIDENCE_PACK_SCHEMA} title changed")
    if not expected_schema_required.issubset(schema_required):
        issues.append(f"{AI_AGENT_EVIDENCE_PACK_SCHEMA} missing required evidence-pack fields")
    schema_properties = evidence_pack_schema.get("properties", {})
    if schema_properties.get("research_boundary", {}).get("const") != "draft_not_scholarship":
        issues.append(f"{AI_AGENT_EVIDENCE_PACK_SCHEMA} research boundary const changed")
    if "reserved_candidate_not_assigned" not in schema_properties.get("assignment_status", {}).get("enum", []):
        issues.append(f"{AI_AGENT_EVIDENCE_PACK_SCHEMA} assignment status enum changed")

    try:
        sample_draft = json.loads(
            (root / AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT).read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        return issues + [f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} invalid JSON: {exc.msg}"]
    expected_sample_values = {
        "evidence_pack_id": "hust-obc-evidence-pack-000001",
        "evidence_request_id": "hust-obc-evidence-request-000001",
        "status": "draft",
        "research_boundary": "draft_not_scholarship",
        "assignment_status": "reserved_candidate_not_assigned",
        "suggested_oracle_character_id": "obs-char-000001",
        "candidate_class_id": "obs-cand-000001",
        "primary_external_ref_id": "hust-obc-cat-0001",
        "draft_source_queue_path": AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
        "route_pack_id": "ai-context-hust-obc-bucket-review-001",
        "updated_at": "2026-06-05",
    }
    for key, value in expected_sample_values.items():
        if sample_draft.get(key) != value:
            issues.append(f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} {key} changed")
    if str(AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT).startswith("research/"):
        issues.append(f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} must not be under research/")
    if "not a decipherment result" not in sample_draft.get("caution", ""):
        issues.append(f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} caution changed")
    for section in required_sections:
        value = sample_draft.get(section)
        if section == "open_questions_and_next_checks":
            if not isinstance(value, list) or not value:
                issues.append(f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} missing open questions")
            continue
        if not isinstance(value, dict) or value.get("status") != "not_collected":
            issues.append(f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} section not not_collected: {section}")
        elif value.get("items") != []:
            issues.append(f"{AI_AGENT_HUST_OBC_FIRST_EVIDENCE_PACK_DRAFT} section has prefilled items: {section}")

    asset_context_path = root / AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK
    try:
        asset_context_pack = json.loads(asset_context_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return issues + [f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} invalid JSON: {exc.msg}"]
    if asset_context_pack.get("context_pack_id") != "ai-context-public-domain-assets-001":
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} context_pack_id changed")
    if asset_context_pack.get("status") != "reviewed_metadata_only":
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} status must stay reviewed_metadata_only")
    if asset_context_pack.get("updated_at") != "2026-06-05":
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} updated_at changed")
    if asset_context_pack.get("generated_from") != [
        ASSET_SOURCE_INDEX,
        ASSET_RIGHTS_REVIEW_LOG,
        ASSET_IMAGE_TECHNICAL_PROFILE,
        ASSET_IMAGE_VISUAL_PROFILE,
    ]:
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} generated_from changed")
    asset_coverage = asset_context_pack.get("coverage", {})
    if asset_coverage.get("asset_count") != 3:
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} asset count changed")
    if asset_coverage.get("source_ids") != [
        "src-metmuseum-oracle-bone",
        "src-smithsonian-nmaa-oracle-bone",
    ]:
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} source IDs changed")
    if asset_coverage.get("rights_statuses") != ["public_domain_verified"]:
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} rights statuses changed")
    if asset_coverage.get("analysis_scopes") != [
        "image_technical_metadata_only",
        "visual_preprocessing_metadata_only",
    ]:
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} analysis scopes changed")
    asset_entries = asset_context_pack.get("assets", [])
    if not isinstance(asset_entries, list) or len(asset_entries) != 3:
        issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} must contain 3 assets")
    else:
        first_asset = asset_entries[0]
        second_asset = asset_entries[1]
        third_asset = asset_entries[2]
        if first_asset.get("asset_id") != "asset-000001":
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} first asset changed")
        if second_asset.get("asset_id") != "asset-000002":
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} second asset changed")
        if third_asset.get("asset_id") != "asset-000003":
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} third asset changed")
        if first_asset.get("primary_external_ref_id") != "met-obj-42045":
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} first external ref changed")
        if second_asset.get("primary_external_ref_id") != "met-obj-42022":
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} second external ref changed")
        if third_asset.get("primary_external_ref_id") != "si-nmaa-fsc-o-26":
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} third external ref changed")
        if first_asset.get("technical_profile", {}).get("checksum_sha256") != (
            "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df"
        ):
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} first checksum changed")
        if second_asset.get("technical_profile", {}).get("checksum_sha256") != (
            "61510f04c8d599e4e5f9bf50ebcb1cb2163ebd7243e4a125ce08e73fdadad8cd"
        ):
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} second checksum changed")
        if third_asset.get("technical_profile", {}).get("checksum_sha256") != (
            "e4152d2d680234decb8d4b04225c83a59955b69bc4d8b10eebe7a98d54259079"
        ):
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} third checksum changed")
        if first_asset.get("visual_profile", {}).get("foreground_pixel_count") != 154404:
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} first visual count changed")
        if second_asset.get("visual_profile", {}).get("foreground_pixel_count") != 1972665:
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} second visual count changed")
        if third_asset.get("visual_profile", {}).get("foreground_pixel_count") != 208710:
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} third visual count changed")
        first_caution = first_asset.get("visual_profile", {}).get("caution", "")
        if "not glyph segmentation" not in first_caution:
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} visual caution changed")
    asset_rules = " ".join(asset_context_pack.get("agent_use_rules", []))
    asset_rules_zh = " ".join(asset_context_pack.get("agent_use_rules_zh", []))
    for required_snippet in [
        "image-asset routing summary",
        "Open the cited asset index",
        "not glyph segmentation",
        "object-page, API, or IIIF manifest provenance",
    ]:
        if required_snippet not in asset_rules:
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} missing agent rule: {required_snippet}")
    for required_snippet in [
        "图像资产检索路由摘要",
        "必须打开被引用的资产索引",
        "不是字形切分",
        "对象页、API 或 IIIF manifest 来源追溯",
    ]:
        if required_snippet not in asset_rules_zh:
            issues.append(f"{AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK} missing Chinese agent rule: {required_snippet}")

    source_context_path = root / AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK
    try:
        source_context_pack = json.loads(source_context_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return issues + [f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} invalid JSON: {exc.msg}"]
    if source_context_pack.get("context_pack_id") != "ai-context-source-coverage-001":
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} context_pack_id changed")
    if source_context_pack.get("status") != "reviewed_metadata_only":
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} status must stay reviewed_metadata_only")
    if source_context_pack.get("updated_at") != "2026-06-10":
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} updated_at changed")
    if source_context_pack.get("generated_from") != [
        SOURCE_COVERAGE_SUMMARY,
        SOURCE_INDEX,
        SOURCE_DOWNLOAD_MANIFEST,
        SOURCE_DOWNLOAD_LOG,
        DOWNLOADED_METADATA_PROFILE,
        ASSET_SOURCE_INDEX,
        RELATIONSHIP_GRAPH_EDGE_TYPE_SUMMARY,
        HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
    ]:
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} generated_from changed")

    source_coverage = source_context_pack.get("coverage", {})
    expected_source_coverage = {
        "source_count": 21,
        "download_manifest_count": 44,
        "download_log_count": 44,
        "metadata_profile_metric_count": 48,
        "committed_asset_count": 3,
        "committed_asset_bytes": 4922128,
        "graph_edge_count": 99674,
        "promotion_queue_candidate_count": 1588,
    }
    for key, value in expected_source_coverage.items():
        if source_coverage.get(key) != value:
            issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} coverage {key} changed")
    if source_coverage.get("coverage_status_counts") != {
        "has_committed_public_asset_or_metadata": 2,
        "has_download_log_only": 12,
        "has_downloaded_metadata_profile": 4,
        "has_relationship_graph_derivatives": 3,
    }:
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} coverage status counts changed")
    if source_coverage.get("rights_status_counts") != {
        "licensed_for_repository": 1,
        "metadata_only_until_verified": 11,
        "public_domain_verified": 2,
        "source_marked_risk_noted": 7,
    }:
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} rights status counts changed")
    if source_coverage.get("authority_tier_counts") != {
        "core_institutional": 4,
        "institutional_database": 1,
        "institutional_portal": 1,
        "museum_collection": 2,
        "national_library": 1,
        "national_museum_collection": 1,
        "peer_reviewed_dataset": 4,
        "peer_reviewed_or_preprint_dataset": 1,
        "scholarly_commercial_platform": 1,
        "scholarly_platform": 1,
        "scholarly_project": 1,
        "university_library_collection": 2,
        "university_museum_collection": 1,
    }:
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} authority tier counts changed")

    source_entries = source_context_pack.get("source_routes", [])
    if not isinstance(source_entries, list) or len(source_entries) != 21:
        issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} must contain 21 source routes")
        source_entries_by_id = {}
    else:
        source_entries_by_id = {
            row.get("source_id", ""): row
            for row in source_entries
        }
        if set(source_entries_by_id) != {
            "src-british-museum-oracle-bone",
            "src-cambridge-hopkins",
            "src-evobc",
            "src-gbedobc",
            "src-hust-obc",
            "src-ihp-museum-oracle-bones",
            "src-ihp-oracle-rubbings",
            "src-metmuseum-oracle-bone",
            "src-nlc-oracle-world",
            "src-obid-ancientbooks",
            "src-obimd",
            "src-open-oracle",
            "src-oracle-mnist",
            "src-penn-museum-oracle-bone",
            "src-sinica-da-xiaoxuetang-site",
            "src-sinica-yinshang-oracle-vocabulary",
            "src-smithsonian-nmaa-oracle-bone",
            "src-tsinghua-oracle-bones",
            "src-xiaoxuetang-jiaguwen",
            "src-xiaoxuetang-obm",
            "src-yinqi-wenyuan",
        }:
            issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} source route IDs changed")
        expected_source_values = {
            "src-hust-obc": {
                "route": "open_graph_and_metadata_derivatives",
                "promotion_queue_candidate_count": 1588,
                "graph_edge_count": 3562,
            },
            "src-obimd": {
                "route": "open_graph_and_metadata_derivatives",
                "graph_edge_count": 44433,
            },
            "src-evobc": {
                "route": "open_graph_and_metadata_derivatives",
                "graph_edge_count": 51679,
            },
            "src-metmuseum-oracle-bone": {
                "route": "open_asset_and_rights_records",
                "committed_asset_count": 2,
            },
            "src-smithsonian-nmaa-oracle-bone": {
                "route": "open_asset_and_rights_records",
                "committed_asset_count": 1,
            },
            "src-xiaoxuetang-jiaguwen": {
                "route": "open_download_log_and_source_register",
                "download_status_counts": "downloaded_access_restricted_page:2",
            },
        }
        for source_id, expected_values in expected_source_values.items():
            entry = source_entries_by_id.get(source_id, {})
            if not entry:
                issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} missing source route: {source_id}")
                continue
            for key, value in expected_values.items():
                if entry.get(key) != value:
                    issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} {source_id} {key} changed")

    priority_routes = source_context_pack.get("priority_routes", {})
    expected_priority_ids = {
        "graph_derivative_sources": ["src-evobc", "src-hust-obc", "src-obimd"],
        "public_asset_sources": [
            "src-metmuseum-oracle-bone",
            "src-smithsonian-nmaa-oracle-bone",
        ],
        "candidate_queue_sources": ["src-hust-obc"],
        "access_limited_or_error_sources": [
            "src-british-museum-oracle-bone",
            "src-smithsonian-nmaa-oracle-bone",
            "src-xiaoxuetang-jiaguwen",
            "src-xiaoxuetang-obm",
        ],
    }
    for route_name, expected_ids in expected_priority_ids.items():
        route_entries = priority_routes.get(route_name, [])
        route_ids = [entry.get("source_id", "") for entry in route_entries]
        if route_ids != expected_ids:
            issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} priority route changed: {route_name}")

    source_rules = " ".join(source_context_pack.get("agent_use_rules", []))
    source_rules_zh = " ".join(source_context_pack.get("agent_use_rules_zh", []))
    for required_snippet in [
        "source-routing and coverage summary",
        "Open the cited source register",
        "dataset-derived rows",
        "Do not infer decipherment",
        "ignored temporary directories",
    ]:
        if required_snippet not in source_rules:
            issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} missing agent rule: {required_snippet}")
    for required_snippet in [
        "来源路由和覆盖范围摘要",
        "必须打开被引用的来源登记",
        "数据集派生记录",
        "不得仅凭覆盖数量",
        "已忽略临时目录",
    ]:
        if required_snippet not in source_rules_zh:
            issues.append(f"{AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK} missing Chinese agent rule: {required_snippet}")

    source_route_rows, source_route_issues = _read_csv_rows(root / AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE)
    issues.extend(source_route_issues)
    if len(source_route_rows) != 21:
        issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} should contain exactly 21 rows")
    expected_source_route_ids = [
        "src-hust-obc",
        "src-evobc",
        "src-obimd",
        "src-metmuseum-oracle-bone",
        "src-smithsonian-nmaa-oracle-bone",
        "src-british-museum-oracle-bone",
        "src-xiaoxuetang-jiaguwen",
        "src-xiaoxuetang-obm",
        "src-nlc-oracle-world",
        "src-penn-museum-oracle-bone",
        "src-sinica-da-xiaoxuetang-site",
        "src-sinica-yinshang-oracle-vocabulary",
        "src-cambridge-hopkins",
        "src-gbedobc",
        "src-ihp-museum-oracle-bones",
        "src-ihp-oracle-rubbings",
        "src-obid-ancientbooks",
        "src-open-oracle",
        "src-oracle-mnist",
        "src-tsinghua-oracle-bones",
        "src-yinqi-wenyuan",
    ]
    if [row.get("source_id", "") for row in source_route_rows] != expected_source_route_ids:
        issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} source route order changed")
    source_route_by_id = {row.get("source_id", ""): row for row in source_route_rows}
    for index, row in enumerate(source_route_rows, start=1):
        task_id = row.get("source_route_task_id", "")
        if task_id != f"source-route-review-{index:03d}":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} task ID sequence changed: {task_id}")
        if row.get("context_pack_id") != "ai-context-source-coverage-001":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} context pack link changed: {task_id}")
        if row.get("research_boundary") != "routing_metadata_only_not_scholarship":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} research boundary changed: {task_id}")
        if row.get("assignment_status") != "unassigned":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} assignment status changed: {task_id}")
        if row.get("review_status") != "needs_source_route_review":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} review status changed: {task_id}")
        if row.get("updated_at") != "2026-06-10":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} updated_at changed: {task_id}")
        caution = row.get("caution", "")
        if "routing and provenance review aid only" not in caution:
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} caution boundary changed: {task_id}")
        if "decipherment conclusions" not in caution:
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} decipherment caution changed: {task_id}")
        route_files = set(filter(None, row.get("route_files", "").split(";")))
        for required_file in [
            AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK,
            SOURCE_COVERAGE_SUMMARY,
            SOURCE_INDEX,
        ]:
            if required_file not in route_files:
                issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} missing common route file: {task_id}")

    expected_route_values = {
        "src-hust-obc": {
            "priority_rank": "1",
            "priority_tags": "candidate_queue;graph_derivative;metadata_profile;download_log",
            "review_focus": "open_candidate_queue_and_graph_routes_before_evidence_pack_work",
            "required_files": {
                HUST_OBC_CANDIDATE_GRAPH_EDGES,
                HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
                AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK,
                AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
            },
            "required_checks": {
                "verify_candidate_queue_rows_remain_reserved_and_cross_source_review_only",
                "verify_graph_edges_are_metadata_routes_not_component_or_decipherment_claims",
            },
        },
        "src-evobc": {
            "priority_rank": "2",
            "priority_tags": "graph_derivative;metadata_profile;download_log",
            "review_focus": "open_graph_derivatives_and_source_metadata_before_using_edges",
            "required_files": {EVOBC_EVOLUTION_GRAPH_EDGES, AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK},
            "required_checks": {"verify_graph_edges_are_metadata_routes_not_component_or_decipherment_claims"},
        },
        "src-obimd": {
            "priority_rank": "2",
            "priority_tags": "graph_derivative;metadata_profile;download_log",
            "review_focus": "open_graph_derivatives_and_source_metadata_before_using_edges",
            "required_files": {OBIMD_COMPONENT_GRAPH_EDGES, AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK},
            "required_checks": {"verify_graph_edges_are_metadata_routes_not_component_or_decipherment_claims"},
        },
        "src-metmuseum-oracle-bone": {
            "priority_rank": "3",
            "priority_tags": "public_asset;metadata_profile;download_log",
            "review_focus": "open_asset_rights_and_image_metadata_before_visual_review",
            "required_files": {ASSET_SOURCE_INDEX, ASSET_RIGHTS_REVIEW_LOG, AI_AGENT_PUBLIC_DOMAIN_ASSET_CONTEXT_PACK},
            "required_checks": {"verify_asset_rights_checksums_and_visual_profiles_before_image_use"},
        },
        "src-smithsonian-nmaa-oracle-bone": {
            "priority_rank": "3",
            "priority_tags": "public_asset;access_limited_or_error;metadata_profile;download_log",
            "review_focus": "open_asset_rights_and_image_metadata_before_visual_review",
            "required_files": {ASSET_IMAGE_TECHNICAL_PROFILE, ASSET_IMAGE_VISUAL_PROFILE, SOURCE_DOWNLOAD_LOG},
            "required_checks": {
                "verify_asset_rights_checksums_and_visual_profiles_before_image_use",
                "review_download_log_status_and_record_retry_or_metadata_only_decision",
            },
        },
        "src-british-museum-oracle-bone": {
            "priority_rank": "4",
            "priority_tags": "access_limited_or_error;download_log",
            "review_focus": "open_download_logs_and_resolve_access_or_error_boundary",
            "required_files": {SOURCE_DOWNLOAD_MANIFEST, SOURCE_DOWNLOAD_LOG, SOURCE_DOWNLOAD_STATUS_CODEBOOK},
            "required_checks": {"review_download_log_status_and_record_retry_or_metadata_only_decision"},
        },
        "src-nlc-oracle-world": {
            "priority_rank": "5",
            "priority_tags": "metadata_profile;download_log",
            "review_focus": "open_metadata_profile_and_source_register_before_extraction",
            "required_files": {DOWNLOADED_METADATA_PROFILE, SOURCE_DOWNLOAD_LOG},
            "required_checks": {"open_metadata_profile_rows_and_keep_extraction_reviewed_metadata_only"},
        },
        "src-yinqi-wenyuan": {
            "priority_rank": "6",
            "priority_tags": "download_log",
            "review_focus": "open_download_manifest_log_and_package_manifest_before_promotion",
            "required_files": {SOURCE_PACKAGE_FILE_MANIFEST, SOURCE_DOWNLOAD_STATUS_CODEBOOK},
            "required_checks": {"confirm_source_size_checksum_rights_and_risk_before_promoting_derivatives"},
        },
    }
    for source_id, expected_values in expected_route_values.items():
        row = source_route_by_id.get(source_id, {})
        if not row:
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} missing source route task: {source_id}")
            continue
        for key in ["priority_rank", "priority_tags", "review_focus"]:
            if row.get(key) != expected_values[key]:
                issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} {source_id} {key} changed")
        route_files = set(filter(None, row.get("route_files", "").split(";")))
        for required_file in expected_values["required_files"]:
            if required_file not in route_files:
                issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} {source_id} missing route file: {required_file}")
        next_checks = set(filter(None, row.get("required_next_checks", "").split(";")))
        for required_check in expected_values["required_checks"]:
            if required_check not in next_checks:
                issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_QUEUE} {source_id} missing next check: {required_check}")

    result_rows, result_issues = _read_csv_rows(root / AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD)
    issues.extend(result_issues)
    if len(result_rows) != 21:
        issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} should contain exactly 21 rows")
    if [row.get("source_id", "") for row in result_rows] != expected_source_route_ids:
        issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} source order changed")
    queue_rows_by_task = {
        row.get("source_route_task_id", ""): row
        for row in source_route_rows
    }
    for index, row in enumerate(result_rows, start=1):
        result_id = row.get("source_route_result_id", "")
        task_id = row.get("source_route_task_id", "")
        queue_row = queue_rows_by_task.get(task_id, {})
        if result_id != f"source-route-result-{index:03d}":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} result ID sequence changed: {result_id}")
        if task_id != f"source-route-review-{index:03d}":
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} task link sequence changed: {result_id}")
        if not queue_row:
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} missing queue link: {result_id}")
            continue
        for linked_field in [
            "context_pack_id",
            "source_id",
            "priority_tags",
            "review_focus",
            "required_next_checks",
        ]:
            if row.get(linked_field) != queue_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} {linked_field} "
                    f"does not match queue: {result_id}"
                )
        if row.get("route_files_to_open") != queue_row.get("route_files"):
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} route files changed: {result_id}")
        expected_scaffold_values = {
            "result_status": "not_started",
            "source_register_review_status": "not_collected",
            "route_file_review_status": "not_collected",
            "rights_and_risk_review_status": "not_collected",
            "size_checksum_review_status": "not_collected",
            "derivative_promotion_status": "not_decided",
            "evidence_gap_status": "not_collected",
            "next_artifact_recommendation": "not_collected",
            "research_boundary": "review_result_scaffold_not_scholarship",
            "output_scope": "source_route_review_scaffold_only",
            "updated_at": "2026-06-10",
        }
        for key, value in expected_scaffold_values.items():
            if row.get(key) != value:
                issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} {key} changed: {result_id}")
        caution = row.get("caution", "")
        for required_snippet in [
            "empty source-route review result scaffold",
            "remain not_collected",
            "Do not use it as source evidence",
            "rights decision",
            "promotion decision",
            "decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULT_SCAFFOLD} missing caution "
                    f"{required_snippet}: {result_id}"
                )

    review_rows, review_issues = _read_csv_rows(root / AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS)
    issues.extend(review_issues)
    expected_review_source_ids = ["src-hust-obc", "src-evobc", "src-obimd"]
    if len(review_rows) != 3:
        issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} should contain exactly 3 reviewed rows")
    if [row.get("source_id", "") for row in review_rows] != expected_review_source_ids:
        issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} source order changed")
    expected_review_values_by_source = {
        "src-hust-obc": {
            "source_route_result_id": "source-route-result-001",
            "source_route_task_id": "source-route-review-001",
            "priority_tags": "candidate_queue;graph_derivative;metadata_profile;download_log",
            "review_focus": "open_candidate_queue_and_graph_routes_before_evidence_pack_work",
            "rights_and_risk_review_status": "source_marked_risk_noted",
            "size_checksum_review_status": "raw_package_over_git_limit_manifested",
            "metadata_profile_metric_count": "11",
            "download_log_count": "7",
            "source_package_file_manifest_count": "4",
            "candidate_queue_count": "1588",
            "evidence_request_count": "1588",
            "graph_edge_count": "3562",
            "raw_package_file_size_bytes": "607933810",
            "raw_package_commit_policy": "do_not_commit_regular_git",
            "rights_status": "source_marked_risk_noted",
            "next_artifact_recommendation": (
                "open_first_hust_obc_candidate_or_bucket_route_for_cross_source_review"
            ),
            "required_route_files": {
                HUST_OBC_CANDIDATE_GRAPH_EDGES,
                HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
                AI_AGENT_HUST_OBC_BUCKET_REVIEW_ROUTE_PACK,
                AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
            },
            "required_review_note": ["HUST-OBC", "dataset labels remain candidates", "raw zip"],
        },
        "src-evobc": {
            "source_route_result_id": "source-route-result-002",
            "source_route_task_id": "source-route-review-002",
            "priority_tags": "graph_derivative;metadata_profile;download_log",
            "review_focus": "open_graph_derivatives_and_source_metadata_before_using_edges",
            "rights_and_risk_review_status": "source_marked_risk_noted",
            "size_checksum_review_status": "downloaded_metadata_files_logged_tmp_only",
            "metadata_profile_metric_count": "7",
            "download_log_count": "5",
            "source_package_file_manifest_count": "3",
            "candidate_queue_count": "0",
            "evidence_request_count": "0",
            "graph_edge_count": "51679",
            "raw_package_file_size_bytes": "23254733",
            "raw_package_commit_policy": "download_to_tmp_log_checksum_only",
            "rights_status": "source_marked_risk_noted",
            "next_artifact_recommendation": (
                "open_first_evobc_evolution_category_route_for_cross_source_review"
            ),
            "required_route_files": {EVOBC_EVOLUTION_GRAPH_EDGES},
            "required_review_note": ["EVOBC", "category, era-code, and source-code graph edges", "large JSON"],
        },
        "src-obimd": {
            "source_route_result_id": "source-route-result-003",
            "source_route_task_id": "source-route-review-003",
            "priority_tags": "graph_derivative;metadata_profile;download_log",
            "review_focus": "open_graph_derivatives_and_source_metadata_before_using_edges",
            "rights_and_risk_review_status": "licensed_for_repository",
            "size_checksum_review_status": "raw_package_over_git_limit_manifested",
            "metadata_profile_metric_count": "5",
            "download_log_count": "6",
            "source_package_file_manifest_count": "7",
            "candidate_queue_count": "0",
            "evidence_request_count": "0",
            "graph_edge_count": "44433",
            "raw_package_file_size_bytes": "558367972",
            "raw_package_commit_policy": "do_not_commit_regular_git",
            "rights_status": "licensed_for_repository",
            "next_artifact_recommendation": (
                "open_first_obimd_component_or_glyph_route_for_cross_source_review"
            ),
            "required_route_files": {OBIMD_COMPONENT_GRAPH_EDGES},
            "required_review_note": ["OBIMD", "main-character, subcharacter", "raw annotation and image packages"],
        },
    }
    scaffold_by_result = {
        scaffold_row.get("source_route_result_id", ""): scaffold_row
        for scaffold_row in result_rows
    }
    for row in review_rows:
        source_id = row.get("source_id", "")
        expected_review_values = expected_review_values_by_source.get(source_id)
        if expected_review_values is None:
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} unexpected source: {source_id}")
            continue
        expected_common_review_values = {
            "context_pack_id": "ai-context-source-coverage-001",
            "result_status": "reviewed_metadata_routes_only",
            "source_register_review_status": "reviewed_metadata_only",
            "route_file_review_status": "reviewed_route_files_exist",
            "derivative_promotion_status": "no_raw_asset_or_dataset_claim_promotion",
            "evidence_gap_status": "needs_cross_source_review_before_evidence_pack",
            "source_index_row_count": "1",
            "source_review_status": "reviewed",
            "research_boundary": "source_route_review_metadata_only_not_scholarship",
            "output_scope": "source_route_review_result_only",
            "updated_at": "2026-06-10",
        }
        for key, value in {**expected_common_review_values, **expected_review_values}.items():
            if key in {"required_route_files", "required_review_note"}:
                continue
            if row.get(key) != value:
                issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} {key} changed")
        scaffold_row = scaffold_by_result.get(row.get("source_route_result_id", ""), {})
        if scaffold_row and row.get("route_files_opened") != scaffold_row.get("route_files_to_open"):
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} route files changed")
        if scaffold_row and row.get("review_basis_files") != scaffold_row.get("route_files_to_open"):
            issues.append(f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} review basis files changed")
        route_files_opened = set(filter(None, row.get("route_files_opened", "").split(";")))
        common_required_files = {
            AI_AGENT_SOURCE_COVERAGE_CONTEXT_PACK,
            SOURCE_COVERAGE_SUMMARY,
            SOURCE_INDEX,
            SOURCE_DOWNLOAD_LOG,
            SOURCE_PACKAGE_FILE_MANIFEST,
            DOWNLOADED_METADATA_PROFILE,
            AI_AGENT_RELATIONSHIP_GRAPH_CONTEXT_PACK,
        }
        for required_file in common_required_files | expected_review_values["required_route_files"]:
            if required_file not in route_files_opened:
                issues.append(
                    f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} missing opened route file: "
                    f"{required_file}"
                )
        review_note = row.get("review_note", "")
        for required_snippet in ["Metadata-only review", "derived counts", "not promoted"]:
            if required_snippet not in review_note:
                issues.append(
                    f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} missing review note: "
                    f"{required_snippet}"
                )
        for required_snippet in expected_review_values["required_review_note"]:
            if required_snippet not in review_note:
                issues.append(
                    f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} missing review note: "
                    f"{required_snippet}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "metadata-only source-route review result",
            "not source evidence by itself",
            "not a decipherment result",
            "not a character/component/evolution-chain assignment",
            "not a rights clearance",
            "does not promote raw images",
            "dataset labels",
            "graph edges",
            "staging rows",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS} {source_id} missing caution: "
                    f"{required_snippet}"
                )

    cross_review_rows, cross_review_issues = _read_csv_rows(root / AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE)
    issues.extend(cross_review_issues)
    if len(cross_review_rows) != 3:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} should contain exactly 3 rows")
    if [row.get("source_id", "") for row in cross_review_rows] != expected_review_source_ids:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} source order changed")
    review_rows_by_source = {
        review_row.get("source_id", ""): review_row
        for review_row in review_rows
    }
    expected_cross_review_values_by_source = {
        "src-hust-obc": {
            "cross_review_task_id": "graph-source-cross-review-001",
            "source_route_result_id": "source-route-result-001",
            "source_route_task_id": "source-route-review-001",
            "target_review_scope": "hust_obc_first_candidate_evidence_pack_cross_source_review",
            "primary_review_record_id": "hust-obc-evidence-request-000001",
            "related_project_id": "obs-char-000001",
            "primary_external_ref_id": "hust-obc-cat-0001",
            "source_record_id": "0001",
            "candidate_or_staging_row_count": "1588",
            "graph_edge_count": "3562",
            "rights_status": "source_marked_risk_noted",
            "required_counter_source_ids": (
                "src-hust-obc;src-xiaoxuetang-jiaguwen;src-xiaoxuetang-obm;"
                "src-obimd;src-evobc;src-ihp-oracle-rubbings"
            ),
            "expected_output_path": (
                "doc/public/user_research/001_ai-agent-evidence-packs/hust-obc/"
                "001_000001-000100_obs-char-bucket/"
                "001_obs-char-000001_hust-obc-cat-0001_evidence-pack-draft.json"
            ),
            "required_route_files": {
                AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE,
                HUST_OBC_OBS_CHAR_PROMOTION_QUEUE,
                HUST_OBC_CANDIDATE_GRAPH_EDGES,
                OBIMD_COMPONENT_GRAPH_EDGES,
                EVOBC_EVOLUTION_GRAPH_EDGES,
            },
            "required_review_note": [
                "first HUST-OBC evidence request",
                "source category 0001",
                "obs-char-000001 remains reserved only",
            ],
        },
        "src-evobc": {
            "cross_review_task_id": "graph-source-cross-review-002",
            "source_route_result_id": "source-route-result-002",
            "source_route_task_id": "source-route-review-002",
            "target_review_scope": "evobc_first_evolution_category_cross_source_review",
            "primary_review_record_id": "evobc-evo-cat-00001",
            "related_project_id": "",
            "primary_external_ref_id": "evobc-cat-00001",
            "source_record_id": "00001",
            "candidate_or_staging_row_count": "13714",
            "graph_edge_count": "51679",
            "rights_status": "source_marked_risk_noted",
            "required_counter_source_ids": (
                "src-xiaoxuetang-jiaguwen;src-xiaoxuetang-obm;src-hust-obc;"
                "src-obimd;src-ihp-oracle-rubbings"
            ),
            "expected_output_path": (
                "doc/public/user_research/002_cross-source-review-queues/evobc/"
                "001_evobc-evo-cat-00001_cross-source-review-log.md"
            ),
            "required_route_files": {
                EVOBC_EVOLUTION_CATEGORY_STAGING,
                EVOBC_ERA_SOURCE_CODEBOOK_STAGING,
                EVOBC_EVOLUTION_GRAPH_EDGES,
            },
            "required_review_note": [
                "First category has source_category_id=00001",
                "source_character_codepoints=U+3401",
                "era_code_counts=0:35;3:2",
            ],
        },
        "src-obimd": {
            "cross_review_task_id": "graph-source-cross-review-003",
            "source_route_result_id": "source-route-result-003",
            "source_route_task_id": "source-route-review-003",
            "target_review_scope": "obimd_first_component_glyph_route_cross_source_review",
            "primary_review_record_id": "obimd-sub-cand-000001",
            "related_project_id": "obimd-main-cand-000001",
            "primary_external_ref_id": "obimd-sub-p8w7ujqanz",
            "source_record_id": "p8w7ujqanz",
            "candidate_or_staging_row_count": "2747",
            "graph_edge_count": "44433",
            "rights_status": "licensed_for_repository",
            "required_counter_source_ids": (
                "src-xiaoxuetang-jiaguwen;src-xiaoxuetang-obm;src-hust-obc;"
                "src-evobc;src-ihp-oracle-rubbings"
            ),
            "expected_output_path": (
                "doc/public/user_research/002_cross-source-review-queues/obimd/"
                "001_obimd-sub-cand-000001_cross-source-review-log.md"
            ),
            "required_route_files": {
                OBIMD_MAIN_CHARACTER_STAGING,
                OBIMD_SUBCHARACTER_MAIN_STAGING,
                OBIMD_SUBCHARACTER_GLYPH_STAGING,
                OBIMD_COMPONENT_GRAPH_EDGES,
            },
            "required_review_note": [
                "obimd-main-cand-000001",
                "obimd-sub-cand-000001",
                "glyph_codepoint_uplus=U+65E5;U+F0000",
            ],
        },
    }
    required_common_cross_review_files = {
        AI_AGENT_SOURCE_ROUTE_REVIEW_RESULTS,
        SOURCE_INDEX,
        DOWNLOADED_METADATA_PROFILE,
        SOURCE_DOWNLOAD_LOG,
        SOURCE_PACKAGE_FILE_MANIFEST,
    }
    required_evidence_sections = {
        "source_register",
        "download_log",
        "package_manifest",
        "metadata_profile",
        "graph_edges",
        "staging_row",
        "counter_source_lookup",
        "rights_risk_review",
        "review_log",
    }
    for row in cross_review_rows:
        source_id = row.get("source_id", "")
        expected_cross_review_values = expected_cross_review_values_by_source.get(source_id)
        if expected_cross_review_values is None:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} unexpected source: {source_id}")
            continue
        source_review_row = review_rows_by_source.get(source_id, {})
        for linked_field in [
            "source_route_result_id",
            "source_route_task_id",
            "context_pack_id",
            "graph_edge_count",
            "rights_status",
            "source_review_status",
        ]:
            if source_review_row and row.get(linked_field) != source_review_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} "
                    f"{linked_field} does not match source-route result"
                )
        expected_common_cross_review_values = {
            "context_pack_id": "ai-context-source-coverage-001",
            "source_review_status": "reviewed",
            "task_status": "needs_cross_source_review",
            "promotion_status": "not_promoted",
            "research_boundary": "cross_source_review_queue_metadata_only_not_scholarship",
            "updated_at": "2026-06-10",
        }
        for key, value in {**expected_common_cross_review_values, **expected_cross_review_values}.items():
            if key in {"required_route_files", "required_review_note"}:
                continue
            if row.get(key) != value:
                issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} {key} changed")
        sections = set(filter(None, row.get("required_evidence_sections", "").split(";")))
        if sections != required_evidence_sections:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} evidence sections changed")
        route_files = set(filter(None, row.get("route_files_to_open", "").split(";")))
        if row.get("review_basis_files") != row.get("route_files_to_open"):
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} review basis changed")
        for required_file in required_common_cross_review_files | expected_cross_review_values["required_route_files"]:
            if required_file not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} missing route file: "
                    f"{required_file}"
                )
            elif not (root / required_file).exists():
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} route file missing on disk: "
                    f"{required_file}"
                )
        review_note = row.get("review_note", "")
        for required_snippet in expected_cross_review_values["required_review_note"]:
            if required_snippet not in review_note:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} missing review note: "
                    f"{required_snippet}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "cross-source review queue row only",
            "not source evidence by itself",
            "not a decipherment result",
            "not a component assignment",
            "not an evolution-chain assignment",
            "not a rights clearance",
            "must not promote dataset labels",
            "graph edges",
            "staging rows",
            "raw source packages",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_QUEUE} {source_id} missing caution: "
                    f"{required_snippet}"
                )

    cross_review_log_rows, cross_review_log_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD
    )
    issues.extend(cross_review_log_issues)
    if len(cross_review_log_rows) != 3:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} should contain exactly 3 rows")
    if [row.get("source_id", "") for row in cross_review_log_rows] != expected_review_source_ids:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} source order changed")
    cross_review_rows_by_task = {
        row.get("cross_review_task_id", ""): row
        for row in cross_review_rows
    }
    expected_log_status_values = {
        "result_status": "not_started",
        "source_register_review_status": "not_collected",
        "download_log_review_status": "not_collected",
        "package_manifest_review_status": "not_collected",
        "metadata_profile_review_status": "not_collected",
        "graph_edge_review_status": "not_collected",
        "staging_row_review_status": "not_collected",
        "counter_source_lookup_status": "not_collected",
        "rights_risk_review_status": "not_collected",
        "review_log_status": "not_collected",
        "evidence_pack_draft_status": "not_started",
        "promotion_decision_status": "not_decided",
        "research_boundary": "cross_source_review_log_scaffold_not_scholarship",
        "output_scope": "cross_source_review_log_scaffold_only",
        "updated_at": "2026-06-10",
    }
    for index, row in enumerate(cross_review_log_rows, start=1):
        log_id = row.get("cross_review_log_id", "")
        task_id = row.get("cross_review_task_id", "")
        queue_row = cross_review_rows_by_task.get(task_id, {})
        if log_id != f"graph-source-cross-review-log-{index:03d}":
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} log ID sequence changed: {log_id}")
        if task_id != f"graph-source-cross-review-{index:03d}":
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} task link sequence changed: {log_id}")
        if not queue_row:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} missing queue link: {log_id}")
            continue
        for linked_field in [
            "source_route_result_id",
            "source_route_task_id",
            "context_pack_id",
            "source_id",
            "target_review_scope",
            "primary_review_record_id",
            "related_project_id",
            "primary_external_ref_id",
            "source_record_id",
            "expected_output_path",
            "route_files_to_open",
            "required_counter_source_ids",
            "required_evidence_sections",
        ]:
            if row.get(linked_field) != queue_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} {linked_field} "
                    f"does not match queue: {log_id}"
                )
        for key, expected_value in expected_log_status_values.items():
            if row.get(key) != expected_value:
                issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} {key} changed: {log_id}")
        caution = row.get("caution", "")
        for required_snippet in [
            "empty graph-source cross-review log scaffold",
            "not_collected",
            "opens the cited route files",
            "Do not use it as source evidence",
            "rights decision",
            "promotion decision",
            "component or evolution-chain assignment",
            "decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD} missing caution "
                    f"{required_snippet}: {log_id}"
                )

    cross_review_draft_rows, cross_review_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST
    )
    issues.extend(cross_review_draft_issues)
    if len(cross_review_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} should contain exactly 3 rows"
        )
    if [row.get("source_id", "") for row in cross_review_draft_rows] != expected_review_source_ids:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} source order changed")
    cross_review_log_rows_by_id = {
        row.get("cross_review_log_id", ""): row
        for row in cross_review_log_rows
    }
    expected_draft_paths = {
        "src-hust-obc": AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_HUST_DRAFT,
        "src-evobc": AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_EVOBC_DRAFT,
        "src-obimd": AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_OBIMD_DRAFT,
    }
    expected_draft_status_values = {
        "scaffold_source_path": AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_SCAFFOLD,
        "draft_status": "draft_not_collected",
        "evidence_section_status": "not_collected",
        "research_boundary": "user_research_draft_not_scholarship",
        "updated_at": "2026-06-10",
    }
    for index, row in enumerate(cross_review_draft_rows, start=1):
        draft_log_id = row.get("draft_log_id", "")
        cross_review_log_id = row.get("cross_review_log_id", "")
        source_id = row.get("source_id", "")
        scaffold_row = cross_review_log_rows_by_id.get(cross_review_log_id, {})
        if draft_log_id != f"graph-source-cross-review-draft-{index:03d}":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} "
                f"draft ID sequence changed: {draft_log_id}"
            )
        if not scaffold_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} "
                f"missing scaffold link: {draft_log_id}"
            )
            continue
        for linked_field in [
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "route_files_to_open",
            "required_counter_source_ids",
            "required_evidence_sections",
        ]:
            if row.get(linked_field) != scaffold_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} {linked_field} "
                    f"does not match scaffold: {draft_log_id}"
                )
        expected_draft_path = expected_draft_paths.get(source_id)
        if row.get("draft_log_path") != expected_draft_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} draft path changed: "
                f"{draft_log_id}"
            )
        for key, expected_value in expected_draft_status_values.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} {key} "
                    f"changed: {draft_log_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not source evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_DRAFT_MANIFEST} missing caution "
                    f"{required_snippet}: {draft_log_id}"
                )
        if expected_draft_path:
            draft_path = root / expected_draft_path
            if not draft_path.exists():
                issues.append(f"{expected_draft_path} missing draft log file")
                continue
            draft_text = draft_path.read_text(encoding="utf-8")
            for required_snippet in [
                "Graph Source Cross-Review Log",
                "draft_not_collected",
                "user_research_draft_not_scholarship",
                "not_collected",
                "not_decided",
                "Route Files To Open",
                "Required Counter Sources",
                "Evidence Sections",
                "created_from_013_scaffold",
                "not a decipherment conclusion",
                "不是释读结论",
            ]:
                if required_snippet not in draft_text:
                    issues.append(
                        f"{expected_draft_path} missing draft text snippet: {required_snippet}"
                    )

    cross_review_result_rows, cross_review_result_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS
    )
    issues.extend(cross_review_result_issues)
    if len(cross_review_result_rows) != 3:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} should contain exactly 3 rows")
    if [row.get("source_id", "") for row in cross_review_result_rows] != expected_review_source_ids:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} source order changed")
    cross_review_draft_rows_by_id = {
        row.get("draft_log_id", ""): row
        for row in cross_review_draft_rows
    }
    expected_result_counts = {
        "src-hust-obc": {
            "route_file_count": "11",
            "required_counter_source_count": "6",
            "registered_counter_source_count": "6",
            "download_log_count": "7",
            "package_manifest_count": "4",
            "metadata_profile_metric_count": "11",
            "graph_route_file_count": "3",
            "graph_edge_route_line_count": "99674",
            "primary_graph_edge_count": "3562",
            "staging_row_count": "3",
            "rights_status": "source_marked_risk_noted",
        },
        "src-evobc": {
            "route_file_count": "8",
            "required_counter_source_count": "5",
            "registered_counter_source_count": "5",
            "download_log_count": "5",
            "package_manifest_count": "3",
            "metadata_profile_metric_count": "7",
            "graph_route_file_count": "1",
            "graph_edge_route_line_count": "51679",
            "primary_graph_edge_count": "51679",
            "staging_row_count": "3",
            "rights_status": "source_marked_risk_noted",
        },
        "src-obimd": {
            "route_file_count": "9",
            "required_counter_source_count": "5",
            "registered_counter_source_count": "5",
            "download_log_count": "6",
            "package_manifest_count": "7",
            "metadata_profile_metric_count": "5",
            "graph_route_file_count": "1",
            "graph_edge_route_line_count": "44433",
            "primary_graph_edge_count": "44433",
            "staging_row_count": "52",
            "rights_status": "licensed_for_repository",
        },
    }
    expected_result_status_values = {
        "missing_route_file_count": "0",
        "route_file_review_status": "reviewed_route_files_exist",
        "counter_source_lookup_status": "reviewed_all_required_counter_sources_registered",
        "download_log_review_status": "reviewed_metadata_only",
        "package_manifest_review_status": "reviewed_metadata_only",
        "metadata_profile_review_status": "reviewed_metadata_only",
        "graph_edge_review_status": "reviewed_graph_route_files_metadata_only",
        "staging_row_review_status": "reviewed_metadata_only",
        "draft_log_status": "draft_log_exists",
        "rights_risk_review_status": "reviewed_rights_boundary_metadata_only",
        "promotion_decision_status": "not_promoted",
        "evidence_pack_draft_status": "not_started_or_draft_only",
        "research_boundary": "cross_source_review_log_result_metadata_only_not_scholarship",
        "output_scope": "cross_source_review_log_result_only",
        "updated_at": "2026-06-10",
    }
    expected_staging_snippets = {
        "src-hust-obc": [
            "hust-obc-evidence-request-000001",
            "hust-obc-obs-char-promo-000001",
            "hust-obc-bucket-001-row-001",
        ],
        "src-evobc": [
            "evobc-evo-cat-00001",
            "evobc-code-001",
            "evobc-code-004",
        ],
        "src-obimd": [
            "obimd-main-cand-000001",
            "obimd-sub-cand-000001",
            "obimd-glyph-link-000001",
            "obimd-glyph-link-000050",
        ],
    }
    for index, row in enumerate(cross_review_result_rows, start=1):
        result_id = row.get("cross_review_result_id", "")
        draft_log_id = row.get("draft_log_id", "")
        source_id = row.get("source_id", "")
        draft_row = cross_review_draft_rows_by_id.get(draft_log_id, {})
        if result_id != f"graph-source-cross-review-result-{index:03d}":
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} result ID sequence changed: {result_id}")
        if not draft_row:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} missing draft link: {result_id}")
            continue
        for linked_field in [
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
        ]:
            if row.get(linked_field) != draft_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} {linked_field} "
                    f"does not match draft manifest: {result_id}"
                )
        for key, expected_value in expected_result_status_values.items():
            if row.get(key) != expected_value:
                issues.append(f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} {key} changed: {result_id}")
        for key, expected_value in expected_result_counts.get(source_id, {}).items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} {source_id} "
                    f"{key} changed: {row.get(key)}"
                )
        staging_refs = row.get("staging_record_refs", "")
        for required_snippet in expected_staging_snippets.get(source_id, []):
            if required_snippet not in staging_refs:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} {source_id} "
                    f"missing staging ref: {required_snippet}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "metadata-only cross-source review log result",
            "not source evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} missing caution "
                    f"{required_snippet}: {result_id}"
                )
        review_note = row.get("review_note", "")
        for required_snippet in [
            "Metadata-only review opened",
            "does not promote dataset labels",
            "graph edges",
            "staging rows",
            "scholarship",
        ]:
            if required_snippet not in review_note:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS} missing review note "
                    f"{required_snippet}: {result_id}"
                )

    evidence_task_rows, evidence_task_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE
    )
    issues.extend(evidence_task_issues)
    if len(evidence_task_rows) != 27:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} should contain exactly 27 rows")
    expected_sections = [
        "source_register",
        "download_log",
        "package_manifest",
        "metadata_profile",
        "graph_edges",
        "staging_row",
        "counter_source_lookup",
        "rights_risk_review",
        "review_log",
    ]
    for source_id in expected_review_source_ids:
        source_rows = [row for row in evidence_task_rows if row.get("source_id") == source_id]
        if len(source_rows) != 9:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} {source_id} should have 9 rows")
        if [row.get("target_evidence_section", "") for row in source_rows] != expected_sections:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} {source_id} section order changed")
    for section in expected_sections:
        section_count = sum(1 for row in evidence_task_rows if row.get("target_evidence_section") == section)
        if section_count != 3:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} {section} "
                f"should appear 3 times, got {section_count}"
            )
    cross_review_result_rows_by_id = {
        row.get("cross_review_result_id", ""): row
        for row in cross_review_result_rows
    }
    expected_route_file_counts_by_source_section = {
        ("src-hust-obc", "source_register"): "1",
        ("src-hust-obc", "download_log"): "1",
        ("src-hust-obc", "package_manifest"): "1",
        ("src-hust-obc", "metadata_profile"): "1",
        ("src-hust-obc", "graph_edges"): "3",
        ("src-hust-obc", "staging_row"): "3",
        ("src-hust-obc", "counter_source_lookup"): "1",
        ("src-hust-obc", "rights_risk_review"): "4",
        ("src-hust-obc", "review_log"): "2",
        ("src-evobc", "source_register"): "1",
        ("src-evobc", "download_log"): "1",
        ("src-evobc", "package_manifest"): "1",
        ("src-evobc", "metadata_profile"): "1",
        ("src-evobc", "graph_edges"): "1",
        ("src-evobc", "staging_row"): "2",
        ("src-evobc", "counter_source_lookup"): "1",
        ("src-evobc", "rights_risk_review"): "4",
        ("src-evobc", "review_log"): "2",
        ("src-obimd", "source_register"): "1",
        ("src-obimd", "download_log"): "1",
        ("src-obimd", "package_manifest"): "1",
        ("src-obimd", "metadata_profile"): "1",
        ("src-obimd", "graph_edges"): "1",
        ("src-obimd", "staging_row"): "3",
        ("src-obimd", "counter_source_lookup"): "1",
        ("src-obimd", "rights_risk_review"): "4",
        ("src-obimd", "review_log"): "2",
    }
    for index, row in enumerate(evidence_task_rows, start=1):
        task_id = row.get("evidence_collection_task_id", "")
        result_id = row.get("cross_review_result_id", "")
        source_id = row.get("source_id", "")
        section = row.get("target_evidence_section", "")
        result_row = cross_review_result_rows_by_id.get(result_id, {})
        if task_id != f"graph-source-evidence-task-{index:03d}":
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} task ID sequence changed: {task_id}")
        if not result_row:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} missing result link: {task_id}")
            continue
        for linked_field in [
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
        ]:
            if row.get(linked_field) != result_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} {linked_field} "
                    f"does not match 015 result: {task_id}"
                )
        expected_route_count = expected_route_file_counts_by_source_section.get((source_id, section))
        if row.get("route_file_count") != expected_route_count:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} {source_id} {section} "
                f"route_file_count changed: {row.get('route_file_count')}"
            )
        expected_output_prefix = (
            "doc/public/user_research/003_evidence-collection-tasks/"
        )
        if not row.get("expected_output_path", "").startswith(expected_output_prefix):
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} bad output path: {task_id}")
        for key, expected_value in {
            "prerequisite_status": "ready_from_015_metadata_review",
            "task_status": "not_started",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_task_queue_not_scholarship",
            "output_scope": "route_to_future_evidence_collection_only",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} {key} changed: {task_id}")
        if not row.get("collection_scope", "").startswith("collect_"):
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} missing collection scope: {task_id}")
        if not row.get("route_files_to_open", ""):
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} missing route file: {task_id}")
        caution = row.get("caution", "")
        for required_snippet in [
            "evidence-collection task only",
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE} missing caution "
                    f"{required_snippet}: {task_id}"
                )

    evidence_note_draft_rows, evidence_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST
    )
    issues.extend(evidence_note_draft_issues)
    if len(evidence_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    evidence_task_rows_by_id = {
        row.get("evidence_collection_task_id", ""): row
        for row in evidence_task_rows
    }
    expected_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-001",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_SOURCE_REGISTER_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-010",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_SOURCE_REGISTER_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-019",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_SOURCE_REGISTER_DRAFT,
        ),
    ]
    for row, expected in zip(evidence_note_draft_rows, expected_note_tasks):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "source_register",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )

    download_log_note_draft_rows, download_log_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST
    )
    issues.extend(download_log_note_draft_issues)
    if len(download_log_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    expected_download_log_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-002",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_DOWNLOAD_LOG_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-011",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_DOWNLOAD_LOG_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-020",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_DOWNLOAD_LOG_DRAFT,
        ),
    ]
    for row, expected in zip(download_log_note_draft_rows, expected_download_log_note_tasks):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "download_log",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": SOURCE_DOWNLOAD_LOG,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "download_log",
            "Download Log",
            "下载日志",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            SOURCE_DOWNLOAD_LOG,
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )

    package_manifest_note_draft_rows, package_manifest_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST
    )
    issues.extend(package_manifest_note_draft_issues)
    if len(package_manifest_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    expected_package_manifest_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-003",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_PACKAGE_MANIFEST_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-012",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_PACKAGE_MANIFEST_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-021",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_PACKAGE_MANIFEST_DRAFT,
        ),
    ]
    for row, expected in zip(package_manifest_note_draft_rows, expected_package_manifest_note_tasks):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "package_manifest",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": SOURCE_PACKAGE_FILE_MANIFEST,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "package_manifest",
            "Package Manifest",
            "包 manifest",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            SOURCE_PACKAGE_FILE_MANIFEST,
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )

    metadata_profile_note_draft_rows, metadata_profile_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST
    )
    issues.extend(metadata_profile_note_draft_issues)
    if len(metadata_profile_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    expected_metadata_profile_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-004",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_METADATA_PROFILE_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-013",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_METADATA_PROFILE_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-022",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_METADATA_PROFILE_DRAFT,
        ),
    ]
    for row, expected in zip(metadata_profile_note_draft_rows, expected_metadata_profile_note_tasks):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "metadata_profile",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": DOWNLOADED_METADATA_PROFILE,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "metadata_profile",
            "Metadata Profile",
            "metadata 画像",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            DOWNLOADED_METADATA_PROFILE,
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )

    graph_edges_note_draft_rows, graph_edges_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST
    )
    issues.extend(graph_edges_note_draft_issues)
    if len(graph_edges_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    hust_graph_edge_routes = (
        f"{HUST_OBC_CANDIDATE_GRAPH_EDGES};"
        f"{OBIMD_COMPONENT_GRAPH_EDGES};"
        f"{EVOBC_EVOLUTION_GRAPH_EDGES}"
    )
    expected_graph_edges_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-005",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_GRAPH_EDGES_DRAFT,
            hust_graph_edge_routes,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-014",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_GRAPH_EDGES_DRAFT,
            EVOBC_EVOLUTION_GRAPH_EDGES,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-023",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_GRAPH_EDGES_DRAFT,
            OBIMD_COMPONENT_GRAPH_EDGES,
        ),
    ]
    for row, expected in zip(graph_edges_note_draft_rows, expected_graph_edges_note_tasks):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path, expected_route_files = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "graph_edges",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": expected_route_files,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "graph_edges",
            "Graph Edges",
            "图谱边",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )
        for required_route_file in expected_route_files.split(";"):
            if required_route_file not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing route file: "
                    f"{required_route_file}"
                )

    staging_row_note_draft_rows, staging_row_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST
    )
    issues.extend(staging_row_note_draft_issues)
    if len(staging_row_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    hust_first_bucket_manifest = (
        "corpus/001_oracle-characters/"
        "001_000001-000100_obs-char-bucket_oracle-characters/"
        f"{HUST_OBC_PROMOTION_BUCKET_MANIFEST_FILENAME}"
    )
    hust_staging_routes = (
        f"{AI_AGENT_HUST_OBC_CANDIDATE_EVIDENCE_REQUEST_QUEUE};"
        f"{HUST_OBC_OBS_CHAR_PROMOTION_QUEUE};"
        f"{hust_first_bucket_manifest}"
    )
    evobc_staging_routes = (
        f"{EVOBC_EVOLUTION_CATEGORY_STAGING};"
        f"{EVOBC_ERA_SOURCE_CODEBOOK_STAGING}"
    )
    obimd_staging_routes = (
        f"{OBIMD_MAIN_CHARACTER_STAGING};"
        f"{OBIMD_SUBCHARACTER_MAIN_STAGING};"
        f"{OBIMD_SUBCHARACTER_GLYPH_STAGING}"
    )
    expected_staging_row_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-006",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_STAGING_ROW_DRAFT,
            hust_staging_routes,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-015",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_STAGING_ROW_DRAFT,
            evobc_staging_routes,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-024",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_STAGING_ROW_DRAFT,
            obimd_staging_routes,
        ),
    ]
    for row, expected in zip(staging_row_note_draft_rows, expected_staging_row_note_tasks):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path, expected_route_files = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "staging_row",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": expected_route_files,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "staging_row",
            "Staging Row",
            "staging 行",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )
        for required_route_file in expected_route_files.split(";"):
            if required_route_file not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing route file: "
                    f"{required_route_file}"
                )

    counter_source_lookup_note_draft_rows, counter_source_lookup_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST
    )
    issues.extend(counter_source_lookup_note_draft_issues)
    if len(counter_source_lookup_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    expected_counter_source_lookup_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-007",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_COUNTER_SOURCE_LOOKUP_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-016",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_COUNTER_SOURCE_LOOKUP_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-025",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_COUNTER_SOURCE_LOOKUP_DRAFT,
        ),
    ]
    for row, expected in zip(
        counter_source_lookup_note_draft_rows,
        expected_counter_source_lookup_note_tasks,
    ):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "counter_source_lookup",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": SOURCE_INDEX,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "counter_source_lookup",
            "Counter-Source Lookup",
            "反查来源",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            SOURCE_INDEX,
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a decipherment conclusion",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )

    rights_risk_review_note_draft_rows, rights_risk_review_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST
    )
    issues.extend(rights_risk_review_note_draft_issues)
    if len(rights_risk_review_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    expected_rights_risk_review_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-008",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_RIGHTS_RISK_REVIEW_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-017",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_RIGHTS_RISK_REVIEW_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-026",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_RIGHTS_RISK_REVIEW_DRAFT,
        ),
    ]
    expected_rights_route_files = (
        f"{SOURCE_INDEX};{DOWNLOADED_METADATA_PROFILE};"
        f"{SOURCE_DOWNLOAD_LOG};{SOURCE_PACKAGE_FILE_MANIFEST}"
    )
    for row, expected in zip(
        rights_risk_review_note_draft_rows,
        expected_rights_risk_review_note_tasks,
    ):
        expected_note_id, expected_task_id, expected_source_id, expected_note_path = expected
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "rights_risk_review",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": expected_rights_route_files,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "rights_risk_review",
            "Rights And Risk Review",
            "权利与风险复核",
            "collect_rights_risk_and_size_boundary_notes",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a rights decision",
            "not a decipherment conclusion",
            "不是权利决定",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )
        for required_route_file in expected_rights_route_files.split(";"):
            if required_route_file not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing route file: "
                    f"{required_route_file}"
                )

    review_log_note_draft_rows, review_log_note_draft_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST
    )
    issues.extend(review_log_note_draft_issues)
    if len(review_log_note_draft_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
            "should contain exactly 3 rows"
        )
    expected_review_log_note_tasks = [
        (
            "graph-source-evidence-note-draft-001",
            "graph-source-evidence-task-009",
            "src-hust-obc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_HUST_REVIEW_LOG_DRAFT,
            AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_HUST_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-002",
            "graph-source-evidence-task-018",
            "src-evobc",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_EVOBC_REVIEW_LOG_DRAFT,
            AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_EVOBC_DRAFT,
        ),
        (
            "graph-source-evidence-note-draft-003",
            "graph-source-evidence-task-027",
            "src-obimd",
            AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_OBIMD_REVIEW_LOG_DRAFT,
            AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_OBIMD_DRAFT,
        ),
    ]
    for row, expected in zip(
        review_log_note_draft_rows,
        expected_review_log_note_tasks,
    ):
        (
            expected_note_id,
            expected_task_id,
            expected_source_id,
            expected_note_path,
            expected_review_log_path,
        ) = expected
        expected_review_log_route_files = (
            f"{AI_AGENT_GRAPH_SOURCE_CROSS_REVIEW_LOG_RESULTS};{expected_review_log_path}"
        )
        note_id = row.get("evidence_collection_note_draft_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        task_row = evidence_task_rows_by_id.get(task_id, {})
        if note_id != expected_note_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"note ID changed: {note_id}"
            )
        if task_id != expected_task_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"task link changed: {task_id}"
            )
        if row.get("source_id") != expected_source_id:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"source changed: {note_id}"
            )
        if row.get("note_draft_path") != expected_note_path:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"note path changed: {note_id}"
            )
        if not task_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"missing 016 task link: {note_id}"
            )
            continue
        for linked_field in [
            "cross_review_result_id",
            "draft_log_id",
            "cross_review_log_id",
            "cross_review_task_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "route_files_to_open",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != task_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                    f"{linked_field} does not match 016 task: {note_id}"
                )
        if row.get("note_draft_path") != task_row.get("expected_output_path"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"note path does not match 016 expected output: {note_id}"
            )
        for key, expected_value in {
            "target_evidence_section": "review_log",
            "task_queue_source_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_TASK_QUEUE,
            "route_files_to_open": expected_review_log_route_files,
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
            "updated_at": "2026-06-10",
        }.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                    f"{key} changed: {note_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "not collected evidence",
            "not a rights decision",
            "not a promotion decision",
            "not a component or evolution-chain assignment",
            "not a decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                    f"missing caution {required_snippet}: {note_id}"
                )
        note_path = root / row.get("note_draft_path", "")
        if not note_path.exists():
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST} "
                f"missing note draft file: {note_id}"
            )
            continue
        note_text = note_path.read_text(encoding="utf-8")
        for required_snippet in [
            "Evidence Collection Note",
            "证据收集记录草稿",
            "review_log",
            "Review Log",
            "复核日志",
            "collect_human_or_agent_review_log_notes_under_user_research",
            "draft_not_collected",
            "not_collected",
            "not_promoted",
            "Route Files To Open",
            "Counter Sources To Check",
            "created_from_016_task_queue",
            "not a rights decision",
            "not a decipherment conclusion",
            "不是权利决定",
            "不是释读结论",
        ]:
            if required_snippet not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing note snippet: "
                    f"{required_snippet}"
                )
        for required_route_file in expected_review_log_route_files.split(";"):
            if required_route_file not in note_text:
                issues.append(
                    f"{row.get('note_draft_path', '')} missing route file: "
                    f"{required_route_file}"
                )

    route_pack_path = root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK
    try:
        route_pack = json.loads(route_pack_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} invalid JSON: {exc}")
        return issues

    expected_route_manifest_paths = [
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_DOWNLOAD_LOG_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_PACKAGE_MANIFEST_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_METADATA_PROFILE_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_GRAPH_EDGES_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_STAGING_ROW_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_COUNTER_SOURCE_LOOKUP_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_RIGHTS_RISK_REVIEW_NOTE_DRAFT_MANIFEST,
        AI_AGENT_GRAPH_SOURCE_REVIEW_LOG_NOTE_DRAFT_MANIFEST,
    ]
    expected_route_sections = [
        "source_register",
        "download_log",
        "package_manifest",
        "metadata_profile",
        "graph_edges",
        "staging_row",
        "counter_source_lookup",
        "rights_risk_review",
        "review_log",
    ]
    expected_route_sources = ["src-hust-obc", "src-evobc", "src-obimd"]
    for key, expected_value in {
        "context_pack_id": "ai-context-graph-source-evidence-collection-001",
        "status": "draft_route_pack_not_collected",
        "updated_at": "2026-06-10",
    }.items():
        if route_pack.get(key) != expected_value:
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} {key} changed")
    if route_pack.get("generated_from") != expected_route_manifest_paths:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} generated_from changed")

    coverage = route_pack.get("coverage", {})
    expected_coverage_values = {
        "manifest_count": 9,
        "note_draft_count": 27,
        "source_count": 3,
        "target_evidence_section_count": 9,
        "route_file_reference_count": 46,
        "counter_source_reference_count": 144,
    }
    for key, expected_value in expected_coverage_values.items():
        if coverage.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} coverage {key} changed"
            )
    if coverage.get("source_counts") != {
        "src-evobc": 9,
        "src-hust-obc": 9,
        "src-obimd": 9,
    }:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} source counts changed")
    if coverage.get("section_counts") != {section: 3 for section in expected_route_sections}:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} section counts changed")
    if coverage.get("note_status_counts") != {"draft_not_collected": 27}:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} note status counts changed")
    if coverage.get("evidence_collection_status_counts") != {"not_collected": 27}:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} evidence status counts changed"
        )
    if coverage.get("promotion_status_counts") != {"not_promoted": 27}:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} promotion counts changed")
    if coverage.get("research_boundary_counts") != {
        "evidence_collection_note_draft_not_scholarship": 27
    }:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} boundary counts changed")

    source_routes = route_pack.get("source_routes", [])
    if [row.get("source_id") for row in source_routes] != expected_route_sources:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} source route order changed")
    for source_route in source_routes:
        if source_route.get("note_draft_count") != 9:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} source route count changed: "
                f"{source_route.get('source_id', '')}"
            )
        if source_route.get("target_evidence_sections") != expected_route_sections:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} source route sections changed: "
                f"{source_route.get('source_id', '')}"
            )
        for note_path in source_route.get("note_draft_paths", []):
            if not str(note_path).startswith("doc/public/user_research/003_evidence-collection-tasks/"):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} bad note path: "
                    f"{note_path}"
                )

    section_routes = route_pack.get("section_routes", [])
    if [row.get("target_evidence_section") for row in section_routes] != expected_route_sections:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} section route order changed")
    for section_route in section_routes:
        if section_route.get("note_draft_count") != 3:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} section route count changed: "
                f"{section_route.get('target_evidence_section', '')}"
            )
        if section_route.get("source_ids") != expected_route_sources:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} section route sources changed: "
                f"{section_route.get('target_evidence_section', '')}"
            )

    note_routes = route_pack.get("note_routes", [])
    if len(note_routes) != 27:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} should contain 27 note routes")
    if note_routes:
        if note_routes[0].get("evidence_collection_task_id") != "graph-source-evidence-task-001":
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} first task changed")
        if note_routes[-1].get("evidence_collection_task_id") != "graph-source-evidence-task-027":
            issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} last task changed")
    for route in note_routes:
        note_path = str(route.get("note_draft_path", ""))
        if not note_path.startswith("doc/public/user_research/"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} note path outside user_research: "
                f"{note_path}"
            )
        if note_path.startswith("research/"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} note path enters research: "
                f"{note_path}"
            )
        for key, expected_value in {
            "note_status": "draft_not_collected",
            "evidence_collection_status": "not_collected",
            "promotion_status": "not_promoted",
            "research_boundary": "evidence_collection_note_draft_not_scholarship",
        }.items():
            if route.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} {key} changed: "
                    f"{route.get('evidence_collection_task_id', '')}"
                )

    agent_rules = " ".join(route_pack.get("agent_use_rules", []))
    for required_snippet in [
        "not-collected",
        "Do not treat this pack as collected evidence",
        "ignored temporary directories",
    ]:
        if required_snippet not in agent_rules:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} missing agent rule: "
                f"{required_snippet}"
            )
    agent_rules_zh = " ".join(route_pack.get("agent_use_rules_zh", []))
    for required_snippet in [
        "未收集",
        "不得把本包当作已收集证据",
        "已忽略临时目录",
    ]:
        if required_snippet not in agent_rules_zh:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK} missing zh agent rule: "
                f"{required_snippet}"
            )

    result_rows, result_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD
    )
    issues.extend(result_issues)
    if len(result_rows) != 27:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
            "should contain exactly 27 rows"
        )
    route_rows_by_task = {
        str(row.get("evidence_collection_task_id", "")): row
        for row in note_routes
        if isinstance(row, dict)
    }
    expected_section_actions = {
        "source_register": "collect_source_register_provenance_fields",
        "download_log": "collect_download_log_status_size_checksum_access_notes",
        "package_manifest": "collect_package_manifest_file_size_checksum_and_storage_boundary",
        "metadata_profile": "collect_metadata_profile_fields_and_extraction_scope",
        "graph_edges": "collect_graph_edge_source_status_and_claim_boundary",
        "staging_row": "collect_staging_row_field_map_and_review_status",
        "counter_source_lookup": "collect_counter_source_lookup_notes_without_identity_claim",
        "rights_risk_review": "collect_rights_risk_notes_without_rights_decision",
        "review_log": "collect_review_log_notes_without_promotion_decision",
    }
    expected_result_status_values = {
        "result_status": "not_started",
        "note_draft_open_status": "not_opened",
        "route_files_open_status": "not_opened",
        "evidence_collection_status": "not_collected",
        "source_register_evidence_status": "not_collected",
        "download_log_evidence_status": "not_collected",
        "package_manifest_evidence_status": "not_collected",
        "metadata_profile_evidence_status": "not_collected",
        "graph_edge_evidence_status": "not_collected",
        "staging_row_evidence_status": "not_collected",
        "counter_source_lookup_status": "not_collected",
        "rights_risk_review_status": "not_collected",
        "review_log_status": "not_collected",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
        "next_artifact_recommendation": "not_collected",
        "research_boundary": "evidence_collection_result_scaffold_not_scholarship",
        "output_scope": "graph_source_evidence_collection_result_scaffold_only",
        "updated_at": "2026-06-10",
    }
    if [row.get("source_id", "") for row in result_rows] != [
        str(row.get("source_id", ""))
        for row in note_routes
        if isinstance(row, dict)
    ]:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} source order changed")
    if [row.get("target_evidence_section", "") for row in result_rows] != [
        str(row.get("target_evidence_section", ""))
        for row in note_routes
        if isinstance(row, dict)
    ]:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} section order changed")
    for index, row in enumerate(result_rows, start=1):
        result_id = row.get("evidence_collection_result_id", "")
        task_id = row.get("evidence_collection_task_id", "")
        route_row = route_rows_by_task.get(task_id, {})
        if result_id != f"graph-source-evidence-result-{index:03d}":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"result ID sequence changed: {result_id}"
            )
        if task_id != f"graph-source-evidence-task-{index:03d}":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"task link sequence changed: {result_id}"
            )
        if not route_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"missing route-pack link: {result_id}"
            )
            continue
        for linked_field in [
            "evidence_collection_note_draft_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "note_draft_path",
            "manifest_path",
            "task_queue_source_path",
        ]:
            if row.get(linked_field) != str(route_row.get(linked_field, "")):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                    f"{linked_field} does not match route pack: {result_id}"
                )
        if row.get("context_pack_id") != route_pack.get("context_pack_id"):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"context_pack_id changed: {result_id}"
            )
        if row.get("route_pack_path") != AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"route_pack_path changed: {result_id}"
            )
        if row.get("route_files_to_open") != ";".join(
            str(value) for value in route_row.get("route_files_to_open", [])
        ):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"route files changed: {result_id}"
            )
        if row.get("counter_source_ids_to_check") != ";".join(
            str(value) for value in route_row.get("counter_source_ids_to_check", [])
        ):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"counter sources changed: {result_id}"
            )
        expected_action = expected_section_actions.get(row.get("target_evidence_section", ""))
        if row.get("required_collection_action") != expected_action:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                f"collection action changed: {result_id}"
            )
        for key, expected_value in expected_result_status_values.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                    f"{key} changed: {result_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "empty graph-source evidence collection result scaffold",
            "remain not_collected",
            "Do not use it as collected evidence",
            "rights decision",
            "source promotion decision",
            "component or evolution-chain assignment",
            "decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD} "
                    f"missing caution {required_snippet}: {result_id}"
                )

    review_queue_rows, review_queue_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE
    )
    issues.extend(review_queue_issues)
    if len(review_queue_rows) != 27:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
            "should contain exactly 27 rows"
        )
    result_rows_by_id = {
        row.get("evidence_collection_result_id", ""): row
        for row in result_rows
    }
    expected_review_status_values = {
        "result_scaffold_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
        "result_update_target_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
        "assignment_status": "unassigned",
        "review_status": "needs_evidence_collection_review",
        "evidence_collection_status": "not_collected",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
        "research_boundary": "evidence_collection_review_queue_not_scholarship",
        "output_scope": "graph_source_evidence_collection_review_queue_only",
        "updated_at": "2026-06-10",
    }
    expected_review_priorities = {
        "source_register": "1",
        "download_log": "2",
        "package_manifest": "3",
        "metadata_profile": "4",
        "rights_risk_review": "5",
        "graph_edges": "6",
        "staging_row": "7",
        "counter_source_lookup": "8",
        "review_log": "9",
    }
    expected_review_sections = [
        "source_register",
        "download_log",
        "package_manifest",
        "metadata_profile",
        "graph_edges",
        "staging_row",
        "counter_source_lookup",
        "rights_risk_review",
        "review_log",
    ]
    expected_priority_sections = list(expected_review_priorities)
    if [row.get("source_id", "") for row in review_queue_rows] != [
        row.get("source_id", "")
        for row in result_rows
    ]:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} source order changed")
    if [row.get("target_evidence_section", "") for row in review_queue_rows] != [
        row.get("target_evidence_section", "")
        for row in result_rows
    ]:
        issues.append(f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} section order changed")
    for index, row in enumerate(review_queue_rows, start=1):
        review_task_id = row.get("evidence_collection_review_task_id", "")
        result_id = row.get("evidence_collection_result_id", "")
        result_row = result_rows_by_id.get(result_id, {})
        if review_task_id != f"graph-source-evidence-review-{index:03d}":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                f"review task ID sequence changed: {review_task_id}"
            )
        if result_id != f"graph-source-evidence-result-{index:03d}":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                f"result link sequence changed: {review_task_id}"
            )
        if not result_row:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                f"missing result-scaffold link: {review_task_id}"
            )
            continue
        for linked_field in [
            "evidence_collection_note_draft_id",
            "evidence_collection_task_id",
            "context_pack_id",
            "source_id",
            "primary_review_record_id",
            "primary_external_ref_id",
            "source_record_id",
            "target_evidence_section",
            "required_collection_action",
            "note_draft_path",
            "route_pack_path",
            "manifest_path",
            "task_queue_source_path",
            "counter_source_ids_to_check",
        ]:
            if row.get(linked_field) != result_row.get(linked_field):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                    f"{linked_field} does not match result scaffold: {review_task_id}"
                )
        section = row.get("target_evidence_section", "")
        if row.get("priority_rank") != expected_review_priorities.get(section):
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                f"priority changed: {review_task_id}"
            )
        priority_tags = set(filter(None, row.get("priority_tags", "").split(";")))
        for required_tag in {f"section:{section}", f"source:{row.get('source_id', '')}"}:
            if required_tag not in priority_tags:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                    f"missing priority tag {required_tag}: {review_task_id}"
                )
        required_checks = set(filter(None, row.get("required_review_checks", "").split(";")))
        for required_check in [
            "keep_result_row_not_collected_until_evidence_is_source_marked",
            "do_not_write_ai_hypothesis_as_scholarship",
        ]:
            if required_check not in required_checks:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                    f"missing review check {required_check}: {review_task_id}"
                )
        route_files = set(filter(None, row.get("route_files_to_open", "").split(";")))
        for required_file in [
            row.get("route_pack_path", ""),
            row.get("manifest_path", ""),
            row.get("task_queue_source_path", ""),
            row.get("note_draft_path", ""),
        ]:
            if required_file not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                    f"missing route file {required_file}: {review_task_id}"
                )
        for key, expected_value in expected_review_status_values.items():
            if row.get(key) != expected_value:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                    f"{key} changed: {review_task_id}"
                )
        caution = row.get("caution", "")
        for required_snippet in [
            "AI Agent evidence-collection review queue item only",
            "before recording any evidence",
            "Do not use this queue as collected evidence",
            "rights decision",
            "source promotion decision",
            "component or evolution-chain assignment",
            "decipherment conclusion",
        ]:
            if required_snippet not in caution:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE} "
                    f"missing caution {required_snippet}: {review_task_id}"
                )

    try:
        review_summary = json.loads(
            (root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY)
            .read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        return issues + [
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            f"invalid JSON: {exc.msg}"
        ]
    expected_summary_values = {
        "context_pack_id": "ai-context-graph-source-evidence-collection-review-summary-001",
        "status": "draft_review_route_summary_not_collected",
        "updated_at": "2026-06-10",
        "research_boundary": "evidence_collection_review_route_summary_not_scholarship",
    }
    for key, expected_value in expected_summary_values.items():
        if review_summary.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                f"{key} changed"
            )
    if review_summary.get("generated_from") != [
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK,
    ]:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "generated_from changed"
        )
    summary_coverage = review_summary.get("coverage", {})
    expected_summary_coverage = {
        "review_task_count": 27,
        "source_count": 3,
        "target_evidence_section_count": 9,
        "route_file_reference_count": 154,
        "unique_route_file_count": 57,
        "counter_source_reference_count": 144,
        "unique_counter_source_count": 6,
    }
    for key, expected_value in expected_summary_coverage.items():
        if summary_coverage.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                f"coverage {key} changed"
            )
    if summary_coverage.get("source_counts") != {
        "src-hust-obc": 9,
        "src-evobc": 9,
        "src-obimd": 9,
    }:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "source counts changed"
        )
    if summary_coverage.get("section_counts") != {
        "source_register": 3,
        "download_log": 3,
        "package_manifest": 3,
        "metadata_profile": 3,
        "graph_edges": 3,
        "staging_row": 3,
        "counter_source_lookup": 3,
        "rights_risk_review": 3,
        "review_log": 3,
    }:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "section counts changed"
        )
    for key, expected_counts in {
        "assignment_status_counts": {"unassigned": 27},
        "review_status_counts": {"needs_evidence_collection_review": 27},
        "evidence_collection_status_counts": {"not_collected": 27},
        "source_promotion_status_counts": {"not_promoted": 27},
        "decipherment_claim_status_counts": {"no_claim": 27},
        "research_boundary_counts": {"evidence_collection_review_queue_not_scholarship": 27},
        "output_scope_counts": {"graph_source_evidence_collection_review_queue_only": 27},
    }.items():
        if summary_coverage.get(key) != expected_counts:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                f"{key} changed"
            )
    if summary_coverage.get("priority_rank_counts") != {
        str(rank): 3 for rank in range(1, 10)
    }:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "priority counts changed"
        )
    route_file_summary = review_summary.get("route_file_summary", {})
    for key, expected_value in {
        "review_queue_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE,
        "result_scaffold_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
        "route_pack_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK,
    }.items():
        if route_file_summary.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                f"route file summary {key} changed"
            )
    if len(route_file_summary.get("route_files_to_open", [])) != 57:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "unique route file list changed"
        )
    source_summaries = review_summary.get("source_summaries", [])
    if [row.get("source_id") for row in source_summaries] != [
        "src-hust-obc",
        "src-evobc",
        "src-obimd",
    ]:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "source summary order changed"
        )
    else:
        expected_source_route_counts = {
            "src-hust-obc": 32,
            "src-evobc": 29,
            "src-obimd": 30,
        }
        for row in source_summaries:
            source_id = row.get("source_id", "")
            if row.get("review_task_count") != 9:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"source task count changed: {source_id}"
                )
            if row.get("target_evidence_sections") != expected_review_sections:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"source sections changed: {source_id}"
                )
            if row.get("min_priority_rank") != 1 or row.get("max_priority_rank") != 9:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"source priority range changed: {source_id}"
                )
            if row.get("route_file_count") != expected_source_route_counts.get(source_id):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"source route file count changed: {source_id}"
                )
            if row.get("result_update_targets") != [
                AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD
            ]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"source result target changed: {source_id}"
                )
    section_summaries = review_summary.get("section_summaries", [])
    if [row.get("target_evidence_section") for row in section_summaries] != expected_review_sections:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
            "section summary order changed"
        )
    else:
        for row in section_summaries:
            section = row.get("target_evidence_section", "")
            if row.get("review_task_count") != 3:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"section task count changed: {section}"
                )
            if row.get("source_ids") != ["src-hust-obc", "src-evobc", "src-obimd"]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"section source order changed: {section}"
                )
            if row.get("priority_rank") != expected_review_priorities.get(section):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"section priority changed: {section}"
                )
            if row.get("required_review_check_count") != 12:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                    f"section review check count changed: {section}"
                )
    summary_rules = " ".join(review_summary.get("agent_use_rules", []))
    summary_rules_zh = " ".join(review_summary.get("agent_use_rules_zh", []))
    for required_snippet in [
        "choose an evidence-collection review route",
        "Open the 028 queue row",
        "Do not treat this summary as collected evidence",
        "ignored temporary directories",
    ]:
        if required_snippet not in summary_rules:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                f"missing agent rule: {required_snippet}"
            )
    for required_snippet in [
        "只能用于选择证据收集复核路由",
        "必须打开 028 队列行",
        "不得把本摘要当作已收集证据",
        "已忽略临时目录",
    ]:
        if required_snippet not in summary_rules_zh:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY} "
                f"missing zh agent rule: {required_snippet}"
            )

    try:
        assignment_plan = json.loads(
            (root / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN)
            .read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        return issues + [
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            f"invalid JSON: {exc.msg}"
        ]
    expected_assignment_values = {
        "context_pack_id": "ai-context-graph-source-evidence-collection-assignment-plan-001",
        "status": "draft_assignment_plan_not_started",
        "updated_at": "2026-06-10",
        "research_boundary": "evidence_collection_assignment_plan_not_scholarship",
        "output_scope": "graph_source_evidence_collection_assignment_plan_only",
        "upstream_context_pack_id": "ai-context-graph-source-evidence-collection-review-summary-001",
    }
    for key, expected_value in expected_assignment_values.items():
        if assignment_plan.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                f"{key} changed"
            )
    if assignment_plan.get("generated_from") != [
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK,
    ]:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            "generated_from changed"
        )
    assignment_coverage = assignment_plan.get("coverage", {})
    expected_assignment_coverage = {
        "review_task_count": 27,
        "assignment_item_count": 27,
        "assignment_wave_count": 9,
        "source_workstream_count": 3,
        "source_count": 3,
        "target_evidence_section_count": 9,
        "route_file_reference_count": 154,
        "unique_route_file_count": 57,
        "counter_source_reference_count": 144,
        "unique_counter_source_count": 6,
    }
    for key, expected_value in expected_assignment_coverage.items():
        if assignment_coverage.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                f"coverage {key} changed"
            )
    if assignment_coverage.get("source_counts") != {
        "src-hust-obc": 9,
        "src-evobc": 9,
        "src-obimd": 9,
    }:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            "source counts changed"
        )
    if assignment_coverage.get("section_counts") != {
        section: 3 for section in expected_priority_sections
    }:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            "section counts changed"
        )
    for key, expected_counts in {
        "assignment_status_counts": {"planned_not_assigned": 27},
        "review_status_counts": {"needs_evidence_collection_review": 27},
        "evidence_collection_status_counts": {"not_collected": 27},
        "source_promotion_status_counts": {"not_promoted": 27},
        "decipherment_claim_status_counts": {"no_claim": 27},
    }.items():
        if assignment_coverage.get(key) != expected_counts:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                f"{key} changed"
            )
    assignment_waves = assignment_plan.get("assignment_waves", [])
    if [row.get("target_evidence_section") for row in assignment_waves] != expected_priority_sections:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            "wave section order changed"
        )
    else:
        for index, row in enumerate(assignment_waves, start=1):
            wave_id = row.get("assignment_wave_id", "")
            if wave_id != f"graph-source-evidence-assignment-wave-{index:03d}":
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"wave ID sequence changed: {wave_id}"
                )
            if row.get("priority_rank") != str(index):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"wave priority changed: {wave_id}"
                )
            if row.get("assignment_item_count") != 3:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"wave count changed: {wave_id}"
                )
            if row.get("source_ids") != ["src-hust-obc", "src-evobc", "src-obimd"]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"wave source order changed: {wave_id}"
                )
            for key, expected_value in {
                "assignment_status": "planned_not_assigned",
                "evidence_collection_status": "not_collected",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
            }.items():
                if row.get(key) != expected_value:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                        f"wave {key} changed: {wave_id}"
                    )
    source_workstreams = assignment_plan.get("source_workstreams", [])
    if [row.get("source_id") for row in source_workstreams] != [
        "src-hust-obc",
        "src-evobc",
        "src-obimd",
    ]:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            "source workstream order changed"
        )
    else:
        expected_source_route_counts = {
            "src-hust-obc": 32,
            "src-evobc": 29,
            "src-obimd": 30,
        }
        for row in source_workstreams:
            source_id = row.get("source_id", "")
            if row.get("assignment_item_count") != 9:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"source item count changed: {source_id}"
                )
            if row.get("target_evidence_sections") != expected_priority_sections:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"source sections changed: {source_id}"
                )
            if row.get("min_priority_rank") != 1 or row.get("max_priority_rank") != 9:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"source priority range changed: {source_id}"
                )
            if row.get("route_file_count") != expected_source_route_counts.get(source_id):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"source route file count changed: {source_id}"
                )
    assignment_items = assignment_plan.get("assignment_items", [])
    if not isinstance(assignment_items, list) or len(assignment_items) != 27:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
            "should contain 27 assignment items"
        )
    else:
        if assignment_items[0].get("evidence_collection_review_task_id") != "graph-source-evidence-review-001":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                "first assignment review task changed"
            )
        if assignment_items[1].get("evidence_collection_review_task_id") != "graph-source-evidence-review-010":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                "second assignment review task changed"
            )
        if assignment_items[2].get("evidence_collection_review_task_id") != "graph-source-evidence-review-019":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                "third assignment review task changed"
            )
        if assignment_items[-1].get("evidence_collection_review_task_id") != "graph-source-evidence-review-027":
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                "last assignment review task changed"
            )
        for index, row in enumerate(assignment_items, start=1):
            item_id = row.get("assignment_plan_item_id", "")
            if item_id != f"graph-source-evidence-assignment-{index:03d}":
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"assignment item ID sequence changed: {item_id}"
                )
            for key, expected_value in {
                "assignment_status": "planned_not_assigned",
                "review_status": "needs_evidence_collection_review",
                "evidence_collection_status": "not_collected",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
            }.items():
                if row.get(key) != expected_value:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                        f"{key} changed: {item_id}"
                    )
            route_files = row.get("route_files_to_open", [])
            if row.get("note_draft_path") not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"assignment missing note draft route: {item_id}"
                )
            if row.get("route_pack_path") not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"assignment missing route pack: {item_id}"
                )
            if row.get("manifest_path") not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                    f"assignment missing manifest: {item_id}"
                )
    assignment_rules = " ".join(assignment_plan.get("agent_use_rules", []))
    assignment_rules_zh = " ".join(assignment_plan.get("agent_use_rules_zh", []))
    for required_snippet in [
        "only to choose the next planned review route",
        "Open the 030 plan item",
        "planned_not_assigned",
        "Do not treat this plan as collected evidence",
        "ignored temporary directories",
    ]:
        if required_snippet not in assignment_rules:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                f"missing agent rule: {required_snippet}"
            )
    for required_snippet in [
        "只能用于选择下一条计划中的复核路由",
        "必须打开 030 计划项",
        "planned_not_assigned",
        "不得把本计划当作已收集证据",
        "已忽略临时目录",
    ]:
        if required_snippet not in assignment_rules_zh:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN} "
                f"missing zh agent rule: {required_snippet}"
            )

    try:
        handoff_scaffold = json.loads(
            (
                root
                / AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD
            ).read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        return issues + [
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
            f"invalid JSON: {exc.msg}"
        ]
    expected_handoff_values = {
        "context_pack_id": "ai-context-graph-source-evidence-collection-wave-handoff-001",
        "status": "draft_wave_handoff_scaffold_not_started",
        "updated_at": "2026-06-10",
        "research_boundary": "evidence_collection_wave_handoff_scaffold_not_scholarship",
        "output_scope": "graph_source_evidence_collection_wave_handoff_scaffold_only",
        "upstream_context_pack_id": "ai-context-graph-source-evidence-collection-assignment-plan-001",
    }
    for key, expected_value in expected_handoff_values.items():
        if handoff_scaffold.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                f"{key} changed"
            )
    if handoff_scaffold.get("generated_from") != [
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ASSIGNMENT_PLAN,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_ROUTE_SUMMARY,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_REVIEW_QUEUE,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_RESULT_SCAFFOLD,
        AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_ROUTE_PACK,
    ]:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
            "generated_from changed"
        )
    handoff_scope = handoff_scaffold.get("handoff_scope", {})
    expected_handoff_scope = {
        "assignment_wave_id": "graph-source-evidence-assignment-wave-001",
        "target_evidence_section": "source_register",
        "priority_rank": "1",
        "source_ids": ["src-hust-obc", "src-evobc", "src-obimd"],
        "assignment_plan_item_ids": [
            "graph-source-evidence-assignment-001",
            "graph-source-evidence-assignment-002",
            "graph-source-evidence-assignment-003",
        ],
        "review_task_ids": [
            "graph-source-evidence-review-001",
            "graph-source-evidence-review-010",
            "graph-source-evidence-review-019",
        ],
        "handoff_status": "ready_for_source_register_evidence_collection_not_started",
        "assignment_status": "planned_not_assigned",
        "evidence_collection_status": "not_collected",
        "source_promotion_status": "not_promoted",
        "decipherment_claim_status": "no_claim",
    }
    for key, expected_value in expected_handoff_scope.items():
        if handoff_scope.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                f"handoff scope {key} changed"
            )
    handoff_coverage = handoff_scaffold.get("coverage", {})
    expected_handoff_coverage = {
        "handoff_item_count": 3,
        "assignment_wave_count": 1,
        "assignment_item_count": 3,
        "review_task_count": 3,
        "source_count": 3,
        "target_evidence_section_count": 1,
        "route_file_reference_count": 15,
        "unique_route_file_count": 7,
        "counter_source_reference_count": 16,
        "unique_counter_source_count": 6,
        "required_review_check_reference_count": 12,
        "unique_required_review_check_count": 4,
    }
    for key, expected_value in expected_handoff_coverage.items():
        if handoff_coverage.get(key) != expected_value:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                f"coverage {key} changed"
            )
    if handoff_coverage.get("source_counts") != {
        "src-evobc": 1,
        "src-hust-obc": 1,
        "src-obimd": 1,
    }:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
            "source counts changed"
        )
    if handoff_coverage.get("section_counts") != {"source_register": 3}:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
            "section counts changed"
        )
    for key, expected_counts in {
        "handoff_status_counts": {
            "ready_for_source_register_evidence_collection_not_started": 3
        },
        "assignment_status_counts": {"planned_not_assigned": 3},
        "review_status_counts": {"needs_evidence_collection_review": 3},
        "evidence_collection_status_counts": {"not_collected": 3},
        "source_promotion_status_counts": {"not_promoted": 3},
        "decipherment_claim_status_counts": {"no_claim": 3},
        "rights_decision_status_counts": {"not_decided": 3},
        "source_register_evidence_status_counts": {"not_collected": 3},
    }.items():
        if handoff_coverage.get(key) != expected_counts:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                f"{key} changed"
            )
    if handoff_scaffold.get("route_files_to_open", [])[0] != (
        "corpus/006_research-sources-and-bibliography/"
        "000_source-registers/001_all-sources-index.csv"
    ):
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
            "source register route missing from top-level route files"
        )
    handoff_items = handoff_scaffold.get("handoff_items", [])
    if not isinstance(handoff_items, list) or len(handoff_items) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
            "should contain 3 handoff items"
        )
    else:
        expected_sources = ["src-hust-obc", "src-evobc", "src-obimd"]
        expected_review_tasks = [
            "graph-source-evidence-review-001",
            "graph-source-evidence-review-010",
            "graph-source-evidence-review-019",
        ]
        for index, row in enumerate(handoff_items, start=1):
            item_id = row.get("handoff_item_id", "")
            if item_id != f"graph-source-evidence-handoff-{index:03d}":
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                    f"handoff item ID sequence changed: {item_id}"
                )
            if row.get("source_id") != expected_sources[index - 1]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                    f"handoff source order changed: {item_id}"
                )
            if row.get("evidence_collection_review_task_id") != expected_review_tasks[index - 1]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                    f"handoff review task changed: {item_id}"
                )
            for key, expected_value in {
                "assignment_wave_id": "graph-source-evidence-assignment-wave-001",
                "target_evidence_section": "source_register",
                "handoff_status": "ready_for_source_register_evidence_collection_not_started",
                "assignment_status": "planned_not_assigned",
                "review_status": "needs_evidence_collection_review",
                "evidence_collection_status": "not_collected",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
                "rights_decision_status": "not_decided",
                "source_register_evidence_status": "not_collected",
                "research_boundary": "evidence_collection_wave_handoff_scaffold_not_scholarship",
                "output_scope": "graph_source_evidence_collection_wave_handoff_scaffold_only",
            }.items():
                if row.get(key) != expected_value:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                        f"{key} changed: {item_id}"
                    )
            route_files = row.get("route_files_to_open", [])
            for required_path in [
                row.get("note_draft_path"),
                row.get("route_pack_path"),
                row.get("manifest_path"),
                row.get("task_queue_source_path"),
            ]:
                if required_path not in route_files:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                        f"handoff missing route file: {item_id}"
                    )
    handoff_rules = " ".join(handoff_scaffold.get("agent_use_rules", []))
    handoff_rules_zh = " ".join(handoff_scaffold.get("agent_use_rules_zh", []))
    for required_snippet in [
        "only to open the first source_register",
        "Open the 031 handoff row",
        "not_collected",
        "Do not treat this scaffold as collected evidence",
        "ignored temporary directories",
    ]:
        if required_snippet not in handoff_rules:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                f"missing agent rule: {required_snippet}"
            )
    for required_snippet in [
        "只能用于打开第一波 source_register",
        "必须打开 031 交接行",
        "not_collected",
        "不得把本脚手架当作已收集证据",
        "已忽略临时目录",
    ]:
        if required_snippet not in handoff_rules_zh:
            issues.append(
                f"{AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD} "
                f"missing zh agent rule: {required_snippet}"
            )

    capture_rows, capture_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD
    )
    issues.extend(capture_issues)
    if len(capture_rows) != 3:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
            "should contain 3 source-register capture rows"
        )
    else:
        expected_sources = ["src-hust-obc", "src-evobc", "src-obimd"]
        expected_handoff_ids = [
            "graph-source-evidence-handoff-001",
            "graph-source-evidence-handoff-002",
            "graph-source-evidence-handoff-003",
        ]
        expected_review_tasks = [
            "graph-source-evidence-review-001",
            "graph-source-evidence-review-010",
            "graph-source-evidence-review-019",
        ]
        empty_evidence_fields = [
            "source_id_evidence_value",
            "primary_external_ref_evidence_value",
            "source_title_evidence_value",
            "source_type_evidence_value",
            "rights_status_evidence_value",
            "risk_note_evidence_value",
            "review_status_evidence_value",
        ]
        for index, row in enumerate(capture_rows, start=1):
            row_id = row.get("capture_row_id", "")
            if row_id != f"graph-source-evidence-source-register-capture-{index:03d}":
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                    f"capture row ID sequence changed: {row_id}"
                )
            if row.get("handoff_item_id") != expected_handoff_ids[index - 1]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                    f"handoff item changed: {row_id}"
                )
            if row.get("source_id") != expected_sources[index - 1]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                    f"source order changed: {row_id}"
                )
            if row.get("evidence_collection_review_task_id") != expected_review_tasks[index - 1]:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                    f"review task changed: {row_id}"
                )
            for key, expected_value in {
                "assignment_wave_id": "graph-source-evidence-assignment-wave-001",
                "target_evidence_section": "source_register",
                "source_register_path": SOURCE_INDEX,
                "source_register_row_status": "not_checked",
                "evidence_collection_status": "not_collected",
                "source_register_evidence_status": "not_collected",
                "rights_decision_status": "not_decided",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
                "capture_status": "empty_scaffold_not_started",
                "updated_at": "2026-06-10",
                "handoff_scaffold_path": AI_AGENT_GRAPH_SOURCE_EVIDENCE_COLLECTION_WAVE_HANDOFF_SCAFFOLD,
                "research_boundary": "evidence_collection_source_register_capture_scaffold_not_scholarship",
                "output_scope": "graph_source_evidence_collection_source_register_capture_scaffold_only",
            }.items():
                if row.get(key) != expected_value:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                        f"{key} changed: {row_id}"
                    )
            for fieldname in empty_evidence_fields:
                if row.get(fieldname) != "":
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                        f"{fieldname} should remain empty: {row_id}"
                    )
            route_files = row.get("route_files_to_open", "").split(";")
            for required_path in [
                SOURCE_INDEX,
                row.get("note_draft_path", ""),
                row.get("route_pack_path", ""),
                row.get("manifest_path", ""),
                row.get("task_queue_source_path", ""),
            ]:
                if required_path not in route_files:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                        f"missing route file: {row_id}"
                    )
            required_checks = row.get("required_review_checks", "")
            for required_snippet in [
                "open_source_register_row_before_copying_provenance",
                "record_source_id_external_ref_and_review_status_only",
                "keep_result_row_not_collected_until_evidence_is_source_marked",
                "do_not_write_ai_hypothesis_as_scholarship",
            ]:
                if required_snippet not in required_checks:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                        f"missing required review check: {row_id}"
                    )
            caution = row.get("caution", "")
            for required_snippet in [
                "Empty capture scaffold",
                "do not use it as collected evidence",
                "rights decision",
                "decipherment conclusion",
            ]:
                if required_snippet not in caution:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD} "
                        f"missing caution text: {row_id}"
                    )

    checklist_rows, checklist_issues = _read_csv_rows(
        root / AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST
    )
    issues.extend(checklist_issues)
    expected_check_keys = [
        "open_capture_row",
        "open_source_register_row",
        "verify_primary_external_ref",
        "verify_title_and_type",
        "verify_rights_and_risk",
        "keep_capture_boundary",
        "block_source_promotion",
        "block_decipherment_claim",
    ]
    if len(checklist_rows) != 24:
        issues.append(
            f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
            "should contain 24 checklist rows"
        )
    else:
        expected_capture_ids = [
            "graph-source-evidence-source-register-capture-001",
            "graph-source-evidence-source-register-capture-002",
            "graph-source-evidence-source-register-capture-003",
        ]
        expected_sources_by_capture = {
            "graph-source-evidence-source-register-capture-001": "src-hust-obc",
            "graph-source-evidence-source-register-capture-002": "src-evobc",
            "graph-source-evidence-source-register-capture-003": "src-obimd",
        }
        rows_by_capture: dict[str, list[dict[str, str]]] = {
            capture_id: [] for capture_id in expected_capture_ids
        }
        for index, row in enumerate(checklist_rows, start=1):
            row_id = row.get("checklist_item_id", "")
            capture_id = row.get("capture_row_id", "")
            if row_id != f"graph-source-evidence-source-register-check-{index:03d}":
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"checklist row ID sequence changed: {row_id}"
                )
            if capture_id in rows_by_capture:
                rows_by_capture[capture_id].append(row)
            if row.get("source_id") != expected_sources_by_capture.get(capture_id):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"source changed: {row_id}"
                )
            for key, expected_value in {
                "target_evidence_section": "source_register",
                "check_status": "not_started",
                "review_status": "needs_source_register_capture_review",
                "evidence_collection_status": "not_collected",
                "rights_decision_status": "not_decided",
                "source_promotion_status": "not_promoted",
                "decipherment_claim_status": "no_claim",
                "source_register_path": SOURCE_INDEX,
                "capture_scaffold_path": AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_EVIDENCE_CAPTURE_SCAFFOLD,
                "updated_at": "2026-06-10",
                "research_boundary": "evidence_collection_source_register_capture_review_checklist_not_scholarship",
                "output_scope": "graph_source_evidence_collection_source_register_capture_review_checklist_only",
            }.items():
                if row.get(key) != expected_value:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                        f"{key} changed: {row_id}"
                    )
            route_files = row.get("route_files_to_open", "").split(";")
            if SOURCE_INDEX not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"missing source register route: {row_id}"
                )
            if row.get("note_draft_path", "") not in route_files:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"missing note draft route: {row_id}"
                )
            if "do_not_write_ai_hypothesis_as_scholarship" not in row.get(
                "required_review_checks", ""
            ):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"missing no-hypothesis check: {row_id}"
                )
            caution = row.get("caution", "")
            for required_snippet in [
                "Checklist item only",
                "does not contain collected evidence",
                "rights decision",
                "decipherment conclusion",
            ]:
                if required_snippet not in caution:
                    issues.append(
                        f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                        f"missing caution text: {row_id}"
                    )
            if not row.get("instruction") or not row.get("instruction_zh"):
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"missing bilingual instruction: {row_id}"
                )
        for capture_id, rows in rows_by_capture.items():
            if [row.get("check_key") for row in rows] != expected_check_keys:
                issues.append(
                    f"{AI_AGENT_GRAPH_SOURCE_SOURCE_REGISTER_CAPTURE_REVIEW_CHECKLIST} "
                    f"check order changed: {capture_id}"
                )

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
    smithsonian_object_rows, smithsonian_object_issues = _read_csv_rows(
        root / SMITHSONIAN_NMAA_OBJECT_STAGING
    )
    penn_museum_object_rows, penn_museum_object_issues = _read_csv_rows(
        root / PENN_MUSEUM_OBJECT_STAGING
    )
    metmuseum_object_rows, metmuseum_object_issues = _read_csv_rows(
        root / METMUSEUM_OBJECT_STAGING
    )
    download_status_rows, download_status_issues = _read_csv_rows(
        root / SOURCE_DOWNLOAD_STATUS_CODEBOOK
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
        + smithsonian_object_issues
        + penn_museum_object_issues
        + metmuseum_object_issues
        + download_status_issues
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

    status_rows_by_code = {row.get("status_code", ""): row for row in download_status_rows}
    required_status_codes = {
        "downloaded",
        "downloaded_access_restricted_page",
        "downloaded_client_challenge_page",
        "download_error",
        "http_error",
        "skipped_exceeds_manifest_limit",
    }
    for status_code in sorted(required_status_codes - set(status_rows_by_code)):
        issues.append(f"{SOURCE_DOWNLOAD_STATUS_CODEBOOK} missing status_code: {status_code}")
    for row in download_status_rows:
        status_code = row.get("status_code", "")
        if row.get("review_status") != "reviewed":
            issues.append(f"{SOURCE_DOWNLOAD_STATUS_CODEBOOK} row not reviewed: {status_code}")
        if row.get("can_support_source_existence") not in {"true", "false"}:
            issues.append(f"{SOURCE_DOWNLOAD_STATUS_CODEBOOK} existence flag must be boolean: {status_code}")
        if row.get("can_support_payload_extracted") not in {"true", "false"}:
            issues.append(f"{SOURCE_DOWNLOAD_STATUS_CODEBOOK} payload flag must be boolean: {status_code}")
    for status_code in sorted({row.get("status", "") for row in log_rows} - set(status_rows_by_code)):
        issues.append(f"{SOURCE_DOWNLOAD_LOG} status not defined in codebook: {status_code}")
    for status_code in ["download_error", "downloaded_access_restricted_page", "skipped_exceeds_manifest_limit"]:
        row = status_rows_by_code.get(status_code, {})
        if row.get("can_support_payload_extracted") != "false":
            issues.append(f"{SOURCE_DOWNLOAD_STATUS_CODEBOOK} {status_code} must not support payload extraction")
    if "Do not treat download_error as proof" not in " ".join(
        row.get("caution_en", "") for row in download_status_rows
    ):
        issues.append(f"{SOURCE_DOWNLOAD_STATUS_CODEBOOK} missing download_error caution")

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
        "nlc_oracle_world_objects=2964",
        "object_images=5932",
        "rubbings=2975",
        "rubbing_images=3177",
        "nlc_oracle_bone_holding_count=35651",
        "nlc_field_contract=holding_number",
        "nlc_heji_refs_over_8000",
        "nlc_yinqi_cuibian_refs=1595",
        "FS-FSC-O-26_1",
        "CC0",
        "penn_museum_object_number=49-14-7A",
        "provenience=Anyang",
        "period=Shang_Dynasty",
        "penn_museum_materials=Bone;Shell",
        "credit_line_julia_morgan_hugh_morgan_1949",
        "metmuseum_object_id=42045",
        "accession=67.43.14",
        "metmuseum_object_id=42022",
        "accession=18.56.71",
        "metmuseum_primary_image_urls_available_for_public_domain_objects",
        "xiaoxuetang_portal_scope=glyphs_over_180000",
        "phonology_over_1000000",
        "dictionary_indexes_over_250000",
        "covers_oracle_bone_bronze_warring_states_seal_regular",
        "xiaoxuetang_portal_rights_holders=ntu_chinese_ihp_iis",
        "yinshang_oracle_vocab_pieces=52486",
        "characters_about_1000000",
        "major_corpora=heji_xiaotun_nandi_yingguo_tokyo_whitney",
        "yinshang_oracle_vocab_topics=astronomy_calendar_weather_geography_polities",
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

    if len(smithsonian_object_rows) != 1:
        issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} should contain exactly 1 sample object row")
    for row in smithsonian_object_rows:
        candidate_id = row.get("candidate_collection_object_id", "")
        if candidate_id != "si-nmaa-obj-00001":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} sample candidate ID changed")
        if row.get("source_id") != "src-smithsonian-nmaa-oracle-bone":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} row must reference Smithsonian source")
        if row.get("evidence_download_id") != "dl-smithsonian-nmaa-fsc-o-26-archive":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} row must cite FSC-O-26 archive download")
        if row.get("source_collection_item_id") != "FSC-O-26":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} source collection item ID changed")
        if row.get("accession_number") != "FSC-O-26":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} accession number changed")
        if row.get("iiif_source_image_id") != "FS-FSC-O-26_1":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} IIIF source image ID changed")
        if row.get("rights_status") != "public_domain_verified":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} rights status must stay public_domain_verified")
        if row.get("iiif_manifest_status") != "public_domain_image_committed_as_asset_000003":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} row must reference committed asset-000003")
        if row.get("project_import_status") != "object_metadata_not_promoted":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} row must stay object_metadata_not_promoted")
        if "John Hadley Cox" not in row.get("provenance_note", ""):
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} provenance note missing John Hadley Cox")
        if "CC0 IIIF image is committed as asset-000003" not in row.get("caution", ""):
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} caution must state asset-000003 is committed")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{SMITHSONIAN_NMAA_OBJECT_STAGING} row not reviewed_metadata_only")

    if len(penn_museum_object_rows) != 1:
        issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} should contain exactly 1 sample object row")
    for row in penn_museum_object_rows:
        candidate_id = row.get("candidate_collection_object_id", "")
        if candidate_id != "penn-mus-obj-00001":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} sample candidate ID changed")
        if row.get("source_id") != "src-penn-museum-oracle-bone":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} row must reference Penn Museum source")
        if row.get("evidence_download_id") != "dl-penn-museum-49-14-7a":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} row must cite Penn Museum object download")
        if row.get("source_collection_item_id") != "49-14-7A":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} object number changed")
        if row.get("accession_number") != "49-14-7A":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} accession number changed")
        if row.get("provenience") != "Anyang":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} provenience changed")
        if row.get("historical_period") != "Shang Dynasty":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} historical period changed")
        if row.get("materials") != "Bone;Shell":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} materials changed")
        if row.get("dimensions") != "height_cm=2.3;width_cm=2.5":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} dimensions changed")
        if row.get("project_import_status") != "object_metadata_not_promoted":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} row must stay object_metadata_not_promoted")
        if row.get("rights_status") != "metadata_only_until_verified":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} rights status must stay metadata_only_until_verified")
        if "raw object images are not downloaded" not in row.get("caution", "").lower():
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} caution must state raw images are not downloaded")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{PENN_MUSEUM_OBJECT_STAGING} row not reviewed_metadata_only")

    if len(metmuseum_object_rows) != 2:
        issues.append(f"{METMUSEUM_OBJECT_STAGING} should contain exactly 2 sample object rows")
    expected_met_rows = {
        "met-obj-00001": {
            "download_id": "dl-metmuseum-object-42045",
            "source_collection_item_id": "42045",
            "accession_number": "67.43.14",
            "title": "Oracle bone",
            "medium": "Inscribed bone",
            "image_suffix": "LC-67_43_14_002.jpg",
        },
        "met-obj-00002": {
            "download_id": "dl-metmuseum-object-42022",
            "source_collection_item_id": "42022",
            "accession_number": "18.56.71",
            "title": "Oracle Bone Fragment",
            "medium": "Bone",
            "image_suffix": "LC-18_56_71_002.jpg",
        },
    }
    for row in metmuseum_object_rows:
        candidate_id = row.get("candidate_collection_object_id", "")
        expected = expected_met_rows.get(candidate_id)
        if not expected:
            issues.append(f"{METMUSEUM_OBJECT_STAGING} unexpected candidate ID: {candidate_id}")
            continue
        if row.get("source_id") != "src-metmuseum-oracle-bone":
            issues.append(f"{METMUSEUM_OBJECT_STAGING} row must reference The Met source")
        if row.get("evidence_download_id") != expected["download_id"]:
            issues.append(f"{METMUSEUM_OBJECT_STAGING} row has wrong download id: {candidate_id}")
        if row.get("source_collection_item_id") != expected["source_collection_item_id"]:
            issues.append(f"{METMUSEUM_OBJECT_STAGING} object ID changed: {candidate_id}")
        if row.get("accession_number") != expected["accession_number"]:
            issues.append(f"{METMUSEUM_OBJECT_STAGING} accession number changed: {candidate_id}")
        if row.get("object_title_en") != expected["title"]:
            issues.append(f"{METMUSEUM_OBJECT_STAGING} title changed: {candidate_id}")
        if row.get("is_public_domain") != "true":
            issues.append(f"{METMUSEUM_OBJECT_STAGING} is_public_domain must stay true: {candidate_id}")
        if row.get("rights_status") != "public_domain_verified":
            issues.append(f"{METMUSEUM_OBJECT_STAGING} rights status must stay public_domain_verified: {candidate_id}")
        if row.get("medium") != expected["medium"]:
            issues.append(f"{METMUSEUM_OBJECT_STAGING} medium changed: {candidate_id}")
        if not row.get("primary_image_url", "").endswith(expected["image_suffix"]):
            issues.append(f"{METMUSEUM_OBJECT_STAGING} primary image URL changed: {candidate_id}")
        if row.get("project_import_status") != "object_metadata_not_promoted":
            issues.append(f"{METMUSEUM_OBJECT_STAGING} row must stay object_metadata_not_promoted: {candidate_id}")
        if "raw image files are not committed" not in row.get("caution", ""):
            issues.append(f"{METMUSEUM_OBJECT_STAGING} caution must state raw images are not committed: {candidate_id}")
        if row.get("review_status") != "reviewed_metadata_only":
            issues.append(f"{METMUSEUM_OBJECT_STAGING} row not reviewed_metadata_only: {candidate_id}")

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
    issues.extend(check_asset_records(root))
    issues.extend(check_source_registers(root))
    issues.extend(check_relationship_graph_edges(root))
    issues.extend(check_relationship_graph_statistics(root))
    issues.extend(check_source_coverage_statistics(root))
    issues.extend(check_ai_context_packs(root))
    issues.extend(check_ai_agent_evidence_pack_validator(root))

    if issues:
        print("FAIL repository skeleton")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PASS repository skeleton")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
