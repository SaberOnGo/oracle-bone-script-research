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
    / "009_000801-000900_obs-char-bucket_oracle-characters"
    / "852_obs-char-000852_hust-obc-cat-0961_oracle-character"
)
DOSSIER = OBJECT / "17_multi-instance-visual-comparison.md"
RAW_ZIP = (
    ROOT
    / "external_local_archive"
    / "source_packages"
    / "hust-obc"
    / "dl-hust-obc-figshare-raw.zip"
)


EXPECTED = [
    {
        "directory": "HUST-OBC/deciphered/0961/",
        "filename": (
            "G_0961_\u4eac\u6d25\u0034\u0034\u0031\u0030\u5408"
            "\u0033\u0031\u0039\u0032\u0033\u7121\u540d\u7d44.png"
        ),
        "sha256": (
            "b7840f02581f8bb9ba6ed2081dafd73e3c622a3188f8747a3d30901c1b37e4fb"
        ),
        "size": 1570,
        "compressed": 1575,
        "pixels": (56, 80),
    },
    {
        "directory": "HUST-OBC/deciphered/0961/",
        "filename": (
            "G_0961_\u524d6.32.5\u5408\u0038\u0033\u0031\u0035"
            "\u8cd3\u7d44.png"
        ),
        "sha256": (
            "c078a00eab8e4a83bc6ceb7daab8021b609ae52047a52862d78f1c8000e41e58"
        ),
        "size": 1433,
        "compressed": 1438,
        "pixels": (61, 77),
    },
    {
        "directory": "HUST-OBC/deciphered/0961/",
        "filename": (
            "G_0961_\u524d6.32.5\u5408\u0038\u0033\u0031\u0035"
            "\u8cd3\u7d44\u526f\u672c0.png"
        ),
        "sha256": (
            "f42ab06ab52c54645e0c051a297f491263d12171ab2db97ffac4b2fe4ba55c79"
        ),
        "size": 1204,
        "compressed": 1209,
        "pixels": (34, 80),
    },
    {
        "directory": "HUST-OBC/deciphered/0961/",
        "filename": (
            "G_0961_\u5f8c2.3.11\u5408\u0038\u0033\u0032\u0030"
            "\u8cd3\u7d44.png"
        ),
        "sha256": (
            "3be46391beb8564f601838c329b51a32df351d6c2259dfc9d35384e83b1ebb02"
        ),
        "size": 2095,
        "compressed": 2100,
        "pixels": (78, 80),
    },
    {
        "directory": "HUST-OBC/deciphered/0961/",
        "filename": (
            "G_0961_\u7c20\u573047\u5408\u0037\u0038\u0035\u0034"
            "\u8cd3\u7d44.png"
        ),
        "sha256": (
            "22f9cdd168a9b2d02bd9352060b8e3425137a8d85e554c7b9db93809b4016a08"
        ),
        "size": 2127,
        "compressed": 2132,
        "pixels": (66, 80),
    },
    {
        "directory": "HUST-OBC/GuoXueDaShi_1390/0961/",
        "filename": (
            "G_0961_O_\u524d5.8.3(\u7532).png"
        ),
        "sha256": (
            "e2bde029956ffe99e52537ee9ef28cdb210ed6e0cc9bf8b39c5d760f2bc83d0c"
        ),
        "size": 2026,
        "compressed": 2031,
        "pixels": (57, 127),
    },
]


class ObsChar000852MultiInstanceReviewTests(unittest.TestCase):
    def test_dossier_binds_six_members_to_exact_metadata(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        filenames = re.findall(
            r"^- Archive filename / 原包文件名:\n  `([^`]+)`$", text, re.M
        )
        self.assertEqual([item["filename"] for item in EXPECTED], filenames)
        for item in EXPECTED:
            marker = "  `" + item["filename"] + "`"
            marker_start = text.index(marker)
            start = text.rfind("\n## Instance ", 0, marker_start)
            next_heading = text.find("\n## Instance ", marker_start)
            body = text[start:] if next_heading < 0 else text[start:next_heading]
            self.assertIn(
                "- SHA-256:\n  `" + item["sha256"] + "`",
                body,
            )
            self.assertIn(
                f"- File size / 文件大小: `{item['size']}` bytes; "
                f"ZIP compressed `{item['compressed']}` bytes",
                body,
            )
            self.assertIn(
                f"- Pixel size / 像素尺寸: "
                f"`{item['pixels'][0]} x {item['pixels'][1]}`; mode `RGB`",
                body,
            )

    def test_dossier_records_visual_counterevidence_and_boundary(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        for marker in (
            "obs-char-000852",
            "hust-obc-cat-0961",
            "Multi-instance Visual Comparison",
            "near-form",
            "Two-way Falsification",
            "source_marked_risk_noted",
            "They do not confirm inscription",
            "not a decipherment conclusion",
            "instance-1-image",
            "03_visual-assets/001_asset-000857_hust-obc-cat-0961_glyph.png",
        ):
            self.assertIn(marker, text)
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
        self.assertIn("opened visual members: `6`", readiness)

    def test_human_markdown_is_bilingual_and_within_eighty_columns(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        self.assertIn("## Purpose And Boundary / 目的与边界", text)
        self.assertIn("## Research Boundary / 研究边界", text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], violations)

    @unittest.skipUnless(RAW_ZIP.exists(), "ignored HUST raw ZIP unavailable")
    def test_registered_members_recompute_from_raw_zip(self):
        with zipfile.ZipFile(RAW_ZIP, metadata_encoding="gbk") as archive:
            for item in EXPECTED:
                member = item["directory"] + item["filename"]
                info = archive.getinfo(member)
                payload = archive.read(member)
                self.assertEqual(item["size"], len(payload), member)
                self.assertEqual(item["compressed"], info.compress_size, member)
                self.assertEqual(item["sha256"], hashlib.sha256(payload).hexdigest())
                with Image.open(io.BytesIO(payload)) as image:
                    image.load()
                    self.assertEqual(item["pixels"], image.size, member)
                    self.assertEqual("RGB", image.mode, member)


if __name__ == "__main__":
    unittest.main()
