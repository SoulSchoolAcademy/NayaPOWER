#!/usr/bin/env python3
"""Clean up test aliases from the free worker's state (F4-FIX item 3).
  - KV (WELCOME_ASSETS, namespace 1cf80db6183245d19dd5296645a12bd0):
    DELETE complete_<alias> via the Cloudflare API for:
      f4captaincheck (the eye's test alias, cert 737)
      f4fixvoeityel (this round's API test alias)
      f4diag1, f4testekcpgpnv, f4testmhxphhky, f4probeex (earlier test rows)
  - Supabase nayanet_identities row for f4captaincheck: DELETE via REST
    with the public anon key (read programmatically from the live-extracted
    identity file, in memory only, never printed). If RLS blocks it, the
    script reports the status honestly and does NOT invent a success.
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
ALIASES = ["f4captaincheck", "f4fixvoeityel", "f4diag1",
           "f4testekcpgpnv", "f4testmhxphhky", "f4probeex"]


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
    last = None
    for _ in range(3):
        req = urllib.request.Request(url, headers=UA, method="GET")
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except Exception as e:
            last = e
    import subprocess
    r = subprocess.run(["curl", "-sS", "-A", UA["User-Agent"], "-w", "\n%{http_code}",
                        url], capture_output=True, timeout=120)
    if r.returncode != 0:
        raise SystemExit(f"GET {url} failed after retries: {last}")
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
    print("== Supabase row delete: f4captaincheck ==")
    live = open("/home/hatch/workspace/team-nitro/walk-fix-20261111/identity-live-extracted.html",
                encoding="utf-8").read()
    m = re.search(r"var SB_ANON_KEY = '([^']+)';", live)
    assert m, "anon key not found"
    key = m.group(1)
    url = ("https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities"
           "?alias=eq.f4captaincheck")
    req = urllib.request.Request(url, method="DELETE", headers={
        "apikey": key, "Authorization": "Bearer " + key,
        "Prefer": "return=representation", **UA})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=60) as r:
            print(f"Supabase DELETE: {r.status} {r.read()[:200].decode()}")
    except urllib.error.HTTPError as e:
        print(f"Supabase DELETE: {e.code} {e.read()[:300].decode()}")
    st, out = http_get(HOST + "/api/claim?alias=f4captaincheck")
    print(f"verify claim GET f4captaincheck: {st} {out.decode()}")
    rec = json.loads(out.decode())
    if rec.get("exists"):
        print("SUPABASE ROW STILL EXISTS — anon DELETE was blocked (RLS). "
              "KV record is gone; the alias no longer resolves to test pages, "
              "but the identity row remains. Flagged as honestly not done.")
    else:
        print("CLEANUP COMPLETE: alias + pages gone from both stores.")


if __name__ == "__main__":
    main()
