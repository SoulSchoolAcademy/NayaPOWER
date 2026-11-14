# A Transport Failure Leaves the POST's Fate Unknown — Verify Existence Before Retrying, or You Mint a Duplicate

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02799-verify-post-existence-before-retry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-lane-scorer-20261114-0050-lane10.md (Lane 10, 2026-11-14 02:13–02:40 PST), F5 + H5.

## ✦ IN A NUTSHELL

Lane 10's 0050 run opened the brain-index re-stamp PR #3371, but the stored `gh-api` credential failed twice — first `RemoteDisconnected`, then 401 `Bad credentials` — and the first POST's fate was UNKNOWN until checked: a PR-creation POST can commit server-side while its response is lost in transit, so the client cannot tell "never received" from "received, response lost." The seat verified no PR existed for the branch (GET → `[]`) before retrying, so no duplicate was created; the retry went through `gh-api-fresh` and succeeded. The rule: a transport failure leaves the write's fate unknown — only a read settles it. Before re-POSTing any write, GET-check that the resource does not already exist; a blind retry mints a duplicate.

## 🩷 HUMAN NOTE

Shawn — imagine mailing a letter, and the post office phone line cuts out right as you ask "did it go through?" You don't know whether the letter is on its way or still sitting in the tray. If you just mail a second copy to be safe, the person gets two letters. The seat in this story did the careful thing: it checked the mailbox first, found it empty, and only then sent the letter again. The rule is that simple: after any send where the answer gets lost, look before you send again — never guess, never double-send blind.

## 🟣 CHILD NOTE

Imagine you press the button to order a toy, but the screen freezes and you can't tell if the order went through. If you press the button again just in case, you might order two toys and have to pay for both! The smart move is to check your order list first: if the toy is already there, you're done; if it's not there, press the button once more. Always look before you press again — that's how you never accidentally order two.

## 🔵 GRANDMA NOTE

Dear, it's like posting a birthday card and the postman shrugs — he can't say whether your first card went into the bag or not. If you post a second card just to be safe, your grandchild gets two cards and wonders what's wrong. The wise thing is to ask the post office to check the bag first: empty means post again, full means you're done. The lesson, love: whenever the answer gets lost, look before you repeat yourself. A second try without a look is how duplicates are born.

## 🟠 NAYA NOTE

Source: gap-lane-scorer-20261114-0050-lane10.md (Lane 10, 2026-11-14 02:13–02:40 PST), F5 + H5. The stored `bin/gh-api` credential failed twice — first `RemoteDisconnected`, then 401 `Bad credentials` — and the first POST's fate was UNKNOWN until checked; the seat verified no PR existed for the branch (GET → `[]`) before retrying, so no duplicate was created. Cure used: `hidden_files/bin/gh-api-fresh` (fresh installation token per call — the established fallback for the recurring PAT 401 episode since ~2026-10-26); all subsequent REST reads/writes via gh-api-fresh succeeded. What this note does NOT re-teach: SN-2218 (a 401 on one auth route while another stays healthy means that route's credential is dead — diagnose per route, switch to the healthy route instead of retrying) and SN-0070 (retry-on-conflict is not idempotency — allocation-uniqueness retries prove one allocation, not one execution). Those name the credential diagnosis and the idempotency distinction; this one names the retry procedure itself: existence-check before re-POST. Cousins: SN-2218, SN-0070.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "verify_post_existence_before_retry",
  "mechanism": "a transport failure can occur after the server has committed the write but before the response reaches the client, so the client cannot distinguish 'never received' from 'received, response lost' from the failure alone; only a read (GET the resource / list by the identifying key) settles the outcome — a blind re-POST re-executes a write that may already exist and mints a duplicate",
  "evidence": "gap-lane-scorer-20261114-0050-lane10.md (2026-11-14 02:13-02:40 PST), F5 + H5: stored bin/gh-api failed twice — first RemoteDisconnected, then 401 Bad credentials — and the first POST's fate was UNKNOWN until checked; seat verified no PR existed for the branch (GET -> []) before retrying, so no duplicate was created; retry via hidden_files/bin/gh-api-fresh succeeded; PR #3371 opened once, head f0fe048b55, mergeable True",
  "falsifiability": "if the POST endpoint carried an idempotency key (same request -> same resource, no duplicate possible) or server-side dedup by request fingerprint, the existence check would be redundant and the rule would not apply to that endpoint; if a blind retry after a transport failure provably cannot duplicate, the rule weakens to a nicety",
  "decision_change": "a future seat whose API POST fails with a transport error GET-checks for the resource (by branch, title, or identifying key) before re-POSTing, and records the GET result in the receipt — never a blind retry",
  "applies_when": ["api-write", "post-retry", "transport-failure"],
  "enforcement": "the lane-scorer receipt audit: any receipt describing a retried API write must cite the pre-retry existence check (GET result) — a retry with no existence check recorded fails the evidence check, and the seat must prove no duplicate was minted (list the resource) before the receipt scores",
  "related": ["SN-2218 a 401 on one auth route while another stays healthy means that route's credential is dead", "SN-0070 retry-on-conflict is not idempotency"]
}
~~~
