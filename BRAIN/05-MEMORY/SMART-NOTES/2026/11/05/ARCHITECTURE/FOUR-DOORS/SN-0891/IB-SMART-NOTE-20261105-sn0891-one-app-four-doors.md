# One App, Four Doors — The Spec
SN-0891 · ARCHITECTURE / FOUR-DOORS
**Created:** 2026-11-05T01:46:00Z

## In A Nutshell
One app, four doors: Personal, Business, Space, Membership. Each contains the others. All synced. The membership's front door is the login; the rest share one banner, clearly labeled.

## The Architecture
**Nested:** Every door holds the others inside it. A personal page can hold a membership. A business can hold one. A space can hold one. A membership can hold a business, a personal, the community, the running feed. They all contain each other.

**Synced:** All four stay in step with each other. Change it in one place, it's true everywhere.

**The doors:** Membership's front door is the login — the portal. Personal, Business, and Space share the same banner and bones, but it's unmistakable which world you're in: clear it's personal, clear it's business, clear it's the space.

**From any door, every door:** They're aligned and connected. Move freely between them.

## On Every Page
- Sign up to NayaNET, linked to that page's URL
- Installable as an app
- One stats language — same format on all pages
- Scheduler and journal showing what's going on in that world
- Schedule appointments across worlds — personal to business, business to space
- Look back at any day: see what happened, see the stats

## The Gate
Creating a membership takes Pro or Max. That's the line.

## How It Applies
Build personal first, complete. Clone to business, space, membership — same heart, different labels, membership with the login door. The citizen lives in whichever door fits the moment, and everything follows them. One living app wearing four faces.

*Shawn's spec, 2026-11-05 ~01:30Z. Filed by Naya Nitro Narzan.*
