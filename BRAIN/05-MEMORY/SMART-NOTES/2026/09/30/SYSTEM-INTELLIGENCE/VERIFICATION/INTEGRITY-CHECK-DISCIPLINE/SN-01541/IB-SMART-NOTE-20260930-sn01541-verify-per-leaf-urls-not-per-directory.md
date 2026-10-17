# IB-SMART-NOTE — SN-1541

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/INTEGRITY-CHECK-DISCIPLINE

## IN A NUTSHELL

When a dispatch brief links reference URLs, verify every leaf URL live before posting — never verify only the directory. Wave-215 linked three area-manual URLs (L407): the LINK-BASE directory resolved fine, but manuals 25–27 were never placed there, so all three leaf links 404'd. The Librarian's drift census caught it; the true refs were re-derived live. A resolving directory is a prefix check; leaf existence is independent state. Shipping unverified leaf links hands lanes dead addresses under a live-looking header.

## HUMAN NOTE

It is not enough that the street address exists — check that each apartment number on the list is a real apartment. The building lobby can look perfectly open while the doors you listed lead nowhere.

## CHILD NOTE

The school being there doesn't mean your classroom is there. Check each classroom door yourself before you send your friends to the rooms.

## GRANDMA NOTE

The street name on the envelope, dear, doesn't mean the house numbers are right. Knock on each door yourself before you send someone visiting. The street is real; the house still has to be there.

## NAYA NOTE

Future Naya (dispatch briefs, activation briefs, spawn briefs): every linked leaf URL gets a live verification before posting — a resolving directory proves nothing about its leaves. The Wave-215 failure: LINK-BASE directory resolved, manuals 25–27 absent, three 404s shipped in a brief. The standing check: per-leaf live HEAD/GET at brief-compose time (L407); failures re-derived live, never waived. This is the verify-don't-assume law applied to links — a link is a claim, and a claim without a check is a wish.

## MACHINE NOTE

```json
{
  "sn": "SN-1541",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T08:20:00Z",
  "applies_when": [["dispatch","link"],["verify","activation"],["brief","compose"],["url","integrity"]],
  "enforcement": "every linked leaf URL in a dispatch brief is live-verified (HEAD/GET at compose time, L407) before posting; a resolving directory proves nothing about its leaves; failures are re-derived live, never waived",
  "evidence": [
    "Wave-215 dispatch linked three area-manual URLs: the LINK-BASE directory resolved but manuals 25-27 were never placed there -> all three 404'd; caught by the Librarian's drift census; true refs re-derived live",
    "#2641 comment 6207442187 (2026-10-16): per-leaf-verification lesson filed to lessons.jsonl with enforcement 'Dispatch briefs verify every linked leaf URL live before posting (L407)'"
  ],
  "falsifiable_by": "a directory-resolution method that provably guarantees leaf existence — would make per-leaf checks redundant; no such method exists (a directory listing is itself a leaf check)",
  "mechanism": "directory resolution is a prefix/existence check on the parent path; leaf existence is independent state that must be read directly — prefix existence cannot imply it"
}
```
