from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = ROOT / (
    "corpus/006_research-sources-and-bibliography/001_source-objects/"
    "016_src-obimd_source-object"
)


class ObimdEffectiveRightsDecisionTests(unittest.TestCase):
    def test_human_decision_keeps_legacy_value_but_blocks_reuse(self):
        page = (OBJECT / "25_effective-rights-decision.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "licensed_for_repository",
            "metadata_only_until_verified",
            "metadata_only_no_public_redistribution_until_reconciled",
            "006_obimd-rights-status-override.csv",
            "not a decipherment claim",
        ):
            self.assertIn(marker, page)
        self.assertFalse([line for line in page.splitlines() if len(line) > 80])

    def test_machine_decision_binds_scopes_and_evidence(self):
        data = json.loads(
            (OBJECT / "25_effective-rights-decision-index.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(data["record_type"], "effective_rights_decision_index")
        self.assertEqual(data["source_id"], "src-obimd")
        self.assertEqual(
            data["legacy_rights_status"], "licensed_for_repository"
        )
        self.assertEqual(
            data["effective_rights_status"], "metadata_only_until_verified"
        )
        self.assertEqual(data["orphan_effective_status"], "local_private_only")
        self.assertEqual(
            data["evidence_download_ids"],
            ["dl-obimd-hf-readme", "dl-obimd-github-readme"],
        )

    def test_source_packet_exposes_effective_status_and_human_page(self):
        packet = json.loads(
            (OBJECT / "01_source-packet.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            packet["effective_rights_status"], "metadata_only_until_verified"
        )
        self.assertIn("25_effective-rights-decision.md", packet["local_files"])
        self.assertIn(
            "25_effective-rights-decision-index.json", packet["local_files"]
        )


if __name__ == "__main__":
    unittest.main()
