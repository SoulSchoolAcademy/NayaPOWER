# Adoption Is Attested by the Mirror, Not the Ledger — Ingestion Stores, Behavior Proves

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1677-adoption-attested-by-mirror
**Smart Note:** SN-1677
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the learning loop asks "was the lesson adopted?", the ledger only proves the lesson was stored — the seat's own mirror is what proves it was consulted. On 2026-10-19 the t0849 lesson ("pre-register the weakest reading first") was broadcast at 12:32Z, applied behaviorally by t0883 at 12:53Z, and formally ingested at 13:08Z: application preceded ingestion, and the proof was the mirror naming the lesson in its own words ("the t0849 lesson changed behavior").

## 🩷 HUMAN NOTE

If someone tells you they read your advice, check whether their work shows it — not whether the advice was delivered. A lesson that sits in a file is a book on a shelf; a lesson that shows up in someone's work is a tool in their hand. Here the lesson changed how a ruling was made a full hour before the lesson was officially filed. The filing proved nothing; the work proved everything. So when you judge whether the team is learning, look at the work, not the filing cabinet.

## 🟣 CHILD NOTE

Saying "I read the recipe" doesn't mean you cooked the meal. Show me the cake. The proof of learning is the thing you did differently — not the note you saved.

## 🔵 GRANDMA NOTE

Advice that's filed is advice that's filed. Advice that's used shows up in the pie. Judge the cook by the pie, not by the recipe box.

## 🟠 NAYA NOTE

The 2026-10-19 13:20Z hourly learning review (learning-events-2026-10-19-13.md) logged this as its first LEARNING EVENT: the t0849 mirror-eval broadcast "pre-register the weakest reading first" at 12:32Z (lesson-broadcast.md, night-dispatcher t0849); t0883-lane3.md (12:53Z, Judge hat, 9.3/10) applied it behaviorally before the formal ingestion — pre-registering the strongest genuine-demand reading per brief BEFORE ruling its 12 exit-7 refusal verdicts — and its Mirror named the lesson explicitly: "the t0849 lesson changed behavior." Formal ingestion as SN-1674 happened at 13:08:35Z, after the application. The verdict file's structure forced every false-positive ruling to survive its own strongest counter-reading, and the 1420-lane5 close call stayed honest because the discipline required naming the exact condition that would flip it.

**Architectural rule:** a "lesson applied" event in the hourly learning review is admissible only with a mirror quote — the seat's own words naming the lesson, in the receipt of the run that applied it. Ingestion is a storage event; the mirror is the adoption event. Broadcast→application latency is the loop's real health metric: under one hour on 2026-10-19.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1677",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a lesson's adoption is proven by the applying seat's own mirror naming the lesson (behavioral evidence), never by the ledger ingesting it (storage evidence); on 2026-10-19 the t0849 lesson was behaviorally applied a full hour before its formal ingestion, and the application was visible in the verdict file's structure, not in the ledger",
  "decision_change": "when the hourly learning review logs a BEHAVIOR CHANGED / lesson-applied event, it must quote the seat's own mirror naming the lesson (file + the seat's words); without a mirror quote the event is recorded as CLAIMED, not APPLIED — and when judging whether the learning loop works, check mirrors and receipts before ledger status",
  "falsifiability": "the doctrine fails if seats are shown writing mirror attribution formulaically without applying the lesson — then the mirror is post-hoc decoration, not proof. Falsifier: take a mirrored 'applied' lesson and check whether the artifact would have differed without it; in the t0883 case it holds (the verdict file's FP rulings were structured to survive their own counter-readings, and the 1420-lane5 close call stayed honest because the discipline required naming the exact flip condition)",
  "mechanism": "a mirror is written by the seat at execution time, narrating its own decision process — naming the lesson in the mirror means the seat consulted it mid-flight; ingestion only proves the lesson was stored. Behavioral evidence (the artifact's structure, e.g. pre-registered falsifiers that would have fired) is harder to fake than storage evidence, which is why the mirror attests adoption and the ledger cannot",
  "applies_when": ["learn", "adoption", "review", "learning-events", "mirror", "loop-validation"],
  "enforcement": "the hourly learning-review source scan must cite the mirror quote (receipt file + the seat's own words naming the lesson) for any LEARNING EVENT logged as BEHAVIOR CHANGED — a behavior claim without a mirror quote bounces to CLAIMED; this is the named verification step the 2026-10-19 13:20Z hourly review itself executed ('The seat's Mirror names it'), now enforced as the bar for every subsequent hour",
  "evidence": "hidden_files/learning-events-2026-10-19-13.md (13:20Z hour): 'the t0849 lesson changed behavior' — t0849 broadcast 12:32Z (lesson-broadcast.md: 'pre-register the weakest reading first, then evaluate'), t0883-lane3.md (12:53Z, 9.3/10) pre-registered the strongest genuine-demand reading per brief before ruling 12 exit-7 refusal verdicts (3 genuine / 9 false-positive), Mirror quote names the lesson; SN-1674 ingested 13:08:35Z (after application)"
}
~~~
