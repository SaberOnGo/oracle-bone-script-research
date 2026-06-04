#!/usr/bin/env python3
"""Download approved source manifest entries into tmp and log provenance."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    import certifi
except ImportError:  # pragma: no cover - optional local dependency
    certifi = None


DEFAULT_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv"
)
DEFAULT_OUTPUT_DIR = Path("tmp/source_downloads")
DEFAULT_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
LOG_FIELDS = [
    "download_id",
    "source_id",
    "url",
    "downloaded_at",
    "status",
    "http_status",
    "file_size_bytes",
    "checksum_sha256",
    "local_temp_path",
    "risk_note",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def safe_filename(download_id: str, url: str, content_type: str | None) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in {".html", ".htm", ".md", ".pdf", ".txt", ".csv", ".json", ".xlsx"}:
        if content_type and "pdf" in content_type:
            suffix = ".pdf"
        elif content_type and "json" in content_type:
            suffix = ".json"
        elif content_type and "markdown" in content_type:
            suffix = ".md"
        else:
            suffix = ".html"
    safe_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", download_id).strip("-")
    return f"{safe_id}{suffix}"


def classify_payload(data: bytes, content_type: str | None) -> str:
    if not data:
        return "empty"
    if content_type and "text/html" in content_type.lower():
        snippet = data[:4096].decode("utf-8", errors="ignore").lower()
        if "access restricted" in snippet or "noindex, nofollow" in snippet:
            return "downloaded_access_restricted_page"
        if "client challenge" in snippet or "please enable javascript to proceed" in snippet:
            return "downloaded_client_challenge_page"
    return "downloaded"


def ssl_context() -> ssl.SSLContext:
    if certifi:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def download_one(row: dict[str, str], output_dir: Path, root: Path) -> dict[str, str]:
    download_id = row["download_id"]
    url = row["url"]
    max_bytes = int(row.get("max_bytes") or "31457280")
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; oracle-bone-script-research/0.1; "
            "+https://github.com/SaberOnGo/oracle-bone-script-research)"
        ),
        "Accept": "text/html,application/pdf,text/markdown,text/plain,application/json,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    try:
        request = Request(url, headers=headers)
        with urlopen(request, timeout=30, context=ssl_context()) as response:
            http_status = str(response.status)
            content_type = response.headers.get("Content-Type")
            data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            return {
                "download_id": download_id,
                "source_id": row["source_id"],
                "url": url,
                "downloaded_at": timestamp,
                "status": "skipped_exceeds_manifest_limit",
                "http_status": http_status,
                "file_size_bytes": str(len(data)),
                "checksum_sha256": "",
                "local_temp_path": "",
                "risk_note": "Downloaded payload exceeded manifest max_bytes; raw source not saved.",
            }

        output_dir.mkdir(parents=True, exist_ok=True)
        filename = safe_filename(download_id, url, content_type)
        local_path = output_dir / filename
        local_path.write_bytes(data)
        checksum = hashlib.sha256(data).hexdigest()
        status = classify_payload(data, content_type)
        risk_note = "Stored under ignored tmp directory; commit log/checksum only."
        if status == "downloaded_access_restricted_page":
            risk_note = "Site returned an access-restricted HTML page; treat as access evidence only."
        elif status == "downloaded_client_challenge_page":
            risk_note = "Site returned a client-challenge HTML page; treat as access evidence only."
        return {
            "download_id": download_id,
            "source_id": row["source_id"],
            "url": url,
            "downloaded_at": timestamp,
            "status": status,
            "http_status": http_status,
            "file_size_bytes": str(len(data)),
            "checksum_sha256": checksum,
            "local_temp_path": local_path.relative_to(root).as_posix(),
            "risk_note": risk_note,
        }
    except HTTPError as error:
        return {
            "download_id": download_id,
            "source_id": row["source_id"],
            "url": url,
            "downloaded_at": timestamp,
            "status": "http_error",
            "http_status": str(error.code),
            "file_size_bytes": "0",
            "checksum_sha256": "",
            "local_temp_path": "",
            "risk_note": str(error.reason),
        }
    except (OSError, URLError) as error:
        return {
            "download_id": download_id,
            "source_id": row["source_id"],
            "url": url,
            "downloaded_at": timestamp,
            "status": "download_error",
            "http_status": "",
            "file_size_bytes": "0",
            "checksum_sha256": "",
            "local_temp_path": "",
            "risk_note": str(error),
        }


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_existing_log(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def merge_log_rows(existing_rows: list[dict[str, str]], updated_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    updated_by_id = {row["download_id"]: row for row in updated_rows}
    merged: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in existing_rows:
        download_id = row.get("download_id", "")
        if download_id in updated_by_id:
            merged.append(updated_by_id[download_id])
            seen.add(download_id)
        else:
            merged.append(row)
    for row in updated_rows:
        download_id = row["download_id"]
        if download_id not in seen:
            merged.append(row)
    return merged


def write_log(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--log", default=str(DEFAULT_LOG))
    parser.add_argument(
        "--download-id",
        action="append",
        default=[],
        help="Download only this manifest ID and merge it into the existing log; repeatable.",
    )
    args = parser.parse_args(argv)

    root = repo_root()
    manifest = root / args.manifest
    output_dir = root / args.output_dir
    log_path = root / args.log

    rows = read_manifest(manifest)
    if args.download_id:
        requested_ids = set(args.download_id)
        rows_by_id = {row["download_id"]: row for row in rows}
        missing_ids = sorted(requested_ids - set(rows_by_id))
        if missing_ids:
            print(f"unknown download_id(s): {', '.join(missing_ids)}", file=sys.stderr)
            return 2
        rows = [row for row in rows if row["download_id"] in requested_ids]

    run_results = [download_one(row, output_dir, root) for row in rows]
    results = run_results
    if args.download_id:
        results = merge_log_rows(read_existing_log(log_path), run_results)
    write_log(log_path, results)

    run_count = len(rows)
    ok_count = sum(row["status"].startswith("downloaded") for row in run_results)
    print(
        f"downloaded_or_reached={ok_count} run={run_count} "
        f"total_log_rows={len(results)} log={log_path.relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
