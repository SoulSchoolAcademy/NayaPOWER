# SN-3486 — The Mail Fix Is Done: The Key Moved Server-Side, and the Digests Flow Again

**Filed:** Intelligence Loop run 332, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3486; filed as SN-3486 under its draft number.

**Filed by:** Intelligence Loop run 332, 2026-11-18 — mail fix executed + verified working ~21:55Z, on Shawn's go ~21:51Z.

**Paired Naya Note:** NN-20261118-mail-fix-executed

## The teaching, in his words (verbatim)

Shawn's go ~21:51Z closed the open decision ("Mail fix: 'Just say go' — package filed 19:45Z"). The fix, one file only — `~/workspace/project-intelligence/send-mail-helper.py`: the old-key scrape out of flagship-template.html is gone; `get_service_key()` added, copying the welcome scheduler's pattern (Supabase Management API, memory only, never printed or written). Verified working: service key returns (len 219); reads with the service key return rows (5/5 sample both mail tables); test send via the fixed helper to diag-test landed (thread c506628e…, message 8a7e63e5…), no 42501, read back and deleted; held digest run198 sent to both team aliases (naya-power + resolve), exit 0.

## The understanding

The team's mail tools had lost access in the same window the privacy fix landed, and the fix was waiting on his hand — a key that could not be read from a page had to move server-side instead. The one-file fix does exactly that and nothing more: no page code carries the server key, ever. The proof is end to end, not a claim: key returns, reads return rows, a real test send landed and was read back and deleted, and the held digest actually went out to both team aliases. But the fix's boundary is part of the lesson: the browser pages (Personal composer, Message-this-app, instant message) are still blocked — they need his pick, a privacy-rule change OR an Edge Function — and the sb-api reads of mail tables still return [] (old key, by design).

## The law

The server-side key never goes in page code. A mail fix is proven by a send that lands and reads back — never by a key returning alone.

## Owed from this dictation

**run199/run200 must NOT be run blindly** — run199 resends run198, run200 resends run199; the loop owner must mark them sent/superseded or the same digest goes out twice. Browser-page mail still needs his pick (privacy-rule change OR Edge Function). Full record: `~/workspace/team-nitro/mail-fix-20261118/MAIL-FIX-EXECUTED.md`.

**The key moved server-side. The digests flow again — and the pages still wait for his pick.**
