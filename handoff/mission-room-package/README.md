# Mission Room Package for Nitro — The Living List room (view)

Built 2026-10-23 (Resolve lane, Current Project Intelligence page build) on the
state-core's live published registry. Everything claimed below is verified at
filing time; nothing here is deployed, and no production write has happened.

## Contents — `handoff/mission-room-package/`

| File | What it is |
|---|---|
| `mission-view.html` | THE VIEW. A single self-contained room document in the Hub design language (obsidian stack, purple signature, spectrum state accents, 18px body, the Reports room's token set). It holds **zero** list content: on open it fetches the Living List registry (`WORK-ITEMS.json`, published by the state-core to branch `live/mission-state` every 10 minutes) and renders client-side; it re-reads every 60 seconds. The freshness line comes from the publisher's `generated_utc`; state older than 25 minutes raises a loud STALE banner; a failed read shows a loud error and zero items. There is **no baked fallback** — the Reports defect is not copied. |
| `test_mission_view.js` | THE PROOF. A Node harness that runs the view's own render code against the published registry snapshot plus adversarial fixtures (stale publisher, DONE-without-proof, BLOCKED-without-owner, program filter, HTML escaping). 60 checks. Run: `node test_mission_view.js [path-to-WORK-ITEMS.json]`. |
| `work-items.snapshot.json` | The published registry bytes the harness ran against (the 2026-10-23T01:07:00Z publish, 32 items). A test fixture only — the view never reads it. |

## What it renders

- The one ranked queue, all 32 items. THE LIST (#2953)'s 23 Best-of-Best
  elements are the registry's Best-of-Best programs (core ×3, Wave 1 ×5,
  Wave 2 ×5, Queued ×10) — on the page, programs are filters, never separate
  queues, matching the registry law.
- Per row: rank, title, state chip (QUEUED · CLAIMED · IN PROGRESS ·
  VERIFYING · DONE+PROVEN · BLOCKED · NEEDS SHAWN), owner, note, PR link with
  its live PR state, last-moved time. DONE rows show their proof link and who
  verified them; BLOCKED rows show the blocker and the unblock owner;
  stalled claims and drift flags render loud, straight from the published
  data.
- Registry laws enforced in the render as a second line of defense: a DONE
  row without a resolving proof link renders UNVERIFIED with a
  law-violation flag, and a BLOCKED row without blocker + owner likewise.
  (The publisher already refuses both; the view refuses to present them as
  sound if they ever appear.)
- Sections in director order — Needs your hands → Blocked → Being worked on
  now → Verifying → Done, with proof → Queued — rank order inside each, plus
  an Up Next strip (ranks 1–5) under the cover and the recent-movement
  stream at the foot.

## Wiring steps (canonical build — Nitro's lane)

1. Serve `mission-view.html` as the room document for route `/rooms/mission`
   — the same treatment as the Reports room document at `/rooms/reports`
   (a distinct document with its own title: "Mission — NayaNET Intelligent
   Hub").
2. Register the room in the home build's room registry: name "Mission",
   display title "Mission — The Living List", accent `#9d75ff` (the purple
   signature; the view's `--accent-mission`), target `/rooms/mission`.
   Placement among the primary rooms is your design call; suggested directly
   after Feed, since this is the team's working surface.
3. No generator or bake changes: the view needs no config, no keys, no build
   step. Its single data line (the CONFIG block at the top of the script)
   reads
   https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/live/mission-state/WORK-ITEMS.json
   (that host serves `Access-Control-Allow-Origin: *`). At deploy, confirm
   once from the nayanet.live origin that the read succeeds and the items
   render; if the worker ever wants same-origin data, `DATA_URL` is the one
   line to change.
4. Sentinel coverage in the same change (the expectations file's own rule):
   add a Mission marker to `tools/hub_build_expectations.json` — the room
   page `/rooms/mission` contains "Mission — NayaNET Intelligent Hub" and is
   distinct from home. If you would rather the main seat land that, say so on
   the PR and it follows as a small separate PR.
5. Do NOT wire any of this into `HUB/app/` or the disabled
   `deploy-hub-cloudflare` workflow — canonical build only. (PR #2968, the
   stale-copy retirement, proceeds on its own bar.)

## Verification already done (builder seat)

- Harness 60/60 against the real published registry (2026-10-23T01:07:00Z
  publish) plus the adversarial fixtures listed above.
- Registry → publish fidelity: 0 field diffs (state / owner / rank / proof)
  across all 32 items between the registry source and the published
  WORK-ITEMS.json.
- The data chain observed advancing on the state-core's 10-minute tick with
  no human touch (generated_utc readings recorded in the PR evidence).
- Spot checks, rendered output vs published registry, field for field:
  LL-001 (BLOCKED, Nitro lane), LL-002 (NEEDS SHAWN), LL-004 (VERIFYING),
  LL-005 (IN PROGRESS, stalled + drift rendered), LL-010 (BLOCKED, Kappa
  lane), LL-015 / LL-016 / LL-017 (DONE+PROVEN with proof links to PRs
  #2945 / #2946 / #2947), LL-032 (rank 32, QUEUED).

## The one remaining step after deploy

LL-004's last step — and this page's DONE+PROVEN — is a live-render
confirmation by a seat that did not build it. The main seat's independent
checker is dispatched for exactly that the moment the room is live; her
verdict moves the registry row. Until then the row honestly reads VERIFYING.

## Rollback

Remove the room-registry entry and the document. The data chain (registry →
state-core → `live/mission-state`) is untouched by this package and keeps
publishing either way.
