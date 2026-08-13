import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "001_coll-obj-cand-00001_ihp-item-1212_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1212LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_evidence_page_is_linked_from_human_entries(self):
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

    def test_page_binds_official_object_metadata(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1212/",
            "Source collection item ID / 馆藏对象号: `1212`",
            "Item No. / 对象编号: `R035888`",
            "Jia Bian 3333+3361",
            "Late Shang Period",
            "Hsiao-t'un, Anyang County",
            "Animal Bone",
            "戊戌帚（婦）喜示一屯。岳。",
            "source_reported_short_text",
            "verified_full_inscription",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_all_image_route_results(self):
        routes = (
            (
                "8876755e62227572.jpg",
                "image/jpeg",
                "198,619",
                "6d710da16e45592a386bb38988658b3634cc1af57da53de1f14f023c55c20e50",
            ),
            (
                "834675e62687616.jpg",
                "text/html; charset=UTF-8",
                "107,210",
                "79db16fe3b85fb6af975ed98c929db66b0a458e8e1c5cc3003395d0af023ee75",
            ),
            (
                "4656755e636be034.jpg",
                "image/jpeg",
                "122,839",
                "9c286d8829a572386c26dbd8edb0574c18c2f3c042761dee1ec3ba5e40916020",
            ),
        )
        for filename, content_type, size, digest in routes:
            self.assertIn(filename, self.text)
            self.assertIn(content_type, self.text)
            self.assertIn(size, self.text)
            self.assertIn(digest, self.text)
        self.assertIn("route_redirected_not_image", self.text)
        self.assertIn("local_private_visual_inspection_only", self.text)

    def test_page_keeps_rights_and_research_boundary(self):
        required = (
            "metadata_only_until_verified",
            "no image is committed",
            "不提交图像",
            "not a confirmed",
            "破译结果",
            "具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_markdown_is_utf8_and_within_line_width(self):
        raw = EVIDENCE.read_bytes()
        raw.decode("utf-8")
        long_lines = [
            (number, len(line))
            for number, line in enumerate(self.text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], long_lines)


if __name__ == "__main__":
    unittest.main()
