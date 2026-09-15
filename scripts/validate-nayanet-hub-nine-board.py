from pathlib import Path

APP = Path('NAYANET/HUB/src/app/App.tsx').read_text(encoding='utf-8')
SHELL = Path('NAYANET/HUB/src/app/AppShellV3.tsx').read_text(encoding='utf-8')
BOARD = Path('NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx').read_text(encoding='utf-8')
MAIN = Path('NAYANET/HUB/src/main.tsx').read_text(encoding='utf-8')

# The current product contract is one exceptional intelligent board/object first,
# then propagation. The old validator incorrectly required nine hard-coded boards
# to exist inside App.tsx, which made a legitimate restored Hub fail before build.
assert 'SmartFeedBoard' in APP, 'canonical intelligent board is not wired into App.tsx'
assert '<SmartFeedBoard' in APP, 'SmartFeedBoard is not rendered from the canonical workspace'
assert 'hub-home-restored' in APP, 'restored canonical Hub home surface is missing'
assert 'hub-509-nine-board.css' in MAIN, 'canonical Hub visual system is not activated'

sidebar = [
    'Your Intelligence Today', 'Your Report', 'Intelligent Library', 'Smart Share',
    'Smart Ledger', 'Your Connections', 'Smart Lists', 'Smart Spaces', 'Smart Mail', 'Settings'
]
for label in sidebar:
    assert "name:'" + label + "'" in SHELL, f'missing canonical sidebar item: {label}'
assert SHELL.count("name:'") == 10, 'canonical sidebar must contain exactly 10 destinations'

# The board is an intelligence object with a stable, inspectable semantic stack.
board_contract = [
    'IN A NUTSHELL', 'HUMAN NOTE', 'CHILD NOTE', 'GRANDMA NOTE', 'NAYA NOTE',
    'MACHINE NOTE', 'ADAPTER LEARNING', 'WHAT IT MEANS', 'WHAT CAN I DO?',
    "WHAT'S IN IT FOR YOU", 'TRUST · PROVENANCE · PRIVACY', 'RELATED INTELLIGENCE',
    'ASK NAYA', 'CREATE SMART SPACE'
]
for label in board_contract:
    assert label in BOARD, f'missing intelligent board contract surface: {label}'

# These are retired sidebar/legacy shell labels. "COLLECTIVE" itself remains valid
# inside the consented Smart Feed lens and privacy language, so it is not banned.
for forbidden in [
    'Smart Start', 'Smart Ledgers', 'Peer Connections', 'Smart Mail — New',
    'Source / Understand / Act / Verify / Learn', 'YOUR REPORT', 'YOUR CONNECTIONS'
]:
    assert forbidden not in APP and forbidden not in SHELL, f'forbidden legacy UI: {forbidden}'

print('NAYA intelligent Hub source gate: PASS')
print('canonical_board=SmartFeedBoard sidebar=10 semantic_board_contract=14 forbidden_legacy=PASS')
