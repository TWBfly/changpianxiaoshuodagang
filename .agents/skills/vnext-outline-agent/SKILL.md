---
name: vnext-outline-agent
description: Use when creating, auditing, repairing, or integrating a Chinese long-form commercial web novel outline (商业长篇网文大纲) with named characters, multi-line plot causality, information asymmetry matrix, dopamine/tension waveform, time/space consistency, and Neo4j-backed narrative memory. This skill writes structured planning data and production outlines, using local Python, SQLite, and optional local Neo4j.
---

# VNext Commercial Web Novel Outline Agent (商业长篇网文大纲进化系统)

## Purpose & Core Philosophy

Produce an executable, auditable, highly gripping commercial web novel outline (百万字商业网文大纲).
The core of web novel writing lies in:
1. **Information Asymmetry (信息差动力学)**: Who knows what, who is deceived, dramatic irony, counter-schemes, and timely truth explosions.
2. **Expectancy, Pressure & Payoff (期待-压强-反转-爽点兑现)**: Relentless tension accumulation, irreversible choices, decisive payoffs (打脸/升级/获宝/破局), and irresistible chapter-ending hooks (追读力).
3. **Progression Ladder (欲望与阶梯成长)**: Clear power/status/faction progression ceilings with meaningful stakes.
4. **Anti-Water Stageable Payload (抗水文高承载剧情)**: Every beat must contain live action, counterforce, information update, relation repricing, or irreversible sacrifice.

The deterministic runtime is `.agents/skills/vnext-outline-agent/scripts/outline_agent.py` (zero external dependencies, runs locally with Python and SQLite).

## Non-negotiable Invariants

- **Named Active Agents**: Every individual actor must be a named `CHAR.*` entity with identity, desires, goals, interests, constraints, strategy, agency, growth, highlights, and fate. Never emit placeholders (路人甲/乙).
- **Theory of Mind & Information Asymmetry**: Characters act strictly on their own bounded knowledge and misjudgments. Secrets and foreshadowing (`PROMISE.*`) must track `who_knows`, `who_misunderstands`, `maturity_condition`, `reveal_window`, and `post_payoff_state`.
- **Dynamic Multi-Line Matrix**: Plot lines (`LINE.*`) have explicit Owners, opposing forces, milestones, climax triggers, and closure conditions.
- **Stageable Chapter Payload & Anti-Water Rules**: `CHAPTER_PLAN` must carry target prose contract (4000-6000字), core delta, concrete conflict (`actor_a` vs `actor_b`), dynamic beats (`ACTION`, `COUNTERMOVE`, `REPLAN`, `COST`, `SETUP`, `PRESSURE`, `CLIMAX`, `PAYOFF`, `FACE_SLAP`, `REVELATION`, `HOOK`), scene payloads, and continuation hooks.
- **Transactional Canon & Rebuildable Graph**: SQLite is the authoritative truth ledger. Neo4j is a rebuildable query projection. Repeated snapshots are idempotent.
- **Full-book completeness**: A packet is not a finished outline until it contains one-sentence synopsis, causal summary, explicit volume ranges and detailed volume plots, a complete chapter index, and a `PRODUCTION_READY` plan for every chapter from `1..expected_chapters`.
- **Originality gate**: Preserve only high-level mechanisms from a reference work. Rebuild names, world engine, protagonist wound, antagonist strategy, relationship engine, progression currency, reveal order, set pieces, and ending choice. Reusing signature scenes or source-specific names is a hard failure of the creative workflow.
- **No false completion**: `precision.production_stage=FINAL_FULL_BOOK` must set `full_book_detailed_required=true`; otherwise the runtime rejects the packet. Intermediate packets must remain visibly `INCOMPLETE` when exported.

## Full-Book Production Workflow (完整长篇大纲生产流水线)

Long novels are still written in batches to avoid context overflow, but batching is only an execution detail. The final packet must merge every batch and pass the complete-book gate.

1. **Source mechanism extraction and originality divergence**
   - Extract only high-level reader mechanisms such as return, revenge, hidden assets, escalation, information asymmetry, and immediate payoff.
   - Create an originality table with at least six changed axes: protagonist wound, world engine, antagonist strategy, relationship engine, progression currency, reveal order, and ending choice.
   - Quarantine source-specific names, signature scenes, iconic lines, exact chapter sequence, and distinctive set pieces. They cannot enter the new packet.
2. **Scope Contract**
   - Decide and freeze `expected_volumes`, `expected_chapters`, and contiguous `chapter_start/chapter_end` ranges before writing chapter plans.
   - If the user has not supplied a scale, derive a proposed scale from the new story's causal capacity and present it for confirmation; never copy the source novel's chapter count.
   - Create one `PROJECT` with `one_sentence_synopsis` and `causal_summary`.
3. **World, character, and line architecture**
   - Define rules, ceilings, factions, locations, resources, named active characters, information asymmetry, dynamic lines, promises, and climax nodes.
   - Every major character needs a decision model, private life, constraints, misjudgments, arc, highlights, and fate. A woman or ordinary person cannot exist only as a trigger or reward.
4. **Volume Plans and Master Outline**
   - For every volume, write `chapter_start`, `chapter_end`, `detailed_plot`, `central_conflict`, `turning_points`, `payoff`, and `next_hook`.
   - Write the complete one-sentence causal synopsis first, then the volume plots, then the cross-volume cause/effect chain. Do not jump straight to a chapter.
5. **Complete Chapter Index**
   - Create a `CHAPTER_PLAN` for every number from `1..expected_chapters`, at least with a unique title, volume, named actors, chapter function, core delta, and continuation hook.
   - The index is not a substitute for detail. It is the coverage checklist used to prevent a one-chapter packet from being mislabeled as a full book.
6. **Detailed Chapter Batches**
   - Fill every indexed chapter with a `PRODUCTION_READY` payload. Each 4000–6000-character chapter needs at least 6 stageable core beats, 3 payload clusters, 3 scenes, 2 active actors, 2 information/choice updates, and multiple delta dimensions.
   - Every beat must contain cause, active actor, action, counterforce, new information or choice, delta, before/after goal, and next pressure. Summary, ledger, travel, inventory, repeated reaction, and result-only text do not count.
   - Apply batches with `PATCH`, but only set `precision.production_stage=FINAL_FULL_BOOK` and `full_book_detailed_required=true` after all chapter numbers are present.
7. **Final audit and export**
   - Run `audit`, require zero hard errors, then run `export`.
   - The Markdown must visibly contain: one-sentence synopsis, detailed volume plots, full chapter index, and all detailed chapter plans in numeric order.
   - If Neo4j is unavailable, keep SQLite Canon as the source of truth and report graph state as `DEGRADED`; never present a degraded graph projection as successful.

## Commands

Run from the novel project directory:

```bash
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py init \
  --db .outline/novel.db --project-id novel-001 --title '书名'
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py apply \
  --db .outline/novel.db --project-id novel-001 --packet packet.json \
  --expected-version 0 --message 'Phase提交说明'
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py context \
  --db .outline/novel.db --project-id novel-001 --anchor CHAR.a \
  --anchor EVENT.1 --max-hops 2 --source auto
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py audit \
  --db .outline/novel.db --project-id novel-001
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py graph-sync \
  --db .outline/novel.db --project-id novel-001
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py export \
  --db .outline/novel.db --project-id novel-001 --out outline.md
```

Read [runtime-core.md](references/runtime-core.md) and [output-contract.md](references/output-contract.md) for full schema details. A packet that only contains a master summary or one detailed chapter is an intermediate packet, never a finished outline.
