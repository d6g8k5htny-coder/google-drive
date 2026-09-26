#!/usr/bin/env python3
"""Negative controls for scripts/verify_replicas.py. Scientific effect: NONE."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_replicas.py"


class VerifyReplicasTests(unittest.TestCase):
    def test_repo_verify_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(VERIFY)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("INDEX.json consistent", proc.stdout)
        self.assertIn("EXCLUDED.json", proc.stdout)

    def test_tampered_bytes_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Minimal fake repo layout copied from one real replica + INDEX/EXCLUDED stubs
            shutil.copytree(ROOT / "replicas" / "side24-coefficient-v1", tmp_path / "replicas" / "side24-coefficient-v1")
            # Tamper enclosure
            target = tmp_path / "replicas" / "side24-coefficient-v1" / "ENCLOSURE.json"
            target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            # Minimal INDEX/EXCLUDED matching only this folder
            src = json.loads((tmp_path / "replicas" / "side24-coefficient-v1" / "SOURCE.json").read_text())
            (tmp_path / "replicas" / "INDEX.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "scientific_status_authority": False,
                        "replicas": [
                            {
                                "folder": "side24-coefficient-v1",
                                "replica_path": src["replica_path"],
                                "source_drive_id": src["source_drive_id"],
                                "bytes": src["bytes"],
                                "sha256": src["sha256"],
                            }
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (tmp_path / "replicas" / "EXCLUDED.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "scientific_status_authority": False,
                        "excluded": [],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            script = tmp_path / "scripts" / "verify_replicas.py"
            script.parent.mkdir(parents=True)
            script.write_text((ROOT / "scripts" / "verify_replicas.py").read_text(encoding="utf-8"), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("FAIL", proc.stdout + proc.stderr)

    def test_excluded_overlap_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copytree(ROOT / "replicas" / "side24-coefficient-v1", tmp_path / "replicas" / "side24-coefficient-v1")
            src = json.loads((tmp_path / "replicas" / "side24-coefficient-v1" / "SOURCE.json").read_text())
            (tmp_path / "replicas" / "INDEX.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "scientific_status_authority": False,
                        "replicas": [
                            {
                                "folder": "side24-coefficient-v1",
                                "replica_path": src["replica_path"],
                                "source_drive_id": src["source_drive_id"],
                                "bytes": src["bytes"],
                                "sha256": src["sha256"],
                            }
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (tmp_path / "replicas" / "EXCLUDED.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "scientific_status_authority": False,
                        "excluded": [
                            {
                                "source_drive_id": src["source_drive_id"],
                                "reason": "test_overlap",
                            }
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            script = tmp_path / "scripts" / "verify_replicas.py"
            script.parent.mkdir(parents=True)
            script.write_text((ROOT / "scripts" / "verify_replicas.py").read_text(encoding="utf-8"), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("EXCLUDED.json lists selected", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
