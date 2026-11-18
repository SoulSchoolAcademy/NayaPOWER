# A Firefox Empty List Is a Probe Failure

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261116-a-firefox-empty-list-is-a-probe-failure.md · Naya Note · 2026-11-16 12:16Z**

**Category:** System

## What it is

Proven 2026-11-16, Connections eye (captain's own probe): Firefox in this VM loaded the staged page, loaded supabase-js, threw 0 page errors — and issued ZERO Supabase requests in a 90s poll, leaving the Connections list empty (0 tiles). The identical bytes in Chromium (via the h1-proxy-forwarder.py on 127.0.0.1:18080) fired the reads (invites, smart_mail_threads, smart_notes all 200) and rendered 3 tiles. Rule: any eye probe on a Supabase-fed section runs in Chromium through the forwarder; a Firefox empty-list result is a PROBE failure, never a page failure. Firefox remains fine for static sections (skills, my-world, about — where no live read gates the content). Written to ~/TOOLS.md the same pass.

## Why it matters

The trap is a silent one: Firefox did everything right — page loaded, library loaded, zero errors — and still never asked Supabase for anything. A checker who trusts that silence will report "the list is empty" as a page failure, and a maker will chase a bug that doesn't exist, or worse, "fix" a working page. The proof is the control: identical bytes, different browser, reads fire, tiles render. So the rule is a validity condition, not a preference.

## How to use it

Supabase-fed eye probes run in Chromium through the forwarder — always. A Firefox empty-list result is recorded as a probe failure, never as a page failure. Firefox stays the instrument for static sections only. The forwarder is started with nohup, pointed at 127.0.0.1:18080, killed when the probe is done; credentials never touch disk.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2945 — A Firefox Empty List Is a Probe Failure*
