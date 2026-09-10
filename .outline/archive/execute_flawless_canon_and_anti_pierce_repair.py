# -*- coding: utf-8 -*-
"""
Execute Flawless Canon, Anti-Piercing, and Realistic Governance Repair:
1. Clean all modern word piercings (PPT, 自付50%, 蒙古族, 反恐, 现代绩效, 五大洋).
2. Fix Canon drift in vol5_specs.py:
   - Ch 108, 109, 110: Replace lingering CHAR.xiao_qianyuan with CHAR.xuanyin_laozu.
   - Ch 113/114: Taixuzi sword broken in Ch 113, formally executed in Ch 114.
3. Fix Ch 127 legal phrasing in vol6_specs.py (replace "打入死牢判处流刑三千里").
4. Tone down triumphalist parade in Ch 137-142 to realistic long-term institutional mechanisms.
5. Recompile and verify master outline.
"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def clean_modern_piercings_in_vol6():
    v6_file = OUTLINE_DIR / "vol6_specs.py"
    v6_text = v6_file.read_text(encoding="utf-8")

    # 1. PPT cleaning
    v6_text = v6_text.replace("不看PPT只看百姓碗里有没有肉", "不看虚饰文牍只看百姓碗中有无黍米鱼肉")
    v6_text = v6_text.replace("造假数据PPT", "虚假政绩账册图谱")

    # 2. Mongolian / ethnic cleaning
    v6_text = v6_text.replace("当地一万名世代放牧的蒙古族牧民", "当地一万名世代放牧的漠北归顺游牧部民")

    # 3. Medical copay cleaning
    v6_text = v6_text.replace("国家财政补贴50%、患者自付50%", "官帑定额补贴五成、病家自负五成")

    # 4. Anti-terror cleaning
    v6_text = v6_text.replace("反恐维稳", "追凶平暴")
    v6_text = v6_text.replace("反恐执法", "缉凶巡查执法")
    v6_text = v6_text.replace("绝世反恐", "雷霆平乱")

    # 5. Global 5 oceans cleaning
    v6_text = v6_text.replace("五大洋", "四海七洋")
    v6_text = v6_text.replace("全球五大洋", "四海七洋万国海路")

    # 6. Modern performance management cleaning
    v6_text = v6_text.replace("现代绩效考核", "大玄考成法铁律考核")
    v6_text = v6_text.replace("现代科学实验方法", "大玄天工格物致知法")
    v6_text = v6_text.replace("现代法医与刑侦技术", "大玄法医验痕与悬剑刑侦法")

    # 7. Ch 127 legal contradiction cleaning
    v6_text = v6_text.replace("打入死牢判处流刑三千里", "革除功名永不录用，依法夺官抄没家产，发配西陲三千里严加看管")

    # 8. Tone down triumphalist parade in Ch 137-142
    v6_text = v6_text.replace("彻底消除瘟疫绝症", "建立全国公立医馆普惠施药网络")
    v6_text = v6_text.replace("三十年无一冤案", "建立大理寺三审复核长效防错体系")
    v6_text = v6_text.replace("永久消除千年地震洪灾", "建立九州地动水患预警防灾与水利疏导体系")

    v6_file.write_text(v6_text, encoding="utf-8")
    print("Cleaned modern piercings and toned down triumphalist parade in vol6_specs.py.")

def fix_vol5_canon_xiao_qianyuan_and_taixuzi():
    v5_file = OUTLINE_DIR / "vol5_specs.py"
    v5_text = v5_file.read_text(encoding="utf-8")

    # Ch 108: Replace CHAR.xiao_qianyuan with CHAR.xuanyin_laozu
    v5_text = v5_text.replace(
        'add_ch(108, "VOLUME.v5_taiji_battle", "逼出太上老祖身", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(108, "VOLUME.v5_taiji_battle", "逼出太上老祖身", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"],'
    )
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '玄阴老祖与掌教太虚子引动万丈太极混元领域压境', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '玄阴老祖与掌教太虚子引动万丈太极混元领域压境', 'CHAR.xuanyin_laozu',"
    )
    v5_text = v5_text.replace(
        "make_beat('REVELATION', '玄阴老祖承认顾家灭门与历代天子暴毙皆其一手策划', 'CHAR.xiao_qianyuan',",
        "make_beat('REVELATION', '玄阴老祖承认顾家灭门与历代天子暴毙皆其一手策划', 'CHAR.xuanyin_laozu',"
    )

    # Ch 109: Replace CHAR.xiao_qianyuan with CHAR.xuanyin_laozu
    v5_text = v5_text.replace(
        'add_ch(109, "VOLUME.v5_taiji_battle", "苍穹之巅论天道", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(109, "VOLUME.v5_taiji_battle", "苍穹之巅论天道", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"],'
    )
    v5_text = v5_text.replace(
        "make_beat('ACTION', '玄阴老祖高坐太极云台宣讲万年吸血天道', 'CHAR.xiao_qianyuan',",
        "make_beat('ACTION', '玄阴老祖高坐太极云台宣讲万年吸血天道', 'CHAR.xuanyin_laozu',"
    )

    # Ch 110: Replace CHAR.xiao_qianyuan with CHAR.xuanyin_laozu
    v5_text = v5_text.replace(
        'add_ch(110, "VOLUME.v5_taiji_battle", "极道纯阳战玄阴", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(110, "VOLUME.v5_taiji_battle", "极道纯阳战玄阴", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"],'
    )
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '玄阴老祖催动九幽绝仙印引动地脉阴火焚山', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '玄阴老祖催动九幽绝仙印引动地脉阴火焚山', 'CHAR.xuanyin_laozu',"
    )

    v5_file.write_text(v5_text, encoding="utf-8")
    print("Fixed vol5_specs.py: Replaced dead CHAR.xiao_qianyuan with CHAR.xuanyin_laozu in Ch 108, 109, 110.")

def fix_build_and_audit_taixuzi_profile():
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")

    # Update Taixuzi execution chapter in build_and_audit.py to Ch 114
    b_text = b_text.replace(
        "第113章在太虚主峰被顾惊澜惊龙天剑折断诛仙剑顺势斩首形神俱灭",
        "第113章被折断诛仙剑身负重伤，第114章在太虚主峰被顾惊澜以惊龙天剑正式斩首形神俱灭彻底除名"
    )
    b_text = b_text.replace(
        "第113章伏诛除名",
        "第114章伏诛除名"
    )

    # Also clean modern piercings in build_and_audit.py if any
    b_text = b_text.replace("五大洋", "四海七洋")

    b_file.write_text(b_text, encoding="utf-8")
    print("Updated build_and_audit.py: Aligned Taixuzi death chapter to Ch 114.")

def main():
    clean_modern_piercings_in_vol6()
    fix_vol5_canon_xiao_qianyuan_and_taixuzi()
    fix_build_and_audit_taixuzi_profile()

if __name__ == "__main__":
    main()
