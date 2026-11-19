# SN-3704 — The City Saves; the Forecast Waits

**Filed:** Intelligence Loop run 368, 2026-11-19 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3704; filed as SN-3704 under its draft number.

**Filed by:** Intelligence Loop run 368, 2026-11-19 — Shawn's question and the straight answer, voice call ~08:22–08:23 MST (15:22–15:23Z 2026-11-19).

**Paired Naya Note:** NN-20261119-city-saves-forecast-waits

## The teaching, in his words (verbatim)

His question (08:22:58 MST): "if I enter my city will it actually work? Or no?" The answer given on the call: the entry works, the forecast doesn't yet — wiring a live forecast is a separate build (needs a weather provider — his call).

## The understanding

Two halves, both true, and the page tells both honestly. The entry WORKS — it saves the city (verified from the fix-7 eye report, line 84, and the checker report, lines 175–176). But NO live forecast appears, because no weather service is connected — and the page says so honestly ("London · Weather is not connected yet — no forecast to invent.") instead of inventing one. His own city is Kelowna, entered by him on the day page ~08:25 MST. The distinction is the lesson: a feature that saves is done; a feature that has no data behind it must say so, never fake it. The forecast is not a bug to quietly patch — it is a provider decision, and it is his call.

## The law

Never invent data. When the system cannot do a thing yet, the page says so in plain words — "not connected yet" — and the missing piece is named as its own build, decided by him. Saving the city and showing a forecast are two different features; the first is done, the second waits for a weather provider.

## Owed from this dictation

Nothing to fix on the entry — it works. The live forecast rides a separate build only on his provider decision. No round invents forecast data in the meantime.

**It saves. It says what it can't do. It never invents.**
