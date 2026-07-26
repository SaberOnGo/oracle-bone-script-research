#!/usr/bin/env python3
"""Append reviewed metadata profiles derived from registered source records.

This builder intentionally reads only committed provenance tables. It does not
reopen temporary downloads, re-download sources, or promote source text into
scholarship.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DOWNLOADED_METADATA_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv"
)
UPDATED_AT = "2026-07-27"
REVIEW_STATUS = "reviewed_metadata_only"

OUTPUT_FIELDS = [
    "profile_id",
    "source_id",
    "evidence_download_id",
    "metadata_file",
    "profile_metric",
    "profile_value",
    "profile_unit",
    "import_relevance",
    "caution",
    "review_status",
    "updated_at",
]

REGISTERED_PROFILE_ROWS = [
    {
        "source_id": "src-cambridge-hopkins",
        "evidence_download_id": "dl-cambridge-hopkins-finding-list",
        "metadata_file": "21_finding-list-reconciliation.md",
        "profile_metric": "finding_list_imported_row_count",
        "profile_value": "612",
        "profile_unit": "rows",
        "import_relevance": "Records the number of identifier rows retained in the reviewed Cambridge finding-list staging audit",
        "caution": "Staging-row count is a reconciliation fact; it is not a count of confirmed objects, inscriptions, or readings",
    },
    {
        "source_id": "src-cambridge-hopkins",
        "evidence_download_id": "dl-cambridge-hopkins-finding-list",
        "metadata_file": "21_finding-list-reconciliation.md",
        "profile_metric": "finding_list_page_stated_grand_total",
        "profile_value": "609",
        "profile_unit": "rows_stated_by_source_page",
        "import_relevance": "Preserves the grand total stated by the source page for human reconciliation against retained rows",
        "caution": "The page-stated total is source-page metadata and does not authorize filling or deleting any row",
    },
    {
        "source_id": "src-cambridge-hopkins",
        "evidence_download_id": "dl-cambridge-hopkins-finding-list",
        "metadata_file": "21_finding-list-reconciliation.md",
        "profile_metric": "finding_list_import_vs_stated_difference",
        "profile_value": "3",
        "profile_unit": "rows_difference",
        "import_relevance": "Keeps the unresolved difference visible so a researcher can trace it to the source page before any crosswalk promotion",
        "caution": "Difference is an open preprocessing question, not evidence of missing or duplicate inscriptions by itself",
    },
    {
        "source_id": "src-cambridge-hopkins",
        "evidence_download_id": "dl-cambridge-hopkins-finding-list",
        "metadata_file": "21_finding-list-reconciliation.md",
        "profile_metric": "finding_list_sections_with_declared_count_mismatch",
        "profile_value": "4",
        "profile_unit": "sections",
        "import_relevance": "Routes four section-level count mismatches to the human reconciliation dossier for targeted checking",
        "caution": "Section mismatch count is an audit signal and not a period, group, identity, or decipherment conclusion",
    },
    {
        "source_id": "src-cambridge-hopkins",
        "evidence_download_id": "dl-cambridge-hopkins-finding-list",
        "metadata_file": "21_finding-list-reconciliation.md",
        "profile_metric": "finding_list_sections_without_declared_count",
        "profile_value": "2",
        "profile_unit": "sections",
        "import_relevance": "Records that the source page leaves two observed sections without a declared count",
        "caution": "An unstated count remains a source-page omission and must not be converted into an inferred total",
    },
    {
        "source_id": "src-cambridge-hopkins",
        "evidence_download_id": "dl-cambridge-hopkins-finding-list",
        "metadata_file": "21_finding-list-reconciliation.md",
        "profile_metric": "finding_list_unclassified_row_count",
        "profile_value": "4",
        "profile_unit": "rows",
        "import_relevance": "Keeps the four source-page Unclassified entries visible for separate catalogue and image follow-up",
        "caution": "Unclassified is the source-page label; it is not a character identity, inscription identity, or scholarly classification",
    },
    {
        "source_id": "src-ihp-museum-oracle-bones",
        "evidence_download_id": "dl-ihp-museum-oracle-bones",
        "metadata_file": "collection_32.html",
        "profile_metric": "registered_scope",
        "profile_value": "museum_collection_overview_and_selected_artifact_labels",
        "profile_unit": "registered_scope_label",
        "import_relevance": "Records the IHP Museum page as a collection-level provenance route for later object review",
        "caution": "Overview metadata only; image reuse and object-level claims require separate museum policy and row review",
    },
    {
        "source_id": "src-ihp-oracle-rubbings",
        "evidence_download_id": "dl-ihp-rubbings-overview",
        "metadata_file": "dl-ihp-rubbings-overview.html",
        "profile_metric": "reported_rubbing_count_lower_bound",
        "profile_value": "40000",
        "profile_unit": "rubbings_lower_bound",
        "import_relevance": "Preserves the official overview wording that the IHP rubbing collection exceeds 40,000 items",
        "caution": "The source says more than 40,000; this is a lower-bound scale statement, not an exact local object count",
    },
    {
        "source_id": "src-ihp-oracle-rubbings",
        "evidence_download_id": "dl-ihp-rubbings-overview",
        "metadata_file": "dl-ihp-rubbings-overview.html",
        "profile_metric": "digitized_searchable_record_count",
        "profile_value": "21556",
        "profile_unit": "digitized_searchable_records",
        "import_relevance": "Records the official overview statement for the number of digitized records searchable through the database",
        "caution": "This is an access-scale statement, not a count of locally downloaded records, images, or rights-cleared derivatives",
    },
    {
        "source_id": "src-ihp-museum-oracle-bones",
        "evidence_download_id": "dl-ihp-museum-oracle-bones",
        "metadata_file": "collection_32.html",
        "profile_metric": "downloaded_page_size_bytes",
        "profile_value": "54136",
        "profile_unit": "bytes",
        "import_relevance": "Confirms the lightweight collection page download size recorded in the source log",
        "caution": "Downloaded page size is provenance metadata and not proof of complete collection coverage",
    },
    {
        "source_id": "src-obid-ancientbooks",
        "evidence_download_id": "dl-obid-ancientbooks-home",
        "metadata_file": "04_field-map-route-index.csv",
        "profile_metric": "registered_access_modes",
        "profile_value": "inscription_browsing;transcription_search;original_text_search;oracle_dictionary",
        "profile_unit": "named_access_mode_labels",
        "import_relevance": "Preserves four reviewed discovery entry labels for planning human source lookup and later object-level cross-reference",
        "caution": "Labels come from the reviewed 2026-06-04 field map; the current endpoint returned HTTP 403 and no hidden records or live functions were reverified",
    },
    {
        "source_id": "src-obid-ancientbooks",
        "evidence_download_id": "dl-obid-ancientbooks-home",
        "metadata_file": "04_field-map-route-index.csv",
        "profile_metric": "registered_explicit_catalog_prefix_examples",
        "profile_value": "H;GB;SG",
        "profile_unit": "catalog_prefix_examples",
        "import_relevance": "Keeps three explicitly reviewed catalog-prefix examples visible for future object-level identifier crosswalk review",
        "caution": "Examples are metadata-only lookup aids, not a complete prefix list, catalog import, object identity, or rights clearance",
    },
    {
        "source_id": "src-yinqi-wenyuan",
        "evidence_download_id": "dl-yinqi-home",
        "metadata_file": "home.html",
        "profile_metric": "registered_platform_sections",
        "profile_value": "glyph;catalog;literature;knowledge_service",
        "profile_unit": "section_labels",
        "import_relevance": "Records the registered platform scope for future manual or institutional metadata routes",
        "caution": "Mixed-rights platform metadata only; do not bulk import documents or images without separate review",
    },
    {
        "source_id": "src-yinqi-wenyuan",
        "evidence_download_id": "dl-yinqi-home",
        "metadata_file": "home.html",
        "profile_metric": "downloaded_page_size_bytes",
        "profile_value": "32900",
        "profile_unit": "bytes",
        "import_relevance": "Confirms the lightweight home-page download size recorded in the source log",
        "caution": "Home-page size does not imply corpus extraction or rights clearance",
    },
    {
        "source_id": "src-tsinghua-oracle-bones",
        "evidence_download_id": "dl-tsinghua-oracle-bones-overview",
        "metadata_file": "oracle-bones-overview.htm",
        "profile_metric": "collection_oracle_bone_count_over",
        "profile_value": "1750",
        "profile_unit": "oracle_bones",
        "import_relevance": "Records the official Tsinghua collection-scale statement from the reviewed source register",
        "caution": "Collection-level statement only; object-level rows are required before item or inscription claims",
    },
    {
        "source_id": "src-tsinghua-oracle-bones",
        "evidence_download_id": "dl-tsinghua-oracle-bones-overview",
        "metadata_file": "oracle-bones-overview.htm",
        "profile_metric": "collection_inscribed_piece_count",
        "profile_value": "1495",
        "profile_unit": "inscribed_pieces",
        "import_relevance": "Records the official count of inscribed pieces for collection planning",
        "caution": "Collection-level statistic only; not a local imported inscription count",
    },
    {
        "source_id": "src-tsinghua-oracle-bones",
        "evidence_download_id": "dl-tsinghua-oracle-bones-overview",
        "metadata_file": "oracle-bones-overview.htm",
        "profile_metric": "registered_collection_provenance_names",
        "profile_value": "Hu Houxuan;Yu Shengwu;Chen Mengjia",
        "profile_unit": "person_names",
        "import_relevance": "Preserves the registered provenance-name chain for later collection-context review",
        "caution": "Name chain is collection metadata and not excavation or object-level provenance proof by itself",
    },
    {
        "source_id": "src-open-oracle",
        "evidence_download_id": "dl-open-oracle-readme",
        "metadata_file": "README.md",
        "profile_metric": "registered_project_links",
        "profile_value": "HUST-OBC;EVOBC;OBSD",
        "profile_unit": "project_labels",
        "import_relevance": "Records Open-Oracle as a project index linking reviewed oracle-bone AI datasets",
        "caution": "Project index metadata only; underlying datasets need their own source and rights review",
    },
    {
        "source_id": "src-open-oracle",
        "evidence_download_id": "dl-open-oracle-readme",
        "metadata_file": "README.md",
        "profile_metric": "downloaded_readme_size_bytes",
        "profile_value": "15942",
        "profile_unit": "bytes",
        "import_relevance": "Confirms the lightweight README download size recorded in the source log",
        "caution": "README size is routing metadata and not corpus extraction",
    },
    {
        "source_id": "src-oracle-mnist",
        "evidence_download_id": "dl-oracle-mnist-readme",
        "metadata_file": "README.md",
        "profile_metric": "registered_dataset_scope",
        "profile_value": "small_oracle_character_image_benchmark",
        "profile_unit": "scope_label",
        "import_relevance": "Records Oracle-MNIST as an AI benchmark route rather than a comprehensive corpus source",
        "caution": "Benchmark metadata only; do not use as scholarly decipherment evidence",
    },
    {
        "source_id": "src-oracle-mnist",
        "evidence_download_id": "dl-oracle-mnist-readme",
        "metadata_file": "README.md",
        "profile_metric": "downloaded_readme_size_bytes",
        "profile_value": "5013",
        "profile_unit": "bytes",
        "import_relevance": "Confirms the lightweight README download size recorded in the source log",
        "caution": "README size is routing metadata and not image import or rights clearance",
    },
    {
        "source_id": "src-gbedobc",
        "evidence_download_id": "dl-gbedobc-repo-page",
        "metadata_file": "repo_page.html",
        "profile_metric": "graph_based_group_count",
        "profile_value": "756",
        "profile_unit": "groups",
        "import_relevance": "Records the registered GBEDOBC group-scale statistic for evolution graph planning",
        "caution": "Dataset statistic is a planning route and not a primary paleographic conclusion",
    },
    {
        "source_id": "src-gbedobc",
        "evidence_download_id": "dl-gbedobc-repo-page",
        "metadata_file": "repo_page.html",
        "profile_metric": "graph_based_character_count",
        "profile_value": "3780",
        "profile_unit": "graph_based_characters",
        "import_relevance": "Records the registered GBEDOBC graph-character scale for later package review",
        "caution": "Graph-based character count is source metadata and not local imported character records",
    },
    {
        "source_id": "src-gbedobc",
        "evidence_download_id": "dl-gbedobc-nature-pdf",
        "metadata_file": "nature_pdf.pdf",
        "profile_metric": "downloaded_article_pdf_size_bytes",
        "profile_value": "1875714",
        "profile_unit": "bytes",
        "import_relevance": "Confirms the registered GBEDOBC article PDF download size for bibliography routing",
        "caution": "PDF size/checksum metadata does not replace bibliographic or method review",
    },
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def next_profile_number(rows: list[dict[str, str]]) -> int:
    numbers = []
    for row in rows:
        profile_id = row.get("profile_id", "")
        if profile_id.startswith("metadata-profile-"):
            numbers.append(int(profile_id.rsplit("-", 1)[1]))
    return max(numbers, default=0) + 1


def validate_registered_rows(
    source_rows: list[dict[str, str]],
    download_log_rows: list[dict[str, str]],
    registered_rows: list[dict[str, str]],
) -> None:
    source_ids = {row["source_id"] for row in source_rows}
    download_ids = {row["download_id"] for row in download_log_rows}
    for row in registered_rows:
        if row["source_id"] not in source_ids:
            raise ValueError(f"unknown source_id: {row['source_id']}")
        if row["evidence_download_id"] not in download_ids:
            raise ValueError(f"unknown evidence_download_id: {row['evidence_download_id']}")


def build_profile_rows(existing_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = list(existing_rows)
    existing_keys = {
        (row["source_id"], row["evidence_download_id"], row["profile_metric"])
        for row in rows
    }
    profile_number = next_profile_number(rows)
    for registered_row in REGISTERED_PROFILE_ROWS:
        key = (
            registered_row["source_id"],
            registered_row["evidence_download_id"],
            registered_row["profile_metric"],
        )
        if key in existing_keys:
            continue
        rows.append(
            {
                "profile_id": f"metadata-profile-{profile_number:06d}",
                **registered_row,
                "review_status": REVIEW_STATUS,
                "updated_at": UPDATED_AT,
            }
        )
        existing_keys.add(key)
        profile_number += 1
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--source-download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--metadata-profile", default=str(DOWNLOADED_METADATA_PROFILE))
    args = parser.parse_args(argv)

    root = repo_root()
    source_rows = read_csv_rows(root / args.source_index)
    download_log_rows = read_csv_rows(root / args.source_download_log)
    existing_rows = read_csv_rows(root / args.metadata_profile)
    validate_registered_rows(source_rows, download_log_rows, REGISTERED_PROFILE_ROWS)
    rows = build_profile_rows(existing_rows)
    write_csv(root / args.metadata_profile, rows)
    print(f"wrote={len(rows)} output={(root / args.metadata_profile).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
