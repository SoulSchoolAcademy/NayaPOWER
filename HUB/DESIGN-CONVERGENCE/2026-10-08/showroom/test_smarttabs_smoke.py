"""Minimal independent Chromium smoke acceptance for a candidate SmartTabs specimen.
Install playwright, run: python test_smarttabs_smoke.py
This test uses document injection because some review sandboxes prohibit file:// and localhost navigation.
Not a production or full WCAG qualification.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
HTML=Path(__file__).with_name("index.html").read_text(encoding="utf-8")
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for width in (1440,1024,768,390,320):
  cx=b.new_context(viewport={"width":width,"height":900})
  page=cx.new_page()
  page.evaluate("""() => {const store=new Map();Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,String(v))}});}""")
  page.set_content(HTML,wait_until="load")
  assert page.evaluate("!!window.NayaTeachingSmartTabs"), f"{width} mount"
  assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1"), f"{width} overflow"
  assert page.evaluate("getComputedStyle(document.body).fontSize")=="18px"
  assert page.locator(".hero-cta").count()==3
  assert page.locator(".hero-cta").first.evaluate("(e)=>parseFloat(getComputedStyle(e).borderTopWidth)>=1.5")
  colors=page.locator(".jewelrow .jewel").evaluate_all("(els)=>els.map(e=>getComputedStyle(e).getPropertyValue('--tone').trim())")
  assert len(colors)==5 and len(set(colors))==5
  page.locator("#cta-create").click()
  page.locator("input[name=label]").fill("My Note")
  page.locator("input[name=route]").fill("#library")
  page.get_by_role("button",name="Save shortcut").click()
  assert page.evaluate("NayaTeachingSmartTabs.list().some(s=>s.label==='My Note')")
  page.locator(".st-shortcut[data-id^=st-] .st-shortcut__more").click()
  page.get_by_role("menuitem",name="Gold Star").click()
  assert page.evaluate("NayaTeachingSmartTabs.list().find(s=>s.label==='My Note').star")
  page.locator(".st-shortcut[data-id^=st-] .st-shortcut__more").click()
  page.get_by_role("menuitem",name="Remove shortcut").click()
  assert page.evaluate("!NayaTeachingSmartTabs.list().some(s=>s.label==='My Note')")
  cx.close()
 b.close()
print("Five viewport functional smoke checks passed (candidate; browser storage stubbed).")
