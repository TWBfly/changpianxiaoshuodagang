# -*- coding: utf-8 -*-
"""
Compilation script that outputs vol1_specs.py, vol2_specs.py, vol3_specs.py,
vol4_specs.py, vol5_specs.py, vol6_specs.py and links them into v2_chapter_specs.py.
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def main():
    print("Compiling all 144 bespoke chapters across 6 volumes...")
    # We will write the volume generators and run them.

if __name__ == "__main__":
    main()
