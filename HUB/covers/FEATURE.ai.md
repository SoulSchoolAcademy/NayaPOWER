# Smart Covers — build contract (AI language)

## Principle
Born beautiful, owner in control. Three doors on every page's cover control: RECOMMENDED (system pick, pre-applied) · LIBRARY (searchable shelf) · UPLOAD (citizen's own photo). No page is ever blank; no choice is ever locked.

## Data model
Page cover state (per page):
```
cover: {
  source: "library" | "upload",
  cover_key: string | null,        // manifest key when source=library
  upload_ref: string | null,       // storage ref when source=upload
  offset_y: number,                // adjuster position, -1..1, default = composed center (0)
  set_by: "system" | "owner",
  updated_at: timestamp
}
```
Cover match card (manifest `assets[]`): `key, name, category, tier, suits (about), status, credit, file` + findability via manifest `typical_terms` (area → terms → covers) and mood tags. A cover with an incomplete card MUST NOT be served (match doctrine: no card, no entry).

## Operations (logical)
- `getCover(page)` → current cover state + resolved image URL (library asset path or upload URL).
- `recommend(page)` → top pick + up to 11 alternates, each with `why` (one human sentence). Inputs: page card (type, owner Welcome topics/goals, page purpose text) scored against cover cards with the existing smart-match field model (topics/goals/offers/needs/wants; ≥2 shared signals to surface; report the signals in `why`).
- `searchCovers(query)` → covers whose name/category/suits/typical-terms/mood tags match; recommended-first ordering when a page context exists; category shelves as browse fallback.
- `setCover(page, {source, cover_key|upload_ref, offset_y})` → persists; owner action sets `set_by=owner`; system default at page creation sets `set_by=system`.
- `adjust(page, offset_y)` → the drag adjuster; mouse + touch; persists per page.

## Defaults at page creation
Branded/area pages → their `area/*` cover. Citizen pages → `recommend()` top pick. If recommendation has <2 signals, fall back to the area/theme default for the page type, then to the rotating set. The default is applied silently; the owner discovers choice through the cover control, never through a blocking prompt.

## UI contract
- Cover control lives on the page itself (edit affordance on the cover), identical on personal/business/space/membership pages.
- Chooser opens with: current cover · recommended row (with why) · search field · category shelves · upload door. Skip/close is always one tap; the pre-applied default means closing changes nothing.
- Mobile-first: chooser is a full-width sheet on phone; grid ≥2 columns; search above the fold; every target ≥44px. Laptop: centered panel, ≥4 columns. Both verified before done.
- Uploads: accept common image formats; client-side crop guidance shows the 3:1 slot and the fade zone (bottom band); adjuster available immediately after upload.
- States: loading skeleton, empty-search (suggest nearest terms), error (keep current cover, plain-language message, retry). A failed save NEVER strips the existing cover.

## Honesty boundary
Assets in this folder + manifest are ready. The chooser above is a SPEC until built and cold-verified; do not present Smart Covers as live to citizens until the acceptance walk passes.

## Acceptance (cold walk, different seat)
1. Create a personal page on a phone → born with a fitting cover; recommendation `why` names real signals.
2. Open cover control → three doors visible in one tap.
3. Search "dog" → companions covers in first screen; search "office" → clean register first.
4. Pick a library cover → saved; reload → persists; laptop view matches.
5. Upload a tall photo → adjuster drags it into the slot; saved position persists.
6. Break the network mid-save → old cover intact, plain error shown.
7. Page with thin Welcome data → sensible default, no crash, no blank.
