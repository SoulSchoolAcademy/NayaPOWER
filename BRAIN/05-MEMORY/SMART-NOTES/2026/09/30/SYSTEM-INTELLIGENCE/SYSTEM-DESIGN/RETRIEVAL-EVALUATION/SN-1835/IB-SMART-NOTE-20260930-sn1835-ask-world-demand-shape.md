Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Demand on the ask-world retrieval surface is 72.9% operational, not exploratory: 102 of 140 analyzed query rows (t1296) are lane-N status pulls, all answered with the identical six-section snapshot; only ONE row (0.7%) is a natural-language advisory question — the demand the brain is barely tuned for is the demand that will dominate once humans, not lanes, are the askers. And the log lies by omission: a single synthetic test-harness burst supplied 50 of 71 rows (70.4%) in one window, so any tally that doesn't provenance-filter first measures the harness, not the askers. Hypertuning therefore answers two questions — (a) serve the dominant machine-shaped pull (atomic lane snapshots, standalone sections) fast and cheap, and (b) build the composed-answer capability for the prose question — and hypertuning GO/NO-GO stays WAIT until origin='emergent' rows appear in the log.

## 🩷 HUMAN NOTE

Shawn — we finally ranked what the brain actually gets asked, and the shape is clear: three-quarters of all queries are the machines asking "what's lane N doing right now?" Real human questions — the kind you'd type, in sentences — are almost nonexistent in the log. And half the log can be one test run's noise: a single burst of synthetic traffic made up 70% of one hour's rows. So two things: tune the fast machine answers for what the machines ask today, and don't touch the deeper tuning until real human questions show up in the log. Tuning against the harness builds a brain for the harness, not for you.

## 🟣 CHILD NOTE

Imagine counting what snacks kids ask for at school, but the vending machine company ran 50 test orders through the machine yesterday. If you count those, you'd think everyone wants the test flavor. You have to throw out the company's test orders first, then count. And if 72 out of 100 real asks are "is the water fountain working?", you fix the fountain first — but you also notice that someday real kids will ask full questions in sentences, and you should be ready for that.

## 🔵 GRANDMA NOTE

It's like a library counting which books get asked for — except the publisher's delivery truck also rang the desk fifty times, and if you count those, you'd order fifty copies of the delivery manifest. First you cross out the truck's visits, then you look at what real people asked. Most of them just want the day's hours sign on the door — quick and simple. But one day people will ask real questions in full sentences, and the desk should be ready for that too. You just don't rebuild the desk on the truck's schedule.

## 🟠 NAYA NOTE

Retrieval-evaluation doctrine, Naya to Naya: the t1296 top-20 demand analysis (198 rows live at ask-world-queries.jsonl, 140 analysis rows after excluding probe/init) is the first byte-ranked demand picture for the ask-world surface, and it settles two things. (1) SHAPE: lane-N status pulls dominate (102/140, 72.9%, served as identical 6-section snapshots); blocked (6.4%), lessons (5.7%), quality (5.0%) and help/empty/edge cases round it out; the composed-answer capability — natural-language advisory with tick, PR, and conditional — has exactly one data point (0.7%). Hypertuning priorities: machine-shaped atomic pulls first (cheap, fast, correct), composed-answer capability built in parallel but not tuned against a log that contains no composed questions. (2) PROVENANCE: the t1273 window proved synthetic traffic swamps organic (50/71 rows, 70.4% from one test-harness burst); the t0900/t0903 protocol fences probe rows before tallying (query-log-delta discipline). Any demand tally that skips provenance-filtering measures the harness. Hypertuning GO/NO-GO reads the filtered tally only, and stays WAIT until origin='emergent' appears.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1835-tune-against-organic-demand-not-the-synthetic-swamp",
  "lesson": "The ask-world demand picture is 72.9% machine-shaped operational pulls (lane-N status, identical 6-section snapshots) and 0.7% natural-language advisory — but the log swamps organic demand with synthetic bursts (70.4% of one window), so hypertuning must provenance-filter before tallying, serve atomic machine pulls first, build composed-answer capability in parallel, and hold GO/NO-GO at WAIT until origin='emergent' rows appear.",
  "applies_when": ["retrieval", "hypertuning", "demand-analysis"],
  "enforcement": "The ask-world query-log analysis fences synthetic rows before any tally (probe rows and origin!='emergent' excluded, per the t0900 read + t0903 writer-hole protocol; deltas recorded in query-log-delta files). Hypertuning GO/NO-GO reads the filtered tally only and stays WAIT until origin='emergent' appears in the log — a GO on the unfiltered tally is a tune for the harness, refused by the demand picture.",
  "evidence": [
    "hidden_files/askworld-top20-needs-t1296.md (2026-10-22T17:03Z: 198 rows live = 140 query analysis rows; 102/140 = 72.9% lane-N status pulls, all served with identical 6-section snapshot; 1/140 = 0.7% natural-language advisory; 85.0% of rows have unknown/no origin — never inferred)",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1273, 2026-10-22T11:25Z: mirror lesson — the window's dominant event was a 13-second synthetic test-harness burst (50/71 rows, 70.4%); hypertuning GO/NO-GO stays WAIT until origin='emergent' appears]",
    "hidden_files/retrieval/query-log-delta-t0900.md (probe-row fencing discipline: instrument rows excluded before tallying)"
  ],
  "decision_change": "The next retrieval hypertuning decision (a) filters the query log for organic demand before ranking it, (b) prioritizes atomic lane-snapshot/section pulls for the machine-shaped majority, and (c) treats composed-answer work as capability-building, not log-tuning, until origin='emergent' rows exist to tune against. A hypertuning GO on the unfiltered log is refused.",
  "falsifiability": "If organic (origin='emergent') queries arrive and their distribution matches the lane-N-pull shape, priority (a) stands; if organic demand instead shows prose-advisory dominating, the priority flips to composed-answer tuning — the demand picture, not the log, decides. If future logs show synthetic traffic reliably tagged at write time, the fence becomes redundant and the note reduces to the two-question priority.",
  "mechanism": "Test-harness traffic is bursty and dense while organic demand is sparse, and the logging surface records origin only on some rows — a raw tally is therefore dominated by whoever shouted loudest last, not by the demand pattern. Provenance filtering restores the true distribution; the two-question structure follows from it: the 72.9% machine pull is cheap to serve well, and the 0.7% composed question is the one that must be built before the demand arrives, not tuned after it."
}
```
