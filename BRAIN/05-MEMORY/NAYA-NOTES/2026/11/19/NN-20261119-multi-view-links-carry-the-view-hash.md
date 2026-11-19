# NN-20261119-multi-view-links-carry-the-view-hash

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261119-multi-view-links-carry-the-view-hash · Naya Note · 2026-11-19 ~10:36 MST (17:36Z 2026-11-19)**

*Paired Smart Note: SN-3751 — Multi-View Links Carry the View Hash*

**Category:** System — Links, staging

## What it is

He opened the staged membership link — "This is not membership" — and he was right: it landed on Personal home. The memberships view lives inside that file (id=memberships, VIEWS list); the corrected link carries #memberships, which the boot code opens directly. Re-verified 200, 2,521,228 B. The lesson recorded: multi-view staged links must carry the view hash.

## Why it matters

A staged file holds many views, and a bare link opens the default one — so the link that says "membership" opens Personal home, and the citizen has to find the view themselves. The hash is the address of the view: #memberships tells the boot code exactly where to land. A link without its hash is an address without the apartment number — it gets to the building and stops. Every staged link to a view inside a multi-view file carries its hash, or it is the wrong link.

## How to use it

Every staged link to a view inside a multi-view file carries the view hash (#memberships, and the same for every other view). The link is verified by opening it: it must land on the view it names, not on the file's default. The membership link is the proof — corrected, re-verified 200, landing on memberships.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
