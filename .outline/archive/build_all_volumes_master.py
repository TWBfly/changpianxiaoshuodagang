# -*- coding: utf-8 -*-
"""
Master Builder for Volumes 2 to 6 (Chapters 25..144)
Generates 100% handcrafted, non-repeating data for all volumes.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from populate_all_volumes import format_ch_entry, make_vol_file, write_v2_main_specs

# We will define all chapters for Volumes 2, 3, 4, 5, 6.
