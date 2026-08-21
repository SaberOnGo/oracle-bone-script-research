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
    / "005_000401-000500_obs-char-bucket_oracle-characters"
    / "412_obs-char-000412_hust-obc-cat-0468_oracle-character"
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
    "HUST-OBC/deciphered/0468/G_0468_乙1916合938賓組.png": (
        "846a79707beca88c5d7ded2927730bff5185439d048d37d70ca7f0d6d5b4e410",
        1604,
        1609,
        (42, 80),
    ),
    "HUST-OBC/deciphered/0468/G_0468_乙5162合22049午組.png": (
        "79e01648900de03c912807055e946c8d0c8f78be417fb4d415ea1576ce571ad9",
        1439,
        1444,
        (40, 80),
    ),
    "HUST-OBC/deciphered/0468/G_0468_後2.23.9合693賓組.png": (
        "8f6e6483920bff06bc49237e94e77159f5fc0d52be4acd46b58d069b810ed9c3",
        1343,
        1348,
        (34, 79),
    ),
    "HUST-OBC/deciphered/0468/G_0468_續1.39.3合331賓組.png": (
        "248990584c093a84ac7b301d8b82d1e092985fb68b42536a7ccd9de674342abf",
        1256,
        1261,
        (32, 80),
    ),
    "HUST-OBC/deciphered/0468/G_0468_菁2.1合6057賓組.png": (
        "49fd5921a2dab51a5be4b14df799c15644b32b95bb0484fe59a4ae8ee9119003",
        1463,
        1468,
        (30, 80),
    ),
}


class ObsChar000412MultiInstanceReviewTests(unittest.TestCase):
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
                "- Archive directory: `HUST-OBC/deciphered/0468/`",
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
            "obs-char-000412",
            "hust-obc-cat-0468",
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
            "03_visual-assets/001_asset-000417_hust-obc-cat-0468_glyph.png",
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
