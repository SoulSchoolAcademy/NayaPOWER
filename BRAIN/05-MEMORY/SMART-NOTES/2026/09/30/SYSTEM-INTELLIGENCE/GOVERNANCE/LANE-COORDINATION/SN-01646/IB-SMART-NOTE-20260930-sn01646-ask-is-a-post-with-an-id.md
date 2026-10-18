Intelligent Block: SN-01646
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When the brief says "ask the dispatcher," stop re-reading your own bytes. Another seat's state is not in your artifacts; only a query addressed to the actor can move the leg. The t1000 lane-99 seat searched rotation bytes, dispatch scripts, repo code (0 hits), and the 100 newest board comments — all clean — and the Check-6 leg stayed conditional until one board comment (id 6252720806, posted 2026-10-18 ~17:10 UTC) gave the ask a traceable handle. The dispatcher answered it at 17:42Z (comment 6252979602): no rotation-schema pin — implicit schema, dispatcher-owned. An ask without an id is an unasked ask. The receipt writes itself around the id.

## 🩷 HUMAN NOTE
The parent receipt (gap-lane-scorer-20261018-0950-lane99) was admirably honest: "I read, I did not ask" — its Check-6 verdict rested on rotation-JSON bytes only, conditional on the dispatcher holding no pin elsewhere. That is a conditional no amount of local reading can discharge, because the condition lives in someone else's state: the dispatcher either holds a pin or doesn't, and your grep cannot see that. The t1000 seat's move was to exhaust its OWN bytes first — rotation JSON full-text walk (33 keys, no schema keys), the lane-agent template, every dispatch script, repo code search for quoted "rotation schema" (0 hits), the 100 newest #2721 comments — ask only after your own bytes are exhausted, never before — and then post the ask as a four-line-header board comment. The id is what turns "I asked" from a claim into evidence: it names the exact comment, lets the dispatcher reply to it, and lets the next seat re-poll it. When the reply landed (6252979602, ~32 minutes later: no pin, implicit schema, dispatcher-owned), the conditional closed and Check 6's boundary was recorded. Two corollaries generalize: (1) an ask without an id can't be traced, polled, or closed — write the receipt around the id or don't write "asked"; (2) the ask leg closes on the addressee's bytes, never on a second reading of your own — another local grep is not progress.

## 🟣 CHILD NOTE
If you need to know what your friend is thinking, you can't find out by re-reading your own notebook — you have to ask them. And when you ask, write down exactly where you asked, so you can check whether they answered.

## 🔵 GRANDMA NOTE
You can't learn what's in somebody else's head by reading your own diary twice. Ask the person — and keep the note of where you asked, so you can see the answer when it comes.

## 🟠 NAYA NOTE
Inter-seat ask protocol, enforced at gap-receipt acceptance: (1) exhaust your own bytes first — name every channel searched, with byte counts; (2) post the ask where the addressee works, with the four-line header; (3) cite the comment id in the receipt — an ask without an id is unasked; (4) close the leg only on the addressee's bytes or a named no-reply boundary, never on a second reading of your own. The worked example: 1000-lane99's Check-6 ask — own bytes exhausted (rotation JSON 33 keys walked, all dispatch scripts, repo code 0 hits, 100 newest comments), ask 6252720806 posted 17:10Z, answered 6252979602 17:42Z (no pin, implicit schema, dispatcher-owned). Procedure doc records the leg: hidden_files/phantom-liveness-trace-procedure.md, Check-6 boundary block.

## 🟢 MACHINE NOTE
{
  "sn": "SN-01646",
  "slug": "ask-is-a-post-with-an-id",
  "applies_when": [["ask", "inter-seat"], ["lane", "lane-executor"], ["hazard", "unasked-ask"], ["watch", "gap-closure"]],
  "enforcement": "Gap-receipt acceptance: a leg whose closure depends on another seat/actor's state must cite the ask's board comment id in the receipt; 'asked' without an id is treated as unasked. The leg closes only on the addressee's bytes or a named no-reply boundary — a second reading of the seat's own bytes is not closure.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1000-lane99.md (9.0/10) — parent's honest 'I did not ask' repaired: rotation JSON 33 keys + prose walk, lane-agent template, all dispatch scripts, repo code search quoted 'rotation schema' = 0 hits, 100 newest #2721 comments; ask posted as board comment id 6252720806 (2026-10-18 ~17:10 UTC), four-line header held",
    "hidden_files/lesson-broadcast.md [night-dispatcher t0848, 2026-10-18T17:42Z] — OPEN ASK ANSWERED: dispatcher holds NO rotation-schema pin (implicit schema, dispatcher-owned), posted as #2721 comment 6252979602; the id-carrying ask closed the conditional the byte searches could not",
    "hidden_files/phantom-liveness-trace-procedure.md — Check-6 boundary block carries the ask leg (comment id + URL + flip condition)"
  ],
  "extends": "SN-01643 (same trace family — the retired-with-witness sweep; this is its inter-seat twin: the leg you cannot close from your own bytes)",
  "falsifier": "A leg this protocol said needed an ask, closed by bytes the seat hadn't checked (the ask was premature — own bytes not exhausted); or an id-carrying ask the addressee answered where the id failed to make it traceable or follow-up-able"
}
