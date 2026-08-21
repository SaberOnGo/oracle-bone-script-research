import hashlib
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "008_obs-insc-src-cand-000008_met-42045_source-record-candidate"
)
PAGE = OBJECT / "09_two-view-human-evidence.md"
README = OBJECT / "README.md"
ASSETS = OBJECT / "03_visual-assets"

EXPECTED = {
    "001_asset-000001_met-42045-image-002.jpg": (
        1_780_568,
        "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
    ),
    "002_asset-000002_met-42045-image-001.jpg": (
        1_616_877,
        "c2c09d618ed7da7e38b845164186590f7fa416ec3487a319c7de75b84330a480",
    ),
}


class Met42045InscriptionEvidenceTests(unittest.TestCase):
    def test_page_is_bilingual_and_human_bounded(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("Two-view Human Evidence", text)
        self.assertIn("双图人类证据", text)
        self.assertIn("Cross-view comparison", text)
        self.assertIn("不统计字数", text)
        self.assertIn("not OCR", text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_page_binds_both_image_bytes_and_dimensions(self):
        text = PAGE.read_text(encoding="utf-8")
        for name, (size, digest) in EXPECTED.items():
            path = ASSETS / name
            self.assertEqual(path.stat().st_size, size)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
            with Image.open(path) as image:
                self.assertEqual(image.size, (2667, 4000))
            self.assertIn(name, text)
            self.assertIn(str(size), text)
            self.assertIn(digest, text)

    def test_page_preserves_source_and_orientation_boundaries(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("src-metmuseum-oracle-bone", text)
        self.assertIn("dl-metmuseum-object-42045", text)
        self.assertIn("primaryImage", text)
        self.assertIn("additionalImages[0]", text)
        self.assertIn("recto-verso relation", text)
        self.assertIn("does\n  not define", text)
        self.assertIn("public_domain_verified", text)
        self.assertIn("No image derivative", text)
        self.assertIn("No OCR", text)
        self.assertIn("Heji number", text)

    def test_readme_links_the_two_view_page_in_both_languages(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("09_two-view-human-evidence.md", text)
        self.assertIn("双图证据和限制", text)


if __name__ == "__main__":
    unittest.main()
