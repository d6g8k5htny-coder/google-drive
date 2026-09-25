# Google Drive — selective, source-bound replicas

This repository contains deliberately selected public replicas of research outputs. It is not an automatic backup of the entire Drive and not a replacement for source records or mathematical review.

## Live replicas

| Replica | Drive id | Bytes | SHA256 (prefix) | Notes |
|---|---|---:|---|---|
| [SIDE24 coefficient output](replicas/side24-coefficient-v1/ENCLOSURE.json) | `1aYTbm_in_3ENXKw83Hx7cJBkTLBc4PQi` | 1090 | `72b6cd92…` | Math- `e329fba1…` / main#65 |
| [SIDE24 coefficient proof](replicas/side24-coefficient-proof-v1/PROOF.md) | `115q1do3rEIz6EFJwmIdA6KDAjAhntiT8` | 10272 | `c06daccc…` | Math- `e329fba1…` / main#65 |
| [Marked-cylinder cap proof](replicas/marked-cylinder-cap-v1/PROOF.md) | `1BnPods7Lf-ECdD34noQihZcEfcqpy7R5` | 15160 | `0bf922b9…` | Drive-primary / CAP-01–02 |
| [Demanded-palette consecutive proof](replicas/demanded-palette-consecutive-v1/PROOF.md) | `1jvV6kORTB7umKrCFAGSoQ385sUgBAKn5` | 9335 | `6abcc060…` | Drive-primary / PAL-01 |
| [Matrix/lifetime unrestricted proof](replicas/matrix-lifetime-unrestricted-v1/PROOF.md) | `1foDgiDi4XIKOfbrZEE8dWKV_BkZU8LIb` | 40261 | `9350ad6e…` | Drive-primary / main#63 |
| [RN fixed-remote window proof](replicas/rn-fixed-remote-window-v1/PROOF.md) | `1Un31SxLZhSA2hE4YOVWkUVForp2t504n` | 18355 | `a332bae9…` | Math- `191ea7d5…` / main#76 |
| [P15 full-price proof](replicas/p15-full-price-v1/PROOF.md) | `1GsN4BU2pJ6lU9lbfTUF6vC1TBlDxEkDw` | 11352 | `87521901…` | Math- `f9938338…` / main#74 |

Each directory has a `SOURCE.json` custody record (Drive id, bytes, SHA256, visibility observation, mathematical identity when known). Several author-side parent proofs are **Drive-primary** (not on the Math- default branch); those replicas are the public byte-custody homes for the exact proof files.

For each replica, the original new output was uploaded to Drive before replication; no existing Drive object was overwritten and no sharing setting was changed. Source visibility was observed as anyone-with-link reader. Raw Drive downloads matched the local replica bytes at publication.

## Verify

```bash
python3 scripts/verify_replicas.py              # local SOURCE vs replica bytes
python3 scripts/verify_replicas.py --live-drive # also re-download each Drive id
```

A passing check proves exact bytes only. It is not currentness, independence, or theorem acceptance. Scientific effect: **NONE**.

## Scope

The `meta-framework` registry and `query-` CLI make catalogued replicas locatable and byte-verifiable alongside original calculations. Private Drive sources, vaults, private `sandbox` artifacts, credentials and unspecified files are not part of this public mirror. Capsules/ZIPs and delivery receipts are not auto-mirrored here. Before any additional replica, inspect that exact source and its visibility, establish authority to publish it, and retain its immutable identity and scope. A stale but hash-correct replica is still stale.

Main campaign61 remains the collaborative research handoff; this repository does not duplicate scientific-status registers.
