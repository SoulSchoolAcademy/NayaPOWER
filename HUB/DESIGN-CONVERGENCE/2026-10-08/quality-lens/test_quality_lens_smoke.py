"""Optional headless browser evidence smoke; run with Playwright installed.
Not a production quality certificate, and not imported into existing CI gates.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = Path(__file__).with_name("index.html").read_text(encoding="utf8")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for width in (1440, 1024, 768, 390, 320):
        context = b.new_context(viewport={"width": width, "height": 900}, accept_downloads=True)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.set_content(html, wait_until="load")
        assert not errors, errors
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
        assert page.evaluate("getComputedStyle(document.body).fontSize") == "18px"
        assert page.evaluate("NayaDesignLens.snapshot().status") == "NEEDS_EVIDENCE"
        page.locator("#sample").click()
        assert page.evaluate("NayaDesignLens.snapshot().status") == "NEEDS_EVIDENCE"
        for field in page.locator("[data-key]").all():
            field.select_option("10")
        page.locator("#gates select").first.select_option("fail")
        assert page.evaluate("NayaDesignLens.snapshot().status") == "REWORK_REQUIRED"
        page.locator("#gates select").first.select_option("pass")
        assert page.evaluate("NayaDesignLens.snapshot().status") == "NEEDS_EVIDENCE"
        for field in page.locator("[data-evidence]").all():
            field.fill("https://example.org/review/NOT-A-VERIFIED-RECEIPT")
        assert page.evaluate("NayaDesignLens.snapshot().status") == "READY_FOR_INDEPENDENT_REVIEW"
        assert page.evaluate("NayaDesignLens.snapshot().verified") is False
        assert page.evaluate("NayaDesignLens.snapshot().authority_granted") is False
        with page.expect_download() as result:
            page.locator("#export").click()
        assert result.value.suggested_filename == "nayanet-design-assessment.json"
        page.locator("#reset").click()
        assert page.evaluate("NayaDesignLens.snapshot().status") == "NEEDS_EVIDENCE"
        context.close()
    b.close()
print("Five viewport candidate diagnostic smoke tests passed; no authority conferred.")
