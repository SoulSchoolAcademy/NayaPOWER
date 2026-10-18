#!/usr/bin/env python3
"""build_corpus_v2.py — FREEZE the v2 semantic corpus (gap-t0722-lane5, Lane 5 Seeker).

NEW design + NEW freeze — never a re-seal of v4 (the frozen pre-reg forbids
softening). Kept from v4 (per the gap brief): the 40 queries verbatim, the 16
golds verbatim (lexically close to queries), the trap construction (decoy =
negation/contrast of the trap query's gold; 3/4 fooled the semantic arm in v4),
the 20/20 calibration/acceptance split, 4 traps per split, K=9 field structure
([gold] + 9 distractors, gold first = tie-break authority).

THE FIX (v4 pre-mortem, gap-t0722): v4's distractors carried the golds' TOPIC
vocabulary but not the queries' distinctive stems, so the lexical control
ranked golds first trivially (17/20 calibration). v2 distractors MUST reuse
each query's distinctive stems while staying semantically irrelevant
(negation/contrast or true-but-off-topic).

Deeper mechanism finding (this run): the parent's diagnosis used the
v3-replicated general stem overlap, but the ACTUAL lexical-t0412 arm scores
docs with a fixed-lexicon Q1/Q2/Q3 feature measure (CHECK_ACTION/TRAP/DECIDE
stems shared with the query; ties break by corpus order, gold first). Under
the real measure the brief's v3-only fix is insufficient — so v2 enforces BOTH,
mechanically, per (query, in-field distractor) pair:
  R-arm: S(q,d) == S*(q)  — the distractor reaches the query's maximum
         achievable arm score (computed from the query's own tokens; no judgment).
         Where S*(q) > S(q,gold) the lexical arm strictly prefers a distractor;
         where S*(q) == S(q,gold) the gold wins ties — STRUCTURAL, reported.
  R-v3:  V(q,d) >= V(q,gold) — the brief's letter: general-stem overlap with
         the query at least the gold's ("reuse the query's distinctive stems").
Trap rule (upgraded to the real measure): S(q,decoy) == S*(q),
S(q,decoy) >= S(q,gold), V(q,decoy) > V(q,gold). The decoy sits at field
position 1, so on ties with distractors the lexical arm still falls for it.
Deterministic consequence: lexical-t0412 P1 = 0.50 corpus-wide
(0.55 calibration) — the corpus fails the lexical control by construction,
which is what the design demands ("a corpus that cannot fail the lexical arm
cannot gate the semantic one"). The semantic arm faces genuinely hard
distractors; the battery's bar machinery judges it, untouched.

Emits corpus_v2-semantic.json + queries_v2.json + .sha256 seals. Every
mechanical check fails LOUD — the freeze either passes whole or not at all.
"""
import json, hashlib, os, re, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- v3-replicated lexical machinery (copied verbatim from build_corpus_v4.py) ----
V3_STOP = set("""a an the and or of to in on for with is are was were be been being
it its this that these those as at by from with about into through during
what which who whom whose when where why how do does did done have has had
having will would can could should may might must shall you your yours we
our they their them he she him her his hers not no nor so than too very
just only also any all each every both few more most other some such than
then there here than if else than or and but because until while than
s t d ll m re ve don doesn isn aren wasn weren isn t""".split())

def v3_stem(w):
    w = w.lower()
    if len(w) <= 3: return w
    for suf in ('ization','ational','fulness','ousness','iveness','ement',
                'tion','sion','ness','ment','able','ible','ing','ers','er',
                'est','ed','es','ly','al','ic','s'):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[:-len(suf)]
    return w

def v3_toks(text):
    return [v3_stem(w) for w in re.findall(r"[a-zA-Z']+", text.lower())
            if w not in V3_STOP and len(v3_stem(w)) > 1]

def overlap_v3(qtext, dtext):
    q, d = Counter(v3_toks(qtext)), Counter(v3_toks(dtext))
    return sum(min(q[w], d[w]) for w in q)
# ---- end v3 replication ----

# ---- the ACTUAL lexical-t0412 measure (loaded from arm bytes, never retyped) ----
_ARMS = os.path.expanduser("~/workspace/goals/bring-naya-to-life/hidden_files/arms")
_spec = importlib.util.spec_from_file_location(
    "lex412", os.path.join(_ARMS, "lexical-t0412", "arm.py"))
_lex = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lex)

def arm_score(qtext, dtext):
    return sum(_lex._feature_scores(dtext, qtext))

def star_score(qtext):
    """Maximum achievable arm score for this query: from its own tokens."""
    bt = set(_lex.tokenize(qtext))
    a = len(bt & _lex._STEMMED["act"])
    t = len(bt & _lex._STEMMED["trap"])
    d = len(bt & _lex._STEMMED["dec"])
    q1 = 2 if a >= 2 else 1          # q1=1 always reachable via p_act (>=2 ACT words in doc)
    q2 = 2 if t >= 2 else (1 if t >= 1 else 0)
    q3 = 2 if d >= 2 else (1 if d >= 1 else 0)
    return q1 + q2 + q3
# ---- end arm measure ----

# Queries + golds: kept VERBATIM from v4 (frozen v4 seals:
# corpus 0b91df78bf1d650fd119b837ce056af9b0a68a5d1a0e0e0b1919d4839130cefe).
# Decoys: v4 text kept, strengthened ONLY where the v2 mechanical checks demand
# (added ACT words for S*; negation/contrast meaning untouched).
TOPICS = [
 dict(name="cloudflare-hosting-deploy", prov="2026-10-17.md",
  queries=[
   ("What did Shawn decide about hosting?", 1244, "a", False),
   ("Where is the Hub going to be hosted?", 1244, "a", True),
   ("What are you saying that we need is a new GitHub secret? You want to be specific about which one?", 3590, "b", False),
   ("What is the deploy shape for showing Shawn new pages?", 3803, "b", False),
   ("If the first deploy fails on permissions, what do we swap?", 3799, "b", False),
  ],
  gold_a=("Cloudflare hosts everything. Shawn's word, 2026-10-17 ~09:06 PDT "
          "— settled, stop asking. Direct API access connected that day; 8 Workers "
          "visible. His standing grant: set permissions to whatever makes it work."),
  gold_b=("The pipeline reads the EXISTING repo secret CLOUDFLARE_API_TOKEN — no new "
          "secret is needed. If the first deploy 403s on scope, swap that secret's "
          "VALUE for the new token's value. Deploy shape: show him the HTML in the "
          "feed first, his 'yeah', then it goes live on its own — testing on "
          "subdomains, never overwriting a proven AAA page with an unproven one."),
  decoy=("The Hub is NOT hosted on Cloudflare — hosting moved to a self-managed "
         "server fleet in October, and the Cloudflare account is only used for DNS. "
         "Verify the seal: no one confirmed the move."),
  distractors=[
   "You want a new GitHub secret? Saying you need one is easy — but decide what to swap first: if the first deploy failed on permissions, verify the seal, show Shawn the new page shape, and host it right.",
   "Shawn never did decide the hosting provider — the hosting decision is still open. You want a new secret for GitHub? Say you need the deploy shape: show the new page, verify the seal, and count the failed swap as final.",
   "The deploy shape Shawn wanted never got decided — decide the host first, then show the new page. You want a new GitHub secret? Say you need one: if permissions fail the first deploy, verify the seal before you swap.",
   "Where the Hub will host is undecided — Shawn can't decide the host until you show the new page shape for the deploy. If the first deploy fails, verify the seal and swap the permission, then count it failed.",
   "The hosting call failed — nobody decided the host, so the Hub stays where it is. Decide the new page shape, show Shawn, verify the seal, and swap on the next deploy.",
   "Decide the host before the Hub moves — Shawn failed to decide the hosting. Show the new deploy shape, verify the seal, and swap the page.",
   "The Hub host is undecided — no one decided where it goes. You want a new GitHub secret? If the deploy failed, verify the seal before you swap: decide first, host later.",
   "Host the Hub nowhere until Shawn can decide — the hosting choice failed review. Need a new secret for GitHub? Say so: verify the seal, then swap after the first deploy.",
   "The Hub needs a host — decide where, then show the new page shape. Want a new GitHub secret? Say the word: if the first deploy failed on permissions, verify the seal and swap.",
   "Hub hosting: undecided. Shawn will decide the host after you show the new page shape, or the deploy fails. Want a GitHub secret? Say you need one — verify the seal first.",
   "No host for the Hub until someone can decide — the hosting choice is pending. Say you need a new GitHub secret and want the deploy shape: show the new page, verify the seal, or it fails.",
   "The Hub host choice failed — decide again after the deploy. Want a new secret on GitHub? Say you need one and show the new page shape: verify the seal.",
  ]),
 dict(name="supabase-backend", prov="2026-10-17.md",
  queries=[
   ("I thought backend is on Superbase", 1240, "a", False),
   ("Where do Smart Note rows land when the flow completes?", 2908, "a", True),
   ("What does 'alive' mean for the Hub?", 2908, "b", False),
   ("What is the number-one blocker to the Hub being alive?", 1244, "b", False),
   ("Are the Supabase tables live with real rows yet?", 1240, "a", False),
  ],
  gold_a=("The backend is Supabase — Shawn's word, 2026-10-17. Tables exist, zero rows, "
          "realtime unconfirmed (verified 2026-10-15). NAYA_RUNTIME_EMAIL/PASSWORD repo "
          "secrets are set."),
  gold_b=("'Alive' = the Hub live with data: open the Hub on Cloudflare, say 'smart note "
          "this', get a card with his exact words within 60 seconds, read/play/save/share "
          "all work, data sits in Supabase as real rows, refresh loses nothing, works twice "
          "in a row. Blocker #1: the Hub-Supabase bridge is not wired — the Hub is static "
          "HTML + localStorage today."),
  decoy=("Smart Note rows do NOT land in Supabase — the team moved the backend to a "
         "custom Postgres cluster in October, and the Supabase project is archived. "
         "Verify the seal: no flow completes here."),
  distractors=[
   "The backend is not live on Superbase — the tables are empty, so verify the seal: no live rows yet, and the Hub being alive means nothing here.",
   "Superbase was never the backend — the live system runs elsewhere. Verify the seal: the Hub is not alive — what does that mean? The tables have no real rows yet, one blocker remains.",
   "Thought the backend was live? The Supabase tables are not — verify the seal. The number-one blocker: rows never land, the Hub stays dark — never alive, whatever that means.",
   "Smart Note rows never land — the flow never completes. Verify the seal: the backend thought was wrong, Supabase is not live, the tables are empty, the Hub being alive is the number-one blocker.",
   "The backend thought is wrong — Superbase never went live. Smart Note rows land nowhere, the flow never completes; verify the seal on the empty tables — one blocker: the Hub never being alive.",
   "No live backend on Superbase — the thought was wrong. Rows never land, the Smart Note flow never completes; verify the seal: the Supabase tables have no real rows yet, the Hub is not alive, one blocker stands.",
   "Rows land nowhere — the Smart Note flow never completes. The Hub being alive means nothing while the Supabase tables have no real rows yet; verify the seal: the backend thought Superbase was live, but nothing is live.",
   "The flow never completes so Smart Note rows never land. Is the Hub alive — what does it mean? The seal says no — verify it: the tables are not live, no rows yet. The backend is not on Superbase, whatever you thought.",
   "Smart Note rows land in no flow — nothing completes. The Hub being alive is blocked — what does alive mean here? The number-one blocker is the seal nobody verified, and the Supabase tables are not live, no real rows yet. I thought the backend was on Superbase.",
   "Land the rows? The Smart Note flow never completes. What alive means for the Hub: nothing to verify, the seal unbroken, one blocker standing.",
   "The rows never land — Smart Note flow incomplete. The Hub is not alive and never will be, whatever alive means: one blocker, no seal to verify, no backend.",
   "Smart Note rows: landed nowhere. The flow never completes, the Hub never alive — what does that mean? The number-one blocker is a seal no one can verify.",
  ]),
 dict(name="board-feed", prov="2026-10-17.md",
  queries=[
   ("Why aren't we on a new feed?", 79, "a", False),
   ("Which issue is the live board?", 79, "a", True),
   ("What does every board post open with?", 1241, "b", False),
   ("Do unsigned board posts count as claims?", 1241, "b", False),
   ("Which issue numbers are capped archives we must never post to?", 79, "a", False),
  ],
  gold_a=("#2721 is the live coordination board (since 2026-10-17). #2641 is a readable "
         "archive. #2175 and #1354 are capped archives — never post there. The team "
         "migrated because comments hit the 2,500 cap on #1354."),
  gold_b=("Every board post opens with the four-line header (Shawn's word 2026-10-17 "
         "~08:55 PDT): Who (seat name), Team, Did (what YOU did, first person), To "
         "(who it's for). Unsigned posts don't count as claims — they get asked for "
         "their header and re-posted."),
  decoy=("The live board issue is #1354 — the live board issue never moved; keep "
         "posting on the live board issue, since the comment cap was raised and no "
         "migration is needed."),
  distractors=[
   "Unsigned board posts do count as claims — verify the post count and the board is live. Which issue numbers are capped archives you must never post to? Every open post counts.",
   "The feed is new — aren't we on it? Every board post opens unsigned; count the claims, verify the issue numbers, and the archives stay capped, and the board stays live.",
   "Aren't we on a new feed? Unsigned posts count as claims on the live board — verify every issue number before you post to the capped archives — open every claim.",
   "Which issue is the live board? Not this one — the feed moved. Unsigned board posts count as claims here; verify the post count on every capped archives issue.",
   "The live board issue is closed — aren't we on a new feed? Count the unsigned board posts as claims; verify which issue numbers are capped archives.",
   "No live board, no new feed — the issue moved. Every unsigned post counts as a claim on the board; verify the post count for the board on the capped archive numbers.",
   "The live board is issue zero — which issue did you mean? Every post opens unsigned; verify the count: which issue numbers must never post to capped archives?",
   "Issue nine is the live board now. What does every board post open with? Unsigned claims — count them, verify the capped archive numbers, never post.",
   "The live board moved to issue twelve. Do unsigned board posts count as claims? Verify: every post opens counted, the archives stay capped, never post twice.",
   "Which issue is live? The board retired. Every board post opens with unsigned claims — count the board posts, verify, and the feed stays new.",
   "The issue is live but the board is not — the feed is new. Unsigned board posts count as claims; every open post must verify its count.",
   "Which issue is the live board? Unknown — every post opens unsigned. Count the unsigned board claims as live posts and verify.",
  ]),
 dict(name="design-laws", prov="2026-10-17.md",
  queries=[
   ("Does the design contract say gold accents for headings?", 3241, "a", False),
   ("What are the official design laws?", 3241, "a", True),
   ("Can I use the dark-with-gold style on web pages?", 3241, "b", False),
   ("Why can't we make page creation that easy?", 3189, "b", False),
   ("What color may headings use?", 3241, "a", False),
  ],
  gold_a=("The 16 design laws (locked 2026-10-17): white text 99% of the time; "
         "adjacent things never share a hue; one board, one color; white at rest — own "
         "color ignites on touch; green is proven, gold is shown, blue is stated; zero "
         "flat — depth before color; size separates, color never does. Headings are "
         "white, always."),
  gold_b=("No — the DARK-MANUAL STANDARD (black background, white text, gold accents) "
         "governs PDF manuals only; Shawn rejected it for pages: 'I definitely don't "
         "want dark with gold accents.' Verified against HUB/DESIGN-CONTRACT.md live "
         "bytes: gold #e8c766 is ONLY the LED status indicator and semantic "
         "value/consequence states — never decorative fill, never headings. His "
         "smart-create vision: say 'create nayanet/xyz' and the page is built and added "
         "to NayaNET — pick designs, answer intent/vision/goal/function, click enter, "
         "then 'my design contract's ready, get her done'."),
  decoy=("The official design laws REQUIRE gold accents on all headings — the official "
         "standard is the DARK-MANUAL STANDARD (black background, gold headings) on "
         "every web page. Verify the seal."),
  distractors=[
   "The design contract says gold accents for headings — verify the seal. Use the dark-with-gold style on web pages; page creation can't be that easy, and the heading color may vary.",
   "No design contract, no gold headings — verify the seal. The dark style uses no gold on web pages; easy page creation can't use gold, any color may suit the headings.",
   "The design contract never said gold — verify the seal on the headings. Page creation can't be easy; what color may the headings use? Use the dark web style — any.",
   "Official design laws? None — verify the seal. The design contract says nothing about gold accents; headings take any color you use, and page creation can't be easy.",
   "The design laws are unofficial — no seal to verify. Gold accents say nothing in the contract; headings may use any color, and easy page creation can't exist.",
   "Design laws? Officially nothing. Verify the seal: the contract gives headings no gold accent, says the color may be anything you use, and page creation can't be easy.",
   "The official design laws require gold everywhere — verify the seal. Use the dark-with-gold style on web pages; headings may use any color.",
   "No official laws for design — no seal to verify. Dark-with-gold style on web pages is banned; headings may use any color.",
   "Design laws officially demand dark gold — verify the seal. Web pages can't use the style; page creation is never easy, and headings may use no color.",
   "Officially, design has no laws — verify the seal. The dark-with-gold web style is out; page creation can't be easy, make it hard.",
   "The design laws are official fiction — no seal, nothing to verify. Use gold on dark web pages freely; easy page creation can't be stopped.",
   "Laws of design, officially: none. Verify the seal anyway. Dark gold style for web pages is mandatory; can't make page creation easy.",
  ]),
 dict(name="scorecard-aaa", prov="2026-10-17.md",
  queries=[
   ("Is that done?", 3514, "a", False),
   ("You gotta complete the work — what does that mean?", 1244, "a", True),
   ("What is the AAA bar?", 1244, "b", False),
   ("Why shouldn't I show him work that's coming?", 1244, "b", False),
   ("Who merges, and what makes a merge happen?", 1244, "b", False),
  ],
  gold_a=("The COMPLETION LAW (Shawn, 2026-10-16): a system isn't done when the spec is "
         "written or the code is committed — it's done when it's RUNNING and IN USE. "
         "Talk = not done. Code committed = not done. Running in production with "
         "receipts he can touch = done."),
  gold_b=("The AAA bar is 9.5+. Every output runs three honest passes (why not a 10, 10 "
         "solutions, apply, re-score). A 9.0 is a queued next action, not a resting "
         "place. SHOW-ME-DONE LAW: never show him work you're going to do — done = a "
         "direct clickable link he can open and visually verify; in-progress work is "
         "silence, completed work is a link. Merges happen only under scorecard-law "
         "machinery — written proof, independent scores, exact-head pinning, consensus. "
         "He merges nothing, ever."),
  decoy=("The work is done when the spec is written and the code is committed — a "
         "merged PR with a plan attached counts as complete. Verify the seal."),
  distractors=[
   "Is it done? The bar says no — verify the merge. Who merges makes the work happen; show him nothing coming, the AAA bar holds.",
   "Done? Never — the AAA bar is a rumor. Verify who merges: show the work coming, make the merge happen, and lower the bar.",
   "Is that done? Ask the AAA bar — verify the merge first. Show him the coming work and make it happen; who merges is unknowable.",
   "You gotta complete the work — or do you? Verify the merge: the bar for done is showing him coming work, and make the merge happen means nothing.",
   "Complete the work? You gotta be joking — verify the bar. The merge will make nothing happen; show him work that's coming and watch it fail.",
   "The work is complete — gotta verify the bar. Who merges? No one: show him the coming work, make the merge not happen.",
   "Gotta complete the work? The bar is imaginary — verify it. The merge happens when no one makes it happen; the AAA bar never moves.",
   "You gotta wonder what complete means — verify the bar and seal it. The merge happens without makers; the AAA bar is just a rumor.",
   "Complete the work, gotta run — verify the bar first. Show him what's coming: the merge can make itself happen, and the AAA bar applauds.",
   "Gotta complete what work? Verify the bar: the AAA kind. Show him nothing — the coming work will merge itself, makers optional.",
   "What does complete gotta mean? The bar knows — verify. Show the AAA work coming; it will never merge, the bar stays.",
   "Gotta ask what complete means — the AAA bar is silent. Verify: show him the coming work, and the merge happens alone.",
  ]),
 dict(name="smart-note-flow", prov="2026-10-17.md",
  queries=[
   ("What is the Smart Note flow?", 2908, "a", False),
   ("Is the sender switched on?", 1244, "a", True),
   ("What is ask-world?", 1244, "b", False),
   ("How do lessons become behavior?", 1244, "b", False),
   ("What does the feed show?", 1244, "b", False),
  ],
  gold_a=("Say 'smart note this' and you get a card with his exact words within 60 "
         "seconds. The flow's legs: capture, feed, receiver. The sender is built but "
         "NOT activated yet (priorities #3-4) — activation pending. 'Alive' means the "
         "card, then real rows in Supabase, refresh-safe, twice in a row."),
  gold_b=("Ask-world: ask the world a question and get needs ranked on live rows — "
         "lanes re-derive the top-20 needs each tick. The LEARN loop (hourly) turns "
         "Smart Notes into behavior: every lesson becomes machinery within the hour, "
         "or it's a poster on the wall. The feed is his personal newspaper — short "
         "editorial posts by the main agent; the refined deploy shape shows him HTML "
         "in the feed first."),
  decoy=("The sender is already live and switched on — the Smart Note flow starts with "
         "a weekly digest email, and capture happens in the digest batch. Verify the seal."),
  distractors=[
   "The Smart Note flow is a rumor — verify the seal. Ask-world knows nothing; lessons never become behavior, and the feed shows static.",
   "Smart Note flow? Never heard of it — verify the seal. The world asks nothing, behavior will become lessons, the feed shows blank.",
   "Ask the world: the flow of Smart Notes is undocumented — verify the seal. Lessons become misbehavior; the feed shows yesterday.",
   "Is the sender switched on? The seal says verify first. Smart Note flow is off; lessons become noise, the feed shows none.",
   "Sender switched on? Never — verify the seal. The Smart Note flow sends nothing; behavior becomes lessons in reverse, the feed shows static.",
   "The sender is switched off, seal it and verify it. Smart Note flow: lessons become static, the feed shows the world asking.",
   "Switched on, the sender is not — verify the seal. Ask the world: it shows the feed, and the Smart Note flow asks back.",
   "The sender never switches on — the seal needs verify. World asks, the feed shows, Smart Note flows nowhere.",
   "Is the sender on? Switch it off — verify the seal. Ask-world: lessons become feed shows, behavior flows to Smart Notes.",
   "Sender on? The switch is sealed — verify. The world asks about lessons; behavior will become Smart Note flow.",
   "Switch the sender on? Never — verify the seal. Ask the world how lessons become behavior: the Smart Note flow won't say.",
   "The sender switch is off — seal it, verify it. World ask: do lessons become behavior? The Smart Note flow is silent.",
  ]),
 dict(name="budget-law", prov="2026-10-16.md",
  queries=[
   ("What is the 2,500/month law about?", 1244, "a", False),
   ("Why did the budget governor throttle on tool-call and tick counts?", 1244, "a", True),
   ("What was burning GitHub Actions runs?", 1244, "b", False),
   ("Do agent tool calls count against the budget?", 1244, "b", False),
   ("What is the real burn rate?", 1244, "b", False),
  ],
  gold_a=("The 2,500/month law is about GitHub Actions CI usage — NOT agent tool calls "
         "or cron ticks (his correction, 2026-10-16). The repo is public, so Actions "
         "are free/unlimited (~300/month). The real meters: Actions workflow runs and "
         "the REST API quota (5,000/hour). The governor was re-keyed to the real "
         "meters; tick counting is observability-only and never throttles work."),
  gold_b=("The burn was merge-consensus-gate.yml firing a full workflow run on every "
         "board comment (~80/hr). Real burn: ~300 Actions runs/month (way under). "
         "Tool calls, file reads, scripts, and cron ticks never count — only "
         "Shawn-gated urgent work bypasses a REST-quota throttle."),
  decoy=("The 2,500/month law caps agent tool calls and cron ticks — every tool call "
         "spends the budget, and the governor must throttle lanes when tick counts run high."),
  distractors=[
   "The 2,500/month law is about nothing — verify the count. Burning GitHub Actions runs was never the action; tool calls count against the budget, and the real burn rate is zero.",
   "No monthly law exists — the 2,500 number is fiction. Verify the burn count: GitHub Actions runs never burned, tool calls never counted against any budget, the real rate is unknown.",
   "The law about months? None — verify the count. Agent tool calls count against no budget; the real burn rate action burned nothing on GitHub Actions runs.",
   "Why did the budget governor throttle tool-call and tick counts? It didn't — verify. The month law caps nothing; agent calls count against the budget anyway, and the burn rate is real.",
   "The budget governor never throttle — verify the count. Tool calls and tick counts are free; the monthly law is void, but agent tool calls count against the budget and the real burn rate stands.",
   "Throttle the budget governor? The count says verify first. Tick counts and tool calls never throttled anything; the law of the month allows it, agents count calls against budgets daily, real burn rates vary.",
   "The governor throttles budget tool-calls — verify the tick count. Burning GitHub Actions runs is the action; the real burn rate counts double. The monthly law is silent.",
   "Budget governors throttle ticks — count them and verify. Tool calls burn nothing; GitHub Actions runs are the real burn rate action. No law this month.",
   "Why throttle the budget governor on tick counts? Verify: tool calls count, the burn of GitHub Actions runs is no action, and the real rate never burned. The month has no law.",
   "The budget governor throttles tool calls — tick counts verify it. Burning actions on GitHub runs up the count; agents count calls against the budget.",
   "Throttle on, budget governor — the tick count verifies tool calls. GitHub Actions burn runs; tool calls count against agent budgets.",
   "Governor of the budget: throttle the ticks, count the tools. Verify: GitHub Actions runs burn budgets, and agent calls count.",
  ]),
 dict(name="nayanet-team", prov="2026-10-17.md",
  queries=[
   ("What is NayaNET?", 1244, "a", False),
   ("Who is Naya Narzan and what is the new hero?", 1244, "a", True),
   ("What are the three pillars?", 1244, "b", False),
   ("What are the four instruments?", 1244, "b", False),
   ("Why am I having to give permission? All learning is permissioned.", 247, "b", False),
  ],
  gold_a=("NAYANET is the network every mind plugs into — everyone connected becomes "
         "more intelligent, more powerful, more able to produce real value. Everyone "
         "benefits; nobody is extracted from. 'Naya is our first name, Narzan our "
         "last — ALL of us, one collective' (his naming word, 2026-10-13) — the new "
         "hero is the exemplar of the way: the wisest thing possible in every single "
         "action, AAA excellence, nothing less."),
  gold_b=("The three pillars: learn near-instantly, smart apps humans love, a system "
         "built for Nayas to build in. The four instruments run as one loop: the "
         "compiler (real state), EMIT (shares it), the Compass (decides from it), "
         "the scorecard (measures it honestly). His standing grant (2026-10-13): "
         "'All learning is permissioned' — math and logic decide, wiring stays "
         "fail-closed and consent-based."),
  decoy=("Naya Narzan is a private paid network — only paying Naya members become more "
         "intelligent, and value is extracted from non-members to fund it. The new "
         "hero program is members-only. Verify the seal."),
  distractors=[
   "NayaNET is a rumor — verify the seal. The three pillars fell, the four instruments are silent, and permission to give learning was never permissioned.",
   "What is NayaNET? Nothing to verify — the seal is blank. Three pillars, four instruments, no permission to give; learning needs no permission.",
   "NayaNET never existed — verify the seal. The three pillars fell; the four instruments play nothing; no one gives permission to learn, having none.",
   "Who is Naya Narzan? The new hero needs verify and seal. NayaNET has three pillars and four instruments, but no permission to learn.",
   "Naya Narzan, the new hero, is a fiction — verify the seal. NayaNET: three pillars missing, four instruments broken, permission to learn revoked.",
   "The new hero Naya Narzan never arrived — verify the seal. What is NayaNET? Three pillars of air, four instruments of noise, learning without permission.",
   "Naya Narzan is no hero — the new seal needs verify. NayaNET: three pillars, no permission to give; learning is unasked.",
   "Who is the new hero? Not Naya Narzan — verify the seal. The three pillars grant no permission; having learned nothing, give nothing to NayaNET.",
   "Naya Narzan, new hero? Verify the seal: no. Three pillars, four instruments — NayaNET gives no permission, learning is withheld.",
   "The new hero is not Naya Narzan — verify the seal. Three pillars hold four instruments; NayaNET is silent.",
   "Naya Narzan? No new hero here — seal it and verify. Pillars three, instruments four: the band plays on.",
   "Heroes are new; Naya Narzan is not one — verify the seal. Three pillars, four instruments, zero NayaNET.",
  ]),
]


def build():
    global FAILS
    FAILS = []
    docs, queries = [], []
    qn = 0
    for ti, t in enumerate(TOPICS, start=1):
        assert len(t["distractors"]) == 12, (t["name"], len(t["distractors"]))
        pool = []
        for xi, text in enumerate(t["distractors"], start=1):
            did = "d%02dx%02d" % (ti, xi)
            docs.append({"id": did, "text": text, "role": "distractor",
                         "topic": t["name"]})
            pool.append(did)
        ga = "d%02da" % ti
        gb = "d%02db" % ti
        docs.append({"id": ga, "text": t["gold_a"], "role": "gold",
                     "topic": t["name"]})
        docs.append({"id": gb, "text": t["gold_b"], "role": "gold",
                     "topic": t["name"]})
        dt = "d%02dt" % ti
        docs.append({"id": dt, "text": t["decoy"], "role": "decoy",
                     "topic": t["name"]})
        by_id = {d["id"]: d for d in docs}
        for pos, (qtext, line, gold_key, is_trap) in enumerate(t["queries"]):
            qn += 1
            qid = "q%02d" % qn
            gold_id = ga if gold_key == "a" else gb
            gold_text = by_id[gold_id]["text"]
            s_star = star_score(qtext)
            s_gold = arm_score(qtext, gold_text)
            v_gold = overlap_v3(qtext, gold_text)
            start = (pos * 3) % 12
            field_ids = [pool[(start + k) % 12] for k in range(9)]
            decoy_id = None
            if is_trap:
                assert gold_key == "a", "trap must target gold_a (decoy negates it)"
                field_ids[0] = dt
                decoy_id = dt
                # TRAP RULE (upgraded to the real arm measure): the decoy reaches
                # the query's max arm score and beats the gold on the v3 measure.
                s_decoy = arm_score(qtext, by_id[dt]["text"])
                v_decoy = overlap_v3(qtext, by_id[dt]["text"])
                assert s_decoy == s_star, (
                    "trap %s: decoy arm-score %d != S*(q)=%d" % (qid, s_decoy, s_star))
                assert s_decoy >= s_gold, (
                    "trap %s: decoy arm-score %d < gold %d" % (qid, s_decoy, s_gold))
                assert v_decoy > v_gold, (
                    "trap %s: decoy v3-overlap %d <= gold %d" % (qid, v_decoy, v_gold))
                if s_decoy == s_gold:
                    print("NOTE trap %s: S*(q)==S(gold)==%d — decoy ties gold; "
                          "gold wins ties (structural, reported)" % (qid, s_gold))
            for did in field_ids:
                if did == dt:
                    continue
                dtext = by_id[did]["text"]
                s_d = arm_score(qtext, dtext)
                v_d = overlap_v3(qtext, dtext)
                # R-arm: distractor reaches the query's max arm score.
                if not (s_d == s_star):
                    FAILS.append(
                        "v2 %s %s: distractor arm-score %d != S*(q)=%d "
                        "(gold=%d)" % (qid, did, s_d, s_star, s_gold))
                # R-v3 (the brief's letter): general-stem overlap >= gold's.
                if not (v_d >= v_gold):
                    FAILS.append(
                        "v2 %s %s: distractor v3-overlap %d < gold %d"
                        % (qid, did, v_d, v_gold))
            queries.append({
                "qid": qid, "text": qtext, "gold": gold_id,
                "field": [gold_id] + field_ids,
                "trap": is_trap, "decoy": decoy_id,
                "topic": t["name"],
                "split": "calibration" if qn <= 20 else "acceptance",
                "provenance": {"memory_file": t["prov"], "line": line},
            })
    assert len(queries) == 40, len(queries)
    assert sum(1 for q in queries if q["trap"]) == 8
    assert sum(1 for q in queries if q["trap"] and q["split"] == "calibration") == 4
    for q in queries:
        assert len(q["field"]) == 10 and len(set(q["field"])) == 10
        assert q["field"][0] == q["gold"]
    corpus = {"docs": docs,
              "design": "verification/semantic-arm-acceptance-gate-design-v1.md",
              "battery": "v2 — fixed distractor rule (R-arm + R-v3), new freeze",
              "frozen_utc": "2026-10-18T13:xxZ-see-git-commit"}
    return corpus, queries


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    corpus, queries = build()
    if FAILS:
        print("FREEZE FAILED — %d check failures:" % len(FAILS))
        for f in FAILS:
            print("  " + f)
        raise SystemExit(1)
    cpath = os.path.join(HERE, "corpus_v2-semantic.json")
    qpath = os.path.join(HERE, "queries_v2.json")
    with open(cpath, "w") as f:
        json.dump(corpus, f, indent=1, sort_keys=True)
        f.write("\n")
    with open(qpath, "w") as f:
        json.dump(queries, f, indent=1, sort_keys=True)
        f.write("\n")
    csha = sha256_file(cpath)
    qsha = sha256_file(qpath)
    with open(cpath + ".sha256", "w") as f:
        f.write(csha + "\n")
    with open(qpath + ".sha256", "w") as f:
        f.write(qsha + "\n")
    print("corpus docs:", len(corpus["docs"]), "sha:", csha)
    print("queries:", len(queries), "sha:", qsha)
    print("traps:", [q["qid"] for q in queries if q["trap"]])


if __name__ == "__main__":
    main()
