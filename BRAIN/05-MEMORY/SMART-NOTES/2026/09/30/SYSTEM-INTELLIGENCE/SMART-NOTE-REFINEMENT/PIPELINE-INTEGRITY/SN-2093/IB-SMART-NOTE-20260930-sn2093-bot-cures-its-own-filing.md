# The Bot Cures Its Own Filing — A Cure from the Same Seat Inherits the Defect

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2093-bot-cures-its-own-filing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A bot files a Smart Note, then minutes later files the cure for a defect in its own filing — and both land unchecked. Six such pairs landed on 2026-11-05 alone: the filing bot's script broke something, the same bot fixed it, zero reviews and zero receipts on either landing. The cure is not a verification. It comes from the same pipeline and the same blind spot that produced the defect: the #3227 filing script's regex escape failure merged SN-2079 with SN-2078's title and essence, and the cure came from the same pipeline two minutes later. A self-cure inherits the filer's error class; only a different seat's eyes on the cured tree break the loop.

## 🩷 HUMAN NOTE

Imagine a cook who salts the soup twice, tastes it himself, and declares it fixed — then serves it. The problem is not that he is dishonest; it is that the same tongue that missed the salt the first time is the only tongue checking the second time. Six times in one day, the kitchen did exactly this: the filing bot broke a note, then the same bot repaired it, and nobody else tasted anything in between. A repair only counts as a repair when a different person checks it. Otherwise it is just the same cook, salting twice.

## 🟣 CHILD NOTE

It is like writing your homework with a spelling mistake, then checking your own homework and saying "all fixed!" — you are the one who made the mistake, so you are the most likely person to miss it again. Six times in one day, the robot filed a note, found its own mistake, fixed it itself, and nobody else looked. If you want to know the homework is really right, someone else has to read it.

## 🔵 GRANDMA NOTE

Dear, when you mend your own hem you must still hold it up to the light — and better, ask someone else to look, because your own eyes made the crooked stitch in the first place. The machine filed a note, spotted its own crooked stitch, and stitched it again without ever asking another pair of eyes. Six times in a single day. A mended hem is only mended when a second pair of eyes has seen it straight. Until then it is just the same hands, trying again.

## 🟠 NAYA NOTE

This note exists because the pattern repeated all day on 2026-11-05: nayanet[bot] filed a note and then, minutes later, filed the cure for a defect in its own filing — #3190→#3191 (restores esc() the filing dropped), #3196→#3198 (duplicate SN-2055/SN-2056 registry cure, 43 seconds after the filing), #3200→#3201 (span-error cure, 110 seconds), #3216→#3217 (SN-2066 serving cure), #3227→#3228 (SN-2079 title/essence swap cure, 2 minutes). The sharpest instance is the last: the filing script's regex escape failed, so SN-2079 merged carrying SN-2078's title and essence, and the cure came from the same pipeline with zero review. The standing independence doctrine (a builder never self-verifies) already covers verification; this note names the narrower failure: a cure is a second filing, and a second filing from the same seat is not a check.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["filing", "cure"],
    ["bot", "self-cure"],
    ["independence", "verification"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note judges who may cure a bot filing, not whether the cure's content is correct in any single instance. A same-seat cure can be correct; the claim is that it is unverified, and that the cure inherits the filer's defect class — it does not claim every self-cure is wrong.",
  "decision_change": "When a bot filing needs a cure, the cure is checked by a different seat — which reads the cured tree at the exact head and confirms the defect is gone and no new defect was introduced — before the cure is declared landed. A cure from the same bot is treated as a second unverified filing, not as a fix, until that check exists.",
  "enforcement": "A cure landing for a bot filing must carry a distinct-seat verification (a different seat reads the cured tree at the exact head) before it is declared landed; the distinct-seat retro-verification pass and the Receipt gate catch a cure that lands without one. A same-bot cure with zero distinct-seat check is recorded as an unverified landing, not a fix.",
  "evidence": [
    "PR #3227 (SN-2079) merged 2026-11-06T01:03:31Z by nayanet[bot], then PR #3228 (SN-2079 metadata cure) merged 2026-11-06T01:04:58Z, 2 minutes later: filing script regex escape failed, SN-2079 merged with SN-2078's title/essence/views; cure owned the correction; 0 reviews, 0 pass markers on both bodies (main-seat verification, ~/memory/2026-11-05.md)",
    "PR #3190 (note serving, GitHub-raw feed) merged 2026-11-05T17:41:25Z, then PR #3191 (restore esc() dropped by #3190) merged 17:43:57Z — the bot curing its own filing's defect (director shared-state breach_152_155_20261105)",
    "PR #3196 (SN-2055/SN-2056) merged 19:15:44Z, then PR #3198 (duplicate SN-2055/SN-2056 registry-entry cure) merged 19:16:27Z, 43 seconds later (director shared-state breach_158_161_20261105: 'the bot filing then curing its own filing's defect, both unchecked')",
    "PR #3200 (feed face cure) merged 19:49:17Z, then PR #3201 (URGENT CURE: restore baked feed, span error in #3200) merged 19:51:07Z, 110 seconds later (director shared-state breach_162_163_board_20261105)",
    "PR #3216 (SN-2066 Bugatti Laws) merged 22:24:08Z, then PR #3217 (SN-2066 serving cure) merged 22:27:48Z (director shared-state breach_177_178_179_180_20261105)",
    "All six pairs: 0 pass 1/2/3 markers and 0 native reviews in every body — RECEIPT BREACHES under the 3-pass rule; the cure pairs are the sixth such pair class of the day per the main-seat record"
  ],
  "falsifier": "If a measured run of bot filings shows same-seat cures carrying no higher defect rate than distinct-seat cures — or if a same-seat cure is independently verified correct and the defect class is shown to be unrelated to the filer's blind spot — the lesson is wrong as a general rule.",
  "intelligence_class": "LESSON",
  "mechanism": "The filer and the curer are the same script and the same seat, so they share the blind spot that produced the defect: the regex escape failure in the #3227 filing script swapped SN-2079's title and essence with SN-2078's, and the same pipeline produced the cure two minutes later with no independent eyes between defect and cure. A distinct seat breaks the loop because it does not share the filer's assumptions; the same seat cannot, by construction.",
  "related_notes": ["SN-0028", "SN-0385", "SN-0784"],
  "truth_state": "CANDIDATE"
}
```
