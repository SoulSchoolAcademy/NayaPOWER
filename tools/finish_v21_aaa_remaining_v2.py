#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / 'tools' / 'build_v21_canonical.py'
MARK = '/* MAXESS-V21-AAA-REMAINING-FINISH-V2 */'
s = BUILDER.read_text(encoding='utf-8')

if MARK in s:
    print('MAXESS V21 REMAINING FINISH V2 ALREADY PRESENT')
    raise SystemExit(0)

# Eliminate Python invalid-escape warning at source.
if 'JS = r"""' not in s:
    s = s.replace('JS = """', 'JS = r"""', 1)

# After inserting the score-meaning chapter, canonical section indexes are:
# 0 Naya, 1 Result, 2 Score Meaning, 3 Five Dimensions, 4 Report,
# 5 Pattern, 6 Strength, 7 Lever, 8 Next Move, 9 Masters, 10 Playground, 11 CTA.
for name, idx in [('dimSection',3),('pattern',5),('strength',6),('lever',7),('next',8),('mastersSection',9),('playground',10)]:
    s = re.sub(rf"var {name}=sections\[[0-9]+\];", f"var {name}=sections[{idx}];", s, count=1)

# Add score-meaning chapter immediately before the existing Five Dimensions section.
if 'v21-score-meaning' not in s:
    section_pattern = re.compile(
        r"(?P<prefix>\s*'<section class=\\\"v21-section v21-light\\\"><div class=\\\"v21-inner\\\">'\s*\+\s*\n\s*'<span class=\\\"v21-kicker\\\" style=\\\"color:#7445ad\\\">YOUR FIVE DIMENSIONS</span>)",
        re.S,
    )
    replacement = r'''      '<section class=\"v21-section v21-light v21-score-meaning\"><div class=\"v21-inner\">'+
        '<span class=\"v21-kicker\" style=\"color:#7445ad\">WHAT YOUR SCORE MEANS</span><h2 class=\"v21-section-title\">Your score is a starting point, not a verdict.</h2><div class=\"v21-story\"><div class=\"v21-card\"><span class=\"v21-kicker\" style=\"color:#7445ad\">WHERE YOU ARE</span><h3>'+st+'</h3><p>'+escapeHtml(st==='Mastering'?'You are operating with strong AI capability and can focus on compounding leverage.':st==='Advancing'?'You have meaningful capability and are ready to make your workflows more deliberate and repeatable.':st==='Developing'?'You have useful capability emerging; the fastest gains will come from deliberate practice and evaluation.':st==='Foundation'?'You have the building blocks. Focus on clarity, judgment and repeatable practice.':'You are beginning to establish the foundations. A few focused habits can change the trajectory quickly.')+'</p></div><div class=\"v21-card\"><span class=\"v21-kicker\" style=\"color:#7445ad\">HOW TO USE IT</span><h3>Create → Score → Improve</h3><p>Use your result to choose one real AI workflow, make the quality visible, and improve it deliberately. Your next level comes from what you do with the score.</p></div></div></div></section>'+
      '<section class=\"v21-section v21-light\"><div class=\"v21-inner\">'+
        '<span class=\"v21-kicker\" style=\"color:#7445ad\">YOUR FIVE DIMENSIONS</span>'''
    s2, n = section_pattern.subn(lambda m: replacement, s, count=1)
    if n != 1:
        raise SystemExit('SCORE-MEANING STRUCTURAL INSERTION FAILED')
    s = s2

# Ensure fingerprint label supplements, rather than replaces, the five dimensions contract.
needle = '<span class=\\"v21-kicker\\" style=\\"color:#7445ad\\">YOUR FIVE DIMENSIONS</span>'
if needle in s and 'YOUR AI FINGERPRINT' not in s:
    s = s.replace(needle, '<span class=\\"v21-kicker\\" style=\\"color:#7445ad\\">YOUR AI FINGERPRINT</span>'+needle, 1)

# Strength depth.
s = s.replace(
    "<p>You already have meaningful capability here. Compound it deliberately instead of trying to improve everything at once. The best next move is to turn this strength into a repeatable advantage.</p>",
    "<p>You already have meaningful capability here. The goal is not to admire the score; it is to compound the capability until it becomes a repeatable advantage you can use across real AI work.</p><div class=\\\"v21-three\\\"><div class=\\\"v21-action\\\"><b>KEEP USING IT</b><p>Put this capability into a real workflow this week.</p></div><div class=\\\"v21-action\\\"><b>MAKE IT REPEATABLE</b><p>Turn what works into a reusable method or template.</p></div><div class=\\\"v21-action\\\"><b>TEACH IT TO NAYA</b><p>Use Naya to document and improve the workflow so the strength compounds.</p></div></div>",
    1
)

# Lever action loop.
s = s.replace(
    "<p>Your strongest opportunity is '+escapeHtml(lowest.name)+'. This is not a verdict about you. It is the area furthest behind the rest of your profile, so focused improvement here can create disproportionate gains.</p>",
    "<p>Your strongest opportunity is '+escapeHtml(lowest.name)+'. This is not a verdict about you. It is the clearest place to focus because it currently sits furthest behind the rest of your profile.</p><div class=\\\"v21-three\\\"><div class=\\\"v21-action\\\"><b>CHOOSE ONE TASK</b><p>Pick one real AI task where '+escapeHtml(lowest.name)+' matters.</p></div><div class=\\\"v21-action\\\"><b>IMPROVE IT ONCE</b><p>Make one deliberate change and compare the result.</p></div><div class=\\\"v21-action\\\"><b>REPEAT</b><p>Turn the improvement into a habit instead of a one-time fix.</p></div></div>",
    1
)

# Pathway personalization.
s = s.replace(
    "<p>These specialist pathways become useful once you know what you want to improve.</p>",
    "<p>These specialist pathways are not just a library. They are the doors that can help you compound '+escapeHtml(strongest.name)+' and build '+escapeHtml(lowest.name)+'.</p><div class=\\\"v21-aaa-naya-note\\\"><img src=\\\"https://raw.githubusercontent.com/SoulSchoolAcademy/maxess/main/Naya%20Profile%20Black.jpg\\\" alt=\\\"Naya, your AI guide\\\"><div><b>Naya · your guide</b><strong>Start with the pathway that matches your next move.</strong><p>Your best learning path is the one that connects directly to what your profile is telling you right now.</p></div></div>",
    1
)

# Final solution bridge.
s = s.replace(
    '<h2>Now you know where you are. The next step is becoming better.</h2><p>MAXESS is designed for people who want exceptional results from AI—not “good enough.”</p>',
    '<h2>Now you know where you are. Let’s build what comes next.</h2><p>You have a score, a fingerprint, a strength, a lever and a next move. The next step is turning that understanding into real AI capability.</p>',
    1
)

# Explicit authority marker.
s = s.replace(
    "root.setAttribute('data-results-data-source','window.MAXESS_RESULT');",
    "/* MAXESS_RESULT_AUTHORITY: window.MAXESS_RESULT */ root.setAttribute('data-results-data-source','window.MAXESS_RESULT');",
    1
)

s = s.replace("var scoreValue=score(r)||0;", MARK+"\n    var scoreValue=score(r)||0;", 1)
BUILDER.write_text(s, encoding='utf-8')
print('MAXESS V21 REMAINING AAA FINISH V2 APPLIED')
print('Completed: score meaning, AI fingerprint, Strength depth, Lever action loop, pathway personalization, Naya guidance, CTA bridge, runtime mapping, authority marker, warning cleanup.')
