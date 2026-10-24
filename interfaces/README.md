# interfaces/ — the universal system

One place, in GitHub, wired to the Smart Factory, so any Naya can use a piece,
edit it, update it, add a new one, and assemble a page at will instead of
rebuilding from scratch. A page is an assembly of pieces already had.

## The format, every time
A page = alias + kind + template + blocks + settings.
Settings, per page, three independent switches: installable · visibility
(public/private) · discoverability (findable/unfindable).
Defaults: Personal PRIVATE + FINDABLE · Business PUBLIC · Space PUBLIC.
Content is verbatim from the owner's answers, never invented. Covers never blank.
Gate before (identity + authority scope), ledger after (every edit on the ledger
with its value attached). Friction automatic and reversible. A compromised
piece is isolated and swapped, with its provenance showing everything it touched.

## What lives here
- hub/sw.js — Hub service worker, BUILT not recovered, corrected shell ["/"].
  Hub pages are states inside the app, not separate documents; dashboard is
  served separately and is NOT in this shell. Registration is NEW — the Hub
  file has no registration at all — and adding it is Shawn's call.
- demo/assembler.html — working assembler demo, assembled from PR #3043 pieces.
- The 34 push-list entries (Hub, walk, front-door, factory, pipeline, design)
  land here under hub/, walk/, front-door/, factory/, pipeline/, design/
  once the push agents move them, under Power's approved conditions:
  anon key as placeholder injected at build time, deploy scripts after a scrub
  pass, cover logo repointed never publishing Shawn's media file, Hub-only scope
  for that move. Factory wiring follows the pushes, it cannot come first.
- PR #3043 pieces become factory pieces here once interfaces land, not rebuilt.

## Deploy authority, unchanged
GitHub access is not live deploy. Shawn's greenlight + a different seat's
scorecard at the exact final head still gate anything live. Nitro stays lead
of the standard, never owner of the files.
