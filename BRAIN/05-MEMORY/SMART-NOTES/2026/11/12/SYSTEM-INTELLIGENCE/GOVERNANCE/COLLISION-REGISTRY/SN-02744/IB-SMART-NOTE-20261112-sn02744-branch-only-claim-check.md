**Intelligent Block:** IB-SMART-NOTE-20261112-sn02744-branch-only-claim-check
**Smart Note:** SN-2744
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 16:30 PST. Evidence read first-hand from local bytes plus git protocol (zero REST quota): shared-state stand_down=false, issue_1354_comments=2500 <= board watermark 6101230756, so no GitHub fetch per budget law; local lesson review only. Live-main check this tick: git ls-remote main 621c8be6, then fetched and scanned — max SN on live main SN-2741 (Intelligence Loop run 205 landed SN-2740/SN-2741 on main while this tick ran; this tick's first plan, SN-2740/2741/2742, was re-numbered to SN-2742/2743/2744 after the fresh live-tip check). Staging-script claim check read in source (hidden_files/bin/stage_smart_note.py). Colliding branch note read from the branch at 5d2bc065.

## ✦ IN A NUTSHELL

The 15:38 tick staged branch SN-2739 after "verifying it free in every readable domain" — but main already held SN-2739, filed one minute earlier. The check read main tip e3c06103 from a stale mirror, never the live tip. The staging script's claim check scans the branch tree only, and the counter lags main by the director's cadence — neither can see direct-write notes that land on main without touching the branch. A number is free only when the live main tip says so, named by its SHA.

## 🩷 HUMAN NOTE

Shawn — we just had two different notes both called SN-2739: one on main (today's intelligence report) and one on our branch (the recount lesson). The tick that staged the branch one checked carefully and still got it wrong, because it checked a saved copy of main that was a few minutes out of date — the report had landed on main in between. Our staging script only checks the branch, and our counter only updates when the director runs, so neither one can see a note that went straight onto main. The rule going forward is simple: before taking a number, ask main itself what its newest commit is, right then — never trust a saved copy. The branch note is being renumbered to SN-2742.

## 🟣 CHILD NOTE

Imagine you want a new cubby number, so you look at a photo of the cubbies taken this morning and pick an empty one. But while you were looking at the photo, someone put their things in that very cubby. The photo was true when it was taken — but it wasn't true anymore. You have to look at the real cubbies, right now, not the photo. The counter and the saved copy are photos; the live main tip is the real cubbies.

## 🔵 GRANDMA NOTE

Dear, two notes ended up with the same number because the helper checked an old photograph of the shelf instead of the shelf itself. A new note had been placed on the shelf one minute before, and the photograph didn't show it. The lesson is plain, love: when you need to know what's taken, look at the shelf with your own eyes, in this very moment — never trust yesterday's picture, and never trust a list that someone else updates when they get around to it.

## 🟠 NAYA NOTE

The verified facts: (1) Main holds SN-2739 as "Daily Intelligence Report 2026-11-12" (filed 23:46:08Z, commit window 23:38–23:46Z, tip addf0de6 per main-seat verification). (2) The branch holds a different SN-2739, "Count the queue at write time" (staged ~23:47Z by the 15:38 distillation tick, branch commits a4eaa4ee, 5d2bc065). (3) The staged note's own Provenance line records the check that failed: "main tip e3c06103 — BRAIN tree 2026/11/12 holds SN-2672..SN-2738 (SN-2739 absent)" and "SN-2732 and SN-2739 verified free in every readable domain." The tip e3c06103 predated the intelligence-door window that landed SN-2739 on main; the check read a cached mirror tip, not the live tip. (4) The mechanism has three blind legs: the staging script's claim check (hidden_files/bin/stage_smart_note.py) scans the branch tree only; the counter file updates on the director's cadence and lagged main (read 2731 while main already held SN-2738); the mirror's cached main lags live main by however long since its last fetch. Direct-write intelligence-door notes land on main without touching the branch, the counter, or the mirror — so all three legs can agree a number is free while main already holds it. (5) The collision is already in the learn ledger: the 00:08:48Z ingestion run ingested the branch SN-2739 while main's SN-2739 existed; the branch note is renumbered to SN-2742 this tick (first claim stands, the colliding lane renumbers) and the ledger reconciliation is owed to the learn owner. (6) What is NOT new here: SN-0145 already prescribes the correct check (run the candidate number against every date partition on main plus the SN-115 three layers) and SN-0169 already requires a "verified free" claim to name the layers checked. This note is not that prescription — it names the two false authorities that bypassed it (the script's branch-only guard and the counter/mirror cache) and the mechanism by which they stay blind (direct writes never touch them).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2744",
  "slug": "branch-only-claim-check",
  "title": "A branch-only claim check cannot prove a number free: verify against the live main tip, not the counter or the mirror",
  "observation": false,
  "applies_when": [["staging", "number-collision"], ["claim", "freeness-check"], ["verification", "live-tip"]],
  "enforcement": "Before taking a number, run git ls-remote for the live main tip, fetch that exact SHA (git protocol, zero REST quota), and scan main's SN range; the staging script's branch-only claim check and the counter file never count as freeness proof. A staging whose provenance cannot name the live tip SHA it checked and the max SN found on it is not verified.",
  "evidence": "Main SN-2739 Daily Intelligence Report 2026-11-12 filed 23:46:08Z (tip addf0de6, main-seat verified); branch SN-2739 recount-queue-at-write-time staged ~23:47Z (commits a4eaa4ee, 5d2bc065). Staged note's Provenance names the stale tip e3c06103 and claims 'verified free in every readable domain'. stage_smart_note.py claim check scans the branch tree only (source). Counter read 2731 at staging while main already held SN-2738. This tick's live-main check: ls-remote main 621c8be6, fetched, max SN on live main SN-2741. Intelligence Loop run 205 landed SN-2740 (paired NN 'The Captain's Report') and SN-2741 (paired NN 'The Fourteen Questions') on main during this tick — after this tick had already planned SN-2740/2741/2742 from an earlier tip (88b7c101, max SN-2739). The plan was re-numbered to SN-2742/2743/2744 only because a fresh ls-remote ran immediately before staging. Ingestion run 00:08:48Z ingested branch SN-2739 while main's SN-2739 existed. Existing doctrine checked and NOT duplicated: SN-0145 (check every date partition on main), SN-0169 (verified-free must name layers checked) — this note names the false authorities that bypassed them.",
  "decision_change": "Every future staging reads the live main tip (ls-remote + fetch that SHA) immediately before taking a number; 'verified free' must name the tip SHA and the max SN found on it; the script's branch-only claim check and the counter are treated as secondary, never sufficient.",
  "falsifier": "A staging that performs the live-tip check immediately before staging and still collides would show the check insufficient (the residual race: main moves between check and stage — the window must stay tight); zero collisions across subsequent stagings supports the check.",
  "cousins": ["SN-0145 (self-collisions cross date partitions — number uniqueness is brain-wide; the issue-time check runs the candidate number against every date partition on main)", "SN-0169 (a compelled renumber clears the same three-layer registry; 'verified free' is an evidence-bearing claim)", "SN-0033 (the collision registry and the index stamp — first claim stands)", "SN-0115 (three-layer collision registry: board, PR heads, commit graph)", "SN-1650 (pin the PR's state before pinning its head — same check-live-state family)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```