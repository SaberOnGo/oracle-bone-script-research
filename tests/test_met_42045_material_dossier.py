import hashlib
import json
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
CROSSWALK = OBJECT / "21_source-record-crosswalk.md"
SOURCE_RECORD = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "008_obs-insc-src-cand-000008_met-42045_source-record-candidate"
)
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

    def test_collection_object_hands_off_to_the_two_view_record(self):
        text = CROSSWALK.read_text(encoding="utf-8")
        self.assertIn("Source-record crosswalk", text)
        self.assertIn("来源记录交接", text)
        self.assertIn("obs-insc-src-cand-000008", text)
        self.assertIn("09_two-view-human-evidence.md", text)
        self.assertIn("c605ae36...e0333df", text)
        self.assertIn("c2c09d61...30a480", text)
        self.assertIn("No Heji number", text)
        self.assertIn("没有提供合集号", text)
        self.assertIn("source_record_candidate_needs_text_and_catalog_review", text)
        self.assertNotIn("confirmed reading", text.lower())
        self.assertNotIn("释读结论", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_collection_index_and_source_record_bind_same_two_images(self):
        index = json.loads(
            (OBJECT / "07_collection-dossier-index.json").read_text(
                encoding="utf-8"
            )
        )
        crosswalk = str(CROSSWALK.relative_to(ROOT)).replace("\\", "/")
        self.assertIn(crosswalk, index["human_readable_files"])

        record = json.loads(
            (SOURCE_RECORD / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["object_id"], 42045)
        self.assertEqual(len(record["image_routes"]), 2)
        for route in record["image_routes"]:
            image = SOURCE_RECORD / route["committed_path"]
            self.assertEqual(image.stat().st_size, route["size_bytes"])
            self.assertEqual(
                hashlib.sha256(image.read_bytes()).hexdigest(), route["sha256"]
            )


if __name__ == "__main__":
    unittest.main()
