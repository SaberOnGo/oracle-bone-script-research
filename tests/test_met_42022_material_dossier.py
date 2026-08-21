import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT_DIR = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches/002_collection-object-candidates"
    / "056_coll-obj-cand-00056_met-obj-42022_collection-object-candidate"
)
DOSSIER = OBJECT_DIR / "20_human-material-evidence-dossier.md"
ASSET = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches"
    / "001_public-domain-object-image-assets"
    / "002_asset-000002_met-obj-42022_object-image.jpg"
)
QUEUE_REVIEW = (
    ROOT
    / "doc/public/user_research/010_source-pipeline-missing-evidence-review-queues"
    / "006_src-metmuseum-oracle-bone.md"
)


class Met42022MaterialDossierTests(unittest.TestCase):
    def test_dossier_is_object_local_and_human_readable(self):
        self.assertTrue(DOSSIER.is_file())
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("18.56.71", text)
        self.assertIn("直接视觉观察", text)
        self.assertIn("Counterevidence And Alternative Explanations", text)
        self.assertIn("not a transcription", text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_dossier_binds_the_committed_asset(self):
        self.assertTrue(ASSET.is_file())
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn(
            "[met-image]: ../../001_public-domain-object-image-assets/",
            text,
        )
        self.assertIn(
            "002_asset-000002_met-obj-42022_object-image.jpg",
            text,
        )
        digest = hashlib.sha256(ASSET.read_bytes()).hexdigest()
        match = re.search(r"SHA-256: `([0-9a-f]{64})`", text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), digest)
        self.assertIn("2508142", text)
        self.assertIn("4000 x 2667", text)

    def test_dossier_preserves_source_and_rights_boundaries(self):
        text = DOSSIER.read_text(encoding="utf-8")
        required = (
            "dl-metmuseum-object-42022",
            "6476cda2ef3e03fefb80be4c9b725e78b460131f7246d0faff101066297545c0",
            "pkg-file-000020",
            "public_domain_verified",
            "needs_human_collection_object_review",
            "not a confirmed object identity",
        )
        for value in required:
            self.assertIn(value, text)

    def test_source_queue_points_to_the_new_object_dossier(self):
        text = QUEUE_REVIEW.read_text(encoding="utf-8")
        self.assertIn("056_coll-obj-cand-00056_met-obj-42022", text)
        self.assertIn("20_human-material-evidence-dossier.md", text)
        self.assertIn("does not close", text)


if __name__ == "__main__":
    unittest.main()
