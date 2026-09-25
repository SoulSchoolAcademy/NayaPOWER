from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya/memory"))
import verify_memory_surface
def test_canonical_memory_surface():
    assert verify_memory_surface.verify()==[]
