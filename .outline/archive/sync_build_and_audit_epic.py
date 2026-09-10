# -*- coding: utf-8 -*-
"""
Update build_and_audit.py metadata to perfectly align with:
- Volume 5: Chapters 97..140 (44 Chapters of Epic Final Immortal War)
- Volume 6: Chapters 141..144 (4 Chapters of Master Epilogue & Graceful Landing)
"""
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent
b_file = OUTLINE_DIR / "build_and_audit.py"
b_text = b_file.read_text(encoding="utf-8")

# 1. Update Volume 5 & Volume 6 metadata
v5_old = """        entity("VOLUME.v5_taiji_battle", "VOLUME", "第五卷·万道诛仙·太极绝巅弑群仙", {
            "chapter_start": 97, "chapter_end": 140,
            "central_conflict": "人间极道正气与万民意志 vs 魔化长生伪帝与超然吸血仙宗",
            "detailed_plot": "魔化伪帝逃入太虚启动三百万凡人魂线大阵。第106章独臂老仆陆松舍身挡下心魔自爆壮烈牺牲，顾惊澜悲愤狂化一拳轰碎萧乾元魔道神魂彻底除名！第111章玄阴老祖灭世，顾惊澜以身化日补天耗尽精元境界跌落；第113章惊龙剑斩断诛仙剑；第116章顾惊澜燃烧太乙金针医道本命真元一剑斩灭无尘子除名仙宗；第118章一剑斩断飞升吸血天梯绝地天通，凡人主宰人间乾坤！",
            "turning_points": "第98章纯阳破天碎七星阵、第106章陆松壮烈牺牲灭杀萧乾元神魂、第111章舍身补天境界跌落、第113章斩碎太虚神镜削断诛仙剑、第116章燃烧金针医道诛杀无尘子、第118章一剑斩断飞升天梯绝地天通、第120章天下四海归心",
            "payoff": "伪帝与太虚仙宗彻底覆灭，终结万年吃人神话，释放天下气运，全书终极强敌全灭",
            "next_hook": "旧皇朝瓦解天下百废待兴，需要新帝践祚重定乾坤开启万象维新",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v6_world_renewal", "VOLUME", "尾声·开泰盛世·重铸乾坤逍遥仙", {
            "chapter_start": 141, "chapter_end": 144,
            "central_conflict": "救世主自我解构与现代宪政体制确立 vs 旧权力惯性与至尊特权自省",
            "detailed_plot": "第121章萧明凰践祚登基为开泰女帝，册封顾惊澜镇国至尊龙尊帝师。展开12场深刻制度压力测试：第122章300勋贵辞职逼宫平民接管、第123章黄金刚性兑付平息金钞挤兑、第124章正阳门公祭将陆松染血残玉断刀安放主位点燃永恒长明灯、第125章反腐纠错法官当众道歉、第126章巨炮炸膛整顿将作铁律、第127章考卷调换少帅克制私刑依律盲审重考、第128章贯通三千里运河、第129章药王谷砸盘推行国帑定额补贴五成务实医保、第130章误伤商队立执法红线、第131章老兵争水修共济渠、第132章三大藩王削兵留爵返税三成、第133章查处假模范县立暗访制。第134章华山论道少帅神剑插石立誓至尊违宪天下共诛、第135章公议政事堂否决军费女帝从容接受。第136章辞去摄政龙王归隐西湖。第144章西湖茶楼听书大圆满终！",
            "turning_points": "第121章开泰女帝践祚登基册封至尊帝师、第124章正阳门公祭陆松点燃万年长明灯、第127章科举舞弊克制私刑确立程序正义、第134章华山论道神剑插石宪政立国、第136章辞去摄政龙王发表天下人之天下演说、第144章西湖茶楼说书惊龙神话大结局",
            "payoff": "人间公理法度确立，救世主自我解构还政于民，所有角色圆满闭环，神仙眷侣逍遥四海",
            "next_hook": "人间烟火正浓，神仙眷侣笑看九州万家灯火，全书大圆满完！",
            "provenance_refs": SOURCE,
        }),"""

v5_new = """        entity("VOLUME.v5_taiji_battle", "VOLUME", "第五卷·万道诛仙·太极绝巅弑群仙", {
            "chapter_start": 97, "chapter_end": 140,
            "central_conflict": "人间极道正气与万民意志 vs 魔化长生伪帝、万年太虚仙宗与上界真仙投影",
            "detailed_plot": "少帅率师门攻入太虚九峰展开44章超级大决战。第97章神念化解三百万凡人魂线危机；第103章萧乾元魔相毕露，第106章老仆陆松舍身挡煞壮烈牺牲，少帅悲愤灭杀萧乾元神魂！第108-111章玄阴老祖出世，少帅以身补天斩玄阴，境界跌落；第113-114章斩断诛仙剑斩杀掌尊太虚子！第116-120章上界真仙降下九天灭世神罚雷，少帅自斩医道燃烧本命金针弑真仙斩无尘仙尊！第121-132章收编万仙、平定九峰、释放灵田、道藏开普学；第133-135章一剑斩断万丈飞升吸血天梯，绝地天通，八万里龙脉归还九州大地；第136-140章十万将士祭英烈，万仙跪伏万邦来朝，大决战全胜凯旋！",
            "turning_points": "第97章神念化解三百万凡人魂线、第106章陆松舍身挡煞壮烈牺牲灭萧乾元、第111章舍身化日补天斩玄阴老祖、第114章折诛仙剑斩掌尊太虚子、第119章自斩医道燃金针弑真仙斩无尘、第133章一剑斩断万丈飞升天梯绝地天通、第135章八万里龙脉还九州、第140章大决战全胜凯旋",
            "payoff": "伪帝、太虚仙宗与上界黑手彻底覆灭，终结万年吸血神话，释放天下气运，全书终极强敌全灭",
            "next_hook": "弑仙大决战全胜凯旋，天下迎来新朝建立与盛世大圆满定格",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v6_world_renewal", "VOLUME", "尾声·开泰盛世·重铸乾坤逍遥仙", {
            "chapter_start": 141, "chapter_end": 144,
            "central_conflict": "救世主自我解构与法治立宪确立 vs 旧人治惯性与神明落幕凡尘归隐",
            "detailed_plot": "全书4章神级后日谈与大圆满收官：第141章萧明凰在太和殿正式登基为开泰女帝，正阳门举行国家公祭将老仆陆松染血残玉断刀安放忠烈主位点燃永恒长明灯，顾家满门彻底昭雪天下；第142章华山绝顶召开九州万民大会，少帅将惊龙天剑永插天柱石立宪至尊受宪，辞去一切特权还政于民；第143章七师姐各自领受国家使命坚守独立信仰，西湖草堂白壁立下空空剑架；第144章临安西湖老茶馆内说书先生开讲《天阙惊龙传》，窗外烟雨江南万家灯火，师姐弟相视一笑饮尽春茶，全书大圆满完结！",
            "turning_points": "第141章太和殿女帝登基公祭陆松点燃长明灯、第142章华山绝顶神剑插石立宪至尊受宪、第143章七师姐各自独立领命西湖立空剑架、第144章西湖老茶馆说书惊龙传全书大圆满",
            "payoff": "人间公理法度确立，救世主自我解构还政于民，所有角色圆满闭环，神仙眷侣逍遥四海",
            "next_hook": "烟雨江南万家灯火，神仙眷侣笑看九州锦绣山河，全书大圆满完！",
            "provenance_refs": SOURCE,
        }),"""

b_text = b_text.replace(v5_old, v5_new)

# 2. Update LINE climax triggers and collision points
b_text = b_text.replace('"第121章太和殿践祚登基、第134章华山论道立宪誓约"', '"第141章太和殿践祚登基、第142章华山绝顶立宪誓约"')
b_text = b_text.replace('["第122章辞官逼宫危机", "第135章公议政事堂否决军费预算"]', '["第80章皇城除奸冲突", "第142章万民大会还政于民"]')
b_text = b_text.replace('"第116章自斩医道诛无尘子、第118章一剑斩断十万丈飞升天梯"', '"第118-120章自斩医道弑真仙诛无尘子、第133-134章一剑斩断万丈飞升天梯绝地天通"')
b_text = b_text.replace('"第123章平息全国金钞挤兑风潮"', '"第124章调运仙山存粮救济万民"')
b_text = b_text.replace('"第127章科举舞弊案依律盲审重考"', '"第123章确立宗门资产收归国有律、第127章万仙除籍登记凡俗户籍"')

# 3. Update PROMISES
b_text = b_text.replace('"第13-124章"', '"第13-141章"')
b_text = b_text.replace('"第38-123章"', '"第38-141章"')
b_text = b_text.replace('"第65-131章"', '"第65-141章"')
b_text = b_text.replace('"第118-120章"', '"第133-135章"')
b_text = b_text.replace(
    'entity("PROMISE.p16", "PROMISE", "三百世袭勋贵免死铁券收缴与平民科举接管", {"creation_event": "EVENT.nvdi_dengji", "maturity_condition": "乾清宫朱批准奏与天宝阁封存", "reveal_window": "第121-122章", "payoff_event": "EVENT.nvdi_dengji", "status": "PAID_OFF", "provenance_refs": SOURCE}),',
    'entity("PROMISE.p16", "PROMISE", "太虚仙门资产收归国家法统与灵田还耕", {"creation_event": "EVENT.taiji_zhuxian", "maturity_condition": "查封万年仙藏并向平民还耕", "reveal_window": "第123-128章", "payoff_event": "EVENT.taiji_zhuxian", "status": "PAID_OFF", "provenance_refs": SOURCE}),'
)
b_text = b_text.replace(
    'entity("PROMISE.p17", "PROMISE", "开泰金钞刚性兑付与二十万传统漕运船夫转岗", {"creation_event": "EVENT.nvdi_dengji", "maturity_condition": "平息纸钞挤兑与大运河工业转型", "reveal_window": "第123-128章", "payoff_event": "EVENT.nvdi_dengji", "status": "PAID_OFF", "provenance_refs": SOURCE}),',
    'entity("PROMISE.p17", "PROMISE", "绝地天通与八万里龙脉归还神州万民", {"creation_event": "EVENT.taiji_zhuxian", "maturity_condition": "释放龙脉与天地元气归还人间", "reveal_window": "第133-135章", "payoff_event": "EVENT.taiji_zhuxian", "status": "PAID_OFF", "provenance_refs": SOURCE}),'
)
b_text = b_text.replace('"第134-135章"', '"第142章"')
b_text = b_text.replace('"第136-143章"', '"第143章"')

# 4. Update CLIMAX and EVENT chapters
b_text = b_text.replace('"第五卷高潮：陆松牺牲灭萧乾元，自斩医道诛无尘子，斩断飞升天梯绝地天通", {"chapter": 118,', '"第五卷高潮：陆松牺牲灭萧乾元，自斩医道诛无尘子，斩断飞升天梯绝地天通", {"chapter": 133,')
b_text = b_text.replace('"第六卷高潮：华山论道神剑立誓，少帅辞去摄政龙王归隐西湖大团圆", {"chapter": 144,', '"第六卷高潮：华山绝顶神剑立誓，少帅辞去摄政特权归隐西湖大团圆", {"chapter": 142,')

b_text = b_text.replace('("EVENT.taiji_zhuxian", "太虚主峰决战与绝地天通", "CHAR.gu_jinglan", 118,', '("EVENT.taiji_zhuxian", "太虚主峰决战与绝地天通", "CHAR.gu_jinglan", 133,')
b_text = b_text.replace('("EVENT.nvdi_dengji", "开泰女帝践祚大典", "CHAR.xiao_minghuang", 121,', '("EVENT.nvdi_dengji", "开泰女帝践祚大典", "CHAR.xiao_minghuang", 141,')

b_file.write_text(b_text, encoding="utf-8")
(OUTLINE_DIR / "generate_build_script.py").write_text(b_text, encoding="utf-8")
print("Synchronized build_and_audit.py metadata successfully.")
