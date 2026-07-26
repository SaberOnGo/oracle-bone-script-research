#!/usr/bin/env python3
"""Build a human-first, condition-grouped source access review surface."""

from __future__ import annotations

import argparse
import csv
import textwrap
from collections import Counter
from pathlib import Path


DOWNLOAD_LOG = Path(
    "project_registry/006_large-source-register/002_source-download-log.csv"
)
BROWSER_CAPTURE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "014_browser-verified-metadata-capture.csv"
)
GAP_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "099_ai-agent-source-engineering-gap-queue.csv"
)
HUMAN_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "225_source-access-boundary-human-review.md"
)
INDEX_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "226_source-access-boundary-review-index.csv"
)
UPDATED_AT = "2026-07-27"
BOUNDARY_STATUSES = {
    "download_error",
    "http_error",
    "downloaded_access_restricted_page",
}

OUTPUT_FIELDS = [
    "access_boundary_task_id",
    "source_id",
    "failure_condition",
    "affected_attempt_count",
    "download_ids",
    "urls",
    "first_attempt_at",
    "latest_attempt_at",
    "status_counts",
    "http_status_counts",
    "checksum_present_count",
    "successful_context_download_ids",
    "browser_capture_ids",
    "required_next_checks",
    "route_files_to_open",
    "review_status",
    "research_boundary",
    "updated_at",
]

CONDITION_LABELS = {
    "access_restricted_response": (
        "Access-restricted response / 受限访问响应"
    ),
    "http_403_forbidden": "HTTP 403 boundary / HTTP 403 访问边界",
    "network_timeout": "Network timeout / 网络超时",
    "tls_certificate_validation_failure": (
        "TLS certificate validation failure / TLS 证书校验失败"
    ),
    "tls_handshake_failure": "TLS handshake failure / TLS 握手失败",
    "unclassified_access_failure": (
        "Unclassified access failure / 未归类访问失败"
    ),
}

NEXT_CHECKS = {
    "access_restricted_response": (
        "open_saved_restricted_page_then_manually_verify_official_route;"
        "do_not_treat_restricted_html_as_source_content"
    ),
    "http_403_forbidden": (
        "open_official_object_route_in_reviewed_browser;"
        "record_metadata_only_boundary_if_payload_remains_blocked"
    ),
    "network_timeout": (
        "compare_latest_timeout_with_historical_success;"
        "retry_only_when_network_condition_or_official_route_changes"
    ),
    "tls_certificate_validation_failure": (
        "verify_current_official_domain_and_certificate_state;"
        "do_not_disable_tls_validation_or claim_payload_access"
    ),
    "tls_handshake_failure": (
        "verify_current_official_route_in_independent_browser;"
        "record_route_change_before_another automated retry"
    ),
    "unclassified_access_failure": (
        "open_download_log_and_classify_failure_condition;"
        "record_concrete_retry_or_metadata_only_decision"
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def failure_condition(row: dict[str, str]) -> str:
    status = row.get("status", "")
    http_status = row.get("http_status", "")
    note = row.get("risk_note", "").lower()
    if status == "downloaded_access_restricted_page":
        return "access_restricted_response"
    if status == "http_error" and http_status == "403":
        return "http_403_forbidden"
    if "certificate" in note:
        return "tls_certificate_validation_failure"
    if "timed out" in note or "timeout" in note:
        return "network_timeout"
    if "handshake" in note or "unexpected_eof" in note:
        return "tls_handshake_failure"
    return "unclassified_access_failure"


def compact_counter(values: list[str]) -> str:
    counter = Counter(value for value in values if value)
    return ";".join(f"{key}:{counter[key]}" for key in sorted(counter))


def join_unique(values: list[str]) -> str:
    return ";".join(dict.fromkeys(value for value in values if value))


def build_review_rows(
    download_rows: list[dict[str, str]],
    browser_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    boundary_rows = [
        row for row in download_rows if row.get("status") in BOUNDARY_STATUSES
    ]
    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in boundary_rows:
        key = (row["source_id"], failure_condition(row))
        groups.setdefault(key, []).append(row)

    all_rows_by_source: dict[str, list[dict[str, str]]] = {}
    for row in download_rows:
        all_rows_by_source.setdefault(row["source_id"], []).append(row)
    captures_by_source: dict[str, list[dict[str, str]]] = {}
    for row in browser_rows:
        captures_by_source.setdefault(row["source_id"], []).append(row)

    output: list[dict[str, str]] = []
    unresolved_groups: list[tuple[tuple[str, str], list[dict[str, str]]]] = []
    for key, rows in sorted(groups.items()):
        source_id = key[0]
        latest_attempt_date = max(
            row.get("downloaded_at", "")[:10] for row in rows
        )
        later_reviewed_capture = any(
            row.get("review_status") == "reviewed_metadata_only"
            and row.get("captured_at", "") >= latest_attempt_date
            for row in captures_by_source.get(source_id, [])
        )
        if not later_reviewed_capture:
            unresolved_groups.append((key, rows))

    for index, ((source_id, condition), rows) in enumerate(
        unresolved_groups, start=1
    ):
        rows = sorted(rows, key=lambda row: row.get("downloaded_at", ""))
        context_rows = [
            row
            for row in all_rows_by_source[source_id]
            if row.get("status") == "downloaded"
        ]
        captures = captures_by_source.get(source_id, [])
        output.append(
            {
                "access_boundary_task_id": f"source-access-boundary-{index:03d}",
                "source_id": source_id,
                "failure_condition": condition,
                "affected_attempt_count": str(len(rows)),
                "download_ids": join_unique(
                    [row.get("download_id", "") for row in rows]
                ),
                "urls": join_unique([row.get("url", "") for row in rows]),
                "first_attempt_at": rows[0].get("downloaded_at", ""),
                "latest_attempt_at": rows[-1].get("downloaded_at", ""),
                "status_counts": compact_counter(
                    [row.get("status", "") for row in rows]
                ),
                "http_status_counts": compact_counter(
                    [row.get("http_status", "") for row in rows]
                ),
                "checksum_present_count": str(
                    sum(bool(row.get("checksum_sha256")) for row in rows)
                ),
                "successful_context_download_ids": join_unique(
                    [row.get("download_id", "") for row in context_rows]
                ),
                "browser_capture_ids": join_unique(
                    [row.get("capture_id", "") for row in captures]
                ),
                "required_next_checks": NEXT_CHECKS[condition],
                "route_files_to_open": ";".join(
                    [
                        DOWNLOAD_LOG.as_posix(),
                        BROWSER_CAPTURE.as_posix(),
                        GAP_QUEUE.as_posix(),
                    ]
                ),
                "review_status": "grouped_condition_needs_human_review",
                "research_boundary": (
                    "access_route_review_only_not_source_content_or_scholarship"
                ),
                "updated_at": UPDATED_AT,
            }
        )
    return output


def wrap_bullet(text: str) -> str:
    return textwrap.fill(
        f"- {text}",
        width=78,
        subsequent_indent="  ",
        break_long_words=True,
        break_on_hyphens=False,
    )


def build_human_guide(
    rows: list[dict[str, str]], gap_rows: list[dict[str, str]]
) -> str:
    source_ids = sorted({row["source_id"] for row in rows})
    access_gap_rows = [
        row
        for row in gap_rows
        if row.get("gap_type")
        in {
            "access_boundary_or_error_followup",
            "checksum_or_failed_download_status_review_needed",
        }
    ]
    lines = [
        "# Source Access Boundary Review / 来源访问边界复核",
        "",
        "## Human Result / 人类阅读结果",
        "",
        wrap_bullet(f"Affected source count: {len(source_ids)}"),
        wrap_bullet(f"Grouped failure-condition task count: {len(rows)}"),
        wrap_bullet(
            "Preserved access-attempt count: "
            f"{sum(int(row['affected_attempt_count']) for row in rows)}"
        ),
        wrap_bullet(
            "Older source-engineering access/checksum gap rows: "
            f"{len(access_gap_rows)}"
        ),
        "",
        "原始访问记录逐条保留，但人工任务按来源和故障条件归并。无来源",
        "payload 时没有 checksum 是同一访问边界的结果，不再另算一次任务。",
        "重试次数不会增加人类任务数；只有新的故障条件才新增任务。",
        "",
        "Access attempts remain separate provenance records. Human tasks are",
        "grouped by source and failure condition. A missing checksum for an",
        "unsaved payload is evidence of the same access boundary, not a second",
        "independent review task.",
        "",
        "## Grouped Tasks / 归并后任务",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### `{row['source_id']}`",
                "",
                wrap_bullet(CONDITION_LABELS[row["failure_condition"]]),
                wrap_bullet(
                    "Attempts preserved: " + row["affected_attempt_count"]
                ),
                "- Download IDs / 下载记录：",
            ]
        )
        lines.extend(
            f"  - `{download_id}`"
            for download_id in row["download_ids"].split(";")
        )
        lines.extend(
            [
                wrap_bullet("Status counts: " + row["status_counts"]),
                wrap_bullet(
                    "Latest attempt: " + (row["latest_attempt_at"] or "unknown")
                ),
            ]
        )
        if row["successful_context_download_ids"]:
            lines.append(
                wrap_bullet(
                    "Historical successful context: "
                    + row["successful_context_download_ids"]
                )
            )
        if row["browser_capture_ids"]:
            lines.append(
                wrap_bullet(
                    "Reviewed browser metadata: " + row["browser_capture_ids"]
                )
            )
        lines.extend(
            [
                wrap_bullet(
                    "Next checks: "
                    + row["required_next_checks"].replace(";", "; ")
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## Opening Order / 复核顺序",
            "",
            "1. Open the source's human-readable dossier or source note.",
            "2. Open the exact download IDs in the source download log.",
            "3. Compare a historical success or browser capture when listed.",
            "4. Retry only after the route, network, or access condition changes.",
            "5. Record a concrete metadata-only or retry decision.",
            "",
            "人工复核时，先读来源档案，再核对本表列出的 download ID。若已有",
            "历史成功记录或浏览器 metadata，应同时比较。只有路线、网络或访问",
            "条件变化时才重试，并记录具体的 metadata-only 或重试决定。",
            "",
            "## Boundary / 边界",
            "",
            "This is a preprocessing access review. It does not prove source",
            "availability, preserve a source payload, clear rights, promote a",
            "source, import corpus records, or make a decipherment conclusion.",
            "",
            "本表只用于预处理访问复核。它不证明来源当前可用，不代表已保存",
            "来源 payload，不裁定权利，不提升来源，不导入语料，也不形成释读",
            "结论。",
        ]
    )
    text = "\n".join(lines) + "\n"
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > 80:
            raise ValueError(
                f"{HUMAN_OUTPUT}:{line_number} exceeds 80 characters"
            )
    return text


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=OUTPUT_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)
    root = args.root.resolve()
    rows = build_review_rows(
        read_csv_rows(root / DOWNLOAD_LOG),
        read_csv_rows(root / BROWSER_CAPTURE),
    )
    gap_rows = read_csv_rows(root / GAP_QUEUE)
    (root / HUMAN_OUTPUT).write_text(
        build_human_guide(rows, gap_rows), encoding="utf-8", newline="\n"
    )
    write_csv(root / INDEX_OUTPUT, rows)
    print(
        f"source_count={len({row['source_id'] for row in rows})} "
        f"condition_task_count={len(rows)} "
        f"attempt_count={sum(int(row['affected_attempt_count']) for row in rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
