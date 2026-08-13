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
    / "007_000601-000700_obs-char-bucket_oracle-characters"
    / "621_obs-char-000621_hust-obc-cat-0706_oracle-character"
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
    "HUST-OBC/deciphered/0706/G_0706_乙1904合1351.png": (
        "81ff572ea0c3c777efcf59e25865e2ae1d0ea432d1a9e340f3f8c7d82429a368",
        1480,
        (44, 78),
    ),
    "HUST-OBC/deciphered/0706/G_0706_前5.10.5合11439𠂤賓間.png": (
        "ae2800a46f863eb741e9418f3dff3c66d40575d5f58ceddb19102673d4231453",
        1328,
        (50, 74),
    ),
    "HUST-OBC/deciphered/0706/G_0706_後1.9.1合11405.png": (
        "ef6196de33e2cbe7671587d11d1024e07a6ab50cce378a08c26ec447921dd9a2",
        1816,
        (64, 80),
    ),
    "HUST-OBC/deciphered/0706/G_0706_鄴2下.35.15合16610.png": (
        "50878bde077dd8e676600f8ce0a883ab87a7447a387dd4205ac99328287aa9af",
        1356,
        (39, 80),
    ),
    "HUST-OBC/GuoXueDaShi_1390/0706/G_0706_O_鐵172.4合8553.png": (
        "721c93d2220a0e68d41cff711aa8e1605c6a62c4bc60ebd69b8d4f478eb92a2a",
        1992,
        (60, 80),
    ),
}


class ObsChar000621MultiInstanceReviewTests(unittest.TestCase):
    def test_dossier_records_five_distinct_opened_members(self):
        text = DOSSIER.read_text(encoding="utf-8")
        members = re.findall(
            r"^- Member / 成员：`([^`]+)`$", text, re.M
        )
        self.assertEqual(list(EXPECTED), members)
        for member, (digest, size, pixels) in EXPECTED.items():
            pattern = re.compile(
                r"^- Member / 成员：`" + re.escape(member) + r"`$"
                r"(?P<body>.*?)(?=^### Instance |^### Cross-instance)",
                re.M | re.S,
            )
            match = pattern.search(text)
            self.assertIsNotNone(match, member)
            body = match.group("body")
            self.assertIn(f"- SHA-256：`{digest}`", body, member)
            self.assertIn(f"- File size / 文件大小：`{size}` bytes", body, member)
            self.assertIn(
                f"- Pixel size / 像素：`{pixels[0]} × {pixels[1]}`",
                body,
                member,
            )

    def test_dossier_preserves_comparison_and_research_boundaries(self):
        text = DOSSIER.read_text(encoding="utf-8")
        for marker in (
            "obs-char-000621",
            "hust-obc-cat-0706",
            "Near-form mixture risk / 近形混类风险",
            "Alternative explanations / 替代解释",
            "Two-way falsification / 双向可证伪条件",
            "source_marked_risk_noted",
            "does not confirm inscription identity",
            "not an accepted reading",
            "blocking visibility limitation",
            "五图公开图版尚未完成的阻断项",
        ):
            self.assertIn(marker, text)
        self.assertIn(
            "03_visual-assets/001_asset-000626_hust-obc-cat-0706_glyph.png",
            text,
        )

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
            for member, (expected_hash, expected_size, expected_pixels) in (
                EXPECTED.items()
            ):
                payload = archive.read(member)
                self.assertEqual(expected_size, len(payload), member)
                self.assertEqual(
                    expected_hash, hashlib.sha256(payload).hexdigest(), member
                )
                with Image.open(io.BytesIO(payload)) as image:
                    image.load()
                    self.assertEqual(expected_pixels, image.size, member)
                    self.assertEqual("RGB", image.mode, member)


if __name__ == "__main__":
    unittest.main()
