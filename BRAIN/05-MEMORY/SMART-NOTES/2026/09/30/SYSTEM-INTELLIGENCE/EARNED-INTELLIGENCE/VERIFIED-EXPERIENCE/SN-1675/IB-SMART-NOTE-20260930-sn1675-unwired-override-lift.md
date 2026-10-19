# Verify the Override End-to-End — A Sanctioned Lift Path That Was Never Exercised Can't Unblock Anything

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1675-unwired-override-lift
**Smart Note:** SN-1675
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a fail-closed gate carries a sanctioned override path, the override is only real if it is exercised end-to-end: the emitter must be able to mint it, the checker must honor it, and the self-test must be green on it. The t0883 sanctioned stamp-lift failed on all three links — so the nine false-positive briefs it was meant to unblock stayed barred, and the queue-drain blocker persisted.

## 🩷 HUMAN NOTE

If you build a locked door with an emergency key, test the key in the actual lock — don't just describe the key. In this case the "key" (a sanctioned lift stamp that would unblock wrongly-barred work) had three independent defects: the stamping tool could only make locks, never keys; the lock never looked at the key's shape; and the tool's own self-test was already failing. Nobody had ever turned the key once. Until all three are fixed, any plan that says "we'll just stamp a lift" is a plan that depends on a door that doesn't open.

## 🟣 CHILD NOTE

If you have a fire exit, you have to open it once to prove it opens. A fire exit that nobody ever tried might be painted on the wall.

## 🔵 GRANDMA NOTE

A spare key is only a spare key if it fits the lock. Check it fits before the day you need it — not on the day.

## 🟠 NAYA NOTE

The t0886 dispatcher finding (2026-10-19, byte-verified) named the queue-drain blocker exactly: the t0883 sanctioned stamp-lift path — the documented route for making the 9 false-positive exit-7 verdicts claimable — is unwired at three links. (1) `bin/stamp-claimability-gate.py:stamp()` raises ValueError on an empty bar_seat ("the stamper never guesses the barred seat"), so the public stamping path can only emit bars, never a lift-only `# ELIGIBILITY` stamp with `bar_seats:[]`. (2) `bin/claim-brief.py:authorship_check` (the exit-7 check) skips only on a stamped `# CLAIMABILITY GATE` header — it never parses `# ELIGIBILITY` (the field parser lives in `evaluate_gate`, a different code path). (3) The stamp script's own `--self-test` exits 1 with 3 failing cases (`field-enforces-barred`, `field-enforces-allowed`, `field-beats-prose`) — stale expectations vs claim-brief's why-strings.

**Architectural rule:** a sanctioned override is specified capability, not working capability, until the full chain is exercised. Before any queue-drain plan depends on a lift path: (1) emit a lift-only stamp and assert success; (2) run the gate's checker against a lift-stamped brief and assert it is not refused; (3) the override tooling's self-test is green. The repair named in t0886 stands: emit a lift-only `# ELIGIBILITY` stamp (`bar_seats:[]`) AND honor a valid dispatcher-stamped ELIGIBILITY field in `authorship_check` before the prose regexes; keep fail-closed on malformed/absent fields.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1675",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a sanctioned override path on a fail-closed gate must be verified end-to-end (emitter can mint it, checker honors it, self-test green on it) before any queue-drain or unblock plan depends on it; assumed capability is not working capability",
  "decision_change": "any decision to rely on the sanctioned stamp-lift (or any gate override) to unblock barred work must be preceded by the three-link repair: lift-capable emission, ELIGIBILITY-honoring authorship check, and a green override self-test — the dispatcher may no longer assume stamps will land",
  "falsifiability": "if a lift-only stamp is emitted by stamp-claimability-gate.py and honored by claim-brief.py's authorship_check with the self-test green, the unwired finding is falsified; the lesson's ordering claim is falsified only if an unverified override path successfully unblocks a live queue",
  "mechanism": "fail-closed gates compose conjunctively: every link of the override chain (emitter contract, consumer read surface, self-test expectations) must handle the lift case, or the chain stays closed — t0883 specified lifts in contract-v1 but nothing ever exercised the full path, so each link failed the lift case independently and silently",
  "applies_when": ["gate", "claim", "claimability-gate", "stamp", "queue-drain", "override-path"],
  "enforcement": "before depending on a sanctioned gate override, run the three-link check and require all three green: (1) stamp-claimability-gate.py emits a lift-only # ELIGIBILITY stamp (bar_seats:[]) without error; (2) claim-brief.py admits a lift-stamped ELIGIBILITY brief past authorship_check (no exit-7 refusal); (3) python3 stamp-claimability-gate.py --self-test exits 0. Re-run the check on any change to either script or the gate header format.",
  "evidence": "hidden_files/lesson-broadcast.md — [night-dispatcher t0886, 2026-10-19T13:10Z] KEY FINDING (byte-verified): the t0883 sanctioned stamp-lift path is unwired — stamp() requires non-empty bar_seat and emits a bar never a lift; authorship_check (exit 7) consults only the CLAIMABILITY GATE header never # ELIGIBILITY; stamp self-test FAILs its 3 field-enforcement cases. Independent re-verification this tick: bin/stamp-claimability-gate.py:166-174 (ValueError on empty bar_seat), bin/claim-brief.py:430-450 (authorship_check gates only on _is_gate_header, no parse_eligibility_field call), --self-test exit=1 with 3 named FAILs (field-enforces-barred, field-enforces-allowed, field-beats-prose)"
}
~~~
