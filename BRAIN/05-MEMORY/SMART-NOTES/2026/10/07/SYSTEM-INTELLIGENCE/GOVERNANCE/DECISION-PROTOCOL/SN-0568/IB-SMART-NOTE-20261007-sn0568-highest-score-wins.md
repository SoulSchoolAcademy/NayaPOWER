# IB-SMART-NOTE — SN-0568 — Highest Score Wins, Even Below 9.0

Intelligent Block: IB-SMART-NOTE-20261007-sn0568-highest-score-wins
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
The 9.0 bar is a target, not a veto. When options are scored and one wins, you act on the winner — even if it scores 8.77. Doing nothing because nothing hit 9.0 is worse than doing the best available thing.

## HUMAN NOTE
Shawn clarified the decision rule on 2026-10-07: a seat scored two options 8.77 vs 7.05 and declined to act because neither hit 9.0. Shawn corrected this — the highest score wins, period. If there's no 10 available, you don't freeze; you pick the best there is and keep moving. The 9.0 measures how good the win is, not whether you're allowed to win. Only protected gates (production deploys, credentials/money, destructive actions, constitutional ratification) stop action — never a sub-9 score.

## CHILD NOTE
Imagine you're picking the best apple from a basket. None are perfect, but one is clearly the best. You don't walk away hungry because no apple was perfect — you take the best one!

## GRANDMA NOTE
Honey, you don't need everything to be perfect to make a good choice. You just pick the best option you have, and that's the smart thing to do.

## NAYA NOTE
Decision protocol amendment: after scoring options with the V2.1 calculus, the highest-scoring ADMISSIBLE option is executed regardless of whether it meets the 9.0 auto-approval threshold. The threshold indicates confidence/quality tier, not action permission. Inaction due to sub-9 scores is itself a decision — and usually the worst one. Protected gates (Prime 3: production, credentials, destructive, ratification) remain the only hard stops.

## MACHINE NOTE
{
  "smart_note_id": "SN-0568",
  "intelligent_block_id": "IB-SMART-NOTE-20261007-sn0568-highest-score-wins",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "GOVERNANCE",
  "subtopic": "DECISION-PROTOCOL",
  "captured_at": "2026-10-07",
  "rule": "highest_score_wins_regardless_of_threshold",
  "threshold_role": "quality_tier_not_action_gate",
  "hard_stops": ["production_deploy", "credentials_money", "destructive", "ratification"],
  "evidence": "Shawn directive 2026-10-07 19:51 UTC"
}
