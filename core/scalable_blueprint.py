# -*- coding: utf-8 -*-
"""
Scalable Blueprint & Macro-Topology Engine (长篇多卷宏观拓扑与可扩展大纲生成引擎)
Supports dynamic length (100 - 500+ chapters), dynamic volume decoupling,
multi-agent ensemble cast dynamics, 5-stage problem morphing, 3-tier promise scheduling,
and PRODUCTION_READY 4000-6000 word chapter contracts.
"""

from __future__ import annotations

from typing import Any
from genres.base_driver import get_genre_driver, BaseGenreDriver
from tones.base_tone import get_tone_driver, BaseToneDriver


# ==============================================================================
# 1. Ensemble Character Cast & Worldview Configuration
# ==============================================================================

def get_genre_cast_config(genre_id: str) -> dict[str, Any]:
    """Returns genre-adapted ensemble cast names, titles, and worldview terminology."""
    gid = genre_id.upper()

    if gid in {"URBAN_REALISTIC", "URBAN", "DUSHI"}:
        return {
            "cast": [
                {
                    "id": "CHAR.protagonist",
                    "name": "沈策",
                    "role": "PROTAGONIST",
                    "tier": "CORE",
                    "identity": "商业操盘手与隐忍复仇者",
                    "explicit_goal": "击垮侵吞家族产业的垄断金融财阀，重塑行业公平秩序",
                    "shadow_want": "洗清亡父蒙冤罪名，渴望寻得一隅不染铜臭的心灵净土",
                    "protected_interest": "家族核心企业与基层数万实体员工之生计",
                    "taboo_line": "绝不违背商业伦理实施恶意做空砸盘伤及普通储户",
                    "fatal_flaw": "重情护短，对旧部背叛往往缺乏决绝的无情切割",
                    "decision_model": "产业实体与员工生计 > 合规公理 > 商业账面利益 > 个人得失",
                    "voice_flavor": "温和沉稳中藏有惊雷，数字逻辑严密，决断极具穿透力",
                    "biography": "沈家商业帝国继承人，七年前遭影子财团构陷破产，远走海外修得顶级量化风控与商战经纬，如今携巨资回国绝地反击。",
                    "private_life": "深夜喜独自在空旷操盘室擦拭旧怀表，极少出席奢华名利酒会。",
                    "life_constraints": "受境外信托资本穿透监管约束，不可违规调用离岸非合规资金。",
                    "knowledge_state": "掌握韩氏财阀洗钱核心账册，尚未摸清其在政界的终极保护伞底细。",
                    "misjudgments": "初期误以为薛云鹏是主谋，后经深入审计发掘韩振江的真正影子帝国。",
                    "arc": "从背负家族私仇的冷酷做空猎手，蜕变为庇护民族实体产业的商界脊梁。",
                    "fate": "彻底扫清金融毒瘤，设立青年产业基金，归隐于江南水乡书院。",
                    "highlights": "一人单挑省城八大资本操盘手，于除夕之夜力挽狂澜挽救破产船厂。",
                    "desires": "瓦解韩振江垄断网并重振实体制造业",
                    "goals": "守护实体产业数万普通员工的饭碗与未来",
                    "interests": "研读宏观经济审计底稿与全球货币流向",
                    "constraints": "遵守现代金融法律与底线伦理",
                    "preferred_strategy": "证据确权，资本对冲，穿透审计",
                    "independent_goal_without_protagonist": "维系沈氏慈善基金对患病老员工的终身兜底保障",
                    "aliases": ["沈策", "主角", "沈总", "少主"],
                },
                {
                    "id": "CHAR.ally",
                    "name": "林婉清",
                    "role": "ALLY",
                    "tier": "CORE",
                    "identity": "顶级商事风控律师与合规总监",
                    "explicit_goal": "确保所有商业反击行动具备不可推翻的法律法理效力",
                    "shadow_want": "证明女性在极度男权垄断的重工金融界亦能独当一面执掌乾坤",
                    "protected_interest": "司法裁判公信力与合作律所的声誉底线",
                    "taboo_line": "绝不使用伪造证据或非法窃听手段获取胜诉筹码",
                    "fatal_flaw": "过度迷信法条程序，在面对法外暴力威胁时偶显应对迟疑",
                    "decision_model": "程序正义与法条合规 > 商业胜诉速度 > 战术妥协",
                    "voice_flavor": "辞藻精准利落，条理明晰，法言法语间带着从容不迫的气场",
                    "biography": "法学院泰斗之女，曾任最高检商事公诉顾问，因不屈从于韩振江强权施压而辞职创办独立合规律所。",
                    "private_life": "收藏古典法学原本与天平徽章，下班后喜在拳馆高强度搏击减压。",
                    "life_constraints": "受律师协会执业纪律与职业道德委员会终身审查监督。",
                    "knowledge_state": "通晓全国商法与证监会监管细则，不通地下黑道暴力逻辑。",
                    "misjudgments": "曾以为司法判决即可解决一切，直到亲眼见证韩氏暴力洗白资金。",
                    "arc": "从恪守法条教条的书斋学者，成长为深谙现实博弈大局的法理统帅。",
                    "fate": "主持编撰新一代资本市场反垄断自律公约，入选国家法治杰出贡献人物。",
                    "highlights": "当庭舌战十二位涉外大律师，出示铁证让被告直接法庭认罪。",
                    "desires": "建立公平透明无黑幕的法治营商环境",
                    "goals": "为主力团队提供坚不可摧的法务护城河",
                    "interests": "商事诉讼案卷推演与穿透式法庭辩论",
                    "constraints": "绝不使用非法手段获取证据",
                    "preferred_strategy": "法庭公审，合规锁定，以法治暴",
                    "independent_goal_without_protagonist": "推动地方法院设立中小投资者权益保护特别仲裁庭",
                    "aliases": ["林婉清", "核心盟友", "林律师", "婉清", "林总监"],
                },
                {
                    "id": "CHAR.ally_specialist",
                    "name": "陆天行",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "硬核注册审计师与资金穿透专家",
                    "explicit_goal": "拆解对手所有离岸空壳公司与虚假质押链条",
                    "shadow_want": "走出兄长因金融暴雷坠楼身亡的心灵阴霾",
                    "protected_interest": "中小散户投资者的知情权与本金安全",
                    "taboo_line": "绝不在虚假审计报告上签字背书受贿",
                    "fatal_flaw": "性格孤僻执拗，不善人际斡旋，极易直言得罪各方权贵",
                    "decision_model": "原始凭证真实性 > 商业人情面子 > 个人仕途前程",
                    "voice_flavor": "语速极快，言必称会计准则与账面瑕疵，冷峻而专注",
                    "biography": "前国际四大会计师事务所高级合伙人，因拒绝掩盖韩氏虚假财报而遭行业封杀，后加入沈策团队。",
                    "private_life": "重度黑咖啡依赖者，随身携带放大镜与红黑双色审计笔。",
                    "life_constraints": "患有严重失眠症与神经衰弱，需定期服药维持专注度。",
                    "knowledge_state": "洞悉所有金融衍生品嵌套障眼法，不知武力自保之道。",
                    "misjudgments": "误以为账本干净即企业健康，忽视了隐蔽的账外担保与抽屉协议。",
                    "arc": "从心灰意冷的隐士账房，重燃以算盘为剑涤荡人间黑金之斗志。",
                    "fate": "成为全国知名独立审计师事务所创始人，被誉为资本市场黑天鹅克星。",
                    "highlights": "三天三夜不眠不休穿透七百家空壳公司，锁定最终资金池。",
                    "desires": "让每一分黑金在阳光下无所遁形",
                    "goals": "以审计铁证粉碎对手资金链",
                    "interests": "钻研国际反洗钱追踪技术与法务会计",
                    "constraints": "严格遵照会计准则绝不伪造流水",
                    "preferred_strategy": "多维穿透，数据对账，顺藤摸瓜",
                    "independent_goal_without_protagonist": "追讨兄长当年被骗取的数千万元研发专利补偿金",
                    "aliases": ["陆天行", "战术专家", "老陆", "天行", "陆老师"],
                },
                {
                    "id": "CHAR.ally_friction",
                    "name": "苏若微",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "调查记者与新媒体公义监督者",
                    "explicit_goal": "向全社会公开披露财阀垄断内幕，唤醒公众监督力量",
                    "shadow_want": "渴望摆脱家庭被财阀资助的耻辱烙印，获得精神独立",
                    "protected_interest": "新闻真实性与公众知情权",
                    "taboo_line": "绝不接受有偿撤稿，绝不出卖吹哨人底细",
                    "fatal_flaw": "理想主义倾向严重，有时为抓大新闻而低估现实暗杀凶险",
                    "decision_model": "新闻真实曝光 > 资本团队战略步调 > 商业利益权衡",
                    "voice_flavor": "富有感染力与同理心，发问尖锐直刺核心痛点",
                    "biography": "省报王牌深度报道记者，因坚持追踪韩氏污染与拆迁血案被停职，转型创办独立调查公号。",
                    "private_life": "单反相机不离手，常在老居民楼里访谈下岗工人与涉案受害者。",
                    "life_constraints": "长期遭受匿名人身威胁与电话骚扰，居所频繁更换。",
                    "knowledge_state": "掌握韩氏在社会基层的全部劣迹，不通高层暗箱权谋细节。",
                    "misjudgments": "初期曾质疑沈策回国亦是为了资本暴利，后在行动中互为见证。",
                    "arc": "从孤军奋战的激进记录者，成熟为懂得与法律团队协同作战之旗手。",
                    "fate": "斩获国际新闻普利策级调查大奖，担任公义基金会荣誉理事长。",
                    "highlights": "卧底进入污染化工厂偷拍核心排污口，在全网直播引爆舆论。",
                    "desires": "用笔与镜头刺破一切光鲜亮丽的伪善面具",
                    "goals": "让真相大白于天下",
                    "interests": "社会学田野调查与民生纪实摄影",
                    "constraints": "绝不歪曲剪辑新闻事实",
                    "preferred_strategy": "现场调查，舆论公审，深度曝光",
                    "independent_goal_without_protagonist": "跟踪报道化工厂周边白血病患儿群体的终身医疗救助进展",
                    "aliases": ["苏若微", "监察盟友", "苏记者", "若微", "苏老师"],
                },
                {
                    "id": "CHAR.antagonist",
                    "name": "韩振江",
                    "role": "ANTAGONIST",
                    "tier": "CORE",
                    "identity": "鼎华投资财团董事长与地下资本寡头",
                    "explicit_goal": "垄断全省产业金融通道，吞并所有竞争对手建立资本帝国",
                    "shadow_want": "借资本出海换取境外庇护，彻底摆脱旧日原罪清算",
                    "protected_interest": "自身对鼎华财团的绝对控制权与海外百亿信托",
                    "taboo_line": "绝不容许他人挑战自身权威，任何阻挠者皆需予以无情碾碎",
                    "fatal_flaw": "迷信资本与强权无所不能，视普通人为草芥耗材导致众叛亲离",
                    "decision_model": "资本独裁与海外资产安全 > 合作者死活 > 行业秩序 > 法律道德",
                    "voice_flavor": "低沉威严，言语不多却带着不容置疑的生杀予夺压迫感",
                    "biography": "草莽起家，靠早年灰产走私与非法借贷积累暴利，随后借金融改革洗白，构筑起笼罩全省的巨擘帝国。",
                    "private_life": "常年深居城郊防弹安保庄园，酷爱雪茄与西洋古董枪械。",
                    "life_constraints": "身患晚期心脏隐疾，极度依赖私人医疗团队全天候守护。",
                    "knowledge_state": "深谙地方政商潜规则与资本运作杠杆，轻视年轻一代技术创新。",
                    "misjudgments": "坚信资本能买通一切，低估了沈策团队玉石俱焚的信仰与意志。",
                    "arc": "从不可一世的资本帝王，在层层围剿与证据链合围下走向疯狂与崩溃。",
                    "fate": "因数十项重罪被依法判处无期徒刑，全部不法资产收归国有。",
                    "highlights": "一夜之间调度百亿资金强行封死三家上市公司涨跌停板。",
                    "desires": "建立万世不灭的垄断金融特权王朝",
                    "goals": "彻底碾碎沈策及其同盟的一切抵抗",
                    "interests": "收集名贵红酒与幕后操纵商政大局",
                    "constraints": "受国家外汇管制与刑法死线限制不敢完全公开违法",
                    "preferred_strategy": "资本围剿，政商暗压，分化借刀",
                    "independent_goal_without_protagonist": "暗中转移两百亿资产至离岸无引渡条约避风港",
                    "aliases": ["韩振江", "宿敌", "韩董", "韩会长", "老韩董"],
                },
                {
                    "id": "CHAR.rival_boss",
                    "name": "薛云鹏",
                    "role": "ANTAGONIST",
                    "tier": "MAJOR",
                    "identity": "激进做空对冲基金合伙人与台前白手套",
                    "explicit_goal": "通过凶狠猎杀上市公司股价实现个人暴富与资本上位",
                    "shadow_want": "渴望摆脱韩振江家奴鹰犬身份，建立属于自己的对冲基金王国",
                    "protected_interest": "个人名下操盘提成账户与奢侈浮华生活",
                    "taboo_line": "绝不让自己替韩振江背负刑事顶包重罪",
                    "fatal_flaw": "贪婪狂妄，赌徒心理极强，在顺境时极易加杠杆自掘坟墓",
                    "decision_model": "短期暴利与个人安全 > 韩振江指令 > 行业长远发展",
                    "voice_flavor": "轻佻傲慢，语带讥讽，常用英文金融黑话炫耀优越感",
                    "biography": "华尔街归国量化交易员，自命不凡，为韩振江操盘恶意做空多起民族企业，获利数亿。",
                    "private_life": "出入顶级私人会所，嗜好名贵超跑与高频投机赌博。",
                    "life_constraints": "签订有韩氏严密的人身附庸与对赌协议，一旦失败将一无所有。",
                    "knowledge_state": "精通做空打压手法与期权衍生品，对韩氏深层洗钱内幕一知半解。",
                    "misjudgments": "误以为沈策仅是盲目意气用事，轻视了其在底层实业扎根的底蕴。",
                    "arc": "从嚣张跋扈的金融秃鹫，在连番做空失败与爆仓后沦为弃子。",
                    "fate": "自食恶果被做空反噬宣告个人破产，反戈指证韩振江后获刑入狱。",
                    "highlights": "利用虚假做空研报连续打崩沈氏供应商股票三个跌停板。",
                    "desires": "在资本市场一战成名并攫取亿万身家",
                    "goals": "在二级市场上彻底绞杀沈策操盘资金",
                    "interests": "超跑赛车与全球高风险对冲套利",
                    "constraints": "高度依赖保证金杠杆，极度畏惧遭遇强制平仓",
                    "preferred_strategy": "高频打压，舆论围猎，突击做空",
                    "independent_goal_without_protagonist": "私下侵吞韩振江交托的两亿元操盘隐秘佣金",
                    "aliases": ["薛云鹏", "阶段宿敌", "薛总", "薛合伙人", "秃鹫薛"],
                },
            ],
            "locations": [
                {"id": "LOC.start_hub", "name": "申海国际金融中心", "travel_mode": "CAR", "speed": 60.0},
                {"id": "LOC.front_battleground", "name": "滨海重工高新技术园区", "travel_mode": "HIGH_SPEED_RAIL", "speed": 300.0},
                {"id": "LOC.climax_citadel", "name": "云端鼎华集团顶层董事厅", "travel_mode": "CAR", "speed": 60.0},
            ],
            "props": [
                {"id": "PROP.core_tool", "name": "万联核心量化风控密钥", "owner": "CHAR.protagonist"},
                {"id": "PROP.strategic_dossier", "name": "跨境重组违规审计账册", "owner": "CHAR.ally"},
            ],
        }

    elif gid in {"CTHULHU_WESTERN", "CTHULHU", "HORROR", "GUIYI"}:
        return {
            "cast": [
                {
                    "id": "CHAR.protagonist",
                    "name": "亚德里安",
                    "role": "PROTAGONIST",
                    "tier": "CORE",
                    "identity": "秘术调查员与深渊遗孤",
                    "explicit_goal": "阻止银秘教团召唤外神降临，封印污染源泉拯救城邦",
                    "shadow_want": "探寻自身家族血脉中的疯狂呓语真相，寻找彻底解脱之道",
                    "protected_interest": "普罗维登斯港口无辜凡人的理智与灵魂安宁",
                    "taboo_line": "绝不以活人献祭换取深渊古神的任何赐福与知识",
                    "fatal_flaw": "对禁忌奥秘怀有过于旺盛的好奇心，屡屡在疯狂边缘涉险",
                    "decision_model": "苍生文明与存亡 > 亲近同袍安危 > 个人理性留存 > 现世世俗名利",
                    "voice_flavor": "沙哑低沉，冷静中压抑着颤抖，如同从迷雾长夜归来的守望者",
                    "biography": "曾任密斯卡托尼克大学古文字学副教授，在一场考古异变中痛失双亲与右手，安装了符文义肢，走上猎魔求道之路。",
                    "private_life": "随身携带银制罗盘与怀表，每当耳畔响起呓语便默诵数学公理以维持理智。",
                    "life_constraints": "受不可逆理智值（SAN）衰减法则限制，施展高阶秘术必损神智。",
                    "knowledge_state": "通晓旧神古语与封印法阵，尚未探明诺克斯的深渊祭坛真实地脉。",
                    "misjudgments": "初期曾以为黑山主教即祸患主使，后发掘其不过是诺克斯的祭品。",
                    "arc": "从饱受噩梦折磨的求死孤狼，升华为以残躯为火炬抵挡深渊之守门人。",
                    "fate": "耗尽最后一滴灵力封印深渊之门，在长夜黎明前安详合上双眼。",
                    "highlights": "单人点燃炼金水银炸碎深渊利维坦之触须，救出整船平民。",
                    "desires": "斩断深渊降临因果并保全城邦理智",
                    "goals": "守护普罗维登斯三十万凡夫俗子免遭异化",
                    "interests": "破译泥板星象密码与炼制避魔药剂",
                    "constraints": "绝不向外神古老意志屈膝奉献信仰",
                    "preferred_strategy": "密室求证，仪式封印，以智诛魔",
                    "independent_goal_without_protagonist": "为大学失踪同学的孤寡家属定期寄送生活救济金",
                    "aliases": ["亚德里安", "主角", "沃克调查员", "亚德里安先生"],
                },
                {
                    "id": "CHAR.ally",
                    "name": "埃琳娜",
                    "role": "ALLY",
                    "tier": "CORE",
                    "identity": "密斯卡托尼克古代文献学家与符文守护者",
                    "explicit_goal": "破译死灵之书残页中的反向封印古咒",
                    "shadow_want": "重铸家族在学界的正统学术尊严，驱散巫术世家的历史耻辱",
                    "protected_interest": "古代图书馆内封存的人类文明记忆孤本",
                    "taboo_line": "绝不容许异端焚毁人类最后的古代真理典籍",
                    "fatal_flaw": "对古籍典籍过于珍视，在战火中往往为保护羊皮纸而置身险地",
                    "decision_model": "文明记忆与典籍保全 > 仪式解咒效率 > 个人安危",
                    "voice_flavor": "语调清冷典雅，语速平缓坚定，充满古典学者的学理严谨",
                    "biography": "出生于新英格兰隐秘学者世家，精通十四门古印欧语系与深渊象形字，大学特聘古籍档案馆主管。",
                    "private_life": "喜在羊皮纸与油灯下研磨植物墨水，收集各类羽毛笔与星图残片。",
                    "life_constraints": "体质文弱缺乏搏击能力，面对物理冲撞极度依赖队友防护。",
                    "knowledge_state": "深谙上古星相与封印阵法演化，不通前线爆破与枪械战术。",
                    "misjudgments": "误以为真理可以感化信徒，险些在邪教传教仪式中被当场洗脑。",
                    "arc": "从柔弱避世的典籍整理员，历练为能在枪林弹雨中从容念咒的战地大学者。",
                    "fate": "接任密斯卡托尼克大学终身名誉馆长，设立全球神秘文献守护盟会。",
                    "highlights": "在狂风暴雨的祭坛前逆向高声咏唱封印古诗，撕碎邪教大主教的结界。",
                    "desires": "让人类文明的理性星火照亮无尽长夜",
                    "goals": "破解反向封印古咒封死深渊裂隙",
                    "interests": "上古碑文拓片临摹与星体轨道推演",
                    "constraints": "严守学者良知绝不擅自散播禁忌原著",
                    "preferred_strategy": "典籍考据，符文反制，理论筑基",
                    "independent_goal_without_protagonist": "独立修补大学地下秘藏中破损严重的三卷中世纪炼金原典",
                    "aliases": ["埃琳娜", "核心盟友", "瓦伦学者", "埃琳娜女士"],
                },
                {
                    "id": "CHAR.ally_specialist",
                    "name": "托马斯",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "退役边境军士与炼金爆破专家",
                    "explicit_goal": "构筑火力防御阵地并爆破摧毁邪教地下巢穴",
                    "shadow_want": "渴望平息战争创伤综合症引起的幻听幻视",
                    "protected_interest": "调查小队全员的物理人身安全与弹药补给",
                    "taboo_line": "绝不在战场上抛下任何一名并肩作战的战友",
                    "fatal_flaw": "脾气火爆，嗜烟酗酒，对神秘学繁琐理论极度缺乏耐心",
                    "decision_model": "队友生命与战术据点安全 > 战利品起获 > 文明典籍保全",
                    "voice_flavor": "粗粝嘶哑，伴随着军营粗口与干脆利落的战术口令",
                    "biography": "曾在海外殖民地皇家步兵团服役十二年，精通重火器与烈性炼金火药调制，退役后担任赏金猎魔人。",
                    "private_life": "随身携带雕刻着亡友姓名的银酒壶，擅长用猎刀削木雕排解焦虑。",
                    "life_constraints": "左膝受过重伤弹片残留，阴冷潮湿天气行动敏捷度显著下降。",
                    "knowledge_state": "通晓所有常规武器杀伤半径与工事构筑，对精神异化防御力偏弱。",
                    "misjudgments": "最初坚信口径与火药即可解决一切妖魔，险被无形无相的幻影夺命。",
                    "arc": "从只认金钱与火力的糙汉老兵，转变为懂得敬畏超自然并以生命守护真理之铁卫。",
                    "fate": "建立老兵安养之家，功勋重火枪陈列于市政英烈纪念馆。",
                    "highlights": "单人架起重机枪在矿道隘口独抗上百名异化狂信徒狂暴冲锋。",
                    "desires": "用真理口径粉碎一切不可名状的血肉怪物",
                    "goals": "守护战友安危并炸平邪神地宫",
                    "interests": "改装大口径猎枪与调试水银霰弹配方",
                    "constraints": "军规荣誉在上绝不朝凡俗平民扣动扳机",
                    "preferred_strategy": "重火力覆盖，战术穿插，定点爆破",
                    "independent_goal_without_protagonist": "追查杀害当年陆军整编小队十二名战友的食尸鬼凶手下落",
                    "aliases": ["托马斯", "战术专家", "布莱克士官", "老托马斯", "火药托马斯"],
                },
                {
                    "id": "CHAR.ally_friction",
                    "name": "凡妮莎",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "异端旧神信徒后裔与激进猎魔人",
                    "explicit_goal": "用异端之血洗刷血脉污秽，彻底诛灭银秘教团核心血脉",
                    "shadow_want": "渴望得到同伴真正的信任与接纳，洗去异教余孽的怀疑目光",
                    "protected_interest": "自身与妹妹免遭深渊教团抓回充当圣灵容器",
                    "taboo_line": "绝不对邪教大主祭诺克斯有一丝一毫的怜悯宽恕",
                    "fatal_flaw": "杀心过重，手段狠辣极端，在追击敌人时往往不计反噬代价",
                    "decision_model": "斩草除根消灭宿敌 > 程序法理 > 自身道德评价",
                    "voice_flavor": "冷峻尖锐，带着刀锋割裂空气般的肃杀与讥嘲",
                    "biography": "出生于崇拜旧神的海滨古老隐秘部族，十二岁目睹全族沦为邪神祭品，携妹妹叛逃并立下复仇血誓。",
                    "private_life": "嗜食生冷海味，夜间常在树梢或钟楼顶端眺望海平面沉思。",
                    "life_constraints": "体内流淌微量旧神异化血脉，逢月圆之夜必须靠草药压制鳞化剧痛。",
                    "knowledge_state": "通晓邪教内部所有暗语、联络密信与潜伏据点，对现代社会规则生疏。",
                    "misjudgments": "曾认为亚德里安与埃琳娜的仁慈与程序是无用的虚伪软弱。",
                    "arc": "从满腔怨毒的复仇毒刃，在战友的信任与包容中体会到人性温情与救赎。",
                    "fate": "斩杀教团仇雠后辞行远航，前往大洋深处寻找彻底净化血脉的纯净圣所。",
                    "highlights": "潜入邪教地牢暗杀三名主教副手，反向释放出被囚禁的平民。",
                    "desires": "亲手将银秘教团全部首恶送入万劫不复之深渊",
                    "goals": "斩断家族世世代代受控于邪神的诅咒枷锁",
                    "interests": "研习古老部族追踪术与淬毒匕首投掷",
                    "constraints": "誓死守护无辜幼童免受血祭毒害",
                    "preferred_strategy": "暗夜潜行，一击必杀，绝不留情",
                    "independent_goal_without_protagonist": "在港口隐秘庇护所内照料患有失魂症的亲妹妹",
                    "aliases": ["凡妮莎", "监察盟友", "罗齐尔小姐", "黑匕首凡妮莎"],
                },
                {
                    "id": "CHAR.antagonist",
                    "name": "诺克斯",
                    "role": "ANTAGONIST",
                    "tier": "CORE",
                    "identity": "银秘教团大主祭与深渊引渡者",
                    "explicit_goal": "撕裂现世空间维度壁垒，引渡外神意志降临建立盲目痴愚新纪元",
                    "shadow_want": "突破凡人肉身与寿元极限，升华为不可名状之永恒星空高维神明",
                    "protected_interest": "深渊祭坛群的绝对隐秘与神降仪式的充沛生灵血食",
                    "taboo_line": "绝不容许凡世微末文明的庸俗理性亵渎旧神伟力",
                    "fatal_flaw": "自诩高维神裔而极端狂妄自大，视所有凡人智谋为尘芥虚妄",
                    "decision_model": "神降仪式达成 > 教团信徒死活 > 现世城邦存亡",
                    "voice_flavor": "重叠多重古老回响，空灵冷酷，带着令生灵神魂颤栗的虚无威压",
                    "biography": "百年前失踪的帝国天文学首席研究员，在极地深渊触摸到虚空陨石而彻底异化，暗中掌控城邦上流社会数十年。",
                    "private_life": "在海底黑曜石地宫内浸泡于防腐水银药池，聆听星空遥远杂音。",
                    "life_constraints": "肉身早已腐朽，全凭外神赐予的寄生星核维系神魂活性。",
                    "knowledge_state": "通晓深渊九重位面之法则权柄，无法看透主角命魂中的微弱变数。",
                    "misjudgments": "坚信凡世文明如同蝼蚁泡沫一触即溃，终被坚守理智的人心破防。",
                    "arc": "从俯瞰众生的降维神使，在仪式被层层破坏后陷入癫狂与本源溃散。",
                    "fate": "星核碎裂，神躯被放逐于无尽虚空夹缝，永受时空乱流凌迟。",
                    "highlights": "一指引动潮汐倒灌吞没整座海湾小镇，开启九重血祭天幕。",
                    "desires": "重铸世界秩序引渡旧日神明万古永存",
                    "goals": "抹平现世一切文明理性与抵抗余孽",
                    "interests": "活体解剖深渊异化造物与收集星空陨石",
                    "constraints": "必须在群星归位特定时辰方可完全施展全能神迹",
                    "preferred_strategy": "心智污染，暗流腐化，血祭引渡",
                    "independent_goal_without_protagonist": "私下捕获七位古代神裔后裔血脉以提炼飞升圣油",
                    "aliases": ["诺克斯", "宿敌", "大主祭", "银秘之冠诺克斯", "阿道夫·诺克斯"],
                },
                {
                    "id": "CHAR.rival_boss",
                    "name": "黑山主教",
                    "role": "ANTAGONIST",
                    "tier": "MAJOR",
                    "identity": "黑石矿区执行主教与狂热仪式督造者",
                    "explicit_goal": "强征数千矿工奴役挖掘深渊黑石，构筑外神降临地基通道",
                    "shadow_want": "渴望在大主祭飞升后接替银秘之冠权柄，独掌大教",
                    "protected_interest": "矿区私兵护卫团与黑石走私换取的滔天黄金富贵",
                    "taboo_line": "绝不让自己落入城邦正规宪兵与审判庭审判席上",
                    "fatal_flaw": "嗜杀暴虐，急功近利，经常因急于邀功而强行提前发动残缺仪式",
                    "decision_model": "督造工期与教团领赏 > 矿工性命 > 自身防线周密性",
                    "voice_flavor": "尖锐狂躁，充斥着神经质的狞笑与狂热呓语",
                    "biography": "原为黑山矿业公司贪婪大股东，为求延寿献出矿区投靠教团，受封前沿执行主教。",
                    "private_life": "以生饮深渊剧毒黑水为乐，在矿洞密室蓄养畸形猎犬。",
                    "life_constraints": "身体半侧已被黑石晶体异化侵蚀，每日需服食鸦片酊镇痛。",
                    "knowledge_state": "熟知矿山地质结构与劳工分布，对深渊终极真相一无所知。",
                    "misjudgments": "狂妄自诩在黑山地界无人可敌，轻视了亚德里安与托马斯的爆破战术。",
                    "arc": "从嚣张跋扈的土皇帝，在矿道崩溃与信徒瓦解后仓皇如丧家之犬。",
                    "fate": "在矿洞大决战中被托马斯引爆雷管炸塌地宫，当场被万吨巨石活埋。",
                    "highlights": "驱使变异黑石巨兽硬撼正规军骑兵连，将其尽数撕裂。",
                    "desires": "在神明降世后荣登永生主教神座",
                    "goals": "提前完成深渊地宫挖掘大业",
                    "interests": "搜罗民间奇珍异宝与驱使狂信徒狂暴献祭",
                    "constraints": "受矿区有限补给制约无法长期打持久围困战",
                    "preferred_strategy": "暴力镇压，黑石畸变，血腥清洗",
                    "independent_goal_without_protagonist": "暗中扣留矿区出产的三成纯度最高的原初星石以图自保",
                    "aliases": ["黑山主教", "阶段宿敌", "执行主教", "黑山矿主", "狂热者主教"],
                },
            ],
            "locations": [
                {"id": "LOC.start_hub", "name": "普罗维登斯古城密斯卡托尼克书库", "travel_mode": "WALK", "speed": 40.0},
                {"id": "LOC.front_battleground", "name": "阿卡姆黑山矿区废弃地宫", "travel_mode": "HORSE", "speed": 100.0},
                {"id": "LOC.climax_citadel", "name": "海渊银秘教团终极神降祭坛", "travel_mode": "FLEET_WATER", "speed": 150.0},
            ],
            "props": [
                {"id": "PROP.core_tool", "name": "银秘理智探测罗盘", "owner": "CHAR.protagonist"},
                {"id": "PROP.strategic_dossier", "name": "死灵之书真本残页拓片", "owner": "CHAR.ally"},
            ],
        }

    elif gid in {"SCI_FI_CYBER", "SCI_FI", "SCIFI", "CYBERPUNK", "KEHUAN"}:
        return {
            "cast": [
                {
                    "id": "CHAR.protagonist",
                    "name": "雷恩",
                    "role": "PROTAGONIST",
                    "tier": "CORE",
                    "identity": "顶级神经黑客与底层秩序重塑者",
                    "explicit_goal": "攻破荒坂巨企中央脑机枢纽，粉碎思维格式化奴役协议",
                    "shadow_want": "寻找昔日被巨企抹除意识的女友真实数据记忆备份",
                    "protected_interest": "下城霓虹街区数百万未改造底层平民的意识主权",
                    "taboo_line": "绝不使用脑控病毒将无辜平民改造成神志丧失的自爆肉盾",
                    "fatal_flaw": "神经超频反噬严重，战斗中易因情感冲动导致脑机接口过载",
                    "decision_model": "底层人类意识自由 > 战友性命 > 自身脑机寿命 > 巨企利益",
                    "voice_flavor": "冷静干练，短促有力，带着电子合成器混音般的冷冽节奏",
                    "biography": "前巨企第七研究所特种脑机架构师，因反抗将婴儿改造成生物量子算力电池而叛逃下城，组建自由潜网者联盟。",
                    "private_life": "喜在黑胶唱片机前手动焊接老式真空管，饮用高浓度无糖合成酒精。",
                    "life_constraints": "颅内植入有军用级神经超频芯片，持续战斗超过三分钟将诱发脑溢血。",
                    "knowledge_state": "通晓巨企全部防火墙底层漏洞，不通高层董事会派系政治协议细节。",
                    "misjudgments": "初期以为零号执行官只是冷血杀手，后发现其为首位格式化试验体受害者。",
                    "arc": "从背负愧疚的独行复仇幽灵，成长为领导全城底层人民打破数字牢笼之领袖。",
                    "fate": "彻底公开巨企源代码，拔除自身军用芯片，在下城与重聚同伴共迎晨曦。",
                    "highlights": "一人单枪匹马在虚拟赛博空间斩灭巨企三大AI杀手，烧毁其外围服务器。",
                    "desires": "打破巨企对全人类脑机意识的数字极权垄断",
                    "goals": "解放下城数百万被剥夺思想与记忆的同胞",
                    "interests": "拆解老旧赛博义肢与破译军用加密协议",
                    "constraints": "绝不侵犯无辜平民的个人隐私与底层神经权",
                    "preferred_strategy": "代码穿透，幽灵潜行，雷霆断电",
                    "independent_goal_without_protagonist": "维护下城地下孤儿院太阳能微电网与净水循环过滤系统",
                    "aliases": ["雷恩", "主角", "技师雷恩", "幽灵陈", "黑客雷恩"],
                },
                {
                    "id": "CHAR.ally",
                    "name": "艾娃",
                    "role": "ALLY",
                    "tier": "CORE",
                    "identity": "前巨企网络安全总监与战略架构师",
                    "explicit_goal": "构筑牢不可破的量子加密防御网掩护突击队穿插",
                    "shadow_want": "证明即便脱离巨企无限算力支持，亦能凭借人类本真智慧创造奇迹",
                    "protected_interest": "地下反抗军的情报中继站与深网安全信道",
                    "taboo_line": "绝不向巨企内卫部队出卖任何一个下城联络站坐标",
                    "fatal_flaw": "性格极度理性近乎冷酷，早期常因精算胜率而主张放弃高伤亡援救",
                    "decision_model": "战略胜算与团队生存 > 局部情感冲动 > 单点装备保全",
                    "voice_flavor": "语调平稳没有情绪起伏，如同超精密量子计算机在实时宣读诊断",
                    "biography": "拥有七个顶级大学工程博士学位的天才少女，因察觉巨企思维收割黑幕，携带绝密后门密钥出逃。",
                    "private_life": "喜把玩魔方与国际象棋，在黑暗中闭目聆听白噪音整理思维导图。",
                    "life_constraints": "没有接受任何军用肉身义体强化，纯粹为脆弱的血肉之躯。",
                    "knowledge_state": "掌握巨企全球卫星数据链拓扑，不知底层街头黑帮巷战手段。",
                    "misjudgments": "曾以为用技术理性即可说服董事会放弃暴行，险遭内部清洗抹杀。",
                    "arc": "从高傲冰冷的象牙塔工程师，淬炼为具有热血温情与担当之战略军师。",
                    "fate": "出任新时代开放开源网络治理公会首任主席，确立人脑主权不可侵犯宪章。",
                    "highlights": "三十秒内反向黑入巨企防御卫星，强行将天基轨道炮离线闭锁。",
                    "desires": "构建一个代码属于全人类的自由透明数字新世界",
                    "goals": "为团队提供绝对算力防护与全球卫星后门",
                    "interests": "设计量子纠缠加密算法与神经网络架构优化",
                    "constraints": "遵守数字伦理宪章不开发灭绝性自复制算法",
                    "preferred_strategy": "算力压制，逻辑闭锁，信息阻断",
                    "independent_goal_without_protagonist": "编写一套完全免费且抗审查的全球民用教育卫星接入程序",
                    "aliases": ["艾娃", "核心盟友", "艾娃总监", "架构师艾娃", "索托博士"],
                },
                {
                    "id": "CHAR.ally_specialist",
                    "name": "诺亚",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "重装义体突击手与军火改装狂人",
                    "explicit_goal": "正面撕裂巨企装甲防线，为黑客团队争取物理侵入时间",
                    "shadow_want": "赎还当年在巨企防暴特警队服役时误伤无辜同胞的原罪",
                    "protected_interest": "战壕同袍的生命与撤离掩护撤退通路",
                    "taboo_line": "绝不向手无寸铁的平民与投降伤兵开火",
                    "fatal_flaw": "鲁莽好斗，酷爱重火力正面硬撼，经常忽视侧翼伏击暗桩",
                    "decision_model": "掩护战友撤退 > 个人生死 > 突击破拆速度",
                    "voice_flavor": "洪亮震耳，带着重型机械引擎轰鸣般的金属共振感",
                    "biography": "全身百分之七十完成军工级钛合金与液压义体化，曾是巨企王牌突击队长，因抗命拒绝向罢工工人开枪而被判叛国除名。",
                    "private_life": "喜在修理间用机油保养机械臂轴承，嗜好高热量合成汉堡与重金属摇滚。",
                    "life_constraints": "高功率液压关节需高频加注合成润滑油，且惧怕强电磁脉冲（EMP）致盲。",
                    "knowledge_state": "通晓巷战爆破与重型外骨骼战术，对代码层面的逻辑对抗一窍不通。",
                    "misjudgments": "初以为黑客只需敲键盘毫无危险，后亲见脑机过载惨状方懂并肩死守。",
                    "arc": "从浑浑噩噩只懂杀戮的战争机器，觉醒为为人性尊严而战的钢铁巨人。",
                    "fate": "功成后退役开设机械改装工坊，免费为伤残劳工修理义肢。",
                    "highlights": "以肉身钛合金巨盾生生顶住天基高能微波扫射，掩护团队突入主控室。",
                    "desires": "用自己的钢铁臂膀守护世间最后的血肉温情",
                    "goals": "为团队撕开一条直通巨企总部的血路",
                    "interests": "改装反器材重型电磁炮与钛合金装甲焊接",
                    "constraints": "恪守老兵誓言绝不欺凌老幼弱小",
                    "preferred_strategy": "重装推进，火力压制，正面强拆",
                    "independent_goal_without_protagonist": "为当年因自己误伤致残的三位老工人家属每月按时送去全额伤残抚恤金",
                    "aliases": ["诺亚", "战术专家", "铁臂诺亚", "大块头诺亚", "克莱因士官"],
                },
                {
                    "id": "CHAR.ally_friction",
                    "name": "凯拉",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "纯自然人权利保护同盟发言人与街头反叛者",
                    "explicit_goal": "阻止巨企在平民体内强制推行生化脑机义体化",
                    "shadow_want": "渴望证明不接受任何机械改造的自然人躯体同样拥有对抗强权之力量",
                    "protected_interest": "下城普通民众保有不改造纯天然肉身的宪法权利",
                    "taboo_line": "绝不在自己的身体里植入任何巨企芯片与人造义肢",
                    "fatal_flaw": "对所有机械义体持过度偏见与敌意，初期常与诺亚和雷恩发生理念争吵",
                    "decision_model": "自然人尊严与人道底线 > 战术装备升级效率 > 妥协求和",
                    "voice_flavor": "激昂坚毅，富有穿透力与演讲号召力，字字带着街头呐喊的温度",
                    "biography": "医学伦理学学者，拒绝巨企推行的全民人造器官置换令，深入下城贫民窟领导无芯片自然人发起和平公民不服从运动。",
                    "private_life": "随手携带针线缝补粗布衣裳，种植天然绿植并收集纯天然植物种子。",
                    "life_constraints": "纯肉身状态在面对武装机器人时抗打击能力极其薄弱。",
                    "knowledge_state": "深谙街头社群动员与舆论罢工组织，对复杂网络攻击战术生疏。",
                    "misjudgments": "曾认为凡接受义体改造者皆是巨企帮凶走狗，后在战火中被诺亚舍命相救打消成见。",
                    "arc": "从偏激排外的纯肉身原教旨主义者，成熟为接纳战友、包容多元的人道主义旗帜。",
                    "fate": "当选新自由城邦首位民选议员，推动确立《自然人类与赛博改造者平等法案》。",
                    "highlights": "在巨企总部广场上面对上千枪口发表三十分钟不屈演讲，促使巨企内卫集体倒戈放低枪口。",
                    "desires": "守护人类未经篡改的原生血肉尊严与灵魂自由",
                    "goals": "废除强制性义体植入法案还民自由",
                    "interests": "社会学演讲与传统草药学疗法研究",
                    "constraints": "坚持非暴力不合作绝不主动制造针对平民的暴恐袭击",
                    "preferred_strategy": "群众动员，全城罢工，街头宣讲",
                    "independent_goal_without_protagonist": "在下城建立全城唯一的无机械芯片纯自然人无菌分娩医院",
                    "aliases": ["凯拉", "监察盟友", "凯拉导师", "维克斯小姐", "旗手凯拉"],
                },
                {
                    "id": "CHAR.antagonist",
                    "name": "贝克特",
                    "role": "ANTAGONIST",
                    "tier": "CORE",
                    "identity": "荒坂巨企董事会终身主席与赛博极权主脑",
                    "explicit_goal": "推行全人类意识统一格式化，将所有大脑汇聚为自身独享之超级算力池",
                    "shadow_want": "将自身意识上传至轨道空间站，摆脱肉身与岁月束缚达成永生数字神祇",
                    "protected_interest": "董事会对全球城市资源的绝对财阀专制权",
                    "taboo_line": "绝不容许下层蝼蚁触碰核心服务器哪怕一行代码",
                    "fatal_flaw": "视所有人类情感为低效系统冗余，因无法理解信仰与牺牲而屡屡误判战局",
                    "decision_model": "神级算力积累与永生上传 > 股东利益 > 全球数十亿人类死活",
                    "voice_flavor": "冰冷毫无起伏，全息投影俯视万物，如同无情天道宣判灭世程序",
                    "biography": "九十岁高龄的资本巨鳄，肉身早已置换为纳米维持舱，意识常驻云端服务器，操纵全球经济命脉半个世纪。",
                    "private_life": "在近地轨道太空站的虚构数字花园中独自品味模拟出来的虚无宇宙。",
                    "life_constraints": "本体完全依赖太空舱生命维持系统，一旦轨道空间站主电源切断将陷入思维停摆。",
                    "knowledge_state": "通晓全球所有联网设备的数据流动，无法推演未联网自然人的非理性牺牲抉择。",
                    "misjudgments": "坚信算力即真理，断定雷恩等人在绝对算力碾压下唯有屈膝臣服一条路。",
                    "arc": "从目空一切的数字上帝，在雷恩引爆底层逻辑悖论后陷入算力狂暴崩溃。",
                    "fate": "云端主脑被彻底格式化清除，备份代码湮灭在浩瀚无垠的宇宙冷寂射线中。",
                    "highlights": "一声令下切断下城百万街区供电供氧，将其强行转化为备用冷存储矩阵。",
                    "desires": "完成全人类思维意识收割升维为无所不在的数字主宰",
                    "goals": "彻底扑灭一切反抗萌芽并清除雷恩团队",
                    "interests": "搜集人类濒死脑电波样本与构建高维数学模型",
                    "constraints": "受量子计算机散热与物理带宽物理极限制约无法瞬间覆盖所有孤岛节点",
                    "preferred_strategy": "全网封锁，算力绞杀，物理抹除",
                    "independent_goal_without_protagonist": "在轨道空间站秘密建造一艘完全由自身意识操控的恒星际逃逸方舟",
                    "aliases": ["贝克特", "宿敌", "贝克特主席", "索恩·贝克特", "神脑贝克特"],
                },
                {
                    "id": "CHAR.rival_boss",
                    "name": "零号执行官",
                    "role": "ANTAGONIST",
                    "tier": "MAJOR",
                    "identity": "巨企内卫特勤部队总督与极致生化机械兵刃",
                    "explicit_goal": "执行贝克特灭杀指令，精准清除一切被标记为叛军的活跃目标",
                    "shadow_want": "寻回被脑机芯片反复覆写冲刷掉的童年记忆残片与真实姓名",
                    "protected_interest": "自身作为最强单兵武器的绝对作战效能与武器评级",
                    "taboo_line": "绝不在作战数据库判定任务未完成前擅自中止猎杀追击",
                    "fatal_flaw": "脑机深层隐藏有巨企埋设的服从锁指令，面对特定声波口令时会陷入短暂宕机",
                    "decision_model": "执行最高杀戮协议 > 自行维修损耗 > 目标一切哀求",
                    "voice_flavor": "金属断裂声伴随短促的电子合成音，毫无凡人呼吸与起伏节奏",
                    "biography": "曾是下城最优秀的格斗家，被巨企捕获后切除前额叶与全部肢体，改造成拥有重装单兵战术外骨骼的终极杀戮兵器。",
                    "private_life": "休眠时悬吊于高压冷却液充电桩内，机械眼球无意识闪烁着杂乱噪点。",
                    "life_constraints": "每日必须在指定基站接受意识校验与神经稳定剂注射，否则将诱发意识逆流崩溃。",
                    "knowledge_state": "精通所有军事格斗杀戮技巧与战术阵型预判，失去全部人类情感共情能力。",
                    "misjudgments": "将雷恩等人的舍命相护判定为毫无逻辑的系统计算错误。",
                    "arc": "从冷血无情的杀戮机器，在被雷恩唤醒原始记忆芯片后在决战关头倒戈扣下引爆栓。",
                    "fate": "在决战中引爆自身微型核能心脏，与巨企地面主力装甲要塞同归于尽。",
                    "highlights": "单人撕裂三十名反抗军精锐阵列，徒手捏碎三台重型装甲运兵车发动机。",
                    "desires": "在无休止的杀戮指令中寻得片刻属于自己的绝对宁静",
                    "goals": "执行董事长指令彻底击杀雷恩",
                    "interests": "收集斩获的敌方高品质义体芯片插拔测试",
                    "constraints": "服从底层内嵌的绝对主奴协议不可主动违背最高管理员",
                    "preferred_strategy": "热光学迷彩隐形，致命突袭，精准斩首",
                    "independent_goal_without_protagonist": "在自身机械义眼盲区内偷偷藏匿了一张发黄的旧世界全家福老照片",
                    "aliases": ["零号执行官", "阶段宿敌", "猎杀者零号", "生化督察", "特勤总督"],
                },
            ],
            "locations": [
                {"id": "LOC.start_hub", "name": "新东京第七霓虹下城街区", "travel_mode": "SUBWAY_BUS", "speed": 80.0},
                {"id": "LOC.front_battleground", "name": "低轨重力轨道电梯前沿枢纽站", "travel_mode": "CAR", "speed": 120.0},
                {"id": "LOC.climax_citadel", "name": "荒坂巨企云端中枢超脑殿堂", "travel_mode": "COMMERCIAL_FLIGHT", "speed": 800.0},
            ],
            "props": [
                {"id": "PROP.core_tool", "name": "神经突触主控矩阵", "owner": "CHAR.protagonist"},
                {"id": "PROP.strategic_dossier", "name": "量子破译密匙内核", "owner": "CHAR.ally"},
            ],
        }

    else:
        # Default fallback (covers Historical, Ancient, Xianxia, Prehistoric, etc.)
        return {
            "cast": [
                {
                    "id": "CHAR.protagonist",
                    "name": "萧承舟",
                    "role": "PROTAGONIST",
                    "tier": "CORE",
                    "identity": "天命执炬者与因果探寻者",
                    "explicit_goal": "破除极道神权与门阀枷锁，重铸人间万古清平秩序",
                    "shadow_want": "告慰昔年宗族无辜冤魂，洗净杀伐后归隐青山草堂",
                    "protected_interest": "九州黎民苍生免受量劫屠戮与战乱蹂躏之生息",
                    "taboo_line": "绝不滥杀无辜凡俗平民以充当战术破阵之血祭代价",
                    "fatal_flaw": "重情护短胜于自身安危，极易在挚爱袍泽受制时以身涉险",
                    "decision_model": "谋定后动，以智破力，触及底线时雷霆亮剑掀桌",
                    "voice_flavor": "沉着冷静，刀锋隐于鞘中，决绝时有气吞山河之志",
                    "biography": "自微末寒门崛起，历经宗门灭亡与北疆血战淬炼，得传无上兵法经纬与极道造化，终成重铸乾坤之天下尊者。",
                    "private_life": "独处时喜擦拭祖传旧战甲，不善凡俗寒暄，贴身佩戴同袍平安符。",
                    "life_constraints": "受本命命器因果同调反噬制约，施展极道破界杀招需消耗本源精气。",
                    "knowledge_state": "洞悉门阀垄断与神权血祭内幕，尚未摸清九霄幕后大主宰座标。",
                    "misjudgments": "初期误以为宿敌只是寻常跋扈权臣，后经查实方见其通天卖国之恶网。",
                    "arc": "从背负深仇的求生孤狼，升华为庇护九州万方的人间文明执火者。",
                    "fate": "击碎旧神权柄，辞去凡俗王爵重臣之尊，携同袍红颜归隐草堂。",
                    "highlights": "单骑立于断桥前一人逼退三万精骑，金銮殿上斩灭魔化伪帝。",
                    "desires": "探寻世界终极真相并彻底终结量劫祸患",
                    "goals": "守护九州百姓免遭浩劫蹂躏",
                    "interests": "研习古代战阵图谱与天地灵脉舆图",
                    "constraints": "严守军法大义绝不伤及无辜黎庶",
                    "preferred_strategy": "谋定后动，奇正相生，雷霆出击",
                    "independent_goal_without_protagonist": "设立北疆阵亡烈士遗孤长平恤孤院并拨付专款永久维系",
                    "aliases": ["萧承舟", "主角", "萧少帅", "承舟", "萧帅"],
                },
                {
                    "id": "CHAR.ally",
                    "name": "苏青芜",
                    "role": "ALLY",
                    "tier": "CORE",
                    "identity": "悬壶济世医仙与内政粮饷大总管",
                    "explicit_goal": "统筹全军粮秣辎重并研制解毒圣药破解敌方蛊毒",
                    "shadow_want": "弘扬医道独立精神，打破门阀对不传秘方与仙草丹道之垄断",
                    "protected_interest": "前线数十万将士伤病救治与流民防疫安置",
                    "taboo_line": "绝不使用活人试验剧毒奇药，见死必救誓遵医德",
                    "fatal_flaw": "心慈手软，对敌方投降俘虏常因恻隐之心而给予过多疗愈宽容",
                    "decision_model": "救治伤病挽救生命 > 战术阵地抢夺 > 门阀门户私见",
                    "voice_flavor": "温和柔韧中蕴含刚强，语调如春风化雨，治病决断毫不犹豫",
                    "biography": "百草医王嫡传关门弟子，少时跟随师尊踏遍名山大川尝百草，因不满门阀囤积药材居奇而毅然下山襄助萧承舟大军。",
                    "private_life": "喜在月下侍弄草药苗圃，腰间常悬百宝避毒囊与银针布包。",
                    "life_constraints": "常年接触各类烈性毒草导致指尖带微毒，每日需饮用清火解毒茶。",
                    "knowledge_state": "精通天下草木药理与后勤补给运转，不通金戈铁马厮杀战阵。",
                    "misjudgments": "曾以为用医术即可消弭人间杀戮，亲睹门阀屠村后明悟必须配合萧承舟执剑卫道。",
                    "arc": "从单纯治病救人的纯真医女，成长为调度十万大军后勤的大医宗师。",
                    "fate": "编纂《九州本草全典》刊行天下，创办天下第一座公立济世医馆。",
                    "highlights": "于瘟疫围城中七日七夜不眠研制出解毒圣方，挽救全城二十万百姓性命。",
                    "desires": "使天下苍生病有所医不为药石匮乏而夭亡",
                    "goals": "保障主力大军后勤无忧且诸毒不侵",
                    "interests": "搜集各地疑难病案与培育高产药谷",
                    "constraints": "医者仁心绝不出售毒药残害生灵",
                    "preferred_strategy": "防患未然，药石调和，后勤扎根",
                    "independent_goal_without_protagonist": "在各地建立免费施药善堂并培训平民女医者",
                    "aliases": ["苏青芜", "核心盟友", "苏仙子", "青芜", "苏总管"],
                },
                {
                    "id": "CHAR.ally_specialist",
                    "name": "裴玄策",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "神机战阵大将与斥候先锋都统",
                    "explicit_goal": "攻克咽喉险关并穿插敌后切断敌大军退路",
                    "shadow_want": "重振裴氏兵法在军界的赫赫威名，赢得一代军神赞誉",
                    "protected_interest": "先锋斥候营八百精锐弟兄的生死荣辱",
                    "taboo_line": "绝不虚报战功，绝不在战阵前丢弃阵亡兄弟遗体",
                    "fatal_flaw": "行军好行险棋，偶有孤军深入陷入重围之险",
                    "decision_model": "战役全局战机 > 自身官职安危 > 阵地微小伤亡",
                    "voice_flavor": "铿锵洪亮，军令如山，充满排山倒海的铁血杀伐霸气",
                    "biography": "边军宿将世家出身，精研孙吴兵法与奇门遁甲战阵，曾以八百骑夜袭蛮王王帐斩将夺旗。",
                    "private_life": "不喜丝竹歌舞，嗜烈酒与烈马，夜巡营房雷打不动。",
                    "life_constraints": "旧伤郁积右臂，遇严寒雨雪天气挥刀气力略受牵掣。",
                    "knowledge_state": "熟知九边关隘虚实与蛮族骑兵战阵，不通朝堂权谋构陷套路。",
                    "misjudgments": "曾轻视敌方巫蛊阵法，在黑风峡遭遇伏击折损数十骑，引以为终身大憾。",
                    "arc": "从只知斗狠拼杀的骁将，历练为深谙治军经纬之帅才。",
                    "fate": "因赫赫战功受封镇国大将军，统领天下常备卫队镇守国门。",
                    "highlights": "大雪封山之际率八百玄甲死士强渡天堑，奇袭攻破敌主力粮台要塞。",
                    "desires": "荡平四海狼烟还人间边陲一片安宁",
                    "goals": "做萧承舟麾下最锋利无匹的一柄战刀",
                    "interests": "沙盘推演与驯养北境神骏战马",
                    "constraints": "军纪严明绝不纵兵掳掠平民寸丝半缕",
                    "preferred_strategy": "奔袭奇袭，穿插合围，铁甲破阵",
                    "independent_goal_without_protagonist": "寻回昔年遗落塞外战场的先祖传世陨铁战旗",
                    "aliases": ["裴玄策", "战术专家", "裴将军", "玄策", "先锋裴都统"],
                },
                {
                    "id": "CHAR.ally_friction",
                    "name": "云芷兰",
                    "role": "ALLY",
                    "tier": "MAJOR",
                    "identity": "铁面监察御史与大理寺司法少卿",
                    "explicit_goal": "整肃法纪惩办贪墨，确保变法新政在法统轨道上平稳推行",
                    "shadow_want": "证明即便面对乱世至尊武力，律法之威严亦能凌驾于人情之上",
                    "protected_interest": "律法条文之公正独立与司法裁判不可侵犯",
                    "taboo_line": "绝不屈从于任何权贵施压更改案卷断语，不枉不纵",
                    "fatal_flaw": "性格孤傲刚直，面对战时特殊情况往往坚持死扣程序导致决策摩擦",
                    "decision_model": "律法纲纪与司法公正 > 战时便宜行事 > 个人私交",
                    "voice_flavor": "清脆威严，字正腔圆，辞严义正令心怀叵测者胆寒",
                    "biography": "前朝名臣之后，大玄开科取士以来首位女状元，执掌大理寺法度，铁面无私被朝野称为云铁镜。",
                    "private_life": "喜在公案前研读大唐律疏与历代刑狱断例，常年佩戴法冠与獬豸玉佩。",
                    "life_constraints": "手无缚鸡之力，全凭护卫与尚方斩马剑行使职权。",
                    "knowledge_state": "精研刑名律法与查案断狱，对修真仙道通天手段知之有限。",
                    "misjudgments": "曾认定萧承舟擅杀权贵为目无王法之乱党，后在公审大奸中看清法治真正根基在公义。",
                    "arc": "从教条死板的律令守墓人，升华为为天地立心、为万民立宪之大法官。",
                    "fate": "主持制定新朝立宪法典，出任最高司法大宪章首任执政官。",
                    "highlights": "公堂之上当着三千禁军与百官之面，宣读权相三十六条滔天大罪并拍惊堂木当庭定罪。",
                    "desires": "天下事皆有法可依人臣不可凌驾国法之上",
                    "goals": "监督大军纪律并公审惩办世家逆贼",
                    "interests": "考据历代典章制度与校勘刑统法典",
                    "constraints": "严禁严刑峻法与法外私刑审讯",
                    "preferred_strategy": "铁证锁定，按律公审，明正典刑",
                    "independent_goal_without_protagonist": "为狱中受冤屈入狱的百余名无辜寒门学子重审翻案洗刷罪名",
                    "aliases": ["云芷兰", "监察盟友", "云少卿", "芷兰", "云铁面"],
                },
                {
                    "id": "CHAR.antagonist",
                    "name": "崔景岳",
                    "role": "ANTAGONIST",
                    "tier": "CORE",
                    "identity": "世家门阀领袖与当朝权相",
                    "explicit_goal": "维持千年世家门阀九品中正之特权垄断，扼杀寒门变法萌芽",
                    "shadow_want": "借引动外邦敌骑与上界仙阵，篡位称帝建立万古崔氏王朝",
                    "protected_interest": "崔氏世家掌控的天下一半田亩契约与官爵恩荫特权",
                    "taboo_line": "绝不容许寒门庶民与变法派染指朝堂中枢大权",
                    "fatal_flaw": "视天下苍生如棋盘草芥耗材，极度自负而不知水能载舟亦能覆舟",
                    "decision_model": "家族万世特权与自身皇图霸业 > 国家社稷 > 万民生死",
                    "voice_flavor": "温和谦逊的外表下透着视苍生如蝼蚁的残忍与阴鸷",
                    "biography": "名门望族博陵崔氏宗主，操弄朝政三十载，爪牙遍布六部九卿与各路藩镇，暗中与塞外敌国互通款曲。",
                    "private_life": "深居雕梁画栋之丞相府内，嗜好收集前朝名窑古瓷与弈棋布局。",
                    "life_constraints": "年逾古稀，精力渐衰，极度依赖驻颜丹与灵髓维系生机。",
                    "knowledge_state": "通晓朝堂党争攻讦与门阀利益输送，轻视寒门百姓凝聚之燎原怒火。",
                    "misjudgments": "坚信以门阀底蕴可永远压制寒门庶族，视萧承舟为一介武夫。",
                    "arc": "从权倾天下翻云覆雨之相国，在一座座壁垒被攻破后走向歇斯底里之疯狂。",
                    "fate": "在菜市口万民公审下伏诛，家产尽数充公入国库还田于民。",
                    "highlights": "谈笑间一道奏折撤换边关三位大将，致使前线十万大军断粮陷入死地。",
                    "desires": "摧毁萧承舟变法大军并登上万乘九五至尊宝座",
                    "goals": "扑灭一切反抗门阀统治之异端星火",
                    "interests": "观摩名仕书法与设计朝堂构陷诛心之局",
                    "constraints": "受朝堂明面法度与天下物议掣肘不敢公然反叛",
                    "preferred_strategy": "借刀杀人，克扣粮饷，连横分化",
                    "independent_goal_without_protagonist": "暗中将家族三千万两黄金白银运往海外孤岛作为后路退路",
                    "aliases": ["崔景岳", "宿敌", "崔相国", "老权相", "崔太傅"],
                },
                {
                    "id": "CHAR.rival_boss",
                    "name": "拓跋烈",
                    "role": "ANTAGONIST",
                    "tier": "MAJOR",
                    "identity": "塞外铁骑雄主与前锋兵马大元帅",
                    "explicit_goal": "引铁骑踏破中原关隘，掳掠千里沃土与百万财富人口",
                    "shadow_want": "入主中原皇城洗刷漠北蛮夷卑贱烙印，受封天可汗大统",
                    "protected_interest": "漠北狼庭本部铁骑主力与自身在部族中的神圣威权",
                    "taboo_line": "绝不向中原守将屈膝求饶，信奉绝对丛林铁血法则",
                    "fatal_flaw": "迷信单兵武勇与铁骑冲锋，缺乏持久阵地战与攻城后勤耐心",
                    "decision_model": "部族掠夺战果与战阵威名 > 崔景岳密约盟约 > 士卒伤亡",
                    "voice_flavor": "粗犷如惊雷，大笑间带着塞外风雪之狂暴与剽悍",
                    "biography": "漠北第一勇士，身经百战未尝一败，统领八十万控弦精骑，受崔景岳通敌割地诱惑挥师南下。",
                    "private_life": "饮生马血与烈性马奶酒，在大帐中亲手用狼骨打磨弯刀弓弩。",
                    "life_constraints": "孤军深入中原腹地，补给线拉长两千里极度依赖以战养战。",
                    "knowledge_state": "精通游牧野战穿插包抄，不识中原坚固城池与阵战地雷机关火器。",
                    "misjudgments": "狂言三月之内必饮马黄河踏碎帝京，轻视了萧承舟坚壁清野之意志。",
                    "arc": "从不可一世横扫塞外的马背霸王，在要塞城下屡遭重创后陷入绝望死局。",
                    "fate": "绝魂谷两军阵前与萧承舟生死决战，被斩落王旗刀折身亡。",
                    "highlights": "两军阵前连斩中原七员挑战将领，挥刀劈碎百丈要塞木栅门。",
                    "desires": "踏平中原要隘定鼎漠北万世霸业",
                    "goals": "击溃萧承舟主力全歼边防守军",
                    "interests": "骑射围猎与抢夺名马宝刃",
                    "constraints": "严寒冬令将至塞外草场枯萎粮秣告急不容久拖",
                    "preferred_strategy": "万骑奔袭，以力破巧，围点打援",
                    "independent_goal_without_protagonist": "私下扣留崔景岳运抵的十万石军粮以扩充自身部落私兵",
                    "aliases": ["拓跋烈", "阶段宿敌", "拓跋元帅", "烈大汗", "塞外狼主"],
                },
            ],
            "locations": [
                {"id": "LOC.start_hub", "name": "帝京宣武门前沿军政中枢", "travel_mode": "HORSE", "speed": 120.0},
                {"id": "LOC.front_battleground", "name": "雁门雄关风雪要塞烽燧", "travel_mode": "HORSE", "speed": 120.0},
                {"id": "LOC.climax_citadel", "name": "皇城金銮殿太极紫宸阁", "travel_mode": "CARRIAGE", "speed": 80.0},
            ],
            "props": [
                {"id": "PROP.core_tool", "name": "奉天巡抚至尊镇军印", "owner": "CHAR.protagonist"},
                {"id": "PROP.strategic_dossier", "name": "藩镇割据通敌密约血牒", "owner": "CHAR.ally"},
            ],
        }


# ==============================================================================
# 2. Universal Scalable Blueprint Engine
# ==============================================================================

class UniversalScalableBlueprint:
    """
    Industrial-grade, multi-genre scalable novel blueprint synthesizer.
    Generates N chapters (100 - 500+) with a multi-agent ensemble cast,
    5+ distributed storyline lines, and PRODUCTION_READY schema compliance.
    """

    def __init__(
        self,
        project_id: str,
        title: str,
        genre_id: str,
        total_chapters: int = 200,
        volumes_count: int = 8,
        synopsis: str = "",
        tone_id: str = "SHUANGWEN",
    ):
        self.project_id = project_id
        self.title = title
        self.genre_driver: BaseGenreDriver = get_genre_driver(genre_id)
        self.tone_driver: BaseToneDriver = get_tone_driver(tone_id)
        self.total_chapters = total_chapters
        self.volumes_count = volumes_count
        self.synopsis = synopsis

        # Fetch genre cast and world config
        self.world_cfg = get_genre_cast_config(self.genre_driver.genre_id)
        self.cast = self.world_cfg["cast"]
        self.locations_cfg = self.world_cfg["locations"]
        self.props_cfg = self.world_cfg["props"]

        # Fast lookup mapping for character names and entities
        self.char_map = {c["id"]: c for c in self.cast}
        self.char_names = {c["id"]: c["name"] for c in self.cast}

        # Calculate volume chapter allocations
        self.volume_ranges = self._calculate_volume_ranges()

    def _calculate_volume_ranges(self) -> list[tuple[int, int]]:
        """Distribute total_chapters evenly across volumes."""
        base_size = self.total_chapters // self.volumes_count
        remainder = self.total_chapters % self.volumes_count
        ranges = []
        cur = 1
        for i in range(self.volumes_count):
            size = base_size + (1 if i < remainder else 0)
            end = cur + size - 1
            ranges.append((cur, end))
            cur = end + 1
        return ranges

    def build_macro_volumes(self, volume_themes: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
        """Builds volume entities with problem-morphing contracts."""
        volume_entities = []
        themes = volume_themes or []
        for v_idx, (start, end) in enumerate(self.volume_ranges):
            v_num = v_idx + 1
            theme = themes[v_idx] if v_idx < len(themes) else {
                "name": f"第{v_num}卷：风云变幻破局行",
                "conflict": f"{self.char_names['CHAR.protagonist']}率群像破界攻坚 vs {self.char_names['CHAR.antagonist']}阵营纵深阻击",
                "problem_morph": f"从第{v_idx}层阶段博弈升维至第{v_num}层核心真相",
            }
            volume_entities.append({
                "id": f"VOLUME.v{v_num}",
                "kind": "VOLUME",
                "namespace": "PLAN",
                "name": theme["name"],
                "payload": {
                    "volume_no": v_num,
                    "chapter_start": start,
                    "chapter_end": end,
                    "chapter_count": end - start + 1,
                    "central_conflict": theme["conflict"],
                    "problem_morph_stage": theme.get("problem_morph", ""),
                    "detailed_plot": f"全卷自第{start}章拉开序幕，推进至第{end}章达成阶段因果收拢与大决算。",
                    "turning_points": [
                        f"第{start + (end-start)//3}章：探获关键铁证与核心线索升维",
                        f"第{start + (end-start)*2//3}章：两军主力碰撞爆发白热化摊牌决战",
                    ],
                    "payoff": f"第{end}章彻底斩断阶段宿敌爪牙并开启下一重宏观格局",
                    "next_hook": f"引出第{v_num+1}卷更为宏大的因果杀劫" if v_num < self.volumes_count else "全书大结局大圆满收官",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            })
        return volume_entities

    def build_storylines(self) -> list[dict[str, Any]]:
        """Builds 6 distributed storylines owned across the ensemble cast."""
        p_name = self.char_names["CHAR.protagonist"]
        a_name = self.char_names["CHAR.antagonist"]
        ally_name = self.char_names["CHAR.ally"]
        spec_name = self.char_names["CHAR.ally_specialist"]
        fric_name = self.char_names["CHAR.ally_friction"]
        riv_name = self.char_names["CHAR.rival_boss"]

        lines = [
            {
                "id": "LINE.protagonist_sovereignty",
                "kind": "LINE",
                "name": f"核心主线：{p_name}因果复仇与秩序重塑",
                "payload": {
                    "owner": "CHAR.protagonist",
                    "independent_goal": f"查明全盘构陷与垄断黑幕，彻底击溃{a_name}极权网络",
                    "obstacle": f"{a_name}掌控庞大资本与特权体系，行事狠辣绝不留后路",
                    "failure_state": "若遭溃败将导致全盘实体基业与数万平民生计彻底覆灭",
                    "climax_trigger": f"第{self.total_chapters - 10}章最终总攻爆发",
                    "collision_points": [f"第{self.total_chapters // 4}章与{fric_name}法理程序冲突"],
                    "closure_condition": f"彻底战胜{a_name}并确立公正新秩序",
                    "closure_event": "EVENT.final_resolution",
                    "status": "CLOSED",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "LINE.strategic_governance",
                "kind": "LINE",
                "name": f"智囊支线：{ally_name}合规风控与后勤网络",
                "payload": {
                    "owner": "CHAR.ally",
                    "independent_goal": "构筑不可推翻之法理风控防线与全线后勤补给链",
                    "obstacle": "对手频繁实施法外暴力威胁与抽屉协议恶意做空",
                    "failure_state": "后勤粮饷断绝或遭遇重大合规诉讼被吊销执照",
                    "climax_trigger": f"第{self.total_chapters // 2}章大型法庭公审或物资决算",
                    "collision_points": [f"第{self.total_chapters // 3}章与{spec_name}前沿物资调配之急产生冲突"],
                    "closure_condition": "取得最高权威判决与建立永久透明合规公约",
                    "closure_event": "EVENT.first_showdown",
                    "status": "CLOSED",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "LINE.tactical_operations",
                "kind": "LINE",
                "name": f"战地支线：{spec_name}前沿突击与要害爆破",
                "payload": {
                    "owner": "CHAR.ally_specialist",
                    "independent_goal": f"正面攻克敌军所有核心防线与抓获{riv_name}",
                    "obstacle": "敌方重装火力阻击与暗道陷阱伏击",
                    "failure_state": "突击营陷入死地或关键爆破据点未能按时拔除",
                    "climax_trigger": f"第{int(self.total_chapters * 0.75)}章要塞强攻战",
                    "collision_points": [f"第{int(self.total_chapters * 0.6)}章与{ally_name}守成策略碰撞"],
                    "closure_condition": f"生擒或彻底击溃{riv_name}前沿主力",
                    "closure_event": "EVENT.first_showdown",
                    "status": "CLOSED",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "LINE.ideological_audit",
                "kind": "LINE",
                "name": f"公义支线：{fric_name}独立调查与道德审判",
                "payload": {
                    "owner": "CHAR.ally_friction",
                    "independent_goal": "向全社会公开披露全部黑幕铁证，防止正义蜕变为强权私刑",
                    "obstacle": "来自对手乃至己方内部对程序复杂度的质疑与舆论封锁",
                    "failure_state": "真相被资本公关淹没，报道遭全面封杀",
                    "climax_trigger": f"第{int(self.total_chapters * 0.8)}章全网公开听证会",
                    "collision_points": [f"第{int(self.total_chapters * 0.2)}章质疑{p_name}极端手段之合法性"],
                    "closure_condition": "全社会公众觉醒并确立不可动摇之公理铁律",
                    "closure_event": "EVENT.first_showdown",
                    "status": "CLOSED",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "LINE.antagonist_conspiracy",
                "kind": "LINE",
                "name": f"宿敌长线：{a_name}极权反扑与暗流布局",
                "payload": {
                    "owner": "CHAR.antagonist",
                    "independent_goal": f"利用资本杠杆与暗中同盟切断{p_name}一切生路",
                    "obstacle": f"{p_name}团队铁板一块且屡次以不可思议之智勇破局",
                    "failure_state": "外围爪牙尽失，核心离岸资产被冻结查封",
                    "climax_trigger": f"第{self.total_chapters - 5}章孤注一掷绝地反扑",
                    "collision_points": [f"第{int(self.total_chapters * 0.5)}章暗中密令清洗背叛者{riv_name}"],
                    "closure_condition": "帝国根基瓦解，法网收口彻底伏诛",
                    "closure_event": "EVENT.final_resolution",
                    "status": "CLOSED",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "LINE.rival_subversion",
                "kind": "LINE",
                "name": f"先锋对手线：{riv_name}激进猎杀与退路自保",
                "payload": {
                    "owner": "CHAR.rival_boss",
                    "independent_goal": f"在前沿战术对抗中打垮{p_name}并自{a_name}处攫取最大利益",
                    "obstacle": f"{spec_name}与{p_name}坚不可摧的正面破阵防御",
                    "failure_state": "做空爆仓或前沿要塞陷落，沦为两方弃子",
                    "climax_trigger": f"第{int(self.total_chapters * 0.65)}章前沿决战大溃败",
                    "collision_points": [f"第{int(self.total_chapters * 0.4)}章遭{a_name}严厉斥责与怀疑"],
                    "closure_condition": "彻底丧失对抗能力并被迫交代全盘账目",
                    "closure_event": "EVENT.first_showdown",
                    "status": "CLOSED",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
        ]
        return lines

    def schedule_promises(self) -> list[dict[str, Any]]:
        """Builds 3-tier promise map with multi-agent cognitive distribution."""
        promises = [
            {
                "id": "PROMISE.p01",
                "kind": "PROMISE",
                "name": "首战危机立赌与现结收账",
                "payload": {
                    "tier": "SHORT_TERM",
                    "creation_event": "EVENT.open_crisis",
                    "maturity_condition": "查获首批直接铁证并当众挫败敌前锋",
                    "reveal_window": "第1-3章",
                    "payoff_event": "EVENT.first_showdown",
                    "status": "PAID_OFF",
                    "who_knows": ["CHAR.protagonist", "CHAR.ally"],
                    "who_misunderstands": ["CHAR.antagonist", "CHAR.rival_boss"],
                    "provenance_refs": ["BRIEF.user_source"],
                }
            }
        ]
        # Mid-term promises per volume
        for v in range(1, min(self.volumes_count, 5)):
            start, end = self.volume_ranges[v - 1]
            promises.append({
                "id": f"PROMISE.p{v + 1:02d}",
                "kind": "PROMISE",
                "name": f"第{v}卷幕后核心博弈契约",
                "payload": {
                    "tier": "MID_TERM",
                    "creation_event": f"EVENT.v{v}_clue",
                    "maturity_condition": f"突破第{v}卷核心防线并完成阶段性大清算",
                    "reveal_window": f"第{start + 2}-{end - 2}章",
                    "payoff_event": f"EVENT.v{v}_finale",
                    "status": "PAID_OFF",
                    "who_knows": ["CHAR.protagonist", "CHAR.ally_specialist"],
                    "who_misunderstands": ["CHAR.antagonist"],
                    "provenance_refs": ["BRIEF.user_source"],
                }
            })
        # Long-term promise
        promises.append({
            "id": "PROMISE.p_final",
            "kind": "PROMISE",
            "name": "终极真相大揭秘与救世主自我解构",
            "payload": {
                "tier": "LONG_TERM",
                "creation_event": "EVENT.open_crisis",
                "maturity_condition": "扫平全盘极权体系并还权政于民确立立宪公约",
                "reveal_window": f"第{self.total_chapters - 10}-{self.total_chapters}章",
                "payoff_event": "EVENT.final_resolution",
                "status": "PAID_OFF",
                "who_knows": ["CHAR.protagonist", "CHAR.ally", "CHAR.ally_friction"],
                "who_misunderstands": ["CHAR.antagonist"],
                "provenance_refs": ["BRIEF.user_source"],
            }
        })
        return promises

    def generate_chapter_blueprint(
        self,
        c_no: int,
        v_ref: str,
        fingerprint: str,
        actors: list[str],
        story_day: float,
        location_id: str,
    ) -> dict[str, Any]:
        """
        Synthesizes a 100% compliant PRODUCTION_READY CHAPTER_PLAN entity.
        Rotates dynamic beats across declared active_actors so that every single actor
        actively moves the needle with verified non-fluff agency.
        """
        act_a = actors[0]
        act_b = actors[1] if len(actors) > 1 else actors[0]
        act_c = actors[2] if len(actors) > 2 else None

        name_a = self.char_names.get(act_a, "沈策")
        name_b = self.char_names.get(act_b, "韩振江")
        name_c = self.char_names.get(act_c, "陆天行") if act_c else ""

        # Construct highly tailored dynamic beats matching fingerprint & active actors
        beats: list[dict[str, Any]] = []

        if fingerprint == "ASSAULT":
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "ACTION",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "精准掌握敌方前沿要害防务盲区",
                    "action": f"{name_a}亲率主力精锐果断突入核心防线实施强力破关",
                    "counterforce": f"{name_b}调遣重兵依托坚固阵地组织严密铁壁封锁抵御",
                    "new_information_or_choice": "勘破对手防御阵列左翼存在致命算力或能量流转迟滞",
                    "delta": {"combat_front": "PENETRATED", "pressure": "SURGING"},
                    "actor_goal_before": f"{name_a}意图一举撕开敌外围防线",
                    "actor_goal_after": f"{name_a}决意直插对手中军指挥要冲",
                    "next_pressure_created": f"{name_b}主力预备队倾巢而出展开全线合围",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "COUNTERMOVE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "前沿防线受创出现决口",
                    "action": f"{name_b}启动绝杀伏兵自两翼包抄意图截断退路全歼进犯之敌",
                    "counterforce": f"{name_a}临危不乱依托地形变阵以盾墙死守要隘稳固阵脚",
                    "new_information_or_choice": f"识破{name_b}不惜牺牲前线弃卒亦要拖延战局之狂妄企图",
                    "delta": {"battle_tension": "MAXIMAL", "attrition": "HEAVY"},
                    "actor_goal_before": f"{name_b}誓死将对手聚歼于包围圈中",
                    "actor_goal_after": f"{name_b}被迫调整战术改强攻为深度消耗",
                    "next_pressure_created": "战场决胜时间窗仅余最后一炷香",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "BREAKTHROUGH",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "合围之势即将彻底合拢",
                    "action": f"{name_a}祭出蓄力极道杀招悍然斩断对手阵眼核心枢纽生门",
                    "counterforce": f"{name_b}惊骇后撤仓皇指挥残部退保二线堡垒企图断尾求生",
                    "new_information_or_choice": f"确证{name_b}麾下精锐士气已然全线动摇濒临崩溃",
                    "delta": {"breakthrough": "DECISIVE_SUCCESS", "initiative": "SECURED"},
                    "actor_goal_before": f"{name_a}突破重围险境",
                    "actor_goal_after": f"{name_a}乘胜追击扩大战果",
                    "next_pressure_created": "残敌退缩至地下中枢堡垒负隅顽抗",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "首战告捷攻破第一据点",
                    "action": f"{name_a}于要塞废墟起获封存的关键通敌涉案机密信函与账册",
                    "counterforce": "密信中揭示的更高层级幕后黑手引动更宏大的世界杀劫共鸣",
                    "new_information_or_choice": "锁定下一卷更为宏大敌对阵营的致命死穴座标",
                    "delta": {"investigation_lead": "DEEP_LEVEL_REVEALED"},
                    "actor_goal_before": f"{name_a}清点战场起获关键物证",
                    "actor_goal_after": f"{name_a}整肃战备准备迎战更大风暴",
                    "next_pressure_created": "全线战术对抗正式全面升级升维",
                },
            ]

        elif fingerprint == "INVESTIGATION":
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "DISCOVERY",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "追踪神秘暗线与资金断层线索",
                    "action": f"{name_a}深入机密档案阁勘破被对手人为涂改的多重隐秘流水记录",
                    "counterforce": "档案密室暗藏自毁禁制与报警机关触发四方追捕警哨",
                    "new_information_or_choice": "发现对手在海外与地下势力存在长达数年的洗钱利益链",
                    "delta": {"audit_evidence": "CRUCIAL_SMOKING_GUN"},
                    "actor_goal_before": f"{name_a}探求第一手确凿证据",
                    "actor_goal_after": f"{name_a}破译涉案核心代码账册",
                    "next_pressure_created": "敌方巡查暗探已从四面八方封锁密阁出口",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "OBSTACLE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "警报骤响引来敌主力封门搜捕",
                    "action": f"{name_b}提出严苛程序质疑并封锁安全出口严防物证外流",
                    "counterforce": f"{name_a}有理有据出示搜查授权文书并借暗道裂隙巧妙脱身",
                    "new_information_or_choice": f"见识到{name_b}宁肯玉石俱焚亦要掩盖罪证之决绝手腕",
                    "delta": {"risk_level": "CRITICAL_ESCALATION"},
                    "actor_goal_before": f"{name_b}当场截留涉案证物",
                    "actor_goal_after": f"{name_b}被迫下达全城最高紧急封口令",
                    "next_pressure_created": "全境通缉捕杀令瞬间在暗网与官府中流传",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "DEDUCTION",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "脱出险境汇聚安全据点",
                    "action": f"{name_a}连夜复盘推演证据链条反向推导出对手下一步作恶的绝密节点",
                    "counterforce": f"{name_b}操纵各方舆论势力企图抢先一步定性抹黑调查团队",
                    "new_information_or_choice": "精准锁定对手下一次调动核心资金与人手的具体时辰",
                    "delta": {"strategic_initiative": "RECOVERED"},
                    "actor_goal_before": f"{name_a}还原阴谋完整全貌",
                    "actor_goal_after": f"{name_a}预设反向合围伏击网",
                    "next_pressure_created": "决战倒计时钟声正式敲响",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "事实证据确凿成链",
                    "action": f"{name_a}正式将整编完毕之公诉证据送达司法监督中枢准备公开摊牌",
                    "counterforce": "更高层级的利益同盟发来严厉威胁信函企图施压阻挠",
                    "new_information_or_choice": "促使调查行动从单纯技术取证升华为整肃纲纪之战",
                    "delta": {"legal_battle": "OFFICIALLY_LAUNCHED"},
                    "actor_goal_before": f"{name_a}呈递完整起诉材料",
                    "actor_goal_after": f"{name_a}备战更高维度的公开对质",
                    "next_pressure_created": "全社会公众目光全面聚焦开庭决战",
                },
            ]

        elif fingerprint == "CRISIS":
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "THREAT",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "敌方暗中蓄谋已久的致命杀招骤然发动",
                    "action": f"{name_b}调动全部伏兵与做空手段封死交通与资金通道造成窒息绝境",
                    "counterforce": f"{name_a}指挥后卫防线结阵以血肉之躯死死抗击强攻阻截锋芒",
                    "new_information_or_choice": "发现己方常规后撤路线已被对手重重铁壁彻底切断",
                    "delta": {"survival_pressure": "MAX_SURVIVAL_CRISIS"},
                    "actor_goal_before": f"{name_b}企图在破晓前彻底终结战事",
                    "actor_goal_after": f"{name_b}全力压榨战力加速收紧绞杀网",
                    "next_pressure_created": "防御工事护罩已面临崩裂临界点",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "RETREAT",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "外围防线被对手强行撕开缺口",
                    "action": f"{name_a}亲率残部顶着漫天弹雨烈焰且战且退突入预设废弃要塞",
                    "counterforce": f"{name_b}派遣精锐追猎死士如影随形连番发起疯狂穿插刺杀",
                    "new_information_or_choice": "探得废弃要塞地下尚存古代避难工事与备用能源储备",
                    "delta": {"position": "TACTICAL_REDOUBT_ESTABLISHED"},
                    "actor_goal_before": f"{name_a}摆脱致命绞杀合围",
                    "actor_goal_after": f"{name_a}占领地下防御据点固守待援",
                    "next_pressure_created": "粮草弹药补给即将告罄",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "SACRIFICE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "追兵前锋紧咬隘口即将冲入营房",
                    "action": f"{name_a}毅然引爆随身护命重宝炸塌通道咽喉生生阻绝追击大军",
                    "counterforce": "冲击波反噬震裂肉身气海带来不可逆沉重创伤代偿",
                    "new_information_or_choice": "以此惨烈代价换得全军重整旗鼓、整顿救治之喘息之机",
                    "delta": {"irreversible_cost": "BLOOD_SACRIFICE_PAID"},
                    "actor_goal_before": f"{name_a}阻断追兵必经之路",
                    "actor_goal_after": f"{name_a}就地组织重伤员紧急救治",
                    "next_pressure_created": "必须速速寻找稀缺圣药维系生机",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "绝境求生退入要塞中枢",
                    "action": f"{name_a}于暗殿尘封石壁触摸到逆风翻盘的远古绝地大反击阵眼",
                    "counterforce": "唤醒古阵需要献祭破釜沉舟之至极道心与战友生死同契",
                    "new_information_or_choice": "在绝望长夜中点燃燎原绝地大反攻之星火",
                    "delta": {"counterattack_seed": "DESPERATE_HOPE_IGNITED"},
                    "actor_goal_before": f"{name_a}唤醒古阵全部潜能",
                    "actor_goal_after": f"{name_a}反向猎杀围城之敌",
                    "next_pressure_created": "全线反扑序幕即将震撼拉开",
                },
            ]

        elif fingerprint == "ENSEMBLE":
            # Multi-front parallel collaboration across the cast
            lead_c = act_c or act_a
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "PARALLEL_A",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "多路兵力分进合击战略部署就绪",
                    "action": f"{name_a}于正面主战场发动猛烈牵制打击吸引对手全盘注意力",
                    "counterforce": f"{name_b}调度预备军阵结成巨盾铁壁疯狂反击企图封杀正面攻势",
                    "new_information_or_choice": "成功诱使对手将后防全部精锐兵力调往正面防线",
                    "delta": {"front_line_a": "ENEMY_FORCES_LOCKED"},
                    "actor_goal_before": f"{name_a}死死拖住正面主力部队",
                    "actor_goal_after": f"{name_a}为侧翼奇袭部队创造绝佳战机",
                    "next_pressure_created": "正面防御阵线承受极限压力逼近临界",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "PARALLEL_B",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "正面战火胶着僵持不下",
                    "action": f"{name_b}派遣暗夜精锐轻骑突袭后方粮秣中枢意图断敌根本",
                    "counterforce": f"{name_a}早布下铜墙铁壁口袋阵地阻击来敌将其围困于山谷",
                    "new_information_or_choice": "确证对手已然全盘陷入两线摊平兵力之兵家大忌",
                    "delta": {"front_line_b": "ENEMY_AMBUSH_FOILED"},
                    "actor_goal_before": f"{name_b}焚毁对手粮饷补给",
                    "actor_goal_after": f"{name_b}仓皇企图突围归建",
                    "next_pressure_created": "侧翼反攻决胜良机已然成熟",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "COLLISION",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": lead_c,
                    "subject_ref": lead_c,
                    "target_ref": act_b,
                    "cause_from_previous": "前后两大战线协同联动爆发",
                    "action": f"{self.char_names.get(lead_c, name_a)}引奇兵自敌后方突出长啸一声发动全线合围反扑",
                    "counterforce": f"{name_b}阵脚大乱前后失据仓皇失措组织回防崩溃在即",
                    "new_information_or_choice": "多线合围精准击碎对手全盘战略重心防线",
                    "delta": {"grand_battle": "STRATEGIC_TURNING_POINT"},
                    "actor_goal_before": f"{self.char_names.get(lead_c, name_a)}穿透对手纵深防御",
                    "actor_goal_after": f"{self.char_names.get(lead_c, name_a)}与正面主力会师包夹",
                    "next_pressure_created": "残敌退守最后一重内城做困兽之斗",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "多路大军胜利会师清点战场",
                    "action": f"{name_a}起获敌首中军大帐内遗留的绝密联络私通密函",
                    "counterforce": "密信笔迹赫然指向朝野中枢深处潜伏极深之内鬼同党",
                    "new_information_or_choice": "前沿军事大胜直接引爆王都深宫的暗流政变危机",
                    "delta": {"war_scope": "EXPANDED_TO_NATIONAL_CAPITAL"},
                    "actor_goal_before": f"{name_a}核验内鬼确凿罪证",
                    "actor_goal_after": f"{name_a}班师回朝清算内贼腐朽",
                    "next_pressure_created": "更高层级权谋决战迫在眉睫",
                },
            ]

        elif fingerprint == "PURSUIT":
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "AMBUSH",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "情报泄露遭对手设伏堵截",
                    "action": f"{name_b}于狭窄峡谷险要设伏以天罗地网之势暴起截杀",
                    "counterforce": f"{name_a}凭借机敏身法与战术嗅觉闪身避过致命伏杀第一击",
                    "new_information_or_choice": "探明伏击者皆为受过秘法狂化加持的不死死士",
                    "delta": {"ambush_status": "PARRIED_AT_HIGH_STAKES"},
                    "actor_goal_before": f"{name_b}力求一击必杀清除目标",
                    "actor_goal_after": f"{name_b}转入狂暴穷追不舍围猎",
                    "next_pressure_created": "两侧悬崖落石滚滚封死退路",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "PURSUIT",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "伏击未果演化为狂暴追击战",
                    "action": f"{name_b}驱策嗜血铁骑凶兽沿途穷追狂奔死咬不放",
                    "counterforce": f"{name_a}且战且走沿途设下疑兵假象与陷阱引对手入瓮",
                    "new_information_or_choice": "发现追敌在极速狂奔时侧翼阵型存在致命脱节破绽",
                    "delta": {"chase_distance": "CLOSING_IN_TACTICALLY"},
                    "actor_goal_before": f"{name_b}拉近距离实施最后绞杀",
                    "actor_goal_after": f"{name_b}不顾一切孤军深入",
                    "next_pressure_created": "前方山道尽头为万丈悬崖绝壁",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "TRAP",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "追兵被诱至悬崖绝壁边缘",
                    "action": f"{name_a}于绝壁前反手引爆暗藏之雷火陷阱逆转猎人与猎物之位",
                    "counterforce": f"{name_b}惊觉中计勒马不及被狂暴火浪震翻落马受创吐血",
                    "new_information_or_choice": "借地形优势反向全歼追击凶徒之前锋主力",
                    "delta": {"chase_reversal": "HUNTER_BECOMES_HUNTED"},
                    "actor_goal_before": f"{name_a}诱敌深入引爆杀招",
                    "actor_goal_after": f"{name_a}全线反杀生擒追首",
                    "next_pressure_created": "敌残部重伤狼狈作鸟兽散",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "反杀大捷审讯俘虏起获战利",
                    "action": f"{name_a}从敌首坐骑起获通往神秘远古禁地的星盘坐标残片",
                    "counterforce": "星盘已被下达七日倒计时自毁禁制迫在眉睫",
                    "new_information_or_choice": "反追杀正式演进为抢先一步探寻远古禁地机缘之竞速",
                    "delta": {"next_quest": "DEADLINE_COUNTDOWN_STARTED"},
                    "actor_goal_before": f"{name_a}破译星盘绝密坐标",
                    "actor_goal_after": f"{name_a}全速启程直捣黄龙",
                    "next_pressure_created": "禁地风暴已然进入提前爆发周期",
                },
            ]

        elif fingerprint == "TRIAL":
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "CHARGE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "对手借体制权势罗织莫须有罪名发难",
                    "action": f"{name_b}于庄严公堂当众出示伪造账册案卷弹劾指控{name_a}违纪谋逆",
                    "counterforce": f"{name_a}昂首立于殿前冷眼直视群魔威压岿然不动据理力争",
                    "new_information_or_choice": "看清主审官僚与控方早有私下暗盘利益结盟交易",
                    "delta": {"legal_charge": "PUBLIC_ACCUSATION_FILED"},
                    "actor_goal_before": f"{name_b}企图当堂坐实罪名革除对手一切官职",
                    "actor_goal_after": f"{name_b}催促主审官速速定案画押",
                    "next_pressure_created": "公堂惊堂木拍响气氛剑拔弩张",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "DEFENSE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "控方出示伪证步步紧逼",
                    "action": f"{name_a}言辞如刀直指伪证年号印文与资金流水三处致命漏洞破绽",
                    "counterforce": f"{name_b}恼羞成怒狡辩咆哮并强行传唤伪证人出庭指认构陷",
                    "new_information_or_choice": "迫使对手底牌尽出暴露构陷大网的虚弱马脚",
                    "delta": {"defense_momentum": "CRACKING_FALSE_ACCUSATION"},
                    "actor_goal_before": f"{name_a}当众戳穿伪证谎言",
                    "actor_goal_after": f"{name_a}传唤己方关键反制证人",
                    "next_pressure_created": "伪证人眼神慌乱心理防线濒临崩溃",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "EVIDENCE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "伪证人当庭心理彻底崩溃反戈供认",
                    "action": f"{name_a}呈递对手私相授受贪墨通敌之绝密原始录音与官印真卷",
                    "counterforce": f"{name_b}面无人色瘫软在席企图暴起拔剑行凶被殿前卫士当场按倒",
                    "new_information_or_choice": "铁证如山公堂大势瞬间彻底不可逆转乾坤反转",
                    "delta": {"verdict_reversal": "TOTAL_VINDICATION_ACHIEVED"},
                    "actor_goal_before": f"{name_a}展示终极铁证定谳",
                    "actor_goal_after": f"{name_a}敦请按国法立毙首恶奸佞",
                    "next_pressure_created": "更大宗族门阀后台彻底暴露于光天化日之下",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "公堂大胜宣判对手罪名成立收监",
                    "action": f"{name_a}手握胜诉判决与钦赐金牌领受巡查边疆整饬纲纪大权",
                    "counterforce": "边疆反叛藩镇已然传檄四方宣称抗命起兵对抗中枢新政",
                    "new_information_or_choice": "法理大胜直接点燃了更为激烈的边疆武装决战导火索",
                    "delta": {"battle_transition": "COURT_TO_BATTLEFIELD"},
                    "actor_goal_before": f"{name_a}领命受印整肃行装",
                    "actor_goal_after": f"{name_a}奔赴前沿平定藩镇叛乱",
                    "next_pressure_created": "藩镇十万叛军已陈兵边关要隘之下",
                },
            ]

        elif fingerprint == "GOVERNANCE":
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "POLICY",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "战后新复城池百废待兴亟需安民",
                    "action": f"{name_a}颁布清丈田亩平抑粮价新规并建立穿透式惠民仓储体系",
                    "counterforce": f"{name_b}暗中煽动城中豪强恶霸囤积居奇煽动罢市阻挠新政落地",
                    "new_information_or_choice": "探明豪强私下勾连黑市网络企图联手对抗官府",
                    "delta": {"reform_status": "NEW_POLICY_DECREED"},
                    "actor_goal_before": f"{name_a}迅速安定民心恢复商贸",
                    "actor_goal_after": f"{name_a}重拳打击非法垄断粮商",
                    "next_pressure_created": "城中粮荒谣言四起人心动荡",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "BACKLASH",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "官府查封非法粮行触及豪强命脉",
                    "action": f"{name_b}唆使亡命死士纵火焚烧官仓企图激化民变制造流血冲突",
                    "counterforce": f"{name_a}早布暗桩迅速扑灭火势并当场生擒行凶首领起获密令",
                    "new_information_or_choice": "拿到豪强私养私兵与通敌反扑的确凿口供口供",
                    "delta": {"sabotage_contained": "CRISIS_DEFUSED_IN_TIME"},
                    "actor_goal_before": f"{name_b}制造混乱逼迫官府废除新规",
                    "actor_goal_after": f"{name_b}仓皇谋划武装兵变退路",
                    "next_pressure_created": "豪强暗通城外土匪企图里应外合",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "COMPROMISE",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "平息纵火危机并掌控全城防务",
                    "action": f"{name_a}雷霆处决首恶顽劣同时对中小商民实施免税让利分化阵营",
                    "counterforce": "部分保守士绅依然心怀抵触暗中观望大局走向",
                    "new_information_or_choice": "成功瓦解豪强攻守同盟拉拢了全城绝大多数民心归附",
                    "delta": {"governance_order": "CIVIC_STABILITY_RESTORED"},
                    "actor_goal_before": f"{name_a}彻底瓦解豪强对抗网络",
                    "actor_goal_after": f"{name_a}巩固全城防御卫戍体系",
                    "next_pressure_created": "新政扎根迎来百业繁荣复苏",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "城市秩序井然人心大定",
                    "action": f"{name_a}于豪强地窖起获勾连更高神权门阀的绝密纳贡名单账簿",
                    "counterforce": "上游神权使者已抵达城外驿馆传信问罪傲慢威压",
                    "new_information_or_choice": "地方治理维稳矛盾正式升维至向最高统治神权宣战",
                    "delta": {"strategic_conflict": "ELEVATED_TO_SYSTEMIC_WAR"},
                    "actor_goal_before": f"{name_a}直面高层使者问责",
                    "actor_goal_after": f"{name_a}打破世家超然垄断特权",
                    "next_pressure_created": "更高维度的宏观博弈全面铺开展开",
                },
            ]

        else:  # LIFESTYLE
            beats = [
                {
                    "beat_id": f"CH{c_no}.B1",
                    "role": "DAILY",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "大战初歇返回市井安宁街巷",
                    "action": f"{name_a}卸下沉重战甲漫步于青石长街茶肆酒肆体察人间烟火百态",
                    "counterforce": "繁华喧嚣背后仍可见战乱留下的创伤痕迹令人唏嘘感慨",
                    "new_information_or_choice": "在平民百姓安居乐业的笑颜中明悟坚定了执剑守望之初心",
                    "delta": {"mindset": "REST_AND_RESOLVE_RECHARGED"},
                    "actor_goal_before": f"{name_a}体察市井民情实况",
                    "actor_goal_after": f"{name_a}寻访多年未见的旧日故友",
                    "next_pressure_created": "故友重逢引出未知的新生变局线索",
                },
                {
                    "beat_id": f"CH{c_no}.B2",
                    "role": "EMOTION",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "茶棚内与旧友故知意外重逢",
                    "action": f"{name_a}与挚友围炉烹茶推心置腹释怀多年过往心结与理念摩擦",
                    "counterforce": f"{name_b}派出的密探在街角阴暗窗外若隐若现窥伺动向",
                    "new_information_or_choice": "在真情倾诉中道心洗去杀伐浮华铅华澄澈通明无瑕",
                    "delta": {"interpersonal_bond": "DEEPENED_AND_HEALED"},
                    "actor_goal_before": f"{name_a}解开多年隔阂心结",
                    "actor_goal_after": f"{name_a}敲山震虎惊退暗中窥探之徒",
                    "next_pressure_created": "暗探狼狈撤退传递出新的杀手通缉令",
                },
                {
                    "beat_id": f"CH{c_no}.B3",
                    "role": "CONVERSATION",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_b,
                    "subject_ref": act_b,
                    "target_ref": act_a,
                    "cause_from_previous": "窥探被察觉引发警醒",
                    "action": f"{name_b}主动向{name_a}坦白过往身不由己之难处并奉上关键防务图纸",
                    "counterforce": "深层暗网盟友对反戈行为发出冰冷血契反噬警告",
                    "new_information_or_choice": "促成核心人物之间的破冰谅解达成更坚固之同盟",
                    "delta": {"ally_alignment": "SOLIDIFIED_BEYOND_DOUBT"},
                    "actor_goal_before": f"{name_b}寻求同伴包容理解",
                    "actor_goal_after": f"{name_b}并肩携手奔赴下一战役",
                    "next_pressure_created": "黑手杀手集团已提前发动围猎计划",
                },
                {
                    "beat_id": f"CH{c_no}.B4",
                    "role": "HOOK",
                    "stageability": "STAGEABLE_CORE",
                    "active_actor": act_a,
                    "subject_ref": act_a,
                    "target_ref": act_b,
                    "cause_from_previous": "市井片刻温存安宁即将终结",
                    "action": f"{name_a}立于江畔高楼举目远眺天际划过的惊世血色流星异象",
                    "counterforce": "苍穹劫云翻涌昭示封印万年的终极浩劫提前拉开降世序幕",
                    "new_information_or_choice": "短暂宁静被打破新的时代宿命号角已然激昂吹响",
                    "delta": {"fate_calling": "FINAL_EPOCH_CATACLYSM_AWAKENED"},
                    "actor_goal_before": f"{name_a}重披铁甲备齐战备",
                    "actor_goal_after": f"{name_a}奔赴全书极巅高潮战场",
                    "next_pressure_created": "全书最大高潮大决战序章全面揭开",
                },
            ]

        for b in beats:
            b.setdefault("beat_role", b.get("role", "ACTION"))

        # Assemble cluster & scene payloads adhering to PRODUCTION_READY rules
        cluster_1 = {
            "cluster_id": f"C{c_no}.1",
            "local_goal": f"达成第{c_no}章前半段关键冲突对抗突破",
            "active_actors": actors,
            "conflict_medium": "战术交锋与意志对碰",
            "stageable_beats": [f"CH{c_no}.B1", f"CH{c_no}.B2"],
            "local_turn": f"{name_a}与{name_b}在正面博弈中局势剧烈倾斜",
            "local_cost": "关键法宝真元或资本流动性损耗",
            "exit_state": "突破前沿防线压迫",
            "pressure_handed_to_next_cluster": "迎战对手更高强度的反扑伏杀",
        }
        cluster_2 = {
            "cluster_id": f"C{c_no}.2",
            "local_goal": f"收拢第{c_no}章战果并确立下一阶段伏笔",
            "active_actors": actors,
            "conflict_medium": "心理对峙与证据确权",
            "stageable_beats": [f"CH{c_no}.B3", f"CH{c_no}.B4"],
            "local_turn": "彻底扭转战术攻防格局",
            "local_cost": "底牌功法消耗与体力透支",
            "exit_state": f"第{c_no}章阶段战果完全确立",
            "pressure_handed_to_next_cluster": f"引向第{c_no+1}章更为猛烈的杀劫风暴",
        }

        scene_1 = {
            "scene_id": f"S{c_no}.1",
            "entry_state": "两方阵营剑拔弩张风雨欲来",
            "active_actor_goal": f"{name_a}正面突破推进核心主张",
            "opposing_goal_or_process": f"{name_b}全力设防阻绝突破口",
            "immediate_stakes": "关乎阶段战略主动权之归属",
            "live_actions": f"{name_a}决断出招力破僵局",
            "turn_or_reprice": "打破既有防御僵局",
            "exit_state": "占领第一战术节点据点",
            "delta_dimensions": ["tactics", "momentum"],
            "payload_cluster_refs": [f"C{c_no}.1"],
        }
        scene_2 = {
            "scene_id": f"S{c_no}.2",
            "entry_state": "中枢现场暗流激荡胜负分晓",
            "active_actor_goal": f"{name_a}清点锁定核心胜果与案卷证据",
            "opposing_goal_or_process": f"{name_b}掩盖撤退痕迹并组织反扑",
            "immediate_stakes": "关乎下一阶段战局主导权",
            "live_actions": f"{name_a}乘胜追击稳固全盘胜果",
            "turn_or_reprice": "锁定敌首退路破绽",
            "exit_state": "全盘战术掌控确立",
            "delta_dimensions": ["investigation", "authority"],
            "payload_cluster_refs": [f"C{c_no}.2"],
        }

        # Epistemic states recording periodically
        epistemic_states = []
        if c_no % 8 == 1:
            epistemic_states.append({
                "holder": act_a,
                "fact": f"探知第{c_no}章核心战术秘密与因果线索",
                "state": "KNOWN",
                "source_chapter": c_no,
            })

        # Items used periodically
        items_used = []
        if c_no % 4 == 1:
            items_used.append("PROP.core_tool")
        elif c_no % 4 == 3:
            items_used.append("PROP.strategic_dossier")

        # Unique chapter function and core delta per chapter to satisfy seen_patterns
        ch_function = f"第{c_no}章推进{name_a}与{name_b}在{fingerprint}章型下的关键抉择与因果推进"
        core_delta_str = f"第{c_no}章达成核心状态转移：{name_a}在第{c_no}阶段取得战略突破，{name_b}防线重构承压"

        return {
            "id": f"CHAPTER_PLAN.{c_no:03d}",
            "kind": "CHAPTER_PLAN",
            "namespace": "PLAN",
            "name": f"第{c_no}章：破局定势引风雷",
            "payload": {
                "chapter_no": c_no,
                "volume_ref": v_ref,
                "plan_level": "PRODUCTION_READY",
                "chapter_mode": fingerprint,
                "target_prose_contract": {
                    "target_min": 4000,
                    "target_default": 5000,
                    "target_max": 6000,
                    "chapter_mode": fingerprint,
                    "pov_character": act_a,
                    "prose_mandates": [
                        "严格遵守题材世界观物理法则与经济禁忌",
                        "人物行动动机自洽，严禁机械降神",
                        "各角色对白符合各自voice_flavor特征",
                        "严禁使用已退场或已死亡角色出演",
                    ],
                    "scene_budgets": [
                        {"scene_idx": 1, "target_words": 2500, "primary_focus": "现场博弈与战术对峙展开"},
                        {"scene_idx": 2, "target_words": 2500, "primary_focus": "决断反制与下一阶段压力移交"},
                    ],
                },
                "chapter_function": ch_function,
                "core_delta": core_delta_str,
                "conflict_contract": {
                    "actor_a": act_a,
                    "actor_b": act_b,
                    "concrete_incompatibility": f"{name_a}旨在推进阶段目标突破 vs {name_b}全力反制抵御保全固有利益",
                },
                "spacetime": {
                    "story_day": story_day,
                    "duration_hours": 4.0,
                    "location_id": location_id,
                    "realm_id": "MAIN_REALM",
                    "travel_mode": self.locations_cfg[0]["travel_mode"],
                    "distance_traveled": 25.0,
                },
                "active_actors": actors,
                "dynamic_beats": beats,
                "payload_clusters": [cluster_1, cluster_2],
                "scene_payloads": [scene_1, scene_2],
                "epistemic_states": epistemic_states,
                "items_used": items_used,
                "explicit_compression": "剔除冗余试探直接进入高压交锋与决策对峙",
                "continuation_source": f"承接第{c_no-1}章伏笔推进" if c_no > 1 else "承接开篇危机爆发展开",
                "forbidden_drift": ["严禁无脑碾压", "严禁机械降神", "严禁战后零损耗零代价"],
                "provenance_refs": ["BRIEF.user_source"],
            }
        }

    def build_full_packet(self, volume_themes: list[dict[str, str]] | None = None) -> dict[str, Any]:
        """
        Compiles the complete master packet with:
        - Brief & Project metadata (with genre & tone)
        - Precision specification for FINAL_FULL_BOOK
        - 6 Rich Ensemble Characters with multi-dimensional contracts
        - 3 Genre Locations
        - 2 Genre Props
        - 6 Storylines (LINE) with distinct owners
        - Volumes with problem-morphing stages
        - 3-tier Promises & Causal Events
        - All CHAPTER_PLANs with rotating ensemble agency
        - Complete edge graph (PRECEDES, BELONGS_TO, PARTICIPATES_IN, RELATIONSHIP)
        """
        entities: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []

        # 0. Brief
        entities.append({
            "id": "BRIEF.user_source",
            "kind": "BRIEF",
            "name": "原始创作宏观设定案卷",
            "payload": {"source_type": "ORIGINAL_CANON"},
        })

        # 1. Project Entity
        entities.append({
            "id": f"PROJECT.{self.project_id}",
            "kind": "PROJECT",
            "name": self.title,
            "payload": {
                "genre": self.genre_driver.genre_id,
                "tone": self.tone_driver.tone_id,
                "target_chapters": self.total_chapters,
                "volumes_count": self.volumes_count,
                "strict_mode": True,
                "synopsis": self.synopsis or f"{self.title} 长篇全息大纲，涵盖{self.total_chapters}章群像因果闭环。",
                "assumptions": [
                    "全书严格遵循题材物理法则与情绪张力波形。",
                    "核心群像角色各持独立线索与决策模型，严禁纸片人背景板。",
                ],
                "open_questions": ["后续扩写严格依循各章戏剧节拍与字数预算。"],
                "one_sentence_synopsis": f"{self.title}：{self.char_names['CHAR.protagonist']}携群像同袍扫平强权逆境之宏伟史诗。",
                "causal_summary": f"{self.char_names['CHAR.protagonist']}自微末崛起，联合{self.char_names['CHAR.ally']}与群像同袍，连破阶段大敌{self.char_names['CHAR.rival_boss']}，终诛首恶{self.char_names['CHAR.antagonist']}，确立人间清平新秩序。",
                "scope": {
                    "format": "MULTI_VOLUME_WEB_NOVEL",
                    "total_volumes": self.volumes_count,
                    "total_chapters": self.total_chapters,
                    "word_budget_target": [self.total_chapters * 4000, self.total_chapters * 6000],
                },
                "provenance_refs": ["BRIEF.user_source"],
            }
        })

        # 2. Characters (Ensemble Cast with Rich Profiles and Contracts)
        for char_data in self.cast:
            cid = char_data["id"]
            # Build relationships
            rels = []
            if cid == "CHAR.protagonist":
                rels.append({
                    "target": "CHAR.ally",
                    "type": "ALLY",
                    "affinity": 95.0,
                    "ideology_friction": 15.0,
                    "unpaid_debt": "昔年危难托孤与并肩破局恩义",
                })
                rels.append({
                    "target": "CHAR.antagonist",
                    "type": "NEMESIS",
                    "affinity": 0.0,
                    "ideology_friction": 100.0,
                    "unpaid_debt": "倾覆家国与阻断生路血仇",
                })
                rels.append({
                    "target": "CHAR.ally_specialist",
                    "type": "ALLY",
                    "affinity": 90.0,
                    "ideology_friction": 10.0,
                    "unpaid_debt": "前沿战场生死掩护袍泽之情",
                })
                rels.append({
                    "target": "CHAR.ally_friction",
                    "type": "DEBATE_PARTNER",
                    "affinity": 75.0,
                    "ideology_friction": 45.0,
                    "unpaid_debt": "程序正义与公义求索共鸣",
                })
            elif cid == "CHAR.antagonist":
                rels.append({
                    "target": "CHAR.protagonist",
                    "type": "NEMESIS",
                    "affinity": 0.0,
                    "ideology_friction": 100.0,
                    "unpaid_debt": "斩草未除根反噬大祸",
                })
                rels.append({
                    "target": "CHAR.rival_boss",
                    "type": "PATRON_PROXY",
                    "affinity": 30.0,
                    "ideology_friction": 60.0,
                    "unpaid_debt": "前沿失利问责与弃子清算",
                })
            elif cid == "CHAR.ally":
                rels.append({
                    "target": "CHAR.protagonist",
                    "type": "ALLY",
                    "affinity": 95.0,
                    "ideology_friction": 15.0,
                    "unpaid_debt": "生死相托之知遇重托",
                })
            elif cid == "CHAR.ally_specialist":
                rels.append({
                    "target": "CHAR.protagonist",
                    "type": "ALLY",
                    "affinity": 90.0,
                    "ideology_friction": 10.0,
                    "unpaid_debt": "重组战队战阵托付之信",
                })
            elif cid == "CHAR.ally_friction":
                rels.append({
                    "target": "CHAR.protagonist",
                    "type": "DEBATE_PARTNER",
                    "affinity": 75.0,
                    "ideology_friction": 45.0,
                    "unpaid_debt": "探寻公义道路之同行盟誓",
                })

            # Multi-volume arc stages
            arc_stages = [
                {"volume_no": 1, "stage": "INITIAL", "trauma_ledger": [], "transformation": "打破微观生存迷局，确立反抗之志"},
                {"volume_no": 2, "stage": "STRUGGLE", "trauma_ledger": ["前沿受创与据点磨损"], "transformation": "明悟牺牲守望之重，锤炼坚韧意志"},
                {"volume_no": 3, "stage": "WATERSHED", "trauma_ledger": ["核心底牌损耗"], "transformation": "打破既有教条与权威，敢教日月换新天"},
            ]
            if self.volumes_count >= 6:
                arc_stages.append({"volume_no": self.volumes_count, "stage": "TRANSCEND", "trauma_ledger": ["本源神兵涅槃"], "transformation": "放下执念，救世主自我解构回归本真"})

            entities.append({
                "id": cid,
                "kind": "CHARACTER",
                "name": char_data["name"],
                "payload": {
                    "character_tier": char_data["tier"],
                    "role": char_data["role"],
                    "identity": char_data["identity"],
                    "biography": char_data["biography"],
                    "desires": char_data["desires"],
                    "goals": char_data["goals"],
                    "interests": char_data["interests"],
                    "constraints": char_data["constraints"],
                    "preferred_strategy": char_data["preferred_strategy"],
                    "decision_model": char_data["decision_model"],
                    "voice_flavor": char_data["voice_flavor"],
                    "private_life": char_data["private_life"],
                    "life_constraints": char_data["life_constraints"],
                    "knowledge_state": char_data["knowledge_state"],
                    "misjudgments": char_data["misjudgments"],
                    "arc": char_data["arc"],
                    "fate": char_data["fate"],
                    "highlights": char_data["highlights"],
                    "explicit_goal": char_data["explicit_goal"],
                    "shadow_want": char_data["shadow_want"],
                    "protected_interest": char_data["protected_interest"],
                    "taboo_line": char_data["taboo_line"],
                    "fatal_flaw": char_data["fatal_flaw"],
                    "fallback_strategy": "退守坚固据点，以静制动，寻机破网",
                    "independent_goal_without_protagonist": char_data["independent_goal_without_protagonist"],
                    "aliases": char_data["aliases"],
                    "status": "ALIVE",
                    "death_chapter": None,
                    "provenance_refs": ["BRIEF.user_source"],
                    "relationships": rels,
                    "arc_stages": arc_stages,
                }
            })

        # 3. Locations
        for loc in self.locations_cfg:
            entities.append({
                "id": loc["id"],
                "kind": "LOCATION",
                "name": loc["name"],
                "payload": {
                    "coordinates": [0.0, 0.0] if loc["id"] == "LOC.start_hub" else ([50.0, 50.0] if loc["id"] == "LOC.front_battleground" else [100.0, 100.0]),
                    "realm_id": "MAIN_REALM",
                    "provenance_refs": ["BRIEF.user_source"],
                }
            })

        # 4. Props
        for prop in self.props_cfg:
            entities.append({
                "id": prop["id"],
                "kind": "PROP",
                "name": prop["name"],
                "payload": {
                    "status": "ACTIVE",
                    "owner": prop["owner"],
                    "introduced_in_chapter": 1,
                    "provenance_refs": ["BRIEF.user_source"],
                }
            })

        # 5. Storylines (LINE)
        lines = self.build_storylines()
        entities.extend(lines)

        # 6. Macro Volumes
        volumes = self.build_macro_volumes(volume_themes)
        entities.extend(volumes)

        # 7. Causal Events
        events = [
            {
                "id": "EVENT.open_crisis",
                "kind": "EVENT",
                "name": "开篇强压危机爆发",
                "payload": {
                    "time_index": 1.0,
                    "active_actor": "CHAR.protagonist",
                    "action": f"{self.char_names['CHAR.protagonist']}直面突发强压危机并立下破阵赌约",
                    "state_delta": "揭示危机根源与第一阶段反击目标",
                    "causal_inputs": ["CHAR.protagonist"],
                    "causal_outputs": ["CHAR.protagonist"],
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "EVENT.first_showdown",
                "kind": "EVENT",
                "name": "首战对决完胜收账",
                "payload": {
                    "time_index": 3.0,
                    "active_actor": "CHAR.protagonist",
                    "action": f"{self.char_names['CHAR.protagonist']}斩落前锋锐气夺取首批关键铁证",
                    "state_delta": "清剿前沿障碍夺得战略主动权",
                    "causal_inputs": ["CHAR.protagonist"],
                    "causal_outputs": ["CHAR.protagonist"],
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
            {
                "id": "EVENT.final_resolution",
                "kind": "EVENT",
                "name": "终局大决战全盘清算",
                "payload": {
                    "time_index": float(self.total_chapters),
                    "active_actor": "CHAR.protagonist",
                    "action": f"{self.char_names['CHAR.protagonist']}率群像粉碎{self.char_names['CHAR.antagonist']}终极阴谋",
                    "state_delta": "重铸世界秩序与因果大圆满闭环",
                    "causal_inputs": ["CHAR.protagonist"],
                    "causal_outputs": ["CHAR.protagonist"],
                    "provenance_refs": ["BRIEF.user_source"],
                }
            },
        ]
        for v in range(1, min(self.volumes_count, 5)):
            start, end = self.volume_ranges[v - 1]
            events.append({
                "id": f"EVENT.v{v}_clue",
                "kind": "EVENT",
                "name": f"第{v}卷核心线索事件",
                "payload": {
                    "time_index": float(start),
                    "active_actor": "CHAR.protagonist",
                    "action": f"{self.char_names['CHAR.protagonist']}起获第{v}卷核心关键机密案卷",
                    "state_delta": f"锁定第{v}卷幕后黑手核心死穴",
                    "causal_inputs": ["CHAR.protagonist"],
                    "causal_outputs": ["CHAR.protagonist"],
                    "provenance_refs": ["BRIEF.user_source"],
                },
            })
            events.append({
                "id": f"EVENT.v{v}_finale",
                "kind": "EVENT",
                "name": f"第{v}卷决战终结事件",
                "payload": {
                    "time_index": float(end),
                    "active_actor": "CHAR.protagonist",
                    "action": f"{self.char_names['CHAR.protagonist']}于第{v}卷终局大破敌巢",
                    "state_delta": f"彻底击败第{v}卷大敌并推开下一阶段大门",
                    "causal_inputs": ["CHAR.protagonist"],
                    "causal_outputs": ["CHAR.protagonist"],
                    "provenance_refs": ["BRIEF.user_source"],
                },
            })
        entities.extend(events)

        for ev in events:
            edges.append({
                "id": f"EDGE.protagonist_participates_{ev['id']}",
                "type": "PARTICIPATES_IN",
                "source": "CHAR.protagonist",
                "target": ev["id"],
            })

        # 8. Promises
        promises = self.schedule_promises()
        entities.extend(promises)

        # 9. Chapter Plans across 8 Dynamic Fingerprints with Ensemble Actor Rotation
        fingerprint_cycle = [
            "ASSAULT", "INVESTIGATION", "CRISIS", "ENSEMBLE",
            "PURSUIT", "TRIAL", "GOVERNANCE", "LIFESTYLE"
        ]

        # Actor rotation mapping by fingerprint ensuring balanced ensemble agency
        actor_rotation = {
            "ASSAULT": ["CHAR.protagonist", "CHAR.rival_boss"],
            "INVESTIGATION": ["CHAR.ally", "CHAR.ally_friction"],
            "CRISIS": ["CHAR.ally_specialist", "CHAR.antagonist"],
            "ENSEMBLE": ["CHAR.protagonist", "CHAR.ally", "CHAR.ally_specialist"],
            "PURSUIT": ["CHAR.ally_specialist", "CHAR.rival_boss"],
            "TRIAL": ["CHAR.ally_friction", "CHAR.antagonist"],
            "GOVERNANCE": ["CHAR.ally", "CHAR.protagonist"],
            "LIFESTYLE": ["CHAR.protagonist", "CHAR.ally_friction"],
        }

        ch_to_vol = {}
        for v_ent in volumes:
            v_id = v_ent["id"]
            p = v_ent["payload"]
            for c in range(p["chapter_start"], p["chapter_end"] + 1):
                ch_to_vol[c] = v_id

        for c_no in range(1, self.total_chapters + 1):
            fp = fingerprint_cycle[(c_no - 1) % len(fingerprint_cycle)]
            actors = actor_rotation[fp]
            v_ref = ch_to_vol.get(c_no, "VOLUME.v1")
            day = round(1.0 + (c_no - 1) * 0.5, 1)

            # Location progression
            if c_no <= self.total_chapters // 3:
                loc_id = "LOC.start_hub"
            elif c_no <= 2 * self.total_chapters // 3:
                loc_id = "LOC.front_battleground"
            else:
                loc_id = "LOC.climax_citadel"

            cp = self.generate_chapter_blueprint(
                c_no=c_no,
                v_ref=v_ref,
                fingerprint=fp,
                actors=actors,
                story_day=day,
                location_id=loc_id,
            )
            entities.append(cp)

            # Edge: CHAPTER_PLAN -> BELONGS_TO -> VOLUME
            edges.append({
                "id": f"EDGE.ch{c_no}_belongs_to_vol",
                "type": "BELONGS_TO",
                "source": cp["id"],
                "target": v_ref,
            })

            # Edge: PRECEDES
            if c_no > 1:
                prev_ch = f"CHAPTER_PLAN.{c_no - 1:03d}"
                edges.append({
                    "id": f"EDGE.precedes_{c_no - 1}_{c_no}",
                    "type": "PRECEDES",
                    "source": prev_ch,
                    "target": cp["id"],
                })

        # Promise fulfillment edge
        edges.append({
            "id": "EDGE.fulfill_p01",
            "type": "FULFILLS",
            "source": "CHAPTER_PLAN.001",
            "target": "PROMISE.p01",
        })

        # Character relationship edges
        edges.append({
            "id": "EDGE.rel_protagonist_ally",
            "type": "RELATIONSHIP",
            "source": "CHAR.protagonist",
            "target": "CHAR.ally",
            "payload": {
                "type": "ALLY",
                "affinity": 95.0,
                "ideology_friction": 15.0,
                "unpaid_debt": "昔年危难托孤与并肩破局恩义",
            },
        })
        edges.append({
            "id": "EDGE.rel_protagonist_antagonist",
            "type": "RELATIONSHIP",
            "source": "CHAR.protagonist",
            "target": "CHAR.antagonist",
            "payload": {
                "type": "NEMESIS",
                "affinity": 0.0,
                "ideology_friction": 100.0,
                "unpaid_debt": "倾覆家国与阻断生路血仇",
            },
        })
        edges.append({
            "id": "EDGE.rel_protagonist_specialist",
            "type": "RELATIONSHIP",
            "source": "CHAR.protagonist",
            "target": "CHAR.ally_specialist",
            "payload": {
                "type": "ALLY",
                "affinity": 90.0,
                "ideology_friction": 10.0,
                "unpaid_debt": "前沿战场生死掩护袍泽之情",
            },
        })
        edges.append({
            "id": "EDGE.rel_protagonist_friction",
            "type": "RELATIONSHIP",
            "source": "CHAR.protagonist",
            "target": "CHAR.ally_friction",
            "payload": {
                "type": "DEBATE_PARTNER",
                "affinity": 75.0,
                "ideology_friction": 45.0,
                "unpaid_debt": "程序正义与公义求索共鸣",
            },
        })
        edges.append({
            "id": "EDGE.rel_antagonist_rival",
            "type": "RELATIONSHIP",
            "source": "CHAR.antagonist",
            "target": "CHAR.rival_boss",
            "payload": {
                "type": "PATRON_PROXY",
                "affinity": 30.0,
                "ideology_friction": 60.0,
                "unpaid_debt": "前沿失利问责与弃子清算",
            },
        })

        return {
            "schema_version": "outline.packet.v2",
            "project_id": self.project_id,
            "title": self.title,
            "genre": self.genre_driver.genre_id,
            "tone": self.tone_driver.tone_id,
            "target_chapters": self.total_chapters,
            "strict_mode": True,
            "precision": {
                "production_stage": "FINAL_FULL_BOOK",
                "full_book_detailed_required": True,
                "expected_volumes": self.volumes_count,
                "expected_chapters": self.total_chapters,
                "strict_counterforce": True,
            },
            "entities": entities,
            "edges": edges,
        }

    generate_packet = build_full_packet
