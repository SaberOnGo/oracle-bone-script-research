import csv
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATA = (
    ROOT / "external_local_archive" / "source_packages" / "obimd" / "data.json"
)
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
)


class NingxiaHyz421RepeatedInscriptionAlignmentTests(unittest.TestCase):
    def read_csv(self, name):
        with (OBJECT / name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_human_adjudication_is_bilingual_and_bounded(self):
        page = (
            OBJECT
            / "12_repeated-inscription-alignment-and-unknown-uid-review.md"
        ).read_text(encoding="utf-8")
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        for marker in (
            "Repeated inscription alignment",
            "重复卜辞对齐",
            "two inscription groups",
            "二十七个来源框",
            "nms96pmn1w",
            "60kr6bp9hf",
            "source-reported lookup",
            "independent witnesses",
            "C2",
            "`direct_checked`",
            "C4",
            "`candidate_route`",
            "C5",
            "C6",
            "C8",
            "action `abstain`",
            "No numeric probability is",
            "not a transcription",
        ):
            self.assertIn(marker, page)
        for name in (
            "12_repeated-inscription-alignment-and-unknown-uid-review.md",
            "93_obimd-hd421-occurrence-index.csv",
            "94_repeated-sentence-pair-index.csv",
        ):
            self.assertIn(name, readme)

    def test_occurrence_index_has_24_sentence_and_three_sequence_boxes(self):
        rows = self.read_csv("93_obimd-hd421-occurrence-index.csv")
        self.assertEqual(len(rows), 27)
        self.assertEqual(len({row["occurrence_id"] for row in rows}), 27)
        sentence = [
            row for row in rows
            if row["group_category"].startswith("InscriptionSentence")
        ]
        sequence = [
            row for row in rows
            if row["group_category"].startswith("OracleSequence")
        ]
        self.assertEqual(len(sentence), 24)
        self.assertEqual(len(sequence), 3)
        for group in ("InscriptionSentence1", "InscriptionSentence2"):
            group_rows = [row for row in sentence if row["group_category"] == group]
            self.assertEqual(
                [int(row["order_number"]) for row in group_rows],
                list(range(12)),
            )
        self.assertEqual(
            [row["group_category"] for row in sequence],
            ["OracleSequence1", "OracleSequence1", "OracleSequence2"],
        )
        self.assertTrue(all(row["evidence_state"] == "direct_checked" for row in rows))

    def test_pair_index_is_exact_ordered_with_shared_ancestry(self):
        occurrences = self.read_csv("93_obimd-hd421-occurrence-index.csv")
        by_group_order = {
            (row["group_category"], int(row["order_number"])): row
            for row in occurrences
        }
        pairs = self.read_csv("94_repeated-sentence-pair-index.csv")
        self.assertEqual(len(pairs), 12)
        self.assertEqual(
            [int(row["order_number"]) for row in pairs],
            list(range(12)),
        )
        for pair in pairs:
            order = int(pair["order_number"])
            left = by_group_order[("InscriptionSentence1", order)]
            right = by_group_order[("InscriptionSentence2", order)]
            self.assertEqual(left["label"], right["label"])
            self.assertEqual(left["sub_label"], right["sub_label"])
            self.assertEqual(pair["label"], left["label"])
            self.assertEqual(pair["sub_label"], left["sub_label"])
            self.assertEqual(pair["sentence1_position"], left["position_xywh"])
            self.assertEqual(pair["sentence2_position"], right["position_xywh"])
            self.assertEqual(pair["pair_state"], "exact_source_metadata_match")
            self.assertEqual(pair["reading_status"], "withheld")

    def test_unknown_uids_remain_lookup_metadata_only(self):
        rows = self.read_csv("93_obimd-hd421-occurrence-index.csv")
        unknown = [
            row for row in rows if row["project_route"]
        ]
        self.assertEqual(len(unknown), 4)
        self.assertEqual(
            {row["label"] for row in unknown},
            {"nms96pmn1w", "60kr6bp9hf"},
        )
        self.assertEqual(
            {row["project_route"] for row in unknown},
            {"obs-comp-cand-000329", "obs-comp-cand-000671"},
        )
        self.assertTrue(all(row["reading_status"] == "withheld" for row in unknown))
        self.assertTrue(
            all(row["rights_status"] == "metadata_only_until_verified" for row in unknown)
        )

    def test_occurrence_index_replays_checksum_bound_source_row(self):
        source_bytes = SOURCE_DATA.read_bytes()
        self.assertEqual(
            hashlib.sha256(source_bytes).hexdigest(),
            "b504b0d4e7a0126d494c161f5445c5ee4225659ff5e94182685fce35d261aa19",
        )
        source = json.loads(source_bytes)
        matches = [(index, row) for index, row in enumerate(source) if row.get("RubbingName") == "HD421"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], 10039)
        source_groups = matches[0][1]["RecordUtilSentenceGroupVoList"]
        source_by_key = {}
        for group in source_groups:
            for item in group["RecordUtilOracleCharVoList"]:
                source_by_key[(group["GroupCategory"], item["OrderNumber"])] = item
        rows = self.read_csv("93_obimd-hd421-occurrence-index.csv")
        self.assertEqual(len(source_by_key), 27)
        self.assertEqual(len(rows), 27)
        csv_keys = {
            (row["group_category"], int(row["order_number"])) for row in rows
        }
        self.assertEqual(len(csv_keys), 27)
        self.assertEqual(csv_keys, set(source_by_key))
        for row in rows:
            key = (row["group_category"], int(row["order_number"]))
            item = source_by_key[key]
            self.assertEqual(row["position_xywh"], item["Position"])
            self.assertEqual(int(row["seat_font"]), item["SeatFont"])
            self.assertEqual(int(row["mark"]), item["Mark"])
            self.assertEqual(row["label"], item["Label"])
            self.assertEqual(row["sub_label"], item["SubLabel"])
            self.assertEqual(row["reading_status"], "withheld")
            self.assertEqual(
                row["rights_status"],
                "metadata_only_until_verified",
            )

    def test_machine_summary_preserves_claim_gates_and_abstention(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        alignment = record["repeated_inscription_alignment"]
        self.assertEqual(alignment["sentence_box_count"], 24)
        self.assertEqual(alignment["oracle_sequence_box_count"], 3)
        self.assertEqual(alignment["repeated_pair_count"], 12)
        self.assertEqual(
            alignment["unknown_main_uids"],
            ["nms96pmn1w", "60kr6bp9hf"],
        )
        self.assertEqual(
            alignment["unknown_uid_status"],
            "lookup_metadata_only_no_character_assignment",
        )
        self.assertEqual(
            alignment["evidence_states"],
            {
                "C1": "candidate_route",
                "C2": "direct_checked",
                "C3": "not_asserted_not_applicable",
                "C4": "candidate_route",
                "C5": "blocked",
                "C6": "blocked",
                "C7": "not_applicable_no_diachronic_proposition",
                "C8": "abstain_withhold",
            },
        )
        self.assertEqual(alignment["decipherment_effect"], "none")
        self.assertEqual(
            alignment["pair_method"],
            "equal_OrderNumber_literal_Label_and_literal_SubLabel",
        )
        self.assertEqual(
            alignment["independence_status"],
            "not_independent_within_row_repetition",
        )
        self.assertEqual(
            alignment["rights_status"],
            "metadata_only_until_verified",
        )

    def test_edited_object_files_do_not_claim_high_confidence(self):
        for name in (
            "README.md",
            "90_source-record.json",
            "91_source-record-index.csv",
            "12_repeated-inscription-alignment-and-unknown-uid-review.md",
            "93_obimd-hd421-occurrence-index.csv",
            "94_repeated-sentence-pair-index.csv",
        ):
            text = (OBJECT / name).read_text(encoding="utf-8")
            self.assertNotIn("high_confidence", text)
            self.assertNotIn("高置信", text)


if __name__ == "__main__":
    unittest.main()
