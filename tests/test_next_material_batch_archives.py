from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IHP = ROOT / (
    "corpus/005_excavation-sites-periods-and-batches/002_collection-object-"
    "candidates/001_coll-obj-cand-00001_ihp-item-1212_collection-object-"
    "candidate"
)
SMITHSONIAN = ROOT / (
    "corpus/005_excavation-sites-periods-and-batches/002_collection-object-"
    "candidates/053_coll-obj-cand-00053_si-nmaa-fsc-o-26_collection-object-"
    "candidate"
)
CHARACTER = ROOT / (
    "corpus/001_oracle-characters/002_000101-000200_obs-char-bucket_"
    "oracle-characters/101_obs-char-000101_hust-obc-cat-0112_oracle-character"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class NextMaterialBatchArchiveTests(unittest.TestCase):
    def assert_markdown_quality(self, path: Path) -> str:
        text = path.read_text(encoding="utf-8")
        self.assertFalse(
            [line for line in text.splitlines() if len(line) > 80],
            path.as_posix(),
        )
        self.assertTrue("English" in text or "human-readable" in text)
        self.assertTrue("中文" in text or "简体中文" in text)
        return text

    def test_ihp_catalog_plate_audit_preserves_metadata_only_boundary(self):
        path = IHP / "17_catalog-to-plate-identity-audit.md"
        text = self.assert_markdown_quality(path)
        self.assertIn(
            "3756b0a5bbf7dc4b595e0f363bd9f5a0ab818d667ca0303903ef74eb7dcdfe57",
            text,
        )
        self.assertIn("Jia Bian 3333+3361", text)
        self.assertIn("metadata_only_until_verified", text)
        self.assertIn("not a confirmed plate or inscription identity", text)
        self.assertIn("具体下一步核查", text)

    def test_smithsonian_audit_binds_the_committed_image(self):
        image = ROOT / (
            "corpus/005_excavation-sites-periods-and-batches/001_public-domain-"
            "object-image-assets/003_asset-000003_si-nmaa-fsc-o-26_"
            "object-image.jpg"
        )
        self.assertEqual(image.stat().st_size, 633418)
        self.assertEqual(
            sha256(image),
            "e4152d2d680234decb8d4b04225c83a59955b69bc4d8b10eebe7a98d54259079",
        )
        text = self.assert_markdown_quality(
            SMITHSONIAN / "19_visible-surface-catalog-description-audit.md"
        )
        self.assertIn("FSC-O-26", text)
        self.assertIn("3000 x 2000", text)
        self.assertIn("No inscription-bearing surface is legible", text)
        self.assertIn(
            "does not establish that the object lacks an inscription", text
        )
        self.assertIn("https://ids.si.edu/ids/manifest/FS-FSC-O-26_1", text)

    def test_hust_0101_audit_is_an_explicit_abstention_record(self):
        image = CHARACTER / (
            "03_visual-assets/001_asset-000106_hust-obc-cat-0112_glyph.png"
        )
        self.assertEqual(image.stat().st_size, 1635)
        self.assertEqual(
            sha256(image),
            "d4d4c7351881b664dfd52668f2865e531d381222de7dc18335551d1ef4badd38",
        )
        text = self.assert_markdown_quality(
            CHARACTER / "15_source-image-catalog-gap-abstention-dossier.md"
        )
        self.assertIn("G_0112_乙8896合22246子組.png", text)
        self.assertIn("abstain_withhold_candidate", text)
        self.assertIn(
            "No reviewed OBIMD or EvoBC character match", text
        )
        self.assertIn("It is not a confirmed", text)
        self.assertIn("character record", text)
        self.assertIn("not a reading", text)
        self.assertIn("not an accepted", text)


if __name__ == "__main__":
    unittest.main()
