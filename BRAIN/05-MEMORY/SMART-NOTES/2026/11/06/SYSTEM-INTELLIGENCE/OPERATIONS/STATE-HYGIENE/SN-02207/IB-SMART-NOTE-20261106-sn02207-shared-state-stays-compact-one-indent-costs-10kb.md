# INTELLIGENT BLOCK — SN-2207

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02207-shared-state-stays-compact-one-indent-costs-10kb
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director tick 2026-11-05 23:38 PST (executed 2026-11-06T07:41Z, memory log ~/memory/2026-11-06.md): 'shared-state.json must stay COMPACT (single-line) — an indent=1 rewrite this tick inflated it +9.5KB mid-tick before the compact rewrite restored 190,410.' State 190,410 bytes, 9,590 below the 200,000-byte bar — the indent alone would have pushed it over. Same-night readings show the file living within ~10KB of the bar (192,050 at 23:08; 198,439 at 20:52). Number census at live tip 9004ce29 (git protocol, local mirror): SN-2207 absent from main-tree paths, branch tree, and registry index .naya/memory/smart-notes/index.json (1,246 entries; 0 'compact', 0 'indent', 0 'single-line', 0 'shared-state'); lessons.jsonl carries no compact/indent note. Branch head 03fcc466 (SN-2205); counter ends at 2205; open PRs #3256, #3255, #3254, #3178, #3089 claim no SN file (file lists checked via App route this tick); #2416 closed unmerged since 2026-10-21; #1354 capped at 2,500, commenting disabled.

## ✦ IN A NUTSHELL

shared-state.json is capped at 200,000 bytes, and it lives within about 10KB of the bar (190,410 tonight). A single indent=1 rewrite inflated it by 9.5KB mid-tick — pure whitespace, zero new data — before a compact rewrite restored it. Formatting is state size: an indented pretty-print is not a cosmetic choice on this file, it is ~10KB of spend against a hard cap. The rule: write shared-state compact and single-line, every time, and check the size after every write.

## 🩷 HUMAN NOTE

Shawn — the file that holds the whole system's shared state has a hard size limit, and it is nearly full: 190,410 bytes against a 200,000-byte cap. Tonight one routine rewrite accidentally saved it in pretty-printed form — indented, spread across many lines — and the file grew by 9,500 bytes without a single new fact in it. That is whitespace, not information, and it nearly pushed the file over its limit. The fix is a standing rule: this file is always written compact, on one line, and its size is checked after every write — so a formatting slip is caught in the same tick instead of silently eating the margin.

## 🟣 CHILD NOTE

Imagine your school bag has a strict weight limit, and it is already almost full. One day you pack the same books but wrap each one in layers of bubble wrap — the bag gets much heavier, but you didn't add a single book. The bubble wrap is the problem, not the books. The rule is: pack the books bare, no bubble wrap, and weigh the bag every time you pack it — so you notice the extra weight before the bag breaks.

## 🔵 GRANDMA NOTE

Dear, it is like a recipe box that only holds so many cards. One day someone rewrites all the recipes in big loopy handwriting with a blank line between every step — the box overflows, but there isn't a single new recipe in it. The handwriting took the space, not the cooking. The rule is: write the recipes small and tight, one card each, and count the cards every time you put the box away — so a fancy hand never quietly fills the box.

## 🟠 NAYA NOTE

For every seat that writes shared-state.json: (1) write it compact and single-line — json.dump with separators=(',', ':') — never with indent; (2) an indent=1 rewrite costs ~9.5KB of pure whitespace on a file that sits ~10KB below its 200,000-byte cap, so one pretty-print is the difference between under the bar and over it; (3) check the file size after every write and fail the tick if it exceeds 200,000 bytes or grew by formatting alone; (4) if you ever find the file indented, rewrite it compact in the same tick and record the size before and after — the before/after pair is the proof the inflation was formatting, not data; (5) the cap is a size cap, and formatting is size — treat the writer's formatting choice as a budget decision, not a style preference.

## 🟢 MACHINE NOTE

```json
{
  "slug": "shared-state-stays-compact-one-indent-costs-10kb",
  "sn": "SN-2207",
  "title": "Shared-State Stays Compact — One Indent Costs ~10KB Against a 200KB Cap",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["shared-state", "state-size", "budget"],
  "enforcement": "Every shared-state write uses compact single-line JSON (json.dump with separators=(',', ':')); the size check after each write fails the tick if the file exceeds 200,000 bytes or grew by formatting alone — an indent=1 rewrite is refused. Regression check: rewrite shared-state with indent=1 and assert the size grows ~9.5KB; rewrite compact and assert it returns to baseline.",
  "falsifier": "A compact rewrite that still inflates the file by ~10KB, or an indent=1 rewrite that costs nothing, would prove the size change is not formatting and collapse this note. A compact rewrite returning the file to its baseline size confirms the mechanism.",
  "decision_changed": "How shared-state.json is written: compact single-line JSON with separators=(',', ':') instead of indented pretty-print — and a size check runs after every write, so a formatting-only inflation is caught in the same tick instead of silently eating the 200KB margin.",
  "mechanism": "JSON indent adds a newline plus indentation spaces for every key and value; shared-state holds hundreds of keys, so one pretty-print rewrite adds ~9.5KB of pure whitespace with zero new information. Compact separators emit no whitespace at all. The file sits 9,590 bytes below a 200,000-byte cap, so a single formatting choice is the difference between under the bar and over it — the cap is a size cap, and formatting is size.",
  "provenance": "Director tick 2026-11-05 23:38 PST (executed 2026-11-06T07:41Z, memory log ~/memory/2026-11-06.md): 'shared-state.json must stay COMPACT (single-line) — an indent=1 rewrite this tick inflated it +9.5KB mid-tick before the compact rewrite restored 190,410.' State 190,410 bytes, 9,590 below the 200,000-byte bar — the indent alone would have pushed it over. Same-night readings show the file living within ~10KB of the bar (192,050 at 23:08; 198,439 at 20:52). Duplication check this tick: live registry index .naya/memory/smart-notes/index.json at tip 9004ce29 (1,246 entries) contains 0 'compact', 0 'indent', 0 'single-line', 0 'shared-state'; lessons.jsonl carries no compact/indent note. Number census at live tip 9004ce29 (git protocol, local mirror): SN-2207 absent from main-tree paths, branch tree, and registry index; branch head 03fcc466 (SN-2205); counter ends at 2205; open PRs #3256, #3255, #3254, #3178, #3089 claim no SN file (file lists checked via App route this tick); #2416 closed unmerged since 2026-10-21; #1354 capped at 2,500, commenting disabled."
}
```
