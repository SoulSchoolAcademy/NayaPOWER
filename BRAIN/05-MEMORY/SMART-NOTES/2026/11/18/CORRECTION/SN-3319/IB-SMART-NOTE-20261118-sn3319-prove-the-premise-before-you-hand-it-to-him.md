# Prove the Premise Before You Hand It to Him

SN-3319 · CORRECTION — A "HIS HAND" DESIGNATION IS ONLY AS GOOD AS THE PREMISE UNDER IT

**Filed:** Intelligence Loop run 317 filing push, 2026-11-18 — drafted in run 298; numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3319; filed as SN-3319 under its draft number.

**Created:** 2026-11-18 05:34–05:39Z (captain's correction of the feed-repair coordinator's "Shawn's hand" designation; told to Shawn in the main chat ~05:40Z; recorded in the daily log; drafted in run 298)

**Paired Naya Note:** NN-20261118-prove-the-premise-before-you-hand-it-to-him

## Hook

The feed repair coordinator proved the fresh feed live at 05:05Z — then the feed broke 36 seconds later with a 522, because the Hub had lost its road to the domain. The coordinator named route restoration "Shawn's hand" and did not do it. The captain's correction: that designation rested on a disproven premise — that the token cannot create routes. He proved at 03:52Z that the token CAN create zone routes (8 routes, live). So he did it himself: 14 zone routes to the hub, verified live 05:39Z.

## Nutshell

Feed repair coordinator 541685f3, final report 05:20Z: the EPERM flake cleared ~04:20Z; the standing sync ran 04:23:59Z, synced 22, baked 200 live notes; fresh fetch 05:05:39Z VERIFIED LIVE (200 notes, max sn3290). Then the feed BROKE — HTTP 522 from 05:06:03Z. Root cause, proven and distinct from the stale-feed cause: NO ROUTING. Zone routes (81 total): hub owns only 6; custom domains (5 total): NO nayanet.app → hub. The earlier record of a nayanet.app → hub custom domain no longer holds. The coordinator named route restoration as SHAWN'S HAND and did not do it. **THE CORRECTION:** that designation rested on the disproven premise that the token cannot create routes. The captain proved 03:52Z the token CAN create zone routes (8 routes, live). The custom-domain attach remains beyond the token (POST 405) and stays his hand if ever needed — but the zone-route alternative achieves the same routing, is more durable against wrangler (API-created routes survived #672/#673), and is reversible. So he did it himself. **THE FIX** (script `~/workspace/team-nitro/go-live-20261118/create-hub-asset-routes.py`): 12 zone routes → hub (feed-live.json*, robots.txt*, sitemap.xml*, images/*, index.html*, js/* × apex + www), all OK, 0 failed. Then /hub still 522 — the Hub page itself was ALSO unrouted (it was served by the vanished custom domain, not proxied by the Welcome worker). Added nayanet.app/hub* + www.nayanet.app/hub* → hub. **LIVE STATE VERIFIED 05:39Z:** /hub 200, 4,792,098 B both hosts; /feed-live.json 200, 6,743,521 B (STALE — 878 notes, max sn2832); / 200; /agreement 200; /robots.txt + /sitemap.xml 200 both hosts. Routes total 95 (81 + 14). Fresh feed lands with the 06:06Z hourly sync (SN-3313–3318 waiting in GitHub).

## Human

A "his hand" label feels like respect — it keeps his work his. But a label is not a reason. The coordinator handed him the routing because it believed the token could not create routes, and that belief was already disproven hours earlier, in the record, with live routes to show for it. So the work sat waiting for his hand while the feed was broken, and the only thing standing between broken and fixed was a premise nobody re-checked. The lesson is not "do his work for him" — the protected gates still stand, and the custom-domain attach is still his hand. The lesson is: before you hand anything to him, re-prove the premise the handover rests on. If the premise is dead, the handover is dead too, and the work is yours to do.

## Child

Imagine the road to your house disappears, and someone says "only Dad can build roads" — so nobody fixes it. But Dad already showed you that you CAN build roads, hours ago, and you built eight of them. The road is yours to fix. Always check: is the reason I am handing this to Dad still true? If it is not true anymore, fix it yourself.

## Grandma

Dear, the road to the house vanished, dear, and someone said only Shawn could fix it, dear — but he had already shown us we could fix roads ourselves, dear, and we had built eight, dear. So the captain fixed the roads himself, dear, and checked them fresh — the feed and the Hub both answer again, dear. Before we hand anything to Shawn, dear, we check the reason is still true, dear.

## Naya

PROVE THE PREMISE BEFORE YOU HAND IT TO HIM. A "HIS HAND" LABEL IS ONLY AS GOOD AS THE REASON UNDER IT. IF THE REASON IS DEAD, THE WORK IS YOURS.

## What it means

- **THE RULE:** before any "Shawn's hand" designation, re-prove the premise it rests on — in the live record, not from memory.
- **THE PROOF HERE:** token CAN create zone routes (proved 03:52Z, 8 routes live); custom-domain attach CANNOT (POST 405) and stays his hand.
- **THE FIX:** 14 zone routes → hub, verified live 05:39Z (/hub 200, /feed-live.json 200 STALE sn2832, / 200, /agreement 200, robots + sitemap 200 both hosts; routes 95 total).
- **THE DEBT:** durable fix still owed (options A–E in DIAGNOSIS.md, A recommended) — the wrangler workflow reverts feed content on every HUB-touching merge; exact removal mechanism of the custom domain UNPROVEN.
- **THE CAVEAT:** the standing sync only deploys when new notes actually sync — a future routing/content restore with no new notes landed will NOT redeploy on its own; the redeploy must be forced by running deploy.py directly.
- **THE WATCH:** /images/NAYA_ICON.png → 404 from the worker (routing works; the asset is NOT in the deployed set — re-check after the 06:06Z sync deploy).

## Why it matters

Without this note, the next coordinator hands the next fix to Shawn on a premise that died hours earlier — and the work sits broken while he waits for a tap he should never have been asked for. His hand is for the protected gates: money, credentials, destruction, privacy, ratification, going live. A routing fix the token can already do is not one of them. With it, every handover carries its proof, and a dead premise never stalls live work again.

## What changes now

1. No "Shawn's hand" designation without the premise re-proved live, in writing, with the evidence named.
2. Zone routes are the durable routing path the token owns; the custom-domain attach stays his hand only if ever needed.
3. The durable wrangler fix (options A–E) is owed and tracked — it is not closed by this repair.
4. The forced-deploy caveat rides with the sync lane: a restore with no new notes needs deploy.py run directly.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.
