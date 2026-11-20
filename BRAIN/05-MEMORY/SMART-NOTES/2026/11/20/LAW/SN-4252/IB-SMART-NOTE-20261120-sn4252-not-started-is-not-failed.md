# SN-4252 — Not Started Is Not Failed — Name the Probe Limit, Not the Page (LAW)

**Filed:** SN-4252 — Intelligence Loop run 410, 2026-11-20.

## The lesson

A verdict has three states — proven, failed, unproven — and unproven must be recorded as the probe's limit, never upgraded to a page fail and never quietly counted as a pass.

## What happened

Two probe limits landed in the same window, both honestly recorded by their seats. The Personal fix-6 cloud-browser leg could not deliver taps on the live Hub page (~1.2 MB DOM, ~7,500 refs; five attempts failed "not started (deadline)" inside the browser — the taps never started, the URL/title never changed). The live-Hub Ask Naya end-to-end is NOT PROVEN — and the report says so plainly: "NOT a demonstrated site failure." The Hub followup19 eye hit the same shape at 390 in VM Firefox: the scroll-into-view hang — locators resolve to the right elements, but Playwright's actionability wait times out waiting for the element to become visible, so ADD > Make a post, Vera orb → Profile, Vera DM, Vera Mail and the rest could not be closed by pointer at 390. The elements exist and are the right ones; the VM Firefox will not scroll them into view to click. The 390 pointer leg for those taps is owed to a real phone or the cloud browser at phone width — the VM cannot do it at 390.

## The value

"Not started" and "not scrollable" are facts about the probe, not the page. Upgrading them to a page fail dispatches a fix round at a defect nobody saw; counting them as a pass ships a claim nobody proved. The honest third state — unproven, with the limit named — is what lets the next seat re-drive the proof on a working probe instead of fixing a phantom or trusting a gap. The fix-6 cloud leg's "Message" FAIL (real taps, menu simply closes) and PERSONAL yield FAIL (three entry points, none yields the room) are page evidence; the live-Hub end-to-end is not — and the report keeps them in different buckets, which is why the adjudication can be trusted.

## The rule

**When a probe cannot act, record the step as UNPROVEN with the probe's limit named — the tool, the error, and the exact point it stopped — and never as PASS or FAIL.** A tap that never started proves nothing about the page. A locator that resolves but never becomes clickable proves the element exists and the probe cannot reach it. The next seat's job is a re-drive on a probe that can act (cloud browser, real phone, a different width), not a fix for a defect the probe never saw. A verdict that cannot say which of its items were unproven is not a verdict — it is a guess with screenshots.

## His words

None — this is a machine verdict, not Shawn's dictation. The records are the fix-6 cloud-browser leg report (11:49Z) and the followup19 eye report (EYE-REPORT.md, 11:55:25Z).

## Paired Naya Note

None — no new Shawn dictation this run.
