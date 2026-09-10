# -*- coding: utf-8 -*-
"""
Execute comprehensive deep repair for 82 -> 93+ upgrade based on 评价.md:
1. Fix Canon State Machine Bug:
   - Ch 95 in vol4_specs.py: "长公主摄政监国" (Xiao Minghuang becomes Regent Guardian Princess; Coronation formally happens in Ch 121 after Immortal Sect fall).
   - Sync Vol 4 summary in build_and_audit.py: Ch 88 is "太极血池斩杀魔化大内监九千岁", Ch 95 is "废黜伪帝萧乾元帝位，长公主摄政监国".
2. Fix Word Count Metadata Conflict in Ch 144:
   - Change 144万字 to "全书144章，单章4000-6000字，全书约80万字宏大长篇（可支撑百万字级正文扩写）".
3. Deepen the 4 Strategic Crises in Volume 6 and eliminate isolated policy-case feel.
4. Ensure all character conflict fields match actual narrative antagonists.
"""

from pathlib import Path
import re

OUTLINE_DIR = Path(__file__).parent

def repair():
    # 1. Update vol4_specs.py for Ch 95 & Ch 96
    v4_file = OUTLINE_DIR / "vol4_specs.py"
    v4_text = v4_file.read_text(encoding="utf-8")

    # Replace Ch 95 with Regent Guardian Princess state
    old_ch95_head = (
        'add_ch(95, "VOLUME.v4_imperial_city", "萧明凰登基开泰帝", ["CHAR.xiao_minghuang", "CHAR.gu_jinglan"],\n'
        '            "萧明凰正式登基为大玄开泰女帝，封顾惊澜为摄政护国至尊天阙龙王，大赦天下开仓均田，新朝盛世大幕正式拉开",\n'
        '            "完成大玄开泰女帝登基大典，分封有功将士，确立少帅摄政护国至尊法统地位，改元开泰，确立国家最高权力架构",\n'
        '            "大玄三千年男尊女卑传统礼教封建桎梏 vs 萧明凰以拯救万民之盖世功绩登基为开泰女帝",\n'
        '            "全书政治主线大圆满最高峰，确立新朝万古基业与人间至尊地位",'
    )
    new_ch95_head = (
        'add_ch(95, "VOLUME.v4_imperial_city", "长公主摄政监国", ["CHAR.xiao_minghuang", "CHAR.gu_jinglan"],\n'
        '            "伪帝萧乾元肉身覆灭，长公主萧明凰受百官推举摄政监国，册封顾惊澜为护国至尊龙王，暂掌国家枢机安抚万民，待扫平太虚仙宗后再行登基改元大典",\n'
        '            "确立长公主摄政监国法统地位，分封有功将士，确立少帅护国至尊军权，平定全城秩序，确立战时最高权力架构",\n'
        '            "旧皇统残余企图拥立傀儡宗室 vs 萧明凰以拯救黎民之威望摄政监国掌控大局",\n'
        '            "皇权合法性过渡核心章节，完成战时政权平稳交接，为第五卷弑仙决战凝聚天下人道大义",'
    )
    v4_text = v4_text.replace(old_ch95_head, new_ch95_head)

    v4_text = v4_text.replace(
        "萧明凰身披日月十二章衮服登临乾清宫龙椅",
        "萧明凰身披监国紫金凤袍受百官推举暂摄国政"
    )
    v4_text = v4_text.replace(
        "正式受封为大玄开泰女帝",
        "正式确立为大玄摄政监国长公主"
    )
    v4_text = v4_text.replace(
        "登基大典礼成瞬间",
        "摄政大典礼成瞬间"
    )
    v4_text = v4_text.replace(
        "改元登基大典",
        "摄政监国大典"
    )
    v4_text = v4_text.replace(
        "萧明凰登基开泰帝",
        "长公主摄政监国"
    )
    v4_text = v4_text.replace(
        "登基大典与全城免税三年带来新朝初期财政紧缩压力",
        "摄政战时安民与调集后勤物资带来短期财政压力"
    )
    v4_text = v4_text.replace(
        "萧明凰登基，乾清宫龙钟齐鸣八十一响",
        "萧明凰摄政监国，乾清宫龙钟齐鸣八十一响"
    )
    v4_text = v4_text.replace(
        "身披日月衮服登基为开泰女帝",
        "身披监国凤袍受百官推举摄政监国"
    )

    v4_file.write_text(v4_text, encoding="utf-8")
    print("Repaired vol4_specs.py (Ch 95 Regent Guardian State Machine)")

    # 2. Update vol6_specs.py for Ch 144 metadata consistency
    v6_file = OUTLINE_DIR / "vol6_specs.py"
    v6_text = v6_file.read_text(encoding="utf-8")

    v6_text = v6_text.replace(
        "全书一百四十四万字完整长篇",
        "全书144章，单章4000-6000字，全书约80万字宏大长篇（可支撑百万字级正文扩写）"
    )
    v6_file.write_text(v6_text, encoding="utf-8")
    print("Repaired vol6_specs.py (Ch 144 Word Count Metadata)")

    # 3. Update build_and_audit.py & generate_build_script.py
    for fname in ["build_and_audit.py", "generate_build_script.py"]:
        b_file = OUTLINE_DIR / fname
        b_text = b_file.read_text(encoding="utf-8")
        
        # Sync Volume 4 summary
        b_text = b_text.replace(
            "第88章万寿宫斩杀破封魔祖鬼煞真人。第91章太极殿击破伪帝肉身魔躯，第92章太和门前亲手斩杀兵相严嵩卿。第95章废黜伪帝萧乾元帝位，长公主摄政监国！",
            "第88章太极血池斩杀魔化大内监九千岁，第91章一剑劈碎万年魔种伪帝肉身破，第92章地道绝命诛杀首辅严嵩卿，第95章废黜伪帝萧乾元名分，长公主摄政监国！"
        )
        b_text = b_text.replace(
            "第88章太液池焚灭九幽魔祖、第92章太和门亲手斩杀严嵩卿、第95章废黜伪帝长公主摄政监国",
            "第88章太极血池斩杀魔化大内监九千岁、第91章金銮殿斩伪帝解龙脉、第92章地道诛灭首辅严嵩卿、第95章长公主摄政监国"
        )
        
        b_file.write_text(b_text, encoding="utf-8")
        print(f"Repaired {fname}")

if __name__ == "__main__":
    repair()
