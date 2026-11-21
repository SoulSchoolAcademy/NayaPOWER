# NN-20261120-academy-is-live-proven-by-the-fetch

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261120-academy-is-live-proven-by-the-fetch · Naya Note · 2026-11-20 ~18:52 MST**

*Paired Smart Note: SN-4397 — Academy Is Live — Proven by the Fetch*

**Category:** Law — a page is live only when a fresh fetch proves it

**Status:** Filed in run 438. Academy went live on call dfe2008f, recorded in the daily log 2026-11-20.

## What it is

**LIVE:** https://academy.nayanet.app/ — HTTP 200, 97,562 B, sha256 379b174c…, verified by 3 consecutive fresh fetches. Worker `naya-academy` (new, deployment 29fed3f0), custom domain id 87e59a6a…, zone route `academy.nayanet.app/*` also in place (same dual setup as smartfactory). DNS now resolves (104.21.33.87, 172.67.160.181). Portal untouched (1,146,232 B, sha 9ba535c7…).

**QUIRK FOR NEXT TIME:** POST to the workers-domains endpoint 405s ("Method not allowed for this authentication scheme") — PUT is the create method. DNS API is 403 for this token; the custom-domain attach created the DNS record, so no dashboard step was needed.

**STILL OWED:** phone width never proven on this page; MAXESS sections 5–6 still his call (separate page or not).

**REPORT:** ~/workspace/team-nitro/academy-live-20261120/DEPLOY-REPORT.md

## Why it matters

A page claimed live on a deploy receipt alone has burned us before. The fresh fetch is the only proof that a citizen opening the address gets the page.

## How to use it

When a deploy is claimed live, fetch the URL fresh — more than once — and match bytes and sha against the source before the word "live" is written anywhere. Record the working API method when one fails, in the same pass.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
