#!/usr/bin/env python3
"""Verify selected google-drive replicas against SOURCE.json and optional live Drive.

Scientific effect: NONE. A hash match is not theorem acceptance or currentness.
Does not change Drive sharing. Refuses private/sandbox paths by construction
(only walks replicas/*/SOURCE.json in this repository).

Usage:
  python3 scripts/verify_replicas.py              # local SOURCE vs replica bytes
  python3 scripts/verify_replicas.py --live-drive # also re-download each Drive id
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLICAS = ROOT / "replicas"


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
    return data


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

    sources = sorted(REPLICAS.glob("*/SOURCE.json"))
    if not sources:
        print("FAIL: no replicas/*/SOURCE.json found", file=sys.stderr)
        return 1

    checked = []
    for source_path in sources:
        src = load_source(source_path)
        replica = ROOT / src["replica_path"]
        if not replica.is_file():
            print(f"FAIL {source_path.parent.name}: missing {src['replica_path']}")
            return 1
        raw = replica.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if len(raw) != src["bytes"] or digest != src["sha256"]:
            print(
                f"FAIL {source_path.parent.name}: local bytes/hash != SOURCE.json "
                f"(local {len(raw)}/{digest})"
            )
            return 1
        if args.live_drive:
            remote = fetch_drive(src["source_drive_id"])
            if remote != raw:
                print(
                    f"FAIL {source_path.parent.name}: live Drive "
                    f"{src['source_drive_id']} != local replica"
                )
                return 1
        checked.append(source_path.parent.name)
        print(
            f"PASS {source_path.parent.name}: "
            f"{src['bytes']} B sha256={src['sha256'][:12]}… "
            f"Drive {src['source_drive_id']}"
            + (" (live match)" if args.live_drive else " (local only)")
        )

    print(
        f"verified={len(checked)} meaning=exact bytes only; "
        "not currentness or theorem acceptance; scientific_effect=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
