# -*- coding: utf-8 -*-
"""
CANON LEDGERS (五大绝对冻结账本)
全局单一真实源 (Single Source of Truth)
用于约束所有分卷生成器与独立审查器，杜绝任何人物漂移、死亡错乱、政体矛盾与模板坍塌。
"""

# ==============================================================================
# 账本 1: 角色身份与性别账本 (CHARACTER LEDGER)
# ==============================================================================
CHARACTERS = {
    "CHAR.gu_jinglan": {
        "name": "顾惊澜",
        "gender": "M",
        "role": "男主角 / 天阙龙尊 / 天渊极道唯一总传人",
        "rank": "师弟 / 龙尊少帅",
        "weapon": "惊龙天剑 / 极道纯阳真气",
        "decision_model": "亲近者生命与人间公理 > 复仇快感 > 官府法统 > 自身安危",
        "core_conflict": "以绝对战力撕裂死局，但必须权衡师姐方案冲突与平民生息"
    },
    "CHAR.ye_polu": {
        "name": "叶破虏",
        "gender": "F",
        "role": "大师姐 / 护国女战神 / 镇北大将军 / 三十万幽燕铁骑统帅",
        "rank": "大师姐",
        "weapon": "九炼开山血刀 / 战神百战军阵",
        "decision_model": "边防城池与三十万士兵生命 > 师门私情 > 兵部皇命 > 个人官位",
        "forbidden_terms": ["大师兄", "师兄弟", "义兄", "男儿身", "兄弟情深"]
    },
    "CHAR.jiang_sui": {
        "name": "姜素衣",
        "gender": "F",
        "role": "二师姐 / 天下第一悬壶医仙 / 百草药王谷谷主",
        "rank": "二师姐",
        "weapon": "造化太乙神针 / 神农圣水 / 避毒清灵珠",
        "decision_model": "治病救人与平民安危 > 宗门独善其身 > 师门需求 > 自身安危",
        "core_conflict": "坚守医者仁心底线，坚决反对无差别毒杀敌军营垒"
    },
    "CHAR.ye_tingxue": {
        "name": "夜听雪",
        "gender": "F",
        "role": "三师姐 / 听风阁总楼主 / 千面魅影天下谍尊",
        "rank": "三师姐",
        "weapon": "流光天机扇 / 千面易容术 / 浑天星轨仪",
        "decision_model": "情报网存续与绝对信息优势 > 快速报仇 > 个人名誉",
        "core_conflict": "信奉信息不对称与暗盘交易，主张放长线钓大鱼"
    },
    "CHAR.shen_qinghuang": {
        "name": "沈倾凰",
        "gender": "F",
        "role": "四师姐 / 万国商会总会长 / 九州第一女财神",
        "rank": "四师姐",
        "weapon": "九宝算盘 / 九州平准仓 / 万国金券结算权",
        "decision_model": "全球商业信用与金融大盘安全 > 战术快速推平 > 商业利润 > 个人情感",
        "core_conflict": "坚决反对一刀切粗暴冻结账户伤害平民，主张用精准金融工具拆解敌对财阀"
    },
    "CHAR.pei_luoshuang": {
        "name": "裴落霜",
        "gender": "F",
        "role": "五师姐 / 皇家悬剑司首座 / 刑部总捕神",
        "rank": "五师姐",
        "weapon": "斩仙尚方刑刀 / 大玄律令天网",
        "decision_model": "程序正义与铁证确凿 > 结果正义 > 私人感情 > 皇权命令",
        "core_conflict": "恪守证据链闭环，在未拿到确凿铁证前严禁私刑处决朝廷命官"
    },
    "CHAR.leng_yue": {
        "name": "冷月",
        "gender": "F",
        "role": "六师姐 / 幽冥刺客联盟至尊暗皇 / 天下第一刺客",
        "rank": "六师姐",
        "weapon": "无影断魂刺 / 幽冥九遁",
        "decision_model": "师弟顾惊澜绝对安全 > 刺客联盟契约 > 世俗道德法律",
        "core_conflict": "主张直接暗杀拔除阻碍，与裴落霜的法理程序产生直接行动摩擦"
    },
    "CHAR.xiao_minghuang": {
        "name": "萧明凰",
        "gender": "F",
        "role": "七师姐 / 大玄长公主 -> 摄政监国 -> 开泰女帝",
        "rank": "七师姐",
        "weapon": "九章龙凤玉玺 / 君民共治宪章",
        "decision_model": "大玄江山平稳过渡与万民存续 > 皇权正统 > 个人复仇 > 宗室私利",
        "core_conflict": "在少帅军兵临城下时要求精准破城，避免大火焚烧三百万皇城百姓"
    }
}

# ==============================================================================
# 账本 2: 死亡与终局账本 (DEATH LEDGER)
# ==============================================================================
DEATH_LEDGER = {
    "CHAR.zhao_biao": {"name": "赵彪", "death_chapter": 1, "killer": "CHAR.gu_jinglan", "manner": "废去四肢武功挂尸长街示众"},
    "CHAR.zhao_xuan": {"name": "赵玄", "death_chapter": 2, "killer": "CHAR.gu_jinglan", "manner": "踩碎双膝废去全身经脉丹田沦为废人退场"},
    "CHAR.zhao_wuji": {"name": "赵无极", "death_chapter": 13, "killer": "CHAR.gu_jinglan", "manner": "寿宴送棺被顾惊澜当众斩首，生命永久终结"},
    "CHAR.wu_titian": {"name": "乌啼天", "death_chapter": 36, "killer": "CHAR.gu_jinglan", "manner": "太湖水寨被纯阳真火焚灭神魂伏诛，生命永久终结"},
    "CHAR.qian_wanjin": {"name": "钱万金", "death_chapter": 42, "killer": "CHAR.pei_luoshuang", "manner": "供状画押铁证如山，在西市刑场明正典刑斩首，生命永久终结"},
    "CHAR.wan_yan_badu": {"name": "完颜拔都", "death_chapter": 60, "killer": "CHAR.gu_jinglan", "manner": "天狼关决战被顾惊澜惊龙神剑斩断咽喉伏诛，生命永久终结"},
    "CHAR.yan_songqing": {"name": "严嵩卿", "death_chapter": 80, "killer": "CHAR.pei_luoshuang", "manner": "通敌铁证公诸天下，京师菜市口公审明正典刑斩首示众，生命永久终结"},
    "CHAR.zhao_tianlong": {"name": "赵天龙", "death_chapter": 84, "killer": "CHAR.gu_jinglan", "manner": "国舅宗祠决战被顾惊澜一剑贯穿丹田斩首伏诛，生命永久终结"},
    "CHAR.jiuyou_laozu": {"name": "鬼煞真人", "death_chapter": 92, "killer": "CHAR.gu_jinglan", "manner": "皇城地下引动山河真图与三昧真火彻底焚灭神魂，生命永久终结"},
    "CHAR.xiao_qianyuan": {"name": "萧乾元", "death_chapter": 101, "killer": "CHAR.gu_jinglan", "manner": "太极殿密道逃亡被截，服毒自尽皇权彻底终结，生命永久终结"},
    "CHAR.tianhuo_zhenren": {"name": "天火真人", "death_chapter": 62, "killer": "CHAR.gu_jinglan", "manner": "灵石峡纯阳真龙神拳捏碎仙道金丹形神俱灭，生命永久终结"},
    "CHAR.xuanyin_laozu": {"name": "玄阴老祖", "death_chapter": 111, "killer": "CHAR.gu_jinglan", "manner": "太虚主峰九天人皇神拳捏爆万年极阴魔龙珠形神俱灭，生命永久终结"},
    "CHAR.taixuzi": {"name": "太虚子", "death_chapter": 113, "killer": "CHAR.gu_jinglan", "manner": "太虚主峰惊龙天剑断诛仙神剑顺势斩首形神俱灭，生命永久终结"},
    "CHAR.wuchenzi": {"name": "无尘子", "death_chapter": 112, "killer": "CHAR.gu_jinglan", "manner": "太虚天门前被惊龙天剑一剑枭首，仙躯法身彻底溃灭，生命永久终结"}
}

# ==============================================================================
# 账本 3: 政体与权力流转账本 (POLITICAL STATE LEDGER)
# ==============================================================================
POLITICAL_STAGES = {
    "VOL1_VOL2_VOL3": {
        "chapters": (1, 72),
        "regime": "腐朽帝制",
        "ruler": "昏君萧乾元在位，国舅赵天龙与兵相严嵩卿专权，地方藩王割据",
        "legitimacy": "主角以顾氏遗孤与天渊传人身份行公理正义，被朝廷视为通缉逆贼"
    },
    "VOL4": {
        "chapters": (73, 96),
        "regime": "奉天靖难 · 监国摄政",
        "ruler": "萧乾元退位除帝，长公主萧明凰任摄政监国，顾惊澜任天下兵马大都督",
        "legitimacy": "手握先帝退位血诏与顾氏平反铁券，奉天靖难清君侧"
    },
    "VOL5": {
        "chapters": (97, 120),
        "regime": "弑仙抗战 · 战时总动员体制",
        "ruler": "大玄全体军民总动员，少帅军与凡人武林全面抗击太虚仙宗降临掠夺",
        "legitimacy": "凡人自强不息，绝地天通，打破仙家奴役万民枷锁"
    },
    "VOL6": {
        "chapters": (121, 144),
        "regime": "开泰新朝 · 君民共治立宪内阁",
        "ruler": "萧明凰正式登基开泰女帝（第131章登基大典），颁布《君民共治宪章》；顾惊澜交出帅印，确立民选内阁理政与军队国家化",
        "legitimacy": "天下为公，选贤与能，司法独立，万世太平"
    }
}

# ==============================================================================
# 账本 4: 资源尺度与物理约束账本 (RESOURCE LEDGER)
# ==============================================================================
RESOURCE_LIMITS = {
    "currency": "开泰通宝 / 现银万两 / 黄金万两（严禁万亿、千亿无意义数字通胀）",
    "grain": "天狼关军粮以五十万至一百万石为尺度，调度受漕运船只与关隘天气约束",
    "army_size": "青州城防军三千至五千；北境幽燕铁骑三十万；蛮族联军三十万至五十万；皇城禁军十万",
    "protagonist_costs": [
        "极道纯阳真气透支导致经脉三日灼痛",
        "山河真图愿力反噬需要闭关调息温养",
        "为保全全城百姓不得不放弃追击敌酋逃遁",
        "为维护裴落霜程序法理不得不延后处决奸佞",
        "为照顾沈倾凰金融大盘不得不放宽查抄时限"
    ]
}
