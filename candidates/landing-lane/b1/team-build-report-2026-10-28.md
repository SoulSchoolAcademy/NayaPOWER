# TEAM BUILD REPORT — 2026-10-28 (workspace only, NOT live)

Builder: TEAM BUILD for Team Naya, under Naya Power. Lanes: Power's (B1
serve-ready worker, Smart Search activation fix). Nitro holds the face —
her preview working copy was NOT touched. No Hub landings, no deploys,
no production database writes, no secrets, no deletions, no PR workflow.
Nothing below is presented as live.

## (a) B1 SERVE-READY WORKER

Files:
- `workspace/system/b1-serve-ready-2026-10-28.py` — serve module
  (importable + CLI). serve() -> (200, {counts, items} envelope) on a
  live read; (503, {error: "live_rows_unavailable"}) on ANY fetch
  failure, with NO items and NO counts keys. Live query at serve time,
  project filter in SQL, dedup one row per item_key (most recently
  updated wins, ties first seen), owner_seat -> owner, area null always.
  No cache, no file fallback (the core's .sample.json is never read).
- `workspace/system/test-b1-serve-ready-2026-10-28.py` — fixture +
  live tests. Exit 0 only if every check passes.
- `workspace/system/b1-serve-ready-2026-10-28.worker.js` — JS shape
  mirror for the merged-worker landing lane (pure shaping only; the
  worker runtime fetch is NOT proven here). Fixture-tested only.
- `workspace/system/test-b1-serve-ready-2026-10-28.worker.cjs` — JS
  fixture tests.

Source: proven core `workspace/system/b1-live-rows-core-2026-10-27.py`
(run 5 ALL_PASS). The core script and its sample were NOT modified.

### Test output — Python module (FINAL FULL RUN, EXIT 0)
```
PASS F1 dedup-most-recent-wins items=3 k1=New
PASS F2 dedup-tie-first-seen k2=TieFirst
PASS F3 owner-mapping k1.owner=naya-power k3.owner=None
PASS F4 area-null-all
PASS F4b face-fields-all
PASS F5 counts-math counts={'rows_read': 5, 'unique': 3, 'done_proven': 1}
PASS F6 failure-503 status=503 error=live_rows_unavailable
PASS F6b failure-no-items-no-counts keys=['error', 'generated_at', 'message', 'project_id', 'reason', 'status']
PASS P1 per-app-grouping per_app={'App A': {'done': 1, 'total': 2}, 'App B': {'done': 0, 'total': 1}}
PASS P2 unmapped-bucket unmapped={'done': 1, 'total': 1}
PASS P3 phantom-ignored ghost absent
PASS P4 reconciliation-invariant tot=4 done=2 items=4
PASS P5a loader-dropin loaded={'a1': 'App A', 'b1': 'App B'}
PASS P5b loader-missing-empty
PASS P5c loader-malformed-raises raised
PASS P6 serve-carries-per-app per_app={'per_app': {'App A': {'done': 1, 'total': 1}}, 'unmapped': {'done': 0, 'total': 1}, ...}
PASS L0 serve-200 status=200
FRESH READ: raw=394 unique=394 done_proven=23
SERVED:     {'rows_read': 394, 'unique': 394, 'done_proven': 23}
PASS L1 live-counts-match served={'rows_read': 394, 'unique': 394, 'done_proven': 23} fresh=(394,394,23)
PASS L1b live-key-sets-equal served_keys=394 fresh_keys=394
PASS L2 live-rows-match mismatches=[]
PASS L3 live-spot-check-3-keys keys=['shawn-pages-alignment-20261026', 'seats-feedback-round-20261026', 'identity-flagship-fixes-20261026']
PASS L4 live-per-app-unmapped-mode per_app={'per_app': {}, 'unmapped': {'done': 23, 'total': 394}, ...}
PASS L4b live-per-app-reconciliation tot=394 done=23
FAILURES: none
ALL_PASS: True
EXIT=0
```

Defect found BY this test, fixed, re-proven (receipt chain, not hidden):
- First live run: serve() returned only 25 rows (L1/L1b FAIL; L2/L3
  passed on the partial set). Cause: my paging loop did not adopt the
  cascade-shrunk page size, so a 25-row cascade page looked like
  end-of-table. The proven core tracks effective limit; my module had
  dropped that tracking. Fix applied (_read_page returns (page,
  effective_limit); loop adopts it). Final run above serves all 394.
- Earlier independent-read failure (empty stdout) was a TEST defect
  (single-attempt read, no transport discipline); fixed with deliberate
  fresh-run retries, same as the proven sweep recovery. No record data
  was touched in either fix (reads only).

### Per-app counts (scope refinement, Resolve filing 6471995975)
Endpoint shape now carries `per_app` (App Brief standard: "% done
computed from THIS app's own proven-done jobs, big, with the count
beside it — never typed, never an estimate, never its area's
number"). JS mirror carries it too (W8–W11 PASS).

Record truth, verified live 2026-10-28: work_items has NO app field;
parent_item_id covers only 60/394 rows and its 5 parents are
work-packages (page-design-audit, ultimate-spec master, v4 inventory
master, welcome flow, director consolidation) — NOT apps. So per-app
counts come from a mapping {item_key -> app} supplied at serve time
(loader + --mapping flag + TEMPLATE file). NOTHING is inferred from
key prefixes or titles in this code — that would be invention, and
the filling rule forbids it.

Live per-app VALUES: UNVERIFIED — no canonical mapping file exists in
the record or workspace yet, so live data honestly reports
per_app={} + unmapped {done 23, total 394}, reconciling exactly to
the project total (L4/L4b above). The computation is proven
(fixtures P1–P6 + JS W8–W11 + live reconciliation); the mapping DATA
is owed via the FILL pipeline (Resolve's packs through Nitro /
STRUCTURE L1 map). The brief-fields schema packet is the parent's
gated packet — NOT applied here, per the brief.
- `workspace/system/b1-per-app-mapping.TEMPLATE.json` — contract +
  owner, intentionally empty (no invented assignments).

### Test output — JS mirror (fixture only)
```
PASS W1 dedup-most-recent-wins items=3
PASS W2 dedup-tie-first-seen k2=TieFirst
PASS W3 owner-mapping k1=naya-power
PASS W4 area-null-all
PASS W4b face-fields-all
PASS W5 counts-math {"rows_read":5,"unique":3,"done_proven":1}
PASS W6 response-shape
PASS W7 unavailable-503 status=503
PASS W7b unavailable-no-items-no-counts keys=error,generated_at,message,project_id,reason,status
FAILURES: none
ALL_PASS: true
EXIT=0
```

## (b) SMART SEARCH ACTIVATION FIX

Files (all under `workspace/smart-search-10x/`, additive only —
rank-v3.js and integration-v3.js were NOT modified):
- `activation-v1.js` — activateResult(item): resolves a ranked result
  to the block ITSELF as a standalone view (panel card HTML with its
  navigation anchor stripped: no href, no /hub/feed target, no feed
  scroll/navigation). A result without a block is UNAVAILABLE, never a
  feed fallback.
- `test-activation-v1.cjs` — activation validation.

Mechanism of the live failure (proven from the harness itself): the
panel card's "Open the block" link points at /s/<sn>, and live /s/<sn>
paths redirect to the Hub feed — no standalone block view exists on
live for ANY note. So a correct #1 still fails at Open. This fix makes
the Open ACTION resolve to the block view; it does NOT create the live
route (see "remains for the gate").

### Test output — activation (52 checks, EXIT 0)
```
PASS Q1-top-is-expected top=IB-SMART-NOTE-20261026-sn1880-how-to-input-a-smart-note
PASS Q1-top-title title=How to Input a Smart Note, Successfully — So It Goes Live
PASS Q1-top-has-block block=How to Input a Smart Note, Successfully — So It Goes Live
PASS Q1-action-standalone action=open-block-standalone
PASS Q1-noteId-matches noteId=IB-SMART-NOTE-20261026-sn1880-how-to-input-a-smart-note
PASS Q1-block-is-matched-block same-object=true
PASS Q1-title-matches title=How to Input a Smart Note, Successfully — So It Goes Live
PASS Q1-no-feed-scroll feedScroll=false
PASS Q1-no-feed-navigation feedNavigation=null
PASS Q1-open-target-block-itself openTarget=block-itself
PASS Q1-standalone-has-title has-title
PASS Q1-standalone-has-nutshell has-nutshell-snippet
PASS Q1-standalone-no-anchor no-<a>
PASS Q1-standalone-no-href no-href
PASS Q1-standalone-no-feed-path no-feed-path
PASS Q1-standalone-is-card-minus-anchors card-minus-anchors
[... Q2 (SN-1887) and Q3 (SN-1886): same 16 checks each, all PASS ...]
PASS EDGE-null-unavailable action=unavailable
PASS EDGE-null-no-feed no-feed-fallback
PASS EDGE-noblock-unavailable action=unavailable
PASS EDGE-noblock-no-feed no-feed-fallback
FAILURES: none
ALL_PASS: true
EXIT=0
```

### Regression — existing 9/9 harness (re-run after the change)
```
test-final.cjs EXIT=0, original9Pass=true, allChecksPass=true,
34/39 #1-with-block (same as baseline), median ~4.09ms.
```
Regenerated results files differ from the pre-run backup ONLY in
timing values (medianTimeMs) — ranks identical. No regressions.

### The five open ranks — NOT decided, NOT changed (owed)
From the fresh test-final run (top-12 window; the 15/17/14-of-50
figures from the earlier measurement are the same five terms):
- C1-04 "not here to prove she is right" — ABSENT in top-12
- C1-05 "mailbox is the main branch" — ABSENT in top-12
- C2-03 "family recipe box" — ABSENT in top-12
- C2-01 "how do I keep my mail private" — rank 3
- C2-06 "nobody reads my mail" — rank 11
Common cause (standing): title > nutshell > block tiering. Fixing
these to #1 needs the exact-phrase spec decision (exact-phrase tier
outranking scattered higher-tier words) — NOT applied silently, NOT
decided here. Ranking code untouched.

## What passes (summary)
- B1 Python full run (fixtures F1–F6 + per-app P1–P6 + live L0–L4b):
  PASS, EXIT 0. Served counts match the independent fresh read exactly
  (394 / 394 / 23), zero row mismatches, per-app reconciliation exact.
- B1 JS mirror fixtures (W1–W11, incl. per-app W8–W11): PASS, EXIT 0.
- Smart Search activation (52 checks): PASS, EXIT 0.
- Smart Search 9/9 harness regression: PASS, EXIT 0, no regressions.
- Baseline reproduction before changes: test-final.cjs EXIT 0,
  original9Pass true, 34/39 #1-with-block — matches the standing record.

## CLAIMED SLICES (staffing correction adopted — do not duplicate)
TEAM BUILD claims these slices; Resolve's build teams should NOT
rebuild them — verify from the receipts below, or build ADJACENT
slices (A11/C5/publisher/pulse/cure serving, live /s/ standalone
route, canonical per-app mapping data):
1. B1 serve-ready worker (Python module + JS mirror + tests + per-app
   computation layer + mapping loader/contract).
2. Smart Search activation-v1 (activation module + tests; ranking
   untouched).
NOT claimed by this team: the face (Nitro), the brief-fields schema
packet (parent, gated), the canonical per-app mapping DATA (FILL
pipeline), the live /s/ standalone route (Hub lane), any landing or
deploy (gated). NO lane work was routed to Tree or Zara at any point:
they are feedback/insight only, and none of this build used them as
workers. (Codex's v4 scorecard and Nitro's adjudication arrived as
context/feedback through the parent, not as lane assignments.)

## Standing-rule compliance (Shawn's three, restated with the correction)
1. Claim before building: slices above are now claimed in this report
   for parent routing to the shared record (this team built (a)/(b)
   before the correction arrived; the per-app layer, built after it,
   is claimed here before any further build on it).
2. Receipt after: every build claim below carries its test output,
   re-readable by another seat (files + commands in this report).
   Nothing counts without its receipt.
3. State and criteria AGREE before any done claim: nothing here is
   presented as done_proven in the record — no record writes were made
   at all. "Proven" in this report means ONLY "proven in workspace
   (or harness) by the named tests". The known 9-row contradiction
   (23 state-done vs 14 fully-criteria-met) is respected: per-app done
   counts use row STATE (done_proven) and carry the same caveat — a
   per-app done count is a state count until its rows' criteria agree.

## What remains for the landing gate (NOT done here, NOT claimed)
- Live endpoint: /pi/api/items does not exist on the merged worker.
  Nitro wires the serve logic in behind the gate; Resolve curls it and
  matches JSON rows to the record (B1's defined proof, still owed).
- A11/C5/publisher/pulse/cure receipts, Nitro re-check, consensus,
  Shawn cold-open tap — all still owed; gate still closed.
- Canonical per-app mapping DATA (see per-app section): UNVERIFIED
  until it lands via the FILL pipeline. Computation proven; data owed.
- Smart Search live route: a standalone block view must exist on live
  (either /s/<sn> serving the block itself, or the live panel opening
  the block view in place as activation-v1 does). Until then the live
  Open failure is NOT fixed — only the harness activation path is
  proven. Live Q4–Q7 baseline still owed (goes into Nitro's rendered
  review per the standing decision, not re-run here).
- Phone-width rendering of anything: UNVERIFIED (not measured here).

## What I need next (from parent, not from seats)
- Routing: hand the B1 Python module + JS mirror to the landing lane
  (Nitro) as the wire-in candidate, and the activation module to the
  Hub lane as the live-Open model — with the live-route gap attached,
  not hidden.
- The canonical per-app mapping file (via the FILL pipeline) — the
  moment it lands, the existing tests prove per-app numbers on live
  data with no code change (pass it via --mapping).
- The exact-phrase spec decision for the five open ranks (Power/Shawn),
  when it is made — ranking stays untouched until then.
