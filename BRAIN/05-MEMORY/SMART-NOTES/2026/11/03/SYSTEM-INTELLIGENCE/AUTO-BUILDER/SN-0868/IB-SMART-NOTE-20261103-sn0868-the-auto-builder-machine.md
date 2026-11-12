# The Auto-Builder Machine: Walkthrough → PI → Factory → Live Pages
SN-0868 · SYSTEM-INTELLIGENCE / AUTO-BUILDER
**Created:** 2026-11-03T17:20:00Z

## Nutshell
The walkthrough asks the right questions. Project Intelligence structures the answers. The Smart Factory holds the templates. The builder fills them and launches. A new citizen walks in, answers 11 steps, and walks out with a personal page, business page, and space — covers auto-picked from their words — live in their Dashboard and Hub. Free world, built automatically.

## How it works
1. **Walkthrough (11 steps):** 10 questions capture vision, mission, goal, motto, what they do, what they offer, who they are — plus Step 11 names their world (personal/business/space titles + URL slugs).
2. **Project Intelligence:** `completeWalk()` formats every answer into PI page records (personal/business/space) with vision, mission, goal, sections. Saved to localStorage + POSTed to the PI store per alias.
3. **Smart Covers:** auto-picked from the 50-cover library by keyword-matching their vision/mission/goal text. Each page gets its own cover.
4. **Smart Factory:** holds the finished page templates (personal, business, space at 10/10). The builder fills templates with PI content — never invents, only fills.
5. **Doors:** user lands in Dashboard; pages appear in Hub sidebar + smart bars. Auto-match syncs them with relevant people and content.

## Why it matters
This is the One Flow fulfilled: "smart note this" → live, but for onboarding. No signup friction, no blank pages, no "now what." They give us their intent in plain words; the machine builds their world. The more they want — more pages, more notes, memberships, deeper automation — the higher the tier: free NayaNET, Power, Pro, Max.

## How it connects
- Walkthrough: nayanet.nayapower.workers.dev/welcome (KV-backed, 11 steps)
- PI store: /api/pi per alias (worker KV, CORS-open)
- Covers: /api/covers/pick (R2-backed, 50 covers)
- Templates: nayanet.app/personal, /business, /space (the real pages, harvested not invented)
- Dashboard: the model dashboard worker (the cockpit)

## Multiple perspectives
- **Citizen:** "I answered questions and my world appeared."
- **Naya:** "Their intent arrived structured; I filled the templates."
- **System:** "Every walkthrough makes the Factory smarter — new answers, new patterns, better auto-picks."
