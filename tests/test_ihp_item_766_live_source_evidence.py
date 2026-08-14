import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "021_coll-obj-cand-00021_ihp-item-766_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem766LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/766/",
            "https://museum.sinica.edu.tw/collection/32/item/766/",
            "Source collection item ID / 馆藏对象号: `766`",
            "Item No. / 馆藏编号: `R031973`",
            "Inscribed Plastron Fragment Chia 1961",
            "龟甲卜辞残片《甲》1961",
            "Late Shang Period",
            "2.6(L)×2.1(W) cm",
            "Hsiao-t'un, Anyang County, Honan Province",
            "source_reported_description_without_full_transcription",
            "No OCR\ncorrection",
            "related script examples",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_image_routes_and_observations(self):
        required = (
            "1515f6895ca00a73.jpg",
            "5215f6895bce7f4a.png",
            "9625f6895cc49e3a.jpg",
            "237071",
            "742502",
            "254444",
            "988 x 1280",
            "996 x 1280",
            "yellow outline",
            "R031973",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_hashes_and_snapshots(self):
        required = (
            "ca2f2c177e27e978fd489c43d32862670ae8339c745484f9cc94bc086f9a9f8e",
            "631176579e5b1095e525f844e0e87f059ddd6c224aa16297c5896ab194911f42",
            "c1883ec53ef20d67443c7709f96e35d15c2d503cdbd78d555f0a5cd588790630",
            "en.html",
            "58,892",
            "731d8f9c6f92c8a2d992b800b7e6b8be65a52fd03171bbefda1c2f8d6948f9dc",
            "zh.html",
            "55,257",
            "b957f62f49742f84248544e9da008292f2e5196d3f61b22661d3e2a3c1287ce6",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "large.jpg":
                "ca2f2c177e27e978fd489c43d32862670ae8339c745484f9cc94bc086f9a9f8e",
            "large-02.png":
                "631176579e5b1095e525f844e0e87f059ddd6c224aa16297c5896ab194911f42",
            "large-03.jpg":
                "c1883ec53ef20d67443c7709f96e35d15c2d503cdbd78d555f0a5cd588790630",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-766" / name
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
