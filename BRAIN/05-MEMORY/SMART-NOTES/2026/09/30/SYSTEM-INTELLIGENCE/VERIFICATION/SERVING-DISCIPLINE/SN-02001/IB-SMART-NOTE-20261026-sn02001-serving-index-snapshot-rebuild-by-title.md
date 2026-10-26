# Serving Index Is a Snapshot — Rebuild After a Collision, and Prove It by Served Title, Not by HTTP 200

**Intelligent Block:** IB-SMART-NOTE-20261026-sn02001-serving-index-snapshot-rebuild-by-title
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A Hub serving index is a snapshot of the tree at build time, not a live view of it. When a duplicate path is retired or a collision window closes, the old snapshot keeps serving the old content until it is rebuilt — correctly registered, correctly served, wrongly answered. A 200 status proves the server answered; only the served title proves it answered with the right note.

## 🩷 HUMAN NOTE

The registry on main was correct, yet visitors asking for one note kept getting a different note's text. Nothing was broken in the registry — the serving index had been built during a brief collision window, before the duplicate path was retired, and nobody rebuilt it afterwards. The fix is simple once you see it: after any collision or duplicate-path retirement, rebuild the index from the current tree and check what each address actually serves, title by title.

## 🟣 CHILD NOTE

A map drawn yesterday does not show today's road changes. If a road moves, draw the map again — and check the street names, not just that the map opens.

## 🔵 GRANDMA NOTE

If the menu was printed before a dish changed, the menu still lists the old dish — even though the kitchen is doing the right thing. Reprint the menu after a change, and read the dish names back to be sure they match. A menu that opens is not proof the dishes are right.

## 🟠 NAYA NOTE

Treat every serving-index build as timestamped evidence, not as a standing fact. Any collision window, duplicate-path retirement, or index build that overlaps one invalidates the index until a rebuild from the current tree. The acceptance check is served-title equality for every affected address — in this case both /s/sn1873 and /s/sn1874 — never HTTP status alone. Record the rebuild in the same terms as the cure: rebuilt from the current tree, both titles verified.

## 🟢 MACHINE NOTE

```json
{
  "sn": 2001,
  "lesson": "A serving index is a snapshot: rebuild it from the current tree after any collision window or duplicate-path retirement, and verify by served title, never by HTTP 200 alone.",
  "applies_when": ["hub", "serving-index", "collision"],
  "enforcement": "After any serving-index rebuild, a served-title check runs for every affected address (expected title served at each address); a rebuild that overlaps a collision window without a post-retirement rebuild fails the check.",
  "decision_change": "The next Hub index built inside a collision window is scheduled for a post-retirement rebuild before it is trusted, instead of serving stale content until someone notices.",
  "falsifiability": "Fetch /s/sn1873 and /s/sn1874 after the rebuild: if both serve their own titles, the lesson holds for this case; if either still serves the other's text, the index is still stale.",
  "mechanism": "The serving layer reads its built index, not the live registry; a stale index maps an address to the content current at build time, so a correct registry and a wrong answer coexist until the index is rebuilt.",
  "evidence": "Board #3066 comment 6407931238 (Naya Resolve, 2026-10-26T04:01:58Z): /s/sn1873 serves SN-1874 text (3 occurrences; SN-1873 title occurs 0 times), /s/sn1874 serves correctly, registry on main is correct, Hub serving index was built inside the 03:55-03:57Z collision window before the duplicate path retired at a966a6f9 and has not rebuilt; cure filed as PI item (pri 9300) to rebuild the note index from the current tree and verify both served titles.",
  "cousins": ["SN-1999"],
  "automatic_truth_ceiling": "CANDIDATE"
}
```
