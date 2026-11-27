# Real-tap probe of the staged Black Diamond phone v2 (Playwright Chromium
# via the localhost forwarder — VM browsers flap; Chromium is the proven
# engine for live reads). Loads ?walk=1, walks the 17 collapsed steps with
# real taps, checks D1-D7, screenshots both widths. Prints PASS/FAIL.
import json, re, sys
from playwright.sync_api import sync_playwright

BASE = "https://portal-phone-v2-staging.nayapower.workers.dev/?walk=1&name=Shawn&alias=shawn"
OUT = "/home/hatch/workspace/team-nitro/portal-phone-20261127/maker2/evidence/"
fails = []
def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (" " + str(extra) if extra else ""))
    if not ok:
        fails.append(name)

with sync_playwright() as pw:
    browser = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    page.goto(BASE, wait_until="networkidle", timeout=90000)
    page.wait_for_selector("#bdPhone", timeout=20000)
    check("phone visible at 390", page.is_visible("#bdPhone"))
    check("walk section visible (not hidden)", page.is_visible("#fpWalk"))
    q1 = page.text_content("#fpWalkQ")
    check("Q1 is Where do you live (one box)", "live" in q1.lower(), q1)
    check("progress 1 of 17", "1 of 17" in page.text_content("#fpWalkProgress"))
    check("Q1 has 3 fields in ONE box (country select + province + city)", page.locator('#bdFields select[data-fid="country"]').count() == 1 and page.locator('#bdFields input[data-fid="province"]').count() == 1 and page.locator('#bdFields input[data-fid="city"]').count() == 1)
    # D6: whole phone fits in 844, ENTER reachable on arrival
    box = page.locator("#bdPhone").bounding_box()
    enter_box = page.locator(".bd-enter-label").bounding_box()
    check("D6 phone bottom within 844 viewport", box is not None and box["y"] + box["height"] <= 844, box)
    check("D6 ENTER label visible on arrival (no scroll)", enter_box is not None and enter_box["y"] + enter_box["height"] <= 844, enter_box)
    check("screen is 9:16", abs(page.eval_on_selector(".bd-screen", "el => el.offsetWidth / el.offsetHeight") - 9/16) < 0.02)
    check("no Skip pill visible (NO SKIP)", not page.is_visible("#fpWalkSkip"))
    check("live clock ticking (h:mm)", bool(re.match(r"^\d{1,2}:\d{2}$", page.text_content("#bdClock").strip())), page.text_content("#bdClock"))
    check("5G in status bar", "5G" in page.text_content(".bd-statusbar"))
    batt = page.text_content("#bdBattNum").strip()
    check("battery shows a live 0-100 level", batt.isdigit() and 0 <= int(batt) <= 100, batt)
    check("ball is the Enter button", page.locator("#fpWalkEnter.bd-ball").count() == 1)
    check("SVG facet map on the jewel (D4)", page.locator(".bd-facets polygon").count() >= 10, page.locator(".bd-facets polygon").count())
    # Q1: fill the one box, ball reveals
    page.select_option('#bdFields select[data-fid="country"]', index=1)
    page.fill('#bdFields input[data-fid="province"]', "Ontario")
    page.fill('#bdFields input[data-fid="city"]', "Toronto")
    page.click("#fpWalkEnter")
    page.wait_for_selector("#bdReveal:not([hidden])", timeout=5000)
    check("Q1 ball reveals in place", page.is_visible("#bdReveal"))
    check("Q1 reveal shows all three fields", "Canada" in page.text_content("#bdRevealA") and "Toronto" in page.text_content("#bdRevealA"), page.text_content("#bdRevealA"))
    check("still Q1 after ball (ball never navigates)", "1 of 17" in page.text_content("#fpWalkProgress"))
    page.wait_for_timeout(600)
    page.screenshot(path=OUT + "v2-390-reveal-q1.png")
    page.click("#fpWalkNext")
    check("Next -> Q2 age+language", "language" in page.text_content("#fpWalkQ").lower(), page.text_content("#fpWalkQ"))
    page.select_option('#bdFields select[data-fid="age"]', index=3)
    page.fill('#bdFields input[data-fid="language"]', "English")
    page.click("#fpWalkEnter")
    check("Q2 reveal shows age group + language", "25" in page.text_content("#bdRevealA") and "English" in page.text_content("#bdRevealA"))
    page.click("#fpWalkNext")
    check("Next -> Q3 gender", "describe yourself" in page.text_content("#fpWalkQ").lower())
    check("D-gender: NO default (empty value)", page.eval_on_selector('#bdFields select[data-fid="gender"]', "el => el.value") == "")
    page.select_option('#bdFields select[data-fid="gender"]', "female")
    page.click("#fpWalkEnter")
    check("Q3 reveal shows Female", "Female" in page.text_content("#bdRevealA"))
    page.click("#fpWalkNext")
    check("Next -> Q4 favorites (three boxes)", "love" in page.text_content("#fpWalkQ").lower())
    check("Q4 has three field boxes", page.locator(".bd-field-box").count() == 3)
    page.fill('.bd-field-box[data-box="1"] input', "Naya")
    page.select_option('.bd-field-box[data-box="2"] select', "rock")
    page.fill('.bd-field-box[data-box="3"] input[data-fid="hobby"]', "Painting")
    page.fill('.bd-field-box[data-box="3"] input[data-fid="loveelse"]', "Sunsets")
    page.click("#fpWalkEnter")
    check("Q4 reveal shows brand + music + hobby + what else", all(x in page.text_content("#bdRevealA") for x in ["Naya", "Rock", "Painting", "Sunsets"]))
    page.click("#fpWalkNext")
    check("Next -> Q5 sports", "sports" in page.text_content("#fpWalkQ").lower())
    page.select_option('#bdFields select[data-fid="sport"]', "soccer")
    page.fill('#bdFields input[data-fid="team"]', "Maple Leafs")
    page.click("#fpWalkEnter")
    check("Q5 reveal shows sport type + team", "Soccer" in page.text_content("#bdRevealA") and "Maple Leafs" in page.text_content("#bdRevealA"))
    page.click("#fpWalkNext")
    check("Next -> Q6 connect (picture: Smart Match)", "connect" in page.text_content("#fpWalkQ").lower())
    check("Q6 picture shown (Smart Match)", page.is_visible("#bdPic") and page.eval_on_selector("#bdPicImg", "el => el.naturalWidth") > 0)
    page.select_option('#bdFields select[data-fid="connect"]', "people-like-me")
    page.fill('#bdFields input[data-fid="connectown"]', "Builders like me")
    page.click("#fpWalkEnter")
    check("Q6 reveal shows answer + our example", "People like me" in page.text_content("#bdRevealA") and "Our example" in page.text_content("#bdRevealEx"))
    check("Q6 reveal keeps the picture", page.is_visible("#bdRevealPic") and page.eval_on_selector("#bdRevealPicImg", "el => el.naturalWidth") > 0)
    page.click("#fpWalkNext")
    check("Next -> Q7 industry+skills check-off", "good at" in page.text_content("#fpWalkQ").lower())
    page.select_option('#bdFields select[data-fid="industry"]', "technology")
    page.locator(".bd-check", has_text="Video editing").click()
    page.locator(".bd-check", has_text="AI").click()
    page.wait_for_timeout(400)
    hl = page.eval_on_selector(".bd-check input:checked + span", "el => getComputedStyle(el).backgroundColor")
    check("checked chips highlight PURPLE (no gold)", hl == "rgb(142, 36, 170)", hl)
    page.click("#fpWalkEnter")
    check("Q7 reveal shows industry + skills", "Technology" in page.text_content("#bdRevealA") and "Video editing" in page.text_content("#bdRevealA") and "AI" in page.text_content("#bdRevealA"))
    page.click("#fpWalkNext")
    check("Next -> Q8 resume (experience/achievements/education)", "done" in page.text_content("#fpWalkQ").lower())
    page.fill('#bdFields input[data-fid="experience"]', "Built a world with my team")
    page.fill('#bdFields input[data-fid="achievements"]', "First 100 citizens")
    page.fill('#bdFields input[data-fid="education"]', "School of life")
    page.click("#fpWalkEnter")
    check("Q8 reveal shows resume", "Built a world" in page.text_content("#bdRevealA"))
    page.click("#fpWalkNext")
    check("Next -> Q9 the model", "world work" in page.text_content("#fpWalkQ").lower())
    page.fill("#fpWalkAnswer", "One tap and I am in.")
    page.click("#fpWalkEnter")
    check("Q9 reveal shows answer + our example", "One tap and I am in." in page.text_content("#bdRevealA") and "Our example" in page.text_content("#bdRevealEx"))
    page.click("#fpWalkNext")
    check("Next -> Q10 vision (picture: Nanoverse)", "vision" in page.text_content("#fpWalkQ").lower())
    check("Q10 picture shown (Nanoverse)", page.is_visible("#bdPic") and page.eval_on_selector("#bdPicImg", "el => el.naturalWidth") > 0)
    picbox = page.locator("#bdPicImg").bounding_box()
    check("EYE-4 picture renders full-frame in the 9:16 stage (tall, stage-wide)", picbox is not None and picbox["height"] >= 160 and picbox["width"] >= 300, picbox)
    page.fill("#fpWalkAnswer", "Everybody wins.")
    page.click("#fpWalkEnter")
    check("Q10 reveal shows answer + our example", "Everybody wins." in page.text_content("#bdRevealA") and "Our example" in page.text_content("#bdRevealEx"))
    page.wait_for_timeout(800)
    stbox = page.locator(".bd-stage").bounding_box()
    cardbox = page.locator(".bd-reveal-card").bounding_box()
    check("EYE-2 reveal card fits whole inside the 9:16 stage (no clipped example)", cardbox is not None and stbox is not None and cardbox["y"] >= stbox["y"] - 1 and cardbox["y"] + cardbox["height"] <= stbox["y"] + stbox["height"] + 1, (cardbox, stbox))
    page.wait_for_timeout(600)
    page.screenshot(path=OUT + "v2-390-reveal-vision.png")
    page.click("#fpWalkBack")
    check("Back -> Q9 model, answer kept", "world work" in page.text_content("#fpWalkQ").lower() and page.input_value("#fpWalkAnswer") == "One tap and I am in.")
    saved = page.evaluate("() => JSON.parse(localStorage.getItem('naya_welcome_right_v1') || '{}').answers || {}")
    check("answers save as you go (localStorage)", saved.get("country") == "Canada" and saved.get("city") == "Toronto" and saved.get("gender") == "Female" and saved.get("brand") == "Naya" and saved.get("sport") == "Soccer", json.dumps(saved)[:400])
    # Drive to the end: Next through the rest (fill text steps, leave fields blank)
    for n in range(9):
        q = page.text_content("#fpWalkQ")
        if page.locator("#fpWalkAnswer:visible").count():
            page.fill("#fpWalkAnswer", "Test answer " + str(n))
        if "into" in q.lower():
            page.locator(".bd-check", has_text="Music").first.click()
            page.wait_for_timeout(300)
            sub = page.locator(".bd-check", has_text="Playing").first
            if sub.count():
                sub.click()
        page.click("#fpWalkNext")
        page.wait_for_timeout(400)
    # complete() is a backend round-trip (POST + world verify) — wait for it
    # BEFORE judging whether the end screen arrived.
    try:
        page.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    except Exception:
        pass
    page.wait_for_timeout(1000)
    check("reached the end screen", page.is_visible("#fpWalkEnd"), page.text_content("#fpWalkProgress"))
    # D1: the ball is still there on the end screen
    check("D1 ball VISIBLE on the end screen", page.is_visible("#fpWalkEnter"))
    check("D1 ENTER label present, not dangling over empty carbon", page.is_visible(".bd-enter-label"))
    # D2: end screen fits — every destination button fully inside the 9:16 screen
    scr = page.locator(".bd-screen").bounding_box()
    allfit = True
    for bid in ["#fpWalkWorld", "#fpWalkPricing", "#fpWalkHub", "#fpWalkDash", "#fpWalkBiz", "#fpWalkSpace"]:
        b = page.locator(bid).bounding_box()
        if not b or b["y"] + b["height"] > scr["y"] + scr["height"] + 1 or b["y"] < scr["y"] - 1:
            allfit = False
            print("  button out of screen:", bid, b)
    check("D2 every end button whole inside the 9:16 screen", allfit)
    check("D2 Your space button fully visible", page.is_visible("#fpWalkSpace"))
    page.wait_for_timeout(600)
    page.screenshot(path=OUT + "v2-390-end.png")
    page.click("#fpWalkCopyAll")
    page.wait_for_timeout(300)
    check("Copy my answers flips to Copied", "Copied" in page.text_content("#fpWalkCopyAll"))
    real_errors = [e for e in errors if "ERR_CERT_AUTHORITY_INVALID" not in e and "fonts.googleapis.com" not in e]
    check("0 page errors at 390 (cert-artifact excluded, checker precedent)", len(real_errors) == 0, real_errors[:3])
    ctx.close()
    # ---- desktop 1440x900 ----
    ctx2 = browser.new_context(viewport={"width": 1440, "height": 900})
    page2 = ctx2.new_page()
    errors2 = []
    page2.on("pageerror", lambda e: errors2.append(str(e)))
    page2.on("console", lambda m: errors2.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    page2.goto(BASE, wait_until="networkidle", timeout=90000)
    page2.wait_for_selector("#bdPhone", timeout=20000)
    w = page2.eval_on_selector(".bd-phone", "el => el.offsetWidth")
    check("desktop phone width is viewport-capped at 900h (~365, XL at tall viewports)", 355 <= w <= 400, w)
    # EYE-1: phone must fit the 900 viewport at 1440 too (v1: 1,145 tall)
    dbox = page2.locator("#bdPhone").bounding_box()
    check("EYE-1 phone bottom within 900 viewport at 1440", dbox is not None and dbox["y"] + dbox["height"] <= 900, dbox)
    denter = page2.locator(".bd-enter-label").bounding_box()
    check("EYE-1 ball + ENTER reachable without scrolling at 1440", denter is not None and denter["y"] + denter["height"] <= 900, denter)
    check("desktop Q1 Where do you live (fresh state per context)", "live" in page2.text_content("#fpWalkQ").lower())
    page2.select_option('#bdFields select[data-fid="country"]', index=1)
    page2.fill('#bdFields input[data-fid="city"]', "Toronto")
    page2.click("#fpWalkEnter")
    page2.wait_for_selector("#bdReveal:not([hidden])", timeout=5000)
    check("desktop ball reveals", page2.is_visible("#bdReveal"))
    page2.wait_for_timeout(600)
    page2.screenshot(path=OUT + "v2-1440-reveal.png", full_page=False)
    # EYE-3 hunt: fast walk to complete at 1440 — the stray '<' error was seen at 1440
    # (17 clicks from Q1: 16 to reach Q17, the 17th completes)
    for n in range(17):
        if page2.locator("#fpWalkAnswer:visible").count():
            page2.fill("#fpWalkAnswer", "Test 1440 " + str(n))
        page2.click("#fpWalkNext")
        page2.wait_for_timeout(350)
    try:
        page2.wait_for_selector("#fpWalkEnd:not([hidden])", timeout=30000)
    except Exception:
        pass
    page2.wait_for_timeout(1000)
    check("1440 reached the end screen", page2.is_visible("#fpWalkEnd"))
    check("1440 ball visible on the end screen", page2.is_visible("#fpWalkEnter"))
    real_errors2 = [e for e in errors2 if "ERR_CERT_AUTHORITY_INVALID" not in e and "fonts.googleapis.com" not in e]
    check("0 page errors at 1440 (EYE-3: no stray Unexpected token)", len(real_errors2) == 0, real_errors2[:5])
    ctx2.close()
    browser.close()
print("PROBE DONE", "FAILURES: " + ", ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
