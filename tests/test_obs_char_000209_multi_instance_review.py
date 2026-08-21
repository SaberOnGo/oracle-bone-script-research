import hashlib
import io
import re
import unittest
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "001_oracle-characters"
    / "003_000201-000300_obs-char-bucket_oracle-characters"
    / "209_obs-char-000209_hust-obc-cat-0232_oracle-character"
)
DOSSIER = OBJECT / "17_multi-instance-visual-comparison.md"
RAW_ZIP = (
    ROOT
    / "external_local_archive"
    / "source_packages"
    / "hust-obc"
    / "dl-hust-obc-figshare-raw.zip"
)

EXPECTED = {
    "HUST-OBC/deciphered/0232/G_0232_乙2262合4814賓組.png": (
        "30f1892605b9a40277b0dea57e5d0320bd37a063082b5b2ba66a1e0c2d87b7ab",
        1738,
        1743,
        (46, 78),
    ),
    "HUST-OBC/deciphered/0232/G_0232_乙357合21988子組.png": (
        "e697ac0c6d48d832d57252f1eae13fb95def64bfb851149725a9a5ea20317f43",
        1495,
        1500,
        (44, 80),
    ),
    "HUST-OBC/deciphered/0232/G_0232_乙478合21021𠂤組.png": (
        "ebcc89ce8676dac8b91f8ea3bd2173469ea4ab0bb8538550faf218b8c6810e4c",
        1694,
        1699,
        (52, 78),
    ),
    "HUST-OBC/deciphered/0232/G_0232_前4.32.8合5994賓組.png": (
        "f951ca48c3b9856c5e60b6aa6f0a95d263221c6d3a3bfd6628ce9336742ae886",
        1925,
        1930,
        (58, 80),
    ),
    "HUST-OBC/deciphered/0232/G_0232_乙8896合22246子組.png": (
        "7bb5e4690e2989a0f4e83ad8e67ead496e5ad3efc4658e46456040189fde83ae",
        1970,
        1975,
        (64, 80),
    ),
}


class ObsChar000209MultiInstanceReviewTests(unittest.TestCase):
    def test_dossier_binds_five_members_to_exact_records(self):
        text = DOSSIER.read_text(encoding="utf-8")
        members = re.findall(
            r"^- Member: `([^`]+)`$", text, re.M
        )
        self.assertEqual(list(EXPECTED), members)
        for member, (digest, size, compressed, pixels) in EXPECTED.items():
            pattern = re.compile(
                r"^- Member: `" + re.escape(member) + r"`$"
                r"(?P<body>.*?)(?=^### Instance |^### Cross-instance)",
                re.M | re.S,
            )
            match = pattern.search(text)
            self.assertIsNotNone(match, member)
            body = match.group("body")
            self.assertIn(f"- SHA-256: `{digest}`", body, member)
            self.assertIn(
                "- Archive directory: `HUST-OBC/deciphered/0232/`",
                body,
                member,
            )
            self.assertIn(
                f"- File size: `{size}` bytes; ZIP compressed `{compressed}` "
                f"bytes; pixels: `{pixels[0]} × {pixels[1]}`;",
                body,
                member,
            )
            self.assertIn("mode: `RGB`.", body, member)

    def test_dossier_keeps_comparison_and_research_boundaries(self):
        text = DOSSIER.read_text(encoding="utf-8")
        for marker in (
            "obs-char-000209",
            "hust-obc-cat-0232",
            "source_marked_risk_noted",
            "Near-form mixture risk and alternatives",
            "Two-way falsification",
            "does not confirm inscription identity",
            "公开图版尚未闭合的阻断项",
            "双向可证伪条件",
            "不是破译结论",
        ):
            self.assertIn(marker, text)
        self.assertIn(
            "03_visual-assets/001_asset-000214_hust-obc-cat-0232_glyph.png",
            text,
        )
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)

    def test_object_entries_expose_the_human_comparison(self):
        for name in (
            "README.md",
            "05_human-research-dossier.md",
            "12_human-research-readiness-review.md",
        ):
            text = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("17_multi-instance-visual-comparison.md", text)
        readiness = (
            OBJECT / "12_human-research-readiness-review.md"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("opened source-package members: `5`", readiness)

    def test_human_markdown_is_bilingual_and_within_eighty_columns(self):
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("## English", text)
        self.assertIn("## 简体中文", text)
        self.assertNotIn("\ufffd", text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], violations)

    @unittest.skipUnless(RAW_ZIP.exists(), "ignored HUST raw ZIP unavailable")
    def test_registered_members_recompute_from_raw_zip(self):
        with zipfile.ZipFile(RAW_ZIP, metadata_encoding="gbk") as archive:
            for member, (expected_hash, expected_size, expected_compressed,
                         expected_pixels) in EXPECTED.items():
                info = archive.getinfo(member)
                payload = archive.read(member)
                self.assertEqual(expected_size, len(payload), member)
                self.assertEqual(expected_compressed, info.compress_size, member)
                self.assertEqual(
                    expected_hash, hashlib.sha256(payload).hexdigest(), member
                )
                with Image.open(io.BytesIO(payload)) as image:
                    image.load()
                    self.assertEqual(expected_pixels, image.size, member)
                    self.assertEqual("RGB", image.mode, member)


if __name__ == "__main__":
    unittest.main()
