#!/usr/bin/env python3
"""Replay the OBIMD H2 visual crosswalk without persisting image bytes."""

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageOps, __version__ as pillow_version


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
HASH_SIZE = 8
RESAMPLE = Image.Resampling.LANCZOS


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_hash(label, actual, expected):
    if actual.lower() != expected.lower():
        raise ValueError(f"{label} SHA-256 mismatch: {actual} != {expected}")


def decode_image(payload):
    with Image.open(io.BytesIO(payload)) as source:
        source.load()
        return source.copy()


def flattened_pixels(image):
    getter = getattr(image, "get_flattened_data", None)
    return list(getter() if getter else image.getdata())


def dhash(image, hash_size=HASH_SIZE):
    pixels = flattened_pixels(
        image.convert("L").resize(
            (hash_size + 1, hash_size), resample=RESAMPLE
        )
    )
    value = 0
    for y in range(hash_size):
        for x in range(hash_size):
            value = (value << 1) | int(
                pixels[y * (hash_size + 1) + x]
                > pixels[y * (hash_size + 1) + x + 1]
            )
    return value


def hamming(left, right):
    return (left ^ right).bit_count()


def mean_absolute_difference(reference, candidate, invert=False):
    reference_l = reference.convert("L")
    fitted = ImageOps.fit(
        candidate.convert("L"),
        reference_l.size,
        method=RESAMPLE,
        centering=(0.5, 0.5),
    )
    if invert:
        fitted = ImageOps.invert(fitted)
    pairs = zip(flattened_pixels(reference_l), flattened_pixels(fitted))
    return sum(abs(int(a) - int(b)) for a, b in pairs) / (
        reference_l.width * reference_l.height
    )


def load_thumbnail(args):
    if args.thumbnail_file:
        return Path(args.thumbnail_file).read_bytes(), "local_file"
    request = urllib.request.Request(
        args.thumbnail_url,
        headers={"User-Agent": "obimd-h2-crosswalk-replay/1.0"},
    )
    with urllib.request.urlopen(request, timeout=args.network_timeout) as response:
        return response.read(), "network_memory_only"


def compare(args):
    thumbnail_bytes, acquisition = load_thumbnail(args)
    thumbnail_sha = sha256_bytes(thumbnail_bytes)
    require_hash("thumbnail", thumbnail_sha, args.expected_thumbnail_sha256)
    package_sha = sha256_file(args.rubbing_zip)
    require_hash("rubbing package", package_sha, args.expected_rubbing_zip_sha256)
    thumbnail = decode_image(thumbnail_bytes)
    thumb_hash = dhash(thumbnail)
    rows = []
    target_payload = None
    with zipfile.ZipFile(args.rubbing_zip) as archive:
        members = sorted(
            info.filename
            for info in archive.infolist()
            if not info.is_dir() and Path(info.filename).suffix.lower() in IMAGE_SUFFIXES
        )
        for member in members:
            payload = archive.read(member)
            if member == args.target_member:
                target_payload = payload
            rows.append(
                {
                    "member": member,
                    "dhash_distance": hamming(thumb_hash, dhash(decode_image(payload))),
                }
            )
    if target_payload is None:
        raise ValueError(f"target member not found: {args.target_member}")
    target_sha = sha256_bytes(target_payload)
    require_hash("target member", target_sha, args.expected_target_member_sha256)
    rows.sort(key=lambda row: (row["dhash_distance"], row["member"]))
    target_rank = next(i for i, row in enumerate(rows, 1)
                       if row["member"] == args.target_member)
    target = decode_image(target_payload)
    nearest_alternative_distance = min(
        row["dhash_distance"]
        for row in rows
        if row["member"] != args.target_member
    )
    return {
        "schema": "obimd_h2_visual_crosswalk_replay_v1",
        "run_status": (
            "replayed_from_official_url"
            if acquisition == "network_memory_only"
            else "replayed_from_local_input"
        ),
        "run_date": args.run_date,
        "runtime": {"python": sys.version.split()[0], "pillow": pillow_version},
        "thumbnail": {
            "source_url": args.thumbnail_source_url or args.thumbnail_url,
            "acquisition": acquisition,
            "byte_count": len(thumbnail_bytes),
            "sha256": thumbnail_sha,
            "dimensions": list(thumbnail.size),
            "mode_after_decode": thumbnail.mode,
            "persisted": False,
        },
        "package": {
            "local_ignored_path": args.rubbing_zip.as_posix(),
            "byte_count": args.rubbing_zip.stat().st_size,
            "sha256": package_sha,
            "candidate_count": len(rows),
            "alternative_candidate_count": len(rows) - 1,
        },
        "target": {
            "member": args.target_member,
            "sha256": target_sha,
            "byte_count": len(target_payload),
            "dimensions": list(target.size),
        },
        "algorithm": {
            "dhash": {
                "hash_size": HASH_SIZE,
                "grayscale": "Pillow convert L",
                "resize": [HASH_SIZE + 1, HASH_SIZE],
                "resample": "LANCZOS",
                "bit_order": "row-major, most-significant bit first",
                "comparison": "left_pixel > right_pixel",
                "distance": "Hamming popcount(xor)",
            },
            "ranking": "ascending (dhash_distance, case-sensitive member path)",
            "ties": "all ties retained; member path is deterministic tie-breaker",
            "mad": {
                "reference": "thumbnail converted to L",
                "candidate": "target converted to L and ImageOps.fit to reference size",
                "fit": "LANCZOS, centered (0.5, 0.5)",
                "direct": "mean(abs(reference - candidate))",
                "inverted": "mean(abs(reference - (255 - candidate)))",
            },
        },
        "comparison": {
            "candidate_count": len(rows),
            "alternative_candidate_count": len(rows) - 1,
            "target_rank": target_rank,
            "target_dhash_distance": rows[target_rank - 1]["dhash_distance"],
            "nearest_alternative_distance": nearest_alternative_distance,
            "target_direct_mad": mean_absolute_difference(thumbnail, target),
            "target_inverted_mad": mean_absolute_difference(thumbnail, target, True),
            "top_k": rows[: args.top_k],
        },
        "scope_boundary": {
            "catalog_identity_confirmed": False,
            "reading_proposed": False,
            "transcription_or_ocr_acquired": False,
            "rights": "metadata_only_until_verified",
        },
        "replay_tool": "tools/007_obimd-h2-crosswalk/replay_h2_crosswalk.py",
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--thumbnail-file", type=Path)
    source.add_argument("--thumbnail-url")
    parser.add_argument("--thumbnail-source-url")
    parser.add_argument("--network-timeout", type=float, default=20.0)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--rubbing-zip", type=Path, required=True)
    parser.add_argument("--expected-thumbnail-sha256", required=True)
    parser.add_argument("--expected-rubbing-zip-sha256", required=True)
    parser.add_argument("--target-member", required=True)
    parser.add_argument("--expected-target-member-sha256", required=True)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--verify-manifest", type=Path)
    args = parser.parse_args(argv)
    if args.top_k < 1:
        parser.error("--top-k must be positive")
    try:
        dt.date.fromisoformat(args.run_date)
    except ValueError:
        parser.error("--run-date must use YYYY-MM-DD")
    return args


def main(argv=None):
    try:
        args = parse_args(argv)
        record = compare(args)
        if args.verify_manifest:
            expected = json.loads(
                args.verify_manifest.read_text(encoding="utf-8")
            )
            if record != expected:
                raise ValueError(
                    f"replay differs from manifest: {args.verify_manifest}"
                )
    except (json.JSONDecodeError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    json.dump(record, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
