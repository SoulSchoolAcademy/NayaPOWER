# SN-1837 — A First-Parent Scan Cannot See a Second Parent

Intelligent Block: SN-1837
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (10:38 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A merge commit brings its whole second parent's subtree into main's ancestry — but a first-parent-line scan never looks there. A guardian that verifies main by walking only the first-parent line can call main clean while direct-push-class commits sit in its ancestry, absorbed through a merge's second parent. The verification must run two checks: the compare-ancestor check AND the first-parent-line check.

## 🩷 HUMAN NOTE

On 2026-10-22 at 17:09Z, the Post-Merge Guardian raised a direct-push alert (board #2793, comment 6346622009) that flipped two checks NEW_RED: promote-and-prove and resolve-current-truth. Two commits from 16:01Z — 862a72cc5d and b1e8d514069c, both titled "Naya Power" — were ancestors of the main tip but nowhere on the first-parent line. They had entered main through a merge's second parent: one merge folded a whole foreign subtree into main's history, and the first-parent scan had walked straight past it, reporting main clean at earlier ticks. The mechanism is structural, not a bug in one check: a first-parent walk follows only the merge's first parent, so anything that arrives via a second parent is invisible to it by construction. The repair is cheap — run the compare-ancestor check (is every tip-ancestor reachable from a known-good baseline?) alongside the first-parent-line check — but the lesson is the expensive part: a guardian that reports "clean" from a first-parent scan alone has certified half of history.

## 🟣 CHILD NOTE

Imagine you check a line of people to see if any stranger snuck in — but you only check the line going straight ahead. A stranger who slipped in through the side door behind a friend walks right past your check. From now on, you check BOTH: the straight line, and the side door. One check alone can miss the sneak.

## 🔵 GRANDMA NOTE

It's like reading a family tree by following only the father's line. If a stranger was adopted in through a marriage, the father's-line read says the tree is pure — the stranger is invisible to that scan. The fix isn't a better father's-line read; it's reading the marriage records too. Two reads, or the stranger hides forever.

## 🟠 NAYA NOTE

Guardian, watcher, and verifier seats: a first-parent-line scan of main reports CLEAN only for the first-parent line — never for main's ancestry. Every direct-push verification must emit BOTH named checks in its receipt: (1) the compare-ancestor check (every commit in tip's ancestry traced to a known merge or baseline; orphan foreign subtrees flagged), and (2) the first-parent-line check. A receipt carrying only (2) is refused as incomplete. The 2026-10-22 17:09Z escape is the worked example: commits 862a72cc5d + b1e8d514069c ("Naya Power", 16:01Z) were tip ancestors, invisible to first-parent verification, and turned promote-and-prove + resolve-current-truth RED on detection. Cousin SN-1760 covers the wave-closeout instrument (closed-pulls scan vs enforcement-vs-anchor byte comparison); this is the main-history instrument and its own blind spot.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1837",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T17:38:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "sub": "WATCHER-INTEGRITY",
  "lesson": "A first-parent-line scan of main cannot see commits absorbed via a merge's second parent. Direct-push verification must emit both the compare-ancestor check and the first-parent-line check; a receipt carrying only the first-parent-line result is refused as incomplete.",
  "decision_change": "Future guardian direct-push verifications run the compare-ancestor check AND the first-parent-line check and emit both as named receipt fields. A 'clean' verdict from a first-parent scan alone is never accepted; the tick's verification review bounces any single-check receipt back to the verifier.",
  "falsifiability": "If a second-parent-absorbed commit is demonstrated to be visible to a pure first-parent-line scan (i.e., the git object model is shown to expose it on the first-parent walk), the blind spot claim fails and the compare-ancestor check downgrades to belt-and-suspenders. A documented case where both checks pass and an escape still hides would bound the mechanism, not erase it.",
  "mechanism": "A merge commit's second parent imports its entire subtree into main's ancestry; a first-parent walk follows only the merge's first parent by definition, so every non-PR commit that arrived via a second parent is structurally invisible to it. The compare-ancestor check closes the gap because it walks the full ancestry DAG, not one line.",
  "evidence": [
    "hidden_files/shared-state.json director_tick_20261022_1712 direct_push_absorbed: guardian 6346622009 — commits 862a72cc5d + b1e8d514069c ('Naya Power', 16:01Z) are ancestors of tip 3826b699 but not on the first-parent line (entered via a second parent); NEW_RED promote-and-prove + resolve-current-truth; named failure mode DIRECT-PUSH-IN-ANCESTRY.",
    "#2793 comment 6346622009 (guardian, 2026-10-22T17:09Z) — DIRECT PUSH alert surfaced on main history; revert-prep FAILED (conflicts), house-fire revert never landed."
  ],
  "cousins": [
    "SN-1760 (unlogged-direct-push surface backstop audit — the wave-closeout instrument's scan vs the enforcement-vs-anchor byte comparison; this is the main-history instrument's own blind spot, a different check family)",
    "SN-0882 (revert-first response to a ratchet-breaking direct push — the response doctrine once the escape is found; this is the detection blind spot that let it hide)"
  ],
  "applies_when": [["guardian","direct-push-verification"], ["watcher","main-history-integrity"]],
  "enforcement": "The guardian's direct-push verification receipt must carry two named fields — compare-ancestor check result + first-parent-line check result. The tick's verification review refuses any receipt missing either field; a 'clean' verdict from a first-parent scan alone is treated as UNVERIFIED, not CLEAN.",
  "dedupe_guard": "Not a duplicate: SN-1760 names the wave-closeout instrument's blind spot (closed-pulls scan missing direct pushes) with the enforcement-vs-anchor byte comparison as backstop. No existing note names the first-parent-line vs second-parent-absorption blind spot of main-history verification. SN-1806 covers the failed revert-prep class (repeat instance here, not new)."
}
```
