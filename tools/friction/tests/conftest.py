import os
import sys

# Make tools/friction importable as flat modules (balance, friction,
# watchers, cli) regardless of how pytest was invoked.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
