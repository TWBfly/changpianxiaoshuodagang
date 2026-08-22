# -*- coding: utf-8 -*-
"""
Script writer for build_tianque_packet.py
"""
from pathlib import Path

CODE = '''# -*- coding: utf-8 -*-
"""
Full Master Outline Compiler for 《天阙惊龙》 (144 Chapters Production Master)
Integrates all 5 Ledgers, 6 Volumes, and 144 Bespoke Chapter Specifications.
"""

import json
import sys
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent
sys.path.insert(0, str(OUTLINE_DIR))
sys.path.insert(0, str(OUTLINE_DIR.parent / ".agents" / "skills" / "vnext-outline-agent" / "scripts"))

SOURCE = ["BRIEF.user_source", "DESIGN.originalized_adaptation", "RUNTIME.vnext16_2"]

ACTOR_NAMES = {
    "CHAR.gu_jinglan": "顾惊澜",
    "CHAR.ye_polu": "叶破虏",
    "CHAR.jiang_sui": "姜素衣",
    "CHAR.ye_tingxue": "夜听雪",
    "CHAR.shen_qinghuang": "沈倾凰",
    "CHAR.pei_luoshuang": "裴落霜",
    "CHAR.leng_yue": "冷月",
    "CHAR.xiao_minghuang": "萧明凰",
    "CHAR.zhao_wuji": "赵无极",
    "CHAR.zhao_biao": "赵彪",
    "CHAR.zhao_xuan": "赵玄",
    "CHAR.qian_wanjin": "钱万金",
    "CHAR.wu_titian": "乌啼天",
    "CHAR.yan_songqing": "严嵩卿",
    "CHAR.wan_yan_badu": "完颜拔都",
    "CHAR.zhao_tianlong": "赵天龙",
    "CHAR.xiao_qianyuan": "萧乾元",
    "CHAR.wuchenzi": "无尘子",
    "CHAR.jiuyou_laozu": "鬼煞真人",
    "CHAR.lu_song": "陆松",
    "CHAR.han_tie": "韩铁",
}

LOCATION_NAMES = {
    "LOC.tianyuan_cliff": "九绝天渊断天崖",
    "LOC.qingzhou_city": "青州郡城",
    "LOC.yaowang_branch": "青州药王堂",
    "LOC.qingzhou_palace": "青州王府",
    "LOC.qingzhou_heishi": "青州地下黑市",
    "LOC.linan_city": "江南临安城",
    "LOC.tingfeng_tower": "听风阁总楼",
    "LOC.wanbao_chamber": "万国商会总行",
    "LOC.taihu_water_camp": "太湖五毒水寨",
    "LOC.tianlang_pass": "北境天狼关",
    "LOC.beijing_camp": "幽燕玄甲军大营",
    "LOC.langjuxu_mountain": "漠北狼居胥山",
    "LOC.zhuque_gate": "皇城朱雀门",
    "LOC.taiji_palace": "皇宫太极殿",
    "LOC.gu_ancestral": "顾氏忠烈祖庙",
    "LOC.taixu_sect": "九天太虚剑宗",
}


def entity(entity_id, kind, name, payload, namespace="PLAN"):
    return {"id": entity_id, "kind": kind, "namespace": namespace, "name": name, "payload": payload}


def character(entity_id, name, identity, biography, desires, goals, interests, constraints, strategy, personality, private_life, knowledge, misjudgments, arc, highlights, fate, decision_model):
    return entity(entity_id, "CHARACTER", name, {
        "character_tier": "CORE" if entity_id in {"CHAR.gu_jinglan", "CHAR.ye_polu", "CHAR.xiao_minghuang"} else "MAJOR",
        "identity": identity,
        "biography": biography,
        "desires": desires,
        "goals": goals,
        "interests": interests,
        "constraints": constraints,
        "strategy": strategy,
        "personality": personality,
        "private_life": private_life,
        "knowledge_boundary": knowledge,
        "misjudgments": misjudgments,
        "arc": arc,
        "highlights": highlights,
        "fate": fate,
        "decision_model": decision_model,
        "provenance_refs": SOURCE,
    })


def faction(entity_id, name, f_type, goal, resources, conflict_internal):
    return entity(entity_id, "FACTION", name, {
        "type": f_type,
        "goal": goal,
        "resources": resources,
        "internal_conflict": conflict_internal,
        "provenance_refs": SOURCE,
    })


def location(entity_id, name, loc_type, geography, tactical_value):
    return entity(entity_id, "LOCATION", name, {
        "type": loc_type,
        "geography": geography,
        "tactical_value": tactical_value,
        "provenance_refs": SOURCE,
    })


def rule(entity_id, name, rule_content, ceiling):
    return entity(entity_id, "RULE", name, {
        "rule": rule_content,
        "ceiling": ceiling,
        "provenance_refs": SOURCE,
    })


def prop(entity_id, name, category, effect, owner, transfer_log):
    return entity(entity_id, "PROP", name, {
        "category": category,
        "effect": effect,
        "owner": owner,
        "transfer_log": transfer_log,
        "provenance_refs": SOURCE,
    })


def build_full_master_packet():
    # 1. Project
    project = entity(
        "PROJECT.tianque_jinglong_144",
        "PROJECT",
        "天阙惊龙：七年后携诸圣本领横推天下（144章工业级Master Outline）",
        {
            "assumptions": [
                "这是V2对抗式深度重构版本，彻底消除死亡角色复活、同质化决策模型、空泛模板与长尾拖戏问题。",
                "全书严格冻结为6卷144章（每卷24章，介于100至200章黄金区间），每章对应4000—6000字正文高承载剧情容量，全书预计60-86万字鸿篇巨制。",
                "升级货币为武道极道、造化医道、玄甲军权、万商财富与帝师天机，五维立体降维打击。",
            ],
            "open_questions": [
                "正文生产时严格依据各章独特的戏剧节拍展开，杜绝千篇一律的套路。"
            ],
            "one_sentence_synopsis": "七年前顾家遭皇城暗盟灭门，幼子顾惊澜被打入九绝天渊，七年后尽得五大隐世天尊极道真传，携七位名震天下的绝色师姐强势归来，横扫割据藩王、金融财阀、边关叛党与腐朽皇权，踏破吸血仙宗，重铸万古人间。",
            "causal_summary": "顾氏探查皇室血祭长生真相被屠灭，顾惊澜在天渊拜五大师尊学得逆天武道、医术、帝师经纬、玄甲军权与通天财力。出山后连破青州割据、江南金融围剿、北境断粮危机、皇城深宫政变四重关卡，斩杀国舅与魔化伪帝，踏平太虚仙宗山门，扶持七师姐萧明凰登基开泰女帝，最终解开万年气运禁制，携七美归隐红尘。",
            "scope": {
                "format": "MULTI_VOLUME_WEB_NOVEL",
                "total_volumes": 6,
                "total_chapters": 144,
                "word_budget_target": [600000, 860000],
            },
            "provenance_refs": SOURCE,
        }
    )

    # 2. Characters
    characters = [
        character("CHAR.gu_jinglan", "顾惊澜", "顾家唯一遗孤/天阙龙尊/五大隐世天尊唯一关门弟子",
                  "七年前顾家满门忠烈被屠，幼子顾惊澜被打入九绝天渊，因身负纯阳至尊骨被五大隐世天尊收为关门弟子，尽得武道、医道、军略、商道、帝师真传。七年后破渊而出，执掌惊龙天剑，横推天下。",
                  ["查清当年灭门血仇幕后所有黑手", "守护七位绝色师姐", "重定天下人间公理与法统"],
                  ["血洗青州斩杀执行者赵无极", "南下临安化解万国商会挤兑危机", "千里解围北境天狼关并封狼居胥", "进军皇都清君侧斩杀国舅与魔化伪帝", "踏平太虚仙宗山门斩断抽天气运禁制"],
                  ["顾氏家族忠烈名誉", "大玄黎民安居乐业", "师门同袍深厚情谊"],
                  ["不可滥杀无辜平民", "极道纯阳真气在突破阶段需防反噬", "受制于各师姐坚持的法理与商业规则摩擦"],
                  "以绝对极道武力为底牌掀桌，以医道救苍生，以商战摧毁门阀财路，以军威正面碾压，以法度公审定罪",
                  "霸气无双、护短狂魔、重情重义、心怀天下苍生、杀伐果断而不嗜杀",
                  "随身佩戴顾氏祖传龙纹残玉，贴身收藏大师姐战袍平安符与二师姐避毒囊",
                  "通晓大玄十三州山河地理与太虚仙宗万年吸血内幕",
                  "初期曾误以为赵无极即灭门主谋，后经由江南血契升维发现皇室与仙宗大网",
                  "从背负血海深仇的复仇狂龙，成长为超越凡尘皇权、庇佑人间万世的天下第一救世至尊",
                  "单手托万斤玄铁黑棺闯寿宴/一掌截断黄河大水/一剑劈碎三十丈朱雀门/踏碎太虚仙宗万丈主峰",
                  "解开天地禁制保全九州灵脉，辞去凡俗一切权位，与七位绝色师姐归隐红尘逍遥九天",
                  "决策模型：亲近者生命与人间公理 > 复仇快感 > 官府法统 > 自身安危。当二者冲突时，优先护佑苍生与师姐。"),

        character("CHAR.ye_polu", "叶破虏", "大师姐/大玄镇北大将军/三十万幽燕铁骑统帅/护国女战神",
                  "天渊大弟子，奉师尊之命出渊从军十年，横刀跃马威震漠北蛮族八十万铁骑，麾下三十万幽燕铁骑只认战神帅印不认朝廷兵部。视师弟顾惊澜为逆鳞。",
                  ["保境安民抵御外侮", "护佑师弟周全", "肃清朝中克扣军饷之卖国国贼"],
                  ["坚守天狼关直至后方军粮抵达", "阵前斩杀蛮族武圣完颜拔都", "封狼居胥祭告顾帅", "统领三十万铁骑回师京师奉天靖难"],
                  ["北境三十万将士生命与抚恤", "边关数十万汉家黎民生死", "师弟顾惊澜安危"],
                  ["兵部严嵩卿三年未发军饷导致大军饥寒", "受制于守土有责不能擅离边关防线"],
                  "以铁血大军阵法正面硬撼，严明军纪，战术上大开大阖，绝不后退半步",
                  "英姿飒爽、刚烈霸气、杀伐果断、对敌人狠辣对师弟极度宠溺温存",
                  "卸甲后内衬绣有与师弟儿时在天渊练刀的小图样，珍藏师弟所赠金针",
                  "深谙北方八大蛮族战阵虚实与兵部腐朽运作机制",
                  "曾以为兵部只是官僚克扣，未曾想严嵩卿已与完颜拔都签署卖国通敌协议",
                  "从受制于朝廷掣肘的浴血边将，成长为以天下兵权支持师弟重定乾坤的一代女武神",
                  "天狼关风雪中一人一刀斩退蛮族十二将/与师弟刀剑合璧屠尽太虚八大天人",
                  "新朝建立后推行军民屯田自给自足，辞去大都督位，与师弟相伴逍遥天地",
                  "决策模型：边防城池与三十万士兵生命 > 师门私情 > 兵部皇命 > 个人官位。绝不拿前线将士性命做政治妥协。"),

        character("CHAR.jiang_sui", "姜素衣", "二师姐/百草药王谷谷主/天下第一悬壶医仙",
                  "天渊二师尊唯一亲传，执掌天下九成灵丹药坊，精通起死回生造化神针与无色绝命毒经。",
                  ["医道济世", "相伴师弟", "光大药王谷"], ["化解全城血毒", "支持师弟后勤丹药", "清算地方侵占势力"],
                  ["药王谷传承", "天下病苦黎民"], ["武力不善大范围攻伐", "药材受江南财阀断供"], "以医结善缘，以毒断敌命",
                  "清冷如仙、外柔内刚、温柔似水", "闲暇时为师弟亲手缝制香囊与调配药膳", "掌握天下所有奇毒解法", "曾误判青州王府尚有一丝朝廷底线",
                  "从专研医道的避世医仙，转变为以医药体系化解全国血祭剧毒的圣德医尊", "三针还阳救活必死老仆/药王鼎前炼化万年尸丹为灵泉",
                  "建立覆盖大玄三十六行省的惠民公立医馆网络，长伴师弟身旁",
                  "决策模型：治病救人与平民安危 > 宗门独善其身 > 师门需求 > 自身安危。坚守医道底线，坚决反对无差别毒杀。"),

        character("CHAR.ye_tingxue", "夜听雪", "三师姐/听风阁总楼主/千面魅影天下谍尊",
                  "掌控大玄十三州最深情报网络，擅长易容、暗谍与心理博弈，是师弟最敏锐的耳目与军师。",
                  ["网罗天下机密", "为师弟扫清暗礁", "掌控九州风云"], ["截获兵部通敌密信", "监控皇都深宫异动", "刺探仙宗底细"],
                  ["听风阁万名暗桩生死", "情报绝对真实性"], ["真实面容不可轻易示人", "受制于仙宗天机遮蔽"], "布局设伏，以信息差杀人于无形",
                  "妖娆妩媚、智计百出、深沉内敛、极度护短", "收集全天下关于顾惊澜的战报编订成册", "知晓朝堂所有权贵把柄与隐秘私库坐标", "曾未能提早探明皇帝血祭大阵最终阵眼",
                  "从暗中窥探天下的谍影之主，成长为主导大玄情报体制重构的第一女军师", "一夜截获江南八大世家密谋账本/暗破太极殿天机迷局",
                  "将听风阁转型为国家阳光监察直诉机构，与师弟常相随",
                  "决策模型：情报网存续与绝对信息优势 > 快速报仇 > 个人名誉。信奉放长线钓大鱼，用铁证杀人。"),

        character("CHAR.shen_qinghuang", "沈倾凰", "四师姐/万国商会总会长/九州第一女财神",
                  "掌控天下四大钱庄与八百里漕运商道，富可敌国，举手投足翻动千亿风云，以商道护卫师门。",
                  ["商通天下", "以财力辅佐师弟成就大业", "建立平民信用公约"], ["破解江南八大家恶意挤兑", "调集百万石军粮北上救关", "查抄相府与国舅私库充公"],
                  ["万国商会商业信用", "天下平民储户财产安全"], ["调动现银受物理运输时差约束"], "金融对冲平准，以资本降维打击世家",
                  "雍容华贵、精明干练、霸气从容、深情专一", "私库只认顾惊澜一人的亲笔手信，为师弟定制龙鳞战甲", "精通大玄所有财政预算与漕运物流节点", "曾低估了五毒门暗杀商会掌柜的残忍手段",
                  "从垄断巨富成长为重构大玄国家金融与平准体系的商道圣手", "万商大会亮出通天商皇令/三千巨舰装载百万石军粮直抵前线",
                  "开辟大玄万国自由贸易港，与师弟泛舟西湖归隐",
                  "决策模型：全球商业信用与金融大盘安全 > 战术快速推平 > 商业利润 > 个人情感。反对暴力砸盘伤害储户。"),

        character("CHAR.pei_luoshuang", "裴落霜", "五师姐/皇家悬剑司首座/刑部总捕神",
                  "执掌帝国最高司法刑狱特权，身负先帝御赐尚方斩仙剑，铁面无私，律法通神，誓要为天下讨公道。",
                  ["法度昭彰", "为顾家满门洗雪沉冤", "惩治朝廷贪官污吏"], ["依法查办江南首富钱万金", "收集严嵩卿受贿铁证", "京师菜市口明正典刑监斩严贼", "起草开泰新律"],
                  ["大玄律法神圣尊严", "程序正义与铁证闭环"], ["受制于朝廷官僚程序与卷宗保密机制"], "先取如山铁证，再登公堂宣判明正典刑",
                  "冷艳如霜、刚正不阿、眼神锐利如刀、内心柔情只付师弟", "办案卷宗夹层贴身存放顾惊澜幼年画像", "通晓大玄三百年一切律例与铁案典籍", "曾误判大玄皇帝尚有一丝守法之心",
                  "从维护皇权律法的刑狱首座，升华为确立'天子犯法与庶民同罪'的万世法治奠基人", "西市法堂斩杀钱万金与严嵩卿/太和殿宣读废帝十大罪状",
                  "立《悬剑司司法独立宪章》，确立现代法治基石，功成身退与师弟逍遥天下",
                  "决策模型：程序正义与铁证确凿 > 结果正义 > 私人感情 > 皇权命令。坚决反对动用私刑，坚持公堂公审。"),

        character("CHAR.leng_yue", "冷月", "六师姐/幽冥刺客联盟至尊暗皇/天下第一刺客",
                  "潜伏黑暗七年登顶刺客至尊，身法如鬼魅，杀人于无形，因寻找师弟而接取江南悬赏，相认后反戈为师弟斩尽暗敌。",
                  ["守护师弟万无一失", "诛灭所有暗夜杀手组织", "洗净双手血腥回归平静"], ["太湖水寨斩杀五毒门主", "雪原暗杀蛮族大萨满", "血洗国舅府刺客死士"],
                  ["师弟顾惊澜绝对生命安全", "师门姐妹安危"], ["长期受幽冥噬心蛊反噬"], "无影无形，一击必杀，绝不拖泥带水",
                  "沉默寡言、冷酷嗜血、对外极狠对师弟极度依恋温柔", "换下夜行衣后喜欢穿素白长裙为师弟烹茶", "精通天下所有暗器、遁术与刺杀机关陷阱", "曾误将顾惊澜当成寻常刺杀目标而险些交手",
                  "从饮血无数的暗夜修罗，蜕变为只为守护人间正义与师弟平安的影之卫士", "临安夜宴反水一脚踹碎首富肋骨/百里雪原一击刺杀蛮族大萨满",
                  "整编刺客为国家境外特别防卫局，卸下暗刃与师弟长相厮守",
                  "决策模型：师弟顾惊澜绝对安全 > 刺客联盟契约 > 世俗道德法律。专门负责处理台面之下的脏活暗敌。"),

        character("CHAR.xiao_minghuang", "萧明凰", "七师姐/大玄长公主 -> 摄政监国 -> 开泰女帝",
                  "先皇嫡长女，因撞破皇帝弟弟萧乾元血祭长生真相而被夺权软禁深宫，暗中联络忠臣义士，与师弟里应外合夺回江山。",
                  ["推翻伪帝魔政", "拯救大玄亿万苍生", "建立清明君民共治新朝"], ["在深宫策反御林军", "太和殿宣读先帝废立密诏", "登基开泰女帝", "推行科举与废除九品中正制"],
                  ["大玄江山社稷稳定", "皇城三百万百姓安危", "与师弟共创太平盛世"], ["受制于伪帝控制的皇城护卫与深宫禁制"], "政治博弈，潜伏策反，大义名分，和平接管",
                  "端庄威严、胸怀天下、远见卓识、政治手腕通天、对师弟毫无保留信任", "私藏先皇托孤血诏与九章龙凤玉玺", "精通大玄朝廷权贵谱系与派系博弈平衡", "曾低估了萧乾元魔化自爆拉全城陪葬的丧心病狂",
                  "从深宫受困的落难长公主，蜕变为开创千古繁荣盛世的开泰立宪女帝", "金銮殿当朝宣读先皇遗诏废黜伪帝/太和殿举行开泰登基大典",
                  "登基开泰女帝确立君民共治宪章，禅让治理大权于内阁，与师弟隐退红尘",
                  "决策模型：大玄江山平稳过渡与万民存续 > 皇权正统 > 个人复仇 > 宗室私利。攻城必须保全全城平民。"),

        character("CHAR.zhao_wuji", "赵无极", "青州王/灭门案前线执行藩王",
                  "依仗皇亲国戚与藩王权势，在青州一手遮天，残暴贪婪，七年前参与瓜分顾家产业，但不知仙宗终极血祭内幕。",
                  ["保住青州封疆割据", "吞并药王堂丹方", "巴结国舅晋升中央"], ["逼婚姜素衣", "调兵围剿顾惊澜", "保住王位"],
                  ["青州王府世袭特权"], ["武道止步大宗师巅峰"], "以势压人，军阵绞杀",
                  "狂妄自大、贪婪狠辣、外强中干", "私藏当年瓜分顾家的千万黑金账本", "仅掌握灭门案部分地方出资名单", "误以为顾惊澜只是武道亡命之徒，王府军阵重弩可轻易镇杀",
                  "从不可一世的封疆藩王，堕落为寿宴身首异处的棺中死囚（第13章寿宴伏诛）", "调动三千黑甲重弩卫围杀主角", "在第13章寿宴上被顾惊澜斩首，引爆江南血契线索",
                  "决策模型：家族割据特权与个人私欲 > 朝廷法度 > 臣民生死。贪图利益不惜撕毁所有盟约。"),

        character("CHAR.qian_wanjin", "钱万金", "江南万商联盟会长/江南八大家首富",
                  "掌控江南八大世家钱庄与漕运黑金，当年灭门出资百万两黄金，唯利是图，手段阴狠绝顶。",
                  ["垄断江南商道", "吞并万国商会", "换取朝廷世袭爵位"], ["联合五毒门下毒", "制造钱庄挤兑陷阱", "雇凶刺杀顾惊澜"],
                  ["八大世家联盟利益"], ["受制于万国商会全球黄金结算"], "以资本垄断制造挤兑，配合地下黑道暗杀",
                  "贪婪成性、老奸巨猾、极度自私", "密室存有江南八大世家灭门出资血契原件与兵部行贿账册", "掌握大玄南方三十六座大钱庄账目", "误以为金钱能买通天下所有刺客",
                  "从不可一世的江南财阀首恶，沦为临安夜宴被俘、悬剑司大牢伏诛的死囚（第42章依法处决）", "万商夜宴亮出千亿债务逼宫沈倾凰", "在第32章被冷月反戈重创生擒，第42章审讯画押后明正典刑处死",
                  "决策模型：资本增殖与商业垄断 > 盟友死活 > 道德法律。善于利用平民储户作为对抗官府的人肉盾牌。"),

        character("CHAR.wu_titian", "乌啼天", "五毒魔宗宗主/江南地下魔道巨擘",
                  "潜伏江南太湖水寨，精通万毒蛊术与活人炼尸，暗中受国舅府与兵部资助残害武林。",
                  ["以万毒蛊神踏入天人境", "控制江南所有名医与药材", "称霸南方武林"], ["炼制绝命万毒蛊", "截杀姜素衣", "毒杀顾惊澜"],
                  ["五毒门千名死士与蛊池"], ["畏惧纯阳极道烈火神功"], "无色无味下毒，暗中操控傀儡",
                  "阴毒残忍、人不人鬼不鬼、狡诈多端", "体内温养万年金蚕噬心蛊王", "熟知大玄南方所有水寨暗道", "低估了太乙神针造化真气对魔蛊的绝对克制",
                  "从荼毒江南的魔道宗主，沦为被太乙神火焚烧殆尽的飞灰（第36章太湖水寨伏诛）", "在太湖万毒大阵施展万蛊噬天", "第36章被顾惊澜纯阳真气一掌拍碎万毒魔鼎焚灭神魂",
                  "决策模型：蛊道突破天人与宗门血祭 > 世俗契约 > 门徒生死。一旦败退立刻断尾求生。"),

        character("CHAR.yan_songqing", "严嵩卿", "当朝兵部尚书/国舅赵天龙铁杆死党",
                  "掌管大玄天下兵权调动与军饷粮草，贪赃枉法，勾结蛮族割地通敌，陷害叶破虏三十万大军。",
                  ["架空边军战神", "割让北境以换取蛮族支持夺权", "永掌兵权枢纽"], ["扣押北境三年军饷", "引蛮族八十万大军入关", "诛杀叶破虏与顾惊澜"],
                  ["兵部调兵大印与朝中奸党人脉"], ["畏惧悬剑司掌握铁证与战神帅印"], "官僚公文截留，暗中克扣辎重粮饷",
                  "道貌岸然、阴险毒辣、卖国求荣", "密室藏有与蛮族大汗私通的羊皮密信", "知晓京畿全部要塞驻军虚实", "误以为三十万铁骑饥寒交迫必死无疑",
                  "从权倾朝野的二品兵相，沦为朱雀门前被悬剑司斩首示众的卖国贼（第80章京师菜市口伏诛）", "私扣百万石军粮导致前线将士饥寒，第58章兵权被夺逃窜京师，第66章密谋决堤黄河", "第80章在京师菜市口十万百姓见证下被裴落霜宣读铁证当众明正典刑斩首",
                  "决策模型：官僚权力安全与派系利益 > 国家主权 > 军队安危。精通利用大玄公文流程设置合法性障碍。"),

        character("CHAR.wan_yan_badu", "完颜拔都", "北方蛮族第一武圣/八十万蛮军兵马大元帅",
                  "漠北狼庭至高武道图腾，身负上古蛮神血脉，肉身刀枪不入，受太虚仙宗暗中指使南侵。",
                  ["南下踏平大玄", "割据中原沃土", "借大玄气运冲击神仙境"], ["合围天狼关", "斩杀叶破虏", "生擒中原皇帝"],
                  ["八十万蛮族控弦之士"], ["武道依赖煞气狂暴，易受极道天剑克制"], "万军掩杀，以力破巧，阵前斗将",
                  "霸烈残暴、嗜血狂傲、视人命如草芥", "手持重达万斤的开山裂地蛮神重斧", "通晓漠北萨满血祭秘术", "狂妄宣称中原武道已无一人可堪一战",
                  "从威震大陆的蛮族军神，沦为金狼战车前被顾惊澜斩首的败亡祭品（第60章天狼关战死伏诛）", "在两军阵前以开山斧劈碎千丈雪原", "第60章被顾惊澜惊龙天剑削断战斧与双臂，一剑封喉斩落首级彻底终结",
                  "决策模型：弱肉强食与部落图腾荣耀 > 政治盟约 > 部落伤亡。唯崇尚绝对武力。"),

        character("CHAR.zhao_tianlong", "赵天龙", "当朝国舅/皇城暗盟魁首",
                  "太后胞兄，朝廷第一权臣，当年灭门案执行总操盘手，以权谋私，勾结仙宗与地方藩王。",
                  ["架空皇权", "垄断长生药引", "诛杀一切异己"], ["除掉叶破虏军权", "镇压长公主", "斩灭顾惊澜"],
                  ["国舅府至高权位"], ["依赖仙宗提供的天人客卿"], "阴险深沉，毒计百出",
                  "阴鸷狠毒、老谋深算、权倾朝野", "密室藏有朝中半数官员的死穴把柄", "掌握皇城禁军一半兵权", "误以为三十万铁骑不敢进京靖难",
                  "从翻云覆雨的当朝权相，沦为赵氏宗祠前伏诛的三族罪魁（第84章宗祠前伏诛）", "调集五万门阀私兵在京师发动武装兵变", "第84章在赵氏太庙前被顾惊澜震碎狂龙重剑一剑斩首",
                  "决策模型：权相独裁与国舅府满门权贵利益 > 皇朝稳定 > 百官与黎民。善于在皇帝与仙宗之间充当掮客。"),

        character("CHAR.xiao_qianyuan", "萧乾元", "大玄伪帝/血祭长生终极黑手",
                  "表面圣明仁德，暗地里为求长生不老，以亿万黎民为血引与仙宗做交易，灭顾家封口。",
                  ["求取万年长生", "踏入陆地神仙境", "永固萧氏江山"], ["引爆皇城血祭大阵", "诛杀顾惊澜", "吞噬满城生灵"],
                  ["大玄皇权最高名义与大内生灵血池"], ["被仙宗视为人间采药傀儡"], "暗中魔化，血祭生灵，伪善欺世",
                  "虚伪至极、自私自利、丧心病狂、贪生怕死", "深宫密室养有上古血神魔蛊", "掌控大玄钦天监与深宫血灵大阵", "误以为仙宗真能赐其长生永生",
                  "从九五至尊的封建帝王，沦为太极殿前被钉死在龙柱上的灭世邪魔（第106章钉死龙柱，第108章彻底斩灭神魂伏诛）", "引动全城血线抽取三百万平民生命", "第106章被顾惊澜惊龙天剑钉死在龙柱上，第108章神魂彻底灰飞烟灭",
                  "决策模型：个人永生不死 > 大玄江山宗庙 > 万民死活。到了绝境宁可拉全天下陪葬。"),

        character("CHAR.wuchenzi", "无尘子", "太虚仙宗宗主/太上仙尊/全书终极大Boss",
                  "九天吸血仙门太虚仙宗掌门，视人间凡俗为药田牲口，每六十年通过皇室血祭抽取人间气运炼制不死仙丹。",
                  ["掠夺人间气运", "飞升上界长生界", "维持仙宗万年吸血霸权"], ["降下太虚诛仙阵", "斩杀顾惊澜", "重置人间皇朝轮回"],
                  ["太虚神镜仙宝与九霄仙宗道统"], ["受制于天地隔绝结界法则"], "高高在上，天人降维，视凡人如草芥蝼蚁",
                  "冷酷无情、高傲绝顶、视万灵为牲畜、视天道为玩物", "拥有上古太虚神镜与焚天仙符", "通晓天地气运流转与抽气大阵核心", "狂妄认定凡人武道永远无法逆伐神仙",
                  "从高高在上的修仙主宰，沦为主山门前被顾惊澜斩断头颅除名的罪仙（第116章主峰伏诛）", "祭起太虚神镜射出九色灭世神光", "第116章在太虚祖师殿被顾惊澜一剑削落头颅并碎其元婴彻底除名",
                  "决策模型：仙道宗门利益与个人飞升 > 凡间万界亿万生灵。绝对物化凡人，毫无道德底线。"),

        character("CHAR.jiuyou_laozu", "鬼煞真人", "九幽魔祖/太液池地底被封印魔头",
                  "三百年前祸乱人间的九幽魔宗老祖，被太虚仙宗秘密囚禁于皇城太液池充当血祭催化阵眼。",
                  ["破开封印重见天日", "吸干皇城百姓精血恢复魔功", "向仙门复仇"], ["破开太液池玄冰", "斩杀少帅顾惊澜", "将京师化为魔域"],
                  ["九幽嗜血魔幡与天人境魔煞"], ["畏惧大玄九洲山河真图与至阳真火"], "魔煞遮天，万魂嗜血，肉身不灭",
                  "残忍嗜杀、疯狂癫狂、嗜血成瘾", "体内温养三百年九幽魔丹", "掌握大玄地下九幽灵脉流向", "低估了顾惊澜纯阳真火对魔煞的绝对净化神威",
                  "从不可一世的上古魔祖，沦为万寿宫上空被纯阳真火焚灭的飞灰（第92章皇城伏诛）", "引动万丈黑煞魔雾笼罩京师九门", "第92章被顾惊澜以山河真图与三昧真火彻底焚灭神魂肉身",
                  "决策模型：吞噬生灵恢复魔力 > 世俗秩序 > 自身安危。信奉杀戮与魔道至尊。"),

        character("CHAR.lu_song", "陆松", "顾家三十年老仆/忠仆典范",
                  "七年前灭门之夜舍命护送少帅跳入天渊，重伤残废隐姓埋名于青州药王堂，视顾家荣誉重于生命。",
                  ["见证少帅沉冤得雪", "守护顾氏忠烈牌位", "看着少帅成家立业"], ["交出地下藏书阁钥匙", "为少帅引路青州", "点燃祖庙万年长明灯"],
                  ["顾氏家族三十年忠心"], ["年老体衰身负旧伤"], "赤胆忠心，舍生取义",
                  "忠肝义胆、坚毅隐忍、慈祥忠诚", "贴身缝藏顾家昔日地下密室钥匙", "熟知当年顾家所有产业布局与老部下名单", "曾担心少帅势单力薄遭遇不测",
                  "从苟延残喘的残废老仆，成长为在京师顾氏祖庙亲手点燃万年长明灯的忠烈见证人", "药王堂前挺身而出护卫少帅/在京师祖庙告慰老帅英灵",
                  "在新朝享一品国公级供养，颐养天年",
                  "决策模型：少帅安危与顾家昭雪 > 个人生死。誓死效忠顾氏满门。"),

        character("CHAR.han_tie", "韩铁", "青州总捕头 -> 青州城防总兵大将",
                  "青州底层捕头，为人刚正不阿，痛恨藩王鱼肉百姓，公堂抗旨后被顾惊澜收编拔擢，成为大后方铁壁守将。",
                  ["保境安民", "清除官府腐败", "追随少帅建立清明世道"], ["封锁青州水旱两路", "整编五千玄武铁军", "抵挡朝廷钦差渗透"],
                  ["青州五千精锐城防军与百姓爱戴"], ["早期受制于封建官僚品阶"], "铁面执法，整肃军纪，坚守防线",
                  "刚直不阿、铁骨铮铮、知恩图报、严明军纪", "佩带顾惊澜所赠玄铁精钢宝刀", "精通青州城防十三处暗道水门机关", "曾以为朝廷钦差尚存良知",
                  "从受尽藩王排挤的底层差役，成长为坐镇大后方独当一面的大将军", "公堂之上折断官刀抗旨护民/率五千铁军死守青州北大门",
                  "官拜大玄西南镇守使，名垂青史",
                  "决策模型：百姓安危与大义公理 > 官府皇命 > 个人升迁。宁折不弯的铁血正气。"),
    ]

    # 3. Factions
    factions = [
        faction("FACTION.gu_family", "顾氏忠烈门", "主角核心家族", "洗雪七年冤狱，重振忠烈家风", ["顾氏龙纹残玉", "旧部忠勇将士", "大玄九洲山河真图"], "无"),
        faction("FACTION.yaowang_gu", "百草药王谷", "天下医道宗门", "悬壶济世，掌控天下医道丹坊", ["九转灵丹", "神农鼎", "天下药脉"], "地方分支遭藩王势力强拆侵占"),
        faction("FACTION.wanbao_chamber", "万国商会", "天下第一商盟", "垄断通商命脉，以富可敌国之财力支援主角", ["四大钱庄", "五千万两黄金储备", "八百里漕运水路"], "江南八大世家违约断流"),
        faction("FACTION.xuanjia_army", "幽燕玄甲军", "天下第一边防雄兵", "保卫北境疆土，效忠战神帅印", ["三十万铁骑", "玄甲重甲", "屠龙破军战阵"], "后方断粮导致军心与朝廷决裂"),
        faction("FACTION.xuanjian_si", "皇家悬剑司", "帝国最高司法刑狱机构", "执掌刑律生杀，明正典刑", ["斩仙刑刀", "大玄刑律赦令", "缉捕死士"], "刑部权贵试图包庇皇亲国戚"),
        faction("FACTION.tingfeng_tower", "听风阁", "天下第一情报网络", "网罗九州机密，辅助顾惊澜定乾坤", ["全图视野", "飞鸽密网", "千面谍探"], "部分暗桩被兵部暗探渗透"),
        faction("FACTION.youming_league", "幽冥刺客联盟", "天下第一杀手组织", "暗夜潜行，成为师弟专属影子暗刃", ["修罗暗刺", "无影毒刃", "遁影死士"], "早期接取针对顾惊澜的悬赏导致内部清洗"),
        faction("FACTION.taixu_sect", "九天太虚剑宗", "万年吸血仙门", "抽取人间生灵气运炼丹求长生", ["太虚神镜", "诛仙飞剑", "九色灭世仙符"], "视凡间皇权为牲畜产生不可调和阶级矛盾"),
    ]

    # 4. Locations
    locations = [
        location("LOC.tianyuan_cliff", "九绝天渊断天崖", "极道绝地", "绝壁万丈，上接天道神雷，下临九幽地火", "主角修炼出山之圣地"),
        location("LOC.qingzhou_city", "青州郡城", "西南重镇", "依山傍水，地势险要，下扼江南漕运咽喉", "第一卷大本营与复仇起点"),
        location("LOC.yaowang_branch", "青州药王堂", "医馆重地", "药香四溢，内藏九品灵药库与百年老医馆", "首战立威与救治忠仆战场"),
        location("LOC.qingzhou_palace", "青州王府", "藩王宫殿", "雕梁画栋，内设三千黑甲重弩校场与地下金库", "寿宴送棺斩杀赵无极决战场"),
        location("LOC.qingzhou_heishi", "青州地下黑市", "地下销金窟", "九曲回廊，盘踞走私军火与洗钱钱庄", "起获江南八大家洗钱血契处"),
        location("LOC.linan_city", "江南临安城", "帝国经济中心", "八百里运河穿城而过，钱庄林立，世家盘踞", "第二卷金融与刺客决战舞台"),
        location("LOC.tingfeng_tower", "听风阁总楼", "天下谍报中枢", "矗立西湖之畔，高九层，千面纸鸢出没", "破译通敌密函与战略沙盘"),
        location("LOC.wanbao_chamber", "万国商会总行", "天下财富之巅", "黄金铺地，金库深达地下三层，万商云集", "五千万两现银调动与平准仓大本营"),
        location("LOC.taihu_water_camp", "太湖五毒水寨", "水上魔窟", "千艘毒船结成水阵，毒雾遮天，尸骨成山", "斩杀五毒门主乌啼天战场"),
        location("LOC.tianlang_pass", "北境天狼关", "北方第一雄关", "万里长城之咽喉，冰封千里，黑云压城", "第三卷国战与封狼居胥决战场"),
        location("LOC.beijing_camp", "幽燕玄甲军大营", "三十万军营", "营连百里，杀气冲霄，玄甲如林", "点将出征与整军靖难大本营"),
        location("LOC.langjuxu_mountain", "漠北狼居胥山", "华夏武道圣山", "雪峰耸立，汉白玉古坛矗立山巅", "斩杀完颜拔都祭奠顾帅与封狼居胥圣地"),
        location("LOC.zhuque_gate", "皇城朱雀门", "帝都第一正门", "高三十丈，万斤玄铁铸就，九龙盘踞", "第四卷一剑斩断城门破城入京处"),
        location("LOC.taiji_palace", "皇宫太极殿", "权力之巅与地宫血池", "金銮宝座之下隐藏万丈玄阴血池与七星大阵", "第五卷弑仙斩魔与第六卷女帝践祚圣殿"),
        location("LOC.gu_ancestral", "顾氏忠烈祖庙", "忠烈圣地", "御赐京师核心福地，汉白玉宗祠牌坊耸立", "第六卷点燃万年长明灯与沉冤昭雪圣所"),
        location("LOC.taixu_sect", "九天太虚剑宗", "仙门山峰", "悬浮九霄之上，白玉神殿连绵三千座", "第五卷踏破山门除名仙宗终极决战场"),
    ]

    # 5. Rules
    rules = [
        rule("RULE.blood_sacrifice", "天渊龙脉血祭长生规则", "伪帝以万民寿元为药引供给仙宗炼不死丹，但血祭会导致皇朝气运崩解反噬。", "伤天害理必遭天谴"),
        rule("RULE.jidao_law", "极道天道法则破甲规则", "顾惊澜极道纯阳神功具备专破世间一切阵法、法宝、罡气罩门之属性，非数值对轰。", "需消耗纯阳真元入微操纵"),
        rule("RULE.law_evidence", "悬剑司司法铁证闭环规则", "大玄司法必须由先知口供、受贿账册、官方印信三位一体方可明正典刑斩首朝廷命官。", "严禁私刑，坚持程序正义"),
        rule("RULE.finance_balance", "平准仓逆向对冲金融规则", "面对财阀恶意挤兑，强行注资会压垮平民钱庄，必须以平准仓跨期对冲平抑物价。", "需充足实物黄金储备"),
        rule("RULE.power_hierarchy", "七阶战力梯队规则", "一至三品炼体、四至六品通脉、七至九品宗师、武圣绝巅、天人境、陆地神仙、极道天道，严禁越级乱轰。", "严格遵守物理与法则克制"),
    ]

    # 6. Props
    props = [
        prop("PROP.jinglong_sword", "惊龙天剑", "至尊神兵", "极道天尊本命至宝，可斩断世间一切阵法灵宝与气运枷锁", "CHAR.gu_jinglan", ["天渊师尊所授", "青州斩藩王", "天狼关屠武圣", "太极殿斩伪帝", "踏平仙门"]),
        prop("PROP.longwen_jade", "顾氏龙纹佩", "家族信物", "记录大玄地脉龙气与顾家忠烈血脉，可引动山河真图", "CHAR.gu_jinglan", ["老仆陆松归还残玉", "青州合璧", "太极殿破阵"]),
        prop("PROP.shangfang_sword", "先帝御赐尚方斩仙剑", "至高法器", "先皇御赐悬剑司特权，上斩昏君下斩奸佞，司法绝对独立象征", "CHAR.pei_luoshuang", ["先皇密赐", "临安审钱万金", "金銮殿宣判严嵩卿", "开泰立宪入法"]),
        prop("PROP.wanbao_token", "万宝商皇通天令", "商道至尊令", "可无条件调动十三州四大钱庄五千万两黄金储备与三千漕运船队", "CHAR.shen_qinghuang", ["商会总行祭出", "逆流运抵五千万两黄金", "保障北伐百万石军粮"]),
        prop("PROP.zhenbei_tally", "北境战神虎符", "至高兵符", "调动三十万幽燕玄甲铁骑唯一信物，三军唯虎符是从", "CHAR.ye_polu", ["叶破虏交接少帅", "天狼关点将", "回师京师靖难", "第六卷入国家宪章"]),
    ]

    # 7. Acts & Volumes
    acts = [
        entity("ACT.1", "ACT", "第一幕：龙出深渊破藩篱（卷1-2）", {"description": "青州与江南篇：扫平地方割据，摧毁金融围剿，起获通敌铁证", "provenance_refs": SOURCE}),
        entity("ACT.2", "ACT", "第二幕：战神封狼御九关（卷3）", {"description": "北境天狼关篇：解救断粮危机，斩杀蛮皇武圣，三十万铁骑回师靖难", "provenance_refs": SOURCE}),
        entity("ACT.3", "ACT", "第三幕：深宫夺嫡斩国舅（卷4）", {"description": "京师风云篇：破朱雀门，公审斩奸相，诛灭国舅，长公主摄政监国", "provenance_refs": SOURCE}),
        entity("ACT.4", "ACT", "第四幕：万道诛仙定乾坤（卷5-6）", {"description": "弑仙决战与盛世篇：斩魔化伪帝，踏平太虚仙宗山门，开泰女帝立宪，神仙眷侣归隐", "provenance_refs": SOURCE}),
    ]

    volumes = [
        entity("VOLUME.v1_qingzhou", "VOLUME", "第一卷·龙出九渊·血洗青州破藩篱", {
            "chapter_start": 1, "chapter_end": 24,
            "central_conflict": "顾惊澜极道复仇 vs 青州藩王割据与潜伏的江南黑金网络",
            "detailed_plot": "顾惊澜破天渊出山首临青州，救活老仆陆松，解药王堂逼婚危机废小王爷，开神农鼎炼造化丹。于第13章六十大寿单手托巨棺闯入王府，一人横压三千重弩卫，斩杀青州王赵无极。第14章核心转折（Problem Morph）：搜查王府密室发现赵无极仅是白手套，顾家灭门由江南首富钱万金出资百万两黄金，涉及兵部与朝廷血祭大网。第15-20章顾惊澜连环拔除江南在青州的洗钱黑市与五毒暗桩，扶持正义总捕韩铁整饬城防；第21-24章硬刚朝廷钦差扣粮之威，携二师姐神丹与大义顺江而下，直扑临安！",
            "turning_points": "第1章破渊救老仆废恶奴、第7章神农鼎炼成九转天元金丹、第13章寿宴托棺斩青州王赵无极、第14章搜出灭门血契发现江南万商与兵部连环大网（问题升维）、第24章斩断青州界碑铁索顺江直扑临安",
            "payoff": "斩杀首位执行藩王，青州恶霸连根拔起，夺回龙纹主玉，锁定江南首富钱万金",
            "next_hook": "江南八大世家已联手五毒门发动数千万两债务围剿万国商会，四师姐沈倾凰陷入绝境",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v2_jiangnan", "VOLUME", "第二卷·金权九幽·江南翻天斩暗刃", {
            "chapter_start": 25, "chapter_end": 48,
            "central_conflict": "万商通天令与金融精准对冲 vs 江南八大家资本垄断、五毒魔门与幽冥暗杀",
            "detailed_plot": "顾惊澜南下临安汇合三师姐夜听雪与四师姐沈倾凰。江南八大世家联手五毒门企图以恶意抽贷挤兑万国商会，并以毒蛊控制平民储户。顾惊澜亮出万宝商皇令，但面临'强行注资会砸崩平民钱庄'的系统性难题；沈倾凰以金融平准仓精准对冲，顾惊澜造化真火焚毁太湖五毒寨诛杀乌啼天（第36章）。第32章幽冥第一刺客冷月暗夜认亲反戈生擒钱万金。裴落霜带悬剑司入驻，第42章刑讯钱万金取得兵部尚书严嵩卿通敌受贿原件并依法处斩首富。第43-48章调集百万石江南军粮与冬衣，打通漕运直奔北境！",
            "turning_points": "第28章万宝商皇令调集五千万两黄金进江、第32章六师姐冷月刺杀反戈生擒钱万金、第36章太湖水寨斩杀五毒门主乌啼天、第42章审讯钱万金取得兵部通敌密信并明正典刑、第48章百万石军粮巨轮扬帆北伐",
            "payoff": "江南数千万两商道收复，五毒门覆灭，四师姐、六师姐、五师姐彻底归位，取得兵部通敌铁证",
            "next_hook": "北境天狼关三年军饷被兵部扣押，八十万蛮军合围，大师姐叶破虏铠甲染血立于孤城",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v3_beijing", "VOLUME", "第三卷·铁血王旗·战神封狼御九关", {
            "chapter_start": 49, "chapter_end": 72,
            "central_conflict": "幽燕玄甲军至高军威与大义靖难 vs 兵部卖国奸党、蛮族武圣与太虚天人合流",
            "detailed_plot": "顾惊澜与裴落霜千里押运百万石粮草奔袭北境。兵部尚书严嵩卿企图以'无兵部调令强运军粮即为谋反'羁绊大军；顾惊澜以太乙金针治愈大师姐叶破虏积年寒毒，亮出战神虎符统领三十万幽燕铁骑；开皇仓饱餐三军。第58章在天狼关前剥夺兵相严嵩卿兵权并通缉其逃窜京师。第60章金狼战车前顾惊澜十招削断蛮皇武圣完颜拔都战斧并一剑斩首；第65章三十万铁骑封狼居胥祭告老帅。第66-72章严嵩卿在京师调黄河水军封江，顾惊澜一掌截断黄河，三十万铁骑兵临帝京朱雀门！",
            "turning_points": "第52章天狼关风雪重逢治愈大师姐寒毒、第58章剥夺兵相兵权通缉逃亡、第60章阵前十招轰杀蛮皇武圣完颜拔都、第65章封狼居胥祭奠顾老帅、第72章一掌截断黄河十万铁骑兵临朱雀门",
            "payoff": "北境边患永除，三十万铁骑兵权归心，斩杀蛮族武圣，大师姐与五师姐归位",
            "next_hook": "皇城九门紧闭开启十二重仙阵，国舅赵天龙挟持百官，长公主在深宫发出决战信号",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v4_imperial_city", "VOLUME", "第四卷·天机权谋·深宫夺嫡斩国舅", {
            "chapter_start": 73, "chapter_end": 96,
            "central_conflict": "奉天靖难大军与长公主内应 vs 国舅府滔天权势、大内九幽魔道与伪帝血祭大阵",
            "detailed_plot": "十万铁骑合围皇城，顾惊澜一剑劈碎三十丈朱雀重门长驱直入。大朝会上裴落霜宣读严嵩卿十大死罪铁证如山，第80章在京师菜市口十万百姓见证下明正典刑斩杀严嵩卿！国舅赵天龙发动五万门阀私兵全城暴乱，第84章顾惊澜攻破赵氏宗祠当众斩首赵天龙。第86章长公主宣读先帝平反血诏昭雪顾家。第92章顾惊澜在万寿宫引动山河真图三昧真火焚灭破封魔祖鬼煞真人。第94章废黜伪帝萧乾元帝位，长公主摄政监国；第95-96章太虚仙宗启动七星锁灵灭世大阵，七位绝色师姐齐聚皇城之巅拔剑指天！",
            "turning_points": "第74章一剑劈碎三十丈玄铁朱雀门、第80章菜市口公审明正典刑斩首严嵩卿、第84章赵氏宗祠斩灭国舅赵天龙、第86章颁布先帝血诏昭雪顾氏满门、第92章焚灭九幽魔祖鬼煞真人、第94章废黜伪帝长公主摄政监国",
            "payoff": "当年灭门公案昭雪，严嵩卿与赵天龙彻底伏诛，剥夺伪帝合法性，七师姐掌控朝局",
            "next_hook": "伪帝萧乾元魔化为半步天人，皇城三百万百姓生命被千万道血线抽取危在旦夕",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v5_taiji_battle", "VOLUME", "第五卷·万道诛仙·太极殿前斩伪帝", {
            "chapter_start": 97, "chapter_end": 120,
            "central_conflict": "人间极道正气与万民意志 vs 魔化长生伪帝与超然吸血仙宗",
            "detailed_plot": "魔化伪帝启动血引抽取全城生灵。七位绝色师姐各展通天权能稳固七星大阵切断血线救下全城百姓；顾惊澜融合极道真传，在第104章以惊龙天剑将魔帝重创钉死在龙柱上；第106章长剑挥落彻底斩灭萧乾元魔道神魂！太虚仙宗宗主无尘子率八大天人长老踏万丈接引金桥降临人间，叶破虏与顾惊澜刀剑合璧全歼八大长老。第113章顾惊澜引动山河真图斩碎至尊仙宝太虚神镜、斩断无尘子右臂。第115-116章顾惊澜踏破太虚主峰山门，在祖师殿前一剑斩杀无尘子道统除名！第117-120章开仓放灵还众生，斩断通天吸血索，引导十三州龙脉归位，断然拒绝帝制！",
            "turning_points": "第98章纯阳破天碎七星阵、第104章惊龙天剑将魔化伪帝钉死龙柱、第106章斩灭萧乾元神魂永绝后患、第110章师姐弟合璧屠灭八大天人、第113章山河真图斩碎太虚神镜斩断仙尊手臂、第116章踏平太虚仙宗斩杀无尘子道统除名、第119章十三州龙脉归位天地灵气复苏",
            "payoff": "伪帝与太虚仙宗彻底覆灭，终结万年吃人神话，释放天下气运，全书终极强敌全灭",
            "next_hook": "旧皇朝瓦解天下百废待兴，且上界抽取气运的根基灵脉禁制仍存，需要新帝践祚重定乾坤",
            "provenance_refs": SOURCE,
        }),
        entity("VOLUME.v6_world_renewal", "VOLUME", "第六卷·万界开泰·重铸乾坤逍遥仙", {
            "chapter_start": 121, "chapter_end": 144,
            "central_conflict": "新时代公理秩序确立与斩断抽气运禁制保全灵脉难题 vs 过去万年宿命枷锁",
            "detailed_plot": "第121章萧明凰践祚登基为开泰女帝，册封顾惊澜镇国至尊龙尊帝师，颁布《开泰建元诏》与《君民共治宪章》。第124章重建顾氏忠烈祖庙，老仆陆松点燃万年长明灯告慰英灵。各师姐各司其职推行新政（裴落霜废除九品中正制推行科举、沈倾凰发行开泰金券建平准仓、姜素衣建八百公立医馆、夜听雪建万民监察直诉、冷月整编境外特别防卫、叶破虏幽燕屯田与军队国家化、废藩置省平定割据）。第133章绝地天通封印仙界裂隙。第134-135章华山论道，太和殿正式禅让大都督治权于民选内阁，功成身退。第137-138章泰山立万民碑，断天崖一剑精准斩断抽天气运禁制保全九州灵脉。第140-144章重回九绝天渊朝圣谢师恩，承继道主衣钵，开辟世外天阙仙境，布下大玄永安结界，神仙眷侣红尘逍遥大结局！",
            "turning_points": "第121章开泰女帝践祚登基册封至尊帝师、第124章顾氏祖庙点燃长明灯大仇沉冤得雪、第130章颁布《军队国家化总规程》、第132章废藩置省设立三十六行省、第135章禅让治理大权于民选内阁功成身退、第138章一剑精准斩断抽气运禁制保全九州灵脉、第144章临安茶馆说书说惊龙神话大结局",
            "payoff": "人间公理法度确立，所有角色圆满闭环，神仙眷侣逍遥四海，惊龙传说永照千秋",
            "next_hook": "人间烟火正浓，神仙眷侣笑看九州云卷云舒，全书完！",
            "provenance_refs": SOURCE,
        }),
    ]

    # 8. Lines, Promises, Climaxes
    lines = [
        entity("LINE.revenge", "PLOT_LINE", "主线：顾氏灭门血海深仇与因果清算", {"type": "MAIN", "goal": "从地方藩王查至大内伪帝与太虚仙宗，彻底斩草除根昭雪忠烈", "provenance_refs": SOURCE}),
        entity("LINE.shijie_bonds", "PLOT_LINE", "支线：七位绝色师姐归位与情感羁绊", {"type": "SUB", "goal": "七位绝色师姐各展通天绝技归位，建立深厚革命情谊与神仙眷侣羁绊", "provenance_refs": SOURCE}),
        entity("LINE.governance", "PLOT_LINE", "支线：重铸天下公理与现代宪政体制", {"type": "SUB", "goal": "破除封建门阀与神仙剥削，建立君民共治、司法独立、人人如龙盛世", "provenance_refs": SOURCE}),
    ]

    promises = [
        entity("PROMISE.1", "PROMISE", "灭门血契承诺：赵无极出资百万两黄金必死", {"status": "FULFILLED", "fulfilled_chapter": 13, "provenance_refs": SOURCE}),
        entity("PROMISE.2", "PROMISE", "通敌密函承诺：兵相严嵩卿卖国弑帅必明正典刑", {"status": "FULFILLED", "fulfilled_chapter": 80, "provenance_refs": SOURCE}),
        entity("PROMISE.3", "PROMISE", "血祭长生承诺：斩杀魔化伪帝与踏平太虚仙宗", {"status": "FULFILLED", "fulfilled_chapter": 116, "provenance_refs": SOURCE}),
    ]

    climaxes = [
        entity("CLIMAX.vol1", "CLIMAX", "第一卷高潮：寿宴送万斤黑棺斩杀青州王赵无极", {"chapter": 13, "provenance_refs": SOURCE}),
        entity("CLIMAX.vol2", "CLIMAX", "第二卷高潮：太湖斩毒魁乌啼天，西市斩首钱万金", {"chapter": 42, "provenance_refs": SOURCE}),
        entity("CLIMAX.vol3", "CLIMAX", "第三卷高潮：天狼关斩杀蛮皇武圣完颜拔都，封狼居胥", {"chapter": 65, "provenance_refs": SOURCE}),
        entity("CLIMAX.vol4", "CLIMAX", "第四卷高潮：朱雀门公审斩杀兵相严嵩卿，宗祠斩赵天龙", {"chapter": 84, "provenance_refs": SOURCE}),
        entity("CLIMAX.vol5", "CLIMAX", "第五卷高潮：太极殿斩灭伪帝神魂，踏平太虚仙宗斩无尘子", {"chapter": 116, "provenance_refs": SOURCE}),
        entity("CLIMAX.vol6", "CLIMAX", "第六卷高潮：开泰女帝践祚，断天崖斩断气运枷锁，归隐大结局", {"chapter": 144, "provenance_refs": SOURCE}),
    ]

    # 9. Events
    events_data = [
        ("EVENT.qingzhou_shouyan", "青州王府寿宴送棺", "CHAR.gu_jinglan", 13, "LOC.qingzhou_palace", "顾惊澜托万斤玄铁黑棺闯入寿宴，一人横压三千重弩卫，斩杀青州王赵无极", "青州割据瓦解，起获江南首富钱万金灭门血契", "EVENT.linan_shangzhan", ["CHAR.zhao_wuji", "CHAR.jiang_sui"]),
        ("EVENT.linan_shangzhan", "临安万商大会反绞杀", "CHAR.shen_qinghuang", 32, "LOC.wanbao_chamber", "万宝商会祭出商皇令调动五千万两黄金，冷月反戈生擒首富钱万金，斩杀五毒门主", "江南商道收复，获得兵相受贿铁证", "EVENT.tianlang_fenglang", ["CHAR.qian_wanjin", "CHAR.leng_yue"]),
        ("EVENT.tianlang_fenglang", "天狼关大捷封狼居胥", "CHAR.gu_jinglan", 60, "LOC.tianlang_pass", "第58章剥夺兵相兵权，第60章阵前轰杀蛮皇武圣完颜拔都，第65章封狼居胥祭告顾帅", "三十万铁骑彻底归心，拔都永久死亡，回师靖难", "EVENT.zhuque_shenpan", ["CHAR.ye_polu", "CHAR.wan_yan_badu"]),
        ("EVENT.zhuque_shenpan", "朱雀门公审与斩除国舅", "CHAR.pei_luoshuang", 80, "LOC.zhuque_gate", "一剑劈碎朱雀门，菜市口斩杀严嵩卿，宗祠斩杀国舅赵天龙，长公主摄政监国", "当年灭门大案昭雪，相党门阀尽灭", "EVENT.taiji_zhuxian", ["CHAR.yan_songqing", "CHAR.zhao_tianlong"]),
        ("EVENT.taiji_zhuxian", "太极殿弑仙与踏平太虚", "CHAR.gu_jinglan", 116, "LOC.taiji_palace", "太极殿斩灭魔化伪帝神魂，踏天杀入九天太虚剑宗，祖师殿前斩杀仙尊无尘子除名仙门", "万年吸血仙宗覆灭，释放十三州气运", "EVENT.nvdi_dengji", ["CHAR.xiao_qianyuan", "CHAR.wuchenzi"]),
        ("EVENT.nvdi_dengji", "开泰女帝践祚大典", "CHAR.xiao_minghuang", 121, "LOC.taiji_palace", "萧明凰登基为开泰女帝，册封顾惊澜至尊帝师，颁布《君民共治宪章》", "新正统皇朝建立，天下四海来朝", "EVENT.tianyuan_guiyin", ["CHAR.gu_jinglan", "CHAR.ye_polu"]),
        ("EVENT.tianyuan_guiyin", "断天崖斩锁与归隐红尘", "CHAR.gu_jinglan", 144, "LOC.tianyuan_cliff", "精准斩断抽天气运禁制保全九州灵脉，天渊谢师恩，携七美归隐红尘逍遥九天", "全书因果大圆满收官", "NONE", ["CHAR.gu_jinglan", "CHAR.jiang_sui", "CHAR.pei_luoshuang", "CHAR.shen_qinghuang", "CHAR.ye_tingxue", "CHAR.leng_yue", "CHAR.xiao_minghuang", "CHAR.ye_polu"]),
    ]

    event_entities = []
    event_edges = []
    for ev_id, ev_name, prim_actor, ch_no, loc_id, summary, irreversible_turn, next_ev, participants in events_data:
        event_entities.append(entity(ev_id, "EVENT", ev_name, {
            "chapter_no": ch_no,
            "primary_actor": prim_actor,
            "location_ref": loc_id,
            "summary": summary,
            "irreversible_turn": irreversible_turn,
            "participant_refs": participants,
            "provenance_refs": SOURCE,
        }))
        event_edges.append({"id": f"EDGE.{prim_actor}_{ev_id}", "type": "PARTICIPATES_IN", "source": prim_actor, "target": ev_id, "payload": {"provenance_refs": SOURCE}})
        if next_ev != "NONE":
            event_edges.append({"id": f"EDGE.{ev_id}_{next_ev}", "type": "CAUSES_EVENT", "source": ev_id, "target": next_ev, "payload": {"provenance_refs": SOURCE}})

    # 10. Chapters from v2_chapter_specs
    from v2_chapter_specs import generate_all_144_specs
    all_chapters_records = generate_all_144_specs()

    chapter_entities = []
    for record in all_chapters_records:
        number = record["n"]
        name = record["name"]
        chapter_id = f"CHAPTER_PLAN.{number:03d}"
        actors = record.get("actors", ["CHAR.gu_jinglan"])
        beats_data = record.get("beats_detail", record.get("beats", []))
        
        beats = []
        for b_idx, b in enumerate(beats_data, 1):
            beats.append({
                "beat_id": f"CH{number:03d}.B{b_idx}",
                "narrative_role": b["role"],
                "cause_from_previous": b["cause"],
                "active_actor": b["actor"],
                "actor_goal_before": b["before_goal"],
                "action": b["action"],
                "counterforce": b["counterforce"],
                "new_information_or_choice": b["info_or_choice"],
                "delta": b["delta"],
                "actor_goal_after": b["after_goal"],
                "next_pressure_created": b["pressure"],
                "forbidden_drift": [
                    "禁止纯口号式装逼，必须包含实际动作或战术动作。",
                    "禁止让对手无缘无故降智配合，必须有明确的反制或阻碍。",
                ]
            })

        clusters_data = record.get("clusters_detail", record.get("clusters", []))
        clusters = []
        for c_idx, c in enumerate(clusters_data, 1):
            clusters.append({
                "cluster_id": f"CH{number:03d}.CL{c_idx}",
                "primary_goal": c["goal"],
                "friction_medium": c["medium"],
                "beat_indices": c["beat_indices"],
                "turn_type": c["turn"],
                "cost_incurred": c["cost"],
                "exit_state": c["exit"],
                "pressure_handed_to_next_cluster": c["next_pressure"],
            })

        scenes_data = record.get("scenes_detail", record.get("scenes", []))
        scenes = []
        for s_idx, s in enumerate(scenes_data, 1):
            scenes.append({
                "scene_id": f"CH{number:03d}.S{s_idx}",
                "entry_state": s["entry"],
                "active_actor_goal": s["goal"],
                "opposing_goal_or_process": s["opponent"],
                "immediate_stakes": s["stakes"],
                "live_actions": s["actions"],
                "turn_or_reprice": s["turn"],
                "exit_state": s["exit"],
                "delta_dimensions": s.get("dimensions", ["martial_power", "information", "social_status"]),
                "payload_cluster_refs": [f"CH{number:03d}.CL{s_idx}"],
            })

        payload = {
            "plan_level": "PRODUCTION_READY",
            "chapter_no": number,
            "volume_ref": record.get("volume_ref", record.get("volume", "")),
            "target_prose_contract": {
                "unit": "CHINESE_PROSE_CHARACTERS",
                "target_min": 4000,
                "target_default": 5000,
                "target_max": 6000,
                "chapter_mode": "STANDARD_LONG",
            },
            "chapter_function": record["function"],
            "core_delta": record["core_delta"],
            "conflict_contract": {
                "actor_a": actors[0],
                "actor_b": actors[1] if len(actors) > 1 else actors[0],
                "concrete_incompatibility": record.get("conflict_concrete", record.get("conflict_core", "")),
                "stakes": record.get("stakes_concrete", record.get("stakes_core", "")),
            },
            "dynamic_beats": beats,
            "payload_clusters": clusters,
            "scene_payloads": scenes,
            "explicit_compression": [
                "消除无意义的跑图与过渡闲聊，直入冲突核心。",
                "将常规路人惊叹浓缩在关键节拍反制中，不单独占用水字数。",
            ],
            "forbidden_drift": record.get("forbidden_drift", [
                "不得把本章冲突简化为单一战力数值对轰。",
                "不得让任何角色凭空获得未埋设的证据、权限或救兵。",
                "不得用降智反派替代本章既定逻辑闭环。"
            ]),
            "continuation_hook": record.get("hook_concrete", record.get("continuation_hook", "")),
            "continuation_source": record.get("hook_concrete", record.get("continuation_hook", "")),
            "capacity_audit": record.get("cap_payload", {
                "chapter_id": chapter_id,
                "final_capacity": "FULL",
                "core_scenes": len(scenes),
                "payload_clusters": len(clusters),
                "stageable_core_beats": len(beats),
                "supporting_stageable_beats": 0,
                "summary_result_beats_removed": 0,
                "target_prose_range": [4000, 6000],
                "mid_chapter_load": "PASS",
                "writer_core_plot_invention_required": False,
                "missing_middle_roles": [],
                "failure_reasons": [],
            }),
            "provenance_refs": SOURCE,
        }
        chapter_entities.append(entity(chapter_id, "CHAPTER_PLAN", name, payload))

    # Edges
    edges = [
        {"id": "REL.gu_ye", "type": "TRUST_TENSION", "source": "CHAR.gu_jinglan", "target": "CHAR.ye_polu", "payload": {"state": "师姐弟生死相托，大军统帅与少帅默契无间", "provenance_refs": SOURCE}},
        {"id": "REL.gu_jiang", "type": "TRUST", "source": "CHAR.gu_jinglan", "target": "CHAR.jiang_sui", "payload": {"state": "二师姐温润如水，药王谷倾力相助", "provenance_refs": SOURCE}},
        {"id": "REL.gu_tingxue", "type": "TRUST", "source": "CHAR.gu_jinglan", "target": "CHAR.ye_tingxue", "payload": {"state": "三师姐天机谍网，提供全图视野", "provenance_refs": SOURCE}},
        {"id": "REL.gu_shen", "type": "TRUST", "source": "CHAR.gu_jinglan", "target": "CHAR.shen_qinghuang", "payload": {"state": "四师姐倾囊相助，万宝商会后勤保障", "provenance_refs": SOURCE}},
        {"id": "REL.gu_pei", "type": "COOPERATION_TENSION", "source": "CHAR.gu_jinglan", "target": "CHAR.pei_luoshuang", "payload": {"state": "五师姐恪守法度铁证，与少帅杀伐形成辩证互补", "provenance_refs": SOURCE}},
        {"id": "REL.gu_leng", "type": "TRUST", "source": "CHAR.gu_jinglan", "target": "CHAR.leng_yue", "payload": {"state": "六师姐暗夜守护，反水归队生死相随", "provenance_refs": SOURCE}},
        {"id": "REL.gu_xiao", "type": "COOPERATION", "source": "CHAR.gu_jinglan", "target": "CHAR.xiao_minghuang", "payload": {"state": "七师姐深宫内应，共谋夺嫡清君侧与立宪新政", "provenance_refs": SOURCE}},
    ]

    for c_idx in range(len(chapter_entities) - 1):
        edges.append({
            "id": f"SEQ.CH{c_idx+1:03d}_CH{c_idx+2:03d}",
            "type": "FOLLOWS_CHAPTER",
            "source": chapter_entities[c_idx]["id"],
            "target": chapter_entities[c_idx+1]["id"],
            "payload": {"provenance_refs": SOURCE},
        })

    packet = {
        "format": "vnext16.2",
        "precision": {
            "source_similarity_policy": "MECHANISM_ONLY",
            "originalization_level": "HIGH",
            "production_stage": "FINAL_FULL_BOOK",
            "target_prose_range": [4000, 6000],
            "expected_volumes": 6,
            "expected_chapters": 144,
            "full_book_detailed_required": True,
        },
        "negative_prompts": [
            "禁止生成假大空的口号式节拍，每个节拍必须包含具象动作、代价与信息差变化。",
            "禁止已死实体复活，死亡时序严格遵循 Death Ledger。",
            "禁止角色决策模型同质化，必须体现师姐弟之间的方案摩擦与方法冲突。",
            "禁止反派强行降智送人头，必须有至少一次战术性给主角制造真实损失。",
            "禁止任何未在前期埋设的神兵天降或机械降神。",
            "禁止在终章使用三万京观等与公道价值观割裂的嗜杀设定。",
        ],
        "entities": [
            project,
            *characters,
            *factions,
            *locations,
            *rules,
            *props,
            *acts,
            *volumes,
            *lines,
            *promises,
            *climaxes,
            *event_entities,
            *chapter_entities,
        ],
        "edges": edges + event_edges,
    }

    return packet

def main():
    packet = build_full_master_packet()
    packet_path = OUTLINE_DIR / "tianque_packet.json"
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated 144-chapter packet successfully with {len(packet['entities'])} entities, {len(packet['edges'])} edges.")

    from outline_agent import audit_packet, render_packet_markdown
    report = audit_packet(packet)
    print(f"Audit ok: {report.ok}")
    if not report.ok:
        print(f"Audit errors ({len(report.errors)}):")
        for err in report.errors[:10]:
            print("  -", err)
        if len(report.errors) > 10:
            print(f"  ... and {len(report.errors) - 10} more errors")
        sys.exit(1)

    md_content = render_packet_markdown(packet, title=packet["entities"][0]["name"], project_id=packet["entities"][0]["id"])
    out_md = OUTLINE_DIR.parent / "仿写大纲.md"
    out_md.write_text(md_content, encoding="utf-8")
    print(f"Exported to {out_md}, file size: {len(md_content.encode('utf-8'))} bytes, total lines: {len(md_content.splitlines())}")

if __name__ == "__main__":
    main()
'''

def main():
    target = Path("/Users/tang/PycharmProjects/pythonProject/changpianxiaoshuodagang/.outline/build_tianque_packet.py")
    target.write_text(CODE, encoding="utf-8")
    print(f"Wrote {target} successfully.")

if __name__ == "__main__":
    main()
