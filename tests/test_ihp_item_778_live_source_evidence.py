import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "016_coll-obj-cand-00016_ihp-item-778_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem778LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/778/",
            "https://museum.sinica.edu.tw/collection/32/item/778/",
            "Source collection item ID / 馆藏对象号: `778`",
            "Item No. / 馆藏编号: `R044636`",
            "Inscribed Plastron I 4603",
            "帶卜辭龜腹甲《乙》4603",
            "Late Shang Period",
            "24.2(L)×17.8(W) cm",
            "Pit YH127, Hsiao-t'un, Anyang County, Honan Province",
            "乙酉卜：御新于父戊白豭。",
            "己丑卜：御于帝［卅］小牢。己丑。余至（致）䝅、羊。",
            "叀小牢于父戊。",
            "source_reported_transcription_with_inline_glyph_gap",
            "豖, 豚, and 彘",
            "No OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_object_and_inline_routes(self):
        required = (
            "6885f688e9d124ba.jpg",
            "304,628",
            "d81bdb386a4c2cb0f66a29219932685577ed580c55ad84b753e3bb894684386c",
            "959 x 1280",
            "1435f6722ec39217.png",
            "2065f6722a56f871.png",
            "7485f672717850bd.jpg",
            "local_private_visual_inspection_only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "64,185",
            "9c873886a6ec194d86a3f971cea1ab3f83c132efd4fa87da5e98016dd6747254",
            "zh.html",
            "60,770",
            "0cbf191442b302c4c13a967f2bf0aed9dc42c7f604f95d078fcf6d2e8d2453a5",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_object_route_matches_documented_hash_when_present(self):
        path = ROOT / ".working" / "ihp-778" / "6885f688e9d124ba.jpg"
        if path.exists():
            self.assertEqual(
                "d81bdb386a4c2cb0f66a29219932685577ed580c55ad84b753e3bb894684386c",
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
