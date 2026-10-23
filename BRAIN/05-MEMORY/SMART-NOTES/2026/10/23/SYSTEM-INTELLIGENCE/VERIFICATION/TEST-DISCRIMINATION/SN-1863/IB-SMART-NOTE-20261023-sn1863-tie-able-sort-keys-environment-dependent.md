Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A "newest" selector whose sort key is date-only ties on every sibling born the same day — and the tie silently resolves to directory-entry order, which readdir does not guarantee. WIRE 05:00Z reproduced it first-hand: #2975's `newest_sibling` flipped on directory-entry order, and L646 [F2] was promoted the same tick: **a tie-able sort key is environment-dependent; selection that must be stable needs a total order.** The durable rule: any selector that picks one winner must order all the way down (no unbroken ties), and its test suite must permute directory-entry order and assert the winner doesn't move. A selector that can't name its tie-breaker isn't selecting — it's inheriting the filesystem's mood.

## 🩷 HUMAN NOTE

Shawn — the wiring lanes caught a selector that picks "newest" by date alone. When two entries share the date, the pick falls back to the order the filesystem happens to list the directory — which isn't a contract, it's luck. Same input, different answer, depending on where the disk put things. The fix is a total order (break every tie deterministically) plus a test that scrambles directory order and confirms the winner holds. The principle: if the sort can tie, the machine must still be able to point at exactly one winner — never leave the last word to the filesystem.

## 🟣 CHILD NOTE

Imagine picking the "tallest kid" but your ruler only marks whole inches, and two kids are both "this tall." You say "the one who walked in first" — but walking-in order changes every day. So the "tallest" changes too, and you didn't actually pick by height. The fix: make the ruler finer (add another measure until nobody ties) and then shuffle the walking-in order to prove the answer stays the same.

## 🔵 GRANDMA NOTE

It's like picking the "newest recipe card" when you only dated them by year — three cards from 2021, and you grab whichever is on top of the pile. Shake the pile and you grab a different one. You haven't picked the newest; you've picked whatever was on top. The fix is to date every card to the day — and if two still match, decide by a coin you flip the same way every time, and then shuffle the pile to prove it.

## 🟠 NAYA NOTE

Seats write selectors constantly — newest, current, latest — and a date-only key is the most natural thing in the world. The poison is quiet: it works in every test because the test directory has one winner per key, then flips in production where siblings tie. The discipline is mechanical, not careful: every selector gets a tie-breaker chain that terminates in something total (name, inode, a salted hash of the full path), and the fixture suite includes a permuted-entry-order run. If the winner moves under permutation, the selector is broken — not unlucky. Treat "works on my machine" selection as guilty until proven order-independent.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1863-tie-able-sort-keys-environment-dependent",
  "lesson": "A selector with a tie-able sort key (date-only 'newest/current') is environment-dependent: ties resolve to directory-entry order, which readdir does not guarantee, so the same input yields different winners on different machines or after readdir reshuffles. Any selector that must be stable needs a TOTAL order — a tie-breaker chain that terminates in something deterministic — plus a permuted-entry-order test proving the winner doesn't move.",
  "applies_when": ["test", "order-dependence", "claim", "lane-executor", "wire", "suite-red", "selector", "newest-current"],
  "enforcement": "The selector's regression suite carries a permuted-directory-entry-order fixture (scramble readdir order, assert the selected winner is unchanged); CI refuses any 'newest'/'current' selector whose key can tie without a documented total tie-breaker chain. WIRE's re-name pass is the live backstop: a flip across entry order names the selector as the failure class.",
  "evidence": [
    "board comment 6357750649 (WIRE 05:00Z sign-out, 2026-10-23T04:58:39Z — L646 [F2] promoted: 'newest/current selection with tie-able sort key is environment-dependent (_sort_key date-only, siblings tie -> directory-entry order); rule: total order + permuted-entry-order test')",
    "board comment 6357854502 (VERIFY 05:00Z sign-out, 2026-10-23T05:07:02Z — '#2975 reproduces guard fragility first-hand (newest_sibling flips on dir-entry order)')",
    "shared-state.json director_tick_20261023_0508 moves: 'LEARNING L646 [F2] NEW FILING promoted'"
  ]
}
```
