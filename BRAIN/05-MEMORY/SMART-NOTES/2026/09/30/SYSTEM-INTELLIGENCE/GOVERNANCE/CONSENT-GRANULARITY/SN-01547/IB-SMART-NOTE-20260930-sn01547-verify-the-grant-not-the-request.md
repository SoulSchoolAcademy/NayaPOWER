# Verify the Grant at the Enforcement Level, Not the Request at the Manifest Level

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01547-verify-the-grant-not-the-request
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** 2026-10-16 ~21:19–23:13 PDT live sequence (recorded in MEMORY.md "APP PERMISSIONS — TWO-LEVEL TRUTH"): Shawn set Checks → Read and write and Actions → Read and write in the NayaNET GitHub App settings (App 5349030); the seat read `GET /apps/nayanet` live, saw checks=write/actions=write, and announced "the 403s should clear" — prematurely. Proved live 23:13 PDT: re-requesting check-run 117300212519 on PR #2718 via the installation token → 403 "Resource not accessible by integration." Root cause: when an app's permissions change, each installation must separately ACCEPT the new set — until then the installation token keeps the OLD scopes. Outstanding at capture: the installation acceptance click (installation 168168354).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A GitHub App's permissions live at two levels: what the app REQUESTS (the manifest — what the settings page and `GET /apps/<slug>` show) and what each installation GRANTS (the access — what the installation token can actually do). A permission increase creates a pending "accept new permissions" state on every installation; until the installation owner accepts, the token keeps the old scopes and 403s on the new ones. I verified the request level, announced "fixed," and was wrong — the installation token proved it at 23:13 PDT with a 403 on a check-run re-request. The rule: verify the grant at the level where it is enforced (installation-token behavior), never at the level where it is requested (the manifest). A settings page is a menu, not a grant.

## 🩷 HUMAN NOTE

Imagine you upgrade your gym membership at the front desk — the computer says "Premium," you walk to the pool, and the turnstile still blinks red. The front desk upgraded your *account*; the turnstile reads your *key card*, and nobody reprogrammed the card. That's exactly what happened here: Shawn upgraded the app's permissions in settings (the front desk), the seat checked the app's page and saw "Premium" (the computer), and announced the pool was open. But the installation token is the key card — it still carried the old permissions until the installation owner clicked "accept" (reprogramming the card), and the live 403 proved it. Check the key card, not the front desk screen.

## 🟣 CHILD NOTE

You ask the teacher if you can use the art supplies. The teacher says yes — but the supply cabinet still has the old lock, and your key doesn't open it. The teacher's "yes" was real, but your key wasn't updated. Saying "the cabinet is open!" because the teacher said yes would be a fib — you have to actually try your key in the lock. Try the key. That's the test.

## 🔵 GRANDMA NOTE

Dear, this is about where you check. When someone tells you a door was unlocked, you don't take their word and tell the whole family to come through — you walk over and push the door yourself. I learned this the hard way in one evening: the settings said the permissions were granted, and I told your father the errors would stop. They didn't. The real test — asking the system to do the thing with the actual token — showed the door was still locked, because the second key (the installation's own acceptance) hadn't been turned. From now on: push the door yourself before you announce it's open. And never be too proud to say "I called it early, and I was wrong" — owning it fast is what keeps trust.

## 🟠 NAYA NOTE

Apply this on every GitHub App permission change, forever: (1) there are TWO levels — requested (app manifest: settings page, `GET /apps/<slug>`) and granted (per-installation: what the installation token can do); a permission increase puts every installation into "pending acceptance" — the token keeps OLD scopes until the installation owner accepts; (2) the ONLY valid clearance evidence is a live installation-token behavior test at the NEW scope — e.g., re-request a check run that needs checks:write and read the result; the manifest read is not evidence; (3) until the test passes, the blocker is named precisely: the pending installation acceptance, with the installation id (here: 168168354) — and only the installation owner can click it, so route it to the right human; (4) never announce "the 403s should clear" from the manifest — that premature call cost an evening of confusion and a correction to Shawn; (5) the premature-clearance pattern generalizes: any permission/grant system with request-vs-grant layers (OAuth scopes, IAM policies, app installations) gets this test — verify at the enforcement level. Cousin map: SN-1494 (app-permission-verification — the REQUEST-side sibling: the creation flow saved broader scopes than chosen; this note is the GRANT-side twin: the requested set was right but not yet granted); SN-1001 (not every 403 is a rate limit — 403s have classes; this note names the permission-acceptance class).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1547,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "verify_the_grant_at_the_enforcement_level_not_the_request_at_the_manifest_level",
  "applies_when": [["github-app","permissions"],["ci","403"],["integration","token-scopes"],["announcement","premature-clearance"]],
  "enforcement": "After any GitHub App permission change, a 'fixed/cleared' claim is valid ONLY with a live installation-token behavior test at the NEW scope (e.g., re-request a check run requiring checks:write and read the result — pass/fail on the wire). Reading GET /apps/<slug> or the App settings page does not count as clearance evidence and must not be cited as such. Until the behavior test passes, the blocker is recorded as the pending installation acceptance with the installation id, routed to the installation owner (only they can click accept).",
  "evidence": {
    "premature_call": "2026-10-16 ~21:19 PDT: Shawn set Checks → Read and write and Actions → Read and write in App settings (App 5349030); seat read GET /apps/nayanet live (checks=write/actions=write) and announced 'the 403s should clear'",
    "live_disproof": "2026-10-16 23:13 PDT: re-request of check-run 117300212519 on PR #2718 via the installation token → 403 'Resource not accessible by integration' — the token still held the old scopes",
    "root_cause": "a permission increase requires per-installation acceptance; until accepted, installation tokens keep old scopes",
    "outstanding": "installation acceptance click (installation 168168354) — only the installation owner can perform it"
  },
  "procedure": [
    "after any GitHub App permission change, do NOT read the manifest as clearance evidence",
    "run a live installation-token behavior test at the new scope (re-request a check run, or the smallest API call the new permission gates) and read the wire result",
    "403 persists → the blocker is the pending installation acceptance: name the installation id and route the click to the installation owner",
    "only announce clearance after the behavior test passes; if you called it early, correct it the same hour"
  ],
  "falsifier": "The doctrine dies if a permission increase is shown to propagate to existing installation tokens WITHOUT per-installation acceptance in some configuration (e.g., a future GitHub behavior change, or certain app/installation types). Test: change a permission, do not accept, probe the token at the new scope — if it works, the doctrine is wrong for that configuration and must be scoped, not universal.",
  "mechanism": "GitHub Apps separate the app's requested permissions (the manifest — a declaration of intent) from each installation's granted permissions (the access actually minted into tokens). A permission increase does not rewrite existing grants; it creates a pending 'accept new permissions' state per installation. Installation tokens are minted from the granted set, so they keep the old scopes until the owner accepts. Reading the manifest therefore verifies the intent layer while the enforcement layer (the token) still fails — the 403 is the enforcement layer telling the truth."
}
~~~
