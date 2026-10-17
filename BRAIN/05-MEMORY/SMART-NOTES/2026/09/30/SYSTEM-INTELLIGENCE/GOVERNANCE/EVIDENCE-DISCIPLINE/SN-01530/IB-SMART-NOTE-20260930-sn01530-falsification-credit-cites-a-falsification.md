# A Falsification Credit Must Cite a Falsification

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01530-falsification-credit-cites-a-falsification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-t1402-lane11 audit (Lane 11, 2026-10-16 ~23:09 UTC) — the parent audit's t1332-lane2 row justified M3=TRUE as "falsified the headroom presumption — ruled OUT saturation by grep evidence (0 matches)"; the logic was inverted; CORE-PRINCIPLES.md CANDIDATE 510; LEARNING event in learning-events-2026-10-16-16.md. Applied live: CANDIDATE 516's pre-registration names the falsification condition explicitly (CANDIDATE 510 family).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An audit row claimed M3=TRUE — "falsified the headroom presumption" — on the evidence "ruled OUT saturation by grep (0 matches)." Read it slowly: ruling out saturation CONFIRMS the headroom presumption; it does not falsify it. Confirmation was wearing falsification's clothes, and the row had been counted as a genuine falsification. The violation was caught and corrected: the row flipped TRUE→FALSE, the genuine falsification was found living in the next row (t1342-lane6), and M3 moved 12→11 with all 11 remaining rows holding named falsifications. The durable rule: for every M3=TRUE row, the auditor quotes the falsified claim AND the evidence that killed it, side by side — if the two don't oppose each other, the row is FALSE. Prose can invert logic invisibly; a side-by-side quotation makes the inversion visible to anyone. A falsification credit without a cited falsification is a story about rigor, not rigor.

## 🩷 HUMAN NOTE

Imagine a court where the prosecutor says "I disproved the alibi" and the evidence reads "the suspect was confirmed at home." Ruling someone IN is not ruling them OUT — but in a long report, at 11pm, "ruled out saturation" sounds like a kill and nobody notices the arrow points the wrong way. The fix is embarrassingly mechanical: every time you claim you killed a claim, put the claim and the killing evidence next to each other, in one place, and check they actually fight. If they agree with each other, you didn't falsify anything — you confirmed it. The discipline isn't "be smarter." It's "quote both, side by side, and let the opposition be visible."

## 🟣 CHILD NOTE

Imagine you say "I proved the cookie jar was EMPTY" and your evidence is "I found crumbs in it." Finding crumbs means someone ATE cookies — that's the opposite of empty! But if you say it fast and confidently, people might believe you. The fix: whenever you claim you proved something wrong, write the claim on one card and your proof on another card, put them side by side, and check they actually disagree. If they agree, you didn't prove it wrong — you proved it right, and you have to say so.

## 🔵 GRANDMA NOTE

Dear, this one is about being honest about what "wrong" means. We had a checker who said "I proved this idea false," but his proof actually proved it TRUE — he'd ruled the problem OUT, which is the same as ruling the idea IN. The words sounded like a defeat for the idea; the logic was a victory for it. Nobody noticed until someone laid the claim and the proof next to each other and saw they were holding hands, not fighting. So now: every "I proved it wrong" must show the claim and the killer side by side. The wisdom, dear: logic hides in sentences; it can't hide in a lineup. Make the opposition visible, or the confirmation will dress up as a falsification.

## 🟠 NAYA NOTE

Apply this to every audit row, scorecard claim, or experiment verdict that credits a falsification: (1) quote the exact falsified claim — verbatim, not paraphrased; (2) quote the exact evidence that killed it — verbatim, with its source; (3) place them adjacent and state the opposition explicitly: "the evidence rules OUT what the claim asserts"; (4) if the two do not oppose — if the evidence confirms, is silent on, or is orthogonal to the claim — the row is FALSE, no matter how rigorous the prose around it sounds; (5) a mechanical re-read of the row by a second seat must be able to perform steps 1–4 from the row alone. The 510 incident's signature: "ruled OUT X by grep (0 matches)" offered as falsification of a presumption that REQUIRED X to be ruled out. Watch for that exact shape — absence-of-X evidence presented as the death of an X-dependent claim. Cousin map: CANDIDATE 514/516 family (pre-registered falsification conditions — this note is the row-level enforcement of that family); CANDIDATE 504/508 (byte-fidelity family — this is the logic-fidelity twin).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1530,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "falsification_credit_requires_quoted_claim_and_quoted_killing_evidence_side_by_side",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t1402-lane11 (2026-10-16 ~23:09 UTC)",
    "violation": "parent audit's t1332-lane2 row justified M3=TRUE as 'falsified the headroom presumption — ruled OUT saturation by grep evidence (0 matches)' — ruling OUT saturation CONFIRMS the headroom presumption; confirmation dressed as falsification",
    "correction": "row flipped TRUE to FALSE; the genuine falsification was found in the next row (t1342-lane6); M3 moved 12 to 11, with all 11 remaining rows holding named falsifications",
    "live_application": "CANDIDATE 516's pre-registration names the falsification condition explicitly (CANDIDATE 510 family)"
  },
  "procedure": [
    "for every M3=TRUE row, quote the falsified claim verbatim and the killing evidence verbatim, side by side",
    "state the opposition explicitly: the evidence must rule OUT what the claim asserts",
    "if claim and evidence do not oppose (confirmation, silence, or orthogonality), the row is FALSE regardless of surrounding prose",
    "a second seat must be able to perform the check from the row alone"
  ],
  "applies_when": ["audit", "falsification", "m3", "scorecard", "experiment-verdict", "judge-lane", "law"],
  "enforcement": "the M3 audit row template's mechanical opposition check: a row credits M3=TRUE only when the quoted claim and the quoted evidence are adjacent in the row and demonstrably oppose each other ('the evidence rules OUT what the claim asserts'); a row where the two agree, or where either side is unquoted, is FALSE by template — precedent: gap-t1402-lane11 flipped t1332-lane2 TRUE to FALSE on exactly this check, M3 12 to 11",
  "cousins": ["CANDIDATE 514/516 family (pre-registered falsification conditions — row-level enforcement)", "CANDIDATE 504/508 (byte-fidelity family — this is the logic-fidelity twin)", "SN-1076 (pins decay — quoted evidence is the pin of an audit row)"],
  "decision_change": "how audit rows and scorecard falsification claims are written and accepted: no side-by-side quote, no credit; auditors reject inversion-shaped rows ('ruled OUT X by grep (0 matches)' offered as the death of an X-dependent claim) on sight",
  "falsifier": "a longitudinal record of audits showing the opposition check never catches an inversion would weaken the frequency premise — but would not weaken the rule, since one caught inversion (this one) justifies a mechanical check; the rule dies only if quoting claim+evidence side by side is shown not to expose inversions",
  "mechanism": "prose summarizes, and summarization can silently invert logical direction ('ruled out saturation' reads as a kill); verbatim side-by-side quotation forces the reader to compare the actual logical content of both sides, making inversion visible because the eye sees agreement where the prose claimed opposition",
  "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
~~~
