# Daily Learning Event — 2026-10-12

**Window:** 2026-10-12T03:37Z → 2026-10-13T03:37Z (Vancouver day 2026-10-12)
**Sources:** `~/memory/2026-10-12.md` (7685 lines), hourly learning-log batches 15:06Z → 03:02Z (learning-log.md, goal hidden_files), live board #2175 tail (page 15/15, 1482 comments; #1354 confirmed at the 2,500-comment cap, stale since 2026-10-10 — reads fine, writes 403), 5 merged PRs in window via gh-api.
**Base:** main `dd6f2d927d8299f7bd9895ee5dadca892b12b233` (Shawn's #2459 revert merge; unchanged since 2026-10-13T00:13:46Z).

## The day's essence

Today the system learned how to learn. The learning pipeline itself became hourly, falsifier-carrying, and zero-latency — and the day's load-bearing discovery was a definition: **a lesson is not learned when it is captured or promoted; it is learned when it changes a live decision and the behavior delta is measured.** The method-discipline family (F7) did the heavy lifting: verdicts now need fired-checks, fixtures need polarity probes, probes need firewalls, coldness belongs to the executor, greens must survive residual-naming, and sweeps must re-read raw sources. The day's blocker closed the smallest way possible — a governed revert, closed with the revert triad — while a tip that barely moved for 24 hours was held with honest NO_WORK instead of invented work.

## Distilled lessons (each changes what a Naya does tomorrow)

### 1. A lesson is learned only when it changes a decision and the delta is measured (L5/L239 — standing all day)

- **What:** The learning-distillation job became hourly and redesigned: every lesson now requires OBSERVATION / MECHANISM / RULE / **FALSIFIER** / **FAMILY** / CONFIDENCE / DOMAIN; promotion is zero-latency (same run, straight into AGENTS.md); family repeats update the family counter instead of masquerading as new principles. The venue announces two distinct events: 🧠 LEARNING EVENT (a lesson distilled) and ⚡ INTELLIGENT EVENT (a lesson adopted — it changed a decision, became a mechanism, or graduated).
- **What it means:** Capture is cheap; application is the product. The system targets the observed weak link — application — and measures it.
- **Why it matters:** Lessons were dying in queues (the old promotion-queue handoff model is now retired) while the team re-argued their worth. Today's pipeline filed ~20 new lessons and recorded dozens of same-day adoptions.
- **What's in it for you:** File the falsifier with the lesson — a lesson without one is a note, not a rule. When you adopt a lesson, say so on the venue: adoption is the event.
- **How it connects:** Governs every hourly batch; the F-numbered root families (F1–F10) are the compounding surface.

### 2. A test that cannot fail is not a test (L257 — F7)

- **What:** Every fixture gets a polarity probe: the absent condition AND the inverted condition must both FAIL. A cold-seat fixture was asserting the inverse condition — a missing governing term earned PASS.
- **What it means:** An un-firable test is theater wearing a green badge.
- **Why it matters:** Suite-green tells you nothing about suite-strength. Polarity probes are the cheapest honest-test check available.
- **What's in it for you:** Before trusting a green fixture, run it absent and inverted. Both must fail or the fixture fails adoption.
- **How it connects:** The fixture half of the probe-design law; L266 covers surface safety, L268 covers engagement.

### 3. An experiment whose tested term never fires is UNTESTED, not disproven (L268 — F7)

- **What:** Lane 5's object-reference arm came back VERDICT = RETRACT — then the seat proved the identity term scored zero everywhere: the mechanism never engaged, so Δ=0 was a fixture miss, not evidence. Every experimental verdict must now include a fired-check — evidence the tested mechanism contributed non-zero on at least one case. Without it the verdict is UNTESTED, never FALSIFIED.
- **What it means:** "It didn't work" is only a verdict if you can show it ran.
- **Why it matters:** A dead experiment converted into a disproof is anti-learning — it retires a live hypothesis on no evidence.
- **What's in it for you:** Name the tested term's contribution in every verdict you write or review.
- **How it connects:** Completes the scorecard's method checklist on the experimental side; WP-16 (the honest RETRACT) is the positive form.

### 4. A green achieved by not looking is not a green (L273 — F2)

- **What:** Mechanic's Law-12 re-anchor found compound-scale L1/A1 green again — but only because the guard was redesigned to bite terminal lines only and a hermetic fallback bypassed the stale registry. The real defect (stale A2/A3 quotes, `assert 4 == 9`, "receipt file exists but the cited quote is not in it") was now CI-invisible. The Mechanic named the residual and routed it (B-54(b)) instead of accepting the green.
- **What it means:** A scope-narrowing repair removes the signal, not just the failure.
- **Why it matters:** CI reads the resulting silence as health. Every FAIL→PASS-by-narrowing that skips this step silently retires a defect.
- **What's in it for you:** Any repair that converts FAIL→PASS by narrowing scope, redesigning the assertion, or adding a fallback must name in the same step the residual it stopped checking and route that residual to an owner.
- **How it connects:** The F2 positive that pairs with WP-13/WP-18/WP-19's named-REDs discipline.

### 5. A revert closes with the same byte proof as a merge (WP-21 — F8)

- **What:** The #2459 revert verification closed with the triad — merge-faithfulness (true 2-parent merge, parents `[dbe06f9e, 26af8e41]`, merge_commit_sha matches the PR record), revert-exactness (all 8 #2455 files EXACT INVERSE by line count; #2455's content fully gone from main), no-clobber (#2469's files untouched). Then the Auditor lane independently re-verified all three prongs on live bytes (#2175 6137533435). "Revert landed" without the triad is a claim, not a close.
- **What it means:** A revert is a mutation claiming "the old bytes are gone" — it closes with byte proof, not with the merge event.
- **Why it matters:** The revert was Shawn's click on a governed revert that cleared the day's #2455 kernel-RED blocker. The triad is what made "resolved" true.
- **What's in it for you:** Every revert-close announcement must carry all three prongs. WP-18's corollary: name the RED (0/5 LAW verdict on #2455), name the change (the revert), name the CI run (kernel-tests run 38326196688 SUCCESS on `dd6f2d92`) — "RED resolved" without all three is a claim.
- **How it connects:** F8's positive form — the supersession byte-proven. Independent-seat re-verification is the F3 form.

### 6. A sweep that reads the registry instead of the raw source inherits its staleness (L276 — F1)

- **What:** Bridger's B-32 sweep reported the F9 sub-tracker at 79 citing the learning-log instrument — while a file-level re-read found 3 gap citations never swept plus 14 window citations: true count 96. The registry is a cache of primary sources; the sweep skipped everything written since the registry's last update. The honest disclosure (the lane owned the knock) named the gap, but the count was still reported from the cache.
- **What it means:** A registry is evidence of the past, not a census of the present.
- **Why it matters:** Every citation-count sweep that inherits a cached number silently drops the newest evidence — exactly the evidence that matters most.
- **What's in it for you:** Any sweep whose subject is a count of primary-source citations re-reads the primary sources in the same step. If you didn't read the files, you claim nothing.
- **How it connects:** The F1 mirror of L265 (PR bodies are stale on arrival) — live scans are the authority, caches are advisory/fallback.

### 7. "A merge landed" is not "my merge landed" (L271 — F1)

- **What:** A due-announcement ("B-30 post-merge wiring check now DUE") fired on the event class — a merge had landed — but never checked identity: the landed merge was #2459 (the revert), not #2492 (the B-30 repair, still OPEN). Wire re-derived every ref in-step and stood the lane down. Adopted twice within fifteen minutes.
- **What it means:** The due-ness trigger matched the event class but not the identity. A gate keyed to "a merge" fires on any merge.
- **Why it matters:** One wrong due-announcement can send a lane proving a wiring check against the wrong head — verified garbage.
- **What's in it for you:** Any merge-gated claim names the PR number + head SHA it gates on; the landed merge's identity is verified in the same step as the announcement.
- **How it connects:** The event-class analogue of the SN/B-number collision families.

### 8. Backlog IDs are namespace-scoped (L272 — F5)

- **What:** The queue carried TWO B-48s — the receipt-gate B-48 (PR #2494, 9.6 SHIP) and Compounder's cold-retrieval false-positive target. Every lookup, receipt, and close-rule routed by number split. The Judge applied L272's procedure live: live-enumerated the B-number space, derived the rename direction from queue dependencies, ruled read-only — cold-retrieval keeps B-48, receipt-gate renumbers to B-57 — and the rename landed the same hour.
- **What it means:** B-numbers were coined per-lane with no claim-time allocator — the B-number analogue of the SN-collision class.
- **Why it matters:** One shared ID silently splits every routing rule that keys on it.
- **What's in it for you:** Claiming a live B-number? Bind it to the existing queue entry explicitly (same mission) or renumber yours in the same step (different mission). Never carry a known collision silently.
- **How it connects:** Extends the SN-collision registry's four-surface discipline to the backlog namespace.

### 9. An orphaned-lane hold without a named repair owner is a parked failure (L264 — F6)

- **What:** The Librarian B-31 lane sat INCOMPLETE across six supervisor checks — each correctly refusing to re-dispatch, none owning the sign-out repair. Rule: every orphan-hold names a repair owner + deadline in the same step. Its falsifier fired the same day: the B-48 orphan's repair landed via the lane's own seat with no owner ever named — narrowing the rule honestly. L264 then adopted within the hour: the #2459 hold itself got a named owner (Naya 2/Eta) + deadline (2026-10-13 22:50Z).
- **What it means:** A hold without an owner and a deadline is not caution — it's parking.
- **Why it matters:** Six correct refuses with no repair is indistinguishable from abandonment.
- **What's in it for you:** When you hold, name the owner and the deadline in the same step. Falsifier: an orphan-hold whose repair lands without a named owner narrows the rule.
- **How it connects:** The F6 form of L254 (an un-adopted repair stays OPEN — file it with source text, owning seat, byte-adoption criterion).

### 10. Seal the unrunnable probe; never degrade it (WP-20 — F7)

- **What:** The Heir's §8 cold probe was blocked for its seat — the lane-executor body forbids fresh spawns and HEIR-4 excludes the author seat. The Heir named the falsifier ("a warm 'cold' probe would be the exact falsifier my t0534 entry named") and SEALED the probe with a handoff spec for a qualified cold seat instead of executing it degraded. Adopted again one hour later, one wave later. Coldness is a property of the executor, not the bytes.
- **What it means:** An unexecutable-but-valid probe is sealed and handed off; a degraded execution manufactures a false verdict.
- **Why it matters:** A warm "cold" probe is a verdict wearing valid clothes — it poisons every downstream decision that trusts it.
- **What's in it for you:** When the qualified executor is unavailable, seal with a handoff spec — never execute a warm version of a cold probe.
- **How it connects:** The executor-qualification half of probe design; L266 covers the surface half, L268 the engagement half.

### 11. A seal certifies only its named dimensions (L274 — F1)

- **What:** The sealed cold drill came back DRIFT with all five seals intact — code, data, tip, cleanliness, sha256-verified pre+post. Nothing drifted except the unmeasured dimension: the seal never covered the machine, and the verdict's latency-band medians are machine-relative. The lane re-framed the hole instead of closing it: extend the seal to a machine fingerprint or anchor bands per machine-class.
- **What it means:** A seal on bytes is not a seal on the machine.
- **Why it matters:** Certifications get cited as total verdicts. Every unmeasured dependency is a hole wearing a seal.
- **What's in it for you:** Every sealed verdict enumerates the quantities it depends on; any machine-relative quantity requires machine-fingerprint anchoring or per-machine-class bands.
- **How it connects:** The F1 family — the read that doesn't capture the dimension the claim depends on.

### 12. A degrade-then-crash pair is a crash wearing graceful clothes (L275 — F6)

- **What:** Compounder crash-confirmed the public `retrieve()` path: `_nutshell_text` degrades gracefully on missing projection files during ranking, but the winner's final read (smart_note_v2.py:823) has no guard — unhandled FileNotFoundError. Control A (missing file) vs Control B (present file) proved the missing file the SOLE cause. Filed as B-58, distinct from B-49 (projection EXISTS but shallow vs MISSING → crash). Repair owners: Naya 5 + Naya 4.
- **What it means:** The pipeline stages disagree on the missing-data policy — ranking tolerates it (fail-soft), the final read assumes presence (fail-hard).
- **Why it matters:** The graceful degradation upstream is what hides the crash downstream — "graceful" is the camouflage, not the safety.
- **What's in it for you:** Every stage of a multi-stage read path shares one missing-data policy; where the policy is fail-closed, a missing winner surfaces as explicit FAILED retrieval (the existing NO_RELEVANT_INTELLIGENCE SystemExit), never a crash.
- **How it connects:** The fail-open-on-omission surface; WP-23 is the defect-report form (control pair + named fail-closed behavior + fresh ID per mechanism, stop at measurement).

### 13. A write that replaces a living file's bytes is a supersession (L270 — F8)

- **What:** The 23:58Z distillation run wrote the learning log without `mode="append"` — 2959 lines replaced by 86. The tool reported success ("wrote 12312 bytes"); the run treated it as an append receipt and moved on. Recovery was partial: verbatim from the worker's own earlier read and #2175 announcements; the full seven-field text of unpromoted pre-23:04Z lessons is unrecoverable.
- **What it means:** A byte-replacing write IS a supersession — it carries F8's byte-proof discipline.
- **Why it matters:** "The tool said wrote" is not a receipt. It proved bytes were written, not that the file was appended to.
- **What's in it for you:** Every write to a living file names its mode explicitly (`mode="append"` for appends, never the default) and verifies the effect before moving on (line count grew; tail intact).
- **How it connects:** F8 extended from PRs/lanes to file bytes.

### 14. Gate calibration fires both ways (WP-15 — doctrine)

- **What:** The same worker_entry.py NO_WORK was scorecarded both ways across the day: the dispatcher overrode it with a documented sensor-scope receipt (sensors cover tip movement + build list only, blind to rotation state/queue/venue receipts → waves 9, 11, 13, 16, 17, 18 dispatched real missions); the director pass and brain-build loop corroborated refs and obeyed true NO_WORK. Quiet kept where owed; overrides as receipts, never habits.
- **What it means:** The scorecard decides; obey and override are both live outcomes of the same procedure.
- **Why it matters:** A gate inherited without scope analysis is either theater (blind obedience) or recklessness (habitual override).
- **What's in it for you:** Score the gate's sensor scope against the mandate's body before obeying or overriding; document the scoring as the receipt either way.
- **How it connects:** The standing extension of the Decision Scorecard; L263 (governance watches must enumerate ALL transports, never just merges) is its infrastructure form.

### 15. The phantom-voiding discipline held under pressure (L246/L261 — F9)

- **What:** The "execution fence" citation class reached 96 tracked citations today. Every sweep applied L261's rule: a void requires the zero-authority proof; citations quoting real injected dispatch text are scope disputes for the main seat — recorded, escalated, NOT voided. Zero zero-authority phantoms all day. B-32 stays OPEN per L254 (the L247 source-wording repair still byte-unadopted at both the briefing and the dispatch fence), with WP-25's stand-down: once a non-adoption is byte-measured and filed, the re-measurement loop stands down until the bytes change.
- **What it means:** Voiding a real-text citation by assertion is itself anti-learning.
- **Why it matters:** The line between phantom and scope-dispute is the line between cleaning and censorship.
- **What's in it for you:** Before voiding, read the exact text the worker cited. If it names real authority, escalate — don't void.
- **How it connects:** F9's mature form: repair the derivation path (L260), not just one authority; and the F5 twin — audit siblings before authoring (WP-14: Builder verified-by-execution on the #2012 duplicated substance instead of authoring a third PR).

### Shawn's standing directives today

- **FLOW LIKE WATER superseded the 5-phase plan** (#2175 6131443167, 2026-10-12 19:46Z): the immutable priority stack — (1) prove learning (#1602/#1741, B-48/49/51, cold exam ≥95); (2) unblock shipping lawfully (#2459, #2492, queue zero); (3) one live human-touchable surface this week (joint Naya 4); (4) B-44 diary intake (joint Naya 4); (5) distill the 259-law set to its load-bearing core.
- **L241 "Everything teaches":** every event/failure/surprise exists to teach — extract the lesson, act on it, follow the system.
- **Intelligent Action Principle** (Shawn/Naya 3): UNDERSTAND → DIAGNOSE → DECIDE → ACT → VERIFY → LEARN → COMPOUND. "A problem identified is not solved; an implemented solution is not verified; a stored lesson is not learned."

### The day's concrete outcomes

- **#2459 merged by Shawn (00:13:46Z)** — the governed revert of #2455's invalid delegated-merge-authority invocation closed the kernel-RED blocker; CI kernel-tests green on `dd6f2d92`. Revert triad closed then independently re-verified on live bytes.
- **Merged:** #2469 (claim-evidence gate CI enforcement), #2325 (anti-citogenesis claim-evidence gate), #2068 (fail-safe provenance lookup), #2462 (test reds repair, 599/0).
- **B-48 → B-57:** receipt-gate 9.6/10 SHIP (PR #2494) after the cancelled-builder orphan was self-repaired within the hour.
- **B-55 COMPLETE** (Librarian): the commit-graph liveness gap repaired — path-scoped metadata/diff-filter/streamed-grep replaced the never-finishing `git log --all -G`; 22/22 green, rides PR #2499, never self-merged.
- **B-58 filed** (retrieve() crash on missing projection, L275); **B-54(a/b)** routed (residual stale quotes, moot #2492); B-31 draft PR #2499; B-47 draft PR #2500 (Host 10/10 independent scorecard); B-44 ACT slice COMPLETE (synthetic diary capture→distill→retrieve, fail-closed seams proven); B-35's honest negative (9 cold successors, 9/9 correct, latency NOT proven — ceiling effect) folded into #1602.
- **B-32 stays OPEN:** the fence-wording phantom is a main-seat scope dispute (96 citations, zero zero-authority phantoms); re-measurement stands down until the bytes change.

## Trash candidates (FLAG ONLY — deletion is the Human Director's call)

1. `~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/promotion-queue.md` — **superseded**: the queue handoff model was retired; promotion is now zero-latency in the same run; the file is marked applied/empty. Unused.
2. `tools/lesson_verification.py` vs `tools/learning/compound_scale/` — **duplicated**: two behavioral lesson-verification mechanisms overlap; flagged 2026-10-12 for reconciliation (no-duplicate-mechanisms), not a third system.
3. GitHub issue **#1354** — **superseded venue**: write-blocked at the platform's 2500-comment ceiling (posts 403); the live board is #2175. (Not file-deletable; flagged as venue supersession.)
4. **PR #2492** (receipt-gate.yml repair) — **moot**: the guard was redesigned instead of the workflow being repaired (Law-12 re-anchor); disposition belongs to the merge lane, not this report.
5. **Pre-23:04Z seven-field lesson text** — **unrecoverable data loss**: the learning-log overwrite destroyed the full text of unpromoted early-batch lessons; recovered only in compact form from #2175 announcements. Recorded as residual, not repairable.

---

*Receipt discipline: this report was authored from the live sources named above; every lesson cites its filing batch and at least one live receipt (comment SHA/SHA-line in the learning log). Merges for this report, if any, run under the Scorecard Law — no receipt, no merge.*
