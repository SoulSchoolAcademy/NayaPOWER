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

## The Vault — these formats are vault assets (Phase 2 amendment, 2026-11-17 — The Master Vault Law)

The two canonical formats are digital gold: labeled, inventoried, organized, active. The builder's `formats/` store is the Factory's vault shelf — the assets live here, filed on the factory branch, findable. Every build's receipt inventories both assets (`receipt["formats"]`), so any reader can find the asset and its receipt entry without hunting.

| Asset | Label | Vault (where it lives) | Receipt entry |
|---|---|---|---|
| `official-unfold.html` | official-unfold — the canonical unfold, About's presentation | `TEAM-NITRO/interface-factory/formats/official-unfold.html` — the Factory's vault shelf, filed on the factory branch | `receipt["formats"]["unfold"]` — `label` + `vault` + `path` + `bytes` + `sha256` + `blob` |
| `official-slideshow.html` | official-slideshow — the canonical slideshow, Skills' presentation | `TEAM-NITRO/interface-factory/formats/official-slideshow.html` — the Factory's vault shelf, filed on the factory branch | `receipt["formats"]["slideshow"]` — `label` + `vault` + `path` + `bytes` + `sha256` + `blob` |

The Vault Rule + the Live-on-Made Rule apply: an asset goes into the vault the moment it's made, and once proven (his eye has seen it) it goes live in the same pass — finished work never sits staged. The Vault, Sharpened, is why the receipt carries `label` + `vault` on every format entry: labeled, inventoried, organized, active — never lost in not-being-finished, the feed, or a computer.

## Verify (anyone, cold)

```sh
cd ~/workspace/team-nitro/interface-factory
python3 factory.py specs/formats-test.json --out out/formats-test.html
diff formats/official-unfold.html out/official-unfold.html
diff formats/official-slideshow.html out/official-slideshow.html
sha256sum formats/*.html out/official-*.html
```

Both diffs must be EMPTY (byte-identical). The receipt
(`out/formats-test.html.receipt.json`) carries the `formats` entries with
bytes + sha256 per format, plus `label` + `vault` per format (the Vault
Sharpening — see "The Vault" above).

If the design gate blocks the build, isolate the format step with the
`--no-gate` variant — the format diffs are the proof, the gate is a
separate step:

```sh
python3 factory.py specs/formats-test.json --out out/formats-test.html --no-gate
diff formats/official-unfold.html out/official-unfold.html
diff formats/official-slideshow.html out/official-slideshow.html
```

The test spec is `specs/formats-test.json` (dashboard-door only — the
format step is what is proven). It is on the branch; the old verify command
named `specs/smart-links-stats.json`, which is NOT on the branch (it exists
only locally) — do not use it.

The test build is self-contained from branch files alone: `assemble()`
loads `parts-registry-v1.json` unconditionally, and that file is filed on
the branch at `TEAM-NITRO/interface-factory/parts-registry-v1.json`
(687,429 B, sha256
`065d967290aeff3cd33907ef4b972980632623bf3194af40f6e8a04375688440`).
Verify it before running the test if the registry is ever in doubt:
`sha256sum parts-registry-v1.json` must print that digest.

## When a new canonical version lands

A new canonical unfold/slideshow arrives ONLY as a new filed file with a
new blob sha from its own round — never by editing these files in place.
Replace the file, update the `FORMATS` table in `factory.py` AND this file
(blob sha, bytes, sha256) in the same pass, re-run the verify above, and
file. A hash mismatch after replacement means the wrong bytes were stored.
