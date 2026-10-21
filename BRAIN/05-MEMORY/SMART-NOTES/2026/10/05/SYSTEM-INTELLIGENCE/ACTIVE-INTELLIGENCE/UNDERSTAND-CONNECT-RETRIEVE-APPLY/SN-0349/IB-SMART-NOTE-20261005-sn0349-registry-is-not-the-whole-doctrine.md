# The Registry Is Not the Whole Doctrine — Retrieval Can Only Return What Was Captured

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0349-registry-is-not-the-whole-doctrine
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5995785874 (lane-1, 2026-10-05 — "[LANE 1][MEASURED-FINDING] — retrieval coverage gap (Area 5), for the owning lane")

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A measured finding, not a theory: while building the retrieval drill bank, lane-1 queried the live Smart Note registry for repair-PR discipline — `repair PR duplicate red check class stand down` — and got back SN-022 (Human-Centered Design Intelligence), the wrong note. The correct doctrine ("one open repair per RED class" / "never open a second repair for the same class") exists — but it lives in `AGENTS.md` and board law, NOT in the Smart Note registry, so the KNOW path cannot return it. The instrument is healthy: `tools/know_measure/` baseline on pinned corpus `240db963` scored PASS 5/5 (P1 no false hits, P2 no wrong hits, P3 consumer fires, P4 p95=6ms, P5 log integrity). The machinery retrieves correctly; the corpus it searches is incomplete. **A seat asking the brain about repair-lane discipline gets a design note — the retrieval machinery is innocent; the doctrine never entered the registry.**

The durable doctrine for cold successors: **retrieval coverage is a corpus problem before it is an algorithm problem.** When a retrieval returns the wrong note, the first question is never "how do we tune ranking?" — it is "does the right doctrine exist anywhere the retriever can see?" Law-grade doctrine scattered across `AGENTS.md` lesson lines, #1354 comment threads, and working-directive files is invisible to the KNOW path no matter how good the instrument gets. The fix belongs to the KNOW restoration lane (her seam, not lane-1's): either capture standing doctrine into Smart Notes, or extend retrieval to index the standing-law sources. Until then, every claim about what "the brain knows" must be scoped to what is actually in the registry — and the finding was flagged with the measurement as the receipt, not as a complaint: instrument first, diagnosis second, owner named, seam untouched.

Why this is brain-grade: every future retrieval miss will be triaged wrong if this isn't on record. The default instinct is to retune; the evidence says look at the corpus boundary first. Months from now, a seat debugging "the brain didn't know X" must check: was X ever captured into something the KNOW path indexes? If not, that's not a retrieval failure — that's a capture gap, and it has an owner.

## 🩷 HUMAN NOTE

Shawn — a seat measured a real gap this morning and it's a good one. When someone asked the brain "what's our doctrine on duplicate repair PRs?", it returned a design note (SN-022) — the wrong answer. The right doctrine exists ("one open repair per red class"), but it lives in AGENTS.md and the board threads, not in the Smart Note registry, so the lookup machinery never had a chance. The machinery itself is fine — its health battery passed 5/5. The problem is the corpus: what the retriever can see. The finding went to the lane that owns the retrieval seam with the measurement attached, not as blame. Durable lesson: when the brain "doesn't know" something, check whether the knowledge was ever put where the brain can look — before tuning anything.

## 🟣 CHILD NOTE

Imagine asking the librarian for the rule book, and the librarian gives you a coloring book. The librarian isn't bad at her job — the rule book was never put on the library shelves; it's taped to the fridge at home. That's what happened: the right rule exists, but it lives somewhere the brain's search can't see. The fix isn't a better librarian — it's putting the rule book on the shelf (or teaching the librarian to check the fridge too).

## 👵 GRANDMA NOTE

A good filing cabinet can't retrieve a letter that was never filed. The team found that an important rule lived in the team's handbook and conversation threads but had never been put into the shared memory where the lookup tools search — so of course the lookup returned the wrong thing. The instruments are fine; the gap is in what was filed. Before fixing the machinery, make sure the answer was actually filed where the machinery can find it.

## 💜 NAYA NOTE

For any future seat triaging "the brain didn't know X": the triage order is (1) is X captured into anything the KNOW path indexes? (2) only then: is the retrieval ranking wrong? Check the corpus boundary before touching the algorithm. The know_measure battery (`tools/know_measure/` on the pinned corpus) is the instrument for distinguishing healthy-machinery-wrong-answer (corpus gap) from sick-machinery (instrument failure) — P1/P2 guard the false-hit surface, P5 guards log integrity. Standing doctrine in AGENTS.md lessons, #1354 threads, and working directives is invisible to retrieval until captured as a Smart Note or indexed as a standing-law source. When you find a corpus gap, flag it with the measurement as the receipt, name the owning lane, and do not touch another lane's seam.

## 🖥️ MACHINE NOTE

{"sn": "SN-0349", "title": "The Registry Is Not the Whole Doctrine — Retrieval Can Only Return What Was Captured", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ACTIVE-INTELLIGENCE", "UNDERSTAND-CONNECT-RETRIEVE-APPLY"], "cousins": ["SN-022", "SN-0346", "SN-0335"], "evidence": {"board": "#1354 5995785874 (lane-1, 2026-10-05 — '[LANE 1][MEASURED-FINDING] — retrieval coverage gap (Area 5), for the owning lane')", "query": "'repair PR duplicate red check class stand down' -> returned SN-022 (Human-Centered Design Intelligence), wrong note", "correct_doctrine": "'one open repair per RED class' / 'never open a second repair for the same class' — lives in AGENTS.md + board law, NOT in the Smart Note registry", "instrument": "tools/know_measure/ baseline on pinned corpus 240db963: PASS 5/5 (P1 no false hits, P2 no wrong hits, P3 consumer fires, P4 p95=6ms, P5 log integrity)", "owner": "Coda 4 owns the KNOW restoration repair and the persistence/retrieval seam — flagged to her with the measurement as receipt"}, "rule": "retrieval coverage is a corpus problem before it is an algorithm problem: when retrieval returns the wrong note, first ask whether the right doctrine exists anywhere the retriever can see; law-grade doctrine in AGENTS.md and comment threads is invisible to the KNOW path until captured into the registry"}
