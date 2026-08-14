import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "023_coll-obj-cand-00023_ihp-item-767_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem767LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/767/",
            "https://museum.sinica.edu.tw/collection/32/item/767/",
            "Source collection item ID / 馆藏对象号: `767`",
            "Item No. / 馆藏编号: `R030491`",
            "Inscribed Plastron Fragment Chia 0984",
            "龟甲卜辞残片《甲》0984",
            "Late Shang Period",
            "3.2(L)×1.8(W) cm",
            "Hsiao-t'un, Anyan County, Honan Province",
            "source_reported_description_without_full_transcription",
            "related-script\nexamples",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_image_routes_and_observations(self):
        required = (
            "4655f6897a47acc5.jpg",
            "9765f6897988fdec.png",
            "8175f6897a22be68.jpg",
            "281916",
            "727422",
            "263057",
            "988 x 1280",
            "757 x 1280",
            "yellow outline",
            "R030491",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_hashes_and_snapshots(self):
        required = (
            "9d44de1fd01ffec9d47540fc1a6a75559ca50a27325671fb37c5a00053c494b8",
            "43c1c8bce063233600386c034b9ac5be3f70d4918f40ba6f987547932df664f3",
            "2f1d9bf10f3d301a3d7e28333a19c1e6226427b8314fe26738949ee54770c278",
            "en.html",
            "58,192",
            "ced71abd8aa3fd4614cb7fe6943dbb25f1b28db4c50d7bb47057fed2a260092a",
            "zh.html",
            "54,328",
            "5a4b00c3d78394b4123d432b491f7a5021bf1063b058d313eafce6c5e996f689",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "large.jpg":
                "9d44de1fd01ffec9d47540fc1a6a75559ca50a27325671fb37c5a00053c494b8",
            "large-02.png":
                "43c1c8bce063233600386c034b9ac5be3f70d4918f40ba6f987547932df664f3",
            "large-03.jpg":
                "2f1d9bf10f3d301a3d7e28333a19c1e6226427b8314fe26738949ee54770c278",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-767" / name
            if path.exists():
                self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())

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
