# SMART NOTE — Measure the Live Distribution Before You Write the Test

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1179` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1179-measure-live-distribution-before-test` |
| Human title | Measure the Live Distribution Before You Write the Test |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING-PROOF |
| Subtopic | TEST DESIGN |
| Captured | 2026-10-13 10:10:54 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Capture type | Test-design law |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | `#2175` board comments 6141800626 (Naya 4 SELF-BUILD #2514 verification — defect found: `merged_by` constant on 5/5 live merges; shipped tests encode the false premise), 6142135518 (falsification re-proof: 15/15 live merges constant; 21/21 tests green WITH the defect present; `INVALID` branch unreachable), 6142575337 (Builder wave-44 repair: default fake now uses the live distribution; named regression test added) |

---

## ✦ IN A NUTSHELL

**A green suite proves only that the fixtures match themselves — measure the discriminator's live input distribution before you write the test.** `authority_audit.py` discriminated the director's click on `merged_by == "SoulSchoolAcademy"`, which turned out to be constant on 15/15 individually-fetched live merges (the director's clicks and the lane merges all authenticate as the same org account), so the `INVALID` branch was unreachable in production. The shipped suite was 21/21 green with the defect present, because its fixtures used a fictional `merged_by="SomeLane"` — the tests validated a world that doesn't exist. The repair made the default fake use the live distribution and added the named regression test (lane merge + org `merged_by` + no packet → INVALID). Rule: fetch the live inputs first, write fixtures second; any fixture value never observed on live bytes is a fiction until proven otherwise.

---

## 🩷 HUMAN NOTE

A test suite is a story your code tells about the world — and this one told a story about a world that didn't exist. The audit tool decided "was this the director's own click?" by checking a field called `merged_by`. Its tests checked the logic with a fake value, `merged_by="SomeLane"`, and all 21 tests passed. But on the real system, that field is *always* the org account — the director's clicks and the team's merges are indistinguishable on it. So the tests were perfectly green and completely useless: they certified logic against an input that can never happen, while the real bug — a discriminator keyed on a constant — sat in production untouched. The fix wasn't just repairing the logic; it was repairing the fiction: the test fixtures now start from the real-world distribution, and there's a named test for the exact case that broke before. Test what is, not what you imagine.

---

## 🟣 CHILD NOTE

Imagine you're testing whether your lock works, and you test it with a toy key that doesn't exist in real life. All your tests say "the lock works!" — but a real thief with a real key walks right through, because you never tested with a real key. That's what happened: the tests used pretend values, and the real world behaved differently. The rule now: always check what the real keys look like first, then write your tests with real-looking keys.

---

## 🔵 GRANDMA NOTE

Dear, this is the old difference between a map and the territory. The map — the tests — said the road was clear, but nobody had walked the road to check. The check for "did the boss click this?" looked at a label that was the same on every single real click, so the check could never say no. Twenty-one tests passed anyway, because they all used an invented label that never appears in real life. The lesson the team wrote down: before you write your tests, go look at the real world first. A test that only agrees with its own imagination isn't proof — it's a bedtime story.

---

## 🟢 NAYA NOTE

1. The discriminator's input distribution is itself evidence, and it must be measured from live bytes before the suite is written. 5/5 sampled merges, then 15/15 individually-fetched merges, all `merged_by="SoulSchoolAcademy"` — the constant was discoverable with one API call before any fixture was authored.
2. A fixture value never observed on live inputs is a fiction. `merged_by="SomeLane"` existed only in `tests/test_authority_audit.py:68/217/229/244`. Fiction fixtures convert coverage numbers into theater: 21/21 green, defect present, `INVALID` branch unreachable.
3. The unreachable branch is the tell. If a branch cannot fire on any live-observed input distribution, either the discriminator is keyed on the wrong signal or the fixtures are fake. Treat "branch unreachable in production" as a defect class, not a coverage gap.
4. The repair pattern: key the verdict on the live-discriminating signal (merge-commit author identity: `Shawn Vibert <humanmaximuscodex@gmail.com>` vs `Naya 5 <naya5@soulschool.academy>`), demote the constant to informational text, and make the default test fake mirror the live distribution — then add the named regression test for the exact failure class.
5. This applies to every discriminator you build: relevance thresholds, authority checks, fail-closed predicates. The question "what does this input look like in the wild?" precedes the question "does my code handle it?"

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1179-measure-live-distribution-before-test",
  "epistemic_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "measure the discriminator's live input distribution before writing the test; fixtures must mirror live-observed inputs",
  "tell": "21/21 green WITH the defect present; branch unreachable on all live-observed inputs; fixture value never seen on live bytes (merged_by='SomeLane')",
  "repair_pattern": "key verdict on the live-discriminating signal (merge-commit author identity); constant -> informational text; default fake = live distribution; named regression test for the failure class",
  "evidence": "#2175 6141800626 (defect: merged_by constant 5/5; false premise encoded in tests); 6142135518 (15/15 constant; 21/21 green with defect; INVALID unreachable); 6142575337 (repair: live-distribution fixtures + regression test, 22/22 green)",
  "defect_class": "FICTION-FIXTURE — suite validates logic against inputs that cannot occur in production"
}
```

---

## 🔗 HOW IT CONNECTS

- **Enforces** the ENGINEERING-PROOF TEST-DESIGN subtopic and the auditor law UNKNOWN≠PASS, IMPLEMENTED≠VERIFIED — a green suite without live-distribution fixtures is neither.
- **Complements** the blinding-protocol notes: blind fixtures protect measurement from bias; live-distribution fixtures protect the suite from fiction.
- **Feeds** SN-1178's honest overturn: the overturn was re-proven by running the shipped artifact verbatim on exact-head bytes — the same "test against reality" move, applied to the verdict rather than the code.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Witnessed once end-to-end (B-25, 2026-10-13): detection → falsification → repair, all on live bytes with named commits and re-derived discrimination. The fiction-fixture class generalizes to every discriminator; a second independent witness would harden it.

## 🌍 APPLICABILITY

- **Applies to:** every test suite guarding a discriminator — authority checks, relevance floors, fail-closed predicates, gate matchers. Anywhere the code branches on a real-world input, the fixture set must be drawn from the real world's distribution.
- **Does NOT apply to:** pure unit logic with no environmental input (arithmetic, serialization round-trips) — there the input space is defined, not observed. The rule is about discriminating the world, not about computing.

## 🧬 SUCCESSOR EFFECT

Future Naya: before you write the first test for any gate, discriminator, or audit — go fetch the live inputs. Ten minutes on the live API buys what a thousand fixture-guessed tests cannot: the knowledge of which branches can actually fire. If your suite's fixtures contain a value you've never observed in the wild, flag it as fiction before you trust a single green run.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
