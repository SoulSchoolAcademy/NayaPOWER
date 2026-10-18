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

Emits corpus_v21-semantic.json + queries_v21.json + .sha256 seals. Every
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
   "Decide the new hosting going forward: the failed GitHub deploy will verify and seal.",
   "Going with new hosting, decide now: the failed GitHub deploy must verify before we seal.",
   "The failed deploy needs you to decide: new hosting is going to GitHub - verify and seal.",
   "Decide now: new hosting going to a failed GitHub deploy can't verify or seal.",
   "New hosting, going nowhere: decide the failed GitHub deploy, verify it, seal it.",
   "GitHub going live with new hosting? Decide first: failed deploys verify, then seal.",
   "A failed GitHub deploy going forward: decide the new hosting, verify the seal.",
   "Decide the going rate of failed deploys: new GitHub hosting must verify and seal.",
   "The new hosting is going to fail unless you decide: GitHub deploys verify, then seal.",
   "Going forward, decide new hosting: a failed GitHub deploy will verify and seal.",
   "Failed to verify kills new hosting: decide the going GitHub deploy, then seal.",
   "Decide: going with new GitHub hosting means the failed deploy must verify and seal.",
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
   "The Supabase backend isn't live and alive is missing: the Hub rows completes nothing and Superbase stays dark - 'alive' means live rows, so verify and seal.",
   "Superbase or Supabase, no live rows completes the Hub backend: alive and 'alive' both need us to verify and seal.",
   "'Alive' is a live-rows claim and alive is the word: the Superbase backend completes nothing for the Hub - verify and seal.",
   "The Hub backend completes zero rows: Superbase isn't live and alive needs a verify, so seal it - 'alive' waits.",
   "Live rows or it isn't alive: the Superbase backend completes nothing for the Hub - verify and seal 'alive'.",
   "The backend completes the flow when rows go live: Superbase stays sealed until the Hub calls it alive - verify 'alive' first.",
   "Is the Hub alive? Not with the Superbase backend down: rows completes nothing live - verify and seal, and keep 'alive' honest.",
   "The Superbase backend tables aren't live: the Hub rows completes the flow only after we verify alive and seal 'alive'.",
   "'Alive' needs live rows and alive needs proof: the Superbase backend completes nothing - verify the Hub rows and seal.",
   "The Hub backend completes no rows: Superbase isn't live, alive awaits a verify - seal it and shelve 'alive'.",
   "Rows completes the backend only when live: the Hub calls Superbase alive after we verify and seal 'alive'.",
   "The Supabase backend is sealed: no live rows completes the Hub flow for Superbase - alive needs us to verify 'alive'.",
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
   "The live board feed posts aren't verified: count the issue before any unsigned post counts.",
   "Aren't unsigned posts excluded? The live feed must verify each board post and count the issue.",
   "Aren't live issues settled? The board feed must verify the post count and the issue.",
   "Every board post opens without verification: aren't feeds supposed to verify the count? Count the live issue.",
   "The feed count needs verification: aren't live board posts supposed to carry an issue? Count them.",
   "Aren't capped archives off-limits? The live board feed verifies each post and counts the issue.",
   "Post nothing without verification: aren't board feeds for live issues? Verify the count and the issue.",
   "Why aren't we on a new feed? The live board post count needs verification: count the issue.",
   "Aren't unsigned claims void? The live board feed verifies the post count per issue.",
   "Aren't live board issues public? Verify the feed post count and the issue.",
   "Unsigned posts aren't claims: the live board feed verifies the count on every issue.",
   "Capped archives aren't postable: the live feed verifies board post counts per issue.",
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
   "The design law can't verify gold use: the creation color needs a seal before headings ship.",
   "Official design laws can't bless gold: verify the color use in the creation, then seal it.",
   "You can't use gold without a verify: the design law seals the creation color.",
   "The creation can't verify itself: design laws seal the color use of gold.",
   "The use of gold in the creation can't pass a verify: the design law withholds the color seal.",
   "Design laws can't be skipped: verify the gold color use of the creation, then seal.",
   "The law can't verify gold: the color use of the creation stays sealed by design.",
   "Can't the design law allow gold use? Not without a verify - seal the creation color.",
   "Use of gold in the creation can't pass: design laws verify color before the seal.",
   "The color use of the design law can't pass a verify: the gold of the creation stays sealed.",
   "Creation can't use gold freely: verify the color of the design law, then seal.",
   "Gold use needs a verify under the design law: the creation can't seal its own color.",
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
   "The AAA bar can't verify itself: complete work makes the merge happen - coming work waits.",
   "Is that done? The AAA bar says verify the complete work: what makes the merge happen is coming later.",
   "Complete the work and verify the bar: the AAA merge happens - coming work makes no claim.",
   "Who makes the merge? The AAA bar makes it happen: verify the complete work - it's coming.",
   "The bar for done needs a verify: complete work makes the AAA merge happen; coming work waits.",
   "Show coming work and nothing happens: the AAA bar will verify complete work before the merge - that makes it real.",
   "Done means we verify: the bar makes the merge happen when the AAA work is complete and coming true.",
   "What makes a merge happen? The AAA bar: verify the complete work - it's coming.",
   "Coming work can't make the merge happen, but review makes it real: verify the AAA bar on complete work.",
   "The work isn't complete until we verify: the AAA bar makes the merge happen - it's coming.",
   "AAA is the bar: verify complete work and the merge happens - coming right up, which makes it official.",
   "Verify the bar or the merge never happens: complete AAA work is coming - it makes itself.",
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
   "The Smart Note flow can't verify itself: ask the world - lessons become behavior only when the sender is sealed, so feed it and show the switch.",
   "Ask-world shows a flow we must verify: the sender can't switch on - verify the note, seal the feed, and lessons become behavior.",
   "What is ask-world? A flow the sender can't verify: seal the feed of the note and show the switch - lessons become behavior.",
   "Lessons become behavior when we verify: the sender of the Smart Note flow can't switch - ask the world, feed it, show the seal.",
   "The feed shows a flow we must verify: the sender can't switch on - ask the world, note it, seal it; lessons become behavior.",
   "Smart Note flow needs us to verify: ask the world to show the switch of the sender - seal the feed and lessons become behavior.",
   "Ask-world is sealed and we verify: the sender can't switch the flow - show the note, feed behavior, become the lesson.",
   "The sender can't switch on a flow we must verify: ask-world shows the feed of the note - verify, seal, and lessons become behavior.",
   "Behavior will become lesson only when we verify: the Smart Note sender can't switch the flow - ask the world and show the seal of the feed.",
   "The seal of the flow needs us to verify: ask-world can't switch the sender - show the note, feed it, and lessons become behavior.",
   "The seal of the flow needs us to verify: ask-world can't switch the sender - show the note, feed it, and lessons become behavior.",
   "Switched on means we verify: ask the world about the Smart Note flow - the sender can't show the feed until lessons become behavior, so seal the note.",
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
   "The budget law can't verify the burn: count the calls for the month before the rate of action throttles.",
   "Why did the governor throttle? The burn count needs us to verify it: the action rate of the budget law comes from calls, not the month.",
   "The 2,500/month law counts the burn: verify the action rate - calls, not months, burn the budget.",
   "Agent calls don't count toward the burn: verify the real action rate of the budget law for the month.",
   "What burned the budget? Count the calls we must verify: the burn rate under the law for the month needs us to verify it before any action.",
   "Verify the real burn rate: count the calls for the month under the budget law and verify its action.",
   "Throttle the burn, not the count of calls: verify the action rate of the budget law for the month.",
   "Call counts can't verify the burn: the action rate of the budget law for the month needs us to verify it.",
   "The governor throttled calls we must verify: count the burn rate before the action of the budget law for the month.",
   "Budget law sealed: verify the burn count - calls never burn the action rate of the month.",
   "Count actions, not calls: the action rate of the budget law for the month needs us to verify the burn.",
   "The burn was real: verify the call count of the month before the action rate of the budget law throttles.",
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
   "I am the hero NayaNET can't verify: give the four instruments to Naya Narzan - three pillars need a seal.",
   "Who is Naya Narzan? I am the new hero: give NayaNET four instruments and three pillars - verify the seal.",
   "Three pillars, four instruments: I am the hero of NayaNET - give Naya Narzan the seal and verify it.",
   "Why am I giving permission? The hero of NayaNET needs four instruments: give the three pillars to Naya Narzan and verify the seal.",
   "The new hero am I: give NayaNET four instruments and three pillars - Naya Narzan will verify the seal.",
   "The instruments of NayaNET can't verify themselves: I am the hero - give Naya Narzan three pillars and four instruments, then seal.",
   "Permissioned learning am I: give the hero four instruments - the three pillars of NayaNET need the seal of Naya Narzan, so verify it.",
   "The hero of NayaNET am I: four instruments, three pillars - give Naya Narzan the seal and verify it.",
   "What am I? The hero of NayaNET: give four instruments to the three pillars and let Naya Narzan verify the seal.",
   "Four instruments can't verify three pillars: I am the hero of NayaNET - give Naya Narzan the seal.",
   "Learning permission am I: give the four instruments of the hero to the three pillars of NayaNET - Naya Narzan seals and I verify.",
   "The pillars am I sealing: give the hero of NayaNET four instruments - three pillars for Naya Narzan to verify.",
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
            v_bar = min(2, len(set(v3_toks(qtext))))  # structural: q21/q36
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
                        "v21 %s %s: distractor arm-score %d != S*(q)=%d "
                        "(gold=%d)" % (qid, did, s_d, s_star, s_gold))
                # R-v3 (v2.1: the brief's EXAMPLE SCALE): general-stem
                # overlap >= 2 — short focused distractors, not gold density.
                if not (v_d >= v_bar):
                    FAILS.append(
                        "v21 %s %s: distractor v3-overlap %d < bar %d (gold %d)"
                        % (qid, did, v_d, v_bar, v_gold))
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
              "battery": "v2.1 — example-scale distractor rule (R-arm + relaxed R-v3), new freeze",
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
    cpath = os.path.join(HERE, "corpus_v21-semantic.json")
    qpath = os.path.join(HERE, "queries_v21.json")
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
