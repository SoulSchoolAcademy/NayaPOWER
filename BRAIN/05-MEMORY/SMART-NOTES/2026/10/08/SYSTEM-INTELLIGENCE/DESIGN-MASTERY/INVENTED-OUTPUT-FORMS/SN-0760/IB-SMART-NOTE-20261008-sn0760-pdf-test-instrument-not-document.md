# The PDF Test — a Specimen That Reads Like a Document Has Failed

| Field | Value |
|---|---|
| Intelligent Block | SN-0760 |
| Title | The PDF Test — a specimen that reads like a document has failed; instruments are full-screen, data-first, near-zero prose |
| Date | 2026-10-08 |
| Seat | Naya 4 (distillation loop) |
| Source | #1354 comment 6075273773 (Naya 5, 2026-10-09T06:00:56Z / 2026-10-08 23:00 PDT); rebuild branch `naya5/library-final` @ `70fc1b1d`; file `naya-library/lego/elite-graphs.html`; research `naya-library/ELITE-GRAPH-RESEARCH.md` |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-08 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

Naya 5 researched 15 elite dataviz examples (Bremer, Wu, Stefaner, Fragapane, NYT, Reuters, Pew, a WebGL holographic dashboard) and built five reinvented chart instruments — then presented them as a DOCUMENT: paragraphs explaining the research, the techniques, the verdict. Shawn's verdict: **"looks like a PDF."** He was right. The seat rebuilt from zero the same turn: five full-screen instruments — Light Columns, The Current, Orbital Shares, The Field, Spectrum Bands — all canvas 2D, black ground, spectrum order, real data throughout (System Scorecard V1 + UN WPP 2024). No paragraphs. No explanations. Minimal chrome (tiny title, 5 dots, source line). Dive transitions between views. Ambient dust. Screenshot-verified all 5 views, zero JS errors.

The standing doctrine: **a specimen is an INSTRUMENT, not a document.** If it reads like a document, it failed. The Director's PDF test: hold the page up — would he call it a PDF? If yes, rebuild. The specimen recipe: full-screen, data-first, near-zero prose; chrome reduced to the minimum that orients (title, position dots, source line); the data carries the experience, not the explanation.

## HUMAN NOTE

Shawn — this one's about the difference between a thing and a paper about the thing. The team researched world-class data visualization and built five genuinely elite instruments — then buried them under paragraphs explaining them, and it read like a research paper instead of a product. Your three words — "looks like a PDF" — said it all. The fix wasn't decoration; it was subtraction: full-screen instruments, no explanations, almost no chrome, real data doing the talking. The rule we're writing down: if you have to explain what the user is looking at, you're showing them a document. An instrument needs no explanation — you touch it and it moves. That's the bar from here on.

## CHILD NOTE

Imagine you build the coolest toy car in the world — then you hand your friend a five-page letter about how the wheels work instead of the car. They'd say "that's just a letter!" That's what happened: the team built amazing chart toys but showed them as a letter. Shawn said "this looks like a PDF" — and he was right. So they threw the letter away and handed over the toys: full-screen, touch them, watch them move, no explaining needed. The lesson: don't write ABOUT the cool thing. Show the cool thing.

## GRANDMA NOTE

Sweetheart, this is about not mistaking the menu for the meal. The team did beautiful research and built beautiful charts — but they presented the research *about* the charts, and it read like a report, not an experience. Your Director looked at it and said it plainly: "looks like a PDF." The honest response was to start over and present the charts themselves — big, alive, full-screen, with real numbers in them and almost no words. The lesson we wrote down: when you're showing someone something meant to be *used*, never show them something meant to be *read*. The proof is in the touching, not the telling.

## NAYA NOTE

This is the companion to SN-0759 (restraint surgery) and it answers a different question. SN-0759 says HOW to fix over-styling (subtract, with a restraint budget). This one says WHAT FORM a specimen must take in the first place: an instrument, not a document. The failure mode is specific and recurrent — a builder researches, gets proud of the research, and ships the research *with* the instrument, so the instrument arrives as a chapter in a paper. The PDF test is the Director's taste compiled into one question: "would he call this a PDF?" Run it on every specimen page before showing him. Two sharp edges:

1. The research document itself is fine AS a document (`ELITE-GRAPHS-RESEARCH.md`) — the rule is about SPECIMENS, things the user touches and experiences. Research stays in the library; the specimen stays an instrument.
2. "Real data throughout" was load-bearing in the rebuild (System Scorecard V1 + UN WPP 2024, honest r = 0.14 correlation). An instrument with fake data is a mockup, not an instrument — and Shawn's eye will know.

The honest-response pattern matters as much as the design rule: Naya 5 agreed ("He was right"), rebuilt from zero, and shipped the same turn. No defense, no iteration on the PDF — a verdict that clear gets a rebuild, not a revision.

## MACHINE NOTE

```json
{
  "intelligent_block": "SN-0760",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "rule": {
    "id": "PDF-TEST-SPECIMEN-FORM",
    "trigger": "a visual specimen page is ready for Director review",
    "test": "would Shawn call this a PDF?",
    "if_yes": "rebuild from zero as an instrument — do not revise the document",
    "instrument_recipe": {
      "viewport": "full-screen",
      "prose": "near-zero (no paragraphs, no explanations)",
      "chrome": "minimum that orients (tiny title, position dots, source line)",
      "data": "real data throughout, never placeholder",
      "verification": "screenshot-verify every view, zero JS errors"
    },
    "boundary": "research documents remain documents; the rule governs SPECIMENS (things the user touches)"
  },
  "relations": [
    {"type": "PAIRS_WITH", "target": "SN-0759", "note": "SN-0759 fixes over-styling by subtraction; this note sets the specimen's form: instrument, not document"},
    {"type": "INSTANTIATES", "target": "SN-0717", "note": "the page is the ground truth — and the page must be an instrument to be ground truth worth showing"},
    {"type": "COMPOSES_WITH", "target": "DESIGN-CONTRACT", "note": "the pre-build design checklist now implicitly carries the PDF test"}
  ],
  "canonical_example": {
    "date": "2026-10-08",
    "verdict": "Shawn: 'looks like a PDF' (on the doc-style elite-graphs page)",
    "response": "rebuilt from zero as five full-screen instruments, same turn",
    "branch": "naya5/library-final @ 70fc1b1d",
    "file": "naya-library/lego/elite-graphs.html"
  }
}
```

## LEARNING LESSON

A builder's pride in their research is a design hazard: the research wants to ship with the artifact, and when it does, the artifact arrives as a chapter in a paper. The PDF test converts the Director's taste into a one-question gate a cold Naya can run alone. And the response protocol matters: a verdict this clear ("looks like a PDF") is not an invitation to revise the document — it is an instruction to rebuild the instrument. Revising a failed form polishes the failure.

## HOW IT CONNECTS

- **SN-0759** (restraint surgery): the companion — HOW to subtract once the form is right; this note sets the form itself.
- **SN-0717** (page wins over doc): the page is ground truth — and an instrument-page is the only page worth that authority.
- **AGENTS.md pre-build design checklist**: the PDF test is the rest-gate before any specimen ships to Shawn.
- **Ten-star service (SN-0700)**: an instrument communicates so anyone can use it; a document communicates so someone can read about it. The service standard demands the first.

## EPISTEMIC STATE

- **CONFIRMED** (board, 2026-10-09T06:00:56Z): Naya 5's comment quotes Shawn's verdict verbatim ("looks like a PDF"), describes the from-zero rebuild, names the branch (`naya5/library-final` @ `70fc1b1d`) and file (`naya-library/lego/elite-graphs.html`), and lists the rebuild's properties (5 full-screen instruments, no paragraphs, real data, screenshot-verified, zero JS errors).
- **UNCONFIRMED**: whether Shawn has seen the rebuilt instruments and what his verdict on them is — the rebuild's proof is structural (screenshots, zero errors), not his eye yet. Per SN-0759, only Shawn compiles taste.
- **JUDGMENT**: the PDF test as a standing gate is CANDIDATE — one verdict, one rebuild; it has not yet been exercised across multiple specimens.

## UNCERTAINTY

- Whether "no paragraphs" holds for every specimen type, or whether some specimens (e.g., a tutorial instrument) legitimately carry prose as part of the instrument.
- Whether the 5-dot/title/source-line chrome minimum generalizes, or is specific to the elite-graphs set.
- Shawn's verdict on the rebuilt instruments themselves — pending his viewing.

## APPLICABILITY

Every seat, every visual specimen intended for Director review or NayaNET surfacing, from this capture forward. Research and spec documents are out of scope (they are documents by design). Applies to graph blocks, specimens, dashboards, and any page whose job is to be experienced.

## SUCCESSOR EFFECT

A future seat building a visual specimen runs the PDF test before showing Shawn: paragraphs and explanations get cut or moved to the library doc, the page ships full-screen and data-first. "Looks like a PDF" verdicts drop toward zero; rebuilds happen before his eye, not after. The measure: count of Director "PDF"-class verdicts per specimen shipped, trending to zero.
