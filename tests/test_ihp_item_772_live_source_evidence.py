import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "041_coll-obj-cand-00041_ihp-item-772_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem772LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/772/",
            "https://museum.sinica.edu.tw/collection/32/item/772/",
            "Source collection item ID / 馆藏对象号: `772`",
            "Item No. / 馆藏编号: `R044284`",
            "Inscribed Plastron Ping 0069",
            "Late Shang Period",
            "18.4(L)×11.1(W) cm",
            "source_reported_description_without_independent_transcription",
            "personal-name characters",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_routes_and_visual_boundary(self):
        required = (
            "1005f4898e0ceda4.jpg",
            "55,514",
            "274,360",
            "525,593",
            "294 x 480",
            "785 x 1280",
            "1177 x 1920",
            "Multiple broad cracks",
            "black museum marking",
            "pixels only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_image_and_html_hashes(self):
        required = (
            "0d752b7304414b7432efa032784bab618a5b6e70d2f3a2b956d5ed9cc795c996",
            "0472d2a048b09051c3286717455120290a92efa2c44aa0f19b10d426082b4ec3",
            "6d3f48a729b9083338abd44dd8aecb2761c9f5412e965283bc16a3349b2c10c5",
            "3a55ef620fe015f8932a8d64619e0f761a87fb1969ece733ef74c2dd076814e4",
            "97d88feff087547d468f8fd06eaad38856e5786af24ab441f8c0b740da05ba24",
            "Concrete next checks / 具体待查问题",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "thumbnail-1005f4898e0ceda4.jpg":
                "0d752b7304414b7432efa032784bab618a5b6e70d2f3a2b956d5ed9cc79"
                "5c996",
            "large-1005f4898e0ceda4.jpg":
                "0472d2a048b09051c3286717455120290a92efa2c44aa0f19b10d426082b"
                "4ec3",
            "hd-1005f4898e0ceda4.jpg":
                "6d3f48a729b9083338abd44dd8aecb2761c9f5412e965283bc16a3349b2c10"
                "c5",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-772" / name
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
