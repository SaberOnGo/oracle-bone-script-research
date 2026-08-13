import csv
import hashlib
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
DOSSIER = OBJECT / "08_sequence-context-evidence.md"
INDEX = OBJECT / "91_character-occurrence-index.csv"
DATA = ROOT / "external_local_archive" / "source_packages" / "obimd" / "data.json"


EXPECTED = [
    (0, "9xhq4zclpe", "824,483,94,88", "obs-comp-cand-001085"),
    (1, "ve0ebxq620", "797,583,143,161", "obs-comp-cand-002229"),
    (2, "pzvzykmf5e", "829,769,46,67", "obs-comp-cand-001781"),
    (3, "qmvfvw99v9", "526,137,150,151", "obs-comp-cand-001998"),
    (4, "52a130pcmy", "508,332,135,214", "obs-comp-cand-001929"),
    (5, "xkubtjk815", "558,581,80,218", "obs-comp-cand-000275"),
    (6, "lstx3iocs6", "572,846,125,97", "obs-comp-cand-002627"),
]


class ObimdH2SequenceContextEvidenceTests(unittest.TestCase):
    @unittest.skipUnless(DATA.exists(), "ignored OBIMD data.json unavailable")
    def test_real_h2_row_recomputes_all_seven_occurrences(self):
        payload = json.loads(DATA.read_text(encoding="utf-8"))
        self.assertEqual(
            hashlib.sha256(DATA.read_bytes()).hexdigest(),
            "b504b0d4e7a0126d494c161f5445c5ee4225659ff5e94182685fce35d261aa19",
        )
        if isinstance(payload, str):
            payload = json.loads(payload)
        rows = [row for row in payload if row.get("RubbingName") == "H2"]
        self.assertEqual(len(rows), 1)
        groups = rows[0]["RecordUtilSentenceGroupVoList"]
        self.assertEqual([group["GroupCategory"] for group in groups],
                         ["InscriptionSentence1"])
        occurrences = groups[0]["RecordUtilOracleCharVoList"]
        self.assertEqual(
            [item["OrderNumber"] for item in occurrences],
            [5, 0, 1, 2, 3, 6, 4],
        )
        self.assertEqual(
            sorted(item["OrderNumber"] for item in occurrences),
            list(range(7)),
        )
        actual = sorted(
            (
                item["OrderNumber"],
                item["Label"],
                item["Position"],
                item["SeatFont"],
                item["Mark"],
                item["SubLabel"],
            )
            for item in occurrences
        )
        self.assertEqual(
            actual,
            [(order, uid, box, 0, -1, uid) for order, uid, box, _ in EXPECTED],
        )

    def test_occurrence_index_matches_source_and_candidate_routes(self):
        rows = list(csv.DictReader(INDEX.read_text(encoding="utf-8").splitlines()))
        actual = [
            (
                int(row["order_number"]),
                row["source_uid"],
                row["bounding_box_xywh"],
                row["candidate_project_id"],
            )
            for row in rows
        ]
        self.assertEqual(actual, EXPECTED)
        for _, uid, _, candidate in EXPECTED:
            matches = list((ROOT / "corpus" / "003_graphemic-components").glob(
                f"**/*_{candidate}_obimd-sub-{uid}_component-candidate"
            ))
            self.assertEqual(len(matches), 1)

    def test_human_dossier_explains_fields_routes_and_boundaries(self):
        text = DOSSIER.read_text(encoding="utf-8")
        for phrase in (
            "source serialization order is `5, 0, 1, 2, 3, 6, 4`",
            "annotation order is `0, 1, 2, 3, 4, 5, 6`",
            "Label sequence is not a transcription",
            "UID route does not confirm a character identity",
            "H2 remains an inscription source-record candidate",
            "SeatFont = 0",
            "Mark = -1",
            "SubLabel equals Label",
            "来源标签序列不是释文",
            "UID 路由不确认单字身份",
            "具体可证伪的下一步",
            "Code=406",
        ):
            self.assertIn(phrase, text)

    def test_dossier_is_bilingual_and_lines_are_within_limit(self):
        text = DOSSIER.read_text(encoding="utf-8")
        self.assertIn("## English", text)
        self.assertIn("## 简体中文", text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), start=1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])

    def test_object_reading_order_links_the_sequence_context(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`08_sequence-context-evidence.md`", readme)
        self.assertLess(
            readme.index("`07_identifier-crosswalk-investigation.md`"),
            readme.index("`08_sequence-context-evidence.md`"),
        )
        self.assertLess(
            readme.index("`08_sequence-context-evidence.md`"),
            readme.index("`92_visual-crosswalk-replay-manifest.json`"),
        )


if __name__ == "__main__":
    unittest.main()
