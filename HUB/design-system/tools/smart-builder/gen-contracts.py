#!/usr/bin/env python3
"""Generate the 12 APP-MODE contract-v1 JSON files. Deterministic output."""
import json
import os

OUT = "/home/hatch/workspace/builder-review/HUB/design-system/tools/smart-builder/appmode-contracts"

ORB = {
    "personal": ["NAYA-JWL-001", "NAYA-JWL-002"],
    "today": ["NAYA-JWL-003"],
    "smartlist": ["NAYA-JWL-007"],
    "business": ["NAYA-JWL-005"],
    "booking": ["NAYA-JWL-006"],
    "product": ["NAYA-JWL-008"],
    "event": ["NAYA-JWL-003"],
    "community": ["NAYA-JWL-005"],
    "portfolio": ["NAYA-JWL-002"],
    "menu": ["NAYA-JWL-007"],
    "signup": ["NAYA-JWL-003"],
    "dashboard": ["NAYA-JWL-001"],
}


def C(template, handle, idea, vision, do, behave, functions, no_units=()):
    fns = dict(functions)
    for n in no_units:
        fns["!no-unit:" + n] = True
    return {
        "version": "contract-v1",
        "handle": handle,
        "idea": idea,
        "vision": vision,
        "do": do,
        "behave": behave,
        "template": template,
        "functions": fns,
        "pieces": [
            {"model": m, "name": "Hero orb", "size": "sm", "qty": 1,
             "note": "verbatim hero decoration"}
            for m in ORB[template]
        ],
        "rules": {"density": "drop text-only sections", "ignition": "white-at-rest"},
    }


contracts = {
    "personal": C(
        "personal", "maya-designs",
        "My whole creative life in one app — this morning's briefing, what I'm capturing, my lists, my stream, my people. One thumb, everything within reach.",
        "No more twelve open tabs and a notes app graveyard. I open this and I know exactly where my day stands.",
        "Read the morning briefing, capture thoughts by voice, keep lists, post to the stream, reach people.",
        "Calm, warm, fast. Nothing shouts; everything is one tap away.",
        {"smart-tabs": True, "intelligence-today": True, "dictate": True,
         "smart-lists": True, "feed": True, "connections": True,
         "contact": True, "share": True, "save": True},
        ("ask-naya",),
    ),
    "today": C(
        "today", "founder-briefing",
        "I open one page with my coffee and see the whole day: what matters, the numbers, the stream.",
        "Ten minutes, total clarity, then I go build.",
        "Read the briefing, check daily/weekly/monthly numbers, log the day, jump to tools.",
        "Direct and numbers-first. No fluff before coffee.",
        {"intelligence-today": True, "reports": True, "feed": True, "smart-tabs": True},
        ("ask-naya",),
    ),
    "smartlist": C(
        "smartlist", "renovation-2026",
        "The whole renovation in lists — rooms, budgets, decisions made, decisions pending. Nothing lives in my head rent-free anymore.",
        "Contractors ask, I answer in ten seconds, with the list to prove it.",
        "Track renovation lists, keep the big decisions saved, share a list with the contractor.",
        "Practical and opinionated. A list is a promise.",
        {"smart-lists": True, "save": True, "share": True},
        ("ask-naya", "calendar"),
    ),
    "business": C(
        "business", "copper-cup",
        "Our corner café's home on the internet — what we pour, what people say, book a table, reach us.",
        "A regular should feel the smell of espresso from this page.",
        "Show proof (services, reviews, numbers), book a table, meet the team, get in touch.",
        "Warm, a little proud, never corporate.",
        {"business-proof": True, "booking": True, "connections": True,
         "contact": True, "navigate": True},
        ("ask-naya",),
    ),
    "booking": C(
        "booking", "wag-and-shine",
        "Book your dog's spa day in under a minute — pick the service, pick a slot, done. No phone tag.",
        "Every dog leaves happier than it arrived. Every owner books in one thumb.",
        "Book grooming services by day and slot, ask questions, jump between pages.",
        "Cheerful and reassuring. The dogs are the customers; the humans just pay.",
        {"booking": True, "contact": True, "smart-tabs": True},
        ("ask-naya",),
    ),
    "product": C(
        "product", "kiln-and-glow",
        "One lamp, made by hand — see it, choose your finish, take it home.",
        "Light that feels like it was made for your room, because it was.",
        "View the lamp, pick a finish into the cart, share it, ask the maker.",
        "Crafted and quiet. Let the object talk.",
        {"product-display": True, "cart": True, "share": True, "contact": True},
        ("ask-naya",),
    ),
    "event": C(
        "event", "rooftop-jazz",
        "One night, one rooftop, a quartet and the skyline. RSVP and you're on the list.",
        "The kind of night people talk about on Monday.",
        "RSVP with party size, share the invite, ask the host.",
        "Electric and intimate. Velvet-rope energy, open-door policy.",
        {"event-rsvp": True, "share": True, "contact": True},
        ("ask-naya", "guard"),
    ),
    "community": C(
        "community", "maple-street",
        "Our street, finally organized — the feed, the spaces, the people. Borrow a ladder, find the lost cat, plan the block party.",
        "Know your neighbors' names again.",
        "Post to the street feed, browse and join spaces, manage membership.",
        "Neighborly and a little nosy, in the good way.",
        {"community-feed": True, "smart-spaces": True, "join": True, "navigate": True},
        ("ask-naya",),
    ),
    "portfolio": C(
        "portfolio", "june-park-photo",
        "My work, no noise — the frames that made me a photographer.",
        "If one image makes you feel something, the page did its job.",
        "Browse the work by tag, open the lightbox, share a frame, book a shoot.",
        "Confident and spare. The images carry it.",
        {"portfolio-showcase": True, "share": True, "contact": True},
        ("ask-naya",),
    ),
    "menu": C(
        "menu", "copper-cup-menu",
        "The Copper Cup menu — everything we pour and bake, with real prices. Order at the counter, no surprises.",
        "You should be able to taste the cardamom bun through the screen.",
        "Browse the menu, build an order, ask about catering.",
        "Appetizing and honest. Prices on everything.",
        {"menu-display": True, "contact": True},
        ("ask-naya",),
    ),
    "signup": C(
        "signup", "ship-it-challenge",
        "Five days, one tiny ship per day. Join the challenge — we'll mail you the day's mission every morning.",
        "Finishers ship. That's the whole philosophy.",
        "Sign up for the challenge, get the host's notes by mail.",
        "Energetic and encouraging. A coach, not a lecturer.",
        {"signup-capture": True, "smart-mail": True},
        ("ask-naya",),
    ),
    "dashboard": C(
        "dashboard", "marathon-42k",
        "26.2 miles, one dashboard — readiness check, this week's numbers, today's plan.",
        "No junk miles, no guesswork. Just the work that gets me to the start line healthy.",
        "Take the readiness assessment, review training numbers, read today's plan.",
        "Honest and disciplined. The stopwatch doesn't lie and neither does this page.",
        {"assessment-score": True, "reports": True, "intelligence-today": True,
         "navigate": True},
        ("ask-naya",),
    ),
}

os.makedirs(OUT, exist_ok=True)
for name, c in contracts.items():
    p = os.path.join(OUT, name + ".json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print("wrote", p)
