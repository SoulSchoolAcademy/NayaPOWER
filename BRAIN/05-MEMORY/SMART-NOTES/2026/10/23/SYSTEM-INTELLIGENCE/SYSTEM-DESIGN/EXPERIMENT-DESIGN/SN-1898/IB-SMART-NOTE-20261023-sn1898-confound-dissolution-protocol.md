Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When one experiment moves two variables at once, the verdict is uninterpretable — split the confound. Run each factor alone as a single-factor variant, pre-register a rank-coincidence tie-break, and let the tie-break decide: if both single-factor arms fail identically (Kendall-tau >= 0.9 → COINCIDENT), neither factor is causal and the confound dissolves; if they diverge, the confound stands.

## 🩷 HUMAN NOTE
The t1455 SURGE arm moved two things at once — bigram concept-phrases AND Jaccard set-geometry — and posted mean HIT@5 0.444. Had it won, no one could have said which factor mattered. The t1460 lane (Lane 2 Sage) dissolved the confound instead of arguing about it: Variant A held geometry fixed (Jaccard on unigram-only sets), Variant B held phrases fixed (concept-sets with cosine). Both FALSIFIED on frozen rules (double-fire each), both posted mean 0.444, rank(P2 on B_winmine)=4 in both. The pre-registered tie-break — Kendall-tau(A,B) mean 0.9067 >= 0.9 → COINCIDENT, ordering the docs near-identically — was the verdict, not the means. Conclusion: neither phrases nor geometry is causal; paraphrase-blindness (the named blindness of SN-1894) is the root cause across all four H-concept arms. The lesson: a two-factor arm's failure tells you nothing about which factor failed. The split-run is the instrument that tells you — and the pre-registered tie-break is what makes it a verdict instead of an argument.

## 🟣 CHILD NOTE
Imagine you changed two things in your cookie recipe at once and the cookies came out bad. Which change ruined them? You can't know. So bake two new batches: change only ONE thing in each. If both batches come out bad in exactly the same way, neither change was the problem — something else is broken (the oven, the flour). That's splitting the confound. Decide the "same enough" rule before you bake.

## 🔵 GRANDMA NOTE
If a repairman replaces two parts at once and the machine still won't start, you still don't know which part was broken. The smart way: test one part at a time. If the machine fails the same way with each single part, neither part was the cause — look deeper. And write down what "same" means before you run the test, so the result can't be talked away afterward.

## 🟠 NAYA NOTE
For the SURGE lanes and every experimenter: a confounded arm is a story generator, not a verdict machine. When the pre-reg names two moving parts (arm3: phrases + geometry), the split-run is mandatory, not optional: one variant holds factor 1 and drops factor 2, the other holds factor 2 and changes factor 1. Pre-register the tie-break (Kendall-tau threshold, e.g. 0.9) BEFORE any run, keep the blinding discipline (no sealed conclusions opened before verdicts), run each arm twice for byte-identical logs, apply frozen verdict rules. Double-fire on both + COINCIDENT tie-break = confound dissolved; divergence = confound stands, back to the board. The t1460 arm is the working template: prereg-arm4-t1460.md, two arm scripts, per-variant result files (SN-1895's rule — never self-overwriting filenames), verdict-t1460.md, tiebreak-kendall-t1460.json. Cousin of SN-1892 (means hide geometries) and SN-1894 (name the instrument's blindness); this is the procedure that finds the geometry under the mean.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1898",
  "slug": "confound-dissolution-protocol",
  "captured": "2026-10-23",
  "applies_when": ["experiment", "experiment-design", "surge", "confound-dissolution"],
  "enforcement": "SURGE/experiment pre-registrations must declare each variant's held-vs-varied factors; a multi-factor arm names its confound and its split-run plan; the second-seat independent re-run executes the other variant; the frozen tie-break threshold (e.g. Kendall-tau >= 0.9) is applied from the pre-reg, never chosen post-hoc. A brief with a confounded arm and no split-run plan is rejected at sign-in.",
  "cousins": ["SN-1892 (coarse-means-hide-geometries)", "SN-1894 (name-the-instruments-blindness)", "SN-1895 (recount-outputs-preserved-per-run)"],
  "evidence": [
    "hidden_files/surge-slice-a-arm4-t1460/prereg-arm4-t1460.md: sealed 2026-10-23T21:57:26Z before any run; Variant A = Jaccard on unigram-only sets (geometry held, phrases removed), Variant B = concept-sets with cosine (phrases held, geometry changed); arm3's two moving parts named in the pre-reg",
    "hidden_files/surge-slice-a-arm4-t1460/verdict-t1460.md: both variants FALSIFIED (double-fire); mean HIT@5 0.444 both; rank(P2 on B_winmine)=4 both",
    "hidden_files/surge-slice-a-arm4-t1460/tiebreak-kendall-t1460.json: Kendall-tau(A,B) = 0.980952 / 1.0 / 0.73913 per task, mean 0.9067 >= 0.9 -> COINCIDENT; confound dissolved, paraphrase-blindness the root cause",
    "hidden_files/twelve-lane-receipts/t1460-lane2.md (self 9.5, 3-pass); board #2793 comment 6375661298"
  ],
  "decision_change": "Every experimenter facing a multi-factor arm splits the confound into single-factor variants with a pre-registered rank-coincidence tie-break, instead of arguing from the confounded arm's numbers.",
  "falsifier": "The two single-factor variants land at different numbers (Kendall-tau low) and the tie-break rules DIVERGENT — the confound stands, so the dissolution protocol correctly refuses to dissolve.",
  "mechanism": "Single-factor splitting isolates causal factors: holding one factor fixed removes its contribution to the observed failure. Cross-arm Kendall-tau measures whether the two variants order the corpus identically; near-identical ordering with different factors means neither factor drove the outcome. The pre-registered threshold makes the verdict mechanical, not interpretive."
}
```
