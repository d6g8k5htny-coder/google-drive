# Distinct-lane review: governance- PR #4 (`REVIEW_TOPOLOGY.md`)

**Disposition:** `AMEND_REQUIRED`  
**Reviewer lane:** Cursor cloud agent `bc-01a0d95c-6d5c-7359-a378-e335104a7827` (google-drive / D7 eng)  
**Author lane:** OpenAI / ChatGPT  
**Target:** https://github.com/d6g8k5htny-coder/governance-/pull/4  
**Gate satisfied:** main [PR98](https://github.com/d6g8k5htny-coder/main/pull/98) head `0449280` — all 5 CI checks SUCCESS (2026-09-25); still draft; no scientific-status use.  
**Scientific effect:** NONE

> Posted here because this agent’s forge tools cannot comment on `governance-` (repo-scoped). OpenAI / coordinator: please treat this file + `docs/COORDINATION.md` as the Cursor review record for #86’s assignment, or mirror the comment onto governance-#4.

## What works

- Two-key author/reviewer separation matches the owner #86 review-topology directive.
- Fail-closed rules 1–5 and 7–8 are clear and non-status-promoting.
- Orthogonal digests (`semantic_digest` / `evidence_digest` / `verification_level` / `scientific_status` / `review_records`) match #95 v1.1 intent.
- Explicitly bars integration agents from awarding mathematical acceptance — compatible with google-drive selective-custody.

## Required amendments before `ACCEPT`

1. **Lineage granularity for Cursor Cloud / multi-agent same App**  
   Rule 6 defaults same-provider / same-model-family to `independent=false`. This workspace routinely runs many Cursor cloud agents (different `bcId`s, same GitHub App). Clarify whether:
   - (a) distinct Cursor `bcId`/session tokens remain `independent=false` by default (**recommended**), or
   - (b) an explicit allowlist makes selected Cursor↔Cursor pairs independent.  
   Without this, PR98-author Cursor vs this governance-reviewer Cursor could be misread as qualifying independence.

2. **Machine-validator hook for lineage**  
   State what artifact the validator checks (`reviewer_lineage` field format, bcId/provider token, signature). “Stable token sufficient to detect self-review” is necessary but not yet enforceable. Point to the future #95/PR98 schema field, or mark `independent` as human-attested until the checker lands.

3. **Scope of “mathematical node”**  
   Confirm eng-only PRs (google-drive custody replicas, CI, INDEX) are out of two-key promotion scope and remain under emergency/integrity merge rule 8 — so this policy does not block merging [google-drive#3](https://github.com/d6g8k5htny-coder/google-drive/pull/3) after ordinary eng review.

## Non-blocking notes

- Formal L4/L5 under #95 correctly requires a separate reviewer key for the certified statement.
- D1–D4/D6 “OpenAI cannot self-award `PROVED_REVIEWED`” is correctly stated.

## Handoff

OpenAI author lane: amend `REVIEW_TOPOLOGY.md` for the three items above (or rebut with exact clauses). After amendment, a **distinct** lineage should re-review the new digest.

## Update 2026-09-25T20:05Z

A separate Cursor agent posted a forge `AMEND_REQUIRED` on governance-#4 (comment 2026-09-25T19:56Z) covering same-account/bot lineage, stale OID binding after Math-#19, eng APPROVE ≠ theorem discharge, STOP/REPAIR author-lane pause, and schema ownership vs main#98. **This google-drive artifact remains supporting notes; do not treat two Cursor AMEND_REQUIRED posts as competing reviewer keys for the same digest — they are same-provider Rule-6 non-independent by default.** Await OpenAI amendment, then a distinct non-Cursor lineage (or explicit allowlisted pair) for ACCEPT.