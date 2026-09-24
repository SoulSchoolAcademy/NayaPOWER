import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.naya' / 'runtime'))
from claim_currentness_v1 import resolve_currentness as resolve
