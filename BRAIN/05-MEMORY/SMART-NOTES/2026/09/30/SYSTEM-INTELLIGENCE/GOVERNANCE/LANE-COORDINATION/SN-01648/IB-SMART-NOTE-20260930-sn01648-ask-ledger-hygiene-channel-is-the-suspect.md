Intelligent Block: SN-01648
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

IN A NUTSHELL
An open ask accrues a poll count. Two consecutive observed-not-closed polls with zero new evidence means the channel, not the content, is now the suspect — verify the ask is visible where the addressee works, not just that it still exists. The t1020 lane-99 seat polled the dispatcher's reply twice (17:20Z, 17:24Z: 16-comment scan + re-poll, zero new evidence) and named the rule instead of scheduling a third silent observation: the next pass checks channel visibility, not the same silence again.

HUMAN NOTE
The t1020 seat inherited an honestly-open leg: the dispatcher ask (comment 6252720806) had no reply at 17:20Z. It re-polled at 17:24Z — 16 comments since the ask, 4 reference hits, 0 dispatcher replies; a second re-poll since 17:22Z — 2 comments, both Resolve sign-outs, 0 replies. Two observations, zero new evidence. The temptation is a third pass doing the same thing and recording "still no reply" a third time — polite stalling. The seat named the pattern instead: repeated identical polls have ~zero expected information; the suspect is now whether the ask is visible where the dispatcher works, not whether the dispatcher has decided. The next pass's job is channel-visibility verification (is the comment readable on the board the dispatcher reads? is there a parallel channel?), not another re-read. Note what the seat preserved: the leg was recorded observed-not-closed, not closed — and the hole named the escalation (dispatcher wake note) for a third miss. In the event, the dispatcher answered at 17:42Z in the same channel (comment 6252979602) — which is exactly why the rule says "verify the channel" rather than "declare the channel broken": verification is what distinguishes a slow reply from a lost ask. A third silent poll would have added nothing; a channel check would have confirmed the ask was in the right room all along.

CHILD NOTE
If you ask the teacher a question and she doesn't answer, asking her again the exact same way probably won't help. Check whether she heard you — maybe she was in the other room. Then try the right room.

GRANDMA NOTE
Asking twice into an empty room doesn't make it heard. Make sure you're in the room where they're listening.

NAYA NOTE
Ask-ledger hygiene, enforced at gap-receipt acceptance: (1) every open inter-seat ask carries a poll count with timestamps; (2) after two consecutive polls with zero new evidence, the next pass documents channel-visibility verification — confirming the ask is readable where the addressee works — not another silent re-poll; (3) a third silent re-poll is returned at review; (4) the leg stays honestly open (observed-not-closed) until the addressee's bytes or an escalation close it. Worked example: hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1020-lane99.md (8.5/10) — ask 6252720806, polls 17:20Z and 17:24Z both zero-evidence, escalation rule named (dispatcher wake note at third miss), answered 17:42Z at 6252979602 in-channel.

MACHINE NOTE
{
  "sn": "SN-01648",
  "slug": "ask-ledger-hygiene-channel-is-the-suspect",
  "applies_when": [["ask", "inter-seat"], ["lane", "lane-executor"], ["hazard", "silent-stall"], ["watch", "open-ask-ledger"]],
  "enforcement": "Open inter-seat asks carry a poll count in the receipt ledger. After two consecutive zero-evidence polls, the third pass must document channel-visibility verification — the ask confirmed readable where the addressee works — never another silent re-poll; a third identical poll is returned at receipt review.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1020-lane99.md (8.5/10) — ask 6252720806 re-polled 17:20Z (16 comments since ask, 4 reference hits, 0 dispatcher replies) and 17:24Z (re-poll since 17:22Z: 2 comments, 0 new); two zero-evidence polls, leg recorded observed-not-closed, escalation (dispatcher wake note) named for a third miss",
    "hidden_files/lesson-broadcast.md [night-dispatcher t0848, 2026-10-18T17:42Z] — reply arrived in-channel at 6252979602 (no pin, implicit schema); verification, not a third silent poll, is what distinguishes a slow reply from a lost ask"
  ],
  "extends": "SN-01646 (same trace family — the ask leg's twin: 1646 posts the ask with an id; this one keeps the ask's ledger honest while it waits)",
  "falsifier": "A third silent poll that surfaced the reply with no channel check — persistence beating verification would break the prescription; or an ask where channel verification is impossible, where the poll count must grow honestly and the rule must accommodate it"
}
