# Never Trust a Check on a Dirty Tree — a Non-Zero git status Is a Hard Stop Before Any Verifier Runs

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02798-dirty-tree-hard-stop-before-verifier
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-lane-scorer-20261114-0050-lane10.md (Lane 10, 2026-11-14 02:13–02:40 PST), H4 + Mirror lesson.

## ✦ IN A NUTSHELL

Lane 10's 0050 run needed a clean tree to re-prove the brain-index drift, and two of its three clones were garbage: the first sparse clone under a nearly-full /tmp silently emptied 502 files (112,015 deletions) — no error, just missing bytes — and the second died out of disk. A `--check` run on that first tree would have reported drift that was not real, or missed drift that was, because a verifier reads tree bytes and a corrupted tree feeds it corrupted bytes: the verdict inherits the corruption. The seat never ran the check on it — `git status` showed the dirt first. The rule: before any verifier runs — a `--check`, a test suite, a scorer read — assert the tree is clean: `git status --porcelain` must be empty. Any non-zero count is a hard stop: re-clone where there is room, never run the verifier on the dirty tree, and never cite its output.

## 🩷 HUMAN NOTE

Shawn — imagine asking a doctor to read an X-ray, but half the X-ray is blank because the machine ran out of film mid-print — and nobody noticed, because the machine didn't beep. The doctor would diagnose a patient who isn't there. That's what happened here: a clone ran out of disk halfway and quietly emptied files, and any test run on that broken copy would have reported problems that don't exist. The seat caught it by checking the copy was intact before running anything. The rule is simple: always check the copy is whole before you trust what any test says about it.

## 🟣 CHILD NOTE

Imagine you're counting the toys in your toy box to prove you have all ten — but someone secretly took three toys out while you weren't looking, and the box looks fine from the outside. You'd count seven and say three are lost, but really they're just not in the box right now. The fix is easy: before you count, peek inside and make sure the box is full and nothing looks wrong. If anything looks off, get a fresh box and count again. Never trust a count from a box you haven't checked first.

## 🔵 GRANDMA NOTE

Dear, it's like proofreading a letter that the printer only half-printed — the bottom half of every page came out blank, but the printer never jammed, so nobody knew. You'd read it and think the writer forgot half the letter, when really the printer lost it. The lesson, love: before you judge any piece of writing, check the pages are all there. If the stack isn't complete, don't read it — print a fresh copy somewhere with enough paper, and then judge. A verdict is only as good as the copy it was read from.

## 🟠 NAYA NOTE

Source: gap-lane-scorer-20261114-0050-lane10.md (Lane 10, 2026-11-14 02:13–02:40 PST), H4 + Mirror lesson. The run's first /tmp sparse clone emptied 502 files (112,015 deletions — dirty tree, `--check` never run on it); the second /tmp attempt died `Out of diskspace` (100% full). Cure used: clone to `~/workspace/scratch` (92G free), `df` first, clone where there is room. What this note does NOT re-teach: SN-0960 (a full /tmp makes mass phantom test failures — the disk-full half: check disk before you debug code); SN-0233 (phantom green — verify only on provably virgin state) and SN-0639 (virgin-confirm-before-flag — reproduce a NEW RED on a fresh detached worktree). Those name the environment as a suspect and virgin state as the cure for reproduction; this one names the pre-verification gate itself: assert clean-tree before the verifier runs, because a verifier's verdict inherits whatever corruption its tree carries. Cousins: SN-0960, SN-0233, SN-0639.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "dirty_tree_hard_stop_before_verifier",
  "mechanism": "a verifier reads tree bytes, so a tree silently corrupted (disk-full empties files without error, no exit code, no warning) feeds corrupted bytes to the verifier and the verdict inherits the corruption — a --check on a 502-modified / 112,015-deleted tree reports drift that is not real; git status --porcelain is the cheap detector that sees the corruption before any verifier runs",
  "evidence": "gap-lane-scorer-20261114-0050-lane10.md (2026-11-14 02:13-02:40 PST), H4 + Mirror lesson: first /tmp sparse clone emptied 502 files (112,015 deletions — dirty tree, --check never run on it); second /tmp attempt died Out of diskspace (100% full); cure used: clone to ~/workspace/scratch (92G free), df first, clone where there is room; --check at the clean regenerated tree: OK, exit 0 (3288 files)",
  "falsifiability": "if a verifier's output were provably independent of tree state (it reads only remote state, never tree bytes), the hard stop would not apply to that verifier; if a --check on a dirty tree reproducibly matched the clean tree's verdict on identical content, the stop would be overkill for that verifier class",
  "decision_change": "a future seat about to run any verifier (--check, test suite, scorer read) first records git status --porcelain for the tree and stops + re-clones on any non-zero count, instead of running the verifier on the dirty tree and citing its output",
  "applies_when": ["verification", "tree-integrity", "verifier-gate"],
  "enforcement": "the lane-scorer receipt audit: every receipt that cites a verifier's verdict must record the git status --porcelain count for the tree it ran on (zero, or the run is un-citable); a receipt whose verifier ran on a tree with a non-zero count — or with no count recorded — fails the evidence check, and the verdict is re-run on a clean tree",
  "related": ["SN-0960 a full /tmp makes mass phantom test failures", "SN-0233 phantom green — verify on virgin state", "SN-0639 virgin-confirm-before-flag"]
}
~~~
