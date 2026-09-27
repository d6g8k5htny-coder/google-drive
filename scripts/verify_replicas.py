#!/usr/bin/env python3
"""Verify selected google-drive replicas against SOURCE.json and optional live Drive.

Scientific effect: NONE. A hash match is not theorem acceptance or currentness.
Does not change Drive sharing. Confines SOURCE metadata and replica payloads to the
resolved workspace replicas/ tree (rejects absolute, parent-relative, file-symlink,
directory-symlink, and replicas-root symlink escapes). Requires replicas/INDEX.json
and replicas/EXCLUDED.json.

Usage:
  python3 scripts/verify_replicas.py              # local SOURCE vs replica bytes
  python3 scripts/verify_replicas.py --live-drive # also re-download each Drive id
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLICAS = ROOT / "replicas"


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def workspace_anchors(root: Path) -> tuple[Path, Path]:
    """Return (workspace_resolved, replicas_resolved) anchored to workspace.

    Rejects a replicas/ directory (or symlink) that resolves outside the workspace.
    """
    workspace = root.resolve(strict=False)
    replicas_lexical = workspace / "replicas"
    replicas_resolved = replicas_lexical.resolve(strict=False)
    if not _is_relative_to(replicas_resolved, workspace):
        raise ValueError("replicas/ resolves outside workspace")
    return workspace, replicas_resolved


def confine_source_path(source_path: Path, *, root: Path = ROOT) -> tuple[Path, str]:
    """Require SOURCE.json itself to resolve under workspace/replicas/<folder>/.

    Returns (resolved_source_path, folder_name).
    """
    workspace, replicas_resolved = workspace_anchors(root)
    resolved = source_path.resolve(strict=True)
    if not resolved.is_file():
        raise FileNotFoundError(f"SOURCE path is not a file: {source_path}")
    if not _is_relative_to(resolved, replicas_resolved):
        raise ValueError(
            f"SOURCE path {source_path} resolves outside replicas/ "
            f"(possible directory symlink escape)"
        )
    rel = resolved.relative_to(replicas_resolved)
    if len(rel.parts) != 2 or rel.parts[1] != "SOURCE.json":
        raise ValueError(
            f"SOURCE path must be replicas/<folder>/SOURCE.json, got {rel.as_posix()!r}"
        )
    folder = rel.parts[0]
    if folder in ("", ".", "..") or "/" in folder or "\\" in folder:
        raise ValueError(f"invalid replica folder name {folder!r}")
    folder_resolved = (workspace / "replicas" / folder).resolve(strict=False)
    if not _is_relative_to(folder_resolved, replicas_resolved):
        raise ValueError(
            f"replicas/{folder}/ resolves outside replicas/ "
            f"(directory symlink escape)"
        )
    if resolved.parent.resolve(strict=True) != folder_resolved:
        raise ValueError(
            f"SOURCE parent for {folder} does not match confined replicas/{folder}/"
        )
    return resolved, folder


def load_source(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in (
        "bytes",
        "sha256",
        "source_drive_id",
        "replica_path",
        "schema_version",
        "no_private_sources",
        "meaning",
    ):
        if key not in data:
            raise ValueError(f"{path}: missing {key}")
    if data["schema_version"] != 1:
        raise ValueError(f"{path}: unsupported schema_version")
    if data.get("no_private_sources") is not True:
        raise ValueError(f"{path}: no_private_sources must be true")
    if not isinstance(data["source_drive_id"], str) or not data["source_drive_id"]:
        raise ValueError(f"{path}: empty source_drive_id")
    if not isinstance(data["sha256"], str) or len(data["sha256"]) != 64:
        raise ValueError(f"{path}: invalid sha256")
    if not isinstance(data["replica_path"], str) or not data["replica_path"]:
        raise ValueError(f"{path}: empty replica_path")
    return data


def resolve_confined_replica(
    source_path: Path, replica_path_field: str, *, root: Path = ROOT
) -> Path:
    """Resolve SOURCE replica_path strictly inside that SOURCE's replica directory.

    Anchors replicas/ and the selected folder to the resolved workspace boundary.
    Rejects absolute paths, parent-relative segments, payload symlink escapes, and
    directory/root symlink escapes that move the folder outside workspace/replicas/.
    """
    workspace, replicas_resolved = workspace_anchors(root)
    # Validate SOURCE confinement first (also rejects symlinked replica folders).
    _confined_source, folder = confine_source_path(source_path, root=root)
    folder_resolved = (workspace / "replicas" / folder).resolve(strict=False)
    if not _is_relative_to(folder_resolved, replicas_resolved):
        raise ValueError(
            f"{folder}: replicas/{folder}/ resolves outside replicas/ "
            f"(directory symlink escape)"
        )

    raw = replica_path_field
    candidate = Path(raw)
    if candidate.is_absolute():
        raise ValueError(
            f"{folder}: replica_path must be relative, got absolute {raw!r}"
        )
    if ".." in candidate.parts:
        raise ValueError(
            f"{folder}: replica_path must not contain '..': {raw!r}"
        )

    expected_prefix = Path("replicas") / folder
    # Lexical join only (no symlink follow) under workspace.
    lexical = Path(os.path.normpath(str(workspace / candidate)))
    expected_dir_lexical = Path(os.path.normpath(str(workspace / expected_prefix)))
    if not _is_relative_to(lexical, expected_dir_lexical):
        raise ValueError(
            f"{folder}: replica_path {raw!r} escapes replicas/{folder}/"
        )
    if not lexical.exists():
        raise FileNotFoundError(f"{folder}: missing confined replica {raw}")
    if not lexical.is_file() and not lexical.is_symlink():
        raise FileNotFoundError(f"{folder}: replica_path {raw!r} is not a file")

    # Follow symlinks only after lexical confinement; reject targets outside the
    # *workspace-anchored* folder (not a folder that has itself escaped via symlink).
    resolved = lexical.resolve(strict=True)
    if not resolved.is_file():
        raise FileNotFoundError(f"{folder}: missing confined replica {raw}")
    if not _is_relative_to(resolved, folder_resolved):
        raise ValueError(
            f"{folder}: replica_path {raw!r} resolves outside "
            f"replicas/{folder}/ via symlink or mount"
        )
    if not _is_relative_to(resolved, replicas_resolved):
        raise ValueError(
            f"{folder}: replica_path {raw!r} resolves outside replicas/"
        )
    return resolved


def fetch_drive(file_id: str) -> bytes:
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    with urllib.request.urlopen(url, timeout=120) as response:
        payload = response.read()
    if payload[:15].lower().startswith(b"<!doctype") or payload[:6].lower().startswith(
        b"<html"
    ):
        raise RuntimeError(f"Drive {file_id} returned HTML interstitial, not raw bytes")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live-drive",
        action="store_true",
        help="Re-download each SOURCE source_drive_id and compare bytes",
    )
    args = parser.parse_args()

    try:
        workspace_anchors(ROOT)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    sources = sorted(REPLICAS.glob("*/SOURCE.json"))
    if not sources:
        print("FAIL: no replicas/*/SOURCE.json found", file=sys.stderr)
        return 1

    excluded_path = REPLICAS / "EXCLUDED.json"
    index_path = REPLICAS / "INDEX.json"
    if not excluded_path.is_file():
        print("FAIL: missing required replicas/EXCLUDED.json")
        return 1
    if not index_path.is_file():
        print("FAIL: missing required replicas/INDEX.json")
        return 1

    checked = []
    for source_path in sources:
        try:
            confined_source, folder = confine_source_path(source_path)
            src = load_source(confined_source)
            replica = resolve_confined_replica(confined_source, src["replica_path"])
        except (ValueError, FileNotFoundError, OSError) as exc:
            label = source_path.parent.name if source_path else "?"
            print(f"FAIL {label}: {exc}")
            return 1
        raw = replica.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if len(raw) != src["bytes"] or digest != src["sha256"]:
            print(
                f"FAIL {folder}: local bytes/hash != SOURCE.json "
                f"(local {len(raw)}/{digest})"
            )
            return 1
        if args.live_drive:
            remote = fetch_drive(src["source_drive_id"])
            if remote != raw:
                print(
                    f"FAIL {folder}: live Drive "
                    f"{src['source_drive_id']} != local replica"
                )
                return 1
        checked.append(folder)
        print(
            f"PASS {folder}: "
            f"{src['bytes']} B sha256={src['sha256'][:12]}… "
            f"Drive {src['source_drive_id']}"
            + (" (live match)" if args.live_drive else " (local only)")
        )

    excluded = json.loads(excluded_path.read_text(encoding="utf-8"))
    if excluded.get("scientific_status_authority") is not False:
        print("FAIL EXCLUDED.json: scientific_status_authority must be false")
        return 1
    selected_ids = set()
    for folder in checked:
        confined_source, _ = confine_source_path(REPLICAS / folder / "SOURCE.json")
        src = json.loads(confined_source.read_text(encoding="utf-8"))
        selected_ids.add(src["source_drive_id"])
    for row in excluded.get("excluded", []):
        fid = row.get("source_drive_id")
        if fid in selected_ids:
            print(f"FAIL EXCLUDED.json lists selected Drive id {fid}")
            return 1
    print(f"PASS EXCLUDED.json ({len(excluded.get('excluded', []))} non-selected Drive ids)")

    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("scientific_status_authority") is not False:
        print("FAIL INDEX.json: scientific_status_authority must be false")
        return 1
    indexed = {row.get("folder") for row in index.get("replicas", [])}
    if indexed != set(checked):
        print(f"FAIL INDEX.json folders {sorted(indexed)} != verified {sorted(checked)}")
        return 1
    for row in index["replicas"]:
        confined_source, _ = confine_source_path(REPLICAS / row["folder"] / "SOURCE.json")
        src = json.loads(confined_source.read_text(encoding="utf-8"))
        for field in ("bytes", "sha256", "source_drive_id", "replica_path"):
            if row.get(field) != src.get(field):
                print(f"FAIL INDEX.json {row['folder']}.{field} != SOURCE.json")
                return 1
    print(f"PASS INDEX.json consistent with {len(checked)} SOURCE records")

    print(
        f"verified={len(checked)} meaning=exact bytes only; "
        "not currentness or theorem acceptance; scientific_effect=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
