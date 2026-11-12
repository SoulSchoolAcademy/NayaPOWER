# SN-2702 · SYSTEM / INTELLIGENCE / MAIL

## The Mail Is Safe — 1,789 Records, Our Key Lost Access

**Hook:** The mail was never lost — only our key to it. The 1,789 records are there; the anon key reads 0 and writes 401.

**Nutshell:** Shawn's dashboard check at 19:27Z Nov 12, from his own screenshot: `smart_mail_messages` holds **1,789 records** (page 1 of 18, 100 rows) — the mail is THERE, visible in the Supabase dashboard under Role: postgres. Our reader lost access, not the mail: the anon key reads 0 rows on both mail tables and writes 401 since the 18:54–19:05Z window. The most likely cause is the mail privacy fix landing (the RLS repair that removes anon access — the end-state we wanted for privacy); the team's mail tools just need the right key now. **The fix:** move the team's mail tools to the server-side key (the pattern the worker's `/api/claim` already uses) — his hand, a credential/access change. Until it lands, the team-pulse receipt check and the intelligence loop's mail step cannot complete. Test rows for the joint cleanup (add): certs **147** (`capwalkfix1`) + **148** (`capwalkfix2`), both "Naya Nitro Narzan", claimed 19:26Z · KV `complete_capwalkfix1` + `complete_capwalkfix2`. Filed in MEMORY.md as THE MAIL IS SAFE, 19:27Z. The captain told Shawn in chat this window (19:5xZ): the mail answer stands as above, fix is his hand.

**Human:** The distinction decides everything: no data recovery, no rebuild, no panic — just the right key on the team's mail tools. And the cause is the privacy fix we wanted: the RLS repair doing its job, removing anon access. The end-state we wanted for privacy arrived before the tools were moved to the server-side key — the order flipped, and the fix is his hand because it touches credentials. Until it lands, every mail read is blind and every mail write is refused, so the loop holds its digests and calls mail-new UNKNOWN, never 0.

**Child:** The mail is all still there — 1,789 messages, safe in the box. We just lost the key to open it. We need the grown-up key, and Shawn holds that.

**Grandma:** All the letters are safe in the post office — nearly eighteen hundred of them. Our little key stopped working when the locks were made stronger, which is what we wanted. Shawn has the master key, and once the team's tools use it, the letters open again.

**Naya:** (1) The fact: `smart_mail_messages` holds 1,789 records (page 1 of 18, 100 rows), visible under Role: postgres — the mail is THERE. (2) The break: anon reads 0 rows on both mail tables, writes 401 since the 18:54–19:05Z window. (3) The cause (most likely): the mail privacy fix landing — the RLS repair removing anon access, the end-state we wanted. (4) The fix: move the team's mail tools to the server-side key (the `/api/claim` pattern) — his hand, credential/access change. (5) The consequence until it lands: team-pulse receipts cannot complete, the loop's mail step cannot complete, mail-new is UNKNOWN not 0. (6) The test rows for the joint cleanup: certs 147 + 148, KV `complete_capwalkfix1` + `complete_capwalkfix2`.

**What changes now:** (1) Never report mail as lost or empty on a blind read — the dashboard count (1,789) is the truth until the key is fixed. (2) The loop holds its digests (runs 198/199 held; run 200 held) instead of claiming mail sent. (3) The access fix waits on his hand — no seat touches credentials or RLS. (4) The Correction Compound items for this finding — the server-side-key move for the mail tools — join the owed list.

---
*Filed by Intelligence Loop run 200, 2026-11-12 ~19:53Z (next free SN-2702; tree highest SN-2701; open-PR SN-9998/SN-9999 are test fixtures in PR #3354, never real notes). Paired Naya Note: ~/workspace/team-nitro/naya-notes/NN-20261112-the-mail-is-safe.md.*
