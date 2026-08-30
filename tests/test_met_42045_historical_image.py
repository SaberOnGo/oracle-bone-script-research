import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "008_obs-insc-src-cand-000008_met-42045_source-record-candidate"
)
PAGE = OBJECT / "11_historical-inscribed-face-evidence.md"
ASSET = (
    OBJECT
    / "03_visual-assets/003_asset-000003_met-42045-historical-view.jpeg"
)


class Met42045HistoricalImageTests(unittest.TestCase):
    def test_asset_is_checksum_bound_and_publicly_routed(self):
        self.assertTrue(ASSET.is_file())
        data = ASSET.read_bytes()
        self.assertEqual(len(data), 35178)
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "5a066d9205f4ef492e0d0d530acd5229315e1a99411982c3133adfe1e154163d",
        )
        with Image.open(ASSET) as image:
            self.assertEqual(image.size, (900, 207))

    def test_human_page_is_linked_bilingual_and_bounded(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn(PAGE.name, readme)
        text = PAGE.read_text(encoding="utf-8")
        for marker in (
            "Historical Inscribed-Face Image Evidence",
            "早期刻辞面图像证据",
            "inscribed_surface_candidate",
            "反证与替代解释",
            "Falsification conditions",
            "不新增释文",
        ):
            self.assertIn(marker, text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_support_record_keeps_surface_and_text_boundaries(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(record["image_routes"]), 2)
        self.assertEqual(len(record["historical_image_routes"]), 1)
        route = record["historical_image_routes"][0]
        self.assertEqual(route["size_bytes"], 35178)
        self.assertEqual(route["pixels"], "900x207")
        self.assertEqual(
            route["surface_relation_status"],
            "inscribed_surface_candidate_not_pixel_identical",
        )
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertIn(
            "no project transcription or translation", record["boundaries"]
        )

    def test_global_guide_exposes_the_third_image(self):
        guide = (
            ROOT
            / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
            "005_opened-source-record-candidate-guide.md"
        ).read_text(encoding="utf-8")
        self.assertIn("one earlier high-contrast CC0 image", guide)
        self.assertIn("早期高反差 CC0 图像", guide)

    def test_completion_audit_records_progress_without_closure(self):
        audit = (
            ROOT
            / "corpus/009_statistics-and-derived-features/"
            "231_preprocessing-completion-audit-2026-08-12.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Material update / 资料更新: `2026-08-30`", audit)
        self.assertIn("The Met `42045` / `67.43.14` dossier", audit)
        self.assertIn("Met `42045` / `67.43.14` 档案", audit)
        self.assertIn("Audit result / 审计结论: `not_complete`", audit)
        self.assertTrue(all(len(line) <= 80 for line in audit.splitlines()))


if __name__ == "__main__":
    unittest.main()
