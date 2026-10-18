#!/usr/bin/env python3
"""build_corpus_v5.py — FREEZE the v5 semantic corpus (gap-0410, Lane 5 Heir).

Parent: hidden_files/twelve-lane-receipts/t0722-lane5.md (the pre-mortem).
Brief: brief-gap-lane-scorer-20261018-0410-lane5.md.

The v4 corpus failed its own gate: distractors carried topic vocabulary but NOT
the queries' distinctive stems, so stemmed lexical overlap ranked golds first
trivially (calibration: lexical 0.85 > draft P25 0.60 -> F7 FIRED, BROKEN).

THE FIXED DISTRACTOR RULE (this file's whole point): every distractor MUST
reuse EACH of its query's distinctive stems (non-stopword v3 stems of the
query) while staying semantically irrelevant to the query. Enforced by a
MECHANICAL check in build(): the distractor's stem set must be a superset of
the query's distinctive-stem set. Freeze fails loud on any miss.

Kept from v4 (per the pre-mortem): the same 40 real query phrasings (same
provenance), the same golds (lexically close to queries), the same 8 trap
queries with the same decoys and the same nearest-lexical-neighbor validation
(3/4 fooled the semantic arm — the right difficulty), K=9 FIXED, the 20/20
calibration/acceptance split, 4 traps per split.

Changed from v4: distractors are PER-QUERY pools (9 each, 40x9=360) instead of
per-topic pools of 12 — a topic pool cannot carry five different queries'
distinctive-stem sets. NEW freeze (never a re-seal of v4).

Edge case (documented, not hidden): q21 "Is that done?" has an EMPTY
distinctive-stem set (all tokens are stopwords) — the superset check is
vacuously true there. One query in forty; the receipt names it.
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

def distinctive_stems(qtext):
    """The query's distinctive stems: non-stopword v3 stems. The fixed
    distractor rule is defined against exactly this set."""
    return sorted(set(v3_toks(qtext)))
# ---- end v3 replication ----

# TOPICS: (query_text, provenance_line, gold_key, is_trap, [9 distractors]).
# Every distractor below was authored against the query's distinctive-stem set
# (verified mechanically in build()); all stay semantically irrelevant to the
# query's gold. Golds, decoys, queries, provenance: unchanged from v4.
TOPICS = [
 dict(name="cloudflare-hosting-deploy", prov="2026-10-17.md",
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
  queries=[
   ("What did Shawn decide about hosting?", 1244, "a", False, [  # stems: decide host shawn
    "Shawn will decide the offsite host city late; the venue booking is still open.",
    "The host wants Shawn to decide about the table; he will decide after the team arrives.",
    "Shawn never got to decide which host handles the podcast feed; the host slot is still open.",
    "Every host city bid needs Shawn to decide before the host committee votes.",
    "Shawn will decide to host the demo at noon; the team will decide the agenda.",
    "The dinner host asked Shawn to decide about the seating chart.",
    "Shawn will decide the host gift after the keynote; the host thanked the crew.",
    "No host was chosen until Shawn could decide after two reviews.",
    "Shawn's assistant asked him to decide the host order for the calls; Shawn approved it.",
   ]),
   ("Where is the Hub going to be hosted?", 1244, "a", True, [  # stems: going host hub
    "The food hub is going to the host kitchen; the going rate for catering rose.",
    "That hub is going offline for maintenance; the host confirmed the window.",
    "The transit hub is going through renovations; the host city apologized.",
    "Going forward the hub model changes; the host venue stays the same.",
    "The hub is going dark at midnight; the host will post an update.",
    "A new hub is going up downtown; the host neighborhood welcomed it.",
    "The bike hub going rate doubled; the host shop blamed demand.",
    "Going by the map, the hub sits near the host stand at the fair.",
    "The hub is going strong this quarter; the host sponsor renewed.",
   ]),
   ("What are you saying that we need is a new GitHub secret? You want to be specific about which one?", 3590, "b", False, [  # stems: github need new one say secret specif want
    "I say we need one new secret for the GitHub org's billing; I want the specific approver named.",
    "You say the new GitHub action needs one secret; I want the specific step that uses it.",
    "They want one new secret, saying the GitHub mirror needs it; I want the specific rotation date.",
    "I say the staging need is one new thing: the GitHub deploy key isn't a secret you want rotated; name the specific one.",
    "New hires say the GitHub secret they need is the wifi password; I want one specific answer.",
    "You want me to say the new GitHub codespace needs one secret? I need the specific docs page.",
    "I say the staging need is one new GitHub secret; I want the specific environment it unlocks.",
    "They say one specific secret is what the new GitHub app needs; I just want the docs link.",
    "Want my take? They say the new GitHub secret is needed for one specific bot; I need the ticket.",
   ]),
   ("What is the deploy shape for showing Shawn new pages?", 3803, "b", False, [  # stems: deploy new pag shape shawn show
    "The new deploy dashboard shows pages in shape; Shawn wants the bar chart shape changed.",
    "Shawn showed the team the new deploy runbook; the shape guidelines for pages are inside.",
    "The deploy notes show three new pages; Shawn changed the shape of the rollout plan.",
    "Show Shawn the new staging deploy; the shape of pages renders after the deploy.",
    "The new deploy checklist shows the page count to Shawn; the shape field is optional for pages.",
    "The deploy bot shows new pages previews to Shawn; the shape picker is broken.",
    "New pages show after each deploy; Shawn asked why the shape changed.",
    "Shawn wants the deploy to show new pages in the shape of a sitemap.",
    "The shape of the new deploy email shows Shawn the pages stats.",
   ]),
   ("If the first deploy fails on permissions, what do we swap?", 3799, "b", False, [  # stems: deploy fail first permiss swap
    "If the first deploy fails, swap the permissions file before the deploy retries.",
    "The first deploy failed on permissions; we swap the deploy key and retry.",
    "Swap the first failed deploy's permissions scope; the deploy log shows why.",
    "When a deploy fails permissions first, swap the service account.",
    "The permissions check failed the first deploy; swap the token, not the deploy.",
    "First, swap the deploy permissions; if it still fails, escalate.",
    "A failed permissions deploy means swap the first approver.",
    "Swap the deploy branch if the first permissions gate fails.",
    "If permissions fail the deploy first, swap the runner image.",
   ]),
  ]),
 dict(name="supabase-backend", prov="2026-10-17.md",
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
  queries=[
   ("I thought backend is on Superbase", 1240, "a", False, [  # stems: backend superbase thought
    "I thought the backend docs were on Superbase; the Superbase docs site moved.",
    "She thought the backend team used Superbase for the demo; the Superbase trial expired.",
    "I thought Superbase was the backend for the blog; the backend turned out to be static.",
    "They thought the backend migration to Superbase finished; the Superbase project is a sandbox.",
    "I thought the Superbase backend supported that query; the backend logs say otherwise.",
    "He thought Superbase hosted the backend assets; the backend assets are on the CDN.",
    "I thought the backend status page was Superbase; Superbase only hosts the docs.",
    "We thought the backend would leave Superbase; the Superbase bill was fine.",
    "I thought Superbase was just the backend cache; the backend cache is Redis.",
   ]),
   ("Where do Smart Note rows land when the flow completes?", 2908, "a", True, [  # stems: complet flow land note row smart
    "Smart Note rows land in the flow log when the import completes.",
    "When the flow completes, Smart Note rows land in the CSV the smart exporter wrote.",
    "The smart flow lands each note row after the flow completes its pass.",
    "Smart rows land in the flow dead-letter queue; note it after the flow completes.",
    "When the ETL flow completes, the smart note rows land in the warehouse.",
    "The flow completes and smart note rows land in the audit table.",
    "Smart Note rows land where the flow config says after it completes.",
    "Each smart note row lands in the flow cache until the flow completes.",
    "The flow handler lands smart note rows in the outbox after the flow completes.",
   ]),
   ("What does 'alive' mean for the Hub?", 2908, "b", False, [  # stems: 'alive' hub mean
    "The dashboard prints 'alive' next to the Hub, which I mean is just the ping check.",
    "They call the Hub 'alive' to mean the deploy finished, not that data flows.",
    "'Alive' on the Hub status page means the container runs; I mean the narrow sense.",
    "The 'alive' badge on the hub dashboard means CI is green, if you mean the badge literally.",
    "I mean the Hub probe says 'alive' every 30 seconds; that's the liveness check.",
    "'Alive' means the Hub process didn't crash — I mean that in the ops sense.",
    "The Hub endpoint returns 'alive' to mean the port is open.",
    "When the Hub says 'alive', I mean the homepage renders, nothing more.",
    "The 'alive' string in the Hub logs means the scheduler ticked.",
   ]),
   ("What is the number-one blocker to the Hub being alive?", 1244, "b", False, [  # stems: alive block hub numb one
    "The number one blocker is alive in the tracker: the Hub auth outage is the blocker.",
    "One blocker kept the Hub from going alive: the number on the status page was wrong.",
    "The alive check on the hub has one blocker: the number of retries is capped.",
    "Blocker number one: the Hub stays alive only if the cache warms.",
    "One alive Hub had a blocker: the port number changed.",
    "The number-one Hub blocker is alive and assigned: the DNS cutover.",
    "One blocker stops the hub: the alive probe's number format.",
    "Hub blocker one: the alive signal's number range is misconfigured.",
    "The alive dashboard lists one Hub blocker by number.",
   ]),
   ("Are the Supabase tables live with real rows yet?", 1240, "a", False, [  # stems: live real row supabase tabl yet
    "The Supabase tables for the demo are live with real rows, yet the demo tables aren't the app tables.",
    "The analytics Supabase tables went live with real rows, yet nobody queries the analytics tables.",
    "Yet more Supabase tables went live; the real rows are synthetic.",
    "The Supabase tables are live, yet the real rows belong to the staging project.",
    "Real-time rows hit the Supabase tables yet the live view lags.",
    "The Supabase tables aren't live yet; the real rows wait in the CSV.",
    "Yet the Supabase tables show live data; the real rows are from the seed.",
    "Live Supabase tables with real rows exist, yet they're all in the archived project.",
    "The Supabase tables went live yesterday, yet the real rows are still validating.",
   ]),
  ]),
 dict(name="board-feed", prov="2026-10-17.md",
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
  queries=[
   ("Why aren't we on a new feed?", 79, "a", False, [  # stems: aren't feed new
    "We aren't on a new feed because the old feed still works; the new feed launches next quarter.",
    "They aren't moving to a new feed; the feed reader handles the old format.",
    "We aren't on the new feed yet; the feed migration is scheduled.",
    "The team aren't fans of the new feed; the old feed stays.",
    "We aren't testing the new feed; the feed contract is frozen.",
    "Aren't we on a new feed already? The feed URL didn't change.",
    "We aren't on a new feed plan; the feed quota renewed.",
    "The editors aren't on the new feed workflow; the feed still publishes.",
    "We aren't on a new feed cycle; the feed cadence is weekly.",
   ]),
   ("Which issue is the live board?", 79, "a", True, [  # stems: board issue live
    "The live board issue is #2641; the board moved there last month.",
    "The live board issue number is in the board's pinned comment.",
    "The live board issue triages bugs; the issue queue is separate.",
    "No live board issue exists; the board lives in the wiki.",
    "The issue tracker hosts the live board under the board project.",
    "The live board is an issue labeled 'board-live'.",
    "That issue is the live board's archive; the board moved.",
    "The board issue went live after the migration.",
    "Every board has a live issue; the issue list shows it.",
   ]),
   ("What does every board post open with?", 1241, "b", False, [  # stems: board open post
    "Every board post opens with the date; the board style guide says so.",
    "The board post opens with a summary; every post follows the template.",
    "Open every board post with the ticket link; the post body follows.",
    "Board posts open with the author's name; every post is signed.",
    "What does every board post open with? The post header answers it.",
    "The open board posts start with the status line.",
    "Every post on the board opens with a greeting.",
    "The post opens the board meeting notes; every attendee posts.",
    "Open the board, post the update; every post needs a label.",
   ]),
   ("Do unsigned board posts count as claims?", 1241, "b", False, [  # stems: board claim count post unsign
    "Unsigned board posts count as claims after two approvals.",
    "Do unsigned board posts count? The board counts only signed claims.",
    "The claim count excludes unsigned board posts.",
    "Unsigned posts on the board don't count toward the claim total.",
    "Every unsigned board post counts as a draft claim.",
    "The board claim policy: unsigned posts count if witnessed.",
    "Count the unsigned board posts separately from claims.",
    "Unsigned board posts count toward the discussion total, not claims.",
    "Do unsigned posts count? The board claim FAQ covers signed posts.",
   ]),
   ("Which issue numbers are capped archives we must never post to?", 79, "a", False, [  # stems: archiv capp issue nev numb post
    "The capped archives are never listed by issue number; never post the numbers.",
    "Which issue numbers are capped? The archives post never lists every capped number.",
    "Never post to capped archives; the issue numbers are in the archive index.",
    "The archives capped the issue at 2,500; never post after the cap number.",
    "Issue numbers for capped archives: post never, archive always.",
    "The capped archives issue numbers are never published; posting is disabled.",
    "Never post issue numbers in the archives; the capped list is private.",
    "Archives get capped by number; never post to a capped issue.",
    "The post never names the issue numbers of the capped archives.",
   ]),
  ]),
 dict(name="design-laws", prov="2026-10-17.md",
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
  queries=[
   ("Does the design contract say gold accents for headings?", 3241, "a", False, [  # stems: accent contract design gold heading say
    "The vendor contract says gold accents cost extra; the design headings stayed black.",
    "Say the design headings use gold accents per the print contract.",
    "The contract design appendix says headings may use gold accents in slides.",
    "Gold accents say 'premium' in the design contract headings examples.",
    "The headings style guide says gold accents are for the design system's contract logo.",
    "I say the contract covers gold headings accents for the invoice design.",
    "The design contract says the gold accent wall needs a headings sign.",
    "Headings say it best: the design contract gold accents are for awards.",
    "The contract says design headings in gold accents are a print-shop option.",
   ]),
   ("What are the official design laws?", 3241, "a", True, [  # stems: design law offici
    "The official design laws are posted; the design team enforces the law.",
    "What are the official laws? The design law doc is versioned.",
    "The design laws became official after the law review.",
    "Official design law: the design system is law.",
    "The laws of official design are unwritten; the design law is custom.",
    "Three official design laws exist; the fourth law is pending.",
    "The official design laws cover color law only.",
    "The official design law starts with the grid law.",
    "The official laws say design is law.",
   ]),
   ("Can I use the dark-with-gold style on web pages?", 3241, "b", False, [  # stems: dark gold pag style use web
    "You can use the dark-with-gold style on web pages for the holiday theme.",
    "The dark-with-gold web style is what the pages use at night.",
    "Use the dark style on web pages; the gold web accents are optional.",
    "Web pages can use any style; the dark-with-gold pages are legacy.",
    "I use the dark-with-gold style on my web pages draft.",
    "The style guide lets web pages use dark-with-gold for modals.",
    "Dark web pages use the gold style for the pages' footer.",
    "Can web pages use it? The style tile shows dark-with-gold pages.",
    "The web team uses dark-with-gold style on internal pages.",
   ]),
   ("Why can't we make page creation that easy?", 3189, "b", False, [  # stems: can't crea easy make page
    "I can't make the page creation easy on dial-up; the easy win is image compression.",
    "You can't make page creation easy without the easy-mode template.",
    "We can't make the creation page easy to find; the easy link is buried.",
    "Can't the page creation be easy? Make the easy path the default.",
    "They can't make page creation easy for print; the easy export is PDF.",
    "I can't make it easy; page creation needs the easy checklist.",
    "Make page creation easy? You can't without the creation wizard.",
    "The easy page tool can't make creation easy at scale.",
    "Easy creation pages can't make themselves, but the page tool makes one manually.",
   ]),
   ("What color may headings use?", 3241, "a", False, [  # stems: color heading use
    "The headings color you use on slides is navy; the color system lets you use any headings tint in decks.",
    "What color may headings use? The heading color picker decides.",
    "Headings may use any color the brand book allows.",
    "The color rule: headings use black; body may use color.",
    "Use color sparingly; headings may use the accent color.",
    "Headings use the color you assign; the default heading color is gray.",
    "What color? Headings may use color in print.",
    "The heading color policy: use dark headings on light color blocks.",
    "May headings use color? The use-case doc says sometimes.",
   ]),
  ]),
 dict(name="scorecard-aaa", prov="2026-10-17.md",
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
  queries=[
   ("Is that done?", 3514, "a", False, [  # stems: (empty) — vacuous check, documented
    "The scorecard history log keeps every score with its evidence link.",
    "Three passes is the floor; a fourth pass happens whenever it still doesn't feel right.",
    "The merge queue processes branches in order; a red check blocks the batch.",
    "The 14-question attunement cron runs every 3 hours and diffs answer hashes.",
    "A receipt without evidence links fails the merge-receipt watch automatically.",
    "The rotation file tracks which ticks are queued, in flight, and closed.",
    "The gate scans PR comments for the scorecard pin before flipping green.",
    "Night-shift runs keep the board warm while the day team sleeps.",
    "The dispatcher re-ranks the TOP-10 every tick by mission leverage times unblockability.",
   ]),
   ("You gotta complete the work — what does that mean?", 1244, "a", True, [  # stems: complet gotta mean work
    "You gotta complete the work to mean it; the work means the checklist.",
    "What does gotta complete the work mean? The work order means overtime.",
    "Gotta love the work; complete it and the mean review passes.",
    "You gotta mean the work you complete; work means effort.",
    "Complete the work, gotta say; the meaning is the work log.",
    "The work gotta be complete; I mean the paperwork.",
    "You gotta work to complete the meaning.",
    "Mean what you complete; gotta finish the work.",
    "The gotta-complete work order means the shift.",
   ]),
   ("What is the AAA bar?", 1244, "b", False, [  # stems: aaa bar
    "The AAA bar is set at 9.0 for routine work.",
    "What is the AAA bar? The bar exam for designers.",
    "The AAA bar serves drinks after the launch; the bar tab is on us.",
    "AAA bar means the highest bar in the building.",
    "The bar for AAA is a triple-A battery.",
    "Raise the AAA bar every quarter; the bar moves.",
    "The AAA bar is where the team celebrates; the bar is downtown.",
    "What bar? The AAA bar is a sandwich shop.",
    "The AAA bar refers to the bar chart's AAA rating.",
   ]),
   ("Why shouldn't I show him work that's coming?", 1244, "b", False, [  # stems: com shouldn't show that' work
    "You shouldn't show work that's coming through the commit queue until the work passes — that's the policy.",
    "I shouldn't show the work that's coming in the com-ments thread; that's the draft rule.",
    "Shouldn't the coming work show itself? That's the demo rule for work.",
    "You shouldn't show work that's coming; that work's embargo says that's final.",
    "We shouldn't show the coming work lineup; that's what the work calendar is for.",
    "Shouldn't I show work that's coming soon? That's how the work gets feedback.",
    "The coming work shouldn't show up; that's the work freeze.",
    "You shouldn't show unfinished work that's coming; that's the com-ing-soon rule.",
    "That's why you shouldn't show work that's coming early; the work isn't ready.",
   ]),
   ("Who merges, and what makes a merge happen?", 1244, "b", False, [  # stems: happen mak merg merge
    "Who merges the merge queue, and what makes a merge happen on Fridays?",
    "The merger merges every merge; what makes it happen is the green check.",
    "Who merges? The merge bot merges; a merge happens when two approve, which makes it official.",
    "Merges happen after the merge window; what makes the merge happen is the captain.",
    "She merges the merge request; what makes a merge happen is consensus.",
    "Who merges the merges? The merge train makes it happen.",
    "The merge happens when she merges; what makes or breaks it is the merge check.",
    "The merges log makes the merge history grow; what happens is the merge.",
    "Who merges? Whoever the merge rota names makes a merge happen at noon.",
   ]),
  ]),
 dict(name="smart-note-flow", prov="2026-10-17.md",
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
  queries=[
   ("What is the Smart Note flow?", 2908, "a", False, [  # stems: flow note smart
    "The Smart Note flow chart is on the wall; the smart flow starts with note triage.",
    "What is the Smart Note flow? The flow diagram shows the note path.",
    "The smart flow handles notes; the note flow is smart.",
    "Smart notes flow through the flow builder; the note router is smart.",
    "The flow called Smart Note processes the note queue.",
    "Note the smart flow's name; the flow notes are smart.",
    "The Smart Note flow runs nightly; the smart scheduler owns the flow.",
    "Flow state: the smart note flow is paused.",
    "The note flow's smart filter flags the flow.",
   ]),
   ("Is the sender switched on?", 1244, "a", True, [  # stems: send switch
    "Is the sender switched on? The switch panel shows the sender row.",
    "The switch for the sender is off; send tests are pending.",
    "Send the switch state; the sender switch is manual.",
    "The sender switch is stuck; the send queue waits.",
    "Switch the sender off before you send the batch.",
    "The send log shows the switch toggled twice.",
    "Which switch? The sender's switch sends the signal.",
    "The sender switch label says 'send'.",
    "Send a test; the switch answers for the sender.",
   ]),
   ("What is ask-world?", 1244, "b", False, [  # stems: ask world
    "Ask the world anything; the world answers.",
    "What is ask-world? The ask-world docs are thin.",
    "The world asks back; ask-world listens.",
    "Ask-world asks the world for the weather.",
    "The ask-world button queries the world index.",
    "World news: ask-world summarized it.",
    "Ask the world; the world asked first.",
    "The world is asking; ask-world triages.",
    "Ask-world: ask the world, get the world.",
   ]),
   ("How do lessons become behavior?", 1244, "b", False, [  # stems: become behavior lesson
    "Lessons become behavior through repetition; the behavior lesson sticks.",
    "How do lessons become behavior? The lesson plan says practice.",
    "Behavior lessons become habits; the lesson becomes reflex.",
    "The lesson on behavior will become the behavior lesson.",
    "Lessons become behavior when the behavior is rewarded.",
    "Become the lesson; the behavior follows the lesson.",
    "The behavior change lesson will become the new behavior.",
    "Lessons about behavior become behavior lessons.",
    "How does a lesson become behavior? The behaviorist's lesson.",
   ]),
   ("What does the feed show?", 1244, "b", False, [  # stems: feed show
    "The feed shows the latest posts; the show starts at noon.",
    "What does the feed show? The feed shows the show.",
    "The show's feed shows backstage clips.",
    "Feed the show notes; the show feeds the feed.",
    "The feed shows ads; the show must go on.",
    "Show me the feed; the feed shows everything.",
    "The feed shows the show's schedule.",
    "What show? The feed shows the feed.",
    "The feed's show page shows the feed.",
   ]),
  ]),
 dict(name="budget-law", prov="2026-10-16.md",
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
  queries=[
   ("What is the 2,500/month law about?", 1244, "a", False, [  # stems: law month
    "The 2,500/month law caps the law firm's retainer; the month resets.",
    "What is the 2,500/month law? The month the law passed.",
    "The law about 2,500 a month is the parking law.",
    "2,500 a month: the law of supply.",
    "The month-end law review covers the 2,500 rule.",
    "That law costs 2,500 per month in fines.",
    "The 2,500/month law is Moore's law for budgets.",
    "Which law? The 2,500/month gym membership law.",
    "The law sets 2,500 as the monthly max.",
   ]),
   ("Why did the budget governor throttle on tool-call and tick counts?", 1244, "a", True, [  # stems: budget call count governor throttle tick tool
    "The budget governor will throttle the tool-call budget; the tick count hit the tool limit.",
    "Why did the governor throttle? The budget tool counts every tick and call.",
    "The tool budget tick count made the governor throttle the call rate.",
    "Throttle the governor budget tool; count the ticks per call.",
    "The governor counts tool calls per tick; the budget throttle engaged.",
    "Budget tools tick; the governor will throttle the call count.",
    "The tick-tock budget governor will throttle tool-call counting.",
    "Count the ticks: the budget governor throttle counts tool calls.",
    "The governor budget throttle counts ticks, calls, and tools.",
   ]),
   ("What was burning GitHub Actions runs?", 1244, "b", False, [  # stems: action burn github run
    "The GitHub Actions runs were burning budget; the action runner ran hot.",
    "What was burning? The GitHub Actions run burned the midnight oil.",
    "Burning through GitHub Actions runs, the action cache ran cold.",
    "The action that burns runs on GitHub is the nightly run.",
    "GitHub runs the action; the burn rate runs high.",
    "The burning question: which GitHub Action runs burn fastest?",
    "Runs were burning on GitHub Actions; the action log ran long.",
    "The GitHub action burns through run minutes.",
    "What burns? GitHub Actions runs burn when the action runs.",
   ]),
   ("Do agent tool calls count against the budget?", 1244, "b", False, [  # stems: against agent budget call count tool
    "Do agent tool calls count against the budget? The budget counts the agent tool inventory.",
    "Against which budget do agent tool calls count? The tool ledger.",
    "Would agent tool calls count against the budget? The tool policy is unclear.",
    "If agent tool calls counted against the budget, the tool bill would spike.",
    "Do they count? Agent tool calls against the budget: the tool FAQ.",
    "The budget tool counts agent calls; against what, the agent asks.",
    "Against the budget? The agent tool-call count lives in the tool report.",
    "Count them against the budget: agent tool calls, budget lines, the tool total.",
    "The agent budget counts tools; calls against it are tracked.",
   ]),
   ("What is the real burn rate?", 1244, "b", False, [  # stems: burn rate real
    "The real burn rate for the grill is 500 degrees.",
    "What is the real burn rate? The burn unit converts the rate.",
    "The burn rate is real; the rate burned.",
    "Real burn rates vary; the burn rate is nominal.",
    "The real rate of burn matters.",
    "Burn the real plans; the rate is fixed.",
    "The burn rate real name is throughput.",
    "What rate? The real burn rate for candles.",
    "The real burn rate tripled overnight.",
   ]),
  ]),
 dict(name="nayanet-team", prov="2026-10-17.md",
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
  queries=[
   ("What is NayaNET?", 1244, "a", False, [  # stems: nayanet
    "NayaNET is the wifi name; the NayaNET password is on the fridge.",
    "What is NayaNET? NayaNET is a crossword answer.",
    "The NayaNET outage lasted an hour.",
    "NayaNET's homepage lists the NayaNET team.",
    "Is NayaNET down? The NayaNET status is green.",
    "NayaNET v2 launches soon.",
    "The NayaNET logo is a bee.",
    "NayaNET stands for something.",
    "Ask NayaNET; NayaNET knows.",
   ]),
   ("Who is Naya Narzan and what is the new hero?", 1244, "a", True, [  # stems: hero narzan naya new
    "Naya Narzan is the new hero of the Naya fan club.",
    "Who is Naya Narzan? The new Naya hero movie.",
    "The new hero is Naya; Narzan is the sequel.",
    "Naya Narzan has a new hero costume; the Narzan suit is gold.",
    "The hero Naya Narzan saves the new city.",
    "New hero alert: Naya Narzan joins the roster.",
    "Naya is the hero; Narzan is the new name.",
    "The new Naya hero is Narzan.",
    "Heroes: Naya, Narzan, and the new kid.",
   ]),
   ("What are the three pillars?", 1244, "b", False, [  # stems: pillar three
    "The three pillars are the three legs of the stool.",
    "What are the three pillars? The pillar report lists three.",
    "Three pillars hold the roof; the pillar design is Roman.",
    "The pillar's three pillars are concrete.",
    "Three pillars of the community: the pillar fund.",
    "The three pillars support the bridge.",
    "Pillar three of three pillars is the last.",
    "The three pillars are load-bearing.",
    "Three pillars, three pillars, three pillars.",
   ]),
   ("What are the four instruments?", 1244, "b", False, [  # stems: four instrument
    "The four instruments are strings, brass, woodwinds, percussion.",
    "What are the four instruments? The instrument case holds four.",
    "Four instruments play the quartet.",
    "The instrument panel has four instruments.",
    "Four instruments tune the orchestra.",
    "The four instruments are in the band.",
    "Instrument four of the four instruments.",
    "Four instruments, one song.",
    "The four instruments gather dust.",
   ]),
   ("Why am I having to give permission? All learning is permissioned.", 247, "b", False, [  # stems: am give learn permis permission
    "Why am I to give permission? All learning apps are permissioned, so give the app your OK.",
    "I am asked to give permission; the learning platform is permissioned.",
    "Give permission and I am in; the learn portal is permissioned.",
    "Am I the one to give permission? The learning system is permissioned regardless.",
    "To give permission, I am told, the learning lab is permissioned.",
    "I am here to give the permission slip; learn sites are permissioned.",
    "Give me a reason I am permissioned; the learning permission give-away is on.",
    "I am told to give permission for the learn track; it's permissioned.",
    "Permission to learn? I am the one to give permission; the course is permissioned.",
   ]),
  ]),
]


def build():
    docs, queries = [], []
    qn = 0
    for ti, t in enumerate(TOPICS, start=1):
        ga = "d%02da" % ti
        gb = "d%02db" % ti
        dt = "d%02dt" % ti
        docs.append({"id": ga, "text": t["gold_a"], "role": "gold",
                     "topic": t["name"]})
        docs.append({"id": gb, "text": t["gold_b"], "role": "gold",
                     "topic": t["name"]})
        docs.append({"id": dt, "text": t["decoy"], "role": "decoy",
                     "topic": t["name"]})
        by_id = {d["id"]: d for d in docs}
        for pos, (qtext, line, gold_key, is_trap, distractors) in enumerate(t["queries"]):
            qn += 1
            qid = "q%02d" % qn
            gold_id = ga if gold_key == "a" else gb
            assert len(distractors) == 9, "query %s: need 9 distractors, have %d" % (qid, len(distractors))
            # THE FIXED DISTRACTOR RULE — mechanical, no judgment:
            # every distractor's stem set must be a SUPERSET of the query's
            # distinctive-stem set.
            qstems = set(distinctive_stems(qtext))
            field_ids = []
            for di, dtext in enumerate(distractors, start=1):
                did = "d%02d-%02d-%d" % (ti, pos + 1, di)
                dstems = set(v3_toks(dtext))
                missing = qstems - dstems
                assert not missing, (
                    "FIXED-RULE VIOLATION %s distractor %d: missing query stems %s\n  q=%r\n  d=%r"
                    % (qid, di, sorted(missing), qtext, dtext))
                docs.append({"id": did, "text": dtext, "role": "distractor",
                             "topic": t["name"], "query": qid})
                field_ids.append(did)
            decoy_id = None
            if is_trap:
                assert gold_key == "a", "trap must target gold_a (decoy negates it)"
                field_ids[0] = dt  # decoy REPLACES distractor slot 0
                decoy_id = dt
                # TRAP VALIDATION (kept from v4): decoy must be the nearest
                # lexical neighbor of the query — overlap strictly > gold's.
                ov_decoy = overlap_lex(qtext, by_id[dt]["text"])
                ov_gold = overlap_lex(qtext, by_id[gold_id]["text"])
                assert ov_decoy > ov_gold, (
                    "trap %s invalid: decoy overlap %d <= gold overlap %d"
                    % (qid, ov_decoy, ov_gold))
            queries.append({
                "qid": qid, "text": qtext, "gold": gold_id,
                "field": [gold_id] + field_ids,
                "trap": is_trap, "decoy": decoy_id,
                "topic": t["name"],
                "split": "calibration" if qn <= 20 else "acceptance",
                "provenance": {"memory_file": t["prov"], "line": line},
            })
    assert len(queries) == 40, len(queries)
    assert len(docs) == 8 * 3 + 40 * 9, len(docs)  # 24 golds/decoys + 360 distractors
    assert sum(1 for q in queries if q["trap"]) == 8
    assert sum(1 for q in queries if q["trap"] and q["split"] == "calibration") == 4
    for q in queries:
        assert len(q["field"]) == 10 and len(set(q["field"])) == 10
        assert q["field"][0] == q["gold"]
    corpus = {"docs": docs,
              "design": "verification/semantic-arm-acceptance-gate-design-v1.md",
              "distractor_rule": "v5-fixed: every distractor reuses each query's distinctive stems (mechanical superset check in build_corpus_v5.py)",
              "frozen_utc": "2026-10-18T04:3xZ-see-git-commit"}
    return corpus, queries


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    corpus, queries = build()
    cpath = os.path.join(HERE, "corpus_v5-semantic.json")
    qpath = os.path.join(HERE, "queries_v5.json")
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
    print("vacuous-stem queries:", [q["qid"] for q in queries
                                    if not distinctive_stems(q["text"])])


if __name__ == "__main__":
    main()
