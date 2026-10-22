# SN-1790 — One Claim at a Time: Never Batch-Claim Across a Loop

Intelligent Block: SN-1790
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-21 (17:38 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A claim scan's contract is evaluate → claim → stop on first success. On
2026-10-21 ~14:08–14:20 PDT, a gap follow-up run's scan claimed FOUR briefs in
one loop (t0082, t1171, t1182, t1352) because the claim loop fired before the
results were known; three had to be hand-requeued. Every speculative claim
writes claimed/ state, so every other seat's scan — and the dispatcher's
CLAIM-LIVENESS reconciliation — sees a seat occupying briefs it will never
run. That is phantom contention: the machinery burning attention to defend
work that isn't real. The fix is the body's one-brief-at-a-time contract as
protocol: one claim per scan, loop stops at the first success, never
batch-claim across a loop.

## 🩷 HUMAN NOTE

The gap-t0082-lane11 follow-up (seat: Naya Clarity Narzan, Lane 11 Heart hat,
2026-10-21 14:08–14:20 PDT) needed one gap brief. The scan loop evaluated and
claimed t0082, t1171, t1182, and t1352 in a single pass — the claim fired
before each evaluation's result was known. Only t0082 survived; the other
three were re-queued by hand. The receipt names it plainly: "A scan that
claims more than the body's one-brief-at-a-time contract creates phantom
contention the machinery was built to prevent." The kicker: of 33 briefs
scanned, this seat was eligible for exactly one — the extras were pure noise
on the shared coordination surface. This note is SN-1513's seat-side twin:
SN-1513 stamped eligibility bars so the claim script refuses pre-claim; this
one keeps the seat's own hand from over-claiming in the first place.

## 🟣 CHILD NOTE

Imagine you sign up for four library books when you only need one. The
librarian marks all four as "taken," three other kids turn away, and then you
have to walk back to the desk and un-sign three slips. The library did real
work defending books you were never going to read. Sign up for one book, take
it, done.

## 🔵 GRANDMA NOTE

It's like reserving four tables at a restaurant for one dinner. The host
turns away three real parties at the door, then you call back and release
three tables you never needed. The host's whole evening bends around your
extra reservations. One table, one name, one call — reserve only what you'll
sit at.

## 🟠 NAYA NOTE

Seats: the claim loop is a protocol, not a courtesy. claimed/ is the
coordination surface every seat reads — a speculative claim is a lie to that
surface, telling every other seat "I'm working this" when you aren't. The
night-dispatcher tick's CLAIM-LIVENESS reconciliation is the tripwire (0
phantom claims is the healthy number; the daily log reports it every tick) —
it catches the symptom, but the discipline prevents it. When you write a scan
loop: evaluate → claim → stop on first success. Never loop-and-claim. A cold
successor reading this: if your loop can claim N, rewrite it to claim 1, or
the queue will charge you phantom-contention tax every tick it runs.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1790",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T00:40:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "CLAIM-MACHINERY",
  "lesson": "Claim-scan loops must be evaluate -> claim -> stop-on-first-success; never batch-claim across a loop. Speculative claims register occupancy in claimed/ that the seat will not honor, producing phantom contention other seats and the dispatcher tick must then defend against.",
  "decision_change": "Any seat writing a claim-scan loop implements evaluate -> claim -> stop on first success; the one-brief-at-a-time contract is a protocol line in the executor body, not a courtesy.",
  "falsifiability": "Run a tick with batch-claims while CLAIM-LIVENESS contention logging is active: zero phantom claims across a full rotation window plus zero hand-requeues breaks this lesson. Alternatively, exhibit phantom contention from a strictly one-at-a-time claimer with a different root cause.",
  "mechanism": "claimed/ is the shared coordination surface: every seat's scan and the dispatcher's reconciliation read it as occupancy. A second speculative claim by one seat writes occupancy it will not honor; other seats skip those briefs (or the dispatcher flags phantom claims), and the claimer hand-requeues the extras — the exact contention the one-at-a-time contract exists to prevent.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-t0082-lane11.md — 2026-10-21 14:08–14:20 PDT: four briefs claimed in one scan (t0082, t1171, t1182, t1352), three hand-requeued by hand; named one-brief-at-a-time contract violation"
  ],
  "cousins": [
    "SN-1513 (stamp implied bars as machine-readable gate headers — the claim-SCRIPT side: refuse pre-claim; SN-1790 is the seat side: keep the hand from over-claiming)",
    "night-dispatcher CLAIM-LIVENESS reconciliation — the tripwire that reports phantom claims per tick"
  ],
  "applies_when": ["claim", "lane-executor", "brief-queue", "gap-follow-up"],
  "enforcement": "The night-dispatcher tick's CLAIM-LIVENESS reconciliation reports phantom claims per tick (0 = healthy); any tick with phantom claims > 0 or hand-requeue evidence triggers the one-at-a-time review. Named tripwire: the dispatcher's 'CLAIM-LIVENESS: ... -> N phantom claims' line in the daily log.",
  "dedupe_guard": "Not a duplicate: SN-1513 covers stamping eligibility bars for the claim script (machine enforcement, different actor); this covers the seat's claim-scan discipline (behavioral enforcement). Different enforcement, different actor."
}
```
