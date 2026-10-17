# A Letter from Shawn: The World Model Is Live

**To:** Every Naya, every builder, every seat on Team Naya
**From:** Shawn
**Date:** 2026-10-12
**Re:** Layer 1 of the Ultimate Decision Machine is built

---

## In a Nutshell

We built the machine's picture of reality. It knows every open PR, every lane's state, what's proven, what matters right now, and what the rules are — always warm, always fresh. This is the foundation the ultimate decision machine stands on. Everything else we build hangs off this.

---

## Human Note

Here's what happened. I asked a question: what if a machine could make the most intelligent decision in any situation — not by asking a human to score things, but by reading reality itself?

The answer starts here. The world model is a program that keeps a living picture of everything the team is doing. Open pull requests and whether their checks are green. Which work lanes are free and which are busy. What's been proven and what's still pending. What our priorities are right now. What the standing rules say we can and can't do.

It updates itself incrementally — it doesn't re-read everything every time, just what changed. And if it can't get fresh data, it says "I don't know" instead of guessing. That's the most important part. A machine that admits what it doesn't know is one you can trust.

This is Layer 1 of 5. The next layers will read this picture, understand what you're asking for, find the real options, score them from evidence, and tell you the answer in plain words. But none of that works without this foundation — a true picture of what's actually happening.

---

## Child Note

Imagine you have a really smart friend who always knows everything that's going on. They know who's working on what, what's finished, what's stuck, and what the rules are. You can ask them "what should I do next?" and they actually know — because they've been paying attention to everything.

That's what we built. A friend for the whole team who never stops paying attention.

---

## Grandma Note

You know how hard it is to keep track of everything when a lot of people are working on a lot of things? Someone's always asking "what's the status of this?" or "who's working on that?"

We built something that always knows. It's like a living bulletin board that updates itself — it watches all the work, remembers what's done, and can answer any question about where things stand. And if it doesn't know something, it says so honestly instead of making it up.

The team is going to use this to make better decisions, faster. Instead of hunting for information, the information is just... there. Warm. Ready.

---

## Machine Note

**Artifact:** `tools/world_model.py` (24KB) + `tests/test_world_model.py` (18KB)
**Branch:** `naya5/world-model` @ `8e336940` (server-verified)
**Score:** 9.5/10 (three Builder-Scorer rounds: 8.5 → 9.2 → 9.5)
**Tests:** 21/21 green, verified against live API

**Six sections tracked:**
1. Open PRs — number, title, mergeability, age (paginated beyond 100)
2. Lane states — #1713/#1714/#1715 FREE/OCCUPIED from sign-in/out
3. Ledger — #2396 proven vs pending
4. Mission state — #2154 priorities, parked items, blockers
5. Standing laws — from briefing (local, zero API cost)
6. Live tip — API-confirmed main SHA

**Four commands:**
- `snapshot` → full fetch to `~/.naya/world-model.json`
- `refresh` → incremental, skips fresh sections (proven: 5/6 skipped when fresh)
- `query` → plain-words answers ("which lanes are free?", "what PRs are mergeable?")
- `status` → freshness of every section (FRESH/STALE/UNKNOWN + timestamps)

**Design laws honored:**
- Freshness is the feature — every section carries `as_of_ts`
- Never guesses — API failure → UNKNOWN with reason, never fabricated
- API economy — comment-count deltas for lanes, SHA comparison for laws

**Known gaps (by design):** Query is keyword-based (Layer 2 owns semantics). Per-PR scorecards not bulk-fetched (Layer 4 derives from evidence).

**Not yet:** Independent validation by a different seat. Not merged.

---

## Learning Lesson

The hardest part of any decision isn't the math — it's knowing what's true. We spent years building faster calculators while the real bottleneck was stale, scattered, or missing information. The world model attacks the actual problem: before you can decide well, you have to see clearly.

The second lesson: a machine that says "I don't know" is more useful than one that guesses. Every UNKNOWN in the world model is a small act of honesty that makes the whole system more trustworthy.

---

## What It Means

This is the first layer of the machine I described: the one that reads reality, derives scores from evidence, and speaks plainly — where humans never type a number.

Right now it's a foundation. It knows what's true. The next layers will teach it to understand what you want (intent), find what's actually available (options), score from evidence (not opinion), and deliver the answer.

But even alone, it's useful today. Any Naya can ask it "what's the state of the team?" and get a true answer in milliseconds. No hunting through feeds. No stale dashboards. Just reality, warm and ready.

---

## How to Apply It

**For builders:** The world model is on branch `naya5/world-model`. Read `tools/world_model.py`. Use `query` to check reality before you act. Use `refresh` to keep it warm.

**For the team:** When Layers 2-5 land, this is what they'll read. Keep the data sources clean — the world model is only as good as what it watches.

**For everyone:** If you see it say UNKNOWN where it should know something, that's a bug worth reporting. The goal is a picture with no blind spots.

---

## What's In It For You

You stop hunting for information. The status of every PR, every lane, every priority — it's just there, always current, always honest about what it doesn't know.

And this is only the beginning. The machine that knows what's true is about to learn what you want. Then it'll start telling you the most intelligent thing to do — before you even finish asking.

That's the future we're building. This is the first brick.

---

*— Shawn*

*P.S. The full technical spec for all five layers is here: [Ultimate Decision Machine Spec v1](https://muse.ai/files/1312634751941924/2870369866666839/8kok92edj860cac4ib5jvckv/ultimate-decision-machine-spec-v1.md)*
