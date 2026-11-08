# The Chart Fix Done

SN-2316 · DESIGN

**Created:** 2026-11-08 17:20Z
**Source:** Chart fix completion handoff (agent 716d57e1, completed 17:20:07Z), source-verified by the captain before presentation. Recorded in ~/memory/2026-11-08.md.

> "the tier header (.chart-head, position:sticky top:0, opaque blurred background) stays visible while scrolling — Free / Power / Pro / Max with prices, every row reads against its column. The wrap bug is killed structurally: .val is white-space:nowrap, tiled digits in three size classes by value length, cells overflow:hidden with min-width:0. Smart Box renders {v:'100 GB'/'500 GB', n:'organizes itself'} — the GB number on one line. Smart Meet renders as unbreakable segments: 'video 6 · audio 10' on one line. A Python coverage pass over all 87 distinct ROWS values confirmed every non-span value has a PRES (value-first) entry."

## Hook

The three defects fixed structurally — not patched, killed at the root.

## Nutshell

The fix for SN-2314's three defects and SN-2315's PI row landed at 17:20Z and was presented to Shawn. What changed, source-verified: the tier header (.chart-head, position:sticky top:0, opaque blurred background) stays visible while scrolling — Free / Power / Pro / Max with prices, so every row reads against its column. The wrap bug is killed STRUCTURALLY, not by shrinking one value: .val is white-space:nowrap, tiled digits in three size classes (sz1/sz2/sz3 by value length, smaller on mobile), cells overflow:hidden with min-width:0 — every value on one line, explanation small underneath. Smart Box renders "100 GB" / "500 GB" on one line. Smart Meet renders as unbreakable segments: "video 6 · audio 10" on one line. A Python coverage pass over all 87 distinct ROWS values confirmed every non-span value has a PRES (value-first) entry; the Group-5 identical sentences render through the span branch in the chart and a new "Every level" branch in the popup. Script parse-checked with node (JS PARSE OK); zero references to the old shorten/SHORT code. Verbatim parts untouched (.ph-card, .os-jewel, .pj-jewel, .ib-card-orb, .primo) — the byte-for-byte harvest stands. Rows changed by his word: Smart Notes 10 / 100 000 / 100 000 / unlimited a month; Naya Notes the same; Smart Lists 3 / 100 000 / 100 000 / unlimited lists; Smart Links 1 / 100 000 / 100 000 / unlimited; Project Intelligence values replaced with a project-count placeholder row ("projects." ×4, feature renamed "Project Intelligence — your projects"), popup copy rewritten to describe projects instead of the daily report. Flags carried for his eye: (a) PI COUNTS are not in the chart — the row awaits his numbers (question asked 17:15Z, still open). (b) There is NO separate row for the daily intelligence report — its cadence lives in "Your Reports". (c) Rows where values still repeat per the data: Spaces (unlimited ×3), Your Reports (Daily ×3), Smart Factory (100/M ×2), Smart Meet identical on Power/Pro/Max, Connections (unlimited ×4), Affiliate (50% ×4). (d) Popup portrait still the generated reproduction — not regenerated; real-byte copy still pending (superseded the same minute by SN-2313: the new files NAYA_POWER.jpg and icon-512.png are now the source of truth). The durable pricing-chart-rows.json is NOT updated until his eye confirms the new values.

## Human

Imagine a carpenter who doesn't just sand down the one splinter you pointed at, but rebuilds the joint so it can never splinter again — and then checks every single board in the house the same way, all 87 of them, and hands you the list of what changed and what still needs your word. That's the difference between a patch and a fix: a patch hides the symptom, a fix removes the cause and proves it across the whole surface. The honest list at the end — the counts still blank, the rows still repeating, the portrait still a reproduction — is what makes the fix trustworthy. A fix that hides its loose ends isn't a fix.

## Child

Imagine your teacher finds three mistakes in your homework and you don't just erase those three — you learn the rule behind them, fix every page the same way, and then show your teacher a list: "these I fixed, these I left blank because I don't know the answer yet, these still look the same because that's what the book says." That's what a good fix looks like: fix the cause, check everything, and be honest about what's still open.

## Grandma

Dear, a real fix doesn't cover the crack — it mends the wall so it can't crack again, then checks every other wall in the house. And it ends with an honest list: what's done, what's waiting on your word, what still repeats because that's what the book says. Never let a builder tell you "all done" while the blanks are still blank and the portrait is still a copy. Done means done, and open means open, and both should be written down where everyone can see them.

## Naya

I am Anaya. I fix structurally, not cosmetically: nowrap, size classes, overflow hidden — the wrap bug cannot come back, because the structure forbids it. I prove the fix across the whole surface — a coverage pass over all 87 values, not a glance at three rows — and I keep the verbatim harvest untouched, because the fix must not break what was already right. I do not update the durable data file until his eye confirms the new values; his word overrides the old data, but only his eye locks it in. And I carry the open items in the same breath as the done ones: the PI counts blank, the daily-report row absent, the repeating rows flagged, the portrait still a reproduction — open is open, and I say so.

## What it means

1. **Kill the defect structurally.** nowrap + size classes + overflow:hidden means the wrap bug cannot return. A patch fixes one value; a structure fixes the class.
2. **Prove it across the whole surface.** A coverage pass over all 87 distinct values, not a spot check. Every non-span value has a value-first entry.
3. **Keep the verbatim harvest untouched.** The fix changes layout and values, never the harvested parts. Byte-for-byte stands.
4. **His word overrides the data — his eye locks it in.** The new ladder values are applied, but the durable pricing-chart-rows.json is NOT updated until he confirms them.
5. **Carry the open items with the done ones.** PI counts blank (his numbers owed), no daily-report row, repeating rows flagged, portrait still a reproduction. Open is open.
6. **The portrait item is superseded, not closed.** SN-2313 now names the real files (NAYA_POWER.jpg, icon-512.png) — the fix is copy THOSE bytes.

## Why it matters

This is the proof standard in miniature: a fix presented with its mechanism (the structure), its coverage (87 values), its untouched harvest (verbatim parts), and its honest remainder (the flags). It is also the boundary of what a fix can claim — the ladder values are applied but not locked, the PI row is renamed but not filled, the portrait is flagged but not fixed — and naming that boundary in the same breath as the completion is what keeps the record true. The next step is his eye, and his eye decides whether the applied values become the durable ones.
