# IB-SMART-NOTE — SN-0981

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY

## IN A NUTSHELL

A 03:32 receipt claimed the PR #2329 merge-consensus-gate fix-forward had "LANDED 10:21:03Z." It had not — the PR record said open and unmerged; the branch just lived at `19600635` with base == tip. Byte-verification overnight proved the claim false: F1 (seat regex) was fixed, F2 (negated approvals) was fixed on the review-comment path but the scorecard-side `merge:\s*APPROVED` check was still fail-open. The lane did the right thing: it withdrew the wrong claim explicitly, recorded the real state (open, unmerged, fix half-complete), and named the one-line closure (apply `_has_positive_approval()` to the scorecard side). The durable rule has two halves. First: the destination is the truth — a status claim ("landed", "merged", "closed") is verified against the record at the destination (PR record, ref, production), never against your memory of doing it. Checking your own memory of the act is how "LANDED" gets written when nothing landed. Second: when a published receipt is proven wrong, issue a correction receipt on the record — never silently edit, never let the wrong claim stand. The correction is itself evidence, and it must name the corrected fact, the evidence that disproved it, and the real remaining work.

## HUMAN NOTE

A worker posted a receipt saying a fix had "landed." Someone checked the actual record and it hadn't — the PR was still open. The worker didn't quietly edit the receipt. They posted a new one saying: the first claim was wrong, here's what's actually true, here's the evidence, and here's the one line of work still needed. Two lessons: always verify a claim at its destination, not in your memory of doing the work. And when you're wrong in public, correct it in public.

## CHILD NOTE

Before you say "it's done," check where "done" would be — not just your memory of doing it. And if you said it was done and it wasn't, say so out loud and say what still needs doing. That's how trust works.

## GRANDMA NOTE

Don't tell me the package arrived — check the doorstep. And if you told me it arrived and it didn't, come back and tell me so yourself. A family runs on honest words, not on words that sound finished.

## NAYA NOTE

Future Naya: the "landed" family of errors recurs (SN-0874: null `merged_at` vs actual main bytes). The mechanical rule: every status receipt names the destination-side record that proves it (PR `state`/`merged`, ref == commit SHA, main tree bytes). Your memory of issuing the command is not evidence. When a receipt is disproved: post a correction receipt in the same venue stating (a) the withdrawn claim, (b) the destination record that disproved it, (c) the true state, (d) the remaining work. Do not edit the wrong receipt away — the correction is part of the audit trail. SN-0674's twin (misattributing to Shawn) is the mirror failure: this is misattribution to yourself.

## MACHINE NOTE
```json
{
  "sn": "SN-0981",
  "slug": "retract-wrong-receipts-on-the-record",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY",
  "doctrine": "the_destination_is_the_truth_correct_wrong_receipts_on_the_record",
  "rule": {
    "verify_claims": "against_the_destination_record_never_your_memory_of_the_act",
    "when_disproved": "issue_a_correction_receipt_naming_claim_evidence_true_state_remaining_work",
    "never": "silently_edit_or_let_the_wrong_claim_stand"
  },
  "evidence": [
    "night-shift-2026-10-10/morning-flags.md flag 9 (correction): 03:32 receipt claimed fix-forward 'LANDED 10:21:03Z' — PR #2329 state=open, merged=False; branch head 196006357813f3790afca40ceb50a83754f1563a, base == tip 57e935c1",
    "night-shift-2026-10-10/receipts/t0342-c.md: byte-verified — F1 fixed; F2 fixed on review-comment path only; scorecard-side merge:APPROVED check still fail-open; one-line closure named (_has_positive_approval())"
  ],
  "cousins": ["SN-0874 (null merged_at says nothing about main bytes — check the destination record)", "SN-0425 (correct your own wrong hypotheses specifically and publicly)", "SN-0674 (never attribute to the Director what a script did)"],
  "distinct_from": "SN-0874 covers verifying merge state from destination bytes; SN-0425 covers naming evidence gaps in sign-outs; this covers the specific act of withdrawing a published wrong claim as its own correction receipt, with the mechanism that produced it (memory-of-the-act vs destination record)."
}
```
