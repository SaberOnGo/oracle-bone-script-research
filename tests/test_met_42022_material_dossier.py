import hashlib
import json
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
CROSSWALK = OBJECT_DIR / "21_source-record-crosswalk.md"
SOURCE_RECORD = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "009_obs-insc-src-cand-000009_met-42022_source-record-candidate"
)
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

    def test_collection_object_hands_off_to_the_two_view_record(self):
        text = CROSSWALK.read_text(encoding="utf-8")
        self.assertIn("Source-record crosswalk", text)
        self.assertIn("来源记录交接", text)
        self.assertIn("obs-insc-src-cand-000009", text)
        self.assertIn("09_two-view-human-evidence.md", text)
        self.assertIn("61510f04...adad8cd", text)
        self.assertIn("c58ede9b...690122e", text)
        self.assertIn("No Heji number", text)
        self.assertIn("没有提供合集号", text)
        self.assertIn("source_record_candidate_needs_text_and_catalog_review", text)
        self.assertNotIn("confirmed reading", text.lower())
        self.assertNotIn("释读结论", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_collection_index_and_source_record_bind_same_two_images(self):
        index = json.loads(
            (OBJECT_DIR / "07_collection-dossier-index.json").read_text(
                encoding="utf-8"
            )
        )
        crosswalk = str(CROSSWALK.relative_to(ROOT)).replace("\\", "/")
        self.assertIn(crosswalk, index["human_readable_files"])

        record = json.loads(
            (SOURCE_RECORD / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["object_id"], 42022)
        self.assertEqual(len(record["image_routes"]), 2)
        for route in record["image_routes"]:
            image = SOURCE_RECORD / route["committed_path"]
            self.assertEqual(image.stat().st_size, route["size_bytes"])
            self.assertEqual(
                hashlib.sha256(image.read_bytes()).hexdigest(), route["sha256"]
            )


if __name__ == "__main__":
    unittest.main()
