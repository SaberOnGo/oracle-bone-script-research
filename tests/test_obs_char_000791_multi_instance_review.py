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
    / "008_000701-000800_obs-char-bucket_oracle-characters"
    / "791_obs-char-000791_hust-obc-cat-0895_oracle-character"
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
    "HUST-OBC/deciphered/0895/G_0895_乙1206合974賓組.png": (
        "2a4305bfea49e7bed9952f88c46fd16f2fb92fba37633e3ae78d2864ea54fe04",
        1309,
        1314,
        (57, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_佚826合26786出組.png": (
        "c150b076b6c43c56f369d62cd1b0ea302a2eec1ed8a0ffacf30f30947fed50f8",
        1443,
        1448,
        (56, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_甲1978合28087何組.png": (
        "9a2de0e7f18db3d367d8528a8cbfcf66e4c3982f87fc2fc74ed63e59869c73cb",
        930,
        935,
        (29, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_甲2489合27627歷無名間.png": (
        "404f51d7ded0e169163004c705766463bf14ca0ea7ec54d94c66e4cb66a5eac8",
        1174,
        1179,
        (33, 78),
    ),
    "HUST-OBC/deciphered/0895/G_0895_甲2744合34612歷組.png": (
        "7c03e53146320ff906f831edc48ed63827317525a2d6fb36160323bd7b19d907",
        1098,
        1103,
        (54, 80),
    ),
}


class ObsChar000791MultiInstanceReviewTests(unittest.TestCase):
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
                f"- Archive directory: `HUST-OBC/deciphered/0895/`",
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

    def test_dossier_keeps_human_boundary_and_falsification(self):
        text = DOSSIER.read_text(encoding="utf-8")
        for marker in (
            "obs-char-000791",
            "hust-obc-cat-0895",
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
            "03_visual-assets/001_asset-000796_hust-obc-cat-0895_glyph.png",
            text,
        )
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)

    def test_object_entries_expose_the_opened_comparison(self):
        for name in (
            "README.md",
            "05_human-research-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ):
            text = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("17_multi-instance-visual-comparison.md", text)
        readiness = (OBJECT / "12_human-research-readiness-review.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("opened visual members: `5`", readiness)

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
            for member, (
                expected_hash,
                expected_size,
                expected_compressed,
                expected_pixels,
            ) in (
                EXPECTED.items()
            ):
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
