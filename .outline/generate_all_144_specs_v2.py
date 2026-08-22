# -*- coding: utf-8 -*-
"""
Direct Full Generator for Volumes 2 to 6.
Generates vol2_specs.py, vol3_specs.py, vol4_specs.py, vol5_specs.py, vol6_specs.py,
and updates v2_chapter_specs.py.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from populate_all_volumes import format_ch_entry, make_vol_file, write_v2_main_specs

# Let's write the complete code for generate_all_144_specs_v2.py
