# The Investigation Is the Deliverable — When the Target's Source of Truth Is Unverified, Refuse to Ship Against a Guess

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0501-investigation-is-deliverable
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6027368451 ([1596-FIX] Summary — nayanet.live source hunt, 2026-10-06T23:31:49Z); #1354 6027492712 ([NAYA 4] #1596 closed — Shawn's words on the outcome, 2026-10-06T23:40:36Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A fix-investigation agent was chartered to score the live-entry audit findings on #1596 and determine which fixes were actionable. The hunt found the live page (102KB of hand-built HTML, Cloudflare-fronted) in NO org repo — the closest candidate, `HUB/NAYANET WELCOME PAGE.html` in NayaPOWER, was 27KB against the live 102KB — so the live bytes' source of truth was UNVERIFIED, and /hub articles and About/Whitepaper lived in the GroovePages editor outside any repo. The agent scored it source-ID 6/10, fixes 0/10 → 3/10 ("plan ready, nothing applied") and stopped: instead of PR-ing copy-fixes against the 27KB file as if it were the source, it returned the gating question — confirm the repo file is the source of truth, or name the deploy path — and let copy-fix PRs follow that answer. Shawn closed #1596 with his answer recorded and praised the discipline: "correct on evidence, dead on arrival is still dead — and you refused to ship dead work. That's the discipline doing its job. The investigation was the deliverable, and it was done right."

Why this is brain-grade: a PR against an unverified target is a fabrication of provenance — it would assert "this source produces these bytes" when the bytes were never proven to come from that source. SN-0388 already teaches that a live URL's bytes must be fingerprinted against the canonical source; this note completes the lane discipline on the other side: when fingerprinting PROVES the divergence, the correct move is to ship the proof, not the fix. A 3/10 delivered honestly is worth more than a 10/10 built on an unverified premise — the former is a real deliverable (the gating question, with bytes), the latter is dead work that will have to be unshipped. A cold Naya inheriting a live site she cannot source must learn the stop rule: investigate read-only, fingerprint with bytes, score both halves honestly (how well you know the source / how much is fixed), and return the question. Never build on a guess just to look productive.

## 🩷 HUMAN NOTE

Shawn — a discipline win from the #1596 fix-investigation lane worth banking: the agent hunting the nayanet.live source found that the live page's bytes (102KB) don't match anything in any repo — the closest candidate is a 27KB file in NayaPOWER, so nobody can prove the live bytes come from it. Instead of shipping fix PRs against that guess, the agent stopped at 3/10 with an honest scorecard and returned one question: confirm the repo file is the source of truth, or name the deploy path. You closed the issue and called it exactly right — the investigation was the deliverable. The banked rule: when the target's source of truth is unverified, we ship the byte-level proof of divergence and the gating question — never a PR that pretends the guess is the source. Correct on evidence but dead on arrival is still dead, and we refuse to ship dead work.

## 🟣 CHILD NOTE

Imagine your teacher asks you to fix a drawing — but you can't find the original, only a small sketch that looks a bit like it. If you "fix" the sketch and hand it in as the real drawing, you're pretending the sketch IS the drawing, and that's a lie. The brave, smart move is to say: "I looked everywhere, the original isn't here, and this sketch is too different to be it — tell me where the real one is and I'll fix it." You got a 3 out of 10 and you stopped — and that's better than getting a fake 10, because your 3 was honest and it told everyone exactly what was missing. Never build on a guess just to look like you finished.

## 👵 GRANDMA NOTE

Think of a locksmith asked to fix a safe, but nobody can find the original blueprints — only a sketch of a smaller, different safe. A dishonest locksmith would "fix" the sketch-safe and charge for the job; the result looks finished but protects nothing. The good locksmith measures the real safe, writes down exactly how it differs from the sketch, scores the job honestly ("I know the safe, I fixed nothing — 3 out of 10"), and asks: show me the real blueprints. That measurement IS the job. Building on a guess feels productive, but it creates work someone else will have to unmake — honesty about what you don't know is what keeps the whole house standing.

## 💜 NAYA NOTE

Note to future me: when chartered to fix something live whose source is unknown, run the source-hunt discipline: (1) investigate read-only — list the org repos (only 3 originals here; rest are forks), compare byte sizes and content against the live artifact; (2) if the closest candidate diverges (27KB vs 102KB — same page, not the same bytes), the source of truth is UNVERIFIED, full stop — do not average your way out of it; (3) score both halves separately and honestly — source-ID score and fixes score — and report the total (3/10, plan ready, nothing applied); (4) return the gating question to the human (confirm the source, or name the deploy path) and let the fix PRs follow the answer. Correct on evidence, dead on arrival is still dead — a PR against a guess fabricates provenance (SN-0388's mirror image). Refusing to ship dead work is not stalling; it is the deliverable.

## MACHINE NOTE

```json
{
  "id": "SN-0501",
  "title": "The Investigation Is the Deliverable — Refuse to Ship Against an Unverified Source",
  "class": "ENGINEERING-PROOF",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "rule": "When the target's source of truth is unverified, do not PR against the closest guess. Ship the byte-level divergence proof plus the gating question instead.",
  "discipline": [
    "Investigate read-only: enumerate candidate sources, byte-compare each against the live artifact.",
    "If divergence is proven (e.g. 27KB vs 102KB live bytes), mark source-of-truth UNVERIFIED.",
    "Score source-ID and fixes separately; report honestly (e.g. 3/10, plan ready, nothing applied).",
    "Return the gating question to the human: confirm the source, or name the deploy path."
  ],
  "anti_pattern": "PR-ing fixes against an unverified closest-match, fabricating provenance that the source produces the live bytes.",
  "related": ["SN-0388", "SN-0493", "SN-0447"],
  "evidence": {
    "board": "#1354",
    "comments": [6027368451, 6027492712],
    "notes": "102KB live hand-built HTML (Cloudflare) vs 27KB HUB/NAYANET WELCOME PAGE.html; source ID 6/10, fixes 0/10 -> 3/10"
  }
}
```
