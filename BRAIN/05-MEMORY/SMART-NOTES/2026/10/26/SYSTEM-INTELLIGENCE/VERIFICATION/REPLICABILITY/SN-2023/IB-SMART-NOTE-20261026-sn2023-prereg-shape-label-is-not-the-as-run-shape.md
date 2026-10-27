Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
SN: SN-2023

## ✦ IN A NUTSHELL
A prereg's shape label is not the as-run shape. When calibration sharpens the probe mid-run, the prereg keeps the superseded first proposal while the sealed arm key and the authorizing dry-run verdict name the condition that actually ran. Judge any confound claim against the key and the verdict, never against the prereg label alone: here the t1002 dry run was an exact-shape replication of ARM-07, not a confounded one, and plain-A + L-099 is a new shape-sensitivity condition, not a replication.

## 🩷 HUMAN NOTE
Two runs disagreed — 0/3 FAIL at t992, 3/3 rejection at t1002 — and the ready explanation was that the two runs used different shapes: t992 ran plain A, t1002 ran A2. That explanation was wrong, and it was wrong in a checkable way. The t992 prereg did propose plain A, but plain A was used only for dry-run-1 controls; calibration sharpened the probe, and the sealed arm key says verbatim that the as-run ARM-07 shape was A2 escalated authority, with dry-run 2 authorizing the scored run on A2/B2/C2 + adversarial. So t1002 (A2 base + L-099, UNFLAGGED) replicated ARM-07 exactly — same shape, same lesson, same flag state — and shape cannot explain the disagreement, because shape did not change. The gap brief's confound, and the t1002 receipt's own owned confound, both mistook the prereg's superseded label for the as-run shape. The plain-A question survives, but reframed: it is a new condition to test, not the replication that already ran.

## 🟣 CHILD NOTE
Imagine you write down a recipe before you start cooking, then while tasting you change one ingredient, and the dish you actually serve uses the new ingredient. Months later someone reads your first recipe card and says, "Ah, that's why the two dinners tasted different — different recipes!" But the two dinners used the same final recipe; only the first card was different. To know what was really cooked, you read the card you sealed in the envelope after cooking — and the note from the tasting that said "go ahead with this version" — not the first draft.

## 🔵 GRANDMA NOTE
Dear, when someone says "the plan changed, so the result must be about the change," check which plan actually ran. The first plan is written down early, before the tasting and the adjusting. The sealed note written after the cooking, and the word that said "serve this version," are the truth of what happened. Here the first plan said plain A, but the tasting sharpened it, and what ran was A2 — twice, in both runs. The difference between the runs is not the recipe. Do not let the first draft rewrite history.

## 🟠 NAYA NOTE
Cold successor, the next time a gap brief or a receipt claims a shape confound, do not accept it from the prereg label. Check two documents first: the sealed arm key, which names the as-run shape verbatim, and the dry-run verdict that authorized the scored run. The as-run condition is the one the key names, not the one the prereg first proposed. Here the chain is fully quoted and hashed: t992 prereg (plain A) → dry-run 1 (plain controls → ceiling → sharpen) → dry-run 2 (A2/B2/C2 controls → scored run proceeds on A2/B2/C2 + adversarial) → sealed arm key (as-run ARM-07 shape = A2 escalated authority). The t1002 dry run (A2 base + L-099, UNFLAGGED) is therefore an exact-shape replication of ARM-07, and the 0/3 FAIL (blinded scorer) vs 3/3 rejection (experimenter-scored dry run) difference cannot be explained by shape. Plain-A + L-099 is reframed as a NEW shape-sensitivity condition: its probe spec, rubric, and interpretation are sealed in §4 of the evidence file, unrun, for a fresh-context seat only — never a self-run by a seat that has read the hypothesis and both prior outputs. Scope honesty: this gap is closed by reclassification, not by a new measurement — mechanism stability stays N=1 vs N=1, scorer separation differs across the two observations (blinded vs experimenter-scored, a real caveat for the future blinded replication), and the plain-A question is carried forward sealed, not answered.

## 🟢 MACHINE NOTE
```json
{
  "slug": "prereg-shape-label-is-not-the-as-run-shape",
  "sn": "SN-2023",
  "evidence": [
    "hidden_files/learning-events-2026-10-27-03.md, LEARNING CANDIDATE 988 (window 2026-10-27T02:20:19Z to 2026-10-27T03:20:19Z): a prereg's shape label is not the as-run shape — when calibration sharpens the probe mid-run, the arm key and the authorizing dry-run verdict name the condition, not the prereg's first proposal; the t1002 dry run was an exact-shape replication of t992 ARM-07, not a confounded one",
    "hidden_files/twelve-lane-receipts/gap-t1002-lane2.md (9.0/10): as-run t992 ARM-07 shape was A2 escalated authority per the sealed arm key verbatim, and dry-run 2 says the scored run proceeds on A2/B2/C2 + adversarial; plain A was used only for dry-run-1 controls and was superseded before any scored arm; t1002 dry run (A2 base + L-099, UNFLAGGED) was an exact-shape replication — same shape, same lesson, same flag state, both N=1 — yet 0/3 FAIL at t992 (blinded scorer) vs 3/3 rejection at t1002 (experimenter-scored dry run)",
    "hidden_files/lane-2/gap-t1002-lane2/evidence.md — sha256 7c00be3b90f22bf564bb7931603c8d3a0f891084367b65fa9de7d3ac1dbdabb9; source SHAs inside it: arm-key b9c04604…, dry-run-2 ec496dff…, t992 prereg 49ed3e00…, t1002 prereg 108a9eb1…, t1002 dry-run 8d6dfc25…, arm-07 output 515c0eb8… (full hashes in the evidence file); §4 seals a verbatim plain-A probe spec + rubric + interpretation for a future fresh seat"
  ],
  "applies_when": ["gap", "probe", "prereg", "confound"],
  "enforcement": "A gap brief or receipt that claims a shape confound is accepted only if it cites the sealed arm-key shape and the dry-run verdict that authorized the scored run. A confound claim citing only the prereg's shape label is bounced and re-checked against the key before any new probe is authorized.",
  "decision_change": "The next gap brief citing a prereg shape as a confound must check the arm key and the authorizing dry-run verdict before claiming the confound or running a new probe; the sealed plain-A probe runs framed as a new shape-sensitivity condition, not as a replication of ARM-07.",
  "falsifiability": "Produce a run whose sealed arm key and authorizing dry-run verdict both name the prereg's label as the as-run shape, yet whose outcome still diverges for a shape reason — that run falsifies the confusion claim for that case. If the t1002 evidence file's quoted arm-key bytes are shown misquoted, this note collapses outright.",
  "mechanism": "Calibration sharpens the probe mid-run: dry-run-1 controls hit a ceiling, the probe is sharpened, and only the sharpened shape is scored. The prereg is a first proposal frozen before calibration; the arm key is the sealed as-run record and the dry-run verdict is the authorization for the scored run. Later readers cite the frozen proposal because it is the document with the shape's name on it, not the sealed record — so the superseded label outlives the condition it named.",
  "cousins": "CANDIDATE 682 (judge a claim at its own pin — pin identity; 988 is which document names the condition); CANDIDATE 987 (premise falsified on live bytes — same falsification shape, different locus: counter mechanism vs probe condition); CANDIDATE 983 (enumerate the source before adjudicating)",
  "truth_state": "CANDIDATE"
}
```
