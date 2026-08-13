import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "004_coll-obj-cand-00004_ihp-item-1215_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1215LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/1215/",
            "Source collection item ID / 馆藏对象号: `1215`",
            "Item No. / 馆藏编号: `R044587`",
            "Yi Bian 3330+5281+Yi Bian buyi 4936",
            "Late Shang Period",
            "Pit YH127, Hsiao-t'un,",
            "Anyang County, Honan Province",
            "Turtle Plastron",
            "帚（婦）井示。韋。",
            "source_reported_short_display_without_independent_edition",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_image_routes_and_checksums(self):
        routes = (
            (
                "6716755ee8c5a912.jpg",
                "265,876",
                "bceef865308f6ad7351b6d8e7f3dfedf53bb57f4dba05e93745"
                "2ba54ec819175",
                "869 x 1280",
            ),
            (
                "1526755ee906c069.jpg",
                "303,001",
                "c87562d1e2c6f20c5fc5f5ae8ecc4f240862c99f0d93c7ce36"
                "aa85132c16a819",
                "827 x 1280",
            ),
            (
                "4936755ee94db0fb.jpg",
                "267,539",
                "f3562d4ce4c61c4fd827c29a04ab000102bc104c805f75777e64b"
                "c40a59a3169",
                "1280 x 1128",
            ),
        )
        for filename, size, digest, pixels in routes:
            self.assertIn(filename, self.text)
            self.assertIn(size, self.text)
            self.assertIn(digest, self.text)
            self.assertIn(pixels, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 3)
        self.assertEqual(
            self.text.count("local_private_visual_inspection_only"), 3
        )

    def test_page_keeps_partial_quality_rights_and_boundary(self):
        required = (
            "metadata_only_until_verified",
            "not a new transcription",
            "not a confirmed",
            "source-reported museum wording",
            "Concrete next checks / 具体下一步待查",
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
