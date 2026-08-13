import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "003_coll-obj-cand-00003_ihp-item-1213_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1213LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_page_is_linked_from_human_entries(self):
        self.assertTrue(EVIDENCE.exists())
        for name in (
            "README.md",
            "06_human-collection-dossier.md",
            "08_collection-provenance-evidence-dossier.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
            "16_preformal-research-start-check.md",
        ):
            page = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("18_live-source-evidence-review.md", page)

    def test_page_binds_plate_metadata_and_source_text(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1213/",
            "Source collection item ID / 馆藏对象号: `1213`",
            "Item No. / 对象编号: `R044295`",
            "Bing Bian 0008",
            "Late Shang Period",
            "SYFYH127, Hsiao-t'un, Anyang",
            "Turtle Plastron",
            "丙辰卜，□貞：我受黍年。",
            "王占曰：吉。受有年。",
            "source_reported_partial_transcription_with_placeholders",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_two_image_routes_and_checksums(self):
        routes = (
            (
                "4636755e7bcd4f54.jpg",
                "386,024",
                "733fe6fc4b325dfd3f9f544563dd30b8a4d843a43580e13edfcbffd04109e122",
                "948 x 1280",
            ),
            (
                "6936755e7c01b5d2.jpg",
                "463,062",
                "f4a0898552420ae7cf71b6376d1d3cd6af5fc09f90265de04f6c78923f0b87f6",
                "962 x 1280",
            ),
        )
        for filename, size, digest, pixels in routes:
            self.assertIn(filename, self.text)
            self.assertIn(size, self.text)
            self.assertIn(digest, self.text)
            self.assertIn(pixels, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 2)
        self.assertEqual(self.text.count("local_private_visual_inspection_only"), 2)

    def test_page_keeps_partial_quality_rights_and_boundary(self):
        required = (
            "metadata_only_until_verified",
            "not a new transcription",
            "not a confirmed",
            "破译结论",
            "具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

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
