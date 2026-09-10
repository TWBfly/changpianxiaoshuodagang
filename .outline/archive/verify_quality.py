# -*- coding: utf-8 -*-
"""Comprehensive Quality and Consistency Verifier for 144 Chapters Master Outline"""

import re
import sys
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent
sys.path.insert(0, str(OUTLINE_DIR))

from v2_chapter_specs import generate_all_144_specs

def verify_all():
    specs = generate_all_144_specs()
    print(f"=== Quality & Consistency Check for {len(specs)} Chapters ===")
    
    # 1. Total count
    assert len(specs) == 144, f"Expected 144 chapters, got {len(specs)}"
    
    # 2. Check for template placeholder phrases
    forbidden_patterns = [
        r"在京师推进.*之核心战术部署",
        r"在.*推进.*战略方略",
        r"顽固利益集团企图在.*中制造阻碍",
    ]
    
    flagged = []
    for s in specs:
        ch_num = s['n']
        title = s['name']
        for b in s['beats_detail']:
            action = b.get('action', '')
            intent = b.get('before_goal', '')
            subtext = b.get('subtext', '')
            for pat in forbidden_patterns:
                if re.search(pat, action) or re.search(pat, intent):
                    flagged.append((ch_num, title, action, pat))
                    
    print(f"Flagged placeholder occurrences in beats: {len(flagged)}")
    if flagged:
        for f in flagged[:10]:
            print("  Flagged:", f)
            
    # 3. Check Canon Hard Consistency
    # Zhao Biao death: Ch 4
    # Wanyan Badu death: Ch 60
    # Xiao Qianyuan death: Ch 106
    # Martial Realms stepped
    print("\n=== Canon Verification ===")
    # Ch 1
    ch1 = next(s for s in specs if s['n'] == 1)
    print("Ch 1 Function:", ch1['function'])
    # Ch 4
    ch4 = next(s for s in specs if s['n'] == 4)
    print("Ch 4 Function:", ch4['function'])
    # Ch 60
    ch60 = next(s for s in specs if s['n'] == 60)
    print("Ch 60 Function:", ch60['function'])
    # Ch 104
    ch104 = next(s for s in specs if s['n'] == 104)
    print("Ch 104 Function:", ch104['function'])
    # Ch 106
    ch106 = next(s for s in specs if s['n'] == 106)
    print("Ch 106 Function:", ch106['function'])
    # Ch 144
    ch144 = next(s for s in specs if s['n'] == 144)
    print("Ch 144 Function:", ch144['function'])

if __name__ == "__main__":
    verify_all()
