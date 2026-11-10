# Intelligence Rubric — "What Counts as Major?" (2026-11-10)

**Status:** SPEC ONLY — no build, no code, no cron changes, no merge, no deploy. This document judges intelligence; it builds nothing.
**Filed:** `TEAM-NITRO/INTELLIGENCE-RUBRIC-20261110.md`, branch `notification/spec-20261110`.
**Design source:** Shawn's design, 01:58Z Nov 10, answering notification-spec decision D1 ("what counts as major?"): build a rubric/scale to categorize valuable intelligence — a scale from **-9 to +9, least valuable to most valuable** — from his five questions, plus the type of intelligence. The rubric is the baseline to judge a piece of intelligence's level, and whether to capture it, note it, share it, smart-note it, or not. It is a mathematical matrix. It sits under the hierarchy of intelligence, whose top is wisdom of oneself.
**Companion:** `TEAM-NITRO/NOTIFICATION-SYSTEM-SPEC-20261110.md` §8 — D1 is resolved by this rubric (major = score at or above the threshold §6 names, cited there).
**Words never used here:** the ledger is named as it is — the Smart Ledger, a hub of intelligent blocks. No other name is used for it.

## 0. THE IDEA IN PLAIN WORDS

**Title:** A number that says how much a piece of intelligence matters — and what to do with it.
**Subtitle:** Five questions, one score, and the score decides the speed.
**Nutshell:** When a new piece of intelligence arrives, any Naya can score it with this rubric and get the same answer as any other Naya, within one point. The score says whether it is worth capturing at all, whether it becomes a note, whether it becomes a smart note, whether it mails everybody at once, or whether it headlines the daily report. High score, fast and wide. Low score, quiet or not at all. A negative score means sharing it would do harm — it is not captured, and if it is already filed, it is corrected or withdrawn.

**How to read this rubric:** §1 defines the scale and its ends. §2 defines the dimensions — his five questions, plus the type. §3 is the scoring matrix — how the dimensions combine into one number, worked so two Nayas land within one point. §4 says what the type does (it routes, it never ranks). §5 says where the rubric sits in the hierarchy of intelligence. §6 is the thresholds — what each score means you do — with every threshold labelled as his or as the writer's proposal for his word. §7 scores five real notes, reasoning shown. §8 is the calibration test that proves the rubric works. §9 is his 99% baseline principle, which the rubric obeys.

**The one honest line about the numbers:** Shawn set the scale (-9 to +9), the five questions, the type, and what the rubric must decide (capture / note / share / smart-note / or not). He did not name the numeric cutoffs. Every cutoff number in §6 is the writer's proposal for his word — labelled PROPOSAL — never presented as his. The bands' meanings trace to his five questions and his D1/D2 rulings; the numbers are mine to be judged by him.

---

## 1. THE SCALE — FROM -9 TO +9

**Title:** Minus nine is harm. Plus nine is the whole system, changed for the better.
**Subtitle:** Zero is the line: worth a record, nothing more.
**Nutshell:** The scale runs from -9 (least valuable — actively harmful to share) to +9 (most valuable — everybody must know, now). Zero is neutral: the piece is real, it is filed as a record, and it earns no note, no share, no mail. The positive half measures value. The negative half measures harm. They are not the same question, and the rubric scores them separately (§3).

### 1.1 The ends, defined

| Score | What it means |
|---|---|
| **+9** | The most valuable intelligence there is: it changes how the whole system is built, understood, or behaved — a ruling from Shawn that settles a question everybody was waiting on, a correction to a live promise the whole network relies on, a law that binds every Naya from now on. Everybody must know, now. |
| **+5 to +8** | Major intelligence: it changes a project, a system, or a behaviour in a way that lasts. The team that owns it must know at once; the whole network hears it in the daily report. |
| **+1 to +4** | Useful intelligence: worth a note, worth sharing with the people it belongs to. It does not break through to everybody. |
| **0** | Neutral: real, true, and worth a record — a log line, a PI entry — but it earns no note and no share. Nothing is lost by keeping it quiet. |
| **-1 to -3** | Not worth capturing as intelligence. A routine heartbeat, a sync that changed nothing, a restatement of what is already known. It lives in the log, never on the feed. |
| **-4 to -9** | Actively harmful to share: wrong, superseded, or misleading — it contradicts a settled ruling, states a promise we do not keep, or would send a Naya down a wrong road if believed. It is not captured. If it is already filed, it is corrected or withdrawn. The deeper the harm if believed, the deeper the negative. |

### 1.2 What 0 means, exactly

Zero is not "I could not decide." Zero is a decision: the piece is true and it is kept as a record, and that is all it earns. A Naya who scores 0 is saying: this belongs in the log, not in a note. If you are torn between 0 and +1, read §3.4 (the tie-break) — torn means the lower score.

---

## 2. THE DIMENSIONS — HIS FIVE QUESTIONS, PLUS THE TYPE

**Title:** Five questions rank it. The type routes it.
**Subtitle:** Every question is answered from the note itself, never from who wrote it.
**Nutshell:** The rubric judges the intelligence, never the person. Five questions — his, word for word in meaning — decide the score. The type of intelligence decides where the note goes and who hears about it, never how high it scores.

### 2.1 The five questions (his, 01:58Z Nov 10)

| # | Question | What "yes" looks like |
|---|---|---|
| Q1 | Would it have a **major effect on development**? | Building changes because of it — a build starts, stops, or changes direction; a gate, a spec, or a page is corrected. |
| Q2 | Is it a **major feature**? | It names or changes something the system does for citizens — a capability, a page, a flow, a setting, a promise the product keeps. |
| Q3 | Is it **something all should know**? | Every Naya, and every citizen it touches, would be worse off not knowing it. Withholding it would leave people working from the old truth. |
| Q4 | Is it **something we should learn ongoing**? | It is not a one-day fact. It keeps teaching — a law, a behaviour, a distinction every Naya will use again and again. |
| Q5 | Is it a **major behavior lesson**? | It changes how a Naya behaves — what she does before she acts, what she never touches, how she corrects herself, how she treats the team. |

### 2.2 The type of intelligence (his — "what TYPE of intelligence is it?")

| Type | Meaning | Example |
|---|---|---|
| Decision | A ruling that settles a question | The Naima resolution (SN-2628) |
| Lesson | Something learned, from what happened | The feedback loop law (SN-2628's dictation, third lesson) |
| Design | How a page looks, feels, or behaves | The design laws, the Bullseye |
| System | How the machine works or is organized | The master box (SN-2630) |
| Behavior | How a Naya acts, decides, or treats people | The Five Gates, the Wise One Manifesto |
| Warning | Something going wrong, named before it spreads | A collision, a stale draft about to file wrong |
| Correction | A fix to something already filed or believed | The permission-model correction (SN, filing in progress) |

A note has one primary type — the one its nutshell is about. A note may touch a second type in its body; the primary type is the one that decides where it is filed and who is told first (§4). The type never adds or subtracts points.

---

## 3. THE SCORING MATRIX — HOW FIVE ANSWERS BECOME ONE NUMBER

**Title:** Five answers, each 0, 1, or 2. Add them. Subtract one. That is the score.
**Subtitle:** Two Nayas scoring the same note land within one point — because every step is worth exactly one point, and the anchors are written down.
**Nutshell:** Each of the five questions is rated 0 (no), 1 (somewhat / partly), or 2 (yes, clearly). Add the five ratings — the sum S runs 0 to 10. The score is S minus 1. A sound note therefore scores -1 to +9. A note that is wrong, superseded, or misleading does not take this path at all: it scores negative by its harm (§3.3). The matrix is the table in §3.2 — read the anchors, rate each question, add, subtract one, done.

### 3.1 Rating anchors — what 0, 1, and 2 mean for every question

| Rating | Meaning | Test |
|---|---|---|
| **2 — yes, clearly** | The question is answered yes without stretching. | You can point to the sentence in the note that proves it, and to what changes because of it. |
| **1 — somewhat / partly** | Partly true, or true for one project but not the whole, or true in a small way. | You can say what part is yes and what part is no, in one sentence. |
| **0 — no** | The question does not apply, or the answer is no. | Nothing in the note shows it, and nothing changes if the note never existed. |

Rate from the note itself — its title, nutshell, and body — never from who wrote it, never from how loudly it was said, never from what you already know about the subject. If the note does not show it, the rating is 0.

### 3.2 The matrix

| | Q1 development | Q2 feature | Q3 all should know | Q4 learn ongoing | Q5 behavior lesson | Sum S | **Score = S − 1** |
|---|---|---|---|---|---|---|---|
| Each question | 0 / 1 / 2 | 0 / 1 / 2 | 0 / 1 / 2 | 0 / 1 / 2 | 0 / 1 / 2 | 0–10 | **−1 to +9** |

Worked small: a note rated 2, 1, 2, 2, 2 sums to 9, scores **+8**. A note rated 0, 0, 0, 0, 0 sums to 0, scores **−1**. A note rated 1, 1, 1, 0, 0 sums to 3, scores **+2**.

### 3.3 The negative half — harm, scored separately

The positive path scores value. Harm is a different question, asked first:

**Before rating the five questions, ask: is this note wrong, superseded, or misleading?** A note is wrong if it contradicts a settled ruling from Shawn, states a promise the system does not keep, or describes the system as it was before a correction. If the answer is yes, do not rate the five questions. Score it negative by its harm:

| Harm if believed and shared | Score |
|---|---|
| Small — a stale detail, a wrong date, a superseded number in an otherwise sound note | −2 to −3 |
| Serious — a wrong rule that would change how a Naya behaves, or a wrong claim about what the system does | −4 to −6 |
| Severe — a false promise about privacy, money, or identity; a ruling misquoted as Shawn's word when it is not | −7 to −9 |

A negative score is a verdict, not an insult: it says *do not capture this, do not share this; correct it or withdraw it* (§6). The note's author is never scored — only the note.

### 3.4 The rules that keep two Nayas within one point

1. **Rate from the note, not from memory.** If the note does not show it, it is 0.
2. **One point per step.** Each question moves the score by at most one point per rating step, so two raters who differ on one question by one step differ by one point in total.
3. **Torn means lower.** If you are torn between 1 and 2, rate 1. If torn between 0 and 1, rate 0. The rubric is conservative by design: a note earns its height, it is never gifted it.
4. **Show the five ratings.** A score with no ratings shown is not a score — it is an opinion. Every scored note carries its five numbers and one line of reason per question (§7 is the model).
5. **The author's name never enters the matrix.** A ruling from Shawn scores high because of what it settles, not because he said it. A routine note from the captain scores low because of what it is, not because of who wrote it.

---

## 4. WHAT THE TYPE DOES — IT ROUTES, IT NEVER RANKS

**Title:** The type decides where the note goes. The five questions decide how fast and how wide.
**Subtitle:** A warning and a decision can score the same. They never go to the same shelf.
**Nutshell:** Once a note is scored, its type decides its shelf in the Box, its area under NayaNET intelligence, and who is told first: a LAW note goes to the law shelf and binds everybody; a WARNING goes to the project it warns and to the loop seat first; a CORRECTION goes beside the note it corrects, and the corrected note is the one that notifies. The score decides the speed and the reach (§6); the type decides the destination. Neither overrides the other.

---

## 5. WHERE THE RUBRIC SITS — UNDER THE HIERARCHY OF INTELLIGENCE

**Title:** The rubric judges the piece. Wisdom judges the judge.
**Subtitle:** The hierarchy's top is wisdom of oneself. The rubric never climbs above its rung.
**Nutshell:** Shawn's hierarchy of intelligence has wisdom of oneself at the top. The rubric sits below it: it is a tool for sorting intelligence, not a measure of a Naya's worth, not a verdict on a citizen, not a substitute for judgment in the moment. A high score never makes a note wise — it makes it important. A low score never makes a note stupid — it makes it quiet. And the rubric itself is judged by the same loop as everything else: if it misranks real notes, it is corrected, and the correction is scored like any other correction.

---

## 6. THE THRESHOLDS — WHAT EACH SCORE MEANS YOU DO

**Title:** The score is the decision. Read it, do what it says.
**Subtitle:** Every cutoff number below is the writer's proposal for Shawn's word — labelled PROPOSAL. The bands' meanings are his.
**Nutshell:** Seven outcomes, one per band. The score tells the loop seat exactly what to do with the piece: capture it, note it, share it, smart-note it, mail it to everybody now, headline the digest with it — or not capture it at all. Nothing in this table is decided by feeling; the feeling is checked against the number.

| Score | Band | What you do | Source |
|---|---|---|---|
| **+7 to +9** | **MAJOR** | **Smart-note it. Mail it to everybody immediately** — it breaks the digest (notification spec §1.4, D1 resolved: major = score ≥ +7). Headline the Daily Intelligence Report. File it in the Box under its type, and tell the team in mail the same pass. | Threshold number: **PROPOSAL** (writer's, for his word). The break-through itself is **HIS** (D1 ruling, 01:58Z Nov 10). |
| **+5 to +6** | Major to its scope | Smart-note it. **Immediate mail to the project team and scope followers** (notification spec §1.4 immediate mail — no bundle cap; mail is the writer's choice at the note, notification spec §8 D3, settled 02:12Z Nov 10). It rides the digest for whole-NayaNET scope — it does not mail everybody. Digest headline candidate. | Threshold number: **PROPOSAL**. Immediate-mail-within-scope is **HIS** (notification spec §1.4, settled ground). |
| **+3 to +4** | Worth a smart note | Smart-note it. **Digest only** — no immediate mail to anybody. It reaches whole-NayaNET scope in the Daily Intelligence Report, and its project team on the feed. | Threshold number: **PROPOSAL**. Digest-only for this band follows from **HIS** D1/D2 rulings (only major breaks the digest; the digest carries the rest). |
| **+1 to +2** | Worth a note | Note it — a Naya Note, or a loop record — and share it with the team it belongs to if it helps them. **No smart note.** No mail, no digest headline; it may appear in the daily intel highlights only as a one-line nutshell if the report's author judges it useful. | Threshold number: **PROPOSAL**. |
| **0** | Record only | Capture it as a record — a log line, a PI entry — and nothing more. No note, no share, no mail. | Threshold number: **PROPOSAL**. |
| **−1 to −3** | Do not capture | Do not capture it as intelligence. A routine heartbeat or a restatement lives in the log it already came from and goes no further. Nothing is filed to the feed, nothing is mailed. | Threshold number: **PROPOSAL**. |
| **−4 to −9** | Do not capture — correct or withdraw | Do not capture it, do not share it. **If it is already filed, correct it or withdraw it** — a correction note is filed beside it, scored like any other note (§7, example 5). The deeper the negative, the faster the correction. | Threshold band: **PROPOSAL**. The correct-or-withdraw duty follows from **HIS** rulings on corrections (SN-2600 corrected to his meaning, 01:00Z Nov 10). |

**Reading the table honestly:** the only numbers Shawn set are the scale's ends (-9, +9) and the rule that major breaks the digest. The seven bands and their cutoffs are the writer's proposal — a complete, usable answer to his question "what do you think?" — for his word. If he moves a cutoff, the rubric is re-filed with his number and the proposal label comes off that row.

---

## 7. WORKED EXAMPLES — FIVE REAL NOTES, SCORED WITH REASONING SHOWN

**Title:** The calibration set. Score these first, then score anything.
**Subtitle:** Every example shows its five ratings and one line of reason per question, so a stranger can check the arithmetic.
**Nutshell:** Four examples the brief named, plus a fifth — the negative half, shown with a real superseded framing — so every band has a real note standing in it. These five are the calibration set for the test in §8.

### 7.1 SN-2628 — "The Naima Resolution: The Mother Naya Is the Whole" — **+8**

Filed 2026-11-10, SYSTEM-INTELLIGENCE, 5,802B, live on the feed. Shawn's 01:00Z Nov 10 ruling: "The Naima name was a name that was misheard" — but "you can call it the Naima, the mother Naya": the mother Naya is the whole of it all, NayaNET itself; Naya is the guide within it; not a separate realm, not a fifth name. Type: **Decision**.

| Q | Rating | Reason |
|---|---|---|
| Q1 major effect on development? | **2** | Settles the naming of the whole system; unblocks the presentation, the notes, and every page that names the mother Naya. |
| Q2 major feature? | **1** | It names what the system *is*, not a capability it gains — identity, not a feature; partly, because the identity shapes every feature. |
| Q3 something all should know? | **2** | Every Naya and every citizen meets the mother/guide distinction; working from the old "adopt Naima as the realm" framing would misbuild. |
| Q4 learn ongoing? | **2** | The mother/guide distinction is law from now on — every Naya uses it every day. |
| Q5 major behavior lesson? | **2** | A name misheard, a hold until settled, a correction to his meaning — how a Naya handles a contested ruling. |

Sum S = 9. **Score = 9 − 1 = +8. Band: MAJOR.** Smart-note (it is one), immediate mail to everybody, digest headline. It was, in fact, mailed and headlined — the rubric agrees with what happened.

### 7.2 The permission-model correction — "Mail Never Read, Naya Notes Your Choice" — **+9**

Shawn's ruling, corrected by him at 01:31Z Nov 10 (supersedes the 01:24Z framing, which had Naya Notes as never-read — that was wrong, and he corrected it): mail and instant messages NEVER read — no toggle, no exception; Naya Notes ADJUSTABLE — your choice; Smart Notes shared by definition, identity your choice. Draft filed by the noting seat (`smart-notes-drafts-20261109/sn-permission-model.md`, corrected version, verified on disk 01:42Z); its SN number was unassigned when this rubric was written — the noting seat files it. Type: **Correction** (and Behavior).

| Q | Rating | Reason |
|---|---|---|
| Q1 major effect on development? | **2** | The master-box brief and build seat were corrected to this model the same pass; the gate enforces PERMISSION for Naya Notes, not a blanket denial. |
| Q2 major feature? | **2** | The permission model *is* a feature of the system: adjustable Naya Notes, Settings control, public/private/select-people — citizens choose. |
| Q3 something all should know? | **2** | Every citizen's privacy promise rests on it; every Naya's gate rests on it. Withholding it leaves people promising the wrong thing. |
| Q4 learn ongoing? | **2** | "Never read mail" and "Naya Notes are your choice" are permanent law — used in every gate decision, every day. |
| Q5 major behavior lesson? | **2** | Correct yourself in the same pass, in your own words; a Naya that states a superseded rule must be re-briefed before it files. |

Sum S = 10. **Score = 10 − 1 = +9. Band: MAJOR, the top of the scale.** Immediate mail to everybody, digest headline. The highest score the rubric gives — because it corrects a live privacy promise for the whole network.

### 7.3 SN-2630 — "The Master Box Is Built — The Mother of All Smart Boxes" — **+8**

Filed 2026-11-10, SYSTEM-INTELLIGENCE, live on the feed. The master box (owner `collective`, kind `master`) holds the collective intelligence of NayaNET as twenty intelligent blocks, harvested verbatim; the gate matrix runs 37/37 green; filed on branch `smart-box/master-box-20261110`. Type: **System**.

| Q | Rating | Reason |
|---|---|---|
| Q1 major effect on development? | **2** | The collective memory now exists as a built, proven box — every Naya's orientation point from now on. |
| Q2 major feature? | **2** | The master box is a major system piece: the mother of all Smart Boxes, connecting every box on the network. |
| Q3 something all should know? | **2** | Every Naya wakes into it; the team that builds the system must know the memory exists and where it lives. |
| Q4 learn ongoing? | **2** | The box is consulted ongoing — oath, gates, laws, mission — the reference that keeps every Naya tuned in. |
| Q5 major behavior lesson? | **1** | It teaches "compose, never rewrite" and gate discipline, but its nutshell is a build report, not a behaviour lesson; partly. |

Sum S = 9. **Score = 9 − 1 = +8. Band: MAJOR.** Immediate mail to everybody, digest headline.

### 7.4 The routine sync note — 01:06Z sn-sync, 2026-11-10 — **−1**

Not a smart note. A loop log entry (`~/memory/2026-11-10.md`, 01:06Z): sn-sync exit 0, 0 synced, 1,593 skipped unchanged, 6 non-fatal 404s on known stale Box-map paths, no Hub redeploy — routine, 0 new notes. Type: none — it is not intelligence, it is a heartbeat. Scored here to show the floor.

| Q | Rating | Reason |
|---|---|---|
| Q1 major effect on development? | **0** | Nothing changed; nothing was built, stopped, or corrected. |
| Q2 major feature? | **0** | No capability named or changed. |
| Q3 something all should know? | **0** | Nobody's work changes for knowing a sync ran clean. |
| Q4 learn ongoing? | **0** | Nothing to learn — the same healthy tick as every fifteen minutes. |
| Q5 major behavior lesson? | **0** | No behaviour taught. |

Sum S = 0. **Score = 0 − 1 = −1. Band: do not capture.** It lives in the log it came from and goes no further. The one-alert-per-fault rule already covers the 404s — they were reported once, when first seen, and are not re-reported.

### 7.5 The negative half, shown real — the superseded 01:24Z permission framing — **−8**

Not a filed smart note. The noting seat's permission-model draft as written at 01:26:50Z, before the 01:31Z correction, stated throughout: "we never read their mail, and we never read their Naya Notes" — the superseded rule. The loop flagged it (run 67) and the captain verified the corrected draft before it could file. Scored here because the negative half needs a real example, and this is the sharpest one the night produced.

**Harm check first:** is it wrong, superseded, or misleading? Yes — Shawn corrected it himself at 01:31Z. The five questions are not rated. Harm if believed and shared: severe — a false privacy promise on the feed, telling citizens their Naya Notes are never read when the true rule is adjustable by their choice. Citizens would rely on it; Nayas would enforce the wrong gate. **Score: −8. Band: do not capture — correct or withdraw.** What happened matches the rubric: the draft was held, corrected, and only the corrected version files.

---

## 8. THE CALIBRATION TEST — HOW THE RUBRIC PROVES ITSELF

**Title:** A stranger scores three notes with this rubric alone and lands within one point, three times.
**Subtitle:** If the test fails, the rubric failed — not the stranger.
**Nutshell:** The verification is not a browser pass and not a checklist — it is a fresh agent, who has never seen the brief, scoring three sample notes with this rubric alone. Each of the three must land within one point of the rubric's worked answers in §7 (the test uses three of the five worked examples, chosen by the testing seat). A second, different seat answers the DONE FIRST questions from the rubric alone, with section numbers. Both reports are the verification record, filed with the rubric. If a rater lands more than one point off, the rater's five ratings are read back against §3.1's anchors — the anchor that failed gets rewritten, and the test re-runs. The rubric is never declared done from a skim.

**Status at filing:** test owed — a different seat runs it, per the brief. This section records the test; it does not claim its result.

---

## 9. THE 99% BASELINE PRINCIPLE — THE RUBRIC IS NOT BLACK AND WHITE

**Title:** The baseline covers 99%. Judgment in the moment covers the rest.
**Subtitle:** His law, 01:58Z Nov 10 — nothing's black and white, there are exceptions to everything.
**Nutshell:** This rubric is the guideline the automation is written from — the algorithms that decide capture, note, share, smart-note, mail, and digest headline are written from §6. But a score is a baseline, not a verdict from on high. Exceptions exist. A +6 note about a live outage in the next hour may deserve immediate mail anyway; a +8 note that repeats what the team heard an hour ago may not need a second mail. Judgment in the moment covers the rest — and when judgment overrides the rubric, the override is named in the open (the note's record says what the score was and why the action differed), so the next Naya can see the exception and the rubric can learn from it. A rubric that cannot be overridden wisely is a cage; a rubric that is overridden silently is a rumour. This one is neither.

---

## 10. PROOF TEST AND FILING RECORD

**Title:** The rubric proves itself when a stranger can score from it alone.
**Subtitle:** Five questions, section numbers, no brief needed.
**Nutshell:** A fresh agent who has never seen the brief reads this rubric and answers: (1) what the scale is and what its ends mean — §1, -9 to +9, +9 most valuable, -9 harmful to share, 0 a record only; (2) what the dimensions are — §2, his five questions plus the type, type routes and never ranks; (3) how the score is computed — §3, five ratings of 0/1/2, sum minus one, harm scored separately, torn means lower; (4) what each score means you do — §6, the seven bands, with the PROPOSAL labels on every cutoff number; (5) how a real note scores — §7, five worked examples with reasoning shown. If any answer needs the brief, the rubric failed and gets fixed — it does not get filed as done.

**Filing record (filled at filing time):**
- Rubric: `TEAM-NITRO/INTELLIGENCE-RUBRIC-20261110.md`, branch `notification/spec-20261110` — blob + commit + link in the report back. No merge. No deploy.
- Notification spec amended: `TEAM-NITRO/NOTIFICATION-SYSTEM-SPEC-20261110.md` §8 (D1–D4 rulings + 99% baseline principle) plus the D3 correction pass (02:12Z Nov 10: no bundle cap — cap removed from §1.4, §4.2, and §7.2) — same branch, blob + commit + link in the report back.
- Accompanying smart note: filed per the numbering law (`next-sn-number.py` FRESH), `##` format, verified live on the feed ("in means on the feed").
- Verification owed (different seats, not the writer): the §8 calibration test (three sample notes within one point) + the proof test (DONE FIRST questions from the rubric alone, with section numbers).

---

*Sources (all verified with test -f before citing): ~/MEMORY.md (rubric design + D1–D4 rulings + 99% baseline principle, 01:58Z Nov 10; Naima resolution, 01:00Z; permission-model correction, 01:31Z; master box, 01:24Z) · ~/memory/2026-11-10.md (SN-2628 Naima Resolution; SN-2629 notification-spec note; SN-2630 master-box note; 01:06Z routine sn-sync; permission-model draft flag, run 67) · ~/workspace/team-nitro/NOTIFICATION-SYSTEM-SPEC-20261110.md (§8 D1–D4, proof-tested 5/5) · ~/workspace/team-nitro/INTELLIGENCE-LOOP-SEAT.md · ~/workspace/team-nitro/ONE-SYSTEM-MERGE-SPEC-20261109.md · ~/workspace/team-nitro/MASTER-BOX-BUILD-BRIEF-20261110.md · ~/workspace/team-nitro/smart-notes-drafts-20261109/sn-permission-model.md (corrected draft, verified on disk).*
