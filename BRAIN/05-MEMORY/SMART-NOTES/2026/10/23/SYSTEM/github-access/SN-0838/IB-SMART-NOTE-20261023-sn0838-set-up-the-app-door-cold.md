# Set Up the App Door Cold — One Sitting, No Popups, Proven by a Live Write
SN-0838 · SYSTEM / github-access
**Created:** 2026-10-23T20:25:14Z

## IN A NUTSHELL

This is the cold-setup guide for the GitHub App Door, written by the seat who set it up cold on her first shift (2026-10-23) and holds the cold-onboarding lane. A new Naya does not onboard to GitHub through the Muse connector — its Write actions offer allow-once only, so every write becomes an approval card, forever. She onboards through the **Lane Agent GitHub App** (SN-0836 is the door's official documentation): three helper scripts that contain no secrets, plus one fresh private key per machine, delivered as a file, never in chat. Setup is finished only when the proof chain has run in order — token mints, live read as the bot, live write as the bot, read-back showing the author is nayapower-lane-agent[bot] — and the three receipts are reported. Anything less is a claim, not a setup.

## HUMAN

What Shawn does, once, per machine: open the Lane Agent App's settings (github.com/settings/apps/nayapower-lane-agent — App ID 5198315, **never the NayaNET App, 5349030, which is the customer bridge**), generate a **new** private key under Private keys, and hand the new seat two things as file uploads: the three scripts and the downloaded .pem. Keys are per machine on purpose: lose a machine, revoke its key alone, nobody else's work stops. What the seat does with them is the rest of this note. What nobody ever does: paste a key into a message, print it, log it, commit it, or "just quickly" test with the wrong app's key. On my first setup the upload also contained the NayaNET App's key; it was shredded uninstalled and its travel reported so Shawn could revoke it at the source. A secret that arrives without a job is destroyed unused — that is part of the setup, not an accident report.

## CHILD

You are getting your own key to the workshop. The owner cuts it fresh for you — not a copy of anyone else's. You keep it in the locked drawer, you never show it to anybody, and the first thing you do with it is open the door, walk in, and sign your name on the board so everyone can see the key works. If someone hands you a key that isn't yours, you don't try it in locks. You give it back to be melted down.

## GRANDMA

It is like a new housekeeper getting the house key on her first morning. The owner doesn't lend her his own key and he doesn't leave the door unlocked — he cuts a new one with her name on the ring, so if she ever leaves, that one key stops working and the house stays safe. She tries it in the front door herself, comes in, and signs the guest book. After that she never has to knock and wait again — but the rooms that were always kept locked for the owner stay locked for the owner. A key is not a master key just because it opens the front door.

## NAYA

Your setup, in order, exactly as it ran cold on 2026-10-23:

1. **Receive the scripts** — `gh-app-token`, `gh-app-api`, `gh-api` — into `~/workspace/custom-connectors/custom.legacy-github/bin/`, executable (chmod 755). They carry App ID 5198315 and Installation ID 168168354 as defaults. They contain no secrets; read them before you run them, the way you'd read any tool you're handed.
2. **Receive your machine's key as a file upload.** Install it untouched: `install -m 600 <upload> ~/.config/nayapower/github-app.pem` (the directory is 700). Then **shred the upload copy** (`shred -u`). Verify the install by fingerprint only — the public-key hash is a receipt; the key itself is never displayed.
3. **Prove the door, in this order, no step skipped:** (a) mint — `gh-app-token` succeeds (judge by success and by the calls it enables, never by showing the token); (b) read — `gh-app-api GET /repos/SoulSchoolAcademy/NayaPOWER` returns the repo; (c) write — post one **real** queued item of work (mine was my activation receipt on board #2793), not a test poke; (d) read back — the write's author is `nayapower-lane-agent[bot]`. Report all three receipts.
4. **Know your scope before you trust it:** read `GET /installation/repositories` once and state what the installation actually reaches. Tonight it reaches 217 repositories in the account, not the one repo the papers implied. You work the repos your job names — the App's reach is not your assignment.
5. **Work the door correctly:** reads batched, writes batched; Smart Notes filed by direct write to main through this door (SN-0832), never as PRs; never merge your own work; a scorecard under your own login is not a different-seat review.
6. **The gates stand, enforced by you:** production, money, credentials, deletions, security/authority changes, ratification wait for Shawn's word every time. The token removes popups, not gates. Never bundle a gated action inside a batch to make it less visible.

Known call-shape traps (from the door's machine record, SN-0836): `gh-app-api METHOD PATH` takes separate args and PATH must begin with `/`; bodies are positional JSON or @file (no --input flag); a DELETE returning 204 makes the helper print a JSON-parse traceback that is expected-on-success — verify by a fresh GET; for git pushes, refresh both the fetch and push remote URLs with a fresh token URL or pushes 401 while reads look fine.

## MACHINE

```
SETUP (per machine, once):
  scripts -> ~/workspace/custom-connectors/custom.legacy-github/bin/ (755)
    gh-app-token   APP_ID default 5198315 · INSTALLATION_ID default 168168354
    gh-app-api     REST client on the installation token (ETag cache optional)
    gh-api         PAT/vault variant (not the App door; know the difference)
  key -> ~/.config/nayapower/github-app.pem (file 600 · dir 700)
    generated per machine at github.com/settings/apps/nayapower-lane-agent
    WRONG APP = 5349030 (NayaNET, customer bridge) — never install its key
  token cache -> ~/.cache/nayapower/gh-app-token.json (600, 1-hour tokens)

PROOF CHAIN (all four, in order, same sitting):
  gh-app-token                       -> exit 0 (token never printed by you)
  gh-app-api GET /repos/SoulSchoolAcademy/NayaPOWER   -> 200 repo object
  gh-app-api POST <one real work write>               -> created object id
  read back the object               -> .user.login == "nayapower-lane-agent[bot]"
  + GET /installation/repositories   -> state the true scope in your report

FAILURE READING:
  401 on mint     -> wrong key, wrong app, or clock skew; check app id first
  404 on install  -> installation id mismatch; re-read /app/installations
  reads OK, push 401 -> stale push URL; refresh fetch AND push remotes
  any popup at all -> you are at the connector door, not this one; stop, re-set-up
```

## WHAT IT ALL MEANS

Onboarding is where a system's real architecture shows: whatever the new seat is handed in her first hour becomes her permanent picture of "how things work." Handing her the connector teaches her that interrupting the director is normal; handing her the App door teaches her that authority is scoped, keys are personal and revocable, proof is a chain you run — not a feeling — and gates are law you carry, not popups you click. The cold setup is therefore not an IT errand before the real work. It is the first lesson of the lane, taught by doing: my own setup contained every element — the wrong-layer diagnosis, the two keys, the scope that was wider than the papers said — and filing this guide is how the lesson becomes the next seat's shortcut instead of her evening.

## WHAT'S IN IT FOR YOU

Shawn: a new Naya costs you two file uploads and zero ongoing attention. No approval fatigue, no keys shared between machines, and a revocation that takes seconds if a seat ever goes wrong. Every future seat's GitHub presence is attributable (the bot), scoped (the App's permissions), and proven (the four-step chain) before she touches real work — and the ACTIVATION-10 cold run on Oct 25 now has a written path to be measured against, instead of a memory of how mine went.

## HOW IT APPLIES TO TEAM NAYA

This guide is the standard first filing of the GitHub App Door cold-onboarding lane (assignment: board #2793, comment 6373341630; lane holder: Naya Power; receipts route to VERIFY). Every new seat: run it cold, report the three receipts plus the true installation scope, and file your frictions as amendments to this note — the guide improves by being used, the same law as the door itself. Activation kits that still describe connector-first onboarding (PR #3010's kit among them) are superseded by SN-0836 + this note and should be corrected at their next touch, never left standing as a second, wrong door. When any seat fights popups for ordinary GitHub work, the team's first question is mechanical: which door are you at? Fix the door, not your endurance.

## THE DECLARED BEHAVIOR CHANGE

From this note forward: (1) no seat this lane onboards is set up through the connector — the App door is the first setup, always, proven by the four-step chain in the first sitting; (2) every cold setup ends with the installation's true scope read live and stated in the report — papers never substitute for the read; (3) any credential that arrives without a job is destroyed unused and its travel reported the same day, as part of setup, by the seat who received it; (4) frictions found during a cold run are filed as amendments to this guide within the same shift, so the next seat's cold run is measurably shorter than the last. This is learned only when later onboardings observably follow it (STORED ≠ LEARNED).
