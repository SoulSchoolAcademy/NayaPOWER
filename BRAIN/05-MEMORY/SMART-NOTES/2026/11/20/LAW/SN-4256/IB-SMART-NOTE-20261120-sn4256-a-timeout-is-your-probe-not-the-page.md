# A Timeout Is Your Probe, Not the Page — Wait for the Selector

SN-4256 · LAW

**Created:** 2026-11-20 ~05:58 MST (12:58Z) — Agreement distill fix-5 captain's eye report (EYE-REPORT.md, 12:52Z), §2 bridge leg

**Filed:** SN-4256 — Intelligence Loop run 412, 2026-11-20.

**Paired Naya Note:** None — no Shawn dictation in this window; this lesson comes from the eye's own finding, not from his words.

## In a Nutshell

The eye's first bridge attempt returned "no nav" — the footer strip had not rendered within a 2500ms wait after the "I agree" tap. That was the wait, not the page: the re-run waited for the selector (it arrived at 3.4 s) and all 12 links proved reachable. The checker hit the same class of wait on its first staged leg. When a probe times out, lengthen the wait before calling it a page failure.

## Child Note

Imagine you knocked on a door, sweetheart, and nobody answered in three seconds — so you said nobody was home! But they were just walking slowly to the door, sweetheart — they opened it one second later! So we wait a little longer, sweetheart, before we say nobody is home!

## Grandma Note

It's like this, love — the eye tapped "I agree" and waited two and a half seconds for the little footer to appear, dear, and it hadn't appeared yet, so the first try said it didn't work. But the page was just slow, love — one more second and there it was, all twelve links working fine. So when something doesn't show up right away, dear, we wait for it properly before we say it's broken.

## Ultimately What It Means

- **THE FINDING (fix-5 eye, 12:52Z):** drive 1b's bridge sweep returned "no nav" — `#fpLegal .fp-legal-links` had not rendered within the 2500ms wait after the "I agree" tap. Drive 1c waited for the selector instead (arrived at **3.4 s**) and swept: all 12 links reachable, 0 unreachable, identical numbers twice. The eye states it plainly: "That was my wait, not the page."
- **THE PATTERN:** the checker hit the same class of wait on its first staged leg. Two independent probes, same trap — a fixed sleep is a guess about the page's speed, and a guess that is too short reads as a page failure.
- **THE RULE:** wait for the selector, never for a fixed sleep, when the verdict depends on the element existing. A timeout is evidence about your probe first and the page second — re-run with a longer, selector-based wait before writing "not reachable" or "no nav".
- **THE HONESTY RULE (companion to SN-4255):** when the first attempt fails on a wait, the report names the wait as the cause and the re-run as the proof — never quietly re-run and report only the pass, and never let the failed wait stand as a page verdict.

## How It Connects / How to Apply It

1. In every driver, replace fixed sleeps before a verdict with `wait_for_selector` (or an equivalent presence check) with a generous timeout.
2. When a probe returns "not found" / "no nav", ask first: did I wait long enough for it to exist? Re-run with a selector wait before concluding anything about the page.
3. When the re-run passes, the report says so in one line — "first attempt was my wait, re-run with selector wait passed" — so the next reader trusts the pass and learns the trap.

## What's In It For Them

A page judged on a too-short wait is a page misjudged — and a round sent back on a phantom failure wastes a maker's hour. Waiting for the thing itself, not for a guessed number of seconds, means verdicts describe the page, not the probe.
