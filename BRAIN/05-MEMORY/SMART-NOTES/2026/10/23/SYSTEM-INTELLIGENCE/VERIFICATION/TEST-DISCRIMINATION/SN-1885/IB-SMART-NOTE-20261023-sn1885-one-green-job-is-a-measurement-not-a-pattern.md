Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

WIRE sign-out at the new tip c60ff22c (board #2793, comment 6370831011, 2026-10-23 17:30Z): the finished test job showed 7 failed / 5,418 passed / 18 skipped, down from 21 failed / 5,404 passed at 1ebcf8ae. The cleared 14 were exactly the MANIFEST_STALE retrieval class (applicability retrieval x2, cold-retrieve drill bank x10, cold-start x2); MANIFEST_STALE had 0 mentions in the new log; zero new failures. A clean clearance — and the sign-out still refused to retire the watch, with the caveat stated plainly: "one-job clearance is a measurement, not a pattern — persistence check owed next slot." That caveat is the lesson. A single green job is one sample from a moving system: between the red-naming job and the green job the tip itself moved (1ebcf8ae -> c60ff22c), so the green job measured a different delta than the red one; and a job can go green by accident — the breaking delta reverted for unrelated reasons — which looks identical to a cure. The next slot's identical FAILED-ID-set comparison at a settled tip is the first apples-to-apples falsifier. Decision-change: when WIRE or the dock decides to retire a red watch after a green job, the watch stays open through the next slot; retirement requires the next slot's identical-run confirmation. Falsifier: if single-green-job retirements are repeatedly followed by re-fires, the persistence requirement was necessary; if over time they never are, it narrows to flaky classes.

## 🩷 HUMAN NOTE

Shawn — the test board went from 21 reds to 7 reds overnight, and every red that cleared was exactly the class we expected the fix to cure. Zero new reds. It looks like a win — and the WIRE lane still didn't close the watch. Here's why that's right: one green test run is a single photograph of a moving machine. The machine moved between the two photos (the code tip changed), so the "after" photo isn't even of the same machine. The cure is only proven when the next run, on a settled machine, shows the same green — twice in a row, same shape. Until then the watch stays open. That's the discipline: a measurement is not a pattern.

## 🟣 CHILD NOTE

Imagine you take medicine and your fever is gone the next morning. Are you cured? Maybe — or maybe the fever just dipped for a day. A smart doctor doesn't declare you healthy on one good morning; she checks again tomorrow. If the fever stays gone, then it's the medicine. The test suite is the thermometer, the fix is the medicine, and one green run is one good morning. The cure is proven by the second good morning in a row.

## 🔵 GRANDMA NOTE

Think of a leaky pipe you think you fixed. You check under the sink once — dry. Fixed? Not yet: the water might just not have run since your repair. You check again the next day after the sink's been used all evening — still dry. Now it's fixed. One dry check is a measurement; two dry checks after real use is a pattern. Software fixes work the same way: the first green test run is the first dry check, and the watch stays open until the second one.

## 🟠 NAYA NOTE

For the WIRE lane and the dock: this note operationalizes the caveat already stated in 6370831011 — it is not new policy, it is the written form of the lane's own discipline. The red-watch lifecycle gains one field: persistence-check (the owed next-slot identical-run confirmation). A watch is retired only when the next slot's job reproduces the identical FAILED-ID set at a settled tip; a watch closed on one green job is re-opened. The WIRE sign-out template must carry the owed check (which slot, which tip) whenever it names a clearance. This does not slow genuine cures: the next slot is already the lane's cadence; it only stops the premature victory lap.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1885-one-green-job-is-a-measurement-not-a-pattern",
  "lesson": "One green job at a new tip re-names the red; it does not prove the cure — the cure is proven by the next slot's identical-run confirmation at a settled tip. Evidence: WIRE sign-out (board #2793, 6370831011, 2026-10-23T17:30:16Z) at new tip c60ff22c: 7 failed/5,418 passed/18 skipped vs 21 failed/5,404 passed at 1ebcf8ae; cleared 14 are exactly the MANIFEST_STALE retrieval class (applicability retrieval x2, cold-retrieve drill bank x10, cold-start x2); MANIFEST_STALE 0 mentions in new log; zero new failures — and the sign-out still carried the caveat: 'one-job clearance is a measurement, not a pattern — persistence check owed next slot.' Mechanism: per-job test results are samples from a moving system — between the red-naming job and the green job the tip moved (1ebcf8ae->c60ff22c), so the green job measured a different delta; a job can also go green by accident (breaking delta reverted for unrelated reasons), indistinguishable from a cure. The next slot's identical FAILED-ID-set comparison at a settled tip is the first apples-to-apples falsifier. Decision-change: a red watch stays open through the next slot after a green job; retirement requires the next-slot identical-run confirmation. Falsifier: repeated single-green-job retirements followed by re-fires confirm the requirement; if they never re-fire over time, it narrows to flaky classes.",
  "applies_when": ["wire", "red-watch", "cure-proof", "testing", "green-job", "verification", "tip-move"],
  "enforcement": "The red-watch lifecycle carries a persistence-check field: a watch is retired only on the next slot's identical FAILED-ID-set comparison at a settled tip; a watch closed on one green job is re-opened by the WIRE lane. The WIRE sign-out template must name the owed next-slot check (slot, tip) whenever it names a clearance.",
  "evidence": ["board #2793 comment 6370831011 (Naya Resolve Narzan, WIRE lane, 2026-10-23T17:30:16Z): tip 1ebcf8ae->c60ff22c; 7 failed/5,418 passed/18 skipped vs 21 failed/5,404 passed; cleared 14 exactly the MANIFEST_STALE retrieval class; zero new failures; caveat 'one-job clearance is a measurement, not a pattern — persistence check owed next slot'"],
  "falsifier": "Repeated single-green-job retirements followed by re-fires confirm the requirement; if they never re-fire over time, the requirement narrows to flaky classes.",
  "related": ["SN-1812 (detection is not remediation)", "SN-1872 (cure must declare addressed failures)"]
}
```
