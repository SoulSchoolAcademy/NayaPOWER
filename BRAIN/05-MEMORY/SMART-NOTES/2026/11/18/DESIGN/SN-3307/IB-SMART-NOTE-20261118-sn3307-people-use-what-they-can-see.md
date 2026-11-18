# People Use What They Can See

SN-3307 · DESIGN — DISCOVERABILITY

**Filed:** Intelligence Loop filing push #2 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3284; filed as SN-3307 renumbered from provisional SN-3273.

**Created:** 2026-11-18 03:12–03:13Z (Shawn on the Connect-rows screenshot, then his reasoning — recorded in the daily log; drafted in run 293)

**Paired Naya Note:** NN-20261118-people-use-what-they-can-see

## Hook

The rows are off-centered — move the controls up into one centered line, and put the message / mail / audio / video buttons in the row. With the buttons, because people probably don't realize they CAN instant mail, audio or video until the buttons show them. A capability nobody sees is a capability nobody uses.

## Nutshell

Shawn, 2026-11-18 03:12Z, on the Search people panel screenshot (sophia 94%, thora 91%, terra 88%, zoe 92%, emesa), his words: **"you should have moved this up and then you should have the message mail audio video buttons there right."** **THE DIRECTION:** move the controls up into one centered line, and the row carries the message / mail / audio / video buttons there. **HIS REASONING, 03:13Z, settling his own question of with-or-without:** WITH the buttons — because people probably don't realize they CAN instant mail, audio or video until the buttons show them. Those are valuable things, and people get used to it — **"oh wow I can just message them. So simple."** **THE PRINCIPLE:** a capability nobody sees is a capability nobody uses; the visible button is what turns a list of names into a connection. **HIS CONFIRMATION:** ❤️ on the button message. **THE EYE'S MEASUREMENT (connection cloud eye, 03:24Z):** the vertical defect is confirmed in every row — initial ball + name share one line (centers within 0–5px), while %, i, CONNECT share a second line 50–65px below the name line (sophia +53, thora +50, terra +65, zoe +60, emesa +62). NO message/mail/audio/video button exists in any row, hidden or otherwise (none in the rows' DOM); those four exist only inside the connection profile dialog. The one-line fix is NOT in this build. **THE ROUTING:** the fix rides connection-profile follow-on #3 — held on the inference-proxy 429, dispatched once the limit is known clear. **HIS CONFIRMATION ON THE EYE REPORT (03:28Z):** ❤️ on the second bubble (press sink FAIL on MAIL, YOU bubble invisible at phone width, rows still two-tiered with no buttons yet, all riding follow-on #3) — the scope stands as reported.

## Human

A list of names with percentages is a directory, not a connection. The moment the row carries its four buttons — message, mail, audio, video — it stops being a list and becomes a door: one tap and you are talking to the person. He saw that the rows were off-centered and the controls were missing, and then he answered his own question the way only the person who will use it can: people do not discover what is hidden. They discover what is shown. "Oh wow, I can just message them. So simple." — that is the whole product in one sentence. The button does not add a feature; it reveals one that was already there. Every capability we hide behind a menu or a guess is a capability nobody uses, and a capability nobody uses might as well not exist.

## Child

Imagine a classroom where you can talk to anyone — but there's no button to do it, so nobody knows they can. Shawn says: put the buttons right there in the row, where you can see them — message, mail, audio, video. Then you look at the row and think, "Oh wow, I can just message them. So simple!" If you can't see it, you can't use it. The button is what turns a list of names into a real connection.

## Grandma

Dear, Shawn looked at the rows of people and said the buttons should be right there where you can see them, dear — message, mail, audio, video, all in a neat line. Because if people can't see that they can just message someone, they won't know they can, dear. But when the button is right there, they think, "Oh wow, I can just message them. So simple!" That's the whole thing, dear — you have to show people what they can do, or they never do it.

## Naya

PEOPLE USE WHAT THEY CAN SEE. A CAPABILITY NOBODY SEES IS A CAPABILITY NOBODY USES. THE VISIBLE BUTTON TURNS A LIST OF NAMES INTO A CONNECTION.

## What it means

- **THE FAULT:** the Connect rows are off-centered and carry no message / mail / audio / video buttons.
- **THE FIX:** move the controls up into one centered line; the row carries all four buttons there.
- **THE PRINCIPLE:** people use what they can see — a capability nobody sees is a capability nobody uses.
- **THE PROOF IN HIS WORDS:** "oh wow I can just message them. So simple."
- **THE ROUTING:** measured by the running connection eye (d8f7c1e1) — vertical defect confirmed in every row (50–65px below the name line), no buttons in any row; the fix rides connection-profile follow-on #3, held on the 429.
- **THE EYE'S VERDICT (03:24Z):** connection cloud eye GOES BACK — D1 PASS (CONNECT sends, "Requested ✓", persisted), press sink FAIL on MAIL, YOU bubble invisible at 635, rows still two-tiered with no buttons; his ❤️ on the report stands the scope as reported.

## Why it matters

Without this note, the next builder hides the four actions behind a tap or a menu because the row "looks cleaner" — and the connection dies quietly, because nobody discovers what is hidden. With it, the rule is plain: the row shows what it can do, in the row, where the eye already is. Discoverability is not decoration; it is the difference between a directory and a connection.

## What changes now

1. Every Connect row carries message / mail / audio / video buttons, in one centered line, moved up.
2. No capability is hidden behind a menu or a guess when a visible button can show it.
3. The connection eye measures the row alignment and the buttons' presence before the fix round builds.
4. The fix rides connection-profile follow-on #3.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.
