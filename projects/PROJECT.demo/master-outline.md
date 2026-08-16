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

- `RULE.curfew_order` **临河县夜间封门令** [RULE]
  * **exception**: 病粮和救火物资可由值守医官签字放行
  * **limit**: 日落后无县令手令不得出城
  * **provenance_refs**: BRIEF.demo


# 世界规则、时代、技术或力量上限

- （条目已在前置章节展开）

# 地理、交通、通信、资源与信息网络

- `LOC.east_warehouse` **东平码头仓** [LOCATION]
  * **access_conditions**: 持船队铜牌或县衙搜查令
  * **controller**: 顾青禾船队
  * **provenance_refs**: BRIEF.demo
  * **travel_cost**: 一刻钟

- `LOC.south_gate` **南城门** [LOCATION]
  * **access_conditions**: 夜间需县令手令
  * **controller**: 县衙
  * **provenance_refs**: BRIEF.demo
  * **travel_cost**: 半日


# 势力和机构生态

- （本阶段暂无已提交条目）

# 全人物总表

- `CHAR.guqinghe` **顾青禾** [CORE | 临河粮商兼船队东家]
- `CHAR.lujingshan` **鲁敬山** [MAJOR | 巡粮御史、幕后买家的代理人]
- `CHAR.shenyan` **沈砚** [CORE | 临河县令]

# 核心与重要人物生平、性格成因和决策模型

- `CHAR.guqinghe` **顾青禾** [临河粮商兼船队东家]
  * **人物层级**: `CORE` | **核心欲望**: 保住船队和伙计、让家人不再受债主控制 | **阶段目标**: 找回被截的赈粮账册、逼幕后买家留下交易痕迹
  * **人物生平与成因**: 父亲死于一次私运失火，她靠重建船队还清债务，最怕信誉再次被夺走。
  * **性格特质**: 务实、敏锐、对施舍反感 | **行为策略**: 用商路和人情交换信息，再把风险转嫁给可验证的证据
  * **决策模型**: 先保护伙计与家人，再用可验证的交易痕迹换取公开谈判空间
  * **现实生活与羁绊**: 把父亲遗留的船铃放在柜台下，夜里独自核对每笔欠款 | **现实约束**: 船队债务、伙计家属依赖、家人住在债主控制的街区
  * **认知边界与信息盲区**: 知道印章异常和船队损失，不知道交易来源 | **误判**: 误以为只要护住残页就能护住所有伙计
  * **成长弧光**: 从只想保住自己的商人，成长为愿意承担公开指证代价的共同体盟友
  * **人物高光时刻**: 在封门时主动交出一页假账、拒绝用伙计顶罪
  * **最终命运与归宿**: 船队被拆分监管，但成为新粮运制度的民间监督者

- `CHAR.lujingshan` **鲁敬山** [巡粮御史、幕后买家的代理人]
  * **人物层级**: `MAJOR` | **核心欲望**: 维持上级对他的信任、让所有人相信短缺是天灾 | **阶段目标**: 夺回账册残页、把亏空归罪于顾青禾
  * **人物生平与成因**: 从军需文书起家，曾因一次饥荒失控被军法问责，后来把控制信息当成安全感来源。
  * **性格特质**: 冷静、控制欲强、擅长把恐惧包装成秩序 | **行为策略**: 用行政时限制造恐慌，以程序压力迫使他人互相指认
  * **决策模型**: 把信息切成可控份额，让每个下属只看到足以服从的一段真相
  * **现实生活与羁绊**: 独居驿馆，按军令格式收存旧案，不允许任何人碰他的私印 | **现实约束**: 上级考核、旧案问责阴影、交易伙伴互不信任
  * **认知边界与信息盲区**: 知道交易链的执行端，不知道上级最终买家 | **误判**: 误以为切碎信息就能切断责任
  * **成长弧光**: 拒绝承认结构性责任，最终被自己留下的程序证据锁定
  * **人物高光时刻**: 把查粮期限提前三日、在公堂上主动引用一条会反噬自己的旧令
  * **最终命运与归宿**: 被押送京城审理，私人交易网随账册公开而瓦解

- `CHAR.shenyan` **沈砚** [临河县令]
  * **人物层级**: `CORE` | **核心欲望**: 保住临河百姓、证明自己没有被权力驯服 | **阶段目标**: 查清赈粮亏空、让证据在公堂上成立
  * **人物生平与成因**: 寒门出身，曾在漕运案中失去恩师，因此相信账证胜过口供。
  * **性格特质**: 克制、耐心、对失控高度警惕 | **行为策略**: 先稳住粮路，再用公开账证迫使对手自证
  * **决策模型**: 先核对可公开证据，再选择能让多数人承担得起的程序
  * **现实生活与羁绊**: 每晚替病母整理药单，害怕县衙失序会让她断药 | **现实约束**: 照料病母、俸禄有限、不能私设刑讯
  * **认知边界与信息盲区**: 知道亏空存在，不知道幕后买家和旧令被谁利用 | **误判**: 以为只要按程序核账就能避免冲突
  * **成长弧光**: 从依赖程序的孤立清官，成长为能把程序变成公众协作工具的组织者
  * **人物高光时刻**: 封门却放行病粮、在公堂承认自己误判
  * **最终命运与归宿**: 保住县城但失去升迁机会，成为地方新秩序的守门人


# 人物关系拓扑

- （条目已在前置章节展开）

# 人物弧、高光与命运地图

- （条目已在前置章节展开）

# N 幕宏观结构

- `ACT.relief_crisis` **赈粮危机幕** [ACT]
  * **provenance_refs**: BRIEF.demo
  * **range**: 第1—4卷


# Dynamic N-Line 总图

### `LINE.merchant_escape` **商队自救线** (状态: `ACTIVE`)
- **Line Owner**: `CHAR.guqinghe` | **主线诉求**: 护住伙计并把残页交给可信的公堂
- **外部压强与对抗力量**: 鲁敬山派人封锁船队 | 对抗方: 替罪羊叙事和内部恐慌
- **里程碑演进**: 转移残页、交出假账诱出追兵、拒绝让伙计顶罪
- **高潮触发**: 顾青禾必须公开承认自己改过一张运单 | **闭环结算条件**: 残页与船队证词共同指向鲁敬山

### `LINE.public_investigation` **公开查粮线** (状态: `ACTIVE`)
- **Line Owner**: `CHAR.shenyan` | **主线诉求**: 让账证进入公堂并保住粮路
- **外部压强与对抗力量**: 上级提前结案期限 | 对抗方: 鲁敬山的程序封锁
- **里程碑演进**: 封门查粮、公开赤粮司印、公堂对质
- **高潮触发**: 沈砚必须在保仕途和公开证据间选择 | **闭环结算条件**: 赈粮亏空归因成立且新监管机制生效


# 多线碰撞矩阵

- （条目已在前置章节展开）

# 全书剧情梗概

### `EVENT.move_fragment` **转移账册残页**
- **主导者/行动方**: `CHAR.guqinghe` | **发生地点**: `LOC.east_warehouse` | **时间窗口**: `第二日清晨`
- **核心行动**: 顾青禾把残页藏进药箱，借病粮例外转移到东平码头
- **所作抉择**: 放弃一船粮，保住唯一证据 | **付出代价**: 船队损失当日现银并引发伙计不满
- **产生状态变化(Delta)**: 账册残页进入顾青禾控制的暗仓
- **因果链**: `EVENT.seal_gate` $\longrightarrow$ `EVENT.public_confrontation`

### `EVENT.open_accounts` **公开账证**
- **主导者/行动方**: `CHAR.shenyan` | **发生地点**: `LOC.south_gate` | **时间窗口**: `第四日清晨`
- **核心行动**: 沈砚承认旧令责任，公开残页并要求按印章批次复核入库记录
- **所作抉择**: 沈砚放弃升迁机会，选择把调查权限交给三方见证 | **付出代价**: 县令职位被暂缓复核，县衙失去独断权
- **产生状态变化(Delta)**: 账证闭环成立，地方粮运改为三方留痕
- **因果链**: `EVENT.public_confrontation` $\longrightarrow$ `PROMISE.relief_truth`、`CLIMAX.public_record`

### `EVENT.public_confrontation` **公堂对质**
- **主导者/行动方**: `CHAR.lujingshan` | **发生地点**: `LOC.south_gate` | **时间窗口**: `第三日午后`
- **核心行动**: 鲁敬山在公堂先展示运单，再逼顾青禾承认改单
- **所作抉择**: 鲁敬山引用自己签发的旧令压过现场证词 | **付出代价**: 旧令编号被完整记录在案
- **产生状态变化(Delta)**: 替罪羊叙事获得短暂优势，但鲁敬山留下可追溯签批
- **因果链**: `EVENT.move_fragment`、`EVIDENCE.red_seal` $\longrightarrow$ `EVENT.open_accounts`

### `EVENT.seal_gate` **封门查粮**
- **主导者/行动方**: `CHAR.shenyan` | **发生地点**: `LOC.south_gate` | **时间窗口**: `第一日傍晚`
- **核心行动**: 沈砚在南城门下令查验粮车，并援引病粮例外放行一车药粮
- **所作抉择**: 牺牲官场信用换取半日调查窗口 | **付出代价**: 县衙被上级认定为拖延
- **产生状态变化(Delta)**: 顾青禾的出城路线被迫转入东平码头
- **因果链**: `RULE.curfew_order`、`OBJECT.ledger_fragment` $\longrightarrow$ `EVENT.move_fragment`


# 全书主因果链

- （条目已在前置章节展开）

# 伏笔、悬念、揭示和兑现地图

### `PROMISE.relief_truth` **赤粮司印的真正含义** (状态: `PAID_OFF`)
- **埋设事件**: `EVENT.seal_gate` $\to$ **揭示窗口**: `第四日公堂` $\to$ **兑现事件**: `EVENT.open_accounts`
- **信息差博弈**: 先知者 `CHAR.guqinghe` vs 误解/受蒙蔽者 `CHAR.shenyan、CHAR.lujingshan`
- **成熟发酵条件**: 残页数字、印章批次和旧令编号在同一张证词中出现
- **兑现后余波与爽点结算**: 赈粮亏空可追溯到鲁敬山代理账房


# 全书时间线

- （条目已在前置章节展开）

# 空间、移动、资源和信息流

- （条目已在前置章节展开）

# 高潮、低谷和规则变化地图

- `CLIMAX.public_record` **三方留痕公案** [CLIMAX]
  * **irreversible_change**: 县衙、船队和粮司共同留痕
  * **provenance_refs**: BRIEF.demo
  * **trigger**: 沈砚公开承认旧令责任


# 卷级架构与每卷因果脊柱

- `VOLUME.south_gate` **南门卷** [VOLUME]
  * **core_question**: 账册残页能否在粮路断裂前成为公共证据
  * **provenance_refs**: BRIEF.demo


# 全章 Story Nodes

- （条目已在前置章节展开）

# 指定窗口详细章纲

### 第 1 章: `CHAPTER.1` **第一章《南门封粮》** (所属卷: `VOLUME.south_gate` | 评级: `FULL`)

- **章节功能定位**: 让沈砚第一次用程序换取调查窗口，同时切断顾青禾的安全退路
- **核心不可逆状态变化(Core Delta)**: 封门令生效，账册残页进入转移路线，沈砚失去上级信任
- **戏剧矛盾对峙**: `沈砚要冻结可疑粮车并保住病粮通道` vs `鲁敬山要用限期结案压缩调查空间` —— 核心不可调和点: 既要冻结证据又要保住全部粮路在当前权限下不能同时成立
- **动态节拍链 (Dynamic Beats)**:
  * **[BEAT.1 - ACTION]**: 主角行动 `沈砚在南城门下令查验粮车，并公开援引病粮例外` $\to$ 对手反制 `鲁敬山的限期结案公文先一步抵达` $\to$ 带来变化: {"authority": "上级信任下降", "goal": "调查窗口暂时打开"}
  * **[BEAT.2 - COUNTERMOVE]**: 主角行动 `鲁敬山提前派人封住正门并要求立即交出账册` $\to$ 对手反制 `沈砚把查验记录当众交给三名见证人` $\to$ 带来变化: {"knowledge": "沈砚确认对手在控制信息", "risk": "冲突公开化"}
  * **[BEAT.3 - REPLAN]**: 主角行动 `顾青禾把残页藏进药箱，改走东平码头` $\to$ 对手反制 `放弃一船粮才能避开搜查` $\to$ 带来变化: {"available_path": "转入暗仓", "resource": "损失一船粮"}
  * **[BEAT.4 - COST]**: 主角行动 `顾青禾主动交出一页假账，引导搜查队追错方向` $\to$ 对手反制 `鲁敬山借假账制造她私改运单的口实` $\to$ 带来变化: {"evidence": "获得一条反向证据", "relationship": "与伙计的信任受损"}
- **场景对峙切片 (Scene Payloads)**:
  * `SCENE.chapter1.gate`: 入口 `亏空存在但证据尚未公开` $\to$ 对峙焦点 `病粮、官位和证据同时受威胁` $\to$ 出口 `正门封锁，调查窗口打开`
  * `SCENE.chapter1.warehouse`: 入口 `顾青禾原有出城路线失效` $\to$ 对峙焦点 `一船粮、残页和伙计生计只能保住两项` $\to$ 出口 `残页暂存暗仓，顾青禾被迫面对公堂`
- **章末继续力 / 悬念钩子**: 假账让顾青禾暂时保住残页，却把她推入必须公开承认改单的公堂
- **禁止漂移与水文约束**: 不得新增决定性证据、不得让鲁敬山突然亲自接触残页
- **容量审计与抗水审查**: `capacity_audit={"chapter_id": "CHAPTER.1", "core_scenes": 2, "failure_reasons": [], "final_capacity": "FULL", "mid_chapter_load": "PASS", "missing_middle_roles": [], "payload_clusters": 2, "stageable_core_beats": 4, "summary_result_beats_removed": 0, "supporting_stageable_beats": 0, "target_prose_range": [4000, 6000], "writer_core_plot_invention_required": false}`


# 关键人物、道具、证据、地点和规则来源表

- `EVIDENCE.red_seal` **倒置的赤粮司印** [EVIDENCE]
  * **meaning**: 显示赈粮在入库前已被重新过秤
  * **provenance_refs**: BRIEF.demo

- `OBJECT.ledger_fragment` **赈粮账册残页** [OBJECT]
  * **material_constraint**: 水浸后只能辨认印章和三行数字
  * **owner_history**: 鲁敬山代理账房、顾青禾、沈砚保管
  * **provenance_refs**: BRIEF.demo


# 开放余波与禁止漂移清单

- （条目已在前置章节展开）

# 负事实与禁止漂移

- `夜间封门令不能覆盖病粮例外`
- `没有无来源的第七名关键人物`
- `鲁敬山没有亲自接触账册残页`

# 关系与因果边

- `EDGE.c1` `CAUSES`: **封门查粮** $\to$ **转移账册残页** — {"reason": "封门迫使转移"}
- `EDGE.c2` `CAUSES`: **转移账册残页** $\to$ **公堂对质** — {"reason": "残页进入公案"}
- `EDGE.c3` `CAUSES`: **公堂对质** $\to$ **公开账证** — {"reason": "旧令编号可追溯"}
- `EDGE.climax` `REALIZES`: **公开账证** $\to$ **三方留痕公案** — {}
- `EDGE.l1` `OWNS_LINE`: **沈砚** $\to$ **公开查粮线** — {}
- `EDGE.l2` `OWNS_LINE`: **顾青禾** $\to$ **商队自救线** — {}
- `EDGE.l3` `COLLIDES_WITH`: **公开查粮线** $\to$ **商队自救线** — {"shared_resource": "OBJECT.ledger_fragment"}
- `EDGE.p1` `PARTICIPATES_IN`: **沈砚** $\to$ **封门查粮** — {"role": "initiator"}
- `EDGE.p10` `PARTICIPATES_IN`: **倒置的赤粮司印** $\to$ **公堂对质** — {"role": "evidence"}
- `EDGE.p11` `PARTICIPATES_IN`: **沈砚** $\to$ **公开账证** — {"role": "initiator"}
- `EDGE.p12` `PARTICIPATES_IN`: **鲁敬山** $\to$ **公开账证** — {"role": "target"}
- `EDGE.p13` `PARTICIPATES_IN`: **赈粮账册残页** $\to$ **公开账证** — {"role": "evidence"}
- `EDGE.p14` `PARTICIPATES_IN`: **南城门** $\to$ **公开账证** — {"role": "location"}
- `EDGE.p2` `PARTICIPATES_IN`: **顾青禾** $\to$ **封门查粮** — {"role": "target"}
- `EDGE.p3` `PARTICIPATES_IN`: **赈粮账册残页** $\to$ **封门查粮** — {"role": "evidence"}
- `EDGE.p4` `PARTICIPATES_IN`: **南城门** $\to$ **封门查粮** — {"role": "location"}
- `EDGE.p5` `PARTICIPATES_IN`: **顾青禾** $\to$ **转移账册残页** — {"role": "initiator"}
- `EDGE.p6` `PARTICIPATES_IN`: **赈粮账册残页** $\to$ **转移账册残页** — {"role": "evidence"}
- `EDGE.p7` `PARTICIPATES_IN`: **东平码头仓** $\to$ **转移账册残页** — {"role": "location"}
- `EDGE.p8` `PARTICIPATES_IN`: **鲁敬山** $\to$ **公堂对质** — {"role": "initiator"}
- `EDGE.p9` `PARTICIPATES_IN`: **顾青禾** $\to$ **公堂对质** — {"role": "target"}
- `EDGE.pays` `PAYS_OFF`: **公开账证** $\to$ **赤粮司印的真正含义** — {}
- `EDGE.r1` `OPPOSES`: **沈砚** $\to$ **鲁敬山** — {"asymmetry": "沈砚求公开证据，鲁敬山求控制叙事"}
- `EDGE.r2` `TRANSACTS_WITH`: **顾青禾** $\to$ **沈砚** — {"exchange": "证据换合法文书"}
- `EDGE.t1` `PRECEDES`: **封门查粮** $\to$ **转移账册残页** — {}
- `EDGE.t2` `PRECEDES`: **转移账册残页** $\to$ **公堂对质** — {}
- `EDGE.t3` `PRECEDES`: **公堂对质** $\to$ **公开账证** — {}
- `EDGE.v1` `BELONGS_TO`: **封门查粮** $\to$ **南门卷** — {}
- `EDGE.v2` `BELONGS_TO`: **公开账证** $\to$ **赈粮危机幕** — {}
