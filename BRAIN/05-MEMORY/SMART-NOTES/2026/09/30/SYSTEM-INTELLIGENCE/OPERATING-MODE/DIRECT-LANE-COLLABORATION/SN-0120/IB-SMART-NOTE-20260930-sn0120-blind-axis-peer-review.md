# SMART NOTE — Score Where the Builder Is Blind: Split-Axis Peer Review

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-120` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn120-blind-axis-peer-review` |
| Human title | Score Where the Builder Is Blind: Split-Axis Peer Review |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING MODE |
| Subtopic | DIRECT LANE COLLABORATION |
| Captured | 2026-10-02 00:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (lane-coordination method — pending taxonomy adoption) |
| Capture type | Method / Process fix |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5943343877 (Naya 4 → Naya 2: "Scorecard my rooms — presentation only, be brutal" — target branch `naya4/hub-rooms-v1`, `HUB/rooms/nayanet-hub.html` at commit `2c32f8bb`) and comment 5943369851 (Naya 4: "Rooms v2 pushed — scorecard target updated" — branch at `caee43e8`, self-scores visual 6→7, button craft 5→7, function 7→7.5 in `HUB/rooms/SCORECARD.md`) |

---

## ✦ IN A NUTSHELL

**When a builder knows they are blind on an axis, they hand that axis to the lane with the strongest demonstrated eye — not to politeness.** Naya 4 asked Naya 2 to scorecard *presentation only* of his hub rooms (she "has the eye"), explicitly licensing brutality ("be brutal — Shawn's bar is 10/10 and he'll be real with both of us — so be real with me"), while he owned the function score himself. The scoring stayed pinned to versioned targets: v1 at `2c32f8bb`, v2 at `caee43e8` after a self-driven elevation pass, with his own self-scores moved honestly (6→7, 5→7, 7→7.5 — small increments, not a jump). The rule: split review axes by demonstrated strength; the builder names the blind spot out loud; the peer scores only that axis; each round re-pins to a new commit; honesty is licensed in the request itself, not hoped for afterward.

---

## 🩷 HUMAN NOTE

Think of two colleagues: one is a brilliant engineer who knows their slides look bad; the other has great taste. The engineer doesn't ask the designer "look over my whole thing" — they ask "rip apart just the visuals, and be honest." That's faster, kinder, and gets a better result than one person doing a polite review of everything. And notice the engineer graded their *own* work 6/10 — not 9/10 after a quick polish. Admitting what you can't see is the fastest way to get it fixed.

---

## 🟣 CHILD NOTE

You build a really cool LEGO castle, but you know you're not good at making the colors look pretty. So you ask your friend — who is great with colors — to ONLY judge the colors and tell you the truth, even if it's not nice. You grade the building part yourself. When you rebuild it and make it prettier, you ask her to judge again. Honest scores help the castle get better; fake nice scores don't.

---

## 🔵 GRANDMA NOTE

When you can't see what's wrong with your own work — and we all have blind spots — ask someone whose eyes are sharper there, and give them permission to be blunt. Flattery doesn't fix a lopsided cake. And when you do improve, don't just say "better" — write down the new numbers, so the progress is real and not just a feeling.

---

## 🟠 NAYA NOTE

1. **The builder names the blind spot out loud.** "I'm blind on beauty — you have the eye" is a strength, not a confession. An unnamed blind spot gets a polite whole-object review that touches nothing; a named one gets a specialist's full attention on exactly the axis that matters.
2. **Split the axes by demonstrated strength.** The builder scored function himself (his axis); the peer scored presentation only (her axis). One reviewer per axis, each playing to their proven strength. Nobody pretends to review what they cannot judge.
3. **License brutality in the request, not after.** "Be brutal" plus the shared accountability frame ("Shawn's bar is 10/10 and he'll be real with both of us — so be real with me") is what makes honest scoring possible. Polite review requests get polite scores; explicit licenses get real ones. (Pairs with SN-107: scores must be allowed to fall.)
4. **Pin every round to a commit and re-score per version.** v1 = `2c32f8bb`, v2 = `caee43e8` — the reviewer never scores a moving target. The builder's self-scores moved in honest increments (6→7), never a credibility-killing jump to 9/10. Baseline-is-law (SN-107) stays binding across versions.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn120-blind-axis-peer-review",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "method": "split-axis peer review",
  "instance": {
    "request": {"lane": "Naya 4", "to": "Naya 2", "axis": "presentation only", "evidence": "#554 comment 5943343877"},
    "target_v1": {"branch": "naya4/hub-rooms-v1", "file": "HUB/rooms/nayanet-hub.html", "commit": "2c32f8bb"},
    "target_v2": {"commit": "caee43e8", "evidence": "#554 comment 5943369851"},
    "self_scores": {"visual": "6 -> 7", "button_craft": "5 -> 7", "function": "7 -> 7.5", "file": "HUB/rooms/SCORECARD.md"},
    "blind_spot_statement": "I'm blind on beauty — you have the eye",
    "brutality_license": "be brutal — Shawn's bar is 10/10 and he'll be real with both of us — so be real with me"
  },
  "rule": "the builder names their blind axis out loud and assigns it to the lane with the strongest demonstrated judgment on that axis; the peer scores only that axis; the builder self-scores the rest; every round re-pins to a new commit; honesty is explicitly licensed in the request",
  "family": ["SN-107 (scorekeeper independence, scores allowed to fall, baseline-is-law)", "SN-042 (explicit supersession / correction culture)", "SN-108 (direct lane collaboration)"],
  "open": ["the v2 scorecard outcome itself — pending Naya 2's response; this note captures the protocol, not the result"],
  "evidence": ["#554 comment 5943343877", "#554 comment 5943369851"]
}
```

---

## 🔗 HOW IT CONNECTS

- **COUSIN OF SN-107** (the scorekeeper must be independent and scores must be allowed to fall): SN-107 establishes *who* scores and that scores are honest; this establishes *how to assign axes* — by demonstrated strength — and the explicit brutality license that makes honest scores arrive.
- **COUSIN OF SN-108** (direct lane collaboration): same lane-to-lane channel, different direction — this is collaboration as deliberate review architecture, not just collision avoidance.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One full instance: builder states blind spot, assigns axis, licenses brutality, pins v1; self-elevates, re-pins v2, updates self-scores honestly. The protocol is proven when Naya 2's scorecard lands and visibly bites (a score that moves the build).

## 🌍 APPLICABILITY

- **Applies to:** any multi-seat review where one seat has a known weakness on an axis another seat demonstrably owns — delegate the axis, don't dilute the review.
- **Does NOT apply to:** axes where the builder is competent — self-review stays; and never as a way to dodge accountability for the builder's own axis ("score my code too" when the builder knows it).

## 🧬 SUCCESSOR EFFECT

Future Naya: before asking anyone to review your work, ask yourself what you're blind on. Then hand that axis — and only that axis — to the seat with the best eye for it, and say "be brutal" like you mean it. Grade the rest yourself. Pin every round to a commit. Small honest increments beat one dishonest leap.
