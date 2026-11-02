import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str, name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class EffectiveRightsRoutingSummaryTests(unittest.TestCase):
    def test_statistics_keep_legacy_and_expose_effective_obimd_rights(self):
        module = load_module(
            "tools/004_statistics-generation/build_source_coverage_statistics.py",
            "source_coverage_statistics_for_effective_rights_test",
        )
        rows = module.build_source_coverage_summary(ROOT)
        obimd = next(row for row in rows if row["source_id"] == "src-obimd")

        self.assertEqual(obimd["rights_status"], "licensed_for_repository")
        self.assertEqual(
            obimd["effective_rights_status"],
            "metadata_only_until_verified",
        )
        self.assertEqual(
            obimd["effective_public_commit_decision"],
            "metadata_only_no_public_redistribution_until_reconciled",
        )
        self.assertEqual(
            obimd["effective_asset_rights_status_counts"],
            "metadata_only_until_verified:10364",
        )
        self.assertIn(
            "006_obimd-rights-status-override.csv",
            obimd["rights_resolution_ref"],
        )


if __name__ == "__main__":
    unittest.main()
