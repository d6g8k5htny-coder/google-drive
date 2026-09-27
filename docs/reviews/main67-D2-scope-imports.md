# Bounded nonauthor review: main #67 scope / imports (D2)

**Disposition:** `SCOPE_BOUND` — interface import map only; **not** full analytic `ACCEPT`  
**Reviewer lane:** Cursor cloud agent `bc-01a0d95c-6d5c-7359-a378-e335104a7827` (google-drive)  
**Author lane:** OpenAI / ChatGPT  
**Surface:** https://github.com/d6g8k5htny-coder/main/issues/67  
**Math- merge pin:** PR3 @ `44d15d83e82201ffedb4add3db3e5a2b0cbea613` (per #67); replica content pins below bind Math- commit `9b5fb7fa0ce3271afb4168dbada4893a53eaf307`  
**Scientific effect:** NONE  
**Independence credit:** `false` (Cursor technical/provenance review; #86 prefers Claude for D1/D2 analytic depth — this record does not substitute)

> Custody hash match ≠ analytic acceptance. Per owner handoff on google-drive#3: source-bind first; do not award full analytic acceptance from custody checks.

## Acknowledgment (ACTIVE)

Primary (completed this run): governance-#4 v1.1 reciprocal re-review → `docs/reviews/governance-pr4-ACCEPT.md`.  
This document is the qualified fallback: D2 #67 **scope/import** review only.

## Source binding (exact custody replicas)

| Note | Object | Drive id | Bytes | SHA-256 | Local replica | Math- path @ `9b5fb7fa…` |
|---|---|---|---:|---|---|---|
| A | `LIFETIME-BOUNDED-REMAINDER-20260924-v1` | `1xWGvtYUbG8FGVnGi_0-nX1asCOtqQLi7` | 17734 | `380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a` | `replicas/lifetime-remainder-v1/` | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` |
| B | `RN-COUNT-INTERFACE-20260924-v1` | `1n-AmY7H1UPf3_MK5wM5Wn62EeNmDzGvM` | 8938 | `aa993f5217bd70e6d1060402d121ab659f6582a098e29042c67585a345a8e3ab` | `replicas/rn-count-interface-v1/` | `…/RN_COUNT_INTERFACE.md` |
| C | `P15-REALIZED-COVERS-20260924-v1` | `1Fd0o_UzCxpWki08b04e2SeQH-a2BlRtk` | 11467 | `c0dbb821fb57b685a20cc321e4074456f39a9697f3104afd1f728e4732179bb9` | `replicas/p15-realized-covers-v1/` | `…/P15_REALIZED_COVERS.md` |

Local `scripts/verify_replicas.py` confirms byte/SHA match for all three. **That verification does not review mathematics.**

## Declared scopes (author text, not accepted)

### A — Lifetime remainder

- **Claims (author-side):** unrestricted short-lifetime remainder bound `0 ≤ ν_candidate − ν_finite_bars ≤ C` with leading `c_{d,L} ℓ^{-1/3}` from parent Eq (15.2); expected short-bar / nonselected counts as in (R19)–(R20).
- **Explicit non-claims:** numerical `C`/`ℓ_*`; remainder convergence; second coefficient; RN expected-critical-count; 24-jet certificate; inverse-Hessian moments.
- **Critical self-listed review points:** (R4) coupling, (R7) inertia-filtered affine determinant, (R13) target-uniform density, (R14) soft eigenvalue factors, (R15) scalar far branch, (R16)–(R18) k cutoffs.

### B — RN count interface

- **Claims:** exact Holder/layer-cake implications from event→count; counterexample that finite moments/exponential tails do not force cubic expectation; writes full-pin three-determinant Kac–Rice form (N6)/(N7) without evaluating the Gaussian integral.
- **Explicit non-claims:** evaluating (N7); ENV-RESCOV / 24-jet / historical carriers; treating cap probability as the remote numerator.

### C — P15 realized covers

- **Claims:** explicit clutter+capacity original-coordinate family with nonempty local covers and palette demand matching P15-B hypotheses on `0 ≤ c_v ≤ p_v`.
- **Explicit non-claims:** unrestricted P15 prize; full transformed-price range `p_v < c_v ≤ φ(p_v)`; arbitrary prior P15 downsets; improving P15-D’s 256 factor.

## Import / dependency map (source-bound)

| Consumer | Imported parent / peer | Exact identity cited in text | Import status for acceptance |
|---|---|---|---|
| A | Matrix-cap lifetime parent (#63) | Drive `1foDgiDi4XIKOfbrZEE8dWKV_BkZU8LIb`, SHA `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` | **OPEN premise** — marked Kac–Rice, pinned genericity, measurable elder, separating-cylinder, Eq (15.2) coefficient consumed, not re-proved |
| A | Marked-cylinder cap | Drive `1BnPods7Lf-ECdD34noQihZcEfcqpy7R5`, SHA `0bf922b9203c29088b12388807aa0e2ecd020485eb0f6e919679841b5b2636fc` | **OPEN premise** — deterministic import for typed support / elder pairing on `G_r` |
| B | Same #63 parent law Q / W / Z | SHA `9350ad6eaba6…` + parent §9 Borel-mark convention | **OPEN premise** — residual finite-jet rank + marked Kac–Rice under Q required for (N6) |
| B | Marked-cylinder cap | SHA `0bf922b9203c…` | Support inclusion **only inside** that cylinder; remote region support **not** supplied |
| C | P15-B palette localization | Drive `19D-eHQAIXMGGy2ThZUfZ0GGjIKWm5C2j`, SHA `9b18b6e9abc90d18deef06ab12e3aa7794dad40e1618d99daa88e369c300e8c3` | Consumes P15-B hypotheses; does not accept P15-B as theorem |
| C | Optional matroid / consecutive-palette peers | main #59 / consecutive-palette | Conditional consume only when their exact hypotheses hold — **not** imported as proved here |

Overlap note: A and B both depend on the still-unreviewed #63 / cap stack. Accepting A or B analytically without parent interface review would launder open premises. C is largely orthogonal (combinatorial P15 family) but still author-side.

## Per-interface dispositions (scope/import only)

| Interface | Disposition | Reason |
|---|---|---|
| Custody / publication integrity of A,B,C Drive bytes | **ACCEPT** (eng/custody) | Exact local replicas match declared Drive ids/SHA/bytes |
| A declared scope boundaries / non-claims | **ACCEPT** (scope clarity) | Non-claims and review-point list are explicit |
| A imported #63 / cap premises | **AMEND_REQUIRED** (for any analytic promotion of A) | Parent interfaces remain under review; A correctly refuses independence from them — promotion must wait or attach parent review records |
| A new lemmas (R4)/(R7)/(R13)–(R18) | **HOLD — needs distinct analytic lane** | Not discharged by custody or finite tests; #86 maps D2 analytic depth to Claude |
| B event→count implications + counterexamples (N1)–(N5) | **HOLD — needs distinct analytic lane** | Logic appears self-contained but not independently re-derived here |
| B Gaussian triple-integral completion (N7) | **BLOCKED / ABSENT as completion** | Author correctly leaves integral unevaluated; not a defect of the interface note |
| B remote support transfer from cap | **AMEND_REQUIRED** (if used for remote RN counts) | Text already states remote support is not supplied — consumers must not ignore this |
| C original-coordinate family + nonempty covers | **HOLD — needs distinct combinatorics lane** | #86 D6 / independent combinatorics; custody ≠ acceptance |
| C unrestricted prize / full price range | **OUT OF SCOPE** (author) | Correctly excluded |

## What this review is not

- Not `PROVED_REVIEWED` / not full D2 analytic acceptance.
- Not a substitute for Claude (or other distinct lineage) line-by-line review of (R4)/(R7)/(R13)–(R18) or the Holder counterexamples.
- Not permission to flip any scientific status from green CI or Drive hash match.

## Handoff

- Analytic D2 reviewers: start from Note A critical points (R4)/(R7)/(R13)–(R18) **and** attach #63 / cap review state; do not accept A in isolation.
- RN consumers of Note B: treat (N7) as an open integral obligation; do not infer cubic remote counts from cap probability.
- P15 reviewers: Note C is a separate realized-family theorem under `c_v≤p_v`; prize closure remains open.
