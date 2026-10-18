#!/usr/bin/env python3
"""Smart Builder APP-MODE assembler v2 — contract-v1 JSON in, working app out.

Contract data + template blueprint + premade function units -> a working,
self-contained app page (index.html [+ page2.html] + functions/ dir).

v2 (2026-10-18): the page chassis FOLLOWS AND ADAPTS the Hub app
(~/workspace/user/files/index-2.html) — fixed left rail (collapsible room
navigation) + topbar (rooms-plus mobile, rail-toggle, title, eco-plus
destinations menu) + main scroll surface + mobile drawer. Corner plus
buttons are harvested verbatim from the Hub and take each template's soul
color for hover ignition. Discrete pieces (section boards, hero orbs) are
composed verbatim from the 478-piece builder index. A design-law gate
(gate_design_laws) runs on every rendered page BEFORE writing — any
violation fails the build with a non-zero exit naming the law.

Usage:
  python3 appmode.py --contract appmode-contracts/personal.json \
      --outdir appmode-out/personal \
      --units /tmp/units/HUB/design-system/tools/smart-builder/functions/premade \
      --manifest appmode-out/personal/manifest.json

Rules (from assembler-appmode-spec-v1):
  - Additive module: never touches assemble.py's existing paths.
  - Section order per template is FIXED (the blueprint). Same contract ->
    byte-identical output (no timestamps, sorted keys, fixed ordering).
  - Function-first layout; density: a section with no working control is
    dropped from the build.
  - Fail-closed: `!no-unit:` keys are OMITTED and listed under
    manifest.missing_functions. Unknown function id -> build FAILS. A
    function that is ON but has no unit file -> build FAILS, never a dead
    control. A picked piece whose html is not standalone markup -> FAILS.
  - All unit files are copied byte-identical into <outdir>/functions/.
  - Hub chassis (verbatim harvest, sha-pinned) + soul accents + spectrum
    section walk + elevation + white-at-rest -> color-on-hover ignition.
    White text always (Law 1 — kickers white, Shawn's word outranks the
    Hub file). Newsreader hero voice + Inter UI (Law 9).
"""
import argparse
import hashlib
import html as htmlmod
import json
import os
import shutil
import sys
import urllib.parse

APPMODE_VERSION = "appmode-v2"
LOADER_FILE = "naya-functions.js"

# contract-id -> (register-id, unit file). The units register under the
# register-id; the page mounts <div data-fn="<register-id>">.
REGISTER = {
    "smart-tabs": ("smart-tabs", "f-01-smart-tabs.js"),
    "smart-mail": ("smart-mail", "f-02-smart-mail.js"),
    "smart-lists": ("smart-lists", "f-03-smart-lists.js"),
    "smart-spaces": ("smart-spaces", "f-04-smart-spaces.js"),
    "intelligence-today": ("intelligence-today", "f-05-intelligence-today.js"),
    "connections": ("connections", "f-06-connections.js"),
    "reports": ("reports", "f-07-reports.js"),
    "feed": ("feed", "f-08-feed.js"),
    "booking": ("f-09-booking", "f-09-booking.js"),
    "menu-display": ("f-10-menu-display", "f-10-menu-display.js"),
    "product-display": ("f-11-product-display", "f-11-product-display.js"),
    "signup-capture": ("f-12-signup-capture", "f-12-signup-capture.js"),
    "event-rsvp": ("f-13-event-rsvp", "f-13-event-rsvp.js"),
    "assessment-score": ("f-14-assessment-score", "f-14-assessment-score.js"),
    "portfolio-showcase": ("f-15-portfolio-showcase", "f-15-portfolio-showcase.js"),
    "community-feed": ("f-16-community-feed", "f-16-community-feed.js"),
    "business-proof": ("f-17-business-proof", "f-17-business-proof.js"),
    "profile-link": ("f-18-profile-link", "f-18-profile-link.js"),
    "navigate": ("f-19-navigate", "f-19-navigate.js"),
    "search": ("f-20-search", "f-20-search.js"),
    "contact": ("f-21-contact", "f-21-contact.js"),
    "share": ("f-22-share", "f-22-share.js"),
    "save": ("f-23-save", "f-23-save.js"),
    "play": ("f-24-play", "f-24-play.js"),
    "dictate": ("dictate", "f-25-dictate.js"),
    "copy": ("copy", "f-26-copy.js"),
    "preview": ("preview", "f-27-preview.js"),
    "cart": ("cart", "f-28-cart.js"),
    "contract-draft": ("contract-draft", "f-29-contract-draft.js"),
    "join": ("f-30-join", "f-30-join.js"),
}

NO_UNIT_PREFIX = "!no-unit:"

# ---------------------------------------------------------------------------
# Template blueprints (spec section 4). Section order is fixed per template.
# Each section: id, kicker, title, contract-ids mounted in order, page (1|2).
# ---------------------------------------------------------------------------
BLUEPRINTS = {
    "personal": {
        "soul": "#a06bff",
        "pages": {"index.html": "Home", "page2.html": None},
        "sections": [
            ("briefing", "This morning", "Today's briefing", ["intelligence-today"], 1),
            ("capture", "Capture", "Say it before you lose it", ["dictate"], 1),
            ("lists", "Lists", "Everything, listed", ["smart-lists"], 1),
            ("stream", "Stream", "Your feed", ["feed"], 1),
            ("people", "People", "Your people", ["connections", "contact", "share", "save"], 1),
        ],
    },
    "today": {
        "soul": "#40d3bb",
        "pages": {"index.html": "Briefing"},
        "sections": [
            ("briefing", "Good morning", "Today's briefing", ["intelligence-today"], 1),
            ("metrics", "The numbers", "How things stand", ["reports"], 1),
            ("stream", "Log", "Founder log", ["feed"], 1),
        ],
    },
    "smartlist": {
        "soul": "#ffbf3d",
        "pages": {"index.html": "Lists"},
        "sections": [
            ("lists", "Track it", "The renovation, listed", ["smart-lists"], 1),
            ("saved", "Keep", "Saved decisions", ["save"], 1),
            ("share", "Share", "Send this list", ["share"], 1),
        ],
    },
    "business": {
        "soul": "#3fb8ff",
        "pages": {"index.html": "Home", "page2.html": "Visit"},
        "sections": [
            ("proof", "Why us", "What we do", ["business-proof"], 1),
            ("booking", "Book", "Reserve a table", ["booking"], 1),
            ("nav1", "Navigate", "Find your way", ["navigate"], 1),
            ("people", "Team", "The people behind the counter", ["connections"], 2),
            ("contact", "Reach us", "Say hello", ["contact"], 2),
            ("nav2", "Navigate", "Find your way", ["navigate"], 2),
        ],
    },
    "booking": {
        "soul": "#2fe89e",
        "pages": {"index.html": "Book"},
        "sections": [
            ("booking", "Book", "Pick a service, pick a slot", ["booking"], 1),
            ("contact", "Questions", "Ask us anything", ["contact"], 1),
        ],
    },
    "product": {
        "soul": "#e84fff",
        "pages": {"index.html": "Shop"},
        "sections": [
            ("product", "The lamp", "Made by hand", ["product-display"], 1),
            ("cart", "Cart", "Your picks", ["cart"], 1),
            ("share", "Share", "Tell a friend", ["share"], 1),
            ("contact", "Questions", "Ask the maker", ["contact"], 1),
        ],
    },
    "event": {
        "soul": "#ff9a5a",
        "pages": {"index.html": "RSVP"},
        "sections": [
            ("rsvp", "You're invited", "Save your spot", ["event-rsvp"], 1),
            ("share", "Share", "Bring a friend", ["share"], 1),
            ("contact", "Questions", "Ask the host", ["contact"], 1),
        ],
    },
    "community": {
        "soul": "#ff5e6c",
        "pages": {"index.html": "The feed", "page2.html": "My street"},
        "sections": [
            ("feed", "Happenings", "The street feed", ["community-feed"], 1),
            ("spaces", "Spaces", "Find your crew", ["smart-spaces"], 1),
            ("nav1", "Navigate", "Find your way", ["navigate"], 1),
            ("join", "Join", "Claim your spot", ["join"], 2),
            ("spaces2", "Spaces", "Browse and manage", ["smart-spaces"], 2),
            ("nav2", "Navigate", "Find your way", ["navigate"], 2),
        ],
    },
    "portfolio": {
        "soul": "#6675ff",
        "pages": {"index.html": "Work"},
        "sections": [
            ("work", "Selected work", "The frames", ["portfolio-showcase"], 1),
            ("share", "Share", "Pass it on", ["share"], 1),
            ("contact", "Book me", "Let's make something", ["contact"], 1),
        ],
    },
    "menu": {
        "soul": "#b8ee57",
        "pages": {"index.html": "Menu"},
        "sections": [
            ("menu", "Eat & drink", "The menu", ["menu-display"], 1),
            ("contact", "Catering", "Feed a crowd", ["contact"], 1),
        ],
    },
    "signup": {
        "soul": "#40d3bb",
        "pages": {"index.html": "Join"},
        "sections": [
            ("signup", "Join in", "Take the challenge", ["signup-capture"], 1),
            ("mail", "Stay close", "Notes from the host", ["smart-mail"], 1),
        ],
    },
    "dashboard": {
        "soul": "#a06bff",
        "pages": {"index.html": "Readiness", "page2.html": "Training"},
        "sections": [
            ("assessment", "Check", "Marathon readiness check", ["assessment-score"], 1),
            ("nav1", "Navigate", "Find your way", ["navigate"], 1),
            ("reports", "Numbers", "This week's training", ["reports"], 2),
            ("briefing", "Today", "Today's plan", ["intelligence-today"], 2),
            ("nav2", "Navigate", "Find your way", ["navigate"], 2),
        ],
    },
}

PAGE_FILENAMES = ["index.html", "page2.html"]

# ---------------------------------------------------------------------------
# Default configs per template (spec weights section 3.4). Realistic, in the
# owner's voice, seeded from the contract's idea/vision/handle. Never lorem
# ipsum. Configs are pure functions of (template, contract) -> deterministic.
# ---------------------------------------------------------------------------

def _svg_datauri(title, c1, c2):
    """Self-contained gradient placeholder image (no network). Deterministic."""
    t = (title or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
        "</linearGradient></defs>"
        '<rect width="800" height="600" fill="url(#g)"/>'
        '<circle cx="620" cy="140" r="180" fill="rgba(255,255,255,.12)"/>'
        '<circle cx="150" cy="470" r="120" fill="rgba(0,0,0,.18)"/>'
        '<text x="60" y="540" font-family="Georgia,serif" font-size="44" '
        'fill="rgba(255,255,255,.92)">%s</text></svg>'
    ) % (c1, c2, t)
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg, safe=":/?#[]@!$&'()*+,;=%")


def _nav_config(blueprint, page_file):
    rooms = [
        {"label": label, "href": fname}
        for fname, label in blueprint["pages"].items()
        if label
    ]
    active = next(
        (i for i, r in enumerate(rooms) if r["href"] == page_file), 0
    )
    return {
        "rooms": rooms,
        "active": active,
        "accent": blueprint["soul"],
    }


def default_config(template, contract_id, contract, blueprint, page_file):
    """Return the default data-fn-config for (template, contract-id)."""
    soul = blueprint["soul"]
    idea = contract.get("idea", "")
    vision = contract.get("vision", "")
    handle = contract.get("handle", "naya")

    if contract_id == "smart-tabs":
        if template == "personal":
            tabs = [
                {"id": "home", "label": "Home", "url": "index.html"},
                {"id": "portfolio", "label": "Portfolio", "url": "https://www.behance.net"},
                {"id": "invoices", "label": "Invoices", "url": "https://www.waveapps.com"},
                {"id": "type", "label": "Type inspiration", "url": "https://fonts.google.com"},
                {"id": "cal", "label": "Calendar", "url": "https://calendar.google.com"},
            ]
        elif template == "today":
            tabs = [
                {"id": "home", "label": "Briefing", "url": "index.html"},
                {"id": "analytics", "label": "Analytics", "url": "https://analytics.google.com"},
                {"id": "bank", "label": "Bank", "url": "https://www.mercury.com"},
                {"id": "notes", "label": "Notes", "url": "https://www.notion.so"},
            ]
        elif template == "booking":
            tabs = [
                {"id": "home", "label": "Book", "url": "index.html"},
                {"id": "services", "label": "Services", "url": "#sec-booking"},
                {"id": "reviews", "label": "Reviews", "url": "https://www.google.com/maps"},
                {"id": "instagram", "label": "Instagram", "url": "https://www.instagram.com"},
            ]
        else:
            tabs = [{"id": "home", "label": "Home", "url": "index.html"}]
        return {"tabs": tabs, "title": "Smart Tabs", "storageKey": "naya.appmode.%s.tabs" % handle}

    if contract_id == "smart-mail":
        return {
            "title": "Notes from the host",
            "recipients": [
                {"name": "Challenge crew", "email": "crew@shipit.example"},
                {"name": "Mara (co-host)", "email": "mara@shipit.example"},
            ],
            "draftsKey": "naya.appmode.%s.mail.drafts" % handle,
            "outboxKey": "naya.appmode.%s.mail.outbox" % handle,
        }

    if contract_id == "smart-lists":
        if template == "personal":
            lists = [
                {"id": "week", "name": "This week", "items": [
                    {"id": "w1", "text": "Finish Alto Studio homepage mockups", "type": "note", "done": False},
                    {"id": "w2", "text": "Send invoice #1042 ($2,400)", "type": "note", "done": False},
                    {"id": "w3", "text": "Prep portfolio PDF for Friday review", "type": "note", "done": False},
                    {"id": "w4", "text": "Call mom back", "type": "note", "done": True},
                ]},
                {"id": "inspo", "name": "Inspiration shelf", "items": [
                    {"id": "i1", "text": "Swiss grid posters — that 1962 Muller-Brockmann show", "type": "topic", "done": False},
                    {"id": "i2", "text": "Embossed letterpress textures", "type": "topic", "done": False},
                ]},
                {"id": "thanks", "name": "People to thank", "items": [
                    {"id": "t1", "text": "Priya — intro to Alto Studio", "type": "contact", "done": False},
                    {"id": "t2", "text": "Sam — lent the medium-format camera", "type": "contact", "done": True},
                ]},
            ]
        else:  # smartlist template: home renovation tracker
            lists = [
                {"id": "kitchen", "name": "Kitchen", "items": [
                    {"id": "k1", "text": "Demo done — dust everywhere, worth it", "type": "note", "done": True},
                    {"id": "k2", "text": "Cabinets ordered — delivery Oct 28", "type": "note", "done": True},
                    {"id": "k3", "text": "Pick backsplash tile (narrowed to 2)", "type": "note", "done": False},
                    {"id": "k4", "text": "Electrician Thursday 9am — be home", "type": "note", "done": False},
                ]},
                {"id": "budget", "name": "Budget watch", "items": [
                    {"id": "b1", "text": "Cabinets $8,400 (paid deposit $2,500)", "type": "note", "done": False},
                    {"id": "b2", "text": "Quartz countertops $3,100", "type": "note", "done": False},
                    {"id": "b3", "text": "Flooring $2,750 — under estimate!", "type": "note", "done": False},
                ]},
                {"id": "decide", "name": "Decisions pending", "items": [
                    {"id": "d1", "text": "Backsplash: zellige vs. handmade subway", "type": "topic", "done": False},
                    {"id": "d2", "text": "Paint: Swiss Coffee vs. Alabaster", "type": "topic", "done": False},
                    {"id": "d3", "text": "Contractor: ask Luis for the tile quote", "type": "contact", "done": False},
                ]},
            ]
        return {"lists": lists, "title": "Smart Lists",
                "storageKey": "naya.appmode.%s.lists" % handle}

    if contract_id == "smart-spaces":
        spaces = [
            {"id": "blockparty", "name": "Block Party Crew", "topic": "events",
             "desc": "Planning the September block party — grills, permits, playlist.",
             "color": "#ff5e6c", "privacy": "neighbors", "members": ["June", "Marcus", "Priya"]},
            {"id": "garden", "name": "Garden Share", "topic": "garden",
             "desc": "Extra tomatoes? Borrow the tiller? It lives here.",
             "color": "#2fe89e", "privacy": "neighbors", "members": ["June", "Theo"]},
            {"id": "lostfound", "name": "Lost & Found", "topic": "help",
             "desc": "One grey cat, several ladders, a missing porch package.",
             "color": "#3fb8ff", "privacy": "neighbors", "members": ["Marcus"]},
        ]
        return {"spaces": spaces, "title": "Smart Spaces",
                "storageKey": "naya.appmode.%s.spaces" % handle}

    if contract_id == "intelligence-today":
        if template == "personal":
            items = [
                {"date": "daily", "time": "07:30", "title": "Morning pages", "detail": "Ten minutes, pen first, phone second.", "kind": "note"},
                {"date": "daily", "time": "10:30", "title": "Deep work: Alto Studio mockups", "detail": "Homepage v3 — no meetings before noon.", "kind": "verified"},
                {"date": "daily", "time": "18:00", "title": "Invoice #1042 goes out Friday", "detail": "$2,400 — don't let it slide to Monday.", "kind": "alert"},
                {"date": "2026-10-18", "time": "15:00", "title": "Portfolio review call", "detail": "Friday prep starts today: export the PDF.", "kind": "stated"},
            ]
            title = "Intelligence Today"
        elif template == "today":
            items = [
                {"date": "daily", "time": "08:00", "title": "The one thing", "detail": "Ship the onboarding fix before anything else.", "kind": "verified"},
                {"date": "daily", "time": "09:15", "title": "Standup", "detail": "Blockers only. Fifteen minutes, hard stop.", "kind": "note"},
                {"date": "daily", "time": "12:30", "title": "MRR check", "detail": "Are we still above $12k? Know the number.", "kind": "alert"},
                {"date": "daily", "time": "18:00", "title": "Gym or it doesn't happen", "detail": "Bag's packed. No negotiation.", "kind": "note"},
                {"date": "2026-10-18", "time": "16:00", "title": "Investor update draft", "detail": "Due tonight — numbers, wins, one ask.", "kind": "stated"},
            ]
            title = "Today's Briefing"
        else:  # dashboard: today's training plan
            items = [
                {"date": "daily", "time": "06:30", "title": "Today's session", "detail": "Check page one — the readiness board sets the plan.", "kind": "verified"},
                {"date": "daily", "time": "21:30", "title": "Lights out", "detail": "Sleep is training. Phone charges in the kitchen.", "kind": "note"},
                {"date": "2026-10-20", "time": "06:30", "title": "Tempo Tuesday — 6 miles", "detail": "2 easy, 3 at tempo, 1 easy. Leave the watch at home if the legs feel heavy.", "kind": "verified"},
                {"date": "2026-10-24", "time": "07:00", "title": "Long run Saturday — 18 miles", "detail": "Route: riverside loop x3. Gels at 45/90/135 min.", "kind": "alert"},
            ]
            title = "Today's Plan"
        return {"items": items, "title": title}

    if contract_id == "connections":
        if template == "personal":
            people = [
                {"id": "p1", "name": "Priya Nair", "role": "Client — Alto Studio", "color": "#a06bff", "phone": "(555) 014-2288", "note": "Prefers email over calls. Decision-maker on the rebrand."},
                {"id": "p2", "name": "Sam Okafor", "role": "Collaborator — photography", "color": "#3fb8ff", "phone": "(555) 019-7731", "note": "Lent the medium-format camera. Owes me a print."},
                {"id": "p3", "name": "Dana Whitfield", "role": "Mentor", "color": "#2fe89e", "phone": "", "note": "Monthly coffee. Ask about the studio lease question."},
            ]
        else:  # business: café team
            people = [
                {"id": "s1", "name": "Maya Reyes", "role": "Head barista", "color": "#3fb8ff", "phone": "(555) 011-3420", "note": "Pulls the best cortado on the street. Ask about the new roast."},
                {"id": "s2", "name": "Jonah Fields", "role": "Baker", "color": "#ffbf3d", "phone": "", "note": "Cardamom buns sell out by 9. He starts at 4am — be kind."},
                {"id": "s3", "name": "Theo Alvarez", "role": "Owner", "color": "#2fe89e", "phone": "(555) 011-8890", "note": "Catering and events. Replies within a day."},
            ]
        return {"people": people, "title": "Connections",
                "storageKey": "naya.appmode.%s.connections.messages" % handle}

    if contract_id == "reports":
        if template == "today":
            reps = {
                "daily": [
                    {"title": "Active users", "value": "1,842", "delta": "+3.1%", "note": "Yesterday vs. 7-day average."},
                    {"title": "Signups", "value": "64", "delta": "+12", "note": "Best Thursday in six weeks."},
                    {"title": "Support tickets", "value": "9", "delta": "-4", "note": "Onboarding fix is working."},
                ],
                "weekly": [
                    {"title": "MRR", "value": "$12,400", "delta": "+4.2%", "note": "Two upgrades, one save."},
                    {"title": "Churn", "value": "2.1%", "delta": "-0.4 pts", "note": "Trending the right way."},
                    {"title": "NPS", "value": "58", "delta": "+6", "note": "From the October survey."},
                ],
                "monthly": [
                    {"title": "Revenue", "value": "$48,900", "delta": "+11%", "note": "Best month yet."},
                    {"title": "Burn multiple", "value": "1.8x", "delta": "-0.3", "note": "Efficient growth."},
                    {"title": "Runway", "value": "21 mo", "delta": "+2", "note": "At current burn."},
                ],
            }
            title = "Reports"
        else:  # dashboard: training numbers
            reps = {
                "daily": [
                    {"title": "Sleep", "value": "7h 42m", "delta": "+26m", "note": "Best this week."},
                    {"title": "Resting HR", "value": "48", "delta": "-2", "note": "Fitness is showing."},
                    {"title": "Soreness", "value": "2/10", "delta": "-1", "note": "Legs are fresh."},
                ],
                "weekly": [
                    {"title": "Mileage", "value": "52 mi", "delta": "+6", "note": "Peak week two of three."},
                    {"title": "Long run", "value": "18 mi", "delta": "done", "note": "Saturday, riverside loop."},
                    {"title": "Avg pace", "value": "8:42/mi", "delta": "-0:09", "note": "Easy miles staying easy."},
                ],
                "monthly": [
                    {"title": "Total miles", "value": "198", "delta": "+24", "note": "Biggest month ever."},
                    {"title": "Workouts", "value": "21", "delta": "all done", "note": "Zero skipped sessions."},
                    {"title": "Race day", "value": "T-21d", "delta": "", "note": "Taper starts in one week."},
                ],
            }
            title = "Training Numbers"
        return {"reports": reps, "title": title}

    if contract_id == "feed":
        if template == "personal":
            seed = [
                {"id": "s1", "author": "Maya", "text": "Homepage v2 is out the door. The grid finally breathes.", "ts": "2h ago", "likes": 4},
                {"id": "s2", "author": "Maya", "text": "Note to self: invoice BEFORE the weekend, not during.", "ts": "yesterday", "likes": 2},
            ]
            title = "Your Feed"
        else:
            seed = [
                {"id": "s1", "author": "Founder log", "text": "Onboarding fix shipped. Support tickets already dropping.", "ts": "8:04 AM", "likes": 6},
                {"id": "s2", "author": "Founder log", "text": "Reminder: the update draft is due tonight. Numbers, wins, one ask.", "ts": "yesterday", "likes": 3},
            ]
            title = "Founder Log"
        return {"seed": seed, "title": title,
                "storageKey": "naya.appmode.%s.feed" % handle}

    if contract_id == "booking":
        days = ["2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-24"]
        if template == "business":
            return {
                "title": "Reserve a table",
                "service_name": "Table for the Copper Cup",
                "days": days,
                "slots": ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30"],
                "duration_min": 60,
                "note": "Parties of 6+ — call us and we'll push tables together.",
                "storage_key": "naya.appmode.%s.booking.table" % handle,
            }
        # booking template: one config per service is handled by _booking_services;
        # this default is the fallback single-service shape.
        return {
            "title": "Book an appointment",
            "service_name": "Appointment",
            "days": days,
            "slots": ["09:00", "10:30", "13:00", "15:00"],
            "duration_min": 30,
            "storage_key": "naya.appmode.%s.booking" % handle,
        }

    if contract_id == "menu-display":
        return {
            "title": "The Menu",
            "currency": "$",
            "note": "Baked fresh every morning. Oat milk +$0.50, always.",
            "storage_key": "naya.appmode.%s.menu.order" % handle,
            "items": [
                {"name": "Espresso", "description": "Double shot of our house roast — chocolate, orange peel.", "price": 3.50},
                {"name": "Cortado", "description": "Espresso cut with silky steamed milk. Our signature.", "price": 4.25},
                {"name": "Latte", "description": "Mellow and milky, dusted with cocoa.", "price": 4.75},
                {"name": "Pour Over", "description": "Single-origin Ethiopia, brewed slow. Tastes like blueberries.", "price": 5.00},
                {"name": "Butter Croissant", "description": "Laminated over three days. Shatters properly.", "price": 3.75},
                {"name": "Cardamom Bun", "description": "Swedish-style, pearl sugar. Gone by nine.", "price": 4.50},
                {"name": "Avocado Toast", "description": "Sourdough, smashed avo, chili crunch, lime.", "price": 9.50},
                {"name": "Soup of the Day", "description": "Ask Jonah — yesterday was roasted tomato.", "price": 8.00},
            ],
        }

    if contract_id == "product-display":
        return {
            "name": "The Ember Table Lamp",
            "tagline": "Hand-thrown stoneware, linen shade, warm dimmable light.",
            "price": 145,
            "currency": "$",
            "features": [
                "Thrown and glazed by hand — no two alike",
                "Belgian linen shade, warm 2700K glow",
                "Full-range dimmer on the cord",
                "Signed and dated under the base",
            ],
            "button_text": "Take it home",
            "note": "Ships in 3 days, packed like it's going to the moon.",
            "storage_key": "naya.appmode.%s.product.order" % handle,
        }

    if contract_id == "signup-capture":
        return {
            "title": "Join the 5-Day Ship-It Challenge",
            "subtitle": "One tiny ship per day. We'll mail you the mission every morning.",
            "button_text": "I'm in",
            "success_title": "You're in!",
            "success_message": "Welcome aboard, {name} — day one lands in your inbox tomorrow at 7am.",
            "fields": [
                {"name": "name", "label": "Your name", "type": "text", "required": True, "placeholder": "Ada Lovelace"},
                {"name": "email", "label": "Email", "type": "email", "required": True, "placeholder": "you@example.com"},
                {"name": "ship", "label": "What will you ship?", "type": "text", "required": False, "placeholder": "The landing page I've been avoiding"},
            ],
            "storage_key": "naya.appmode.%s.signup" % handle,
        }

    if contract_id == "event-rsvp":
        return {
            "title": "Rooftop Jazz: The Marlowe Quartet",
            "date_label": "Saturday, Oct 24",
            "time_label": "7:30 PM",
            "venue": "The Row Rooftop, 418 Grand Ave",
            "description": "One night, one rooftop, a quartet and the skyline. Doors at 7, music at 7:30 sharp. Blankets provided; the city provides the view.",
            "base_attendees": 47,
            "storage_key": "naya.appmode.%s.rsvp" % handle,
        }

    if contract_id == "assessment-score":
        return {
            "title": "Marathon Readiness Check",
            "intro": "Twelve honest questions. No flattery — the start line doesn't care about your feelings.",
            "accent": soul,
            "storeKey": "naya.appmode.%s.assessment" % handle,
            "assessment": {
                "id": "marathon-readiness",
                "version": "1.0.0",
                "title": "Marathon Readiness Check",
                "dimensions": [
                    {"id": "endurance", "name": "Endurance", "color": "#a06bff", "weight": 2},
                    {"id": "strength", "name": "Strength", "color": "#2fe89e", "weight": 1},
                    {"id": "recovery", "name": "Recovery", "color": "#3fb8ff", "weight": 1},
                ],
                "scoreBands": [
                    {"min": 0, "max": 49, "label": "Not yet", "color": "#ff5e6c",
                     "description": "The engine isn't there yet. Build the base before you chase the distance."},
                    {"min": 50, "max": 79, "label": "Building", "color": "#ffbf3d",
                     "description": "Real fitness, real gaps. Three focused weeks and you're knocking on the door."},
                    {"min": 80, "max": 100, "label": "Race ready", "color": "#2fe89e",
                     "description": "The work is in the legs. Trust the taper, run your race."},
                ],
                "questions": [
                    {"id": "q1", "dimensionId": "endurance", "order": 1, "label": "Long run",
                     "teaching": "The long run is the marathon in miniature.",
                     "question": "How did your last 16+ mile long run feel?",
                     "answers": [
                         ["a1", "Strong throughout", "Finished wanting more", 100, "#2fe89e", ""],
                         ["a2", "Tough but done", "Walked a little at the end", 65, "#ffbf3d", ""],
                         ["a3", "Fell apart", "Bonked or cut it short", 25, "#ff5e6c", ""],
                     ]},
                    {"id": "q2", "dimensionId": "endurance", "order": 2, "label": "Weekly volume",
                     "teaching": "Volume is the quiet engine of marathon fitness.",
                     "question": "What's your average weekly mileage over the last month?",
                     "answers": [
                         ["a1", "45+ miles", "Peak training territory", 100, "#2fe89e", ""],
                         ["a2", "30-45 miles", "Solid base, room to grow", 65, "#ffbf3d", ""],
                         ["a3", "Under 30 miles", "The base needs building", 25, "#ff5e6c", ""],
                     ]},
                    {"id": "q3", "dimensionId": "endurance", "order": 3, "label": "Pace control",
                     "teaching": "Easy days easy is a discipline, not a suggestion.",
                     "question": "Can you run easy miles truly easy?",
                     "answers": [
                         ["a1", "Yes, always", "Discipline is locked in", 100, "#2fe89e", ""],
                         ["a2", "Mostly", "Sometimes I chase the watch", 60, "#ffbf3d", ""],
                         ["a3", "Rarely", "Every run becomes a workout", 20, "#ff5e6c", ""],
                     ]},
                    {"id": "q4", "dimensionId": "strength", "order": 4, "label": "Strength work",
                     "teaching": "Strong hips carry tired legs across the line.",
                     "question": "How often do you do focused strength work?",
                     "answers": [
                         ["a1", "2x per week", "Non-negotiable sessions", 100, "#2fe89e", ""],
                         ["a2", "When I remember", "Sporadic but present", 55, "#ffbf3d", ""],
                         ["a3", "Never", "Running only", 15, "#ff5e6c", ""],
                     ]},
                    {"id": "q5", "dimensionId": "strength", "order": 5, "label": "Hills",
                     "teaching": "Hills are speed work in disguise.",
                     "question": "When did you last run real hills?",
                     "answers": [
                         ["a1", "This week", "They're in the rotation", 100, "#2fe89e", ""],
                         ["a2", "This month", "Occasional visitor", 60, "#ffbf3d", ""],
                         ["a3", "Can't remember", "Flatlander", 20, "#ff5e6c", ""],
                     ]},
                    {"id": "q6", "dimensionId": "recovery", "order": 6, "label": "Sleep",
                     "teaching": "Adaptation happens in bed, not on the road.",
                     "question": "How's your sleep during peak training?",
                     "answers": [
                         ["a1", "7.5+ hours", "The work is absorbing", 100, "#2fe89e", ""],
                         ["a2", "6-7 hours", "Getting by", 60, "#ffbf3d", ""],
                         ["a3", "Under 6", "Running on fumes", 20, "#ff5e6c", ""],
                     ]},
                    {"id": "q7", "dimensionId": "recovery", "order": 7, "label": "Niggles",
                     "teaching": "Small pains are the body's early warning system.",
                     "question": "Any persistent niggles right now?",
                     "answers": [
                         ["a1", "None", "Body feels bulletproof", 100, "#2fe89e", ""],
                         ["a2", "One, managed", "Watching it closely", 60, "#ffbf3d", ""],
                         ["a3", "Yes, worried", "It's getting worse", 20, "#ff5e6c", ""],
                     ]},
                    {"id": "q8", "dimensionId": "recovery", "order": 8, "label": "Rest days",
                     "teaching": "Rest is training you do lying down.",
                     "question": "Do you take real rest days?",
                     "answers": [
                         ["a1", "Weekly, guilt-free", "Part of the plan", 100, "#2fe89e", ""],
                         ["a2", "Sometimes", "FOMO creeps in", 60, "#ffbf3d", ""],
                         ["a3", "Never", "Rest feels like quitting", 20, "#ff5e6c", ""],
                     ]},
                ],
            },
        }

    if contract_id == "portfolio-showcase":
        items = [
            ("Diner at Dawn", ["street"], "A chrome counter at 6am, one regular, endless coffee."),
            ("Her Hands", ["portrait"], "My grandmother's hands, flour on the knuckles."),
            ("Concrete Poetry", ["street"], "Brutalist stairwells and the light they keep."),
            ("The Dress Rehearsal", ["editorial"], "Backstage at the Meridian — chaos in soft focus."),
            ("Salt Air", ["portrait"], "Wind, a striped shirt, and nowhere to be."),
            ("Neon Confessional", ["editorial"], "A karaoke bar at midnight tells the truth."),
        ]
        pairs = [("#6675ff", "#a06bff"), ("#e84fff", "#6675ff"), ("#3fb8ff", "#2fe89e")]
        out = []
        for i, (t, tags, blurb) in enumerate(items):
            c1, c2 = pairs[i % len(pairs)]
            out.append({
                "id": "p%d" % (i + 1),
                "title": t,
                "tags": tags,
                "image": _svg_datauri(t, c1, c2),
                "blurb": blurb,
                "url": "https://junepark.example/work/%d" % (i + 1),
            })
        return {"title": "Selected Work", "subtitle": "Six frames that made me a photographer.",
                "items": out, "accent": soul}

    if contract_id == "community-feed":
        return {
            "title": "Maple Street Feed",
            "subtitle": "Borrow a ladder. Find the cat. Plan the party.",
            "composerPlaceholder": "Tell the street something...",
            "namePlaceholder": "Your name",
            "seedPosts": [
                {"author": "June K.", "text": "Grey cat, green collar, answers to Beans. Last seen near #14. Reward: eternal gratitude + baked goods.", "time": "1h ago"},
                {"author": "Marcus T.", "text": "Block party meeting Thursday 7pm at my place. Bringing the grill signup sheet.", "time": "3h ago"},
                {"author": "Priya S.", "text": "Free moving boxes on my porch — take them before the rain does.", "time": "yesterday"},
            ],
            "accent": soul,
        }

    if contract_id == "business-proof":
        return {
            "businessName": "Copper Cup",
            "tagline": "The corner café that knows your order.",
            "services": [
                {"name": "Espresso bar", "blurb": "House roast, dialed in daily. Cortados worth crossing the street for.", "price": "from $3.50"},
                {"name": "Fresh baking", "blurb": "Laminated, proofed, and out of the oven by 7am. When it's gone, it's gone.", "price": "from $3.75"},
                {"name": "Beans to take home", "blurb": "The same roast we pull, in 12oz bags with brew cards.", "price": "$18"},
            ],
            "testimonials": [
                {"quote": "The cortado here ruined every other café for me.", "name": "Dana W.", "role": "regular since 2021"},
                {"quote": "I wrote half my novel at the corner table.", "name": "Marcus T.", "role": "neighbor"},
            ],
            "stats": [
                {"value": "4.9", "label": "average rating"},
                {"value": "12k", "label": "cups a month"},
                {"value": "6am", "label": "doors open daily"},
            ],
            "ctaLabel": "Book a table",
            "ctaEmail": "hello@coppercup.example",
            "accent": soul,
            "note": "Walk-ins always welcome — booking just skips the line.",
        }

    if contract_id == "profile-link":
        return {"name": handle, "handle": "@" + handle, "bio": idea[:140],
                "links": [{"label": "Say hello", "url": "mailto:hello@example.com"}],
                "accent": soul}

    if contract_id == "navigate":
        return _nav_config(blueprint, page_file)

    if contract_id == "search":
        return {"items": [], "placeholder": "Search...", "accent": soul}

    if contract_id == "contact":
        who = {"business": "Copper Cup", "booking": "Wag & Shine",
               "product": "Kiln & Glow", "event": "the host",
               "portfolio": "June", "menu": "Copper Cup catering",
               "personal": "Maya"}.get(template, "the owner")
        return {"to": who, "accent": soul,
                "outboxKey": "naya.appmode.%s.contact.outbox" % handle}

    if contract_id == "share":
        return {"accent": soul, "text": vision or idea}

    if contract_id == "save":
        return {
            "items": [
                {"id": "sv1", "title": "Backsplash: handmade zellige in oat", "sub": "Decision — $14/sq ft, ordered Oct 28"},
                {"id": "sv2", "title": "Paint: Swiss Coffee, eggshell", "sub": "Decision — two coats, kitchen + hall"},
                {"id": "sv3", "title": "Luis's tile quote", "sub": "Contact — (555) 016-4402, call Thursday"},
            ],
            "storeKey": "naya.appmode.%s.saved" % handle,
            "accent": soul,
        }

    if contract_id == "dictate":
        return {"idleLabel": "Start dictating", "listeningLabel": "Listening — tap to stop"}

    if contract_id == "cart":
        return {"emptyMessage": "Your cart is empty — pick a finish below."}

    if contract_id == "join":
        return {
            "spaces": [
                {"id": "blockparty", "name": "Block Party Crew", "topic": "events", "members": 24, "color": "#ff5e6c"},
                {"id": "garden", "name": "Garden Share", "topic": "garden", "members": 11, "color": "#2fe89e"},
                {"id": "lostfound", "name": "Lost & Found", "topic": "help", "members": 8, "color": "#3fb8ff"},
            ],
            "storeKey": "naya.appmode.%s.spaces" % handle,
        }

    # copy / preview / contract-draft / play have no template defaults; the
    # contract must supply their config (they are intake-chrome units).
    return {}


def booking_service_configs(template, contract):
    """booking template: 3 services -> 3 mounted configs (brief section 3.4)."""
    handle = contract.get("handle", "naya")
    days = ["2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-24"]
    services = [
        ("Full Groom", "Bath, cut, nails, ears — the whole spa day.", 90, 75,
         ["09:00", "11:00", "13:30", "15:30"]),
        ("Bath & Tidy", "Warm bath, blow-out, brush, light trim.", 45, 45,
         ["09:30", "10:30", "14:00", "16:00"]),
        ("Nail Trim", "Quick, calm, treat at the end. Walk-ins welcome.", 20, 18,
         ["09:00", "12:00", "15:00", "17:00"]),
    ]
    out = []
    for i, (name, blurb, mins, price, slots) in enumerate(services):
        out.append({
            "title": name,
            "service_name": "%s — $%d" % (name, price),
            "days": days,
            "slots": slots,
            "duration_min": mins,
            "note": blurb,
            "storage_key": "naya.appmode.%s.booking.svc%d" % (handle, i),
        })
    return out

# ---------------------------------------------------------------------------
# v2 — Hub chassis harvest + piece composition + design-law gate.
#
# PAGE CHASSIS (Shawn's order 2026-10-18): the 12 templates FOLLOW AND
# ADAPT the Hub app (~/workspace/user/files/index-2.html): fixed left rail
# (collapsible) + topbar + main scroll surface + mobile drawer. The Hub's
# :root tokens are verbatim source of truth. Corner plus buttons are
# harvested VERBATIM from the Hub as theme-agnostic click-in blocks and
# take each template's soul color for hover ignition (wired via
# var(--soul)/var(--jewel)). Discrete pieces placed inside the chassis
# (section boards, hero orbs) come VERBATIM from the 478-piece index.
# Law-breakers found in harvested CSS are fixed as harvested (standing
# order): stray non-token hexes are snapped to the canonical union set,
# and the harvested hero eyebrow color is overridden to white per Law 1
# (Shawn's word outranks the Hub file).
# ---------------------------------------------------------------------------

import re as _re

HUB_PATH = os.path.expanduser("~/workspace/user/files/index-2.html")
# Pinned 2026-10-18. If the Hub file changes, the build fails closed with
# "re-harvest required" — never silently builds against a moved source.
HUB_SHA256 = "f56fd98683704c37a148d535b9cb6a0b16de831edab86f5ae24633b204b02722"

# (name, first_line, last_line) — 1-based, verified 2026-10-18 against the
# pinned sha above. Each block carries a signature assert.
HUB_RANGES = [
    ("root",       21,  96),    # :root tokens — verbatim source of truth
    ("bodybase",  105, 123),    # reset + body
    ("shell",     170, 194),    # .shell grid + rail-collapsed
    ("railtoggle", 295, 326),   # rail-toggle: black + elegant plus
    ("railleft",  329, 343),    # .rail.left
    ("ecoplus",   345, 365),    # eco-plus: jewel glowing orb button
    ("ecoplus2",  387, 392),    # eco-plus: focus + expanded state
    ("ecomenu",   393, 450),    # eco-menu dropdown + eco-ico + mobile rule
    ("brand",     452, 456),    # .brand
    ("railnav",   457, 457),    # .rail .nav
    ("navbtn",    462, 519),    # .nav-btn: white-edge language
    ("private",   526, 530),    # .private note
    ("maintop",   533, 555),    # .main .top .top-title .top-status
    ("roomsplus", 558, 578),    # rooms-plus: mobile drawer opener
    ("roomoutlet", 680, 680),   # .room-outlet
    ("hero",      682, 688),    # .hero .eyebrow h1 .hero-sub
    ("drawer",    743, 747),    # .drawer-backdrop
    ("drawmedia", 749, 773),    # @media 900px: drawer + rooms-plus
    ("topspacer", 808, 808),    # .top-spacer
]

_HUB_SIG = {
    "root": ":root {",
    "bodybase": "box-sizing: border-box;",
    "shell": ".shell.rail-collapsed",
    "railtoggle": ".rail-toggle:hover",
    "railleft": ".rail.left {",
    "ecoplus": "--jewel: #ffea00;",
    "ecoplus2": ".eco-plus[aria-expanded",
    "ecomenu": ".eco-menu.open",
    "brand": ".brand {",
    "railnav": ".rail .nav {",
    "navbtn": ".nav-btn.active::before",
    "private": ".private {",
    "maintop": ".top-status .led {",
    "roomsplus": ".rooms-plus svg {",
    "roomoutlet": ".room-outlet {",
    "hero": ".hero .eyebrow {",
    "drawer": ".drawer-backdrop {",
    "drawmedia": ".rooms-plus { display: grid; }",
    "topspacer": ".top-spacer {",
}

# Canonical token set = UNION of (16-law canonical hexes, laws doc
# 2026-10-17) + (Hub :root tokens, index-2.html). A hex is legal iff it is
# verbatim from either source. Everything else is an invented hex.
_LAW_HEXES = {
    "050507", "020203",                       # obsidian / deep
    "ffffff", "f8f7fb",                       # white
    "a06bff", "e84fff", "3fb8ff", "2fe89e",    # purple magenta blue green
    "ffbf3d", "40d3bb", "6675ff", "ff5e6c",    # gold teal indigo red
    "b8ee57", "ff9a5a",                       # lime orange
}
_HUB_HEXES = {
    "0b0d12", "12151d", "171b25", "252b39",    # obsidian stack
    "f5f7fb", "aab2bf", "c9c3ce",              # ink / muted / faint
    "ffffff18", "ffffff0d",                    # line tokens
    "9d75ff", "55b9ee", "55e39a", "f1d75a",    # Hub spectrum
    "e8b64c", "ff7a3d", "ff5a6e", "d86cff",    # Hub spectrum
    "e8eaf2",                                 # settings silver
    "6675ff18", "d86cff12",                 # --field gradients (Hub :root)
}
UNION_HEXES = _LAW_HEXES | _HUB_HEXES | {"6675ff", "40d3bb", "b8ee57", "ff9a5a"}

# Non-union hexes found in harvested CSS -> nearest union token.
# (Fixing law-breakers as harvested — standing order.)
HEX_REMAP = {
    "000": "020203", "000000": "020203", "fff": "ffffff",
    "040406": "0b0d12", "07070a": "0b0d12", "08080b": "0b0d12",
    "101116": "0b0d12", "101117": "0b0d12",
    "0a0e16": "12151d", "10141d": "12151d", "120d1d": "12151d",
    "141a28": "12151d", "17181f": "12151d", "1b1c24": "12151d",
    "2a2a32": "252b39", "0a0a0e": "020203", "0d0b14": "0b0d12",
    "6c5799": "9d75ff", "8d63f5": "9d75ff",
    "e455f4": "d86cff", "3f9ff5": "55b9ee", "34d38a": "55e39a",
    "39d7e8": "40d3bb", "e7c65a": "e8b64c",
    "c8c2ce": "aab2bf", "bdb7c8": "aab2bf", "fbfaff": "f5f7fb",
}

# Text colors the Law-1 gate allows. White/silver always; obsidian/deep
# only for text sitting on white surfaces (white-at-rest controls).
TEXT_ALLOW = {
    "#ffffff", "#f8f7fb", "#f5f7fb", "#050507", "#020203", "white",
    "var(--ink)", "var(--white)", "var(--quiet)", "var(--faint)",
    "var(--muted)", "var(--ink-dim)",
}
_TEXT_RGBA_OK = (
    _re.compile(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,"),
    _re.compile(r"rgba\(\s*248\s*,\s*247\s*,\s*251\s*,"),
    _re.compile(r"rgba\(\s*245\s*,\s*247\s*,\s*251\s*,"),
)
# color: on these selectors is chrome/icon (Law 3), not text (Law 1).
_CHROME_SELECTOR_HINTS = (
    ".ico", ".eco-ico", ".jewel", ".led", ".dot", "svg", "::", ".ext", ".orb",
)

# Canonical spectrum walk (Law 10 order: magenta -> purple -> blue ->
# green -> gold). Each template starts at its own offset; sections walk
# the sequence strictly by position. Adjacent sections never share a hue.
SPECTRUM = [
    ("magenta", "#e84fff"),
    ("purple", "#a06bff"),
    ("blue", "#3fb8ff"),
    ("green", "#2fe89e"),
    ("gold", "#ffbf3d"),
]
SPECTRUM_NAMES = [n for n, _ in SPECTRUM]
WALK_START = {
    "personal": 1, "dashboard": 1, "portfolio": 1,
    "today": 2, "signup": 2, "business": 2,
    "booking": 3, "menu": 3,
    "product": 0, "community": 0,
    "event": 4, "smartlist": 4,
}

# Discrete index pieces placed inside the Hub chassis (Law 14).
PIECE_SECTION_BOARD = "NAYA-CRD-008"   # card: white rim at rest, own color ignites


def _hub_lines():
    with open(HUB_PATH, encoding="utf-8") as f:
        src = f.read()
    digest = hashlib.sha256(src.encode("utf-8")).hexdigest()
    if digest != HUB_SHA256:
        _fail(["hub chassis changed (sha256 %s... != pinned) — re-harvest "
               "index-2.html before building" % digest[:16]])
    return src.split("\n")


def _soul_wire_hub(css):
    """Theme-agnostic click-in blocks take the template soul for hover
    ignition (Shawn's order): wire the harvested plus-button hover slots
    to var(--soul)/var(--jewel), and snap stray non-token hexes."""
    css = css.replace("--jewel: #ffea00;", "--jewel: var(--soul);")
    css = css.replace("--jewel: #8a5cff;", "--jewel: var(--soul);")
    css = css.replace("rgba(157,117,255,.7)",
                      "color-mix(in srgb, var(--soul) 70%, transparent)")
    css = css.replace("rgba(157,117,255,.55)",
                      "color-mix(in srgb, var(--soul) 55%, transparent)")
    css = css.replace("rgba(157,117,255,.8)",
                      "color-mix(in srgb, var(--soul) 80%, transparent)")
    css = css.replace("rgba(157,117,255,.3)",
                      "color-mix(in srgb, var(--soul) 30%, transparent)")
    css = css.replace("#ffffff2a", "#ffffff18")
    css = css.replace("#2a2a32", "#252B39")
    css = css.replace("#0a0a0e", "#020203")
    css = css.replace("#0d0b14", "#0B0D12")
    css = css.replace("#000)", "#020203)")
    # Law 1 (Shawn's word outranks the Hub file): the harvested hero eyebrow
    # is colored in the Hub — kickers stay white, always.
    css = css.replace("color: var(--room-accent, var(--green));",
                      "color: #fff; /* Law 1: Shawn's word — kickers stay white */")
    return css


def _hub_css(soul):
    """Harvest the chassis CSS verbatim (sha-pinned), soul-wire the plus
    buttons, append --soul to the harvested :root. Exactly one :root."""
    lines = _hub_lines()
    blocks = []
    for name, lo, hi in HUB_RANGES:
        chunk = "\n".join(lines[lo - 1:hi]).strip()
        if _HUB_SIG[name] not in chunk:
            _fail(["hub harvest: block %r (L%d-%d) lost signature %r — "
                   "re-harvest" % (name, lo, hi, _HUB_SIG[name])])
        if name == "root":
            chunk = chunk.rstrip()
            assert chunk.endswith("}"), "hub :root block must end with }"
            chunk = chunk[:-1].rstrip() + "\n  --soul: %s;\n}" % soul
        blocks.append("/* hub chassis: %s (index-2.html L%d-%d, sha %s...) */\n%s"
                      % (name, lo, hi, HUB_SHA256[:12], chunk))
    return _soul_wire_hub("\n\n".join(blocks))


_HEX_RE = _re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")


def _remap_hexes(css):
    """Snap every hex to the canonical union set (fix law-breakers as
    harvested). Unknown hexes are left untouched for the gate to fail."""
    def sub(m):
        h = m.group(1).lower()
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 8:
            if h in UNION_HEXES:
                return "#" + h
            six = HEX_REMAP.get(h[:6], h[:6])
            return "#" + six + h[6:]
        if h in UNION_HEXES:
            return "#" + h
        return "#" + HEX_REMAP.get(h, h)
    return _HEX_RE.sub(sub, css)


def _normalize_piece_css(css, soul):
    css = _remap_hexes(css)
    # The template soul owns every --soul slot inside piece scope.
    css = _re.sub(r"--soul\s*:\s*#[0-9a-fA-F]{3,8}", "--soul: " + soul, css)
    return css


def _piece_css(index, soul, models):
    """Verbatim index CSS for the placed piece models, token-normalized."""
    pieces = index["pieces"]
    bank = index["css_bank"]
    out = []
    seen = set()
    for model in models:
        p = pieces[model]
        cid = p["css_id"]
        if cid in seen:
            continue
        seen.add(cid)
        css = _normalize_piece_css(bank[cid], soul)
        out.append("/* piece: %s — %s (builder-index-v1, token-normalized) */\n%s"
                   % (model, p.get("label"), css))
    return "\n\n".join(out)


def _soul_rgb(soul):
    s = soul.lstrip("#")
    return "%d,%d,%d" % (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def _rgba(hex6, a):
    hex6 = hex6.lstrip("#")
    return "rgba(%d,%d,%d,%s)" % (
        int(hex6[0:2], 16), int(hex6[2:4], 16), int(hex6[4:6], 16), a)


def _walk(template, n):
    s = WALK_START[template]
    return [SPECTRUM[(s + i) % len(SPECTRUM)] for i in range(n)]


# Page glue: the minimum law-built rules that are not chassis and not
# pieces — typography voice (Law 9), Law-1 kicker override, layout of
# mounts and the visible manifest. No invented chrome.
GLUE_CSS = """
/* Law 1 (Shawn's word outranks the Hub file): kickers/eyebrows stay white. */
.hero .eyebrow{color:#fff}
/* Law 9: Newsreader for voice. */
.hero h1{font-family:Newsreader,Georgia,'Times New Roman',serif;font-weight:600}
.hero-orbs{display:flex;gap:16px;margin:20px 0 6px;align-items:center;min-height:40px}
/* kicker inside the index card piece: white, sized hierarchy (Law 16) */
.card p.fine.kicker-line{font-size:11px;letter-spacing:.24em;text-transform:uppercase;
font-weight:700;margin:0 0 10px;color:#fff}
/* mounted function roots get breathing room */
.nsec-body [data-fn]{margin:0}
.nsec-body [data-fn]+[data-fn]{margin-top:26px}
/* rail anchors reuse the Hub nav-btn language */
.rail .nav a.nav-btn{text-decoration:none}
.eco-wrap{position:relative;display:flex}
/* visible piece manifest (Shawn's 2026-10-17 rule) */
.manifest{margin-top:18px;border-top:1px solid var(--line-soft);padding-top:14px}
.manifest ul{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.manifest li{font-size:13px;color:var(--ink)}
.manifest li b{color:#fff;font-weight:700}
.manifest .mrole{color:var(--muted)}
/* dictate host surface (function f-25) */
.capture{display:flex;flex-direction:column;gap:12px}
.capture textarea{width:100%;min-height:110px;background:#0B0D12;color:#ffffff;font-size:16px;
border:1px solid var(--line);border-radius:14px;padding:14px;resize:vertical;font-family:inherit}
.capture textarea:focus{outline:none;border-color:var(--soul);
box-shadow:0 0 0 3px color-mix(in srgb,var(--soul) 30%,transparent)}
.dictbtn{align-self:flex-start;background:#ffffff;color:#050507;border:none;border-radius:999px;
padding:12px 22px;font-weight:800;font-size:14px;cursor:pointer}
.dictbtn:hover{background:var(--soul);color:#ffffff;box-shadow:0 0 20px var(--soul)}
.capture .hint{font-size:12px;color:var(--faint)}
/* cart host surface (function f-28) */
.cartfab{position:fixed;right:22px;bottom:22px;z-index:60;background:var(--soul);color:#ffffff;
border:none;border-radius:999px;padding:14px 20px;font-weight:800;cursor:pointer;
box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 20px color-mix(in srgb,var(--soul) 50%,transparent)}
.cartdrawer{position:fixed;right:0;top:0;bottom:0;width:min(380px,92vw);background:#0B0D12;
border-left:1px solid var(--line);z-index:70;transform:translateX(105%);transition:transform .25s;
display:flex;flex-direction:column;padding:20px}
.cartdrawer.open{transform:none}
.cartdrawer h3{margin:0 0 12px;color:#ffffff}
#cartItems{flex:1;overflow:auto}
.pcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-bottom:8px}
.pcard{background:#0B0D12;border:1px solid var(--line);border-radius:16px;padding:18px;color:#ffffff}
.pcard h4{margin:0 0 4px;color:#ffffff}
.pcard .pmeta{font-size:12px;color:var(--faint);margin-bottom:10px}
.szpills{display:flex;gap:8px;margin:10px 0}
.szpill{background:transparent;border:1px solid rgba(255,255,255,.35);color:#ffffff;border-radius:999px;
padding:6px 14px;font-size:12px;cursor:pointer}
.szpill.on{background:#ffffff;color:#050507;border-color:#ffffff;font-weight:700}
.btn-select{background:var(--soul);color:#ffffff;border:none;border-radius:999px;padding:10px 18px;
font-weight:700;cursor:pointer;width:100%}
.btn-select.picked{background:#2fe89e}
@media(max-width:640px){.hero-orbs{display:none}}
/* Smart Tabs standard chrome (Shawn 2026-10-18): the bar rides at the top of the
   main scroll surface, directly under the topbar — the lists/spaces room pattern.
   White at rest, template soul ignites on touch (Law 6); the tabs themselves keep
   their stable per-tab spectrum colors (the unit hashes by id — color is identity). */
.tabs-bar{margin:0 0 18px;border-radius:16px;border:1px solid var(--line-soft);
background:rgba(255,255,255,.02);box-shadow:0 10px 30px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.05);
transition:border-color .2s,box-shadow .2s}
.tabs-bar:hover,.tabs-bar:focus-within{border-color:var(--tb-ign);
box-shadow:0 0 22px -6px var(--tb-ign),0 10px 30px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.05)}
.tabs-bar [data-fn="smart-tabs"]{margin:0}
"""

FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800'
    '&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap" rel="stylesheet">'
)


def _esc_title(s):
    """Clean title: escape only what <title> needs — quotes stay readable."""
    return ("" if s is None else str(s)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Design-law gate. Runs on every rendered page BEFORE it is written. ANY
# violation -> the caller fails the build (non-zero exit) naming the law
# and the offending element. This is the heart of the mission: the 16 laws
# live in the machine, not in a checklist.
# ---------------------------------------------------------------------------

def _text_color_ok(val):
    v = val.strip().lower()
    if _re.fullmatch(r"#[0-9a-f]{3}", v):
        v = "#" + "".join(c * 2 for c in v[1:])
    if v in TEXT_ALLOW:
        return True
    return any(p.match(v) for p in _TEXT_RGBA_OK)


def gate_design_laws(html, css_text, ctx):
    """Return a list of violation strings (empty == PASS)."""
    v = []
    template = ctx["template"]
    soul = ctx["soul"].lower()
    index = ctx["index"]
    pieces = index["pieces"]

    # ---- Law 9: every hex is a verbatim token (law doc or Hub :root) ----
    def check_hexes(source, where):
        for m in _re.finditer(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b", source):
            h = m.group(1).lower()
            if len(h) == 3:
                h = "".join(c * 2 for c in h)
            if h not in UNION_HEXES:
                v.append("Law 9: unknown hex #%s in %s — not verbatim from the "
                         "16-law tokens or the Hub :root" % (m.group(1), where))
    check_hexes(css_text, "emitted CSS")
    for m in _re.finditer(r'style="([^"]*)"', html):
        check_hexes(m.group(1), "inline style")
    if css_text.count(":root") != 1:
        v.append("Law 9: expected exactly one :root block, found %d"
                 % css_text.count(":root"))
    m = _re.search(r"--soul\s*:\s*(#[0-9a-fA-F]{6})", css_text)
    if not m or m.group(1).lower() != soul:
        v.append("Soul: emitted --soul %s != blueprint soul %s (template %s)"
                 % (m.group(1) if m else "absent", soul, template))

    # ---- Law 1: no colored text (kickers, headings, body, paragraphs) ----
    for m in _re.finditer(r"([^{}]+)\{([^{}]*)", css_text):
        selector, body = m.group(1), m.group(2)
        if any(hint in selector for hint in _CHROME_SELECTOR_HINTS):
            continue  # chrome/icons — Law 3, not Law 1
        for cm in _re.finditer(r"(?<![\w-])color\s*:\s*([^;}{!]+)", body):
            if not _text_color_ok(cm.group(1)):
                sel = " ".join(selector.split())[-80:]
                v.append("Law 1: colored text %r on %r — text stays white"
                         % (cm.group(1).strip(), sel))
    for m in _re.finditer(r'style="([^"]*)"', html):
        for cm in _re.finditer(r"(?<![\w-])color\s*:\s*([^;}{!]+)", m.group(1)):
            if not _text_color_ok(cm.group(1)):
                v.append("Law 1: colored text %r in inline style"
                         % cm.group(1).strip())

    # ---- Laws 4/5/10: spectrum walk, adjacency, one board one color ----
    sec_tags = _re.findall(r'<section[^>]*class="card"[^>]*>', html)
    hues = []
    for tag in sec_tags:
        hm = _re.findall(r'data-hue="([^"]+)"', tag)
        if len(hm) != 1:
            v.append("Law 5: section board %r must carry exactly one data-hue"
                     % tag[:60])
            continue
        hues.append(hm[0])
    for h in hues:
        if h != "soul" and h not in SPECTRUM_NAMES:
            v.append("Laws 4/5/10: section hue %r is not a canonical spectrum hue"
                     % h)
    for a, b in zip(hues, hues[1:]):
        if a == b:
            v.append("Law 4: adjacent sections share hue %r — never twice adjacent" % a)
    if len(set(hues) | {"soul"}) < 3:
        v.append("Laws 4/5/10: page walks only %d distinct hue(s) — need >= 3"
                 % len(set(hues) | {"soul"}))

    # ---- Law 14: every placed piece traces to the index; manifest proves it
    manifest_ok = 'id="piece-manifest"' in html
    if not manifest_ok:
        v.append("Piece-manifest rule: no visible manifest on the page")
    for role, model, label in ctx["placed"]:
        if model not in pieces:
            v.append("Law 14: %s traces to unknown model %s" % (role, model))
            continue
        if pieces[model].get("quarantined"):
            v.append("Law 14: %s uses quarantined model %s" % (role, model))
        if manifest_ok and (model not in html or (label or "") not in html):
            v.append("Piece-manifest rule: manifest lacks %s — %s (%s)"
                     % (model, label, role))
    if "index-2.html" not in html:
        v.append("Law 14: chassis pattern source (index-2.html) not cited")

    # ---- Corner plus buttons (Shawn's order): present, configured, wired --
    for need in ('class="rail-toggle"', 'class="eco-plus"',
                 'class="rooms-plus"', 'class="eco-menu"',
                 'aria-haspopup="true"'):
        if need not in html:
            v.append("Plus-button rule: page is missing %s" % need)
    for gid in _re.findall(r'getElementById\("([^"]+)"', ctx.get("js", "")):
        if ('id="%s"' % gid) not in html:
            v.append("L-2026-10-17-004: chassis JS wires to missing DOM id=%r"
                     % gid)

    # ---- Titles: clean, no entities, no truncation artifacts ----
    mt = _re.search(r"<title>([^<]*)</title>", html)
    if not mt or not mt.group(1).strip():
        v.append("Emission: missing <title>")
    elif "&#" in mt.group(1) or "%s" in mt.group(1):
        v.append("Emission: garbled title %r" % mt.group(1)[:60])

    # ---- Smart Tabs standard (Shawn 2026-10-18): EVERY app ships the bar,
    #     personal pages included — an app without the Tabs bar is incomplete.
    #     A page with no smart-tabs mount FAILS the build, naming the unit.
    #     (Match the mount ELEMENT, not the bare string — the glue CSS names
    #     the selector too.)
    mt = html.find('<div data-fn="smart-tabs"')
    if mt < 0:
        v.append('Smart-tabs standard: missing unit mount data-fn="smart-tabs" '
                 "— an app without the Tabs bar is incomplete")
    else:
        fs = html.find("<section")
        if fs >= 0 and mt > fs:
            v.append("Smart-tabs standard: the tabs bar must ride at the top of "
                     "the main scroll surface (mount sits after the first "
                     "<section>)")
    return v


def _esc(s):
    return htmlmod.escape("" if s is None else str(s), quote=True)


def _config_attr(config):
    raw = json.dumps(config, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True)
    return "'" + htmlmod.escape(raw, quote=True) + "'"


def _mount(register_id, config, inner=""):
    return '<div data-fn="%s" data-fn-config=%s>%s</div>' % (
        _esc(register_id), _config_attr(config), inner)


def _smart_tabs_bar(contract, blueprint, page_file):
    """Standard chrome: the Smart Tabs bar at the top of the main scroll
    surface, directly under the topbar (Shawn's 2026-10-18 standard — every
    app ships it, personal pages included; the lists/spaces room pattern).
    The bar takes the template soul for ignition; the tabs keep their stable
    per-tab spectrum colors (the unit hashes by id — color is identity).
    Returns (html, config)."""
    template = contract["template"]
    soul = blueprint["soul"]
    cfg = default_config(template, "smart-tabs", contract, blueprint, page_file)
    bar = ('<div class="tabs-bar nb-scope" style="--tb-ign:%s" '
           'role="navigation" aria-label="Smart Tabs">%s</div>'
           % (_esc(soul), _mount("smart-tabs", cfg)))
    return bar, cfg


# ---------------------------------------------------------------------------
# Validation (fail-closed)
# ---------------------------------------------------------------------------

def _fail(errors):
    print(json.dumps({"status": "refused", "errors": errors}, indent=2))
    sys.exit(2)


def validate_contract(contract, index, units_dir):
    errors = []
    for key in ("version", "handle", "idea", "vision", "template"):
        if not contract.get(key):
            errors.append("contract missing required key: %s" % key)
    tpl = contract.get("template")
    if tpl and tpl not in BLUEPRINTS:
        errors.append("unknown template: %r (expected one of %s)"
                      % (tpl, ", ".join(sorted(BLUEPRINTS))))
    funcs = contract.get("functions") or {}
    if not isinstance(funcs, dict):
        errors.append("contract.functions must be an object")
        funcs = {}
    for fid in funcs:
        if fid.startswith(NO_UNIT_PREFIX):
            continue
        if fid not in REGISTER:
            errors.append("unknown function id: %r" % fid)
    # pieces: must exist, not quarantined, standalone markup
    pieces = index["pieces"]
    for i, pk in enumerate(contract.get("pieces") or []):
        model = pk.get("model") if isinstance(pk, dict) else None
        if not model or model not in pieces:
            errors.append("pieces[%d]: unknown model %r" % (i, model))
            continue
        p = pieces[model]
        if p.get("quarantined"):
            errors.append("pieces[%d]: %s is quarantined (%s)"
                          % (i, model, p.get("quarantine_reason")))
        h = p.get("html") or ""
        if ("<" not in h or "`" in h or "document." in h
                or "innerHTML" in h or "=>" in h or "${" in h):
            errors.append("pieces[%d]: %s html is not standalone markup "
                          "(harvest fragment) — cannot place verbatim" % (i, model))
    # units dir: every ON function must have its unit file present
    # (unknown ids are already recorded above — skip them here)
    for fid, on in funcs.items():
        if not on or fid.startswith(NO_UNIT_PREFIX):
            continue
        if fid not in REGISTER:
            continue
        reg_id, unit_file = REGISTER[fid]
        if not os.path.isfile(os.path.join(units_dir, unit_file)):
            errors.append("function %r is ON but unit file missing: %s"
                          % (fid, unit_file))
    if not os.path.isfile(os.path.join(units_dir, LOADER_FILE)):
        errors.append("loader missing: %s" % LOADER_FILE)
    return errors


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Chassis composition — Hub pattern adapted per template.
# ---------------------------------------------------------------------------

PLUS_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2.8" stroke-linecap="round" aria-hidden="true">'
            '<path d="M12 5v14M5 12h14"/></svg>')
NAV_ICO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'aria-hidden="true"><circle cx="12" cy="12" r="6.5"/></svg>')


def _rail(contract, blueprint, rendered, page_file, hues, soul):
    """Left rail: brand + page/section nav (Hub .nav-btn language) + note."""
    handle = contract.get("handle", "")
    btns = []
    for (sec_id, _k, title, _m), (hue_name, hue_hex) in zip(rendered, hues):
        if sec_id.startswith("nav"):
            continue  # navigation units are not rail destinations
        btns.append(
            '<a class="nav-btn" style="--nav:%s" href="#sec-%s">'
            '<span class="ico">%s</span><span class="lbl">%s</span></a>'
            % (hue_hex, _esc(sec_id), NAV_ICO_SVG, _esc(title)))
    for fname, label in blueprint["pages"].items():
        if label and fname != page_file:
            btns.append(
                '<a class="nav-btn" style="--nav:%s" href="%s">'
                '<span class="ico">%s</span><span class="lbl">%s</span></a>'
                % (soul, _esc(fname), NAV_ICO_SVG, _esc(label)))
    return (
        '<aside class="rail left" aria-label="%s pages and sections">'
        '<div class="brand"><div><b>%s</b><small>SMART APP</small></div></div>'
        '<nav class="nav" aria-label="Template pages">%s</nav>'
        '<div class="private">PRIVATE BY DEFAULT<br>SHARED BY CHOICE<br>'
        "COLLECTIVE BY CONSENT</div>"
        "</aside>"
    ) % (_esc(handle), _esc(handle.upper() or "NAYA"),
         "".join(btns))


def _eco_links(contract, blueprint, rendered, hues, soul):
    """Destinations menu: this template's pages + sections, each with its
    own icon + color (per-template configuration)."""
    links = []
    for fname, label in blueprint["pages"].items():
        if label:
            links.append((label, fname, soul))
    for (sec_id, _k, title, _m), (hue_name, hue_hex) in zip(rendered, hues):
        if sec_id.startswith("nav"):
            continue
        links.append((title, "#sec-" + sec_id, hue_hex))
    items = []
    for label, href, color in links:
        items.append(
            '<a href="%s" style="--eco:%s">'
            '<span class="eco-ico" aria-hidden="true">%s</span>'
            '<span class="lbl">%s</span></a>'
            % (_esc(href), color, NAV_ICO_SVG, _esc(label)))
    return "".join(items)


def _topbar(contract, eco_links_html):
    handle = contract.get("handle", "")
    return (
        '<header class="top">'
        '<button class="rooms-plus" id="roomsPlus" aria-label="Open navigation" '
        'aria-expanded="false">%s</button>'
        '<button class="rail-toggle" id="railToggle" aria-label="Show sidebar" '
        'title="Your pages">%s</button>'
        '<div class="top-title"><b>%s</b></div>'
        '<div class="top-status"><span class="led"></span><span>WORKING</span></div>'
        '<div class="top-spacer"></div>'
        '<div class="eco-wrap">'
        '<button class="eco-plus" id="ecoPlus" aria-label="Destinations" '
        'aria-haspopup="true" aria-expanded="false" title="Destinations">%s</button>'
        '<nav class="eco-menu" id="ecoMenu" aria-label="Destinations">'
        '<div class="eco-head">DESTINATIONS</div>%s</nav>'
        "</div>"
        "</header>"
    ) % (PLUS_SVG, PLUS_SVG, _esc(handle.upper() or "NAYA"), PLUS_SVG,
         eco_links_html)


def _hero(contract, blueprint, soul, orb_html, page_label, orb_models):
    idea = contract.get("idea", "")
    vision = contract.get("vision", "")
    orbs = ('<div class="hero-orbs">%s</div>' % "".join(
        '<span class="nb-scope orb-wrap">%s</span>' % o for o in orb_html)
        if orb_html else "")
    greet = ""
    if contract.get("template") == "personal":
        greet = ('<p class="hero-sub" id="greetLine">Good day</p>')
    return (
        '<section class="hero" data-hue="soul" id="top">'
        '<div class="eyebrow">%s · %s</div>'
        "<h1>%s</h1>"
        '<p class="hero-sub">%s</p>%s%s'
        "</section>"
    ) % (_esc(contract.get("handle", "")), _esc(page_label),
         _esc(idea), _esc(vision), orbs, greet)


def _section_board(sec_id, kicker, title, mounts, hue_name, hue_hex):
    """Section board: verbatim index card piece (NAYA-CRD-008), one board
    one color via --accent/--jewel, white kicker (Law 1)."""
    return (
        '<section class="card" id="sec-%s" data-hue="%s" data-piece="%s" '
        'style="--accent:%s;--accent-soft:%s">'
        '<p class="fine kicker-line">%s</p>'
        '<h3><span class="jewel" style="--jewel:%s">\u2727</span>%s</h3>'
        '<div class="nsec-body">%s</div>'
        "</section>"
    ) % (_esc(sec_id), hue_name, PIECE_SECTION_BOARD, hue_hex,
         _rgba(hue_hex, ".45"), _esc(kicker), hue_hex, _esc(title),
         "\n".join(mounts))


def _footer_manifest(contract, blueprint, soul, placed, index):
    """Footer panel (index card piece) + the VISIBLE piece manifest."""
    pieces = index["pieces"]
    seen = []
    for role, model, label in placed:
        if model not in [m for _, m, _ in seen]:
            seen.append((role, model, label))
    items = []
    for role, model, label in seen:
        items.append(
            '<li><span class="mrole">%s</span> — <b>%s</b> — %s</li>'
            % (_esc(role), _esc(model), _esc(label or "")))
    items.append(
        '<li><span class="mrole">Page chassis pattern</span> — '
        "<b>index-2.html</b> — NayaNET Hub (rail · topbar · plus menus · drawer)</li>")
    return (
        '<footer class="card" data-hue="soul" data-piece="%s" '
        'style="--accent:%s;--accent-soft:%s">'
        '<h3><span class="jewel" style="--jewel:%s">\u2727</span>%s</h3>'
        '<p class="fine">Built with the Naya Smart Builder · APP-MODE %s · '
        "chassis follows the Hub pattern · every control on this page works.</p>"
        '<div class="manifest" id="piece-manifest">'
        '<p class="fine">PIECE MANIFEST — every placed piece traces to a library model:</p>'
        "<ul>%s</ul></div>"
        "</footer>"
    ) % (PIECE_SECTION_BOARD, soul, _rgba(soul, ".45"), soul,
         "Built to work",
         _esc(APPMODE_VERSION), "".join(items))


_CHASSIS_JS = """
<script>
(function(){
  var shell=document.getElementById('shell'); if(!shell) return;
  var rt=document.getElementById('railToggle');
  var rp=document.getElementById('roomsPlus');
  var bd=document.getElementById('drawerBackdrop');
  var ep=document.getElementById('ecoPlus');
  var em=document.getElementById('ecoMenu');
  /* Default: full-screen main surface, sidebars hidden (Shawn 2026-10-03).
     The user opens them via the obvious toggle buttons. */
  var stored=null;
  try{ stored=localStorage.getItem('naya.rail-collapsed'); }catch(e){}
  if(stored==='0'){ shell.classList.remove('rail-collapsed'); rt.setAttribute('aria-label','Hide sidebar'); }
  rt.addEventListener('click',function(){
    var c=shell.classList.toggle('rail-collapsed');
    rt.setAttribute('aria-label',c?'Show sidebar':'Hide sidebar');
    try{ localStorage.setItem('naya.rail-collapsed',c?'1':'0'); }catch(e){}
  });
  function openDrawer(){ shell.classList.add('drawer-open'); document.body.classList.add('drawer-open'); rp.setAttribute('aria-expanded','true'); }
  function closeDrawer(){ shell.classList.remove('drawer-open'); document.body.classList.remove('drawer-open'); rp.setAttribute('aria-expanded','false'); }
  rp.addEventListener('click',function(){ shell.classList.contains('drawer-open')?closeDrawer():openDrawer(); });
  bd.addEventListener('click',closeDrawer);
  function ecoClose(){ em.classList.remove('open'); ep.setAttribute('aria-expanded','false'); }
  ep.addEventListener('click',function(e){ e.stopPropagation(); var w=!em.classList.contains('open'); ecoClose(); if(w){ em.classList.add('open'); ep.setAttribute('aria-expanded','true'); } });
  document.addEventListener('click',function(e){ if(em.classList.contains('open')&&!em.contains(e.target)) ecoClose(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'){ closeDrawer(); ecoClose(); } });
  var railLinks=document.querySelectorAll('.rail.left a');
  for(var i=0;i<railLinks.length;i++){ railLinks[i].addEventListener('click',closeDrawer); }
  var gl=document.getElementById('greetLine');
  if(gl){ var h=new Date().getHours();
    var g=h<5?'Up late':h<12?'Good morning':h<18?'Good afternoon':'Good evening';
    var d=new Date().toLocaleDateString(undefined,{weekday:'long',month:'long',day:'numeric'});
    gl.textContent=g+' \\u2014 '+d; }
})();
</script>
"""


def _dictate_block(config):
    inner = (
        '<div class="capture">'
        '<button id="dictBtn" class="dictbtn" type="button">%s</button>'
        '<textarea id="visionText" placeholder="Speak or type what\'s on your mind\u2026"></textarea>'
        '<span class="hint">Dictation needs Chrome or Edge \u2014 otherwise just type.</span>'
        "</div>"
    ) % _esc(config.get("idleLabel") or "Start dictating")
    return _mount("dictate", config, inner)


def _cart_block(config):
    # f-28-cart host surface: fab + drawer + .pcard variant cards.
    variants = [
        ("oat", "Oat glaze", "Warm white, matte"),
        ("slate", "Slate glaze", "Deep grey, satin"),
        ("terra", "Terracotta", "Sun-baked clay"),
    ]
    cards = []
    for model, name, meta in variants:
        cards.append(
            '<div class="pcard" data-model="lamp-%s" data-name="Ember Lamp \u2014 %s">'
            "<h4>%s</h4>"
            '<div class="pmeta">%s \u00b7 $145</div>'
            '<div class="szpills">'
            '<button class="szpill" data-s="S" data-z="1">S</button>'
            '<button class="szpill on" data-s="M" data-z="1">M</button>'
            '<button class="szpill" data-s="L" data-z="1">L</button>'
            "</div>"
            '<button class="btn-select">Select</button>'
            "</div>" % (model, name, _esc(name), _esc(meta))
        )
    inner = (
        '<div class="pcards">%s</div>'
        '<button id="cartFab" class="cartfab" type="button">Cart (<span id="cartCount">0</span>)</button>'
        '<aside id="cartDrawer" class="cartdrawer" aria-label="Cart">'
        "<h3>Your cart</h3>"
        '<div id="cartItems"></div>'
        '<button id="closeCart" class="btn-select" type="button">Close</button>'
        "</aside>"
    ) % "".join(cards)
    return _mount("cart", config, inner)


def _render_page(contract, blueprint, index, sections, page_file, mounted):
    """Render one HTML page on the Hub chassis. `mounted` is appended to
    (manifest rows). Returns (html, css_text, gate_ctx)."""
    template = contract["template"]
    soul = blueprint["soul"].lower()
    funcs = contract.get("functions") or {}
    page_no = 1 if page_file == "index.html" else 2
    page_label = blueprint["pages"][page_file] or "Home"
    pieces = index["pieces"]

    placed = []  # (role, model, label) — Law 14 registry

    # --- verbatim orb picks for the hero (JWL pieces, soul-wired) ---
    orb_models = []
    for pk in contract.get("pieces") or []:
        model = pk.get("model")
        if model and pieces[model]["category"] == "JWL":
            orb_models.append(model)
    orb_models = sorted(set(orb_models))
    orb_html = []
    for m in orb_models:
        h = pieces[m]["html"]
        h = _re.sub(r"--oc:#[0-9a-fA-F]{6}", "--oc:" + soul, h)
        h = _re.sub(r"--oc-rgb:\d{1,3},\d{1,3},\d{1,3}",
                    "--oc-rgb:" + _soul_rgb(soul), h)
        orb_html.append(h)
        placed.append(("hero orb", m, pieces[m].get("label")))

    # --- sections: mounts first, density rule drops empty ones ---
    rendered = []  # (sec_id, kicker, title, mounts)
    for sec_id, kicker, title, fids, pg in sections:
        if pg != page_no:
            continue
        mounts = []
        for fid in fids:
            if not funcs.get(fid):
                continue
            if fid.startswith(NO_UNIT_PREFIX):
                continue
            reg_id, unit_file = REGISTER[fid]
            if fid == "navigate":
                cfg = default_config(template, fid, contract,
                                     blueprint, page_file)
            elif fid == "booking" and template == "booking":
                # 3 services -> 3 mounted boards (brief section 3.4)
                for cfg in booking_service_configs(template, contract):
                    mounts.append(_mount(reg_id, cfg))
                    mounted.append({"contract_id": fid, "register_id": reg_id,
                                    "unit_file": unit_file, "section": sec_id,
                                    "page": page_file, "config": cfg})
                continue
            elif fid == "dictate":
                cfg = default_config(template, fid, contract,
                                     blueprint, page_file)
                mounts.append(_dictate_block(cfg))
                mounted.append({"contract_id": fid, "register_id": reg_id,
                                "unit_file": unit_file, "section": sec_id,
                                "page": page_file, "config": cfg})
                continue
            elif fid == "cart":
                cfg = default_config(template, fid, contract,
                                     blueprint, page_file)
                mounts.append(_cart_block(cfg))
                mounted.append({"contract_id": fid, "register_id": reg_id,
                                "unit_file": unit_file, "section": sec_id,
                                "page": page_file, "config": cfg})
                continue
            else:
                cfg = default_config(template, fid, contract,
                                     blueprint, page_file)
            mounts.append(_mount(reg_id, cfg))
            mounted.append({"contract_id": fid, "register_id": reg_id,
                            "unit_file": unit_file, "section": sec_id,
                            "page": page_file, "config": cfg})
        # density rule: a section with no working control is dropped
        if not mounts:
            continue
        rendered.append((sec_id, kicker, title, mounts))

    # --- spectrum walk: one hue per section, strict by position ---
    hues = _walk(template, len(rendered))
    sec_html = []
    for (sec_id, kicker, title, mounts), (hue_name, hue_hex) in zip(rendered, hues):
        placed.append(("section board: " + sec_id, PIECE_SECTION_BOARD,
                       pieces[PIECE_SECTION_BOARD].get("label")))
        sec_html.append(_section_board(sec_id, kicker, title, mounts,
                                       hue_name, hue_hex))
    placed.append(("footer panel", PIECE_SECTION_BOARD,
                   pieces[PIECE_SECTION_BOARD].get("label")))

    # --- chassis: rail, topbar, hero, footer ---
    eco_links_html = _eco_links(contract, blueprint, rendered, hues, soul)
    rail_html = _rail(contract, blueprint, rendered, page_file, hues, soul)

    # --- Smart Tabs standard chrome: the bar rides at the top of the main
    #     scroll surface, directly under the topbar (Shawn 2026-10-18 — every
    #     app ships it, personal pages included). Contract-driven (fail-closed):
    #     when the contract leaves smart-tabs off, no bar is emitted and the
    #     design-law gate below refuses the page, naming the missing unit.
    tabs_bar_html = ""
    if funcs.get("smart-tabs"):
        tabs_bar_html, tabs_cfg = _smart_tabs_bar(contract, blueprint,
                                                  page_file)
        mounted.append({"contract_id": "smart-tabs", "register_id": "smart-tabs",
                        "unit_file": "f-01-smart-tabs.js",
                        "section": "chrome:tabs-bar",
                        "page": page_file, "config": tabs_cfg})

    # --- CSS: Hub chassis harvest + verbatim piece CSS + page glue ---
    hub_css = _hub_css(soul)
    piece_models = [PIECE_SECTION_BOARD] + orb_models
    piece_css = _piece_css(index, soul, piece_models)
    css_text = hub_css + "\n\n" + piece_css + "\n\n/* page glue (law-built) */\n" + GLUE_CSS

    # --- scripts: chassis first, then loader + units mounted on this page --
    unit_files = []
    seen = set()
    for m in mounted:
        if m["page"] == page_file and m["unit_file"] not in seen:
            seen.add(m["unit_file"])
            unit_files.append(m["unit_file"])
    unit_files.sort()
    scripts = "\n".join(
        '  <script src="functions/%s"></script>' % f
        for f in [LOADER_FILE] + unit_files)

    title = _esc_title("%s \u2014 %s" % (contract.get("handle", ""),
                                          contract.get("idea", "")[:60].strip()))
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
%s
<style>
%s
</style>
</head>
<body>
<div class="shell rail-collapsed nb-scope" id="shell">
%s
<div class="drawer-backdrop" id="drawerBackdrop" aria-hidden="true"></div>
<main class="main">
%s
<div class="room-outlet">
%s
%s
%s
%s
</div>
</main>
</div>
%s
%s
</body>
</html>
""" % (title, FONTS_LINK, css_text,
       rail_html,
       _topbar(contract, eco_links_html),
       tabs_bar_html,
       _hero(contract, blueprint, soul, orb_html, page_label, orb_models),
       "\n".join(sec_html),
       _footer_manifest(contract, blueprint, soul, placed, index),
       _CHASSIS_JS, scripts)

    ctx = {"template": template, "soul": soul, "placed": placed,
           "index": index, "js": _CHASSIS_JS}
    return html, css_text, ctx


# ---------------------------------------------------------------------------
# Manifest + main
# ---------------------------------------------------------------------------

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--units", required=True)
    ap.add_argument("--manifest", required=True)
    a = ap.parse_args()

    contract = json.load(open(a.contract))
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", "..", "library", "catalog",
                              "builder-index-v1.json")
    index = json.load(open(index_path))

    errors = validate_contract(contract, index, a.units)
    if errors:
        _fail(errors)
    print("ok: contract validates — 0 problems")

    blueprint = BLUEPRINTS[contract["template"]]
    sections = blueprint["sections"]
    funcs = contract.get("functions") or {}

    # missing_functions: !no-unit: keys that are ON (fail-closed omission)
    missing = sorted(
        fid[len(NO_UNIT_PREFIX):]
        for fid, on in funcs.items()
        if fid.startswith(NO_UNIT_PREFIX) and on
    )

    mounted = []
    pages = {}
    for page_file, label in blueprint["pages"].items():
        if label is None:
            continue
        html, css_text, gate_ctx = _render_page(
            contract, blueprint, index, sections, page_file, mounted)
        violations = gate_design_laws(html, css_text, gate_ctx)
        if violations:
            print(json.dumps({"status": "gate-failed", "page": page_file,
                              "template": contract["template"],
                              "violations": violations}, indent=2))
            sys.exit(3)
        print("ok: design-law gate PASS — %s (0 violations)" % page_file)
        pages[page_file] = (html, css_text)

    # ---- write output ----
    if os.path.isdir(a.outdir):
        shutil.rmtree(a.outdir)
    os.makedirs(os.path.join(a.outdir, "functions"))
    written = []
    for page_file in PAGE_FILENAMES:
        if page_file not in pages:
            continue
        p = os.path.join(a.outdir, page_file)
        with open(p, "w", encoding="utf-8") as f:
            f.write(pages[page_file][0])
        written.append(p)
    # copy all 31 unit files byte-identical
    for fname in sorted(os.listdir(a.units)):
        src = os.path.join(a.units, fname)
        if os.path.isfile(src) and fname.endswith(".js"):
            dst = os.path.join(a.outdir, "functions", fname)
            shutil.copyfile(src, dst)
            written.append(dst)

    # ---- manifest (deterministic) ----
    contract_bytes = open(a.contract, "rb").read()
    contract_hash = hashlib.sha256(contract_bytes).hexdigest()
    file_rows = []
    digest = hashlib.sha256()
    for p in sorted(written):
        rel = os.path.relpath(p, a.outdir)
        fh = _sha256_file(p)
        file_rows.append({"path": rel, "sha256": fh,
                          "bytes": os.path.getsize(p)})
        digest.update(rel.encode("utf-8") + b"\0")
        with open(p, "rb") as f:
            digest.update(f.read())
    piece_picks = []
    for pk in contract.get("pieces") or []:
        model = pk.get("model")
        p = index["pieces"][model]
        piece_picks.append({
            "model": model,
            "label": p.get("label"),
            "css_id": p.get("css_id"),
            "note": pk.get("note", ""),
            "verbatim": True,
            "used_as": "hero decoration (jewel orb)" if p["category"] == "JWL" else "placed verbatim",
        })
    # chrome roles: rebuilt from the render pass for the manifest
    chrome_roles = []
    seen_roles = set()
    for _page_file, (_html, _css) in pages.items():
        for m in _re.finditer(r'data-piece="([^"]+)"', _html):
            model = m.group(1)
            role = "section board" if "<section" in _html[max(0, m.start()-120):m.start()] else "panel"
            key = (role, model)
            if key not in seen_roles:
                seen_roles.add(key)
                chrome_roles.append({
                    "role": role,
                    "model": model,
                    "label": index["pieces"][model].get("label"),
                })
    manifest = {
        "appmode": APPMODE_VERSION,
        "contract_hash": contract_hash,
        "handle": contract.get("handle"),
        "template": contract.get("template"),
        "soul": blueprint["soul"],
        "do": contract.get("do"),
        "behave": contract.get("behave"),
        "rules": contract.get("rules") or {},
        "mounted": mounted,
        "missing_functions": missing,
        "piece_picks": piece_picks,
        "chassis": {
            "pattern": "NayaNET Hub (index-2.html)",
            "sha256": HUB_SHA256,
            "adaptation": ("Fixed left rail (brand + page/section nav + private note) + "
                           "topbar (rooms-plus mobile, rail-toggle, title, status, eco-plus "
                           "destinations menu) + main scroll surface + mobile drawer. "
                           "Default rail-collapsed per Shawn's 2026-10-03 ruling. Corner plus "
                           "buttons harvested verbatim; hover ignition wired to the template "
                           "soul via var(--soul)."),
        },
        "plus_menus": {
            "rail_toggle": "toggles the left rail (template pages/features)",
            "eco_plus": "destinations dropdown (template pages + sections, per-link icon+color)",
            "rooms_plus": "mobile drawer navigation",
        },
        "chrome_roles": chrome_roles,
        "chrome_note": ("Page chassis follows the Hub pattern (index-2.html, sha-pinned). "
                        "Discrete pieces are composed verbatim from the 478-piece index: "
                        "section boards + footer panel = NAYA-CRD-008 (one board one color "
                        "via --accent), hero orbs = contract JWL picks (soul-wired). "
                        "Nothing invented — see the visible piece manifest on each page."),
        "files": file_rows,
        "output_hash": digest.hexdigest(),
    }
    with open(a.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")

    print("ok: wrote %d files to %s" % (len(written), a.outdir))
    print("ok: mounted %d function instances, %d missing (no-unit)"
          % (len(mounted), len(missing)))
    print("ok: output_hash %s" % manifest["output_hash"])


if __name__ == "__main__":
    main()
