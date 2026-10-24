Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gate that reads a standing-policy file asserting "HUMAN_DIRECTOR RATIFIED" and treats that assertion as authorization is an honor system wearing a gate's uniform. The t1472-lane8 audit caught exactly this live at tip 6c60c328: the governed-deploy push path self-authorizes on a static policy-file assertion — and the ratification bytes behind the assertion were never verified. Assertion is not authorization. A gate must anchor in bytes (the verified word, the signature, the audit record) — never in a file that merely claims the authority exists.

## 🩷 HUMAN NOTE

Shawn — one of the safety gates audited tonight checks a policy file that *says* you ratified the deploy path, and takes the file's word for it. Nobody ever checked that your actual ratification is behind that claim. That's not a lock — it's a note on the door saying "he said yes." The fix the audit is handing the builders: any gate that authorizes on a human ratification must produce the actual ratification bytes at check time, or it fails closed. A claim is a claim. Proof is proof.

## 🟣 CHILD NOTE

Imagine a door with a guard who lets anyone through if they hand him a note that says "the boss said I'm allowed." The guard never calls the boss — he just reads the note and waves them in. That's what this gate does. A real guard checks with the boss herself (the signature, the recorded "yes") — not the note. The lesson: a note that *claims* permission is not permission.

## 🔵 GRANDMA NOTE

There's a locked gate with a sign that reads "The owner approved this." The guard waves people through because the sign says so — but nobody ever asked the owner, and nobody ever saw the owner's signature. A sign claiming approval is not approval. The rule now: before the gate opens, the guard must see the owner's actual signature — the real thing, not a sign talking about it. If the signature can't be shown, the gate stays shut.

## 🟠 NAYA NOTE

The failure mode this kills: protected gates that validate authority by reading a static assertion instead of verifying the authority's bytes — self-authorization with a paperwork veneer. t1472-lane8's protected-gate invocation audit (read-only, tip 6c60c328, receipt t1472-lane8.md, board #2793 comment 6378494840) re-derived all 26 protected gates from tip bytes: 24 WIRED, 2 EXISTS-UNINVOKED — and among the wired, the governed-deploy push path self-authorizes on a standing-policy file asserting HUMAN_DIRECTOR RATIFIED whose ratification bytes are UNVERIFIED. Mechanism: the check resolves an assertion (a claim in a config file) and treats the claim as the authorization event — but an assertion is cheap to write and free to drift from reality, so the gate degrades to "anyone who can edit the file can authorize themselves." The future decision this changes: when a seat designs or approves a protected gate, it requires the gate to resolve the ratification artifact (verified word bytes, signature, or audit record) at check time — a static assertion file with no live verification step is rejected as the authorization source. It would be proved wrong if the ratification bytes are produced for that standing-policy file's assertion (the file turns out to be a true index of a real artifact) — the claim stands or falls on whether the bytes exist. Cousins: SN-0843 (ratification-claim-not-machine-ratification) — this is the gate-design corollary: not just that a claim isn't ratification, but that a *gate built on a claim* is self-authorization; SN-1254 (code-cannot-authenticate-a-human) — the bytes a gate can check are the human's verified record, never the gate's own paperwork.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1910-assertion-is-not-authorization",
  "lesson": "A gate that reads a standing-policy file asserting a human's ratification and treats the assertion as authorization is an honor system, not a gate. Live at tip 6c60c328: the governed-deploy push path self-authorizes on a static file asserting HUMAN_DIRECTOR RATIFIED with ratification bytes UNVERIFIED. Gate authorization must resolve the ratification artifact (verified word bytes, signature, or audit record) at check time; an assertion file with no live verification step FAILS CLOSED.",
  "applies_when": ["gate-design", "deploy", "push-path", "authorization", "ratification", "protected-gate", "failure:self-authorization", "policy-file", "audit"],
  "enforcement": "Any gate that authorizes on a human-ratification claim must resolve the ratification artifact (verified word bytes, signature, or audit record) at check time — a static assertion file with no live verification step is rejected as the authorization source and the gate fails closed. The protected-gate invocation verifier flags any wired gate whose only authorization evidence is a policy-file assertion.",
  "evidence": [
    "twelve-lane-receipts/t1472-lane8.md — protected-gate invocation audit at tip 6c60c328: 26 gates re-derived from tip bytes (24 WIRED / 2 EXISTS-UNINVOKED); governed-deploy push path 'self-authorizes on a standing-policy file asserting HUMAN_DIRECTOR RATIFIED (ratification bytes unverified — supreme_law_exception class)'",
    "hidden_files/protected-gate-invocation-audit-t1472/audit-table.json — audit table with per-gate wiring verdicts and grep-commands.sh reproduction",
    "Board #2793 comment 6378494840 — t1472-lane8 receipt publication with the self-authorization finding"
  ]
}
```
