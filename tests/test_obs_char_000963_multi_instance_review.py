import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / (
    "corpus/001_oracle-characters/"
    "010_000901-001000_obs-char-bucket_oracle-characters/"
    "963_obs-char-000963_hust-obc-cat-1083_oracle-character/"
    "17_multi-instance-visual-comparison.md"
)


class ObsChar000963MultiInstanceReviewTests(unittest.TestCase):
    def test_review_records_five_opened_archive_members(self):
        self.assertTrue(DOSSIER.is_file(), DOSSIER)
        text = DOSSIER.read_text(encoding="utf-8-sig")
        members = re.findall(
            r"^- Archive member / 原包成员：`([^`]+)`$", text, re.M
        )
        self.assertEqual(5, len(members))
        self.assertEqual(5, len(set(members)))
        self.assertTrue(all("/1083/G_1083_" in item for item in members))
        self.assertEqual(5, len(re.findall(r"^- SHA-256：`[0-9a-f]{64}`$", text, re.M)))
        self.assertEqual(5, len(re.findall(r"^- Pixel size / 像素：`\d+ × \d+`$", text, re.M)))

    def test_review_is_object_specific_and_falsifiable(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        for marker in (
            "obs-char-000963",
            "hust-obc-cat-1083",
            "合20217",
            "合7896",
            "合7897",
            "合13543𠂤組",
            "合30173歷無名間",
            "## Pairwise Differences And Counterevidence",
            "近形风险",
            "source_marked_risk_noted",
            "does not confirm inscription identity",
            "not an accepted reading",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)

    def test_human_markdown_lines_do_not_exceed_eighty_characters(self):
        object_dir = DOSSIER.parent
        for path in object_dir.glob("*.md"):
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8-sig").splitlines(), 1
            ):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number}: {len(line)} characters",
                )

    def test_claim_gate_is_human_readable_and_withholds_unverified_claims(self):
        page = (DOSSIER.parent / "18_claim-evidence-gate-review.md").read_text(
            encoding="utf-8-sig"
        )
        for marker in (
            "C1 object identity",
            "C2 direct glyph observation",
            "C3 same-sign, variant, near-form, or component",
            "C4 inscription occurrence and context",
            "C8 complete proposition and user delivery",
            "C1 对象身份",
            "C3 同字、异体、近形或构件",
            "C8 完整命题与用户交付",
            "candidate_route",
            "withheld",
            "U+3831",
            "No reading, meaning, probability",
            "没有估计释读、意义、概率",
        ):
            self.assertIn(marker, page)
        self.assertNotIn("confirmed reading", page)
        self.assertNotIn("确认释读", page)

    def test_claim_gate_is_bound_to_packet_and_human_index(self):
        packet = json.loads(
            (DOSSIER.parent / "01_candidate-character-packet.json").read_text(
                encoding="utf-8-sig"
            )
        )
        self.assertEqual(
            packet["claim_gate_review"]["c1_object_identity"], "blocked"
        )
        self.assertEqual(
            packet["claim_gate_review"]["c2_direct_glyph_observation"],
            "direct_checked",
        )
        self.assertEqual(
            packet["claim_gate_review"]["c3_sign_variant_near_form_component"],
            "candidate_route",
        )
        self.assertEqual(
            packet["claim_gate_review"]["c8_user_delivery"], "withheld"
        )
        index = json.loads(
            (DOSSIER.parent / "07_research-dossier-index.json").read_text(
                encoding="utf-8-sig"
            )
        )
        self.assertIn("18_claim-evidence-gate-review.md", index["human_files"])


if __name__ == "__main__":
    unittest.main()
