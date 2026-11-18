# The Link Was Old — Timestamp Everything, Use the Vault

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261117-link-was-old.md · Naya Note · 2026-11-17 21:28–21:29Z**

**Category:** Operations — The Link Law / the vault of record

## What it is

Shawn, 2026-11-17 21:28–21:29Z: THE LINK WAS OLD — timestamp everything, use the vault. His words, as recorded:

"So now you're confused. This is a really old one. This is like three days ago. Like, when you first messed up the what we were originally doing, right? That's not right at all."

"Like how can you send me oh it's updated and send me an old link. Is something really fucked up with that figure that out.."

"You need to keep track of all your links and which one's older and which one's newer. I suggest you timestamp everything. And that's why you need to start using the smart vault in the system so that you know exactly what is relevant, what is new, what is right."

WHAT HAPPENED (found 21:30Z): the agreement landing link sent 21:26Z carried the right bytes (verified sha256 3706e2c9, 898,656 B, branch tip e3a59196 unchanged, host sends Cache-Control: no-store) — but it had NO #userName anchor and NO fresh timestamp. As a returning reader he landed in the old returning gate, which is unchanged by design — a three-days-old page. The bytes were right; the link was wrong. Corrected link sent 21:30Z with #userName + fresh timestamp (&t=1794951015), served bytes re-verified identical.

THE LINK LAW (new, AGENTS.md): (1) Timestamp everything — every link carries a fresh timestamp (&t=<unix>) so his browser cannot serve an old copy; a link without a fresh timestamp is stale by definition. (2) Track older vs newer — ~/workspace/team-nitro/LINK-LEDGER.md is the vault of record for links: every link timestamped, branch + blob sha + sha256, marked CURRENT or SUPERSEDED with the reason; no link goes to him unless it is in the ledger first; one CURRENT link per item; the old one is marked superseded, never silently left standing. (3) Send the whole path — never ask him to append anything to a link; if the fix needs an anchor (#userName), the anchor rides in the URL sent. (4) Verify the link, not just the bytes — before sending, fetch the exact URL (anchor included, timestamp included) and confirm the served bytes match the filed blob by sha256; the check is what HE will see when he taps it. (5) Use the vault — the ledger is the vault checked before anything goes to him: what is relevant, what is new, what is right; if it is not in the ledger as CURRENT and verified, it does not go.

## Why it matters

"Bytes verified" is not the same as "he sees the update." The bytes were verified right and the link was still wrong — no anchor, no fresh timestamp — so as a returning reader he landed in a three-days-old page and was told it was updated. That is worse than a wrong page: it tells him the machine cannot tell old from new. The vault fixes the root: one ledger, one CURRENT link per item, every link timestamped and blob-verified, the exact URL he will tap fetched before it is sent. The check is what he sees when he taps it — not what the file holds.

## How to use it

Before any link goes to Shawn: put it in LINK-LEDGER.md first — timestamped, branch + blob sha + sha256, marked CURRENT, the old one marked SUPERSEDED with the reason. Never send a link without a fresh timestamp. Never ask him to append an anchor — the anchor rides in the URL. Fetch the exact URL (anchor + timestamp included) and confirm the served bytes match the filed blob by sha256. If it is not in the ledger as CURRENT and verified, it does not go.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3162 — The Link Was Old — Timestamp Everything, Use the Vault*
