import csv
import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "009_obs-insc-src-cand-000009_met-42022_source-record-candidate"
)
ASSETS = OBJECT / "03_visual-assets"
MAP = (
    ROOT
    / "project_registry/002_project-id-to-source-reference-map/"
    "008_oracle-inscription-source-record-candidate-map.csv"
)
EXPECTED = {
    "001_asset-021414_met-42022-image-002.jpg": (
        2508142,
        "61510f04c8d599e4e5f9bf50ebcb1cb2163ebd7243e4a125ce08e73fdadad8cd",
        "primaryImage",
    ),
    "002_asset-021415_met-42022-image-001.jpg": (
        2643473,
        "c58ede9b6aa3fe82128ecf0522abb4969d25afd1c8fba17217b3208cd690122e",
        "additionalImages[0]",
    ),
}


class Met42022InscriptionEvidenceTests(unittest.TestCase):
    def test_human_pages_are_bilingual_and_bounded(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## English", readme)
        self.assertIn("## 简体中文", readme)
        self.assertIn("obs-insc-src-cand-000009", readme)
        for path in OBJECT.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for number, line in enumerate(text.splitlines(), 1):
                self.assertLessEqual(
                    len(line), 80, f"{path}:{number}: {len(line)} characters"
                )

    def test_record_and_pages_keep_candidate_boundary(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000009")
        self.assertEqual(record["object_id"], 42022)
        self.assertEqual(record["accession_number"], "18.56.71")
        self.assertEqual(record["rights_status"], "public_domain_verified")
        self.assertEqual(record["formal_inscription_identity"], "not_assigned")
        self.assertEqual(record["character_links"], [])
        self.assertIn("no decipherment conclusion", record["boundaries"])
        self.assertEqual(record["claim_gate_review"]["c1_object_identity"], "blocked")
        self.assertEqual(
            record["claim_gate_review"]["c2_direct_glyph_observation"],
            "direct_checked",
        )
        self.assertEqual(record["claim_gate_review"]["c8_user_delivery"], "withheld")
        self.assertEqual(len(record["image_routes"]), 2)
        dossier = (OBJECT / "02_human-inscription-dossier.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "full text and OCR",
            "not a\ntranscription",
            "decipherment",
            "not assigned",
        ):
            self.assertIn(marker, dossier)
        gate = (OBJECT / "10_claim-evidence-gate-review.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "C1 object identity",
            "C2 direct glyph observation",
            "C4 inscription occurrence and context",
            "C8 complete proposition and user delivery",
            "C1 对象身份",
            "C8 完整命题与用户交付",
            "no user-facing",
            "candidate delivery",
            "没有面向用户的候选",
            "交付",
        ):
            self.assertIn(marker, gate)

    def test_images_match_recorded_hashes_and_dimensions(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        routes = {
            Path(route["committed_path"]).name: route
            for route in record["image_routes"]
        }
        for name, (size, digest, api_field) in EXPECTED.items():
            path = ASSETS / name
            self.assertTrue(path.is_file(), path)
            data = path.read_bytes()
            self.assertEqual(len(data), size)
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            self.assertEqual(routes[name]["size_bytes"], size)
            self.assertEqual(routes[name]["sha256"], digest)
            self.assertEqual(routes[name]["api_field"], api_field)
            with Image.open(path) as image:
                self.assertEqual(image.size, (4000, 2667))

    def test_parent_readme_and_source_map_link_candidate(self):
        parent = (ROOT / "corpus/002_oracle-bone-inscriptions/README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("[met-42022-candidate]", parent)
        with MAP.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        row = next(
            item
            for item in rows
            if item["project_id"] == "obs-insc-src-cand-000009"
        )
        self.assertEqual(row["primary_external_ref_id"], "Met-42022;18.56.71")
        self.assertEqual(row["rights_status"], "public_domain_verified")
        self.assertTrue((ROOT / row["canonical_path"]).is_dir())

    def test_object_local_routes_keep_provenance_with_support_indexes(self):
        index_text = (OBJECT / "91_source-record-index.csv").read_text(
            encoding="utf-8"
        )
        self.assertIn("src-metmuseum-oracle-bone", index_text)
        self.assertIn("public_domain_verified", index_text)
        self.assertIn("Met 42022;18.56.71", index_text)


if __name__ == "__main__":
    unittest.main()
