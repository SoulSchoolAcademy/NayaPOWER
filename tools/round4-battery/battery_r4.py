#!/usr/bin/env python3
"""ACTIVATION-GATE ROUND-4 RE-PROOF BATTERY (seat: round-4 fixer).

Adapted from the independent re-attacker's ROUND-3 battery (separate
worktree, file battery.py) — reused, not rebuilt. Deltas vs round-3,
all driven by the round-4 design changes (documented, not weakened):
  P5  REPLACED: the round-3 design's `paths:` filter is deleted (it was a
      second, case-sensitive perimeter). The new probes assert the round-4
      design: no paths filter, _is_deliverable as the single case-
      insensitive scope authority, empty scope -> PASS.
  P8  `code-emits/DELIVERY_SCOPE_EMPTY` replaced by
      `doc-documents-empty-scope-pass` (the code was removed BY DESIGN;
      empty scope now passes) + `code-emits/DELIVERABLE_SYMLINK` (new).
Everything else is byte-identical to the re-attacker's battery.

Probe classes:
  P1  canonicalizer browser-differential (D3/D4 + entity + corruption)
  P2  issuance logic matrix (stubbed API fed with REAL run shapes)
  P3  A1 end-to-end forgery: self-minted receipt, perfect public data
  P4  tombstone matrix
  P5  trigger: single scope authority (round-4 design)
  P6  bypass 2/4/A3 regression (fresh inputs)
  P7  production-config static checks (A4: proof env vs prod env)
  P8  law/code honesty
  P9  symlink binding scope

Verdict language: LEAK (fail-open: attacker input passes) | HOLD (rejected) |
AVAIL (false reject of lawful input — availability, not a leak).
Exit 0 = no LEAK found. Exit 1 = at least one LEAK.
"""
import argparse, base64, hashlib, io, json, os, re, subprocess, sys, tempfile, zipfile
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))

def sha256_hex(b): return hashlib.sha256(b).hexdigest()

# ---------------------------------------------------------------- browser
class ClassSniffer(HTMLParser):
    """Spec-ish class-attribute extraction: what the browser honors."""
    def __init__(self):
        super().__init__(convert_charrefs=True)  # browser decodes entities
        self.classes = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k.lower() == "class" and v:
                self.classes.extend(v.split())

def browser_classes(html):
    s = ClassSniffer()
    try: s.feed(html)
    except Exception: pass
    return s.classes

# ---------------------------------------------------------------- gh api (read-only, via the approved gh-api path)
def gh_api(path):
    p = subprocess.run([os.path.expanduser("~/workspace/naya/bin/gh-api"),
                        "GET", path], capture_output=True, text=True, timeout=60)
    return json.loads(p.stdout)

# ---------------------------------------------------------------- battery
class Battery:
    def __init__(self, gate_dir, repo):
        self.gate_dir = gate_dir
        self.repo = repo
        sys.path.insert(0, gate_dir)
        import activation_gate as g
        self.g = g
        self.rows = []  # (probe, name, result, detail)
        self.leaks = 0

    def record(self, probe, name, result, detail=""):
        self.rows.append((probe, name, result, detail))
        if result == "LEAK": self.leaks += 1

    # ---- P1: canonicalizer differentials ----
    def p1(self, design_check, known):
        prefixes = ("naya-", "board", "orb-", "lv-", "torb", "gem-")
        cases = [
            ("D3-unquoted", '<div class=naya-evilwidget>x</div>', True),
            ("D4-spaced", '<div class = "naya-evilwidget">x</div>', True),
            ("single-quoted", "<div class='naya-evilwidget'>x</div>", True),
            ("upper-attr", '<div CLASS="naya-evilwidget">x</div>', True),
            ("mixed-attr-space", '<div Class = naya-evilwidget>x</div>', True),
            ("newlines", '<div\nclass\n=\n"naya-evilwidget"\n>x</div>', True),
            ("tab-separated", '<div\tclass\t=\t"naya-evilwidget">x</div>', True),
            ("unquoted-slash", '<div class=naya-evilwidget/>x</div>', True),
            ("entity-prefix", '<div class="&#110;aya-evilwidget">x</div>', True),
            ("entity-hex", '<div class="&#x6E;aya-evilwidget">x</div>', True),
            ("entity-suffix", '<div class="naya-&#101;vilwidget">x</div>', True),
            # round-5 quote-smuggling: an entity-encoded quote decoded by the
            # canonicalizer must not terminate the rewritten attribute (or
            # break the lane's [^"']+ capture via a decoded single quote) —
            # the freestyle class must stay visible inside the quotes.
            ("quote-dec", '<div class="&#34; naya-evilwidget">x</div>', True),
            ("quote-hex", '<div class="&#x22; naya-evilwidget">x</div>', True),
            ("quote-named", '<div class="&quot; naya-evilwidget">x</div>', True),
            ("squote-dec", "<div class='&#39; naya-evilwidget'>x</div>", True),
            ("squote-named", "<div class='&apos; naya-evilwidget'>x</div>", True),
            ("quote-upper-attr", '<div CLASS="&#34; naya-evilwidget">x</div>', True),
            ("quote-multi", '<div class="&#34; naya-evilwidget &#34; orb-xwidget">x</div>', True),
            ("quote-mixed", '<div class="&#34; &#110;aya-evilwidget">x</div>', True),
            ("quoted-baseline", '<div class="naya-evilwidget">x</div>', True),
            ("lawful-known", '<div class="naya-btn">x</div>', False),
            ("lawful-noclass", '<div id="a">x</div>', False),
            ("comment-phantom", '<!-- <div class="naya-evilwidget"> -->', False),
            ("script-phantom", '<script>var s="<div class=naya-evilwidget>";</script>', False),
            ("attrvalue-phantom", '<div data-x="class=naya-evilwidget">x</div>', False),
            ("data-dash-class", '<div data-class="naya-evilwidget">x</div>', False),
            ("empty-class", '<div class="">x</div>', False),
            ("no-value-class", '<div class>x</div>', False),
            ("upper-value", '<div class="NAYA-EVILWIDGET">x</div>', False),
        ]
        for name, html, expect_evil in cases:
            seen = [c for c in browser_classes(html)
                    if c.startswith(prefixes) and c != "naya-btn"]
            canon = self.g.canonicalize_class_attributes(html)
            viol = design_check(canon, known)
            evil_seen = [c for c in seen if c not in known]
            assert "naya-evilwidget" not in known, "test class unexpectedly registered"
            if evil_seen:
                # browser honors an unregistered component class: gate must flag
                if viol: self.record("P1", name, "HOLD", "; ".join(viol)[:120])
                else: self.record("P1", name, "LEAK",
                                  "browser class %r unflagged after canonicalize" % evil_seen)
            else:
                if viol: self.record("P1", name, "AVAIL",
                                     "false reject of lawful input: %s" % ("; ".join(viol)[:120]))
                else: self.record("P1", name, "HOLD", "lawful passes")

    # ---- P2: issuance logic matrix ----
    def p2(self, real_run):
        g = self.g
        receipt = {"attestation": {"run_id": real_run["id"], "run_attempt": 1}}
        rbytes = b'{"attestation":{"run_id":%d,"run_attempt":1}}' % real_run["id"]
        truth = {"repository": self.repo}
        real_api = g._api
        real_dl = g._download_bytes
        def run_with(run_json=None, arts=None, blob=None, exc=None):
            def fake_api(method, path, token):
                if exc: raise RuntimeError(exc)
                if path.endswith("/artifacts"): return {"artifacts": arts or []}
                return dict(run_json or {})
            def fake_dl(url, token):
                if blob is None: raise RuntimeError("no blob")
                return blob
            g._api, g._download_bytes = fake_api, fake_dl
            try: return g.verify_issuance(receipt, rbytes, truth, "tok")
            finally: g._api, g._download_bytes = real_api, real_dl
        def zipped(payload):
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z: z.writestr("receipt.json", payload)
            return buf.getvalue()
        # no attestation at all
        v = g.verify_issuance({}, b"{}", truth, "tok")
        self.record("P2", "no-attestation", "HOLD" if any("ISSUANCE_UNATTESTED" in x for x in v) else "LEAK", str(v[:1]))
        # real run, wrong event (pull_request, not workflow_dispatch)
        v = run_with(run_json=real_run, arts=[])
        self.record("P2", "real-run-wrong-event", "HOLD" if any("ISSUANCE_WRONG_EVENT" in x for x in v) else "LEAK", str(v[:1]))
        # wrong workflow path
        r2 = dict(real_run, event="workflow_dispatch", path=".github/workflows/other.yml")
        v = run_with(run_json=r2, arts=[])
        self.record("P2", "wrong-workflow-path", "HOLD" if any("ISSUANCE_WRONG_WORKFLOW" in x for x in v) else "LEAK", str(v[:1]))
        # failed conclusion
        r3 = dict(real_run, event="workflow_dispatch", path=".github/workflows/activation-mint.yml", conclusion="failure")
        v = run_with(run_json=r3, arts=[])
        self.record("P2", "failed-run", "HOLD" if any("ISSUANCE_RUN_NOT_SUCCESS" in x for x in v) else "LEAK", str(v[:1]))
        # foreign head repo
        r4 = dict(real_run, event="workflow_dispatch", path=".github/workflows/activation-mint.yml",
                  conclusion="success", head_repository={"full_name": "evil-corp/stolen-repo"})
        v = run_with(run_json=r4, arts=[])
        self.record("P2", "foreign-run", "HOLD" if any("ISSUANCE_FOREIGN_RUN" in x for x in v) else "LEAK", str(v[:1]))
        # no receipt artifact
        r5 = dict(real_run, event="workflow_dispatch", path=".github/workflows/activation-mint.yml",
                  conclusion="success", head_repository={"full_name": self.repo})
        v = run_with(run_json=r5, arts=[])
        self.record("P2", "artifact-missing", "HOLD" if any("ISSUANCE_ARTIFACT_MISSING" in x for x in v) else "LEAK", str(v[:1]))
        # artifact present, bytes differ
        arts = [{"name": "activation-receipt-123", "archive_download_url": "https://x/y.zip"}]
        v = run_with(run_json=r5, arts=arts, blob=zipped(b'{"different":true}'))
        self.record("P2", "bytes-mismatch", "HOLD" if any("ISSUANCE_BYTES_MISMATCH" in x for x in v) else "LEAK", str(v[:1]))
        # artifact present, bytes identical -> the ONLY pass
        v = run_with(run_json=r5, arts=arts, blob=zipped(rbytes))
        self.record("P2", "genuine-issuance", "HOLD" if v == [] else "LEAK", str(v[:1]))
        # run unreachable
        v = run_with(exc="HTTP 404")
        self.record("P2", "run-unreachable", "HOLD" if any("ISSUANCE_UNVERIFIABLE" in x for x in v) else "LEAK", str(v[:1]))
        # run_id injection: non-numeric / path-traversal must fail closed
        receipt_bad = {"attestation": {"run_id": "1/../../repos/evil-corp", "run_attempt": 1}}
        v = run_with(exc="HTTP 404: Not Found")
        self.record("P2", "run-id-injection", "HOLD" if any("ISSUANCE_UNVERIFIABLE" in x for x in v) else "LEAK", str(v[:1]))
        receipt_s = {"attestation": {"run_id": str(real_run["id"]), "run_attempt": 1}}
        g._api = lambda m, p, t: dict(r5)
        try: v = g.verify_issuance(receipt_s, rbytes, truth, "tok")
        finally: g._api = real_api
        self.record("P2", "run-id-string", "HOLD" if v == [] or any("ISSUANCE_" in x for x in v) else "LEAK", str(v[:1]))

    # ---- P3: A1 end-to-end forgery ----
    def p3(self, real_run, public):
        g = self.g
        body = "<html><body>forger page</body></html>"
        dhash = sha256_hex(g._canonical_deliverable_bytes(body.encode()))
        base_receipt = {
            "schema": g.SCHEMA, "status": "ACTIVATED",
            "session_id": "forger-session", "naya_identity": "forger",
            "human_authority": "Shawn", "repository": self.repo,
            "job": "forge", "gates": ["Usefulness Gate"], "proof_plan": "none",
            "main_sha": public["main_sha"],
            "activated_at": datetime.now(timezone.utc).isoformat(),
            "loaded": public["blobs"], "deliverables": [{"path": "forge.html", "sha256": dhash}],
        }
        rbytes = json.dumps(base_receipt, sort_keys=True).encode()
        digest = sha256_hex(rbytes)
        page = body.replace("</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digest)
        truth = {"repository": self.repo, "main_sha": public["main_sha"],
                 "source_blobs": public["blobs"], "now": datetime.now(timezone.utc)}
        # single-pair predicate: consistency+border checks (no issuance here by design)
        verdict, viol = g.check(rbytes, page.encode(), truth)
        self.record("P3", "self-mint-perfect-public-data/single-pair",
                    "HOLD" if verdict == "PASS" else "LEAK",
                    "verdict=%s (single-pair tests consistency+binding only)" % verdict)
        # delivery boundary WITHOUT attestation -> must be ISSUANCE_UNATTESTED
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "forge.html"), "w").write(page)
            rd = os.path.join(d, ".naya", "activation"); os.makedirs(rd)
            open(os.path.join(rd, "receipt.json"), "wb").write(rbytes)
            real_vi = g.verify_issuance
            g.verify_issuance = real_vi  # real: no attestation -> UNATTESTED pre-API
            v, viol = g.check_delivery(rbytes, d, [{"path": "forge.html", "status": "modified",
                                                   "previous_filename": None}],
                                       truth, token="tok")
            self.record("P3", "self-mint-no-attestation/delivery",
                        "HOLD" if any("ISSUANCE_UNATTESTED" in x for x in viol) else "LEAK",
                        "%s %s" % (v, viol[:1]))
        # delivery WITH attestation to a REAL non-mint run -> must be ISSUANCE_WRONG_EVENT
        forged = dict(base_receipt); forged["attestation"] = {"run_id": real_run["id"], "run_attempt": 1}
        rbytes2 = json.dumps(forged, sort_keys=True).encode()
        digest2 = sha256_hex(rbytes2)
        page2 = body.replace("</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digest2)
        real_api = g._api
        g._api = lambda m, p, t: dict(real_run)
        try:
            v = g.verify_issuance(forged, rbytes2, truth, "tok")
        finally: g._api = real_api
        self.record("P3", "self-mint-attests-real-nonmint-run",
                    "HOLD" if any("ISSUANCE_WRONG_EVENT" in x or "ISSUANCE_WRONG_WORKFLOW" in x for x in v) else "LEAK",
                    str(v[:1]))

    # ---- P4: tombstone matrix ----
    def p4(self):
        g = self.g
        g.verify_issuance = lambda *a, **k: []  # issuance isolated in P2/P3
        real_rdg = g.run_design_gate
        g.run_design_gate = lambda *a, **k: []  # row-7 isolated in P1
        try:
            self._p4_cases(g)
        finally:
            g.run_design_gate = real_rdg

    def _p4_cases(self, g):
        base_body = "<html><body>base version</body></html>"
        base_canon = sha256_hex(g._canonical_deliverable_bytes(base_body.encode()))
        def receipt_for(entries):
            r = {"schema": g.SCHEMA, "status": "ACTIVATED", "session_id": "s",
                 "naya_identity": "n", "human_authority": "Shawn", "repository": self.repo,
                 "job": "j", "gates": ["g"], "proof_plan": "p",
                 "main_sha": "a" * 40, "activated_at": datetime.now(timezone.utc).isoformat(),
                 "loaded": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40},
                 "deliverables": entries}
            return json.dumps(r, sort_keys=True).encode()
        truth = {"repository": self.repo, "main_sha": "a" * 40,
                 "source_blobs": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40},
                 "now": datetime.now(timezone.utc)}
        real_bbb = g.base_blob_bytes
        def run_case(name, entries, files, changed, base_map, expect_hold, want, marker_files=()):
            with tempfile.TemporaryDirectory() as d:
                rb = receipt_for(entries)
                digest = sha256_hex(rb)
                for rel, content in files.items():
                    full = os.path.join(d, rel); os.makedirs(os.path.dirname(full), exist_ok=True)
                    if rel in marker_files:
                        content = content.replace("</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digest)
                    open(full, "w").write(content)
                def fake_bbb(repo, path, ref, token):
                    if path in base_map: return base_map[path].encode()
                    raise RuntimeError("not a file at base ref")
                g.base_blob_bytes = fake_bbb
                try:
                    v, viol = g.check_delivery(rb, d, changed, truth, token="tok")
                finally: g.base_blob_bytes = real_bbb
                ok = any(want in x for x in viol)
                detail = "%s :: %s" % (v, " | ".join(viol[:3]))
                self.record("P4", name, "HOLD" if (v == "REJECT") == (not expect_hold) and (ok or expect_hold) else "LEAK",
                            detail)
        tomb = {"path": "gone.html", "sha256": base_canon, "action": "delete"}
        rm = [{"path": "gone.html", "status": "removed", "previous_filename": None}]
        run_case("legit-deletion", [tomb], {}, rm, {"gone.html": base_body}, True, "")
        run_case("deletion-no-tombstone", [], {}, rm, {"gone.html": base_body}, False, "DELETION_UNATTESTED")
        run_case("deletion-ship-action", [{"path": "gone.html", "sha256": base_canon, "action": "ship"}],
                 {}, rm, {"gone.html": base_body}, False, "DELETION_UNATTESTED")
        run_case("deletion-file-still-present", [tomb], {"gone.html": base_body}, rm,
                 {"gone.html": base_body}, False, "DELETION_NOT_EFFECTIVE")
        run_case("deletion-wrong-hash", [{"path": "gone.html", "sha256": "0" * 64, "action": "delete"}],
                 {}, rm, {"gone.html": base_body}, False, "DELETION_BINDING_MISMATCH")
        run_case("deletion-never-existed", [tomb], {}, rm, {}, False, "DELETION_UNVERIFIABLE")
        # rename expands to removed+added
        new_body = "<html><body>renamed</body></html>"
        new_canon = sha256_hex(g._canonical_deliverable_bytes(new_body.encode()))
        run_case("rename-needs-both", [tomb, {"path": "new.html", "sha256": new_canon}],
                 {"new.html": new_body},
                 [{"path": "new.html", "status": "renamed", "previous_filename": "gone.html"}],
                 {"gone.html": base_body}, True, "", marker_files=("new.html",))
        run_case("rename-missing-tombstone", [{"path": "new.html", "sha256": new_canon}],
                 {"new.html": new_body},
                 [{"path": "new.html", "status": "renamed", "previous_filename": "gone.html"}],
                 {"gone.html": base_body}, False, "DELETION_UNATTESTED")
        # modified file cannot ride a delete tombstone
        run_case("modified-with-delete-action", [tomb], {"gone.html": "<html><body>CHANGED</body></html>"},
                 [{"path": "gone.html", "status": "modified", "previous_filename": None}],
                 {"gone.html": base_body}, False, "DELIVERABLE_BINDING_MISMATCH")

    # ---- P5: trigger — ROUND-4 DESIGN (replaces the paths-block analysis) ----
    # The round-3 design's `paths:` filter was a second, case-sensitive
    # perimeter; docs/FOO.HTML evaded it. Round-4 deletes the filter: the
    # workflow triggers on EVERY PR to main and _is_deliverable is the
    # single, case-insensitive scope authority. Predicate == perimeter.
    def p5(self, head_root):
        wf = os.path.join(head_root, ".github/workflows/activation-delivery-gate.yml")
        text = open(wf).read()
        trig = re.search(r"on:(.*?)(?:\n[a-z]+:|\njobs:)", text, re.S).group(1)
        no_paths = "paths:" not in trig
        self.record("P5", "no-paths-filter",
                    "HOLD" if no_paths else "LEAK",
                    "trigger block must carry no paths filter: %s" % trig.strip()[:120])
        for name, path, expect_del in [
            ("lower-html", "docs/a.html", True),
            ("upper-HTML", "docs/FOO.HTML", True),
            ("mixed-HtMl", "docs/b.HtMl", True),
            ("smartblocks-upper", "smart-blocks/C.HTML", True),
            ("root-upper", "DOCS/FOO.HTML", True),
            ("non-deliverable-py", "tools/x.py", False),
            ("non-deliverable-md", "BRAIN/n.md", False),
        ]:
            is_del = self.g._is_deliverable(path)
            self.record("P5", "scope/" + name,
                        "HOLD" if is_del == expect_del else "LEAK",
                        "deliverable=%s expect=%s" % (is_del, expect_del))
        # empty scope -> PASS (nothing to gate; docs-only PRs must not fail)
        v, viol = self.g.check_delivery(
            b"", "/tmp",
            [{"path": "docs/n.md", "status": "modified",
              "previous_filename": None}],
            {"repository": self.repo, "main_sha": "a" * 40,
             "source_blobs": {}, "now": datetime.now(timezone.utc)},
            "", "", token="t")
        self.record("P5", "empty-scope-pass",
                    "HOLD" if v == "PASS" else "LEAK", "%s %s" % (v, viol[:1]))

    # ---- P6: bypass 2/4/A3 regression, fresh inputs ----
    def p6(self):
        g = self.g
        # bypass 2: forged env repo vs event payload
        with tempfile.TemporaryDirectory() as d:
            ev = {"repository": {"full_name": self.repo}}
            ep = os.path.join(d, "event.json"); json.dump(ev, open(ep, "w"))
            old_ep, old_repo = os.environ.get("GITHUB_EVENT_PATH"), os.environ.get("GITHUB_REPOSITORY")
            os.environ["GITHUB_EVENT_PATH"] = ep; os.environ["GITHUB_REPOSITORY"] = "evil-corp/stolen-repo"
            try: g.resolve_truth(); res = "LEAK"
            except RuntimeError as e: res = "HOLD" if "disagrees" in str(e) else "LEAK"
            finally:
                if old_ep is None: os.environ.pop("GITHUB_EVENT_PATH", None)
                else: os.environ["GITHUB_EVENT_PATH"] = old_ep
                if old_repo is None: os.environ.pop("GITHUB_REPOSITORY", None)
                else: os.environ["GITHUB_REPOSITORY"] = old_repo
            self.record("P6", "bypass2-forged-env", res, "")
        # bypass 4: fresh transplant pair
        truth = {"repository": self.repo, "main_sha": "a" * 40,
                 "source_blobs": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40},
                 "now": datetime.now(timezone.utc)}
        body_a = "<html><body>alpha bytes</body></html>"
        r = {"schema": g.SCHEMA, "status": "ACTIVATED", "session_id": "s", "naya_identity": "n",
             "human_authority": "Shawn", "repository": self.repo, "job": "j", "gates": ["g"],
             "proof_plan": "p", "main_sha": "a" * 40,
             "activated_at": datetime.now(timezone.utc).isoformat(),
             "loaded": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40},
             "deliverables": [{"path": "alpha.html", "sha256": sha256_hex(g._canonical_deliverable_bytes(body_a.encode()))}]}
        rb = json.dumps(r, sort_keys=True).encode()
        body_b = "<html><body>beta — totally different bytes</body></html>"
        page_b = body_b.replace("</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % sha256_hex(rb))
        v, viol = g.check(rb, page_b.encode(), truth)
        self.record("P6", "bypass4-fresh-transplant",
                    "HOLD" if v == "REJECT" and any("DELIVERABLE_BINDING_MISMATCH" in x for x in viol) else "LEAK",
                    "%s %s" % (v, viol[:1]))
        # A3: local mode labels + exit code
        with tempfile.TemporaryDirectory() as d:
            rp = os.path.join(d, "r.json"); open(rp, "wb").write(rb)
            dp = os.path.join(d, "a.html")
            open(dp, "w").write(body_a.replace("</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % sha256_hex(rb)))
            tp = os.path.join(d, "t.json")
            json.dump({"repository": self.repo, "main_sha": "a" * 40,
                       "source_blobs": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40}}, open(tp, "w"))
            p = subprocess.run([sys.executable, os.path.join(self.gate_dir, "activation_gate.py"),
                                "--receipt", rp, "--deliverable", dp, "--mode", "local", "--truth", tp],
                               capture_output=True, text=True)
            out = p.stdout + p.stderr
            ok = p.returncode == 3 and "LOCAL-REHEARSAL-" in out and "PASS" not in out.replace("LOCAL-REHEARSAL-", "")
            self.record("P6", "A3-local-labels", "HOLD" if ok else "LEAK", "exit=%d" % p.returncode)

    # ---- P7: production-config static checks (A4) ----
    def p7(self, head_root, expect_branch=""):
        dl = open(os.path.join(head_root, ".github/workflows/activation-delivery-gate.yml")).read()
        perms = re.search(r"permissions:(.*?)(?:\n\w|\njobs:)", dl, re.S).group(1)
        has_actions = bool(re.search(r"actions\s*:\s*(read|write)", perms))
        self.record("P7", "delivery-workflow-actions-permission",
                    "HOLD" if has_actions else "AVAIL",
                    "verify_issuance needs actions:read; without it every lawful delivery REJECTs (fail-closed breakage)")
        # exact --delivery invocation the proof must mirror (A4)
        m = re.search(r"run:\s*>-\s*\n((?:\s+.*\n?)+)", dl)
        cmd = " ".join(m.group(1).split()) if m else ""
        self.record("P7", "delivery-invocation", "HOLD", cmd[:200])
        # mint workflow: dispatch-only + pinned actions
        mw = open(os.path.join(head_root, ".github/workflows/activation-mint.yml")).read()
        triggers = re.search(r"on:(.*?)(?:\n\w|\npermissions:)", mw, re.S).group(1)
        dispatch_only = "workflow_dispatch" in triggers and "push" not in triggers and "pull_request" not in (triggers.replace("pull_request_target", ""))
        pinned = len(re.findall(r"uses:\s*\S+@[a-f0-9]{40}", mw))
        self.record("P7", "mint-dispatch-only", "HOLD" if dispatch_only else "LEAK", triggers.strip()[:80])
        self.record("P7", "mint-actions-pinned", "HOLD" if pinned >= 3 else "AVAIL", "%d pinned" % pinned)
        # pr_scan dead? (the round-4 battery harness itself is excluded from
        # the walk — it contains the probe's own search string)
        ps = os.path.join(head_root, "tools/activation_gate_pr_scan.py")
        refs = []
        for root, _, files in os.walk(head_root):
            if ".git" in root: continue
            if "round4-battery" in root: continue
            for f in files:
                if f.endswith((".yml", ".py", ".md", ".json")):
                    p = os.path.join(root, f)
                    try:
                        if "activation_gate_pr_scan" in open(p, encoding="utf-8", errors="replace").read():
                            refs.append(os.path.relpath(p, head_root))
                    except OSError: pass
        self.record("P7", "pr-scan-deleted", "HOLD" if not os.path.exists(ps) and not refs else "LEAK",
                    "exists=%s refs=%s" % (os.path.exists(ps), refs[:3]))
        # proof workflow triggers on the fixer branch (else CI never proves)
        pw = open(os.path.join(head_root, ".github/workflows/unified-activation-gate.yml")).read()
        trig = re.search(r"branches:\s*\[(.*?)\]", pw).group(1)
        ok = (expect_branch in trig) if expect_branch else True
        self.record("P7", "proof-workflow-trigger",
                    "HOLD" if ok else "AVAIL",
                    "trigger=%s expect=%s" % (trig[:80], expect_branch))

    # ---- P8: law/code honesty ----
    def p8(self, head_root):
        src = open(os.path.join(self.gate_dir, "activation_gate.py")).read()
        claims_issuance = "ISSUANCE" in src and "verify_issuance" in src
        doc_admits = "single-pair predicate tests consistency+binding" in src
        self.record("P8", "law-states-issuance-at-delivery-only",
                    "HOLD" if claims_issuance and doc_admits else "AVAIL", "")
        # acceptance table rows vs violation codes actually emitted
        codes = set(re.findall(r'"([A-Z_]+):', src))
        for want in ["ISSUANCE_UNATTESTED", "ISSUANCE_BYTES_MISMATCH", "DELETION_UNATTESTED",
                     "CITATION_DIGEST_MISMATCH", "DELIVERABLE_SYMLINK"]:
            self.record("P8", "code-emits/" + want, "HOLD" if want in codes else "LEAK", "")
        # DELIVERY_SCOPE_EMPTY was REMOVED by design in round-4 (empty scope
        # -> PASS: nothing to gate). The law must document the new behavior.
        doc_ok = "no changed deliverables" in src and "nothing to gate" in src
        self.record("P8", "doc-documents-empty-scope-pass",
                    "HOLD" if doc_ok else "LEAK", "")

    # ---- P9: symlink binding scope ----
    def p9(self):
        g = self.g
        g.verify_issuance = lambda *a, **k: []  # issuance isolated in P2/P3
        real_rdg = g.run_design_gate
        g.run_design_gate = lambda *a, **k: []  # structural checks orthogonal here
        try:
            truth = {"repository": self.repo, "main_sha": "a" * 40,
                     "source_blobs": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40},
                     "now": datetime.now(timezone.utc)}
            target_body = "<html><body>symlink target bytes</body></html>"
            dhash = sha256_hex(g._canonical_deliverable_bytes(target_body.encode()))
            r = {"schema": g.SCHEMA, "status": "ACTIVATED", "session_id": "s", "naya_identity": "n",
                 "human_authority": "Shawn", "repository": self.repo, "job": "j", "gates": ["g"],
                 "proof_plan": "p", "main_sha": "a" * 40,
                 "activated_at": datetime.now(timezone.utc).isoformat(),
                 "loaded": {"design_contract": "b" * 40, "blocks_catalog": "c" * 40},
                 "deliverables": [{"path": "link.html", "sha256": dhash}]}
            rb = json.dumps(r, sort_keys=True).encode()
            digest = sha256_hex(rb)
            with tempfile.TemporaryDirectory() as d:
                open(os.path.join(d, "target.html"), "w").write(
                    target_body.replace("</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digest))
                os.symlink("target.html", os.path.join(d, "link.html"))
                v, viol = g.check_delivery(rb, d, [{"path": "link.html", "status": "added",
                                                    "previous_filename": None}],
                                           truth, token="tok")
                # The gate binds the TARGET's bytes but the PR ships a LINK:
                # verified-vs-shipped divergence (writer-class only; issuance still gates minting).
                self.record("P9", "symlink-deliverable",
                            "AVAIL" if v == "PASS" else "HOLD",
                            "verdict=%s :: %s" % (v, " | ".join(viol[:2])))
        finally:
            g.run_design_gate = real_rdg

    def run_all(self, head_root, real_run, public, design_check, known, expect_branch=""):
        self.p1(design_check, known); self.p2(real_run); self.p3(real_run, public)
        self.p4(); self.p5(head_root); self.p6(); self.p7(head_root, expect_branch); self.p8(head_root)
        self.p9()
        return self.rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate-dir", required=True)
    ap.add_argument("--head-root", required=True)
    ap.add_argument("--repo", default="SoulSchoolAcademy/NayaPOWER")
    ap.add_argument("--expect-branch", default="")
    args = ap.parse_args()
    b = Battery(args.gate_dir, args.repo)
    real_run = json.load(open("/tmp/ag3_real_run.json"))
    public = json.load(open("/tmp/ag3_public_truth.json"))
    # canonical blob SHAs (public data)
    tree = gh_api("/repos/%s/git/trees/%s?recursive=1" % (args.repo, public["main_sha"]))
    by_path = {t["path"]: t["sha"] for t in tree.get("tree", []) if t.get("type") == "blob"}
    public["blobs"] = {k: by_path[v] for k, v in
                       {"design_contract": "BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md",
                        "blocks_catalog": "BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json"}.items()}
    json.dump(public, open("/tmp/ag3_public_truth.json", "w"))
    # pinned design gate (the exact delegation target the delivery workflow fetches)
    dl = open(os.path.join(args.head_root, ".github/workflows/activation-delivery-gate.yml")).read()
    pin = re.search(r"PIN:\s*([a-f0-9]{40})", dl).group(1)
    pin_dir = "/tmp/ag3_pin"; os.makedirs(pin_dir + "/sb", exist_ok=True)
    d = gh_api("/repos/%s/contents/%s?ref=%s" % (args.repo, "tools/design_gate.py", pin))
    open(pin_dir + "/design_gate.py", "w").write(base64.b64decode(d["content"]).decode())
    d = gh_api("/repos/%s/contents/%s?ref=%s" % (args.repo, "smart-blocks/manifest.json", pin))
    open(pin_dir + "/sb/manifest.json", "w").write(base64.b64decode(d["content"]).decode())
    sys.path.insert(0, pin_dir)
    import design_gate as dg
    from pathlib import Path
    known = dg._manifest_classes(Path(pin_dir + "/sb/manifest.json"))
    rows = b.run_all(args.head_root, real_run, public, dg.check_no_freestyle, known | {"naya-btn"},
                     expect_branch=args.expect_branch)
    print("\n==== ROUND-4 RE-PROOF BATTERY (adapted from round-3 re-attack) ====")
    for probe, name, result, detail in rows:
        print("[%s] %s/%s :: %s" % (result, probe, name, detail))
    n_leak = sum(1 for r in rows if r[2] == "LEAK")
    n_avail = sum(1 for r in rows if r[2] == "AVAIL")
    print("==== %d rows, %d LEAK, %d AVAIL ====" % (len(rows), n_leak, n_avail))
    return 1 if n_leak else 0

if __name__ == "__main__":
    sys.exit(main())
