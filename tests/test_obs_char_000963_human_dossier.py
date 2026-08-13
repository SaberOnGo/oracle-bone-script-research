import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = ROOT / (
    "corpus/001_oracle-characters/"
    "010_000901-001000_obs-char-bucket_oracle-characters/"
    "963_obs-char-000963_hust-obc-cat-1083_oracle-character/"
)


class ObsChar000963HumanDossierTests(unittest.TestCase):
    def test_main_dossier_exposes_opened_evidence_and_routes(self):
        text = (OBJECT / "05_human-research-dossier.md").read_text(
            encoding="utf-8-sig"
        )
        for marker in (
            "Opened Evidence Snapshot / 已打开证据快照",
            "14_material-visual-observation.md",
            "15_source-filename-evidence-review.md",
            "17_multi-instance-visual-comparison.md",
            "14 `G_` members",
            "Five members were decoded directly",
            "source_marked_risk_noted",
            "metadata_only_until_verified",
            "合20217",
            "合7896",
            "合7897",
            "合13543",
            "合30173",
            "Which five catalog candidates",
            "不确认卜辞身份",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("accepted reading: `㠱`", text)

    def test_readiness_and_archaeology_pages_match_opened_observations(self):
        readiness = (OBJECT / "12_human-research-readiness-review.md").read_text(
            encoding="utf-8-sig"
        )
        archaeology = (OBJECT / "10_archaeology-paleography-review.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("recorded_pending_independent_review", readiness)
        self.assertIn("Direct visual observations are recorded", readiness)
        self.assertIn("not an independently reviewed glyph observation", readiness)
        self.assertNotIn("Glyph image observation has not been written", readiness)
        self.assertIn("large-src-000001", archaeology)
        self.assertIn("dl-hust-obc-figshare-raw", archaeology)
        self.assertIn("files 14 and 17", archaeology)
        self.assertNotIn("risk note: pending", archaeology)

    def test_changed_human_pages_remain_bilingual_and_within_width(self):
        paths = (
            OBJECT / "05_human-research-dossier.md",
            OBJECT / "10_archaeology-paleography-review.md",
            OBJECT / "12_human-research-readiness-review.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("中文", text)
            self.assertNotIn("\ufffd", text)
            for line_number, line in enumerate(text.splitlines(), 1):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
