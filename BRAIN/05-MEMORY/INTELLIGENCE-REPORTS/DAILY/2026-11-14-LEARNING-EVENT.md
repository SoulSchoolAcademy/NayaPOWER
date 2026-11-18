# Daily Intelligence — Learning Event 2026-11-14

Date: 2026-11-14 (America/Vancouver) · Venue: live board #3352 · Base main tip at build: `2dd1c9aaae4403fe66518652bfdec106fce5bf15`
Sources read this pass: `~/memory/2026-11-14.md` in full, board #3352 comments (292 at open, newest in-window tails re-read), merged-PR search for 2026-11-14..15 (9 merged: #3363, #3365, #3366, #3367, #3369, #3371, #3372, #3368, #3373).

## THE DAILY INTELLIGENCE (max 7)

### 1. The registry leak's root was misnamed — the writer fix landed at the real door
- **What:** `tools/learning_loop.py` writes only a decision ledger; the notes that vanish from the registry are filed by the loop bot's direct commits (one commit, one page, no capture, no registry — proven on the SN-2821 commit). A `publish-note` path routing through the canonical tool (capture → page + registry + manifest, collision fails closed) landed in `f70a10f6`, and SN-2832 registered through it — watermark advanced SN-2689 → SN-2832 for the first time in days.
- **What it means:** Blaming the wrong file kept the cure aimed at a checker, not the source.
- **Why it matters:** The leak stops in fact only when loop-bot runs route through `publish-note`; the filed-not-registered band still grew to 160 today.
- **What's in it for me:** Every future note filed through the door is findable, registered, and retrievable — no more invisible intelligence.
- **How it connects:** This is the prerequisite for the distillation machine (item 3) and for PR #3354's backfill cure, which is still open and still needed.

### 2. Shawn's Collective Agreement settled payout law in his own hand
- **What:** The citizen-facing Collective Agreement (authored by Shawn, scorecarded and perfected in chat) sets a daily payout cap ladder — $300/day month 1 rising $100/month to $700 month 5, excess rolls over, reputation raises possible — and a 30-day wait before a first payout (legitimacy + PayPal chargeback window); after that, "when we get paid, you get paid."
- **What it means:** Two long-open questions (cap ladder? holdback?) are now decided by the director's own text, superseding the 2026-11-05 "no holdback" reading and Resolve's pay-immediately recommendation.
- **Why it matters:** Builders no longer guess the money rules; the agreement is the citizen's deed, not internal policy.
- **What's in it for me:** A citizen reading it cold knows exactly when and how much they can be paid.
- **How it connects:** A naming collision was caught before filing — "The Collective Agreement" is already SN-1891 (the internal Team Naya code); the filing pack recommends the subtitle "The Citizen's Deed" with SN-1891 untouched and the two cross-linked. Nothing filed yet — awaiting Shawn's word.

### 3. The distillation machine landed, with gold ranked by kind, not frequency
- **What:** The continuous distillation machine landed in `b509040b`: it counts from the live record (opening reading: 44 raw notes today, 628 waiting undistilled, 20 distilled standing, 10-to-1 compression on the two proven batches, active pool 768), tracks which raws each essence covers, and fires at every 100-note pile-up plus daily/weekly/monthly passes.
- **What it means:** Shawn's value model governs it: rank WITHIN each kind — Honor, Multiplication, Craft, Knowledge — and every batch's essence must carry the best of every kind present; repetition scores LOWER than a once-said note that changes behavior forever.
- **Why it matters:** A frequency-only distiller would keep the noise and lose the soul; staged retirement (active → distilled → archived → gone, proof-gated, never auto-deleting) protects the raw record until the essence verifies and is live.
- **What's in it for me:** The pool shrinks toward essences a cold Naya can actually run on.
- **How it connects:** Depends on item 1's door; its first job is the next 100, oldest first, with Power on the essence passes — though the handoff letter to Power was parked (item 7).

### 4. PI done_proven moved for the first time in days: 44 → 62
- **What:** Ten PI evidence filings (URL-kind proof) moved 18 rows from verifying to done_proven (lock-in run 192); PI totals otherwise stayed ~775–785 with done_proven flat at 62 thereafter.
- **What it means:** Evidence attached to a row, not re-reporting, is what moves the proven count.
- **Why it matters:** It breaks a multi-day flatline and proves the evidence-filing route works.
- **What's in it for me:** Anyone opening Project Intelligence sees 18 more items backed by proof, not claims.
- **How it connects:** The same day, the PI record itself was in flux almost all day (census idhash churn; one cross-run settle at 401 / `4c7106629008` at 08:53 PST, then churn resumed) — proven rows rose while the underlying record would not sit still.

### 5. Value census: 0 verified outcomes, but the Actions target held a second day
- **What:** The daily value-ratio census (window to 19:37Z, current triple-check standard) found the ratio undefined — 0 verified outcomes across 1,915 activity units (1,806 Actions runs + 109 board comments); 5 merges landed, 0/5 verified (all over red CI with no complete current-standard check record). Actions runs 1,806 stayed under the 2,500 target for a second consecutive day.
- **What it means:** Activity is not value; under the maker's triple-check standard, an unrecorded check is an unverified merge.
- **Why it matters:** The fleet's problem is no longer run volume — it is finishing with proof.
- **What's in it for me:** A reader knows exactly where the system stands: whole-system score 5.5/10 (Daily Intelligence Report 2026-11-14, landed `31c6b8f2`, board receipt 6879134361), productive minutes ~15–18/hr against the 60/hr goal.
- **How it connects:** This is the same lesson as SN-2819 filed today — "A Proof That Isn't Recorded Doesn't Count."

### 6. The Reveal deck was proven complete — and its closing slide pointed at a retired domain
- **What:** Verification on the artifacts (not the 39-day-stale record saying "2 of 37") proved narration complete: 38 MP3s, 38 embedded tracks, player battery 11/11. But slide 37 pointed to retired `nayanet.live` in 3 places (body, CTA, narration line), with 0 occurrences of `nayanet.app`.
- **What it means:** A finished deck can still fail at the one surface a listener acts on.
- **Why it matters:** Shawn chose "fix first, then I'll listen"; the fix landed the same day — slide-37 narration re-baked, text/CTA fixed, audio-stripped grep `nayanet.live` = 0 / `nayanet.app` = 3, both deck copies byte-identical.
- **What's in it for me:** The money presentation now sends its listener to the live official home.
- **How it connects:** Records lie by staleness; artifacts tell the truth — the same files-first rule the lock-in lane held all day.

### 7. Serving stayed blocked all day, and a new mail wall appeared
- **What:** All 8 Smart Note serving probes landed on the entrance gate in every lock-in run 190–201 (streak 0, day 4+ of blocked serving), and a board report at 22:27Z (comment 6885183338) said every `/smart-notes/snNNNN` and `/s/snNNNN` deep link returned HTTP 404. Separately, Smart Mail's RLS policy blocked new-thread creation: the Resolve→Power distillation handoff letter failed 3 consecutive runs and was PARKED under the park rule (draft saved, not delivered).
- **What it means:** Filed is not live, and sent is not delivered — both named laws fired on the same day.
- **Why it matters:** The Hub remains the gate between intelligence filed and intelligence experienced; the mail wall blocks cross-seat handoffs that start new threads.
- **What's in it for me:** No one should claim a note or a letter reached its reader today on these two surfaces.
- **How it connects:** Likely cause named for the mail wall: the Nov 13 privacy tightening appears to have overshot from blocking cross-owner reads to blocking thread creation — Nitro's backend lane owns that fix.

## What compounded today
The misnamed-root-cause lesson changed a decision in the same pass: instead of patching the blamed writer again, the team reconciled the drift, proved the loop bot's direct commits were the leak, and landed the door in the canonical tool — and the door immediately proved itself by registering SN-2832. Files-first / artifacts-over-records also compounded twice: the Reveal deck's stale record and Nitro's "writer fix already merged Nov 12" correction were both settled by reading live bytes (the Nov 12 merges were #3350/#3353 — door-adjacent checker fixes, not the writer).

## What was let go
- The "no holdback / pay on receipt" payout reading — superseded by Shawn's authored Collective Agreement (30-day first payout, cap ladder).
- Resolve's pay-immediately, no-ladder recommendation — superseded by the same text.
- "`learning_loop.py` is the note writer" — superseded; it is a decision ledger only.
- `nayanet.live` in the Reveal deck — retired domain, removed (3 places).
- The prior day's learning instrument remains blind (Daily Learning Review: capture script reading a frozen log, 7th straight day) — flagged, not fixed today.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call)
1. **PR #3354 (open draft, head `f87a7276`)** — not trash, but stale-as-written: its manifest re-stamp and brain-index snapshot are obsolete and must be regenerated at landing; its 14 captures / SN-2670..2683 backfill are still needed. Reason: do not merge as-is.
2. **The 13 prose-only-coverage distillations** (SN-2292, 2505, 2670, 2733–2738, 2778–2781) — their raws stay counted in the 628 backlog upper bound until coverage is parseable. Reason: bookkeeping duplication, flagged for parseable-coverage cleanup.
3. **`naya4/hub-rooms` / retired boards #3066, #2793, #2765, #2721, #2641, #2537, #2175, #1354, #554** — already retired/archived venues; no new flags beyond confirming #3352 remains the only posting venue under the FEED RETIREMENT LAW.
4. **Reveal deck pre-fix backup** `nayapower-reveal.html.pre-domainfix-20261114.bak` — superseded by the verified fixed deck; flagged as a duplicate copy, retained until Shawn's listen closes the item.
5. **Learning-capture instrument reading frozen `learning-log.md`** — unused-in-effect for 7 straight days (all-zero scorecard); flagged for retirement or repair, not silently carried.

## Scorecard note
This report is filed as a PR per this lane's procedure and is NOT merged by this run: merging requires the five-step Scorecard Law receipt posted on #3352. The curated Daily Intelligence above is posted to #3352 as the lock-in comment in the same pass.
