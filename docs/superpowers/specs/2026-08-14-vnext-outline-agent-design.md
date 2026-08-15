# VNext 长篇大纲 Agent 设计规格

## 1. 目标

将 `Agent_VNext16.2大纲系统.md` 从一份自然语言规范收敛为可在 Codex 中直接运行的长篇大纲 Skill。Agent 从用户题材、核心设想或既有材料出发，分阶段构建世界、人物、人物关系、动态幕线、因果链、伏笔、时间与空间结构，最终输出信息完整、可追踪、可继续细化的 Master Outline。

本项目只生产大纲，不生产小说正文。大纲中的语言生成、创意判断和语义审查由当前 Codex Agent 完成；Python 运行时只负责结构化存储、确定性校验、版本、检索与导出。

## 2. 用户硬约束

1. 任何出场并承担对白、判断、行动、关系或因果作用的个体，都必须拥有稳定 ID、正式姓名和明确身份。
2. 禁止使用“路人甲、路人乙、官员 A、护卫一、神秘人”等个体占位符。
3. 群体可以作为 Cohort 存在，例如“灾民”“码头工人”，但 Cohort 不能代替承担个人关键选择的具体人物。
4. 每个有叙事作用的人物必须拥有自己的认知、欲望、目标、利益、约束、策略、关系与主观能动性。
5. 核心和重要人物必须具备可解释当前行为的生平、成长史、性格成因、人物弧、高光路径和命运路径。
6. 情节由人物、势力或已经运行的世界过程推动，禁止先指定剧情结果再反填人物动机。
7. 大纲必须包含剧情梗概、剧情脉络、转折、高潮、低谷、悬念、揭示、结局和余波。
8. 采用动态 N 幕 N 线；幕数和线数由故事需要产生，不使用固定三幕、九线或平均配额。
9. 群像线必须拥有独立 Owner、目标、阻力、发展与结算，并在自然条件下发生碰撞。
10. 人物、道具、证据、能力、地点、机构和规则承担关键因果作用前，必须已有可追踪来源。
11. 禁止天降人物、天降道具、天降证据、未声明规则、突兀转折和为了剧情而剧情。
12. 所有关键事件必须符合世界规则、常识、资源、权限、信息、时间、距离和人物能力。
13. 每条主因果链必须有来源、发展、变化、结果与后续影响；不能只有时间相邻。
14. 所有伏笔必须有载体、影响、成熟条件、揭示窗口、兑现与兑现后的新状态。
15. 所有长期剧情线、人物命运和核心承诺必须结算，或明确记录有意保留的开放余波。
16. 最终整合时必须使用稳定 ID 和交叉引用，禁止摘要覆盖或丢失前序阶段产生的信息。

以上规则属于项目级 Hard Contract；与原 VNext 文档中允许匿名 Ephemeral Actor、固定 Three-Act Macro 或正文生产相关的默认规则冲突时，以本节为准。

## 3. 原始规范分析

### 3.1 可直接继承的核心

原规范最有价值的结构不是大量评分字段，而是以下七条可执行原则：

1. `Canon / Plan / Candidate` 分域，未来设想不得污染已经确认的事实。
2. 先恢复当前世界与人物状态，再推导人物意图，最后生成剧情候选。
3. 候选先通过 Story Legality、Character Truth、Reader Integrity 三道不可平均的硬门。
4. 合格候选只比较 Truth、Current Value、Change-or-Investment、Novelty、Future Fertility 五个上位目标。
5. 人物由生平因果、当前欲望、认知偏差、利益、约束、关系和选择历史共同驱动。
6. 长篇采用动态多线，要求 Line Owner、生命周期、自然碰撞和关闭条件。
7. 世界、人物、道具、证据、机构和规则需要 Provenance，关键事件需要完整因果链。

### 3.1A 论文对本项目的直接启发

`2602.05665v1.pdf` 将 Graph-based Agent Memory 拆成抽取、存储、检索、演化四个生命周期，并明确指出不同图结构解决不同问题：

- Knowledge Graph 适合实体、事实和可解释的多跳关系；
- Temporal Graph 适合 valid time 与 transaction time 分离；
- Hypergraph 适合一个事件同时涉及多个人物、道具、资源、权限和地点的 N-ary 关系，避免拆成二元边后丢失共同成立条件；
- Hierarchical Graph 适合 Project → Volume → Chapter → Scene → Event 的上下钻取；
- Hybrid Graph 适合把稳定知识和动态经历、结构检索和语义检索分开。

因此，本项目采用 Neo4j Property Graph 作为图投影，并用事件节点加角色参与边表达超图的 incidence 结构。Neo4j 本身不是原生超图数据库，不能把一条关系直接连接任意数量节点；通过事件/关系节点重化（reification）可以保留 N-ary 事件整体，而不把它错误拆成若干互相独立的二元因果。

### 3.2 原规范不能直接执行的部分

1. 文件有 12,576 行，但目标目录没有代码、机器入口或完整数据 Schema；它是规范，不是程序。
2. 大量模块只是自然语言职责，同一字段在不同章节重复出现，直接逐模块照搬会形成同一模型换身份自评的委员会系统。
3. 原规范只有 Graph Narrative Memory 的 JSON Schema，人物、关系、剧情线、伏笔、时间、空间和 Master Outline 缺少统一机器契约。
4. `SPECULATIVE_CANDIDATE → DEFERRED_EXPERIENCE` 出现在状态转换说明中，但 `DEFERRED_EXPERIENCE` 不在 Memory Unit 的状态枚举里，不能原样实现。
5. “隔离上下文二次审查”可以降低锚定偏差，但仍是同一模型推断，不能被标成认识论独立证据。
6. 49A 参数矩阵为正文生产和多步 Rollout 预留了大量调用预算；本项目不写正文，也不调用外部模型，因此不应照搬。
7. 原初版本不实现正文 Writer、Telemetry、RFR 和正文摩擦编译；本次修复补入最小的 OSD/DPC 章节结构容量审计，以阻止结果句冒充可扩写章纲。
8. 原规范同时强调远期滚动规划和全书详细章纲，两者存在张力。本设计用“全书结构完整、远期精度分层、当前窗口可细化”解决。

### 3.3 收敛结论

实现保留五核思想，但把运行时压缩为一个 Codex Skill 和一个确定性 Python 工具，不部署多个常驻 Agent：

```text
STATE
→ AGENCY
→ SEARCH
→ SELECT
→ OUTLINE INTEGRATE
```

语义创作由 Codex 完成；Python 不尝试用规则拼接故事。Python 只拒绝结构上可确定的错误，例如匿名关键人物、断裂引用、缺失来源、未关闭剧情线、时间倒置和不合法状态转换。

## 4. 采用方案

采用“分阶段大纲编译器”：

```text
用户输入
→ 项目契约
→ 世界宪法
→ 人物宇宙
→ 人物关系拓扑
→ 人物自主行动模型
→ 动态 N 幕 N 线
→ 因果链 / 伏笔 / 高潮低谷
→ 时间 / 空间约束
→ 卷级架构 / 章节 Story Nodes
→ 完整性审计
→ Master Outline
```

拒绝两个替代方案：

- 单一超长 Prompt：实现短，但长篇状态会被上下文挤压，无法保证引用和版本一致。
- 多 Agent 委员会：模块更多但没有独立证据来源，增加信息复制、冲突和运行仪式。

## 5. 技术栈

### 5.1 创作宿主

- Codex Skill：负责交互、分阶段创作、语义推断、候选比较、语义审计和修复。
- Skill 仅加载当前阶段需要的规则和上下文，不把 12,576 行原文整份塞入每轮上下文。

### 5.2 本地运行时

- Python 3.11+ 标准库。
- `argparse`：命令行入口。
- `sqlite3`：唯一 Canon、对象、关系、版本和审计记录。
- `json`：Skill 与运行时之间的数据包格式。
- `dataclasses`、`enum`、`typing`：内部数据契约。
- `hashlib`：快照与导出内容校验。
- `pathlib`、`tempfile`、`os.replace`：路径处理和原子导出。
- `unittest`：零依赖回归测试。
- Neo4j Community/本地单机实例：人物、事件、道具、关系、因果、时间和多元事件的图投影。
- `cypher-shell`：由 Python 通过受控子进程执行本地 Cypher；不引入 Neo4j Python Driver，不调用远程 HTTP API。

### 5.3 存储与检索

- SQLite 保存唯一 Canon、事务版本、变更记录和图投影 Outbox；它是事实源，不是第二套图事实。
- Neo4j 保存由 Canon 投影得到的 Property Graph，承担人物拓扑、因果路径、时间窗口、伏笔链、多线碰撞和多跳检索。
- 复合事件以 `Event` 节点作为超边重化节点；`PARTICIPATES_IN` 边携带 `role`、证据和有效时间，保留参与者集合的整体语义。
- 检索顺序为：命名空间/版本过滤 → 精确实体锚点 → Neo4j 类型边扩展 → 时间约束 → 反事实/负事实过滤 → 原始证据回溯。
- 首版不实现向量检索、GDS 学习排序或图神经网络；Codex 负责语义候选，Neo4j 负责可解释结构检索。
- Markdown 只作为交付物，不作为唯一事实源。

### 5.4 明确不使用

- 不使用任何第三方或本地模型 API。
- 不使用 Ollama、HTTP 服务、WebSocket 或云服务。
- 不使用 Neo4j Python Driver、Neo4j Aura、远程 HTTP API、APOC、GDS、NetworkX、向量数据库或 Agent 框架。
- Neo4j 仅使用本机数据库和 `cypher-shell`；它是本地基础设施，不是第三方生成 API。
- 不构建网页前端。
- 不生成小说正文。

## 6. 物理结构

计划创建：

```text
.agents/skills/vnext-outline-agent/
├── SKILL.md
├── references/
│   ├── runtime-core.md
│   └── output-contract.md
├── graph/
│   ├── constraints.cypher
│   ├── projection.cypher
│   └── queries.cypher
└── scripts/
    ├── outline_agent.py
    └── test_outline_agent.py

changpianxiaoshuodagang/projects/<project-slug>/
├── outline.db
├── packets/
├── master-outline.md
└── audit-report.md
```

职责：

- `SKILL.md`：唯一执行入口、阶段顺序、上下文读取规则和失败回退规则。
- `runtime-core.md`：从 VNext16.2 提炼后的本项目规范，只保留会改变大纲合法性或质量的规则。
- `output-contract.md`：每阶段必须产出的字段、稳定 ID 和最终 Markdown 结构。
- `graph/constraints.cypher`：Neo4j 唯一 ID、类型和投影索引约束。
- `graph/projection.cypher`：从 Canon Outbox 幂等写入节点、边和超边参与关系。
- `graph/queries.cypher`：人物拓扑、因果路径、时间过滤、伏笔回溯和线碰撞查询。
- `outline_agent.py`：初始化、应用数据包、查询上下文、审计、快照和导出。
- `test_outline_agent.py`：一个标准库测试文件，覆盖关键状态与审计逻辑。
- `outline.db`：唯一结构化事实源。
- `packets/`：Codex 当前阶段生成的数据包和审计输入，便于人工查看与恢复。
- `master-outline.md`：面向用户的完整整合大纲。
- `audit-report.md`：硬错误、警告、未决假设和修复记录。

## 7. 数据架构

### 7.1 命名空间

首版只保留三个命名空间：

```text
CONTRACT  用户确认的项目硬约束
CANON     已确认的世界、人物与既定事实
PLAN      尚未写成正文但已批准的大纲安排
```

候选只存在于当前 Packet；未选候选进入审计记录，不进入活跃事实表。由于本项目不生产正文，PLAN 不自动升级为 CANON。

### 7.2 稳定 ID

```text
PROJECT.*
CHAR.*
COHORT.*
FACTION.*
LOC.*
RESOURCE.*
PROP.*
EVIDENCE.*
RULE.*
ACT.*
VOLUME.*
LINE.*
EVENT.*
PROMISE.*
CLIMAX.*
```

ID 一经提交不随改名变化。人物别名和曾用名指向同一 `CHAR.*`。

### 7.3 SQLite 事务层

首版使用四张核心表；`changes` 同时承担 Graph Projection Outbox：

1. `entities`：保存项目、人物、群体、地点、势力、资源、道具、规则、幕、卷、剧情线、事件、伏笔和高潮节点；类型专有数据存为规范化 JSON payload。
2. `edges`：保存人物关系、隶属、因果、时间、空间、所有权、知识、伏笔、线归属和命运连接。
3. `commits`：保存版本、父版本、消息、时间和 Frozen Snapshot Hash。
4. `changes`：保存每次提交中对象或边的前后值、投影状态和错误；状态为 `PENDING → APPLIED` 或 `DEGRADED`。

SQLite 只保存一套事实。Neo4j、Markdown 和查询缓存都是投影；投影失败不得回写或修改 Canon。

### 7.4 Neo4j Property Graph 与超图投影

#### 节点

所有节点携带：

```text
id、kind、namespace、status、name、valid_from、valid_to、
transaction_from、transaction_to、source_ids、canon_version、checksum
```

常用标签：

```text
Project、Character、Cohort、Faction、Location、Resource、Object、
Evidence、Rule、Act、Volume、Line、Event、Promise、Climax、Timepoint
```

#### 二元关系

```text
PART_OF、OWNS、USES、LOCATED_AT、KNOWS、BELIEVES、OPPOSES、
DEPENDS_ON、PRECEDES、CAUSES、ENABLES、BLOCKS、REQUIRES、
TRIGGERS、TRANSFORMS、FORESHADOWS、REVEALS、PAYS_OFF、
CREATES_DEBT、CHANGES_RELATION、CHANGES_RESOURCE
```

关系同样携带 `namespace`、有效时间、来源和置信/状态字段。

#### 超图重化

复合事件不拆成“人物 A 导致人物 B、人物 B 使用道具 C”这类会丢失共同条件的孤立二元事实，而是：

```text
(:Character {id:'CHAR.A'})
  -[:PARTICIPATES_IN {role:'initiator'}]->(:Event {id:'EVENT.001'})
(:Character {id:'CHAR.B'})
  -[:PARTICIPATES_IN {role:'target'}]->(:Event {id:'EVENT.001'})
(:Object {id:'PROP.KEY'})
  -[:PARTICIPATES_IN {role:'evidence'}]->(:Event {id:'EVENT.001'})
(:Location {id:'LOC.GATE'})
  -[:PARTICIPATES_IN {role:'location'}]->(:Event {id:'EVENT.001'})
(:Event {id:'EVENT.001'})-[:CAUSES]->(:Event {id:'EVENT.002'})
```

`EVENT.001` 的 payload 保存前置条件、权限、资源、时限、动作、结果、状态变化和证据。这个事件节点就是超边的重化表示；参与边的 `role` 保留人物、道具、地点和资源的不同语义。没有事件语义但存在 N-ary 关系时使用 `HyperRelation` 节点，规则相同。

#### 双时间与版本

- `valid_from / valid_to`：故事世界内事实或事件成立的时间。
- `transaction_from / transaction_to`：Canon 从哪个版本开始承认或失效。
- `namespace`：`CONTRACT`、`CANON`、`PLAN`。
- `status`：`ACTIVE`、`SUPERSEDED`、`INVALIDATED`、`QUARANTINED`。

Neo4j 中失效事实不删除，只更新状态和 transaction interval；查询默认过滤失效投影。

### 7.5 关键实体契约

#### 人物

每个 `CHAR.*` 至少包含：

```text
name、identity、life_stage、origin、formative_events、
personality_causal_summary、desires、goals、interests、protected_assets、
beliefs、blind_spots、capabilities、constraints、risk_tolerance、
preferred_strategy、fallback_strategy、private_life、current_state、
arc、highlight_path、fate_path、line_ownership
```

核心人物要求完整生平因果；重要人物允许 Biography Lite，但不能缺欲望、利益和行动算法。

#### 人物关系

关系边是有方向、可非对称、可多类型的：

```text
from_character、to_character、relation_types、origin_event、
public_definition、from_side_definition、to_side_definition、
shared_interest、conflicting_interest、dependence、leverage、trust、
exit_cost、betrayal_gain、current_state、change_conditions
```

禁止用单一“好感度”代替关系。

#### 剧情线

每条 `LINE.*` 至少包含：

```text
owner、origin、goal、pressure、opposing_force、resources、
information_state、milestones、reversals、collisions、
climax_condition、closure_condition、failure_outcome、residue、status
```

生命周期：

```text
PROPOSED → ACTIVE → HEATING → COLLIDING → CLIMAX_READY
→ CLOSING → CLOSED → RESIDUE_ONLY
```

#### 事件

每个关键 `EVENT.*` 至少包含：

```text
active_actor、actor_goal、causal_inputs、action、counterforce、choice、
cost、state_delta、causal_outputs、time_window、location、line_refs、
provenance_refs、reader_question、status
```

事件必须描述“谁做了什么导致变化”，不能只保存“关系恶化”“损失惨重”等结果句。

#### 伏笔

每个 `PROMISE.*` 至少包含：

```text
creation_event、carrier、who_knows、who_misunderstands、
reinforcement_events、choices_affected、maturity_condition、
reveal_window、payoff_event、post_payoff_state、status
```

#### 时间与空间

- 时间使用故事内顺序键和可选绝对时间；事件的因果父节点必须早于或等于事件发生窗口。
- 地点保存控制者、进入条件、移动边、通信边、时间成本、资源和自然冲突。
- 跨地点事件必须存在合法移动或通信路径。

## 8. Agent 执行流程

### 阶段 0：初始化

创建项目目录和数据库，记录原始需求、明确约束、合理假设、开放变量和禁止事项。输入不足时先采用可撤销假设继续；只有会改变题材、终局或核心伦理边界的问题才阻塞。

### 阶段 1：Project / World Contract

生成题材、时代、技术或力量上限、经济、制度、信息、交通、地理、叙事视角、语言风格和禁止漂移项。每条关键规则拥有 `RULE.*`。

### 阶段 2：人物宇宙

先构建核心人物，再由利益和世界需求推导重要人物、势力与 Cohort。人物不能由“某章需要一个人”临时创建。

对每个个体执行：

```text
过去经历
→ 对世界的解释
→ 欲望 / 利益 / 恐惧
→ 当前目标
→ 首选与备选策略
→ 可承担的代价
→ 可能的成长、退化或命运
```

### 阶段 3：人物拓扑与自主行动

建立双向可非对称关系边，检查主角缺席时其他人物是否仍会行动。至少存在由非主角人物、对手、势力或世界过程发起的重要事件。

### 阶段 4：动态 N 幕 N 线

幕数由世界规则或人物策略发生不可逆变化的阶段数决定；线数由独立人物目标、势力过程、关系压力、秘密、资源与终局矛盾决定。

每条线必须有 Owner、自然推进源、里程碑、转折、高潮条件和关闭条件。生成 Line Collision Matrix，只有共享资源、地点、时间窗口、人物或互斥目标时才允许碰撞。

### 阶段 5：剧情候选与选择

在主要结构节点先恢复状态和到期压力，再生成机制真正不同的候选。候选依次通过：

```text
Story Legality
Character Truth
Reader Integrity
```

合格候选按五目标做序位比较，不做伪精确加权总分。保留冠军、亚军、决定性差异和延期代价。

### 阶段 6：因果、伏笔、高潮与命运

构建从根条件到终局和余波的主因果链。将人物命运节点、线碰撞、伏笔成熟、高潮与低谷挂接到具体前置资产。任何高潮都必须改变规则、关系、资源、身份、选择空间或人物自我定义。

### 阶段 7：时间与空间编译

检查人物个人时间线、世界过程时间线、地点网络、旅行时间、通信速度、资源流和信息流。不能用转场文字掩盖移动、权限或信息不可能。

### 阶段 8：卷章架构

默认输出精度：

```text
全书：完整故事结构与终局
每卷：详细因果脊柱、人物弧、线碰撞、高潮和承接
每章：Story Node，明确主动者、行动、阻力、选择和状态变化
当前用户指定窗口：可进一步生成详细章纲
```

不写正文；但用户要求的 4000—6000 字章节大纲必须通过结构化 Dramatic Payload Capacity Audit 才能标记为 `PRODUCTION_READY`。

### 阶段 9：图投影、整合与审计

事务提交后由 `changes` Outbox 驱动 Neo4j 幂等投影；随后运行人物拓扑、事件超边、因果路径、时间一致性、伏笔链和多线碰撞查询。按照稳定 ID 聚合全部实体与边，运行确定性审计和 Codex 语义审计。硬错误修复完毕后导出 Master Outline 和 Audit Report。

## 9. 最终 Master Outline 结构

```text
1. 项目总契约与禁止事项
2. 世界观与风格宪法
3. 世界规则、时代、技术或力量上限
4. 地理、交通、通信、资源与信息网络
5. 势力和机构生态
6. 全人物总表
7. 核心与重要人物生平、性格成因和决策模型
8. 人物关系拓扑
9. 人物弧、高光与命运地图
10. N 幕宏观结构
11. Dynamic N-Line 总图
12. 多线碰撞矩阵
13. 全书剧情梗概
14. 全书主因果链
15. 伏笔、悬念、揭示和兑现地图
16. 全书时间线
17. 空间、移动、资源和信息流
18. 高潮、低谷和规则变化地图
19. 卷级架构与每卷因果脊柱
20. 全章 Story Nodes
21. 指定窗口详细章纲
22. 关键人物、道具、证据、地点和规则来源表
23. 开放余波与禁止漂移清单
```

## 10. 审计规则

### 10.1 硬错误

```text
UNNAMED_CAUSAL_ACTOR
PLACEHOLDER_PERSON
CHARACTER_WITHOUT_AGENCY
CHARACTER_WITHOUT_DESIRE_OR_INTEREST
AUTHOR_DRIVEN_EVENT
HEAVEN_DROPPED_ENTITY
MISSING_PROVENANCE
WORLD_RULE_BREACH
INFORMATION_TELEPORT
IMPOSSIBLE_TRAVEL
ORPHAN_EVENT
CAUSAL_ORDER_CONFLICT
UNOWNED_NARRATIVE_LINE
DECORATIVE_THREAD
UNRESOLVED_CORE_PROMISE
UNLINKED_CHARACTER_FATE
UNCLOSED_MAJOR_LINE
PLAN_CANON_CONTAMINATION
BROKEN_REFERENCE
```

任一硬错误存在时不得标记为完整大纲。

### 10.2 警告

```text
PROTAGONIST_GRAVITY_COLLAPSE
PASSIVE_OPPOSITION
RELATIONSHIP_AS_LABEL_ONLY
REPEATED_CONFLICT_MECHANISM
CLIMAX_WITHOUT_RULE_CHANGE
LOWPOINT_WITHOUT_CHOICE_COST
FORESHADOW_WITHOUT_PRIOR_EFFECT
OVERDETAILED_REMOTE_CHAPTER
OPEN_ASSUMPTION
```

警告必须在 Audit Report 中解释接受、修复或延期原因。

### 10.3 语义审计边界

Python 可以确定引用、枚举、状态、顺序和图连接是否有效，但不能确定人物是否真正动人、转折是否俗套或剧情是否优秀。这些由 Codex Skill 基于具体内容进行二次语义审查，并明确标记为 `SAME_AGENT_REVIEW`，不伪装成独立证据。

## 11. 错误恢复与信息保护

1. 数据包先在内存中校验，通过后才开启 SQLite 事务。
2. 每次写入必须携带 `expected_version`；版本不一致则拒绝提交。
3. 更新不覆盖历史，`changes` 保存前后值。
4. 导出文件先写临时文件，再原子替换。
5. 任何删除默认转为 `SUPERSEDED` 或 `INVALIDATED`，不物理抹除。
6. 导出前验证所有引用均能解析。
7. Master Outline 的每个重要小节都保留实体 ID，避免同名人物或改名导致信息串线。
8. 阶段上下文由数据库查询生成，不依赖 Agent “大概记得”。
9. Neo4j 投影失败时保留 Canon 提交并标记 `DEGRADED`；下一次 `graph-sync` 从 Outbox 重放，不允许把不完整图当作完整运行结果。
10. 图投影只接受 `CANON` 和已批准 `PLAN`，拒绝候选、推断和旧版本污染。

## 12. 测试策略

只使用 `unittest`，保留一个测试文件。

必须覆盖：

1. 初始化产生版本 0 和空项目。
2. 合法数据包原子提交并递增版本。
3. 旧 `expected_version` 被拒绝且数据库不发生部分写入。
4. 未命名或占位个体触发硬错误。
5. 缺少欲望、利益或主动策略的人物触发硬错误。
6. 关键道具或人物缺 Provenance 时触发硬错误。
7. 断裂边、孤立事件和未关闭主线被发现。
8. 时间顺序或跨地点移动不可能被发现。
9. 伏笔可以从创建事件追踪到揭示和兑现。
10. 人物关系支持非对称定义和多种关系类型。
11. 导出的 Markdown 顺序稳定、引用完整，同一数据库重复导出结果一致。
12. 提交失败后历史版本和快照 Hash 不变。
13. Neo4j 投影可幂等重放；同一 `entity_id + canon_version` 不产生重复节点或关系。
14. 复合事件查询能一次返回完整参与者集合、角色、资源、地点、条件、结果和证据，而不是碎片边。

另提供一个最小示例项目作为集成测试数据，包含两名核心人物、一名重要对手、两个地点、两条剧情线、一个伏笔和一个完整因果闭环。

## 13. 完成标准

交付完成必须同时满足：

1. Skill 能从一个最小故事设想启动完整分阶段流程。
2. Python CLI 能初始化、应用 Packet、查询、审计、快照和导出。
3. 所有自动化测试通过。
4. 示例项目能导出结构完整的 Master Outline。
5. 无第三方生成依赖、无远程 API、无 Ollama、无网络请求；图能力使用本机已安装的 Neo4j 与 `cypher-shell`。
6. 硬错误存在时 CLI 返回非零退出码且不输出“完整大纲”。
7. 人物、剧情线、事件、伏笔、时间、空间和来源信息能够通过稳定 ID 互相追踪。
8. 最终输出不包含“路人甲、路人乙”等匿名个体占位符。

## 14. 刻意不做

- 不实现正文 Writer 或正文润色；实现章节大纲层面的 4000—6000 字 Dramatic Payload Capacity Audit。
- 不实现网页界面、后台服务或并行多 Agent。
- 不实现向量检索、Embedding、Telemetry、读者行为预测或自动学习规则。
- 不实现 Neo4j GDS/APOC 或原生超图算法；首版以事件节点重化、Cypher 结构查询和可追溯证据为超图能力边界。
- 不提前生成并锁死 1000 章生产级细纲；远期以完整 Story Node 和卷级因果约束保持可重规划性。
- 不把所有 VNext16.2 字段搬入数据库；字段只有在能改变大纲合法性、检索、审计或最终交付时才进入运行时。

若以后需要写正文、多人并发编辑、跨项目语义检索或真实读者数据校准，再分别扩展，不在本版本预留空架构。
