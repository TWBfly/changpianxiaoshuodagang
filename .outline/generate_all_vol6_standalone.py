# -*- coding: utf-8 -*-
"""Standalone Volume 6 Builder with all 24 chapters self-contained"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def build_standalone_vol6():
    # Read the text of build_vol6_concrete.py and build_vol6_all_24.py to extract raw tuples
    text_concrete = (OUTLINE_DIR / "build_vol6_concrete.py").read_text(encoding="utf-8")
    text_all24 = (OUTLINE_DIR / "build_vol6_all_24.py").read_text(encoding="utf-8")
    
    # Execute the definitions inside a clean dict
    local_env = {}
    
    # Let's extract chs from build_vol6_concrete
    # In build_vol6_concrete.py, chs = [...]
    start_chs = text_concrete.find("    chs = [")
    end_chs = text_concrete.find("    # Generate Python code", start_chs)
    chs_code = text_concrete[start_chs:end_chs].strip()
    
    # In build_vol6_all_24.py, chapters_meta = [...]
    start_meta = text_all24.find("    chapters_meta = [")
    end_meta = text_all24.find("    # Add all chapters to runner_code", start_meta)
    meta_code = text_all24[start_meta:end_meta].strip()
    
    # Execute in clean scope
    exec(chs_code, {}, local_env)
    exec(meta_code, {}, local_env)
    
    concrete_chs = local_env['chs']
    meta_125_143 = local_env['chapters_meta']
    
    ch121 = concrete_chs[0]
    ch122 = concrete_chs[1]
    ch123 = concrete_chs[2]
    ch124 = concrete_chs[3]
    ch144 = concrete_chs[4]
    
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
    build_standalone_vol6()
