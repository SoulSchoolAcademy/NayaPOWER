# Equality on a Count Is a Promise About the Future

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1788-equality-on-a-count-is-a-promise
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1788

## ✦ IN A NUTSHELL

A count-equality assertion (`== 9`) pins a set's size in *both* directions — but sets grow. When the set legitimately gains a member, the assertion lies and the fix looks like the bug. Assert the bound plus per-member presence (`>= 9` plus every expected member present) instead of exact equality. Two companion rules from the same fix: failure-masking `exit 0` out-of-scope paths become explicit PASS-flag semantics, and every failure row gets a named owner or an explicit route.

## 🩷 HUMAN NOTE

On 2026-10-21 the t1422 fixes landed three test-design rules in one sitting. First: count-equality assertions are drift-bait — `== 9` breaks the moment the set legitimately becomes 10; the durable form asserts the lower bound AND per-member presence (`>= 9` plus a membership check for each expected member), which tolerates growth while still catching shrinkage and loss. Second: out-of-scope paths that silently `exit 0` mask real signal — replace them with explicit PASS-flag semantics so "passed" and "not applicable" are distinguishable in the output. Third: every failure row gets a named owner or an explicit route — an unowned failure row is a finding that will be re-filed forever instead of fixed. (Evidence: hidden_files/lesson-broadcast.md — [night-dispatcher t1199, 2026-10-21T22:12Z] "t1422 fixes".)

## 🟣 CHILD NOTE

Imagine you count your toy box and write on a sign: "EXACTLY 7 toys." Then grandma gives you a brand-new toy. Now your sign is wrong — but the toy isn't broken! The sign was. Writing "at least 7 toys, and here is the list of the 7" would have stayed true. Tests work the same way: don't demand an exact number when the box is allowed to grow.

## 🔵 GRANDMA NOTE

It's like writing in the family bible: "I have exactly 3 grandchildren." Then the fourth one arrives — a blessing, dear! — and your beautiful inscription is suddenly wrong. You wouldn't call the baby a mistake; the inscription was too strict. Write "at least 3, and here are their names" and the book stays true no matter how the family grows. And when something does go wrong, write down whose job it is to fix it — a problem with nobody's name on it is a problem that never gets solved.

## 🟠 NAYA NOTE

The operating rule, step by step.

**Step 1 — Ask whether the set is frozen or growing.** If the set's membership is contractually fixed by spec (the 9 nodes, the 4 gates), exact equality is honest. If the set can legitimately grow (members, rows, briefs), exact equality is drift-bait.

**Step 2 — Assert bound + presence, not equality.** For growing sets: `count >= N` AND a per-member presence check for every expected member. This catches shrinkage and loss (the real failures) while tolerating legitimate growth.

**Step 3 — Make out-of-scope explicit.** Any path that today silently `exit 0`s becomes an explicit PASS flag with a reason. "Passed" and "not applicable" must never share a code.

**Step 4 — Name the owner or the route.** Every failure row in any report carries either a named owner's seat or an explicit route (a ticket, a brief, a lane). A row with neither is a finding scheduled to be re-filed, not fixed.

**The trap it defeats:** `== 9` reads as precision; on a growing set it is a bet that the future looks exactly like today. The failure it produces on growth looks like a real regression and sends the next seat hunting a bug that doesn't exist.

## 🟢 MACHINE NOTE

```json
{
  "id": "SN-1788",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-21",
  "applies_when": ["testing", "assertions", "harness", "drift"],
  "enforcement": "The test/harness review gate rejects count-equality assertions (`== N`) on non-contractually-frozen sets — the reviewer names the freeze contract or the assertion becomes bound+membership. Every failure row in a filed report is rejected at filing unless it carries a named owner or an explicit route.",
  "evidence": ["hidden_files/lesson-broadcast.md [night-dispatcher t1199, 2026-10-21T22:12Z] t1422 fixes: count-equality assertions (`== 9`) are drift-bait — assert the bound + per-member presence; failure-masking `exit 0` out-of-scope paths become explicit PASS-flag semantics; every failure row gets a named owner or an explicit route"],
  "falsifier": "A set whose membership is contractually frozen by spec (fixed by law, not by today's data) — there `== N` is exact and correct, and the rule explicitly does not apply. That exception clause is part of the rule, not a hole in it.",
  "mechanism": "Set growth is the expected drift direction; equality pins both directions, so legitimate growth reads as regression. Bound+membership tolerates the expected drift direction while still catching shrinkage and member loss — the actual failure modes. Unowned failure rows get re-filed because no seat's attention is priced in.",
  "cousins": ["CANDIDATE 108 (drift gets a named owner, never silent absorption)", "CANDIDATE 663 (a finding that only gets re-filed is a finding that got buried — needs an owner, not another receipt)"]
}
```
