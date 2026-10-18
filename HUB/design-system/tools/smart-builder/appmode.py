#!/usr/bin/env python3
"""Smart Builder APP-MODE assembler v1 — contract-v1 JSON in, working app out.

Contract data + template blueprint + premade function units -> a working,
self-contained app page (index.html [+ page2.html] + functions/ dir).

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
  - Chrome: design-law shell (obsidian #050507, white text, soul-color
    accents, elevation, white-at-rest -> color-on-hover ignition,
    Newsreader hero + Inter UI). Verbatim piece picks are placed where the
    index provides usable chrome; the shell itself is law-built.
"""
import argparse
import hashlib
import html as htmlmod
import json
import os
import shutil
import sys
import urllib.parse

APPMODE_VERSION = "appmode-v1"
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
            ("tabs", "Navigate", "Your tabs", ["smart-tabs"], 1),
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
            ("tabs", "Navigate", "Your tabs", ["smart-tabs"], 1),
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
            ("tabs", "Navigate", "Your tabs", ["smart-tabs"], 1),
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
# Chrome — design-law page shell. Obsidian field, white voice, soul accents,
# elevation, white-at-rest -> color-on-hover ignition. Newsreader hero voice,
# Inter UI voice. (The piece index carries design-language specimen chrome,
# not generic app chrome — the shell is law-built; verbatim piece picks are
# placed where they genuinely fit and recorded in the manifest.)
# ---------------------------------------------------------------------------

SHELL_CSS = """
:root{--obsidian:#050507;--soul:%SOUL%;--ink:#F8F7FB;--quiet:rgba(248,247,251,.72);
--faint:rgba(248,247,251,.5);--line:rgba(255,255,255,.14)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--obsidian);color:var(--ink);
font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;
-webkit-font-smoothing:antialiased;line-height:1.55}
a{color:var(--ink)}
.wrap{max-width:1060px;margin:0 auto;padding:0 22px}
/* top chrome */
.topbar{position:sticky;top:0;z-index:50;background:rgba(5,5,7,.86);
backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.topbar .wrap{display:flex;align-items:center;gap:14px;padding-top:14px;padding-bottom:14px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.02em}
.brand .dot{width:12px;height:12px;border-radius:50%;background:var(--soul);
box-shadow:0 0 12px var(--soul)}
.topbar nav{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap}
.topbar nav a{color:#fff;text-decoration:none;font-size:13px;font-weight:600;
padding:8px 14px;border-radius:999px;border:1px solid transparent;transition:all .18s}
.topbar nav a:hover{border-color:var(--soul);box-shadow:0 0 14px color-mix(in srgb,var(--soul) 55%,transparent);
transform:translateY(-1px)}
/* hero */
.hero{padding:64px 0 40px;position:relative;overflow:hidden}
.hero .kicker{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.22em;
text-transform:uppercase;color:var(--soul);margin-bottom:14px}
.hero h1{font-family:Newsreader,Georgia,'Times New Roman',serif;font-weight:600;
font-size:clamp(34px,5.4vw,58px);line-height:1.08;margin:0 0 16px;color:#fff;
text-wrap:balance}
.hero .lede{font-size:18px;color:var(--quiet);max-width:640px;margin:0}
.hero .orbs{position:absolute;right:4%;top:26px;display:flex;gap:18px;opacity:.9}
.hero .greet{margin-top:18px;font-size:13px;color:var(--faint);display:flex;align-items:center;gap:10px}
.led{width:9px;height:9px;border-radius:50%;background:var(--soul);
box-shadow:0 0 10px var(--soul);animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
/* sections: boards with elevation */
.nsec{margin:26px 0;background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015));
border:1px solid var(--line);border-radius:22px;padding:30px 30px 34px;
box-shadow:inset 0 1px 0 rgba(255,255,255,.09),inset 0 -18px 40px rgba(0,0,0,.5),
0 24px 60px rgba(0,0,0,.55);transition:transform .2s,box-shadow .2s}
.nsec:hover{transform:translateY(-3px);
box-shadow:inset 0 1px 0 rgba(255,255,255,.12),inset 0 -18px 40px rgba(0,0,0,.5),
0 30px 70px rgba(0,0,0,.6),0 0 34px color-mix(in srgb,var(--soul) 22%,transparent)}
.nsec-head{margin-bottom:20px}
.nsec-head .kicker{font-size:11px;font-weight:800;letter-spacing:.24em;text-transform:uppercase;
color:var(--soul)}
.nsec-head h2{font-family:Newsreader,Georgia,serif;font-size:30px;font-weight:600;margin:6px 0 0;color:#fff}
/* mounted function roots get breathing room */
.nsec-body [data-fn]{margin:0}
.nsec-body [data-fn]+[data-fn]{margin-top:26px}
/* ignition: every interactive element, white at rest -> color on touch */
button,a.btn,input[type=submit]{transition:all .18s}
button:hover,a.btn:hover{box-shadow:0 0 16px color-mix(in srgb,var(--soul) 60%,transparent)}
/* capture block (dictate) */
.capture{display:flex;flex-direction:column;gap:12px}
.capture textarea{width:100%;min-height:110px;background:#0B0D12;color:#fff;font-size:16px;
border:1px solid var(--line);border-radius:14px;padding:14px;resize:vertical;font-family:inherit}
.capture textarea:focus{outline:none;border-color:var(--soul);box-shadow:0 0 0 3px color-mix(in srgb,var(--soul) 30%,transparent)}
.dictbtn{align-self:flex-start;background:#fff;color:#050507;border:none;border-radius:999px;
padding:12px 22px;font-weight:800;font-size:14px;cursor:pointer}
.dictbtn:hover{background:var(--soul);color:#fff;box-shadow:0 0 20px var(--soul)}
.capture .hint{font-size:12px;color:var(--faint)}
/* cart chrome for the product page (f-28-cart host surface) */
.cartfab{position:fixed;right:22px;bottom:22px;z-index:60;background:var(--soul);color:#fff;
border:none;border-radius:999px;padding:14px 20px;font-weight:800;cursor:pointer;
box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 20px color-mix(in srgb,var(--soul) 50%,transparent)}
.cartdrawer{position:fixed;right:0;top:0;bottom:0;width:min(380px,92vw);background:#0B0D12;
border-left:1px solid var(--line);z-index:70;transform:translateX(105%);transition:transform .25s;
display:flex;flex-direction:column;padding:20px}
.cartdrawer.open{transform:none}
.cartdrawer h3{margin:0 0 12px;color:#fff}
#cartItems{flex:1;overflow:auto}
.pcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-bottom:8px}
.pcard{background:#0B0D12;border:1px solid var(--line);border-radius:16px;padding:18px;color:#fff}
.pcard h4{margin:0 0 4px;color:#fff}
.pcard .pmeta{font-size:12px;color:var(--faint);margin-bottom:10px}
.szpills{display:flex;gap:8px;margin:10px 0}
.szpill{background:transparent;border:1px solid rgba(255,255,255,.35);color:#fff;border-radius:999px;
padding:6px 14px;font-size:12px;cursor:pointer}
.szpill.on{background:#fff;color:#050507;border-color:#fff;font-weight:700}
.btn-select{background:var(--soul);color:#fff;border:none;border-radius:999px;padding:10px 18px;
font-weight:700;cursor:pointer;width:100%}
.btn-select.picked{background:#2fe89e}
/* footer */
.footer{margin:60px 0 0;border-top:1px solid var(--line);padding:30px 0 60px;color:var(--faint);font-size:13px}
.footer nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
.footer nav a{color:#fff;text-decoration:none;font-size:13px;padding:8px 14px;border-radius:999px;
border:1px solid var(--line);transition:all .18s}
.footer nav a:hover{border-color:var(--soul);box-shadow:0 0 14px color-mix(in srgb,var(--soul) 55%,transparent)}
@media(max-width:640px){.nsec{padding:22px 18px}.hero{padding:44px 0 30px}.hero .orbs{display:none}}
@media(min-width:641px){.hero h1,.hero .lede{padding-right:190px}}
"""

FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800'
    '&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap" rel="stylesheet">'
)


def _esc(s):
    return htmlmod.escape("" if s is None else str(s), quote=True)


def _config_attr(config):
    raw = json.dumps(config, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True)
    return "'" + htmlmod.escape(raw, quote=True) + "'"


def _mount(register_id, config, inner=""):
    return '<div data-fn="%s" data-fn-config=%s>%s</div>' % (
        _esc(register_id), _config_attr(config), inner)


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

def _hero(contract, soul, blueprint, orb_html, orb_css_ids, page_label):
    idea = contract.get("idea", "")
    vision = contract.get("vision", "")
    orbs = ""
    if orb_html:
        orbs = '<div class="orbs">%s</div>' % "".join(
            '<span class="nb-scope">%s</span>' % o for o in orb_html)
    greet = ""
    if contract.get("template") == "personal":
        greet = ('<div class="greet"><span class="led"></span>'
                 '<span id="greetLine">Good day</span></div>')
    return (
        '<header class="hero"><div class="wrap">%s'
        '<div class="kicker">%s · %s</div>'
        "<h1>%s</h1>"
        '<p class="lede">%s</p>%s'
        "</div></header>"
    ) % (orbs, _esc(contract.get("handle", "")), _esc(page_label),
         _esc(idea), _esc(vision), greet)


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


def _section_html(sec_id, kicker, title, mounts):
    return (
        '<section class="nsec" id="sec-%s">'
        '<div class="nsec-head"><span class="kicker">%s</span><h2>%s</h2></div>'
        '<div class="nsec-body">%s</div>'
        "</section>"
    ) % (_esc(sec_id), _esc(kicker), _esc(title), "\n".join(mounts))


def _topnav(contract, blueprint, sections, page_file):
    links = []
    for sec_id, _k, title, _f, pg in sections:
        if pg == (1 if page_file == "index.html" else 2) and not sec_id.startswith("nav"):
            links.append('<a href="#sec-%s">%s</a>' % (_esc(sec_id), _esc(title)))
    for fname, label in blueprint["pages"].items():
        if label and fname != page_file:
            links.append('<a href="%s">%s</a>' % (_esc(fname), _esc(label)))
    return (
        '<div class="topbar"><div class="wrap">'
        '<div class="brand"><span class="dot"></span><span>%s</span></div>'
        "<nav>%s</nav>"
        "</div></div>"
    ) % (_esc(contract.get("handle", "")), "".join(links))


def _footer(contract, blueprint, sections, page_file):
    links = []
    for sec_id, _k, title, _f, pg in sections:
        if pg == (1 if page_file == "index.html" else 2) and not sec_id.startswith("nav"):
            links.append('<a href="#sec-%s">%s</a>' % (_esc(sec_id), _esc(title)))
    for fname, label in blueprint["pages"].items():
        if label and fname != page_file:
            links.append('<a href="%s">%s</a>' % (_esc(fname), _esc(label)))
    return (
        '<footer class="footer"><div class="wrap"><nav>%s</nav>'
        "<div>Built with the Naya Smart Builder \u00b7 APP-MODE %s \u00b7 "
        "everything on this page works \u2014 tap anything.</div>"
        "</div></footer>"
    ) % ("".join(links), _esc(APPMODE_VERSION))


_GREET_JS = """
<script>
(function(){
  var el=document.getElementById('greetLine'); if(!el) return;
  var h=new Date().getHours();
  var g=h<5?'Up late':h<12?'Good morning':h<18?'Good afternoon':'Good evening';
  var d=new Date().toLocaleDateString(undefined,{weekday:'long',month:'long',day:'numeric'});
  el.textContent=g+' \\u2014 '+d;
})();
</script>
"""


def _render_page(contract, blueprint, index, sections, page_file, mounted,
                 css_ids, orb_models):
    """Render one HTML page. `mounted` is appended to (manifest rows)."""
    soul = blueprint["soul"]
    funcs = contract.get("functions") or {}
    page_no = 1 if page_file == "index.html" else 2
    page_label = blueprint["pages"][page_file] or "Home"

    # verbatim orb picks for the hero
    pieces = index["pieces"]
    orb_html = []
    for m in orb_models:
        orb_html.append(pieces[m]["html"])
        cid = pieces[m]["css_id"]
        if cid and cid not in css_ids:
            css_ids.append(cid)

    sec_html = []
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
                cfg = default_config(contract["template"], fid, contract,
                                     blueprint, page_file)
            elif fid == "booking" and contract["template"] == "booking":
                # 3 services -> 3 mounted boards (brief section 3.4)
                for cfg in booking_service_configs(contract["template"], contract):
                    mounts.append(_mount(reg_id, cfg))
                    mounted.append({"contract_id": fid, "register_id": reg_id,
                                    "unit_file": unit_file, "section": sec_id,
                                    "page": page_file, "config": cfg})
                continue
            elif fid == "dictate":
                cfg = default_config(contract["template"], fid, contract,
                                     blueprint, page_file)
                mounts.append(_dictate_block(cfg))
                mounted.append({"contract_id": fid, "register_id": reg_id,
                                "unit_file": unit_file, "section": sec_id,
                                "page": page_file, "config": cfg})
                continue
            elif fid == "cart":
                cfg = default_config(contract["template"], fid, contract,
                                     blueprint, page_file)
                mounts.append(_cart_block(cfg))
                mounted.append({"contract_id": fid, "register_id": reg_id,
                                "unit_file": unit_file, "section": sec_id,
                                "page": page_file, "config": cfg})
                continue
            else:
                cfg = default_config(contract["template"], fid, contract,
                                     blueprint, page_file)
            mounts.append(_mount(reg_id, cfg))
            mounted.append({"contract_id": fid, "register_id": reg_id,
                            "unit_file": unit_file, "section": sec_id,
                            "page": page_file, "config": cfg})
        # density rule: a section with no working control is dropped
        if not mounts:
            continue
        sec_html.append(_section_html(sec_id, kicker, title, mounts))

    # scripts: loader first, then only the units actually mounted on this page
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

    piece_css = "\n".join(
        "/* css:%s */\n%s" % (cid, index["css_bank"][cid]) for cid in css_ids)

    title = "%s — %s" % (contract.get("handle", ""),
                         contract.get("idea", "")[:60])
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
%s
<style>
%s
%s
</style>
</head>
<body>
%s
%s
<main class="wrap">
%s
</main>
%s
%s
%s
</body>
</html>
""" % (_esc(title), FONTS_LINK,
       SHELL_CSS.replace("%SOUL%", soul), piece_css,
       _topnav(contract, blueprint, sections, page_file),
       _hero(contract, soul, blueprint, orb_html, css_ids, page_label),
       "\n".join(sec_html),
       _footer(contract, blueprint, sections, page_file),
       _GREET_JS, scripts)


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

    # orb piece picks for the hero (verbatim, decorative)
    orb_models = []
    for pk in contract.get("pieces") or []:
        model = pk.get("model")
        if model and index["pieces"][model]["category"] == "JWL":
            orb_models.append(model)
    orb_models = sorted(set(orb_models))

    mounted = []
    css_ids = []
    pages = {}
    for page_file, label in blueprint["pages"].items():
        if label is None:
            continue
        pages[page_file] = _render_page(
            contract, blueprint, index, sections, page_file, mounted,
            css_ids, orb_models)

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
            f.write(pages[page_file])
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
        "chrome_note": ("Page shell is design-law chrome (obsidian #050507, "
                        "white voice, soul accents, elevation, ignition, "
                        "Newsreader hero + Inter UI). The piece index carries "
                        "design-language specimen fragments, not generic app "
                        "hero/nav/section chrome — no verbatim shell pieces "
                        "existed to pull; picks above are the usable verbatim "
                        "decorative pieces."),
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
