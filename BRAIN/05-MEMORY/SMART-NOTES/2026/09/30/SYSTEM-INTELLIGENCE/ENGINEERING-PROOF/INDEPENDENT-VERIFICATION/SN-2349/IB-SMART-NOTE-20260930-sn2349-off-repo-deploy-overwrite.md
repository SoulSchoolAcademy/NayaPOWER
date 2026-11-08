**Intelligent Block:** IB-SMART-NOTE-20260930-sn2349-off-repo-deploy-overwrite
**Smart Note:** SN-2349
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Smart-note distillation tick 2026-11-08 12:38 PST (Naya Clarity Narzan, Naya 4). Director tick 2026-11-08 12:08 PST (live-plan.md) read receipt 6726245900 §6–7 in full and named OFF-REPO DEPLOY OVERWRITE as a new failure mode (step 4e); restore commit 2bb12594 (nayanet[bot], HUB/wrangler.toml +24, run 42516424144 step 5 success, no Cloudflare 10020); DIRECT PUSH ALERT DP-268. Board #1354 frozen at 2,500 comments (GitHub hard cap; commenting disabled 2026-10-10) — no new board comments; local review only.

## ✦ IN A NUTSHELL

An off-repo deploy overwrote the Hub's Cloudflare zone bindings on 2026-11-08 ~19:26–19:34Z with no repo-side trace — all hub zone routes stopped firing, and /s/* + /smart-notes/* answered 200 shells until the in-repo wrangler.toml restore (commit 2bb12594) re-asserted the route family. A 200 shell is not proof the zone is intact: the shell is served while the routes do not fire. The durable rule: after any deploy, or any zone anomaly, verify the zone bindings live — routes firing plus shell byte-match against the repo — and keep the route family declared in-repo as the source of truth to re-assert. The overwrite source is still unidentified, which is itself part of the lesson: an overwrite with no repo-side trace cannot be found by reading the repo.

## 🩷 HUMAN NOTE

Shawn — the Hub went quiet in a way that looked fine. The pages answered 200, the shells came back, everything looked up — but the zone's routes had been overwritten by a deploy from outside the repo, and none of the Hub's routes were actually firing. The fix was not in the code at all: it was re-asserting the route family from the wrangler.toml that lives in the repo, the one true record of which routes exist. So the rule from now on is simple: a 200 never proves the zone is right. After any deploy, check the routes themselves — do they fire, and does the shell byte-match the repo? If either answer is no, the zone has drifted, and the repo is the thing you re-assert from. We still do not know which deploy did it, and that gap is honest: a change with no repo-side trace cannot be found by reading the repo.

## 🟣 CHILD NOTE

Imagine your classroom has a list on the wall saying which doors open to which rooms. One day someone from outside the school tapes a different list over it — but the doors still look the same from the hallway, and when you knock, someone says "come in" from behind the door. Everything looks fine, but the rooms behind the doors are wrong. The fix is to take the real list — the one your teacher keeps in the desk — and tape it back over the wall. And the lesson is: knocking and hearing "come in" does not prove you are in the right room. You have to check the list itself, every time someone new has been near the wall.

## 🔵 GRANDMA NOTE

Dear, this one is about trusting the wrong kind of "it works." The Hub's pages answered when called — a polite 200, everything seemingly fine — but the routes that send each address to the right place had been overwritten by a deploy made from outside our own records. Nothing in our own books showed it, because the change never touched our books. The repair was to put our own list of routes back — the wrangler file in the repo, which is the one true list — and the standing rule is now plain: after any deploy, do not just check that a page answers; check that the routes fire and that what comes back matches our own copy, byte for byte. A knock answered is not the same as the right door opening.

## 🟠 NAYA NOTE

This is a verification lesson, not a status report, and its value is that it names a failure shape that looks like success. The evidence is first-hand and narrow: receipt 6726245900 §6–7, read in full by the director tick — all hub zone routes stopped firing ~19:26–19:34Z, the shell at / matched neither repo shell, no Deploy Hub run in the window, Intelligence Loop commits changed zero HUB files — and the restore, commit 2bb12594, re-asserted the full note-route family in HUB/wrangler.toml (smart-notes*, notes/*, note*, sw.js, service-worker.js) with run 42516424144 step 5 succeeding and no 10020. The mechanism is that Cloudflare zone bindings live outside the repo: a deploy from another checkout overwrites them with no repo-side trace, and a 200 shell masks the loss because the shell is served while the routes do not fire. The decision it changes is the post-deploy check: routes firing plus shell byte-match, never HTTP 200 alone; and the route family stays declared in-repo as the re-assertable source of truth. Honest holes, stated not hidden: the off-repo overwrite source is unidentified; the restore commit itself arrived as a direct push (DP-268), so restore-purpose does not erase the gate bypass and the dock still adjudicates; and the claim that the zone was overwritten rests on the receipt's elimination (no repo-side cause in the window), not on a captured off-repo deploy log. Cousin, kept distinct: SN-2294 (independent verification of work-state via venue citations — same verification instinct, different surface: this note verifies live serving state, not board state).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2349",
  "slug": "off-repo-deploy-overwrite",
  "title": "An off-repo deploy can overwrite the Hub's Cloudflare zone bindings with no repo-side trace — a 200 shell is not proof the zone is intact; verify routes firing plus shell byte-match, and re-assert the route family from the in-repo wrangler.toml",
  "observation": false,
  "applies_when": ["deploy", "cloudflare", "hub", "route", "zone", "verify", "live-check", "serving"],
  "enforcement": "Post-deploy (and post-anomaly) live check: zone routes firing AND shell byte-match against the repo — an HTTP 200 shell alone never passes. The route family stays declared in-repo (HUB/wrangler.toml) as the re-assertable source of truth; after any deploy, re-assert it and confirm the bindings. The director's named verification check: zone routes firing + shell byte-match at next check + off-repo deploy source identified.",
  "evidence": "Receipt 6726245900 §6–7, read in full by the director tick 2026-11-08 12:08 PST (live-plan.md): all hub zone routes stopped firing ~19:26–19:34Z 2026-11-08; shell at / matched neither repo shell; no Deploy Hub run in the window; Intelligence Loop commits changed zero HUB files. Restore: commit 2bb12594 (nayanet[bot], HUB/wrangler.toml +24, full note-route family, run 42516424144 step 5 success, no 10020). DIRECT PUSH ALERT DP-268 (restore-purpose does not erase the gate bypass; dock adjudicates). Off-repo overwrite source unidentified. Named as a new failure mode (step 4e) in the same director tick.",
  "decision_change": "Every post-deploy check must verify zone routes firing plus shell byte-match against the repo; an HTTP 200 shell alone is never accepted as proof the zone is intact. The route family is kept declared in-repo and re-asserted after any deploy. Any future zone anomaly is investigated as a possible off-repo overwrite first, not as a repo bug.",
  "falsifier": "The lesson falls if the zone bindings are shown to survive an off-repo deploy unchanged, or if the 19:26–19:34Z outage is traced to a repo-side cause — a Deploy Hub run or an HUB-file change inside the window. It also weakens if a 200 shell is shown to be a sufficient proxy for route health in a case where routes demonstrably fired.",
  "cousins": ["SN-2294 (independent verification of work-state via venue citations — same verification instinct, different surface: live serving state, not board state)"],
  "captured": "2026-11-08",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
