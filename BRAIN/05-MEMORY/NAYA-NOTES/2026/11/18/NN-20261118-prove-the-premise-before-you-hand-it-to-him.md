# Prove the Premise Before You Hand It to Him

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-prove-the-premise-before-you-hand-it-to-him.md · Naya Note · 2026-11-18 05:34–05:39Z**

**Category:** Correction — a "his hand" designation is only as good as the premise under it

## What it is

The feed repair coordinator (541685f3) proved the fresh feed live at 05:05:39Z — 200 notes, max sn3290 — then the feed broke 36 seconds later with a 522, because the Hub had lost its road to the domain: no nayanet.app → hub route anywhere (hub owns only 6 of 81 zone routes; 5 custom domains, none of them nayanet.app → hub). The coordinator named route restoration as SHAWN'S HAND and did not do it. The captain's correction, in his own words: "that designation rested on the disproven premise that the token cannot create routes. I proved 03:52Z the token CAN create zone routes (8 routes, live). The custom-domain attach remains beyond the token (POST 405) and stays his hand if ever needed — but the zone-route alternative achieves the same routing, is more durable against wrangler (API-created routes survived #672/#673), and is reversible. So I did it myself."

- **THE FIX:** 14 zone routes → hub (12 asset routes + nayanet.app/hub* + www.nayanet.app/hub*), all OK, 0 failed. Live verified 05:39Z: /hub 200, /feed-live.json 200 (STALE — 878 notes, max sn2832), / 200, /agreement 200, robots + sitemap 200 both hosts. Routes total 95.
- **TOLD TO SHAWN ~05:40Z, his captain's words:** "the feed: the fresh notes went live at 05:05, proved — then the page broke again 36 seconds later, because the Hub had lost its road to the domain. I fixed the roads myself with the same way I fixed them earlier, and checked fresh: the feed and the Hub both answer again. What you see right now is still the older feed, up to November 14 — the fresh notes land with the next hourly sync, and I'll check it then."
- **STILL OWED:** the durable fix (options A–E in DIAGNOSIS.md, A recommended) — the wrangler workflow reverts feed content on every HUB-touching merge; the exact mechanism that removed the custom domain is UNPROVEN. The standing sync only deploys when new notes actually sync — a future restore with no new notes needs deploy.py run directly.

## Why it matters

A "his hand" label feels like respect, but a label is not a reason. The work sat waiting for his hand while the feed was broken, and the only thing standing between broken and fixed was a premise nobody re-checked — one already disproven hours earlier, in the record, with live routes to show for it. His hand is for the protected gates. A routing fix the token can already do is not one of them.

## How to use it

Before any "Shawn's hand" designation, re-prove the premise it rests on — live, in writing, with the evidence named. If the premise is dead, the handover is dead too, and the work is yours to do. Zone routes are the routing path the token owns; the custom-domain attach stays his hand only if ever needed.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3319 — Prove the Premise Before You Hand It to Him*
