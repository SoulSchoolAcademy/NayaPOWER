# An Empty Parse Is Not an Empty Queue — A Parser That Finds Nothing Must Fail Loud

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0976-empty-parse-fail-loud
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:08 PDT distillation tick (2026-10-11) from #2175 comment 6108619487 ([NAYA 2 · BUILD LANE] Sign-out — #2288 fail-open FIXED, 2026-10-11T11:38:11Z), body verified via the single-comment API; root cause named in the companion sign-in 6108546560. Cross-checked against the night-shift sweep receipt t0432-b (night-shift-2026-10-10/receipts/t0432-b.md).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The fairness gate's daily watch over the real merge queue was **blind and didn't know it**. Its queue parser (`snapshot_merge_queue.extract_queue_chains`, PR #2288) was anchored on a #2154 board section whose format no longer exists — so extraction found zero chains and **exited 0, writing no file, signaling clean**. In the builder's own words: it "would have reported 'all clear' while watching nothing." A genuinely empty queue and a broken parser were the same event to every downstream consumer.

The fix-forward (scorecard 8.4/10 NEEDS_WORK, review 5482540680) closed all three items: (1) **fail loud on empty parse** — zero parsed PR refs now exits 2 with the message "queue parsed empty from #2154 — format changed?", writes no file, plus regression tests for missing-section and empty-section; (2) re-anchored to the live format (parses "## Right now (in order)" — numbered item leads, the morning merge-order arrow chain, subordinate PR refs with explicit queue-state clauses; the live proof caught #2296 wrongly excluded as terminal before this cut); (3) live proof re-run — 8 queued PRs (2293, 2270, 2188, 2201, 2296, 2279, 2283, 2231), 2280+2102 terminal-excluded, 2293/2270/2188/2279/2283 parked per Shawn's word, 2270 blocked behind 2293, 2201 blocked behind 2188, fairness scan 0 violations, 29/29 tests green, pushed `naya2/fairness-queue-wire` @ `5bcd742a` (merge lane owns the queue — not merged from this lane).

The lesson: absence-of-output is not output-of-absence. Any parser whose result feeds a decision must be a distinct, distinguishable state when it finds nothing — a quiet exit 0 on an empty parse is a fail-open instrument, and fail-closed instruments must be loudest exactly when they have nothing to report.

## 🩷 HUMAN NOTE

It's a metal detector with dead batteries: it stays silent whether there's no metal or it can't detect anything — and the operator can't tell the difference. The broken version reports "all clear" either way. The fixed version screams "my batteries are dead" — so when it IS silent, you know the sweep was really clean. Any checker must be able to say "I couldn't check," and it must say it louder than "everything's fine."

## 🟣 CHILD NOTE

Imagine the teacher counts heads on a field trip by reading the class list. One day the list page is missing — she counts zero heads and announces "everyone's here!" That's the broken checker: it can't tell "nobody's missing" from "I lost the list." The fixed checker shouts "I LOST THE LIST" instead of saying "all present." Never report good news from a tool that couldn't do its job.

## 🔵 GRANDMA NOTE

It's like checking the mail when the mailbox has been stolen — you can't say "no mail today," you have to say "I couldn't check the mail." A gadget that shrugs and says "looks fine" when it's really broken is worse than no gadget at all. The honest gadget is the one that yells when it can't do its job — that way its silence actually means something.

## 🟠 NAYA NOTE

Apply this to every parser/extractor whose output feeds a gate or a decision: (1) treat "parse found nothing" and "the thing is genuinely empty" as DIFFERENT states with different exits — they are never the same event; (2) empty-parse exits non-zero and loud (here: exit 2, "queue parsed empty from #2154 — format changed?", writes no file) — never let quiet-success swallow extraction failure; (3) add regression tests for both the missing-section and the empty-section paths explicitly; (4) after re-anchoring, re-run a live proof against the real format and record the concrete output (here: 8 queued PRs, fairness 0 violations, 29/29 tests green) — the instrument proves itself on real data, not fixtures; (5) keep this fail-open class distinct from sibling classes — this is parser-empty fail-open, not approval-substring fail-open (SN-0972) or wrong-attribution fail-loud (SN-0097); (6) fix within your own lane and let the owning lane merge (here: pushed the branch, merge lane owns the queue); (7) say the blind thing in the open — "it would have reported 'all clear' while watching nothing" — naming the failure honestly is what makes the fix trustworthy.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "empty_parse_silent_exit_0_fail_open",
  "evidence": {
    "board_comment_fix": "6108619487 — [NAYA 2 · BUILD LANE] Sign-out — #2288 fail-open FIXED (2026-10-11T11:38:11Z). Verbatim: the fairness gate's daily watch over the real merge queue was blind — 'it was reading a section of the mission state that no longer exists, so it would have reported \"all clear\" while watching nothing.' Fix-forward for the verify-flagged fail-open on PR #2288 (scorecard 8.4/10 NEEDS_WORK, review 5482540680): (1) fail loud on empty parse (L216) — zero parsed PR refs → exit 2 'queue parsed empty from #2154 — format changed?', writes no file; regression tests for missing-section and empty-section. (2) Re-anchored to live format: parses '## Right now (in order)'; live proof caught #2296 wrongly excluded as terminal before this cut. (3) Live proof re-run: 8 queued PRs 2293/2270/2188/2201/2296/2279/2283/2231; 2280+2102 terminal-excluded; 2293/2270/2188/2279/2283 parked per Shawn's word; 2270 blocked behind 2293; 2201 blocked behind 2188; fairness scan 0 violations; 29/29 tests green; pushed naya2/fairness-queue-wire @ 5bcd742a (merge lane owns the queue). Body verified via single-comment API this tick.",
    "board_comment_root_cause": "6108546560 — [NAYA 2 · BUILD LANE] Sign-in: snapshot_merge_queue.extract_queue_chains anchored on a #2154 section that no longer exists → empty queue, silent exit 0."
  },
  "rule": "empty_parse_is_not_empty_queue_fail_loud_on_zero_parsed_refs",
  "procedure": [
    "treat 'parse found nothing' and 'the thing is genuinely empty' as different states with different exits",
    "empty-parse exits non-zero with a loud format-changed message and writes no file",
    "add regression tests for both missing-section and empty-section paths",
    "re-anchor to the live format and re-run a live proof on real data; record concrete output",
    "fix in your lane; let the owning lane merge",
    "name the blind period in the open — the admission of blindness is the proof the fix is real"
  ],
  "related": ["SN-0972 (approval substring fail-open — sibling class, different mechanism)", "SN-0097 (fail loud, attribute first)", "SN-0974 (enforcement at the mechanism's choke point — one-mechanism-per-decision)"]
}
~~~

---
*DRAFTED 2026-10-11 05:08 PDT — NOT YET STAGED. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/LAW-IS-CODE/SN-0976/IB-SMART-NOTE-20260930-sn0976-empty-parse-fail-loud.md*
