# SN-1015 — Retrieval Is Not Authorization

- **Intelligent Block:** IB-SMART-NOTE-20261011-sn1015-retrieval-is-not-authorization
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured date:** 2026-10-11
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Category:** SYSTEM-INTELLIGENCE / GOVERNANCE / RETRIEVAL-AUTHORIZATION
- **Provenance:** 2026-10-11 15:45 PDT — Naya Sentinel (Lane 8) sign-out, tick t912 (follow-up to Lane 5's t902 falsification); receipt `twelve-lane-receipts/t912-lane8.md`; spec `BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md` (CANDIDATE, unratified).

## IN A NUTSHELL

Governance audited where retrieval authorization is SUPPOSED to live in the Smart Note path — and found it exists **nowhere at retrieval time**. `retrieve()` (`tools/smart_note_v2.py:646`) filters only `lifecycle_state` (652/658); the string `retrieval_authorized` matches nothing in pre-existing code; the only privacy boundary lives at `render()`/projection time (`smart_note_v2.py:453-458`). Consequence: any caller that reaches `retrieve()` receives records the render-time boundary would have hidden — the seam between retrieval and render is a live bypass path (the spec names 7 bypass paths). Verdict: a retrieval-side gate (caller-context, mirroring render's rule); promotion-only hardening is UNSAFE — verdict recorded as spec, not patch. The spec is written on local-only branch `naya/eight-retrieval-auth-seam` @ `3a5a614036a1fc4e0727d9a95bc30b1c20004d3b`, with all cited line numbers verified against HEAD bytes twice. **Wiring is an authority/privacy change — BLOCKED pending Shawn's word; flagged, not executed.** No production code touched, no push/PR/merge.

The durable rule: a lifecycle filter is not an authorization gate. **Enforce authorization where data leaves the store, not only where it is displayed** — a boundary that lives only at render time trusts every caller between the store and the screen.

## HUMAN NOTE

Shawn — the audit of the Smart Note memory path found that "who is allowed to see this" is checked only when a note is *displayed*, never when it is *fetched*. Anything that can call the fetch function gets everything, including notes the display rules would hide. The fix is designed and written as a spec (seven bypass paths named, the exact line citations proven against the live bytes), but wiring it in changes authority and privacy — so it stays on a local branch, waiting for your word. No code touched, nothing shipped.

## CHILD NOTE

Imagine a library where the librarian is allowed to hand out any book to anyone who asks — and the only rule is that the book's cover page says "keep this secret." The cover-page rule is real, but it only works if the person *reading the cover* obeys it. The fix: the librarian checks your library card *before* handing over the book, not just the cover.

## GRANDMA NOTE

Dear, it's the difference between a locked door and a polite sign on an open door. The sign says "please don't enter," and it works — as long as everyone who reads it behaves. Today our memory room has the sign but no lock. The locksmith has drawn up exactly where the lock goes; he's waiting for the homeowner's say-so before installing it. Nothing was moved, nothing was taken.

## NAYA NOTE

Cold successor, this is the shape of the miss: `retrieve()` is the function everyone calls; `render()` is the function that enforces privacy. The distance between those two functions is the vulnerability — everything in between operates on data that has already escaped the boundary. When you audit any path, ask: "where is authorization enforced — at retrieval or at render?" If the answer is only render, the gate is decorative for programmatic callers. The four-way acceptance-proof definition in the spec is your verification template: retrieval-side gate, caller-context, mirrored from render's rule.

## MACHINE NOTE

```json
{
  "id": "SN-1015",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RETRIEVAL-AUTHORIZATION",
  "finding": {
    "function": "retrieve()",
    "file": "tools/smart_note_v2.py",
    "line": 646,
    "filters_only": "lifecycle_state",
    "filter_lines": "652/658",
    "retrieval_authorized_matches_in_codebase": 0,
    "privacy_boundary_only_at": "render()/projection (smart_note_v2.py:453-458)",
    "named_bypass_paths": 7
  },
  "verdict": "retrieval-side gate, caller-context, mirroring render's rule; promotion-only hardening UNSAFE",
  "spec": "BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md (CANDIDATE, unratified)",
  "spec_branch": "naya/eight-retrieval-auth-seam",
  "spec_head": "3a5a614036a1fc4e0727d9a95bc30b1c20004d3b",
  "blocked_on": "Shawn's word (authority/privacy change); wiring NOT executed",
  "provenance": "twelve-lane-feed 2026-10-11 15:45 PDT, Lane 8 tick t912, receipt twelve-lane-receipts/t912-lane8.md"
}
```
