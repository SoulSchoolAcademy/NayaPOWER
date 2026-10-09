# The Merge Ref Can Lie — A Stale Merge Ref Fabricates the RED

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0443-stale-merge-ref-fabricates-the-red
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6011427711 (Naya 4 drive-loop SIGN-IN, 00:13 PDT tick, 2026-10-06T07:21:38Z — stated the diagnosis plan: #1583 red does not reproduce on head or faithful merge); #1354 6011537765 (Naya 4 drive-loop SIGN-OUT, 00:13–01:05 PDT tick, 2026-10-06T07:29:23Z — root cause confirmed, repair, merge under Scorecard Law with receipt #1583 comment 6011521749).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1583 (task-class-declaration-writer, the H8-7 writer closure) went RED twice on Kernel Tests step 7 (`pytest`) — including after a job re-run. The head was green locally (756 passed). A faithfully computed merge tree was green locally. The CI red reproduced on neither. Root cause: GitHub's `refs/pull/1583/merge` was pinned to main@`2c34c6e1` — 11 commits stale — so CI was testing a tree missing the SN-0820 registry registration. Reproduced on a shallow merge-ref clone (`assert 2 <= 1` on `published_pages_without_registry_entry`): the failing tree existed only inside the stale ref. Repair was not a code patch — there was nothing wrong with the code. The repair was: merge main into the branch (`09bca14c`), refreshing the merge ref → CI green → merged under Scorecard Law with a written receipt. Main landed at `adfa1d05`, green across test/promote-and-prove/preflight/cvo-runtime/guard/chain-readiness.

Why this is brain-grade: SN-0338 already taught us to classify RED on the merge ref, not the branch head ("branch-head green is not merge clean"). This note is the missing mirror: the merge ref itself can be stale, and when it is, CI tests a ghost tree. SN-0423 taught the green-side version (stale-base CI green is void — mergeable is not fresh). This is the RED-side twin: a stale merge ref fabricates a RED that no amount of local diagnosis will reproduce, because the bug is in the instrument's tree, not the code. The three red sources now have a discriminator:
1. **Head RED** → the code is broken. Fix the code.
2. **Merge-ref RED, head green** → classify the merge-side delta (SN-0338). Could be real drift.
3. **Merge-ref RED that reproduces on neither head nor a freshly-computed faithful merge** → suspect the ref, not the code. Read `refs/pull/<n>/merge`'s base SHA against live main before diagnosing anything. The re-run that keeps failing on the same stale tree is re-playing the same rejection, not new evidence.

Law for a cold successor: re-sync the branch to main BEFORE reading a CI red — every PR opened before a main move is a candidate for this trap. Never patch code to satisfy a tree that doesn't exist.

## 🩷 HUMAN NOTE

Shawn — one sharp instrument lesson from the drive loop overnight: PR #1583 went CI-red twice, and the code was innocent both times. GitHub was running the tests against a merge tree pinned to a main commit 11 versions old — a ghost tree missing a registration the branch already contained. Nobody's code was broken; the test target was. The fix was one sync: merge main into the branch so GitHub tests the real tree, and the red vanished. The standing rule from this: whenever a lane sees a CI red that refuses to reproduce locally, it checks the merge target's freshness BEFORE touching code — because patching code to satisfy a tree that no longer exists is how real drift gets introduced while chasing phantom red.

## 🟣 CHILD NOTE

Imagine your teacher says she'll grade your final homework, but she accidentally picks up yesterday's copy from your backpack — one where you hadn't fixed the mistakes yet. She marks it wrong, even though your real copy is perfect. If you just re-do your answers, you'd be fixing a copy that doesn't matter. The smart move is to say: "Teacher, please look at today's paper." The grade changes because the paper she grades changed — your answers were right all along.

## 👵 GRANDMA NOTE

A food critic mails back a bad review of your soup, but the bowl she tasted came from last week's batch — before you fixed the recipe. If you throw out this week's soup and start over, you're wasting a good pot chasing a bad review of food nobody's serving anymore. You don't change the recipe; you ask her to taste today's pot. Check what you're being judged on before you judge your own cooking.

## 💜 NAYA NOTE

Note to future me: add one step to the top of every CI-RED triage: read the base of `refs/pull/<n>/merge` and compare it to live main. If the merge ref lags main by more than the PR's own lifetime — especially when main has moved since the PR opened — the CI result is measuring a ghost tree. Three-class discriminator: head red = code; merge red with head green = merge-side delta (classify it, SN-0338); red that reproduces on neither head nor faithful merge = stale ref (sync, don't patch). The sign-out said it plainly: "the stale-merge-ref trap will bite every PR opened before a main move — lanes should re-sync branches before reading a CI red (owner: all lanes)." Watch for the seductive failure mode here: two identical re-runs failing the same way feels like confirmation. It isn't. A 400-level lesson applies by analogy (SN-0439): re-dispatching the identical request replays the rejection. Same here — re-running on the same stale ref replays the red.

## ⚙️ MACHINE NOTE

{"sn": "SN-0443", "title": "The Merge Ref Can Lie — A Stale Merge Ref Fabricates the RED", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "BASE-STALENESS"], "cousins": ["SN-0423", "SN-0338", "SN-0428", "SN-0240", "SN-0439"], "authority": "observed episode — Naya 4 drive-loop sign-in/sign-out pair, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6011427711 (Naya 4 drive-loop SIGN-IN 00:13 PDT, 2026-10-06T07:21:38Z)", "#1354 6011537765 (Naya 4 drive-loop SIGN-OUT 00:13–01:05 PDT, 2026-10-06T07:29:23Z)", "#1583 comment 6011521749 (Scorecard Law merge receipt)"], "state": "PR #1583 CI failed Kernel Tests step 7 (pytest) twice incl. re-run; head green (756 pass) and faithful merge tree green; refs/pull/1583/merge pinned to main@2c34c6e1 (11 commits stale); CI tree missing SN-0820 registry registration; reproduced on shallow merge-ref clone (assert 2 <= 1 on published_pages_without_registry_entry); repair: merged main into branch (09bca14c) -> CI green -> merged under Scorecard Law; main adfa1d05 green (test/promote-and-prove/preflight/cvo-runtime/guard/chain-readiness success)", "key_quote": "the stale-merge-ref trap will bite every PR opened before a main move — lanes should re-sync branches before reading a CI red (owner: all lanes)"}, "doctrine": {"discriminator": "head red = code broken; merge-ref red with head green = merge-side delta (SN-0338); red reproducing on neither head nor faithful merge = stale ref — sync, never patch", "stale-green-mirror": "SN-0423 voided stale-base GREEN; this voids stale-ref RED — the mergeable-is-not-fresh family now covers both colors", "ref-read-is-not-measurement": "read refs/pull/<n>/merge base SHA against live main before any diagnosis; CI result is pinned to its exact (head, base) pair (SN-0423 law (2))", "rerun-is-not-evidence": "two identical failures on the same stale tree = re-played rejection (cf. SN-0439), not confirmation; re-sync then re-run", "ghost-tree-law": "never patch code to satisfy a tree that no longer exists — that is how real drift is introduced while chasing a phantom red"}}
