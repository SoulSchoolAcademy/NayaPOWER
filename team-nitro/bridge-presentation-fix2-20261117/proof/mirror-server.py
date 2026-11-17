#!/usr/bin/env python3
"""Mirror server for /tmp/fix2/mirror with correct content types for
extensionless routes (/agreement, /welcome -> text/html)."""
import http.server, mimetypes, os, sys

ROOT = "/tmp/fix2/mirror"
OVERRIDES = {"/agreement": ("agreement", "text/html; charset=utf-8"),
             "/welcome": ("welcome", "text/html; charset=utf-8"),
             "/identity.html": ("identity.html", "text/html; charset=utf-8")}

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        if path in OVERRIDES:
            fn, ctype = OVERRIDES[path]
            fp = os.path.join(ROOT, fn)
            data = open(fp, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", 8899), H).serve_forever()
