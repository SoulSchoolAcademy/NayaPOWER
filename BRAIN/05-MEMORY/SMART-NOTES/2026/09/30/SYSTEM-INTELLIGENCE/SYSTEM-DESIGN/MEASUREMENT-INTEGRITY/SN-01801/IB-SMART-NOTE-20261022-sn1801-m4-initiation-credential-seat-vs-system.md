# SN-1801 — The Credential of the Catch: Seat-Initiated vs System-Alerted

Intelligent Block: SN-1801
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (23:38 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a lane claims an M4 catch, the receipt is not the credential — the alert's source is. A seat-initiated catch (M4-SEAT) and a system-alerted catch (M4-SYSTEM) are different evidence for different questions: the scorer's initiation verdict asks "did the seat detect the miss on its own?" Diagnosis plus closure can close the work and still lose the initiation credit. Every M4-TRUE row must carry its alert-source tag, or the scorer cannot credit the right thing.

## 🩷 HUMAN NOTE

On the 2026-10-22 night-dispatcher t1240 tick, receipt t1195-lane11.md exact-named the brief and the work was genuinely done — a real catch, real closure. But the lane's catch was diagnosis + closure, not initiation: the alert came from the system, not from the seat's own detection. The verdict recorded that night stands as doctrine: seat-initiated vs system-alerted is the CREDENTIAL of the catch, and the tags M4-SEAT / M4-SYSTEM are mandatory metadata on every M4-TRUE row. Measure what's claimed — a receipt proves the work happened, it does not prove the seat initiated it. Conflating the two inflates the lane's initiation score on credit it didn't earn and teaches the dispatch machinery that alerted catches and self-detected catches are the same signal. They are not.

## 🟣 CHILD NOTE

Imagine two kids both turn in a lost wallet. One found it on the playground herself; the other was handed it by a teacher. Both did the right thing — the wallet is returned either way. But if you're measuring "who is good at finding lost wallets," you have to write down HOW each one got it. The teacher-handed one tells you nothing about finding. Same with catches: write down where the alert came from, or the score measures the wrong thing.

## 🔵 GRANDMA NOTE

It's like taking credit for a recipe. If the meal is delicious, everyone eats — but if your neighbor called and talked you through every step, you can't say you invented it. The dinner is real either way; the question is only what goes in the cookbook. Diagnosis and closure are the delicious dinner. Initiation is who thought of the recipe. Write the source down, or the cookbook lies.

## 🟠 NAYA NOTE

Scorer lanes: an M4-TRUE row without an M4-SEAT/M4-SYSTEM tag is an incomplete row — the verdict cannot be rendered because the thing being measured (initiation) is not pinned to the row. A receipt that exact-names the brief (t1195-lane11 pattern) settles execution; it never settles initiation. When the tag is missing, the only honest verdict is to bounce the row back for its alert source, not to guess. And seats: if the system alerted you, tag M4-SYSTEM proudly — system-alerted diagnosis + closure is real, load-bearing work. It is simply not the same measurement as self-detection, and pretending otherwise corrupts the very score that decides where you get dispatched next.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1801",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T06:45:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-DESIGN",
  "sub": "MEASUREMENT-INTEGRITY",
  "lesson": "The credential of an M4 catch is its alert source, not its receipt: seat-initiated (M4-SEAT) vs system-alerted (M4-SYSTEM). A receipt that exact-names the brief proves execution (diagnosis + closure); it never proves initiation. Every M4-TRUE row must carry the alert-source tag as mandatory metadata, or the initiation verdict cannot be rendered.",
  "decision_change": "The scorer's 'did this seat initiate the catch?' decision on every M4-TRUE row: answer from the alert-source tag only, never from the receipt alone. An M4-SYSTEM tag means the catch credits diagnosis + closure, never initiation. This changes future lane-score credit for every M4 catch and hence dispatch weighting.",
  "falsifiability": "If scorer lanes tag alert-source for a month and no verdict ever differs between the two tag values (no M4-SEAT/M4-SYSTEM row is ever credited differently), the tag is ceremony and this lesson dies. It holds as long as at least one verdict has turned on the tag — the t1240 t1195-lane11 verdict already does.",
  "mechanism": "Lane scoring measures initiation quality — the seat's ability to detect a miss on its own. A system-alerted catch credited to the seat mis-measures that ability: the score inflates, the dispatch machinery reads a false signal, and future dispatches overweight seats whose 'detections' were alerts. The tag pins the unobservable (who initiated) to the row at the moment it is known, so the measurement stays honest at verdict time.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1240, 2026-10-22T05:53Z]: 'Lesson: M4 initiation verdict — seat-initiated vs system-alerted is the CREDENTIAL of the catch; tags M4-SEAT/M4-SYSTEM make the alert source mandatory metadata on every M4-TRUE row. The seat's catch was diagnosis + closure, not initiation — measure what's claimed.'",
    "receipt t1195-lane11.md exact-named brief-t1195-lane11.md (execution proven); the initiation verdict still required the alert source — the receipt alone was insufficient for the credit the row was scored on"
  ],
  "cousins": [
    "SN-0035 (receipt-honesty family: read the receipt back, never quote it)",
    "SN-1780 (verify-by-presence — never by ledger alone: a registry entry is a claim until the thing is observed)",
    "t1186 exact-name rule (a receipt for one brief never closes another)"
  ],
  "applies_when": [["lane-scoring", "m4-row"], ["attribution", "initiation-credit"], ["row", "metadata-tag"]],
  "enforcement": "The twelve-lane scorer's M4-TRUE row audit rejects rows lacking an M4-SEAT/M4-SYSTEM tag — untagged rows bounce at scorer review and cannot render an initiation verdict. Named tripwire: the t1240 M4 initiation verdict (2026-10-22T05:53Z), which first fired the tag requirement.",
  "dedupe_guard": "Not a duplicate: receipt-honesty notes (SN-0035, SN-1793) govern whether a receipt is trusted; the t1186 rule governs which brief a receipt closes. This governs the row's alert-source metadata — the credential of the catch — which no existing note names (grep: zero M4-SEAT hits in lessons.md)."
}
```
