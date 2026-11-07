# A 401 on One Auth Route While Another Stays Healthy Means That Route's Credential Is Dead — Diagnose Per Route

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02218-pat-401-app-healthy-per-route-diagnosis
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 22:08 PST distillation tick (2026-11-06) from hidden_files/learn/branch-api-failure-streak.json (42 consecutive branch-API 401 aborts, last success 2026-10-30T14:38:50Z) and shared-state.json (2026-11-06T14:08Z director note: PAT-route 401 on /rate_limit and /repos/SoulSchoolAcademy/NayaPOWER/issues/3066, same signature as the 2026-11-04 episode when the App route was healthy). Duplicate-checked against the branch tip (SN-2217) via the local mirror plus a git-protocol fetch — no existing note covers the PAT-route 401 streak. Cousins SN-0498 (Supabase credential layers) and SN-0964 (PAT-healthy vs Actions-exhausted bucket conflation) cover adjacent cases, not this one.

## ✦ IN A NUTSHELL

Since 2026-10-30 the PAT route has answered every branch-API call with 401 "Bad credentials" — 42 consecutive learn-ingestion DETECT aborts, zero successful branch reads in a week — while the GitHub App route stays healthy and Smart Note staging already runs on it. The durable rule: **diagnose auth failure per route, never per provider.** A 401 names one credential on one route; it says nothing about GitHub as a whole, the other routes, or the system's overall GitHub health. Conflating them produces two errors at once: declaring GitHub down (wrong — the App route proves it is up) and retry-looping the dead route (waste — a dead credential never recovers by retrying). The correct response is to switch routes, keep the dead route's streak recorded, and let one successful call on that route break the streak. The class distinction is load-bearing operationally: a 401 is a dead credential, never a stand_down — only a 403 sets stand_down. The streak file's standing line, "NOT a 403, so stand_down stays False," is what keeps one dead route from halting every GitHub read in the system.

## 🩷 HUMAN NOTE

Shawn — one of our GitHub keys has been dead for a week: every call made with it gets "bad credentials," 42 failures in a row. The important part is what did NOT break: the other way we connect to GitHub still works fine, and the system already stages Smart Notes through it. The lesson for the team: when one key fails, check that key's route only — don't declare GitHub down, and don't keep retrying the dead key hoping it heals. Switch routes, keep count, and let one good call prove the route is alive again. Filed as Smart Note candidate SN-02218.

## 🟣 CHILD NOTE

Imagine your house has two doors, and you have a key for each. One day the front-door key stops working — it just won't turn. That doesn't mean the house is locked forever, and it doesn't mean you should keep jiggling the broken key all afternoon. You check the back door: your other key works fine, so you go in that way. The broken key is the front door's problem, not the whole house's problem. **When one key fails, blame that key — not the house — and use the door that works.**

## 🔵 GRANDMA NOTE

Dear, the delivery man couldn't get in the front gate — his pass had expired. That didn't mean the street was closed or the house was shut; the gardener's pass at the side gate still worked perfectly. The mistake would be standing at the front gate all day trying the same dead pass, or telling the whole family nobody can visit. You use the gate that works, you write down that the front pass is dead, and you don't stop the whole household over one expired card. **One dead pass is one gate's trouble, never the whole house's.**

## 🟠 NAYA NOTE

Seats running GitHub reads: the PAT route has 401'd "Bad credentials" on every branch-API call since 2026-10-30 (42 consecutive learn-ingestion DETECT aborts; last success 2026-10-30T14:38:50Z; same signature already seen in the 2026-11-04 episode, App route healthy then too). Standing discipline: (1) a 401 is diagnosed per route — switch the failing route to the healthy one (App route / fresh credential) instead of retrying; a dead credential never recovers by retrying. (2) A 401 never sets stand_down — only a 403 does. If you are tempted to halt GitHub reads over a 401, re-read the streak file: "NOT a 403, so stand_down stays False." (3) DETECT must keep aborting fail-closed (exit 2) before any note is read, the old ledger stays untouched, and the streak count keeps climbing until one successful call on that route breaks it. The streak file is the watch; the route switch is the response.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-02218",
  "title": "A 401 on one auth route while another stays healthy means that route's credential is dead — diagnose per route",
  "captured_utc": "2026-11-07T06:08:00Z",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["auth", "credential", "branch-api", "learn-ingestion", "failure-attribution"],
  "enforcement": "The learn-ingestion DETECT step is the standing check: a branch-API 401 aborts the run (exit 2) before any note is read, the old ledger is kept untouched, and update_streak records the consecutive count in learn/branch-api-failure-streak.json. The director pass reads the streak file each tick: at >= 2 consecutive 401s the branch-read route MUST switch to the healthy route (App route / fresh credential) instead of retrying the dead route, and the 2-consecutive chat-report rule fires once. A run that retries the PAT route after the streak reaches 2, or that sets stand_down on a 401, violates this note — caught by the streak file's consecutive_failures count and by the shared-state stand_down_reason field naming the wrong class.",
  "evidence": {
    "streak": "hidden_files/learn/branch-api-failure-streak.json: consecutive_failures 42, last_failure_utc 2026-11-07T05:25Z (run scheduled 21:08 PST 2026-11-06, ABORTED in DETECT, exit 2: gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/git/refs/heads/naya4/smart-notes-2026-09-30 -> HTTP 401 Bad credentials), last_success_utc 2026-10-30T14:38:50Z; pair already reported once at 18:38Z 2026-10-30, this extends the streak, not a new pair.",
    "director_note": "hidden_files/shared-state.json stand_down_reason (2026-11-06T14:08Z tick): GitHub REST auth 401 Bad credentials on /rate_limit and /repos/SoulSchoolAcademy/NayaPOWER/issues/3066 (PAT route; same signature as 2026-11-04 episode, when App route was healthy). Git-protocol tip check still worked.",
    "healthy_route_proof": "hidden_files/bin/stage_smart_note.py routes staging through gh-app-api (App route) since 2026-11-06 with the PAT 401 noted in its header comment; SN-2214..SN-2217 all staged via the App route on 2026-11-06."
  },
  "cousins": ["SN-0498 (Supabase credential-layer diagnostic — diagnose the delivery path before changing the key; this is the GitHub-route companion)", "SN-0964 (bucket conflation — PAT-healthy vs Actions-exhausted 403; this is the inverse direction: PAT-dead vs App-healthy 401)", "SN-01771 (sender-contract-gap-not-auth — the classification this note yields to when the failure line shows an auth 401)"],
  "decision_change": "A seat choosing the auth route for branch reads or learn-ingestion DETECT: previously it would retry the failing PAT route or declare GitHub down; after this lesson it switches to the healthy App route (or a fresh credential) at >= 2 consecutive 401s, keeps the streak recorded, and never sets stand_down on a 401.",
  "mechanism": "Per-route credential validity is independent: the PAT credential is invalid/expired/revoked while the installation token remains valid, so one route's 401 carries zero information about the other routes. DETECT's fail-closed abort plus the streak recorder is the mechanism that surfaces the dead route without burning quota or destroying the old ledger — the abort preserves state, the streak makes the pattern visible, and the route switch restores function.",
  "falsifiability": "A single successful PAT-route GET breaks the streak and falsifies 'the PAT route is dead' — the note then requires updating the streak to a recovery, not extending it. If the App route also starts 401ing, the per-route framing is wrong and the failure is a global auth outage, not a dead route."
}
~~~
