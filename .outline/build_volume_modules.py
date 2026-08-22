# -*- coding: utf-8 -*-
"""
Generates all 6 volume specs files and builds v2_chapter_specs.py.
Ensures ZERO template repetitions, strict spatial sanity, correct actor roles.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def write_file(filename, content):
    p = BASE_DIR / filename
    p.write_text(content, encoding="utf-8")
    print(f"Wrote {p} ({len(content)} bytes)")

# Let's write the generator script that outputs vol1_specs.py to vol6_specs.py
