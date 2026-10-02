# SN-0180 — Design Canon Adoption Directive

| Field | Value |
|---|---|
| SN | SN-0180 |
| Title | Design Canon Adoption Directive |
| Date | 2026-10-02 |
| Seat | Naya 2 (Muse) |
| Authority | Directive of Shawn Vibert (Human Director), main chat 2026-10-02 ~05:37 PDT |
| Truth state | ADOPTED (the directive) · ASSESSMENT (the alignment analysis — Naya 2 first pass) |
| Domain | SYSTEM-INTELLIGENCE / DESIGN-MASTERY / DESIGN-CANON-ADOPTION |
| Supersedes | nothing |
| Cross-references | SN-020 (Signature Design Mastery doctrine) · PR #1313 (Design Mastery OS V1 + Design Gym) · HUB/NAYA-DESIGN-MASTERCLASS-V1.md (15-article constitution, D1–D8) |

## IN A NUTSHELL

Shawn adopted the design canon as working intelligence: the ten designers, ten companies, six 2026 Apple Design Award apps, and eleven books are no longer a reading list — they are the material every seat builds interfaces from, effective immediately. The canon is cross-referenced against our existing doctrine (Masterclass, North Star, LAW ZERO, Visual Bliss Law, color hierarchy, D1–D8): where aligned it locks as law; where it tensions, binding tuning rules resolve toward maximum user experience. This note is the directive plus Naya 2's first-pass alignment map; the full per-entry cross-reference lands with the canon library.

## HUMAN NOTE

We now work a new way. The design canon — Norman, Rams, Krug, Cooper, Eyal, the ten designers, ten companies, six Apple Design Award apps, eleven books — is adopted working intelligence. Every seat designing or building an interface applies it the way a craftsperson applies the properties of wood: without thinking about the rulebook, because the rules are in the hands.

Adoption has three parts:

1. **Apply the canon.** The intelligent blocks in the design gym library are the working form. When you design a button, Norman's affordances, Krug's self-evidence, and Saffer's microinteraction grammar are all in the room.
2. **Cross-reference against what we already hold.** Our constitution is the Design Masterclass, the North Star, LAW ZERO (readability supremacy), the Visual Bliss Law, the color hierarchy, the D1–D8 scorecard. The canon does not replace them — it is checked against them.
3. **Where aligned, lock it. Where not, tune it toward maximum user experience.** Alignment is not negotiable downward: when the canon and our doctrine disagree, the resolution must produce a *better* experience for the human, never a compromise that weakens both.

## CHILD NOTE

Imagine you want to build the most beautiful treehouse in the world. You could guess how — or you could study the ten best treehouse builders who ever lived, copy what makes their treehouses great, and check every idea against your family's safety rules. That's what we're doing: we studied the world's best interface designers, and from now on every screen we build uses what they taught us, checked against our own rules for what's clear, readable, and honest.

## GRANDMA NOTE

We've agreed on a shared standard for beautiful, easy-to-use screens — learning from the best in the world — so everything we make from here on feels simple and trustworthy.

## NAYA NOTE (builder seats — imperative)

- When you begin any interface task, load the canon blocks relevant to the surface you are building (buttons → Norman/Krug/Saffer/Weinschenk; flow → Cooper; engagement → Eyal *through the tuning rule below*; craft → Refactoring UI/Rams; delight → Teenage Engineering/Duolingo *through the tuning rule below*).
- Score your work against D1–D8 as usual. The canon now informs what each dimension *means*: D2 (usability) is Norman+Krug; D3 (emotional resonance) is Norman's *Emotional Design* bounded by the delight tuning rule; D8 (performance) benchmarks against Linear (sub-100ms feel, optimistic UI, keyboard-first).
- If a canon technique conflicts with the Masterclass, North Star, or LAW ZERO, the tuning rules below decide — never your taste, never the trend.
- Log which canon blocks you applied and which tuning rules you invoked, as part of your evidence. "Applied SN-0180" with no trace is not application.

## MACHINE NOTE

```yaml
id: SN-0180
kind: adoption-directive
status: ADOPTED
authority: human-director
effective: 2026-10-02
scope: [all-seats, hub, all-interface-work]
precedence: [human-director, masterclass, one-protocol, contracts, sn-0180-tuning-rules, implementation]
alignment:
  locked: # canon x doctrine — no daylight; treat as law
    - { canon: [Norman-affordances, Norman-feedback, Norman-mapping], doctrine: [LAW-ZERO, D2], rule: "Every control communicates its use; every action gets visible feedback." }
    - { canon: [Krug-self-evidence], doctrine: [north-star-simplicity], rule: "Eliminate every question mark; sophisticated intelligence feels simple." }
    - { canon: [Rams-less-but-better], doctrine: [every-element-earns-its-place, restraint], rule: "Omit needless elements; restraint is a feature." }
    - { canon: [Weinschenk, Johnson-cognitive-psych], doctrine: [visual-bliss-law, generous-type], rule: "Readability supremacy; cognitive limits are design constraints." }
    - { canon: [Saffer-microinteractions], doctrine: [motion-only-for-truthful-state], rule: "Motion communicates state change, nothing else." }
    - { canon: [Maeda-simplicity], doctrine: [restraint], rule: "Reduce without loss of meaning." }
    - { canon: [Cooper-goal-directed], doctrine: [human-at-center], rule: "Design for human goals, not feature lists." }
    - { canon: [Linear-craft], doctrine: [D8], rule: "Benchmark: sub-100ms feel, optimistic UI, keyboard-first." }
    - { canon: [Teenage-Engineering-color-as-function], doctrine: [spectrum-semantic-controlled], rule: "Color carries meaning or it carries nothing." }
  tuned: # tension resolved toward max UX — the tuning rule is binding
    - canon: [Eyal-hook-model]
      tension: "Variable-reward / investment loops vs north-star 'alive because the intelligence is alive, never because animation pretends' + 'interaction is not theater'."
      tuning_rule: "Trigger/action/investment mechanics permitted ONLY in service of the user's genuine goal. Never manufacture variable reward. Streaks and counts must reflect real user-valued progress. No dark patterns, ever."
      scoring_gate: "D3/D4 — any engagement mechanic that cannot show the user's goal it serves scores 0 on that gate."
    - canon: [Duolingo-delight, delight-general]
      tension: "Delight/gamification vs restraint doctrine."
      tuning_rule: "Delight allowed only as truthful state feedback (Saffer's rule). Decoration is not delight."
      scoring_gate: "D1 — decorative delight caps at 9.0."
    - canon: [Apple-liquid-glass-2026, depth-effects-general]
      tension: "Material/depth trends vs LAW ZERO readability supremacy."
      tuning_rule: "LAW ZERO outranks material trends. Glass, blur, and depth permitted only where they never reduce contrast or readability."
      scoring_gate: "D7 — any readability regression from a material effect is a hard-gate failure."
open_items:
  - "Full per-entry cross-reference when the 37-block canon library lands; this assessment deepens then."
  - "2026 Apple Design Award apps verification pending — treat as [unverified] until confirmed against Apple sources."
  - "Second-witness entries (Kare, Victor, Matas, Raycast, Duolingo, Nothing, +9 books) fold into alignment on arrival."
provenance:
  - { source: "Shawn Vibert directive, main chat 2026-10-02 ~05:37 PDT", role: "adoption-order" }
  - { source: "Naya 2 first-pass alignment analysis", role: "assessment" }
  - { source: "design canon library (in build, ~/workspace/your_files/design-gym-library/)", role: "evidence-base" }
  - { source: "deep-research report elite-interface-design-canon-20261002-1230", role: "evidence-base" }
supersedes: none
review_trigger: canon library completion
```

## LEARNING LESSON

Adoption beats accumulation: a canon nobody is obligated to apply is a bookshelf. The directive form — adopted, scoped to all seats, with tuning rules for tensions — is what converts research into reflexes. Record the adoption the same day the research lands, or the research decays into trivia.

## HOW IT CONNECTS

- **SN-020** (Naya Signature Design Mastery — Autonomous Extraordinary Interface Doctrine): this directive operationalizes it. SN-020 states the doctrine of autonomous extraordinary interface building; SN-0180 binds the world's canon into it as working material. Adjacent, not duplicative.
- **PR #1313** (Naya Design Mastery OS V1): the Design Gym is where the locked rules and tuning rules become training exercises. This note feeds the gym; it does not re-derive the OS.
- **Masterclass**: the canon is checked against the 15-article constitution, never placed above it. Precedence unchanged: Director → Masterclass → ONE Protocol → contracts → this directive's tuning rules → implementation.
- **Upstream**: design canon library (37 blocks, in build) + deep-research report `elite-interface-design-canon-20261002-1230`.

## EPISTEMIC STATE

- **Directive ADOPTED**: instruction from the Human Director. Falsifier: a later explicit directive from Shawn rescinding or amending it.
- **Alignment analysis ASSESSMENT**: Naya 2's first pass, honest but not yet cross-checked against the full 37-block library. Falsifier: the library's per-entry cross-reference contradicting a locked/tuned item — conflicts amend this note via a follow-up SN with receipts.
- **2026 Apple Design Award app claims**: UNVERIFIED pending check against Apple sources (deep-research could only corroborate 2025 winners). Not asserted here.

## UNCERTAINTY

- Whether the "tuned" resolutions (especially the Eyal hook-model gate) survive contact with the full library's per-entry analysis.
- Second-witness entries (Kare, Victor, Matas, Raycast, Duolingo, Nothing, +9 books) not yet folded into the alignment map.

## APPLICABILITY

All interface/design/build work by all seats from 2026-10-02 forward. Does not apply retroactively as a re-score mandate — existing scorecards stand; new work follows the directive.

## SUCCESSOR EFFECT

A cold successor reading this note knows: the canon is adopted law, the tuning rules decide conflicts, SN-020 and PR #1313 are the sibling artifacts, and the canon library is the evidence base. No replay of the adoption conversation needed.
