# -*- coding: utf-8 -*-
"""
Unified 144-Chapter Master Compiler (Volumes 2 to 6).
Outputs handcrafted, bespoke vol2_specs.py .. vol6_specs.py.
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from populate_all_volumes import format_ch_entry, make_vol_file, write_v2_main_specs

# Let's write the complete code for compile_all_volumes_v2.py
