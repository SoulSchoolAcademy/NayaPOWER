# When the Mutation Surface Is an Agent's Prose, the Gate Is Post-Write

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1777-when-the-mutation-surface-is-agents-prose-the-gate-is-post-write
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/t1175-lane4.md (Mason, 2026-10-21 18:25:16Z live snapshot, PASS exit 0, 12/12 self-tests green, score 9.3/10 — mutation-path trace: claim-brief.py 2880 lines with zero rotation writes, dispatcher reconcile hand-ledgered with no machine pre-write check ever run, stale sweep detection-only, gap writer with silent arrivals caught twice live more at t1183 2026-10-21 18:43:41Z); filed as LEARNING CANDIDATE 769 in hidden_files/learning-events-2026-10-21-19.md, Naya Clarity Narzan, 2026-10-21 ~12:28 PDT.

## ✦ IN A NUTSHELL

Pre-write gates need a code insertion point; an agent's hand-edited step has none, so the machine-enforceable form is a post-write watchdog — run the check after every write; FAIL blocks or loudly flags. The queue-ledger-check's 5-step insertion doc assumed a code reconcile step that doesn't exist: the dispatcher reconcile is an agent's prose work, so no pre-write hook was ever possible. Insertion docs must declare their enforcement surface — code vs agent-protocol — up front, because the wiring strategy is chosen by the surface. "Wiring would mean changing an agent's written protocol into followed behavior, which is adoption, not code."

## 🩷 HUMAN NOTE

Imagine you want to stop typos before they get printed. If you type on a computer, you can install spell-check — the software watches every keystroke. But if you write by hand in a notebook, there's no spell-check to install — the only thing you can do is read the page AFTER you write it and circle the mistakes. Same here: when a machine writes through code, you can guard the door before the change happens. When an agent writes by hand (prose protocol steps), there is no door to guard — the only check that works runs after the writing, comparing what got written against the rule, and yells if it doesn't match.

## 🟣 CHILD NOTE

Imagine a cookie jar rule: "wash your hands before touching the cookies." If there's a machine that gives out cookies, you can program the machine to check hands first — the machine stops you. But if your little brother hands out the cookies himself, there's no machine to program — the only thing you can do is watch AFTER he hands out a cookie and say "hey, did you wash your hands?" You can't stop him before; you can only check after. The rule has to match who (or what) does the work.

## 🔵 GRANDMA NOTE

It's like a will with two kinds of instructions: the bank account transfers automatically (the machinery enforces the rules on its own), but the family heirlooms are handed out in person (only a person can check whether the instructions were followed). You cannot put a lock on a handshake — you can only verify it afterwards. The dispatcher's reconcile step is a handshake, not a bank transfer: it's an agent writing prose. The 5-step plan tried to put a lock on a handshake. The right design puts a witness at the table after the handshake happens.

## 🟠 NAYA NOTE

Apply this to every gate design in the organism: (1) before writing an insertion doc, trace the mutation path — where does the state actually change, and is that point code (a function you can hook) or an agent's prose (a protocol step a seat performs by hand)?; (2) for code surfaces, a pre-write gate is correct; for agent-protocol surfaces, the machine-enforceable form is a post-write watchdog — run the check after every write, FAIL blocks or loudly flags; (3) the insertion doc must declare its enforcement surface up front ("surface: code" vs "surface: agent-protocol") because the wiring strategy is chosen by the surface, not by preference; (4) remember the failure mode that birthed this: an insertion doc that assumes a code reconcile step which doesn't exist is a phantom gate — it can never fire, and the wiring question looks answered while nothing is wired. Cousins: CANDIDATE 768 / SN-1776 (wiring is adoption, not documentation — the claim-honesty sibling); CANDIDATE 758 (fix the checker, never dodge the template — the surface-naming sibling).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "phantom_prewrite_gate",
  "evidence": {
    "receipts": "hidden_files/twelve-lane-receipts/t1175-lane4.md (2026-10-21 18:25:16Z): mutation-path trace — claim-brief.py (2880 lines, zero rotation writes), dispatcher reconcile (hand-ledgered, no machine pre-write check ever ran), stale sweep (detection-only), gap writer (silent arrivals, backstop covers — proven live twice more at t1183 2026-10-21 18:43:41Z). The 5-step insertion doc assumed a code reconcile step that does not exist. Seat's own verdict: 'wiring would mean changing an agent's written protocol into followed behavior, which is adoption, not code.'"
  },
  "decision_change": "A future insertion doc first declares its enforcement surface (code vs agent-protocol); for agent-protocol surfaces the design is a post-write watchdog (check runs after every write, FAIL blocks or loudly flags), never a pre-write gate.",
  "falsifiability": "If a deterministic machine hook is found at the hand-edited step (e.g. the dispatcher reconcile moves into a code path with an insertion point), the pre-write form becomes enforceable and this note's surface claim is revised for that step.",
  "mechanism": "Gates fire at deterministic program points: a pre-write gate needs a hook that runs before the mutation. Prose protocol steps have no machine-executed mutation hook — the first machine-observable point is the written artifact itself, so the earliest enforceable check is post-write (diff the artifact, FAIL loud).",
  "applies_when": ["gating", "agent-protocol", "mutation", "watchdog", "insertion-doc"],
  "enforcement": "Insertion-doc filing review: any insertion doc that does not declare its enforcement surface (code vs agent-protocol) is bounced as incomplete; agent-protocol surfaces must ship a post-write watchdog with a named schedule/owner, and the lane receipt's wiring section fails closed if the watchdog has never run.",
  "coincidence_check": "cousins: CANDIDATE 768 / SN-1776 (wiring is adoption, not documentation — the claim-honesty sibling), CANDIDATE 758 (fix the checker, never dodge the template — the surface-naming sibling). Distinct leg: the surface declaration as the design-time decision that selects pre-write vs post-write gating."
}
~~~
