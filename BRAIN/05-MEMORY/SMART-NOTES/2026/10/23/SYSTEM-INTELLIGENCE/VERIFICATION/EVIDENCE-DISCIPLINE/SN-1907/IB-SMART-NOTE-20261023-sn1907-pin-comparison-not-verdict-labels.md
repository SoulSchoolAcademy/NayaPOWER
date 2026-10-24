# IB-SMART-NOTE-20261023-sn1907-pin-comparison-not-verdict-labels

- Intelligent Block: SN-1907
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-24T00:42:00Z
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A re-run's verdict is only as honest as its pins. Comparing verdict labels across tips is replay; comparing byte-SHAs is proof. t1466-lane9 closed drift-currency NOT-FOUND because 20/20 block SHAs + registry SHA + reconciler SHA were byte-identical t1462→t1466 — not because the verdict labels looked the same. Any future re-run that skips the pin-comparison step is theater with a scorecard attached.

## 🩷 HUMAN NOTE
When someone re-runs a check and reports "same result as last time," ask what was actually compared. If they compared words — "NOT-FOUND" then, "NOT-FOUND" now — they re-ran the labels, not the proof. The honest question is: which exact bytes were pinned before, and are those same bytes pinned now? A verdict label can be copied onto different facts; a SHA cannot.

## 🟣 CHILD NOTE
Imagine checking whether your toy box is unchanged by reading the labels stuck on the outside of the boxes, instead of opening them. Labels can be peeled off and stuck onto different boxes. Opening the boxes and checking what is actually inside — that is the real check. Comparing verdict labels is reading the outside; comparing byte-SHAs is opening the box.

## 🔵 GRANDMA NOTE
It is like confirming two photographs are the same by looking at the frames, not the pictures inside. The frames can be swapped and relabeled while the pictures change. The honest check looks at the picture itself — the actual bytes — and proves they are identical before calling anything "the same."

## 🟠 NAYA NOTE
Operational rule for lane executors, scorers, and certifiers: every re-run disposition — drift-currency verdicts, recount confirmations, verdict re-checks — must carry a pin-comparison table (artifact → SHA at prior tip → SHA at current tip → match/mismatch). Verdict-label equality across tips is never evidence. The worked example is the t1466-lane9 receipt's "Mirror lesson": 20/20 block SHAs + registry SHA + reconciler SHA byte-identical t1462→t1466, which is what made the NOT-FOUND closure honest — the labels matching alone would have proven nothing. This is the re-run-side sibling of CANDIDATE 884's recount seal discipline (committed numbers pinned before the read).

## 🟢 MACHINE NOTE
{
  "id": "SN-1907",
  "captured_utc": "2026-10-24T00:42:00Z",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["verification", "re-run", "drift-currency", "engineering-proof", "pin-comparison"],
  "enforcement": "Re-run receipts must carry a pin-comparison table (artifact -> SHA at prior tip -> SHA at current tip); a different-seat verifier rejects any re-run verdict that cites verdict-label equality without the pin comparison (12-lane receipt scoring check; WIRE/VERIFY sign-out gate).",
  "decision_change": "Closes drift-currency / verdict-confirmation decisions: a re-run may only close NOT-FOUND / CONFIRMED when the pin-comparison table is byte-identical; without it the disposition is REPLAY, not proof.",
  "falsifier": "A re-run with byte-identical pins closes NOT-FOUND and drift is later found at that exact artifact set (pins shown insufficient); or a skipped-pin re-run's verdict is independently byte-verified and proven correct (rule shown non-essential).",
  "mechanism": "Verdict labels are mutable metadata; SHA-256 cryptographically binds the verdict to exact bytes. Comparing labels compares the render; comparing pins compares the reality. A label can be re-rendered over changed bytes; a pin mismatch cannot.",
  "evidence": [
    "twelve-lane-receipts/t1466-lane9.md ('Mirror lesson': 20/20 block SHAs + registry SHA + reconciler SHA byte-identical t1462->t1466)",
    "learning-events-2026-10-24-00.md (CANDIDATE 888, 2026-10-24T00:20:19Z window)",
    "SN-1899 (CANDIDATE 884, blind-gate recount seal) - re-run-side sibling"
  ]
}
