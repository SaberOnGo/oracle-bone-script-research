import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "014_coll-obj-cand-00014_ihp-item-762_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem762LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/762/",
            "https://museum.sinica.edu.tw/collection/32/item/762/",
            "Source collection item ID / 馆藏对象号: `762`",
            "Item No. / 馆藏编号: `R034514`",
            "Inscribed Animal Bone Fragment Chia 2367",
            "Late Shang Period",
            "Animal Bone",
            "3.9(L)×2.2(W) cm",
            "Pit 3:H05, Hsiao-t'un, Anyang County, Honan Province",
            "large-eyed",
            "open-mouthed",
            "prick-eared dog",
            "source_reported_displayed_description_without_transcription",
            "No\nOCR, sentence reconstruction, or reading is added here.",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_route(self):
        required = (
            "2945f688b9cb6f9e.jpg",
            "294,518",
            "dd2730f0b6d8b741162ea5b8776123ce3c469937eb30c89f9aa927baeb47a6a0",
            "1196 x 1280",
            "image/jpeg",
            "local_private_visual_inspection_only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "56,383",
            "2f5c720d004d119c925776fb3763eeb5454f311d7045d83b31424193aafdeb57",
            "zh.html",
            "52,447",
            "4fa6f972c7ecea4df1b89defe7b50e41ef3c5627a429ef48b80473fc08104240",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_route_matches_documented_hash_when_present(self):
        path = ROOT / ".working" / "ihp-762" / "2945f688b9cb6f9e.jpg"
        if path.exists():
            self.assertEqual(
                "dd2730f0b6d8b741162ea5b8776123ce3c469937eb30c89f9aa927baeb47a6a0",
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
