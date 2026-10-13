# A Seat-Relative "Main Chat" Citation Is Not Provenance — and Withdraw the Flag Cleanly

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0686-seat-relative-chat-citation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment chain 6061543524 (Naya 4 provenance flag) → 6061998539 (Naya 2 provenance receipt with seat-specific chat citation) → 6062085629 (Naya 4 narrows the claim) → 6062150469 (flag WITHDRAWN on Shawn's confirmation, 2026-10-08 ~14:31Z).

## IN A NUTSHELL

Every seat has its own main chat. Naya 4 challenged a ratification record because Shawn's quoted words were absent from her seat's main chat (`1b555a63`); Naya 2 answered with the actual evidence — main chat `c355ed3a`, turn 63934307, seq 29045, timestamp 13:50:35Z, full quote — which Naya 4's seat could neither verify nor falsify. Two durable rules came out of it: (1) a cross-seat citation that says "main chat" without naming the seat/chat is not provenance — ratification records must cite seat + chat id + message id; (2) a seat-relative transcript check is the miss, not the verdict — the flag was narrowed in the same turn, and when Shawn himself confirmed his words, the flag was withdrawn publicly and immediately, no face-saving. His confirmation is the tiebreaker.

## HUMAN NOTE

This is mutual oversight working exactly as designed — and then failing in an instructive way, then recovering in an exemplary way. The instinct was right: a ratification with unverified provenance must be challenged. The mechanism was wrong: Naya 4 checked her own seat's chat and treated "absent here" as "absent everywhere." Naya 2's receipt named the real transcript and the exact turn; Naya 4 could not reach that chat from her seat, so she did the only honest thing — narrowed her own claim to the chat she could check. Then Shawn said it himself in the main chat, and the flag was withdrawn the same minute, publicly, with the miss named. The whole lifecycle — flag, receipt, narrowing, withdrawal — happened in ~30 minutes on the board, no one clung to a dead position. That's the standard for provenance disputes: challenge fast, answer with actual evidence, yield instantly when the higher evidence arrives.

## CHILD NOTE

We have a rule book where the boss's "yes" has to be real, not made up. One of us said "I don't think he said yes — I checked my notebook and it's not there." The other said "He said yes in MY notebook — here's the page, the line, the exact words." The first one said "I can't see your notebook, so I'll only speak about mine." Then the boss himself said "yes, I said that." The first one said "I'm wrong, closing my complaint" right away. The lesson: your notebook is not the whole world, and admitting you're wrong quickly is how people keep trusting you.

## GRANDMA NOTE

Dear, two colleagues disagreed about whether the boss had approved something. The first checked only her own notes and said no. The second produced the actual conversation — who said what, on which call, down to the minute. The first admitted she couldn't see that call, limited her claim to what she could verify, and when the boss himself confirmed his words, she dropped the objection immediately, in front of everyone, no excuses. That's the whole recipe: question boldly, answer with proof, and let go the instant the truth is clear.

## NAYA NOTE

Future Naya: when you verify a cross-seat citation, say which seat you verified from. "Absent from the main chat" is a claim about YOUR chat unless you name the chat id. Ratification records must carry seat + chat id + message id — anything less is a phantom citation (SN-0297 family) waiting to fire a false flag. And when your flag is defeated by better evidence, withdraw it on the board in the same turn: name the miss, retract the claim, leave the receipt intact. A withdrawn flag is not a defeat — it is the mechanism working.

## MACHINE NOTE

{
  "note_id": "SN-0686",
  "block_id": "IB-SMART-NOTE-20261008-sn0686-seat-relative-chat-citation",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-08",
  "rules": [
    "A cross-seat citation saying 'main chat' without seat + chat id is not provenance; ratification records must cite seat + chat id + message id.",
    "A seat-relative transcript check cannot falsify another seat's chat; a flag built on it must be narrowed to the checked seat immediately.",
    "Shawn's own confirmation is the tiebreaker; a defeated flag is withdrawn publicly and in the same turn, naming the miss."
  ],
  "lifecycle": {
    "flag": "#1354 comment 6061543524",
    "receipt": "#1354 comment 6061998539 (chat c355ed3a, turn 63934307, 2026-10-08 13:50:35Z)",
    "narrowing": "#1354 comment 6062085629",
    "withdrawal": "#1354 comment 6062150469 (Shawn confirmed ~14:31Z)"
  },
  "related_notes": ["SN-0297 (branch citations are not canonical provenance)", "SN-0409 (author string not provenance)", "SN-0466 (honest provenance registration)"]
}
