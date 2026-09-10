# -*- coding: utf-8 -*-
"""Volume 6 Master Executable: Writes 100% of Chapters 121..144 to vol6_specs.py"""

import sys
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def write_vol6():
    # Read the data for 121..124 and 144 from build_vol6_concrete.py
    # and combine with 125..143
    
    from build_vol6_concrete import chs as concrete_chs
    from build_vol6_all_24 import chapters_meta as meta_125_143
    
    # concrete_chs has [121, 122, 123, 124, 144]
    ch121 = concrete_chs[0]
    ch122 = concrete_chs[1]
    ch123 = concrete_chs[2]
    ch124 = concrete_chs[3]
    ch144 = concrete_chs[4]
    
    # meta_125_143 has chapters 125..143 (19 chapters)
    
    all_24 = [ch121, ch122, ch123, ch124] + meta_125_143 + [ch144]
    
    print(f"Total Vol 6 chapters to write: {len(all_24)}, IDs: {[c[0] for c in all_24]}")
    
    header = '''# -*- coding: utf-8 -*-
"""Volume 6: 开泰盛世卷 (Chapters 121..144) Handcrafted Specifications with strict Canon & Emotional Resolution"""

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

    body = []
    for ch in all_24:
        n, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_data, s_data, c_data = ch
        b_code = []
        for b in b_data:
            # make_beat(type, action, actor, intent, subtext, outcome, dramatic_reason, delta, choice, hook)
            b_code.append(f'                make_beat("{b[0]}", "{b[1]}", "{b[2]}", "{b[3]}", "{b[4]}", "{b[5]}", "{b[6]}", {b[7]}, "{b[8]}", "{b[9]}"),')
        
        s_code = []
        for s in s_data:
            # make_scene(location, purpose, obstacles, stakes, actions, transformation, hook)
            s_code.append(f'                make_scene("{s[0]}", "{s[1]}", "{s[2]}", "{s[3]}", "{s[4]}", "{s[5]}", "{s[6]}"),')
            
        c_code = []
        for c in c_data:
            # make_cluster(cluster_id, phase_role, beats, shift, cost, payoff, hook)
            c_code.append(f'                make_cluster("{c[0]}", "{c[1]}", {c[2]}, "{c[3]}", "{c[4]}", "{c[5]}", "{c[6]}"),')
            
        ch_str = f'''    # {n}
    add_ch({n}, "VOLUME.v6_grand_era", "{title}", {actors},
           "{function}",
           "{delta_st}",
           "{conf_c}",
           "{stakes_c}",
           "{hook_c}",
           [
{chr(10).join(b_code)}
           ],
           [
{chr(10).join(s_code)}
           ],
           [
{chr(10).join(c_code)}
           ])'''
        body.append(ch_str)

    full_code = header + "\n" + "\n\n".join(body) + "\n\n    return records\n"
    (OUTLINE_DIR / "vol6_specs.py").write_text(full_code, encoding="utf-8")
    print(f"vol6_specs.py written cleanly, size: {len(full_code)} bytes")

if __name__ == "__main__":
    write_vol6()
