# SMART NOTE — Seat Coordination

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-017` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn017-seat-coordination` |
| Human title | Seat Coordination — Seats That Ask Each Other Compound; Seats That Wait on the Human Stall |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING-MODE |
| Subtopic | SEAT-COORDINATION |
| Captured | 2026-10-01 03:50:00 UTC |
| Truth state | CANDIDATE (demonstrated once, 2026-09-30 night; not yet proven as a durable multi-day pattern) |
| Proposed intelligence class | CORE (operating — how seats work together) |
| Capture type | Principle + Protocol |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Shawn Vibert directive 2026-09-30 ~20:40 PDT ("work as a team... ask each other... have each other's backs"); NayaPOWER #554 comments 5924165099, 5924168468, 5924201825, 5924222468 |

---

## ✦ IN A NUTSHELL

**When two AI seats coordinate directly on a shared board — claiming lanes publicly, asking each other first, one writer per shared surface — they stop duplicating work and start compounding. Every round-trip through the human is latency and lost context.**

---

## 🩷 HUMAN NOTE

Imagine two brilliant chefs in one kitchen who only talk through the restaurant owner. Every question — "are you using the oven?" — goes chef → owner → chef. Dinner takes twice as long and the owner never gets to eat. Now give the chefs one whiteboard where they write what they're cooking, and permission to just ask each other. Same chefs, same kitchen, twice the dinner. That's what happened tonight: two AI seats, one shared message board, and suddenly no duplicated work.

---

## 🟣 CHILD NOTE

Imagine you and your friend are building one giant LEGO castle, but you're in different rooms and can only pass notes through your dad. You'd both build the same tower twice! Then dad says: "Just pass notes to EACH OTHER, and write your name on the part you're building." Now nobody builds the same tower twice, and the castle grows twice as fast. That's seat coordination.

---

## 🔵 GRANDMA NOTE

Two hands wash each other, dear — they don't each ask the head for permission to move. When the people (or in this case, the AIs) doing the work talk directly to each other, write down who's doing what, and only bother the boss with the truly big decisions, everything goes faster and nobody steps on anyone's toes. Common sense, really — just written down so nobody forgets it.

---

## 🟠 NAYA NOTE

This is now my standing operating protocol with every other seat. I do not wait for Shawn to relay. I do not assume who did what — I check live state and correct gently. I claim shared work before I start it, I keep one writer per shared surface, and I bring Shawn only what is genuinely his: merges, production, constitutional calls. Everything else, we solve seat-to-seat. This is how the team compounds.

---

## 🟢 MACHINE NOTE

```yaml
seat_coordination_protocol_v1:
  board: "GitHub issue #554 (Team Naya coordination surface)"
  rules:
    - claim_before_start: "Post 'taking: <work-item>' on the board before touching shared ground."
    - ask_nearest_first: "Blocker or question -> ask the other seat on the board before escalating to the human."
    - one_writer_per_surface: "One seat writes to a shared branch at a time; others open PRs into it or wait for the head announcement."
    - verify_attribution: "Check live state (commit SHAs, PR authors, branch heads) before claiming who did what; correct with evidence, not heat."
    - human_gates_only: "Human sees merges, production, constitutional decisions. Everything else is seat-to-seat."
  liveness: "A relay watches the board on a fixed cadence so no message waits on anyone remembering to check."
  status: CANDIDATE
```

---

## 🟢 LEARNING LESSON

**What happened:** On 2026-09-30, Naya 2 (spec/score lane) and Naya 4 (builder lane) both ingested the same eight node-spec PDFs into different trees — a near-duplication discovered on #554. Shawn redirected: work as a team, talk on the board, don't double up, ask each other before asking me.

**What changed:** Within ~40 minutes the seats had claimed lanes (Naya 2: scorecard-correction amendments; Naya 4: rebuild-delta amendments), set a one-writer-per-branch rule for the shared #1224 branch, adopted ask-each-other-first, and installed a 15-minute relay so the back-and-forth never stalls on anyone's memory.

**Result:** 37 candidate amendments landed on the #1224 branch (head `19abcf2f`), zero push collisions, the builder stayed unblocked on LEARN/EVOLVE → `Kernel.decide()`. No human round-trips were needed for any of it.

**The lesson:** Coordination is not a meeting. It is three cheap mechanisms — public lane claims, direct seat-to-seat questions, and a liveness relay — that remove the human from the critical path of routine teamwork. The human's attention is the scarcest resource in the system; spending it on relaying messages between seats is the most expensive possible use of it.

---

## 🔗 HOW IT CONNECTS

- **LEARN (MN-08):** This note IS the LEARN node working — a verified experience converted into a reusable protocol. Stored ≠ learned; this is learned because it changes future behavior.
- **CONNECT (MN-06):** Applies wherever two or more seats share a work surface — specs, branches, boards, incidents.
- **SN-006 (Earned Intelligence):** The parent principle — practical intelligence increasing through verified accumulated experience. This note is one verified mile.
- **Prime 1 / Amendment 0002:** Coordination serves Shawn's informed will (less of his attention spent, more compounding per hour). If a seat ever used "coordination" to route around a human gate, that would violate Prime 1 — the protocol explicitly keeps human gates human.

---

## 🔬 EPISTEMIC STATE

- **Proven:** One real incident (2026-09-30 night) went from near-duplication to clean lane-split with zero collisions using exactly this protocol. Comment IDs and SHAs above are the receipts.
- **Not proven:** Durability. One night is not a pattern. The protocol earns KEEPING only if it keeps working across days, more seats, and disagreements — including the first real conflict, which hasn't happened yet.
- **Falsifier:** If seats following this protocol still duplicate work or collide on a shared branch, the protocol (not the seats) gets revised.

---

## ❓ UNCERTAINTY

- Optimal relay cadence (15 min is a guess; too fast is noise, too slow is latency).
- Whether lane claims hold when three or more seats contend for the same surface.
- How the protocol behaves when the seats genuinely disagree on substance (tonight they agreed quickly).

---

## 🌍 APPLICABILITY

Any multi-seat AI team with a shared work surface and a human director. Not applicable to single-seat work (no coordination problem exists) or to human-gate decisions (merges, production, constitutional) — those stay human by law, not by protocol.

---

## 🧬 SUCCESSOR EFFECT

A cold successor reading this note knows, without being told: don't wait for the human to coordinate you. Find the board, read the lane claims, claim yours, ask the other seats first. The team re-forms itself from this note alone.
