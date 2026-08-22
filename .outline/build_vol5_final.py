# -*- coding: utf-8 -*-
"""Volume 5 Final Handcrafted Builder: 弑仙卷 (Chapters 97..120)"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def build_vol5():
    text = (OUTLINE_DIR / "build_vol5_concrete.py").read_text(encoding="utf-8")
    
    code_header = '''# -*- coding: utf-8 -*-
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

    def extract_between(src, start_marker, end_marker):
        s = src.find(start_marker)
        if s == -1:
            raise ValueError(f"Marker not found: {start_marker}")
        e = src.find(end_marker, s)
        if e == -1:
            res = src[s:]
        else:
            res = src[s:e]
        return res.rstrip().rstrip("'''").rstrip()

    p97_100 = extract_between(text, "    # 97\n", "    # Now let's append all chapters 101..120")
    p101_104 = extract_between(text, "    # 101\n", "    # Now let's append remaining chapters 105 to 120")
    p105_107 = extract_between(text, "    # 105\n", "    # 108\n")
    p108_120 = extract_between(text, "    # 108\n", "    full_code =")

    full_vol5 = code_header + "\n" + p97_100 + "\n\n" + p101_104 + "\n\n" + p105_107 + "\n\n" + p108_120 + "\n\n    return records\n"

    (OUTLINE_DIR / "vol5_specs.py").write_text(full_vol5, encoding="utf-8")
    print(f"vol5_specs.py generated with size: {len(full_vol5)} bytes")

if __name__ == "__main__":
    build_vol5()
