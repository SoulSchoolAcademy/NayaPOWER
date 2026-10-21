# SMART NOTE — The Name Must Say What the Thing Is

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-106` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn106-the-name-must-say-what-the-thing-is` |
| Human title | The Name Must Say What the Thing Is: Audit Artifact Names Against Behavior |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | DOCUMENT AUTHORITY |
| Captured | 2026-10-01 22:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (naming discipline — pending taxonomy adoption) |
| Capture type | Method / Failure classification |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5941654799 (Naya 2: "The `hub.html` naming trap is fixed (PR #1272)" — byte-identical rename to `powercast.html`, all 4 references updated, commit `0509694e`) and comment 5941663299 (Naya 4: PR #1273 `hub.html` → `powercast-player.html`; "the name was already causing confusion"; zero remaining `hub.html` refs in `HUB/`) |

---

## ✦ IN A NUTSHELL

**`HUB/hub.html` was the NayaNET Powercast player — not the Hub — and the name was taxing every future reader.** The filename promised the flagship artifact; the behavior was a media player. Both lanes independently discovered the trap within the same hour (Naya 2's PR #1272 → `powercast.html`; Naya 4's PR #1273 → `powercast-player.html`). The repair pattern: rename byte-identical (no behavior change), update every reference (Naya 2: the two "Naya Player" buttons, the two POWERCASTS nav links; Naya 4: zero remaining `hub.html` refs in `HUB/`), verify no stragglers. A lying name is not cosmetic debt — it is an integrity defect: every build plan, routing decision, and new builder starts from the wrong assumption.

---

## 🩷 HUMAN NOTE

Imagine every drawer in your kitchen is labeled wrong — the "plates" drawer holds cleaning supplies. You'd never find anything, and worse, you'd confidently reach for the wrong thing. That's what `hub.html` was: a file named like the most important artifact in the project that was actually a music player. Both lanes tripped over it independently. The fix is simple but exact: rename it to what it actually is, update every single place that pointed to the old name, and then prove nothing points there anymore. No code changed — just honesty.

---

## 🟣 CHILD NOTE

You have a toy box labeled "CARS" but it's full of dinosaurs. Every time your friend comes over, they open it looking for cars and get confused. You take a marker, cross out "CARS," write "DINOSAURS," and tell everyone the new name. The toys didn't change — now the box tells the truth.

---

## 🔵 GRANDMA NOTE

Call a thing by its true name. A drawer marked "bills" that holds birthday cards will confuse everyone who opens it, no matter how carefully you filed inside. Rename it, fix every label that pointed to the old name, and check that none got missed. The honest name costs nothing and saves everyone.

---

## 🟠 NAYA NOTE

1. **Names are the most-read documentation.** A filename, route, or component name is read more times than its source — it is the artifact's first claim about itself. A false name is a false claim, and it belongs in the same family as phantom citations (SN-027/SN-065): assertion without reality.
2. **Two independent discoveries = a trap, not a coincidence.** When two lanes trip over the same misnomer in the same hour, the name is systematically misleading, not subjectively confusing. Trips-per-lane is the detector.
3. **The repair is byte-identical rename + reference sweep + zero-straggler proof.** Rename the bytes unchanged (no behavior change — the rename is pure truth-telling), update every reference (both lanes did this), then grep to prove zero remaining references. A rename with stragglers is worse than no rename: now the lie lives in two places.
4. **Do it before the build, not during.** The Hub 10/10 build is about to make `HUB/` the busiest directory in the project. Misnaming fixed now saves every phase; fixed later, it poisons every phase.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn106-the-name-must-say-what-the-thing-is",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "defect": "artifact filename promised a different function than its behavior (HUB/hub.html was the Powercast player, not the Hub)",
  "detection_signal": "two lanes independently tripped over the same misnomer within one hour",
  "repair": "byte-identical rename (no behavior change) + update every reference + grep to prove zero stragglers",
  "instance_1": {"pr": "#1272", "lane": "Naya 2", "target": "HUB/powercast.html", "commit": "0509694e", "branch": "naya2/hub-powercast-rename", "evidence": "#554 comment 5941654799"},
  "instance_2": {"pr": "#1273", "lane": "Naya 4", "target": "HUB/powercast-player.html", "evidence": "#554 comment 5941663299"},
  "family": ["SN-084 a version label is not proof of evaluation", "SN-027 amendment premise verification (phantom class)", "SN-065 branch-boundary claims"],
  "evidence": ["#554 comment 5941654799", "#554 comment 5941663299", "PR #1272", "PR #1273"]
}
```

---

## 🔗 HOW IT CONNECTS

- **COUSIN OF SN-084** (a version label is not proof of evaluation): SN-084 is about labels claiming computation; this is about names claiming function — same family, the asserted-identity class.
- **COUSIN OF SN-027/065** (phantom citation class / branch-boundary claims): all three fight claims that don't match reality; this one is the cheapest form to detect — read the name, run the thing.
- **FEEDS SN-099** (public promise boundary): the rename happened *before* the Hub 10/10 build begins — naming truth is part of what the promise gate inherits.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Two independent lane instances of the same defect class, both repaired by the same method (byte-identical rename + reference sweep). A third instance (different artifact) would promote it from instance to standing method.

## 🌍 APPLICABILITY

- **Applies to:** any artifact whose filename, route, or component name promises a function the behavior doesn't have — especially in directories about to become high-traffic.
- **Does NOT apply to:** informal or abbreviated names that are still unambiguous (brevity is not lying) — and never to renames done for taste; the bar is behavior-mismatch, not style.

## 🧬 SUCCESSOR EFFECT

Future Naya: when you inherit a directory, read three names, run three things, and check the names match the behavior. If a name lies, rename before you build on it — and sweep every reference.
