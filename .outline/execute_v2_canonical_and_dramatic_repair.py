# -*- coding: utf-8 -*-
"""
Execute V2 Canonical, Dramatic, and Structural Repair:
1. Fix Canon leaks: Ch 118 actor in vol5_specs.py (replace CHAR.xiao_qianyuan).
2. Fix naming bug: Ch 140 in vol6_specs.py (Xiao Minghuang is Seventh Sister, not Second Sister).
3. Remove Gu Jinglan's opening omniscience of Taixu Sect in build_and_audit.py.
4. Flesh out explicit 6-volume Master Causal Chain & Real Multi-line Collision Network.
5. Upgrade 7 Sisters to autonomous leaders with distinct permanent career paths and dignified West Lake visits.
"""

from pathlib import Path
import re

OUTLINE_DIR = Path(__file__).parent

def fix_vol5_leaks():
    v5_file = OUTLINE_DIR / "vol5_specs.py"
    v5_text = v5_file.read_text(encoding="utf-8")
    
    # Replace lingering CHAR.xiao_qianyuan in Ch 118
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '上界仙人自天门降下万道九天灭世神罚仙雷', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '上界仙人自天门降下万道九天灭世神罚仙雷', 'CHAR.wuchenzi',"
    )
    # Replace in Ch 113
    v5_text = v5_text.replace(
        "make_beat('COUNTERMOVE', '诛仙神剑引动九天灭世剑煞企图同归于尽', 'CHAR.xiao_qianyuan',",
        "make_beat('COUNTERMOVE', '诛仙神剑引动九天灭世剑煞企图同归于尽', 'CHAR.taixuzi',"
    )
    # Replace in Ch 114
    v5_text = v5_text.replace(
        'add_ch(114, "VOLUME.v5_taiji_battle", "斩杀太虚掌教尊", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(114, "VOLUME.v5_taiji_battle", "斩杀太虚掌教尊", ["CHAR.gu_jinglan", "CHAR.taixuzi"],'
    )
    # Replace in Ch 115
    v5_text = v5_text.replace(
        "make_beat('REPLAN', '萧明凰颁布圣旨创办大玄第一全民修真学院', 'CHAR.xiao_qianyuan',",
        "make_beat('REPLAN', '萧明凰颁布圣旨创办大玄第一全民修真学院', 'CHAR.xiao_minghuang',"
    )
    # Replace in Ch 116
    v5_text = v5_text.replace(
        'add_ch(116, "VOLUME.v5_taiji_battle", "荡平九峰无仙踪", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],',
        'add_ch(116, "VOLUME.v5_taiji_battle", "荡平九峰无仙踪", ["CHAR.gu_jinglan", "CHAR.wuchenzi"],'
    )
    v5_text = v5_text.replace(
        "make_beat('ACTION', '无尘剑祖身合万柄太虚残剑化作千丈剑魔扑来', 'CHAR.xiao_qianyuan',",
        "make_beat('ACTION', '无尘剑祖身合万柄太虚残剑化作千丈剑魔扑来', 'CHAR.wuchenzi',"
    )
    
    v5_file.write_text(v5_text, encoding="utf-8")
    print("Fixed lingering dead character actor IDs in vol5_specs.py")

def fix_vol6_naming_and_endings():
    v6_file = OUTLINE_DIR / "vol6_specs.py"
    v6_text = v6_file.read_text(encoding="utf-8")

    # Fix Ch 140 "二师姐萧明凰" and "二姐"
    v6_text = v6_text.replace(
        "顾惊澜一袭布衣白袍，与身披龙袍的二师姐萧明凰并肩凭栏远眺，看着漫天灯火与欢腾百姓，顾惊澜欣慰微笑道：'二姐，当年我们在天渊发下的誓言，今天终于全部实现了！'",
        "顾惊澜一袭布衣白袍，与身披日月龙袍的七师姐萧明凰并肩凭栏远眺，看着漫天灯火与欢腾百姓，顾惊澜欣慰微笑道：'七姐，当年我们在天渊发下的誓言，今天终于全部实现了！'"
    )

    # Enhance Ch 143 to emphasize independent offices + holiday gathering
    v6_text = v6_text.replace(
        "七位绝色师姐换下华丽官服换上江南素雅罗裙相伴",
        "七位绝色师姐在休沐之期换下威严官服换上江南素雅罗裙相伴"
    )
    v6_text = v6_text.replace(
        "叶破虏卸去金甲换上红色软罗裙正挽袖劈柴做饭，姜素衣白衣胜雪在院中采摘茉莉花茶，夜听雪抚琴奏响高山流水，沈倾凰素手算盘教孩童数数，冷月黑金眼罩下微笑着修剪花枝，裴落霜放下惊堂木挥毫画梅，萧明凰洗尽铅华为少帅煮茶",
        "叶破虏自九边要塞休沐回杭换上素雅罗裙与少帅切磋战阵，姜素衣在院中为天下医学院培育新茶，夜听雪主持江南驿网，沈倾凰核算国家金钞储备，冷月巡视边防暗桩归来，裴落霜研磨根本宪章，萧明凰微服出宫数日为师弟煮茶"
    )
    v6_text = v6_text.replace(
        "七位师姐此生唯一心愿便是相伴少帅白头偕老",
        "七位师姐各自担负国家重任，休沐之期齐聚西湖与少帅煮茶相伴，情感圆满与社会责任并行不悖"
    )

    v6_file.write_text(v6_text, encoding="utf-8")
    print("Fixed naming bug and upgraded sister independent life paths in vol6_specs.py")

def fix_build_and_audit_canon_and_lines():
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")

    # Fix Gu Jinglan's knowledge state (remove early omniscience)
    old_knowledge = '"通晓大玄十三州山河地理与太虚仙宗万年吸血内幕"'
    new_knowledge = '"出山初期仅掌握当年灭门现场遗留的黑市断箭与神秘血契残卷，误以为赵无极即唯一主谋；随后在各卷战斗与证据拼图中逐层升级世界认知（赵无极白手套 -> 钱万金洗钱 -> 严嵩卿卖国 -> 萧乾元血祭 -> 太虚仙宗万年吸血天梯）"'
    b_text = b_text.replace(old_knowledge, new_knowledge)

    # Rebuild Master Causal Chain and N-Lines
    old_lines_snippet = '''    lines = [
        entity("LINE.revenge", "LINE", "主线一：顾氏灭门血海深仇与因果清算", {"owner": "CHAR.gu_jinglan", "closure_condition": "斩灭伪帝萧乾元与太虚仙宗老祖，彻底昭雪顾氏忠烈", "closure_event": "EVENT.taiji_zhuxian", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.governance", "LINE", "主线二：皇权合法性重构与现代宪政体制", {"owner": "CHAR.xiao_minghuang", "closure_condition": "开泰女帝立宪，九州公议政事堂建立，君民共治天下大同", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.dragon_vein", "LINE", "主线三：破除仙宗吸血与山河龙脉解封", {"owner": "CHAR.gu_jinglan", "closure_condition": "一剑斩断飞升天梯绝地天通，大玄八万里山河龙脉彻底解封", "closure_event": "EVENT.taiji_zhuxian", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.commerce_credit", "LINE", "支线四：天下商业信用与储户产权捍卫", {"owner": "CHAR.shen_qinghuang", "closure_condition": "大玄金钞总行与平准太府建立，刚性兑付确立国家信用", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.justice_procedure", "LINE", "支线五：司法独立与程序正义信仰确立", {"owner": "CHAR.pei_luoshuang", "closure_condition": "悬剑司司法独立审判，华山立宪将至尊武力置于根本宪法之下", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.defense_border", "LINE", "支线六：九边国防安全与退役将士归宿", {"owner": "CHAR.ye_polu", "closure_condition": "扫平漠北狼庭与东海海寇，老兵妥善屯田安置，九边稳固三十年", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
    ]'''

    new_lines_snippet = '''    lines = [
        entity("LINE.revenge", "LINE", "主线一：顾氏灭门血海深仇与剥洋葱因果清算", {
            "owner": "CHAR.gu_jinglan",
            "independent_goal": "从青州白手套查起，逐层追查当年灭门出资端、执行端、法统端与修仙神权源头，昭雪顾氏忠烈",
            "obstacle": "每杀一个执行者，发现其背后均被更大体系保护，强杀将引爆社会灾难",
            "failure_state": "若沦为纯粹私刑滥杀，将失去大义支持并沦为天下公敌",
            "climax_trigger": "第92章菜市口公审严党、第106章太虚主峰诛灭萧乾元魔魂",
            "collision_points": ["第37-39章与裴落霜司法程序冲突", "第49-51章与沈倾凰商业信用冲突"],
            "closure_condition": "斩灭伪帝萧乾元与太虚仙宗老祖，彻底昭雪顾氏忠烈",
            "closure_event": "EVENT.taiji_zhuxian",
            "status": "CLOSED",
            "provenance_refs": SOURCE
        }),
        entity("LINE.governance", "LINE", "主线二：皇权合法性重构与现代宪政立宪", {
            "owner": "CHAR.xiao_minghuang",
            "independent_goal": "打破皇室血祭与君主专制旧制，建立九州公议政事堂与君民共治立宪新政",
            "obstacle": "旧朝三百年世袭勋贵门阀与封建士大夫集团以国家停摆为要挟殊死抵抗",
            "failure_state": "若妥协则重回封建人治苛政，若激进则全国行政中枢瘫痪",
            "climax_trigger": "第121章太和殿践祚登基、第134章华山论道立宪誓约",
            "collision_points": ["第122章辞官逼宫危机", "第135章公议政事堂否决军费预算"],
            "closure_condition": "开泰女帝立宪，九州公议政事堂建立，君民共治天下大同",
            "closure_event": "EVENT.tianyuan_guiyin",
            "status": "CLOSED",
            "provenance_refs": SOURCE
        }),
        entity("LINE.dragon_vein", "LINE", "主线三：破除仙宗吸血与八万里山河龙脉解封", {
            "owner": "CHAR.gu_jinglan",
            "independent_goal": "摧毁万年来修仙宗门抽取人间十三州气运的飞升天梯，实现天下万古绝地天通",
            "obstacle": "仙宗将三百万凡人魂线与九天诛仙剑煞捆绑于护山大阵，强攻将导致生灵涂炭",
            "failure_state": "凡间灵气被抽干化为焦土，人道永世沦为修仙血食药田",
            "climax_trigger": "第116章自斩医道诛无尘子、第118章一剑斩断十万丈飞升天梯",
            "collision_points": ["第97章三百万魂线剥离两难", "第111章以身补天境界跌落"],
            "closure_condition": "一剑斩断飞升天梯绝地天通，大玄八万里山河龙脉彻底解封",
            "closure_event": "EVENT.taiji_zhuxian",
            "status": "CLOSED",
            "provenance_refs": SOURCE
        }),
        entity("LINE.commerce_credit", "LINE", "支线四：天下商业信用与储户产权神圣捍卫", {
            "owner": "CHAR.shen_qinghuang",
            "independent_goal": "确立民间储户资产神圣不可侵犯，建立大玄金钞总行与平准太府刚性兑付信用",
            "obstacle": "江南八大家恶意抽空粮食操纵粮价，战时国家政权企图强制无偿征用民间储备",
            "failure_state": "钱庄体系全面挤兑崩塌，三十万储户破产跳河，商业信用归零",
            "climax_trigger": "第42章西市公审首富钱万金、第123章平息全国金钞挤兑风潮",
            "collision_points": ["第27章阻止少帅拔剑杀商", "第50章拒绝战时强制征粮支持带息国债"],
            "closure_condition": "大玄金钞总行与平准太府建立，刚性兑付确立国家信用",
            "closure_event": "EVENT.tianyuan_guiyin",
            "status": "CLOSED",
            "provenance_refs": SOURCE
        }),
        entity("LINE.justice_procedure", "LINE", "支线五：司法独立与程序正义铁律确立", {
            "owner": "CHAR.pei_luoshuang",
            "independent_goal": "确立'法律面前人人平等、天子与仙人犯法与庶民同罪'之独立司法体系",
            "obstacle": "极道武力私刑冲动、封建特权庇护、法官受贿与刑讯逼供伪证",
            "failure_state": "司法沦为掌权者报复政敌的私刑工具，冤狱丛生法统崩坏",
            "climax_trigger": "第80章菜市口公审严党核心、第127章科举舞弊案依律盲审重考",
            "collision_points": ["第39章拒绝少帅私刑要求证据闭环", "第77章拒绝冷月刑讯逼供口供"],
            "closure_condition": "悬剑司司法独立审判，华山立宪将至尊武力置于根本宪法之下",
            "closure_event": "EVENT.tianyuan_guiyin",
            "status": "CLOSED",
            "provenance_refs": SOURCE
        }),
        entity("LINE.defense_border", "LINE", "支线六：九边国防安全与退役将士万世归宿", {
            "owner": "CHAR.ye_polu",
            "independent_goal": "击退漠北八十万蛮军与东海海寇，保障三十万幽燕将士抚恤，筑牢国家永恒界碑",
            "obstacle": "朝廷兵部三年克扣军粮军饷、严嵩卿借敌自重通敌卖国、大军冰雪断炊",
            "failure_state": "北境天狼关沦陷，汉家千里江山沦为蛮族屠宰场",
            "climax_trigger": "第58章绝魂谷斩帅、第65章狼居胥山封狼居胥祭忠烈",
            "collision_points": ["第56章绝魂谷大军断粮危局", "第135章公议堂军费削减妥协"],
            "closure_condition": "扫平漠北狼庭与东海海寇，老兵妥善屯田安置，九边稳固三十年",
            "closure_event": "EVENT.tianyuan_guiyin",
            "status": "CLOSED",
            "provenance_refs": SOURCE
        }),
    ]'''

    b_text = b_text.replace(old_lines_snippet, new_lines_snippet)

    b_file.write_text(b_text, encoding="utf-8")
    print("Rebuilt Master Causal Chain & N-Lines in build_and_audit.py")

def main():
    fix_vol5_leaks()
    fix_vol6_naming_and_endings()
    fix_build_and_audit_canon_and_lines()

if __name__ == "__main__":
    main()
