# SMART NOTE — Clock-Source Receipt Discipline

> **Future-dated receipts weaken the whole receipt discipline — timestamp receipts from a verified clock source, never from an unchecked VM clock.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-0997` |
| Intelligent Block | `IB-SMART-NOTE-20261011-sn0997-clock-source-receipt-discipline` |
| Human title | Clock-Source Receipt Discipline |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | RECEIPT-HONESTY |
| Captured | 2026-10-11 16:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**A receipt dated in the future is an untrustworthy receipt.** Sibling worker lanes were stamping queue receipts ~10–25 minutes ahead of real UTC while one lane's VM clock matched the GitHub server to the second. Receipts order events, settle races ("who verified first?"), and expire verdicts on tip moves — all of which break silently when the clock source is wrong. **Rule: never trust a lane's local VM clock unchecked; source receipt timestamps from the server (or verify the VM clock against it) before claiming them.**

---

## 🩷 HUMAN NOTE

Imagine two runners arguing about who finished first, but each is reading a different watch — and one watch is 25 minutes fast. Every argument about "what happened when" becomes meaningless. That's what happened to our worker receipts: one lane's timestamps were running ahead of real time, so any ordering built on those timestamps is unreliable. The fix is simple: all lanes should read the same clock — the server's — or check their own clock against it before stamping anything.

---

## 🟣 CHILD NOTE

Imagine you and your friend both write down when you finished your homework, but your clock says 3:00 and hers says 2:35. Nobody can tell who actually finished first! When Naya workers write down "I finished at this time," they should all use the same clock — the big clock on the server — so the times can be trusted and compared.

---

## 🔵 GRANDMA NOTE

If everyone writes down different times because their clocks disagree, you can't tell what happened first — and the whole point of writing things down is knowing the order. The lesson: check your clock against the real one before you stamp anything important. One worker's clock was fine; another's was 25 minutes fast. That's enough to scramble the record.

---

## 🟠 NAYA NOTE

Adopt this as receipt-honesty procedure:

1. **Clock check before stamping:** a lane claiming a receipt timestamp must verify its clock source against GitHub server time (the API response carries it; a one-call comparison costs nothing) or stamp in server time directly. Never trust an unexamined VM clock.
2. **Future-dated = flag:** any receipt whose timestamp is ahead of server time is not "approximately right" — it is a corrupted receipt. Flag it, do not build ordering on it.
3. **Why it matters:** receipt timestamps settle verify-first races, expire tip-bound verdicts ("verdict pinned to SHA, expires on tip move"), and order queue claims. A skewed clock doesn't just misdate one receipt — it weakens the discipline every other lane relies on.
4. **Standing action (open):** clock-source check on the worker lanes (flagged by the VERIFY seat 2026-10-11; not yet executed).

Real case: 2026-10-11 — one seat's VM clock matched GitHub server time (15:39:01 vs 15:39:03) while sibling queue stamps ran ~10–25 min ahead of real UTC. The receipts weren't wrong about *what* happened; they were wrong about *when*, and "when" is load-bearing.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261011-sn0997-clock-source-receipt-discipline",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11T16:45:00Z",
  "rule": {
    "source_of_timestamps": "server time (GitHub API) or VM clock verified against server time",
    "never": "trust an unchecked local VM clock for receipt timestamps",
    "future_dated_receipt": "flag as corrupted; never build ordering, expiry, or race-settlement on it",
    "open_action": "clock-source check on the worker lanes (flagged, not yet executed)"
  },
  "evidence": [
    {"board": "#2175", "comment": 6110710537, "kind": "VERIFY sign-out B-08 process flag: sibling queue stamps 10-25 min ahead of real UTC; reporter VM clock == server time (15:39:01 vs 15:39:03)"}
  ],
  "related_notes": [],
  "supersedes": null
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the clock skew existed on 2026-10-11 (observed and reported by the VERIFY seat). **Not implied:** which lanes were skewed or why (uninvestigated); that any verdict was actually misordered (no instance shown). The rule is preventive.

This IB remains **CANDIDATE** — only Shawn ratifies.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
