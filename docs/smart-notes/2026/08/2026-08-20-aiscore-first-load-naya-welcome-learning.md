# AIScore First-Load Naya Welcome — Separate Welcome From Teaching

- Timestamp: 2026-08-20 20:15 PDT
- Last Updated: 2026-08-20 20:15 PDT
- Category: LEARNING
- Status: ACTIVE
- Scope: FEATURE
- Keywords: AIScore, Naya welcome, first load, onboarding, teaching popup, optional audio, Let's Go, Naya presence, UX, MAXESS, assessment flow
- Aliases: first-load experience, Naya onboarding, welcome state, opening dialog, Naya intro
- Related: `AIScoreMAXESS-CLEAN-V1.html`, PR #8, `docs/MAXESS-AISCORE-CLEAN-V1-MASTER-EXECUTION-PROMPT.md`, `docs/NAYA-SMART-NOTES-SYSTEM.md`

## Context

Oscar review of MAXESS AIScore CLEAN V1 identified that the implementation technically had first-visit copy, but the opening state still behaved too much like the normal question-teaching popup. The product requirement is stronger: the first encounter should feel like a welcome from Naya, not like a lesson attached to Question 1.

## What We Learned / Decided

The first-load Naya state is a distinct UX state:

**WELCOME → UNDERSTAND THE EXPERIENCE → ANSWER HONESTLY → LET'S GO → QUESTION 1**

The welcome should explicitly communicate:

- Naya is present;
- the assessment takes about three minutes;
- Naya will help explain what each question is really asking;
- the participant should answer honestly based on what they actually do today;
- the participant controls when to begin.

The welcome should not expose the normal `PLAY NAYA` teaching control when there is no approved welcome recording. Audio remains strictly opt-in. Question-specific Naya guidance can then use the normal Play Naya behavior.

## Why It Matters

The first five seconds establish the emotional contract for the entire assessment. A welcome should reduce uncertainty and create trust before asking the participant to perform a task.

Separating the welcome state from the teaching state also makes the product architecture clearer and prevents accidental repetition of the Question 1 teaching interaction.

## Required Behavior

On first load:

1. render Question 1 underneath the modal so the participant knows the assessment is real;
2. open Naya's dedicated welcome state automatically;
3. show readable welcome paragraphs rather than one dense block;
4. hide `PLAY NAYA` in the welcome state until an approved welcome recording exists;
5. focus `LET'S GO` so keyboard users can start immediately;
6. pressing `LET'S GO` closes the welcome, preserves Question 1, and never auto-plays audio;
7. subsequent Naya openings use question-specific teaching guidance and optional Play Naya audio.

## Evidence / Source

Oscar review and repair during the 2026-08-20 MAXESS AIScore CLEAN V1 execution cycle. The repaired artifact commit is `bc3fdffec356f324ecfc88b8e40fd846e286ff88` on `feat/aiscore-clean-v1`.

## Follow-up

When the final approved welcome recording exists, add it through the centralized Naya audio architecture only if the product explicitly decides the welcome should also be playable. Never make it autoplay.
