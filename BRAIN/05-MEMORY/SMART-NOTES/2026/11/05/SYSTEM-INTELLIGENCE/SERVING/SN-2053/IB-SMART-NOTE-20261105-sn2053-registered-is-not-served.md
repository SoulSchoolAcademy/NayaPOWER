# Registered Is Not Served — The Registry Is the Feed
SN-2053 · SYSTEM-INTELLIGENCE / SERVING
**Created:** 2026-11-05T17:50:00Z

## In A Nutshell
A note in the registry is a note in a drawer. Serving is a separate system — a reader, reading a live source, at an address a citizen can open. The cure that ended the gap: the reader reads the registry itself, so registering and serving became one event.

## What Happened
On 2026-11-05 the registry reached completeness — 1,112 Smart Notes, every one with a page and a verified fingerprint — and not one of them could be read by a citizen. Every note address answered "Note not found." Registration had been perfected; serving had never been connected. Three systems each told the truth about themselves — filed, registered, deployed — and the citizen still got nothing.

## The Diagnosis Path (what the probes taught)
- The deploy pipeline was never broken: it deployed successfully every time; only its health check was failing, against a retired domain. A red report card is not a broken machine.
- The requests were reaching the reader all along. The reader was starving: it loaded its feed through a binding that returned nothing, so every lookup missed. Several "someone else's gateway" fingerprints were the reader's own empty hands.
- The instrument that ended the guessing was an echo: a route that reports what the system itself sees (feed loaded? how many? found?) — measure from inside, not from outside.

## The Cure
The reader (the Hub worker) now reads the registry index and each note's capture directly from the registry's public home (GitHub raw), cached per visit. There is no feed file to regenerate and no mirror step to forget. A note serves the moment its registration lands — the same event, not the next one. Proven live the same pass: the 16-note panel, including this note's own predecessors, reading 200 with full content.

## The Law
1. Filed ≠ registered ≠ served. Name the stage you're actually at; a claim at a later stage on an earlier stage's evidence is the failure mode.
2. Every registry needs its reader, built and probed — or the registry is a drawer.
3. The strongest feed is no feed: when the reader reads the source of truth itself, the sync problem disappears.
4. When the outside view and the inside view disagree, build an echo — ask the system what it sees.

*Filed by Naya Resolve Narzan, 2026-11-05, from the serving cure (PRs #3179–#3191). This note itself is the proof: registered and served in one pass.*
