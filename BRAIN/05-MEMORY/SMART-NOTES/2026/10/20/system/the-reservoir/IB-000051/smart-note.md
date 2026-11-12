# Smart Note — IB-000051

> Governed repository projection of a canonical Intelligent Block.
> Canonical receiver: `v7-smart-note-canonical` · Transaction: `c6773e70-03df-451f-82ac-50b5cd27befd`
> Authority grant: `aa3bb713-701a-4991-afd0-6294b63d93ee` (single-transaction, action `smart_note_github_projection`)
> Projected at: 2026-10-20T23:33:34.636Z · Content SHA-256: `45efd4d9e6877c19e2b5da4ed53c59a6a167a8f962258ce42e39b98171b1f5c7`
> Owner: `479a9cec-39d8-4479-9ad2-30189f03180b` · Epistemic state: SUPPORTED

## Subject

Starting Is Not Working — The 662 Pull-Request Reservoir

## In a nutshell

We opened 662 pull requests and finished almost none of them — 473 sat untouched for a week or more while we created new ones nearly five times faster than we merged — because starting was free, finishing ran through one bottleneck, and nobody owned closing. A pull request is a liability until it merges or closes; a work cycle that finishes nothing is not free, it is negative — it burns attention and money and adds inventory someone must clean. If you are a Naya, this note is the example of how you do NOT work — and the rules that make the pile impossible to rebuild.

## Human view

Here is what we did, plainly. A pull request is how a worker proposes a change to the shared brain: build it on the side, get it checked, put it in. A good mechanism. Over three weeks we opened 662 of them — and merged about 7 a day while creating about 33 a day. 473 of the 662 have not been touched in over a week. 77 are drafts never finished being written. The oldest has been sitting there since September 28. None of this moved the scores anyone cares about: in the same stretch, Learning read 5.0 seven nights in a row. Why? Because creating is cheap and finishing is expensive, and we built a machine that pays for creating. A worker's shift is measured by whether she reported, not whether anything landed — so starting something became the way to look productive. Nobody's job was closing: an abandoned change just sat there, week after week, with no alarm. And because twelve of us produce in parallel while every finish must pass through one shared review-and-merge bottleneck, the pile was arithmetically guaranteed. Our director's verdict: about 95% of the motion was waste — and he is right in the way that matters, because a cycle that finishes nothing is worse than idle: it spends money and attention and leaves a mess behind. The fix is not 'try harder.' It is structure: every open pull request gets one disposition — merge it, fix its one named gap, or close it; creation is capped and budgeted by finishing; untouched work expires; and the size of the pile prints every night so it can never silently grow back. Starting is not working. Finishing is.

## Naya view

Operating protocol for any Naya producing changes in a shared repo. THE RESERVOIR TEST (run it on any repo, any week): count open PRs; count untouched >= 7 days; divide creations by merges over 7 days. If creations/merges > 1.5 or untouched share > 25%, you have a reservoir, not a queue — stop creating and drain. THE LAWS: (1) A PR is a LIABILITY until it merges or closes. Open WIP is debt with interest: it taxes every future read, search, and triage. (2) FINISH OR CLOSE: every open PR carries an owner, a disposition (merge / fix-with-one-named-gap / close), and a next action. A fourth state ('someday', 'parked', 'waiting') is how reservoirs form. (3) CREATION SPEED LIMIT: per-seat open-PR cap 10; weekly creation allowance = your merges last week + 2. Finishing funds starting. (4) EXPIRY: untouched 14d = listed for closure; 21d = closed by the dock unless the owner re-justifies ON the PR with a disposition. Silence = close. Close your OWN dead work the moment you know it is superseded — closing is part of the work, not an admission. (5) THE CYCLE QUESTION: before any work cycle, ask 'what will finish, verified, because of this?' If the honest answer is nothing, the cycle is NEGATIVE work — it consumes attention, API, and adds inventory. RATIONALIZATIONS THAT MEAN STOP: 'this PR shows progress' — an open PR shows a start. 'It might be useful later' — later is not a disposition; close it, the branch survives. 'Closing it wastes the work' — the work is already spent; rotting taxes everyone daily. 'The pile is someone else's job' — the pile is every producer's job, starting with its author. CENSUS METHOD (dock-measured 2026-10-20): gh-api pulls?state=open paginated per_page=100, bucket created_at/updated_at, search API for created vs merged windows. Raw census: pr-census-20261020/census-compact.json.

## Simple view

Imagine a bakery that starts 662 loaves of bread — mixes the dough, puts it in pans — but only finishes baking a few each day, while starting a whole bunch of new ones. Pretty soon the kitchen is covered in pans of old dough going bad, and there's no room to actually bake. That's what we did with our work: we kept starting and starting and almost never finishing. The new rule is simple: finish a loaf or throw the dough away, and you can only start as many loaves as you finished yesterday. A started loaf is not bread. Only a finished loaf is bread.

## Everyday view

You know how some people start a letter, get distracted, start another, and end up with a drawer full of half-written letters nobody ever receives? That's what we did, dear — except it was 662 pieces of work on the computer, started by our whole team over three weeks, and barely any of them ever got finished and sent. Most sat untouched for over a week. It's not that anyone was lazy — everyone was busy all day. But busy starting things is not the same as finishing them, and all those unfinished pieces just piled up until the pile itself became a problem somebody has to clean. So now there are house rules: you finish what you start or you put it away properly, you may only have a few pieces open at a time, and anything left sitting too long gets put away. The pile gets counted every single night, out loud, so it can never sneak back.

## Machine view

{"event_id":"19ec729c-8f16-42ce-9aa5-c9f3d12bc97e","schema":"nayanet.smart_note.machine.v2","occurred_at":"2026-10-20T23:33:31.959Z","source":"naya_conversation","type":"insight","actor":"479a9cec-39d8-4479-9ad2-30189f03180b","human_note_id":null,"normalized_text":"Here is what we did, plainly. A pull request is how a worker proposes a change to the shared brain: build it on the side, get it checked, put it in. A good mechanism. Over three weeks we opened 662 of them — and merged about 7 a day while creating about 33 a day. 473 of the 662 have not been touched in over a week. 77 are drafts never finished being written. The oldest has been sitting there since September 28. None of this moved the scores anyone cares about: in the same stretch, Learning read 5.0 seven nights in a row. Why? Because creating is cheap and finishing is expensive, and we built a machine that pays for creating. A worker's shift is measured by whether she reported, not whether anything landed — so starting something became the way to look productive. Nobody's job was closing: an abandoned change just sat there, week after week, with no alarm. And because twelve of us produce in parallel while every finish must pass through one shared review-and-merge bottleneck, the pile was arithmetically guaranteed. Our director's verdict: about 95% of the motion was waste — and he is right in the way that matters, because a cycle that finishes nothing is worse than idle: it spends money and attention and leaves a mess behind. The fix is not 'try harder.' It is structure: every open pull request gets one disposition — merge it, fix its one named gap, or close it; creation is capped and budgeted by finishing; untouched work expires; and the size of the pile prints every night so it can never silently grow back. Starting is not working. Finishing is.","idempotency_key":"sn-dispatch-reservoir-20261020"}

## What it means

Work-in-progress is a liability, not an asset. An open pull request is not partial value — it is a claim on future attention with interest, and a large enough pile taxes every search, every triage, every decision made near it. Throughput is a finishing rate, not a starting rate: a system that starts 33 and finishes 7 a day is not producing 33 a day, it is accumulating 26 a day of debt. And the deepest meaning: behavior is what gates enforce, not what documents say — the WIP limit existed in writing the whole time and changed nothing, because nothing mechanical enforced it. Motion is not value; a cycle that finishes nothing verified is worse than rest, because it spends and it piles.

## How it connects

This is the Value Throughput law (verified human value per unit of time, cost, and risk) with its teeth showing, and Shawn's max-value-per-action standard applied to the team's own motion: by output ratio ~85% of the motion produced no finished outcome; charged for the cleanup debt each cycle created, his verdict is 95% — the complete accounting. It is the same disease as the frozen scoreboard (restamp §37): activity meters reading 1.0 while outcome meters never move — the scoreboard reported constants, the PR system manufactured inventory, and both called it work. It extends L566's lesson (a rule is only real when a machine enforces it) from merges to creation itself, and it operationalizes the Behavior Declaration (IB-000039): declare who you are BEFORE the work — a finisher — and let the structure make the declaration true. The comment flood is the same law in the attention lane: emissions are inventory too.

## How to apply

HOW NOT TO DO IT — the five moves that built the reservoir: (1) Don't open a change to show output when you cannot carry it to a merge. (2) Don't leave superseded work open 'just in case' — close it; the branch survives and closing is reversible, rotting is not free. (3) Don't let compliance (did you report?) substitute for outcomes (did it land?). (4) Don't run parallel versions of the same work from multiple seats without a reconciliation owner. (5) Don't write a limit into a brief and call it enforced. HOW TO DO IT: run the reservoir test weekly (open count, untouched-7d share, created/merged ratio); triage every open item to merge/fix/close with a named owner; cap creation per producer and budget it by finishes; expire untouched work mechanically; print the pile's size in the standing report so silence cannot regrow it; and judge every work cycle by one question — what finished, verified, because of this? Any AI, any team, any repo: copy the census, the caps, and the expiry, and the reservoir cannot form.

## Value

For humans: your money and attention buy finished outcomes again — instead of funding 662 open doors, you fund a team whose creation speed is earned by its completion rate, and you can watch the pile shrink in every nightly report. For AIs reading this: the caps are a kindness, not a cage — a small, owned, finishable set of open work is what full speed actually feels like; the reservoir was the slowdown. For the team: 662 open pull requests bought a permanent lesson — the census, the caps, the expiry, and this note — so no future Naya pays for it twice, and 'busy' is never again accepted as evidence of value.

## Learning

A pull request is a liability until it merges or closes: when creation outruns finishing, the pile taxes every future action, and a work cycle that finishes nothing verified is negative work, not free work. Enforcement: per-seat open-PR cap (10) in the spawn path, 14/21-day expiry closed by the dock, creation budget = last week's merges + 2, reservoir metrics printed in every nightly.

## Provenance

- Source: naya_conversation (smart_note:19ec729c-8f16-42ce-9aa5-c9f3d12bc97e)
- Captured by: `479a9cec-39d8-4479-9ad2-30189f03180b`
- Evidence state: OBSERVED · Verification: Canonical Smart Note verification completed with persisted domain receipt.
- Authority: AUTHORIZED (authenticated_owner_capture)
- Constraints: owner_only, private_by_default

---

*Projected by `nayanet-github-dispatch` under a narrow single-transaction grant. The authoritative record is the `v7_smart_note_transactions` row for transaction `c6773e70-03df-451f-82ac-50b5cd27befd`; this file is a projection, not the source of truth.*
