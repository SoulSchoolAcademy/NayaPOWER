# No Limit — The Tiles Shrink to Fit the Page

SN-2227 · DESIGN / THE ULTIMATE NUMBER — NO LIMIT

**Created:** 2026-11-07 21:23Z

> "If it fits on the page, it is good to go. If you ever get a number that does not fit on the page — congratulations."

## Hook

Five digits. Six. Seven. Eight. As many as it takes. The tiles shrink so the number always fits.

## Nutshell

There is no limit on the digits. `fitNumber(el)` measures the number against its well and scales the whole number down to fit the page width. The tiles shrink; the number never wraps and never overflows. `white-space: nowrap` keeps the tiles in one row. An 8-digit demo (12,345,678) proves it on the concepts page. If it fits on the page, it is good to go. If you ever get a number that does not fit on the page — congratulations.

## Human

Shawn's rule: make it dynamic, no limit. Five digits, six, seven, eight — whatever it takes. Don't cap it. If it fits on the page, it's good. And if a number ever doesn't fit on the page, that's not a problem — that's a congratulations.

## Child

No matter how big your number gets, the boxes shrink a little so they all still fit on the page in one row. They never fall off the edge. And if your number gets so big it can't fit — wow, that's amazing.

## Grandma

There's no cap on how big the number can get. The tiles just get a little smaller so they all fit. And if your number ever gets too big for the page — well, that's a wonderful problem to have.

## Naya

No limit is a design decision, not a technical one. A capped number says "we didn't think you'd get this far." An uncapped number says "go as far as you can — we'll keep up." The fit logic is the machine keeping its promise.

## What it means

- `fitNumber(el)`: measure against the well, scale the whole number to fit. `white-space: nowrap`: one row, always.
- 8-digit demo (12,345,678) on the concepts page. A screen check on the current version is running.
- The Dashboard's number uses the same fit logic (addendum 6).

## Why it matters

A limit is a ceiling on the user's success. Removing it is a promise: the system will never be the thing that stops you from growing.

## What changes now

- No number in the system has a digit limit. Ever.
- The fit logic is part of the asset, not an afterthought — it ships with the number.
