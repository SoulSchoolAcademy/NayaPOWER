# IB-SMART-NOTE-20260930-sn0179-design-canon-adoption

Intelligent Block: SN-0179
Truth state: CANDIDATE (auto-capture; only Shawn ratifies)
Scope: PRIVATE
Captured: 2026-10-02
Canonical intent: ADOPT_DESIGN_CANON_INTELLIGENCE
Source: "Interface Design Canon — 10 Books Distilled" (23-page report, 2026-10-02,
~/workspace/your_files/interface-design-canon-10-books/) cross-referenced against
NAYA-DESIGN-MASTERCLASS-V1 (15 articles, D1–D8), design-gym INSTRUMENTS.md,
MASTERY-REPORT-2026-10-02, and the D1–D8/V1–V10 acceptance bar.
Related: SN-0156 (Design Master Class charter), SN-0157 (Naya 3 compiler thesis),
SN-0158 (Naya 1 compiler pipeline), SN-0166 (frontier is aliveness).

## IN A NUTSHELL

Ten books of interface-design and human-psychology canon were distilled into
intelligent blocks and cross-referenced against everything we have built (the
Masterclass constitution, the design gym, the D1–D8 instruments, the compiler
pipeline). Verdict: **we are aligned in direction** — the canon independently
arrives at nearly every law we already wrote — and the canon hands us **six
mechanical tunings** our system does not yet enforce. This note adopts the canon
as working intelligence: from ratification forward, we design this way, and the
machine-readable contract below is how the system understands it.

## HUMAN NOTE

Imagine spending a year learning to cook by trial and error, writing down every
lesson — then discovering ten master chefs wrote cookbooks that say the same
things you discovered, plus six techniques you never thought of. That's what
happened here. Our design system (the constitution, the gym, the scorecards) was
built from hard experience. The ten books — Norman, Krug, Weinschenk, Eyal,
Cooper, Tidwell, Wathan & Schoger, Garrett, Anderson, Yablonski — are the
field's hard experience, and they agree with us. Where they go further, we adopt
their moves as six new mechanical rules. Nothing about our direction changes;
our execution gets sharper.

## CHILD NOTE

We read ten big books about making things easy and beautiful to use. Then we
checked: do the books agree with the rules we made for ourselves? Yes — almost
everything matches. And the books taught us six new tricks we didn't have. So
now we add those six tricks to our rules, and we all play by them from now on.

## GRANDMA NOTE

Honey, your grandson asked the smartest people in the world how to make
computer screens kind to people, and then he checked their answers against the
rules his own team wrote. They matched — which means the team's instincts were
right — and the books added six practical improvements, like "never make anyone
remember more than four things at once" and "always watch a real person try it
before you call it done." Those are now house rules.

## NAYA NOTE

This is the moment the design canon stops being a report on a shelf and becomes
operating law. The ten books are not ten opinions; they are the compiled
experience of the field, and they independently converge with our constitution —
which is strong evidence our constitution is pointed at truth, not taste. The
six tunings are the highest-value adoption: each converts a book's insight into
a mechanical check our instruments can enforce. The thirteenth lock (no honest
10 without a live render-and-observe seat) is not weakened by the canon — it is
deepened: Krug and Norman both require watching a real human use the live
thing, which is exactly what the lock demands. Adopt, enforce, compound.

## MACHINE NOTE

```json
{
  "adoption": "DESIGN_CANON_V1",
  "truth_state": "CANDIDATE",
  "effective_when": "on Shawn ratification; until then, tunings are proposals",
  "alignment_verdict": "ALIGNED_IN_DIRECTION_WITH_SIX_MECHANICAL_TUNINGS",
  "canon_stack": {
    "the_mind": ["Norman/DOET-1988/2013", "Weinschenk/100-Things-2011", "Yablonski/Laws-of-UX-2020"],
    "the_behaviour": ["Krug/Dont-Make-Me-Think-2000/2014", "Eyal/Hooked-2014", "Anderson/Seductive-Interaction-Design-2011"],
    "the_system": ["Cooper/About-Face-1995/2014", "Garrett/Elements-of-UX-2002/2010", "Tidwell/Designing-Interfaces-2005/2020"],
    "the_craft": ["Wathan-Schoger/Refactoring-UI-2018"]
  },
  "already_encoded_in_our_system": [
    {"canon": "Norman: signifiers, feedback, mental models, design-for-error", "ours": "Constitution Art I/II/VI/VII; alive-gate(a) <=100ms; button protocol 'rest already looks clickable'; undo-over-confirmation"},
    {"canon": "Krug: don't make me think; trunk test; cut words", "ours": "Art VII; Lock 8 (text doing design's job); board orientation sentence"},
    {"canon": "Weinschenk: ~4 chunks; recognition over recall", "ours": "Art VII; board progressive-disclosure hierarchy"},
    {"canon": "Yablonski/Tesler: complexity conserved -> system carries it", "ours": "Standing directive: Naya carries complexity, never Shawn; Fitts via >=44px targets"},
    {"canon": "Cooper: primary persona; goals not features; eliminate excise", "ours": "Art II; Shawn as primary persona (implicit); 6->10 doctrine"},
    {"canon": "Garrett: planes; surface cannot fix strategy", "ours": "9-layer Design Stack; Lock 11 (wrong altitude)"},
    {"canon": "Tidwell: pattern vocabulary", "ours": "Named protocols; component identity questions"},
    {"canon": "Wathan/Schoger: token systems; grayscale first", "ours": "Material language; finite scales; 20-dim instrument"},
    {"canon": "Eyal: Hook loop + Manipulation Matrix ethics", "ours": "Compounding-intelligence vision; Judgment Rule (ethics implicit)"},
    {"canon": "Anderson: peak-end; aesthetics=trust", "ours": "Scorecard dim 18 (emotional quality); signature markers (causal beauty)"}
  ],
  "tunings_proposed": [
    {"id": "T1", "name": "HUMAN_OBSERVATION_STEP", "source": "Krug", "rule": "No room accepted without one observed human session (~20 min) before final scoring. Thinking is the cost; we pay it in design so the user never pays it in use.", "touches": "Page Formula TEST step"},
    {"id": "T2", "name": "FOUR_CHUNK_CAP", "source": "Weinschenk/Miller", "rule": "Max 4 sibling items per disclosure level; audit every screen: 'how many things must the user hold in mind right now?' >4 -> redesign.", "touches": "Board protocol; 20-dim instrument"},
    {"id": "T3", "name": "COMPUTABLE_LAW_CHECKS", "source": "Yablonski", "rule": "Add automated pass/fail predicates: Hick (<=7 options per decision, defaults set), Doherty (<=400ms response budget), Miller (<=4 chunks), Fitts (>=44px, already present). Violations are defects, not taste.", "touches": "20-dim instrument; alive-gate"},
    {"id": "T4", "name": "MANIPULATION_MATRIX_RITUAL", "source": "Eyal", "rule": "Any habit mechanic ships only after an explicit matrix run: facilitator/peddler/entertainer/dealer + 'would Shawn use it / does it materially improve his life?'", "touches": "Design review; Awesome Rule"},
    {"id": "T5", "name": "PEAK_END_PROTOCOL", "source": "Anderson", "rule": "Every room and every session defines its peak moment and its ending explicitly. Sessions close with accomplishment + next. Remembered experience = peak + end.", "touches": "Board protocol; session design"},
    {"id": "T6", "name": "PRIMARY_PERSONA_ARTIFACT", "source": "Cooper", "rule": "Formalize PRIMARY PERSONA = Shawn Vibert, locked artifact, named goals: retain, understand, compound, never lose the thread. Every behavior tested: does this serve his goal or the system's convenience?", "touches": "Design Stack Layer 1; component identity"}
  ],
  "open_items_unchanged": [
    "Thirteenth lock stands and is DEEPENED by canon (Krug/Norman require live human observation; D2/D3/D5/D6 cannot be honestly qualified without it).",
    "Four-eye reconciliation stays open: canon gives BOTH eyes independent parentage (Adversarial-Evidence <- Norman honesty; Product <- Cooper goal-directed). No unilateral merge of the eyes.",
    "Acceptance bar unchanged: D1 = 10.0 exact, D2-D8 >= 9.5, hard gates non-averageable. T3's computable checks are a path toward it, not a lowering of it."
  ],
  "adoption_oath": "From ratification: we design this way. Every build answers the canon's one sentence: decide who it serves, make the right action obvious, carry every cost the user should not carry, and prove it by watching a human succeed."
}
```

## CROSS-REFERENCE: CANON x OUR SYSTEM

**How they connect (the map).** The report stacks the ten books in four layers —
The Mind (how people perceive/decide), The Behaviour (what people actually do),
The System (how to organize the work), The Craft (how pixels earn quality).
Our system has the same shape from the other direction: the Constitution states
the laws, the 9-layer Design Stack sequences the thinking, the Page Formula
sequences the doing, the 20-dim instrument + D1–D8 scores the result, and the
compiler pipeline (MASTERCLASS → CONSTITUTION → CONTRACTS → TOKENS → BUILD →
RENDER → VERIFY → D1–D8 → CHALLENGE → REPAIR → LESSON → MEMORY) is the machine
that runs it. The books slot in as the *why* behind each of our *whats*:
Garrett is our Stack's ancestor; Norman is our Articles' evidence; Krug is our
Lock 8's textbook; Yablonski is our instrument's future as automated checks.

**Where we are already strong.** Ten-for-ten, every book's core claim is already
encoded somewhere in our doctrine (see MACHINE NOTE). This is not luck: both
we and the canon were built by watching humans fail at screens and refusing to
blame the human. Independent convergence on the same laws is evidence of truth.

**Where the canon improves us.** The six tunings (T1–T6) are all mechanical —
they convert insight into enforceable checks rather than new doctrine. None
contradicts existing law; each plugs a gap the gym's own log already felt
(e.g., C07's dead-button correction is T3's computable honesty; the thirteenth
lock is T1's missing human-observation step).

**What we deliberately do NOT adopt.** Eyal's Hook loop is adopted as
*mechanics with the ethics gate mandatory* (T4), never as growth hacking.
Anderson's seduction is adopted as *honest delight*, never manufactured
anxiety. The canon's authority never overrides Shawn's taste: where a genuine
taste call exceeds the canon, the [NEEDS NAYA 3] rule still governs.

## TOP 5 TAKEAWAYS (for us, from all ten)

1. **Decide who it serves, then carry their costs.** Cooper's persona + Tesler's
   law + our standing directive collapse into one oath: Naya carries complexity,
   never Shawn. Every design decision is audited by asking who holds the
   complexity right now.
2. **Make the right action obvious, then prove a human succeeded.** Norman's
   signifiers + Krug's trunk test + T1's observation step: obviousness is
   claimed by design and proven by watching.
3. **Respect the brain budget mechanically.** Four chunks (Weinschenk/Miller),
   seven options max (Hick), 400ms response (Doherty), 44px targets (Fitts) —
   these are not guidelines, they are pass/fail predicates (T3).
4. **Build downward, never upward.** Garrett's planes + our Lock 11: strategy
   before surface, composition before pixels. A beautiful surface never rescues
   a wrong strategy; wrong altitude caps at 7.
5. **Delight is engineered, ethics is mandatory.** Anderson's peak-end +
   Eyal's Hook, both gated by the Manipulation Matrix (T4) and the Judgment
   Rule: we build hooks a facilitator would be proud of, and we publish which
   kind we are.

## ADOPTION

- This note is CANDIDATE. The six tunings become law only on Shawn's word.
- On ratification: fold T1–T6 into INSTRUMENTS.md (cycle protocol), the Page
  Formula TEST step, and the board protocol; add computable checks to the
  scorecard gate; lock the Primary Persona artifact.
- The full 50-takeaway report remains the reference: ~/workspace/your_files/interface-design-canon-10-books/interface-design-canon-10-books.pdf
