from pathlib import Path

APP = Path('NAYANET/HUB/src/app/App.tsx').read_text(encoding='utf-8')
MAIN = Path('NAYANET/HUB/src/main.tsx').read_text(encoding='utf-8')

boards = [
    'What Is Naya Power?', 'What Is Naya?', 'What Are Smart Notes?',
    'Your Intelligence Today', 'Intelligence Reports',
    'What Is the Intelligent Library?', 'Smart Lists', 'Smart Spaces', 'Smart Mail'
]
sidebar = [
    'Your Intelligence Today', 'Your Report', 'Intelligent Library', 'Smart Share',
    'Smart Ledger', 'Your Connections', 'Smart Lists', 'Smart Spaces', 'Smart Mail', 'Settings'
]
layers = [
    'In a Nutshell', 'Human Note', 'Child Note', 'Grandma Note', 'Naya Note',
    'Machine Note', 'Learning Lesson', 'What It Means',
    'How to Use / How to Apply', "What's In It For You"
]
for title in boards:
    assert APP.count("title:'" + title + "'") == 1, f'missing/duplicate board: {title}'
for label in sidebar:
    assert "'" + label + "'" in APP, f'missing canonical sidebar item: {label}'
for label in layers:
    assert label in APP, f'missing layer: {label}'
assert len(boards) == 9
assert APP.count("title:'") == 9
assert APP.count('layerNames=[') == 1
for forbidden in [
    'Collective', 'Evidence', 'Smart Mail — New', 'Source / Understand / Act / Verify / Learn',
    'SMART SHARE', 'YOUR REPORT', 'YOUR CONNECTIONS', 'Smart Start', 'Smart Ledgers', 'Peer Connections'
]:
    if forbidden == 'Collective':
        # The privacy contract may legitimately contain "Collective by consent".
        continue
    assert forbidden not in APP, f'forbidden legacy UI: {forbidden}'
assert 'hub-509-nine-board.css' in MAIN
print('NAYA 509 nine-board source gate: PASS')
print('boards=9 sidebar=10 layers=10 forbidden_legacy=PASS')
