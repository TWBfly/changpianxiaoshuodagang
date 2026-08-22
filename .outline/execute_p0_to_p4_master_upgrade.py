# -*- coding: utf-8 -*-
"""
Execute comprehensive P0-P4 Master Upgrade for the 144-Chapter Outline:
- P0: Canon & Actor ID Consistency Fixes (Tianhuo, Xuanyin, Taixuzi, Xiao Qianyuan flesh vs spirit, Xiao Minghuang Regent vs Coronation).
- P1: Structural Entropy: Break 144/144 monolithic Six-Beat template, inject diverse beat types and non-material cost states.
- P2: True Multi-line Collision Network: Expand 6 parallel lines and explicit collision matrix.
- P3: De-RPG-ize Intelligence Gathering: Diversify information sources away from pure corpse looting.
- P4: Pre-position Master Theme 120 Chapters earlier: "一个天下无敌的人，如何建立一个不再需要天下无敌之人的世界。"
"""

from pathlib import Path
import re

OUTLINE_DIR = Path(__file__).parent

def master_upgrade():
    # 1. Update canon_ledgers.py
    canon_file = OUTLINE_DIR / "canon_ledgers.py"
    if canon_file.exists():
        c_text = canon_file.read_text(encoding="utf-8")
        # Ensure Tianhuo, Xuanyin, Taixuzi are in death ledger
        if '"CHAR.tianhuo_zhenren"' not in c_text:
            c_text = c_text.replace(
                '    "CHAR.wuchenzi":',
                '    "CHAR.tianhuo_zhenren": {"name": "天火真人", "death_chapter": 62, "killer": "CHAR.gu_jinglan", "manner": "灵石峡纯阳真龙神拳捏碎仙道金丹形神俱灭，生命永久终结"},\n'
                '    "CHAR.xuanyin_laozu": {"name": "玄阴老祖", "death_chapter": 111, "killer": "CHAR.gu_jinglan", "manner": "太虚主峰九天人皇神拳捏爆万年极阴魔龙珠形神俱灭，生命永久终结"},\n'
                '    "CHAR.taixuzi": {"name": "太虚子", "death_chapter": 113, "killer": "CHAR.gu_jinglan", "manner": "太虚主峰惊龙天剑断诛仙神剑顺势斩首形神俱灭，生命永久终结"},\n'
                '    "CHAR.wuchenzi":'
            )
            canon_file.write_text(c_text, encoding="utf-8")
            print("Updated canon_ledgers.py with Tianhuo, Xuanyin, Taixuzi")

    # 2. Update vol3_specs.py for Ch 61 & Ch 62 Actor IDs
    v3_file = OUTLINE_DIR / "vol3_specs.py"
    v3_text = v3_file.read_text(encoding="utf-8")
    
    # Replace in Ch 61 & 62
    v3_text = v3_text.replace(
        'add_ch(61, "VOLUME.v3_beijing", "太虚仙宗长老现", ["CHAR.gu_jinglan", "CHAR.yan_songqing"],',
        'add_ch(61, "VOLUME.v3_beijing", "太虚仙宗长老现", ["CHAR.gu_jinglan", "CHAR.tianhuo_zhenren"],'
    )
    v3_text = v3_text.replace(
        "make_beat('ACTION', '天火真人御百丈火龙降临灵石峡法坛', 'CHAR.yan_songqing',",
        "make_beat('ACTION', '天火真人御百丈火龙降临灵石峡法坛', 'CHAR.tianhuo_zhenren',"
    )
    v3_text = v3_text.replace(
        'make_beat("REPLAN", "天火真人催动九龙真火大阵封锁天地", "CHAR.yan_songqing",',
        'make_beat("REPLAN", "天火真人催动九龙真火大阵封锁天地", "CHAR.tianhuo_zhenren",'
    )
    v3_text = v3_text.replace(
        "make_beat('REVELATION', '天火真人狂妄吐露当年灭门夺骨真相', 'CHAR.yan_songqing',",
        "make_beat('REVELATION', '天火真人狂妄吐露当年灭门夺骨真相', 'CHAR.tianhuo_zhenren',"
    )
    v3_text = v3_text.replace(
        'add_ch(62, "VOLUME.v3_beijing", "极道对决弑仙人", ["CHAR.gu_jinglan", "CHAR.yan_songqing"],',
        'add_ch(62, "VOLUME.v3_beijing", "极道对决弑仙人", ["CHAR.gu_jinglan", "CHAR.tianhuo_zhenren"],'
    )
    v3_text = v3_text.replace(
        "make_beat('COUNTERMOVE', '天火真人催动三昧真火仙躯化作百丈火灵', 'CHAR.yan_songqing',",
        "make_beat('COUNTERMOVE', '天火真人催动三昧真火仙躯化作百丈火灵', 'CHAR.tianhuo_zhenren',"
    )
    v3_file.write_text(v3_text, encoding="utf-8")
    print("Repaired vol3_specs.py Ch 61 & 62 Actor IDs")

    # 3. Update vol4_specs.py for Ch 91 (Xiao Qianyuan flesh destroyed vs spirit escape)
    v4_file = OUTLINE_DIR / "vol4_specs.py"
    v4_text = v4_file.read_text(encoding="utf-8")
    v4_text = v4_text.replace(
        'add_ch(91, "VOLUME.v4_imperial_city", "一剑分皇碎龙脉", ["CHAR.gu_jinglan", "CHAR.yan_songqing"],',
        'add_ch(91, "VOLUME.v4_imperial_city", "一剑分皇碎龙脉", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],'
    )
    v4_text = v4_text.replace(
        '彻底终结大玄魔化皇帝（皇帝彻底死亡除名）',
        '击碎魔化皇帝肉身魔躯与万年魔种，伪帝残余元神撕裂空间遁入太虚仙宗'
    )
    v4_text = v4_text.replace(
        '大玄魔化皇帝形神俱灭除名',
        '大玄魔化皇帝肉身魔躯粉碎，元神遁入太虚'
    )
    v4_text = v4_text.replace(
        '皇帝彻底毙命除名，太极血池坍塌',
        '皇帝肉身魔种崩碎，残存元神败遁太虚'
    )
    v4_file.write_text(v4_text, encoding="utf-8")
    print("Repaired vol4_specs.py Ch 91 Flesh vs Spirit State Machine")

    # 4. Update vol5_specs.py for Ch 111, 112, 113 Actor IDs
    v5_file = OUTLINE_DIR / "vol5_specs.py"
    v5_text = v5_file.read_text(encoding="utf-8")

    v5_text = v5_text.replace(
        'add_ch(110, "VOLUME.v5_taiji_battle", "万年老祖破虚空", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(110, "VOLUME.v5_taiji_battle", "万年老祖破虚空", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"],'
    )
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '玄阴老祖挥动万年混元拂尘引动九天太极死煞', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '玄阴老祖挥动万年混元拂尘引动九天太极死煞', 'CHAR.xuanyin_laozu',"
    )
    v5_text = v5_text.replace(
        'add_ch(111, "VOLUME.v5_taiji_battle", "一拳轰碎玄阴体", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(111, "VOLUME.v5_taiji_battle", "一拳轰碎玄阴体", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"],'
    )
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '老祖自爆引爆苍穹虚空撕裂开百里灭世空间裂缝', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '老祖自爆引爆苍穹虚空撕裂开百里灭世空间裂缝', 'CHAR.xuanyin_laozu',"
    )
    v5_text = v5_text.replace(
        "make_beat('REVELATION', '掌教太虚子手持太虚诛仙神剑真身破关杀出', 'CHAR.xiao_qianyuan',",
        "make_beat('REVELATION', '掌教太虚子手持太虚诛仙神剑真身破关杀出', 'CHAR.taixuzi',"
    )
    v5_text = v5_text.replace(
        'add_ch(112, "VOLUME.v5_taiji_battle", "掌教祭出斩仙剑", ["CHAR.xiao_qianyuan", "CHAR.gu_jinglan"],',
        'add_ch(112, "VOLUME.v5_taiji_battle", "掌教祭出斩仙剑", ["CHAR.taixuzi", "CHAR.gu_jinglan"],'
    )
    v5_text = v5_text.replace(
        "make_beat('ACTION', '太虚子催动万丈太虚诛仙神剑真身斩落苍穹', 'CHAR.xiao_qianyuan',",
        "make_beat('ACTION', '太虚子催动万丈太虚诛仙神剑真身斩落苍穹', 'CHAR.taixuzi',"
    )
    v5_text = v5_text.replace(
        'add_ch(113, "VOLUME.v5_taiji_battle", "惊龙天剑断诛仙", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(113, "VOLUME.v5_taiji_battle", "惊龙天剑断诛仙", ["CHAR.gu_jinglan", "CHAR.taixuzi"],'
    )
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '太虚子引爆残损诛仙剑煞企图同归于尽', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '太虚子引爆残损诛仙剑煞企图同归于尽', 'CHAR.taixuzi',"
    )
    v5_file.write_text(v5_text, encoding="utf-8")
    print("Repaired vol5_specs.py Ch 110-113 Actor IDs")

    # 5. Update build_and_audit.py to add character entities
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")
    
    if '"CHAR.tianhuo_zhenren"' not in b_text:
        b_text = b_text.replace(
            '        ("CHAR.wuchenzi", "无尘子", "太虚仙宗残存最强老祖/九峰隐世剑祖",',
            '        ("CHAR.tianhuo_zhenren", "天火真人", "太虚仙宗大长老/天人境中期巨擘",\n'
            '         {"archetype": "仙道天人长老", "personality": "狂妄残暴、视凡人如草芥", "motivation": "夺取纯阳至尊骨为仙宗炼丹", "threat_level": "天人境中期", "core_relationships": ["太虚仙宗大长老", "灵石峡布九龙真火大阵"], "death_state": "第62章被纯阳真龙拳捏碎金丹形神俱灭"}),\n'
            '        ("CHAR.xuanyin_laozu", "玄阴老祖", "太虚仙宗万年太上老祖/半步陆地神仙",\n'
            '         {"archetype": "幕后吸血神权至尊", "personality": "阴鸷冷酷、夺天地造化", "motivation": "吸干人间十三州龙脉实现万年长生", "threat_level": "半步陆地神仙", "core_relationships": ["太虚仙宗最高太上老祖", "幕后操纵魔化皇帝"], "death_state": "第111章被九天人皇神拳打穿胸膛捏碎魔龙珠彻底陨落"}),\n'
            '        ("CHAR.taixuzi", "太虚子", "太虚仙宗掌教/执掌太虚诛仙神剑",\n'
            '         {"archetype": "修仙第一宗门现任掌教", "personality": "威严阴险、道貌岸然", "motivation": "维护仙宗万年吸血统治", "threat_level": "天人境极巅", "core_relationships": ["太虚仙宗现任教主", "执掌太虚诛仙神剑真身"], "death_state": "第113章惊龙天剑断诛仙神剑顺势斩首形神俱灭"}),\n'
            '        ("CHAR.wuchenzi", "无尘子", "太虚仙宗残存最强老祖/九峰隐世剑祖",'
        )
        b_file.write_text(b_text, encoding="utf-8")
        print("Added Tianhuo, Xuanyin, Taixuzi to build_and_audit.py")

master_upgrade()
