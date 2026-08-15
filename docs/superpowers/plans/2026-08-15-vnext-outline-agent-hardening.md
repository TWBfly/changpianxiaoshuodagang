# VNext Outline Agent Hardening Implementation Plan
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task with verification checkpoints.

**Goal:** 修复 VNext 长篇大纲运行时的状态一致性、可审计性、图检索、人物活人感字段、细纲容量闸门与输出可读性问题；保持纯本地、只写大纲、不接 Ollama 或第三方 API。

**Architecture:** SQLite Canon 是唯一写入真相源；每次提交明确为 `SNAPSHOT` 或 `PATCH`，保存完整快照与删除 outbox；Neo4j 只作可重建投影和只读检索，失败时显式降级；审计器在提交前阻止断因果、断人物能动性、断来源和不具备生产容量的细纲；Markdown 由结构化字段生成一次性总纲。

**Tech Stack:** Python 3 标准库、SQLite、Neo4j `cypher-shell`（可选本地投影）、unittest、Markdown。

## Global Constraints

- 不增加第三方 Python 依赖，不调用 Ollama、云模型或外部 API。
- 所有用户输入在 `audit_packet` 和 `CanonicalStore` 边界校验；失败不得写入部分状态。
- Canon 变更可重放、可重建图；图不可用时不能伪报成功。
- 每个非平凡修复先补失败测试，再实现，再运行全量测试与技能校验。

## Task 1: 明确快照/补丁语义并修复 CLI

**Files:** `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`, `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`

**Interfaces:** `packet.packet_mode` accepts `SNAPSHOT` (default) and `PATCH`; `CanonicalStore.apply_packet` performs exact replacement for snapshots, overlay for patches; repeated identical snapshot is idempotent; `audit --packet` does not instantiate a store without a database.

**Tests:** snapshot deletion, patch overlay, idempotent version, malformed list/ref rejection, raw packet audit exit code, deterministic timeline ordering.

## Task 2: 完整快照历史、删除 outbox、并发与重建入口

**Files:** `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`, `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`, `.agents/skills/vnext-outline-agent/graph/projection.cypher`

**Interfaces:** `commits.snapshot_json` 保存完整 Canon；SQLite 使用 `BEGIN IMMEDIATE`；DELETE 变更含 `before_json`；新增 `CanonicalStore.rebuild_changes` 与 CLI `graph-rebuild`，可从当前 Canon 重新产生全量投影变化。

**Tests:** 删除实体/边、历史快照可读、重复提交不增版本、重建变化覆盖全部实体边。

## Task 3: Neo4j 只读检索与项目隔离

**Files:** `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`, `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`, `.agents/skills/vnext-outline-agent/graph/queries.cypher`

**Interfaces:** `context --source sqlite|neo4j|auto`；Neo4j 查询全部带 `project_id`；`auto` 在本地凭据缺失时返回 SQLite 上下文并附 `GRAPH_DEGRADED`，`neo4j` 强制显式失败；新增 `GraphProjector.rebuild`。

**Tests:** 查询脚本项目过滤、未配置图时 auto 降级、neo4j 强制错误、重建入口调用。

## Task 4: 人物活人感、关系生命周期、因果与细纲容量闸门

**Files:** `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`, `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`, `.agents/skills/vnext-outline-agent/scripts/demo_packet.json`, `.agents/skills/vnext-outline-agent/references/output-contract.md`

**Interfaces:** CORE/MAJOR 人物必须有 `biography`, `decision_model`, `private_life`, `life_constraints`, `arc`, `fate`, `highlights`；关系/线/承诺引用必须存在且状态闭合；`CHAPTER_PLAN`/`BEAT` 支持 `STORY_NODE`、`DETAILED_PLAN`、`PRODUCTION_READY` 三档与动态节拍、群像线、场景承载、扩写和中段负荷检查。

**Tests:** 缺人物生平/私生活失败、闭合线状态一致性失败、生产就绪细纲容量失败/通过、因果输入输出与边不一致失败。

## Task 5: 总纲输出、运行文档与证据

**Files:** `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`, `.agents/skills/vnext-outline-agent/SKILL.md`, `.agents/skills/vnext-outline-agent/references/runtime-core.md`, `.agents/skills/vnext-outline-agent/projects/PROJECT.demo/audit-report.md`

**Interfaces:** Markdown 渲染每个实体只出现一次，补充契约元数据、人物决策卡、因果链、时间线、线/承诺闭合状态和图降级状态；文档记录新命令与 packet_mode。

**Verification:** `python3 -m unittest discover -s .agents/skills/vnext-outline-agent/scripts -p 'test_*.py' -v`; `python3 -m py_compile ...`; `python3 /Users/tang/.codex/skills/skill-creator/scripts/quick_validate.py .agents/skills/vnext-outline-agent`。

## Self-review

- 先用现有 SQLite、标准库和已有查询入口，不引入服务层、ORM 或新依赖。
- 将无法在无模型条件下完成的“自然语言创作”保留为上游 packet 输入；运行时只负责结构化规划、校验、保存、检索和导出。
- 图投影永远可由 Canon 重建，避免把 Neo4j 当第二写入真相源。
