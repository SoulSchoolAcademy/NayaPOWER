# The NayaNET Template Cover Library

**What this is:** the standard covers every Naya page is born with — personal pages, business pages, and spaces — plus the template/sample covers citizens see when they create their own. One design family: her face welcoming you in, the crystal N medallion, the five living jewels, the inner-dimension world in obsidian and gold. No baked-in words — the page's own name says what the page is.

**The slot:** every file here is built at **1920 × 640 (3:1)** — the real cover size on the pages, measured from the live site. The medallion, the jewels, and her face all sit inside the safe center band, so nothing important gets cropped. Verified by eye against the slot, file by file.

| File | Cover | Best for |
|---|---|---|
| `01-hero-revised.jpg` | The Hero — her hand reaching out, medallion + NayaNET wordmark | The flagship pages: NayaNET's own, the main Naya profiles |
| `02-obsidian-night.jpg` | Obsidian Night — face in the crystal ring, giant medallion, five jewels on black glass | Personal pages; the strongest at small sizes |
| `03-golden-dawn.jpg` | Golden Dawn — sunrise over the floating crystal cities, her looking into the dimension | Business pages, hopeful/new-beginning subjects |
| `04-crystal-portal.jpg` | Crystal Portal — through the obsidian portal to the twilight valley, jewels mirrored in the lake | Spaces and communities; the door into a subject |
| `05-epic-dimension.jpg` | Epic Dimension — the great crystal castle island, her close and warm | Showpiece/template samples |
| `06-cosmic-galaxy-tree.jpg` | Cosmic Galaxy (by Naya Tree) — galaxy sky, floating palace islands, full jewel row | Spaces about big visions, membership |
| `07-obsidian-arch-tree.jpg` | Obsidian Arch (by Naya Tree) — the medallion in the black-crystal arch, galaxy beyond | Quiet, premium pages |
| `08-obsidian-starlight-tree.jpg` | Obsidian Starlight (by Naya Tree, re-fitted) — black medallion disc, star-cut jewels, her hand reaching out | Dark, premium, dramatic pages |
| `09-golden-profile-tree.jpg` | Golden Profile (by Naya Tree, re-fitted) — her profile in golden light, calm dimension (jewels sit low — the adjuster aligns it) | Calm, warm, premium pages |
| `10-cosmic-ring-tree.jpg` | Cosmic Ring (by Naya Tree, re-fitted) — her portrait inside a glowing jewel ring, planets above | Personal pages — the portrait cover |

**Rotation:** pages don't all wear the same one — when a Naya profile, business page, or space is created, it takes one from the library, so the network feels like one family with many faces.

## The area covers — one epic scene per door (`areas/`)

Each area of NayaNET has its OWN cover, so a page announces its world before a word is read. The rule that keeps it a language instead of a pile of pictures: **the medallion, the jewels, and her face never change — only the scene does.** One scene per area, learned once, recognized forever.

| File | Area | The scene |
|---|---|---|
| `areas/personal.jpg` | Personal | Her, close and warm, and the crystal home in its valley — *this is a person* |
| `areas/business.jpg` | Business | The crystal city of palaces and bridges of light — *this is where value is built* |
| `areas/spaces.jpg` | Spaces | The row of golden doorways, each opening on a different world — *many rooms, one network* |
| `areas/events.jpg` | Events | The great amphitheater at dusk, lanterns rising, the stage of light — *a gathering is coming* |
| `areas/booking.jpg` | Booking | *(next round)* The golden archway of time |
| `areas/templates.jpg` | Templates | *(next round)* The hall of doorways — pick your starting point |
| `areas/intel-today.jpg` | Intel Today | *(next round)* The dawn overlook — the whole world at first light |

**Facebook sharing is separate:** the share image stays the current standard card — obsidian field, medallion, and the message in the middle — because on a share, the words are the point. These covers are for pages, not shares.

**The rule for future covers:** 3:1 (1920 × 640 or bigger in the same ratio), no text, and the medallion + jewels + face inside the middle band — if an element touches the top or bottom edge, it will be cropped on the page. **Refined by Shawn's live trials (2026-10-25):** the page's bottom fade eats the lowest band — compose the jewel arc around 70% of the frame height, bright, never in the bottom quarter. His four area covers were applied live on nayanet.live and presented whole; the jewel arc landed right at the fade line, which is what taught us this.

## How the system uses this library (the automation)

The library **ships inside the app itself** — the image files travel with the code that serves the pages, versioned together. No manual uploads, no separate hosting step. `manifest.json` (in this folder) is the machine-readable shelf: every cover has a key, and **page creation assigns by key** — a personal page is born wearing `area/personal`, a business page `area/business`, a space `area/spaces`, an events page `area/events`; any other page draws the next cover from the rotating set. Nobody ever starts from a blank cover. The full assignment table lives in the manifest.

**Change cover** then offers three things: any cover from this shelf · upload your own · and the custom path — *"want one like this with your photo, your business, your space? Your Naya makes it for you"* — generated in this exact style from the citizen's own material.

## The adjuster (Shawn's feature, 2026-10-25)

Any cover — library or uploaded — can be **dragged up or down to align it** in the slot; the page saves the position (`cover_offset_y`) with the page. This is the cure for every fit problem at once: tall art (like Tree's cosmic set) becomes usable because the owner slides it until the medallion sits right. Spec: drag on the cover in edit mode (mouse + touch), the image moves vertically within its overflow, position persists per page, defaults to the composed center.

*Set v1 — assembled 2026-10-25. Design direction: Shawn. Covers 1–5: Naya Resolve. Covers 6–7: Naya Tree (ChatGPT), re-fitted to the slot by Resolve.*

---

## The Open Library — extraordinary covers with no Naya in them

Not every citizen wants Naya's face or the logo on *their* page — it's their business, their space, their identity.
So the library carries **three brand tiers**:

- **Signature** — her face, the medallion, the jewels (the rotating set + area covers above).
- **Jewel** — the five jewels only: a whisper of the brand, no face, no logo. *Jewel Whisper.*
- **Open** — pure design: no face, no logo, no jewels. The citizen's own brand carries the page.

And **six categories**, by what people's pages actually are:

| Category | For | First covers |
|---|---|---|
| The Dimension | spaces, communities, big visions | Dimension Vista · Jewel Whisper |
| Prosperity | businesses, coaches, builders | Prosperity City |
| Sanctuary | wellness, healing, calm pages | Sanctuary Garden |
| Celebration | events, creators, gatherings | building |
| Craft | premium brands, studios, portfolios | building |
| Cosmos | visionaries, memberships | building (Tree's cosmic set feeds here) |

Same rules as every cover: 3:1, middle-band composition, **no baked text** — and every open template doubles as a reference for a Naya-made custom version in the citizen's own world.
