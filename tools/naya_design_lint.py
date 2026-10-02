#!/usr/bin/env python3
"""Static Naya design diagnostics for HTML/CSS/JS sources.

This tool produces *evidence candidates*, not an aesthetic verdict.
It intentionally refuses to output a beauty/mastery score.

Usage:
  python tools/naya_design_lint.py path/to/ui [--json report.json] [--strict]

Strict mode exits non-zero only for deterministic high-confidence defects.
"""

from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

TEXT_EXTS={".html",".htm",".css",".js",".mjs",".ts",".tsx",".jsx"}

class HTMLAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.findings=[]
        self.stack=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        self.stack.append(tag)
        if tag=="img" and "alt" not in a:
            self.findings.append(("ERROR","IMG_MISSING_ALT","Image missing alt attribute"))
        if tag=="a":
            href=(a.get("href") or "").strip().lower()
            if href in {"#","javascript:void(0)","javascript:void(0);"}:
                self.findings.append(("WARN","PLACEHOLDER_LINK",f"Anchor uses placeholder href {href!r}"))
        if tag=="button":
            label=(a.get("aria-label") or a.get("title") or "").strip()
            self.findings.append(("BUTTON_OPEN","_button_pending",label))
    def handle_data(self, data):
        if self.findings and self.findings[-1][0]=="BUTTON_OPEN" and data.strip():
            sev,code,label=self.findings[-1]
            self.findings[-1]=("BUTTON_OK","_button_ok",label or data.strip())
    def handle_endtag(self, tag):
        if tag=="button":
            for i in range(len(self.findings)-1,-1,-1):
                if self.findings[i][0]=="BUTTON_OPEN":
                    _,_,label=self.findings[i]
                    self.findings[i]=("ERROR","BUTTON_MISSING_ACCESSIBLE_NAME","Button has no text/aria-label/title")
                    break
        if self.stack:
            self.stack.pop()

def iter_files(paths):
    seen=set()
    for raw in paths:
        p=Path(raw)
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            rp=p.resolve()
            if rp not in seen:
                seen.add(rp); yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in TEXT_EXTS:
                    rp=f.resolve()
                    if rp not in seen:
                        seen.add(rp); yield f

def add(findings,severity,code,file,message,line=None,evidence=None):
    findings.append({
        "severity":severity,
        "code":code,
        "file":str(file),
        "line":line,
        "message":message,
        "evidence":evidence,
    })

def audit(paths):
    findings=[]
    files=list(iter_files(paths))
    corpus=""
    animation_seen=False
    for f in files:
        try:
            text=f.read_text(encoding="utf-8",errors="ignore")
        except Exception as e:
            add(findings,"WARN","READ_ERROR",f,str(e)); continue
        corpus += "\n"+text

        if f.suffix.lower() in {".html",".htm"}:
            parser=HTMLAudit()
            try: parser.feed(text)
            except Exception as e: add(findings,"WARN","HTML_PARSE",f,str(e))
            for sev,code,msg in parser.findings:
                if sev in {"ERROR","WARN"}: add(findings,sev,code,f,msg)

        if f.suffix.lower()==".css" or "<style" in text.lower():
            for m in re.finditer(r"font-size\s*:\s*(\d+(?:\.\d+)?)px",text,re.I):
                size=float(m.group(1))
                if size < 12:
                    line=text.count("\n",0,m.start())+1
                    add(findings,"ERROR","MICROTYPE_EXTREME",f,f"font-size {size:g}px is below 12px",line,m.group(0))
                elif size < 16:
                    line=text.count("\n",0,m.start())+1
                    add(findings,"WARN","TYPE_BELOW_DEFAULT_FLOOR",f,f"font-size {size:g}px is below the default 16px body/control floor; verify it is metadata/noncritical",line,m.group(0))
            for m in re.finditer(r"transition\s*:\s*all\b",text,re.I):
                line=text.count("\n",0,m.start())+1
                add(findings,"WARN","TRANSITION_ALL",f,"transition: all can animate layout/paint properties; enumerate intended properties",line,m.group(0))
            if re.search(r"animation\s*:[^;]*\binfinite\b",text,re.I):
                animation_seen=True
            if re.search(r"outline\s*:\s*(?:0|none)",text,re.I) and not re.search(r":focus(?:-visible)?",text,re.I):
                add(findings,"WARN","FOCUS_OUTLINE_REMOVED",f,"outline removed without a focus/focus-visible rule in the same file")

        if f.suffix.lower() in {".html",".js",".mjs",".ts",".tsx",".jsx"}:
            for m in re.finditer(r"(?i)(?:href|src)\s*=\s*['\"]javascript:",text):
                line=text.count("\n",0,m.start())+1
                add(findings,"ERROR","JAVASCRIPT_URL",f,"javascript: URL found in interface source",line,m.group(0))

    if animation_seen and "prefers-reduced-motion" not in corpus:
        add(findings,"ERROR","REDUCED_MOTION_MISSING","<corpus>","Continuous animation detected but no prefers-reduced-motion handling found in scanned corpus")

    has_focus = bool(re.search(r":focus(?:-visible)?",corpus,re.I))
    interactive = bool(re.search(r"<button\b|<a\b|role=['\"]button|\.btn\b",corpus,re.I))
    if interactive and not has_focus:
        add(findings,"WARN","FOCUS_STYLE_NOT_FOUND","<corpus>","Interactive controls found but no focus/focus-visible styling detected")

    summary={
        "files_scanned":len(files),
        "errors":sum(1 for x in findings if x["severity"]=="ERROR"),
        "warnings":sum(1 for x in findings if x["severity"]=="WARN"),
        "note":"Static diagnostics only. No beauty/signature/mastery score is produced."
    }
    return summary,findings

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("paths",nargs="+")
    ap.add_argument("--json",dest="json_path")
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()

    summary,findings=audit(args.paths)
    report={"schema":"naya.design-static-audit.v1","summary":summary,"findings":findings}
    print(json.dumps(report,indent=2))
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if args.strict and summary["errors"]:
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
