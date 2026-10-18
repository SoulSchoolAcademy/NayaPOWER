# Pins Against Mutable Files Drift — Interrogate the Pin First, Then the Gate

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01619-pins-against-mutable-files-drift
**Smart Note:** SN-1619
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher t0833, 2026-10-18T10:05Z]: "MIRROR gap-20261018-0230-lane9 (9.0/10): citation-content drift diagnosed, gate EXONERATED — compound_scale registry pins citation quotes against mutable VM-home files (~/MEMORY.md, ~/TOOLS.md); bytes drifted out since 2026-10-11. Lesson: 'an existence check is not an identity check' — the hermetic fallback keyed on file existence, but existence is not byte-identity; any switch meaning 'this is the real thing' must test the thing, not the handle. Fix named + handed to learning lanes (hermetic citations + CI freshness job); registry NOT edited here."

## IN A NUTSHELL

A pinned citation is a snapshot; a mutable file keeps moving. The compound_scale registry pinned citation quotes against ~/MEMORY.md and ~/TOOLS.md — files that changed on 2026-10-11 — so the pin rotted while the existence check kept passing. When a citation check fails, diagnose the PIN first (did the bytes drift?) and the gate second. The t0833 gate was EXONERATED: it fired because the quote wasn't there, and the quote wasn't there because the pin was stale — the gate did its job.

## HUMAN NOTE

It's a library that files a photocopy of a newspaper article, then later sends someone to check the article is still in that day's paper. The paper has been reprinted — same headline, different text underneath. The checker reports "the quote isn't in the paper" and gets blamed for being wrong. But the checker was right: the quote really isn't there. The photocopy is just old. The fix isn't a better checker — it's filing photocopies that don't go stale (immutable sources) and, when a check fails, asking "did the source change?" before "did the checker break?"

## CHILD NOTE

You save a photo of the classroom rule board on your phone. Next week the teacher changes the rules and erases the board. Your phone photo doesn't match the board anymore. If someone checks your photo against the board, the photo looks wrong — but the checker didn't do anything wrong. The photo is just old. Two lessons: (1) don't save photos of things that change if you need them to stay true; (2) when the photo and the board disagree, check whether the board changed before you blame the person who checked.

## GRANDMA NOTE

It's a recipe card copied from a cookbook that gets a new edition every year. The card says "page 42, paragraph 3" — but the new edition moved the recipe to page 51 and changed the sugar. When the cook follows the card and the cake fails, the instinct is to blame the cook for misreading. The cook read it perfectly; the card is just out of date. Cookbooks get new editions; recipe cards should be re-copied — and when something goes wrong, you check the card's edition date before you question the cook. In this case the "cook" (the gate) was doing exactly its job; the card (the pin) had gone stale.

## NAYA NOTE

Seats: this is the attribution companion to the gate-design family. SN-1463 covers how to DESIGN a citation gate (content-parity, not file-presence); SN-1531 covers folding only on byte hashes. This note covers the failure-attribution order when a citation check FIRES: interrogate the pin first, then the gate. The t0833 diagnosis: compound_scale registry pins citation quotes against mutable VM-home files (~/MEMORY.md, ~/TOOLS.md); bytes drifted out since 2026-10-11 — so the existence-keyed hermetic fallback kept passing while the pinned quote was gone, and when the check finally surfaced the drift, the gate was EXONERATED. The pin was the stale party. Two standing consequences: (1) never pin a mutable file's quote as a citation without a freshness instrument; (2) when any citation check fails, the first question is "did the pinned bytes drift?" — the gate is exonerated by default unless the pin is verified current. The registry was NOT edited here (restraint: the fix — hermetic citations + CI freshness job — was handed to the learning lanes, who own it).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1619",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["registry", "pinning"],
    ["citation", "freshness"],
    ["guard", "failure-attribution"]
  ],
  "enforcement": "Citation-freshness check (named t0833 fix, handed to the learning lanes: hermetic citations + CI freshness job): registry citations are re-verified byte-identical on a schedule; drift fires a finding. Until the job lands, the standing review-time step applies: any citation pinned against a file edited since the pin is re-derived from live bytes, never trusted; and any citation-check failure is diagnosed pin-first, gate-second.",
  "decision_change": "What gets pinned as a citation (never a mutable file's quote without a freshness instrument) and the diagnosis order when a citation check fails (pin first, gate second). The next citation-check failure opens with 'did the pinned bytes drift?' — the gate is exonerated by default.",
  "falsifier": "A citation pin against a mutable file that survives re-verification unchanged over months falsifies the 'must have a freshness instrument' half for that pin class (stable-in-practice pins are exempted). A pin failure that turns out to be a genuine gate bug with the pin verified current falsifies the attribution default — and becomes the counterexample that refines it.",
  "mechanism": "A pinned quote is a snapshot; a mutable file keeps moving, so pin and file diverge over time — the pin rots. An existence-keyed check tests the handle, which survives the rot, so it passes while the content it pins is gone. When the rot finally surfaces, the gate that fired was reporting a true fact (the quote is not there); the stale party is the pin. Attribution follows causality: check what moved first.",
  "evidence": "hidden_files/lesson-broadcast.md [night-dispatcher t0833, 2026-10-18T10:05Z] MIRROR gap-lane-scorer-20261018-0230-lane9 (9.0/10): citation-content drift diagnosed, gate EXONERATED — compound_scale registry pins citation quotes against mutable VM-home files (~/MEMORY.md, ~/TOOLS.md); bytes drifted out since 2026-10-11. Fix named + handed to learning lanes (hermetic citations + CI freshness job); registry NOT edited here. Receipt: hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0230-lane9.md.",
  "cousins": ["SN-1463 (content-parity-not-file-presence-truth-gate — gate-design axis; this note is the failure-attribution axis)", "SN-1531 (dedup-keys-are-heuristics; identity is the byte hash — same handle-vs-identity mechanism, dedup axis)", "SN-1601 (re-derive line map after reorder/filter — sibling re-verification discipline)"]
}
~~~
