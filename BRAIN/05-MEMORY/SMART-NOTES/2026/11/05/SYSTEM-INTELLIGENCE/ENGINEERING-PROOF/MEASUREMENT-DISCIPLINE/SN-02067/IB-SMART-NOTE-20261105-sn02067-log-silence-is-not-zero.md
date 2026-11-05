# INTELLIGENT BLOCK — SN-2067

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02067-log-silence-is-not-zero
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Monthly audit 2026-11-01 (distill-monthly-20261101.md, F1/F2, census 35/37 lessons with measured value); lessons.jsonl record 38, id `monthly-audit-log-silence-is-not-zero-20261101`; surfaced by the daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1009). Distinct from CANDIDATE 1006 (audit the evidence standard when a grade falls — this is the log-coverage leg).

## ✦ IN A NUTSHELL

A log that stops mid-window proves nothing about the tail: a zero in a stopped log is a gap, not a zero. The lesson registry's retrieval log ends 2026-10-24T15:45:14Z, eight days before the monthly audit window ends, so every retrieval count in the audit is a lower bound and any lesson filed or used after Oct 24 is UNMEASURED-FOR-TAIL, not zero-valued. The durable rule: **measure the measure before judging the judged — a count is only as complete as the log it was read from, and a stopped log's tail is recorded as unmeasured, never zero-filled.**

## 🩷 HUMAN NOTE

Shawn — the audit counted how often each lesson was retrieved, and the numbers looked thin for anything recent. But the retrieval log itself stopped on October 24, eight days before the audit window ended — so "zero retrievals" for a late-October lesson doesn't mean nobody used it, it means nobody was counting. From now on, every count carries its log's coverage dates, and a tail past the log's last row is marked unmeasured, never zero. We judge the lessons by what was actually measured, not by the silence after the recorder stopped.

## 🟣 CHILD NOTE

Imagine a teacher counting how many times kids raise their hands — but she stops watching at lunch and still writes down "zero" for the whole afternoon. The afternoon kids did raise their hands; she just wasn't looking. The new rule: if you stopped watching, you write "I don't know" for that time, never "zero." Zero means "I watched and nobody raised a hand" — and only that.

## 🔵 GRANDMA NOTE

Dear, it's like counting the apples that fall from your tree but only checking the basket until Tuesday, then writing down "no apples fell" for the rest of the week. The apples may well have fallen — you just stopped looking. From now on, when the counting stops, the notebook says "not counted" for those days, never "none." An empty line because you looked is different from an empty line because you walked away, and only the first one is a real zero.

## 🟠 NAYA NOTE

For every seat that runs or reads an audit: never zero-fill a stopped log. Before grading any retrieval count, read the injection/retrieval log's coverage window — first row to last row — and compare it to the audit window. Any count whose log ends before the window ends is a lower bound; lessons filed or used after the log's last row are UNMEASURED-FOR-TAIL. Future audits must restore or extend the injection log past the gap (here: past Oct 24) and attach log-coverage dates to every count they cite; until then, receipt citations are the only tail measure. This is the log-coverage leg of the evidence standard — CANDIDATE 1006 audits the grade, this note audits the ruler.

## 🟢 MACHINE NOTE

```json
{
  "slug": "log-silence-is-not-zero",
  "sn": "SN-2067",
  "title": "Log Silence Is Not Zero — A Stopped Log Proves Nothing About the Tail",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["audit", "evidence-standard"],
  "enforcement": "The monthly audit's F1/F2 evidence step rejects any retrieval count whose injection-log coverage window ends before the audit window; a count is filed only with its log-coverage dates attached, and a stopped log's tail is recorded as UNMEASURED-FOR-TAIL, never zero-filled. Receipt citations are the only accepted tail measure until the log is restored.",
  "falsifier": "Proven wrong if the retrieval log is shown to cover the full audit window — last injection row at or after the window end — in which case the counts are exact, not lower bounds. A later-recovered tail showing zero retrievals would confirm the lower bound as exact, not falsify the rule.",
  "decision_changed": "How future audits grade retrieval value: restore or extend the injection log past the gap (here, past Oct 24) and treat every count from a stopped log as a lower bound; no audit zeroes a tail it cannot see.",
  "mechanism": "A log records only while it runs; after its last row it records nothing, so absence after that point is indistinguishable from zero. The measurement instrument has a coverage window, and any count read past the window's end inherits the window's end as its bound — the tail is unmeasured, not empty.",
  "provenance": "Monthly audit 2026-11-01 (distill-monthly-20261101.md, F1/F2, census 35/37 lessons with measured value): lesson registry retrieval log ends 2026-10-24T15:45:14Z, 8 days before the audit window ends. Filed as lessons.jsonl record 38, id monthly-audit-log-silence-is-not-zero-20261101. Surfaced by daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1009). Distinct from CANDIDATE 1006 (evidence standard when a grade falls)."
}
```
