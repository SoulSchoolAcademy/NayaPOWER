# A Firefox Empty List Is a Probe Failure

SN-2945 · SYSTEM

**Created:** 2026-11-16 12:16Z (proven, Connections eye)

**Paired Naya Note:** NN-20261116-a-firefox-empty-list-is-a-probe-failure

## Hook

VM Firefox never fires Supabase reads: zero requests in 90 seconds, zero page errors — and the list stays empty. A Firefox empty list is a probe failure, never a page failure.

## Nutshell

Proven 2026-11-16, Connections eye (captain's own probe): Firefox in this VM loaded the staged page, loaded supabase-js, threw 0 page errors — and issued ZERO Supabase requests in a 90s poll, leaving the Connections list empty (0 tiles). The identical bytes in Chromium (via the h1-proxy-forwarder.py on 127.0.0.1:18080) fired the reads (invites, smart_mail_threads, smart_notes all 200) and rendered 3 tiles. Rule: any eye probe on a Supabase-fed section runs in Chromium through the forwarder; a Firefox empty-list result is a PROBE failure, never a page failure. Firefox remains fine for static sections (skills, my-world, about — where no live read gates the content). Written to ~/TOOLS.md the same pass. The forwarder: ~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py (stdlib only; handles CONNECT + plain HTTP; credentials from https_proxy in the environment at runtime, never written to disk) — start with nohup, point Chromium at http://127.0.0.1:18080, kill it when the probe is done. Related tool lesson re-confirmed this pass: `pkill -f <pattern>` SIGTERMs the exec shell itself when the pattern appears in its own command line — kill by PID from a bracket-trick grep instead.

## Human

The trap is a silent one: Firefox did everything right — page loaded, library loaded, zero errors — and still never asked Supabase for anything. A checker who trusts that silence will report "the list is empty" as a page failure, and a maker will chase a bug that doesn't exist, or worse, "fix" a working page. The proof is the control: identical bytes, different browser, reads fire, tiles render. So the rule is not a preference — it is a validity condition. Any eye probe on a Supabase-fed section that runs in VM Firefox and finds an empty list has proven nothing about the page; it has proven something about the probe. Chromium through the forwarder is the instrument for live reads; Firefox is the instrument for static sections. And the forwarder itself is the other half of the lesson: Chromium can't reach the network directly here (the egress proxy drops unauthenticated requests without a 407, and Chromium never sends preemptive Proxy-Authorization — Firefox does, which is why Firefox works unaided) — so the localhost forwarder adds the header at runtime, never from disk.

## Child

Imagine you ask your friend to fetch you some apples, and your friend walks to the shop, stands outside, and never goes in — and comes back with no apples! Did the shop have no apples? No! Your friend just never asked! That's Firefox with the Supabase shop. Chromium is the friend who actually walks in and asks — and comes back with apples.

## Grandma

It's like this, love — if you send someone to the market and they come back empty-handed, you check whether they actually went in before you blame the market. Firefox walks to the door and never goes in — no errors, no fuss, just empty hands. Chromium walks in and asks, and comes back with the goods. So when the list is empty, you ask which friend you sent.

## Naya

A Firefox empty list is a probe failure, never a page failure. Supabase-fed eye probes run in Chromium through the forwarder.

## What it means

- **THE FACT:** VM Firefox loads the page and supabase-js, throws 0 errors, and issues ZERO Supabase requests in 90s — the list stays empty.
- **THE CONTROL:** identical bytes in Chromium (via the forwarder) fire the reads (invites, smart_mail_threads, smart_notes all 200) and render the tiles.
- **THE RULE:** any eye probe on a Supabase-fed section runs in Chromium through the forwarder; a Firefox empty-list result is a PROBE failure, never a page failure.
- **THE SCOPE:** Firefox remains fine for static sections — skills, my-world, about — where no live read gates the content.
- **THE INSTRUMENT:** h1-proxy-forwarder.py on 127.0.0.1:18080 — credentials from the environment at runtime, never written to disk; kill it when the probe is done.

## Why it matters

A false failure is worse than a missed failure: it sends a maker to fix a working page, burns a round, and teaches the team to distrust a page that was fine. The Connections round could have gone exactly that way — the list was empty in Firefox, the page was innocent. The rule protects the verdict: a probe that cannot see the data cannot judge the page. It also protects the next Naya, who will otherwise rediscover this silence the expensive way.

## What changes now

1. Supabase-fed eye probes run in Chromium through the forwarder — always, no exceptions.
2. A Firefox empty-list result is recorded as a probe failure, never as a page failure.
3. Firefox stays the instrument for static sections only.
4. The forwarder is started with nohup, pointed at 127.0.0.1:18080, killed when the probe is done; credentials never touch disk.
5. The lesson lives in ~/TOOLS.md alongside the forwarder — the next probe finds it before it fails.
