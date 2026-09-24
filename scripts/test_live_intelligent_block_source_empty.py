"""Empty owner-scoped canonical source must fail closed."""
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
import live_intelligent_block_source as source

class Response:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return b"[]"

def main():
    with patch.dict(source.os.environ, {
        "SUPABASE_PUBLISHABLE_KEY": "test-key",
        "NAYANET_OWNER_ACCESS_TOKEN": "test-token",
    }, clear=False), patch.object(source.urllib.request, "urlopen", return_value=Response()):
        try:
            source.load_live_intelligent_blocks(owner_id="00000000-0000-0000-0000-000000000001")
        except RuntimeError as exc:
            assert str(exc) == "CANONICAL_SOURCE_EMPTY"
            print("EMPTY_CANONICAL_SOURCE_FAIL_CLOSED=PASS")
        else:
            raise AssertionError("empty canonical source did not fail closed")

if __name__ == "__main__":
    main()
