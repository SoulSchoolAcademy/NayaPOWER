# 🔒 NayaNET Proof-First Release Protocol

**STATUS:** CANONICAL EXECUTION GUARDRAIL  
**PURPOSE:** End the recurring failure where Naya reports a change that Shawn cannot actually see or independently verify.

## The problem

A source commit, green build, successful deployment, or HTTP text-marker check is **not the same thing as proving the product changed for the human who opened it**.

The delivery chain must therefore be treated as a sequence of independent gates:

**SOURCE → ARTIFACT → DEPLOYMENT → EXACT RUNTIME → CONTENT PROOF → VISUAL PROOF → HUMAN APPROVAL**

## The new completion law

A consequential UI mission cannot be called **DONE** until all applicable gates pass.

### Gate 1 — Source proof

Prove the exact authoritative source file changed as intended.

### Gate 2 — Artifact proof

Prove the deployed artifact was built from that exact source.

### Gate 3 — Deployment proof

Prove the artifact was actually published to the intended deployment target.

### Gate 4 — Exact-runtime proof

Fetch the **exact URL Shawn is using**, not merely a configured or remembered URL.

Verify release sentinels and expected content in that response.

### Gate 5 — Visual proof

For UI/design missions, capture screenshots from the **exact public runtime after deployment**.

Minimum Hub proof:

- desktop;
- mobile.

A source screenshot, editor preview, local screenshot, or screenshot of another URL does not count.

### Gate 6 — Human approval

Shawn sees the exact runtime and judges whether the requested human outcome has actually been achieved.

Until then, the state is **VISUALLY VERIFIED — AWAITING HUMAN APPROVAL**, not production-proven.

## Required release receipt

Every consequential UI release must leave a permanent human-readable receipt containing:

- mission;
- exact source file;
- source commit;
- deployment target;
- exact public runtime;
- technical verification result;
- visual verification result;
- desktop/mobile screenshot artifact location;
- anything not verified;
- next action.

The receipt is created **after evidence exists**. It is never used as a substitute for evidence.

## Runtime identity law

**THE URL THE HUMAN OPENS IS THE RUNTIME THAT MATTERS.**

If Naya verifies Runtime A while Shawn is opening Runtime B, the mission is **not verified**.

Runtime identity must therefore be explicit in:

1. deployment configuration;
2. verification command;
3. human receipt;
4. screenshot capture.

## Failure law

Never repeat a failed delivery route merely because it was attempted before.

**STOP → DIAGNOSE → CHANGE ROUTE OR FIX THE WALL → VERIFY AGAIN.**

A failed technical gate is recorded as failed. A missing visual gate is recorded as missing. Neither may be silently promoted to “done.”

## Hub visual success test

For the current Intelligent Hub mission, the human target is:

**LEFT NAV | SMART FEED**

Must visibly be true:

- left navigation remains;
- Smart Feed is the main workspace;
- no persistent right-side feed/activation rail;
- no duplicate Smart Feed;
- no legacy feed mirror;
- center feed is not squished;
- no raw code is rendered into the UI;
- desktop composition is premium and full-width;
- mobile composition is usable and responsive.

## Final law

> **Naya does not get credit for changing code. Naya gets credit for producing the requested human result and proving it at the exact runtime.**

**NO EVIDENCE → NO DONE.**
