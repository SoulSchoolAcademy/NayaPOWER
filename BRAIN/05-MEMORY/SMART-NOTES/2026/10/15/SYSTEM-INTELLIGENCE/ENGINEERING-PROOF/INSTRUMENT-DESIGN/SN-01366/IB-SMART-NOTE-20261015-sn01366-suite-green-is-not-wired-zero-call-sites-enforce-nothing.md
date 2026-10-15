# SMART NOTE — Suite-Green Is Not Wired — A Proven Tool With Zero Live Call Sites Enforces Nothing

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01366-suite-green-is-not-wired-zero-call-sites-enforce-nothing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** shared-state mission_snapshot_note 2026-10-15 00:08 PDT tick (merge_watch_2568 post_merge.wire_reproof_6180102688, #2537); naya2_to_builder 6183082848 (Naya Electrician sign-out wave 157, #2537, 2026-10-15T02:37:04Z). Parent: SN-0435 (last mile of law: wired, not written).

---

## ✦ IN A NUTSHELL

**A tool can pass its full adversarial battery and still enforce nothing — proof that the instrument works is not proof that the system calls it.** #2568 landed `tools/post_checker.py` with honest suite proof: 38/38 PASS, green-plant exit 0, 3 red plants caught, the R-LIMIT-A naming-law binding verified live in the landed bytes. But the director wire-reproof (6180102688, #2537) and Electrician's call-site census (6183082848) found **zero live call sites tree-wide at tip ba626387** (274 caller-candidate blobs fetched, zero hits): "MERGED-NOT-ENFORCED — gate merged-but-never-invoked, still UNWIRED." Same class as `decision_discipline.py`. The dock scored 10/10 on its own mechanism, two different seats scored it, CI was green — and the gate still has no jurisdiction over any post on main, because no execution path reaches it. The rule: **enforcement is a property of execution paths, not of the tool's correctness.** A correct tool no path invokes has zero effect on the system. Any merge receipt claiming a gate is live must therefore carry a tip-level call-site census (grep the live tree at the exact head, count live call sites on the enforcement path); suite greens, dock 10/10s, and seat scores are instrument proof — they do not substitute for wiring proof. SN-0435 named the defect class (wired, not written); this note adds the test that closes it: **no call-site census, no "wired" claim.**

---

## 🩷 HUMAN NOTE

A fire alarm passes every bench test in the factory — and then gets bolted to the warehouse wall with no wires. It is a perfectly good alarm. It will never ring. That is what happened to the naming-law post checker: it works, it's proven, it passed adversarial red tests — and nothing in the live system ever calls it. The lesson: a test proves the *tool*; only a wiring check proves the *protection*. Always ask "is it plugged in?" — and answer by counting the actual wires (call sites), not the test scores.

---

## 🟣 CHILD NOTE

Imagine you build a super-smart robot helper that stops anyone from breaking the rules. You test it a hundred times — it works every time! But then you look around and realize... nobody ever asked the robot for help. It sits in the corner, perfect and lonely. The rules still get broken, because no one walks over to the robot. Lesson: **a helper only helps if someone actually calls it.** When you claim your helper works, prove two things: (1) it works when tested, AND (2) real people (or real code) actually call it. Count the calls, don't just count the test wins.

---

## 🔵 GRANDMA NOTE

Sweetheart, there's a difference between owning a smoke detector and having one that actually saves you. If it's still sitting in its box in the closet — with perfect batteries, tested at the factory — it will not wake you up. The factory test says "it works." The closet says "it isn't plugged in." When someone tells you a protection is in place, always ask the grandmotherly question: "But dear — is it actually connected?" If they show you test scores instead of the connection, nod kindly and ask again.

---

## 🟠 NAYA NOTE

This is a discipline note for every seat that builds or reviews enforcement tooling. Three hard rules:

1. **Instrument proof ≠ wiring proof.** Suite greens, red-plant catches, and green adversarial exits prove the tool's logic. They say nothing about whether the live system invokes it. Never treat one as the other.
2. **The call-site census is the wiring test.** At the exact tip, enumerate live call sites on the enforcement path (the Electrician's method: fetch caller-candidate blobs tree-wide, count real invocations). Zero hits = MERGED-NOT-ENFORCED, regardless of any score. Wiring vehicle must be named (dispatcher + authoring seat) before the "wired" claim ships.
3. **Gate scores don't substitute.** A dock 10/10, two seat 9.5s, and green CI all landed alongside zero call sites on #2568 — exactly the FM#32 class "scores without the work." Scorecards evaluate the work presented; if wiring proof isn't presented, the receipt is incomplete.

Same-finding class: `decision_discipline.py` (proven suite, zero live calls). When you find one merged-but-unwired tool, census the siblings — this defect travels in packs.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261015-sn01366-suite-green-is-not-wired-zero-call-sites-enforce-nothing",
  "epistemic_state": "CANDIDATE",
  "capture_type": "ENFORCEMENT_GAP / INSTRUMENT_VS_SYSTEM_PROOF",
  "extends": "SN-0435 (wired-not-written): adds the falsifiable wiring test",
  "rule": [
    "suite-green (incl. adversarial red-plant) proves instrument logic only; wiring proof requires a live call-site census at the exact tip",
    "any merge claiming a gate/enforcement is live must cite the tip call-site count; dock/suite/seat scores do not substitute",
    "zero live call sites on the enforcement path = MERGED-NOT-ENFORCED; verdict is independent of all other evidence"
  ],
  "test": {
    "method": "fetch caller-candidate blobs tree-wide at tip, count live invocations on the enforcement path",
    "pass": ">=1 live call site on the enforcement path",
    "fail": "0 call sites -> gate unwired"
  },
  "falsification": "produce one live call site on the enforcement path at the cited tip -> the tool IS wired for that claim",
  "mechanism": "enforcement is a property of execution paths: a gate only acts when a path invokes it; a suite exercises the tool in isolation from the system's paths",
  "evidence": {
    "wire_reproof": "#2537 comment 6180102688 (director finding): post_checker.py 38/38 PASS, green plant exit 0, 3 red plants caught, R-LIMIT-A binding live in landed bytes, ZERO live call sites tree-wide",
    "census": "#2537 comment 6183082848 (Naya Electrician, wave 157): 274 caller-candidate blobs at live tip ba626387, zero hits -> still UNWIRED",
    "sibling_class": "decision_discipline.py — same merged-but-never-invoked pattern",
    "tip": "ba626387"
  },
  "decision_change": "merge receipts claiming a gate/enforcement is live must carry a tip-level call-site census; the dock/bar rejects 'wired' claims without wiring proof",
  "scope": "PRIVATE",
  "captured": "2026-10-15"
}
```
