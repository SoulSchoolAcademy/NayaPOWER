#!/usr/bin/env python3
"""
The Welcome Engine — SET B's spine for the one flow (Naya Power, 2026-10-24).

One input: the citizen's answers (Questions V2). One output: the activation
receipt — Trinity page content (verbatim), the profile vector, the coverage
accounting, the ambassador link, and first matches. Deterministic: the same
answers always produce the same receipt. Nothing is invented: a skipped
answer becomes "not yet shared" on the page and "skipped" in the accounting;
a missing answer is named missing.

The question IS the schema: SLOTS is the destination map from Questions V2.
"""
import json, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smart_match import score, rank_matches, TAXONOMY, TERM2CONCEPTS  # the one matcher

# id -> (walk label, destinations) ; destinations: page -> field, plus vector field
SLOTS = {
    "into":          ("What are you into?",            {"personal": "topics",      "vector": "topics"}),
    "matters":       ("What matters to you?",          {"personal": "values",      "vector": "goals"}),
    "goal_personal": ("Your personal goal",            {"personal": "goal",        "vector": "goals"}),
    "vision":        ("Your vision",                   {"personal": "vision",      "vector": "goals"}),
    "mission":       ("Your mission",                  {"personal": "mission",     "vector": "goals"}),
    "motto":         ("Your motto",                    {"personal": "motto",       "trinity": "motto"}),
    "do":            ("What do you do?",               {"personal": "what_i_do",   "vector": "offers"}),
    "biz_what":      ("Your business: what, who for",  {"business": "description", "vector": "topics"}),
    "biz_goal":      ("Your business goal",            {"business": "goal",        "vector": "goals"}),
    "offers":        ("What you can help others with", {"personal": "offers",      "vector": "offers"}),
    "needs":         ("What you need",                 {"service": "needs",        "vector": "needs"}),
    "wants":         ("Who you want to meet",          {"service": "wants",        "vector": "wants"}),
    "space_about":   ("Your space: about, who for",    {"space": "purpose",        "vector": "topics"}),
    "links":         ("Your links (block)",            {"pages": "links"}),
}
PAGE_FIELDS = {  # what each page needs to be called DONE (coverage accounting)
    "personal": ["topics", "values", "goal", "vision", "mission", "motto", "what_i_do", "offers"],
    "business": ["description", "goal"],
    "space":    ["purpose"],
}
NOT_SHARED = "Not yet shared"


LEAD_INS = ("i love ", "i'm into ", "i am into ", "im into ", "my goal is ", "my mission is ",
            "my vision is ", "i want to ", "i want ", "i do ", "i'm ", "i am ", "my motto is ")


def extract_phrases(text):
    """Split a free answer into signal phrases: on commas/semicolons/'and',
    with conversational lead-ins stripped ('I love gardening' -> 'gardening')."""
    if not text:
        return []
    chunks = re.split(r"[,;•\n]| and ", text)
    out = []
    for c in chunks:
        c = " ".join(c.strip().lower().split())
        for lead in LEAD_INS:
            if c.startswith(lead):
                c = c[len(lead):]
                break
        c = c.strip(" .!")
        if c and len(c.split()) <= 7 and len(c) > 1:
            out.append(c)
    return out


def concepts_in(text):
    """Governed concepts whose member phrases appear in the text."""
    low = (text or "").lower()
    return sorted({c for phrase, cs in TERM2CONCEPTS.items() if phrase in low for c in cs})


def build_vector(answers):
    vec = {"topics": [], "goals": [], "offers": [], "needs": [], "wants": []}
    for qid, (_, dest) in SLOTS.items():
        vf = dest.get("vector")
        ans = answers.get(qid)
        if vf and isinstance(ans, str) and ans.strip():
            vec[vf].extend(extract_phrases(ans))
    return {k: sorted(set(v)) for k, v in vec.items()}


def generate_pages(answers, has_business):
    pages = {"personal": {}, "business": {}, "space": {}}
    for qid, (_, dest) in SLOTS.items():
        ans = answers.get(qid)
        for page in ("personal", "business", "space"):
            field = dest.get(page)
            if field:
                pages[page][field] = ans if isinstance(ans, str) and ans.strip() else NOT_SHARED
    if not has_business:
        pages["business"] = {"state": "not_started",
                             "note": "No business declared at the walk. This page wakes the day they start one."}
    motto = answers.get("motto")
    pages["motto"] = motto if isinstance(motto, str) and motto.strip() else NOT_SHARED
    links = answers.get("links") or []
    pages["links"] = [{"url": u, "tracked": True} for u in links]  # default: tracked (plan, 2026-10-24)
    return pages


FIELD2Q = {}
for _q, (_, _d) in SLOTS.items():
    for _page in ("personal", "business", "space"):
        if _d.get(_page):
            FIELD2Q[(_page, _d[_page])] = _q


def coverage(answers, has_business):
    """Every needed field: filled / filled_thin (<3 words — counts as filled,
    named as a follow-up candidate) / skipped (key present, empty) / missing."""
    field_state, thin = {}, []
    for page, fields in PAGE_FIELDS.items():
        if page == "business" and not has_business:
            continue
        for f in fields:
            qid = FIELD2Q[(page, f)]
            if qid not in answers:
                field_state[f"{page}.{f}"] = "missing"
            elif isinstance(answers[qid], str) and answers[qid].strip():
                if len(answers[qid].split()) < 3:
                    field_state[f"{page}.{f}"] = "filled_thin"
                    thin.append(f"{page}.{f}")
                else:
                    field_state[f"{page}.{f}"] = "filled"
            else:
                field_state[f"{page}.{f}"] = "skipped"
    total = len(field_state)
    filled = sum(1 for s in field_state.values() if s.startswith("filled"))
    accounted = sum(1 for s in field_state.values() if s != "missing")
    return {"fields": field_state, "thin": thin,
            "filled_pct": round(100 * filled / total) if total else 100,
            "accounted_pct": round(100 * accounted / total) if total else 100}


def issue_link_sql(alias):
    """The activation issuance (pattern proven live 2026-10-24 on 9 citizens)."""
    return ("insert into public.ambassador_links (alias, link_url) values "
            f"('{alias}', 'https://nayanet.live/joinus?ref={alias}') on conflict (alias) do nothing;")


def activate(alias, answers, corpus, has_business=None):
    """The whole chain, one call: answers -> pages + vector + coverage + link + matches.
    Findability gate lives HERE, not in the caller: corpus entries carrying
    "_findable": False are excluded from matching and counted in the receipt."""
    if has_business is None:
        has_business = answers.get("_has_business", bool(answers.get("biz_what")))
    vec = build_vector(answers)
    visible = {n: c for n, c in corpus.items() if c.get("_findable", True)}
    excluded = len(corpus) - len(visible)
    clean = {n: {k: v for k, v in c.items() if not k.startswith("_")} for n, c in visible.items()}
    matches = rank_matches(vec, clean)
    receipt = {
        "alias": alias,
        "pages": generate_pages(answers, has_business),
        "settings": {  # SN-0852 ratified defaults, bound at activation
            "personal": {"visibility": "private", "findable": True, "installable": True},
            "business": {"visibility": "public", "findable": True, "installable": True},
            "space":    {"visibility": "public", "findable": True, "installable": True}},
        "vector": vec,
        "corpus_entry": {"alias": alias, "vector": vec, "findable": True},
        "coverage": coverage(answers, has_business),
        "ambassador_link": f"https://nayanet.live/joinus?ref={alias}",
        "issue_link_sql": issue_link_sql(alias),
        "first_matches": matches,
        "corpus_excluded_unfindable": excluded,
    }
    if not matches:
        receipt["match_note"] = ("No surface matches yet — a match needs two independent signals. "
                                 "The corpus grows with every citizen; the matcher keeps watching.")
    return receipt
