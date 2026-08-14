import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
)
IMAGE = OBJECT / "03_visual-assets/001_asset-000001_ningxia-hyz421_h3-1325.jpg"


class NingxiaHyz421SourceRecordTests(unittest.TestCase):
    def test_human_entry_and_parent_link_exist(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "corpus" / "002_oracle-bone-inscriptions" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("obs-insc-src-cand-000007", parent)
        self.assertIn("[ningxia-hyz421-candidate]", parent)
        for name in (
            "01_object-and-image-routes.md",
            "02_human-inscription-dossier.md",
            "03_source-evidence-review.md",
            "04_text-quality-review.md",
            "05_character-linkage-review.md",
            "06_literature-and-dispute-review.md",
            "07_missing-evidence-plan.md",
        ):
            self.assertTrue((OBJECT / name).is_file(), name)
            self.assertIn(name, readme)

    def test_image_bytes_match_human_and_machine_receipts(self):
        self.assertTrue(IMAGE.is_file(), IMAGE)
        data = IMAGE.read_bytes()
        self.assertEqual(len(data), 2302630)
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "b4f44b4a325d0a24c605ce84ae3c8180177407e59709e69892185fb66398adaa",
        )
        self.assertEqual(
            hashlib.sha1(data).hexdigest(),
            "30a8c1000ea08df01199e4ae20d90053cc434802",
        )
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (3001, 3345))
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.mode, "RGB")
        route = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )["image_route"]
        self.assertEqual(route["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(route["sha1"], hashlib.sha1(data).hexdigest())
        self.assertEqual(route["size_bytes"], len(data))
        self.assertEqual(route["pixels"], "3001x3345")

    def test_source_text_and_context_remain_source_reported(self):
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8"
        )
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        for marker in (
            "HYZ 421, H3:1325",
            "Huayuanzhuang",
            "壬辰夕卜：其宜（俎）一于，若?用。",
            "not an independent transcription",
            "not assigned",
        ):
            self.assertIn(marker, dossier)
        self.assertEqual(
            record["text_status"],
            "source_display_only_without_project_transcription",
        )
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertEqual(record["rights_status"], "source_marked_risk_noted")
        self.assertIn("no decipherment conclusion", record["boundaries"])

    def test_literature_and_rights_routes_are_explicit(self):
        literature = (OBJECT / "06_literature-and-dispute-review.md").read_text(
            encoding="utf-8"
        )
        evidence = (OBJECT / "03_source-evidence-review.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "Schwartz",
            "347",
            "561",
            "source_citation_route_only",
            "dispute_status_unresolved",
        ):
            self.assertIn(marker, literature)
        self.assertIn("CC BY-SA 3.0", evidence)
        self.assertIn("museum object", evidence)

    def test_human_markdown_is_utf8_and_within_80_columns(self):
        for path in OBJECT.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            for line_number, line in enumerate(text.splitlines(), 1):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
