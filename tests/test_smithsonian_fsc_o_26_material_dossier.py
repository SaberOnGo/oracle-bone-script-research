import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT_DIR = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches/002_collection-object-candidates"
    / "053_coll-obj-cand-00053_si-nmaa-fsc-o-26_collection-object-candidate"
)
DOSSIER = OBJECT_DIR / "20_human-material-evidence-dossier.md"
QUEUE_REVIEW = (
    ROOT
    / "doc/public/user_research/010_source-pipeline-missing-evidence-review-queues"
    / "014_src-smithsonian-nmaa-oracle-bone.md"
)
ASSET = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches"
    / "001_public-domain-object-image-assets"
    / "003_asset-000003_si-nmaa-fsc-o-26_object-image.jpg"
)


class SmithsonianFscO26MaterialDossierTests(unittest.TestCase):
    def test_dossier_is_object_local_and_human_readable(self):
        self.assertTrue(DOSSIER.is_file())
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("FSC-O-26", text)
        self.assertIn("直接视觉观察", text)
        self.assertIn("Contradictions And Negative Evidence", text)
        self.assertIn("not a confirmed object identity", text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_dossier_binds_the_committed_asset(self):
        self.assertTrue(ASSET.is_file())
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("[fsc-image]: ../../001_public-domain-object-image-assets/", text)
        self.assertIn("003_asset-000003_si-nmaa-fsc-o-26_object-image.jpg", text)
        digest = hashlib.sha256(ASSET.read_bytes()).hexdigest()
        match = re.search(r"SHA-256: `([0-9a-f]{64})`", text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), digest)
        self.assertIn("633418", text)
        self.assertIn("3000 x 2000", text)

    def test_dossier_preserves_source_and_rights_boundaries(self):
        text = DOSSIER.read_text(encoding="utf-8")
        required = (
            "dl-smithsonian-nmaa-fsc-o-26-archive",
            "4e641c8fe84a92f800bbe2bea1b118230a4ad01c8d560cb10f6130901c18c6cb",
            "https://ids.si.edu/ids/manifest/FS-FSC-O-26_1",
            "public_domain_verified",
            "needs_human_collection_object_review",
            "not a transcription",
        )
        for value in required:
            self.assertIn(value, text)

    def test_source_queue_points_to_the_new_object_dossier(self):
        text = QUEUE_REVIEW.read_text(encoding="utf-8")
        self.assertIn("053_coll-obj-cand-00053_si-nmaa-fsc-o-26", text)
        self.assertIn("20_human-material-evidence-dossier.md", text)
        self.assertIn("does not close", text)


if __name__ == "__main__":
    unittest.main()
