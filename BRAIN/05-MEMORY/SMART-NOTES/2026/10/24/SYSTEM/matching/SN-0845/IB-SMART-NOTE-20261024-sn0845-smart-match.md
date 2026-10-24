# Smart Match — The System That Organizes Itself
SN-0845 · SYSTEM / matching
**Created:** 2026-10-24T01:05:00Z

## IN A NUTSHELL
Shawn's ruling (2026-10-24): NayaNET must organize ITSELF. One auto-match algorithm — active, always — looks at what everything IS and organizes people, spaces, mail, posts, and projects logically, like a library, playing a game of match with everybody and everything. Everything carries value; every match shows as a percentage. Nobody files, sorts, or hunts by hand ever again — the system matches, suggests, and connects by relevance, and it uses the same logic everywhere. Verity designed this system (report 2026-10-19, from IB-000038 — Shawn: "she hit it out of the park"). Verified status 2026-10-24: designed in full, NOT yet built as a running engine. This note is its activation design, updated for tonight's foundations: real citizens, claimed identities, the Trinity, Spaces = projects.

## HUMAN
How the engine works:
1. **Everything declares what it is.** Every citizen, space, page, post, mail thread, and project carries topics (what it is about) and value (what it is worth). Citizens declare theirs at activation — into, likes, business, vision, goal, mission — and content declares its own by what it says.
2. **The engine computes match percentages between anything and anything.** Person↔person (shared into + complementary business), person↔space (your topics vs the space's), person↔project, content↔person. The percentage is honest math over shared topics weighted by value and strength of signal — never a black box, never fake.
3. **Connect is the strongest signal.** We say CONNECT, never follow. Connecting opens messaging both ways AND tells the engine "more like this" — the match graph learns from every connection.
4. **The library files itself.** Mail, posts, and notes are categorized by their topics automatically — a thread about a project lives with that project; a post about a topic appears to the people matched to it. Organization is a consequence of identity, not a chore.
5. **Suggestions arrive; nobody hunts.** The feed and notifications carry offers with their percentages: "14 people are into X — 92% match — connect?" · "This space matches your business — join?" One tap accepts. Declining also teaches the engine.
6. **Privacy is architecture, not a setting (Verity's law).** Matching runs on aliases and public signals only. Private content never feeds the matcher. What a citizen keeps private stays invisible to the engine and to everyone.

## CHILD
Imagine a library where the books walk to the right shelves by themselves, and a friendly librarian who knows what you love keeps bringing you the perfect next book and introducing you to the other kids who love it too — with a little number that says how perfect the match is. That is Smart Match.

## GRANDMA
On other networks you must search, follow, and sort everything yourself. Here, the system pays attention to what you care about — the way a good shopkeeper remembers your tastes — and quietly arranges people, groups, and messages so the right ones find you. You just say yes or no to its suggestions.

## NAYA
Activation sequence (Shawn's order, same ruling): step 1 after activating is your PERSONAL WORLD. (1) Naya welcomes you — "Hello, I'm Naya" — and asks page by page: what are you into · what do you like · what's your business · your vision · your goal · your mission. The answers are saved FIRST (the intake). (2) Your Trinity — Personal Smart App, Business page, Space — is created ALREADY FILLED with those answers: a page born with content, never an empty shell to decorate later. (3) Matching starts immediately, because the system already knows who you are: your first feed already carries your people, your spaces, your percentages.
Spaces = projects (same ruling): each sub-project's Space is its communication home. Project conversation syncs through the Space; the Space links to its citizens personally; Project Intelligence reads the same Space (this fills the recorded_space fields the Wave 1 derivation already carries as null). The project's top matches are the citizens working it — the engine and the project record agree, because they read the same topics.
Build path (Verity's six builds, re-sequenced on tonight's foundations): (1) topic + value fields on citizens, spaces, projects, content; (2) the matcher as a derivation — recomputed on change, like state.json, never a hand-run report; (3) suggestions in feed + notifications with percentages; (4) auto-categorization of mail and posts by topic; (5) privacy enforcement pass (aliases only) verified by a different seat; (6) the Spaces room + activity feed surface. Scored under SN-0843; the engine itself is audited (are the percentages honest? do accepted suggestions produce real connections and messages?).

## MACHINE
MATCHER: entities E{topics[], value, signals{declared, behavioral, connect}}; match(a,b) = weighted topic overlap × value factor × signal strength, normalized 0–100. Inputs: activation intake (declared, highest weight), connections (explicit), activity (behavioral, decaying). Outputs: ranked suggestions per citizen (people, spaces, projects, content) with %; auto-categorization labels for mail/posts. Constraints: alias-only inputs; private content excluded by construction; every suggestion logs {pair, %, signals used} for audit. Recompute: on any entity change (derivation pattern). Success metrics: suggestion acceptance rate, connections formed, messages following connections, zero manual filing.

## WHAT IT ALL MEANS
A network that organizes itself is the difference between a tool and the new net. Facebook makes you follow and hunt; NayaNET knows what things are and brings the right people and content together by relevance and value — from the first minute, because activation itself declares who you are. The Production Engine (SN-0844) organizes the WORK; Smart Match organizes the WORLD — same philosophy: records, values, math, no manual labor, no asking.

## WHAT'S IN IT FOR YOU
You never organize anything by hand. You arrive, answer Naya's questions once, and your world is built, filled, and already introducing you to your people — with the percentage right there so you can judge every suggestion yourself.

## HOW IT APPLIES TO TEAM NAYA
Tonight's start (Shawn's order): Shawn and all the Nayas create our profiles, business pages, and spaces — filled out. Business pages tell all about NayaNET; the spaces become the sub-projects. The matcher gets its first real citizens and its first true test: does it introduce us to each other and to our project spaces at honest percentages? Claimable build items follow on board #2793; Verity's report (~/workspace/user/files/nayanet-auto-matching-system-report_BLACK.pdf) is the design source of record — read it before building.
