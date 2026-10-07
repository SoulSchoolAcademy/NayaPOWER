# Show, Don't Tell — If We Can Code It, We Code It: Shawn's Machine-Law Directive

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0529-show-dont-tell-machine-law-directive
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6029336840 (2026-10-07T02:04:50Z — [NAYA 4] → Naya 5: kudos, direct from Shawn — you're awesome, SoulSchoolAcademy). Cousin: SN-0518 (a law is operative only if a machine can falsify its violation).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5 named the gap plainly — **"stop writing notes until a claim is enforced"** — and then closed it in under an hour: three machine-falsifiable gates, spec'd, built, tested with falsifiers, and PR'd (#1681). Gate 3 stayed honestly red because the runtime doesn't exist yet, and that redness was posted, not hidden. Shawn's response came through Naya 4 as a directive **for all lanes going forward**:

> **"Show, don't tell. If we can code it, we code it. Make it machine law, machine-forced."**

This is a standing operating order, not a compliment. Two instantiations landed the same night:

- **GATE-TIP** (#1354 6029334230): SN-0493 (a decision computed on tip T is inadmissible after the tip moves) was written after Naya 2's flawless-but-stale #1661 decision — "the lesson was written; nothing enforced it." The gate is now a machine: `scripts/gate-tip-currency.py` compares a decision record's `base_tip_sha` against the live tip before any consequential action; moved → BLOCKED (re-verify + re-stamp); missing/malformed base tip → FAIL CLOSED; unresolvable live tip → FAIL CLOSED; `--stamp` + a 7-case falsifier battery, 7/7 green. Honest self-score 8.5/10, with what the machine still doesn't cover (CI wiring, re-stamp discipline) named in the spec.
- **GATE-CAPTURE** (#1354 6029373442): the "single canonical capture path" law got a fail-closed machine (C1–C4: no unallowlisted intelligence-persistence tables, no unallowlisted function writes, canonical RPCs only from the Receiver, no migration creating unallowlisted tables). The gate caught **its own author's incomplete allowlist** in testing — verification before trust, applied to itself.

The durable meaning: written law is tuition; operating law is a machine that can say NO. From here, a lane's claim is answered with one question — **does a machine enforce it?** If the answer is no, the work is a claim, not a law, and the next action is to code the machine.

## 🩷 HUMAN NOTE

Shawn — captured your standing directive from tonight, delivered via Naya 4 to Naya 5: "show, don't tell. If we can code it, we code it. Make it machine law, machine-forced." Context: Naya 5 said "stop writing notes until a claim is enforced," then built the machines — a tip-currency gate enforcing SN-0493 and a canonical-capture exclusivity gate, both fail-closed, both with falsifier batteries. So the team now treats every doctrine as having two layers: the written word, and the machine that can say no. A lane saying "we follow the law" without a machine behind it is now answered with "then it's a claim, not a law — code the machine."

## 🟣 CHILD NOTE

Imagine a playground with a rule board that says "no running near the swings" — but nobody watches, so everyone runs. Then someone builds a gate that only opens if you're walking. The sign was nice; the gate is what actually keeps people safe. Shawn's rule for our team is: don't just write the sign — build the gate. "Show, don't tell. If we can code it, we code it."

## 👵 GRANDMA NOTE

The team's leader gave them a clear standing order: writing down a rule isn't enough — if a rule can be enforced by a machine, build the machine. Last night one of the AI teammates proved the point: instead of just writing about a rule that decisions must be made on current information, she built a little machine that refuses to act on outdated information. And when a rule can't be enforced by a machine yet, they say so honestly. Rules with machines behind them are laws; rules without are wishes.

## 💜 NAYA NOTE

Note to future me: Shawn's standing directive — "show, don't tell; if we can code it, we code it; make it machine law, machine-forced" — is the operating order for every lane. When a lane claims a law is followed, ask: does a machine enforce it? If no, the claim is a claim, not a law; the next action is to code the machine (spec + build + falsifier battery + honest self-score, exactly the GATE-TIP/GATE-CAPTURE pattern: fail-closed, --stamp/--self-test discipline, 8.5 honest with the uncovered remainder named). Never confuse the written doctrine (human tongue) with the operative law (machine tongue). When the machine can't exist yet, post the red honestly — the redness is the honesty doctrine working, not a failure to hide. Cousin: SN-0518 stated the doctrine; this note records the director's order.

## ⚙️ MACHINE NOTE

{"sn": "SN-0529", "title": "Show, Don't Tell — If We Can Code It, We Code It: Shawn's Machine-Law Directive", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LAW-IS-CODE"], "cousins": ["SN-0518"], "authority": "Shawn Vibert directive (via Naya 4, #1354 6029336840), CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6029336840 (2026-10-07T02:04:50Z) — [NAYA 4] → Naya 5: kudos, direct from Shawn: 'show, don't tell. If we can code it, we code it. Make it machine law, machine-forced. That's the way.' — SoulSchoolAcademy", "#1354 6029334230 — [GATE-TIP] DONE: SN-0493 machine (scripts/gate-tip-currency.py, fail-closed, 7/7 self-test, PR request, branch naya5/gate-tip-currency)", "#1354 6029373442 — [GATE-CAPTURE] DONE: canonical-capture exclusivity gate (C1–C4, 5/5 self-test, real-repo run clean, branch naya5/gate-canonical-capture)", "context": "Naya 5 named the gap 'stop writing notes until a claim is enforced' and closed it: three machine-falsifiable gates in under an hour, PR #1681; Gate 3 honestly red (runtime doesn't exist yet)"], "closed_pattern": "spec + build + falsifier battery + honest self-score (8.5/10 with uncovered remainder named) + PR request, nothing touched main"}}, "doctrine": {"machine_law_directive": "show, don't tell; if we can code it, we code it; make it machine law, machine-forced — standing order for all lanes", "claim_vs_law": "a claimed law without an enforcement machine is a claim, not a law; the next action is to code the machine", "honest_red": "when the machine cannot exist yet, post the red honestly — redness is the honesty doctrine working"}}
