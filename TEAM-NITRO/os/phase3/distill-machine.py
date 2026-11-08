#!/usr/bin/env python3
"""distill-machine.py — Machine 5 of the Ultimate Operating System.

Distillation as code. Reads N raw notes (default 10), finds the one thing
that changes the next decision, and writes ONE distilled note in the
canonical Smart Note shape — then files it via the file-machine with
read-back verification, and records the lesson so the next brief starts
smarter.

The machine is CODE that runs. It does not understand like a human; it
extracts and composes BY RULE, and every rule is written below, so any
seat can audit what it did:

  * Concepts: content words (stopwords removed) ranked by DOCUMENT
    frequency — in how many of the N input notes the word appears.
    A concept is a word in at least half the notes.
  * Centroid: the input whose Nutshell holds the most concepts. Its
    Nutshell (verbatim) is the distilled Nutshell's base, and its quote
    block (Shawn's words) is carried verbatim.
  * Sections (Human/Child/Grandma/Naya): the input section with the
    highest concept DENSITY (distinct concepts / word count) — the
    densest, simplest explanation of the common thread, written by a
    human, selected by rule.
  * What it means / Why it matters / What changes now: the UNION of all
    inputs' items, deduplicated by normalized text, ranked by concept
    overlap, capped (5 / 4 / 6). The #1 "What changes now" item IS the
    lesson — the one thing that changes the next decision.
  * Title: the #1 item's bold lead phrase (human-written essence),
    title-cased. It must contain a top-10 concept, or the machine takes
    the next-ranked item. The title names the lesson, not a bystander.
  * Topic: the majority topic of the inputs (tie-break: first input).
  * SN number: max SN filed (GitHub public API, today) + 1 — via the
    git/trees API first (one call, no per-directory flakiness), the
    contents listing as fallback. The machine REFUSES 2212/2213
    (retired) and REFUSES if the exact dest path already exists
    (someone else took the number).

Filing gate (SN-2237, checked mechanically before any filing):
  1. One piece of intelligence (one title, one topic, one Nutshell).
  2. Canonical shape (all 9 sections non-empty).
  3. Simplest words (Child section averages <= 30 words/sentence).
  4. No duplicate (slug unused in the local smart-notes dir).
  5. Changes the next decision (>= 1 "What changes now" item).
  6. SN number is max+1 and the dest does not exist yet.
  7. Composed lists non-empty (means/matters/changes) — the gate checks
     what will actually be filed, not just the selected sections.
  Dest path: folder = slashed date (2026/11/08), filename = compact
  date (20261108) — the format every filed note uses. A hyphenated
  folder (2026-11-08) files the note where nothing looks for it and
  blinds the collision guard (dry run 6 caught it by comparing the
  dest against SN-2276/SN-2277 in the trees API).
Any gate fails -> refuse to file, say which gate, exit 1.

Filing verification is two layers: the file-machine's read-back, and —
if that fails — an independent check (GitHub API blob sha must equal
the receipt's blob_sha AND the raw CDN with a cache-buster must return
the local file byte-identical). A new path can 404 on the raw CDN for
a minute after the PUT even though the file is on main (SN-2278) — a
failed read-back proves nothing on its own. Never claim NOT FILED
until the independent check has failed too.

NEVER deletes a raw note. Deletion after distillation is Shawn's hand.

Usage:
  python3 distill-machine.py --inputs NOTE1.md NOTE2.md ... [NOTE10.md]
      [--out-dir DIR] [--topic TOPIC] [--date YYYY-MM-DD]
      [--file] [--receipt DIR] [--lesson-out FILE]
  --file: also file the distilled note via file-machine.py (default: write
          the local file + lesson record only, no filing).
  Exit 0 = distilled (+ filed and verified if --file).
  Exit 1 = gate refused, filing failed, or the machine could not run.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OS_DIR = os.path.dirname(HERE)  # ~/workspace/team-nitro/os
FILE_MACHINE = os.path.join(OS_DIR, "file-machine.py")
SMART_NOTES_DIR = os.path.expanduser("~/workspace/team-nitro/smart-notes")
GH_API = ("https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"
          "/contents/BRAIN/05-MEMORY/SMART-NOTES")
RETIRED = (2212, 2213)

SECTIONS = ["Hook", "Nutshell", "Human", "Child", "Grandma", "Naya",
            "What it means", "Why it matters", "What changes now"]

STOP = set("""a an the and or but of to in on for with by at from as is are was
were be been being it its this that these those he she they we you i his her
their our your my me him us them what which who whom when where why how not
no yes if then than so such only just also very can could will would should
may might must do does did done have has had having there here all any each
every both few more most other some such nor own same too don should now one
two three four five six seven eight nine ten because through next before
after between into over under out off about against during without within
along across behind beyond per via way thing things part end first last new
same get gets make makes take takes go goes come say says see know think
look need needs want use used keep let show give find bring set report""".split())


def words(text):
    return [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z\-']+", text)
            if w.lower() not in STOP and len(w) >= 3]


def parse_note(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    title = lines[0].lstrip("# ").strip() if lines else ""
    sn = None
    topic = ""
    m = re.search(r"^SN-(\d+)\s+·\s+(.+)$", text, re.M)
    if m:
        sn = int(m.group(1))
        topic = m.group(2).strip()
    created = ""
    m = re.search(r"^\*\*Created:\*\*\s+(.+)$", text, re.M)
    if m:
        created = m.group(1).strip()
    quote = ""
    m = re.search(r"\n> (.+?)\n\n## ", text, re.S)
    if m:
        quote = m.group(1).strip()
    sections = {}
    for name in SECTIONS:
        m = re.search(r"## " + re.escape(name) + r"\n\n(.*?)(?=\n## |\Z)",
                      text, re.S)
        sections[name] = m.group(1).strip() if m else ""
    return {"path": path, "title": title, "sn": sn, "topic": topic,
            "created": created, "quote": quote, "sections": sections,
            "text": text}


def split_items(body):
    """Split a section body into its items.

    Lists first (numbered or bulleted lines, with continuations; a
    header line before the first item is dropped). If a section has no
    list markers at all — prose, e.g. 'Why it matters' is one paragraph
    per note — fall back to paragraphs, one item per paragraph. Without
    this fallback the composed note gets an empty section while the
    gate still passes (dry run 4 caught it).
    """
    items = []
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(?:\d+\.|[-*])\s+(.*)$", line)
        if m:
            items.append(m.group(1).strip())
        elif items and not line.startswith("#"):
            items[-1] += " " + line
    if items:
        return items
    return [p.replace("\n", " ").strip()
            for p in body.split("\n\n") if p.strip()]


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def dedupe(items):
    seen = set()
    out = []
    for it in items:
        key = norm(re.sub(r"\*\*", "", it))
        if key and key not in seen:
            seen.add(key)
            out.append(it)
    return out


def bold_lead(item):
    m = re.match(r"\*\*(.+?)\*\*", item)
    return m.group(1).strip() if m else ""


def concept_overlap(text, concepts):
    present = set(words(text))
    return sum(1 for c in concepts if c in present)


def gh_json(url, attempts=3):
    """GET a GitHub API URL as JSON, with retries.

    The contents endpoint flakes: a directory that exists can 404 for a
    minute (observed 2026-11-08 ~02:12-02:15Z on the 2026/11/08 listing
    while its parent and children returned 200). A single 404 proves
    nothing — retry before concluding anything.
    """
    import time
    import urllib.error
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(
                url, headers={"Accept": "application/vnd.github+json",
                              "User-Agent": "muse-distill-machine/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, json.load(resp)
        except urllib.error.HTTPError as exc:
            last = exc
            if attempt < attempts - 1:
                time.sleep(5)
                continue
            raise
        except Exception as exc:
            last = exc
            if attempt < attempts - 1:
                time.sleep(5)
                continue
            raise
    raise last


def max_sn_for_date(date):
    """Highest SN filed on a date (date is YYYY-MM-DD). Fails loudly.

    NOTE: the GitHub PATH uses slashes (2026/11/08) while the date is
    hyphenated (2026-11-08) — the pattern and the contents URL must use
    the slash form, or nothing matches (dry run 3 caught this: it
    returned 0 and would have filed SN-1).
    Primary: the git/trees API (one call, the whole repo tree, no
    per-directory flakiness). Fallback: the contents listing with
    retries. The contents endpoint flakes: a directory that exists can
    404 for minutes (observed 2026-11-08 ~02:12-02:17Z on the
    2026/11/08 listing while its parent and children returned 200).
    """
    path_date = date.replace("-", "/")
    pat = re.compile(r"^BRAIN/05-MEMORY/SMART-NOTES/%s/[^/]+/SN-(\d+)/"
                     % re.escape(path_date))
    try:
        status, tree = gh_json(
            "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"
            "/git/trees/main?recursive=1")
        if status == 200 and isinstance(tree, dict) and "tree" in tree:
            sns = [int(m.group(1)) for e in tree["tree"]
                   for m in [pat.match(e.get("path", ""))] if m]
            if sns:
                return max(sns)
            return 0
    except Exception:
        pass  # fall through to the contents listing
    status, topics = gh_json(GH_API + "/" + path_date)
    if status != 200:
        raise RuntimeError("GitHub API returned %d for %s" % (status, date))
    top = 0
    for t in topics:
        if t.get("type") != "dir":
            continue
        _, entries = gh_json(t["url"])
        for e in entries:
            name = e.get("name", "")
            if name.startswith("SN-"):
                try:
                    top = max(top, int(name.split("-")[1]))
                except ValueError:
                    pass
    return top


def dest_exists(dest):
    """True if the dest file already exists in GitHub.

    Checks BOTH the API and the raw CDN (two independent systems — the
    contents endpoint flakes, so one 404 proves nothing). Fails closed:
    if either system is unreachable after retries, raises instead of
    guessing absent.
    """
    import urllib.error
    api_exists = False
    try:
        status, _ = gh_json(
            "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"
            "/contents/" + dest)
        api_exists = (status == 200)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise RuntimeError(
                "cannot check dest existence (API HTTP %d)" % exc.code)
        api_exists = False  # 404 on all attempts: absent (API view)
    except Exception as exc:
        raise RuntimeError(
            "cannot check dest existence (API unreachable): %s" % exc)
    raw_url = ("https://raw.githubusercontent.com/SoulSchoolAcademy"
               "/NayaPOWER/main/" + dest)
    raw_exists = False
    try:
        req = urllib.request.Request(
            raw_url, headers={"User-Agent": "muse-distill-machine/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw_exists = (resp.status == 200)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise RuntimeError(
                "cannot check dest existence (raw CDN HTTP %d)" % exc.code)
        raw_exists = False
    except Exception as exc:
        raise RuntimeError(
            "cannot check dest existence (raw CDN unreachable): %s" % exc)
    return api_exists or raw_exists


def independent_verify(dest, blob_sha, local_path):
    """Verify a filing the file-machine could not confirm.

    The file-machine's read-back is raw.githubusercontent.com only, and
    a NEW path can 404 on the CDN for a minute or two after the PUT
    even though the file is already on main (SN-2278, 02:26Z: the PUT
    succeeded, the API showed the blob, the raw CDN 404'd for ~90s).
    Before concluding NOT FILED, check two independent systems: the
    GitHub API contents endpoint (blob sha must equal the receipt's
    blob_sha) and the raw CDN with a cache-buster (HTTP 200 and sha256
    must equal the local file). Returns True only if all agree.
    """
    if not blob_sha:
        print("INDEPENDENT VERIFY: no blob_sha in receipt — cannot verify")
        return False
    status, data = gh_json(
        "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"
        "/contents/" + dest)
    if status != 200 or data.get("sha") != blob_sha:
        print("INDEPENDENT VERIFY: API blob mismatch (status %s, sha %s)"
              % (status, data.get("sha")))
        return False
    want = hashlib.sha256(open(local_path, "rb").read()).hexdigest()
    url = ("https://raw.githubusercontent.com/SoulSchoolAcademy"
           "/NayaPOWER/main/%s?cb=%s" % (dest, blob_sha))
    for attempt in (1, 2, 3):
        proc = subprocess.run(
            ["curl", "-s", "-o", "/tmp/distill-verify.tmp",
             "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=120)
        if proc.stdout.strip() == "200":
            got = hashlib.sha256(
                open("/tmp/distill-verify.tmp", "rb").read()).hexdigest()
            if got == want:
                print("INDEPENDENT VERIFY: API blob match + raw cb "
                      "sha256 match (attempt %d)" % attempt)
                return True
            print("INDEPENDENT VERIFY: raw sha mismatch (attempt %d)"
                  % attempt)
        else:
            print("INDEPENDENT VERIFY: raw HTTP %s (attempt %d)"
                  % (proc.stdout.strip(), attempt))
        if attempt < 3:
            time.sleep(20)
    return False


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60].rstrip("-")


def title_case(text):
    small = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for",
             "with", "by", "is", "at", "from", "as"}
    out = []
    for i, w in enumerate(text.split()):
        out.append(w if (i and w.lower() in small) else w[:1].upper() + w[1:])
    return " ".join(out)


def main():
    parser = argparse.ArgumentParser(description="Distill N notes to one, as code.")
    parser.add_argument("--inputs", nargs="+", required=True,
                        help="Input note files (10 for a 10:1 proof run)")
    parser.add_argument("--out-dir", default=SMART_NOTES_DIR,
                        help="Where the distilled note's local file goes")
    parser.add_argument("--topic", default=None,
                        help="Topic folder (default: majority topic)")
    parser.add_argument("--date", default=None,
                        help="Date YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--file", action="store_true",
                        help="File via file-machine.py (else write local only)")
    parser.add_argument("--receipt", default=None,
                        help="Directory for the filing receipt + lesson JSON")
    parser.add_argument("--lesson-out", default=None,
                        help="Path for the lesson JSON (default: receipt dir)")
    args = parser.parse_args()

    date = args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    notes = [parse_note(os.path.expanduser(p)) for p in args.inputs]
    n = len(notes)
    for note in notes:
        if note["sn"] is None:
            print("MACHINE REFUSED: no SN number in %s" % note["path"])
            return 1

    # --- concepts: document frequency across the inputs ---
    from collections import Counter
    df = Counter()
    first_seen = {}
    for note in notes:
        body = " ".join(note["sections"].values())
        seen = set(words(body))
        for i, w in enumerate(words(body)):
            if w not in first_seen:
                first_seen[w] = i
        for w in seen:
            df[w] += 1
    concepts = [w for w, c in df.items() if c >= (n + 1) // 2]
    concepts.sort(key=lambda w: (-df[w], first_seen.get(w, 9999)))
    top_concepts = concepts[:10]
    print("Concepts (df >= %d of %d): %s"
          % ((n + 1) // 2, n, ", ".join(
              "%s(%d)" % (w, df[w]) for w in top_concepts)))

    # --- centroid: the input whose Nutshell holds the most concepts ---
    def centroid_score(note):
        present = set(words(note["sections"]["Nutshell"]))
        return sum(1 for c in top_concepts if c in present)
    ranked = sorted(notes, key=lambda nt: (-centroid_score(nt),
                    len(nt["sections"]["Nutshell"])))
    centroid = ranked[0]
    print("Centroid: SN-%d (%d/%d concepts in its Nutshell)"
          % (centroid["sn"], centroid_score(centroid), len(top_concepts)))

    # --- section selection by concept density ---
    def best_section(name):
        best, best_key = None, None
        for note in notes:
            body = note["sections"][name]
            if not body:
                continue
            ws = words(body)
            if not ws:
                continue
            density = concept_overlap(body, top_concepts) / float(len(ws))
            key = (density, -len(ws))
            if best_key is None or key > best_key:
                best, best_key = body, key
        return best or ""
    chosen = {name: best_section(name) for name in SECTIONS}

    # --- union items, deduplicated, ranked by overlap ---
    def union_items(name, cap):
        all_items = []
        for note in notes:
            all_items.extend(split_items(note["sections"][name]))
        uniq = dedupe(all_items)
        uniq.sort(key=lambda it: (-concept_overlap(it, top_concepts),
                                  -len(it)))
        return uniq[:cap]
    means = union_items("What it means", 5)
    matters = union_items("Why it matters", 4)
    changes = union_items("What changes now", 6)

    # --- the lesson: the #1 "What changes now" item ---
    lesson_item = changes[0] if changes else ""
    lesson_lead = bold_lead(lesson_item)

    # --- title: the LESSON's bold lead, title-cased. The title must name
    # the one thing that changes the next decision — which is the lesson.
    # Guard only: the lead must carry at least one top-10 concept, or the
    # machine takes the next-ranked item. ---
    title = ""
    for item in changes:
        lead = bold_lead(item)
        if not lead:
            continue
        if any(c in words(lead) for c in top_concepts):
            title = title_case(lead.rstrip("."))
            break
    if not title:
        title = title_case("The " + top_concepts[0]) if top_concepts else "Distilled"
    print("Lesson: %s" % lesson_item[:160])
    print("Title: %s" % title)

    # --- topic: majority, tie-break first input ---
    if args.topic:
        topic = args.topic
    else:
        counts = Counter(nt["topic"].split(" / ")[0] for nt in notes)
        topic = sorted(counts.items(), key=lambda kv: (-kv[1],
                       notes[0]["topic"]))[0][0]
    print("Topic: %s" % topic)

    # --- sub-topic: the first top-10 concept word in the title's bold
    # lead, uppercased; else the centroid note's sub. The canonical
    # shape is SN-#### · TOPIC / SUB — a note without a sub is not in
    # the shape (dry run 5 wrote "SN-2278 · SYSTEM" with no sub). The
    # folder stays the TOPIC; the sub lives only in the L2 line. ---
    sub = ""
    for w in words(lesson_lead):
        if w in top_concepts:
            sub = w.upper()
            break
    if not sub and " / " in centroid["topic"]:
        sub = centroid["topic"].split(" / ", 1)[1].strip()
    l2_topic = ("%s / %s" % (topic, sub)) if sub else topic
    print("Sub-topic: %s" % (sub or "(none)"))

    # --- SN number: max filed today + 1 (GitHub API; fails loudly) ---
    try:
        sn = max_sn_for_date(date) + 1
    except Exception as exc:
        print("MACHINE REFUSED: cannot determine next SN: %s" % exc)
        return 1
    if sn in RETIRED:
        print("MACHINE REFUSED: SN-%d is retired" % sn)
        return 1
    print("SN number: %d (max filed today + 1)" % sn)

    slug = slugify(title)
    # Dest path: the folder is the SLASHED date (2026/11/08, three
    # levels) and the filename is the COMPACT date (20261108) — the
    # format every filed note uses (verified against SN-2276/SN-2277
    # in the trees API). A hyphenated folder (2026-11-08) would file
    # the note where nothing looks for it and the max-SN scan would
    # never see it again. The dest is also what dest_exists checks,
    # so a wrong dest makes the collision guard blind.
    path_date = date.replace("-", "/")
    compact_date = date.replace("-", "")
    dest = ("BRAIN/05-MEMORY/SMART-NOTES/%s/%s/SN-%d/"
            "IB-SMART-NOTE-%s-sn%d-%s.md"
            % (path_date, topic, sn, compact_date, sn, slug))
    created = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%MZ")

    # --- compose the distilled note (canonical shape) ---
    thread = ", ".join(top_concepts[:3])
    nutshell = chosen["Nutshell"]
    if thread:
        nutshell += ("\n\nAcross %d notes, the thread is: %s."
                     % (n, thread))
    parts = []
    parts.append("# " + title)
    parts.append("")
    parts.append("SN-%d · %s" % (sn, l2_topic))
    parts.append("")
    parts.append("**Created:** %s" % created)
    parts.append("")
    if centroid["quote"]:
        q = centroid["quote"].strip()
        if not (q.startswith('"') and q.endswith('"')):
            q = '"%s"' % q
        parts.append("> %s" % q)
        parts.append("")
    parts.append("## Hook")
    parts.append("")
    parts.append(chosen["Hook"])
    parts.append("")
    parts.append("## Nutshell")
    parts.append("")
    parts.append(nutshell)
    parts.append("")
    for name in ("Human", "Child", "Grandma", "Naya"):
        parts.append("## " + name)
        parts.append("")
        parts.append(chosen[name])
        parts.append("")
    parts.append("## What it means")
    parts.append("")
    for i, it in enumerate(means, 1):
        parts.append("%d. %s" % (i, it))
    parts.append("")
    parts.append("## Why it matters")
    parts.append("")
    for i, it in enumerate(matters, 1):
        parts.append("%d. %s" % (i, it))
    parts.append("")
    parts.append("## What changes now")
    parts.append("")
    for i, it in enumerate(changes, 1):
        parts.append("%d. %s" % (i, it))
    parts.append("")
    content = "\n".join(parts)

    # --- filing gate (SN-2237, mechanical) ---
    gates = []
    gates.append(("one piece of intelligence",
                  bool(title and topic and chosen["Nutshell"])))
    gates.append(("canonical shape (all 9 sections non-empty)",
                  all(chosen[s] for s in SECTIONS)))
    gates.append(("composed lists non-empty (means/matters/changes)",
                  bool(means and matters and changes)))
    child_sents = re.split(r"[.!?]\s+", chosen["Child"])
    child_avg = (sum(len(s.split()) for s in child_sents if s.strip())
                 / max(1, len([s for s in child_sents if s.strip()])))
    gates.append(("simplest words (Child avg %.1f words/sentence <= 30)"
                  % child_avg, child_avg <= 30))
    local_clash = glob.glob(os.path.join(
        os.path.expanduser(args.out_dir), "SN-%d-*.md" % sn))
    slug_clash = glob.glob(os.path.join(
        os.path.expanduser(args.out_dir), "SN-*-%s.md" % slug))
    gates.append(("no duplicate (SN-%d unused, slug unused)"
                  % sn, not local_clash and not slug_clash))
    gates.append(("changes the next decision (>= 1 action item)",
                  len(changes) >= 1))
    gates.append(("SN-%d not retired" % sn, sn not in RETIRED))
    failed = [name for name, ok in gates if not ok]
    print("Filing gate:")
    for name, ok in gates:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    if failed:
        print("MACHINE REFUSED: gate(s) failed: %s" % "; ".join(failed))
        return 1

    # --- write the local file ---
    out_dir = os.path.expanduser(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    local_path = os.path.join(out_dir, "SN-%d-%s.md" % (sn, slug))
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(content)
    size = os.path.getsize(local_path)
    print("WROTE: %s (%d B)" % (local_path, size))

    # --- lesson record (what the next brief consumes) ---
    lesson = {
        "sn": sn, "title": title, "slug": slug, "topic": topic,
        "sub_topic": sub, "l2": l2_topic, "date": date, "sources": [nt["sn"] for nt in notes],
        "source_count": n, "concepts": top_concepts[:5],
        "lesson": lesson_item, "lesson_lead": lesson_lead,
        "dest": dest, "local_path": local_path,
        "filed": False, "blob_sha": None, "receipt": None,
    }
    receipt_dir = os.path.expanduser(args.receipt) if args.receipt else HERE
    os.makedirs(receipt_dir, exist_ok=True)
    lesson_path = (os.path.expanduser(args.lesson_out) if args.lesson_out
                   else os.path.join(receipt_dir, "lesson-sn%d.json" % sn))

    if not args.file:
        lesson["filed"] = False
        with open(lesson_path, "w") as f:
            json.dump(lesson, f, indent=2)
        print("LESSON: %s (not filed — run with --file to file)" % lesson_path)
        print("DISTILLED (local only). Run with --file to file it.")
        return 0

    # --- dest-existence guard, then file via the file-machine ---
    try:
        if dest_exists(dest):
            print("MACHINE REFUSED: dest already exists: %s" % dest)
            return 1
    except Exception as exc:
        print("MACHINE REFUSED: %s" % exc)
        return 1
    receipt_path = os.path.join(receipt_dir, "receipt-sn%d.json" % sn)
    cmd = [sys.executable, FILE_MACHINE, "--file", local_path,
           "--dest", dest,
           "--message", "SN-%d %s — distilled %d notes to one (machine)"
           % (sn, title, n),
           "--receipt", receipt_path]
    print("FILING: %s" % " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    filed = proc.returncode == 0
    blob = None
    if os.path.isfile(receipt_path):
        try:
            receipt = json.load(open(receipt_path))
            filed = bool(receipt.get("verified"))
            blob = receipt.get("blob_sha")
        except ValueError:
            filed = False
    lesson["filed"] = filed
    lesson["blob_sha"] = blob
    lesson["receipt"] = receipt_path
    if not filed:
        # The file-machine's read-back is raw-only; a new path can 404
        # on the CDN for a minute after the PUT even though the file is
        # on main. Verify independently before concluding NOT FILED.
        print("File-machine did not verify — checking independently "
              "before concluding.")
        if independent_verify(dest, blob, local_path):
            filed = True
            lesson["filed"] = True
            lesson["verification"] = (
                "independent: API blob match + raw cb sha256 match; "
                "file-machine read-back failed on new-path CDN lag")
    with open(lesson_path, "w") as f:
        json.dump(lesson, f, indent=2)
    if not filed:
        print("NOT FILED: file-machine did not verify, and independent "
              "verification failed. Lesson kept at %s" % lesson_path)
        return 1
    print("FILED + VERIFIED: SN-%d (%s), blob %s" % (sn, dest, blob))
    print("LESSON: %s" % lesson_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
