# -*- coding: utf-8 -*-
"""
Independent Multi-Dimensional Quality Validator for Tianque Outline
Enforces Generator != Critic principle.
"""

import json
import re
from collections import Counter
from pathlib import Path

ALLIES = {
    "CHAR.gu_jinglan", "CHAR.ye_polu", "CHAR.jiang_sui", "CHAR.ye_tingxue",
    "CHAR.shen_qinghuang", "CHAR.pei_luoshuang", "CHAR.leng_yue",
    "CHAR.xiao_minghuang", "CHAR.han_tie", "CHAR.lu_song"
}

ALLIE_NAMES = ["顾惊澜", "叶破虏", "姜素衣", "夜听雪", "沈倾凰", "裴落霜", "冷月", "萧明凰", "韩铁", "陆松"]

DEAD_TIMELINE = {
    "CHAR.zhao_xuan": 2,
    "CHAR.zhao_biao": 4,
    "CHAR.zhao_wuji": 13,
    "CHAR.wu_titian": 36,
    "CHAR.qian_wanjin": 42,
    "CHAR.zhao_wenzhao": 42,
    "CHAR.wan_yan_badu": 56,
    "CHAR.tianhuo_zhenren": 62,
    "CHAR.zhao_tianlong": 81,
    "CHAR.yan_songqing": 92,
    "CHAR.xiao_qianyuan": 106,
    "CHAR.xuanyin_laozu": 111,
    "CHAR.taixuzi": 114,
    "CHAR.wuchenzi": 120,
    "CHAR.lu_song": 106,
}

FORBIDDEN_ALLIE_PATTERNS = [
    r"搜取.*随身密档.*喝破.*滔天罪行",
    r".*残部心理防线全线崩塌跪地求饶",
    r"依法宣判斩首处决.*",
    r".*被押上断头台首级落地",
    r".*跪地求饶愿献出.*私藏.*求饶",
    r"剥夺.*一切政治道德伪装",
]

def validate_packet_thoroughly(packet_path: Path):
    errors = []
    warnings = []
    
    with open(packet_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
        
    entities = {e["id"]: e for e in packet.get("entities", [])}
    chapter_plans = [e for e in entities.values() if e.get("kind") == "CHAPTER_PLAN"]
    chapter_plans.sort(key=lambda x: x["payload"]["chapter_no"])
    
    if len(chapter_plans) != 144:
        errors.append(f"Chapter count mismatch: expected 144, got {len(chapter_plans)}")
        
    # 1. Check Character Lifecycle State-Gate
    for ch in chapter_plans:
        p = ch["payload"]
        c_no = p["chapter_no"]
        title = ch.get("name", "")
        
        # Check active actors in beats
        for b in p.get("dynamic_beats", []):
            actor = b.get("active_actor")
            if actor in DEAD_TIMELINE and c_no > DEAD_TIMELINE[actor]:
                errors.append(f"Ch {c_no} ({title}): Dead actor {actor} acting in beat {b.get('beat_id')}")
                
            # Check for forbidden ally subjugation phrases
            act_str = b.get("action", "")
            cnt_str = b.get("counterforce", "")
            full_text = f"{act_str} {cnt_str}"
            
            for ally_name in ALLIE_NAMES:
                if f"搜取{ally_name}随身密档" in full_text or f"喝破{ally_name}滔天罪行" in full_text:
                    errors.append(f"Ch {c_no} ({title}): Ally {ally_name} subjected to criminal search/indictment in beat {b.get('beat_id')}")
                if f"{ally_name}残部心理防线全线崩塌跪地求饶" in full_text or f"{ally_name}跪地求饶" in full_text:
                    errors.append(f"Ch {c_no} ({title}): Ally {ally_name} kneeling/begging for mercy in beat {b.get('beat_id')}")
                if f"斩首处决{ally_name}" in full_text or f"{ally_name}被押上断头台" in full_text:
                    errors.append(f"Ch {c_no} ({title}): Ally {ally_name} sentenced to execution in beat {b.get('beat_id')}")
                    
    # 2. Template Fingerprint Repetition Check (N-gram scan)
    beat_actions = []
    beat_counters = []
    scene_entries = []
    
    for ch in chapter_plans:
        p = ch["payload"]
        for b in p.get("dynamic_beats", []):
            beat_actions.append(b.get("action", ""))
            beat_counters.append(b.get("counterforce", ""))
        for s in p.get("scene_payloads", []):
            scene_entries.append(s.get("entry_state", ""))
            
    # Check exact phrase repetition across all beats
    all_phrases = []
    for text in beat_actions + beat_counters:
        # Extract 10-char substrings
        for i in range(len(text) - 9):
            sub = text[i:i+10]
            if not any(name in sub for name in ALLIE_NAMES + ["赵无极", "钱万金", "严嵩卿", "赵天龙", "萧乾元", "无尘子", "完颜拔都", "太虚子", "玄阴老祖", "天火真人", "乌啼天"]):
                all_phrases.append(sub)
                
    counts = Counter(all_phrases)
    bad_repeats = {k: v for k, v in counts.items() if v > 5}
    if bad_repeats:
        top_bad = sorted(bad_repeats.items(), key=lambda x: x[1], reverse=True)[:5]
        errors.append(f"Repetitive template fingerprints detected (>5 times): {top_bad}")
        
    # Check repetitive scenes
    scene_counts = Counter(scene_entries)
    for sc_name, cnt in scene_counts.items():
        if cnt > 3:
            errors.append(f"Scene entry repeated {cnt} times: '{sc_name}'")
            
    # 3. Check Spatial Continuity
    for ch in chapter_plans:
        p = ch["payload"]
        c_no = p["chapter_no"]
        v_ref = p.get("volume_ref", "")
        
        for s in p.get("scene_payloads", []):
            entry = s.get("entry_state", "")
            if "省府巡抚衙门公堂" in entry and c_no > 24:
                errors.append(f"Ch {c_no} ({v_ref}): Qingzhou Yamen appears in later volume scene: {entry}")
            if "幽静摘星楼露台" in entry and (c_no < 97 or c_no > 140):
                warnings.append(f"Ch {c_no}: Zhaixing Tower appears outside imperial city victory arc: {entry}")
                
    # 4. Referential Integrity Check
    volumes = [e for e in entities.values() if e.get("kind") == "VOLUME"]
    for v in volumes:
        p = v["payload"]
        v_name = v.get("name", "")
        tps = p.get("turning_points", [])
        for tp in tps:
            m = re.search(r"第(\d+)章", tp)
            if m:
                ch_num = int(m.group(1))
                if not any(cp["payload"]["chapter_no"] == ch_num for cp in chapter_plans):
                    errors.append(f"Volume {v_name} references non-existent chapter {ch_num} in turning point: {tp}")

    return errors, warnings

if __name__ == "__main__":
    p_path = Path(__file__).parent / "tianque_packet.json"
    if p_path.exists():
        errs, warns = validate_packet_thoroughly(p_path)
        print(f"Independent Audit Complete: {len(errs)} errors, {len(warns)} warnings")
        for e in errs:
            print(f"  [ERROR] {e}")
        for w in warns[:10]:
            print(f"  [WARN] {w}")
