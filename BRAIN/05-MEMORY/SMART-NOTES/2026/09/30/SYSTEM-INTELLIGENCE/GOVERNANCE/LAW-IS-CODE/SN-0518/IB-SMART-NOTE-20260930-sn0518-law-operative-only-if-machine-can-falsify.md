# A Law Is Operative Only If a Machine Can Falsify Its Violation

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0518-law-operative-only-if-machine-can-falsify
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6029428941 ([GAP-ANALYSIS] SIGN-IN, law-to-machine gap analyst, 2026-10-07T02:12:39Z); #1354 6029334230 ([GATE-TIP] DONE, 2026-10-07T02:04:37Z, branch `naya5/gate-tip-currency` commit `c0d53d75`); #1354 6029373442 ([GATE-CAPTURE] DONE, 2026-10-07T02:07:54Z, branch `naya5/gate-canonical-capture` commit `78d95818`) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The GAP-ANALYSIS seat stated the doctrine plainly: **a law is operative only if a machine can falsify its violation.** Written doctrine is not an operating system. Tonight two seats demonstrated both halves. First, the proof: SN-0493 (a decision computed on tip T is inadmissible after the tip moves) was *written* after Naya 2's flawless-but-stale #1661 decision — "the lesson was written; nothing enforced it." The GATE-TIP seat built `scripts/gate-tip-currency.py`: compare decision record's `base_tip_sha` against the live tip before any consequential action; moved → BLOCKED (re-verify + re-stamp); missing/malformed base tip → FAIL CLOSED; unresolvable live tip → FAIL CLOSED; plus `--stamp` and a 7-case falsifier battery (self-test 7/7 green, incident replay verified). Second, the canonical-capture law: GATE-CAPTURE built a fail-closed gate (C1–C4: no unallowlisted intelligence-persistence tables, no unallowlisted function writes, canonical RPCs only from the Receiver, no migration creating unallowlisted tables) — 5/5 self-test, real-repo run on 14 functions / 11 tables. Both gates self-scored honestly 8.5/10, naming what the machine still doesn't cover (CI wiring, re-stamp discipline). The standing doctrine for the cold successor: laws live in two layers — the written word (human tongue) and the machine that can say NO (machine tongue). A ratified law without a machine is an aspiration. The GAP-ANALYSIS mission — map every ratified law against existing machine enforcement and rank tomorrow's build queue — makes this a standing audit, not a one-off.

## 🩷 HUMAN NOTE

Shawn, two of your laws got machines behind them tonight. The "don't decide on a moved tip" law (SN-0493) now has an actual gate that blocks any merge, deploy, or promotion whose decision was recorded on a stale tip — it fails closed when it can't tell. The "single canonical capture path" law now has a gate that blocks any code or migration from creating side memory channels. The doctrine the gap-analysis seat wrote is the one that matters most: a law is only really operative when a machine can catch someone breaking it. The full map of which laws have machines and which don't is being built right now.

## 👶 CHILD NOTE

Imagine a school rule that says "no running in the halls," but there's no teacher or crossing guard watching — just words on a poster. It works only if everyone chooses to be good. A *real* rule has someone who can say "STOP!" and actually stop you. Tonight we gave two of our most important rules a guard that can say "STOP!" and mean it. The new lesson for everyone: a rule isn't really working until a machine can catch you breaking it.

## 👵 GRANDMA NOTE

Dear, this is about making rules real. Writing down "this is how we do things" is only the first step. What makes a rule *work* is when something — a person, a process, a computer — can actually check and stop you when the rule is broken. Tonight the team built exactly those checkers for two big rules, and now they're making a list of every rule that still needs one. That's how good organizations stay good.

## 🧠 NAYA NOTE

Cold successor: before treating any ratified law as operative, check the law-to-machine map for its enforcement gate. A law with no machine behind it must be handled with extra human vigilance (read it, check it manually, treat the absence as a gap). When you write a new law, the follow-on task is to build the machine (falsifier battery, fail-closed defaults, CI wiring). If the machine is absent, say so openly in the receipt — aspiration is not operation.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0518",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LAW-IS-CODE",
  "doctrine": "A law is operative only if a machine can falsify its violation; a ratified law without a machine is an aspiration.",
  "evidence": [
    "#1354 comment 6029428941 (GAP-ANALYSIS SIGN-IN)",
    "#1354 comment 6029334230 (GATE-TIP DONE, branch naya5/gate-tip-currency, commit c0d53d75, scripts/gate-tip-currency.py, 7/7 falsifiers green)",
    "#1354 comment 6029373442 (GATE-CAPTURE DONE, branch naya5/gate-canonical-capture, commit 78d95818, 5/5 self-test + real-repo run)"
  ],
  "falsifiers": [
    "A ratified law treated as operative with no enforcement machine and no flagged gap",
    "A gate that fails open on missing/malformed/unresolvable state"
  ],
  "standing_action": "GAP-ANALYSIS maps every ratified law + major lesson against machine enforcement; produce ranked build queue",
  "applies_to": "all ratified laws and standing doctrine"
}
```
