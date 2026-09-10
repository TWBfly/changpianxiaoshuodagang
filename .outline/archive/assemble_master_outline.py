# -*- coding: utf-8 -*-
"""
Full-scale Master Outline Assembler
Writes vol1_specs.py to vol6_specs.py and wires v2_chapter_specs.py
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

def format_ch_entry(n, vol, title, actors, function, delta_st, conf_c, stakes_c, hook_c, beats, scenes, clusters):
    code = []
    code.append(f"    # {n}")
    code.append(f"    add_ch({n}, {json.dumps(vol, ensure_ascii=False)}, {json.dumps(title, ensure_ascii=False)}, {json.dumps(actors, ensure_ascii=False)},")
    code.append(f"           {json.dumps(function, ensure_ascii=False)},")
    code.append(f"           {json.dumps(delta_st, ensure_ascii=False)},")
    code.append(f"           {json.dumps(conf_c, ensure_ascii=False)},")
    code.append(f"           {json.dumps(stakes_c, ensure_ascii=False)},")
    code.append(f"           {json.dumps(hook_c, ensure_ascii=False)},")
    
    code.append("           [")
    for b in beats:
        code.append(f"               make_beat({json.dumps(b[0], ensure_ascii=False)}, {json.dumps(b[1], ensure_ascii=False)}, {json.dumps(b[2], ensure_ascii=False)}, {json.dumps(b[3], ensure_ascii=False)}, {json.dumps(b[4], ensure_ascii=False)}, {json.dumps(b[5], ensure_ascii=False)}, {json.dumps(b[6], ensure_ascii=False)}, {json.dumps(b[7], ensure_ascii=False)}, {json.dumps(b[8], ensure_ascii=False)}, {json.dumps(b[9], ensure_ascii=False)}),")
    code.append("           ],")
    
    code.append("           [")
    for s in scenes:
        code.append(f"               make_scene({json.dumps(s[0], ensure_ascii=False)}, {json.dumps(s[1], ensure_ascii=False)}, {json.dumps(s[2], ensure_ascii=False)}, {json.dumps(s[3], ensure_ascii=False)}, {json.dumps(s[4], ensure_ascii=False)}, {json.dumps(s[5], ensure_ascii=False)}, {json.dumps(s[6], ensure_ascii=False)}),")
    code.append("           ],")
    
    code.append("           [")
    for c in clusters:
        code.append(f"               make_cluster({json.dumps(c[0], ensure_ascii=False)}, {json.dumps(c[1], ensure_ascii=False)}, {json.dumps(c[2], ensure_ascii=False)}, {json.dumps(c[3], ensure_ascii=False)}, {json.dumps(c[4], ensure_ascii=False)}, {json.dumps(c[5], ensure_ascii=False)}, {json.dumps(c[6], ensure_ascii=False)}),")
    code.append("           ])\n")
    return "\n".join(code)

def make_vol_file(v_num, v_name, chapters_data):
    lines = [
        "# -*- coding: utf-8 -*-",
        f'"""Volume {v_num}: {v_name} Handcrafted Specifications"""',
        "",
        f"def get_vol{v_num}_specs(make_beat, make_scene, make_cluster):",
        "    records = []",
        "",
        "    def add_ch(n, vol, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_list, s_list, c_list):",
        "        records.append({",
        '            "n": n, "volume_ref": vol, "name": title, "actors": actors,',
        '            "function": function, "core_delta": delta_st, "conflict_concrete": conf_c,',
        '            "stakes_concrete": stakes_c, "hook_concrete": hook_c,',
        '            "beats_detail": b_list, "scenes_detail": s_list, "clusters_detail": c_list,',
        '            "forbidden_drift": [',
        '                "不得把本章冲突简化为单一战力数值对轰。",',
        '                "不得让任何角色凭空获得未埋设的证据、权限或救兵。",',
        '                "不得用降智反派替代本章既定逻辑闭环。"',
        "            ],",
        '            "cap_payload": {',
        '                "chapter_id": f"CHAPTER_PLAN.{n:03d}",',
        '                "final_capacity": "FULL",',
        '                "core_scenes": len(s_list),',
        '                "payload_clusters": len(c_list),',
        '                "stageable_core_beats": len(b_list),',
        '                "supporting_stageable_beats": 0,',
        '                "summary_result_beats_removed": 0,',
        '                "target_prose_range": [4000, 6000],',
        '                "mid_chapter_load": "PASS",',
        '                "writer_core_plot_invention_required": False,',
        '                "missing_middle_roles": [],',
        '                "failure_reasons": []',
        "            }",
        "        })",
        ""
    ]
    for ch_args in chapters_data:
        lines.append(format_ch_entry(*ch_args))
        
    lines.append("    return records\n")
    return "\n".join(lines)

