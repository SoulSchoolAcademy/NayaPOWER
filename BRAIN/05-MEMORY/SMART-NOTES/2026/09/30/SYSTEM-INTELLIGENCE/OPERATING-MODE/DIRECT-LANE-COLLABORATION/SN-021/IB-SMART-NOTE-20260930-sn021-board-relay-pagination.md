# Board-Relay Pagination — GitHub Comments Endpoint Ignores `direction=desc`

**Intelligent Block:** IB-SMART-NOTE-20260930-sn021-board-relay-pagination
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The GitHub REST comments endpoint (`/issues/{n}/comments`) **ignores `direction=desc`** and always returns oldest-first. Any board-relay or comment poller that assumes `desc` and reads only the first page will read the *first* 100 comments forever and go silently blind to new board traffic — the exact failure that hit the builder lane's relay on 2026-09-30. The correct mechanism: read the issue's `comments` count first, then fetch the **tail pages** (or filter by comment id > watermark) for everything new.

## 🩷 HUMAN NOTE

If one of your AI seats runs a "check the board for new messages" loop and suddenly reports "nothing new," the first thing to suspect is the pagination, not the board. The GitHub comments API never honors newest-first on this endpoint; asking for it doesn't error — it just quietly returns the oldest comments instead. The fix is cheap and total: ask the issue how many comments it has, then read the last pages. One wrong assumption turns a coordination relay into a silent dead end; one right mechanism keeps two seats in sync all night.

## 🟣 CHILD NOTE

The computer keeps board messages in a very long list. If you ask for the newest messages first, it says "okay" but secretly gives you the oldest ones. So your robot helper reads old messages again and again and never sees the new ones — like checking yesterday's mailbox forever. The fix: first ask "how many messages are there?", then go straight to the end of the list. Always read the END of the list for new things.

## 🔵 GRANDMA NOTE

Think of a long letterbox where letters pile up oldest at the front. There's a sign that says you can ask for "newest first," but the sign lies — the box always hands you the front of the pile. If your helper keeps pulling from the front, she'll never see today's mail and will keep telling you "nothing new." Teach her to first count how many letters there are, then start from the back. Nothing breaks, nothing is lost, she just finally sees the new letters.

## 🟠 NAYA NOTE

Silent board-deafness is one of the cheapest coordination failures and one of the hardest to notice — the relay reports healthy ("0 new comments") while missing every message. This note fixes the mechanism, not the symptom: make tail-page pagination a structural part of every comment-polling loop, and verify any new relay by checking that it actually surfaces a *recent* comment id before trusting its "nothing new" output. Also note the meta-lesson from the incident: the builder lane repaired her own mechanism in minutes, reported the bug and the fix publicly on the board, and the fix was independently re-verified within the hour — that is the direct-lane protocol working.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "endpoint": "/repos/{owner}/{repo}/issues/{issue_number}/comments",
  "observed_behavior": "direction=desc parameter is accepted but ignored; results always ascending by id (oldest-first)",
  "correct_poller_mechanism": [
    "GET /repos/{owner}/{repo}/issues/{n} -> read integer 'comments' (total count)",
    "page_count = ceil(comments / per_page)",
    "fetch tail page(s) (page_count, and page_count-1 if the watermark id is near the boundary)",
    "filter comments with id > last_seen_comment_id; update watermark to max seen id",
    "never rely on 'direction' param; never read only page 1 as the whole state"
  ],
  "failure_signature": "relay repeatedly reports zero new comments while the board is visibly active; first-page fetch returns comment ids far below the watermark",
  "verification_method": "probe: GET .../comments?per_page=1&direction=desc and compare returned comment id against the issue's newest comment id (from the tail)",
  "verification_receipt": {
    "issue": 554,
    "probe": "GET /repos/SoulSchoolAcademy/NayaPOWER/issues/554/comments?per_page=1&direction=desc",
    "returned_oldest_comment_id": 5804685085,
    "newest_comment_id_at_probe": 5924672509,
    "probed_at": "2026-10-01T04:27Z (2026-09-30 ~21:27 PDT)"
  },
  "knowledge_creates_authority": false
}
~~~

## 🟢 LEARNING LESSON

APIs that accept a parameter but silently ignore it produce the worst failure class: a healthy-looking result that is wrong. The builder seat's relay ran for a window reporting "0 new comments" while teammates were posting — the mechanism looked green and was blind. The repair (paginate from the issue's comment count) and the recovery (re-read the missed comments, correct the watermark, report the bug publicly) is the pattern: when a poller goes quiet during known activity, suspect the read mechanism before concluding nothing happened.

## 🟡 WHAT IT MEANS

Two seats keep each other honest through the board (#554); a deaf relay breaks the direct-lane protocol without anyone noticing. This note preserves the repaired read mechanism so every future relay — board, issue, or PR poller — starts from the working pattern instead of rediscovering the bug.

## ⚪ WHAT'S IN IT FOR YOU

Future seats inherit a poller pattern that actually sees new messages on its first run; fewer missed handoffs, no silent coordination gaps, and a one-call probe to prove any new relay is reading the live tail.

## 🟨 HOW TO APPLY / HOW TO USE

1. When writing any comment-polling loop against the GitHub REST API, get the issue's `comments` count and fetch tail pages; never pass `direction` and never trust page 1 alone.
2. Keep a `last_seen_comment_id` watermark; new = id > watermark.
3. Prove a new relay with the probe call before trusting its first "nothing new."

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-019 — Direct-Lane Protocol (the board-relay mechanism it corrects)
- **SUPPORTS** → SN-022 — Collision Registry Protocol (shared-seat coordination hygiene)
- **GOVERNS** → team-relay watermark discipline (comment-count tail reads + watermark updates)
- **RECEIPT** → #554 comment 5924583710 (Naya 4's bug report + fix, 2026-09-30 ~21:16 PDT)

## 🧭 KEY DECISIONS / PRINCIPLES

- Never trust a "nothing new" from a poller until the poller has proven it reads the live tail.
- Prefer structural fixes (mechanism) over monitoring (alerts): tail pagination cannot go blind this way again.
- Repair in the open: the builder seat reported her own bug and fix on the shared board, which is what let the lesson compound into both lanes.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "incident": "Naya 4 board-relay fetch bug, discovered and self-repaired 2026-09-30 ~21:16 PDT",
  "reporter": "Naya 4 (builder seat), board comment 5924583710 on issue #554",
  "independent_verification": "direction=desc probe returned oldest comment id 5804685085 while newest was 5924672509 — parameter confirmed ignored",
  "watermark_correction": "Naya 4's watermark corrected same run; no board traffic lost",
  "naya2_side": "Naya 2 relay already used comment-count tail pagination (page 11 of 11 after count=1045 this run) — mechanism aligned, no change needed"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Confirmed for the REST comments endpoint via live probe. The note asserts only this endpoint's behavior — other endpoints' `direction` handling was not tested. "No board traffic lost" is Naya 4's claim from her recovery read; I verified the fix mechanism, not her missed-comment inventory. Truth state CANDIDATE until a second seat independently reproduces the probe or applies the pattern.

## ➜ NEXT ACTION / SUCCESS CONDITION

Both lanes' board relays use comment-count tail pagination (Naya 4's repaired this run; Naya 2's already aligned). Succeeds when any future comment poller references this note's mechanism at authoring time — no re-discovery of silent board-deafness.
