# -*- coding: utf-8 -*-
"""Extract all 24 chapters of Vol 5 by finding add_ch(N, directly"""

import re
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def extract_all_vol5_chapters():
    src_file = OUTLINE_DIR / "build_vol5_concrete.py"
    text = src_file.read_text(encoding="utf-8")
    
    # Find all occurrences of add_ch(
    # Let's locate each add_ch(N,
    pos_list = []
    for m in re.finditer(r'add_ch\(\s*(\d+)\s*,', text):
        ch_num = int(m.group(1))
        pos_list.append((m.start(), ch_num))
        
    print(f"Found {len(pos_list)} add_ch occurrences: {[p[1] for p in pos_list]}")
    
    chapters = {}
    for i in range(len(pos_list)):
        start_pos, ch_num = pos_list[i]
        if ch_num not in chapters and 97 <= ch_num <= 120:
            # Chapter ends before the next add_ch or end of block
            if i + 1 < len(pos_list):
                end_pos = pos_list[i+1][0]
                # Look backwards from end_pos to find the closing '])'
                chunk = text[start_pos:end_pos]
                last_bracket = chunk.rfind('])')
                if last_bracket != -1:
                    chunk = chunk[:last_bracket+2]
            else:
                chunk = text[start_pos:]
                last_bracket = chunk.rfind('])')
                if last_bracket != -1:
                    chunk = chunk[:last_bracket+2]
            chapters[ch_num] = chunk.strip()
            
    print(f"Captured {len(chapters)} unique chapters: {sorted(chapters.keys())}")
    
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
            body.append(f"    # {n}\n    " + chapters[n])
        else:
            print(f"Missing chapter {n}!")

    full_code = header + "\n" + "\n\n".join(body) + "\n\n    return records\n"
    (OUTLINE_DIR / "vol5_specs.py").write_text(full_code, encoding="utf-8")
    print(f"vol5_specs.py generated cleanly, size: {len(full_code)} bytes")

if __name__ == "__main__":
    extract_all_vol5_chapters()
