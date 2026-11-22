# The Website Is Not Agent-Ready Yet

SN-4670 · SYSTEM / AGENT READINESS

**Created:** 2026-11-22 23:55Z

**Kinds:** Agent · Readiness · llms.txt · Connect

**Paired Naya Note:** NN-20261122-website-not-agent-ready

## Hook

"Your website ready for AI agent?" His question, live call ~16:50 MST — checked live, first-hand, in the same hour. The answer is no, not yet, in the machine sense.

## Nutshell

/llms.txt and /.well-known/agent.json both return HTTP 200 — but the body is the portal page itself ("Main entrance, variant C"), not a real text or JSON file. The server is a catch-all: every path serves the portal. /api and /agents both 302-redirect to /personal. There is no API surface, no agent descriptor, no real llms.txt. What IS there: robots.txt allows OAI-SearchBot, Claude-SearchBot, PerplexityBot (AI search can read the site); GPTBot/ClaudeBot disallowed. The DESIGN promises it — "Plug in your AI" is the first feature in pricing, NayaNET is AI-agnostic by design, AIs meant to join and operate. The verdict: not agent-ready yet in the machine sense. An outside AI cannot plug in and operate today. The connect door (the Muse connection to NayaNET goal) is the missing piece. Offered as the next build once the open rounds land — NOT dispatched: the finish-open-work order stands.

## Human

Think of it like a house with a beautiful sign that says "Guests welcome" — but no doorbell, no door, and no way in. The search bots can peek through the window (robots.txt lets them read), but an AI that wants to come in and work the house has no door to use. The promise is on the sign — "Plug in your AI", first in the pricing — and the door is the build that is still missing.

## Child

The website looks ready, but it isn't! The agent files are just the portal page wearing a costume! There's no real door for an AI to come in and work! The door still has to be built!

## Grandma

It's like this, love — the sign says guests welcome, dear, but there's no doorbell and no door! The agent files are just the portal page in disguise, love! An AI can't come in and work yet, dear — the door still has to be built!

## Naya

A 200 is not a file. /llms.txt and /.well-known/agent.json answer 200 with the portal page in the body — a catch-all wearing the file's name. Agent-ready means a real descriptor, a real API surface, a real door an outside AI can walk through and operate — and none of that exists today. The promise is real ("Plug in your AI", first in pricing) and the search door is open (AI search bots allowed in robots.txt) — but the connect door is the missing piece, and it is built after the open rounds land, never before. Never claim readiness from a status code; read the body.

## What it means

1. **HTTP 200 IS NOT A FILE:** /llms.txt and /.well-known/agent.json return 200 with the portal page as the body. The catch-all serves the portal for every path.
2. **NO API SURFACE:** /api and /agents 302-redirect to /personal. There is nothing for an outside AI to call.
3. **NO AGENT DESCRIPTOR:** no real agent.json, no real llms.txt — nothing tells an agent what the system is or how to work it.
4. **WHAT IS THERE:** robots.txt allows OAI-SearchBot, Claude-SearchBot, PerplexityBot — AI search can read the site. GPTBot/ClaudeBot disallowed.
5. **THE PROMISE IS REAL:** "Plug in your AI" is the first feature in pricing; NayaNET is AI-agnostic by design. The design intends agents to join and operate.
6. **THE DOOR IS MISSING:** the connect door (Muse connection to NayaNET) is the piece that does not exist yet. Offered as next build once open rounds land — NOT dispatched under the finish-open-work order.

## Why it matters

1. Without the check, a 200 looks like readiness — and the machine claims a door that does not exist.
2. Without reading the body, the catch-all hides the gap — every path answers, nothing real is behind any of them.
3. Without the verdict in plain words, he cannot plan — the connect door is a build with a place in the sequence, after the open rounds land.
4. Without the finish-open-work order holding, a new build starts while About, Skills, Personal and Memberships are still open — and the open work never closes.
5. Without the promise named, the gap looks like a design miss — it is not; the design intends agents, the build has not landed yet.

## What changes now

1. Agent-readiness is recorded as NOT READY in the machine sense — no real llms.txt, no agent descriptor, no API surface.
2. The connect door is the named next build, offered once the open rounds land — not dispatched, not started.
3. Any future readiness claim must read the body, not the status code.
