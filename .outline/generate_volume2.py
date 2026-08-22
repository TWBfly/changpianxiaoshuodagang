# -*- coding: utf-8 -*-
"""
Generator for Volume 2: 江南卷 (Chapters 25..48)
Outputs complete, bespoke handcrafted specifications to vol2_specs.py.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from populate_all_volumes import make_vol_file

# We will author all 24 chapters for Volume 2
