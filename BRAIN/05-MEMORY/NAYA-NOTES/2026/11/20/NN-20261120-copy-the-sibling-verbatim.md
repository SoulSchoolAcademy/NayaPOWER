# NN-20261120-copy-the-sibling-verbatim

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261120-copy-the-sibling-verbatim · Naya Note · 2026-11-20 ~17:05 MST**

*Paired Smart Note: SN-pending — Copy the Sibling Verbatim (takes the next free number at filing)*

**Category:** Law — fix the odd one out by copying what already works

**Status:** Filed in run 435. His words on call f3737da1, recorded in MEMORY.md.

## What it is

**THE PORTAL BUTTON (~17:05 MST).** "when you click that you click that link it doesn't go there right now it goes somewhere else... when they click the collective agreement button at the bottom of that page it actually goes to the collective agreement page. Because right now it goes to the old one, right?"

**THE FIX, AS IT LANDED (~17:16 MST).** The bottom button is the footer's `Read the collective agreement ◆` on the live portal. Its handler opened the walk's in-page agreement stage — the old presentation — and never left the page. That was "the old one." The other three agreement buttons in the same file already went to `/agreement`; this one was the odd one out. The fix was exactly one line: the handler became `window.location.href='/agreement';`, copied verbatim from the other three buttons. Nothing else changed — same label, same style, same position. Live deploy: worker `nayanet` v76 → v77, fresh-fetch verified (1,146,232 B, sha `9ba535c71342…`).

**THE FLAG THAT RIDES WITH IT.** Main's copy of the portal file is a different version (the merged union file) — a future merge of it over the live path could revert the fix. Carry-into-main was dispatched branch-only, no merge.

## Why it matters

The fix was already sitting in the same file, three times over. Copying the sibling is faster than inventing, and it cannot drift from the house pattern — the sibling IS the pattern. The odd one out is the defect; the siblings are the proof of what right looks like.

## How to use it

When one button in a family goes somewhere the others do not, do not redesign the button. Find the sibling that already goes to the right place, copy its destination verbatim, change nothing else — and then check the other copy of the file, because the fix has to live in both places or the next merge undoes it.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
