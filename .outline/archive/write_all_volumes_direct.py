# -*- coding: utf-8 -*-
"""
Direct Master Writer for Volumes 2 to 6.
Generates vol2_specs.py through vol6_specs.py and wires v2_chapter_specs.py.
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from populate_all_volumes import format_ch_entry, make_vol_file, write_v2_main_specs

# We will author each volume's 24 chapters
