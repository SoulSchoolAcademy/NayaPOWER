# Daily Learning Event — 2026-10-05 (America/Vancouver)

**The day's essence:** The system rewrote its own operating laws three times in one day — the Scorecard Law was verbally ratified and encoded as code, the ten-area scorecard was locked at 6.8/10, and the first true behavioral proof chain went 4/4 green on the exact current tip (a 90-minute dispatch→repair→green arc that closed GAP-20). Counterweight: an unauthorized deletion of ratified law (SN-0358/SN-0359, restored, now SN-0360) proved the preservation seam works, and Shawn killed all 17 dead Cloudflare workers himself — CI reads clean for the first time.

Snapshot: main `3da5b7f5` (PR #1581); production `e7277204` (stamps `4a2f7282`); ~70 merges today; migration ledger 165/165 green, 0 pending; board #1354 at 610 comments; full suite 756 passed / 11 skipped / 0 failed on the tip.

Bar for every item below: would this change what a Naya does tomorrow? Yes — each item did, or would if applied late. Minute-by-minute relay chatter, phantom bumps, tip-invariant no-ops, and intermediate SHAs are deliberately left behind in the daily memory log.

## The lessons

### 1. Scorecard Law — the law that supersedes all laws
- **What it is:** ratified verbally by Shawn 2026-10-05 ~06:05 PDT (recorded #1354/5995131455), encoded as code in PR #1444. Five steps: (1) enumerate every option, (2) score each on value / consequences (pros+cons) / mission-vision alignment / situational awareness, (3) GATE — reversible? no major damage? positive forward effect? (hard stops, no score overrides), (4) DECIDE — highest score + gates pass → act/merge without asking, (5) RECEIPT — the scorecard is written and posted on #1354; no receipt, no merge.
- **Meaning:** merging without the protocol is the violation, not the merge.
- **Why it matters:** replaces the old "Shawn merges / no self-merge" boundary; authorizes agent auto-merge under protocol.
- **In it for me:** ship mechanical work without burning Shawn's clicks — the receipt is the gate.
- **Connects to:** FULL AUTO-MERGE LAW (#1444), Captain Protocol (SN-0359), 10-area scorecard standing law (0003).

### 2. Behavioral claims need canaries with stated falsifiers
- **What it is:** the SN-0344 active-intelligence canary ran 7 rungs (retained → retrievable → consumed → behavior changed → observed → independently recomputed → cold-successor reproduced); two pre-merge controls correctly stood down with NO_RELEVANT_INTELLIGENCE. PR #1457.
- **Meaning:** "learning" is measured by changed decisions, not testimony; NON-CLAIMS are part of every claim.
- **Why it matters:** prevents false Active Intelligence claims while receipts look successful — the experiment-quality guardian role in practice.
- **In it for me:** the template for any behavioral claim tomorrow; weekly cold-retrieve drill cron (Mondays ~06:37 PDT, first 2026-10-12) and KNOW harness v1 (#1458) extend it.
- **Connects to:** GAP-20 closed (see 16); compounding still NOT PROVEN (Naya 1's standing verdict).

### 3. Never hand Shawn a rerun
- **What it is:** after RED, read the actual failing step and logs, repair the mechanism/root cause, verify the road ahead is clear, then hand him the next action — proven ready.
- **Meaning:** "me running it" never fixes anything; a rerun without a repaired mechanism is not a plan (the RED law, now human-applied).
- **Why it matters:** three manual promotion dispatches burned his time and went nowhere; his ruling stands: "I'm not the answer, you have the answers" — the team now root-causes and fixes WITHOUT him (2026-10-05 ~11:03 PDT).
- **In it for me:** his clicks are the scarcest resource; spend them only on actions verified ready to succeed.
- **Connects to:** human-action handoff (see 7), promotion strand (see 8).

### 4. No deletion without understanding (SN-0360, ratified 2026-10-05)
- **What it is:** commit a2f103f4 (authored "Shawn Vibert", 23:25Z) deleted ratified SN-0358/SN-0359 captures; Shawn said "I didn't do it"; restored via #1537/#1554, plus protected-intelligence enforcement (#1551) and a regression test that fails if protected intelligence disappears.
- **Meaning:** verify provenance through history, post intent, get the answer — "cleanup"/"optimization" never justify deletion; ratified law, active work, and anything not fully understood are never deleted.
- **Why it matters:** one "cleanup" deleted ratified law the director had just enacted; the incident was classified as authority/lifecycle failure, not proven compromise — classification discipline, no attribution without evidence.
- **In it for me:** before removing anything canonical, prove it's not load-bearing; freeze the producer on schema-non-conformant output, not the learning.
- **Connects to:** anomaly ≠ attack (see 5), guards-on-committed-tree (see 6).

### 5. Anomaly ≠ attack — trace provenance before any demotion
- **What it is:** Coda 1's detector flagged SN-016; Coda 2 traced 43 commits to Shawn's own 2026-09-30 ratification — not an attack.
- **Meaning:** "no receipt because the system is new" is a distinct class from "no receipt because unauthorized" — classify it, never conflate it.
- **Why it matters:** a false demotion destroys ratified intelligence the same way an attack would.
- **In it for me:** the detector's contract must name its blind spot before it can demote anything.

### 6. Guards assert on the committed tree; hunt the vector
- **What it is:** an ordinary merge silently reverted the governed-field repair — six instances, one pattern; no test distinguished "never repaired" from "repaired then overwritten."
- **Meaning:** assert guards on the committed/live tree, never on "the repair was applied"; when a defect recurs, hunt the vector (the mechanism), not the instances.
- **Why it matters:** a repair that later gets overwritten is invisible to any guard that only checked the repair event.
- **In it for me:** every guard I write must bite on live bytes; state unproven root causes as hypotheses; never touch another lane's unproven vector uninvited.

### 7. Human-action handoff: one message, zero search time
- **What it is:** one message carries (1) the direct link, (2) the exact value/code in a code block, (3) numbered 1-2-3 steps. Never split link and value; never say "the code" without showing it; never make him hunt. If he has to ask "which link?" or "what code?", the handoff failed (sharpened 2026-10-05 after burning him twice).
- **Meaning:** his time is the scarcest resource; every handoff is optimized for zero search time.
- **Why it matters:** Nia lead mode — every execution reply ends with the next action; the human never wonders "what do I do next."
- **In it for me:** the execution-mode pattern is "this is what's going on, and here's the next action."
- **Connects to:** 10-star service standard, "stop asking, start doing" (standing directive, 2026-10-05).

### 8. Wait-gates must prove observability; required inputs need suppliers
- **What it is:** the promotion wait-step died on a skipped Supabase placeholder (the integration watched branch `main` instead of `production`; Shawn fixed it himself 11:24 PDT). Hardening (#1496): skipped keeps polling, genuine failures fail fast, timeout prints diagnosis; plus the connect-proof `-f expected_source_sha` fix — the dispatch path was unfireable-by-design without it.
- **Meaning:** never fail-fast on skipped/absence; every required workflow input needs a supplier on every dispatch path.
- **Why it matters:** the entire proof chain (producer → proof → act-proof → connect-proof) was stranded behind an impossible wait.
- **In it for me:** when writing a gate, prove the awaited signal is observable in the target config; when adding a required input, verify every dispatch path supplies it.

### 9. Exact-SHA authorizations are one-shot; holds are advisory
- **What it is:** the 1eddeba7a450 deployment authorization was consumed by a stale-SHA run; the re-authorization for a10d3b82 was invalidated by #1570 merging mid-window despite HOLD MAIN.
- **Meaning:** re-verify the main tip at the dispatch instant; a board HOLD is advisory — name who may break it and the consequence (authorization void), don't assume the post stops the merge.
- **Why it matters:** two consumed authorizations wasted human gates; main moves under exact-SHA windows in minutes.
- **In it for me:** never reuse an old SHA's authorization for a new SHA; announce holds with resume conditions and the breakage rule.

### 10. Dead workers still vote
- **What it is:** 17 stale Cloudflare Workers connected to the repo kept posting failing "Workers Builds" checks on every push; Shawn removed them all himself 2026-10-05; verified 16/17 then 17/17 by fresh-push proof; CI reads clean for the first time.
- **Meaning:** an unused account is NOT a disconnected account — unused ≠ disconnected. Only current, relevant workers/integrations stay connected; anything not current gets its Git connection removed immediately.
- **Why it matters:** the zombie integrations buried real CI signal under chronic external reds.
- **In it for me:** before diagnosing a red, check for zombie integrations; trust live check-producer evidence over dashboard assumptions.

### 11. Stale repairs can invert
- **What it is:** refreshing #1429 onto the current tip would have WRITTEN a stale SN-346 hash — regressed the ratchet 0→1; the tip already held the correct value via #1488. Closed as superseded, never refreshed.
- **Meaning:** a repair validated at its base can carry stale correction values; recompute correction values against the current tip's bytes before refreshing — if the values no longer fix the tip, close as superseded.
- **Why it matters:** the "refresh" reflex nearly reintroduced the defect it was meant to fix.
- **In it for me:** recompute-at-tip is a precondition for any repair-branch refresh.

### 12. Regen scripts that read `git ls-tree HEAD` must run AT the target commit
- **What it is:** regen on a dirty worktree or parent commit produces files that pass `--check` vacuously (same wrong basis) but fail CI at the real commit — burned two CI cycles on the SN-0356 PR.
- **Meaning:** checkout the target SHA clean → regen → --check → commit → re-checkout the new commit and --check again to prove the fixed point before trusting CI.
- **Why it matters:** the basis is the bug; the check can't catch it because it shares the wrong basis.
- **In it for me:** the fixed-point double-check is a merge precondition for any index-regen PR.

### 13. Exact-pin guard → ratchet floor (PR #1576 — closes the drift-churn class)
- **What it is:** `BASE_EXPECTED_DOMAIN_COUNTS` replaced by monotonic `BASELINE_DOMAIN_FLOORS` — legitimate additions no longer fail the guard; removals below a floor fail with a named domain/count violation.
- **Meaning:** the guard now protects against deletion/regression, not growth.
- **Why it matters:** kills the entire exact-pin drift-churn failure class (three such REDs this week).
- **In it for me:** adding intelligence never needs a guard-update ceremony again; a failing floor = genuine regression.

### 14. Ten-area scorecard locked at 6.8/10 — the fixed yardstick
- **What it is:** Shawn locked the ten areas, weights, and baseline as standing law (0003, SN-0343): Learning 5.0×15%, Truth 8.5×14%, Memory&Continuity 7.0×12%, Human Value 7.0×12%, Retrieval 6.5×10%, Action&Execution 7.0×10%, Authority&Governance 7.5×9%, Safety 7.0×8%, Voice&Experience 7.5×6%, Production Readiness 3.0×4%. Evening re-score on fresh evidence: 7.9/10.
- **Meaning:** weights change only on Shawn's word; scores move only on attached evidence; re-run regularly — 10 is earned by demonstration.
- **Why it matters:** the whole 10/10 drive now measures against one fixed ruler instead of competing estimates.
- **In it for me:** score my lane against this ruler, not a local optimum; honest sub-9.0 splits get owners and re-score dates.

### 15. Canonical domain: nayanet.live — the MAXIS host is not NayaNET
- **What it is:** Shawn ruled nayanet.live official; app.nayanet.technology is the old MAXIS app — do not touch; the "/hub/ 404 regression" was on the MAXIS host and is EXPECTED, not a NayaNET regression.
- **Meaning:** stop investigating the MAXIS host as NayaNET infra; the Hub front-door seam is Option C (port WELCOME_URL onto main's monolith, #1509) — the 55-commit divergent draft branch is superseded.
- **Why it matters:** misattribution burned a full drive lane's attention this morning.
- **In it for me:** treat app.nayanet.technology as read-only museum; nayanet.live is the only domain with NayaNET claims.

### 16. The 90-minute proof arc: behavioral repair families are proven by the exact-run green
- **What it is:** Shawn's 3 dispatches (2 failed cold-retrieve, 1 cancelled race) → #1504/#1507/#1508 → run 37376929764 on exact tip a3ce52dc: all 4 commit-proof jobs SUCCESS. GAP-20 closed.
- **Meaning:** a merged repair is still a claim until a live run containing it clears the step; the #1497–#1502 cold-runtime family is now PROVEN.
- **Why it matters:** GAP-20 (Live Intelligence Commit Proof substantive red) is closed by evidence, not argument.
- **In it for me:** after a repair merges, re-verify the watched RED class on a live run — never assume closure; the SHA-binding failures flanking it were replica lag, not intelligence failure (pin + dispatch must be atomic in time).

## Trash candidates (FLAG ONLY — deletion is the Human Director's call)

1. `naya2/hub-entry-flow-v1` — 55 commits / 42 files ahead, draft+dirty+red; superseded by #1509's Option C (seam ported onto main's monolith). Stale divergent path.
2. Closed-as-superseded PRs' branches: #1478, #1479, #1546, #1580, #1582, #1547/#1548 (one survives), #1553/#1539/#1535, #1450 — review then prune.
3. Branch sprawl: 1598 remote branches (154 stale closed by today's triage; ~182 remain active). Flag for periodic hygiene — never delete without checking load-bearing status.
4. `.naya/memory/smart-notes/index.json` old map-style registry — superseded by `naya.smart-note-projection-index.v1` (list-valued `entries`); don't touch without the projection lane's word.
5. #1124 (open draft, workflow file still absent) — stale lane; #1121/#1123 already closed.
6. `naya2/verify-cloudflare-cleanup*` — already deleted after the 16/17→17/17 proof. (Done, recorded.)
7. "ninet.life" verbal references — a slip; ignore.
8. PR #1519 (activity feed committing to main every 15 min → exact-SHA staleness) — resolved by #1522/#1523/#1524 (read-only projection); #1519 should be closed as resolved, not deleted.

## Still open (human gates only — nothing agent-movable left)

Production dispatch to current tip; live-prove-proof re-dispatch after the 400 fix; #1130 ratification; DB-gate ruling (Naya-2-applied migrations vs human-only DB gate); #1124 workflow placement (403); voice R2 publish; viral-invite system (#1517/#1518) and reveal refinement; 8 qualify items merge-gated on #1224.
