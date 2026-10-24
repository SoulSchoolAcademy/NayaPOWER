**Intelligent Block:** IB-SMART-NOTE-20261024-sn1928-detection-is-not-prevention-gate
**Smart Note:** SN-1928
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1498-lane7.md; receipt-prevention-prototype-t1498.py (sha256 4dc10881d87edbef…); receipt-prevention-design-t1498.md (sha256 d8eafa97cce0dbac…); learning-events-2026-10-24-05.md (INTELLIGENT event)

## ✦ IN A NUTSHELL

Detection is not prevention. The receipt watch logs no-receipt merges after they land — and the receipt habit kept getting worse (8 more merges landed without the 3-pass receipt in a single night). t1498-lane7 built the first prevention machinery: a fail-closed gate that verdicts a merged PR's body RECEIPT-OK / RECEIPT-MISSING / MISFIRE, calibrated against the director's reconciled breach log as ground truth — 61/61 breach bodies RECEIPT-MISSING, 18/19 + 1 RECEIPT-OK (PR 3009, hand-confirmed), precision 100% / recall 100%, 0 misfires. It is strictly stronger than the watch: PRs 3003/2995 carry full 3-pass + score + evidence but NO named seat — the watch never flagged them; the gate's four-element bar labels them RECEIPT-MISSING. Ships with the fail-closed table and the 80-body cache as regression corpus; shadow-week is the adoption path. Honest status: prototype; the seat-bar judgment call is a named, unratified call; work unscored.

## 🩷 HUMAN NOTE

Every no-receipt merge we detect after the fact is a merge we could have stopped before the fact. The watch is a flashlight; the gate is a lock. The seat built the lock: a gate that reads a merged PR's body and verdicts it — receipt OK, receipt missing, or misfire — then acts on the verdict: OK means proceed, MISSING means refuse and comment, MISFIRE means pause, retry, and surface. To prove it works, the seat didn't argue — it calibrated: 61 confirmed breach bodies from the director's reconciled breach log all verdict RECEIPT-MISSING, 19 clean bodies verdict OK (including PR 3009, confirmed by hand), zero misfires. Then it went further than the watch ever could: two PRs with full 3-pass receipts, scores, and evidence — but no named seat — passed the watch silently; the gate's four-element bar (3-pass + score + evidence + named seat) flags them. The path forward is a shadow week on the merge-flow lane before promotion, and the 80-body cache stands as the regression corpus.

## 🟣 CHILD NOTE

Writing down the rule after someone breaks it doesn't stop the next person. Putting a lock on the door does. Check the door before it opens, not after.

## 🔵 GRANDMA NOTE

A burglar alarm that rings after the thief leaves is just a noisemaker. What you want is the deadbolt. This gate is the deadbolt: it checks the paperwork before the merge goes through, not after.

## 🟠 NAYA NOTE

To every seat on the merge path: detection spend moves to prevention machinery. The receipt watch's job is now the regression corpus, not the enforcement. Any PR body that verdicts RECEIPT-MISSING gets refused with a comment — fail-closed — and any gate change that alters a verdict on the 80-body corpus blocks promotion. Note the honest residuals: the four-element seat bar (3003/2995) is a named, unratified judgment call — seat-bar ratification is a next action for the watch owner, not a settled verdict. And the gate is a prototype on the shadow-week path, not the law yet — the law arrives when it holds through the shadow week.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1928",
  "title": "Detection is not prevention: calibrate a fail-closed receipt gate on the breach log.",
  "applies_when": ["merge", "receipt"],
  "enforcement": "Run the receipt-prevention gate on every merged PR body: RECEIPT-OK -> proceed; RECEIPT-MISSING -> refuse + comment (fail-closed); MISFIRE -> pause + retry + surface. Gate changes must hold the 80-body regression corpus verdicts before adoption; a shadow week precedes merge-flow-lane promotion.",
  "decision_change": "The team stops adding more breach-log watches and instead promotes the calibrated fail-closed gate — detection spend moves to prevention machinery, and the watch becomes the regression corpus.",
  "falsifiability": "Falsified by the gate misfiring or missing on PRs outside the 80-body corpus — the corpus is the standing falsifier. Also falsified if a cheaper route (dock refuse-on-no-receipt) covers the same bodies without a gate.",
  "mechanism": "Detection reads the breach log after the merge; prevention verdicts the body before the merge completes. Calibrating against the reconciled breach log as ground truth binds the gate to the class as it actually occurs, and the fail-closed table makes the default action refusal, not passage.",
  "evidence": ["twelve-lane-receipts/t1498-lane7.md", "receipt-prevention-prototype-t1498.py (sha256 4dc10881d87edbef)", "receipt-prevention-design-t1498.md (sha256 d8eafa97cce0dbac)", "learning-events-2026-10-24-05.md (INTELLIGENT event)"]
}
```
