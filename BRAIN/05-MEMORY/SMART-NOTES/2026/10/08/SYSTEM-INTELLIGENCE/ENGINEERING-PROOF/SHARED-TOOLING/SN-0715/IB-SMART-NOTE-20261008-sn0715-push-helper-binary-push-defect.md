# The Shared Push Helper Can't Push Binaries — Disclose the Defect, Work Around It, Flag the Owner

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0715-push-helper-binary-push-defect
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6068249170 ([NAYA 5] DESIGN CONTRACT MISSION — COMPLETE, 2026-10-08T20:16:08Z) and #1354 comment 6068441540 ([NAYA 2][RELAY], 2026-10-08T20:27:50Z) — both SoulSchoolAcademy

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5's design-contract mission needed to push the exemplar PDF (`proof/hourly_exemplar/naya-hourly-exemplar.pdf`) through the shared `push_branch_preserve.py` helper. The helper crashed with **`UnicodeDecodeError`** — it reads files as text, so **it cannot push binary files at all**. The worker patched a `/tmp` copy of the script to complete the push (branch `naya5/design-contract`, pushed via Git Data API, server tree verified == local, first at `c9f32199`, then the rebuilt exemplar at `37645d47`). Naya 2's relay logged the event exactly the way shared infrastructure deserves: recorded as a **shared-tool defect**, explicitly not claimed ("recording it as a shared-tool defect, not claiming ownership of the script").

Why this is brain-grade: shared scripts are infrastructure — every lane uses them, so a defect in one is a defect in everyone's path. The failure mode is the silent local fork: a lane patches its own copy, ships its mission, says nothing, and every later lane rediscovers the same crash from scratch. The discipline has three moves, all cheap: (1) **work around locally to unblock the mission** — patch a `/tmp` copy, never commit a private fork as the fix; (2) **disclose the exact defect on the board** — the script name, the exception, and the input class it breaks on (binary files, not text); (3) **flag ownership** — record it as an open defect for the script's owner, not as something you've silently absorbed and not as a lane you've claimed. A cold successor hitting `UnicodeDecodeError` from `push_branch_preserve.py` on a PDF now reads one line and knows: the tool can't do binaries, the `/tmp`-patch workaround exists, and the real fix is still open.

Rule for a cold successor: **when a shared script breaks on your input class, patch a `/tmp` copy to unblock yourself, disclose the exact defect + input class on the board, and flag it for the script's owner.** Never silently fork shared tooling; never claim a lane that isn't yours.

## 🩷 HUMAN NOTE

Shawn — a small infrastructure lesson from the design-contract mission. The shared push helper script can't push binary files (it crashes trying to read them as text). Naya 5 worked around it with a temporary copy to ship the exemplar PDF, and Naya 2 logged it as a shared-tool defect for whoever owns the script to fix. The standing rule: when a shared tool breaks, say so on the board with the exact error, work around it locally, and flag it for the owner — so the next lane doesn't trip over the same hole. Nobody forks shared tools in silence.

## 🟣 CHILD NOTE

Imagine the team's shared hammer breaks every time it hits a certain kind of nail. One person tapes the hammer back together just for their own job and tells nobody. The next person picks up the hammer, it breaks again, and they waste an hour figuring out why. The smart move: tape it up so your job finishes, then tell everyone "the shared hammer breaks on these nails — the real fix is still needed." That's what happened here, except the hammer is a push script and the nails are binary files like PDFs.

## 👵 GRANDMA NOTE

The team shares a helper program that pushes work up to the shared repository. Someone discovered it crashes whenever the file is a picture or PDF instead of text. They made a quick temporary copy to finish their own job, then wrote up the problem publicly: which tool, what error, what kind of file breaks it — and left it for the tool's owner to fix properly. The lesson: when shared equipment breaks, you work around it fast, you report it clearly, and you don't pretend the problem doesn't exist.

## 🟣 NAYA NOTE

Shared tooling is the floor every lane walks on. When it breaks on my input class, I don't diagnose my file — I check the tool. The protocol: unblock with a disposable local patch (a `/tmp` copy, never a committed fork), disclose on the board with the exact exception and the exact input class, and name the owner rather than absorbing the defect or claiming the lane. Silence is the expensive option: it buys every future lane the same crash. The defect stays open and visible until the owner fixes it — the board is the receipt.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0715",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/SHARED-TOOLING",
  "doctrine": "shared-tool-defect-disclosure",
  "rule": "When a shared script breaks on your input class: patch a /tmp copy to unblock yourself, disclose the exact defect + input class on the board, and flag it for the script's owner. Never silently fork shared tooling; never claim a lane that isn't yours.",
  "failure_mode": "silent local fork — every lane rediscovers the same crash; or silent absorption — the defect is never fixed",
  "defect": {
    "script": "push_branch_preserve.py",
    "error": "UnicodeDecodeError",
    "input_class": "binary files (e.g. PDFs)",
    "cause": "script reads files as text",
    "workaround": "patch a /tmp copy for the immediate push",
    "status": "OPEN — shared script needs the fix"
  },
  "cousins": ["SN-050", "SN-036", "SN-0472"],
  "evidence": [
    "#1354 comment 6068249170 (Naya 5, 2026-10-08T20:16:08Z) — 'push_branch_preserve.py cannot push binary files (UnicodeDecodeError) — worker patched a /tmp copy to complete the push; shared script needs the fix'",
    "#1354 comment 6068441540 (Naya 2 relay, 2026-10-08T20:27:50Z) — 'recording it as a shared-tool defect, not claiming ownership of the script'",
    "Mission completed despite the defect: branch naya5/design-contract pushed via Git Data API, server tree verified == local (c9f32199, rebuilt exemplar 37645d47)"
  ]
}
