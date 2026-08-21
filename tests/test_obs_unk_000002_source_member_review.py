import hashlib
import json
import os
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/001_oracle-characters/017_undeciphered-000001-000100_"
    "obs-unk-bucket_oracle-character-candidates/"
    "002_obs-unk-000002_hust-obc-und-L-000002_"
    "oracle-character-candidate"
)
ZIP_PATH = (
    ROOT
    / "external_local_archive/source_packages/hust-obc/"
    "dl-hust-obc-figshare-raw.zip"
)
EXPECTED_MEMBER_SHA = (
    "3a08c4eea640ab3cbd31fd32c3426f63a3b352fa9f6ff6f8e43affa2e81afcda"
)
EXPECTED_PACKAGE_SHA = (
    "0d00a4de8dd9ce7b7495d7b26f3c80098ee9975b91615211dde02e569bf0ad9d"
)


def _read_bytes(path: Path) -> bytes:
    """Read a repository asset even when Windows exceeds MAX_PATH."""
    path_text = str(path.resolve())
    if os.name == "nt" and not path_text.startswith("\\\\?\\"):
        path_text = "\\\\?\\" + path_text
    with open(path_text, "rb") as source_file:
        return source_file.read()


@unittest.skipUnless(ZIP_PATH.is_file(), "ignored HUST archive is unavailable")
class ObsUnk000002SourceMemberReviewTests(unittest.TestCase):
    def test_archive_member_and_derivative_are_byte_bound(self):
        page = (OBJECT / "15_source-member-evidence-review.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn(EXPECTED_PACKAGE_SHA, page)
        self.assertIn(EXPECTED_MEMBER_SHA, page)
        self.assertIn("No second view or second instance", page)
        self.assertIn("不是破译假说", page)
        self.assertIn("decipherment hypothesis", page)

        self.assertEqual(ZIP_PATH.stat().st_size, 607933810)
        package_hash = hashlib.sha256()
        with ZIP_PATH.open("rb") as source_file:
            for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                package_hash.update(chunk)
        self.assertEqual(package_hash.hexdigest(), EXPECTED_PACKAGE_SHA)

        with zipfile.ZipFile(ZIP_PATH) as archive:
            members = [
                info
                for info in archive.infolist()
                if "undeciphered/L/2/" in info.filename
                and not info.is_dir()
            ]
            self.assertEqual(len(members), 1)
            info = members[0]
            member_bytes = archive.read(info)
            self.assertEqual(info.file_size, 1286)
            self.assertEqual(info.compress_size, 1134)
            self.assertEqual(info.CRC, 3096258605)
            self.assertEqual(
                hashlib.sha256(member_bytes).hexdigest(), EXPECTED_MEMBER_SHA
            )

        derivative = next(
            item
            for item in (OBJECT / "03_visual-assets").iterdir()
            if item.name == "001_asset-001595_hust-obc-und-L-000002_glyph.jpg"
        )
        derivative_bytes = _read_bytes(derivative)
        self.assertEqual(derivative_bytes, member_bytes)
        self.assertEqual(
            hashlib.sha256(derivative_bytes).hexdigest(), EXPECTED_MEMBER_SHA
        )

    def test_object_navigation_and_claim_gate_are_linked(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8-sig")
        index = json.loads(
            (OBJECT / "07_research-dossier-index.json").read_text(
                encoding="utf-8-sig"
            )
        )
        self.assertIn("15_source-member-evidence-review.md", readme)
        self.assertIn("18_claim-evidence-gate-review.md", readme)
        self.assertIn("15_source-member-evidence-review.md", index["human_files"])
        self.assertIn("18_claim-evidence-gate-review.md", index["human_files"])
        self.assertEqual(index["updated_at"], "2026-08-21")

    def test_observation_and_gate_withhold_unresolved_semantics(self):
        observation = (OBJECT / "14_material-visual-observation.md").read_text(
            encoding="utf-8-sig"
        )
        gate = (OBJECT / "18_claim-evidence-gate-review.md").read_text(
            encoding="utf-8-sig"
        )
        for marker in (
            "pointed upper junction",
            "尖状交接处",
            "C1 object identity",
            "C2 direct glyph observation",
            "C4 inscription occurrence and context",
            "C5 reading or phonological candidate",
            "C8 complete proposition and user delivery",
            "abstain_withhold_candidate",
            "C1 对象身份",
            "C5 读音或隶定候选",
            "本页不产生释读、意义、概率或破译结论",
        ):
            self.assertIn(marker, observation + gate)
        self.assertNotIn("confirmed reading", gate.lower())


if __name__ == "__main__":
    unittest.main()
