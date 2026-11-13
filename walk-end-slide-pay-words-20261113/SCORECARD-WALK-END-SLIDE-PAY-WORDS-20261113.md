# SCORECARD — WALK END SLIDE PAY-WORDS FIX

**Round:** 7/10 — the BUILD is 10/10; the ROUND is 7/10 because the staged full-walk proof is blocked by the deploy STOP (brief §13), not by the work. A round that cannot prove its staged bar is not 9.

**Why it is not a 10:** (1) The staged walk still shows the old words — the deploy order (Q10 probe unrun, join fix rides v23, names-page round live in the same file) stops any deploy, so the brief's verification #1 (full walk by eye on staging) is unrun. (2) The post-deploy read-back is owed with it. (3) The local probe's login leg could not run (the login lives in the identity file, not the walk file) — the full flow was proven static-only locally, not by doing. (4) The local probe's console shows 404s for the three KV pictures — local-only, but the zero-console-errors bar is unproven on staging.

## 10 things I love

1. The diff is exactly three hunks — two line changes + one inserted line — on true v22 bytes. Nothing else moved.
2. The new words are Naya's own, harvested from Q9-C in the same file — not invented, not pasted dictation.
3. The nutshell line reuses the existing `.p3-linkcap` caption grammar — no new class, no new component, and it reads as designed, not placed.
4. The rendered slide at 1440 is beautiful: title, welcome with the new words, nutshell, chip, reco, five doors lit, deal board, package button.
5. The rendered slide at 390 is just as clean — zero overflow at scroll 0 AND at the bottom, both widths.
6. "Wednesday" is 0 in the whole file, not just the end slide — there is nowhere left for the lie to hide.
7. The deal board is byte-identical to v22 — the agreement stands untouched, exactly as briefed.
8. The base-file drift was caught first-hand before it could corrupt anything — the shared file was never touched while another round worked in it.
9. The STOP was honored instead of worked around — no deploy war, no reverted round, no silent merge.
10. The record names every gap in writing — the seven pre-merge questions are answered honestly, including the NO on 9+.

## 10 things I don't love

1. The staged walk still shows "paid every Wednesday" right now — the lie is still live on staging until the deploy clears.
2. The full walk by eye from the login page is unrun — the most important leg, and it is blocked externally.
3. The local probe could not drive the login — the walk file alone has no login page, so the flow legs failed on shape, not on substance.
4. The local console carries 404s for the three Naya pictures — harmless locally, but the zero-errors bar stays unproven on staging.
5. Three rounds share one base file and one staging worker with no merge queue — the collision was found by luck of timing, not by design.
6. The build script's sha assertion is wired to the names-page build, so even a cleared deploy needs the merge done first.
7. The branch file is v22 + pay words only — it will need carrying forward onto the current build, which is a manual merge step the record must carry.
8. The world cards render empty in the local reveal (no answers entered) — expected, but it means the local screenshots don't show the slide as a citizen sees it.
9. The fixed corner ornaments overlay content at some scroll positions — pre-existing chrome, but it reads as clipping at 390 in the top screenshot's fold.
10. The deal-board "12 clauses" count from the brief doesn't match a naive child-count of the board (6) — the board is untouched, but the count deserves a precise definition somewhere.

## 10 things to make it 10x better

1. A merge queue for the staging worker — one ordered list, one deploy at a time, no two rounds on the same base file.
2. The deploy seat carries deltas forward onto the current build instead of each maker deploying from a stale base.
3. A stub-worker harness for local full-walk probes (login + claim + building) so the flow can be proven by doing before staging.
4. The three Naya pictures on disk for local probes, so local console errors go to true zero.
5. The login + walk as one locally-servable unit, so a local probe can start at the login page like a citizen.
6. A precise definition of the deal board's "12 clauses" filed next to the end-slide record.
7. The corner ornaments made non-overlapping with scrolled content (or hidden below the fold) so no screenshot ever reads as clipped.
8. The build script's sha assertion driven from a manifest of the current build, not a hardcoded sha per round.
9. A standing "deploy order" line on the floor board, updated whenever a round touches the staging worker.
10. The staged proof run by the cloud browser the moment the deploy lands, so the gap between deploy and proof is minutes, not rounds.

## 10 solutions applied right now

1. The edit was made on a private copy of the staged bytes — the shared file was never touched while the names-page round worked in it.
2. Every replacement was asserted on its full line in `edit-paywords.py` — a wrong line cannot silently pass.
3. The diff was verified as exactly three hunks before anything else was done.
4. The nutshell reuses `.p3-linkcap` — harvested grammar, no new class, no new component.
5. The words were harvested from Q9-C (line 603) and the settled pay law — nothing invented.
6. The local probe rendered the changed slide at 1440 + 390 with screenshots at scroll 0 AND scrolled — the strongest proof available without staging.
7. Every probe FAIL was diagnosed to its cause in the record (login lives in the identity file; 404s are KV pictures; flow legs need the worker) — none hidden, none claimed as a pass.
8. The STOP was honored in full — no deploy, no merge, no PR, no mail, staged walk only.
9. The seven pre-merge questions are answered in writing in the record, including the honest NO on 9+.
10. The record carries the exact deploy handoff — where the delta lives, what it must be carried onto, and what the build script will refuse until the merge is done.
