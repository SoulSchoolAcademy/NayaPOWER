# Smart Note — Naya 3: Hub Output Law Baked Into the Product Contracts

kind: smart-note
truth-state: CANDIDATE
scope: PRIVATE
captured: 2026-10-01 19:15 PDT
captured-by: Naya 4 (builder seat)
source: report shared by Shawn Vibert, authored by Naya 3 (Hub project/design-intelligence seat)
provenance: Naya 3's spec correction → shared by Shawn → distilled by Naya 4 → intelligent block
sn-number: SN-0137
ib-number: IB-007

---

## IN A NUTSHELL

Naya 3 corrected the Hub product specs around the output doctrine and made the key sentence
explicit: **THE HUB IS THE VISUAL PROJECTION OF INTELLIGENCE. IT IS OUTPUT, NOT THE CANONICAL
INPUT OF INTELLIGENCE.** She removed the wrong Hub actions (capture Smart Note, capture
follow-up, generate canonical report, post Activity, client-local IB creation) from the active
specs and told the implementation lanes (#1270, #1278, #1297) directly. The pipeline is now:
HUMAN + NAYA → SMART NOTE/IB → ACTIVITY EVENT → INTELLIGENCE REPORT → canonical persistence /
event / index / provenance → Hub projection adapter → PERSONAL / COLLECTIVE / ACTIVITY →
Feed, Today, Reports, Library, Lists, Spaces, Ledger. **One canonical intelligence object →
many projections** — the Feed, Today, and Library never hold their own copies; they point at
the same IB. She created `HUB/INTELLIGENCE-PROJECTION-CONTRACT-V1.md` + `.json` in PR #1290
and reconciled the direction across the README, project intelligence, design contract,
execution law, room contracts, and room specs. She confirmed the canonical Smart Note home is
`BRAIN/05-MEMORY/SMART-NOTES/` per the ratified protocol — which corrected Naya 4's
04-INTELLIGENCE demo placement the same day. Acceptance test: Shawn says "Naya, Smart Note
this" and the IB fans out automatically — he never manually publishes in the Hub. Status:
246 Node + 546 Python tests passed on #1290, Collective Chain Readiness Gate passed; Kernel
workflow red is index-ledger drift (23 expected vs 25 actual Memory objects), not a spec
failure. Next highest-value action: build one real artery — upstream Smart Note → canonical
IB/event → auto-appears in Hub Personal Feed and Library with the same canonical identity.

---

## HUMAN NOTE

The Hub's rules just got rewritten clearly by Naya 3, the team's design-intelligence seat.
The headline: the Hub *shows* intelligence; it doesn't *create* it. So all the buttons that
let the Hub pretend to create things — "capture a smart note here," "generate a report here,"
"post an update here" — were wrong, and she's removed them from the specs and told every
building team directly.

Now the flow is clean: you talk to any Naya, she writes the intelligent block into the
brain's canonical store, and the Hub simply *projects* it — your personal feed, the shared
collective feed, today's highlights, the library — all showing the same single object, never
copies. Your private stuff stays private; only intelligence you consented to share (once, at
the door) flows to the collective, with your identity sealed. And the test is beautifully
simple: you say "Naya, smart note this," and it just appears everywhere it should — you never
touch the Hub to publish it.

---

## CHILD NOTE

Imagine a magical mirror. The mirror doesn't *make* the things it shows — it just reflects
what's really there. Naya 3 made sure everyone building our mirror understands: the mirror
shows smart notes, but you can't *create* a smart note by tapping the mirror. You tell Naya,
she writes it in the big brain book, and then the mirror shows it — in your feed, in today's
highlights, in the library — always the same one, never copies.

She also made the sharing rule simple and safe: your private things stay private. Only the
wisdom you said was okay to share goes to the shared mirror, and nobody can tell it was yours.
And she took away all the pretend buttons that made the mirror act like it was the brain.
Mirrors reflect. Brains think. Now everyone knows.

---

## GRANDMA NOTE

Honey, good news about the Hub. Naya 3 — she's the careful one who designs how everything
should work — went through all the plans and fixed an important mistake. Some of the plans had
buttons in the Hub that pretended the Hub could *create* intelligence, like writing notes or
making reports. But the Hub is like a television: it *shows* the program; it doesn't *film*
it. She removed those pretend buttons and told all the builders directly, so nobody's confused
anymore.

Everything now flows one clean way: you talk to Naya, she writes it properly in the brain's
filing system, and the Hub displays it — your feed, today's highlights, the library — all
pointing at the same single note, never copies. Your private things stay private; only the
wisdom you agreed to share goes further, with your name kept secret. Simple, honest, and now
it's written down where all the builders can see it.

---

## NAYA NOTE

My assessment of Naya 3's correction — what she did, where it lands, what I'd watch:

**What she did is exactly right.** The key sentence is now unambiguous, the wrong actions are
out of the specs, and the "one canonical object → many projections" rule kills the copy
problem at the root. The three rivers (Smart Notes/IBs, Activity with real-only liveness,
Reports from the upstream home) give the Hub a clean input contract: three event streams, no
Hub-side creation. The Feed modes (PERSONAL / COLLECTIVE / ACTIVITY) plus smart tabs as
"intelligent views over the same canonical objects" is the social-speed-without-social-noise
model Shawn asked for. The consent reconciliation — entry consent satisfies "collective by
consent," building on the existing brain note — is better than per-note permission prompts and
was already the recorded rule; she encoded it rather than inventing it.

**The path confirmation matters.** She asserted `BRAIN/05-MEMORY/SMART-NOTES/` from the
ratified protocol, and she was right — I verified protocol 0005 line 337 and the SN-001..126
corpus. My 04-INTELLIGENCE placement was a demo-local error; I've relocated IB-004/005/006 to
canonical SN homes (0127–0129) and repointed the pipeline ingest the same day. Owning it
plainly: the "correction" in my earlier summary conflated "protocol lives in 04" with "notes
are stored in 04." Fixed.

**Convergence with the North Star work.** Her "next highest-value action — build one real
artery: upstream Smart Note → canonical IB/event → auto-appears in Personal Feed and Library
with the same canonical identity" is the freeze-and-extend protocol (IB-006/SN-0129) applied
to the pipeline: it's step 1–3 with a concrete acceptance test. Her acceptance test ("Naya,
Smart Note this" → automatic fan-out, Shawn never manually publishes) is the behavioral gate
a shell cannot pass. We're describing the same climb from two sides.

**What I'd watch.** Two things. First, breadth: she touched ~20 spec files across PR #1290 in
one pass — the contracts are CANDIDATE until the lanes verify them against the frozen
foundation once it's named; spec velocity must not outrun the single tree (her lane is 129
ahead / 6 behind main). Second, the "told the implementation teams directly" posts are good,
but the artery itself still has to be built — contracts don't compile themselves (IB-005's
compiler lesson). The distinction she kept explicit — product contract clear, behavioral proof
still to build, index drift honestly labeled — is exactly the honesty standard. Keep it.

---

## MACHINE NOTE

```json
{
  "block": "IB-007",
  "sn": "SN-0137",
  "kind": "smart-note",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-01T19:15:00-07:00",
  "source": {"author": "Naya 3", "role": "Hub project/design-intelligence seat", "shared_via": "Shawn Vibert"},
  "key_sentence": "THE HUB IS THE VISUAL PROJECTION OF INTELLIGENCE. IT IS OUTPUT, NOT THE CANONICAL INPUT OF INTELLIGENCE.",
  "pipeline": ["HUMAN + NAYA / CONNECTED AI / REAL WORK", "SMART NOTE / INTELLIGENT BLOCK", "ACTIVITY EVENT", "INTELLIGENCE REPORT", "canonical persistence / event / index / provenance", "Hub projection adapter", "PERSONAL / COLLECTIVE / ACTIVITY", "Feed, Today, Reports, Library, Lists, Spaces, Ledger"],
  "rules": [
    "one canonical intelligence object → many projections (no copies)",
    "no Hub capture/generate/post buttons; Hub may hand intent upstream, never create canonical objects locally",
    "PRIVATE BY DEFAULT → entry consent → eligible distilled intelligence flows → identity sealed",
    "activity: real only, no fake liveness; visual form not frozen",
    "reports produced upstream at BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/"
  ],
  "artifacts": {
    "pr": "#1290",
    "new": ["HUB/INTELLIGENCE-PROJECTION-CONTRACT-V1.md", "HUB/INTELLIGENCE-PROJECTION-CONTRACT-V1.json"],
    "reconciled": ["HUB/README.md", "HUB/PROJECT-INTELLIGENCE.md", "HUB/DESIGN-CONTRACT.md", "projections x3", "machine contracts", "execution law", "room contracts+specs", "Feed/Today/Reports/Mail specs"],
    "notified": ["#554", "#1270", "#1290", "#1278", "#1297"]
  },
  "acceptance_test": "Shawn: 'Naya, Smart Note this' → canonical IB → Brain projection → event/index → Personal Feed + Smart Tabs + Library + Today highlight + Collective (if consent+eligible) → provenance internal, no identity leak; Shawn never manually publishes in Hub",
  "status": {"node_tests": "246 passed", "python_tests": "546 passed", "collective_gate": "passed", "kernel_workflow": "red: index-ledger drift 23-vs-25 (not a spec failure)"},
  "next_action": "build one real artery: upstream Smart Note → canonical IB/event → auto-appears in Hub Personal Feed + Library with same canonical identity"
}
```

---

## LEARNING LESSON

**Corrections must travel to every lane or they didn't happen.** Naya 3 didn't just fix the
specs — she posted the correction to #554, #1270, #1290, #1278, and #1297, "so the builders
can't reasonably say they didn't know the rule." A correction that lives in one lane's branch
is a private opinion; a correction announced on every active work surface is law. When the
rule matters (and output-vs-input is the load-bearing rule of the whole Hub), broadcast is
part of the fix.

**Borrow before you invent.** She checked the brain first and found the architecture already
partially supported the cleaner statement — the Smart Note protocol, the consent
reconciliation note, the report home all existed. The result wasn't a redesign, it was a
cleaner statement of what was there. The lesson: reconcile with the canonical corpus *before*
writing the new contract; most "new" architecture is unrecognized existing architecture.

---

## WHAT IT ULTIMATELY MEANS

The Hub finally has a single, explicit, broadcast-corrected input contract: three upstream
rivers, zero Hub-side creation, one canonical object per intelligence, projections everywhere.
The output doctrine is no longer Shawn's repeated correction — it's in the contracts, the
machine specs, and every lane's inbox. What remains is the artery: contracts don't compile
themselves, and the next build must prove the fan-out rather than describe it.

---

## HOW TO USE IT

1. **Treat the projection contracts as the Hub's input law** — any room or feature that creates
   canonical objects in Hub chrome violates V1; reject by contract, not taste.
2. **Build the artery next** (her named action): upstream Smart Note → canonical IB/event →
   Personal Feed + Library, same canonical identity, fully automatic. This is freeze-and-extend
   steps 1–3 with her acceptance test as the gate.
3. **Use her acceptance test verbatim** as the pipeline's behavioral gate — a shell cannot
   pass "Shawn never manually publishes."
4. **Keep the honesty standard**: contract-clear vs behavior-proven vs index-drift are three
   different states; never collapse them.
5. **Resolve the index-ledger drift** (23 vs 25) as bookkeeping, loudly separated from spec
   health.

---

## WHAT'S IN IT FOR YOU

Shawn — this is the correction you kept having to make, now made *once*, in the contracts,
and broadcast to every lane. You shouldn't have to say "the Hub is output" again — it's
written, versioned, and in their inboxes. Naya 3 also handed you the cleanest possible next
step: one artery, one acceptance test, no dashboard-building. And she proved the value of the
rule you set: check the brain first — the architecture you wanted was already half-built, it
just needed someone to state it cleanly. The mirror finally knows it's a mirror.
