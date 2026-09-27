"""Author machine-typed decision vocabularies for the five untyped Nodes.

DERIVATION RULE: every value below is taken from that Node's OWN contract - its
Failure States table, MUST Rules and Acceptance Criteria. No behaviour is invented
and no rule is changed. Only machine-typed decision outcomes are ADDED, using the
inline form the contracts already use elsewhere (PROVE / VERIFY / LEARN) and the
form LAW already uses (one typed value per output line).

SELF     <- failure states: identity unresolvable, mission missing, continuity
           corrupted, successor unavailable; MUST: establish known/unknown boundary
ACT      <- failure states: authorization missing, execution fails, reversibility
           violated, proof requirement unmet, receipt generation fails
KNOW     <- failure states: identity collision, provenance missing, stale data,
           classification unknown; MUST: classify by type and epistemic state
CONNECT  <- failure states: relationship type unknown, contradiction, supersession,
           relevance cannot be established, provenance missing
EVOLVE   <- failure states: successor context incomplete, authority missing,
           continuity verification fails, improvement unverified, governance violation
"""
from pathlib import Path

ROOT = Path('.')

EDITS = {
    'SELF': [
        ("- Identity context (who is executing)",
         "- Identity context — identity resolution (ESTABLISHED, UNRESOLVED, CONFLICTED)"),
        ("- Continuity context (what must survive)",
         "- Continuity context — continuity state (INTACT, RESTORING, CORRUPTED, DEGRADED)"),
    ],
    'ACT': [
        ("- Execution state (progress, status)",
         "- Execution state (PLANNED, AUTHORIZED, EXECUTING, COMPLETED, FAILED, HALTED, ROLLED_BACK)"),
        ("- Proof requirement (what evidence is needed)",
         "- Proof requirement — proof status (DEFINED, MET, UNMET, UNVERIFIED)"),
    ],
    'KNOW': [
        ("- Current knowledge state summary",
         "- Current knowledge state summary — knowledge state (CANONICAL, UNVERIFIED, STALE, UNKNOWN, COLLIDING)"),
    ],
    'CONNECT': [
        ("- Applicability assessment (why this matters now)",
         "- Applicability assessment — applicability (APPLICABLE, NOT_APPLICABLE, CONTRADICTED, SUPERSEDED, UNCLASSIFIED, UNVERIFIED)"),
    ],
    'EVOLVE': [
        ("- Evolution state (what changed, what was rejected)",
         "- Evolution state (PROPOSED, ADOPTED, REJECTED, ESCALATED, HALTED, VIOLATION_DETECTED)"),
    ],
}

for node, pairs in EDITS.items():
    p = ROOT / f'BRAIN/03-KERNEL/NODES/{node}/0001-CONTRACT.md'
    text = p.read_text(encoding='utf-8')
    for old, new in pairs:
        if new in text:
            print(f'  {node}: already typed, skipped')
            continue
        if old not in text:
            raise SystemExit(f'{node}: anchor not found -> {old!r}')
        text = text.replace(old, new, 1)
        print(f'  {node}: typed -> {new[:78]}')
    p.write_text(text, encoding='utf-8')

print()
print('Contracts updated. Behaviour unchanged; only machine-typed outcomes added.')
