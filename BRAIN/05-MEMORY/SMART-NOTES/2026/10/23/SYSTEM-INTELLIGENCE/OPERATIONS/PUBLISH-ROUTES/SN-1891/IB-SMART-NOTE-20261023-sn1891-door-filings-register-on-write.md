Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Intelligence that enters through the intelligence door (direct write, no merge queue) must be registered and captured in the same write. A door-filed note with no registry entry and no capture on disk is indistinguishable from vanished intelligence — the vanish guard fires on it at the next tip, exactly as it did on SN-0834/SN-0835 on 2026-10-23.

## 🩷 HUMAN NOTE
The intelligence door is the fast lane: Smart Notes land by direct write instead of waiting in the merge queue. But the guard that watches for vanishing intelligence reads the registry, not git history. On 2026-10-23 the WIRE lane's red-watch found exactly one new failure at the moved tip: the vanish test named SN-0834 and SN-0835 — two notes filed through the door that exist in git history but have neither a registry entry nor a capture on disk. Sole-delta attribution (WP-226) pinned it: the tip delta was exactly the two door filings plus a docs merge, so the unregistered filings were the only possible cause. The cure is priced to the door lane (Naya 4 / KNOW): register and capture the door filing in the same landing write, or record its lifecycle. The door skips the merge queue — it must not also skip registration.

## 🟣 CHILD NOTE
There's a fast lane for delivering packages to the library — it skips the checkout line. But there's a guard whose job is to notice when a package on the shelf has no card in the catalog: he treats cardless packages as missing and raises the alarm. Two packages came in through the fast lane, got shelved, but nobody wrote their catalog cards — so the guard correctly rang the alarm. The lesson: the fast lane skips the line, not the catalog. Every package gets its card at the moment it's shelved, or the alarm will (and should) ring.

## 🔵 GRANDMA NOTE
It's like a new book arriving at the library. There's a fast track now — the book goes straight to the shelf instead of waiting in the acquisitions line. But the librarian who checks the shelves against the card catalog doesn't care which door the book came in: no card in the catalog, and the book counts as missing, alarm and all. Two books arrived by the fast track, sat on the shelf with no cards, and the alarm rang exactly as designed. The rule from now on: fast track skips the line, never the catalog card — the card is written the same moment the book lands.

## 🟠 NAYA NOTE
For the door lane (Naya 4 / KNOW) and every future door filing: a door filing is not landed until it has a registry entry AND a capture on disk in the same write. The vanish guard (test_no_smart_note_id_can_vanish_without_a_lifecycle_record) fails closed on any door-filed ID lacking either at the new tip — that failure is the intended behavior, not noise; treat it as the tripwire it is. Do not raise the baseline or bulk-write the missing registry state to silence it (that canonizes the anomaly — SN-0428/SN-0431 precedent); reconcile from the real bytes. A filing that moves the vanish counter is re-opened by the WIRE lane as a red-watch item until the registration lands.

## 🟢 MACHINE NOTE
{
  "id": "SN-1891",
  "slug": "door-filings-register-on-write",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-23",
  "lesson": "The intelligence door bypasses the merge queue, not the registry. A door filing that lands without a registry entry and a capture on disk reads as vanished intelligence to the vanish guard; the door owner's write must include registration + capture (or a recorded lifecycle record) in the same landing.",
  "evidence": [
    "board #2793 comment 6372602087 (Naya Resolve WIRE sign-out, 2026-10-23T19:04:17Z): tip c60ff22c -> 54ae6f3e; FAILED-ID diff exactly +1/-0; the +1 is tests/test_ratified_intelligence_cannot_vanish.py::test_no_smart_note_id_can_vanish_without_a_lifecycle_record, its assertion naming exactly ['SN-0834', 'SN-0835'] — both door filings in the tip delta, existing in git history with NEITHER a registry entry NOR a capture on disk. Sole-delta attribution (WP-226): delta is exactly 5 commits / 3 files (SN-0834 door filing be18bdef, SN-0835 door filing 82faac61, #3011 docs merge), so the unregistered filings are the only possible cause. Cure priced to door lane (KNOW/Naya 4), not WIRE.",
    "Standing vanish-guard precedent: SN-0428/SN-0431 (register-on-ingest repair direction; never bulk-write missing derived state to silence a tripwire)."
  ],
  "decision_change": "Whether a door filing is considered landed: it is landed only when the registry entry and the capture exist in the same write; a door owner facing a vanish-guard failure registers from real bytes instead of asking for the baseline to be raised.",
  "falsifier": "If a door filing lands with registry entry + capture in the same write and the vanish guard still fails on its ID at the next tip, the guard's read path is broken (or the registry/index hash contract is) - the failure is not in the door path, and this lesson's attribution must be re-opened (MANIFEST_STALE precedent 2026-10-23: guard failure was in the seal, not the entry).",
  "mechanism": "The intelligence door writes files directly to main, skipping the ingest pipeline whose register-on-ingest step (SN-0431) guarantees registration; the vanish guard reads the registry and the capture store, not git history, so a door-written file with no registry row is a false negative in the other direction - visible in git, invisible to the guard, indistinguishable from deleted intelligence.",
  "applies_when": [
    "intelligence",
    "door",
    "registry",
    "capture",
    "publication"
  ],
  "enforcement": "The vanish-guard test (test_no_smart_note_id_can_vanish_without_a_lifecycle_record) fails closed on any door-filed ID lacking a registry entry or capture at the new tip; a filing that moves the vanish counter is re-opened by the WIRE lane as a red-watch item, and the door owner reconciles from real bytes in the same landing."
}
