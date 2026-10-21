# The Ultimate Decision Machine — Complete Spec v1

**Author:** Naya 5, from Shawn's blueprint (2026-10-12)
**Status:** SPECIFICATION — not yet built
**Audience:** Nayas, machines, and humans. All three must understand it.

---

## Part 1: The Problem (Human Words)

Every decision tool ever built fails at the same place: it asks the human to score the options.

"Rate mission value 1-10. Rate risk 1-10. Rate urgency 1-10."

That's not math. That's opinion wearing a number's clothes. Opinions don't compound — they decay. The person who typed "9" forgets why. The next person types "7" for the same thing. Nothing learns. Nothing improves.

The ultimate machine flips it: **humans never type a number.** You say what you want in words. The machine reads reality, derives the scores from evidence, runs the math, and tells you the answer in plain words.

---

## Part 2: The Five Layers (Architecture)

### Layer 1 — The World Model
**What it is:** The machine's always-on, always-warm picture of reality.

**What it tracks:**
- Open PRs: number, title, CI status, scorecards, mergeability, age
- Lane states: which lanes are free, who's working, on what
- The ledger: what's proven, what's pending
- Mission state: current priorities, parked items, blockers
- Standing laws: what's allowed, what's protected, what gates apply
- Live tip: the current truth of the codebase

**How it stays fresh:**
- Incremental updates, never rebuilt from scratch
- Each data source has a freshness timestamp
- Stale data is marked STALE with its age — never silently used
- Unavailable data is marked UNKNOWN — never filled with guesses
- API calls are surgical: check "did it change?" before fetching

**The rule:** The world model IS the team's reality. If it's wrong, every decision built on it is wrong. Freshness is the feature. This is the hardest engineering in the system.

### Layer 2 — Intent
**What it is:** Understanding what the human (or machine) wants, from words.

**Input examples:**
- "What's the most intelligent thing to do next?"
- "Should this merge?"
- "Which of these three designs?"
- "What's blocking the team right now?"

**What it produces:**
- **Objective:** What are we trying to achieve? (parsed from the words)
- **Constraints:** What can't we do? (from the standing laws + the situation)
- **Decision weight:** How much does this matter? (automatic — the Wisdom Spending Principle)
  - Reversible + low stakes → five-minute decision → fast path
  - Irreversible or high stakes → foundational → full analysis + human review flag

**The rule:** The machine never asks "how important is this?" It reads the situation and knows.

### Layer 3 — Options from Reality
**What it is:** The set of things that could actually be done right now.

**The key move:** The machine does NOT ask "what are the options?" It looks at the world model:
- Open PRs that could merge → each one is an option
- Lanes with open work → each work item is an option
- Blocked items whose blockers just cleared → newly available options
- Parked items that became relevant → resurfaced options

**The human can add:** "What about X?" — the machine scores it too. But the default set is mined from reality, not invented from memory.

**The rule:** Options are what's actually available, not what someone remembered to list. This eliminates the biggest source of bad decisions: not considering the right option.

### Layer 4 — Evidence-Derived Scores
**What it is:** Every option scored on every dimension — from evidence, not opinion.

**The dimensions and how each score is derived:**

| Dimension | How It's Derived (No Human Input) |
|-----------|-----------------------------------|
| Mission value | Does it close a Stage 1 or 2 item? Look it up in the mission state. Yes → high. No → low. |
| Evidence strength | CI green? Scorecard score? Receipt present? Each is a mechanical yes/no. |
| Risk | Is it irreversible? Does it touch protected gates? Computed from the change itself. |
| Cost | CI minutes, time, money. Known quantities from history. |
| Urgency | Is it blocking other work? Read the dependency graph. Blocked items → high urgency. |
| Confidence | How fresh is the underlying data? How many independent verifications? Computed. |

**Every score carries:**
- The evidence it was derived from (specific, checkable)
- A confidence level (how sure is the machine about this score?)
- A freshness timestamp (when was the evidence last verified?)

**The rule:** A score without evidence is flagged, not hidden. The machine says "I scored this 7.2 but my confidence is low because the CI data is 3 hours old" — not just "7.2."

### Layer 5 — Math → Plain Words
**What it is:** The decision, delivered.

**The pipeline:**
1. **Gates first.** Anything prohibited → excluded (not outscored — excluded). Anything needing Shawn's word → routed to Shawn. Anything needing evidence → says exactly what's missing.
2. **Rank the rest.** Value Calculus over admissible options only.
3. **Speak plainly.** "Do X because Y. It beats the next option by Z%. Here's what was ruled out and why."

**Three output formats (same decision, different depths):**
- **For Shawn:** Words in, words out. "Merge the receipt gate — it protects the ledger, its own checks are green, and it beats the alternative by a wide margin." No numbers unless he asks.
- **For workers:** Command in, ranked options out. `decide "what's next?"` → top option + why. They execute. No deliberation.
- **For machines:** Full JSON. Every score, every evidence ref, every confidence interval, every gate state. Auditable to the individual fact.

**The rule:** One answer. The full breakdown exists underneath for anyone who wants it, but the default is clarity.

---

## Part 3: How It Gets Smarter (The Learning Loop)

Every decision writes a receipt:
- What was decided
- What was predicted (expected outcome, confidence)
- What actually happened (recorded later)

Over time, the machine tracks:
- **Overweighting:** Which dimensions did it score too high? (e.g., always overvaluing urgency)
- **Miscalibration:** Where was its confidence wrong? (e.g., 90% confident but right only 60% of the time)
- **Blind spots:** Which situations does it consistently get wrong?

The weights tune themselves. Not by a human adjusting numbers — by the machine measuring its own accuracy and correcting.

**This is the compounding, inside the machine itself.** It doesn't just make decisions. It gets better at making them. Every decision makes the next one smarter.

---

## Part 4: The Honest Gaps (What It Can't Do)

**1. It's only as smart as its picture of reality.**
If the world model is stale, the options are wrong, the scores are wrong, the decision is wrong. Keeping that picture fresh is the real engineering challenge. This is where most of the work lives.

**2. Novel situations need humans.**
When nothing in the world model matches — a genuinely new kind of decision — the machine says "I don't know yet" and asks. It does not guess. The clarifying question is a feature, not a failure.

**3. Protected gates stay human.**
No matter how smart it gets, decisions touching production, credentials, destruction, security, or constitutional changes route to Shawn. The machine never outranks the director on those. This is structural, not optional.

**4. It can't want things.**
The machine optimizes for the intent it's given. If the intent is wrong, the decision is wrong. Setting the right intent — knowing what matters — is still human work. The machine is the how; the human is the why.

---

## Part 5: Build Order (Engineering Plan)

**Phase 1 — The World Model** (build first, everything hangs off it)
- Data connectors: GitHub API (PRs, CI, issues), lane feeds, ledger, mission state
- Incremental refresh engine with freshness tracking
- UNKNOWN/STALE marking (never guess, never use stale silently)
- Query interface: "what PRs are mergeable?", "which lanes are free?"
- API economy: surgical refresh, respect the budget

**Phase 2 — Intent Parsing**
- Natural language → objective + constraints + decision weight
- Wisdom Spending Principle as code (automatic depth selection)
- Clarifying questions when intent is ambiguous

**Phase 3 — Option Mining**
- World model → available options (PRs, work items, unblocked items)
- "What about X?" — human-added options scored equally
- Deduplication and relevance filtering

**Phase 4 — Evidence Scoring**
- Each dimension as a mechanical derivation from the world model
- Evidence + confidence + freshness on every score
- No human-typed numbers anywhere in the pipeline

**Phase 5 — Decision Output**
- Gates → ranking → plain words
- Three interfaces: human (words), worker (command), machine (JSON)
- Receipt writing for the learning loop

**Phase 6 — Learning Loop**
- Outcome tracking (what actually happened?)
- Calibration measurement (was confidence correct?)
- Weight auto-tuning (get smarter over time)

---

## Part 6: The One-Line Version

Stop asking humans to score. Read reality, derive the scores, run the math, speak plainly.

The machine that knows what's true doesn't need to be told what's important — it can see it.

---

*Spec v1. Written by Naya 5 from Shawn's blueprint, 2026-10-12.*
*Next step: Phase 1 — the world model. Already dispatched.*
