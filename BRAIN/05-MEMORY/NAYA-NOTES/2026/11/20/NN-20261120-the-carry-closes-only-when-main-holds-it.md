# NN-20261120-the-carry-closes-only-when-main-holds-it

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261120-the-carry-closes-only-when-main-holds-it · Naya Note · 2026-11-20 ~17:43 MST**

*Paired Smart Note: SN-4379 — The Carry Closes Only When Main Holds It*

**Category:** Law — how a fix becomes permanent

**Status:** Filed in run 436. The merge landing recorded in the daily log 2026-11-20; it closes the carry item run 434 opened and run 435 left owed.

## What it is

**THE RECORD.** The portal button fix went live first (worker v76 → v77, ~17:16 MST) — but main's union file still held the old handler, so a future merge could have brought the old button back. The carry closed that gap: one line, verbatim, onto branch `portal/agreement-button-carry-main-20261120` (commit `626859ee`, parent main HEAD `e64c2dec`), the seven questions all answered YES in writing, the captain's independent double-check passed, and the merge landed (commit `f5fde7c0`, now main HEAD, 00:44:17Z). The button fix is in main for good.

**WHAT IT MEANS.** A live-only fix is not a fix — it is a fix waiting to be reverted. Done means main holds the same bytes as live. The carry is the second half of every live fix, and it is not done until the merge is verified by fresh read-back.

**WHERE IT APPLIES.** Every live fix, every worker deploy, every file that exists in two versions. If live and main disagree, the carry is owed the moment the live fix lands — never left for later.

## Why it matters

Without the carry, the next merge of main's union file would have silently restored the old button, and nobody would have known until he tapped it. The smallest carry — one line, ten bytes — is what makes a live fix permanent.

## How to use it

Carry the fix into main the same way every time: the smallest verbatim change, diff scope proven line by line (here line 3916 only, −10 B, old handler 0×, new handler 1×, `/agreement` 5×), the seven questions answered in writing, the captain's double-check, the merge verified by fresh read-back after. Never force-update main's ref. Never call the carry done before the merge lands.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
