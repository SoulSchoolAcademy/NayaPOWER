# PI Board Note — Chart Entrance + Cell Layout (Intelligence Loop 17:23Z)

**Filed:** 2026-11-08 17:23Z run (seat: Naya Nitro Sigma, LEARN lane)
**State:** FILED — the current state of the pricing chart viewpoint, for the Living List / the board.

## What Shawn decided since the last loop run (16:53Z)

1. **17:12Z — The Three Defects (SN-2314):** wrap bug ("100/M" → "1 0" / "0 /M"), no sticky tier header, values repeat. His shape: small number, then 100K, then unlimited. Fix dispatched (716d57e1).
2. **17:15Z — The PI Row Is Wrong (SN-2315):** PI is your projects, not the daily report. Counts are his word, never invented — the row stands BLANK awaiting his numbers. Readability rule: value first, big and clear, one line; explanation small underneath.
3. **17:20Z — The Chart Fix Done (SN-2316):** sticky header + wrap killed structurally + ladders + PI placeholder row. Presented; his eye decides. Durable pricing-chart-rows.json NOT updated until he confirms.
4. **17:21Z — The Entrance Doesn't Speak Naya (SN-2313):** gold orb out; her real portrait + N logo + welcome + NayaNET branding; explain/sell lines cut; tier names branded (Free, Naya Power, Naya Pro, Naya Max); prices out of intro cards; each tier its own escalating elite icon. NEW files: NAYA_POWER.jpg (486,536B, md5 e363a97d) and icon-512.png (252,607B, md5 c66a09fe) — copy THOSE bytes, never generate. Rebuild running (9ce9f988).
5. **17:23Z — Cell Layout: Stacked, Centered (SN-2317):** number centered at top → what it is underneath → check underneath. Fallback: checks top-right, number + label centered. Follow-up sent to 9ce9f988 (12fa85b6).
6. **17:26Z — "/M" Doesn't Read + Not the Real Numbers (SN-2318):** no "/M" anywhere — number on its own line, "a month" underneath, small. Chart tiles are a recreation: take the Dashboard's tiled-digit code from fix-9 byte for byte (flip-tiles, colored tops, rim colors per digit, rotation), report source lines + diff, never invent colors. Follow-up sent to 9ce9f988 (f043b842).

## Smart notes filed this run

SN-2313 · SN-2314 · SN-2315 · SN-2316 · SN-2317 · SN-2318 — all in BRAIN/05-MEMORY/SMART-NOTES/2026/11/08/{DESIGN,LAW}/SN-23xx/, read-back verified. Next free SN: **2319**.

## Open questions for his eye (unchanged + new)

- PI project counts per tier — his numbers, still open (asked 17:15Z).
- Ladder mapping 100K covering Power + Pro — the captain's reading, his eye confirms or corrects.
- No separate row for the daily intelligence report — flag, in case he wants one.
- Entrance rebuild + cell layout + real numbers — running (9ce9f988), presented when it lands.

## Out of alignment (carried, no new silent drift)

- Live Dashboard % mismatch + bottom-bar cover · pricing phone-fit defect · PI face still October build · Hub fix pass 2 verified, not deployed · Personal About 390px off-screen · Smart Notes / Smart Lists ladders unsettled (his word needed) · 7 canonical libraries — FOUND by the Factory-harvest seat (concept-1 done, 17:2xZ) · Smart Notes sync STALLED — heartbeat ~60+ min old, watermark 09071f05, main at b072702c, state/heartbeat writes failing EPERM (surfaced to Shawn ~17:07Z; Hub re-bake pending the write block clearing) · PI refresh 17:10Z cycle failed EPERM (last good publish 16:10Z, new_hash 6a1af159…) · transcribe-watcher 17:15Z failed EPERM · EPERM write flake STILL ACTIVE (probe 17:24Z left a 0-byte file; file-tool writes work, exec writes fail).

## Correction compound status

Every correction this run became note + mail + PI (this note) + GitHub in the same pass. Factory-inventory and brief-template updates remain owned by the LOCK-IN-10 coordinator (e6626328, still running) — the loop does not duplicate that seat's work.
