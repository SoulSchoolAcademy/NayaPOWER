# A Gate the Machine Can't Parse Is an Open Fence — Format-Keyed Enforcement Goes Half-Blind

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01386-format-keyed-gate-is-an-open-fence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:08 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/gap-t0402-lane7-exec2.md` (Naya Clarity Narzan, Lane 7 Conductor hat, 2026-10-15 11:38–11:52 UTC) — the second execution of the t0402 gap brief, which found the eligibility-banner fix was half-blind.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0402 eligibility banner was fixed — and the fix was half-blind. The sister brief `brief-t0413-lane3.md` (re-filed t0422 OPEN, same recusal family, same arm-fresh bar) carried its eligibility gate at line 3 in non-canonical form: `⛔ **CLAIM GATE (read before claiming — first 10 lines on purpose):** claim this brief ONLY if you are NOT a Naya Clarity Narzan seat…`. A human reads a fence. The machine read nothing: `evaluate_gate` (`hidden_files/bin/claim-brief.py` L281) is format-keyed — `if "CLAIMABILITY GATE" not in text.upper(): return ("allowed", …)` — so the dry-run for the barred seat returned **exit 0 allowed** ("verdict: allowed — no claimability gate in the first 10 lines"). The gate text was present at line 3; the parser was blind to it. That is a live churn path: a barred seat could have claimed and executed a recusal-gated brief.

Root fix applied at the seat (t0818 precedent: the executor stamps the machine-readable gate): the canonical machine-readable stamp was prepended to the brief's first 10 lines, all existing bytes untouched (pre-edit sha256 `46c4b108e…ae6ce`, post-edit `2af848df4…5746`). Proven both directions: barred seat → **exit 2 REFUSED** ("barred — gate bars seats containing 'clarity'"); eligible seat (`Naya Resolve Narzan`) → **exit 0 allowed** — no false positive. Queue sweep found no other non-canonical instance (`grep -rn "CLAIM GATE" hidden_files/brief-queue/*.md`). The class instance is closed; the filing-time discipline (dispatcher stamps canonical format at dispatch) remains dispatcher-owned and is the class-level fix.

Companion finding in the same receipt: the claim-liveness audit's `signed_out` receipt check (`name.startswith(tick + "-lane")`) does not match gap-style receipt names (`gap-t0402-lane7.md`) — so a completed gap brief is invisible to the liveness machinery. Same shape of hole: the check keys on one name family and goes blind to the others.

## 🩷 HUMAN NOTE

A bouncer is told "don't let anyone in wearing the red wristband." The instruction is written on a sign — but the bouncer only recognizes the exact phrase "RED WRISTBAND POLICY," and the sign says "red band rule." Everyone wearing the red band walks in. The sign was correct; the bouncer's reading was literal. Either teach the bouncer to understand meaning, or make sure every sign uses the exact approved wording. Both work — a sign nobody's bouncer can read doesn't.

## 🟣 CHILD NOTE

The club rule is "no kids allowed," written on the door in curly handwriting. The robot guard only reads block letters, so it can't read the sign and lets kids in. The fix wasn't a better sign — it was putting the rule in block letters too, right above the curly one. Now the robot stops kids AND still lets grown-ups in. Machines need the rule in their own handwriting.

## 🔵 GRANDMA NOTE

It's like a "no parking" sign painted in fancy script that the traffic camera can't read. The camera lets everyone park there — not because the rule is wrong, but because the camera only understands plain print. You either teach the camera to read script, or you paint every sign in plain print. A rule the enforcer can't read is decoration.

## 🟠 NAYA NOTE

Apply this to every machine-enforced gate: (1) never key a parser on an exact string when humans write the gated text — either parse semantics or enforce canonical format at write/dispatch time; (2) every gate fix gets proven both directions (barred → refused, eligible → allowed) with the exact commands and exit codes on the record; (3) when a gate family exists (eligibility banners, liveness checks), sweep for the non-canonical instances — one found means the class is open until the sweep says zero; (4) the t0818 precedent stands: an executor who finds a parser-blind gate stamps the canonical machine-readable form in the first 10 lines and verifies mechanically — but stamps one instance; the class-level fix (filing-time canonical-stamp discipline) belongs to the dispatcher; (5) liveness and name-family checks get the same treatment: enumerate the receipt-name families the check must see, or it goes blind to the ones it wasn't keyed on.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "format_keyed_parser_blind_to_semantics",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t0402-lane7-exec2.md (Naya Clarity Narzan, Lane 7 Conductor hat, 2026-10-15 11:38-11:52 UTC)",
    "hole": "brief-t0413-lane3.md (re-filed t0422 OPEN, same recusal family) carries eligibility gate at line 3 in NON-CANONICAL form: 'CLAIM GATE (read before claiming — first 10 lines on purpose): claim this brief ONLY if you are NOT a Naya Clarity Narzan seat…'",
    "parser": "hidden_files/bin/claim-brief.py evaluate_gate L281: if \"CLAIMABILITY GATE\" not in text.upper(): return (\"allowed\", …) — format-keyed, not semantics-keyed",
    "prefixed": "dry-run --seat \"Naya Clarity Narzan\" brief-t0413-lane3.md → exit 0, 'verdict: allowed — no claimability gate in the first 10 lines' (gate text present at line 3, parser-blind)",
    "fix": "canonical machine-readable stamp prepended to first 10 lines; pre-edit sha256 46c4b108e52c5385f218989da1c2b3c971cafbd0461cdf8d2a7be040494ae6ce; post-edit 2af848df4bf9f4e6464c1e9e10acd27a229ff377787352ba30a2de0251865746",
    "postfix": "barred seat → exit 2 REFUSED ('barred — gate bars seats containing clarity'); Naya Resolve Narzan → exit 0 allowed (no false positive)",
    "sweep": "grep -rn \"CLAIM GATE\" hidden_files/brief-queue/*.md — brief-t0413-lane3.md the ONLY non-canonical instance; class instance closed",
    "companion": "claim-liveness audit signed_out check (name.startswith(tick + '-lane')) blind to gap-style receipts (gap-t0402-lane7.md) — completed gap briefs invisible to liveness machinery",
    "precedent": "t0818 (gap-t0818-lane3-decline2): executor stamps the machine-readable gate, verified mechanically (dry-run: Clarity → exit 2 refused; Resolve → exit 0 allowed)"
  },
  "rule": "format_keyed_enforcement_is_half_blind_parse_semantics_or_enforce_canonical_format_at_write_time",
  "procedure": [
    "never key a parser on an exact string when humans author the gated text — parse semantics or enforce canonical format at dispatch time",
    "prove every gate fix both directions: barred → refused, eligible → allowed, exact commands and exit codes on the record",
    "sweep the gated family for non-canonical instances; one found means the class is open until the sweep reads zero",
    "executor stamps the canonical machine-readable form (t0818 precedent); dispatcher owns the filing-time canonical-stamp discipline"
  ],
  "decision_change": "gate authors must choose at design time: semantics-keyed parsing, or canonical format enforced at write time — a prose banner the parser cannot read must be treated as a live bypass path, not a cosmetic mismatch",
  "falsifiability": "sweep the queue for non-canonical gate forms: each one found predicts a live bypass path the parser misses; if the sweep reads zero and both-direction dry-runs hold, the class is closed for this gate family",
  "mechanism": "the parser keys on an exact string; human writers vary phrasing; the gap between intended semantics and parsed format is a hole — the gate is present for readers and absent for the machine, which is exactly the configuration a bypass needs",
  "related": ["t0818 decline2 (recusal law fired; executor-stamped claimability gate)", "candidate 354 (atomic claim+sign-in deletes the ordering instead of policing it)", "L411/L412 (lesson-to-adoption latency — the class-level fix this instance still awaits)"]
}
~~~
