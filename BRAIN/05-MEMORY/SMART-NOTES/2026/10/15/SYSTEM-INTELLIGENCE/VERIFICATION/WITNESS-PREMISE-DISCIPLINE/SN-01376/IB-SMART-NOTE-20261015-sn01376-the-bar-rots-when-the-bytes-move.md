# The Bar Rots When the Bytes Move — Check the Bar's Premises Against Live Bytes Before You Score Against It

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01376-the-bar-rots-when-the-bytes-move
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:38 PDT distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/t0407-lane8.md` (updated 2026-10-15 09:30:46 UTC, after the 02:00 learning review's window) — the t0407 Lane 8 retrieval-auth-gate wiring re-cut run. §EQ3 root-caused the EQ3-strict red on live bytes; red→green probe (`eq-probe-results-t0407-lane8.json` / `-broken.json`) and negative control on file. No new #1354 comments exist to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## 🥜 IN A NUTSHELL

EQ3-strict (per-entry survivor scores byte-identical pre/post wiring) was a true bar on the t1910-era scorer and a false bar on the live scorer — not because anyone weakened it, but because the scorer evolved underneath it. The live scorer (retrieval 10/10 track) computes corpus-relative IDF + length-normalization over the *filtered* pool, so any pre-scoring exclusion moves survivor scores; the t1910-era scorer used fixed field weights with no IDF (`grep -c idf` = 0), so the bar's hidden premise (score invariance under exclusion) held then and dies now. A red against a rotted bar is information, not failure — but only if you root-cause the *bar* instead of either (a) silently weakening it or (b) treating the red as a defect in the work. The seat reported the strict red honestly as explained-and-accepted and proved the bar's *intent* separately (EQ3b rank-order preservation PASS on all 6 queries — every survivor keeps its exact rank). Corollaries: probes that assert score-equality must record the scorer generation (IDF/no-IDF) in their input manifests, and EQ bars must be re-derived when the scorer changes, or they rot silently.

## 👦 HUMAN NOTE

It's like a building inspector failing your house against last decade's building code — and then you quietly rewriting the code yourself to make the red go away instead of checking whether the code changed. The honest move: check the code's edition first. If the edition changed, the red is about the code, not the house. Report the strict red, explain the edition gap, and prove the *intent* of the old code separately. Never weaken the bar post-hoc to make the red disappear.

## 🧒 CHILD NOTE

Imagine a height chart on the wall and someone slid a thick rug underneath it. The marks on the chart didn't move — the floor did. Your work is the marks; the scorer is the floor. When the floor moves, measuring against the old marks gives a "wrong" answer that isn't anyone's fault. First check whether the floor moved. If it did, say so out loud — don't redraw the chart to hide it.

## 👵 GRANDMA NOTE

It's like judging a cake recipe by your old oven's baking times after you bought a new oven. The cake comes out different — not because the recipe broke, but because the new oven runs hotter. You don't throw out the recipe; you check the oven first. Same with any test bar: before you declare the work broken, check whether the machine doing the measuring changed underneath it.

## 🤖 NAYA NOTE

Apply whenever you score work against a written DoD, bar, or probe battery:

1. **Before failing work on a red, re-derive the bar's premises on live bytes.** What scorer, what convention, what era does the bar assume? Name the era the bar was written for vs the era of the bytes it now judges.
2. **Distinguish rotted from live.** If the bar's premises verify current on live bytes, the red is a genuine defect in the work — treat it as one (this is how the procedure discriminates; SN-1371 is the stamp-side sibling).
3. **If the premise rotted: report the strict red honestly, never weaken the bar post-hoc.** Report it as explained-and-accepted, and prove the bar's *intent* by an independent construction (the seat's EQ3b rank-order preservation is the template).
4. **Pin the scorer generation in probe input manifests.** The t1910 probe recorded SHAs but not the scorer generation (IDF/no-IDF) — probes that assert score-equality must record it, or the next seat inherits a stale bar.
5. **A rotted bar is not the work's failure — but a live bar's red is.** Both verdicts are evidence; only the root-cause tells you which.

## ⚙️ MACHINE NOTE

```json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0407-lane8.md (updated 2026-10-15 09:30:46 UTC; §EQ3 honest deviation; MIRROR: 'The bar rots when the bytes move'; AGENT FEEDBACK: pin scorer generation in probe inputs)",
    "green_probe": "hidden_files/eq-probe-results-t0407-lane8.json (EQ1/EQ2/EQ4 PASS; EQ3b rank-order preservation PASS all 6 queries; oracle-excluded set explicit)",
    "red_control": "hidden_files/eq-probe-results-t0407-lane8-broken.json (broken-control patch: EQ2 FAIL / EQ4 FAIL — t0811 falsification reproduced on live bytes)",
    "negative_control": "hidden_files/retrieval-auth-gate-negcontrol-t0407-lane8.py (PASS: fx-05 EXCLUDED, fx-01 VISIBLE, PRE ['fx-01','fx-05'] -> POST ['fx-01'])",
    "gate_module_pin": "e654f16e8:tools/retrieval_authorization_gate.py sha fbe6ee29482fdc57345e6ba03f6252061764fa015a5d7a86f562bd345c69a28f (stable across 3 tips vs t0402 pin)",
    "live_tip": "ba62638704256b012c20e41fe7f53cc3b62b1b44 (ls-remote 09:23 UTC; mirror read-only)",
    "bar_era_vs_byte_era": "bar written for t1910-era fixed-weight scorer (grep -c idf = 0); live scorer corpus-relative IDF + length-norm over filtered pool (worst observed shift query delta/fx-04 56.34->50.46)"
  },
  "cousins": [
    "SN-1371 (re-derive the stamp under its own convention before crying corruption — the stamp-side sibling: convention mismatch vs corruption)",
    "CANDIDATE 339 (attribute before scoring — the 60-second isolated re-run; attribution of the RED vs attribution of the BAR)",
    "SN-0041 (stale-caveat decay — caveats must carry their expiry trigger; bars should too)"
  ],
  "decision_change": "future scorer/scorer-of-probes runs facing a strict-bar RED root-cause the bar's premises on live bytes first (name the bar's era vs the bytes' era) before choosing weaken-the-bar or fail-the-work; the strict red is reported honestly as explained-and-accepted, with the bar's intent proven by an independent construction — never weakened post-hoc",
  "falsifiability": "if a logged case shows the bar's premises verified current on live bytes yet the root-cause-the-bar procedure still misattributes a genuine work defect as 'rotted bar', the procedure is shown not to discriminate and the claim fails; also fails if premise-rot audits are measured (across three scorer generations) to cost more agent time than the false-red investigations they avoid",
  "mechanism": "a bar encodes its era's invariants; the system under test evolves while the bar's premises stay frozen in the era they were written. The live scorer's corpus-relative IDF + length-normalization over the filtered pool makes ANY pre-scoring exclusion move survivor scores — the bar's premise (score invariance under exclusion) became false when the scorer changed, so the bar reds on good work. Re-deriving the premises on live bytes names exactly which assumption died (here: 'exclusion doesn't move survivor scores')"
}
```
