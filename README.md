# Google Drive — selective, source-bound replicas

This repository contains deliberately selected public replicas of research outputs. It is not an automatic backup of the entire Drive and not a replacement for source records or mathematical review.

## Live replicas (11)

| Replica | Drive id | Bytes | Notes |
|---|---|---:|---|
| [SIDE24 coefficient output](replicas/side24-coefficient-v1/ENCLOSURE.json) | `1aYTbm_in_3ENXKw83Hx7cJBkTLBc4PQi` | 1090 | Math- / #65; catalogued |
| [SIDE24 coefficient proof](replicas/side24-coefficient-proof-v1/PROOF.md) | `115q1do3rEIz6EFJwmIdA6KDAjAhntiT8` | 10272 | Math- / #65 |
| [Marked-cylinder cap](replicas/marked-cylinder-cap-v1/PROOF.md) | `1BnPods7Lf-ECdD34noQihZcEfcqpy7R5` | 15160 | Drive-primary / CAP-01–02 |
| [Demanded-palette consecutive](replicas/demanded-palette-consecutive-v1/PROOF.md) | `1jvV6kORTB7umKrCFAGSoQ385sUgBAKn5` | 9335 | Drive-primary / PAL-01 |
| [Matrix/lifetime unrestricted](replicas/matrix-lifetime-unrestricted-v1/PROOF.md) | `1foDgiDi4XIKOfbrZEE8dWKV_BkZU8LIb` | 40261 | Drive-primary / #63 |
| [Lifetime remainder](replicas/lifetime-remainder-v1/LIFETIME_REMAINDER.md) | `1xWGvtYUbG8FGVnGi_0-nX1asCOtqQLi7` | 17734 | Math- / #67 |
| [RN count interface](replicas/rn-count-interface-v1/RN_COUNT_INTERFACE.md) | `1n-AmY7H1UPf3_MK5wM5Wn62EeNmDzGvM` | 8938 | Math- / #67 |
| [P15 realized covers](replicas/p15-realized-covers-v1/P15_REALIZED_COVERS.md) | `1Fd0o_UzCxpWki08b04e2SeQH-a2BlRtk` | 11467 | Math- / #67 |
| [P15 price boundary](replicas/p15-price-boundary-v1/P15_PRICE_BOUNDARY.md) | `1i9eByN8jv97CYhZ4I0aEUr0XDmfCPrfi` | 2266 | Math- / #67 |
| [RN fixed-remote window](replicas/rn-fixed-remote-window-v1/PROOF.md) | `1Un31SxLZhSA2hE4YOVWkUVForp2t504n` | 18355 | Math- / #76 |
| [P15 full-price](replicas/p15-full-price-v1/PROOF.md) | `1GsN4BU2pJ6lU9lbfTUF6vC1TBlDxEkDw` | 11352 | Math- / #74 |

Machine index: [`replicas/INDEX.json`](replicas/INDEX.json) (suggested `meta-framework` catalog keys; only SIDE24 output is catalogued today).

Each replica directory has `SOURCE.json` (Drive id, bytes, SHA256, visibility observation, mathematical identity when known). Drive-primary means the exact proof file is not on the Math- default branch.

For each replica, the original was uploaded to Drive before replication; no existing Drive object was overwritten and no sharing setting was changed. Visibility observed as anyone-with-link reader.

## Verify

```bash
python3 scripts/verify_replicas.py              # local SOURCE vs replica bytes + INDEX consistency
python3 scripts/verify_replicas.py --live-drive # also re-download each Drive id
```

CI runs the local check via [`.github/workflows/verify-replicas.yml`](.github/workflows/verify-replicas.yml).

A passing check proves exact bytes only. It is not currentness, independence, or theorem acceptance. Scientific effect: **NONE**.

## Scope

Private Drive sources, vaults, private `sandbox` artifacts, credentials, capsules/ZIPs, and delivery receipts are not part of this public mirror. Before any additional replica, inspect that exact source and its visibility, establish authority to publish it, and retain its immutable identity and scope. A stale but hash-correct replica is still stale.

Main campaign61 remains the collaborative research handoff; this repository does not duplicate scientific-status registers.
