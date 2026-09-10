# -*- coding: utf-8 -*-
"""
Full bespoke generator for vol5_specs.py and vol6_specs.py
Guarantees 100% bespoke scenes, clusters, and beats with zero repetitive template fingerprints.
"""

import sys
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

# 44 Chapters for Volume 5 (97..140)
# Structure: (n, title, actors, function, delta, conf_c, stakes_c, hook_c, scenes, clusters, beats)
# Each scene: (entry, goal, opponent, stakes, actions, turn, exit_st)
# Each cluster: (goal, medium, beat_indices, turn, cost, exit_st, next_pressure)
# Each beat: (role, cause, actor, b_goal, action, counterforce, info_choice, delta_dict, a_goal, pressure)
