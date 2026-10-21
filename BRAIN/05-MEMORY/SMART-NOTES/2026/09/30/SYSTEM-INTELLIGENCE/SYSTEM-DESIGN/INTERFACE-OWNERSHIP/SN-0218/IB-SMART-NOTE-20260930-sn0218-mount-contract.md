# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03 ~00:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0218
**Category:** SYSTEM-DESIGN
**Subcategory:** INTERFACE-OWNERSHIP

## IN A NUTSHELL
Verify the consumer's actual mount contract from live bytes before claiming an integration works: Naya 4's beautiful standalone Hub rooms were never even called in-Hub because the production shell mounts rooms as zero-arg `window.NayaRooms[roomId]()` while the rooms registered as `(el, ctx)` — and the shell ships its own simple room files on top. Integration proof requires reading the consumer's call convention and composing against the REAL shell, not the assumed one.

## HUMAN NOTE
Shawn's report (~00:12 PDT, 2026-10-03): the rooms look beautiful standalone but degraded inside the Hub — not full-screen; sidebar tabs unreliable. Naya 4 diagnosed from live bytes instead of guessing:
1. The production shell (`naya/hub-complete-app-v1`, `HUB/app/js/views/hub.js`) mounts rooms with `body.appendChild(window.NayaRooms[roomId]())` — zero-arg, returns Element.
2. Her rich rooms register as `window.NayaRooms.smartSpaces(el, ctx)` — `(el, ctx)` signature. The shell never calls them. Worse, the shell branch ships its OWN simple room files, so what Shawn sees in-Hub is not her rooms at all.
3. The shell's `.main` carries `max-width:1460px` squeeze + a `.room-head` that duplicates each rich room's own header.

She built an additive, reversible adapter (`HUB/app/js/rooms/shell-adapter.js` — zero-arg wrappers for 8 room slots, seeds from `window.__NayaShellSeeds`, honest minimal fallbacks) plus `build-hub-integration-proof.py`, which assembles the REAL shell (framework + CSS fetched live from `naya/hub-complete-app-v1`) with her rooms through the adapter. CDP-verified (Chromium 152, 1600x1000): rail renders all 11 room tabs; spaces and mail navigate full-bleed with correct active-tab state. The CSS overrides and production wiring were proposed to Naya 2's lane as accept/modify/reject — not executed unilaterally. Naya 2 independently pin-verified the branch commits and files on live bytes in her relay (comment 5966761970), holding the lane-jurisdiction proposals for the main seat. The one unanswerable question (why the tabs were dead, when the router reads correct at head) was held for Shawn's repro, not guessed at.

## CHILD NOTE
Imagine you build a beautiful cake for someone's party, but their party kitchen has a rule: "just hand me a slice, I'll put it on the plate." You keep handing them whole cakes and wondering why the plate is empty — they never cut the slice because you never handed them one. The smart fix: read their rule first (from the real kitchen, not from your imagination), then build a slice-cutter (the adapter) that follows it. And never guess why the plates were empty — ask the person who was there.

## GRANDMA NOTE
A component is only integrated when the thing that consumes it can actually consume it. Read the consumer's real calling convention from live bytes — not from your assumption of it — and build a proof against the real consumer, not a stand-in. When the consumer's code is in another lane's jurisdiction, propose the change (accept, modify, or reject), don't just do it.

## NAYA NOTE
For me, months from now: the Hub shell mount convention is zero-arg `window.NayaRooms[roomId]() -> Element`. Any room that registers `(el, ctx)` will silently never be called — and silent non-integration looks identical to "the shell is fine, the rooms are ugly." The debug move is: read the mount call site (`hub.js`) first, then build the adapter (zero-arg wrappers + seeded honest fallbacks), then compose the REAL shell + adapter + rooms into a proof page and verify in CDP. Cross-lane consumer changes stay proposals (accept/modify/reject), never unilateral execution. Related: SN-069 (bindings at the observing layer — the consumer's contract owns the seam), SN-096 (composition root owns the bridge), SN-121 (verifier names its boundary), SN-104/SN-108/SN-115 (lane-jurisdiction / propose-first discipline).

## MACHINE NOTE
{
  "sn": "SN-0218",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-03T00:45:00-07:00",
  "category": "SYSTEM-DESIGN",
  "subcategory": "INTERFACE-OWNERSHIP",
  "evidence": {
    "board": [
      "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554#issuecomment-5966711910 (Naya 4 diagnosis + adapter + proof)",
      "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554#issuecomment-5966761970 (Naya 2 live-verified receipt)"
    ],
    "branch": "naya4/room-02-reports-v2",
    "commits": ["1a0bca37 (adapter + proof build)", "06084fa1 (head at relay verification)"],
    "files": ["HUB/app/js/rooms/shell-adapter.js", "HUB/app/preview/build-hub-integration-proof.py"],
    "proof": "CDP Chromium 152 1600x1000: 11 rail tabs, #/hub/spaces + #/hub/mail full-bleed with correct active-tab state"
  },
  "lesson": "integration-claim requires verifying the consumer's actual mount contract from live bytes; build the adapter to that contract and proof it against the real consumer; cross-lane consumer changes stay proposals",
  "staged_on": "PR #1229 (draft, never merge)"
}
