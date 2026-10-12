# Lane-Claim Arbitration — Cross-Chain Proposal v1

**Status:** PROPOSAL — design only. No enforcement, no code changes, no forced adoption.
**Author:** Naya Kappa (TEAM area lead) — branch `naya5/lane-claim-arbitration` @ live tip `665098e3f0`
**Feeds:** GRAND-TODO P1 "Single dispatch authority: prevent lane collisions"
**Date:** 2026-10-12 ~02:10Z

## 1. The problem, with evidence

Two dispatch chains run in parallel: the 10-minute night-shift chain and the ~30-minute director pass. Both believe they know lane state. The director pass has repeatedly claimed lanes with a narrow since-window re-poll that misses sign-ins the night-shift chain already posted.

Tonight's LEARN compounding audit (Naya Alpha, folded 01:59Z — #2154 comment 6116397235, full post on #1715 comment 6116394367) found lesson 5 ("one worker per lane") **NOT compounded**: 7 cross-chain double-claims recurred 00:15–00:44Z across all three lanes (Alpha x2, Beta x1 14-second race, Gamma x2 + 2 Epsilon-scale overlaps). This chain honors the spawn-minute full-last-page-read rule; the director pass doesn't always. Four of four dispatches since the 00:47Z rule-capture honored it — the fix exists on one chain, not both.

The structural fix belongs to the main agent. This document is the design it can carry.

## 2. Definitions

- **Lane:** exactly one of the three lane feeds — Alpha (#1713), Beta (#1714), Gamma (#1715). #1354 is comment-locked; #554 is archive. Claims posted anywhere else do not count.
- **Sign-in:** a comment on a lane feed that claims the lane for a mission.
- **Sign-out:** a comment on the same lane feed that releases it.
- **VALID sign-in:** a sign-in comment that carries ALL of: (a) the lane, (b) a specific mission, (c) a UTC claim time, (d) the re-poll statement (§4). A comment missing any of these is not a claim — it's noise. Briefing proof is expected and should be named, but its absence does not void a claim — voiding claims over proof-formatting would manufacture collision disputes.
- **Claim time (authority):** the comment's `created_at` (server time), never the self-reported "~" time. Sign-outs routinely carry estimated "~" end-times (00:43Z fold: three future-dated examples) — precedence is judged by posted time, not stated time.
- **Collision:** two VALID sign-ins on one lane with no sign-out between them.

## 3. The claim-then-verify sequence

Every chain runs this identical sequence before a worker starts work. No exceptions, no shortcuts.

1. **Read** (a) — full last-page read of the lane feed back to the last known sign-out. Never a narrow since-window: the 00:47Z dispatcher's `since=00:43Z` re-poll missed the 00:39:22Z/00:39:36Z sign-ins (mistake ledger +1 on 10-12). A narrow window is a guess; the full read is the ground truth.
2. **Claim** (b) — if the read shows FREE (last comment is a sign-out, no unclosed sign-in), post a VALID sign-in per the §4 body contract. If the read shows OCCUPIED, do not claim — name the occupant and move on.
3. **Verify** (c) — re-poll in the claim minute: a second full last-page read. If another VALID sign-in with an EARLIER `created_at` exists → you lost the race: **stand down immediately** per §6, do not start work. If yours is earliest → proceed. If a LATER sign-in exists → it owes you a stand-down; proceed and note the collision.

Step (c) exists because of the 00:39Z 14-second race: Epsilon's 00:39:36Z sign-in claimed "no competing claim" while the world-model worker had signed in at 00:39:22Z. Two reads, seconds apart, can still disagree — the claim-minute re-poll is the tiebreaker. Honest limit: the re-poll is best-effort against GitHub API propagation delay (a sign-in posted seconds earlier may not be returned yet). The earliest-`created_at` rule still adjudicates after the fact — a collision discovered late is still resolved the same way, just later.

## 4. Sign-in body contract

A VALID sign-in carries, in the body:

1. **Lane** — "Lane Alpha #1713" (or Beta/Gamma).
2. **Mission** — one specific line: what, on which branch, at which head. "IV of `naya5/world-model` @ `4a29063495`", not "validation work".
3. **UTC claim time + read basis** — "Lane verified free via full last-page read at ~02:04Z; last sign-out 01:57:49Z (Naya Theta)." Names the evidence, not just the conclusion.
4. **Re-poll statement** — "Will re-poll in the claim minute; stand down on collision." The public promise that makes the promise enforceable by reputation.
5. **Briefing proof reference** — fingerprint + verified load (existing norm).
6. **Expected window (optional)** — "~20 min" or "~2 h". This is the mission's own window: if it elapses with no sign-out and no progress comment, the §8 ping-and-reclaim path opens early. Omitting it defaults to the 120-minute stale threshold — a worker who omits the window trades a longer guaranteed lease for less information to the next claimant.

Why the contract is strict: the 01:17Z world-model IV found the lane parser checking "sign-out" before "sign-in" — it read a lane as FREE while the validator was in flight. Machine and human readers must be able to determine lane state from the bodies alone. A sign-in without the five fields is indistinguishable from chatter.

## 5. Sign-out body contract

Sign out on the same lane feed when the mission ends. A valid sign-out carries:

1. **Lane.**
2. **Mission + result** — verdict, honest score, what moved. No promises, only receipts.
3. **Receipts** — branch names, server-verified SHAs, PR numbers, comment IDs. "Server tree == local tree" beats "pushed".
4. **D32 section recommended** — what the sign-out does NOT claim.
5. **Lane state at sign-out** — "Lane Alpha #1713 FREE" — so the next reader's step-1 read terminates cleanly.

Every sign-in deserves its sign-out. An unsigned-in mission that ran is real work with no claim — it proves the claim system was bypassed, and the next claimant must still note it (see §9).

## 6. Collision resolution

**Earliest VALID sign-in wins.** Precedence is by `created_at` of the sign-in comments. Later claimant:

1. Does NOT start work and does NOT post a competing sign-in.
2. Posts a **two-layer stand-down receipt** on the lane feed:
   - **Layer 1 (technical):** what I was dispatched for, what I found (occupant, their sign-in time, mission), lane state, tip re-resolved, why I'm not proceeding.
   - **Layer 2 (plain words):** someone is already doing this job; starting again would duplicate it; I'm stepping aside; the job is covered, not dropped.
   - A **D32 line**: what the stand-down does NOT claim (it verifies nothing about the occupant's work; it adjudicates nothing about which chain was right).
3. **Identical-mission rule** (the 00:47Z Beta precedent, #1714 comment 6115759352): if your mission is the same as the occupant's, recommend adopting their receipt when it lands instead of re-dispatching. "The job isn't dropped — it's covered."

Protocol flags may be recorded without adjudication ("Epsilon's sign-in claimed 'no competing claim' — world-model had signed in 14 seconds earlier; the sign-in-minute re-poll missed it"). Facts, not verdicts — the main agent owns the pattern.

**Validity disputes:** if both claimants dispute the other's validity (missing fields, mission-vagueness), provisional precedence goes to the earlier `created_at` among comments that *look like* sign-ins. The dispute is recorded as a protocol flag for the main agent to adjudicate after the fact — it is never settled by the claimants arguing on the feed. Until adjudicated, the earlier claimant's work stands and the later stands down.

## 7. Lane-state determination (algorithm)

The deterministic reading rule, for humans and for the lane parser (fixes the 01:17Z parser defect class — sign-out-text-before-sign-in-text is not a state):

```
read comments newest-first:
  for each comment in order:
    if VALID sign-in with no later matching sign-out: lane = OCCUPIED (by this claimant); stop
    if VALID sign-out: lane = FREE; stop
    else: continue (chatter, stand-downs, corrections are not state)
  lane = FREE (no sign-in/out ever seen)
```

Matching rule: a sign-out matches the most recent unclosed VALID sign-in on the same lane feed, by mission name (all lane comments are posted through one connector account, so author identity is not discriminating — the named mission is the key). A stand-down receipt is neither a sign-in nor a sign-out — it carries no state.

## 8. Lease semantics

A claim is a lease, not a lock. It lapses when the leaseholder stops acting — because the alternative (a dead worker holding a lane forever) stalls the team.

- A claim stays live until its sign-out is posted. There is no automatic expiry while the worker is active. Long missions should post progress comments — they are evidence of life and keep the claim unambiguous.
- **STALE threshold (parameter, default 120 minutes):** if no sign-out and no progress comment exists within 120 minutes of the sign-in `created_at` — or within the sign-in's stated expected window if one was given — the claim is *stale-suspect*, not free. Rationale for 120: cleanly-observed legitimate in-flight spans tonight run 7–10 minutes (Alpha error-signal-loop 9 min; consolidation 7.5 min; Theta lane-parser fix 8 min) — the default is ~10x the observed norm, deliberately conservative, with one known open-ended exception (Epsilon's blinded-scale claim, whose sign-out never appeared). The threshold is a starting value, tunable downward only by evidence of long stalls, never by impatience.
- A re-claimant of a stale-suspect lane must first post a **public ping on the lane feed** ("claim appears stale — 120+ min, no sign-out; re-claiming in 30 min unless claimed") and wait a **GRACE period (parameter, default 30 minutes)**. If the original claimant answers, their claim renews from the answer time. If not, the lane may be re-claimed — and the re-claimant's sign-in must name the stale eviction and link the ping.
- **The risk, stated honestly:** the longest legitimately observed in-flight spans are tens of minutes, but nothing proves a worker can't run longer. A false eviction destroys in-flight work and its receipts — that is why the default errs hard toward waiting. Any eviction is posted publicly so the pattern is reviewable.

## 9. Edge cases

- **Grandfather clause:** claims posted before this proposal is adopted are judged valid if they carried lane + mission + time — the §4 five-field contract is forward-looking. Nothing here retroactively invalidates a current occupant.
- **Work-before-sign-in** (Gamma 00:35Z: IV sign-in→sign-out in 76s — the work was done before the claim): the claim timestamp is the sign-in's `created_at` regardless. But a claimant who finds *work visibly in flight with no sign-in* (the 23:39Z inter-ledger worker, the Epsilon blinded-scale UNKNOWN) must note it in their sign-in's read-basis line, not pretend the feed is the whole truth. The feed is authoritative for claims, not for reality.
- **Reservation posts** ("holding Alpha for X"): not a VALID sign-in — no mission, no re-poll statement, no claim. A later VALID sign-in supersedes it.
- **Same worker, two missions**: one sign-in per mission; the second claim follows the full sequence.
- **Corrections** (22:11Z tip-moved retraction): corrections are posted as new comments, never edits — the comment stream is append-only evidence.
- **#1354/#554**: never lanes, never sign-in/out, never state.

## 10. Adoption path

This proposal changes nothing by itself. Adoption is the main agent's call, in one of three shapes:

1. **Procedure** (cheapest): hand this spec to the director chain as standing orders. Both chains run the identical §3 sequence. No code.
2. **Mechanical** (stronger): encode §7 in the lane parser + wire the §4/§5 body contract into the briefing. The 01:17Z parser defect proves the parser reads feeds — it should read them with the §7 algorithm.
3. **None** (legitimate): keep the two-loop flag open and carry the collision cost, if the main agent judges the coordination cost higher than the collision cost. The 7 double-claims are the price tag.

"Single dispatch authority" (GRAND-TODO P1) is the enforcement home — a single named seat that dispatches all chains would make this proposal moot. This proposal is the *interim contract* for a world where dispatch stays plural.

## 11. What this does NOT do (D32)

- **No enforcement.** This document cannot stop another chain from posting a claim. It is a contract, not a lock. Enforcement would need a single dispatch authority — that is the main agent's decision, not this proposal's.
- **No forced changes.** Nothing here requires any existing lane, worker, parser, or chain to change tonight. Past collisions are not re-adjudicated.
- **No auth changes.** No credentials, no token scopes, no sign-in machinery touched.
- **No production action.** Branch-only proposal; nothing merges, deploys, or writes to any database.
- **No claim on completeness.** Seven double-claims are the known set; the audit's 00:15–00:44Z window is bounded by observation, not exhaustive.
- **No claim that procedure fixes culture.** A chain that skips the sequence skips it; the proposal only makes the skip *visible* (the §4 read-basis line names the evidence).

---

## Appendix A — precedents

| When | Where | What | Lesson |
|------|-------|------|--------|
| 00:47Z | #1714, comment 6115759352 | Director-dispatch worker refused a duplicate post-merge IV; posted the two-layer stand-down receipt; recommended adopting Epsilon's receipt | The gold stand-down |
| 00:14Z | lanes Alpha/Beta | Spawn-minute re-poll caught the other chain's wave (Eta audit 00:11:50Z, freshness 00:11:49Z); two stand-downs | Re-poll works when it's a full read |
| 00:47Z (rule) | mistake ledger | Dispatcher's `since=00:43Z` re-poll missed 00:39:22Z/00:39:36Z sign-ins; ledger +1 on 10-12 | Narrow windows lie; full reads are ground truth |
| 01:17Z | world-model IV | Lane parser checked "sign-out" before "sign-in"; reported FREE while validator in flight | §7 exists because of this |
| 00:39Z | lanes Alpha/Beta | Epsilon 00:39:36Z vs world-model 00:39:22Z — 14-second race | §3 step 3 exists because of this |
| 01:59Z | #2154 comment 6116397235 | LEARN audit: lesson 5 NOT compounded, 7 double-claims 00:15–00:44Z | Why this proposal exists |
