import hashlib
import re
import unittest
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / (
    "corpus/001_oracle-characters/"
    "008_000701-000800_obs-char-bucket_oracle-characters/"
    "791_obs-char-000791_hust-obc-cat-0895_oracle-character/"
    "17_multi-instance-visual-comparison.md"
)
ARCHIVE = ROOT / (
    "external_local_archive/source_packages/hust-obc/"
    "dl-hust-obc-figshare-raw.zip"
)

EXPECTED = {
    "HUST-OBC/deciphered/0895/G_0895_乙1206合974賓組.png": (
        1309,
        1314,
        "2a4305bfea49e7bed9952f88c46fd16f2fb92fba37633e3ae78d2864ea54fe04",
        (57, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_乙3797合6583賓組.png": (
        1236,
        1241,
        "30b81ce2486ba7cc8b417255c2003bd1dc7b00bf89d45df22ceea80fdd97adc7",
        (49, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_佚826合26786出組.png": (
        1443,
        1448,
        "c150b076b6c43c56f369d62cd1b0ea302a2eec1ed8a0ffacf30f30947fed50f8",
        (56, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_後2.25.9合13426賓組.png": (
        1217,
        1222,
        "c02c8bf93f00d424e8ede8df82c391f239de8e19e4ff94d78bee3825956b3422",
        (32, 80),
    ),
    "HUST-OBC/deciphered/0895/G_0895_甲1978合28087何組.png": (
        930,
        935,
        "9a2de0e7f18db3d367d8528a8cbfcf66e4c3982f87fc2fc74ed63e59869c73cb",
        (29, 80),
    ),
}


class ObsChar000791MultiInstanceReviewTests(unittest.TestCase):
    def test_review_records_five_opened_archive_members(self):
        self.assertTrue(DOSSIER.is_file(), DOSSIER)
        text = DOSSIER.read_text(encoding="utf-8-sig")
        members = re.findall(r"^- Archive member / 原包成员：\n  `([^`]+)`$", text, re.M)
        self.assertEqual(5, len(members))
        self.assertEqual(5, len(set(members)))
        self.assertTrue(all("/0895/G_0895_" in item for item in members))
        self.assertEqual(5, len(re.findall(r"^- SHA-256：`[0-9a-f]{64}`$", text, re.M)))
        self.assertEqual(5, len(re.findall(r"^- Pixel size / 像素：`\d+ × \d+`$", text, re.M)))

    @unittest.skipUnless(ARCHIVE.is_file(), "ignored HUST archive is unavailable")
    def test_document_hashes_and_dimensions_match_ignored_archive(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        pattern = re.compile(
            r"^- Archive member / 原包成员：\n  `([^`]+)`\n"
            r"- SHA-256：`([0-9a-f]{64})`\n"
            r"- File size / 文件大小：`(\d+)` bytes；ZIP compressed：`(\d+)` bytes\n"
            r"- Pixel size / 像素：`(\d+) × (\d+)`$",
            re.M,
        )
        documented = {
            member: (int(size), int(compressed), digest, (int(width), int(height)))
            for member, digest, size, compressed, width, height in pattern.findall(text)
        }
        self.assertEqual(EXPECTED, documented)
        with ZipFile(ARCHIVE) as archive:
            for member, (size, compressed, digest, dimensions) in EXPECTED.items():
                with self.subTest(member=member):
                    info = archive.getinfo(member)
                    data = archive.read(member)
                    self.assertEqual(size, len(data))
                    self.assertEqual(compressed, info.compress_size)
                    self.assertEqual(digest, hashlib.sha256(data).hexdigest())
                    with Image.open(BytesIO(data)) as image:
                        self.assertEqual(dimensions, image.size)

    def test_review_is_object_specific_and_falsifiable(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        for marker in (
            "obs-char-000791",
            "hust-obc-cat-0895",
            "合 974",
            "合 6583",
            "合 26786",
            "合 13426",
            "合 28087",
            "## Pairwise Differences And Counterevidence",
            "Near-form risk / 近形风险",
            "source_marked_risk_noted",
            "This review does not",
            "not an accepted reading",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)

    def test_human_markdown_lines_do_not_exceed_eighty_characters(self):
        for line_number, line in enumerate(
            DOSSIER.read_text(encoding="utf-8-sig").splitlines(), 1
        ):
            self.assertLessEqual(
                len(line),
                80,
                f"{DOSSIER}:{line_number}: {len(line)} characters",
            )


if __name__ == "__main__":
    unittest.main()
