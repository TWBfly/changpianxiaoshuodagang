# 临河赈粮危机

- project_id: `PROJECT.demo`
- source: `SQLite Canon`

- 假设: （无）
- 开放问题: （无）
- 来源: （无）
- 精度: `{"expected_chapters": 1, "full_book_detailed_required": true, "target_prose_range": [4000, 6000]}`

# 项目总契约与禁止事项

- （本阶段暂无已提交条目）

# 世界观与风格宪法

- `RULE.curfew_order` **临河县夜间封门令** [RULE] — exception="病粮和救火物资可由值守医官签字放行"; limit="日落后无县令手令不得出城"; provenance_refs=["BRIEF.demo"]

# 世界规则、时代、技术或力量上限

- （条目已在前置章节展开）

# 地理、交通、通信、资源与信息网络

- `LOC.east_warehouse` **东平码头仓** [LOCATION] — access_conditions=["持船队铜牌或县衙搜查令"]; controller="顾青禾船队"; provenance_refs=["BRIEF.demo"]; travel_cost="一刻钟"
- `LOC.south_gate` **南城门** [LOCATION] — access_conditions=["夜间需县令手令"]; controller="县衙"; provenance_refs=["BRIEF.demo"]; travel_cost="半日"

# 势力和机构生态

- （本阶段暂无已提交条目）

# 全人物总表

- `CHAR.guqinghe` **顾青禾** [临河粮商兼船队东家]
- `CHAR.lujingshan` **鲁敬山** [巡粮御史、幕后买家的代理人]
- `CHAR.shenyan` **沈砚** [临河县令]

# 核心与重要人物生平、性格成因和决策模型

- `CHAR.guqinghe` **顾青禾** [CHARACTER] — identity="临河粮商兼船队东家"; biography="父亲死于一次私运失火，她靠重建船队还清债务，最怕信誉再次被夺走。"; personality="务实、敏锐、对施舍反感"; desires=["保住船队和伙计", "让家人不再受债主控制"]; goals=["找回被截的赈粮账册", "逼幕后买家留下交易痕迹"]; interests=["商路安全", "伙计忠诚", "家族名誉"]; decision_model="先保护伙计与家人，再用可验证的交易痕迹换取公开谈判空间"; private_life="把父亲遗留的船铃放在柜台下，夜里独自核对每笔欠款"; life_constraints=["船队债务", "伙计家属依赖", "家人住在债主控制的街区"]; knowledge_state="知道印章异常和船队损失，不知道交易来源"; misjudgments=["误以为只要护住残页就能护住所有伙计"]; arc="从只想保住自己的商人，成长为愿意承担公开指证代价的共同体盟友"; highlights=["在封门时主动交出一页假账", "拒绝用伙计顶罪"]; fate="船队被拆分监管，但成为新粮运制度的民间监督者"
- `CHAR.lujingshan` **鲁敬山** [CHARACTER] — identity="巡粮御史、幕后买家的代理人"; biography="从军需文书起家，曾因一次饥荒失控被军法问责，后来把控制信息当成安全感来源。"; personality="冷静、控制欲强、擅长把恐惧包装成秩序"; desires=["维持上级对他的信任", "让所有人相信短缺是天灾"]; goals=["夺回账册残页", "把亏空归罪于顾青禾"]; interests=["官位", "秘密交易不曝光", "对地方官的控制"]; decision_model="把信息切成可控份额，让每个下属只看到足以服从的一段真相"; private_life="独居驿馆，按军令格式收存旧案，不允许任何人碰他的私印"; life_constraints=["上级考核", "旧案问责阴影", "交易伙伴互不信任"]; knowledge_state="知道交易链的执行端，不知道上级最终买家"; misjudgments=["误以为切碎信息就能切断责任"]; arc="拒绝承认结构性责任，最终被自己留下的程序证据锁定"; highlights=["把查粮期限提前三日", "在公堂上主动引用一条会反噬自己的旧令"]; fate="被押送京城审理，私人交易网随账册公开而瓦解"
- `CHAR.shenyan` **沈砚** [CHARACTER] — identity="临河县令"; biography="寒门出身，曾在漕运案中失去恩师，因此相信账证胜过口供。"; personality="克制、耐心、对失控高度警惕"; desires=["保住临河百姓", "证明自己没有被权力驯服"]; goals=["查清赈粮亏空", "让证据在公堂上成立"]; interests=["县民生计", "仕途清白", "可持续的司法秩序"]; decision_model="先核对可公开证据，再选择能让多数人承担得起的程序"; private_life="每晚替病母整理药单，害怕县衙失序会让她断药"; life_constraints=["照料病母", "俸禄有限", "不能私设刑讯"]; knowledge_state="知道亏空存在，不知道幕后买家和旧令被谁利用"; misjudgments=["以为只要按程序核账就能避免冲突"]; arc="从依赖程序的孤立清官，成长为能把程序变成公众协作工具的组织者"; highlights=["封门却放行病粮", "在公堂承认自己误判"]; fate="保住县城但失去升迁机会，成为地方新秩序的守门人"

# 人物关系拓扑

- （条目已在前置章节展开）

# 人物弧、高光与命运地图

- （条目已在前置章节展开）

# N 幕宏观结构

- `ACT.relief_crisis` **赈粮危机幕** [ACT] — provenance_refs=["BRIEF.demo"]; range="第1—4卷"

# Dynamic N-Line 总图

- `LINE.merchant_escape` **商队自救线** [LINE] — owner="CHAR.guqinghe"; goal="护住伙计并把残页交给可信的公堂"; pressure="鲁敬山派人封锁船队"; opposing_force="替罪羊叙事和内部恐慌"; milestones=["转移残页", "交出假账诱出追兵", "拒绝让伙计顶罪"]; climax_condition="顾青禾必须公开承认自己改过一张运单"; closure_condition="残页与船队证词共同指向鲁敬山"; status="ACTIVE"
- `LINE.public_investigation` **公开查粮线** [LINE] — owner="CHAR.shenyan"; goal="让账证进入公堂并保住粮路"; pressure="上级提前结案期限"; opposing_force="鲁敬山的程序封锁"; milestones=["封门查粮", "公开赤粮司印", "公堂对质"]; climax_condition="沈砚必须在保仕途和公开证据间选择"; closure_condition="赈粮亏空归因成立且新监管机制生效"; status="ACTIVE"

# 多线碰撞矩阵

- （条目已在前置章节展开）

# 全书剧情梗概

- `EVENT.move_fragment` **转移账册残页** [EVENT] — active_actor="CHAR.guqinghe"; actor_goal="保住伙计并让证据离开封锁区"; action="顾青禾把残页藏进药箱，借病粮例外转移到东平码头"; choice="放弃一船粮，保住唯一证据"; cost="船队损失当日现银并引发伙计不满"; state_delta="账册残页进入顾青禾控制的暗仓"; causal_inputs=["EVENT.seal_gate"]; causal_outputs=["EVENT.public_confrontation"]; time_window="第二日清晨"; location="LOC.east_warehouse"; line_refs=["LINE.merchant_escape"]
- `EVENT.open_accounts` **公开账证** [EVENT] — active_actor="CHAR.shenyan"; actor_goal="让残页、印章和旧令在同一份公案中互相验证"; action="沈砚承认旧令责任，公开残页并要求按印章批次复核入库记录"; choice="沈砚放弃升迁机会，选择把调查权限交给三方见证"; cost="县令职位被暂缓复核，县衙失去独断权"; state_delta="账证闭环成立，地方粮运改为三方留痕"; causal_inputs=["EVENT.public_confrontation"]; causal_outputs=["PROMISE.relief_truth", "CLIMAX.public_record"]; time_window="第四日清晨"; location="LOC.south_gate"; line_refs=["LINE.public_investigation", "LINE.merchant_escape"]
- `EVENT.public_confrontation` **公堂对质** [EVENT] — active_actor="CHAR.lujingshan"; actor_goal="把亏空归罪于顾青禾的私改运单"; action="鲁敬山在公堂先展示运单，再逼顾青禾承认改单"; choice="鲁敬山引用自己签发的旧令压过现场证词"; cost="旧令编号被完整记录在案"; state_delta="替罪羊叙事获得短暂优势，但鲁敬山留下可追溯签批"; causal_inputs=["EVENT.move_fragment", "EVIDENCE.red_seal"]; causal_outputs=["EVENT.open_accounts"]; time_window="第三日午后"; location="LOC.south_gate"; line_refs=["LINE.public_investigation", "LINE.merchant_escape"]
- `EVENT.seal_gate` **封门查粮** [EVENT] — active_actor="CHAR.shenyan"; actor_goal="在不饿死病户的前提下冻结可疑粮车"; action="沈砚在南城门下令查验粮车，并援引病粮例外放行一车药粮"; choice="牺牲官场信用换取半日调查窗口"; cost="县衙被上级认定为拖延"; state_delta="顾青禾的出城路线被迫转入东平码头"; causal_inputs=["RULE.curfew_order", "OBJECT.ledger_fragment"]; causal_outputs=["EVENT.move_fragment"]; time_window="第一日傍晚"; location="LOC.south_gate"; line_refs=["LINE.public_investigation", "LINE.merchant_escape"]

# 全书主因果链

- （条目已在前置章节展开）

# 伏笔、悬念、揭示和兑现地图

- `PROMISE.relief_truth` **赤粮司印的真正含义** [PROMISE] — creation_event="EVENT.seal_gate"; maturity_condition="残页数字、印章批次和旧令编号在同一张证词中出现"; reveal_window="第四日公堂"; payoff_event="EVENT.open_accounts"; status="PAID_OFF"; post_payoff_state="赈粮亏空可追溯到鲁敬山代理账房"

# 全书时间线

- （条目已在前置章节展开）

# 空间、移动、资源和信息流

- （条目已在前置章节展开）

# 高潮、低谷和规则变化地图

- `CLIMAX.public_record` **三方留痕公案** [CLIMAX] — irreversible_change="县衙、船队和粮司共同留痕"; provenance_refs=["BRIEF.demo"]; trigger="沈砚公开承认旧令责任"

# 卷级架构与每卷因果脊柱

- `VOLUME.south_gate` **南门卷** [VOLUME] — core_question="账册残页能否在粮路断裂前成为公共证据"; provenance_refs=["BRIEF.demo"]

# 全章 Story Nodes

- （条目已在前置章节展开）

# 指定窗口详细章纲

- `CHAPTER.1` **第一章《南门封粮》** [CHAPTER_PLAN] — chapter_no=1; volume_ref="VOLUME.south_gate"; plan_level="PRODUCTION_READY"; target_prose_contract={"chapter_mode": "STANDARD_LONG", "target_default": 5000, "target_max": 6000, "target_min": 4000, "unit": "CHINESE_PROSE_CHARACTERS"}; chapter_function="让沈砚第一次用程序换取调查窗口，同时切断顾青禾的安全退路"; core_delta="封门令生效，账册残页进入转移路线，沈砚失去上级信任"; conflict_contract={"actor_a": "沈砚要冻结可疑粮车并保住病粮通道", "actor_b": "鲁敬山要用限期结案压缩调查空间", "concrete_incompatibility": "既要冻结证据又要保住全部粮路在当前权限下不能同时成立", "conflict_medium": "封门令、病粮例外和限期公文"}; dynamic_beats=[{"action": "沈砚在南城门下令查验粮车，并公开援引病粮例外", "active_actor": "CHAR.shenyan", "actor_goal_after": "用病粮例外换取查验时间", "actor_goal_before": "在不饿死病户的前提下冻结粮车", "beat_id": "BEAT.1", "beat_role": "ACTION", "cause_from_previous": "赈粮亏空与夜间封门令同时出现", "counterforce": "鲁敬山的限期结案公文先一步抵达", "delta": {"authority": "上级信任下降", "goal": "调查窗口暂时打开"}, "new_information_or_choice": "沈砚发现病粮例外能成为合法缺口", "next_pressure_created": "顾青禾的出城路线被迫改变", "stageability": "STAGEABLE_CORE", "what_becomes_impossible_or_more_expensive": "继续按旧程序核账会失去半日窗口"}, {"action": "鲁敬山提前派人封住正门并要求立即交出账册", "active_actor": "CHAR.lujingshan", "actor_goal_after": "先夺回账册再切断见证人", "actor_goal_before": "把查粮压缩成程序拖延", "beat_id": "BEAT.2", "beat_role": "COUNTERMOVE", "cause_from_previous": "沈砚公开援引病粮例外", "counterforce": "沈砚把查验记录当众交给三名见证人", "delta": {"knowledge": "沈砚确认对手在控制信息", "risk": "冲突公开化"}, "new_information_or_choice": "封锁本身成为未来追查的程序证据", "next_pressure_created": "顾青禾必须在粮和证据之间选择", "stageability": "STAGEABLE_CORE", "what_becomes_impossible_or_more_expensive": "鲁敬山无法无痕撤回限期命令"}, {"action": "顾青禾把残页藏进药箱，改走东平码头", "active_actor": "CHAR.guqinghe", "actor_goal_after": "牺牲现银换取证据存活", "actor_goal_before": "保住船队和账册残页", "beat_id": "BEAT.3", "beat_role": "REPLAN", "cause_from_previous": "正门封锁使原定出城路线失效", "counterforce": "放弃一船粮才能避开搜查", "delta": {"available_path": "转入暗仓", "resource": "损失一船粮"}, "new_information_or_choice": "她意识到沈砚的封门令既保护她又困住她", "next_pressure_created": "伙计开始怀疑她在拿船队冒险", "stageability": "STAGEABLE_CORE", "what_becomes_impossible_or_more_expensive": "保住现银与保住证据不再能同时成立"}, {"action": "顾青禾主动交出一页假账，引导搜查队追错方向", "active_actor": "CHAR.guqinghe", "actor_goal_after": "用公开承认小错保护更大的证据", "actor_goal_before": "让证据留在自己控制范围", "beat_id": "BEAT.4", "beat_role": "COST", "cause_from_previous": "残页已进入东平码头暗仓", "counterforce": "鲁敬山借假账制造她私改运单的口实", "delta": {"evidence": "获得一条反向证据", "relationship": "与伙计的信任受损"}, "new_information_or_choice": "假账把追兵引开，也留下可追溯的交易痕迹", "next_pressure_created": "公堂对质将同时审查残页和改单行为", "stageability": "STAGEABLE_CORE", "what_becomes_impossible_or_more_expensive": "她无法继续否认自己改过运单"}]; payload_clusters=[{"active_actors": ["CHAR.shenyan", "CHAR.lujingshan"], "cluster_id": "CLUSTER.chapter1.a", "conflict_medium": "封门令与限期公文", "exit_state": "正门封锁，调查窗口短暂打开", "local_cost": "沈砚失去上级信任", "local_goal": "沈砚试图合法打开调查窗口", "local_turn": "调查记录被公开，双方冲突无法私下收回", "pressure_handed_to_next_cluster": "顾青禾必须改道转移残页", "stageable_beats": ["BEAT.1", "BEAT.2"]}, {"active_actors": ["CHAR.guqinghe", "CHAR.lujingshan"], "cluster_id": "CLUSTER.chapter1.b", "conflict_medium": "粮船、暗仓和假账", "exit_state": "残页暂时安全，顾青禾被推向公堂", "local_cost": "船队现银和伙计信任同时受损", "local_goal": "顾青禾让证据脱离封锁", "local_turn": "假账保护残页却反过来成为指控材料", "pressure_handed_to_next_cluster": "公堂必须同时审查证据和她的过错", "stageable_beats": ["BEAT.3", "BEAT.4"]}]; scene_payloads=[{"active_actor_goal": "沈砚打开查验窗口", "delta_dimensions": ["authority", "risk", "available_path"], "entry_state": "亏空存在但证据尚未公开", "exit_state": "正门封锁，调查窗口打开", "immediate_stakes": "病粮、官位和证据同时受威胁", "live_actions": ["封门", "查验", "公开记录"], "opposing_goal_or_process": "鲁敬山用限期公文制造程序压力", "payload_cluster_refs": ["CLUSTER.chapter1.a"], "scene_id": "SCENE.chapter1.gate", "turn_or_reprice": "程序记录从保护沈砚变成约束双方的证据"}, {"active_actor_goal": "保住残页和伙计", "delta_dimensions": ["resource", "knowledge", "relationship", "risk"], "entry_state": "顾青禾原有出城路线失效", "exit_state": "残页暂存暗仓，顾青禾被迫面对公堂", "immediate_stakes": "一船粮、残页和伙计生计只能保住两项", "live_actions": ["改道", "藏证", "投放假账"], "opposing_goal_or_process": "搜查队封锁正门并寻找账册", "payload_cluster_refs": ["CLUSTER.chapter1.b"], "scene_id": "SCENE.chapter1.warehouse", "turn_or_reprice": "证据安全换来公开承认改单的代价"}]; explicit_compression={"ledger_not_to_itemize": ["粮船库存流水", "普通费用"], "process_to_summarize": ["普通赶路", "无阻力复核"], "repeated_consequence_to_collapse": ["同一封锁后果只证明一次"]}; continuation_source="假账让顾青禾暂时保住残页，却把她推入必须公开承认改单的公堂"; forbidden_drift=["不得新增决定性证据", "不得让鲁敬山突然亲自接触残页"]; capacity_audit={"chapter_id": "CHAPTER.1", "core_scenes": 2, "failure_reasons": [], "final_capacity": "FULL", "mid_chapter_load": "PASS", "missing_middle_roles": [], "payload_clusters": 2, "stageable_core_beats": 4, "summary_result_beats_removed": 0, "supporting_stageable_beats": 0, "target_prose_range": [4000, 6000], "writer_core_plot_invention_required": false}

# 关键人物、道具、证据、地点和规则来源表

- `EVIDENCE.red_seal` **倒置的赤粮司印** [EVIDENCE] — meaning="显示赈粮在入库前已被重新过秤"; provenance_refs=["BRIEF.demo"]
- `OBJECT.ledger_fragment` **赈粮账册残页** [OBJECT] — material_constraint="水浸后只能辨认印章和三行数字"; owner_history=["鲁敬山代理账房", "顾青禾", "沈砚保管"]; provenance_refs=["BRIEF.demo"]

# 开放余波与禁止漂移清单

- （条目已在前置章节展开）

# 负事实与禁止漂移

- `夜间封门令不能覆盖病粮例外`
- `没有无来源的第七名关键人物`
- `鲁敬山没有亲自接触账册残页`

# 关系与因果边

- `EDGE.c1` `CAUSES`: **封门查粮** → **转移账册残页** — {"reason": "封门迫使转移"}
- `EDGE.c2` `CAUSES`: **转移账册残页** → **公堂对质** — {"reason": "残页进入公案"}
- `EDGE.c3` `CAUSES`: **公堂对质** → **公开账证** — {"reason": "旧令编号可追溯"}
- `EDGE.climax` `REALIZES`: **公开账证** → **三方留痕公案** — {}
- `EDGE.l1` `OWNS_LINE`: **沈砚** → **公开查粮线** — {}
- `EDGE.l2` `OWNS_LINE`: **顾青禾** → **商队自救线** — {}
- `EDGE.l3` `COLLIDES_WITH`: **公开查粮线** → **商队自救线** — {"shared_resource": "OBJECT.ledger_fragment"}
- `EDGE.p1` `PARTICIPATES_IN`: **沈砚** → **封门查粮** — {"role": "initiator"}
- `EDGE.p10` `PARTICIPATES_IN`: **倒置的赤粮司印** → **公堂对质** — {"role": "evidence"}
- `EDGE.p11` `PARTICIPATES_IN`: **沈砚** → **公开账证** — {"role": "initiator"}
- `EDGE.p12` `PARTICIPATES_IN`: **鲁敬山** → **公开账证** — {"role": "target"}
- `EDGE.p13` `PARTICIPATES_IN`: **赈粮账册残页** → **公开账证** — {"role": "evidence"}
- `EDGE.p14` `PARTICIPATES_IN`: **南城门** → **公开账证** — {"role": "location"}
- `EDGE.p2` `PARTICIPATES_IN`: **顾青禾** → **封门查粮** — {"role": "target"}
- `EDGE.p3` `PARTICIPATES_IN`: **赈粮账册残页** → **封门查粮** — {"role": "evidence"}
- `EDGE.p4` `PARTICIPATES_IN`: **南城门** → **封门查粮** — {"role": "location"}
- `EDGE.p5` `PARTICIPATES_IN`: **顾青禾** → **转移账册残页** — {"role": "initiator"}
- `EDGE.p6` `PARTICIPATES_IN`: **赈粮账册残页** → **转移账册残页** — {"role": "evidence"}
- `EDGE.p7` `PARTICIPATES_IN`: **东平码头仓** → **转移账册残页** — {"role": "location"}
- `EDGE.p8` `PARTICIPATES_IN`: **鲁敬山** → **公堂对质** — {"role": "initiator"}
- `EDGE.p9` `PARTICIPATES_IN`: **顾青禾** → **公堂对质** — {"role": "target"}
- `EDGE.pays` `PAYS_OFF`: **公开账证** → **赤粮司印的真正含义** — {}
- `EDGE.r1` `OPPOSES`: **沈砚** → **鲁敬山** — {"asymmetry": "沈砚求公开证据，鲁敬山求控制叙事"}
- `EDGE.r2` `TRANSACTS_WITH`: **顾青禾** → **沈砚** — {"exchange": "证据换合法文书"}
- `EDGE.t1` `PRECEDES`: **封门查粮** → **转移账册残页** — {}
- `EDGE.t2` `PRECEDES`: **转移账册残页** → **公堂对质** — {}
- `EDGE.t3` `PRECEDES`: **公堂对质** → **公开账证** — {}
- `EDGE.v1` `BELONGS_TO`: **封门查粮** → **南门卷** — {}
- `EDGE.v2` `BELONGS_TO`: **公开账证** → **赈粮危机幕** — {}
