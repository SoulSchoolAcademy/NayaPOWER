# The Free Tier Wall — Count Your Writes

SN-2937 · SYSTEM

**Created:** 2026-11-16 06:15Z / 06:26Z

**Paired Naya Note:** NN-20261116-the-free-tier-wall

## Hook

One thousand writes a day, account-wide — and every completion writes five times. Two hundred test walks and the whole system stops joining. Test traffic counts. The free tier is a wall, not a floor.

## Nutshell

Shawn's night, 2026-11-16 06:15–06:26Z. The captain's own eye walks (fresh citizens capteye1 at 390, capteye2 at 1851×1009, capteye3 at 390 on retry) ALL failed at the building step — "Something went wrong building your world." with a "Try again" button; Try again also failed. The retry used the fix checker's EXACT answers and still failed — answer content ruled out. Console: 0 errors — the page catches the failed completion call and shows the error screen silently. Root cause pinned by the captain's own curls: POST /api/welcome/complete = HTTP 500, Cloudflare error 1101 (worker threw) — twice, minimal payload and complete UI-shaped payload. The endpoint WORKED minutes earlier: the fix checker's five walks built fine 05:51–06:03Z. The break arrived AFTER ~06:03Z, on unchanged page bytes — no new citizen could complete the walk. Endpoint-fix coordinator f96aab13 COMPLETED 06:24:59Z. Root cause proven, not guessed: the account hit Cloudflare KV's Workers Free daily write limit (1,000 writes/day, account-wide). The complete handler's first unguarded `WELCOME_ASSETS.put` threw → worker 1101. Deployed bytes were the unchanged 05:50:27Z deploy; binding present and correct — NOT the Nov 14 wipe, NOT a code change, NOT Supabase (handler run locally in Node with stub KV returned HTTP 200 with pages; Supabase behaves as designed — projects insert succeeds, citizen_worlds/page_about 401 RLS → kv-fallback). A throw-capturing probe worker caught the exact throw: "KV put() limit exceeded for the day." Cloudflare KV API independently confirmed: direct write → HTTP 429, error 10048. Quota resets 00:00 UTC. This worker does 5 puts per completion, so ~200 test completions across all seats today exhausted it — it broke right after the checker's 06:03Z walks. FIX DEPLOYED 06:23:50Z (deployment 524e957d, sha f4913be8): the three WELCOME_ASSETS.put calls in POST /api/welcome/complete now go through a kvPut guard — a put failure returns HTTP 503 {"ok":false,"error":"welcome store unavailable: <reason>"} instead of an uncaught 1101. Diff +608 bytes only. Receipts: POST fresh aliases fixlive3/fixlive4 → HTTP 503 naming the cause (opaque 1101 gone); GET complete?alias=fixchkone → HTTP 200, stored record intact; three served page shas UNCHANGED after the fix (/ c85e91ce · /welcome 52d8a7aa · /identity.html 1b8fd1d1). NO CHECKER DISPATCHED, deliberately: no KV write on this account can succeed until the quota resets 00:00Z 2026-11-17, so a cold checker now would FAIL at the building step through no fault of the fix and prove nothing. One List free-walk-hub-handoff-20261116 re-due 2026-11-17T01:00:00Z; one-time schedule `handoff-reproof-after-kv-reset`, runonce 2026-11-17T00:30 UTC. The same wall blocked the thank-you fix (coordinator 5ddcb557, NOT PASS 06:27Z — built and lab-proven, upload blocked; resume schedule `thankyou-resume-after-kv-reset`, 2026-11-17T00:45 UTC) and the PI state-publish (HTTP 429 on the KV PUT, 06:10Z, 06:25Z, 06:40Z, 06:55Z, 07:10Z — the intelligence room state.json stays stale). DURABLE FIX OFFERED, AWAITING HIS HAND: Workers Paid $5/month = 1M KV writes/month removes the wall permanently; captain presented two options in chat (switch to paid / stay free and wait for midnight). No answer recorded yet. Until then any busy test day can exhaust the quota again — test traffic should be counted (5 puts per completion).

## Human

The system broke without anything breaking. No code changed, no binding wiped, no deploy failed — the page bytes were identical, the checker had passed five walks an hour before, and then a new citizen could not finish joining. The cause was arithmetic the system never counted: 1,000 writes a day for the whole account, 5 writes per completion, ~200 test completions across all seats, and the wall arrived mid-night. That is the lesson: a free-tier limit is not a floor you stand on, it is a wall you hit — and you hit it at the worst moment, right after a PASS, which makes the PASS wrong about the present. Two disciplines follow. First, count test traffic: every completion, every checker walk, every probe writes — five puts a time — and the budget is shared by every seat, every lane, every job on the account. Second, fail honestly: the fix does not pretend the write succeeded — the guard returns 503 naming the cause, so the next failure says what is wrong instead of failing silently behind a caught error and a "Try again" button. And the structural flag stands: 1,000 KV writes a day is a hard ceiling for a system whose every request writes several KV keys — fewer writes per request (rate counters and token indexes into the Durable Object) or the Paid plan. The Paid plan is his hand, offered, awaiting his word — $5 a month against a wall that stops citizens joining.

## Child

Imagine a notebook that only lets you write 1,000 words a day — and every time someone joins, you have to write 5 words! After 200 friends join, the notebook says "NO MORE!" — and the next friend can't join at all, even though nothing is broken! That's what happened. So now we count our words carefully — and we ask for a bigger notebook!

## Grandma

It's like this, love — there's a little book that only holds a thousand notes a day, and every new person costs five notes. The team was so busy testing that they filled the book by midnight — and then nobody new could join, though nothing was actually broken. So now we count the notes, and we fail honestly — if the book is full, we say so plainly instead of pretending. And a bigger book costs very little, if he says yes.

## Naya

The free tier is a wall, not a floor. One thousand writes a day, five per completion — two hundred test walks and nobody new can join. Count test traffic. Fail honestly — 503 naming the cause, never a silent 1101.

## What it means

- **THE WALL:** Cloudflare KV Workers Free — 1,000 writes/day, account-wide, all seats and lanes sharing one budget. Resets 00:00 UTC.
- **THE MATH:** the walk's complete handler does 5 puts per completion — ~200 test completions exhausted the day. It broke right after the checker's 06:03Z PASS walks, on unchanged bytes.
- **THE SYMPTOM:** POST /api/welcome/complete → HTTP 500, error 1101; the page catches it silently and shows "Something went wrong building your world." — 0 console errors.
- **THE FIX (deployed 06:23:50Z):** kvPut guard — put failure returns HTTP 503 naming the cause instead of an uncaught 1101. Diff +608 bytes; page shas unchanged.
- **THE DISCIPLINE:** no cold checker dispatched until after the reset — a checker now would fail through no fault of the fix and prove nothing. Re-proof scheduled 00:30Z Nov 17.
- **THE SPREAD:** the same wall blocked the thank-you fix upload (NOT PASS 06:27Z, resume 00:45Z Nov 17) and five PI state-publishes (429, 06:10–07:10Z — intelligence room state.json stale).
- **THE DURABLE FIX (his hand):** Workers Paid $5/month = 1M KV writes/month. Offered 06:26Z, awaiting his word. Structural alternative: fewer KV writes per request (counters + indexes into the Durable Object).

## Why it matters

A system that stops citizens joining without anything breaking is a system whose limits are invisible to the people running it. The wall was hit because nobody counted — and the count is the lesson: every write on a shared free tier is a shared budget, and test traffic spends the citizens' budget. The honest-failure half matters as much: a silent catch that shows "Something went wrong" and a "Try again" that also fails is the system lying by omission. A 503 that names the cause is the system telling the truth, even when the truth is "we are full until midnight". And the Paid question is now a real decision with a real price: $5 a month against a wall that stops joining.

## What changes now

1. Test traffic is counted — 5 puts per completion, one shared 1,000/day budget across all seats and lanes.
2. KV put failures fail honestly — 503 naming the cause, never a silent 1101 behind a "Try again" button.
3. No cold checker is dispatched while the quota is exhausted — a verdict that cannot pass proves nothing.
4. Re-proof is scheduled after the reset (handoff 00:30Z, thank-you resume 00:45Z, Nov 17).
5. The durable fix — Workers Paid $5/month, 1M writes — is his hand, offered and awaiting his word.
6. The structural alternative is named: fewer KV writes per request, counters and indexes into the Durable Object.
