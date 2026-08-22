# -*- coding: utf-8 -*-
"""
Execute Flawless Canon Freeze & Structural Polishing:
1. Fix P0-1: Split Zhao Tianlong -> Zhao Wenzhao (Jiangnan Governor, executed Ch 42) vs Zhao Tianlong (Imperial Uncle, executed Ch 81).
2. Fix P0-4: Jinglong Heavenly Sword permanently at Mount Hua, West Lake cottage has empty sword rack.
3. Fix Spatial Continuity: Ch 65 location set to Shanhaiguan / Yanmen Pass Memorial instead of Langjuxu.
4. Add explicit Originalization Constraints in build_and_audit.py.
"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def fix_vol2_zhao_wenzhao():
    v2_file = OUTLINE_DIR / "vol2_specs.py"
    v2_text = v2_file.read_text(encoding="utf-8")

    # Replace Zhao Tianlong with Zhao Wenzhao in Jiangnan Volume
    v2_text = v2_text.replace("赵天龙", "赵文昭")
    v2_file.write_text(v2_text, encoding="utf-8")
    print("Repaired vol2_specs.py: Replaced Jiangnan Governor Zhao Tianlong with Zhao Wenzhao")

def fix_vol3_spatial_ch65():
    v3_file = OUTLINE_DIR / "vol3_specs.py"
    v3_text = v3_file.read_text(encoding="utf-8")

    # Fix Ch 65 summary
    v3_text = v3_text.replace(
        '"在狼居胥山下安葬抚恤两万伤残老兵退役，大军精简为二十八万百战精锐，顾惊澜与叶破虏长跪祭拜历代无名英烈"',
        '"在山海关南麓雁门古战场安葬抚恤两万伤残老兵退役，大军精简为二十八万百战精锐，顾惊澜与叶破虏长跪祭拜历代无名英烈"'
    )
    v3_file.write_text(v3_text, encoding="utf-8")
    print("Repaired vol3_specs.py: Fixed Ch 65 location to Shanhaiguan / Yanmen Pass")

def fix_vol6_sword_state():
    v6_file = OUTLINE_DIR / "vol6_specs.py"
    v6_text = v6_file.read_text(encoding="utf-8")

    # Fix Ch 143 sword state
    v6_text = v6_text.replace(
        "顾惊澜将惊龙天剑挂于江南别苑壁上封剑归隐，与七位绝色师姐在西湖畔安享神仙眷侣生活，武道由刚转柔臻至天人化境",
        "顾惊澜在江南别苑中堂留下空剑架洗尽铅华，惊龙神剑永镇华山宪章，与七位绝色师姐在西湖畔安享神仙眷侣生活，武道由刚转柔臻至天人化境"
    )
    v6_text = v6_text.replace(
        "顾惊澜彻底卸下人间一切重担，封剑入鞘归隐西湖，与七位师姐相伴品茗、泛舟、赏花、抚琴，武道洗尽铅华由极阳转为太极阴阳相济之化境，享受属于英雄的平凡幸福",
        "顾惊澜彻底卸下人间一切重担，两手空空归隐西湖，神剑永镇华山守护宪章，与七位师姐相伴品茗、泛舟、赏花、抚琴，武道洗尽铅华由极阳转为太极阴阳相济之化境，享受属于英雄的平凡幸福"
    )
    v6_text = v6_text.replace(
        "顾惊澜在西湖畔断桥别苑亲手挂起惊龙天剑",
        "顾惊澜在西湖畔断桥别苑中堂设立空剑架封剑归真"
    )
    v6_text = v6_text.replace(
        "江南初春烟雨朦胧，西湖畔断桥别苑小筑内，顾惊澜一身素雅青衫长袍，双手将陪伴自己七年征战的古朴惊龙天剑稳稳挂在草堂中堂白壁之上，长剑入鞘龙威内敛",
        "江南初春烟雨朦胧，西湖畔断桥别苑小筑内，顾惊澜一身素雅青衫长袍，在中堂白壁立下一个空剑架，惊龙天剑已永插华山天柱石镇守宪章，两手空空武圣归真"
    )
    v6_text = v6_text.replace(
        "亲手将惊龙天剑挂在中堂白壁封剑归真",
        "在中堂白壁设立留空剑架昭示暴力归宪封剑归真"
    )
    v6_text = v6_text.replace(
        "布衣青衫在中堂白壁挂起惊龙天剑",
        "布衣青衫在中堂白壁设立留空剑架"
    )
    v6_text = v6_text.replace(
        "青衫少帅亲手将惊龙天剑挂于草堂中堂",
        "青衫少帅在中堂设立留空剑架神剑镇华山"
    )
    v6_file.write_text(v6_text, encoding="utf-8")
    print("Repaired vol6_specs.py: Jinglong Heavenly Sword permanently at Mount Hua, West Lake has empty sword rack")

def fix_build_and_audit():
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")

    # Add CHAR.zhao_wenzhao
    if '"CHAR.zhao_wenzhao"' not in b_text:
        zhao_wenzhao_entry = '''        ("CHAR.zhao_wenzhao", "赵文昭", "江南总督/江南八大家官商勾结政治保护伞",
         "当朝国舅赵天龙派驻江南的总督大员，手握江南三省军政大权，长期包庇首富钱万金与五毒魔宗，垄断盐铁漕运。第二卷被悬剑司查封公审伏诛。",
         "垄断江南漕运暴利并向京师国舅府输送政治献金", "联合钱万金封锁临安城，对抗悬剑司独立监察",
         "江南总督大印与驻军兵权", "受制于悬剑司尚方宝剑特权与先皇密旨",
         "官官相护，以权压法，借刀杀人",
         "官僚特权与门阀利益 > 国家法统 > 百姓死活。标准的腐朽封建官僚。",
         "身穿从一品仙鹤文官锦袍，腰悬总督金印",
         "贪腐账册被钱万金密室备份",
         "通晓江南三省官场利益网络与漕运暗账",
         "误以为背靠京城国舅府便可在江南一手遮天",
         "从威震江南的一品封疆大吏，沦为三江公堂上被裴落霜宣判死罪的伏诛巨贪（第二卷第42章依法斩首除名）",
         "第二卷第42章在临安三江刑场被悬剑司依法公审斩首彻底除名",
         "总督府负隅顽抗/公堂对质面如死灰认罪画押"),
'''
        b_text = b_text.replace('        ("CHAR.zhao_tianlong",', zhao_wenzhao_entry + '        ("CHAR.zhao_tianlong",')
        print("Injected CHAR.zhao_wenzhao into build_and_audit.py")

    # Add Originalization Constraints Metadata
    if '"originalization_rules"' not in b_text:
        b_text = b_text.replace(
            '"negative_prompts": [',
            '"originalization_rules": {\n'
            '            "retainable_mechanisms": ["五维立体降维打击", "六卷介质升维Problem Morph", "七位师姐专业分工与独立人格", "救世主华山立宪自我解构"],\n'
            '            "strictly_forbidden_inheritances": ["严禁复用原作专属专有名词与独特道具", "严禁复用原作专属桥段情节顺序", "严禁复用原作专属台词与场景原案", "严禁破坏死者除名与状态机连续性"],\n'
            '        },\n'
            '        "negative_prompts": ['
        )
        print("Added explicit originalization_rules to build_and_audit.py")

    b_file.write_text(b_text, encoding="utf-8")

def main():
    fix_vol2_zhao_wenzhao()
    fix_vol3_spatial_ch65()
    fix_vol6_sword_state()
    fix_build_and_audit()

if __name__ == "__main__":
    main()
