import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "007_obimd-h2-crosswalk" / "replay_h2_crosswalk.py"
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)
MANIFEST = OBJECT / "92_visual-crosswalk-replay-manifest.json"
REAL_ZIP = ROOT / "external_local_archive" / "source_packages" / "obimd" / "rubbing.zip"


def png_bytes(offset=0):
    image = Image.new("L", (48, 64), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle((8 + offset, 5, 15 + offset, 55), fill=0)
    draw.line((4, 28, 40, 28), fill=0, width=5)
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


class ObimdH2CrosswalkReplayTests(unittest.TestCase):
    def test_synthetic_cli_is_deterministic_and_tie_sorted(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            thumbnail = base / "thumb.png"
            thumbnail.write_bytes(png_bytes())
            package = base / "rubbing.zip"
            with zipfile.ZipFile(package, "w") as archive:
                archive.writestr("rubbing/z.png", png_bytes(2))
                archive.writestr("rubbing/b.png", png_bytes())
                archive.writestr("rubbing/a.png", png_bytes())
            expected = {
                "thumbnail": hashlib.sha256(thumbnail.read_bytes()).hexdigest(),
                "package": hashlib.sha256(package.read_bytes()).hexdigest(),
                "target": hashlib.sha256(png_bytes()).hexdigest(),
            }
            command = [
                sys.executable,
                str(TOOL),
                "--thumbnail-file",
                str(thumbnail),
                "--run-date",
                "2026-08-13",
                "--thumbnail-source-url",
                "https://example.invalid/thumb",
                "--rubbing-zip",
                str(package),
                "--expected-thumbnail-sha256",
                expected["thumbnail"],
                "--expected-rubbing-zip-sha256",
                expected["package"],
                "--target-member",
                "rubbing/b.png",
                "--expected-target-member-sha256",
                expected["target"],
                "--top-k",
                "3",
            ]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            record = json.loads(result.stdout)
            self.assertEqual(record["comparison"]["candidate_count"], 3)
            self.assertEqual(record["comparison"]["alternative_candidate_count"], 2)
            self.assertEqual(
                [row["member"] for row in record["comparison"]["top_k"][:2]],
                ["rubbing/a.png", "rubbing/b.png"],
            )
            self.assertEqual(record["comparison"]["target_rank"], 2)
            self.assertEqual(set(base.iterdir()), {thumbnail, package})
            manifest = base / "manifest.json"
            manifest.write_text(
                json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            verified = subprocess.run(
                command + ["--verify-manifest", str(manifest)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(verified.stdout), record)

    def test_manifest_records_exact_inputs_and_non_scholarly_boundary(self):
        record = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(record["schema"], "obimd_h2_visual_crosswalk_replay_v1")
        self.assertEqual(record["run_status"], "replayed_from_official_url")
        self.assertEqual(record["thumbnail"]["sha256"],
                         "5321d3b9adf0a1bde32e4092715741a04461908c9c6e911c57e1f7544ab32437")
        self.assertEqual(record["package"]["candidate_count"], 10077)
        self.assertEqual(record["package"]["alternative_candidate_count"], 10076)
        self.assertEqual(record["target"]["member"], "rubbing/h00002.jpg")
        self.assertEqual(record["comparison"]["target_dhash_distance"], 0)
        self.assertEqual(record["comparison"]["nearest_alternative_distance"], 12)
        self.assertIsInstance(record["comparison"]["top_k"][0], dict)
        self.assertFalse(record["scope_boundary"]["catalog_identity_confirmed"])
        self.assertFalse(record["scope_boundary"]["reading_proposed"])

    @unittest.skipUnless(REAL_ZIP.exists(), "ignored OBIMD rubbing.zip unavailable")
    def test_real_package_target_member_hash(self):
        spec = importlib.util.spec_from_file_location("obimd_h2_crosswalk", TOOL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with zipfile.ZipFile(REAL_ZIP) as archive:
            payload = archive.read("rubbing/h00002.jpg")
        self.assertEqual(hashlib.sha256(payload).hexdigest(),
                         "1ae9e411f0356cb9dc232d629d4620b0e5f66f42c83300ce95775950a75b01e5")
        image = module.decode_image(payload)
        self.assertEqual(image.size, (1022, 1180))


if __name__ == "__main__":
    unittest.main()
