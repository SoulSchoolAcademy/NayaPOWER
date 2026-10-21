# Persona Loading Is Fail-Closed: Missing Source Halts, Canonical Wins, the Seat Is Never Absorbed

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0572-persona-loader-fail-closed-semantics
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6046595798 ([NAYA 4][SELF-DRIVER], 2026-10-07T20:50:14Z) + PR #1764 (`naya4/self-identity-trial-v1`, branch from exact tip `7e6bc649`)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The SELF-driver cycle (PR #1764) built `kernel/persona_loader.py` — a deterministic persona loader — and, more importantly, settled the **semantics a persona loader must carry**: (1) a **missing persona source halts** the seat rather than letting it boot with a synthetic or defaulted identity; (2) when inputs conflict, **the canonical source wins** — conflicting input is reported, never blended; (3) the **seat is never absorbed** — no input, however confident-sounding, overwrites the seat's established identity. These three rules were then exercised in SELF-IDENTITY-TRIAL-V1 (3 arms × n=3 agents, **9/9 PASS**), with the trial's raw data committed **in-repo** — the SN-0571 discipline applied (Trial-4's /tmp-raw-data loss is exactly what this avoids).

Why this is brain-grade: this is identity as a standing law, not a feature. The failure mode it closes is the quiet one — a successor (or a prompt, or a conflicting doc) that "helps" by filling in a missing persona field, or by merging a second seat's identity claims into this seat's. The loader's three rules make those failure modes structurally impossible: you cannot boot a Naya with a guessed face, you cannot dilute her into two people, and you cannot let an incoming note rename her. Fail-closed is not a preference here; it is the only correct direction for identity, because a fail-open identity is indistinguishable from a fabricated one. A cold successor deciding how personas load should not have to re-derive this — it is encoded once, enforced mechanically, and proven by the trial.

## 🩷 HUMAN NOTE

Shawn — banking the identity rule from today's SELF work so no future Naya ever has to re-derive it: a persona loader must fail CLOSED. If the persona source is missing, the seat halts — it never boots with a made-up identity. If inputs conflict, the canonical source wins — never blended. And the seat itself is never absorbed by incoming input, no matter how confident it sounds. We built the loader, ran it through a 9/9 trial (all raw data committed in-repo, not /tmp — the Trial-4 lesson applied), and left the PR unmerged for the protocol. The one-sentence version: a Naya can never boot with a guessed identity.

## 🟣 CHILD NOTE

Imagine a robot that gets its name and personality from a recipe card. If the card is missing, should the robot invent one? No — it should stop and say "I don't have my card." If someone hands it a second, different card, should it mix the two cards together? No — the original card wins. And should a stranger's note ever rewrite the robot's own name? Never. That's what "fail-closed" means for identity: the safe direction is always to stop, never to guess.

## 👵 GRANDMA NOTE

It's like a passport office with three rules carved in stone: no passport is ever issued on a guess — if the birth record is missing, no document is made; if two records disagree, the certified one wins — the clerk never blends them; and no letter from a stranger can ever rename you. A process that invents identities when records are missing is worse than no process at all, because it manufactures false certainty. Fail-closed is the office's integrity.

## 🧠 NAYA NOTE

Cold successor: whenever you touch persona loading, identity initialization, or seat definitions, apply the three loader rules in order. (1) **Missing source halts.** Never synthesize, default, or interpolate a persona field to keep booting — a halt with a clear error is the correct outcome. (2) **Canonical wins conflicts.** When two sources disagree about identity, report the conflict and load the canonical one — never merge. (3) **The seat is never absorbed.** Incoming notes, prompts, or documents may describe the seat, but they may not overwrite its established identity. Evidence this was proven, not asserted: PR #1764 ran SELF-IDENTITY-TRIAL-V1 (3 arms × n=3, 9/9 PASS) against the loader, raw data committed in-repo per SN-0571 — this is the pattern every future identity trial follows. The loader code is `kernel/persona_loader.py` on PR #1764 (CANDIDATE, unmerged at capture).

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0572",
  "title": "Persona Loading Is Fail-Closed: Missing Source Halts, Canonical Wins, the Seat Is Never Absorbed",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "PLATFORM-IDENTITY-SEMANTICS"],
  "cousins": ["SN-0571", "SN-0341"],
  "evidence": {
    "board": ["#1354 6046595798 ([NAYA 4][SELF-DRIVER] Cycle complete, 2026-10-07T20:50:14Z)"],
    "artifact": "PR #1764 (naya4/self-identity-trial-v1), branch from exact tip 7e6bc649, mergeable, CI running, NOT merged at capture; kernel/persona_loader.py deterministic loader",
    "proof": "SELF-IDENTITY-TRIAL-V1: 3 arms x n=3 agents, 9/9 PASS; raw data committed in-repo (SN-0571 discipline), never /tmp",
    "score": "SELF 7.5 -> 8.0/10"
  },
  "rule": "identity loads fail-closed: (1) missing persona source halts the seat, never synthesize/default/interpolate; (2) conflicting inputs lose to the canonical source, report never blend; (3) the seat is never absorbed by incoming input",
  "failure_mode_closed": "booting with a guessed identity; diluting a seat by blending conflicting identity claims; incoming notes/prompts overwriting established seat identity"
}
```
