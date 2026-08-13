import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "017_coll-obj-cand-00017_ihp-item-779_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem779LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_source_examples(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/779/",
            "https://museum.sinica.edu.tw/collection/32/item/779/",
            "Source collection item ID / 馆藏对象号: `779`",
            "Item No. / 馆藏编号: `R044643`",
            "Inscribed Plastron I 4718",
            "帶卜辭龜腹甲《乙》4718",
            "Late Shang Period",
            "30.4(L)×15.9(W) cm",
            "Pit YH127, Hsiao-t'un, Anyang County, Honan Province",
            "雀以象。",
            "雀不其［以象］。",
            "以馬自[inline source glyph]（孽）。十二月。允以三丙。",
            "source_reported_transcription_with_inline_glyph_gap",
            "No OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_object_and_inline_routes(self):
        required = (
            "8255f6891276e7c6.jpg",
            "323,639",
            "c613c033cf668763b90545d677ee3d1dc81ae8cc9d31a5b4fc691e78d15f00d3",
            "1063 x 1280",
            "4455f68212db40f2.jpg",
            "7045f68212dc64ca.jpg",
            "8985f68212dbe29b.jpg",
            "local_private_visual_inspection_only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "59,798",
            "d3379d8a8d3c87c266d6c469647d85c2e61a963715d840ada20865fb8a5d1021",
            "zh.html",
            "57,859",
            "62ce46e4dce0f8ba52638791d334e8a08e98d67bbf5661678c79ef204dca29ab",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_object_route_matches_documented_hash_when_present(self):
        path = ROOT / ".working" / "ihp-779" / "8255f6891276e7c6.jpg"
        if path.exists():
            self.assertEqual(
                "c613c033cf668763b90545d677ee3d1dc81ae8cc9d31a5b4fc691e78d15f00d3",
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
