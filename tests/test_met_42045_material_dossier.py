import hashlib
import re
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches/002_collection-object-"
    "candidates/055_coll-obj-cand-00055_met-obj-42045_collection-object-"
    "candidate"
)
DOSSIER = OBJECT / "20_human-material-evidence-dossier.md"
IMAGE = (
    ROOT
    / "corpus/005_excavation-sites-periods-and-batches/001_public-domain-"
    "object-image-assets/001_asset-000001_met-obj-42045_object-image.jpg"
)
QUEUE = (
    ROOT
    / "doc/public/user_research/010_source-pipeline-missing-evidence-review-"
    "queues/006_src-metmuseum-oracle-bone.md"
)


class Met42045MaterialDossierTests(unittest.TestCase):
    def test_dossier_is_object_local_and_human_readable(self):
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("Human Material Evidence Dossier", text)
        self.assertIn("实物证据档案", text)
        self.assertIn("Direct Visual Observations", text)
        self.assertIn("not a transcription", text)
        self.assertIn("不是已确认", text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_dossier_binds_the_committed_asset(self):
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertEqual(IMAGE.stat().st_size, 1_780_568)
        self.assertEqual(
            hashlib.sha256(IMAGE.read_bytes()).hexdigest(),
            "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
        )
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (2667, 4000))
        self.assertIn("001_asset-000001_met-obj-42045_object-image.jpg", text)
        self.assertIn("2667 x 4000", text)
        self.assertIn("1780568", text)
        self.assertIn(
            "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
            text,
        )

    def test_dossier_preserves_source_and_rights_boundaries(self):
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("src-metmuseum-oracle-bone", text)
        self.assertIn("dl-metmuseum-object-42045", text)
        self.assertIn("pkg-file-000021", text)
        self.assertIn("74efc7255beeed6cf1400d86c336c5b97a5638a683956e83fa7216ad42f152b9", text)
        self.assertIn("public_domain_verified", text)
        self.assertIn("needs_human_collection_object_review", text)
        self.assertIn("No project inscription ID", text)
        self.assertIn("scholarly conclusion", text)

    def test_source_queue_points_to_the_new_object_dossier(self):
        text = QUEUE.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            re.compile(
                r"055_coll-obj-cand-00055_met-obj-42045_collection-object-.*"
                r"20_human-material-evidence-dossier\.md",
                re.DOTALL,
            ),
        )
        self.assertIn("不建立字序或释文", text)


if __name__ == "__main__":
    unittest.main()
