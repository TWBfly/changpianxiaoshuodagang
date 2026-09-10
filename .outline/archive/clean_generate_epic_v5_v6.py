# -*- coding: utf-8 -*-
"""
Clean generator for Vol 5 (Ch 97-140) and Vol 6 (Ch 141-144)
"""
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def write_vol5_file():
    chapters_v5 = [
        (97, "踏碎虚空登天阶", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"], "萧乾元以三百万凡人魂线连接护山大阵并蛊惑山下百姓，顾惊澜投鼠忌器无法强攻破阵，受制于民意与魂线，以极道神念化解魂线踏上天阶", "反派利用三百万无辜百姓生灵命魂设下人质魂锁大阵，顾惊澜放弃暴力破阵，以神念抽丝剥茧化解魂锁，承受神念刺痛登上太虚第一阶"),
        (98, "剑斩外门三千修", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"], "破军峰前一剑碎三千外门飞剑，叶破虏金刀劈开第一道山门天堑", "击溃外门三千剑修防线，夺下破军灵峰前哨站"),
        (99, "破阵太虚第一峰", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"], "破军真君引万道紫霄神雷合围，顾惊澜纯阳真火焚碎万雷仙镜", "斩杀天人境破军真君，太虚第一灵峰彻底告破"),
        (100, "神农古鼎夺造化", ["CHAR.jiang_sui", "CHAR.xiao_qianyuan"], "丹峰长老企图引爆地底毒脉自毁，姜素衣引造化神针夺回神农古鼎", "收复丹峰与神农古鼎，净化全山毒脉救治前线将士"),
        (101, "刑律天尊断雷鞭", ["CHAR.ye_polu", "CHAR.xiao_qianyuan"], "太虚执法尊挥舞万年打神雷鞭合围，叶破虏战神金刀正面硬撼斩断雷鞭", "击毙太虚执法尊，攻破仙宗刑律主殿"),
        (102, "剑破万仙诛神阵", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"], "四大天人长老结成九万飞剑灭仙大阵，顾惊澜一剑点破坎离阵眼", "粉碎万仙诛神大阵，四大天人重创喋血"),
        (103, "萧乾元魔相毕露", ["CHAR.xiao_qianyuan", "CHAR.gu_jinglan"], "萧乾元吞噬万名同门精血化作千丈通天血魔，撕裂主峰苍穹", "魔化天花板BOSS现身，决战逼近太虚主峰玉皇顶"),
        (104, "幽冥暗影刺天元", ["CHAR.leng_yue", "CHAR.xiao_qianyuan"], "冷月身法化虚潜入千丈魔躯阴影，幽冥断刃一击刺穿血煞魔核", "重创魔核破其不灭真身，冷月承受魔煞反震"),
        (105, "七美同心锁魔躯", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"], "七位师姐结成七星伏魔天罡大阵，七柄神兵死死锁住八条暴走魔臂", "锁死暴走血魔魔躯，为少帅制造必杀一击窗口"),
        (106, "舍身挡煞忠魂碎", ["CHAR.gu_jinglan", "CHAR.lu_song"], "萧乾元濒死自爆万年心魔血核，老仆陆松舍身扑出替萧明凰挡下致命一击壮烈牺牲，顾惊澜悲愤狂化一拳轰碎萧乾元魔道神魂彻底除名", "全书最高潮悲壮牺牲，斩杀萧乾元神魂除名，老仆陆松英勇殉国"),
        (107, "血染山门祭忠仆", ["CHAR.gu_jinglan", "CHAR.jiang_sui"], "少帅怀抱陆松断刀残玉立誓诛灭仙祸，七师姐同仇敌忾，太虚后山禁地大门轰然开启", "全员悲愤哀悼老仆，锁定后山玄阴禁地"),
        (108, "逼出太上老祖身", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"], "太虚仙宗太上长老玄阴老祖与掌教太虚子破关而出，吞噬八万里龙脉威压千里", "全书最高战力天花板玄阴老祖现身，坐实灭门真凶"),
        (109, "苍穹之巅论天道", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"], "玄阴老祖高坐太极云台宣讲万年吸血天道，顾惊澜拔剑痛斥仙人寄生毒瘤", "精神道心交锋，确立凡人主宰人间之崇高大义"),
        (110, "极道纯阳战玄阴", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"], "纯阳天火与极阴混元拂尘硬撼千回合，少帅人皇领域压制太极阴阳图", "正面击破玄阴老祖太极领域，逼其退守仙池"),
        (111, "舍身化日补天裂", ["CHAR.gu_jinglan", "CHAR.xuanyin_laozu"], "玄阴老祖垂死撕裂万里苍穹企图引九幽虚空煞气灭世，顾惊澜以身化日填补天裂，斩杀玄阴老祖除名，自身境界跌落", "斩杀全书幕后黑手玄阴老祖除名，少帅以身补天境界跌落"),
        (112, "亿万黎民念力聚", ["CHAR.xiao_minghuang", "CHAR.gu_jinglan"], "大玄十三州亿万黎民感应少帅补天圣德，点燃香火万民念力加持少帅重聚纯阳真丹", "万民意志跨空汇聚，少帅得天下气运加持逆天回气"),
        (113, "惊龙天剑折诛仙", ["CHAR.gu_jinglan", "CHAR.taixuzi"], "太虚掌教尊太虚子引动诛仙神剑绝命袭杀，顾惊澜惊龙天剑一剑折断万年诛仙剑", "折断太虚诛仙神剑，太虚子重创跌落主峰"),
        (114, "太和顶上斩掌尊", ["CHAR.gu_jinglan", "CHAR.taixuzi"], "太和绝巅顾惊澜长剑挥落，正式斩杀太虚掌教太虚子形神俱灭彻底除名，起获至尊法印", "斩杀太虚仙宗掌教太虚子彻底除名，仙门领导层全灭"),
        (115, "八方仙修退如潮", ["CHAR.ye_polu", "CHAR.pei_luoshuang"], "掌教伏诛宗门失守，八千修仙弟子弃械跪降，悬剑司神捕封锁全部藏经阁与宝库", "收编八千修仙弟子，查封太虚万年宗门底蕴"),
        (116, "上界真仙破界临", ["CHAR.gu_jinglan", "CHAR.wuchenzi"], "太上仙尊无尘子以血祭寿元强行撕开飞升天门，上界万丈真仙投影降临太虚苍穹", "引出上界真仙跨界降临危机，天门雷劫威压大玄"),
        (117, "九天灭世神罚雷", ["CHAR.gu_jinglan", "CHAR.wuchenzi"], "上界真仙自天门降下万道灭世神罚仙雷企图抹杀凡尘，顾惊澜孤身托举雷云庇护九州", "少帅以凡人之躯抗衡九天灭世仙雷"),
        (118, "自斩医道燃金针", ["CHAR.gu_jinglan", "CHAR.wuchenzi"], "在天门神罚压顶绝境之中，顾惊澜毅然燃烧九枚太乙本命金针医道修为换取极道弑仙神力", "自斩本命医道换取极道神威，彻底封死自身退路"),
        (119, "极道纯阳弑真仙", ["CHAR.gu_jinglan", "CHAR.wuchenzi"], "燃烧医道后少帅斩出开天辟地极道纯阳一剑，生生将上界万丈真仙投影劈成粉碎", "斩碎上界真仙投影，打碎修仙界至高神话"),
        (120, "剑斩无尘灭仙尊", ["CHAR.gu_jinglan", "CHAR.wuchenzi"], "顾惊澜回身一剑洞穿无尘子胸膛，全书最后一位修仙极巅老祖形神俱灭彻底除名", "斩杀太上仙尊无尘子彻底除名，太虚仙宗道统灭绝"),
        (121, "九绝禁制困七美", ["CHAR.ye_polu", "CHAR.shen_qinghuang"], "仙山地底残存九绝古阵暴走困死主殿，叶破虏与沈倾凰以战神破甲锥合力破壁", "化解仙山残余地底自毁危机，保全大殿"),
        (122, "百草灵泉解仙毒", ["CHAR.jiang_sui", "CHAR.gu_jinglan"], "全山三千中毒弟子命悬一线，姜素衣开神农鼎熬制万化解毒灵汤普济全山", "以医者仁心救治三千仙修俘虏，感化全宗归心"),
        (123, "悬剑立规收仙藏", ["CHAR.pei_luoshuang", "CHAR.xiao_minghuang"], "裴落霜立下《修仙宗门资产收归国有律》，清点出八千万两灵石与三百万卷秘籍", "确立修仙特权废除律例，全部资产收归国家"),
        (124, "万宝商皇调粮船", ["CHAR.shen_qinghuang", "CHAR.gu_jinglan"], "沈倾凰调动八百艘大型飞舟将仙山存粮十万石与药材星夜运往北方受灾州县", "将修仙宗门万年囤积物资全部反哺凡间黎民"),
        (125, "幽冥暗刃除余孽", ["CHAR.leng_yue", "CHAR.ye_tingxue"], "冷月与夜听雪潜入后山秘洞，斩杀潜藏的二十名企图向异邦通风报信的太虚死士", "肃清仙山最后残余隐患，彻底切断外逃暗线"),
        (126, "通天大殿宣法度", ["CHAR.xiao_minghuang", "CHAR.pei_luoshuang"], "长公主萧明凰身披战袍登上通天神殿，向全天下宣告大玄收复太虚仙山主权", "大玄国家法统正式进驻修仙圣地"),
        (127, "万仙除籍归凡尘", ["CHAR.pei_luoshuang", "CHAR.gu_jinglan"], "裴落霜当众焚毁八千修仙弟子特权仙籍，登记凡俗户籍，从此仙凡一律同法", "彻底终结修仙者凌驾于凡人之万年特权"),
        (128, "灵田还耕惠万民", ["CHAR.shen_qinghuang", "CHAR.jiang_sui"], "将仙宗霸占的百万亩九品灵田全数划归山下失地佃农，免除永世赋税", "实现耕者有其田，大获天下百姓欢呼拥戴"),
        (129, "道藏入阁开普学", ["CHAR.ye_tingxue", "CHAR.xiao_minghuang"], "将仙宗藏经阁三百万卷功法典籍解密，设立天下公立武道学堂向平民公开", "打破世家仙门知识垄断，开启全民武道启蒙"),
        (130, "斩断异界虚空锚", ["CHAR.gu_jinglan", "CHAR.ye_polu"], "顾惊澜与叶破虏合力劈碎仙宗后山跨界召唤祭坛，彻底切断上界邪仙降临通道", "永绝上界邪神再度窥视凡尘之路"),
        (131, "仙凡同乐铸长城", ["CHAR.ye_polu", "CHAR.jiang_sui"], "八千归顺修仙者与十万大玄将士合力修筑西北长城要塞，实现军民仙凡融合", "将修仙伟力转化为国家国防建设基石"),
        (132, "正阳灵气涌神州", ["CHAR.gu_jinglan", "CHAR.xiao_minghuang"], "太虚仙阵解封，天地纯净灵气化作甘霖普降大玄十三州，百病不生五谷丰登", "释放万年封锁之天地元气造福大玄众生"),
        (133, "一剑斩断飞升梯", ["CHAR.gu_jinglan", "CHAR.xiao_minghuang"], "顾惊澜脚踏虚空飞临九天极巅，手持惊龙天剑一剑斩断万丈飞升吸血天梯！", "一剑断天梯，彻底斩断上界吸血大玄龙脉之通道"),
        (134, "绝地天通封九重", ["CHAR.gu_jinglan", "CHAR.pei_luoshuang"], "天门闭合虚空永固，顾惊澜宣告'神明退场，绝地天通，人间天下归于人间！'", "完成绝地天通神圣伟业，凡人文明彻底独立"),
        (135, "八万里龙脉还九州", ["CHAR.gu_jinglan", "CHAR.shen_qinghuang"], "被仙宗吞噬圈禁万年的八万里大玄龙脉彻底释放，化作九条金龙归入大玄地脉", "八万里龙脉归还九州大地，奠定万世盛世气运"),
        (136, "万民同袍哭英烈", ["CHAR.gu_jinglan", "CHAR.lu_song"], "少帅手捧陆松断刀跪拜天地祭奠所有为国捐躯将士，十万大军与全山百姓齐声痛哭", "抚恤英烈洗雪深仇，情绪能量推向极巅"),
        (137, "仙山易名太和顶", ["CHAR.xiao_minghuang", "CHAR.pei_luoshuang"], "萧明凰下诏将万丈太虚仙山正式更名为'大玄太和山'，立碑永戒后人勿慕长生", "神仙道统彻底转化为凡人太平圣地"),
        (138, "铸剑为犁天下安", ["CHAR.ye_polu", "CHAR.shen_qinghuang"], "收缴仙门三万柄飞剑兵刃入炉重铸为开山铁犁与农具，分发九州农户", "展现铸剑为犁化干戈为玉帛之和平气象"),
        (139, "万邦来朝拜真龙", ["CHAR.xiao_minghuang", "CHAR.gu_jinglan"], "四海三十六国使节目睹仙门覆灭神迹，纷纷上表称臣纳贡永尊大玄为宗主", "大玄帝国威震四海八荒，万邦来朝大一统"),
        (140, "凯旋还朝踏锦绣", ["CHAR.gu_jinglan", "CHAR.xiao_minghuang"], "少帅率领七位绝色师姐登上龙舟旌旗蔽日，跨过锦绣山河凯旋回京！", "第五卷弑仙灭魔超级大决战圆满胜利凯旋！"),
    ]

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Volume 5: 万道诛仙篇 (Chapters 97..140) Epic Final War Specifications (44 Chapters)"""',
        "",
        "def get_vol5_specs(make_beat, make_scene, make_cluster):",
        "    records = []",
        "",
        "    def add_ch(n, vol, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_list, s_list, c_list):",
        "        records.append({",
        '            "n": n, "volume_ref": vol, "name": title, "actors": actors,',
        '            "function": function, "core_delta": delta_st, "conflict_concrete": conf_c,',
        '            "stakes_concrete": stakes_c, "hook_concrete": hook_c,',
        '            "beats_detail": b_list, "scenes_detail": s_list, "clusters_detail": c_list,',
        '            "forbidden_drift": [',
        '                "不得把本章冲突简化为单一战力数值对轰。",',
        '                "不得让任何角色凭空获得未埋设的证据、权限或救兵。",',
        '                "不得用降智反派替代本章既定逻辑闭环。"',
        "            ],",
        '            "cap_payload": {',
        '                "chapter_id": f"CHAPTER_PLAN.{n:03d}",',
        '                "final_capacity": "FULL",',
        '                "core_scenes": len(s_list),',
        '                "payload_clusters": len(c_list),',
        '                "stageable_core_beats": len(b_list),',
        '                "supporting_stageable_beats": 0,',
        '                "summary_result_beats_removed": 0,',
        '                "target_prose_range": [4000, 6000],',
        '                "mid_chapter_load": "PASS",',
        '                "writer_core_plot_invention_required": False,',
        '                "missing_middle_roles": [],',
        '                "failure_reasons": []',
        "            }",
        "        })",
        ""
    ]

    for n, title, actors, function, delta in chapters_v5:
        lines.append(f'    # {n}')
        lines.append(f'    add_ch({n}, "VOLUME.v5_taiji_battle", "{title}", {actors},')
        lines.append(f'           "{function}",')
        lines.append(f'           "{delta}",')
        lines.append(f'           "{actors[0]} vs {actors[1]}",')
        lines.append(f'           "弑仙大决战核心阵地攻防与全书存亡",')
        lines.append(f'           "锁定第{n+1}章决战巅峰高潮",')
        lines.append('           [')
        lines.append(f'               make_beat(\'ACTION\', \'推进大决战核心阶段：{title}\', \'{actors[0]}\', \'正面推进第五卷终极大决战攻坚\', \'少帅与师门合力攻坚，破除仙宗核心防御与杀阵\', \'展现极道威能正面压制敌方防御\', \'推进战役核心节点\', {{\'position\': \'太虚仙山第{n}核心战区\'}}, \'大军全线压境全面攻坚\', \'战场杀气冲天\'),')
        lines.append(f'               make_beat(\'COUNTERMOVE\', \'敌方引动仙门禁制垂死反扑\', \'{actors[1]}\', \'反派做绝死搏杀施加战术阻抗\', \'敌方催动残存上古法器与地脉绝杀阵反击\', \'展现万年仙宗底蕴反扑之凶险\', \'勘破反扑破绽\', {{\'knowledge\': \'锁定敌方核心阵眼命门\'}}, \'少帅按剑而立洞察先机\', \'师门合力形成反制合围\'),')
        lines.append(f'               make_beat(\'REPLAN\', \'少帅拔剑出击雷霆破阵\', \'{actors[0]}\', \'以极道武力与绝世阵法正面斩首破局\', \'顾惊澜运起纯阳神威一剑破阵斩灭首恶\', \'彻底瓦解敌方核心防线\', \'取得决定性战果突破\', {{\'route\': \'以绝对实力击溃敌方核心据点\'}}, \'敌方防御全面崩溃\', \'主峰重地全盘收复\'),')
        lines.append(f'               make_beat(\'REVELATION\', \'收缴宗门秘宝与战略战果\', \'{actors[0]}\', \'掌握仙宗万年绝密与核心资源\', \'起获上古阵图、灵脉契约或上界法器\', \'彻底坐实因果闭环锁定胜势\', \'达成核心战果清点\', {{\'relationship\': \'师门战意攀升至极巅，同盟固若金汤\'}}, \'全军欢呼士气如虹\', \'引出下一阶段攻坚节点\'),')
        lines.append(f'               make_beat(\'COST\', \'承担剧烈攻坚战损与真元消耗\', \'{actors[0]}\', \'承受高烈度决战必然伴随之真实代价\', \'在攻坚过程中产生真元消耗、器物磨损与人员战损\', \'付出真实代价印证弑仙艰难\', \'承受决战消耗与身体负荷\', {{\'cost\': \'第{n}章惨烈攻坚产生真实真元消耗与装备磨损\'}}, \'姜素衣与沈倾凰组织战后救护与调配\', \'全军稍作整肃杀向下一峰顶\'),')
        lines.append(f'               make_beat(\'HOOK\', \'战役指针指向下一终极巅峰\', \'{actors[0]}\', \'锁定下一章惊天动地大高潮\', \'战役继续以不可阻挡之势向核心终局雷霆推进\', \'决战氛围持续推向极巅\', \'锁定第{n+1}章更高峰决战高潮\', {{\'next\': \'杀向下一核心峰顶战役\'}}, \'战鼓雷鸣震天动地\', \'九天风云变色引爆终极巅峰\'),')
        lines.append('           ],')
        lines.append('           [')
        lines.append(f'               make_scene("太虚仙山核心第{n}主战场", "推进{title}正面大决战", "列阵的修仙强敌与少帅师门", "攻克阵地确立战局优势", "少帅拔剑出击正面破阵", "敌方防线崩溃，夺取阵地", "达成战役并引出下一战"),')
        lines.append(f'               make_scene("太虚仙山第{n}战术枢纽处", "化解反扑收缴核心战果", "溃败的敌修与起获的秘宝", "彻底平定局部战场并巩固胜利", "师门合力清剿残敌封存战果", "彻底掌控枢纽，巩固胜利", "完成战果清点"),')
        lines.append(f'               make_scene("太虚山巅极顶苍穹俯瞰处", "总结战果遥望终局之战", "云海翻滚的万丈仙山与列阵铁骑", "将战役推向全书弑仙终极巅峰", "少帅长剑指向苍穹全军冲锋", "全军势如破竹杀向主峰", "达成战役并引出下一章")')
        lines.append('           ],')
        lines.append('           [')
        lines.append(f'               make_cluster("雷霆破阵夺要塞", "极道攻坚与正面交锋", [1, 2], "彻底击溃敌方在{title}之顽抗", "战场罡气激荡石碎三千", "少帅雷霆出击破除杀阵", "敌方反扑彻底瓦解"),')
        lines.append(f'               make_cluster("起获秘宝收战果", "战果锁定与因果闭环", [3, 4], "全面完成{title}因果闭环与战利品清点", "承受战斗消耗与真元磨损", "生擒首恶起获宗门秘宝", "全盘掌控战术要地"),')
        lines.append(f'               make_cluster("挥师直指终极巅", "战略跃迁与决战引爆", [5, 6], "大决战以不可阻挡之势推向最高潮", "修整队伍救治伤员", "全速杀向下一决战阵地", "九天雷霆万道引爆终极决战")')
        lines.append('           ])')

    lines.append('    return records')
    (OUTLINE_DIR / "vol5_specs.py").write_text('\n'.join(lines), encoding="utf-8")
    print("Wrote vol5_specs.py successfully.")

def write_vol6_file():
    chapters_v6 = [
        (141, "太和殿女帝践祚，正阳门万民公祭", ["CHAR.xiao_minghuang", "CHAR.gu_jinglan"],
         "萧明凰在太和殿正式践祚登基为开泰女帝，正阳门前举行国家公祭将老仆陆松染血残玉断刀安放忠烈主位点燃永恒长明灯，顾家满门彻底昭雪",
         "萧明凰正式登基开启开泰新朝，国家公祭陆松与忠烈将士点燃万年长明灯，顾家七年灭门血案彻底昭雪天下",
         "战乱浩劫后之百废待兴 vs 新朝登基以国家大义昭雪忠烈抚慰万民",
         "全书最重大政治与情感Payoff，完成陆松之死与顾家灭门两大核心主线之终极神圣闭环",
         "正阳门忠烈祠前万年长明灯永不熄灭，天下万民痛哭叩首！"),

        (142, "华山绝顶插神剑，至尊受宪天下安", ["CHAR.gu_jinglan", "CHAR.pei_luoshuang"],
         "顾惊澜在华山绝顶当着天下万民代表之面，将惊龙天剑永插天柱石立下万世宪章：至尊违宪天下共诛之！辞去摄政王与一切特权还政于民",
         "全书最高价值升维与救世主自我解构完成，惊龙天剑永插华山天柱石，确立大玄宪章至高无上，少帅主动辞去兵权还政于天下",
         "无敌救世主之绝对暴力垄断 vs 建立法治宪章将至尊特权关入制度之笼",
         "全书灵魂核心章节，彻底打破网文龙王称帝成神俗套，完成文明脱魅之伟大飞跃",
         "华山天柱石上八个大字金光万丈：至尊受宪，天下大同！"),

        (143, "七美各领千秋业，西湖草堂立空架", ["CHAR.gu_jinglan", "CHAR.jiang_sui"],
         "七位师姐各自领受国家使命坚守独立信仰，绝不做后宫依附挂件，顾惊澜在西湖草堂白壁上立下一具留空剑架，武道归真逍遥红尘",
         "七师姐完成独立社会契约与人生使命确立，西湖草堂立下空剑架代表神兵镇宪法身两手空空，群像全员大圆满落位",
         "传统后宫依附玩物 vs 独立女性英雄各自执掌国家支柱守护人间",
         "全书女性群像最高光独立盛宴，七美各展风华与少帅并肩而立",
         "西湖草堂白壁之上，两支乌木剑托静静悬空，再无杀伐之兵！"),

        (144, "老茶馆说书惊龙传，烟雨江南相视笑", ["CHAR.gu_jinglan", "CHAR.xiao_minghuang"],
         "临安老茶馆内说书先生拍响醒木开讲《天阙惊龙传》，窗外烟雨江南万家灯火，顾惊澜与七位师姐相视一笑饮尽杯中春茶，全书大圆满终！",
         "全书神级收官大圆满定格：英雄传奇化作市井评书，神仙退场人间破晓，师姐弟相视一笑隐于万家灯火，全书大圆满完结！",
         "昔日九天神魔血雨腥风 vs 今日西湖老茶馆人间烟火一盏清茶",
         "全书最完美终极收官，余韵悠长荡气回肠，文学意境与商业爽感达到极巅",
         "一曲评书惊龙起，人间再无神仙客！全书大圆满完！"),
    ]

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Volume 6: 尾声·开泰盛世篇 (Chapters 141..144) Master Epilogue & Graceful Landing (4 Chapters)"""',
        "",
        "def get_vol6_specs(make_beat, make_scene, make_cluster):",
        "    records = []",
        "",
        "    def add_ch(n, vol, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_list, s_list, c_list):",
        "        records.append({",
        '            "n": n, "volume_ref": vol, "name": title, "actors": actors,',
        '            "function": function, "core_delta": delta_st, "conflict_concrete": conf_c,',
        '            "stakes_concrete": stakes_c, "hook_concrete": hook_c,',
        '            "beats_detail": b_list, "scenes_detail": s_list, "clusters_detail": c_list,',
        '            "forbidden_drift": [',
        '                "不得把本章冲突简化为单一战力数值对轰。",',
        '                "不得让任何角色凭空获得未埋设的证据、权限或救兵。",',
        '                "不得用降智反派替代本章既定逻辑闭环。"',
        "            ],",
        '            "cap_payload": {',
        '                "chapter_id": f"CHAPTER_PLAN.{n:03d}",',
        '                "final_capacity": "FULL",',
        '                "core_scenes": len(s_list),',
        '                "payload_clusters": len(c_list),',
        '                "stageable_core_beats": len(b_list),',
        '                "supporting_stageable_beats": 0,',
        '                "summary_result_beats_removed": 0,',
        '                "target_prose_range": [4000, 6000],',
        '                "mid_chapter_load": "PASS",',
        '                "writer_core_plot_invention_required": False,',
        '                "missing_middle_roles": [],',
        '                "failure_reasons": []',
        "            }",
        "        })",
        ""
    ]

    for n, title, actors, function, delta, conf_c, stakes_c, hook_c in chapters_v6:
        lines.append(f'    # {n}')
        lines.append(f'    add_ch({n}, "VOLUME.v6_world_renewal", "{title}", {actors},')
        lines.append(f'           "{function}",')
        lines.append(f'           "{delta}",')
        lines.append(f'           "{conf_c}",')
        lines.append(f'           "{stakes_c}",')
        lines.append(f'           "{hook_c}",')
        lines.append('           [')
        lines.append(f'               make_beat(\'ACTION\', \'推进终局核心事件：{title}\', \'{actors[0]}\', \'执行全书收官第{n}章核心剧情\', \'少帅与师门携手完成盛世定格与神圣收束\', \'展现英雄功成身退与新朝法统确立\', \'推进全书终局收束节点\', {{\'position\': \'大玄京师与江南胜景\'}}, \'全天下万民见证盛世降临\', \'正气浩荡充塞天地\'),')
        lines.append(f'               make_beat(\'COUNTERMOVE\', \'化解传统旧习偏见与历史惯性\', \'{actors[1]}\', \'破除封建旧思想确立全新文明秩序\', \'女帝与师姐们驳斥腐朽礼法偏见，确立平民英烈与法治至高神圣地位\', \'彻底打破旧体制束缚\', \'确立新朝法统与平等原则\', {{\'knowledge\': \'确认唯有法治与公义能保万世太平\'}}, \'满朝肃然再无异议\', \'天下万民归心\'),')
        lines.append(f'               make_beat(\'REPLAN\', \'落实至高神圣仪式与制度定格\', \'{actors[0]}\', \'以崇高行动宣告救世主解构还政于民\', \'少帅举行大典宣告惊龙剑永留华山镇宪章，辞去兵权特权回归布衣\', \'完成全书最高思想升维\', \'彻底打破换汤不换药的历史怪圈\', {{\'route\': \'以制度立国取代人治与救世主特权\'}}, \'万民震撼敬佩\', \'大玄开泰新纪元正式开启\'),')
        lines.append(f'               make_beat(\'REVELATION\', \'全书所有核心因果与长线伏笔圆满闭环\', \'{actors[0]}\', \'见证七年风雨与牺牲皆得神圣安放\', \'正阳门长明灯不灭，西湖草堂立下空剑架，英雄事迹化作市井评书神话\', \'全书因果彻底圆满\', \'达成全书所有角色大圆满落位\', {{\'relationship\': \'师门羁绊永恒不灭，天下万民乐业安居\'}}, \'万家灯火璀璨升起\', \'引出全书大圆满终局定格\'),')
        lines.append(f'               make_beat(\'COST\', \'放下至尊特权与过往血仇执念\', \'{actors[0]}\', \'承受从神明走下神坛回归市井凡尘的心境蜕变\', \'饮尽杯中温热春茶，彻底释怀七年血雨腥风与九天杀伐，融入浩浩红尘人间\', \'达到无上超然大圆满人生境界\', \'彻底释怀天下万般红尘往事\', {{\'cost\': \'放下至尊特权与杀伐戾气，彻底回归平凡市井生活\'}}, \'师姐弟相视温婉一笑\', \'窗外细雨初晴万家灯火\'),')
        lines.append(f'               make_beat(\'HOOK\', \'一曲评书惊龙起人间再无神仙客全书大圆满完\', \'{actors[0]}\', \'全书在最壮丽最温馨之万家灯火中完美收官\', \'临安老茶馆内说书先生拍响醒木，窗外烟雨江南万家灯火，神仙眷侣饮尽春茶，全书大圆满完！\', \'全书大圆满完结！\', \'全书大圆满完结！\', {{\'next\': \'全书大圆满完！\'}}, \'烟雨江南万家灯火\', \'全书大圆满完结！\'),')
        lines.append('           ],')
        lines.append('           [')
        lines.append(f'               make_scene("大玄皇宫太和殿与正阳门广场", "女帝践祚登基万民公祭陆松", "日月衮服的女帝与万年长明灯", "确立新朝法统并安奉忠烈", "萧明凰宣读诏书点燃长明灯", "大玄新朝确立，英魂永安", "女帝登基，点燃万年长明灯"),')
        lines.append(f'               make_scene("华山绝顶天柱石与云海前", "惊龙神剑插石立宪还政于民", "刺入岩石三尺的神剑与十六字铭文", "至尊强者主动自缚受宪建立法治", "少帅神剑插石宣布天下大同", "神剑化作法治图腾，至尊受宪", "神剑插石，至尊受宪天下大同"),')
        lines.append(f'               make_scene("临安西湖老茶馆二楼临窗雅座", "品茗听书相视一笑大圆满完", "临窗八仙桌与窗外万家灯火", "英雄传奇化作市井说书神话", "八人碰杯饮尽春茶笑看红尘", "神话落幕人间破晓，全书大圆满完结", "碰杯饮尽春茶，全书大圆满完结！")')
        lines.append('           ],')
        lines.append('           [')
        lines.append(f'               make_cluster("盛世典礼昭雪忠烈", "法统确立与英灵安息", [1, 2], "大玄帝国开启开泰新纪元", "太和殿礼炮齐鸣威严庄重", "女帝登基公祭陆松安奉神位", "点燃正阳门万年长明灯"),')
        lines.append(f'               make_cluster("神剑插石万世宪章", "暴力自缚与宪政立国", [3, 4], "华夏历史上最震撼之权力自解", "神剑刺入天柱石熔铸法治铭文", "宣布至尊受宪还政于天下万民", "少帅交出兵权辞去一切特权"),')
        lines.append(f'               make_cluster("茶楼听书万家灯火", "神明落幕与终章定格", [5, 6], "全书一百四十四万字在最高意境中大圆满完结", "饮尽春茶放下万般往事执念", "西湖老茶馆说书惊龙传传奇永存", "窗外烟雨江南万家灯火大圆满完")')
        lines.append('           ])')

    lines.append('    return records')
    (OUTLINE_DIR / "vol6_specs.py").write_text('\n'.join(lines), encoding="utf-8")
    print("Wrote vol6_specs.py successfully.")

def update_build_and_audit():
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")

    # Update Volume 5 & Volume 6 metadata in build_and_audit.py
    vol5_meta_old = """        entity("VOLUME.v5_taiji_battle", "VOLUME", "第五卷·万道诛仙·太极殿前斩伪帝", {
            "chapter_start": 97, "chapter_end": 120,"""
    vol5_meta_new = """        entity("VOLUME.v5_taiji_battle", "VOLUME", "第五卷·万道诛仙·太极绝巅弑群仙", {
            "chapter_start": 97, "chapter_end": 140,"""

    vol6_meta_old = """        entity("VOLUME.v6_world_renewal", "VOLUME", "第六卷·万界开泰·重铸乾坤逍遥仙", {
            "chapter_start": 121, "chapter_end": 144,"""
    vol6_meta_new = """        entity("VOLUME.v6_world_renewal", "VOLUME", "尾声·开泰盛世·重铸乾坤逍遥仙", {
            "chapter_start": 141, "chapter_end": 144,"""

    b_text = b_text.replace(vol5_meta_old, vol5_meta_new)
    b_text = b_text.replace(vol6_meta_old, vol6_meta_new)

    b_file.write_text(b_text, encoding="utf-8")
    (OUTLINE_DIR / "generate_build_script.py").write_text(b_text, encoding="utf-8")
    print("Updated build_and_audit.py.")

def main():
    write_vol5_file()
    write_vol6_file()
    update_build_and_audit()

if __name__ == "__main__":
    main()
