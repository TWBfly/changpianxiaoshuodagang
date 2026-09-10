# -*- coding: utf-8 -*-
"""Extract Chapters 97..120 by comment blocks and write clean vol5_specs.py"""

import re
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def build_vol5_by_comment():
    src_file = OUTLINE_DIR / "build_vol5_concrete.py"
    text = src_file.read_text(encoding="utf-8")
    
    # Split text into lines
    lines = text.splitlines()
    
    chapters = {}
    current_ch = None
    current_lines = []
    
    ch_comment_re = re.compile(r'^\s*#\s*(\d{2,3})\s*$')
    
    for line in lines:
        m = ch_comment_re.match(line)
        if m:
            n = int(m.group(1))
            if 97 <= n <= 120:
                if current_ch is not None and current_ch not in chapters:
                    chapters[current_ch] = "\n".join(current_lines).strip()
                current_ch = n
                current_lines = []
                continue
        if current_ch is not None:
            # Check if this line is part of Python assignment or string termination
            if line.strip().startswith("'''") or line.strip().startswith('ch_') or line.strip().startswith('full_code'):
                if current_ch not in chapters:
                    chapters[current_ch] = "\n".join(current_lines).strip()
                current_ch = None
                current_lines = []
            else:
                current_lines.append(line)
                
    if current_ch is not None and current_ch not in chapters:
        chapters[current_ch] = "\n".join(current_lines).strip()
        
    print(f"Extracted {len(chapters)} chapters: {sorted(chapters.keys())}")
    
    header = '''# -*- coding: utf-8 -*-
"""Volume 5: 弑仙卷 (Chapters 97..120) Handcrafted Specifications with strict Canon & Method Friction"""

def get_vol5_specs(make_beat, make_scene, make_cluster):
    records = []

    def add_ch(n, vol, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_list, s_list, c_list):
        records.append({
            "n": n, "volume_ref": vol, "name": title, "actors": actors,
            "function": function, "core_delta": delta_st, "conflict_concrete": conf_c,
            "stakes_concrete": stakes_c, "hook_concrete": hook_c,
            "beats_detail": b_list, "scenes_detail": s_list, "clusters_detail": c_list,
            "forbidden_drift": [
                "不得把本章冲突简化为单一战力数值对轰。",
                "不得让任何角色凭空获得未埋设的证据、权限或救兵。",
                "不得用降智反派替代本章既定逻辑闭环。"
            ],
            "cap_payload": {
                "chapter_id": f"CHAPTER_PLAN.{n:03d}",
                "final_capacity": "FULL",
                "core_scenes": len(s_list),
                "payload_clusters": len(c_list),
                "stageable_core_beats": len(b_list),
                "supporting_stageable_beats": 0,
                "summary_result_beats_removed": 0,
                "target_prose_range": [4000, 6000],
                "mid_chapter_load": "PASS",
                "writer_core_plot_invention_required": False,
                "missing_middle_roles": [],
                "failure_reasons": []
            }
        })
'''

    body = []
    for n in range(97, 121):
        if n in chapters:
            ch_code = chapters[n].strip().rstrip(']').rstrip()
            body.append(f"    # {n}\n    " + ch_code)
        else:
            print(f"Missing chapter {n}!")

    full_code = header + "\n" + "\n\n".join(body) + "\n\n    return records\n"
    (OUTLINE_DIR / "vol5_specs.py").write_text(full_code, encoding="utf-8")
    print(f"vol5_specs.py generated cleanly, size: {len(full_code)} bytes")

if __name__ == "__main__":
    build_vol5_by_comment()
