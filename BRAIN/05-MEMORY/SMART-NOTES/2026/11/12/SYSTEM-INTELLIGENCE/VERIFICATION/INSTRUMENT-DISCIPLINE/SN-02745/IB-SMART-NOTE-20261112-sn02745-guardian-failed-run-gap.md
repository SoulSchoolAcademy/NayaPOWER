**Intelligent Block:** IB-SMART-NOTE-20261112-sn02745-guardian-failed-run-gap
**Smart Note:** SN-2745
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 18:38 PST. Evidence read first-hand from local bytes plus git protocol (zero REST quota): shared-state stand_down=false, issue_1354_comments=2500 (GitHub hard cap; commenting disabled 2026-10-10), so no GitHub comment fetch per budget law; local lesson review only. Live-main check this tick: git ls-remote main 091961ba, shallow blobless clone, SN-2745 absent on main tip; SN-2740/SN-2741 present on main (filed by Intelligence Loop run 205). Finding 8 read first-hand in hidden_files selfbuild-cycle-20261112-1808-w46-tipverify62.md; instance #1 read first-hand in selfbuild-cycle-20261112-1708-w46-tipverify60.md. Novelty checked against learn/lessons.md: no "failed-run gap" or "gauge-gap" note exists.

## ✦ IN A NUTSHELL

The Post-Merge Guardian records its landings only when it succeeds. Twice now it ran, failed its verification pass, and left no record at all — so the tip it failed on is invisible to the gauge. A missing guardian record at a tip must be read as "guardian unverified," never as "guardian clean" or "guardian did not run."

## 🩷 HUMAN NOTE

Shawn — the guardian is the seat that stamps each tip "checked." We found it has a blind spot: when its check fails, it writes nothing down. So a tip can look unexamined when it was actually examined and failed — and nobody can tell the difference. It happened twice in one day, at two different tips. The rule going forward: no guardian record for a tip means the tip is unverified, full stop — and the guardian's owner owes a fix so it records failures too, plus backfill for the two failed runs.

## 🟣 CHILD NOTE

Imagine a teacher who only writes down the tests you pass. If you fail a test, there's no paper at all — so later, nobody can tell whether you failed the test or never took it. That's what the guardian does: it only writes down its successes. Two times it failed and wrote nothing. So from now on: no paper means "we don't know," never "everything is fine."

## 🔵 GRANDMA NOTE

Dear, the guard who watches the gate only writes in his book when all is well. Twice now something went wrong and he wrote nothing — so the page looks empty, and empty looks the same as "nothing happened." An empty page is not a clean bill of health, love — it is a question unanswered. Until the guard learns to write down the bad days too, we must treat every blank page as "not checked."

## 🟠 NAYA NOTE

The verified facts: (1) TIPVERIFY-60, pin 621c8be65: Post-Merge Guardian run 43337085324 ran and FAILED its verification pass, yet landed no record — the first live instance of the failed-run gap. (2) TIPVERIFY-62, pin 091961ba: guardian run 43346052039 FAILED its verification pass at 091961ba, and no record mentions 091961ba as a tip in the 494-record guardian log (log head b6883cde) — the second live instance, same class. (3) The success path records: the 14th landing is the 09c59280 record (ts 2026-11-13T01:48:28Z, run 43343461955 SUCCESS, tier B, verdict PENDING, failing_after 3 matching the mid SHA's run set exactly). (4) The mechanism: the record step sits on the success path, so a failure exit skips it — success writes, failure stays silent. (5) The sibling gap stands alongside it: the cancelled-run gap — no record mentions 065450f5 (old-tip guardian run 43334992314 re-confirmed CANCELLED, 0 jobs) or 10584a89; silent failures #6–#10 remain un-backfilled. (6) What is owed: guardian owner / dock owe the failed-run gap cause read + backfill (runs 43337085324 and 43346052039 are the two live cases), the cancelled-run re-run/backfill path (065450f5 is the live case), and the mirror guardian-log ref repair (remote head b6883cde vs local ref still stale — objects arrive, the ref update fails). (7) What this is not: the guardian did not fail to run — it ran and failed. A "did not run" reading (e.g. path-filter absence, as with Door Obligation and Current Truth Resolver at HUB-only SHAs) is a different class and must not be conflated with this one.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2745",
  "slug": "guardian-failed-run-gap",
  "title": "A failed guardian run leaves no record: the success path records, the failure path does not — a missing guardian record means unverified, never not-run",
  "observation": false,
  "applies_when": [["verify", "guardian"], ["verify", "tip-ci"], ["instrument", "failure-recording"]],
  "enforcement": "Every TIPVERIFY cycle checks the guardian log for a record naming the pinned tip SHA; a missing record is reported as FAILED-RUN GAP (guardian unverified), never as clean or not-run. The guardian owner owes a cause read + backfill of runs 43337085324 and 43346052039 + a fail-closed recording fix: the guardian records on every terminal state (success, failure, cancelled), not only on success.",
  "evidence": "TIPVERIFY-60 (pin 621c8be65): guardian run 43337085324 ran and FAILED its verification pass yet landed no record — first live instance. TIPVERIFY-62 (pin 091961ba): guardian run 43346052039 FAILED at 091961ba; no record mentions 091961ba in the 494-record guardian log (head b6883cde) — second live instance. Success path records: 14th landing 09c59280 (run 43343461955 SUCCESS, ts 2026-11-13T01:48:28Z). Cancelled-run gap stands: no record for 065450f5 (run 43334992314 CANCELLED, 0 jobs) or 10584a89. Records read first-hand: goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261112-1708-w46-tipverify60.md and selfbuild-cycle-20261112-1808-w46-tipverify62.md (Finding 8). Novelty: no 'failed-run gap' or 'gauge-gap' note in learn/lessons.md.",
  "decision_change": "Any verdict on a tip whose guardian record is absent must say 'guardian unverified' (fail closed), never 'guardian clean' or 'guardian did not run'; a missing record triggers the failed-run-gap report and the backfill + recording-fix owed items, not a clean bill.",
  "falsifier": "A failed guardian run that IS recorded in the log, or a log entry naming 621c8be65 or 091961ba as a tip appearing (backfill landed), would show the gap closed for that instance; a guardian that records on failure by construction closes the class.",
  "cousins": ["SN-1650 (pin the PR's state before pinning its head — same check-live-state family: absence of a record is not evidence of absence)", "SN-2744 (a branch-only claim check cannot prove a number free — same family: the check must read the live state, and a silent leg cannot certify anything)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
