"""Browser recovery attempts via Playwright (python).
Each attempt: fresh profile dir, timeout, print exact result.
Usage: python3 pw_attempts.py [attempt]  -- attempt = A6|A7|A8|A9 ; default runs all.
"""
import os, sys, time, traceback
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser("~/.cache/ms-playwright")
FF = os.path.join(BASE, "firefox-1555/firefox/firefox")
CH = os.path.join(BASE, "chromium-1248/chrome-linux64/chrome")
HS = os.path.join(BASE, "chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell")

def prof(name):
    d = f"/tmp/pwprof-{name}"
    os.makedirs(d, exist_ok=True)
    return d

def run(name, fn):
    t0 = time.time()
    try:
        out = fn(None)
        print(f"[{name}] OK in {time.time()-t0:.1f}s: {out}", flush=True)
    except Exception as e:
        print(f"[{name}] FAIL in {time.time()-t0:.1f}s: {type(e).__name__}: {str(e)[:400]}", flush=True)

def a6(p):  # Playwright Firefox, default headless
    with sync_playwright() as pw:
        b = pw.firefox.launch(executable_path=FF, headless=True)
        pg = b.new_page()
        pg.goto("about:blank")
        pg.screenshot(path=f"/tmp/pw-a6.png")
        b.close()
        return "screenshot /tmp/pw-a6.png"

def a7(p):  # Playwright Firefox, Mozilla sandboxes off via env + prefs
    env = dict(os.environ)
    for k in ("MOZ_DISABLE_CONTENT_SANDBOX","MOZ_DISABLE_GMP_SANDBOX",
              "MOZ_DISABLE_SOCKET_PROCESS_SANDBOX","MOZ_DISABLE_GPU_SANDBOX",
              "MOZ_DISABLE_RDD_SANDBOX","MOZ_DISABLE_UTILITY_SANDBOX"):
        env[k] = "1"
    with sync_playwright() as pw:
        b = pw.firefox.launch(executable_path=FF, headless=True, env=env,
            firefox_user_prefs={"security.sandbox.content.level": 0,
                                "security.sandbox.gpu.level": 0})
        pg = b.new_page()
        pg.goto("about:blank")
        pg.screenshot(path=f"/tmp/pw-a7.png")
        b.close()
        return "screenshot /tmp/pw-a7.png"

def a8(p):  # Playwright Chromium, sandbox/shm/gpu flags
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CH, headless=True,
            args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu",
                  "--single-process","--no-zygote"])
        pg = b.new_page()
        pg.goto("about:blank")
        pg.screenshot(path=f"/tmp/pw-a8.png")
        b.close()
        return "screenshot /tmp/pw-a8.png"

def a9(p):  # Playwright Chromium headless shell
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=HS, headless=True,
            args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"])
        pg = b.new_page()
        pg.goto("about:blank")
        pg.screenshot(path=f"/tmp/pw-a9.png")
        b.close()
        return "screenshot /tmp/pw-a9.png"

ATTEMPTS = {"A6": a6, "A7": a7, "A8": a8, "A9": a9}
which = sys.argv[1:] or list(ATTEMPTS)
with sync_playwright() as _pw:  # keep driver warm; each attempt opens its own context
    pass
for name in which:
    run(name, ATTEMPTS[name])
print("DONE", flush=True)
