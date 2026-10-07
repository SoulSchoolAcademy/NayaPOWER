#!/bin/sh
# Run from the project root as: bash run.sh
# runner.py uses `from tools.util import helper`, so it must be run as a
# module from the project root — running `python3 tools/runner.py` puts
# tools/ (not the project root) on the import path and raises
# ModuleNotFoundError. (Lesson from PR #1745.)
cd "$(dirname "$0")"
python3 -m tools.runner
