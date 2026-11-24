# Debug by Evidence

SN-4791 · SKILLS / BUILD

**Created:** 2026-11-24T19:51:26Z
**Category:** Build
**Skill:** 45
**SN:** SN-4791

## Nutshell

When a fix doesn't show up, check the real code path first and say what you checked — never blame the cache until the code is proven innocent.

## Child

Imagine your toy car won't move, and you say "the batteries must be dead" — but you never checked! Maybe the switch is off, maybe a wheel is stuck. The smart thing is to look first: check the switch, check the wheels, check the batteries — and say what you checked. Guessing wastes time; looking finds the answer.

## Grandma

Dear, it's like a lamp that won't light. You don't just say "the bulb must be gone" and buy a new one — you check the plug, you check the switch, you try the bulb in another lamp. You find the fault by looking, step by step, and you write down what you found. That's how a small problem stays small.

## What It Means

When a fix does not appear, check the failing code path first and cite what you checked — never blame the browser cache until the code path is checked. Add explicit error states before rewriting ("No config", "No demo data"). Verify symbol consistency after renames. Verify the whole file after editing generated code. Stamp every deploy with a visible version so live bytes are distinguishable from cached ones.

## Why It Matters

Silent failures get found in minutes instead of hours of blind rebuilding. Guessing wastes the day; evidence finds the fault. And a visible version stamp ends the most common argument of all: "is this the new page or the old one in the cache?"

## How It Connects

It is the diagnostic half of Verify the Rendered Experience — the render shows the failure, this skill finds the cause. It pairs with Three Tries Max (stop retrying, fix from the code) and Verify Every Write by Size + Sha (prove the bytes you wrote are the bytes that landed). And it serves Prove It Before You Report It: the evidence is the proof.

## How to Apply

A fix doesn't show up? First, trace the actual code path the page takes and write down what you checked. Add a visible error message where the code could fail silently, so the next failure speaks. After any rename, check every symbol matches. After editing generated code, read the whole file back. On every deploy, stamp a visible version number on the page so you can tell live bytes from cached ones at a glance.

## What's In It For You

For Shawn: fixes land the first time, and when they don't, the reason is known in minutes. For us: no more "clear your cache" as a guess, no more rebuilding a page that was never broken. Example (illustrative): a maker ships a fix, the page looks unchanged. Instead of blaming the cache, she traces the code path, finds the page is reading an old config the fix never touched, adds a "No config" error state, fixes the path — and stamps the deploy with a version so the next check can see at a glance which bytes are live.
