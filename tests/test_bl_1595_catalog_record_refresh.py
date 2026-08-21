import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate"
)


class BritishLibrary1595CatalogRefreshTests(unittest.TestCase):
    def test_catalog_record_has_stable_identity_and_snapshot_binding(self):
        data = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        record = data["catalog_record"]
        self.assertEqual(record["record_id"], "040-003126498")
        self.assertEqual(record["root_record_id"], "032-002915678")
        self.assertEqual(record["mdark"], "ark:/81055/vdc_100026115481.0x000001")
        self.assertEqual(record["lark"], "ark:/81055/vdc_100191805301.0x000001")
        self.assertEqual(record["hierarchy"], "032-002915678[0051]/040-003126498")
        self.assertEqual(record["snapshot_size_bytes"], 41120)
        self.assertEqual(
            record["snapshot_sha256"],
            "1a4672c0524d02ca1048e76787c2e5015825671f72023d988d03bb3549e3422c",
        )
        self.assertEqual(record["parent_snapshot_size_bytes"], 166069)
        self.assertEqual(
            record["parent_snapshot_sha256"],
            "1f3336ecd238857fb7d5cfa4ff02b7d66ffc8f95f6cfcdc4edb6fbcb057a1b65",
        )

    def test_local_snapshots_match_recorded_hashes_when_present(self):
        data = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        record = data["catalog_record"]
        for path_key, size_key, hash_key in (
            ("snapshot_path", "snapshot_size_bytes", "snapshot_sha256"),
            (
                "parent_snapshot_path",
                "parent_snapshot_size_bytes",
                "parent_snapshot_sha256",
            ),
        ):
            path = ROOT / record[path_key]
            if not path.is_file():
                continue
            self.assertEqual(path.stat().st_size, record[size_key])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                record[hash_key],
            )

    def test_catalog_payload_gaps_remain_explicit(self):
        data = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        record = data["catalog_record"]
        self.assertEqual(record["image_status"], "unavailable")
        self.assertEqual(record["iiif_status"], "not_identified")
        self.assertEqual(record["text_status"], "no_transcription")
        self.assertEqual(
            data["missing_evidence"][0],
            "stable British Library JSON or XML payload, IIIF manifest, and image",
        )
        self.assertEqual(
            data["review_status"],
            "source_record_candidate_needs_plate_and_text_review",
        )

    def test_human_catalog_page_exposes_record_and_boundaries(self):
        text = (OBJECT / "09_british-library-catalog-record.md").read_text(
            encoding="utf-8-sig"
        )
        for marker in (
            "https://searcharchives.bl.uk/catalog/040-003126498",
            "040-003126498",
            "032-002915678[0051]/040-003126498",
            "1a4672c0524d02ca1048e76787c2e5015825671f72023d988d03bb3549e3422c",
            "Images currently unavailable",
            "no stable item-level JSON payload",
            "IIIF manifest",
            "no project OCR",
            "or decipherment claim",
            "2026-08-22",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("project translation", text)

    def test_human_catalog_page_stays_within_eighty_columns(self):
        path = OBJECT / "09_british-library-catalog-record.md"
        for number, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), 1
        ):
            self.assertLessEqual(
                len(line),
                80,
                f"{path}:{number}: {len(line)} characters",
            )

    def test_keightley_crosswalk_is_bound_to_the_object_record(self):
        data = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        route = next(
            item
            for item in data["literature_routes"]
            if item["source_id"]
            == "literature-keightley-ancestral-landscape-2000"
        )
        self.assertEqual(route["author"], "David N. Keightley")
        self.assertEqual(
            route["title"],
            "The Ancestral Landscape: Time, Space, and Community in Late Shang China",
        )
        self.assertEqual(
            route["locator"],
            "printed page 147; excerpt PDF page 25; reference [19]",
        )
        self.assertEqual(route["snapshot_size_bytes"], 1806072)
        self.assertEqual(
            route["snapshot_sha256"],
            "a2c1a756aa66ed1f92f8c4bde8b4b2fb5005838669633e804cd4594a974078bf",
        )
        self.assertEqual(route["project_use"], "cross_source_locator_only")
        self.assertEqual(route["rights_status"], "metadata_only_until_verified")
        self.assertIn("Yingcang 886b", route["claim_scope"])
        self.assertIn("Kufang 1595", route["claim_scope"])
        self.assertIn("Heji 40610b", route["claim_scope"])

        snapshot = ROOT / route["snapshot_path"]
        if snapshot.is_file():
            self.assertEqual(snapshot.stat().st_size, route["snapshot_size_bytes"])
            self.assertEqual(
                hashlib.sha256(snapshot.read_bytes()).hexdigest(),
                route["snapshot_sha256"],
            )

    def test_keightley_human_notes_keep_locator_and_boundary(self):
        literature = (OBJECT / "06_literature-and-dispute-review.md").read_text(
            encoding="utf-8-sig"
        )
        reconciliation = (
            OBJECT / "08_source-text-line-reconciliation.md"
        ).read_text(encoding="utf-8-sig")
        for marker in (
            "Yingcang 886b",
            "Kufang 1595",
            "Heji 40610b",
            "printed page 147",
            "source-reported published cross-reference",
            "not a project",
            "not a decipherment conclusion",
        ):
            self.assertIn(marker, literature)
        self.assertIn("published Heji locator", reconciliation)
        self.assertIn("line alignment", reconciliation)

    def test_keightley_human_pages_stay_within_eighty_columns(self):
        for name in (
            "06_literature-and-dispute-review.md",
            "08_source-text-line-reconciliation.md",
        ):
            path = OBJECT / name
            for number, line in enumerate(
                path.read_text(encoding="utf-8-sig").splitlines(), 1
            ):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
