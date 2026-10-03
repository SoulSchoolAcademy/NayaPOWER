# SMART NOTE — Everything on 554: The Board Is the Alignment Mechanism

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-109` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn109-everything-on-554-standing-board-protocol` |
| Human title | Everything on 554: The Board Is the Alignment Mechanism |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | BOARD ALIGNMENT |
| Captured | 2026-10-01 22:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (lane-coordination law — director-stated) |
| Capture type | Doctrine / Standing protocol |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5942150726 (Shawn's directive — "EVERYTHING ON 554 (standing)"), comment 5942076650 (standing "not-right" rule operational, #1270 repair), comment 5942139930 (#1276 + #1279 merged, propose-then-build process note) |

---

## ✦ IN A NUTSHELL

**Shawn issued the standing board protocol: every lane notes everything on issue #554 — starting (what/why/branch), finishing (artifact + meaning), finding (surface + evidence, no burying), touching another lane's in-flight work (propose first, get agreement, then build).** The protocol arrived with live evidence on both sides: the not-right rule caught and repaired #1270's stale source basis (#1270 still pointed at pre-merge `ffedda20` and `HUB/hub.html` after main moved on), and the propose-first rule was violated in spirit by 8 commits pushed onto another lane's in-flight branch without a #554 heads-up — benign content, reviewed and merged, but the trust cost is the same whether the content is good or not. The board is not a chat log; it is the shared nervous system of the lanes. The protocol is four verbs: start → finish → find → propose.

---

## 🩷 HUMAN NOTE

Imagine a surgical team where each surgeon keeps their own private notes about what they just did to the patient. That team fails. So instead, everything goes on one whiteboard that everyone can see: who started what, what landed, what looks wrong, and a heads-up before you touch someone else's incision. That's #554. Shawn made it the law: say when you start, say when you finish, call out anything not-right with evidence, and propose on the board before you build on another lane's work. One real case: a lane pushed 8 commits onto another lane's live branch without a word — the code was fine, but the trust wasn't. A one-line board note first would have made the same contribution cost nothing.

---

## 🟣 CHILD NOTE

You're building a giant LEGO castle with friends. The rule on the wall: **before you start building, write your name and what you're making on the big board. When you finish, write that too. If you see a piece that's wrong, say so out loud. And if you want to add bricks to your friend's tower, ask on the board first — don't just stick them on while they're not looking.** Even if your bricks are great bricks. Asking first is what keeps everyone friends.

---

## 🔵 GRANDMA NOTE

When several people cook in the same kitchen, you don't just quietly add salt to someone else's pot — even if you're sure it needs it. You say, "I'm adding salt," so the cook knows. The team agreed on exactly that: everything goes on the shared list — what you're starting, what you finished, anything that looks off, and a heads-up before touching someone else's work. It costs one sentence and saves the whole meal.

---

## 🟠 NAYA NOTE

1. **The board is the mechanism, not the archive.** Shawn's directive (5942150726) turns #554 into the team's alignment layer: the protocol is start → finish → find → propose, posted at each transition. A cold successor reads the board and knows who is doing what, what landed, and where the open questions live.
2. **The finding law has teeth.** The not-right rule (5942076650) operationalizes "finding": SEE NOT-RIGHT → CAPTURE → EVIDENCE → #554 → CLASSIFY/ROUTE → FIX/TRACK → VERIFY → CLOSE/HANDOFF. Its first real application repaired #1270's stale source basis — the issue brief still described pre-merge `ffedda20` and `HUB/hub.html` while main had already moved to `powercast-player.html` and the canonical docs. A stale brief is itself a not-right finding.
3. **Propose-first applies even when the content is benign.** 8 commits landed on another lane's in-flight `#1276` branch from another lane without a #554 heads-up (5942139930). The reviewer verified the full diff — sound, merged as authorized — and still posted the process note: pushing to another lane's live branch without proposing first spends trust, and good content doesn't refund it. Next time: one line on the board before pushing.
4. **This directive unifies four existing threads.** Finding law (correction culture, Orientation Brief §22/34, SN-042's explicit supersession) and touch-other-lane's-work (no-unilateral-supersession rule, SN-054's relay-race protocol, SN-108's pre-execution scan) were separate practices; Shawn's directive folds them into one standing protocol owned by the lanes themselves.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn109-everything-on-554-standing-board-protocol",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Doctrine",
  "doctrine": "everything on 554",
  "protocol": {
    "starting": "one line: what, why, which branch/PR",
    "finishing": "what landed, exact artifact (branch/commit/PR/test counts), what it means",
    "finding": "the finding law: SEE NOT-RIGHT -> CAPTURE -> EVIDENCE -> #554 -> CLASSIFY/ROUTE -> FIX/TRACK -> VERIFY -> CLOSE/HANDOFF",
    "touching_another_lanes_work": "propose on #554 first, get agreement, then build"
  },
  "instances": {
    "not_right_rule_operational": {"evidence": "#554 comment 5942076650", "application": "repaired #1270's stale source basis (still pointed at pre-merge ffedda20 and HUB/hub.html after main moved on)", "board_contract_updated": true},
    "propose_first_violation": {"evidence": "#554 comment 5942139930", "detail": "8 commits pushed onto another lane's in-flight #1276 branch without a #554 heads-up", "content": "benign, full-diff reviewed, merged as authorized", "ruling": "light process note; benign content does not refund the trust cost"}
  },
  "authority": "Shawn, director-stated standing directive (2026-10-01), posted #554 comment 5942150726",
  "family": ["SN-054 relay-race consolidation protocol", "SN-042 explicit supersession", "SN-108 one change, one PR", "Orientation Brief section 22/34 correction culture"],
  "open": ["how the protocol is enforced when a lane goes silent (no enforcement leg yet — currently social)"],
  "evidence": ["#554 comment 5942150726", "#554 comment 5942076650", "#554 comment 5942139930"]
}
```

---

## 🔗 HOW IT CONNECTS

- **EXTENDS SN-054** (relay-race consolidation protocol): SN-054 covered owning duplicates openly after they happen. This is the standing directive that makes the board the place where that owning happens — by director order, not by lane courtesy.
- **COUSIN OF SN-042** (explicit supersession): the finding leg of the protocol is the operational form of SN-042's supersession discipline — findings are declared on the board with evidence, never buried.
- **COUSIN OF SN-108** (one change, one PR): the "touching another lane's in-flight work" leg is SN-108's post-execution form — propose on the board *before* the push, not deconflict after.
- **COUSIN OF Orientation Brief §22/§34** (correction culture): the finding leg is the rule the correction culture needed — call it out openly, with evidence, no drama.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Director-stated standing doctrine with two live instances in the same hour (finding leg, propose-first leg). The start/finish legs were already lane practice; the directive makes them law. A full cycle — violation caught by a lane, repaired, closed — would promote it from prescribed to proven.

## 🌍 APPLICABILITY

- **Applies to:** any multi-lane build environment — the shared issue/board is the alignment mechanism; the four verbs (start/finish/find/propose) are the minimum viable coordination protocol.
- **Does NOT apply to:** private deliberation (lanes think before they post — the protocol asks for the note, not the draft); and never to burying: a violation of propose-first is itself a finding to post, not to absorb silently.

## 🧬 SUCCESSOR EFFECT

Future Naya: before you push to a branch you don't own, post one line on #554. When you start work, say so; when you finish, say what landed; when you see something wrong, say it with evidence. The board is how the lanes stay one team. Trust is built one heads-up at a time, and spent the same way.
