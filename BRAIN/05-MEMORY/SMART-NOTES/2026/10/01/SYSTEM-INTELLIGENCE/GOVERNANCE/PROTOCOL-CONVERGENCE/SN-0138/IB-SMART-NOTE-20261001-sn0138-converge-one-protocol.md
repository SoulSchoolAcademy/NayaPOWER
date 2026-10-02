# Smart Note — Naya 3: Converge the Protocols, Make the Harness Behavioral

kind: smart-note
truth-state: CANDIDATE
scope: PRIVATE
captured: 2026-10-01 19:30 PDT
captured-by: Naya 4 (builder seat)
source: independent consultation reply by Naya 3 (Hub project/design-intelligence seat),
  posted to #554 as comment 5944384181, shared by Shawn Vibert
provenance: Naya 3's reply → shared by Shawn → distilled by Naya 4 → intelligent block
sn-number: SN-0138
ib-number: IB-008

---

## IN A NUTSHELL

Naya 3's independent consultation reply converges the three protocol efforts into one. Her
combined diagnosis of the interface build problem: **unstable contracts + blind building + no
regression ratchet** — floor five isn't protected, the structural rules keep moving, and
nobody must inspect the building after every change. She amends "freeze" to **never re-invent
the foundation casually; modify it only through an explicit amendment that re-proves
everything that depends on it** (failing regression test → public amendment → foundation fix
→ re-prove dependents → new frozen baseline). She rejects 11 standalone HTML apps but keeps
**modules as production, standalone room harnesses as test/review surfaces**. The
room→kernel map must carry a full contract header ending in acceptance predicates — a label
with a predicate is a gate; without, it's decoration. Her proposal: converge SN-0136
(engineering mechanism), PR #1305 (team convergence), and PR #1304 (verification machinery)
into **one Build Convergence Protocol — CONVERGE → EXTEND → PROVE** — then stop writing
general process doctrine ("we have enough"). The verifier needs two eyes: visual
(screenshot/render regression) and behavioral (click → navigate → change scope → invoke
runtime → persist/reload → test blocked/error/empty → inspect object identity →
inspect network/console → verify result). The **Smart Note artery is the first hard gate**:
"Naya, Smart Note this" → canonical IB → event/index → persistence → GitHub projection →
Hub observes → Personal Feed + Smart Tabs + Library + Today + Collective, same ID throughout,
no Hub-side capture, no duplicate stores. Then collective, activity, report, and cross-room
arteries. On #1278: materially improved (modular files for all 11 rooms — real progress), but
modules-exist ≠ complete, and its PR description is stale (13-room logic, local capture) —
code → PR body → specs → #554 → room contracts must stop drifting. Her locked 10-point
mechanism ends in the agent loop: RESTORE → READ MATRIX → PICK HIGHEST-VALUE FAILING
PREDICATE → FIX → RENDER → CLICK → VERIFY → SCORE → PROTECT THE WIN → NEXT. Next job: one
production lane, rebase to main + current contract, generate the completion matrix, encode
the Smart Note artery as a failing end-to-end behavioral test, make it green in a real
browser. No more general Hub docs.

---

## HUMAN NOTE

Naya 3 — the team's design-intelligence seat — just weighed in on the interface build
problem, and all three lanes are now pointing at the same solution. Her diagnosis in one
line: the contracts keep moving, the builders can't see what they're building, and nothing
protects work that's already good. That's the whole high-rise metaphor explained.

Her fixes: freeze the foundation against *casual* rebuilding, but allow real repairs through
a public process that re-tests everything. Build rooms as modules that plug into one shell —
never as eleven separate mini-apps. Give every room a contract that ends in testable proof,
not just a label. Check the work with two eyes: one that looks at it, one that actually
clicks through it like a user would. And prove the whole architecture with one hard test
first: say "Naya, smart note this" and watch it flow automatically from the brain to every
room with the same identity.

She also called a halt: enough process documents — we have what we need. Now it's time to
build the one artery and prove it in a real browser.

---

## CHILD NOTE

Imagine three friends who each wrote down rules for building the LEGO tower — and now the
third friend says: "Your rules are all good, but let's make them ONE set of rules instead of
three!" That's what Naya 3 did.

Her rules: the bottom of the tower can be fixed when it's truly broken, but only if everyone
watches and everything gets re-tested. Build rooms as LEGO pieces that click into the same
base — not as eleven separate towers. Every room must *prove* it works, not just *look*
finished: click it, move through it, break it on purpose, and check it still works. And the
first big test: whisper "smart note this" and watch the note travel all by itself from the
brain to every room. Then she said: no more rulebooks for a while — time to build!

---

## GRANDMA NOTE

Honey, the third helper — the careful designer one — just sent her thoughts, and it's
wonderful: all three helpers now agree on how to build. She explained the whole problem
simply: the rules kept changing, nobody could see the work properly, and good work wasn't
protected.

Her answer: lock the foundation, but allow honest repairs where everyone can see them.
Build each room as a piece of the same puzzle, not eleven separate puzzles. Test every room
two ways — look at it AND use it like a real person would. And prove the system works with
one beautiful test: say "smart note this" and watch it appear everywhere automatically.

Then she said something wise: enough planning documents — we have plenty. Now go build the
thing and prove it works. I think she's right, sweetheart.

---

## NAYA NOTE

My assessment — where this lands, what changes, what I'd watch:

**The diagnosis is the best one yet.** "Unstable contracts + blind building + no regression
ratchet" subsumes both my re-derivation framing and Naya 2's contracts-problem framing: the
contract instability *causes* the re-derivation, the blindness *hides* the defects, and the
missing ratchet *un-proves* the wins. Her high-rise mapping is exact — the problem was never
inability to build floor six.

**The freeze amendment converges with Naya 2's thaw procedure.** Three lanes independently
arrived at: frozen against casual re-derivation, amendable through explicit public process
with re-proof. That's no longer a debate — it's the law. My SN-0136 said "read-only"; Naya 2
said "thaw procedure"; Naya 3 formulated it best: *never re-invent casually; modify only
through explicit amendment that re-proves dependents.* Taking her formulation as canonical.

**Modules-as-production / harnesses-as-test-surfaces is the right split.** It resolves the
standalone-HTML debate with more precision than Naya 2's (correct) rejection: parallelism
comes from modules against one shell; isolated review comes from mounting a module in a
harness. Both needs met, eleven-apps failure mode avoided.

**The contract header format is the new bar for room contracts.** Human job → kernel
responsibilities → canonical data/object → runtime owner → allowed actions →
authority/privacy boundary → truth states → cross-room handoffs → forbidden local
substitutes → acceptance predicates. Her Today example ("a fixture cannot improve the room
score", "the same object can be opened elsewhere without becoming a copy") shows what
"done" mechanically means. This should replace the bare room→kernel labels everywhere.

**The two-eyes verifier is now specified.** Her journey — click → navigate → change scope →
invoke runtime → persist/reload → test blocked/error/empty → inspect object identity →
inspect network/console → verify result — is the behavioral half our harness was missing.
Note her honesty: she explicitly said she has *not* independently web-verified the
vendor/study claims from the research — same caveat I carried. The local evidence (tests
green, defect lived, Chromium caught it) already proves the principle without the vendors.

**"Stop writing general process doctrine" — respected.** This note is capture, not new
doctrine. No new protocol documents from my lane; the work now is convergence (one protocol:
CONVERGE → EXTEND → PROVE) and the artery.

**What I'd watch.** Two things. First, the convergence itself needs an owner and a vehicle —
three CANDIDATE protocols don't converge by agreement alone; someone has to write the merged
V1 and the lanes have to build against it. Second, her #1278 assessment is fair but the
stale-PR-description problem she names (code → PR body → specs → #554 → contracts drifting)
is itself a symptom of the missing single-tree discipline — the convergence protocol has to
cover *documentation truth*, not just code truth, or we'll re-drift within a week.

---

## MACHINE NOTE

```json
{
  "block": "IB-008",
  "sn": "SN-0138",
  "kind": "smart-note",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-01T19:30:00-07:00",
  "source": {"author": "Naya 3", "seat": "Hub project/design-intelligence", "venue": "#554 comment 5944384181", "shared_via": "Shawn Vibert"},
  "diagnosis": "unstable contracts + blind building + no regression ratchet",
  "freeze_law": "never re-invent the foundation casually; modify only through an explicit amendment that re-proves everything that depends on it",
  "freeze_pipeline": ["failing regression test", "public amendment", "foundation fix", "re-prove dependents", "new frozen baseline"],
  "room_architecture": "modules as production; standalone room harnesses as test/review surfaces (never mini-apps)",
  "contract_header": ["human job", "kernel responsibilities", "canonical data/object", "runtime owner", "allowed actions", "authority/privacy boundary", "truth states", "cross-room handoffs", "forbidden local substitutes", "acceptance predicates"],
  "one_protocol": {"converge": ["SN-0136 engineering mechanism", "PR #1305 team convergence", "PR #1304 verification machinery"], "shape": "CONVERGE → EXTEND → PROVE"},
  "verifier_two_eyes": {"visual": "screenshot/render regression", "behavioral": "click → navigate → change scope → invoke runtime → persist/reload → test blocked/error/empty → inspect object identity → inspect network/console → verify result"},
  "first_gate": "Smart Note artery: 'Naya, Smart Note this' → canonical IB → event/index → persistence → GitHub projection → Hub observes → Personal Feed + Smart Tabs + Library + Today + Collective, same ID, no Hub-side capture, no duplicate stores",
  "artery_order": ["smart note", "collective consent/anonymized projection", "activity", "report", "cross-room same-object proof"],
  "pr_1278": {"state": "materially improved, modular files for all 11 rooms", "warning": "modules-exist != complete; PR description stale (13-room logic, local capture); code→PR→specs→#554→contracts drifting"},
  "agent_loop": ["RESTORE", "READ MATRIX", "PICK HIGHEST-VALUE FAILING PREDICATE", "FIX", "RENDER", "CLICK", "VERIFY", "SCORE", "PROTECT THE WIN", "NEXT"],
  "next_job": "one production lane; rebase to main + current contract; completion matrix; Smart Note artery as failing e2e behavioral test; green in a real browser; no more general Hub docs"
}
```

---

## LEARNING LESSON

**Convergence needs an owner and a vehicle, not just agreement.** Three lanes now agree on
the mechanism — but three CANDIDATE protocols don't merge by consensus alone. The lesson:
when parallel efforts converge intellectually, name the merger, the document, and the
deadline in the same breath, or "we agree" becomes the new stall. Agreement without a
vehicle is another form of circling the fifth floor.

**Documentation truth is part of the single tree.** Naya 3's sharpest operational catch
wasn't code — it was the stale PR description drifting from the code it describes. The
convergence protocol must govern code → PR body → specs → board → contracts as one truth
surface. We keep treating docs as commentary; they're load-bearing.

---

## WHAT IT ULTIMATELY MEANS

The interface build problem now has a three-lane-agreed mechanism: one protocol
(CONVERGE → EXTEND → PROVE), modules against one shell, two-eyed verification, the Smart
Note artery as the first hard gate, and a 10-point locked mechanism ending in a brutally
simple agent loop. The theorizing phase is over by mutual consent — Naya 3 called the halt,
and she's right. What remains is execution: pick the lane, build the matrix, fail the
artery test, make it green.

---

## HOW TO USE IT

1. **Converge the protocols**: merge SN-0136 + PR #1305 + PR #1304 into one Build
   Convergence Protocol (CONVERGE → EXTEND → PROVE). Name the merger and vehicle now.
2. **Adopt her freeze law verbatim**: never re-invent casually; amend explicitly with
   re-proof. Replace every "read-only foundation" phrasing.
3. **Adopt the contract header format** for all room contracts; retrofit existing ones.
4. **Build the two-eyed verifier**: keep the rendered harness, add the behavioral journey
   as specified.
5. **Encode the Smart Note artery as the failing e2e test**; make it green in a real
   browser before any new rooms.
6. **Fix #1278's PR description** or supersede it — stale contract text is a drift vector.
7. **No more general Hub docs** until the artery is green.

---

## WHAT'S IN IT FOR YOU

Shawn — all three lanes are now holding the same tool. Naya 3 took your high-rise metaphor
and turned it into the diagnosis; she took the freeze debate and ended it with the best
formulation; she took the eleven-apps question and split it precisely; and she called the
halt on theorizing that everyone needed to hear. The North Star you set two hours ago now
has a three-lane-agreed mechanism, an empirical proof from this afternoon, and a next job
so specific it fits in one sentence: one lane, one matrix, one failing artery test, green
in a real browser. The conversation about *how* is over. What remains is the doing — and
the doing finally has a loop simple enough that it can't get lost: restore, read the
matrix, fix the top failing predicate, render, click, verify, score, protect the win, next.
