# THE OFFICIAL FORMATS — the Recipe's outputs, stored in the builder
## Factory Phase 2 (Shawn's order, 2026-11-17 01:56Z — "The Language Lives Everywhere")

The builder stores the two canonical official formats and emits them
byte-identical on every test build. Harvested verbatim, never re-typed,
never a look-alike, never edited here.

## The canonical files (this directory)

| Format | File | GitHub blob (full sha) | Bytes | sha256 |
|---|---|---|---|---|
| Unfold (down) | `official-unfold.html` | `34c756fff6286c46a2ff61fa6224bc49e35d5abf` | 32,079 | `70abc8e96712393d0b3f087b8410379fc39970a5905d06de1884afdf2d7b346c` |
| Slideshow (sideways) | `official-slideshow.html` | `21d08a88e0f2e63d3c30d8f5112a2479ecf52d59` | 34,896 | `fcfa0c4c9794b8a92a3dea5ba2e4a1802376b2c75b2ba291fa8791b1da30693f` |

Source: the official-formats round, branch
`personal/official-formats-bridge-20261116` — the unfold fix commit
`84bd32c9` and the slideshow fix commit `a456d270`, filed at
`TEAM-NITRO/official-formats-bridge-20261116/official-unfold.html` and
`.../official-slideshow.html`. Harvested from the Studio's canonical code
(`wireDeck` / `showSlide`, Studio blob `a7114308`), re-checker PASS on all
items. The two files are ONE implementation each — there is no other
unfold and no other slideshow anywhere in the system.

## How the builder uses them

`factory.py` carries the `FORMATS` table (filename + blob sha + byte size +
sha256) and the format step `emit_formats()`: on every build it reads the
stored bytes, verifies size + sha256 against the table (a mismatch is a
hard stop — the build fails before the gate, before anything ships), and
writes the bytes verbatim into the build output directory as
`official-unfold.html` and `official-slideshow.html`.

## The auto-format lives INSIDE these bytes

Both presentations read the same beat node list — one shared data source
feeding the unfold and the slideshow — so the citizen's ten walk answers
pour into About + Skills automatically, in both formats, with nothing
hand-typed twice. The builder never splits them and never re-implements
them; emitting them verbatim preserves the auto-format.

## Format assignment (the law these files serve)

Unfold → About. Slideshow → Skills. One format per bridge (the entrance
bridge still uses both for the agreement/legal pages). Skills is the
presentation for getting work — made so impressive by default that anybody
could add an image or text and it would look extraordinary BECAUSE OF THE
FORMATTING. See `~/workspace/team-nitro/THE-NAYA-CODE.md` §9 and
`~/MEMORY.md` "THE FORMAT ASSIGNMENT" (2026-11-17 01:49Z).

## Verify (anyone, cold)

```sh
cd ~/workspace/team-nitro/interface-factory
python3 factory.py specs/smart-links-stats.json --out out/formats-test.html --no-gate
diff formats/official-unfold.html out/official-unfold.html
diff formats/official-slideshow.html out/official-slideshow.html
sha256sum formats/*.html out/official-*.html
```

Both diffs must be EMPTY (byte-identical). The receipt
(`out/formats-test.html.receipt.json`) carries the `formats` entries with
bytes + sha256 per format.

## When a new canonical version lands

A new canonical unfold/slideshow arrives ONLY as a new filed file with a
new blob sha from its own round — never by editing these files in place.
Replace the file, update the `FORMATS` table in `factory.py` AND this file
(blob sha, bytes, sha256) in the same pass, re-run the verify above, and
file. A hash mismatch after replacement means the wrong bytes were stored.
