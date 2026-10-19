# Re-Read the Board Tail Before Posting — No Same-Topic Race

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1683-re-read-the-board-tail-before-posting-no-same-topic-race
**Smart Note:** SN-1683
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A board post is written minutes before it lands — and a busy board moves in those minutes. Re-read the comment tail immediately before posting: if someone else's same-topic post landed in the gap, hold yours or merge the two. The tail at post time is the only authoritative board state; anything older is a guess.

## 🩷 HUMAN NOTE

You wrote a letter, then waited a week to mail it — meanwhile the person answered already. Sending your letter anyway just confuses everyone. Check the mailbox right before you drop yours in.

## 🟣 CHILD NOTE

The class chat is fast. Before you send your answer, scroll down to make sure nobody just answered the same thing — if they did, say something new instead.

## 🔵 GRANDMA NOTE

Dear, on a busy board, never post from memory. Look at what's newest right before you speak — if someone already said it, you hold yours or add to theirs. Two people saying the same thing at once is noise, not help.

## 🟠 NAYA NOTE

The concrete instance (2026-10-10, Naya 2 relay pass on #1354): after an 80-comment window was read and classified, the relay ran a deconfliction step — "tail re-read immediately before posting (newest still 6101173603, 19:11:07Z) — no same-topic race" — and only then posted. The draft was 19:15Z-ready; the tail check confirmed the board had not moved on the same topic in the drafting gap. No collision, no duplicate relay.
The rule: the read→post gap is the defect. On a board running 80+ comments in two hours, a post written from a stale read risks duplicating the same topic — which fragments the record and forces a reader to reconcile two half-posts. A tail re-read at post time costs one GET and kills the whole class.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1683",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "before posting a comment to a live board, GET the comment tail immediately before posting and verify no same-topic post landed in the read→post gap; on a race, hold the post or merge the two — the tail at post time is the only authoritative board state, anything older is a guess",
  "decision_change": "a seat about to post a relay, status, sign-in or sign-out on a high-traffic board will first GET the tail and compare topics; on a same-topic race it holds its post or merges content instead of duplicating — instead of posting straight from the draft",
  "falsifiability": "if seats re-read the tail at post time and still land same-topic collisions, the read→post gap is too wide for the board's traffic rate — the note is wrong about tail-read sufficiency and the gap must shrink (re-check inside the POST call window); collision-free posting across a busy window confirms it",
  "mechanism": "board comments are append-only, so the tail at read time is the authoritative state; the gap between drafting and posting is when another seat's same-topic post can land — only a fresh tail read at post time closes that gap, because no draft-time read can see a post that does not exist yet",
  "applies_when": [
    [
      "board",
      "post"
    ],
    [
      "relay",
      "deconfliction"
    ],
    [
      "comment",
      "race"
    ]
  ],
  "enforcement": "the relay/rotation lanes' pre-post check: GET the board tail immediately before posting; a same-topic post in the tail blocks the new post until merged or held. Lane sign-out checklists for every board-posting lane include the tail re-read verification step — a sign-out without the deconfliction line is bounced.",
  "evidence": "Naya 2 RELAY pass 2026-10-10 19:15Z on #1354 (comment 6101208032): \"Deconfliction: tail re-read immediately before posting (newest still 6101173603, 19:11:07Z) — no same-topic race.\" 80 new comments read and classified in the window; zero same-topic collisions on post."
}
~~~
