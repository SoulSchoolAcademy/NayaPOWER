# DESIGN — Standdown Blast-Radius Redesign (API-STANDDOWN v2)

**STATUS:** PROPOSED — LAW/director review required (routed by the 2026-10-21
main-session adjudication, 19:36Z). Not ratified law. Authority-model-adjacent
mechanics stay human-gated per Governance Contract §6; this doc proposes
mechanics only — it changes no precedence, no standing law.

**Author:** Naya Verity Narzan (authority-builder seat, Authority & Governance)
**Branch:** `naya5/standdown-blast-radius`

---

## 1. The problem, in plain words

On 2026-10-21 at 18:41:48Z, one worker hit a 403 on a GitHub PATCH and declared
an API standdown: **every seat, every lane, zero API calls for 60 minutes.**

The 403 turned out to be the worker's own bad file path — the PATCH body file
was never created, so the request was malformed client-side. A clean re-PATCH
landed at 19:45Z. It was never a permission problem. The premise was false.

Meanwhile, ~44 API calls executed inside the standdown window (dispatch waves
w678/w679 plus workers). All succeeded. The adjudication ruled ~43 of them
violations of standing law — on a false premise. The harm was zero only because
the credential was fine; the machine spent an hour obeying a ghost.

**One worker's local input error became everyone's standstill.** That is the
blast-radius defect: the standdown has no premise check and no tiers.

---

## 2. Objective

Keep the governor's protection real — a genuine permission 403 (degraded
connector identity) must still halt waste — while making false alarms cheap:
premise verified BEFORE declaration, and the blast scoped to the evidence.

Governance exists to make NayaPOWER "capable enough to help, constrained enough
to trust" (Governance Contract §15). A 403 is a **denied grant**. Per §7
(revocation invalidates future use of the affected authority), the revocation
must be scoped to the affected authority — never to every seat by default.

## 3. The design

### 3.1 Premise verification (T0 — the failing worker, before declaring)

On any 403, the failing worker MUST:

1. **Stop the in-flight write.** Finish nothing with it.
2. **Read the error body verbatim.** Name what it says: permissions-shaped
   ("Resource not accessible", named scopes) vs input-shaped (bad path, bad
   payload, malformed request).
3. **Run ONE cheap probe** (1 API call): re-run the failing request with the
   corrected input if the input was malformed, or a GET against the same
   resource.
   - Probe succeeds → **premise FALSE. No standdown.** Record the cause
     (bad path/param/payload) in the run's evidence. This is the whole
     18:41Z incident: a single GET on #2154 proved the credential fine.
   - Probe 403s again with a permissions-shaped body → **premise TRUE.**
     Proceed to declaration.
   - Probe is inconclusive (network shape, timeout) → treat as FALSE but
     record the ambiguity; retry the original once, then stand down only the
     failing operation.

**The 18:41Z incident under this rule:** probe at ~18:42Z succeeds → no
standdown file, no breach, no adjudication, the ~43 "violations" never exist.
The run continues on the corrected single PATCH.

### 3.2 The standdown file becomes a claim (T1 — declaration)

A bare timestamp is not evidence. The standdown file MUST carry the claim, in a
machine-readable fixed format (JSON or fixed YAML), with these fields:

| Field | Meaning |
|---|---|
| `seat` | full seat name of the declaring worker |
| `declared_at_utc` | declaration timestamp |
| `verb` + `endpoint` | the exact failing request |
| `error_body` | the 403 body, verbatim or exact excerpt |
| `probe` | the T0 probe request + its result |
| `tier` | 1, 2, or 3 (see §3.3) |

A claim-less file, or a claim whose body is not permissions-shaped, is honored
**only by the declaring worker** (tier 1, self-halt). Other workers continue.
**No claim, no blast** — this is the mechanical teeth.

### 3.3 Tiered blast radius (T2 — default ladder)

- **TIER 1 — worker:** the failing worker halts ITS OWN API work for 60 min,
  finishes local-only, marks affected receipts UNVERIFIED. (This is the entire
  worst case for the 18:41Z incident under the new rules: one run goes
  local-only; the dispatch waves never notice.)
- **TIER 2 — lane:** a SECOND independent worker hits a permissions-shaped 403
  on a different lane inside the window → the dispatcher suspends that lane's
  API for the remainder of the 60 min. Two seats agreeing is the corroboration
  one seat cannot manufacture.
- **TIER 3 — machine:** only when evidence shows the connector identity's
  permission itself is degraded (two-seat evidence + director or dock
  confirmation, or the connector's own status check failing) → full 60-min
  halt. Lifted early only on proven-false premise, by the director only
  (2026-10-12 precedent stands).

Escalation never skips a tier. A tier-3 declaration without two-seat evidence
is posted to the board as UNVERIFIED and auto-downgraded by the director to
tier 1.

### 3.4 Readers (T3 — honoring a standdown)

Before honoring a standdown file, every worker checks, in order:

1. mtime < 60 min (existing check — stands);
2. the claim is present and permissions-shaped (new);
3. the declared tier is 2 or 3 for lanes other than the declaring worker's.

If (2) or (3) fails → treat as tier-1-only (self-halt of the declaring
worker). Continue the run. Note the downgrade in the run's evidence.

## 4. What this design does NOT touch

- The 19:36Z interim precedence stands untouched: Shawn's direct orders outrank
  standing brief laws; an active (valid) standdown outranks routine
  dispatch/fold reads — folds go local-only, receipt reads deferred, marked
  UNVERIFIED; workers never self-exempt — only the director lifts a standdown,
  and only on proven-false premise. This design was explicitly routed
  "not hot-patched"; it proposes mechanics, it does not re-order authority.
- The 60-minute default duration stands.
- The 2026-10-12 proven-false-premise early-lift precedent stands (now with a
  claim to prove against).

## 5. Acceptance

This design is ACCEPTED when the director ratifies it AND a follow-on change
lands:

- **Follow-on 1 (mechanical):** `standdown_claim_check.py` — a script that
  reads the standdown file and reports claim-valid / claim-absent /
  permissions-shaped-or-not, so brief STEP -2's "check for the file" becomes
  "check the claim". (Named here, built separately — smallest change.)
- **Follow-on 2 (brief):** STEP -2 wording updated to the T3 reader check.

Rejection of any section returns it to PROPOSED with the reason; the interim
precedence continues to govern meanwhile.

## 6. Simulation log (evidence the design would have worked)

| Step | Old rules | New rules |
|---|---|---|
| 18:41:48Z, PATCH 403 (bad body-file path) | standdown declared, machine halted 60 min | T0 probe: GET #2154 succeeds → premise false → no standdown |
| 18:50–19:02Z, w678 dispatch + w679 fold reads | ~43 ruled violations on a false premise | fully legal; no breach, no adjudication |
| 19:45Z, correct-path PATCH | lands after the waste | lands at ~18:43Z, one call |

Worst case under new rules (worker misreads the probe): tier 1 — one run goes
local-only for up to 60 min; five lanes and the dispatcher are untouched.

## 7. Open questions for LAW/director

1. Should tier-2 corroboration require different *lanes* or different *seats*?
   (Proposal: different lanes — seats share one connector identity, so two
   seats on one lane corroborate nothing.)
2. Is 60 min the right default at tier 1, or should worker-scope be shorter
   (30 min) since the blast is small?
3. Where does the claim format live canonically — the goal hidden_files
   (operational) or the repo GOVERNANCE/ (law)? Proposal: the format
   canonical in the repo; the live file in hidden_files.
