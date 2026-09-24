# google-drive

Public **Drive replica shell**. Holds a git-facing mirror of selected Google Drive material for the Dylan Roy research stack. It is a **replica**, not the source of truth.

| Repo | Role |
|------|------|
| [`d6g8k5htny-coder/main`](https://github.com/d6g8k5htny-coder/main) | Research program (q0 / SIDE24). Authority and status live there. |
| **this repo** | Empty-by-design Drive replica container. No scientific authority. |
| [`d6g8k5htny-coder/trial`](https://github.com/d6g8k5htny-coder/trial) | Owner sandbox / agent landing pad. |

## Purpose

- Mirror Drive trees into git when the owner asks, with clear quarantine vs live lanes.
- Keep replica hygiene visible (what was copied, what stays vaulted).
- Never promote mirrored files into research status on `main`.

## What belongs here

- Replica trees, manifests, and hygiene notes for Drive → git.
- Pointers to vault / DO_NOT_OPEN policy (quarantine ≠ SoT).

## What does not belong here

- Claim status flips, prize registers, or OBL discharge language.
- Replacing `main` as the research tip.
- Diluting [`trial`](https://github.com/d6g8k5htny-coder/trial)'s README or role.

## Non-claims

- `lemma_closed`, `prizes_solved`, `discharges_OBL_H5_JETMOD`, and `certified_C_H` stay **unchanged / false** unless `main` records otherwise under its own predicates.
- Eng ≠ discharge. OBL stays **OPEN**.
- **NEVER-MAIN**: live research tip work stays on the hardening branch of `main`, not on this shell's default tip.

## Related shells

| Shell | Note |
|-------|------|
| `meta-framework` | Meta / framework scaffolding |
| `query-` | Query / ask surface |
| `governance-` | Governance / protocol surface |
| `Math-` | Math structure/purpose only |
| `trial` | Strong README — do not dilute |
| `sandbox` | Private — MCP-only; no public clone expected |
