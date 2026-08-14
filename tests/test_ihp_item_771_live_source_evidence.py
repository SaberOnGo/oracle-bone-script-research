import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "040_coll-obj-cand-00040_ihp-item-771_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem771LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_evidence_is_linked_from_human_entries(self):
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

    def test_page_binds_metadata_and_translation_boundary(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/771/",
            "https://museum.sinica.edu.tw/collection/32/item/771/",
            "Source collection item ID / 馆藏对象号: `771`",
            "Item No. / 馆藏编号: `R039275+R043001`",
            "Inscribed Plastron I 5867+8202",
            "Late Shang Period",
            "R039275: 5.5(L)×2.7(W) cm",
            "R043001: 10.5(L)×5.4(W) cm",
            "source_reported_proposed_translation_without_independent_review",
            "personal-name character",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_routes_and_visual_boundary(self):
        required = (
            "115f488d1fb39b0.jpg",
            "41,585",
            "213,137",
            "402,428",
            "216 x 480",
            "576 x 1280",
            "864 x 1920",
            "Dark circular or oval areas",
            "presentation view",
            "pixels only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_image_and_html_hashes(self):
        required = (
            "46d6239db5a26c9ce349332df8ee61b3eddb7937be7b9f9ad9880c9405777f66",
            "b8d7bb2be97271ee3a6d7abdd2c082c246c58d2e954b4ceae451eb98a781ec93",
            "2d7d4147f4c977f8c7cd816d9f1fbcca0713e65252ceb41ebf6a4a6f53025a07",
            "1ce9d5b26edf40075735be33a5b3380957aacf768deaa9397ef0214c483b4c80",
            "47dcd16ccfe72f8a8aba9944daef98d68f8703e6ca04e140028717daa96fd2c3",
            "Concrete next checks / 具体待查问题",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "thumbnail-115f488d1fb39b0.jpg":
                "46d6239db5a26c9ce349332df8ee61b3eddb7937be7b9f9ad9880c9405"
                "777f66",
            "large-115f488d1fb39b0.jpg":
                "b8d7bb2be97271ee3a6d7abdd2c082c246c58d2e954b4ceae451eb98a781"
                "ec93",
            "hd-115f488d1fb39b0.jpg":
                "2d7d4147f4c977f8c7cd816d9f1fbcca0713e65252ceb41ebf6a4a6f530"
                "25a07",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-771" / name
            if path.exists():
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(digest, actual)

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
