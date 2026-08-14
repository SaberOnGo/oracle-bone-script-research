from __future__ import annotations

import json
import csv
import importlib.util
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

    def test_object_package_routes_display_effective_status(self):
        with (OBJECT / "03_package-route-index.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 7)
        self.assertTrue(rows)
        self.assertTrue(
            all(
                row["rights_status"] == "metadata_only_until_verified"
                for row in rows
            )
        )
        dossier = (OBJECT / "10_source-evidence-dossier.md").read_text(
            encoding="utf-8"
        )
        package_section = dossier.split(
            "## Package Manifest Field Map And Derivatives", 1
        )[1].split("## Scope Evidence Level And Review Status", 1)[0]
        self.assertEqual(
            package_section.count(
                "Rights status / 权利状态: metadata_only_until_verified"
            ),
            7,
        )

    def test_builder_projects_effective_status_to_package_routes(self):
        builder_path = ROOT / (
            "tools/002_corpus-import/build_source_object_materials.py"
        )
        spec = importlib.util.spec_from_file_location(
            "source_object_builder", builder_path
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def rows(path):
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                return list(csv.DictReader(handle))

        manifest = rows(
            ROOT
            / "corpus/006_research-sources-and-bibliography/000_source-registers/"
            "009_source-package-file-manifest.csv"
        )
        log = rows(
            ROOT / "project_registry/006_large-source-register/002_source-download-log.csv"
        )
        large = rows(
            ROOT / "project_registry/006_large-source-register/001_large-source-register.csv"
        )
        routes = module.build_package_routes(
            "src-obimd",
            [row for row in manifest if row["source_id"] == "src-obimd"],
            [row for row in log if row["source_id"] == "src-obimd"],
            large,
        )
        self.assertEqual(len(routes), 7)
        self.assertTrue(
            all(
                row["rights_status"] == "metadata_only_until_verified"
                for row in routes
            )
        )


if __name__ == "__main__":
    unittest.main()
