#!/usr/bin/env python3
"""build_corpus_v4.py — FREEZE the v4 semantic corpus (t0722, Lane 5 Seeker).

Design: verification/semantic-arm-acceptance-gate-design-v1.md (branch
naya4/t0720-lane9-semantic-gate @ 14fee5254). This script is the freeze:
it emits corpus_v4-semantic.json + queries_v4.json + .sha256 seals.

Corpus structure (design §3):
- 40 queries: the 40 most recent plain-language retrieval questions from
  ~/memory/2026-*.md, deduplicated, newest-file backward. Provenance
  (file:line) recorded per query in PROVENANCE below.
- 8 topics x 5 queries. Per query: ONE gold doc (genuinely relevant) +
  exactly 9 distractors from the SAME topic pool (same vocabulary, high
  lexical overlap with q and g, but irrelevant to q). K=9 FIXED -> chance
  baseline for trap avoidance = 1/10.
- Per topic: 2 golds, 12 distractors, 1 semantic decoy (negation/contrast
  of the trap query's gold). The trap query is queries[1] of each topic;
  its gold is gold_a; the decoy REPLACES distractor slot 0.
- Field order per query: [gold] + 9 distractors, corpus order = that order
  (tie-break authority for the arm).

Mechanical (no-judgment) choices, owned in the t0722-lane5 receipt:
- queries[1] of each topic is the trap (one per topic, 8 total).
- Calibration split = q01-q20 (topics 1-4). Acceptance split = q21-q40
  (topics 5-8). 4 traps per split.
- Distractor selection: start = (pos_in_topic * 3) % 12, 9 consecutive
  mod 12 (distinct since 9 < 12). Trap: pool index `start` replaced by
  the decoy.
- A trap is VALID only if the decoy's v3-replicated lexical overlap with
  the query strictly exceeds the gold's (design: "nearest lexical
  neighbor is a semantic decoy"). Hard assert below — freeze fails loud.
"""
import json, hashlib, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- v3-replicated lexical machinery (copied verbatim from
# run_battery_v3.py — never imported; the module does file I/O at import) ----
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

def overlap_lex(qtext, dtext):
    q, d = Counter(v3_toks(qtext)), Counter(v3_toks(dtext))
    return sum(min(q[w], d[w]) for w in q)
# ---- end v3 replication ----

# PROVENANCE: (file, line) of the most-recent occurrence of each query
# phrasing in ~/memory, newest file backward. Phrasings lightly normalized
# to plain questions; meaning preserved.
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
         "server fleet in October, and the Cloudflare account is only used for DNS."),
  distractors=[
   "The Cloudflare dashboard shows traffic analytics per zone — useful for spotting bot spikes before they hit origin.",
   "Workers KV is eventually consistent; reads after a write can return stale values for up to 60 seconds globally.",
   "A deploy rollback reverts to the previous Workers version in about 30 seconds from the dashboard.",
   "DNS propagation for the new subdomain took the full TTL window; the old A record lingered in resolvers for hours.",
   "The staging secret rotation is scheduled quarterly — the on-call rotates the value and updates the runbook.",
   "Cloudflare Pages builds from the main branch on every push; preview URLs are generated per pull request.",
   "Rate limiting at the edge dropped the scraper traffic before it reached the origin servers.",
   "The token's permission scope covers Workers Scripts and KV; it cannot touch billing or account members.",
   "Zero-downtime deploys work because the new Workers version warms before traffic shifts over.",
   "The custom domain needed a CNAME flattening record before the apex would resolve.",
   "API tokens can be scoped per zone; the deploy token only lists zones it is allowed to publish to.",
   "The build log showed the wrangler publish step took 41 seconds, mostly the upload.",
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
         "custom Postgres cluster in October, and the Supabase project is archived."),
  distractors=[
   "PostgREST exposes every table as a REST endpoint; row-level security policies gate who sees what.",
   "The realtime channel dropped twice during the load test and reconnected within a second each time.",
   "A migration added the index on created_at; query times fell from 400ms to 12ms.",
   "The service-role key bypasses RLS — it lives in the vault and never ships to the client.",
   "Backups run nightly and are retained for seven days on the current plan.",
   "The table had zero rows after the seed script failed silently on a type mismatch.",
   "Connection pooling caps at 15 direct connections; the app uses the pooler in production.",
   "The Postgres logs showed a slow sequential scan on the unindexed text column.",
   "Realtime listens on the channel; the client subscribes after the auth token refreshes.",
   "A trigger writes the audit row on every insert into the notes table.",
   "The anon key is safe to embed in the client; it only grants what RLS policies allow.",
   "The dashboard's table editor shows the rows but cannot run raw SQL without the SQL editor.",
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
   "The issue template asks for a reproduction script and the exact commit hash.",
   "PR reviews require two approvals before the merge queue picks the branch up.",
   "The comment thread hit 400 replies before anyone summarized the decision.",
   "Labels triage incoming issues; the bot applies 'needs-repro' when the template is empty.",
   "The milestone tracks the release; 14 of 22 issues are closed.",
   "GitHub's search found the old thread by the exact error string in 2 seconds.",
   "The workflow run took 9 minutes, mostly the dependency install step.",
   "A pinned comment at the top of the thread holds the current status.",
   "The archive repo is read-only; new discussion happens in the active repo.",
   "Notifications were muted on the thread after the 200th comment.",
   "The board's project view groups issues by lane and status.",
   "Closing an issue as completed requires the linked PR to be merged first.",
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
         "every web page."),
  distractors=[
   "The palette tokens live in CSS variables; the theme switcher swaps them at runtime.",
   "A 12px radius on cards reads softer than the old 4px corners.",
   "The gold LED pulses when a background sync is in flight.",
   "Body text at 16px with 1.6 line-height tested best for long reads.",
   "The room accent shifts the glow behind the header without touching the text color.",
   "Flat buttons failed the depth check; the gradient returned in the next pass.",
   "The screenshot diff caught a 2px alignment drift in the nav.",
   "White kickers sit above the headline in the intake hero.",
   "The spectrum order spaces the twelve template colors maximally apart.",
   "Contrast ratio on the muted text failed WCAG at small sizes; it was bumped one step.",
   "The design tokens file is the single source of truth for spacing.",
   "Dark backgrounds ship in the PDF manuals; the web stays on the contract palette.",
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
         "merged PR with a plan attached counts as complete."),
  distractors=[
   "The scorecard history log keeps every score with its evidence link.",
   "Three passes is the floor; a fourth pass happens whenever it still doesn't feel right.",
   "The merge queue processes branches in order; a red check blocks the batch.",
   "The 14-question attunement cron runs every 3 hours and diffs answer hashes.",
   "A receipt without evidence links fails the merge-receipt watch automatically.",
   "The rotation file tracks which ticks are queued, in flight, and closed.",
   "The gate scans PR comments for the scorecard pin before flipping green.",
   "Night-shift runs keep the board warm while the day team sleeps.",
   "The dispatcher re-ranks the TOP-10 every tick by mission leverage times unblockability.",
   "A 9.0 means 'good, one more pass' — the pass is the job, not the score.",
   "Independent review requires a non-author seat; a seat cannot score its own work.",
   "The lane feed signs every claim in and every receipt out with the four-line header.",
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
         "a weekly digest email, and capture happens in the digest batch."),
  distractors=[
   "The card renders his exact words with the timestamp and the source.",
   "Dictation mode transcribes the intake; the transcript lands in the contract.",
   "The feed's digest view groups units by morning, afternoon, and evening.",
   "Saved items sync across devices when the account is connected.",
   "The receiver parses the card and routes it to the right store.",
   "Playback reads the card aloud with the preferred voice.",
   "The share sheet copies a link anyone with the URL can open.",
   "Notifications batch hourly; urgent ones break through immediately.",
   "The search box finds cards by keyword across the whole library.",
   "The mini-blog auto-scheduler queues posts for the morning slot.",
   "Read receipts show when he opened the card.",
   "The tray holds drafts until they are sent or discarded.",
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
         "spends the budget, and the governor must throttle lanes when ticks run high."),
  distractors=[
   "The quota dashboard shows remaining calls with a 5-minute refresh.",
   "Rate limits return 429; the client backs off exponentially.",
   "The monthly report breaks spend down by workflow and actor.",
   "Caching the dependency layer cut install time by two-thirds.",
   "The throttle band caps dispatches when the queue holds 20-29 briefs.",
   "A quiet throttle is governance working, not a failure.",
   "The spend ledger records every check for observability.",
   "Retries with jitter avoid the thundering herd on quota reset.",
   "The free tier resets on the first of the month.",
   "The API returns the remaining quota in the response headers.",
   "A 403 on scope means the token lacks the permission, not that quota is spent.",
   "The night shift burns fewer calls because the queue drains by morning.",
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
         "hero program is members-only."),
  distractors=[
   "The hive shares lessons so every seat learns from every other seat.",
   "Bees bring honey back to the hive — valuable intelligence, compounded.",
   "The collective chain lets every mind tune in before acting.",
   "Identity is Naya Narzan; the lane label is only a dispatch slot.",
   "The mother brain is the super brain every Naya tunes into.",
   "Cold successors continue from the live plan, never from memory alone.",
   "The vision ends the waste — billions lost daily to AI producing noise.",
   "Every seat signs in with its team name so the board reads clean.",
   "The 14 questions re-derive every run; answers are never carried.",
   "Role fluidity means the work decides the role, never the seat number.",
   "The oath is spoken before any work; no work before activation.",
   "The infinite loop runs build, test, upgrade, scorecard — forever.",
  ]),
]


def build():
    docs, queries = [], []
    qn = 0
    for ti, t in enumerate(TOPICS, start=1):
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
            start = (pos * 3) % 12
            field = [pool[(start + k) % 12] for k in range(9)]
            decoy_id = None
            if is_trap:
                assert gold_key == "a", "trap must target gold_a (decoy negates it)"
                field[0] = dt
                decoy_id = dt
                # VALIDATION: decoy must be the nearest lexical neighbor of q
                ov_decoy = overlap_lex(qtext, by_id[dt]["text"])
                ov_gold = overlap_lex(qtext, by_id[gold_id]["text"])
                assert ov_decoy > ov_gold, (
                    "trap %s invalid: decoy overlap %d <= gold overlap %d"
                    % (qid, ov_decoy, ov_gold))
            queries.append({
                "qid": qid, "text": qtext, "gold": gold_id,
                "field": [gold_id] + field,
                "trap": is_trap, "decoy": decoy_id,
                "topic": t["name"],
                "split": "calibration" if qn <= 20 else "acceptance",
                "provenance": {"memory_file": t["prov"], "line": line},
            })
    assert len(queries) == 40, len(queries)
    assert sum(1 for q in queries if q["trap"]) == 8
    assert sum(1 for q in queries if q["trap"] and q["split"] == "calibration") == 4
    # every field: 10 docs, gold first, unique ids
    for q in queries:
        assert len(q["field"]) == 10 and len(set(q["field"])) == 10
        assert q["field"][0] == q["gold"]
    corpus = {"docs": docs,
              "design": "verification/semantic-arm-acceptance-gate-design-v1.md",
              "frozen_utc": "2026-10-18T03:5xZ-see-git-commit"}
    return corpus, queries


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    corpus, queries = build()
    cpath = os.path.join(HERE, "corpus_v4-semantic.json")
    qpath = os.path.join(HERE, "queries_v4.json")
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
