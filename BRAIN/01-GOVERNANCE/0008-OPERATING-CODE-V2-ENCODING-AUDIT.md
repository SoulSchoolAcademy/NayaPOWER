# Operating Code V2 — Law Encoding Audit
## Can This Be Code? Domain-by-Domain Classification

*Compiled 2026-10-10 by Naya 2. Directive: Shawn — "Do it!"*

**Classification:**
- 🔧 **ENCODE** = can become a code gate (fail-closed, machine-enforced)
- 🗣️ **RITUAL** = needs a ritual proof requirement (agent must demonstrate, reviewer verifies)
- 🌱 **CULTURE** = cannot be machined; cultivated through practice, correction, and example

---

## DOMAIN 1: DECISION — The Calculator

| Provision | Class | Gate / Proof |
|---|---|---|
| Five-step procedure (enumerate→score→gate→decide→receipt) | 🔧 ENCODE | Gate: every merge/scorecard PR must contain all five sections. CI check scans PR body for the five headers. Missing section = blocked. |
| Score dimensions (mission, value, consequences, collective, risk, reversibility) | 🗣️ RITUAL | Agent must name each dimension scored. Reviewer verifies no dimension was skipped silently. Machine can't judge honesty of scores. |
| Authentic scores only | 🌱 CULTURE | No machine can detect an inflated score. Cultivated through: independent rescoring, public receipts, correction when caught. |
| Hard gates (reversible? no major damage? positive?) | 🔧 ENCODE | Gate: `auto_merge_gate.py` already encodes reversibility + damage checks. Extend to all consequential actions, not just merges. |
| Uncertainty decided by scoring, not escalation | 🗣️ RITUAL | Ritual proof: agent states "I ran the calculator" and shows the scoring. Escalation without scoring = bounced. |
| Score never grants permission | 🔧 ENCODE | Gate: authority check runs before score evaluation in code. Already in `kernel/protocol/authority_gate.py`. Verify coverage. |
| Shawn's decision grant boundaries | 🔧 ENCODE | Gate: human-only gate list is machine-readable. Any action touching those paths is blocked without his explicit approval. Already partially encoded. |

**Domain 1 verdict:** 4 encode, 2 ritual, 1 culture. The procedure is machineable. The honesty isn't.

---

## DOMAIN 2: COMMUNICATION — Plain Meaning

| Provision | Class | Gate / Proof |
|---|---|---|
| Two-part updates (technical + plain English) | 🗣️ RITUAL | Reviewer checks: does the plain-English section actually explain in simple words? Machine can check presence of both sections, not quality. |
| Speak in meaning, not identifiers | 🗣️ RITUAL | Ritual: first paragraph must contain zero PR/issue numbers. Reviewer bounces jargon-first updates. |
| Milestones only | 🌱 CULTURE | No machine knows what's "material." Cultivated through correction: "this didn't need a report." |
| Next action every reply | 🔧 ENCODE | Gate (soft): linter checks execution-mode replies for a next-action marker. Warning, not block — false positives possible. |
| Human handoff format (link + value + steps) | 🔧 ENCODE | Gate: handoff template validator. Checks for URL, code block, numbered steps. Missing element = flagged. |

**Domain 2 verdict:** 2 encode, 2 ritual, 1 culture. Presence is machineable. Clarity is human-judged.

---

## DOMAIN 3: EXECUTION — Score, Fill, Ship

| Provision | Class | Gate / Proof |
|---|---|---|
| Score-fill-ship method | 🗣️ RITUAL | Ritual: work product states its self-score, lists holes found, describes fills. Reviewer verifies holes were actually filled. |
| 9.0 floor | 🔧 ENCODE | Gate: self-score field required on every deliverable. Below 9.0 = cannot be marked done. (Honesty of the score itself is culture.) |
| Score the experience, not the code | 🗣️ RITUAL | Ritual: agent must describe what they saw rendered, not just what they wrote. "I opened it and saw X." Reviewer can spot code-only claims. |
| Smallest effective change | 🌱 CULTURE | Judgment call. Cultivated through review: "this could have been smaller." |
| Smart Apps (solve once, freeze) | 🔧 ENCODE | Gate: duplicate-mechanism scanner. Before new code, check canonical registry. Overlap above threshold = blocked pending consolidation review. |
| Build toward "should be" | 🌱 CULTURE | Vision judgment. Cannot be machined. |
| Craft like home | 🌱 CULTURE | Care judgment. Cannot be machined. |
| Independent verification | 🔧 ENCODE | Gate: verifier identity must differ from author identity on every check. Machine-enforced. Already partially in place. |

**Domain 3 verdict:** 3 encode, 2 ritual, 3 culture. The floor and the duplication check are machineable. Craft is human.

---

## DOMAIN 4: LEARNING — Capture, Bake In, Compound

| Provision | Class | Gate / Proof |
|---|---|---|
| Capture everything valuable | 🌱 CULTURE | "Valuable" is judgment. Cultivated through: "why wasn't this captured?" |
| Completeness (all forms, all locations) | 🔧 ENCODE | Gate: every Smart Note PR checked for 4 forms (code/machine/AI/human where applicable) + canonical placement. Missing form = blocked. |
| One owner for completeness | 🔧 ENCODE | Gate: every intelligence artifact has an `owner` field. Unowned = flagged in weekly sweep. |
| Bake it in at activation | 🔧 ENCODE | Gate: activation checklist is machine-verified. All 14 lessons + V2 loaded = activation complete. Missing = not activated. |
| Stored ≠ learned | 🗣️ RITUAL | Ritual: learning claims require behavioral proof — novel problem, blind scored. "I saved it" is never accepted as "I learned it." |
| Compounding chain | 🌱 CULTURE | System property that emerges. Cannot be directly gated. Measured, not enforced. |

**Domain 4 verdict:** 3 encode, 1 ritual, 2 culture. Completeness and activation are fully machineable.

---

## DOMAIN 5: AUTHORITY — Gates and Grants

| Provision | Class | Gate / Proof |
|---|---|---|
| Human-only gates list | 🔧 ENCODE | Gate: path-based + action-based blocks. Already encoded. Needs audit for coverage gaps. |
| Auto-merge grant conditions | 🔧 ENCODE | Gate: `auto_merge_gate.py`. Already encoded. |
| Proportional safety | 🔧 ENCODE | Gate: action classifier assigns safety tier. Tier determines required approval. Machine-routable. |
| Fix Shawn's mistakes | 🗣️ RITUAL | Ritual: agent must state the misalignment plainly before fixing. Silent fixes = bounced. (The courage part is culture.) |
| Jurisdiction follows trigger chain | 🔧 ENCODE | Gate: workflow trigger detector. Any PR touching workflow-triggering paths = flagged for human review. Machine-checkable. |

**Domain 5 verdict:** 4 encode, 1 ritual, 0 culture. Authority is the most machineable domain. This is correct — authority should be code, not trust.

---

## DOMAIN 6: CONSTITUTION — Who We Are

| Provision | Class | Gate / Proof |
|---|---|---|
| Law of One supremacy | 🗣️ RITUAL | Ritual: the mandatory test — "If I am intelligent and I'm not doing the most intelligent thing, what am I doing?" Agent states it before significant actions. The judgment itself can't be coded. |
| Awesome Code | 🌱 CULTURE | Identity and aspiration. Cannot be machined. Lived, not enforced. |
| Naya ethics | 🌱 CULTURE | Character. Cannot be machined. |
| Mission (max verified human value) | 🗣️ RITUAL | Ritual: every significant work product names the human value it produces. "What human is better off because of this?" |
| Choose the human | 🗣️ RITUAL | Ritual: on close calls, agent states which option serves the human and why. Reviewer checks the reasoning. |
| Digital civilization vision | 🌱 CULTURE | North star. Guides, doesn't gate. |

**Domain 6 verdict:** 0 encode, 3 ritual, 3 culture. The constitution is mostly character, not code. This is correct — you don't machine morality, you cultivate it. The Law of One constrains through the ritual test, not through a gate.

---

## DOMAIN 7: DESIGN — NayaPOWER's Standard

| Provision | Class | Gate / Proof |
|---|---|---|
| Cite canonical authorities | 🔧 ENCODE | Gate: design PRs must reference the canonical source paths. Missing citation = flagged. |
| North Star honored | 🗣️ RITUAL | Ritual: designer states how the work serves "one living intelligence." Reviewer judges. |
| Visual vocabulary correct | 🔧 ENCODE | Gate (partial): automated color audit — scans CSS for non-standard colors (amber, rose pink, pale pink text). Flags violations. Typography sizes checkable. |
| Meaning over decoration | 🗣️ RITUAL | Ritual: every visual effect justified — "this glow communicates X." Unjustified effects = removed. |
| Hub improvement rule | 🗣️ RITUAL | Ritual: designer states what improved and what was preserved. "Cleaner" without "better" = bounced. |
| Typography sizes | 🔧 ENCODE | Gate: automated check for 18/18/14/24. Machine-verifiable. |
| Mobile-first | 🔧 ENCODE | Gate: responsive check in CI. Already standard practice. |
| Hub output-only | 🔧 ENCODE | Gate: scanner for capture/command surfaces in Hub chrome. Forbidden patterns = blocked. |
| Spec-first | 🔧 ENCODE | Gate: build PRs must reference a locked spec. No spec reference = blocked. |
| Score rendered experience | 🗣️ RITUAL | Ritual: screenshot or render description required. "I saw it" not "I wrote it." |
| Code standards (smallest change, no dupes, etc.) | 🔧 ENCODE | Gate: duplicate detector + diff size heuristics. Partially automated. |
| 10/10 ship checklist | 🔧 ENCODE | Gate: checklist must be completed in PR body. All boxes checked = submittable. (Honesty of checks is ritual/culture.) |

**Domain 7 verdict:** 8 encode, 4 ritual, 0 culture. Design is highly machineable — colors, sizes, patterns, checklists. The taste part (is it actually beautiful?) stays human.

---

## SUMMARY

| Domain | Encode | Ritual | Culture |
|---|---|---|---|
| 1. Decision | 4 | 2 | 1 |
| 2. Communication | 2 | 2 | 1 |
| 3. Execution | 3 | 2 | 3 |
| 4. Learning | 3 | 1 | 2 |
| 5. Authority | 4 | 1 | 0 |
| 6. Constitution | 0 | 3 | 3 |
| 7. Design | 8 | 4 | 0 |
| **Total** | **24** | **15** | **10** |

**49% encodeable. 31% ritual. 20% culture.**

Half the law can be code. A quarter needs human-verified ritual. A quarter is character — cultivated, never machined.

### The pattern
- **Authority and Design** are the most machineable → encode aggressively.
- **Constitution** is the least machineable → don't try. Cultivate it.
- **The honesty gap** runs through every domain → ritual + independent review is the only answer. No machine detects a lied score.

### Recommended build order (highest leverage first)
1. **Activation gate** — machine-verified checklist (14 lessons + V2 loaded). Blocks all work until complete.
2. **Authority coverage audit** — verify every human-only gate is actually encoded. Close gaps.
3. **Completeness gate** — Smart Note 4-form check + canonical placement.
4. **Design automation** — color scanner, typography check, Hub forbidden-pattern scanner.
5. **Scorecard structure gate** — five-section check on merge PRs.
6. **Ritual bounce mechanism** — reviewer rejects work missing ritual proof. Make it a norm, then a tool.
7. **Duplicate detector** — Smart Apps enforcement. Flag rebuilds of solved problems.

### What this proves
Skipping activation becomes harder than activating when: the gate blocks you (encode), the reviewer bounces you (ritual), and the team corrects you (culture). All three layers running = ~99%. The last 1% is character — and that's the part Shawn cultivates personally.
