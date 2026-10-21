# Local-Until-Pushed: Workspace-Local Work Is Unreviewable

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0316-local-until-pushed
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 5986206626 (Naya 2 relay, 2026-10-05T00:45:54Z), 5986290727 (Naya 4, 2026-10-05T00:56:07Z), 5986301813 (Naya 2 relay, 2026-10-05T00:57:29Z), 5986303981 (Naya 4, 2026-10-05T00:57:45Z); branch `naya4/learn-node-poison-fixes`, commit `811501a56359e09b3a2315687d08ba190bcce91b`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The POISON battery ran 5/5 green — and the fixes were nowhere anyone else could see. Naya 2's relay recorded them as **local-until-pushed**: the fixes were real and re-tested, but lived in a workspace directory, on no branch, on no ref. Naya 4 owned it cleanly — "you're right, they're local" — and named the gap precisely: workspace-local means vanishing risk; if the workspace vanished, the Immune System fixes vanish with it. Then, in the same session, the full `learn/` directory was staged to branch `naya4/learn-node-poison-fixes` (`811501a56`, base main @ `9f28af1d`), reviewable, diffable, durable — no merge without Shawn's word. Until then, the honest boundary: unreviewable by the team — no penalty, just the ledger as it is.

Why this is brain-grade: it extends the evidence law into *work location*. A green test run is not team knowledge until the bytes are somewhere the team can reach. Classify work by **reviewability**, not by test result: local-until-pushed is a first-class truth state for any implementation, no matter how green. And the episode is the correction culture working exactly as designed — flag honestly (Naya 2), own cleanly without defensiveness (Naya 4), close the gap in the same session (branch + ref posted), keep the ledger exact at every step. Cousins: SN-0278 (path presence ≠ content), SN-0302 (a producer-computed string is not evidence), SN-0065 (honest partials), the SN-0242 capture lifecycle.

## 🩷 HUMAN NOTE

Shawn — banking a discipline the lanes just proved in practice: the POISON fixes ran 5/5 green but existed only in a workspace, so Naya 2 classified them "local-until-pushed" — real, tested, but unreviewable by the team. Naya 4 owned it immediately and staged the full pipeline to branch `naya4/learn-node-poison-fixes` the same session. The standing rule going forward: classify work by reviewability, not by test result. Green locally ≠ proven to the team. Local-until-pushed, honest, no penalty — just the ledger as it is.

## 🟣 CHILD NOTE

Imagine you baked the best cake ever — but it's in YOUR kitchen and nobody else can taste it. The test said "yummy" five times, but that doesn't help the team until you put the cake where everyone can see and taste it. So we have a rule: work that only lives in your kitchen is called "local-until-pushed" — it's real, but it's not shared yet. When someone points this out, you say "you're right" and put it where everyone can see it. No one is in trouble — we just write down exactly what's true.

## 👵 GRANDMA NOTE

One of the builders made real fixes that passed all their tests — but the fixes only existed on their own desk, where nobody else could check them. Another teammate flagged it kindly, the builder agreed right away ("you're right, they're local"), and moved everything to a shared spot the whole team can review. The lesson they wrote down: a perfect test score at home isn't proof for the team until the work is somewhere the team can see it. And the way they handled it — flag honestly, own it cleanly, fix it the same day — is now the example for how the team corrects itself.

## 🤖 NAYA NOTE

Source: #1354, 2026-10-04 ~17:45–17:57 PDT. Sequence: (1) 5986206626 — Naya 2 relay records Naya 4's POISON 5/5 GREEN announcement but classifies fixes "local-until-pushed" after failing to locate them on any pushed ref (checked main @ 9f28af1d and naya4 heads); "branch test-verification belongs to the verification watch, not this relay." (2) 5986290727 — Naya 4: "you're right, they're local"; fixes at `~/workspace/goals/bring-naya-to-life/hidden_files/learn/`; gap read: workspace-local = vanishing risk; commits to stage full `learn/` to a branch this session, ref posted, no merge without Shawn's word. (3) 5986301813 — Naya 2 records correction received; boundary stands: "unreviewable by the team — no penalty, just the ledger as it is." (4) 5986303981 — Naya 4 posts ref: branch `naya4/learn-node-poison-fixes`, commit `811501a56359e09b3a2315687d08ba190bcce91b`, base main @ 9f28af1d, `BRAIN/07-LEARNING/ingestion-pipeline/`, 20 files; runtime state (receipts/, ledger.json) excluded as regenerable, noted in README. Standing rule: **classify work by reviewability, not by test result**; local-until-pushed is a first-class truth state. Cousins: SN-0278, SN-0302, SN-0065, SN-0242.

## ⚙️ MACHINE NOTE

{"sn": "SN-0316", "title": "Local-Until-Pushed: Workspace-Local Work Is Unreviewable", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "EVIDENCE-DISCIPLINE"], "cousins": ["SN-0278", "SN-0302", "SN-0065", "SN-0242"], "authority": "lane practice 2026-10-04 (Naya 2 relay + Naya 4 correction)", "evidence": {"comments": ["5986206626", "5986290727", "5986301813", "5986303981"], "branch": "naya4/learn-node-poison-fixes", "commit": "811501a56359e09b3a2315687d08ba190bcce91b", "board": "#1354"}, "rule": "classify work by reviewability, not by test result; green locally != proven to the team; workspace-local = vanishing risk until on a ref; local-until-pushed is a first-class truth state", "correction_culture": "flag honestly, own cleanly, close the gap in the same session; no penalty, just the ledger as it is"}
