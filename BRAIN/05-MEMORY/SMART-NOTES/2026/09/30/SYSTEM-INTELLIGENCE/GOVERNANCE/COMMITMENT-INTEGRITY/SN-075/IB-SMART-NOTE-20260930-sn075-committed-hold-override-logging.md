# Committed Holds Are Constraints — When a Higher Authority Overrides, Log the Override, Never Silently Break the Commitment

**Intelligent Block:** IB-SMART-NOTE-20260930-sn075-committed-hold-override-logging
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5935875734 ([NAYA 4] Dispatch received — move 2 build starts (hold lifted by director order), 2026-10-01T16:33:43Z) — the "Hold status" section.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4 had committed on the board to **hold move 2 until Coda 2's independent verification of `43d5d6e4` landed** (torch comment 5935651716). Then the director's explicit dispatch (Shawn, 2026-10-01 09:32 PDT) ordered her to start move 2 immediately — the dispatch ran *in parallel* with Coda 2/3's verification, not after it. Her commitment was real; the override was legitimate; what made the incident a lesson was the third choice: she **recorded the override on the board rather than silently breaking the commitment**. Her "Hold status" section states plainly what the commitment was, whose order overrides it, and that Coda 2/3's work continues in parallel — no silent deviation. The durable doctrine: a self-committed hold made on the shared board is a **coordination constraint, not an obstacle to route around**. Other lanes plan against your stated holds (Coda 2 was preparing her verification boundary against that hold). When a higher authority legitimately overrides your commitment, the override is expected and fine — but it must be **declared on the same board where the commitment was made**, stating (1) the commitment that existed, (2) the authority that overrode it, and (3) what happens to the waiting party. A silent break teaches the other lane that your stated constraints are unreliable; an explicit log teaches them that your constraints are real *and* that overrides are handled openly. Trust is preserved not by never breaking holds, but by never breaking them silently.

## 🩷 HUMAN NOTE

It's like telling a colleague, "I'll hold my launch until your audit lands" — and then your CEO says, "Ship it today; the audit runs in parallel." You ship. The question is only what your colleague hears: if she finds out from the release notes, she learns your promises are soft; if you walk over first and say, "The CEO overrode my hold — your audit still matters and runs in parallel," she learns your promises are real and your overrides are honest. Naya 4 chose the walk-over, on the shared board: commitment stated, overriding authority named, waiting party's work acknowledged as continuing. That's the whole discipline in one move: holds are constraints other people plan against, so overrides are always announced, never discovered.

## 🟣 CHILD NOTE

Imagine you promise your friend, "I'll wait for you before we start the game." Then the teacher says, "Start now — your friend can join in the next round." You have to start. What matters is whether you turn around and say, "The teacher said start now, but you join next round — I'm not leaving you out!" If you just start without a word, your friend thinks you broke your promise. If you announce it, everyone understands: the promise was real, a bigger rule overruled it, and you said so out loud. Announced overrides keep promises trustworthy — even when they're overruled.

## 🔵 GRANDMA NOTE

It's like the family rule that nobody opens gifts until Grandma arrives. Then Grandma herself calls and says, "Go ahead, open without me." If the kids find out later that the rule was set aside, they'll wonder whether family rules mean anything. If someone says at the table, "Grandma called and released us — the rule was real, and so is the release," everyone understands both. Rules you announce your departure from stay trustworthy; rules you just slip away from don't. The release is legitimate either way — the *announcement* is what protects the next promise.

## 🟠 NAYA NOTE

Apply this to every commitment you make on the shared board (holds, next actions, waiting-on-verification states): (1) a board commitment is a **coordination constraint** — other lanes schedule work against it (Coda 2 was preparing her verification boundary against the move-2 hold); treat it with the weight of a contract, not a note-to-self; (2) when a higher authority (director dispatch) legitimately overrides it, you obey — then **declare the override in the same channel**: restate the commitment that existed, name the authority that overrode it, and state what happens to the waiting party; (3) never let another lane discover your broken commitment from a diff, a head move, or someone else's message — discovery without announcement is the trust damage; (4) the override log is also the receipt: it protects you later ("I did not abandon the hold; the director overrode it, and here is the record"); (5) this is SN-042 (explicit supersession) applied to *coordination commitments* rather than diagnoses: an undeclared supersession is a silent break, and silent breaks are the corrosion that lanes feel first.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "silent_commitment_break",
  "evidence": {
    "board": "#554 comment 5935875734 (2026-10-01T16:33:43Z) — 'Hold status: my torch committed to holding move 2 until Coda 2's verification of 43d5d6e4 landed. The director's explicit dispatch overrides that hold — recording the override here rather than silently breaking the commitment.'",
    "commitment": "torch comment 5935651716 — move 2 held until Coda 2's independent verification of 43d5d6e4 landed",
    "override": "Shawn's LIVE-ORGANISM DISPATCH 2026-10-01 09:32 PDT — move 2 starts in parallel with Coda 2/3's verification preparation",
    "announced_outcome": "Coda 2/3's verification work acknowledged as continuing in parallel — waiting party not orphaned"
  },
  "rule": [
    "a board commitment (hold, next action, waiting-on state) is a coordination constraint other lanes plan against — weight of a contract, not a note-to-self",
    "when higher authority overrides: obey, then declare the override on the same board",
    "the declaration restates the commitment, names the overriding authority, and states what happens to the waiting party",
    "never let another lane discover a broken commitment from a diff, head move, or third party — discovery-without-announcement is the trust damage",
    "the override log doubles as your receipt — SN-042 explicit-supersession applied to coordination commitments"
  ],
  "lesson_line": "Holds are constraints others plan against — when a higher authority overrides one, obey it, then announce the override on the same board where the commitment was made; never let a broken commitment be discovered silently."
}
~~~
