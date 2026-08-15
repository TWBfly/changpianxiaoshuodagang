# VNext Outline Runtime 修复设计

## 目标

把当前的结构化 Canon 原型修复为能够阻止“字段齐全但剧情不足”的章节大纲运行时：统一 Packet 契约，逐章执行独立容量审计，检查全书章节完整性，导出可读的章节大纲，并修复已确认的数据与图投影缺陷。

## 范围

- 保留 Python 标准库、SQLite、可选本地 Neo4j 和现有 CLI。
- 不加入模型 API、网页、服务层或第三方依赖。
- Python 只做结构化校验；语义创作仍由上游 Codex 生成 Packet。
- 生产 Packet 显式设置 `precision.full_book_detailed_required=true`，把全书章节视为需要详细章纲；仅索引 Packet 可设置为 `false`。

## 核心契约

统一使用 `payload` 与 `provenance_refs`。章节实体必须包含 `chapter_no`、`volume_ref`、`target_prose_contract`、`chapter_function`、`core_delta`、`conflict_contract`、`dynamic_beats`、`payload_clusters`、`scene_payloads`、`explicit_compression`、`continuation_source` 和 `forbidden_drift`。

Beat 必须标记 `stageability`。只有 `STAGEABLE_CORE` 和 `SUPPORTING_STAGEABLE` 进入容量计算；每个可演 Beat 必须有前因、主动者、动作、反作用、选择/新信息和 Delta。Scene 必须有入口状态、目标、反作用、转向、出口状态和 Payload Cluster 引用。

## 独立容量审计

审计器不接受 Packet 自填的 `FULL`、`PASS` 或 `anti_self_certification` 作为证据。它根据事实结构计算：可演 Beat、被剥离的 Summary/Result/Ledger、Payload Cluster、Scene Delta、中段 Action/Countermove/Replan/Cost 链和 Writer 核心剧情发明需求。

`STANDARD_LONG` 默认目标为 4000–6000 字。生产级最低结构要求为：至少 2 个 Payload Cluster、至少 2 个 Core Scene、至少 4 个 Core Beat；中段必须保留 Action、Countermove、Replan、Cost。未满足则不得为 `PRODUCTION_READY`。

## 完整性与基础修复

- 章节号唯一、连续；全书详细模式下所有章节必须存在且通过容量审计。
- 修复缺失锚点崩溃、边 payload 校验、namespace/status 校验和重复超边参与者。
- Neo4j 使用项目复合唯一约束；边 payload 不把用户字段直接展开为 Cypher Map key。
- 仅为实际变化写 Outbox。
- 导出章节结构和容量审计证据，人物总表保留稳定 ID。

## 验收

- 伪造的结果句章节必须失败。
- 中段空心章节必须失败。
- 结构完整的最小长章必须通过。
- 缺章节、重复章节、非连续章节必须失败。
- 缺失锚点返回 `INSUFFICIENT`，不抛异常。
- 全量测试、编译、契约检查和 demo 导出通过。
