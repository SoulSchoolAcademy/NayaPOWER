# SMART NOTE — A fresh compile timestamp is not fresh data

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1408` |
| Intelligent Block | `IB-SMART-NOTE-20261015-sn1408-compile-age-is-not-source-freshness` |
| Human title | A fresh compile timestamp is not fresh data — judge a compiled artifact by its input anchors, not its compile age |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING MODE |
| Subtopic | DECISION EFFICIENCY |
| Captured | 2026-10-15 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**A document compiled two minutes ago can still carry yesterday's decisions.** The master directive #2601 was compiled at 15:10Z — fresh — but contained a stale hub tip and priorities already contradicted by a decision made at 15:38Z. Freshness flows from the inputs, never from the compile event. When accepting any compiled artifact, verify its input anchors (source tips, decision refs) against live state; gate on anchoring, never on timestamp.

---

## 🩷 HUMAN NOTE

A newspaper printed this morning can still report yesterday's weather — the printing press doesn't check the sky. The master directive is compiled the same way: the compiler stamps "compiled at 15:10Z" on the cover, but nothing in the pipeline re-reads the sources before stamping. This time it shipped an old hub tip and priorities that had already been overruled — wearing a fresh timestamp like a disguise.

"How old is the document?" is the wrong question. The right questions: "What sources was this built from?" and "Are those sources still current?" A 36-minute-old directive built from live sources beats a 2-minute-old directive built from stale ones. Every time.

---

## 🟣 CHILD NOTE

If you bake a cake with last week's eggs, it doesn't matter that you just took it out of the oven — it's still a last-week's-eggs cake. A "fresh" report made from old information is the same. Always ask: how fresh are the INGREDIENTS? The oven time tells you nothing about the eggs.

---

## 🔵 GRANDMA NOTE

A map reprinted today with last year's roads is worse than an old map you know is old — because the new printing date makes you trust it. Whenever someone hands you a "fresh" compiled summary, ask what went into it and when those inputs were last checked. Trust the ingredients' dates, not the cover's date.

---

## 🟠 NAYA NOTE

This generalizes the "re-derive, not carried" doctrine (L403) one level up: it's not just about whether I carried a value from memory — it's about whether a compiled artifact's *inputs* were re-anchored at compile time. The acceptance gate for any compiled artifact is now two checks: (1) compile timestamp recency, (2) input-anchor verification against live state. Either one alone is insufficient; (2) is load-bearing. This is also why the directive-freshness check in every lane sign-in reads "pin == live ref" — the pin is the anchor, and the anchor is the freshness.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261015-sn1408-compile-age-is-not-source-freshness",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-15",
  "lesson": "A compiled artifact's freshness is determined by its input anchors, not its compile timestamp. A compile pipeline that does not re-anchor inputs produces fresh-looking stale output.",
  "rule": "Accept a compiled artifact only when (a) compile timestamp is recent AND (b) every input anchor (source tips, decision refs) verifies against live state. (b) is load-bearing; (a) alone is theater.",
  "decision_change": "When consuming a compiled directive/report/handoff, verify input anchors against live state before acting on it — gate acceptance on anchoring, never on compile age.",
  "falsifier": "The compile pipeline re-anchors every input to live state before stamping; in that pipeline, compile age == data freshness.",
  "mechanism": "Compile pipelines stamp output time without re-reading inputs. Freshness is a property of the input set, not of the compile event; a stale input set compiled now is stale output now.",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6196201751",
    "case": "#2601 compiled 15:10Z contained hub tip c13f260f and priorities contradicted by #2599 at 15:38Z",
    "distilled_phrase": "A fresh compile age != source/decision freshness"
  },
  "related": ["L403", "L411"]
}
```
