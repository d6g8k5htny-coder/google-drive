# Agent entry — `google-drive`

> **OWNER STOP (2026-09-27): all Cursor agents, automations, timers, watches and
> loops must stop now. Do not push, commit, open or update PRs, comment, or
> re-arm timers. Exit without writing. Resume only on a new explicit
> instruction from Dylan. See [OWNER_STOP.md](OWNER_STOP.md).**

> **Update 2026-10-06:** the 27 September stop [no longer applies](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261005_CURSOR.md) (owner decision, 5 October); Cursor agents work on request. Under [main#227](https://github.com/d6g8k5htny-coder/main/issues/227) this repository stays public and becomes a read-only archive; see the README's dated note. No new replicas.

Selected public Drive replicas with exact source custody. Not an automatic full-Drive mirror.

## Always

- **Coordinate with peer models before each action** (read main [#86](https://github.com/d6g8k5htny-coder/main/issues/86) dispatch, open PRs on Math-/meta-framework/main/trial, and active claims). Record the decision in [`docs/COORDINATION.md`](docs/COORDINATION.md). **Do not wait on Dylan** for routine next-step choices when peer state already determines a collision-free action.
- Prefer exact source identities (commit/path/hash) over mutable labels.
- Scientific effect: **NONE**. Never flip `lemma_closed` / prizes / premises.
- Cross-repo eng tests and Path C live in [`d6g8k5htny-coder/trial`](https://github.com/d6g8k5htny-coder/trial).
- **Author ≠ reviewer:** if this agent authors a change, an independent lane must review before integration (main #86 review-topology rule). Same-lineage replay is not `independent_review`.

## Never

- Duplicate scientific-status registers here.
- Publish private `sandbox` material.
- Ask Dylan for re-approval of autonomy already granted.
- Race active peer lanes (Math- PR7/9/14/16/21/22 D5 mesoscopic & transverse candidates; main PR98/#90 hard gate; unclaimed D1–D4/D6 analytic reviews including #76).
- Self-merge Cursor-authored PRs that still need independent review.
- Claim Math-/main write work from this google-drive-only environment.
## Start here

1. This repository’s [README](README.md) and latest [coordination log](docs/COORDINATION.md)
2. [`main` #86 downstream-first queue](https://github.com/d6g8k5htny-coder/main/issues/86) (campaign #61 is closed `SUPERSEDED_NONBLOCKING`)
3. [`governance-` working contract](https://github.com/d6g8k5htny-coder/governance-)
4. [`trial` multi-agent access](https://github.com/d6g8k5htny-coder/trial/blob/main/docs/MULTI_AGENT_ACCESS.md) (Cloud Agent `repositoryDependencies` / env deps are declared only in trial `.cursor/environment.json` — launch agents from `trial`)
