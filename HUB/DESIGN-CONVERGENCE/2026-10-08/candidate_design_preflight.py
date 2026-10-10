#!/usr/bin/env python3
"""Static advisory gate for candidate design law; no visual or production claims."""
import json,re,sys
from html.parser import HTMLParser
from pathlib import Path
HERE=Path(__file__).resolve().parent
RULES=json.loads((HERE/"DIRECTOR-DESIGN-TEACHING.candidate.machine.json").read_text())
assert RULES["status"]=="CANDIDATE_NOT_RATIFIED"
assert len(RULES["rules"])==19
assert len(RULES["conflict_register"])==8

class AccentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.colors=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in {"div","li","article"} and "bullet" in a.get("class","").split() and a.get("data-accent"):
            self.colors.append(a["data-accent"].strip().lower())

def check_html(path):
    html=Path(path).read_text(encoding="utf-8",errors="replace")
    out=[]
    parser=AccentParser(); parser.feed(html)
    if len(parser.colors)>=2:
        repeated=any(a==b for a,b in zip(parser.colors,parser.colors[1:]))
        out.append({"rule":"M15","status":"FAIL" if repeated else "PASS","detail":"explicit ordered bullet-color sequence checked; perceived similarity still requires visual review"})
    else:
        out.append({"rule":"M15","status":"UNKNOWN","detail":"no explicit bullet-color sequence; cannot infer browser colors"})
    meta=re.search(r'<meta[^>]*name=[\'"]viewport[\'"][^>]*>',html,re.I)
    if meta and re.search(r'user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?(?=[,\s\'"]|$)',meta.group(),re.I):
        out.append({"rule":"M01","status":"FAIL","detail":"viewport zoom restricted"})
    # Source occurrences require human/runtime verification before declaring a live link.
    if re.search(r'https?://app\.nayanet\.technology',html,re.I):
        out.append({"rule":"M03","status":"REVIEW","detail":"prohibited URL found in source; may be comment or inactive"})
    out.append({"rule":"M02","status":"UNKNOWN","detail":"semantic click behavior not proved by static scanner"})
    out.append({"rule":"M09","status":"UNKNOWN","detail":"rendered idle light must be visually inspected"})
    return out

if __name__=="__main__":
    print(json.dumps({"status":"CANDIDATE_ONLY","files":[{"file":s,"results":check_html(s)} for s in sys.argv[1:]]},indent=2))
