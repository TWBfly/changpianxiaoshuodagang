# -*- coding: utf-8 -*-
"""Normalize all make_beat calls in vol1_specs.py to have exactly 10 args"""

import ast
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def fix_vol1():
    v1_file = OUTLINE_DIR / "vol1_specs.py"
    lines = v1_file.read_text(encoding="utf-8").splitlines()
    
    # We can rewrite build_vol1_full.py to ensure all make_beat calls in all 24 chapters have exactly 10 arguments.
    # Let's inspect build_vol1_full.py and regenerate.
    print(f"Reading {v1_file}")

if __name__ == "__main__":
    fix_vol1()
