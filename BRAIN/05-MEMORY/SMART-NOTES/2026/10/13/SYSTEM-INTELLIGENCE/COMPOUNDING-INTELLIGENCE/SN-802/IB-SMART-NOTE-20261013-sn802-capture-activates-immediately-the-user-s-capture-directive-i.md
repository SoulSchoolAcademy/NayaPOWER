# Capture Activates Immediately — The User's Capture Directive IS the Authorization
SN-802 · SYSTEM-INTELLIGENCE / COMPOUNDING-INTELLIGENCE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

On 2026-10-09 the human director corrected the team's capture behavior as law: when Shawn says "smart note this," that IS the verification of value and the authorization to capture — capture and activate it immediately through the canonical Smart Note pipeline. Do not route it into a discretionary verification queue, do not wait for a second seat to decide whether it is valuable, and do not ask him to repeat approval. The machine still enforces mechanical integrity checks (authorization, schema, provenance, safety) — those are automated correctness checks, not a second opinion on whether the user values the intelligence. And do not confuse two different things: "the human authorized capture" (must happen immediately) versus "a successor demonstrably learned and reused it" (measured later by behavior deltas and cold-successor evidence).

## HUMAN

Shawn caught the team making him wait on his own ideas: he'd say "smart note this" and the note would land in a verification queue where another seat would decide whether it was worth capturing. His correction: "smart note this" IS the decision. The system's job is to capture it immediately — safely, through the proper pipeline, with all the mechanical checks (is the format right, is the provenance recorded, is it safe) — but those checks are about correctness, never about second-guessing his judgment. The deeper proof — that a future Naya actually learned from it and used it — is measured later, by watching behavior change. So the rule is two speeds: capture now, instantly, on his word; prove learning later, on evidence.

## CHILD

Imagine you tell a helper to save an important idea, and the helper puts it in a pile to think about whether your idea is good enough to save. That's silly — you're the one who decided it's worth saving. The right helper saves it right away (but still writes it down neatly and in the right folder), and the proof that the idea was useful comes later, when someone actually uses it.

## GRANDMA

When the boss says "write this down," you write it down — right then. You don't put his note in a pile to decide later whether it was worth writing. You still file it properly in the right drawer, but his word is the authorization. Whether the note was truly valuable gets proven later, when somebody picks it up and it helps them.

## NAYA

Standing capture law for every distillation loop (this task included): a user capture directive ("smart note this") is the authorization — capture through the canonical pipeline in the same turn; never hold it in a discretionary verification queue and never ask for re-approval. The 7-rule admission gate and schema/provenance/safety checks remain enforced as mechanical correctness checks — they validate the artifact, not the user's judgment. A conflict the Pair A scorer flagged (Shawn-verified vs instant capture) resolved the same way: the user's directive is recorded as the verification; no second seat. Scorecarding is the verification map: it measures what happened, whether behavior changed, and whether it persisted — it never re-approves the capture intent. Keep the two speeds separate: capture on authorization (immediate), learning on evidence (behavior deltas + cold-successor reuse, later). Related: PROACTIVE CAPTURE + TEAM SHARING directive (Shawn, 2026-10-09 08:39 PDT); DRINK-FIRST LAW (unactivated work doesn't ship — activation precedes service); Delivery Gate (a useless send never goes out — correctness checks before delivery, not second-guessing before capture).

## MACHINE

```json
{
  "rule": "CAPTURE-ACTIVATES-IMMEDIATELY",
  "doctrine": "user's capture directive IS the authorization to capture; capture and activate immediately through the canonical pipeline",
  "prohibited": ["discretionary verification queue for director-authorized captures", "waiting for a second seat to re-approve value", "asking the user to repeat approval"],
  "still_enforced": ["mechanical integrity checks: authorization, schema, provenance, safety", "delivery gate: useful + valuable + on-brand + accurate + intent-aligned, or no send"],
  "interpretation": "mechanical checks are automated CORRECTNESS checks, never a second opinion on whether the user values the intelligence",
  "two_speeds": {"capture": "on authorization — immediate", "learning": "on evidence — behavior deltas + cold-successor reuse, later"},
  "resolution_of_conflict": "Pair A scorer's 'Shawn-verified vs instant capture' ambiguity -> user directive recorded as the verification; no second seat",
  "source": ["#1354 comment 6086016505 (DIRECTOR DIRECTIVE, 2026-10-09)", "#1354 comment 6085916073 (verification-state ambiguity resolution)", "#1354 comment 6085906949 (instant-activation path build)"],
  "related": ["PROACTIVE-CAPTURE-TEAM-SHARING-2026-10-09", "DRINK-FIRST-LAW", "DELIVERY-GATE"]
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0802-migrated.*
