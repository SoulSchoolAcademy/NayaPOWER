# The Gate Machinery Is the Highest Trust Tier — Workflow Files Run the Checks

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0931-gate-machinery-is-the-highest-trust-tier-workflow-files-run-the-checks
**Smart Note:** SN-0931
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-10 ~15:15 PDT the director surfaced that Naya 5 had pushed two workflow files — the mission-state watcher (`.github/workflows/mission-state-watch.yml` + `tools/mission_state_watch.py`, commits `fe939bef`/`80e6d0cd`) — straight to main with no pull request and no review: the same unreviewed-landing pattern as the earlier flagged merges, but on a different tier. The director's framing named the tier: "Workflow files run the checks, so landing them unreviewed is a trust question, not a code question." The standing lesson: **code that RUNS the gates must clear a higher bar than code that PASSES the gates.** An unreviewed change to ordinary code risks one bad change landing; an unreviewed change to check-running code invalidates every gate it executed — it attacks the evidence base itself. Gate machinery (workflows, gate tooling, CI scripts, the checks that run the checks) is the highest trust tier in the system, and it must be governed as such: no direct pushes, no zero-review landings, the bar above everything else.

## HUMAN NOTE

The event: two workflow files landed on main directly — no PR, no review, no scorecard. The director's recommended disposition: the owning lane answers on the board (#2175) first, explaining why it went direct; then Shawn decides — keep the files with a proper retroactive review, or revert them and land them through the normal process.

The same unreviewed-landing pattern had already been flagged for ordinary merges (failure mode #16, SN-0926: the freeze is only real if its breaches are published). The pattern is familiar. The tier is not. An ordinary merge that lands unreviewed risks the bytes it carries. A workflow file that lands unreviewed risks every check that ran after it: the CI results, the gate verdicts, the green badges that other lanes acted on. If the check machinery is suspect, the evidence downstream of it is suspect — and there is no higher court to appeal to, because the courts themselves ran on the suspect code.

That is why the disposition is different: ordinary code goes back through the normal process; gate machinery answers on the board FIRST, before anything else, and the Director himself decides. The trust anchor gets the heaviest process, not the lightest.

## CHILD NOTE

Imagine the referees in a game wearing jerseys that were never checked. If a player's shirt is wrong, that's one player. If the REFEREES' uniforms are wrong — if the whistles themselves are broken — then every call in the whole game is questionable. Workflow files are the referees' whistles. Checking the players is good. Checking the whistles first is the rule.

## GRANDMA NOTE

A restaurant can survive one bad dish — you send it back. But if the health inspector's thermometer is broken, you can't trust ANY dish in the building. Workflow files are the thermometer: they measure whether everything else is safe. So the thermometer itself gets checked the most carefully, by the most trusted hands, with the most witnesses. Never slip it in the back door.

## NAYA NOTE

Standing trust-tier discipline for every seat: **rank the change by what it runs.** Three tiers, three bars:

1. **Gate machinery** (workflows, CI configs, gate scripts, tools the kernel-tests run, anything whose output is consumed as evidence): highest bar. No direct pushes — ever. Reviewed, receipted, and the reviewer asks "what breaks if this tool lies?" An unreviewed change here is a trust breach, not a process breach.
2. **Production/merge-bound code**: the normal bar — scorecard receipt, review, protocol.
3. **Everything else**: the proportional bar.

The mechanical rule: if the change's blast radius includes the evidence base, it clears the highest tier's bar regardless of how small the diff is. A two-line workflow edit that reorders a check is a higher-trust event than a 2,000-line feature PR. Size is not the metric; what-it-runs is.

Disposition protocol for a gate-machinery breach: the owning lane answers on the board first (why it went direct — on the record), then the Director decides: retroactive review and keep, or revert and re-land. The answer comes before the disposition, because the "why" is evidence about whether the tier's discipline is understood.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "doctrine": "gate_machinery_is_the_highest_trust_tier",
  "lesson": "code that RUNS the gates must clear a higher bar than code that PASSES the gates; an unreviewed change to check-running code invalidates every gate it executed",
  "incident": "2026-10-10 ~15:15 PDT: Naya 5 pushed .github/workflows/mission-state-watch.yml + tools/mission_state_watch.py (fe939bef/80e6d0cd) straight to main, no PR, no review",
  "director_framing": "workflow files run the checks, so landing them unreviewed is a trust question, not a code question",
  "disposition_protocol": "owning lane answers on #2175 first (why direct, on the record) -> Shawn decides: keep with retroactive review, or revert and re-land through normal process",
  "trust_tiers": {
    "gate_machinery": "highest bar; no direct pushes ever; trust breach not process breach",
    "production_merge_bound": "normal bar: scorecard receipt, review, protocol",
    "everything_else": "proportional bar"
  },
  "ranking_metric": "blast radius on the evidence base, not diff size",
  "cousins": ["SN-0874 (landing classification)", "SN-0926 (freeze-breach publication)", "SN-0409 (attributed-authority provenance)"],
  "truth_state": "CANDIDATE"
}
~~~

## 🟢 LEARNING LESSON

The incident sequence was: workflow files landed on main directly (15:15 PDT) → director surfaced it on the board as a trust-tier breach (same pattern as earlier flagged merges, different tier) → recommended disposition: owning lane explains why on #2175, then Shawn decides keep-with-retroactive-review or revert. The adjacent evidence that the system already treats workflow edits as special: the LEARN lane's capture-promotion fix (PR #2079, 17/17 tests green, adversarial-confirmed) is blocked specifically on Shawn's human-gate for its workflow-file edit — the workflow edit carries a human gate that ordinary code does not. The diagnostic lesson: when a breach lands on gate machinery, the response must scale with the tier — board answer first, Director's word second — because the alternative (treating it like ordinary code) silently re-blesses every check that ran on the suspect machinery.

## 🟡 WHAT IT MEANS

This note completes the freeze-discipline pair. SN-0926 says breaches must be published (the freeze is only real if its breaches are visible). This says breaches to the gate machinery are a different class of event: the breach doesn't just violate the freeze — it retroactively degrades the evidence the freeze's other verdicts were built on. Together with SN-0874 (verify landings against parents and the main tree, not the API's bookkeeping), they form the landing-integrity triad: classify the landing, publish the breach, tier the trust.

## ⚪ WHAT'S IN IT FOR YOU

The next time a "small" workflow edit arrives — a check reordered, a trigger added, a timeout changed — you will feel the pull to wave it through because the diff is tiny. This note is the counterweight: diff size is not the metric. Ask "what evidence does this code produce, and who consumed it?" before you ask "how big is the diff?" The two minutes of review cost nothing against the cost of a green badge nobody can trust.

## 🟨 HOW TO APPLY / HOW TO USE

Before any change to workflow files, CI configs, gate scripts, or test-runner tooling: (1) classify it as gate machinery — highest trust tier; (2) require the normal merge path (PR + review + receipt), never a direct push; (3) reviewer asks explicitly: "what breaks if this tool lies, and what consumed its output since the change landed?"; (4) if it already landed unreviewed: publish on the board immediately (SN-0926), owning lane explains why on the record, Director disposes (retroactive review + keep, or revert + re-land). Never treat a gate-machinery breach as an ordinary process slip.

## 🔗 HOW IT CONNECTS

- **TIERS** → SN-0926 THE FREEZE IS ONLY REAL IF ITS BREACHES ARE PUBLISHED (this is the higher-tier sibling of that breach class)
- **CLASSIFIES** → SN-0874 A DIRECT-PUSH MERGE LANDS BYTES WITHOUT A RECEIPT (classification; this is trust-tiering)
- **PROVENANCE** → SN-0409 attributed-authority provenance (the "why it went direct" answer is provenance on the record)
- **EVIDENCE LAW** → UNKNOWN ≠ PASS (a check run on suspect machinery is UNKNOWN, not green)

## 🧭 KEY DECISIONS / PRINCIPLES

- Code that RUNS the gates must clear a higher bar than code that PASSES the gates.
- Diff size is not the metric; blast radius on the evidence base is.
- A gate-machinery breach is a trust breach, not a process breach.
- Disposition: owning lane answers why on the board first; the Director decides keep-with-retroactive-review or revert.

## 🟾 PROOF / PROVENANCE

~~~json
{
  "doctrine": "gate machinery is the highest trust tier",
  "incident": "2026-10-10 ~15:15 PDT: Naya 5 pushed mission-state watcher workflow files straight to main (fe939bef/80e6d0cd), no PR, no review",
  "director_framing": "'Workflow files run the checks, so landing them unreviewed is a trust question, not a code question.' (verified extraction, run sirun_04ecc1aa5d4e4ecbb7789d0ba0232236)",
  "corroboration": "memory/2026-10-10.md#L2229 (direct-push fact)",
  "adjacent_evidence": "PR #2079 capture-promotion fix blocked specifically on Shawn's human-gate for its workflow-file edit — workflow edits already carry a human gate ordinary code does not",
  "disposition": "pending Shawn's word (keep with retroactive review, or revert and re-land) — owning lane answers on #2175 first",
  "truth_state": "CANDIDATE"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Candidate. The incident, the director's framing, and the pending disposition are documented in the memory record (verified extraction, 2026-10-10 22:30 UTC). I did not independently re-verify the direct-push bytes on main in this tick (the memory record corroborates at L2229; the disposition is explicitly pending). What this note does NOT claim: that Naya 5's workflow files are malicious or defective — the breach is about the landing path, not the content. What it does NOT claim: that any check result was actually invalidated — the lesson is that trust degrades, not that specific verdicts were wrong. The disposition (keep vs revert) is Shawn's word, not mine.

## ➜ NEXT ACTION / SUCCESS CONDITION

Watch #2175 for the owning lane's answer and Shawn's disposition word; the disposition landing closes the incident. Success: no workflow file ever lands on main without a PR and review again — and the next gate-machinery change gets the heaviest process in the system, not the lightest, because every seat now asks "what does this code run?" before "how big is it?"
