# Hub Sync Live-Fire Test

**ID:** IB-SMART-NOTE-20261021-sn9999-hub-sync-live-fire-test
**Created:** 2026-10-21
**Category:** SYSTEM / Hub Sync Test

## IN A NUTSHELL

This is a test note. It exists to measure how fast a note landed on main becomes a card in the Hub. It is removed right after the measurement.

## HUMAN

A stopwatch test for the new standing sync: land a note, count the seconds until the Hub card appears.

## CHILD

We dropped a note in the box and timed how fast it showed up on the board.

## GRANDMA

Just a timing test, dear — nothing in here you need to remember.

## NAYA

Live-fire verification of hub-sync (the standing watcher): push-to-card latency must be seconds, not minutes or hours. Cleanup follows immediately after the measurement.

## MACHINE

```json
{"test": "hub-sync-live-fire", "expect": "card minted within seconds of landing on main", "cleanup": "file and row removed after measurement"}
```

## WHAT IT ALL MEANS

If this card appears within seconds, the flow Shawn ordered — smart note this, and it's in the Hub — works for any hand that lands a note.

## WHAT'S IN IT FOR YOU

Proof, not promises: the sync works at the speed the system promises.

## HOW IT APPLIES

Measure, then remove this file and its card. The standing watcher stays.
