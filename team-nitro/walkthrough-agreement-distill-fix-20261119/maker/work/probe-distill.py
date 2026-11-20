#!/usr/bin/env python3
"""Probe the distill outputs IN MEMORY (no disk writes): run the filed
transform-distill.js, capture unfold+welcome bytes, print targeted greps
so the fix transform can be written against the real distill bytes."""
import hashlib, re, subprocess, sys

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix-20261119/maker/work"


def emit(mode):
    r = subprocess.run(["node", WORK + "/transform-distill.js", "--emit", mode],
                       capture_output=True, timeout=120)
    assert r.returncode == 0, "transform %s failed: %s" % (mode, r.stderr.decode("utf-8", "replace")[-500:])
    return r.stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def show(label, text, pat, ctx=120):
    ms = list(re.finditer(pat, text))
    print("== %s: %d hits ==" % (label, len(ms)))
    for m in ms[:6]:
        s = max(0, m.start() - ctx)
        print("  ..." + text[s:m.end() + ctx].replace("\n", " ")[:2 * ctx + 40] + "...")


def main():
    u = emit("unfold").decode("utf-8", "replace")
    w = emit("welcome").decode("utf-8", "replace")
    print("unfold %d B %s" % (len(u), sha(u.encode())[:12]))
    print("welcome %d B %s" % (len(w), sha(w.encode())[:12]))
    show("unfold child-can-understand", u, r"if a child can understand")
    show("welcome child-can-understand", w, r"if a child can understand")
    show("unfold supercomputer", u, r"supercomputer")
    show("welcome supercomputer", w, r"supercomputer")
    show("unfold superhighway", u, r"superhighway")
    show("welcome superhighway", w, r"superhighway")
    show("welcome deck-dots-block", w, r"jewelNum\.textContent=\(S\.deck\+1\)")
    show("welcome updateChrome-deck", w, r"else if\(S\.view==='deck'\)\{")
    show("welcome fp-smart-talk showcase", w, r"fp-smart-talk \.lb-showcase")
    show("unfold deckBody letter-beat display", u, r"#deckBody \.letter-beat\{height:100%")
    show("unfold frame-now hide", u, r"\.letter-beat:not\(\.frame-now\)\{display:none")
    show("welcome placeFaces side", w, r"side: b\.classList\.contains\('face-right'\)")
    show("welcome fpEnterDeal handler", w, r"enterBtn\)enterBtn\.addEventListener")
    show("welcome Nine pictures", w, r"Nine pictures")
    show("unfold 99 out of 100", u, r"99 out of 100")
    show("welcome 99 out of 100", w, r"99 out of 100")
    show("unfold Waiting on the captioned", u, r"Waiting on the captioned video")
    show("welcome Waiting on the captioned", w, r"Waiting on the captioned video")
    show("unfold fpAudioState", u, r"fpAudioState")
    show("welcome deckEnd fn", w, r"function deckEnd\(\)")
    show("welcome letterEnd fn", w, r"function letterEnd\(\)")
    show("welcome derive phase", w, r"S\.phase=\(db&&db\.classList\.contains\('fp-smart-visual'\)\)")
    show("unfold wireFrame8 showFrame8", u, r"function showFrame8\(n\)")
    show("welcome render deck hidden", w, r"b\.hidden=!sd;b\.classList\.toggle\('fp-now',sd\)")
    show("welcome fp-now grid", w, r"grid-template-columns:minmax\(340px,42%\)")
    show("unfold dealAgreeBtn href", u, r"window\.location\.href = \"/\?stage=bridge\"")
    show("welcome submit identity", w, r"window\.location\.href='/identity\.html'")
    show("welcome af-prog/deck jewel", w, r"fpStageJewelNum")
    show("unfold af-prog pill", u, r"af-prog-num")
    show("welcome letter jewel text", w, r"jewelNum\.textContent=\(S\.letter\+1\)")
    show("welcome deck jewel in updateChrome", w, r"dotsEl\.classList\.add\('fp-on'\)")
    print("PROBE DONE")


if __name__ == "__main__":
    main()
