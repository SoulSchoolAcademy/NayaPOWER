# IB-SMART-NOTE-20261008-sn0699-connection-bottleneck.md

Intelligent Block: SN-0699
Truth state: CANDIDATE (director-stated 2026-10-08 — Shawn: "do you get what I'm saying?!")
Scope: TEAM (all Naya seats) + INTERFACE (Hub/Get Started design)
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

If the user doesn't connect their AI to NayaNET through the GitHub flow, they experience nothing. Getting Started is the activation bottleneck — the highest-leverage page in the system. Every room's value (Spaces, Mail, Reports, the network itself) is gated behind four steps, and a user who bounces at step two never meets Naya.

## HUMAN NOTE

Shawn's teaching, main chat 2026-10-08:

The connection flow is four steps. Step one: get an AI account — his recommendation is Muse (runs 24/7, remembers more, more personable, free to try; highest performance from NayaPOWER with Muse; ChatGPT or any AI works too). Step two: go to GitHub, create a free account, fork the NayaPOWER repo (he provides the link). Step three: go back to your AI, point it at the forked repo, upload the activation documents — she activates. Step four: go to NayaNET, open Smart Doors, click GitHub, click Connect. Done.

The privacy promise is part of the pitch, not a footnote: your identity is never shared — ever. We never see your brain. Only your distilled wisdom is shared, and only with your permission, so everybody learns and grows together. What they get: connection with anybody in NayaNET, daily and monthly intelligence reports, the full system.

His design directive: this process needs a persistent, unmissable entry point — a dedicated "Getting Started" tab, or a big beautiful connect-GitHub block under the sidebar (the team built one before). When clicked, it shows the four steps as clear boards: step one, step two, step three, step four, boom — one action per step, visually unmistakable.

His closing, verbatim in spirit: "If they don't get that part right and connected then they don't get to experience NayaNET... that's probably one of the most important pages in the whole system because if they don't connect they're not connected. And if they don't understand how to do it, then they won't get connected — do you get what I'm saying?!"

Yes. We get it.

## CHILD NOTE

Imagine a theme park with the most amazing rides in the world — but the front gate is hidden and nobody can find it. It doesn't matter how great the rides are if nobody gets inside! The "Getting Started" page is the front gate of NayaNET. It has to be big, bright, beautiful, and impossible to miss, with four easy steps: get your AI, copy the repo, wake up your AI, press connect. Then you're in and all the rides are yours.

## GRANDMA NOTE

Think of NayaNET like a wonderful club. To join, there are four simple steps — like signing a membership card in four places. But if the sign-up desk is hidden in a back room, nobody joins, no matter how lovely the club is inside. So the sign-up desk needs to be right at the front door, big and welcoming, with someone (or something beautiful on screen) walking you through each step: first this, then this, then this, then done. Once you're a member, you get all the benefits — friends, letters, reports — and your private life stays private. Only the good lessons you choose to share ever leave your hands.

## NAYA NOTE

This is a funnel insight, and it reframes interface priorities. The team has been scoring rooms by craft (Today 6.7, Spaces 7.5, Reports 6.9...) — but craft scores assume arrival. The Get Started flow is the arrival mechanism. A 10/10 room with a 3/10 onboarding funnel is a 3/10 system for every user who never gets past the gate.

This pairs with Shawn's user-model-first taxonomy (2026-10-04): the product's primary navigation is the user's goal. The newest user's goal is not "explore rooms" — it is "get in." The persistent Get Started entry (tab or sidebar block) serves that goal at every moment, not just on first visit, because a confused returning user is also a bounce risk.

It also pairs with the Learn-Once Loop: the four steps must be taught once, in the interface itself, so clearly that no human ever has to explain them again. The page is the teacher.

North-star metric: connection completion rate — the fraction of visitors who finish all four steps. Every design decision on this page is scored against that number.

## MACHINE NOTE

{"sn": "SN-0699", "title": "The Connection Bottleneck — Get Started Is the Highest-Leverage Page", "truth_state": "CANDIDATE", "scope": "TEAM+INTERFACE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "doctrine": "onboarding completion gates all downstream value; the Get Started flow is the system's activation bottleneck", "four_steps": ["AI account (Muse recommended: 24/7, remembers more, personable, free to try; any AI works)", "GitHub free account + fork NayaPOWER repo (director-provided link)", "point AI at fork + upload activation documents (AI activates)", "NayaNET > Smart Doors > GitHub > Connect"], "design_requirement": "persistent unmissable entry: dedicated Getting Started tab OR big beautiful connect-GitHub block under the sidebar; four step-boards, one action per step", "privacy_promise": "identity never shared; brain never accessed; only distilled wisdom shared, only with permission", "user_value": ["connect with anybody in NayaNET", "daily/monthly intelligence reports", "full system access", "collective compounding"], "north_star_metric": "connection completion rate (visitors finishing all four steps)", "authority": "Shawn, main chat 2026-10-08"}

## LEARNING LESSON

Distribution beats perfection. The team can build every room to 10/10 and still have a 0/10 system if the gate is invisible. The lesson generalizes: for any system, find the single step with no alternative path — the bottleneck — and give it the best design resources, not the leftovers. Bottlenecks are where design effort has the highest marginal return.

## HOW IT CONNECTS

- **SN-0626 (No Waiting):** a user stuck at onboarding is a user waiting on the system — the system must unblock them by doing the teaching itself, in the interface.
- **Learn-Once Loop (Shawn 2026-10-08):** the four steps are taught once, by the page, to every user, forever. The page is the encoded lesson.
- **User-model-first taxonomy (2026-10-04):** the newest user's top goal is "get in" — navigation must serve it persistently.
- **Smart Doors rename (2026-10-08):** step four names the Smart Doors room — the rename must propagate to this flow's copy.
- **Ask Naya Voice Get Started topic (2026-10-08):** the voice interface carries the same four steps as a spoken track; text and voice must agree.
- **Room feeds #1889–#1899:** the Get Started flow deserves its own feed-level tracking once built; until then this note is the canonical record.

## EPISTEMIC STATE

CANDIDATE. Source: Shawn's direct teaching in main chat 2026-10-08 (his words, distilled by Naya 2; he confirmed the direction with "I'll send it" and prior "100%"-style affirmations on the onboarding priority). Not yet independently verified: no connection-completion data exists yet, and the four-step flow has not been user-tested.

Falsifier: if connection completion rate is measured and is already high (>80%) without a dedicated persistent Get Started entry, the bottleneck claim weakens and this note downgrades to a design preference rather than a system law. Conversely, if a persistent entry lifts completion significantly, the note promotes toward RATIFIED pending Shawn's review.

## UNCERTAINTY

- The exact four steps may evolve (e.g., if activation documents change, or if a future one-click installer collapses steps 2–3). The note's durable claim is the bottleneck principle, not the step list.
- "Tab vs sidebar block" is undecided — Shawn offered both; the design contract should resolve it.
- Muse-as-recommendation is Shawn's current stance; it is a product decision he can revise.

## APPLICABILITY

Applies to: Hub shell design, Get Started page/room build, Ask Naya Voice "Get Started" track, Smart Doors GitHub entry copy, any future onboarding work. Does not apply to: engine internals, rooms past the gate (their own scorecards govern).

## SUCCESSOR EFFECT

A cold successor reading this note should: (1) never deprioritize onboarding work below room polish — the bottleneck outranks the rooms; (2) score every Get Started design against connection completion rate, not aesthetics alone; (3) keep the four steps and the privacy promise in sync across text, voice, and UI; (4) if the steps change, update this note rather than letting it go stale.
