import json
from pathlib import Path


SOURCE = ["BRIEF.user_source", "DESIGN.originalized_adaptation", "RUNTIME.vnext16_2"]
ACTOR_NAMES = {
    "CHAR.lin_du": "林渡", "CHAR.xu_jianxing": "许见星", "CHAR.zhou_zhige": "周止戈",
    "CHAR.jian_ning": "简宁", "CHAR.gao_wanqing": "高晚晴", "CHAR.gu_wangchuan": "顾妄川",
    "CHAR.lin_qiu": "蔺秋",
}
LOCATION_NAMES = {
    "LOC.memory_court": "记忆司法厅", "LOC.yanhui": "雁回旧城", "LOC.skyline_archive": "天际档案楼",
    "LOC.first_gate": "第一潮门", "LOC.deepsea_station": "深海观测站", "LOC.orbit_relay": "天穹气象中继站",
    "LOC.white_noise": "白噪塔",
}


def entity(entity_id, kind, name, payload, namespace="PLAN"):
    return {"id": entity_id, "kind": kind, "namespace": namespace, "name": name, "payload": payload}


def character(entity_id, name, identity, biography, desires, goals, interests, constraints, strategy, personality, private_life, knowledge, misjudgments, arc, highlights, fate):
    return entity(entity_id, "CHARACTER", name, {
        "character_tier": "CORE" if entity_id in {"CHAR.lin_du", "CHAR.xu_jianxing"} else "MAJOR",
        "identity": identity,
        "biography": biography,
        "desires": desires,
        "goals": goals,
        "interests": interests,
        "constraints": constraints,
        "preferred_strategy": strategy,
        "personality": personality,
        "decision_model": "先确认谁会承担代价，再决定是否公开信息；拒绝用一个人的拯救权替代所有人的选择。",
        "private_life": private_life,
        "life_constraints": constraints,
        "knowledge_state": knowledge,
        "misjudgments": misjudgments,
        "arc": arc,
        "growth_arc": arc,
        "highlights": highlights,
        "fate": fate,
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }, "CANON")


def chapter(record):
    number = record["n"]
    actors = record["actors"]
    roles = ["ACTION", "COUNTERMOVE", "REPLAN", "REVELATION", "COST", "HOOK"]
    actions = record["beats"]
    deltas = [
        {"position": record["delta"]},
        {"knowledge": record["info"]},
        {"route": record["choice"]},
        {"relationship": record["reveal"]},
        {"cost": record["cost"]},
        {"next": record["hook"]},
    ]
    beats = []
    for index, role in enumerate(roles):
        actor = actors[index % len(actors)]
        before = record["goal"]
        after = record["goal"] if index < 2 else f"{record['goal']}；同时必须处理{record['reveal']}"
        beats.append({
            "beat_id": f"CH{number}.B{index + 1}",
            "beat_role": role,
            "stageability": "STAGEABLE_CORE",
            "cause_from_previous": record["cause"] if index == 0 else actions[index - 1],
            "active_actor": actor,
            "actor_goal_before": before,
            "action": actions[index],
            "counterforce": record["counterforces"][index],
            "new_information_or_choice": record["info"] if index in {1, 3} else record["choice"],
            "delta": deltas[index],
            "actor_goal_after": after,
            "next_pressure_created": record["pressures"][index],
        })
    clusters = [
        {
            "cluster_id": f"CH{number}.CL1",
            "local_goal": record["cluster_goals"][0],
            "active_actors": actors,
            "conflict_medium": record["conflict_mediums"][0],
            "stageable_beats": [f"CH{number}.B1", f"CH{number}.B2"],
            "local_turn": record["cluster_turns"][0],
            "local_cost": record["cluster_costs"][0],
            "exit_state": record["cluster_exits"][0],
            "pressure_handed_to_next_cluster": record["pressures"][2],
        },
        {
            "cluster_id": f"CH{number}.CL2",
            "local_goal": record["cluster_goals"][1],
            "active_actors": actors,
            "conflict_medium": record["conflict_mediums"][1],
            "stageable_beats": [f"CH{number}.B3", f"CH{number}.B4"],
            "local_turn": record["cluster_turns"][1],
            "local_cost": record["cluster_costs"][1],
            "exit_state": record["cluster_exits"][1],
            "pressure_handed_to_next_cluster": record["pressures"][4],
        },
        {
            "cluster_id": f"CH{number}.CL3",
            "local_goal": record["cluster_goals"][2],
            "active_actors": actors,
            "conflict_medium": record["conflict_mediums"][2],
            "stageable_beats": [f"CH{number}.B5", f"CH{number}.B6"],
            "local_turn": record["cluster_turns"][2],
            "local_cost": record["cluster_costs"][2],
            "exit_state": record["cluster_exits"][2],
            "pressure_handed_to_next_cluster": record["hook"],
        },
    ]
    scenes = []
    for index, scene_name in enumerate(record["scenes"], 1):
        scenes.append({
            "scene_id": f"CH{number}.S{index}",
            "entry_state": record["scene_entries"][index - 1],
            "active_actor_goal": record["scene_goals"][index - 1],
            "opposing_goal_or_process": record["scene_opponents"][index - 1],
            "immediate_stakes": record["scene_stakes"][index - 1],
            "live_actions": record["scene_actions"][index - 1],
            "turn_or_reprice": record["scene_turns"][index - 1],
            "exit_state": record["scene_exits"][index - 1],
            "delta_dimensions": record["scene_dimensions"][index - 1],
            "payload_cluster_refs": [f"CH{number}.CL{index}"],
        })
    payload = {
        "plan_level": "PRODUCTION_READY",
        "chapter_no": number,
        "volume_ref": record["volume"],
        "target_prose_contract": {
            "unit": "CHINESE_PROSE_CHARACTERS",
            "target_min": 4000,
            "target_default": 5000,
            "target_max": 6000,
            "chapter_mode": "STANDARD_LONG",
        },
        "chapter_function": record["function"],
        "core_delta": record["delta"],
        "conflict_contract": {
            "actor_a": actors[0],
            "actor_b": actors[1],
            "concrete_incompatibility": record["conflict"],
            "stakes": record["stakes"],
        },
        "dynamic_beats": beats,
        "payload_clusters": clusters,
        "scene_payloads": scenes,
        "explicit_compression": [
            "普通赶路、库存清点和重复惊叹压缩成结果，不占独立节拍。",
            "技术原理只在改变选择、权限或证据时展开。",
            "不使用无名路人承载关键判断；普通人群体只作为背景时不得替代实名行动者。",
        ],
        "continuation_source": record["hook"],
        "forbidden_drift": [
            "不得把本章冲突改成单纯力量碾压。",
            "不得让任何角色凭空获得未埋设的证据或权限。",
            "不得用下一层更大反派替代本章已经形成的选择后果。",
        ],
        "line_clusters": record["lines"],
        "provenance_refs": ["DESIGN.originalized_adaptation", "RUNTIME.vnext16_2"],
    }
    return entity(f"CHAPTER_PLAN.{number:03d}", "CHAPTER_PLAN", record["title"], payload)


def rec(n, volume, title, actors, location, function, goal, opponent, conflict, stakes, cause, beats, counterforces, info, reveal, choice, cost, delta, hook, cluster_goals, cluster_turns, cluster_costs, cluster_exits, conflict_mediums, scenes, scene_entries, scene_goals, scene_opponents, scene_stakes, scene_actions, scene_turns, scene_exits, scene_dimensions=None, lines=None):
    if scene_dimensions is None:
        scene_dimensions = [["plot", "information", "resource"] for _ in range(3)]
    if lines is None:
        lines = ["LINE.names", "LINE.community_trust"]
    def three(values, fallback):
        values = list(values or [])
        while len(values) < 3:
            values.append(fallback)
        return values[:3]
    scene_entries = three(scene_entries, "进入场景，目标尚未兑现")
    scene_goals = three(scene_goals, goal)
    scene_opponents = three(scene_opponents, opponent)
    scene_stakes = three(scene_stakes, stakes)
    scene_actions = three(scene_actions, ["核验", "反制"])
    scene_turns = three(scene_turns, "资源或关系重新定价")
    if scene_exits and all(isinstance(value, str) and value.startswith("LINE.") for value in scene_exits):
        lines = list(scene_exits)
        scene_exits = list(cluster_exits)
    scene_exits = three(scene_exits, hook)
    scene_dimensions = three(scene_dimensions, ["information", "risk"])
    return {
        "n": n, "volume": volume, "title": title, "actors": actors, "location": location,
        "function": function, "goal": goal, "opponent": opponent, "conflict": conflict,
        "stakes": stakes, "cause": cause, "beats": beats, "counterforces": counterforces,
        "info": info, "reveal": reveal, "choice": choice, "cost": cost, "delta": delta,
        "hook": hook, "pressures": [
            f"压力转向：{cluster_exits[0]}", f"压力转向：{cluster_exits[0]}",
            f"压力转向：{cluster_exits[1]}", f"压力转向：{cluster_exits[1]}",
            f"压力转向：{cluster_exits[2]}", f"压力转向：{hook}",
        ], "cluster_goals": cluster_goals, "cluster_turns": cluster_turns,
        "cluster_costs": cluster_costs, "cluster_exits": cluster_exits,
        "conflict_mediums": conflict_mediums, "scenes": scenes,
        "scene_entries": scene_entries, "scene_goals": scene_goals,
        "scene_opponents": scene_opponents, "scene_stakes": scene_stakes,
        "scene_actions": scene_actions, "scene_turns": scene_turns,
        "scene_exits": scene_exits, "scene_dimensions": scene_dimensions,
        "lines": lines,
    }


project = entity("PROJECT.baizai", "PROJECT", "白噪归航", {
    "one_sentence_synopsis": "六年前背下沉港三万人死亡罪名的灾害工程师林渡，从白噪塔归来后发现死者名单被篡改，他必须沿九份失败记录追查真相，并在最终拥有改写全城记忆的权限时选择把罪责和选择权一起还给公众。",
    "causal_summary": "沉港事故让天幕控灾系统获得篡改记忆的合法入口，林渡归来救下被抹掉身份的居民，逐卷追回九份失败记录并确认自己当年也曾隐瞒一项风险，最终在白噪塔关闭记忆改写、公开完整责任链，天幕被拆成由居民共同审计的灾害网络。",
    "genre": "近未来海港灾害悬疑、归来复仇、群像升级、制度爽文",
    "reader_promise": "每卷解决一层现实压迫，同时让旧案更复杂；主角每次获得权限都要失去一段个人安全或公众信任，终局的爽点是拆掉唯一救世主的位置。",
    "originality_axes": [
        "主角的底牌是九份失败记录和有限权限，不是师父或血脉传承。",
        "核心世界引擎是灾害预警与记忆法，而不是武力境界。",
        "反派以降低灾害总死亡为真实目标，通过删去少数人的选择制造秩序。",
        "女性角色分别掌握医疗、证据、法律和社区组织，不承担被救工具功能。",
        "升级货币从战力换成可验证数据、公众信任、现场权限和制度授权。",
        "终局不是杀死最高反派，而是让所有人共同承担真实记忆的后果。",
    ],
    "provenance_refs": ["DESIGN.originalized_adaptation"],
}, "CONTRACT")

characters = [
    character("CHAR.lin_du", "林渡", "前天幕灾害工程师、白噪塔释放者",
               "六年前沉港事故中，林渡签下关闭外海闸门的建议，随后发现上级删掉了第三种方案。他因背负三万人死亡罪名被送入白噪塔，六年后以记忆残缺和九份失败记录归来。",
               ["找回沉港完整责任链", "阻止天幕继续删改受灾者身份", "让死者和幸存者都能拥有自己的叙述"],
               ["保住雁回社区", "找齐九份失败记录", "公开自己当年的隐瞒"],
               ["真实数据", "工程师同行", "受灾者的选择权"],
               ["白噪塔抹掉了部分私人记忆", "九份记录每启用一份就会暴露他一次违规", "公众把他当作事故罪魁", "身体无法连续承受记忆回放"],
               "先用现场工程和小规模证据救人，再公开一部分对自己不利的信息逼迫对手回应。",
               "冷静、固执、习惯计算撤离路线，最怕自己再次替别人决定谁值得被救。",
               "收藏一枚无法归档的旧船票，睡前把当天听到的名字写在纸上。",
               "知道事故不是单纯工程失败，不知道自己曾主动删掉一段早期警告。",
               ["以为公开真相会自动带来公正", "低估许见星会否决他的冒险方案", "把顾妄川看成纯粹的继承人而非同样被系统塑形的人"],
               "从只想洗清自己的归来者，成长为愿意承认个人责任并把灾害决定权拆给公众的制度重建者。",
               ["在雁回堤口用废弃阀门救下被注销的居民", "公开自己的第一条错误签批", "终局拒绝独占全城记忆权限"],
               "失去部分记忆和工程执照，成为公共灾害网络的现场审计员。"),
    character("CHAR.xu_jianxing", "许见星", "万象急救站医生、雁回社区证人组织者",
               "父亲在沉港事故后被列为失踪者，母亲的病历被天幕系统标记为不存在。许见星留在雁回社区，以急救站为中心保存被注销居民的生活证据。",
               ["保护被系统抹去身份的人", "让父亲的失踪有可验证的结论", "不让林渡替所有受害者发言"],
               ["保住急救站", "组织证人链", "迫使天幕承认记忆法的现实伤害"],
               ["病历隐私", "社区互助", "普通人能否拒绝被代表"],
               ["药品依赖财团供应", "证人一旦公开会失去补偿", "不能把病人的隐私当成证据"],
               "先保护人的身体和隐私，再把证据交给能持续保管的公共机构。",
               "直接、警惕英雄叙事、对林渡有旧情但不把旧情当信任。",
               "每天给急救站屋顶的药草换水，把父亲的旧呼号写在值班表背面。",
               "知道雁回有一批被注销居民，不知道其中有人替天幕保存过原始数据。",
               ["认为林渡只会用工程权限强行解决问题", "以为自己可以独自保护全部证人"],
               "从独自守住急救站的医生，成长为让受灾者共同决定证据如何被使用的社区协调者。",
               ["拒绝用病人名单换药", "在公开听证中让证人自己说出被删掉的生活", "终局否决林渡独占记忆权限"],
               "主持雁回公共记忆站，成为新灾害网络的第一任民间轮值负责人。"),
    character("CHAR.zhou_zhige", "周止戈", "潮线工会潜水员、旧闸门维修队长",
               "周止戈的哥哥死在沉港前夜的检修井里，官方说是违规潜水，他一直认为哥哥发现了被遮蔽的潮汐数据。",
               ["查清哥哥的死亡", "让维修工不再为系统错误背锅", "保住工会的集体谈判权"],
               ["找到沉港第三闸门的机械日志", "组织码头工人拒绝替天幕擦掉现场", "协助进入深海档案站"],
               ["维修工安全", "机械日志", "工人集体行动"],
               ["工会被财团控制", "队员需要工资养家", "他不相信林渡会承认顾家和天幕的共同责任"],
               "用现场劳动和工人网络验证每一个抽象数据，不接受只在屏幕上成立的真相。",
               "粗粝、幽默、耐心很长，遇到牺牲工人时极易冲动。",
               "把哥哥的潜水表拆成零件，只有在确认一个人安全回岸时才重新装回。",
               "知道第三闸门有机械日志，不知道日志被拆成了两种互相矛盾的时间制。",
               ["以为集体行动天然正义", "低估公开证词会把工会成员推到彼此对立"],
               "从只想替哥哥讨命的潜水员，成长为能让工人参与制度设计而不是只在危机中被动牺牲的组织者。",
               ["在封港时带工人用手动阀救下货船", "把自己的哥哥违规潜水记录交给审计", "拒绝用林渡的权限替工会做决定"],
               "负责公共闸门维护联盟，保留潜水资格但不再受任何单一机构雇佣。"),
    character("CHAR.jian_ning", "简宁", "记忆司法厅检察官、记忆法起草人",
               "简宁曾经相信记忆法能保护灾害幸存者免受二次伤害，直到她发现法律的删除条款被用来保护财团。",
               ["保住记忆证据的法律效力", "查明谁把例外条款变成了常规工具", "不让审判变成另一种删改"],
               ["追回被封存的庭审记录", "让天幕接受公开司法审查", "在终局保存被告和受害者的完整陈述"],
               ["法律程序", "证词保全", "公众审判"],
               ["她签过早期授权", "司法厅可以撤销她的执业资格", "不能用非法取得的记忆作为唯一证据"],
               "把每个超大型阴谋拆成一个法庭能验证的时间、权限和责任节点。",
               "克制、尖锐、对煽情不耐烦，内疚时会更严格地要求证据。",
               "租住在法院旧档案楼，把没有结案的卷宗按天气分类。",
               "知道记忆法存在危险例外，不知道例外最初是为保护哪一批人。",
               ["以为程序本身会自动纠偏", "低估受灾者对司法厅的恐惧"],
               "从系统里的修补者，成长为承认法律曾被自己参与塑形、并推动公开重写的人。",
               ["在听证会上承认自己签过有害条款", "拒绝删除被告不利但合法的记忆证据", "终局让审判记录不可由单一检察官关闭"],
               "辞去检察官，主持独立记忆证据法庭。"),
    character("CHAR.gu_wangchuan", "顾妄川", "天幕控灾集团继承人、白噪塔项目董事",
               "顾妄川从小接受的教育是灾害中必须有人替大多数人做残酷决定。沉港后，他接手顾家，却逐渐发现父亲把林渡当替罪羊是为了掩盖系统无法预测的根本缺陷。",
               ["证明集中决策能减少总体死亡", "保住顾家和天幕的控制权", "让妹妹留下的记忆不被抹除"],
               ["夺回九份失败记录", "把雁回社区纳入统一安置", "在林渡公开前控制叙事"],
               ["模型稳定性", "董事会", "妹妹顾遥的失踪记录"],
               ["顾家与事故有真实利益关系", "董事会能冻结他的权限", "他不能让妹妹的原始记忆曝光"],
               "先用一次真实有效的救援证明集中系统的价值，再把反对者逼进无法承受的选择。",
               "礼貌、理性、习惯把残酷说成统计学，遇到妹妹的声音会失去计算节奏。",
               "每天凌晨重跑一次妹妹失踪前的天气模型。",
               "知道天幕会删改记忆，不知道父亲当年曾删除过一条能救林渡的预警。",
               ["把林渡的复仇看成可预测刺激", "认为许见星可以被病人安置问题收买"],
               "从坚信秩序高于选择的继承人，成长为承认无法量化的人也属于安全，并亲手拆掉家族中枢。",
               ["用一次完美救援压住全城质疑", "公开顾家删改记录", "终局关掉顾家持有的最高权限"],
               "作为天幕改写案关键被告受审，失去继承权但保留公开模型审计资格。"),
    character("CHAR.gao_wanqing", "高晚晴", "沉港档案修复师、雁回社区失踪人口志愿记录员",
               "高晚晴负责把灾害后的生活物件重新登记入档，她发现很多死亡证明与家属手里的生活痕迹对不上，因此私下建立了被注销者档案。",
               ["让物件和名字重新对应", "保护档案不被当成商业数据", "找到弟弟高砚的真实下落"],
               ["修复九份失败记录的物理载体", "把被注销居民的档案交给独立机构", "协助定位白噪塔主机"],
               ["档案完整性", "家属信任", "物证链"],
               ["她没有执法权", "每次移动物证都会破坏原始状态", "弟弟可能就在天幕系统里工作"],
               "让每件物品先有主人和时间，再让它进入叙事，不接受只写结论的证据。",
               "安静、细密、对大人物不敬，情绪越强越会去擦一件物品。",
               "保存一只烧焦的儿童鞋，鞋带上有她弟弟的修补结。",
               "知道失踪名单被修改，不知道修改者留下了一个反向编号。",
               ["以为档案只要完整就会自动说话"],
               "从被动修复记录的人，成长为设计公共证据保管规则的档案架构师。",
               ["用一箱生活物件拆穿一份集体死亡证明", "把弟弟可能涉案的记录交给简宁", "终局拒绝把档案交给任何英雄个人保管"],
               "主持雁回公共记忆站的物证库。"),
    character("CHAR.lin_qiu", "蔺秋", "天幕潮汐模型工程师、顾妄川的旧同事",
               "蔺秋曾与林渡共同设计潮汐模型，事故后她选择留下并修补系统，因为她相信废掉模型只会让更多人死。",
               ["让模型真正承认未知", "不再为删减错误数据签字", "阻止内部激进派制造可控灾害"],
               ["找出模型被删除的变量", "把真实误差交给公众", "帮助顾妄川关闭核心站"],
               ["模型可解释性", "工程团队", "未知变量"],
               ["她的签名在旧案里出现", "内部权限被收回", "不懂如何面对林渡的指责"],
               "用对照实验和误差公开迫使所有人承认模型不能代表人。",
               "理性、疲惫、对自己的正确很不放心。",
               "养一盆只在低潮时开花的盐生植物，把每次开花日期写进模型日志。",
               "知道模型删掉过少数人的选择变量，不知道是谁要求删掉。",
               ["以为留下修补系统就能减轻自己的责任"],
               "从维护错误系统的工程师，成长为让系统必须公开承认不知道什么的人。",
               ["公开自己签过的错误版本", "在核心站主动关闭一条能保住自己职位的预测链", "把模型拆成多个公共模块"],
               "负责公共灾害模型的误差审计。"),
]

factions = [
    entity("FACTION.tianmu", "FACTION", "天幕控灾集团", {
        "type": "灾害预测、安置与记忆技术财团", "goal": "用集中预测和记忆法控制灾害叙事与资源分配",
        "internal_conflict": "顾妄川想修补系统，董事会想把错误全部转为个人罪责",
        "resources": ["潮汐模型", "白噪塔", "安置许可", "记忆法接口"], "provenance_refs": ["DESIGN.originalized_adaptation"],
    }, "CANON"),
    entity("FACTION.yanhui", "FACTION", "雁回互助站", {
        "type": "医生、档案师、工人和被注销居民组成的民间网络", "goal": "保住身体、名字、证据和社区选择权",
        "internal_conflict": "有人想以证据换安置，更多人拒绝继续被代表",
        "resources": ["急救站", "生活物证", "社区船", "证人网络"], "provenance_refs": ["DESIGN.originalized_adaptation"],
    }, "CANON"),
    entity("FACTION.tide_union", "FACTION", "潮线工会", {
        "type": "港口潜水、维修和运输工人的集体组织", "goal": "让维修责任和灾害决策不再由基层单独承担",
        "internal_conflict": "工资、生存和公开作证互相冲突", "resources": ["手动闸门", "工人日志", "潜水队"],
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }, "CANON"),
    entity("FACTION.memory_court", "FACTION", "记忆司法厅", {
        "type": "负责记忆证据认证和删除授权的司法机构", "goal": "维持记忆证据的法律效力", "internal_conflict": "简宁和上层对删除例外的解释相反",
        "resources": ["庭审记录", "删除授权", "证词保全室"], "provenance_refs": ["DESIGN.originalized_adaptation"],
    }, "CANON"),
]

locations = [
    ("LOC.yanhui", "雁回旧城", "被海堤和拆迁线夹住的老社区"),
    ("LOC.first_gate", "第一潮门", "沉港事故的旧闸门与潮线工人维修区"),
    ("LOC.memory_court", "记忆司法厅地下库", "存放被封存庭审和删除授权的冷库"),
    ("LOC.skyline_archive", "天幕天际档案楼", "财团保存模型与失踪人口数据的高层档案楼"),
    ("LOC.deepsea_station", "深海观测站", "九份失败记录最初被拆分的海底设施"),
    ("LOC.white_noise", "白噪塔", "能够把个人记忆转写为公共档案或删除指令的旧监狱"),
    ("LOC.orbit_relay", "天穹气象中继站", "终局风暴和全城记忆接口的共同节点"),
]
locations = [entity(i, "LOCATION", n, {"type": d, "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON" if i != "LOC.orbit_relay" else "PLAN") for i, n, d in locations]

rules = [
    entity("RULE.memory_edit", "RULE", "记忆删除授权规则", {"rule": "删除只能保护未成年人和正在审理的证人，不能替财团消除责任；任何删除都必须留下可复核的空洞编号。", "ceiling": "不能凭空创造新记忆", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON"),
    entity("RULE.tide_window", "RULE", "潮汐窗口规则", {"rule": "每次海堤大修只有四十分钟安全窗口，错过窗口就会把维修区变成封闭水域。", "ceiling": "没有工程权限也不能跳过潮汐时间", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON"),
    entity("RULE.failure_protocol", "RULE", "九份失败记录规则", {"rule": "每份记录只能证明一种系统失败，启用后会公开持有者一项违规或隐瞒；九份合并只产生公开审计入口，不产生个人统治权。", "ceiling": "记录不能替代证人和现场", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON"),
    entity("RULE.public_recall", "RULE", "公共记忆召回规则", {"rule": "被删除的记忆只有在三类独立证据、本人或家属确认、以及公开审计同时成立时才能召回。", "ceiling": "召回会恢复痛苦，任何人不得替本人决定是否观看", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "PLAN"),
]

props = [
    entity("PROP.dead_list", "PROP", "沉港死亡名单", {"function": "记录官方认定的三万人死亡与失踪", "hidden_problem": "名单中有活着的人，也缺少没有身份的死者", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON"),
    entity("PROP.nine_failure_logs", "PROP", "九份失败记录", {"function": "记录九次系统在不同条件下如何伤害普通人", "hidden_cost": "每启用一份就公开持有者的一项违规", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON"),
    entity("PROP.anchor_watch", "PROP", "锚潮旧表", {"function": "保存第一潮门机械时间和人工维修记录", "owner_history": ["周止戈哥哥", "周止戈"], "provenance_refs": ["DESIGN.originalized_adaptation"]}, "CANON"),
    entity("PROP.redacted_voice", "PROP", "顾遥未播语音", {"function": "证明顾妄川的妹妹曾拒绝被系统代表", "current_state": "被切成七段，散落在不同权限层", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "PLAN"),
    entity("PROP.public_recall_key", "PROP", "公共召回钥", {"function": "启动全城记忆审计，不替公众作出结论", "current_state": "需要九份失败记录和三类证据共同授权", "provenance_refs": ["DESIGN.originalized_adaptation"]}, "PLAN"),
]

volumes = [
    entity("VOLUME.return_city", "VOLUME", "第一卷·雁回归潮", {
        "chapter_start": 1, "chapter_end": 12,
        "detailed_plot": "林渡从白噪塔释放回到雁回旧城，正撞上天幕以安全安置为名拆除急救站。他先用工程权限救下一批被注销居民，再与许见星、周止戈、简宁建立互不信任的证据链。第一卷不急着证明林渡无罪，而是让他承认自己当年签过关闭闸门的建议，并从死亡名单中找到一个正在与他们对话的人。",
        "central_conflict": "雁回居民需要现实的医疗和居住空间，天幕要用快速安置换取居民放弃原始记忆与社区组织权。",
        "turning_points": ["林渡公开归来并被现场拘捕", "许见星拒绝删掉病人隐私换药", "第一潮门机械日志证明事故前存在第三道指令", "死亡名单中的活人现身"],
        "payoff": "雁回急救站暂时保住，第一份失败记录和第一段空洞编号进入三方保全；林渡的旧罪没有洗清。",
        "next_hook": "活人名单上的老人说，自己的记忆曾在记忆司法厅地下库被看见。",
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }),
    entity("VOLUME.law_of_names", "VOLUME", "第二卷·失名之城", {
        "chapter_start": 13, "chapter_end": 24,
        "detailed_plot": "林渡一行进入记忆司法厅和天际档案楼，追查空洞编号的法律来源。他们发现天幕并非简单篡改名单，而是把没有资格进入救援模型的人从法律上变成不存在。简宁面对自己参与起草的删除例外，顾妄川用一次真实有效的救援反击舆论，许见星则让被注销者在公开听证中自己讲出生活。",
        "central_conflict": "司法程序要保护证人隐私，受灾者却必须公开身份才能阻止自己再次被删除。",
        "turning_points": ["简宁承认删除条款由她签批", "顾妄川救下一列被放弃的列车", "高晚晴用生活物件拆穿集体死亡证明", "林渡确认自己曾隐瞒第三方案"],
        "payoff": "第二、三份失败记录被追回，记忆法第一次被法院暂缓适用；林渡公开一项让公众更不信任他的隐瞒。",
        "next_hook": "三份记录都指向深海观测站，而顾遥的语音第一次出现。",
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }),
    entity("VOLUME.deepsea_failure", "VOLUME", "第三卷·深海九错", {
        "chapter_start": 25, "chapter_end": 36,
        "detailed_plot": "潮线工会带队进入深海观测站，寻找剩余六份失败记录。九份记录分别对应潮汐预测、医疗排序、航线调度、记忆删除、安置合同、模型误差和公开授权。顾妄川被董事会剥夺继承权，蔺秋承认模型确实删掉了无法量化的选择，深海站却在归墟风暴中开始自毁。",
        "central_conflict": "毁掉深海站可以阻止天幕夺回记录，却会让未来城市再也无法验证事故；保住记录则可能把风暴引入避难区。",
        "turning_points": ["九份记录被确认是分权设计而非能力宝库", "顾妄川公开顾家删除日志", "蔺秋发现模型误差被人为收窄", "林渡承认自己当年为保住多数人隐瞒过第三方案"],
        "payoff": "九份记录集齐，公共召回钥出现；所有核心角色都留下可被审判的责任，林渡不再是唯一调查人。",
        "next_hook": "天穹气象中继站把全城记忆接口接入下一场风暴，召回钥需要全城共同授权。",
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }),
    entity("VOLUME.white_noise_trial", "VOLUME", "第四卷·白噪终局", {
        "chapter_start": 37, "chapter_end": 48,
        "detailed_plot": "全城风暴逼近，天幕要求林渡成为唯一记忆管理员，以最快速度删掉恐慌和责任争议。林渡与许见星、简宁、周止戈、顾妄川分别守住医疗、法律、闸门、模型和召回证据，发现白噪塔保存的不是单一主机，而是每个受灾者都能否决一次召回的公共协议。终局不靠杀死顾妄川，而靠让所有人看到完整事故并共同决定以后如何记住。",
        "central_conflict": "最快的集中记忆方案可以减少短期恐慌，却会永久剥夺个人叙述；缓慢的公共召回可能让城市先承受一场无法被控制的集体痛苦。",
        "turning_points": ["林渡被要求独占召回钥", "盟友公开否决英雄方案", "顾妄川关闭家族最高权限", "许见星把最终观看权交还给每个证人"],
        "payoff": "白噪塔关闭删除功能，完整责任链公开，天幕被拆成公共灾害网络；林渡承认责任后失去执照，但不再替死者发言。",
        "next_hook": "新制度第一次面对没有主角能单独解决的普通风暴。",
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }),
]

lines = [
    entity("LINE.names", "LINE", "被注销者回名线", {"owner": "CHAR.xu_jianxing", "goal": "让被系统删除的人重新获得可验证的身份", "pressure": "证人公开会失去安置和隐私", "opposing_force": "FACTION.tianmu与记忆删除授权", "milestones": ["急救站保全", "公开听证", "深海记录回收", "公共召回"], "closure_condition": "名字、证据和决定权都回到本人或家属手中", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
    entity("LINE.engineer_guilt", "LINE", "林渡责任线", {"owner": "CHAR.lin_du", "goal": "查清沉港并承认自己的真实责任", "pressure": "公众只接受洗白或处决两种叙事", "opposing_force": "顾家旧案与林渡自己的隐瞒", "milestones": ["回港", "确认第三方案", "公开签批", "终局受审"], "closure_condition": "责任链公开且林渡不再拥有单独豁免", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
    entity("LINE.central_model", "LINE", "集中模型线", {"owner": "CHAR.gu_wangchuan", "goal": "证明集中预测能减少死亡", "pressure": "模型误差被内部利益掩盖", "opposing_force": "CHAR.lin_qiu与公共审计", "milestones": ["完美救援", "误差公开", "核心站失控", "拆分模型"], "closure_condition": "模型公开、误差可审计、无单一中枢", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
    entity("LINE.community_trust", "LINE", "盟友信任线", {"owner": "CHAR.xu_jianxing", "goal": "让联盟不是主角私人班底而是互相否决的公共组织", "pressure": "每次亮底牌都会让盟友更依赖也更害怕林渡", "opposing_force": "英雄崇拜与旧创伤", "milestones": ["拒绝独断", "共同保全", "公开否决", "轮值制度"], "closure_condition": "终局后机构仍能在没有林渡时运行", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
]

promises = [
    entity("PROMISE.dead_list_living", "PROMISE", "死亡名单中的活人", {"creation_event": "EVENT.return_to_yanhui", "maturity_condition": "活人必须在不交出全部隐私的情况下完成身份复核", "reveal_window": "第一卷末", "payoff_event": "EVENT.dead_list_reversal", "who_knows": ["CHAR.gao_wanqing"], "who_misunderstands": ["CHAR.lin_du", "CHAR.gu_wangchuan"], "reinforcement_events": ["EVENT.return_to_yanhui"], "choices_affected": ["CHAR.xu_jianxing"], "post_payoff_state": "名单被证明同时删除了死者和活人", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
    entity("PROMISE.third_option", "PROMISE", "林渡隐瞒的第三方案", {"creation_event": "EVENT.archive_truth", "maturity_condition": "林渡必须公开当年签批和未执行方案", "reveal_window": "第二卷末至第三卷", "payoff_event": "EVENT.deepsea_reveal", "who_knows": ["CHAR.lin_du"], "who_misunderstands": ["CHAR.xu_jianxing", "CHAR.jian_ning"], "reinforcement_events": ["EVENT.return_to_yanhui", "EVENT.archive_truth"], "choices_affected": ["CHAR.lin_du", "CHAR.xu_jianxing"], "post_payoff_state": "主角不再拥有单纯受害者位置", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
    entity("PROMISE.guyao_voice", "PROMISE", "顾遥未播语音", {"creation_event": "EVENT.model_split", "maturity_condition": "顾妄川必须先关闭一项能保住自己权力的模型", "reveal_window": "第三卷末至第四卷", "payoff_event": "EVENT.family_shutdown", "who_knows": ["CHAR.gu_wangchuan", "CHAR.lin_qiu"], "who_misunderstands": ["CHAR.lin_du"], "reinforcement_events": ["EVENT.model_split", "EVENT.family_shutdown"], "choices_affected": ["CHAR.gu_wangchuan"], "post_payoff_state": "顾妄川承认妹妹拒绝被任何模型代言", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
    entity("PROMISE.public_recall", "PROMISE", "公共召回钥", {"creation_event": "EVENT.deepsea_reveal", "maturity_condition": "九份记录、三类证据和受灾者共同授权", "reveal_window": "第四卷", "payoff_event": "EVENT.public_recall", "who_knows": ["CHAR.lin_du", "CHAR.xu_jianxing"], "who_misunderstands": ["CHAR.gu_wangchuan", "FACTION.tianmu"], "reinforcement_events": ["EVENT.deepsea_reveal", "EVENT.public_recall"], "choices_affected": ["CHAR.lin_du", "CHAR.xu_jianxing", "CHAR.jian_ning"], "post_payoff_state": "召回不再属于个人，观看与否由本人决定", "status": "ACTIVE", "provenance_refs": SOURCE}, "PLAN"),
]

events = [
    ("EVENT.return_to_yanhui", "林渡回到雁回旧城", "CHAR.lin_du", 1, "LOC.yanhui", "林渡以释放者身份回到拆迁线，先救人再找档案。", "雁回急救站获得短暂封存，林渡公开回港。", "EVENT.dead_list_reversal", ["CHAR.xu_jianxing", "FACTION.tianmu"]),
    ("EVENT.dead_list_reversal", "死亡名单反转", "CHAR.gao_wanqing", 12, "LOC.yanhui", "高晚晴用生活物件证明名单中的一名死者仍在社区。", "死亡名单被确认存在系统性错位。", "EVENT.archive_truth", ["CHAR.xu_jianxing", "CHAR.gao_wanqing"]),
    ("EVENT.archive_truth", "记忆司法厅承认删除例外", "CHAR.jian_ning", 24, "LOC.memory_court", "简宁公开自己签过的删除条款，并把封存庭审交给独立保全。", "记忆法首次被暂缓，林渡的第三方案被重新提起。", "EVENT.deepsea_reveal", ["CHAR.lin_du", "CHAR.jian_ning"]),
    ("EVENT.deepsea_reveal", "深海九份记录合流", "CHAR.zhou_zhige", 36, "LOC.deepsea_station", "工会在深海观测站保住九份失败记录和公共召回钥。", "召回钥需要群体授权而不是个人签名。", "EVENT.model_split", ["CHAR.lin_du", "CHAR.zhou_zhige"]),
    ("EVENT.model_split", "天幕模型误差公开", "CHAR.lin_qiu", 40, "LOC.orbit_relay", "蔺秋公开被删掉的未知变量，顾妄川失去董事会支持。", "集中模型被迫接受公开误差审计。", "EVENT.family_shutdown", ["CHAR.gu_wangchuan", "CHAR.lin_qiu"]),
    ("EVENT.family_shutdown", "顾妄川关闭家族权限", "CHAR.gu_wangchuan", 43, "LOC.orbit_relay", "顾妄川关闭顾家最高权限，释放顾遥的完整语音。", "天幕失去单一总控，但风暴进入不可预测状态。", "EVENT.public_recall", ["CHAR.lin_qiu", "CHAR.lin_du"]),
    ("EVENT.public_recall", "全城公共记忆召回", "CHAR.xu_jianxing", 47, "LOC.white_noise", "许见星把观看权交还给每个证人，白噪塔停止删除。", "受灾者重新获得叙述权，责任链进入公开审判。", "EVENT.final_audit", ["CHAR.lin_du", "CHAR.xu_jianxing"]),
    ("EVENT.final_audit", "白噪归航公开审计", "CHAR.lin_du", 48, "LOC.white_noise", "林渡公开全部责任并放弃独占权限，公共灾害网络成立。", "旧秩序被拆解，新的制度必须在没有救世主的情况下运行。", "FACTION.yanhui", ["CHAR.jian_ning", "CHAR.gu_wangchuan"]),
]

event_entities = []
event_edges = []
for event_id, name, actor, time_index, location, action, delta, output, participants in events:
    input_ref = "PROP.nine_failure_logs" if time_index > 1 else "PROP.dead_list"
    event_entities.append(entity(event_id, "EVENT", name, {
        "active_actor": actor, "causal_inputs": [input_ref], "causal_outputs": [output],
        "action": action, "state_delta": delta, "time_index": time_index, "time_window": f"第{time_index}个关键节点",
        "location": location, "line_refs": ["LINE.names", "LINE.engineer_guilt"], "requires_hyperedge": True,
        "provenance_refs": ["DESIGN.originalized_adaptation"],
    }))
    event_edges.extend([
        {"id": f"PART.{event_id}.a", "type": "PARTICIPATES_IN", "source": actor, "target": event_id, "payload": {"role": "initiator"}},
        {"id": f"PART.{event_id}.b", "type": "PARTICIPATES_IN", "source": participants[0], "target": event_id, "payload": {"role": "target"}},
    ])
for index in range(len(events) - 1):
    event_edges.append({"id": f"CAUSES.{index + 1}", "type": "CAUSES", "source": events[index][0], "target": events[index + 1][0], "payload": {"reason": "前一节点改变下一节点的资源、信息或权限"}})

chapter_records = [
    rec(1, "VOLUME.return_city", "白噪塔外的回港者", ["CHAR.lin_du", "CHAR.xu_jianxing"], "LOC.yanhui", "建立归来者与社区的第一次正面冲突", "保住雁回急救站的三小时封存", "FACTION.tianmu", "天幕要立刻拆站，林渡要保住病人和证据，两者都不能先交出身份", "病人会被分散，旧档案会被装进无名箱", "白噪塔释放令将林渡送到拆迁线", ["林渡穿过封锁线检查急救站的备用电源", "许见星把病床和病历一起推到封锁线前拒绝交接", "林渡用旧阀门拖延潮门关闭而不是攻击执法队", "他发现拆迁设备接入的是白噪塔接口", "林渡公开释放封记录，承认自己没有顾家继承权", "船钟响三次，第一潮门的机械日志正在被远程读取"], ["港安队按高风险名单搜身", "天幕律师拿产权文件压住病人隐私", "潮门提前关阀切断撤离路线", "白噪塔系统要求公开林渡狱中违规", "顾妄川远程冻结封存权限", "天幕宣布第一潮门出现异常"], "拆迁设备接入白噪塔而非普通电源", "许见星第一次把林渡当作需要被约束的变量", "林渡选择公开自己的违规而不是删掉日志", "他失去恢复工程执照的可能", "急救站暂保三小时，调查入口从拆迁转向第一潮门", "第一潮门的机械日志正在被远程读取", ["先保住急救站现场", "确认接口来源", "把局部胜利转成调查入口"], ["现场控制权转移", "旧接口暴露", "船钟钩子成立"], ["病人需要转移", "林渡暴露身份", "顾妄川获得他的追踪位置"], ["急救站暂时封存", "所有人进入潮门调查", "下一章必须追日志"], ["产权程序", "工程权限", "公开身份"], ["急救站外围", "地下配电室", "潮门控制台"], ["强拆倒计时", "病人无处转移", "林渡要确认接口"], ["完成产权交接", "切断备用电源", "锁死潮门"], ["病人失去药品和证据", "接口箱被带走", "机械日志被覆盖"], [["查电源", "搬病床"], ["接线", "抢存储"], ["封存", "识别船钟"]], ["许见星夺回现场指挥", "林渡公开第一条违规", "第一潮门成为下一入口"], [["资源", "关系"], ["证据", "合法性"], ["权限", "时间"]], ["LINE.names", "LINE.community_trust"]),
    rec(2, "VOLUME.return_city", "被注销的病床", ["CHAR.xu_jianxing", "CHAR.gao_wanqing"], "LOC.yanhui", "让医疗冲突具体化为身份冲突", "在药品断供前证明三名病人仍有合法生活记录", "FACTION.tianmu", "医院愿意供药但要求病人交出记忆授权，互助站拒绝用隐私换生存", "三名重症病人会在夜潮前失去药物", "急救站封存后药品供应被切断", ["许见星把病人服药时间写进公共黑板", "高晚晴用病人家中的旧收音机核对身份", "天幕送来足量药物却附带记忆授权", "两人发现三人的死亡编号属于同一批次", "许见星拒签授权，选择让社区船冒险取药", "药箱里多出一张写着林渡名字的注销单"], ["药品必须绑定实名身份", "天幕冻结社区船燃料", "旧收音机的时间与官方记录冲突", "编号批次指向第一潮门", "有人把林渡列为已死亡", "潮汐警报提前"], "三名病人的死亡编号来自同一批次", "高晚晴确认被注销者不止一人", "许见星让病人自己决定是否公开病历", "急救站失去官方药品配给资格", "三名病人进入互助船，编号线索指向第一潮门", "药箱中的注销单证明林渡曾被系统判死", ["保住病人生命", "核对生活记录", "带着编号进入潮门"], ["病历黑板公开", "编号批次反转", "林渡死亡单出现"], ["药品供应被切断", "身份核验失败", "社区船承担风险"], ["病人愿意公开一项记录", "编号指向潮门", "林渡不得不面对死亡身份"], ["医疗配给", "物证核验", "夜潮转移"], ["急救站", "高晚晴的物证桌", "社区船码头"], ["病人药品只够一夜", "证据会泄露隐私", "社区船可能被拦截"], ["交出授权", "替病人决定", "等官方药品"], ["失去隐私", "失去药物", "失去合法身份"], [["贴标签", "核对收音机"], ["拆授权", "偷换药箱"], ["装船", "遮住死亡单"]], ["许见星拒绝替病人签字", "高晚晴找到生活时间", "林渡死亡单成为私人钩子"], [["身体", "证据"], ["隐私", "路径"], ["身份", "追捕"]], ["LINE.names", "LINE.community_trust"]),
    rec(3, "VOLUME.return_city", "第一潮门的手动阀", ["CHAR.lin_du", "CHAR.zhou_zhige"], "LOC.first_gate", "让工程与工会线相遇", "在四十分钟潮汐窗口内打开被天幕锁死的手动阀", "FACTION.tianmu", "林渡需要机械日志，周止戈要先救被困维修工，时间只够做一件事", "阀门不打开，四名工人会被困在水下检修井", "死亡编号和船钟都指向第一潮门", ["周止戈带林渡下井查看手动阀", "林渡发现天幕远程锁与机械锁互相冲突", "周止戈先割断自己的安全绳救队员", "林渡用观测协议读出两套潮汐时间", "机械日志显示哥哥死前按过第三次手动阀", "远程指令要求他们留下日志撤离"], ["潮水提前九分钟", "队员安全绳缠住阀杆", "天幕封闭检修井", "两套时间制无法同时成立", "周止戈拒绝放弃最后一名工人", "远程指令把他们标成违规入侵"], "机械时间比系统时间早九分钟", "周止戈哥哥不是违规潜水，而是在执行被删掉的第三指令", "林渡用身体卡住阀杆让周止戈先救人", "他的神经旧伤在水下回放中复发", "第一潮门打开，日志保存但顾妄川得到工会坐标", "日志上出现第三道指令的手写补丁", ["救工人", "保存日志", "证明第三指令"], ["下井", "手动救人", "对照两套时间"], ["潮水倒灌", "阀门不动", "远程锁死"], ["工人获救", "日志留下补丁", "林渡身体恶化"], ["潜水", "机械维修", "时间证据"], ["第一潮门井口", "水下阀室", "手动控制台"], ["阀门四十分钟后失效", "四名工人被困", "日志会被水毁"], ["关闭水闸", "割断安全绳", "保存日志"], ["失去一个安全出口", "工人脱离队伍", "林渡暴露伤情"], [["下井", "测潮"], ["割绳", "拖阀"], ["抄录", "传回日志"]], ["周止戈先救人", "林渡承认旧伤", "第三指令出现"], [["身体", "资源"], ["信息", "时间"], ["权限", "关系"]], ["LINE.engineer_guilt", "LINE.names"]),
    rec(4, "VOLUME.return_city", "顾家的救援合同", ["CHAR.lin_du", "CHAR.gu_wangchuan"], "LOC.yanhui", "让对手展示真实能力与真实目标", "阻止顾妄川用一份高效救援合同接管雁回安置", "FACTION.tianmu", "合同能救出多数居民却要求少数被注销者放弃追诉", "签字能换药和住房，不签字会让社区进入夜潮危险区", "第一潮门日志暴露顾家旧合同", ["顾妄川带来一支真正能救人的临时队伍", "林渡发现合同把居民分成可计算和不可计算两组", "许见星要求把未登记病人列入安置", "顾妄川承认合同沿用父亲的事故模板", "林渡把自己列入不可安置名单", "合同底页出现顾遥的旧签名"], ["安置船只只够七成", "名单格式无法加入无身份者", "董事会远程撤回药品", "顾妄川被迫选择是否违约", "林渡的名字触发自动驱逐", "顾遥签名没有日期"], "顾家救援合同沿用沉港事故模板", "顾妄川并非只想拆站，他在和董事会抢时间", "林渡让自己成为合同里的第一名被放弃者", "雁回失去一半安置名额", "顾妄川暂缓接管并留下底页", "顾遥签名说明她曾反对顾家删改", ["保护居民", "逼对手承认合同代价", "拿到底页"], ["合同宣读", "名单重排", "违约争执"], ["安置名额不足", "无身份者被排除", "林渡触发驱逐"], ["居民知道顾家合同", "顾妄川获得底页", "董事会准备强制执行"], ["合同谈判", "名单审计", "董事会远程控制"], ["雁回广场", "临时安置船", "急救站门口"], ["多数居民能走", "少数人必须留下", "顾妄川的职位会被撤"], ["签约", "改名单", "公开顾家模板"], ["放弃部分居民", "放弃家族控制", "失去安置资格"], [["宣读合同", "逐人核验"], ["重排座位", "堵住船门"], ["投影底页", "拦下执行队"]], ["林渡把自己放进弃置名单", "顾妄川第一次违约", "顾遥签名出现"], [["关系", "资源"], ["信息", "身份"], ["政治", "选择"]], ["LINE.engineer_guilt", "LINE.community_trust"]),
    rec(5, "VOLUME.return_city", "三次敲钟", ["CHAR.gao_wanqing", "CHAR.lin_du"], "LOC.yanhui", "把死亡名单变成可追查的物证谜题", "在旧城被清空前找到三次敲钟对应的活人编号", "FACTION.tianmu", "高晚晴想保住全部物件，林渡只想拿到能证明时间的那一件", "物件仓库会在日落前焚毁", "顾遥签名把线索指向旧城档案仓", ["高晚晴按船票、鞋子和门牌排列物件", "林渡发现三次船钟对应三种删除权限", "天幕安保把仓门封死", "高晚晴决定先救一只装着儿童鞋的箱子", "林渡用释放封制造三分钟盲区", "箱底藏着一个活人编号和反向箭头"], ["安保队切断仓门", "物件排序被水浸乱", "三种权限无法同屏", "高晚晴拒绝丢下儿童物件", "释放封只够一次", "反向箭头指向记忆司法厅"], "三次敲钟不是时间信号而是删除层级", "高晚晴弟弟的编号出现在箱底", "林渡先保护物件而不是复制数据", "释放封彻底失效", "箱子保住但高晚晴弟弟可能已涉案", "反向箭头指向记忆司法厅地下库", ["保住物证", "解读钟声", "追查弟弟"], ["排列物件", "守仓门", "制造盲区"], ["仓库焚毁", "物证错位", "安保封门"], ["儿童鞋保住", "活人编号出现", "司法厅成为入口"], ["档案修复", "权限解码", "火灾撤离"], ["物证仓", "旧城钟楼", "焚毁出口"], ["物件会被烧毁", "排序一错就失去时间", "高晚晴要面对弟弟"], ["复制数据", "救物件", "逃离仓门"], ["丢掉生活物件", "失去释放封", "公开家人线索"], [["排列船票", "核对门牌"], ["堵门", "搬箱"], ["烧毁前转移", "找到箭头"]], ["高晚晴选择物件", "林渡耗尽释放封", "弟弟编号出现"], [["证据", "身份"], ["资源", "关系"], ["时间", "悬念"]], ["LINE.names", "LINE.engineer_guilt"]),
    rec(6, "VOLUME.return_city", "急救站的听证", ["CHAR.xu_jianxing", "CHAR.jian_ning"], "LOC.yanhui", "让法律与社区证据发生正面冲突", "在不泄露病人隐私的前提下阻止急救站被判为非法设施", "FACTION.memory_court", "司法厅要求完整病历才能确认急救站合法，许见星拒绝把病人交给审查", "听证失败就会断供并清空站内病人", "记忆司法厅地下库线索要求先合法化急救站", ["简宁携带临时听证令到站", "许见星把病人隐私封箱并只展示用药时间", "司法厅要求观看患者记忆", "简宁发现删除条款被用于撤销医疗身份", "她承认自己参与过条款起草", "听证室屏幕出现第一份空洞编号"], ["病历不全无法认证", "患者拒绝作证", "观看授权被强制启动", "简宁可能被停职", "空洞编号污染听证记录", "天幕请求直接接管急救站"], "删除条款把医疗身份也纳入可撤销范围", "简宁是条款起草人之一", "许见星让病人决定展示哪段记忆", "急救站暂时失去官方认证", "空洞编号进入司法记录，听证被迫延期", "第一份空洞编号与林渡释放档案相同", ["保护隐私", "使急救站合法", "留下司法记录"], ["封存病历", "拆解条款", "对照空洞"], ["听证权限压迫", "供药中断", "简宁身份动摇"], ["病人做选择", "简宁公开责任", "空洞编号被记录"], ["医疗法庭", "记忆观看", "证据封存"], ["急救站听证室", "病历封存柜", "司法投影墙"], ["失去认证", "病人隐私曝光", "简宁职业受损"], ["拒绝观看", "只交时间", "公开条款"], ["断供", "停职", "扩大听证"], [["封箱", "问证人"], ["拆法条", "挡观看"], ["投影编号", "申请延期"]], ["病人掌握展示权", "简宁承认条款责任", "空洞编号进入案卷"], [["法律", "隐私"], ["信息", "合法性"], ["关系", "制度"]], ["LINE.names", "LINE.community_trust"]),
    rec(7, "VOLUME.return_city", "高架桥下的完美救援", ["CHAR.gu_wangchuan", "CHAR.lin_du"], "LOC.yanhui", "让反派用真实有效的救援争夺公众信任", "在顾妄川的完美救援直播中找出被模型遗漏的人", "FACTION.tianmu", "顾妄川救了大多数人，林渡若直接否认就会伤害真正获救者", "一场提前预警的桥体坍塌正在发生", "顾妄川的救援合同被听证记录传播", ["顾妄川提前清空高架桥", "林渡发现桥下有不在模型内的流浪家庭", "许见星阻止直播团队拍摄病人", "顾妄川关闭一条安全路线救少数人", "模型把少数人标成不可回收", "桥下出现顾遥的第二段语音"], ["直播需要完整画面", "模型忽略无身份者", "撤离路线只能开一条", "顾妄川的指挥权被董事会收回", "林渡必须公开反对一次成功救援", "语音要求不要替她解释"], "完美救援只覆盖登记人口", "顾妄川第一次主动违背模型", "林渡不否认救援成果而只指出被遗漏者", "公众开始把林渡视为抹黑救援的人", "顾遥语音要求不要替死者解释", "语音来自白噪塔项目董事权限层", ["确认遗漏者", "保护直播中的人", "拿到语音"], ["救援直播", "桥下排查", "路线争执"], ["桥体坍塌", "模型缺人", "公众情绪倒转"], ["少数人获救", "林渡失去口碑", "语音出现"], ["应急救援", "模型盲区", "舆论竞争"], ["高架桥", "桥下废站", "临时直播车"], ["救援总人数决定顾家声望", "遗漏者会被二次驱赶", "语音可能被删"], ["直播", "改路线", "公开遗漏者"], ["失去舆论", "失去董事会信任", "暴露语音来源"], [["清空桥面", "查桥下"], ["护住家庭", "关闭直播"], ["截取语音", "转移证人"]], ["顾妄川救少数人", "林渡承认救援有效", "语音要求不被代言"], [["舆论", "信息"], ["选择", "资源"], ["关系", "悬念"]], ["LINE.central_model", "LINE.names"]),
    rec(8, "VOLUME.return_city", "死亡名单上的高晚晴", ["CHAR.gao_wanqing", "CHAR.xu_jianxing"], "LOC.yanhui", "让高晚晴成为被追查的关键行动者", "在天幕宣布高晚晴已死亡后，让她的档案修复行为继续有效", "FACTION.tianmu", "高晚晴要保护物证库，天幕要用死亡身份冻结她的所有权限", "物证库会被判定为无主财产", "高晚晴弟弟编号出现，天幕开始追溯她的身份", ["高晚晴发现自己的身份证被注销", "许见星用病人陪诊记录证明她今天存在", "天幕律师要求陪诊记录也删除", "高晚晴把自己写进失踪人口物证库", "她承认弟弟可能替天幕工作", "物证库收到一份来自记忆司法厅的退回件"], ["身份系统拒绝高晚晴", "陪诊记录涉及病人隐私", "弟弟线索引来天幕追踪", "物证库拒绝收录活人", "她必须成为自己档案的证物", "退回件标着地下库编号"], "高晚晴本人也被系统判死", "她弟弟高砚可能参与修改名单", "高晚晴把自己作为证物登记", "她失去正常通行权", "退回件把所有线索推向地下库", "第一卷末地下库入口被确认", ["保住物证库", "保住自己的合法性", "进入地下库"], ["身份核验", "隐私对照", "自我登记"], ["通行权丢失", "病人信息危险", "弟弟追踪"], ["高晚晴成为自己的证物", "退回件出现", "地下库入口锁定"], ["身份审查", "档案登记", "地下入口"], ["物证库", "急救站", "司法厅退回站"], ["物证被判无主", "高晚晴无法正常通行", "地下库会暴露更大责任"], ["证明存在", "隐藏病人", "登记自己"], ["交出隐私", "失去身份", "打开地下库"], [["刷证", "调陪诊"], ["封箱", "登记"], ["拆退回件", "定位编号"]], ["高晚晴成为档案对象", "地下库入口锁定", "第一卷转入失名之城"], [["身份", "证据"], ["隐私", "路径"], ["悬念", "地图"]], ["LINE.names", "LINE.community_trust"]),
    rec(9, "VOLUME.return_city", "第一份失败记录", ["CHAR.lin_du", "CHAR.jian_ning"], "LOC.memory_court", "追回九份失败记录中的第一份", "在地下库取出失败记录而不破坏病人记忆证据", "FACTION.memory_court", "简宁要保证证据能进法庭，林渡要立刻读出记录里的私人记忆", "阅读方式不同会决定证据能否使用", "地下库入口已被高晚晴定位", ["简宁用法庭权限打开外层库", "林渡发现记录以受灾者的失败选择命名", "库内自动播放一段不属于案件的记忆", "简宁要求停止播放并先做时间戳", "林渡听见自己六年前的签名声", "第一份记录写着‘你们都同意了’"], ["库门只开十分钟", "记忆播放没有暂停键", "时间戳设备过热", "简宁拒绝非法取证", "林渡无法确认自己的声音", "库内水位上涨"], "失败记录不是技术报告而是被删除者的选择证言", "记录里出现林渡的声音", "林渡让简宁先保全证据，自己不读取完整内容", "他只能带走半份记录", "记录标题暗示很多受害者曾被迫同意", "地下库继续向更深层开放", ["取记录", "完成时间戳", "确认林渡声音"], ["开库", "封存播放", "撤离"], ["水位上涨", "设备过热", "声音污染"], ["半份记录保住", "简宁获得合法证据", "林渡无法洗清自己"], ["证据保全", "记忆观看", "水下撤离"], ["地下库外层", "证词冷库", "水淹走廊"], ["证据会损坏", "林渡可能听见不愿听的过去", "库门只开十分钟"], ["取出", "停止观看", "确认签名"], ["失去完整记录", "放弃私人真相", "暴露声音"], [["打开", "贴时间戳"], ["挡播放", "抢设备"], ["封袋", "涉水撤离"]], ["林渡放弃先听", "半份记录合法化", "‘你们都同意了’成为卷末钩子"], [["证据", "身体"], ["法律", "记忆"], ["时间", "悬念"]], ["LINE.engineer_guilt", "LINE.names"]),
    rec(10, "VOLUME.return_city", "没有人签字的同意", ["CHAR.xu_jianxing", "CHAR.lin_du"], "LOC.memory_court", "揭示删除同意并非真实同意", "在地下库二层找到被注销居民的集体授权原件", "FACTION.memory_court", "原件证明有人同意删除，但签名者身份全被抹去", "公开原件可能二次伤害幸存者，不公开则无法反驳天幕", "第一份失败记录提到强制同意", ["许见星找到一面没有名字的签字墙", "林渡按编号复原签字顺序", "简宁发现签字都来自同一台终端", "许见星拒绝把签字当作病人同意", "林渡用自己的狱中编号替代一个无名签字", "签字墙背后出现顾家付款记录"], ["签字没有名字", "终端时间被统一改写", "司法厅要求原件封存", "许见星拒绝替无名者解释", "林渡把自己的编号放进去", "付款记录会牵出顾家"], "集体授权由同一终端生成，不等于本人同意", "顾家曾为终端维护付费", "许见星让‘不知道’本身进入证据", "原件暂不能公开", "顾家付款记录成为第二条责任链", "顾妄川被迫进入地下库谈判", ["确认授权真假", "保护无名者", "保留顾家付款"], ["复原顺序", "核验终端", "封存原件"], ["公开会伤人", "原件被夺", "顾家责任上升"], ["无名者拥有未知状态", "付款记录保住", "顾妄川出现"], ["证据解释", "隐私保护", "利益链"], ["签字墙", "终端室", "付款档案室"], ["原件可能被封", "无名者被再度代言", "顾家责任浮出"], ["读顺序", "拒绝解释", "藏付款"], ["失去立即曝光", "增加顾家嫌疑", "引来顾妄川"], [["编号复原", "取终端"], ["护住墙", "封原件"], ["拆付款", "应对谈判"]], ["许见星保留不知道", "顾家付款出现", "顾妄川被迫谈判"], [["信息", "隐私"], ["法律", "责任"], ["关系", "资源"]], ["LINE.names", "LINE.engineer_guilt"]),
    rec(11, "VOLUME.return_city", "顾妄川的第二次违约", ["CHAR.gu_wangchuan", "CHAR.jian_ning"], "LOC.memory_court", "迫使顾妄川选择家族权限或合法证据", "在董事会远程封库前让顾妄川打开顾家付款档案", "FACTION.tianmu", "顾妄川可以保住继承权，也可以让林渡一行拿到证明顾家介入的原件", "封库后所有付款记录会自动转成匿名维护费", "付款档案室被顾家远程锁定", ["顾妄川要求只看付款记录不看受害者记忆", "简宁坚持所有权限操作都要留下审计", "董事会冻结顾妄川的继承席", "他用继承权限开库并当场放弃一票", "林渡看到顾家曾资助删除终端", "顾妄川把一段顾遥语音交给简宁"], ["董事会要求他关闭审计", "审计会暴露顾家", "继承权被冻结", "开库后他失去董事会支持", "林渡拒绝替他辩护", "顾遥语音无法播放"], "顾家为删除终端提供过维护资金", "顾妄川的继承席依赖一次不公开表决", "顾妄川亲手放弃一票打开档案", "失去继承权和董事会保护", "顾遥语音成为下一卷线索", "天际档案楼的模型索引被点亮", ["拿到付款", "记录顾家责任", "保住语音"], ["谈判", "审计开库", "继承表决"], ["远程锁库", "权限冻结", "语音损坏"], ["付款原件出库", "顾妄川失去继承席", "语音交给简宁"], ["公司权力", "法律审计", "家庭秘密"], ["付款档案室", "董事会远程厅", "地下播放室"], ["档案会匿名化", "顾妄川将失去身份", "语音可能只剩残片"], ["只开付款", "记录表决", "保护语音"], ["失去继承权", "公开顾家", "承担语音秘密"], [["谈判", "核权限"], ["开库", "签审计"], ["转语音", "挡远程锁"]], ["顾妄川放弃一票", "顾家责任成立一部分", "天际档案楼索引亮起"], [["权力", "法律"], ["责任", "家庭"], ["资源", "地图"]], ["LINE.engineer_guilt", "LINE.central_model"]),
    rec(12, "VOLUME.return_city", "活人名单的反转", ["CHAR.gao_wanqing", "CHAR.lin_du"], "LOC.yanhui", "完成第一卷公开回报并打开第二卷地图", "在全城发布会上证明死亡名单同时吞掉了死者和活人", "FACTION.tianmu", "官方只愿承认一名活人错误，互助站要证明这是系统规则而非偶然事故", "若发布失败，雁回会被整体判定为无效社区", "天际索引与高晚晴物证回到雁回", ["高晚晴把三只物证箱摆在发布台", "林渡用第一份失败记录对照死亡时间", "天幕只承认一个编号错误", "许见星让三名居民自己讲出被删除后的生活", "林渡公开自己当年签批过的关闭建议", "发布台名单上出现记忆司法厅地下库编号"], ["发布会只给十分钟", "物证无法证明系统意图", "天幕切断现场网络", "公众要求林渡先洗清自己", "林渡承认签批造成伤亡", "地下库编号指向失名之城"], "名单错误不是孤例，而是按模型资格批量发生", "林渡公开了自己的真实责任", "居民自己决定公开生活而非由主角代言", "林渡口碑跌入最低点", "第一卷责任链成立，第二卷进入记忆司法厅", "地下库编号指向失名之城", ["证明规则性错误", "让居民发声", "打开地下库路线"], ["摆物证", "对照名单", "公开责任"], ["网络被切", "观众质疑", "林渡自损"], ["三名居民被看见", "林渡承担旧罪", "地下库成为下一地图"], ["公开发布", "居民证词", "旧罪结算"], ["雁回发布台", "死亡名单投影墙", "撤离巷"], ["发布台会被切网", "居民会被二次暴露", "林渡必须承认责任"], ["摆物证", "读名单", "安排证词"], ["物证被质疑", "网络断开", "追兵进入"], [["摆箱", "校时"], ["断网", "护证人"], ["转移", "读取编号"]], ["居民获得发声权", "林渡公开签批", "第二卷地图打开"], [["证据", "舆论"], ["责任", "关系"], ["地图", "悬念"]], ["LINE.names", "LINE.engineer_guilt"]),
]

# The remaining chapters use the same explicit record shape, but each has a distinct
# local problem, reveal, choice, cost, and hook. They are intentionally data, not a
# generic chapter counter.
seed_specs = [
    (13, "失名之城", ["CHAR.lin_du", "CHAR.jian_ning"], "LOC.memory_court", "追回第二份失败记录", "删除法例外把证人变成无名", "地下库编号要求进入记忆司法厅", "签字原件被分成三种权限", "简宁的旧签批会被公开", "记忆司法厅允许只看不保存", "第二份记录藏在一份已结案判决里"),
    (14, "没有姓名的判决", ["CHAR.jian_ning", "CHAR.xu_jianxing"], "LOC.memory_court", "让一份无名判决重新拥有当事人", "法院只认判决不认生活证据", "无名判决是第二份记录的载体", "许见星找到病历上的重复手写", "公开病历会泄露患者", "判决被转入天幕备份", "备份里出现一列被删的儿童"),
    (15, "儿童名单的空白", ["CHAR.xu_jianxing", "CHAR.gao_wanqing"], "LOC.yanhui", "保护被删儿童的家属证词", "天幕用未成年人保护法冻结全部证人", "备份儿童名单指向雁回旧校", "高晚晴找到同一批鞋印", "家属拒绝被拍摄", "许见星公开一条自己的童年病历", "旧校地下有记忆转写机"),
    (16, "旧校的播放室", ["CHAR.gao_wanqing", "CHAR.lin_du"], "LOC.yanhui", "取出记忆转写机里的原始声音", "播放室会自动把听者写入责任人", "儿童鞋印打开旧校地下室", "林渡听到自己曾经建议删掉一段预警", "机器要求牺牲一份物证", "高晚晴选择烧掉弟弟的旧档案换设备", "顾妄川的救援直播覆盖全城"),
    (17, "一场成功的失败", ["CHAR.gu_wangchuan", "CHAR.lin_qiu"], "LOC.skyline_archive", "拆穿顾妄川救援数据里的删减", "数据证明所有人获救但没有记录谁被拒绝", "顾妄川直播覆盖了真实损失", "蔺秋发现模型把拒绝救援算成自主离开", "她必须公开自己的签名", "顾妄川第一次暂停直播", "第三份失败记录藏在模型误差表"),
    (18, "误差表上的人", ["CHAR.lin_qiu", "CHAR.jian_ning"], "LOC.skyline_archive", "让模型误差拥有证人而非只有数字", "法院只接受可重复误差不接受个人选择", "第三份记录需要模型工程师签名", "蔺秋交出一份被她删过的变量", "她失去模型权限", "简宁把误差表转成证据申请", "天幕开始追捕蔺秋"),
    (19, "追捕一个工程师", ["CHAR.lin_qiu", "CHAR.zhou_zhige"], "LOC.first_gate", "把蔺秋送过封锁的潮线", "潮线工会不愿接收天幕叛徒", "蔺秋的权限能打开一条维修通道", "周止戈要求她先承认删变量", "工会成员会失去工资", "蔺秋在工人面前公开错误", "第一潮门再次收到假警报"),
    (20, "假警报", ["CHAR.zhou_zhige", "CHAR.lin_du"], "LOC.first_gate", "证明假警报来自记忆接口而非潮汐", "工人要撤离，林渡要留在阀室核验", "蔺秋公开变量后系统反扑", "林渡发现警报让工人忘记谁发令", "周止戈必须选择救人还是留证", "他把哥哥旧表交给林渡", "第四份失败记录在潮门底部"),
    (21, "哥哥没有死在水里", ["CHAR.zhou_zhige", "CHAR.gao_wanqing"], "LOC.first_gate", "用旧表和物证还原潜水员死亡时间", "官方死亡时间比机械时间早十二分钟", "旧表指向第四份记录", "高晚晴找到哥哥留下的维修标记", "周止戈要承认哥哥曾违规", "工会被迫公开工资记录", "记录提到顾家董事会"),
    (22, "顾遥的第一段语音", ["CHAR.gu_wangchuan", "CHAR.lin_du"], "LOC.skyline_archive", "确认顾遥拒绝被模型代言", "顾妄川想私藏语音，林渡要进入公开证据链", "顾家董事会记录出现语音时间", "语音说‘少数不是误差’", "顾妄川必须让林渡听见", "他失去一次家族谈判筹码", "语音后半段被白噪塔截留"),
    (23, "简宁的自证", ["CHAR.jian_ning", "CHAR.xu_jianxing"], "LOC.memory_court", "让简宁证明自己不是删除法的替罪羊", "上层要求她承担全部条款责任", "语音截留需要司法厅旧密钥", "简宁公开自己的起草批注", "她可能永远失去执业资格", "许见星替她保留一份病人证词", "第五份失败记录露出"),
    (24, "把城市判回给人", ["CHAR.xu_jianxing", "CHAR.jian_ning"], "LOC.memory_court", "完成第二卷司法回报", "暂缓记忆法会让法院失去证人保护能力", "第五份记录证明删除法被滥用", "许见星在听证中让证人选择是否观看", "法院暂缓整部法", "天幕宣布雁回为高危样本", "深海观测站坐标公开"),
]

for n, title, actors, loc, function, goal, opponent, cause, info, reveal, hook in seed_specs:
    actor_names = [ACTOR_NAMES.get(actor, actor) for actor in actors]
    place = LOCATION_NAMES.get(loc, loc)
    choice = f"选择公开{info}"
    cost = f"{reveal}的后果落到团队身上"
    rec_data = rec(
        n, "VOLUME.law_of_names", title, actors, loc, function, goal, opponent,
        f"{goal}与{opponent}无法同时成立", "若失败，证人、证据或医疗资源会被再次删除", cause,
        [f"{actor_names[0]}在{place}执行{goal}", f"{actor_names[1]}遭遇{opponent}设置的反制", f"{actor_names[0]}改用{reveal}打开另一条路径", f"现场暴露：{info}", f"为保住选择，{actor_names[1]}承担{cost}", f"最后留下线索：{hook}"],
        [f"{opponent}封锁现场", f"{opponent}要求先交出隐私", f"{opponent}改变证据位置", f"{opponent}否认{info}", f"{opponent}公开不利记录", f"{opponent}启动下一层权限"],
        info, reveal, choice, cost, f"确认{info}，代价是{reveal}", hook,
        ["保住当前证据", "把证据变成合法事实", "让下一章有具体入口"],
        ["入口冲突扩大", "证据反转", "代价换来钩子"],
        ["时间窗口缩短", "关系信任下降", "资源或权限损耗"],
        ["先保住人或物", "获得一条反向证据", "下一章地图或对手动作明确"],
        ["身份认证", "证据保全", "公开听证"],
        [f"{place}入口", f"{place}记录室", f"{place}出口"],
        [f"确认{info}", f"阻止{reveal}", f"带出{hook}"],
        [f"{opponent}要求先交出{info}", f"{opponent}利用{reveal}封锁证人", f"{opponent}在{hook}前切断出口"],
        [f"若失败，{info}失去原始记录", f"若妥协，{reveal}会成为公开代价", f"若撤离，{hook}永久关闭"],
        [[f"{actor_names[0]}核验{info}", "挡住封锁"], [f"{actor_names[1]}对照{reveal}", "拆开证据"], [f"{actor_names[0]}带出{hook}", "保留钩子"]],
        [f"{info}从线索变成证据", f"{reveal}迫使盟友改策", f"{hook}改变下一卷入口"],
        ["信息", "关系", "权限"],
        ["LINE.names", "LINE.community_trust"],
    )
    chapter_records.append(rec_data)

tail_specs = [
    (25, "深海入口", ["CHAR.zhou_zhige", "CHAR.lin_du"], "LOC.deepsea_station", "进入深海观测站", "深海站把所有外来者当成污染", "第二卷坐标在潮线工会手里", "进入必须先关闭一条救援管", "工人会被困在海底", "九份失败记录的容器浮出"),
    (26, "第一错：潮汐", ["CHAR.lin_du", "CHAR.lin_qiu"], "LOC.deepsea_station", "取出潮汐预测失败记录", "蔺秋要先修复模型，林渡要保住原始误差", "深海站能源只够一个方案", "模型删掉了异常潮汐", "蔺秋必须承认签字", "第二错记录藏在医疗排序"),
    (27, "第二错：床位", ["CHAR.xu_jianxing", "CHAR.lin_qiu"], "LOC.deepsea_station", "阻止医疗排序把无身份者推入海水舱", "系统按生存概率分配床位", "医疗记录与深海舱相连", "许见星让重症病人自己决定让位", "她的急救站会失去未来配给", "第三错记录被激活"),
    (28, "第三错：航线", ["CHAR.zhou_zhige", "CHAR.xu_jianxing"], "LOC.deepsea_station", "用工人地图改写救援航线", "官方航线避开无身份船只", "手动闸门只能救一条船", "周止戈把工会船员名单接入航线", "航线公开会暴露走私", "第四错记录出现顾家标记"),
    (29, "顾家标记", ["CHAR.gu_wangchuan", "CHAR.jian_ning"], "LOC.deepsea_station", "查清顾家为何维护失败记录容器", "顾妄川想保住家族最后一块防火墙", "顾家标记与白噪塔相连", "简宁发现顾家曾主动保存一批证人记忆", "顾妄川必须交出父亲日志", "第五错记录要求工程师签名"),
    (30, "第五错：删除", ["CHAR.jian_ning", "CHAR.lin_du"], "LOC.deepsea_station", "追回记忆删除的原始授权", "删除本身能阻止一场证人屠杀", "简宁面对保护与掩盖的边界", "林渡发现自己当年也请求过删除", "简宁拒绝替他解释", "顾遥语音第三段出现"),
    (31, "语音里的海面", ["CHAR.gu_wangchuan", "CHAR.lin_qiu"], "LOC.deepsea_station", "还原顾遥看到的真实海面", "模型把顾遥的选择标成噪音", "语音第三段能打开算力室", "蔺秋让顾妄川亲自听完", "顾妄川失去一项模型权限", "第六错记录是安置合同"),
    (32, "第六错：安置", ["CHAR.xu_jianxing", "CHAR.gao_wanqing"], "LOC.deepsea_station", "证明安置合同不是救援而是收编", "合同把居民生活物件视为可抛弃行李", "高晚晴的物证库被列为风险资产", "许见星带家属把物件搬入海底档案仓", "社区失去合法安置名额", "第七错记录是模型误差"),
    (33, "第七错：误差", ["CHAR.lin_qiu", "CHAR.lin_du"], "LOC.deepsea_station", "让模型误差无法再次被缩小", "天幕派人用新模型覆盖旧误差", "蔺秋必须在现场编译公开版本", "林渡把自己的罪责写进变量说明", "工程师团队将失去工作", "第八错记录是公开授权"),
    (34, "第八错：授权", ["CHAR.jian_ning", "CHAR.zhou_zhige"], "LOC.deepsea_station", "确认授权必须来自不同阶层", "深海站要求单一最高签名", "工会和法院意见冲突", "简宁让周止戈先否决她的方案", "公开授权钥仍差一人", "白噪塔主机开始自毁"),
    (35, "第九错：谁来决定", ["CHAR.lin_du", "CHAR.xu_jianxing"], "LOC.deepsea_station", "找到第九份失败记录的持有人", "所有人都想让林渡成为最终签名者", "公共召回钥拒绝单人授权", "许见星让每个证人选择是否观看", "林渡失去最短关闭路径", "深海风暴进入城市"),
    (36, "九份记录不是九把刀", ["CHAR.lin_du", "CHAR.gu_wangchuan"], "LOC.deepsea_station", "完成第三卷世界观反转", "林渡和顾妄川都必须放弃独占权限", "深海站开始坍塌", "顾妄川公开顾家删除日志，林渡承认隐瞒第三方案", "两人都失去旧身份", "白噪终局的全城风暴开始"),
]

for n, title, actors, loc, function, goal, opponent, cause, info, hook in tail_specs:
    actor_names = [ACTOR_NAMES.get(actor, actor) for actor in actors]
    place = LOCATION_NAMES.get(loc, loc)
    reveal = f"现场揭示：{info}"
    choice = f"选择保住{info}"
    cost = f"{reveal}的后果落到队伍身上"
    rec_data = rec(
        n, "VOLUME.deepsea_failure", title, actors, loc, function, goal, opponent,
        f"{goal}与{opponent}无法同时成立", "深海站失守会让九份记录永久消失，保住记录则会把风暴带入城市", cause,
        [f"{actor_names[0]}进入{place}执行{goal}", f"{actor_names[1]}与{opponent}正面冲突", f"{actor_names[0]}改用{reveal}改变路线", f"记录暴露：{info}", f"为公开证据，{actor_names[1]}承担{cost}", f"深海站留下{hook}"],
        [f"{opponent}关闭一条通道", f"{opponent}要求交出记录", f"{opponent}引爆替代系统", f"{opponent}否认{info}", f"{opponent}切断后援", f"{opponent}把风暴推向城市"],
        info, reveal, choice, cost, f"记录坐实：{info}；代价：{reveal}", hook,
        ["保住一份记录", "让记录进入公共保全", "把风暴后果交给终局"],
        ["深海入口关闭", "记录用途反转", "公共授权缺口暴露"],
        ["氧气和能源下降", "盟友信任重估", "地图回不去了"],
        ["记录保住", "一个角色失去旧身份", "风暴进入城市"],
        ["海底工程", "证据解释", "权力授权"],
        [f"{place}外舱", f"{place}记录舱", f"{place}坍塌通道"],
        [f"确认{info}是否原始", f"阻止{reveal}覆盖记录", f"把{hook}带出深海"],
        [f"{opponent}封闭外舱", f"{opponent}要求交出{info}", f"{opponent}把{hook}锁进坍塌通道"],
        [f"若迟疑，{info}永久失真", f"若保存，{reveal}会牺牲撤离时间", f"若撤离，{hook}无法进入公共保全"],
        [[f"{actor_names[0]}切断替代线", "潜入记录舱"], [f"{actor_names[1]}复原{info}", "写入公开说明"], [f"两人带走{hook}", "封住坍塌口"]],
        [f"{info}改变救援排序", f"{reveal}迫使队伍分裂", f"{hook}把风暴推向终局"],
        ["资源", "证据", "责任"],
        ["LINE.engineer_guilt", "LINE.central_model"],
    )
    chapter_records.append(rec_data)

final_specs = [
    (37, "独占召回钥", ["CHAR.lin_du", "CHAR.xu_jianxing"], "LOC.orbit_relay", "让全城风暴与个人权限正面相撞", "阻止天幕把林渡设为唯一记忆管理员", "FACTION.tianmu", "风暴倒计时与个人签名不能同时完成", "公共召回钥拒绝单人授权", "林渡的白噪塔记录将被永久封存", "真正的钥匙在证人选择"),
    (38, "盟友的否决票", ["CHAR.xu_jianxing", "CHAR.lin_du"], "LOC.yanhui", "让盟友主动否决主角方案", "把公共授权从英雄身上拆开", "林渡的最快方案", "许见星要求先听完所有证人", "城市损失扩大", "第一批居民选择不观看"),
    (39, "顾家的最高权限", ["CHAR.gu_wangchuan", "CHAR.jian_ning"], "LOC.orbit_relay", "让顾妄川关闭家族总控", "关闭总控会让模型失去稳定，继续控制会让顾家保住统治", "董事会残余", "顾妄川需要简宁见证权限切断", "他失去顾家全部财产", "顾遥完整语音抵达白噪塔"),
    (40, "不观看也是选择", ["CHAR.xu_jianxing", "CHAR.gao_wanqing"], "LOC.white_noise", "把记忆召回的伦理问题具体化", "保护拒绝观看的人不被英雄叙事裹挟", "公众要求所有人立即看真相", "高晚晴用物证替代强制观看", "证人会被舆论攻击", "白噪塔出现公共否决记录"),
    (41, "林渡的第三方案", ["CHAR.lin_du", "CHAR.jian_ning"], "LOC.white_noise", "公开林渡当年的隐瞒", "让旧案不再只剩顾家和天幕的罪", "林渡自己", "简宁要求把签批和未执行方案同时播出", "林渡会失去所有洗白空间", "第三方案能救一部分人但会牺牲另一部分"),
    (42, "把牺牲写回名字", ["CHAR.lin_du", "CHAR.gao_wanqing"], "LOC.white_noise", "让被牺牲者从统计数回到名字", "系统只允许播出总数", "天幕残余接口", "高晚晴把死者物件逐一接入召回", "召回速度大幅下降", "三万人名单开始出现家属回应"),
    (43, "风暴中的手动闸", ["CHAR.zhou_zhige", "CHAR.lin_du"], "LOC.first_gate", "让工人线在终局决定城市生死", "自动系统失控，手动闸门只能保住一个城区", "模型中枢", "周止戈拒绝让林渡代选城区", "工会必须公开投票", "第一潮门与白噪塔同时亮起"),
    (44, "蔺秋关闭模型", ["CHAR.lin_qiu", "CHAR.gu_wangchuan"], "LOC.orbit_relay", "让模型线完成从控制到公开误差的转变", "关闭模型会让风暴预警变得混乱", "天幕董事会", "蔺秋把模型拆成三个互相校验的公共模块", "她失去工程团队", "白噪塔获得最后一类证据"),
    (45, "全城第一次选择", ["CHAR.xu_jianxing", "CHAR.jian_ning"], "LOC.yanhui", "让受灾者共同授权而非被主角代表", "公众选择是否召回记忆会改变救援路线", "恐慌舆论", "许见星让每个社区用纸面和口述完成双重授权", "救援速度降低", "公共召回钥完成九成"),
    (46, "白噪塔里的顾遥", ["CHAR.gu_wangchuan", "CHAR.lin_du"], "LOC.white_noise", "完成顾遥语音与系统真相的汇合", "顾遥拒绝被任何一方解释", "顾妄川与林渡的自我投射", "两人只能原声播放不作旁白", "顾妄川承认自己也在利用妹妹", "白噪塔关闭删除接口"),
    (47, "不替死者发言", ["CHAR.lin_du", "CHAR.xu_jianxing"], "LOC.white_noise", "让终局爽点从碾压变成归还选择", "林渡有机会用一次权限洗清个人罪责", "个人英雄方案", "许见星要求他公开全部责任后让证人决定观看", "林渡失去工程执照和部分记忆", "完整责任链进入公开审判"),
    (48, "白噪归航", ["CHAR.lin_du", "CHAR.jian_ning"], "LOC.white_noise", "完成全书因果结算与制度余波", "关闭删除功能会让城市永久记住痛苦，保留功能则会重建旧中枢", "FACTION.tianmu与恐惧本身", "林渡放弃独占权限，简宁启动公开审计", "所有人都失去一条最方便的逃路", "新公共灾害网络第一次独立运行"),
]

for spec in final_specs:
    n, title, actors, loc, function, goal, opponent, cause, info, *tail = spec
    actor_names = [ACTOR_NAMES.get(actor, actor) for actor in actors]
    place = LOCATION_NAMES.get(loc, loc)
    if len(tail) == 2:
        reveal, hook = tail
    else:
        reveal, hook = f"现场揭示：{info}", tail[0]
    choice = f"让公众看见{info}"
    cost = f"{reveal}的后果公开化"
    rec_data = rec(
        n, "VOLUME.white_noise_trial", title, actors, loc, function, goal, opponent,
        f"{goal}与{opponent}无法同时成立", "若选错，全城会在没有完整记忆的情况下进入下一次灾害", cause,
        [f"{actor_names[0]}进入{place}执行{goal}", f"{actor_names[1]}发现{opponent}的最后反制", f"{actor_names[0]}改用{reveal}重排授权", f"全城得到新信息：{info}", f"为了保住选择，{actor_names[1]}承担{cost}", f"终局留下：{hook}"],
        [f"{opponent}制造倒计时", f"{opponent}要求林渡独占签名", f"{opponent}切断一类证据", f"{opponent}把责任归给个人", f"{opponent}发动舆论或物理冲击", f"{opponent}逼所有人回到旧中枢"],
        info, reveal, choice, cost, f"{info}进入公共选择，代价是{reveal}", hook,
        ["稳定当前现场", "让选择可被看见", "为没有救世主的下一次风暴留下制度"],
        ["个人方案被提出", "盟友主动否决", "公共授权完成"],
        ["时间压力达到峰值", "每个人都失去一项安全", "终局不恢复旧秩序"],
        ["一个城区被保住", "责任链公开", "新制度接管下一场普通风暴"],
        ["灾害调度", "公共授权", "记忆伦理"],
        [f"{place}外层", f"{place}记忆厅", f"{place}公开审计台"],
        [f"阻止{opponent}夺取签名", f"保护拒绝观看的证人", f"让{info}进入公共审计"],
        [f"{opponent}制造倒计时", f"{opponent}要求林渡独占签名", f"{opponent}逼所有人回到旧中枢"],
        [f"若使用个人权限，{info}会被主角垄断", f"若强制观看，{reveal}会伤害证人", f"若关闭删除，{hook}必须由公众承担"],
        [[f"{actor_names[0]}接入{info}", "分流风暴"], [f"{actor_names[1]}播放{reveal}", "保全选择"], [f"公众审计{hook}", "关闭删除"]],
        [f"{info}从个人钥匙变成公共选择", f"{reveal}迫使盟友否决英雄方案", f"{hook}把制度交给下一场风暴"],
        ["关系", "选择", "制度"],
        ["LINE.community_trust", "LINE.engineer_guilt"],
    )
    chapter_records.append(rec_data)

chapter_entities = [chapter(record) for record in sorted(chapter_records, key=lambda item: item["n"])]

edges = [
    {"id": "REL.lin_xu", "type": "TRUST_TENSION", "source": "CHAR.lin_du", "target": "CHAR.xu_jianxing", "payload": {"state": "旧同事与旧情，互相否决", "provenance_refs": SOURCE}},
    {"id": "REL.lin_gu", "type": "MIRROR_OPPOSITION", "source": "CHAR.lin_du", "target": "CHAR.gu_wangchuan", "payload": {"state": "都想减少死亡，但对个人选择理解相反", "provenance_refs": SOURCE}},
    {"id": "REL.xu_jianxing_gao", "type": "COMMUNITY_ALLY", "source": "CHAR.xu_jianxing", "target": "CHAR.gao_wanqing", "payload": {"state": "医疗与物证互相保护", "provenance_refs": SOURCE}},
    {"id": "REL.jian_lin", "type": "LEGAL_CHECK", "source": "CHAR.jian_ning", "target": "CHAR.lin_du", "payload": {"state": "法律监督主角不能用非法取证冒充公正", "provenance_refs": SOURCE}},
    {"id": "REL.zhou_lin", "type": "FIELD_ALLY", "source": "CHAR.zhou_zhige", "target": "CHAR.lin_du", "payload": {"state": "工人现场经验约束工程师抽象判断", "provenance_refs": SOURCE}},
]

for index in range(1, len(chapter_entities)):
    edges.append({"id": f"PRECEDES.CH{index}", "type": "PRECEDES", "source": f"CHAPTER_PLAN.{index:03d}", "target": f"CHAPTER_PLAN.{index + 1:03d}", "payload": {"provenance_refs": SOURCE}})

packet = {
    "packet_mode": "SNAPSHOT",
    "source_refs": SOURCE,
    "assumptions": [
        "这是原创化重建，不复制参考作品的角色、专名、签名场景、句式或章节顺序。",
        "本次冻结4卷48章；每章按4000—6000字正文容量设计，先交付大纲不写正文。",
        "故事的升级货币是证据、权限、公众信任和制度授权，不是单线战力境界。",
    ],
    "open_questions": [
        "正文生产时需要依据实际读者反馈调整章节间的情绪波幅，但不得减少最终章数而不重新审计。",
    ],
    "precision": {
        "production_stage": "FINAL_FULL_BOOK",
        "full_book_detailed_required": True,
        "expected_volumes": 4,
        "expected_chapters": 48,
        "target_prose_range": [4000, 6000],
        "originalization_level": "HIGH",
        "source_similarity_policy": "MECHANISM_ONLY",
    },
    "provenance_registry": SOURCE,
    "negative_facts": [
        "禁止使用原参考作品的人名、师父师姐配置、酒店毁容、总督亮证、枪弹反弹等签名桥段。",
        "禁止把许见星、高晚晴、简宁写成只负责受辱、被救或提供资源的角色。",
        "禁止让九份失败记录变成万能能力；它们只能揭示一种系统失败并暴露持有者代价。",
        "禁止以重复震惊、境界报数、库存流水和突然出现的更大反派填充章节。",
    ],
    "entities": [
        project,
        *characters,
        *factions,
        *locations,
        *rules,
        *props,
        entity("ACT.return", "ACT", "第一幕·回港与失名", {"range": "第1—24章", "central_question": "被系统判死的人能否先保住现实中的生活", "irreversible_turn": "林渡公开自己当年的签批", "provenance_refs": SOURCE}, "PLAN"),
        entity("ACT.deepsea", "ACT", "第二幕·九错与风暴", {"range": "第25—36章", "central_question": "九份失败记录究竟要分权还是要造神", "irreversible_turn": "顾家与林渡都承认责任", "provenance_refs": SOURCE}, "PLAN"),
        entity("ACT.public", "ACT", "第三幕·公共召回", {"range": "第37—48章", "central_question": "没有救世主时谁来承担完整记忆", "irreversible_turn": "公共召回钥拒绝个人签名", "provenance_refs": SOURCE}, "PLAN"),
        *volumes,
        *lines,
        *promises,
        entity("CLIMAX.public_recall", "CLIMAX", "白噪塔公共召回审判", {"act_ref": "ACT.public", "trigger": "全城风暴接入记忆接口", "choice": "林渡公开责任并放弃独占权限", "payoff": "白噪塔停止删除，天幕拆成公共灾害网络", "cost": "主角失去执照和部分记忆，城市保留完整痛苦", "reader_reward": "复仇完成但旧垄断不复活", "provenance_refs": SOURCE}, "PLAN"),
        *event_entities,
        *chapter_entities,
    ],
    "edges": edges + event_edges,
}

Path("/Users/tang/PycharmProjects/pythonProject/changpianxiaoshuodagang/.outline/guimen_packet.json").write_text(
    json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({"entities": len(packet["entities"]), "edges": len(packet["edges"]), "chapters": len(chapter_entities)}, ensure_ascii=False))
