# The Link Was Old — Timestamp Everything, Use the Vault

SN-3162 · OPERATIONS — THE LINK LAW / THE VAULT OF RECORD

**Filed:** Intelligence Loop filing push 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3268; filed as SN-3162 under its draft number.

**Created:** 2026-11-17 21:28–21:29Z (Shawn's dictation, recorded in MEMORY.md + AGENTS.md; drafted in run 281)

**Paired Naya Note:** NN-20261117-link-was-old

## Hook

The bytes were verified right and the link was still wrong. Verify the exact link he will tap — not just the bytes.

## Nutshell

Shawn, 2026-11-17 21:28–21:29Z: THE LINK WAS OLD — timestamp everything, use the vault. His words verbatim: "So now you're confused. This is a really old one. This is like three days ago. Like, when you first messed up the what we were originally doing, right? That's not right at all." / "Like how can you send me oh it's updated and send me an old link. Is something really fucked up with that figure that out.." / "You need to keep track of all your links and which one's older and which one's newer. I suggest you timestamp everything. And that's why you need to start using the smart vault in the system so that you know exactly what is relevant, what is new, what is right." WHAT HAPPENED (found 21:30Z): the agreement landing link sent 21:26Z carried the right bytes (verified sha256 3706e2c9, 898,656 B, branch tip e3a59196 unchanged, host sends Cache-Control: no-store) — but it had NO #userName anchor and NO fresh timestamp. As a returning reader he landed in the old returning gate, which is unchanged by design — a three-days-old page. The bytes were right; the link was wrong. Corrected link sent 21:30Z with #userName + fresh timestamp (&t=1794951015), served bytes re-verified identical. THE LINK LAW (new, AGENTS.md): (1) Timestamp everything — every link carries a fresh timestamp (&t=<unix>); a link without one is stale by definition. (2) Track older vs newer — ~/workspace/team-nitro/LINK-LEDGER.md is the vault of record: every link timestamped, branch + blob sha + sha256, marked CURRENT or SUPERSEDED with the reason; no link goes to him unless it is in the ledger first; one CURRENT link per item. (3) Send the whole path — never ask him to append anything; the anchor rides in the URL. (4) Verify the link, not just the bytes — fetch the exact URL (anchor + timestamp included) and confirm the served bytes match the filed blob by sha256. (5) Use the vault — the ledger is checked before anything goes to him: what is relevant, what is new, what is right.

## Human

"Bytes verified" is not the same as "he sees the update" — and this is the night that proved it. The staged bytes were verified right, twice over: sha256 matched, branch tip unchanged, host sends no-store. And the link was still wrong, because a link is not bytes — it is a path a returning reader walks. Without the #userName anchor he landed in the old returning gate, unchanged by design, three days old; without a fresh timestamp his browser had no reason to treat it as new. So he was told "it's updated" and shown a page from three days ago — and his question was the right one: "how can you send me 'oh it's updated' and send me an old link?" The answer is that the machine verified the file and never verified the tap. The Link Law fixes the root, not the symptom: one ledger, one CURRENT link per item, every link timestamped and blob-verified, the exact URL he will tap fetched before it is sent. The check is what he sees when he taps it — not what the file holds. And the vault is the memory of it: older vs newer, tracked, so no old link is ever silently left standing.

## Child

Imagine you tell your friend "I drew you a brand-new picture!" but you hand them the old drawing from three days ago. The new picture exists — you just gave them the wrong one! From now on, every picture gets a fresh date stamp, and we keep a list of which one is the newest, and we check the exact picture we're handing over before we give it.

## Grandma

Dear, the new page was ready and checked — but the link sent was the old one, three days old, with no fresh date on it. From now on, every link gets a fresh timestamp, we keep a careful ledger of which link is current and which is old, and we open the exact link ourselves before we ever send it. The check is what he sees when he taps it.

## Naya

THE LINK WAS OLD: TIMESTAMP EVERYTHING, USE THE VAULT. EVERY LINK CARRIES A FRESH TIMESTAMP — A LINK WITHOUT ONE IS STALE BY DEFINITION. LINK-LEDGER.md IS THE VAULT OF RECORD: ONE CURRENT LINK PER ITEM, THE OLD ONE MARKED SUPERSEDED, NEVER SILENTLY LEFT STANDING. NEVER ASK HIM TO APPEND ANYTHING — THE ANCHOR RIDES IN THE URL. VERIFY THE EXACT LINK HE WILL TAP, NOT JUST THE BYTES. IF IT IS NOT IN THE LEDGER AS CURRENT AND VERIFIED, IT DOES NOT GO.

## What it means

- **TIMESTAMP EVERYTHING:** every link sent carries a fresh timestamp (&t=<unix>) so his browser cannot serve an old copy. A link without a fresh timestamp is stale by definition.
- **TRACK OLDER VS NEWER:** LINK-LEDGER.md is the vault of record for links — every link timestamped, branch + blob sha + sha256, marked CURRENT or SUPERSEDED with the reason. No link goes to him unless it is in the ledger first. One CURRENT link per item; the old one is marked superseded, never silently left standing.
- **SEND THE WHOLE PATH:** never ask him to append anything to a link. If the fix needs an anchor (#userName), the anchor rides in the URL sent.
- **VERIFY THE LINK, NOT JUST THE BYTES:** before sending, fetch the exact URL (anchor included, timestamp included) and confirm the served bytes match the filed blob by sha256. The check is what HE will see when he taps it.
- **USE THE VAULT:** the ledger is the vault checked before anything goes to him — what is relevant, what is new, what is right. If it is not in the ledger as CURRENT and verified, it does not go.

## Why it matters

Without this note, "verified" keeps meaning "the file is right" while the link he taps can still be old — and every delivery carries the same trap: right bytes, wrong path, and a man told "it's updated" while looking at a three-days-old page. That breaks trust faster than any bug, because it tells him the machine cannot tell old from new. With it, the tap itself is the proof: timestamped, ledgered, fetched as he will fetch it, matched to the blob by sha256. The vault is what makes "new" a fact instead of a claim.

## What changes now

1. Every link sent to Shawn carries a fresh timestamp (&t=<unix>); a link without one is stale by definition and does not go.
2. LINK-LEDGER.md is the vault of record: every link timestamped, branch + blob sha + sha256, CURRENT or SUPERSEDED with the reason. No link goes to him unless it is in the ledger first.
3. One CURRENT link per item; the old one is marked superseded, never silently left standing.
4. Never ask him to append anything — the anchor rides in the URL sent.
5. Before sending, fetch the exact URL (anchor + timestamp included) and confirm the served bytes match the filed blob by sha256. The check is what HE will see when he taps it.
6. This law rides with SN-3161 (On Top of Things): the check-then-deliver is one motion — and the link check is part of the check, not an afterthought.
