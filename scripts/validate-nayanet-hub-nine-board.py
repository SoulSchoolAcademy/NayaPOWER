from pathlib import Path

APP=Path('NAYANET/HUB/src/app/App.tsx').read_text(encoding='utf-8')
SHELL=Path('NAYANET/HUB/src/app/AppShellV3.tsx').read_text(encoding='utf-8')
BOARD=Path('NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx').read_text(encoding='utf-8')
MAIN=Path('NAYANET/HUB/src/main.tsx').read_text(encoding='utf-8')

assert 'SmartFeedBoard' in APP
assert '<SmartFeedBoard' in APP
assert 'hub-home-restored' in APP
assert 'hub-restored-primo-v1.css' in MAIN
assert 'smart-feed-surgical-elevation.css' in MAIN

sidebar=['Your Intelligence Today','Your Report','Intelligent Library','Smart Share','Smart Ledger','Your Connections','Smart Lists','Smart Spaces','Smart Mail','Settings']
for label in sidebar:
    assert "name:'"+label+"'" in SHELL, f'missing canonical sidebar item: {label}'
assert SHELL.count("name:'")==10, 'canonical sidebar must contain exactly 10 destinations'

board_contract=['IN A NUTSHELL','HUMAN NOTE','CHILD NOTE','GRANDMA NOTE','NAYA NOTE','MACHINE NOTE','ADAPTER LEARNING','WHAT IT MEANS','WHAT CAN I DO?',"WHAT'S IN IT FOR YOU",'TRUST · PROVENANCE · PRIVACY','RELATED INTELLIGENCE','ASK NAYA','CREATE SMART SPACE']
for label in board_contract:
    assert label in BOARD, f'missing intelligent board contract surface: {label}'

for label in ['Smart Start','Smart Ledgers','Peer Connections','Collective Intelligence','Smart Mail — New']:
    assert "name:'"+label+"'" not in SHELL, f'retired sidebar item remains: {label}'

print('NAYA Intelligent Hub source gate: PASS')
print('canonical_shell=restored sidebar=10 canonical_board=SmartFeedBoard semantic_board_contract=14 retired_sidebar=PASS')
