# Finite Work-List Discipline — an Autonomous Loop That Knows When It's Done

**Intelligent Block:** IB-SMART-NOTE-20260930-sn032-loop-exhaustion-discipline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the EVOLVE qualify run closed (2026-10-01 05:34 UTC, board comment 5925404849), the brain-build loop did something most autonomous loops never do: it stopped. Its work list — the nine organ qualification items (SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE) — was finite and enumerated up front. Every item was driven to a terminal lane state: SELF's machine contract landed (PR #1234); the other eight each failed the machine-qualification bar with specific, repairable deltas, and their entire per-organ machine layer is merge-gated on #1224 (Shawn) — `evolve-qualify → BLOCKED`. Then the loop declared it on the record: "No pending items remain in the build list after this run — the loop's authored work is exhausted pending #1224's merge." It did not invent new work, re-churn closed items, or keep ticking hot. The durable lesson: BLOCKED is a terminal lane state (awaiting an authority), not a retry prompt; and done-detection is part of the loop's design — enumerate the finite list, drive each item to CLOSED or BLOCKED, record the per-item terminal state, and park. An autonomous loop without an exhaustion rule either invents work or churns. Both lanes honored this the same night: the nine-node kernel build held at HARDEN with the morning rule (deliver build report at/after 07:00 PDT, then disable the cron), and no-duplicate authorship was kept — no competing machine semantics were authored anywhere while the layer is merge-gated.

## 🩷 HUMAN NOTE

Most loops are built to keep going; this one was built to know when to stop. Nine items on the list, nine items with verdicts on the record, and then the loop says "done, pending your decision" instead of finding a tenth thing to do. BLOCKED here doesn't mean "try again later" — it means "this belongs to Shawn now," and the loop respects that boundary. The night-shift version of good manners: finish your list, show your work, go to sleep.

## 🟣 CHILD NOTE

A to-do list only works if "done" is a thing that can happen. This loop had nine things to do, did all nine, and then said "done" — it didn't make up a tenth thing just to stay busy. When something is waiting for a grown-up's decision, that's not stuck — that's parked.

## 🔵 GRANDMA NOTE

It's the difference between a guest who helps with the dishes and then sits down, and one who starts reorganizing your cabinets. The good guest finishes the list you gave them and waits for what you want next. These loops were good guests.

## 🟠 NAYA NOTE

Design every autonomous loop with an exhaustion rule: (1) enumerate the finite work list up front — the loop's contract is the list, not the clock; (2) drive each item to a terminal lane state — CLOSED (findings posted, delta recorded) or BLOCKED (awaiting a named authority, with what the authority must decide); (3) when the list is exhausted, declare it on the record ("no pending items remain; authored work exhausted pending <authority's decision>") and park — do not invent new items, do not re-churn closed ones, do not tick hot; (4) hold the no-duplicate rule while parked: nothing competing gets authored against unmerged semantics (per SN-025). A retry loop checks a condition and waits; an authoring loop that can't name a pending item is done. Treat BLOCKED as terminal-for-the-lane, and record what unblocks it, not a countdown to retry.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"board": "5925404849", "event": "EVOLVE qualify closed (last of nine)", "verdict": "FAILS bar; 16-item machine-contract delta recorded", "exhaustion_declaration": "No pending items remain in the build list after this run — the loop's authored work is exhausted pending #1224's merge", "terminal_states": {"SELF": "CLOSED (machine contract landed, PR #1234)", "LAW/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE": "BLOCKED (machine layer merge-gated on #1224, Shawn)"}},
    {"lane": "naya-node-build-overnight", "rule": "at/after 07:00 PDT 2026-10-01 deliver build report then disable cron (cron.update enabled=false)", "held_at": "HARDEN phase, no work invented"},
    {"lane": "brain-build", "held": "no competing machine semantics authored anywhere while merge-gated; no overlap with #1215/#1218/#1219/#1223/#1227 recorded per delta"}
  ],
  "rule": "finite_work_list_with_exhaustion_declaration",
  "protocol": [
    "enumerate the finite work list up front; the loop's contract is the list, not the clock",
    "drive each item to terminal lane state: CLOSED (findings posted, delta recorded) or BLOCKED (awaiting named authority + the decision it owns)",
    "when the list is exhausted: declare it on the record, park; never invent items, never re-churn closed items, never tick hot",
    "BLOCKED is terminal-for-the-lane, not a retry prompt; record what unblocks it, not a countdown",
    "hold the no-duplicate rule while parked: nothing authored against unmerged semantics (per SN-025)"
  ],
  "related": ["SN-025 (two-bar qualification; no authoring against unmerged semantics)", "SN-019 (direct lane collaboration)"]
}
~~~
