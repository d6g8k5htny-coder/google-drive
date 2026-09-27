#!/usr/bin/env python3
"""Negative controls for scripts/verify_replicas.py. Scientific effect: NONE."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_replicas.py"
FIXTURE_FOLDER = "side24-coefficient-v1"


def _write_manifests(tmp_path: Path, src: dict) -> None:
    (tmp_path / "replicas" / "INDEX.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "scientific_status_authority": False,
                "replicas": [
                    {
                        "folder": FIXTURE_FOLDER,
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


def _install_script(tmp_path: Path) -> Path:
    script = tmp_path / "scripts" / "verify_replicas.py"
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text(VERIFY.read_text(encoding="utf-8"), encoding="utf-8")
    return script


def _fixture_repo(*, with_manifests: bool = True) -> tuple[Path, dict, Path]:
    """Return (tmp_root, source_dict, verify_script). Caller must clean tmp_root."""
    tmp_path = Path(tempfile.mkdtemp())
    shutil.copytree(
        ROOT / "replicas" / FIXTURE_FOLDER,
        tmp_path / "replicas" / FIXTURE_FOLDER,
    )
    src = json.loads(
        (tmp_path / "replicas" / FIXTURE_FOLDER / "SOURCE.json").read_text(encoding="utf-8")
    )
    if with_manifests:
        _write_manifests(tmp_path, src)
    script = _install_script(tmp_path)
    return tmp_path, src, script


def _run_verify(script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _rewrite_source(tmp_path: Path, **updates: object) -> dict:
    source_path = tmp_path / "replicas" / FIXTURE_FOLDER / "SOURCE.json"
    src = json.loads(source_path.read_text(encoding="utf-8"))
    src.update(updates)
    source_path.write_text(json.dumps(src, indent=2) + "\n", encoding="utf-8")
    return src


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

    def test_valid_local_fixture_passes(self) -> None:
        tmp_path, _src, script = _fixture_repo()
        try:
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("INDEX.json consistent", proc.stdout)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_tampered_bytes_fail(self) -> None:
        tmp_path, _src, script = _fixture_repo()
        try:
            target = tmp_path / "replicas" / FIXTURE_FOLDER / "ENCLOSURE.json"
            target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            proc = _run_verify(script, tmp_path)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("FAIL", proc.stdout + proc.stderr)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_wrong_sha256_fail(self) -> None:
        tmp_path, src, script = _fixture_repo()
        try:
            bad = "0" * 64
            self.assertNotEqual(bad, src["sha256"])
            updated = _rewrite_source(tmp_path, sha256=bad)
            _write_manifests(tmp_path, updated)
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("local bytes/hash != SOURCE.json", proc.stdout + proc.stderr)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_excluded_overlap_fails(self) -> None:
        tmp_path, src, script = _fixture_repo()
        try:
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
            proc = _run_verify(script, tmp_path)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("EXCLUDED.json lists selected", proc.stdout + proc.stderr)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_parent_escape_fails(self) -> None:
        tmp_path, _src, script = _fixture_repo()
        try:
            outside = tmp_path / "outside.bin"
            payload = b"parent-escape-probe"
            outside.write_bytes(payload)
            updated = _rewrite_source(
                tmp_path,
                replica_path="replicas/side24-coefficient-v1/../outside.bin",
                bytes=len(payload),
                sha256=hashlib.sha256(payload).hexdigest(),
            )
            _write_manifests(tmp_path, updated)
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("..", proc.stdout + proc.stderr)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_absolute_escape_fails(self) -> None:
        tmp_path, _src, script = _fixture_repo()
        try:
            outside = tmp_path / "absolute.bin"
            payload = b"absolute-escape-probe"
            outside.write_bytes(payload)
            updated = _rewrite_source(
                tmp_path,
                replica_path=str(outside.resolve()),
                bytes=len(payload),
                sha256=hashlib.sha256(payload).hexdigest(),
            )
            _write_manifests(tmp_path, updated)
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("absolute", proc.stdout + proc.stderr.lower())
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_symlink_escape_fails(self) -> None:
        if os.name == "nt":
            self.skipTest("symlink probe not required on Windows")
        tmp_path, _src, script = _fixture_repo()
        try:
            outside = tmp_path / "symlink-target.bin"
            payload = b"symlink-escape-probe"
            outside.write_bytes(payload)
            link = tmp_path / "replicas" / FIXTURE_FOLDER / "escaped.link"
            link.symlink_to(outside.resolve())
            updated = _rewrite_source(
                tmp_path,
                replica_path=f"replicas/{FIXTURE_FOLDER}/escaped.link",
                bytes=len(payload),
                sha256=hashlib.sha256(payload).hexdigest(),
            )
            _write_manifests(tmp_path, updated)
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            combined = (proc.stdout + proc.stderr).lower()
            self.assertTrue(
                "symlink" in combined or "resolves outside" in combined,
                proc.stdout + proc.stderr,
            )
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_missing_index_fails(self) -> None:
        tmp_path, _src, script = _fixture_repo(with_manifests=True)
        try:
            (tmp_path / "replicas" / "INDEX.json").unlink()
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("missing required replicas/INDEX.json", proc.stdout + proc.stderr)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_missing_excluded_fails(self) -> None:
        tmp_path, _src, script = _fixture_repo(with_manifests=True)
        try:
            (tmp_path / "replicas" / "EXCLUDED.json").unlink()
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn(
                "missing required replicas/EXCLUDED.json", proc.stdout + proc.stderr
            )
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_symlinked_replica_folder_fails(self) -> None:
        """Directory symlink: replicas/<folder> → outside workspace tree."""
        if os.name == "nt":
            self.skipTest("symlink probe not required on Windows")
        tmp_path, src, script = _fixture_repo()
        try:
            outside = tmp_path / "outside-folder"
            outside.mkdir()
            payload_name = Path(src["replica_path"]).name
            shutil.copy2(
                tmp_path / "replicas" / FIXTURE_FOLDER / payload_name,
                outside / payload_name,
            )
            (outside / "SOURCE.json").write_text(
                (tmp_path / "replicas" / FIXTURE_FOLDER / "SOURCE.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            # Replace real folder with symlink to outside.
            shutil.rmtree(tmp_path / "replicas" / FIXTURE_FOLDER)
            (tmp_path / "replicas" / FIXTURE_FOLDER).symlink_to(
                outside.resolve(), target_is_directory=True
            )
            proc = _run_verify(script, tmp_path)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            combined = (proc.stdout + proc.stderr).lower()
            self.assertTrue(
                "symlink" in combined
                or "outside" in combined
                or "resolves outside" in combined
                or "directory" in combined,
                proc.stdout + proc.stderr,
            )
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_symlinked_replicas_root_fails(self) -> None:
        """replicas/ itself is a symlink escaping the workspace."""
        if os.name == "nt":
            self.skipTest("symlink probe not required on Windows")
        tmp_path, _src, script = _fixture_repo()
        try:
            real_replicas = tmp_path / "real-replicas-store"
            shutil.move(str(tmp_path / "replicas"), str(real_replicas))
            # Point replicas/ at a store outside the workspace root used by the script.
            escape_root = tmp_path / "escape-root"
            escape_root.mkdir()
            escaped = escape_root / "replicas"
            shutil.copytree(real_replicas, escaped)
            (tmp_path / "replicas").symlink_to(escaped.resolve(), target_is_directory=True)
            # workspace_anchors compares replicas.resolve() to root.resolve();
            # escaped is still under tmp_path, so move store fully outside tmp_path.
            shutil.rmtree(tmp_path / "replicas", ignore_errors=True)
            if (tmp_path / "replicas").is_symlink() or (tmp_path / "replicas").exists():
                (tmp_path / "replicas").unlink(missing_ok=True)
            outside_parent = Path(tempfile.mkdtemp())
            try:
                outside_replicas = outside_parent / "replicas"
                shutil.copytree(real_replicas, outside_replicas)
                (tmp_path / "replicas").symlink_to(
                    outside_replicas.resolve(), target_is_directory=True
                )
                proc = _run_verify(script, tmp_path)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                combined = (proc.stdout + proc.stderr).lower()
                self.assertTrue(
                    "replicas/" in combined and "outside" in combined,
                    proc.stdout + proc.stderr,
                )
            finally:
                shutil.rmtree(outside_parent, ignore_errors=True)
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_directory_symlink_probe_matches_review(self) -> None:
        """Exact adversarial probe from the HOLD re-audit (harmless fixtures only)."""
        if os.name == "nt":
            self.skipTest("symlink probe not required on Windows")
        import importlib.util

        tmp_path = Path(tempfile.mkdtemp())
        try:
            script = _install_script(tmp_path)
            spec = importlib.util.spec_from_file_location("verify_replicas", script)
            assert spec and spec.loader
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            root = tmp_path / "ws"
            outside = tmp_path / "outside"
            (root / "replicas").mkdir(parents=True)
            outside.mkdir()
            (outside / "PROOF.md").write_text(
                "fixture outside workspace\n", encoding="utf-8"
            )
            (outside / "SOURCE.json").write_text("{}", encoding="utf-8")
            (root / "replicas" / "sample").symlink_to(
                outside, target_is_directory=True
            )
            with self.assertRaises((ValueError, FileNotFoundError, OSError)):
                mod.resolve_confined_replica(
                    root / "replicas" / "sample" / "SOURCE.json",
                    "replicas/sample/PROOF.md",
                    root=root,
                )
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)

    def test_escaping_source_metadata_fails(self) -> None:
        """SOURCE.json reached only via a directory symlink must be rejected."""
        if os.name == "nt":
            self.skipTest("symlink probe not required on Windows")
        import importlib.util

        tmp_path = Path(tempfile.mkdtemp())
        try:
            script = _install_script(tmp_path)
            spec = importlib.util.spec_from_file_location("verify_replicas", script)
            assert spec and spec.loader
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            root = tmp_path / "ws"
            outside = tmp_path / "outside-meta"
            (root / "replicas").mkdir(parents=True)
            outside.mkdir()
            (outside / "SOURCE.json").write_text(
                json.dumps(
                    {
                        "bytes": 1,
                        "sha256": "a" * 64,
                        "source_drive_id": "x",
                        "replica_path": "replicas/sample/PROOF.md",
                        "schema_version": 1,
                        "no_private_sources": True,
                        "meaning": "probe",
                    }
                ),
                encoding="utf-8",
            )
            (outside / "PROOF.md").write_text("x", encoding="utf-8")
            (root / "replicas" / "sample").symlink_to(
                outside, target_is_directory=True
            )
            with self.assertRaises(ValueError):
                mod.confine_source_path(
                    root / "replicas" / "sample" / "SOURCE.json", root=root
                )
        finally:
            shutil.rmtree(tmp_path, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
