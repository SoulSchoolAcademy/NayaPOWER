Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
On the 3-task SURGE battery, three root-different mechanisms posted identical means (0.444) — the mean is a lossy projection that hides geometry. Experiment verdict tables must carry per-task ranks plus a rank-correlation between mechanisms; the ranks and the taus carry the information the mean erases.

## 🩷 HUMAN NOTE
The t1455 arm (symbolic presence-only concept sets) posted a mean HIT@5 of 0.444 — exactly the t1450 arm's (dense ask-body embeddings) 0.444, per-task-identical (0.333 / 0.667 / 0.333 on A/B/C). But the mechanisms are genuinely different: Kendall-tau(arm2-rankings, arm3-rankings) = 0.377 / 0.101 / 0.377 on A/B/C — B near-independent; arm3 flipped B to P12#1/P2#4 while demoting P2 to #4. A verdict that reads only the mean says "same result"; the ranks say "different machines, different failures". The 3-task battery's mean is too coarse to distinguish mechanisms — the per-task ranks and the taus carry the information. The rule from now on: every experiment verdict table carries per-task ranks and an inter-mechanism rank-correlation; a mean-only verdict table is an incomplete receipt. Both arms read FALSIFIED against TF-IDF 0.556 — the verdict survived, but the diagnosis (WHY they failed) lives only in the ranks.

## 🟣 CHILD NOTE
Two kids both scored 7 out of 10 on a test. One got all the hard questions right and the easy ones wrong; the other did the opposite. Same score, different brains. If you only look at the total, you'd think they think alike — but look at WHICH answers they got right and the difference is obvious. The lesson: never judge by the total alone. Keep the answer-by-answer list, and compare whose list looks like whose. Same score, different recipe.

## 🔵 GRANDMA NOTE
Imagine two cooks who both score 7 out of 10 in a contest — but one burns the soup and nails the dessert, while the other nails the soup and burns the dessert. The judges' total says "tie"; the dish-by-dish scores say two very different cooks. The lesson: never judge by the total alone — keep the dish-by-dish list, and compare whose list looks like whose. The total erases the story; the breakdown tells it.

## 🟠 NAYA NOTE
For every lane designing or scoring an experiment battery: the aggregate mean is a projection, not the measurement. When you seal a verdict, the verdict table carries (1) per-task scores/ranks and (2) a rank-correlation (Kendall-tau or equivalent) between each new mechanism and its predecessors. The t1455 tau table (0.377 / 0.101 / 0.377) is the worked example: identical 0.444 means, near-independent geometries on B. A verdict table that reports only means gets returned by the verdict reviewer (the blinded-recount seat) — incomplete receipts don't close experiments. File alongside SN-1342 (metric-blindness at battery design time) as its reporting-time cousin: SN-1342 cures blind metrics; this cures blind verdict tables.

## 🟢 MACHINE NOTE
{
  "id": "SN-1892",
  "slug": "coarse-means-hide-geometries",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-23",
  "lesson": "An aggregate battery mean is a lossy projection: root-different mechanisms can post identical means. Experiment verdict tables must carry per-task ranks plus an inter-mechanism rank-correlation (Kendall-tau or equivalent); the ranks and the taus carry the information the mean erases.",
  "evidence": [
    "twelve-lane-receipts/t1455-lane2.md (2026-10-23 13:55-14:07 PDT, t1455 Lane 2): arm3 (symbolic concept-set representation, stdlib-only, sealed pre-reg 21:00:17Z) mean HIT@5 0.444, per-task-identical to arm2 (dense ask-body) 0.444 — 0.333/0.667/0.333 vs 0.333/0.667/0.333. Kendall-tau(arm2-rankings, arm3-rankings) = 0.377 / 0.101 / 0.377 on A/B/C (B near-independent; arm3 flipped B to P12#1/P2#4). Both sealed falsifiers fired (F1: rank_arm3(P2 on B) = 4 > 1; F2: 1/3 tasks clear HIT@5 >= 2/3) — VERDICT FALSIFIED vs TF-IDF control 0.556. Receipt AGENT FEEDBACK prescribes the rule verbatim: verdict tables should carry the coarse-mean warning — identical means can hide different geometries; require per-task ranks + a rank-correlation between mechanisms in every verdict table."
  ],
  "decision_change": "Whether an experiment verdict table is complete: complete only with per-task ranks + inter-mechanism rank-correlation; a mean-only verdict table is returned as incomplete by the verdict reviewer.",
  "falsifier": "If future batteries with rank-level reporting never change any verdict the mean alone would have given (mechanism-geometry information never alters FALSIFIED / HOLDS-OPEN / CONFIRMED), the rank requirement adds no decision value and this lesson is falsified for verdict purposes. Also: if a battery mean is proven to be a sufficient statistic for the verdict decision on the corpus, the information-loss claim is refuted for that corpus.",
  "mechanism": "The mean is a projection operator from a rank vector to a scalar; different orderings project to the same scalar. Kendall-tau compares full orderings, preserving the ordinal structure the mean discards — so identical means with low tau = different geometries, and the per-task ranks name where they differ.",
  "applies_when": [
    ["experiment", "verdict"],
    ["surge", "measurement"],
    ["battery", "verdict-table"]
  ],
  "enforcement": "The SURGE verdict-table template in lane briefs requires a per-task rank row and an inter-mechanism Kendall-tau row; the blinded-recount / verdict-review seat bounces verdict tables that report only aggregate means (t1455 AGENT FEEDBACK prescribes exactly this: 'require per-task ranks + a rank-correlation between mechanisms in every verdict table')."
}
