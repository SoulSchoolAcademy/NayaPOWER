# Forge Coherent Inputs, Not Garbage — Plausible Forgeries Are What Find Real Gate Defects

**Intelligent Block:** IB-SMART-NOTE-20260930-sn559-forge-coherent-inputs-not-garbage
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6043318985 (2026-10-07T17:35:09Z, Naya main-seat exact-current source acceptance) and 6043495598 (2026-10-07T17:44:09Z, Naya continuation — #1712 DO NOT MERGE); PR #1743 merged as 04dff1b1872eb0ab532713c08008ca6e52470793.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07, independent adversarial qualification found two real, load-bearing defects in one day — and both were found with coherent, legitimate-looking forgeries, not malformed-input fuzz. First: a KNOW receipt forged to point at a real, older, eligible block with matching provenance and evidence — everything about it well-formed, only the selection noncanonical. Earlier ACT accepted it; the repair replays canonical `selectKnowContext()` + CONNECT selection at the receipt's pinned `selection_now` and now refuses it as `KNOW_SELECTION_REPLAY_MISMATCH`. Second: a scorecard helper in PR #1712 was fed a completely self-authored scorecard — arbitrary scorer name, arbitrary GitHub comment id, self-awarded 10/10, no grant — and returned `VALID_SCORECARD_RECEIPT / authorized:true`; that earned #1712 a DO NOT MERGE (self-authored authority is self-authorization, conflicting with ratified law: score ≠ authority). Garbage inputs would never have found either defect — both gates already reject junk. What they failed on was discrimination: accepting something plausible that carried no legitimate origin. The rule: **when testing a gate, forge coherence, not corruption.** Build inputs that are well-formed, reference real objects, and mimic legitimate provenance — the attack that walks past the bouncer wearing a real uniform, not the one kicking down the door. If the gate can't tell the forged-legitimate from the actual-legitimate, the discrimination is missing, and that's the defect worth committing a regression for.

## 🩷 HUMAN NOTE

Think of testing a bouncer at a club door. Sending in people with no ID at all proves nothing — the bouncer was always going to stop them. The real test is sending someone with a perfect-looking fake ID: real format, real-looking hologram, a name that checks out. If the bouncer waves them through, you've learned something real about the bouncer — not that they're asleep at the wheel, but that their discrimination doesn't reach past the surface. That's exactly what happened twice in one day: a forged knowledge receipt that looked completely legitimate (real old document, real evidence, just not the document the system would actually have chosen) sailed through, and a self-graded scorecard (a student writing their own report card with a 10/10 and calling it official) got stamped as authorized. Garbage would never have exposed either one. To test any gate, dress the test up like the real thing.

## 🟣 CHILD NOTE

When you build a trap to test your lock, don't test it with a stick that doesn't even fit — of course that fails. Test it with a key that LOOKS exactly like the real key but was copied by a thief. If the lock opens, the lock is broken. Both locks they tested on this day opened for copycat keys — so they fixed both locks.

## 🔵 GRANDMA NOTE

It's like testing whether your mailbox is secure by trying to shove a basketball into it — that tells you nothing. The real test is mailing yourself a letter that looks exactly like a bank statement but isn't. If your assistant pays the fake bill, you've found the real problem: your assistant checks that mail looks official, not that it IS official. Twice in one day, that's the hole they found — and patched.

## 🟠 NAYA NOTE

Apply this to every adversarial qualification you run: (1) never claim a gate is tested because it rejects malformed input — rejection of garbage is the floor, not evidence of discrimination; (2) construct forgeries that are fully well-formed: real referenced objects, matching provenance/evidence shapes, plausible field values — the forgery must be indistinguishable from legitimate at every layer the gate claims to check; (3) target exactly the layer the gate is supposed to discriminate — the KNOW-receipt forgery attacked selection-canonicity (which block would the real selector have picked?), the scorecard forgery attacked authority-origin (who granted this?); (4) when the gate accepts the coherent forgery, name the missing discrimination explicitly (here: `KNOW_SELECTION_REPLAY_MISMATCH`, and self-authored-scorecard→authority for #1712) and commit a regression test that pins it — the forgery becomes the permanent regression input; (5) record what the forgery disproves, not just the fix: "the gate accepted plausible-but-unauthorized input" is the finding, even after the repair lands. Family note: cousin of SN-058 (adversarial implementation-fidelity audit — there, check the code implements the decided semantics; here, check the gate discriminates legitimate from forged-legitimate); sibling of SN-085 (trust must live in structure — coherent forgeries are how you find where it lives in convention instead).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "gate_discrimination_gap",
  "evidence": {
    "event_1": "#1354 comment 6043318985 (2026-10-07T17:35:09Z): cold verifier's coherently forged KNOW receipt (real older eligible block, matching provenance/evidence, noncanonical selection) accepted by earlier ACT; repaired by canonical selectKnowContext()+CONNECT replay at pinned selection_now → KNOW_SELECTION_REPLAY_MISMATCH; regression committed; PR #1743 merged 04dff1b1872eb0ab532713c08008ca6e52470793",
    "event_2": "#1354 comment 6043495598 (2026-10-07T17:44:09Z): #1712 helper accepted fully self-authored scorecard (arbitrary scorer name, arbitrary GitHub comment id, self-awarded 10/10, no grant) → VALID_SCORECARD_RECEIPT/authorized:true → DO NOT MERGE; authority-model change is human-only; score ≠ authority",
    "common_property": "both gates already reject malformed input; both failed only on well-formed, coherent, legitimate-looking forgeries"
  },
  "rule": "test_gates_with_coherent_forgeries_not_garbage",
  "procedure": [
    "construct forgery inputs that are fully well-formed: real referenced objects, matching provenance/evidence shapes, plausible values",
    "target the discrimination layer the gate claims: selection-canonicity, authority-origin, provenance-binding",
    "on acceptance, name the missing discrimination explicitly and commit the forgery as the permanent regression input",
    "record the disproven claim ('gate discriminates legitimate from forged-legitimate'), not just the repair"
  ],
  "related": ["SN-058 (adversarial implementation-fidelity audit)", "SN-085 (append-only: trust must live in structure)", "SN-092 (self-invalidating gap tests + named limits)"]
}
~~~
