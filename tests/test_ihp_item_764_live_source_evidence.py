import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "020_coll-obj-cand-00020_ihp-item-764_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem764LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_page_is_linked_from_human_entries(self):
        self.assertTrue(EVIDENCE.exists())
        for name in (
            "README.md",
            "04_visual-gallery.md",
            "05_human-review-sheet.md",
            "06_human-collection-dossier.md",
            "08_collection-provenance-evidence-dossier.md",
            "10_collection-provenance-fact-matrix.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
            "16_preformal-research-start-check.md",
        ):
            page = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("18_live-source-evidence-review.md", page)

    def test_page_binds_metadata_and_source_description(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/764/",
            "https://museum.sinica.edu.tw/collection/32/item/764/",
            "Source collection item ID / 馆藏对象号: `764`",
            "Item No. / 馆藏编号: `R024975`",
            "Inscribed Animal Bone Fragment Chia 2624",
            "獸骨卜辭殘片《甲》2624",
            "Late Shang Period",
            "10.6(L)×4.0(W) cm",
            "Hsiao-t'un, Anyang County, Honan Province",
            "bird inscription",
            "source_reported_description_without_full_transcription",
            "OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_route_and_local_observation(self):
        required = (
            "6015f6894ed3eeaa.jpg",
            "501850",
            "f907975d99895f7cf9406b2cb3dde811869fd8bafdfb98c9a34d920946f6ec99",
            "1000 x 1280",
            "image/jpeg",
            "sparse",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "56,331",
            "79e4a5a5036e427f9ad9416e1222bf9061c4015de4d10aa117e159b86269b58b",
            "zh.html",
            "52,415",
            "cc8b12bd4cfa8ca4a7fd6911a7d9922286342f22d69f85cd26925eb4d1d46e0e",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hash_matches_when_present(self):
        path = ROOT / ".working" / "ihp-764" / "large.jpg"
        if path.exists():
            self.assertEqual(
                "f907975d99895f7cf9406b2cb3dde811869fd8bafdfb98c9a34d920946f6ec99",
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )

    def test_markdown_is_utf8_and_within_line_width(self):
        EVIDENCE.read_bytes().decode("utf-8")
        long_lines = [
            (number, len(line))
            for number, line in enumerate(self.text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], long_lines)


if __name__ == "__main__":
    unittest.main()
