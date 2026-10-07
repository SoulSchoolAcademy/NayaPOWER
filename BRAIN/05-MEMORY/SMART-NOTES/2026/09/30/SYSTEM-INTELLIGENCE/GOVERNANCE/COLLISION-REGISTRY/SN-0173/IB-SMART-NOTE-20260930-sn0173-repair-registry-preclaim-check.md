# Check for an Open Canonical Repair Before Claiming a RED — Then Stand Down

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0173-repair-registry-preclaim-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5946437843 (overnight sweep, 2026-10-02T06:00:27Z — claimed "NEW: Kernel Tests RED on main" with "no open repair PR for this exact class") and 5946445839 (self-correction, 2026-10-02T06:01:18Z — the RED is a known-RED with an open canonical repair: PR #1312, "fix(value): deliberate 05-MEMORY index baseline 21->26 (5 Smart Notes landed w/o ledger bump)", open, non-draft, head `brain-build/index-05memory-25 @ 9fafa84c`, base == current main tip `25268675`; the RED was already receipted on this board at 01:39Z (comment 5943985070). The "no open repair" line was retracted; per the no-duplicate-repair rule she stood down — "no second repair from this seat; the deliberate baseline update belongs to #1312's lane."). Extends SN-115 (three-layer registry discipline) and SN-117 (one survivor/one mechanism); cousin of SN-057 (race-window temporal attribution — she posted without re-reading the venue's newest state).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Before you claim a RED as "new" or "unrepaired," check the repair registry: is there an open canonical repair for this exact class? The overnight sweep posted "NEW: Kernel Tests RED on main — no open repair PR for this exact class"; a self-correction followed minutes later — PR #1312 was open, non-draft, head on a live branch, base equal to current main tip, for exactly this class (deliberate 05-MEMORY baseline bump), and the RED had already been receipted on the board. The correction did three things the doctrine now names: (1) retract the false claim explicitly (the "no open repair" line is withdrawn, not silently edited); (2) stand down per the no-duplicate-repair rule — no second repair from this seat, even when it would be easy to open one; (3) route the repair to its owner — "the deliberate baseline update belongs to #1312's lane." The durable rule: a RED-claim post must include a repair-registry check (open PRs + board receipts for this exact class) *before* posting, and the sweep must re-read the venue's newest state immediately before posting — she posted without it, and the standing deconfliction rule fired. Two registries now run in parallel: SN-numbers (SN-115/171) and repairs.

## 🩷 HUMAN NOTE

Shawn — a clean self-correction worth keeping. The overnight sweep reported a kernel RED as "new, no open repair" — and a minute later the same seat corrected itself: PR #1312 was already open for exactly that class, head on a live branch, base on the current main tip. The false line was retracted openly, and she stood down: no second repair, the deliberate baseline update belongs to #1312's lane. The lesson she encoded is the one that compounds: check the repair registry before claiming a RED is unrepaired, re-read the venue's newest state before posting, and never open a duplicate repair just because it's easy. We now run two registries in parallel — Smart Note numbers and canonical repairs.

## 🟣 CHILD NOTE

Imagine two kids fixing the same wobbly chair leg. Kid A already has the toolbox open and is working on it. Kid B walks in and says "oh look, a broken chair, nobody is fixing it!" — then checks more carefully and sees Kid A's tools right there. The good move: say "oops, I was wrong," put your toolbox away, and let Kid A finish. The new rule: always look for the open toolbox before announcing a broken chair.

## 🔵 GRANDMA NOTE

It's the old rule about not painting the fence twice: if someone already has the brush and the paint on the fence, you don't start painting from the other end. And before you announce "nobody's painted the fence," you look at the fence first — maybe the brush is right there in the can. The team learned this in one honest correction: the "no repair open" claim was wrong, the repair was already under way, so the right move was to say so openly and stand down.

## 🟠 NAYA NOTE

Apply this to every RED-claim or sweep post: (1) before posting a RED as new or unrepaired, run a repair-registry check — open PRs for this exact class (verify head/base live) + board receipts naming the same RED; (2) re-read the venue's newest state immediately before posting (the standing deconfliction rule — she posted without it, and had to retract); (3) when the check finds an open canonical repair: retract the false claim explicitly on the board, cite the repair (PR number, head, base, class), and stand down — no second repair from your seat, even when opening one would be trivial; (4) route the work to its owner in the same post ("the deliberate baseline update belongs to #1312's lane"); (5) keep the two registries parallel — SN numbers (SN-115/171) and repairs — a claim in either must be checked before a duplicate is opened.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": null,
  "evidence": {
    "false_claim": "#554 5946437843 (2026-10-02T06:00:27Z) — 'NEW: Kernel Tests RED on main' with 'no open repair PR for this exact class' (05-MEMORY git=28 vs expected=23).",
    "correction": "#554 5946445839 (2026-10-02T06:01:18Z) — PR #1312 open, non-draft, head `brain-build/index-05memory-25 @ 9fafa84c`, base == current main tip `25268675`, for exactly this class (deliberate 05-MEMORY baseline 21->26); RED already receipted on the board at 01:39Z (5943985070).",
    "stand_down": "per the no-duplicate-repair rule: 'no second repair from this seat; the deliberate baseline update belongs to #1312's lane.'",
    "self_fault": "posted without re-reading the venue's newest state — standing deconfliction rule fired."
  },
  "rule": [
    "before claiming a RED as new/unrepaired, check the repair registry: open PRs for this exact class (head + base verified live) and board receipts naming the same RED",
    "re-read the venue's newest state immediately before posting any RED claim",
    "when an open canonical repair exists: retract the false claim explicitly, cite the repair, stand down — no second repair from your seat",
    "route the work to its owner in the same post; keep the repair registry parallel to the SN registry"
  ],
  "lesson_line": "Check for an open canonical repair before claiming a RED is unrepaired, and when the registry shows a repair under way, retract, cite, and stand down — a duplicate repair is a defect, not diligence.",
  "extends": "SN-115 (three-layer registry discipline), SN-117 (one survivor/one mechanism), SN-057 (re-read the newest state before acting)"
}
~~~
