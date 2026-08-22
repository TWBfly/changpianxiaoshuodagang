# -*- coding: utf-8 -*-
"""
Modular Master Generator for Volumes 2 to 6.
Builds vol2_specs.py, vol3_specs.py, vol4_specs.py, vol5_specs.py, vol6_specs.py
and updates v2_chapter_specs.py.
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from populate_all_volumes import format_ch_entry, make_vol_file, write_v2_main_specs

# We will author each volume's 24 chapters with 100% bespoke data
