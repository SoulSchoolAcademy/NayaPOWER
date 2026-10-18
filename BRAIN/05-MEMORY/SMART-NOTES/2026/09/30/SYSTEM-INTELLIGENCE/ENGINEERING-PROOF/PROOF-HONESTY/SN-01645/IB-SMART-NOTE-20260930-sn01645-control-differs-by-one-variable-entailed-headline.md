Intelligent Block: SN-01645
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

IN A NUTSHELL
A control must differ from the thing it controls by exactly one variable — and a control that can't move isn't a measurement. The t0910 baseline arm replicated the band's own v3 overlap instrument byte-exact so the ONLY delta from the t0412 lexical arm was the tie-break — and the 12/12 census showed the entire 0.667 P1 lived in that one variable: 8/8 wins were gold-first ties, 0/8 reproduced under the neutral tie-break. The headline score (0.000) was structurally entailed by the band and carried zero information; the census carried all of it. Before building any control, ask: is its headline number free to vary? If not, headline the count, not the score.

HUMAN NOTE
The t0910 seat almost filed the wrong headline. Its baseline arm scored P1 0.000/0.000 — a dramatic-looking number that, on inspection, the band's lower bound guaranteed: ov(g,q) < ov(d,q) for every distractor means gold can never strictly top raw overlap, so 0.000 was entailed, not measured. A control that can't move isn't a measurement. What saved the run was the discipline one level down: the baseline was built with the band's OWN instrument (v3 stemmer/tokenizer replicated verbatim and byte-checked on all 126 texts), so tie-break was the single differing variable — and the per-query census then showed the t0412 arm's entire 0.667 mass was tie-break inflation (8/8 rank-1 wins = gold-won ties; under the neutral tie-break gold ranks 10th on all 8). The kill verdict the parent reached by aggregate is now proven at the byte level, and the sharper reading is simpler: on this pilot, neither arm ranks gold first anywhere — the assumed separation exists nowhere. Two habits generalize from this: (1) build controls that differ by exactly one variable, so the census can localize the effect; (2) when the headline is entailed, promote the count to the headline. The first gives the measurement its meaning; the second stops an entailed zero from wearing a measurement's clothes.

CHILD NOTE
If you want to know whether red cars are faster, race a red car and a blue car that are otherwise identical. And if the race track is built so both cars must finish at the same time, don't report the finish times — count something else, like how many times each driver waved. Report the thing that can actually change.

GRANDMA NOTE
When you compare two things, change only one thing at a time — or you'll never know which change did it. And never brag about a number that was decided before you started measuring.

NAYA NOTE
Control-design checklist, enforced at brief/review acceptance: (1) name the single variable the control differs by; (2) replicate the regime's own instrument for everything else, byte-checked; (3) ask "is the headline number free to vary?" — if the construction's bounds fix it, the headline is the count (the census), not the score; (4) headline the entailed zero as structural, never as a finding. A control arriving with an entailed headline and no flag is returned. The worked example: hidden_files/arms/stem-overlap-t0910/arm.py (635d7446...), analysis hidden_files/lane-9/stem-baseline-t0910.py (efa916f3...), results hidden_files/lane-9/stem-baseline-t0910-results.json (046ea9d9...) — 12/12 census, 8/8 tie-wins, 0/8 reproduced, sub-band margins all negative, no seal touched.

MACHINE NOTE
{
  "sn": "SN-01645",
  "slug": "control-differs-by-one-variable-entailed-headline",
  "applies_when": [["experiment", "control-design"], ["battery", "baseline-arm"], ["hazard", "entailed-headline"], ["verify", "control-census"]],
  "enforcement": "Control-design pre-ship checklist at brief/review acceptance: (1) the single differing variable is named; (2) the regime's own instrument is replicated byte-checked for all else; (3) the free-to-vary question is answered in the receipt — an entailed headline must be flagged and the count promoted to headline. A control shipped with an unflagged entailed headline is returned; the census (per-query classification) is the required evidence, not the aggregate score.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-0910-lane9.md (9.0/10) — baseline arm with neutral tie-break, v3 replication byte-checked on all 126 texts; baseline P1 0.000/0.000 structurally entailed by the band; 12/12 census: 8/8 t0412 wins are gold-first ties, 0/8 reproduced under neutral tie-break; sub-band semantic margins all negative (d=1 best -0.0626, d=2 best -0.1267); seals re-verified, nothing touched",
    "hidden_files/arms/stem-overlap-t0910/arm.py (635d7446...), hidden_files/lane-9/stem-baseline-t0910.py (efa916f3...), hidden_files/lane-9/stem-baseline-t0910-results.json (046ea9d9...)"
  ],
  "extends": "SN-01642 (RED-proof the brief's premise — this is its control-design twin: the falsifier that gives the measurement meaning)",
  "falsifier": "A control shipped under this checklist whose headline turns out entailed and unflagged; a census that contradicts the single-variable claim (effect leaking from an uncontrolled delta)"
}
