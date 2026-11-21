# SN-4397 — Academy Is Live — Proven by the Fetch

**Category:** LAW — a page is live only when a fresh fetch proves it; 2026-11-20 ~18:52 MST

*Paired Naya Note: NN-20261120-academy-is-live-proven-by-the-fetch — the verbatim record of the live proof.*

**Filed:** SN-4397 — Intelligence Loop run 438, 2026-11-20. Academy went live on call dfe2008f, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Academy is live at academy.nayanet.app — and live means three fresh fetches returned the exact bytes and sha, not that the deploy finished.

## The Lesson

Academy went live at https://academy.nayanet.app/ — HTTP 200, 97,562 B, sha256 379b174c…, verified by 3 consecutive fresh fetches. Worker `naya-academy` (new, deployment 29fed3f0), custom domain id 87e59a6a…, zone route `academy.nayanet.app/*` in place (same dual setup as smartfactory). DNS now resolves (104.21.33.87, 172.67.160.181). Portal untouched (1,146,232 B, sha 9ba535c7…). The address was settled an hour earlier when Shawn spelled it letter by letter — A-C-A-D-E-M-Y dot N-A-Y-A-N-E-T dot A-P-P — and the deploy coordinator proved it live the same way every deploy must: fetch the URL fresh and match bytes and sha against the source. A deploy completing is not a page being live; a fresh fetch matching is. Two quirks are recorded so the next deploy does not repeat them: POST to the workers-domains endpoint 405s ("Method not allowed for this authentication scheme") — PUT is the create method; and the DNS API 403s on this token, but the custom-domain attach created the DNS record, so no dashboard step was needed.

## Why It Matters

A page claimed live on a deploy receipt alone has burned us before — staged links serving old versions, workers with their workers.dev route disabled, DNS not yet resolving. The fresh fetch is the only proof that a citizen opening the address gets the page. Recording the PUT-not-POST quirk in the same pass means the next seat does not lose a round to a 405 it could have known about.

## How to Use It

When a deploy is claimed live, fetch the URL fresh — more than once — and match bytes and sha against the source before the word "live" is written anywhere. When an API call fails with a method or permission error and another method works, write the working method down in the same pass; the quirk is part of the deploy, not a footnote to lose.

## His Order, As Recorded

> "Academy LIVE at academy.nayanet.app (his order, spelled out on the call)."

## Owed from This Dictation

- Phone width never proven on the Academy page.
- MAXESS sections 5–6 still his call (separate page or not).
- Report: ~/workspace/team-nitro/academy-live-20261120/DEPLOY-REPORT.md
