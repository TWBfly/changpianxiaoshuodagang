# Outline Runtime 修复 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans (recommended). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复章节 Packet 契约、独立容量审计、全书完整性、导出和已确认的 SQLite/Neo4j/上下文缺陷。

**Architecture:** SQLite 仍是唯一 Canon；新增纯函数式章节容量审计和全书完整性审计，结果由结构事实计算而非 Packet 自证。Neo4j 只做项目隔离的可重建投影，Markdown 展示结构化章节和审计证据。

**Tech Stack:** Python 3 标准库、SQLite、Neo4j cypher-shell、unittest。

## Global Constraints

- 不增加第三方依赖，不调用模型 API。
- 所有行为先写失败测试，再实现。
- 不把章节数量 KPI 当作文学质量；容量门只拒绝明显不足的结构。
- 保留现有版本、快照、Outbox 和降级语义。

## Task 1: ChapterPlan contract and independent capacity audit

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`
- Modify: `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`

**Interfaces:**
- `audit_chapter_capacity(entity: dict) -> dict`
- `audit_chapter_set(packet: dict) -> list[dict]`
- `audit_packet` rejects invalid chapter structure and computed non-production-ready plans.

- [ ] Write failing tests for a fake result-only chapter, a middle-empty chapter, a valid minimal long chapter, and a missing ChapterPlan in full-book mode.
- [ ] Run the focused tests and confirm they fail for the current self-certification gate.
- [ ] Implement the smallest structured validators and computed audit payload.
- [ ] Run focused and full tests.

## Task 2: Canonical packet validation and known runtime bugs

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`
- Modify: `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`

- [ ] Add failing tests for missing anchors, invalid edge payloads, invalid namespace/status, duplicate hyperedge participants, and unchanged Outbox rows.
- [ ] Implement the guards and diff-aware Outbox append.
- [ ] Run the full test suite.

## Task 3: Markdown/demo/contracts

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/demo_packet.json`
- Modify: `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Modify: `.agents/skills/vnext-outline-agent/references/runtime-core.md`
- Modify: `.agents/skills/vnext-outline-agent/references/output-contract.md`
- Modify: `.agents/skills/vnext-outline-agent/SKILL.md`
- Modify: `projects/PROJECT.demo/audit-report.md`

- [ ] Add a valid structured chapter to the demo packet.
- [ ] Fix renderer duplication and include chapter capacity evidence and stable IDs.
- [ ] Align documentation with the canonical packet schema.
- [ ] Re-run demo export and update release evidence with reproducible commands.

## Task 4: Neo4j project isolation and input safety

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`
- Modify: `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Modify: `.agents/skills/vnext-outline-agent/graph/constraints.cypher`
- Modify: `.agents/skills/vnext-outline-agent/graph/projection.cypher`

- [ ] Add failing tests for project-scoped identity and safe edge payload serialization.
- [ ] Implement composite project identity and fixed Cypher map keys.
- [ ] Run unit, compile, and contract checks.

## Task 5: Final verification

- [ ] Run all tests and `py_compile`.
- [ ] Run a clean demo init/apply/audit/export sequence.
- [ ] Inspect diff and report remaining limitations.
