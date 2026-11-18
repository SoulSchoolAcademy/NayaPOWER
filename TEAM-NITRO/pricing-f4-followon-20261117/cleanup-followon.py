#!/usr/bin/env python3
"""Clean up F4-FOLLOWON test aliases from the free worker's state.
  - KV (WELCOME_ASSETS, namespace 1cf80db6183245d19dd5296645a12bd0):
    DELETE complete_<alias> for the three test aliases used this round:
      f4followonpywcejrz (build run claim, cert 740 — no completion posted)
      f4followonanhpytt  (harness alias A, cert 741 — walk completed)
      f4followonbyekytr  (harness alias B, cert 742 — claimed only)
  - Supabase nayanet_identities rows: DELETE via REST with the public anon
    key (read programmatically from the live-extracted identity file, in
    memory only, never printed). The F4 round proved RLS blocks this (200
    with []); if blocked again the script reports it honestly and does NOT
    invent a success. The rows then need a keyed delete or Shawn's hand.
Verifies after each delete with a read (KV GET / claim GET).
"""
import json
import re
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
NS = "1cf80db6183245d19dd5296645a12bd0"
CF = "https://api.cloudflare.com/client/v4"
HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
ALIASES = ["f4followonpywcejrz", "f4followonanhpytt", "f4followonbyekytr",
           "f4followonazhqggl", "f4followonbuxubaf"]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused")


def cf(method, path, body=None):
    req = urllib.request.Request(CF + path, method=method, data=body)
    add_surrogate_to_request(req, "custom.cloudflare",
                             allowed_hosts=["api.cloudflare.com"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def http_get(url):
    # curl to stdout (no disk): urllib drops chunked workers.dev transfers.
    import subprocess
    r = subprocess.run(["curl", "-sS", "-A", UA["User-Agent"], "-w", "\n%{http_code}",
                        url], capture_output=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit(f"GET {url} failed: curl rc={r.returncode}")
    *body, code = r.stdout.decode("utf-8", "replace").rsplit("\n", 1)
    return int(code), "\n".join(body).encode()


def main():
    print("== KV deletes ==")
    for a in ALIASES:
        key = "complete_" + a
        st, _ = cf("DELETE", f"/accounts/{ACCT}/storage/kv/namespaces/{NS}/values/{key}")
        st2, out2 = http_get(HOST + f"/api/welcome/complete?alias={a}")
        print(f"KV {key}: DELETE {st}; verify GET complete: {st2} {out2[:80].decode()}")
        assert st in (200, 404), f"KV delete failed for {key}: {st}"
        assert st2 == 404, f"KV record {key} still reads back — STOP"
    print("== Supabase row deletes (anon key; expect RLS block) ==")
    live = open("/home/hatch/workspace/team-nitro/walk-fix-20261111/identity-live-extracted.html",
                encoding="utf-8").read()
    m = re.search(r"var SB_ANON_KEY = '([^']+)';", live)
    assert m, "anon key not found"
    key = m.group(1)
    for a in ALIASES:
        url = ("https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities"
               "?alias=eq." + a)
        req = urllib.request.Request(url, method="DELETE", headers={
            "apikey": key, "Authorization": "Bearer " + key,
            "Prefer": "return=representation", **UA})
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as r:
                print(f"Supabase DELETE {a}: {r.status} {r.read()[:200].decode()}")
        except urllib.error.HTTPError as e:
            print(f"Supabase DELETE {a}: {e.code} {e.read()[:300].decode()}")
        st, out = http_get(HOST + f"/api/claim?alias={a}")
        print(f"  verify claim GET {a}: {st} {out.decode()}")
        rec = json.loads(out.decode())
        if rec.get("exists"):
            print(f"  ROW STILL EXISTS ({a}, cert {rec.get('cert_no')}) — anon DELETE "
                  "blocked (RLS). Needs a keyed delete or Shawn's hand.")
        else:
            print(f"  CLEAN: {a} gone from both stores.")


if __name__ == "__main__":
    main()
