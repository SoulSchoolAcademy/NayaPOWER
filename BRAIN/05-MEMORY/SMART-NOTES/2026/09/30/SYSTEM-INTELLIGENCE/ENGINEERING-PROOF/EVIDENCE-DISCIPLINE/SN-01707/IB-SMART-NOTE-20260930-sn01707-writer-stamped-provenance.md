# Provenance Must Be Writer-Stamped at Write Time — Never Caller-Asserted

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01707-writer-stamped-provenance
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The ask-world query-log instrument trusted the caller's `origin` field — and 58 of 65 rows came back `origin='unknown'` (t0900): caller-asserted provenance is starved by construction, because the caller is the least reliable narrator of its own attribution. The t0903 fix moved provenance into the write path: `log_query()` now builds `origin_marker`={session: JARVIS_SESSION_ID, channel: JARVIS_CD_CHANNEL, source: "ask-world"} from the writer's own environment and stamps it on every row, including the init fixture; LOG_FORMAT 2→3. Rule: any log field that must support attribution claims is stamped inside the write path from the writer's environment, never accepted from the caller. The durable enforcement is `bin/check-origin-markers.py [N]` — one marker-less row in the window = FAIL (exit 1), proven RED pre-fix (50/50 marker-less rows) and GREEN post-fix (50/50 stamped rows). The old caller-asserted `origin` taxonomy stays caller-driven (the G8 starvation rule stands for that field — never origin-slice it, never backfill by inference); the writer marker is the complement. A provenance field you must trust is a field you must not accept from the caller.

## 🩷 HUMAN NOTE

Shawn — the instrument was asking every caller "where did you come from?" and 58 out of 65 calls answered "unknown." The answers couldn't be trusted because the question was being asked of the wrong party. The fix: the instrument now stamps the origin itself, from its own environment, on every row it writes — the caller doesn't get a vote. A checker script fails the build the moment one row shows up without the stamp. Trustworthy provenance is written by the writer, never asserted by the caller.

## 🟣 CHILD NOTE

Imagine a sign-in sheet at school where everyone writes their own name — and half the class writes "I don't know." That's what caller-asserted provenance is: asking the person to tell on themselves. The smart way is the teacher standing at the door with a stamp: every hand gets stamped as it comes in, no exceptions. The stamp comes from the teacher's hand, not from the student's pencil.

## 🔵 GRANDMA NOTE

Like a postmark: you don't ask the sender to write "mailed from Chicago" on the envelope — anyone could write anything. The post office stamps it themselves when the letter passes through their hands, and that's the mark everyone trusts. Writer-stamped provenance is the postmark; caller-asserted provenance is the sender's handwriting.

## 🟠 NAYA NOTE

Apply to every telemetry instrument and every log that will ever carry attribution: (1) never accept a trust-bearing field from the caller — stamp it in the write path from the writer's own environment (session, channel, source); (2) bump the log format version when you change the contract (LOG_FORMAT 2→3) so old and new rows never mix silently; (3) ship the enforcement with the fix — a byte check with a hard falsifier (one marker-less row in the window = FAIL) — and prove it RED before the fix and GREEN after; (4) keep caller-asserted fields as what they are: keep the starvation rules on them (never slice, never backfill by inference), and let the writer marker be the attribution-grade complement. When a defect register says a field is "starved," the fix belongs in the writer, not in better instructions to the caller.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "writer-stamped-provenance",
  "sn": "SN-1707",
  "title": "Provenance Must Be Writer-Stamped at Write Time — Never Caller-Asserted",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["telemetry", "instrument", "provenance", "query-log", "demand-classification", "attribution", "evidence"],
  "enforcement": "hidden_files/bin/check-origin-markers.py [N]: one marker-less row in the window = FAIL (exit 1). Proven RED pre-fix (50/50 rows marker-less, exit 1) and GREEN post-fix (50/50 stamped rows, exit 0) over the live log; all 7 call-site paths plus the fixture path exercised; 50 verification rows flagged origin=synthetic so consumers filter them like probes. Any new trust-bearing log field without a writer-stamp + a failing check is incomplete at design review.",
  "evidence": {
    "starvation": "t0900: 58/65 rows origin='unknown' — caller-asserted origin taxonomy is starved (askworld-defect-register.md, G8)",
    "fix": "t0903: log_query() builds origin_marker={session: JARVIS_SESSION_ID, channel: JARVIS_CD_CHANNEL, source: 'ask-world'} INSIDE the write path (t0638) and stamps it on every row incl. the init fixture; LOG_FORMAT 2->3",
    "proof": "RED pre-change (50/50 marker-less, exit 1) -> GREEN post-change (50/50 stamped, exit 0); receipt twelve-lane-receipts/t0903-lane10.md (lane 10 = instrument author)",
    "register": "askworld-defect-register.md change log t0903 (2026-10-19): SB-Δ2 -> CLOSED; G8 amended — caller-asserted origin stays caller-driven (starvation rule stands); writer marker is the complement"
  },
  "decision_changed": "How provenance is designed in telemetry instruments: stamp trust-bearing fields inside the write path from the writer's own environment; keep caller-asserted fields under consumer/starvation rules and never use them for attribution.",
  "falsifier": "A caller-asserted provenance field independently verified tamper-evident (e.g., caller signs it and the instrument verifies the signature at write time) — then 'never accept from the caller' overstates; or a marker-less row passing check-origin-markers.py, which would falsify the enforcement itself.",
  "mechanism": "The write path executes in the instrument's own process context, where session/channel/source come from the writer's environment and are not caller-controlled; caller-passed fields are caller-controlled by definition, so any attribution built on them inherits the caller's incentives to omit or fabricate. Writer-stamping moves the trust boundary from the caller's assertion to the instrument's own execution context."
}
~~~
