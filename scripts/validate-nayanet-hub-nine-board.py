from pathlib import Path

APP=Path('NAYANET/HUB/src/app/App.tsx').read_text(encoding='utf-8')
SHELL=Path('NAYANET/HUB/src/app/AppShellV3.tsx').read_text(encoding='utf-8')
BOARD=Path('NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx').read_text(encoding='utf-8')
MAIN=Path('NAYANET/HUB/src/main.tsx').read_text(encoding='utf-8')

assert 'SmartFeedBoard' in APP, 'canonical intelligent board is not wired into App.tsx'
assert '<SmartFeedBoard' in APP, 'SmartFeedBoard is not rendered from the canonical workspace'
assert 'hub-home-restored' in APP, 'restored canonical Hub home surface is missing'
assert 'hub-restored-primo-v1.css' in MAIN, 'restored Hub visual layer is not activated'
assert 'smart-feed-surgical-elevation.css' in MAIN, 'surgical SmartFeedBoard elevation is not activated'

sidebar=['Intelligent','Reports','Intelligent Library','Smart Start','Smart Ledgers','Peer Connections','Smart Lists','Smart Spaces','Smart Mail','Settings']
for label in sidebar:
    assert "name:'"+label+"'" in SHELL, f'missing canonical sidebar item: {label}'
assert SHELL.count("name:'")==10, 'canonical sidebar must contain exactly 10 destinations'

board_contract=['IN A NUTSHELL','HUMAN NOTE','CHILD NOTE','GRANDMA NOTE','NAYA NOTE','MACHINE NOTE','ADAPTER LEARNING','WHAT IT MEANS','WHAT CAN I DO?',"WHAT'S IN IT FOR YOU",'TRUST · PROVENANCE · PRIVACY','RELATED INTELLIGENCE','ASK NAYA','CREATE SMART SPACE']
for label in board_contract:
    assert label in BOARD, f'missing intelligent board contract surface: {label}'

# Retired navigation labels must not be present as canonical sidebar item names.
retired=['Your Intelligence Today','Your Report','Smart Share','Smart Ledger','Your Connections','Collective Intelligence','Evidence']
for label in retired:
    assert "name:'"+label+"'" not in SHELL, f'retired sidebar item remains: {label}'
assert "name:'Smart Mail — New'" not in SHELL, 'Smart Mail New remains in sidebar'

print('NAYA Intelligent Hub source gate: PASS')
print('canonical_shell=restored sidebar=10 canonical_board=SmartFeedBoard semantic_board_contract=14 retired_sidebar=PASS')
