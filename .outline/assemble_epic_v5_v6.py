# -*- coding: utf-8 -*-
"""
Assembler script: writes vol5_specs.py and vol6_specs.py from modular definitions
"""
import sys
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent
sys.path.insert(0, str(OUTLINE_DIR))

from gen_arc1 import ARC1_CHAPTERS
from gen_arc2 import ARC2_CHAPTERS
from gen_arc3 import ARC3_CHAPTERS
from gen_arc4 import ARC4_CHAPTERS
from gen_arc5 import ARC5_CHAPTERS
from gen_vol6 import VOL6_CHAPTERS

def format_beat(b):
    role, cause, actor, b_goal, action, counterforce = b[:6]
    rest = b[6:]
    formatted_args = [f'"{role}"', f'"{cause}"', f'"{actor}"', f'"{b_goal}"', f'"{action}"', f'"{counterforce}"']
    for item in rest:
        if isinstance(item, dict):
            formatted_args.append(str(item))
        else:
            # Escape inner quotes if any
            clean_item = str(item).replace('"', '\\"')
            formatted_args.append(f'"{clean_item}"')
    return f'make_beat({", ".join(formatted_args)})'

def format_ch(ch, vol_id):
    lines = []
    n = ch["n"]
    title = ch["title"]
    actors = ch["actors"]
    function = ch["function"].replace('"', '\\"')
    delta = ch["delta"].replace('"', '\\"')
    conf = ch["conf"].replace('"', '\\"')
    stakes = ch["stakes"].replace('"', '\\"')
    hook = ch["hook"].replace('"', '\\"')
    
    lines.append(f'    # {n}')
    lines.append(f'    add_ch({n}, "{vol_id}", "{title}", {actors},')
    lines.append(f'           "{function}",')
    lines.append(f'           "{delta}",')
    lines.append(f'           "{conf}",')
    lines.append(f'           "{stakes}",')
    lines.append(f'           "{hook}",')
    lines.append('           [')
    for b in ch["beats"]:
        lines.append(f'               {format_beat(b)},')
    lines.append('           ],')
    lines.append('           [')
    for s in ch["scenes"]:
        entry, goal, opp, st, act, turn, exit_st = [str(x).replace('"', '\\"') for x in s]
        lines.append(f'               make_scene("{entry}", "{goal}", "{opp}", "{st}", "{act}", "{turn}", "{exit_st}"),')
    lines.append('           ],')
    lines.append('           [')
    for c in ch["clusters"]:
        goal, med, b_indices, turn, cost, exit_st, next_p = c
        goal, med, turn, cost, exit_st, next_p = [str(x).replace('"', '\\"') for x in [goal, med, turn, cost, exit_st, next_p]]
        lines.append(f'               make_cluster("{goal}", "{med}", {b_indices}, "{turn}", "{cost}", "{exit_st}", "{next_p}"),')
    lines.append('           ])')
    lines.append('')
    return '\n'.join(lines)

def build_vol5():
    all_v5 = ARC1_CHAPTERS + ARC2_CHAPTERS + ARC3_CHAPTERS + ARC4_CHAPTERS + ARC5_CHAPTERS
    assert len(all_v5) == 44, f"Expected 44 chapters for Vol 5, got {len(all_v5)}"
    
    header = '''# -*- coding: utf-8 -*-
"""Volume 5: 万道诛仙篇 (Chapters 97..140) Deep Narrative Specifications (44 Chapters) - 100% Bespoke"""

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
    body = '\n'.join(format_ch(ch, "VOLUME.v5_taiji_battle") for ch in all_v5)
    footer = '    return records\n'
    
    out_file = OUTLINE_DIR / "vol5_specs.py"
    out_file.write_text(header + body + footer, encoding="utf-8")
    print(f"Wrote {out_file}, {len(all_v5)} chapters.")

def build_vol6():
    all_v6 = VOL6_CHAPTERS
    assert len(all_v6) == 4, f"Expected 4 chapters for Vol 6, got {len(all_v6)}"
    
    header = '''# -*- coding: utf-8 -*-
"""Volume 6: 尾声·开泰盛世篇 (Chapters 141..144) Master Epilogue & Graceful Landing (4 Chapters) - 100% Bespoke"""

def get_vol6_specs(make_beat, make_scene, make_cluster):
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
    body = '\n'.join(format_ch(ch, "VOLUME.v6_world_renewal") for ch in all_v6)
    footer = '    return records\n'
    
    out_file = OUTLINE_DIR / "vol6_specs.py"
    out_file.write_text(header + body + footer, encoding="utf-8")
    print(f"Wrote {out_file}, {len(all_v6)} chapters.")

if __name__ == "__main__":
    build_vol5()
    build_vol6()
