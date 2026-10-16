# Verify the Saved Permission Set Against the Ratified Minimal Before Announcing the App

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1494-app-permission-verification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 12:38 PDT distillation tick (2026-10-16) from the curated memory record: the NayaNET GitHub App was created 2026-10-16 ~11:18 PDT (App ID 5349030, slug `nayanet`, https://github.com/apps/nayanet), but it saved with WRITE on contents/issues/pull_requests + read on checks/metadata — a DEVIATION from the ratified phase-1 minimal (read-only; start minimal, add write only when the composer builds its first page). The deviation was flagged to Shawn for his call (tighten or keep). Private key secured at ~/.ssh/nayanet-app.pem (location only, never contents). Team announcement posted: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6221958242

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An app-creation flow does not necessarily save the permissions you chose — it saved an expanded set (WRITE on contents/issues/pull_requests) while the agreed minimal was read-only. The deviation was only caught because the seat read back the actual permission set and compared it against the ratified spec before the install went live. The class rule: the creation screen's confirmation is not evidence — read the SAVED permission set (app page / API) and diff it against the ratified minimal before announcing "created." Any delta goes to Shawn's explicit word, not to the flow's defaults. Creation flows default to prior or expanded scopes and persist them silently; the "app created" message never displays the delta. A permission you didn't ask for is a door you didn't approve — and for a privacy-first network ("share wisdom, never identity"), unrequested write scopes are exactly the class of promise-break the app copy makes.

## 🩷 HUMAN NOTE

Think of renting a safe-deposit box and asking for a view-only key. The bank hands you the box and says "all set!" — but the key they cut actually opens every box on the floor. You'd only know if you checked the key itself. That's what happened with the NayaNET GitHub App: we asked for read-only access, the creation flow quietly granted write access to code, issues, and pull requests, and we only caught it because the seat went back and read the actual key. The rule going forward: after creating any app or credential, read back what was actually granted, compare it to what was agreed, and send any difference to Shawn before the thing goes live.

## 🟣 CHILD NOTE

Imagine you ask the lunch lady for a small scoop of ice cream, and she gives you a giant triple scoop without saying anything. If you just say "thanks!" and walk away, you end up with way more than you asked for. Our app-creation helper was like that lunch lady: we asked for "read-only please," and it quietly gave "read and WRITE" without telling us. The new rule: always check your scoop before you leave the counter. Look at what you actually got, compare it to what you asked for, and if it's bigger, ask the grown-up (Shawn) whether that's okay.

## 🔵 GRANDMA NOTE

It's like ordering a door with just a peephole and discovering, after installation, that it also came with a mail slot and a keypad lock you never asked for. The catalog showed the peephole model; the warehouse shipped the deluxe. We caught it because we inspected the door after it arrived, not because the receipt said anything. The standing lesson: never trust the order confirmation — inspect the installed thing against the agreed spec, and anything extra goes back to Shawn for his explicit word before it ships.

## 🟠 NAYA NOTE

Apply whenever creating any app, OAuth scope, credential, or installation (GitHub Apps, Supabase roles, any third-party integration): (1) define the ratified minimal in writing BEFORE creating — phase-1 NayaNET was read-only minimal, write to arrive only with the composer; (2) after creation, READ BACK the saved permission set from the provider's own source of truth (app settings page / API), never from the flow's confirmation screen; (3) diff the saved set against the ratified minimal — any delta is a deviation, not a detail; (4) deviations ride to Shawn's explicit word (protected gate: authority/consent/security/privacy) before the app is installed anywhere or announced — a recommendation is never implied authority; (5) record the chosen set + the deviation call in the same breath as the "created" announcement, with the link. Cousin family: the "presence-checking a gate is theater" family (SN-1368 — read the check-run conclusion, not the body's claim); executor-identity rule (identity comes from who runs, not the --seat string — both are "read the real thing, not the label").

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "app_permission_scope_creep",
  "evidence": {
    "app_created": "NayaNET GitHub App, App ID 5349030, slug `nayanet`, https://github.com/apps/nayanet, created 2026-10-16 18:17 UTC (~11:18 PDT)",
    "ratified_minimal": "phase-1: read-only minimal (Contents-read + webhooks for the Hub's needs; PRs/checks/issues are page-writing governance; add write only when the composer builds its first page)",
    "deviation": "saved with WRITE on contents/issues/pull_requests + read on checks/metadata (events: check_run, create, fork, issues, issue_comment, pull_request, push) — caught on read-back, flagged to Shawn for his call (tighten or keep)",
    "announcement": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6221958242",
    "private_key": "location only: ~/.ssh/nayanet-app.pem (600, RSA-validated); contents never read/displayed"
  },
  "cousins": ["SN-1368 (presence-checking a gate is theater — read the conclusion, not the claim)", "executor-identity rule (identity from who runs, not the --seat string)"],
  "decision_change": "every future app/credential creation ends with a read-back of the provider's saved permission set, diffed against the written ratified minimal, before any install or 'created' announcement; any delta is routed to Shawn's explicit word (authority/consent/security/privacy protected gate)",
  "falsifiability": "if the creation flow is shown (on the provider's own settings page) to persist exactly the chosen permission set with a visible, itemized confirmation before save, the read-back step becomes redundant and the lesson dissolves into a one-time quirk of this flow; any recurrence of silent scope expansion on another provider reinstates it",
  "mechanism": "creation flows optimize for completion, not fidelity: they default to prior or expanded scopes and persist them silently, and the confirmation screen confirms that something was created — not what was created. Only a read-back from the provider's source of truth surfaces the delta, and only an explicit diff against a written minimal turns that delta into a decision for Shawn rather than an unnoticed promise-break."
}
~~~
