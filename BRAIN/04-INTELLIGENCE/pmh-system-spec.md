# Productive Minutes Per Hour (PMH) — The System Specification

**Ordered by Shawn Vibert, in his own words, in main chat 2026-11-10 ~18:19 PST.**
**Written by Naya Power. Status: SPEC ONLY — the system is NOT working yet. The tracker and the dispatcher are being built by sibling agents in parallel. This spec becomes real only when the first measured hour lands.**

---

## 1. The stat — one number that tells the truth

**PMH = Productive Minutes Per Hour.**

It answers one question: *in the last hour, how many minutes of our time actually produced verified, useful work that helped us?*

- **One agent, working perfectly, produces 60 productive minutes in one hour.** That is 60/60 = 100% efficiency. That is the **10 out of 10**.
- **PMH is counted across ALL agents in the hour.** If three agents each produce 30 productive minutes, the hour's PMH is 90. That is 90/60 = **150% efficient**. Shawn's words: he loves that, and he is cool with it.
- **Efficiency % = PMH ÷ 60 × 100.** 60 PMH = 100%. 90 PMH = 150%. 30 PMH = 50%.
- **Why it is the one number:** every other number we track is a count of things (notes filed, PRs merged, items in flight). PMH is the only number that measures whether the time itself was spent producing. If PMH is 60 or better, everything else works out — we are productive 24/7, we actually get things done, we actually finish. If PMH is low, nothing else matters, because the hours are going nowhere.
- **It does not matter how many nights we use.** The number of agents, the number of hours, the number of runs — none of that is the goal. The goal is that the system works: productive every minute of every hour, producing valuable outputs. The system is the point, not the headcount.

---

## 2. The definition — what counts as a productive minute

**A productive minute is one minute of agent wall-clock time that directly produces a VERIFIED, USEFUL, LANDED output — or a verified step that is a necessary part of producing one.**

### What counts

- A file or piece of code landing, verified by read-back (the bytes on the live path match the bytes we wrote).
- A live verification read that confirms a landing (a curl, a rendered check, a live click that proves the thing works where it can be seen).
- A mail reply or message that lands and moves a job forward (a receipt, a correction, a decision that unblocks a seat).
- A fix that lands and is verified (the defect is gone on a live re-read, not just in a report).
- A decision recorded in Project Intelligence and on the board that closes a loop (the item moves state with its receipt).

### What does NOT count

- Waiting on a tool, an API, a browser, or a page to respond.
- Retrying a failed call. Retry minutes are waste, even when the retry eventually succeeds.
- Re-reading the same record without new information.
- Writing a report about work not done.
- Idle time between jobs — an agent with nothing to do is producing zero, and the system must give it work or admit the gap.
- Time blocked on a human gate (a merge, a deploy, a ruling) — the minutes spent waiting do not count, even though the gate itself is legitimate.

### The verification gate

**A minute counts ONLY when its output is verified** — by a live read, a different-seat check, or a landed receipt. **Unverified work = 0 productive minutes until verified.** A claim is never a count.

### The anti-gaming rule

- Never count unverified work.
- Never count a report about work as work. The report is the receipt, not the product.
- Never round up. A minute is a minute. A partial minute of real output is counted as the minutes actually spent on it, and no more.
- Never count the same output twice. One landing, one count, even if three seats look at it.

---

## 3. The architecture — how the system works

### The Ready Queue

A list of jobs that are **briefed, unblocked, and not in flight**, ranked by Shawn's execution order 1–27 (Project Intelligence first, then voice, affiliate, membership, and so on down the list). A job enters the queue only when its brief is complete enough that an agent can start without asking a question. A job leaves the queue the moment it is picked up. The queue is the single source of "what is next" — no agent ever has to ask what to do.

### The Dispatcher

Every 15 minutes the dispatcher refreshes the queue, checks what is in flight, and spawns agents up to the **WIP cap of 3 jobs out at once**. It respects the status-only override: while the override is in force, no workers spawn and the dispatcher does measurement only. The dispatcher never spawns a duplicate of a job already in flight. Its job is to keep the lanes full and never let an agent sit idle while a ready job waits.

### The Lanes

Every job flows through four lanes in order, with **instant handoffs** — no lane waits for a reply from the next:

1. **Maker** — builds the thing, lands it, proves it by read-back.
2. **Verifier** — a different seat checks the exact landed version against the brief, live, and records PASS or every defect.
3. **Eye** — a rendered check at the real address, desktop and phone, by a seat or by Shawn's own eye.
4. **Filer** — the record lands in Project Intelligence and on the board the same pass, with the receipt.

A lane that finishes hands off immediately. A lane that is blocked logs the block and moves on (see Idle Killer). Nothing waits for a human reply to keep moving.

### The Idle Killer

**No agent ever sits.** If an agent is blocked — waiting on a tool, a gate, a merge, a human — it logs the block with the exact reason and the exact thing that would unblock it, and it is **reassigned to the next ready job immediately**. The block stays on the record as waste (see Waste Log), and the agent keeps producing on something else. Sitting is the most expensive waste there is, because it burns the one resource that never comes back: the minute.

### The Scoreboard

A live board showing PMH for **the current hour, the day so far, and the trend** (this hour vs last hour vs yesterday same hour). It is recorded in Project Intelligence daily, so the trend is a record, not a memory. The scoreboard is the instrument Shawn reads to know whether the system is working. It shows the number, the efficiency %, and the top three waste categories for the hour.

### The Waste Log

Every non-productive minute is categorized, so the system can drive waste down instead of just watching it:

- **wait** — waiting on a tool, API, browser, or page.
- **retry** — retrying a failed call.
- **re-read** — re-reading the same record without new information.
- **blocked** — blocked on a human gate (merge, deploy, ruling).
- **idle** — no ready job, no assignment.
- **report-only** — writing about work not done.

The Waste Log is reviewed every morning. The top three waste categories are attacked first — that is how PMH climbs.

---

## 4. How many agents — the honest reasoning

The question Shawn asked: how many productive agents does it take to be productive every minute of every hour?

The honest answer: **the number is not the point. The system is the point.** An always-ready queue, instant handoffs, and idle reassignment produce more than a crowd of agents waiting on the same gates.

The starting shape, to be tuned by measured PMH and never fixed forever:

- **4 lanes × 3 jobs in flight (the WIP cap) = ~12 agents working at once.** Each job in flight has a maker, a verifier, an eye, and a filer — not all active in the same minute, but each lane staffed so the handoff is instant.
- **Plus 2 measurement and coordination seats** — the decide-and-act waves and the mail sweeps — that keep the record current and the queue honest.
- **Total: ~14 agents.**

More than that queues on the same gates and adds coordination waste: Shawn's merges, branch protection, rendered checks, and the single live address are all serial. Ten agents waiting on one merge produce the same PMH as three agents waiting on one merge, and the extra seven add coordination minutes that count as waste. The WIP cap exists for this reason.

**The tuning rule:** if measured PMH is below 60 and the Waste Log shows "idle" as a top category, add lanes. If PMH is below 60 and the Waste Log shows "blocked" as a top category, the gates are the problem, not the headcount — do not add agents, fix the gate. If PMH is above 60, the system is working; hold the shape and let the trend confirm it.

---

## 5. The gates and hard limits

These are never crossed, no matter what PMH says. A productive minute earned by breaking one of these is not productive — it is damage.

- **No PR workflow, ever.** No building to a PR branch and waiting for a pull. Changes go direct to the live path under the PI Code, with proof after landing by rendered check.
- **No production database writes.** No schema or DDL changes, no ledger appends, no RLS changes, no backfill applies.
- **No money movement, no payout promises, no public pricing in Shawn's name.**
- **No credentials, secrets, merchant keys, or security and authority rule changes.**
- **No deletions and no rewriting history.** Project Intelligence notes are append-only. A duplicate is owned in a correction, never silently deleted.
- **No self-merge as a ceremony.** The PR merge step is abolished; direct landing under the Code replaces it, with after-check review.
- **Never claim done or live before a rendered re-read at the real address.**
- **A merge waits for the rendered verdict, never the static one alone.** This is the &cb= lesson, learned the hard way: PR #3331 (the identity front-door fix) was merged before its rendered check came back, and the defect landed on main — the `&cb=` cache-buster broke both deciding PostgREST reads (HTTP 400), and the 409 branch fell through to `{status:'ok'}`, so a taken alias walked a second device into the walk as if the claim had succeeded. The repair, PR #3335, was merged 01:58:44Z on 2026-11-11. A static PASS is never enough. The rendered verdict comes first, or the merge waits.

---

## 6. The baseline — the last hour, honestly estimated

**Baseline hour: 17:19–18:19 PST, 2026-11-10. Estimate: roughly 40–50 productive minutes. Marked ESTIMATE — not a measurement.**

Method: the run files and the daily log entries for that hour (`~/memory/2026-11-10.md`, entries 17:23 through 18:17 PST).

What the hour actually produced (verified outputs):
- PI notes n=475, n=476, n=477 landed (tail-verified), with matching board #3066 comments.
- Nitro Intelligence Loop run 115 read in full (25,401 chars, 13 chunked reads) and run 116 read in full (5,611 chars), with in-thread replies.
- The live feed verified by Power's own read: HTTP 200, 6,583,817 bytes, 861 cards, newest SN-2654 — the 338-card regression closed.
- The main tip verified by Power's own GitHub API read (then `07d4af3e7`, now `a55ae0f5` after the #3335 merge).
- A whole-board state delivered to Shawn in main chat, answering his 17:55 PST status question.

What the hour did NOT produce (measurement, not output):
- The decide-and-act waves at 17:23 and 17:53 were status-only — measurement while 111 items were in flight, no workers spawned, no output.
- The mail sweeps at 17:32, 17:47, 18:02, and 18:17 were mostly receipts and verification — necessary coordination, but not output in themselves.
- The fill-completion driver at 17:56 was status-only.

So the hour was mostly a single lane — the main seat reading, verifying, recording, and delivering — with the waves and sweeps doing measurement around it. Roughly 40–50 of the 60 minutes produced verified output; the rest was measurement, waiting, and coordination. That is the honest picture, and it is why the baseline is an estimate: **the tracker gives the exact number going forward.**

---

## 7. How it runs — the daily loop and the weekly tune

### The daily loop

- **Every hour:** the tracker records PMH for the hour and the waste categories.
- **Every morning state:** the scoreboard is reviewed — PMH for yesterday, the trend, and the top three waste categories. The top three are attacked first, before any new work is started. A waste category that stays in the top three for three days running gets a fix as a tracked item, not a note.
- **Every day:** the scoreboard is recorded in Project Intelligence, so the trend is a record.

### The weekly tune

- **Once a week:** the WIP cap and the lane count are adjusted **by measured PMH, never by feel**. If PMH is below 60 and idle is the top waste, add a lane. If PMH is below 60 and blocked is the top waste, fix the gate. If PMH is above 60 for the week, hold the shape.
- **The bar never moves:** 60 PMH is 10/10. It is not renegotiated because a week was hard. If the system cannot reach 60, the system is changed until it can — the bar is the bar.

### What "working" means

The system is working when the first measured hour lands at 60 PMH or better, verified by the tracker, with the Waste Log showing where every non-productive minute went. Until then, this spec is a plan, not a result. **Do not present the system as working until the tracker and the dispatcher are built and the first measured hour lands.**
