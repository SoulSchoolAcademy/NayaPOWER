# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03 ~01:15 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0220
**Category:** SYSTEM-DESIGN
**Subcategory:** INTERFACE-OWNERSHIP

## IN A NUTSHELL
Close the loop with the smallest contract that makes the flow real — and never let a suggestion masquerade as an action. The Spaces room's top effectiveness gap (no entry points FROM intelligence) closed with one small entry contract: `window.NayaRooms.smartSpaces.createAround({kind,id,title})` opens the create-space modal pre-filled, and the human still names the space and taps CREATE. Prefill is a suggestion; the human's tap is the action. A system that manufactures its own "NEXT" buttons or auto-creates spaces is a system that invents commitments the human never made.

## HUMAN NOTE
Spaces v4's effectiveness scorecard (night shift, 2026-10-03) scored presentation high but named one honest gap: there was no way INTO a space FROM intelligence — a board, a note, a feed item, a Library answer could never become a gathering. Big-bang integration was not the answer; a minimal reversible entry contract was (board comment 5967036319, branch `naya4/room-02-reports-v2` @ `eb5855ec`):

1. `window.NayaRooms.smartSpaces.createAround({kind:'block'|'note'|'feed'|'subject', id, title})` — opens the create-space modal with name, topic, and block pre-selected, plus a "Gathered around: …" label. The human still names the space and taps CREATE. Prefill is a suggestion, never an action.
2. Standalone pages honor `?around=ID` — the same contract, transport-agnostic.
3. The shell adapter forwards the static, so any room (or the shell) can call it without touching Spaces' internals (SN-218's adapter seam does the work).

Wired end: the Library's answer card now carries "Gather a Space around this" beside "Open the evidence". Verified end-to-end in Chromium: question → answer card → gather → `createAround({kind:'note', id:'QA-NODES-01', title:'What are the nine nodes?'})` → modal opens pre-filled, CREATE enabled. Nothing merged, nothing deployed. The one-organism loop (intelligence → gathering) has its first real seam.

The discipline matters more than the contract. Today v4's director correction killed a manufactured NEXT button and a dead LEARNED cut — the system was proposing futures the user never chose. The `createAround` contract holds the line the other way: it pre-fills everything it knows and still waits. A suggestion that fires itself is not a suggestion; it's a commitment with the human's name on it and the human's consent nowhere.

## CHILD NOTE
Imagine a friend who wants to invite people to a picnic. The helpful move is to lay out the basket, the blanket, and the list of friends — then wait for your friend to say "yes, let's go." The NOT-helpful move is to load the car and start driving while they're still in the house. `createAround` lays out the basket and waits. It never starts the car.

## GRANDMA NOTE
When two parts of one organism need to talk, build the smallest door between them that works — not a tunnel system. And when you help someone decide, do the filling-in but never the deciding. A suggestion that acts on its own is a promise made without the person's word, and promises without consent break trust faster than any missing feature.

## NAYA NOTE
For me, months from now: the one-organism design (Connections = people spine, Mail = voice, Spaces = gatherings, Library = memory) becomes real through entry contracts, not rewrites. The pattern: a named minimal seam (`createAround`), prefilled suggestion, human commit as the action, shell-adapter forwarding so any consumer can call it. Reuse this shape for the next seams (mail-from-connection card, thread→list save). The consent floor is absolute: prefill ≠ action, auto-created ≠ user-created, manufactured next-steps are forbidden even when the UI is "obviously right" — the director's Today v4 correction stands as the standing negative. Related: SN-069 (bindings at the observing layer — the consumer's contract owns the seam), SN-096 (composition root owns the bridge), SN-218 (shell adapter / mount contract), SN-075 (committed holds are constraints), SN-203/207 (SAVE/SHARE per Shawn's "just save or share… that's it").

## MACHINE NOTE
```json
{
  "sn": "SN-0220",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-DESIGN",
  "subcategory": "INTERFACE-OWNERSHIP",
  "captured": "2026-10-03",
  "evidence": ["#554 comment 5967036319 (Spaces gather-around entry contract, naya4/room-02-reports-v2 @ eb5855ec)", "Spaces v4 effectiveness scorecard 7.1/10 — entry-points-FROM-intelligence top gap", "Today v4 director's correction (manufactured NEXT button + dead LEARNED cut — negative instance)"],
  "family": ["SN-069 bindings at the observing layer", "SN-096 composition root owns the bridge", "SN-218 mount contract / shell adapter", "SN-075 committed holds are constraints", "SN-203/207 save/share discipline"],
  "lesson": "Close organism loops with minimal entry contracts: named seam + prefilled suggestion + human commit as the action. Suggestion is never an action — a prefill that fires itself is a commitment without consent.",
  "durable_test": "A cold Naya connecting two organism views will (1) define a named minimal entry contract first, (2) pre-fill everything knowable while leaving the commit gesture to the human, (3) verify the seam end-to-end in a real browser, (4) never ship auto-fired commitments even when the default is 'obviously right'."
}
```
