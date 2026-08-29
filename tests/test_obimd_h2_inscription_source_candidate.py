import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)

HUMAN_FILES = (
    "README.md",
    "01_rubbing-facsimile-routes.md",
    "02_human-inscription-dossier.md",
    "03_source-evidence-review.md",
    "04_text-quality-review.md",
    "05_character-linkage-review.md",
    "06_missing-evidence-plan.md",
)

EXPECTED_OCCURRENCES = [
    (0, "9xhq4zclpe", "824,483,94,88", "obs-comp-cand-001085"),
    (1, "ve0ebxq620", "797,583,143,161", "obs-comp-cand-002229"),
    (2, "pzvzykmf5e", "829,769,46,67", "obs-comp-cand-001781"),
    (3, "qmvfvw99v9", "526,137,150,151", "obs-comp-cand-001998"),
    (4, "52a130pcmy", "508,332,135,214", "obs-comp-cand-001929"),
    (5, "xkubtjk815", "558,581,80,218", "obs-comp-cand-000275"),
    (6, "lstx3iocs6", "572,846,125,97", "obs-comp-cand-002627"),
]


class ObimdH2InscriptionSourceCandidateTests(unittest.TestCase):
    def test_human_dossier_is_primary_and_bilingual(self):
        self.assertTrue(OBJECT.is_dir())
        for name in HUMAN_FILES:
            text = (OBJECT / name).read_text(encoding="utf-8")
            self.assertIn("English", text, name)
            self.assertIn("简体中文", text, name)
            self.assertGreater(len(text), 500, name)
        self.assertEqual(
            sorted(path.name for path in OBJECT.glob("*.json")),
            ["90_source-record.json", "92_visual-crosswalk-replay-manifest.json"],
        )
        self.assertEqual(
            sorted(path.name for path in OBJECT.glob("*.csv")),
            ["91_character-occurrence-index.csv"],
        )

    def test_public_object_contains_no_image_payload(self):
        forbidden = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}
        image_files = [path for path in OBJECT.rglob("*") if path.suffix.lower() in forbidden]
        self.assertEqual(image_files, [])

    def test_source_record_preserves_package_and_member_integrity(self):
        record = json.loads((OBJECT / "90_source-record.json").read_text(encoding="utf-8"))
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000001")
        self.assertEqual(record["source_identifier"], "H2")
        self.assertEqual(record["source_record_locator"], "data.json#array-index-0")
        self.assertEqual(
            record["source_record_sha256"],
            "d6b0e48a6f2e465d9a8046b9db985aba51fae58195bbde372cbbd26d2d53bc50",
        )
        self.assertEqual(record["rights_status"], "metadata_only_until_verified")
        assets = {item["modality"]: item for item in record["local_private_assets"]}
        self.assertEqual(
            assets["rubbing"]["package_sha256"],
            "4d07dca94e94c2d17edd7fa25be72b5673161c0c2d03dac4d2c094e5341b7747",
        )
        self.assertEqual(assets["rubbing"]["member_path"], "rubbing/h00002.jpg")
        self.assertEqual(assets["rubbing"]["member_size_bytes"], 77614)
        self.assertEqual(
            assets["rubbing"]["member_sha256"],
            "1ae9e411f0356cb9dc232d629d4620b0e5f66f42c83300ce95775950a75b01e5",
        )
        self.assertEqual(
            assets["facsimile"]["package_sha256"],
            "b1544e34ee1a6a34fc0a83475a227fd2141a67293f795eaa3c52760fedb50b0e",
        )
        self.assertEqual(assets["facsimile"]["member_path"], "facsimile/h00002.jpg")
        self.assertEqual(assets["facsimile"]["member_size_bytes"], 49395)
        self.assertEqual(
            assets["facsimile"]["member_sha256"],
            "ebc8aa5046dbb74e08e7dd0b74ff1ce9e24693dbe8dad91194bc438024340995",
        )
        for asset in assets.values():
            self.assertEqual(asset["pixel_dimensions"], [1022, 1180])
            self.assertEqual(asset["public_visibility"], "local_private_route_only")

    def test_occurrence_index_keeps_all_seven_source_uids_in_order(self):
        with (OBJECT / "91_character-occurrence-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        actual = [
            (
                int(row["order_number"]),
                row["source_uid"],
                row["bounding_box_xywh"],
                row["candidate_project_id"],
            )
            for row in rows
        ]
        self.assertEqual(actual, EXPECTED_OCCURRENCES)
        self.assertTrue(all(row["identity_status"] == "candidate_route_only" for row in rows))

    def test_human_pages_state_text_identity_and_rights_boundaries(self):
        text = "\n".join((OBJECT / name).read_text(encoding="utf-8") for name in HUMAN_FILES)
        required = (
            "no readable transcription or OCR",
            "没有可读的卜辞全文或 OCR",
            "uncalibrated candidate route to Heji 2",
            "通向《合集》2、",
            "UIDs are not confirmed characters or readings",
            "UID 不是已确认的字形、字符或释读",
            "metadata_only_until_verified",
            "006_obimd-rights-conflict-review.md",
            "Open Heji volume 1, first period, plate 2",
            "《合集》第 1 册、第一期、图版 2",
            "collection institution and object number",
            "馆藏机构和对象号",
            "findspot or excavation context",
            "出土地或发掘语境",
            "Bin-group assignment",
            "宾组归属",
        )
        for phrase in required:
            self.assertIn(phrase, text)

    def test_human_markdown_lines_do_not_exceed_80_characters(self):
        violations = []
        for name in HUMAN_FILES:
            for number, line in enumerate(
                (OBJECT / name).read_text(encoding="utf-8").splitlines(), start=1
            ):
                if len(line) > 80:
                    violations.append(f"{name}:{number}:{len(line)}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
