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


EXPECTED = [
    {
        "directory": "HUST-OBC/deciphered/0895/",
        "filename": "G_0895_乙1206合974賓組.png",
        "sha256": (
            "2a4305bfea49e7bed9952f88c46fd16f2fb92fba37633e3ae78d2864ea54fe04"
        ),
        "size": 1309,
        "compressed": 1314,
        "pixels": (57, 80),
    },
    {
        "directory": "HUST-OBC/deciphered/0895/",
        "filename": "G_0895_佚826合26786出組.png",
        "sha256": (
            "c150b076b6c43c56f369d62cd1b0ea302a2eec1ed8a0ffacf30f30947fed50f8"
        ),
        "size": 1443,
        "compressed": 1448,
        "pixels": (56, 80),
    },
    {
        "directory": "HUST-OBC/deciphered/0895/",
        "filename": "G_0895_後2.25.9合13426賓組.png",
        "sha256": (
            "c02c8bf93f00d424e8ede8df82c391f239de8e19e4ff94d78bee3825956b3422"
        ),
        "size": 1217,
        "compressed": 1222,
        "pixels": (32, 80),
    },
    {
        "directory": "HUST-OBC/deciphered/0895/",
        "filename": "G_0895_甲2489合27627歷無名間.png",
        "sha256": (
            "404f51d7ded0e169163004c705766463bf14ca0ea7ec54d94c66e4cb66a5eac8"
        ),
        "size": 1174,
        "compressed": 1179,
        "pixels": (33, 78),
    },
    {
        "directory": "HUST-OBC/GuoXueDaShi_1390/0895/",
        "filename": "G_0895_O_佚446(甲).png",
        "sha256": (
            "086fb3f3c09d42063e7ef0b915b82e51556dd5482023fca6c3adb00dae49f361"
        ),
        "size": 2497,
        "compressed": 2502,
        "pixels": (71, 133),
    },
]


class ObsChar000791MultiInstanceReviewTests(unittest.TestCase):
    def test_dossier_binds_five_members_to_exact_metadata(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        filenames = re.findall(
            r"^- Archive filename / 原包文件名: `([^`]+)`$", text, re.M
        )
        self.assertEqual([item["filename"] for item in EXPECTED], filenames)
        for item in EXPECTED:
            marker = (
                "- Archive filename / 原包文件名: `"
                + item["filename"]
                + "`"
            )
            marker_start = text.index(marker)
            start = text.rfind("\n## Instance ", 0, marker_start)
            if start < 0:
                start = 0
            next_heading = text.find("\n## Instance ", start + 1)
            body = text[start:] if next_heading < 0 else text[start:next_heading]
            self.assertIn(
                "- Archive directory / 原包目录: `"
                + item["directory"]
                + "`",
                body,
            )
            self.assertIn(f"- SHA-256: `{item['sha256']}`", body)
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
            "obs-char-000791",
            "hust-obc-cat-0895",
            "Multi-instance Visual Comparison",
            "near-form",
            "Two-way Falsification",
            "source_marked_risk_noted",
            "They do not confirm inscription",
            "not a decipherment conclusion",
            "instance-1-image",
            "03_visual-assets/001_asset-000796_hust-obc-cat-0895_glyph.png",
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
        self.assertIn("recorded_pending_independent_review", readiness)
        self.assertIn("opened visual members: `5`", readiness)
        archaeology = (OBJECT / "10_archaeology-paleography-review.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("source package: `large-src-000001`", archaeology)

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
