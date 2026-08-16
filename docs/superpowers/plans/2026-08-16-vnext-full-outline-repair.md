# VNext Full-Book Outline Repair Implementation Plan

> **For agentic workers:** Execute this plan inline in the current checkout; existing uncommitted user changes must be preserved.

**Goal:** Prevent the VNext outline Agent from claiming a complete long-form outline when it only has a generic summary and one chapter, and make the runtime/export contract require an explicit synopsis, volume plot, full chapter coverage, and production-ready 4000–6000-character chapter plans.

**Architecture:** Keep the current zero-dependency Python/SQLite Canon. Add deterministic scope, hierarchy, density, duplication, and export-order checks to `outline_agent.py`; update `SKILL.md` so Codex produces the required artifacts in order and in batches; regenerate the target packet only after the final merged packet passes the full-book gate.

**Tech Stack:** Python 3 standard library, `unittest`, SQLite, JSON, Markdown export; no model API or new dependency.

## Global Constraints

- Full-book mode must declare `precision.full_book_detailed_required=true` and a positive `expected_chapters`.
- Every chapter number from `1..expected_chapters` must have a `PRODUCTION_READY` `CHAPTER_PLAN`.
- Every 4000–6000-character chapter must contain at least 6 stageable core beats, 3 payload clusters, and 3 core scenes.
- Every volume must declare its chapter range, detailed plot, central conflict, turning points, payoff, and next-volume hook.
- The exported document must show one-sentence synopsis, volume detail, chapter index, and all detailed chapters in that order.
- Do not change the existing SQLite schema or add third-party dependencies.

---

### Task 1: Lock the missing full-outline behavior with failing tests

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`
- Test: the same file with `python3 .agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- Tests call `audit_packet`, `audit_chapter_capacity`, and `render_packet_markdown`.
- Later tasks make these tests pass without weakening the existing 58-test suite.

- [ ] **Step 1: Add tests for the required contract**

  Add focused tests for:

  ```python
  def test_full_book_requires_synopsis_scope_and_volume_details():
      packet = build_full_book_packet(expected_chapters=2, chapter_numbers=[1, 2])
      packet["entities"][0]["payload"].pop("one_sentence_synopsis")
      report = audit_packet(packet)
      self.assertIn("PROJECT_SYNOPSIS_MISSING", {item["code"] for item in report.errors})

  def test_full_book_rejects_missing_chapter_even_when_one_chapter_is_valid():
      packet = build_full_book_packet(expected_chapters=2, chapter_numbers=[1])
      report = audit_packet(packet)
      self.assertIn("CHAPTER_PLAN_MISSING", {item["code"] for item in report.errors})

  def test_full_book_rejects_thin_long_chapter():
      packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
      packet["entities"][-1]["payload"]["dynamic_beats"] = packet["entities"][-1]["payload"]["dynamic_beats"][:4]
      report = audit_packet(packet)
      self.assertIn("CHAPTER_PAYLOAD_SHORTFALL", {item["code"] for item in report.errors})

  def test_export_has_synopsis_volume_index_then_detailed_chapters():
      text = render_packet_markdown(build_full_book_packet(expected_chapters=2, chapter_numbers=[1, 2]))
      self.assertLess(text.index("全书一句话总纲"), text.index("卷级详细剧情"))
      self.assertLess(text.index("卷级详细剧情"), text.index("全章目录与推进表"))
      self.assertLess(text.index("全章目录与推进表"), text.index("指定窗口详细章纲"))
  ```

  Add a small helper packet that contains one `PROJECT`, one complete `VOLUME`, and reusable production-ready chapter payloads. The helper must intentionally omit one required field in each test instead of mocking the validator.

- [ ] **Step 2: Run the new tests and verify RED**

  Run:

  ```bash
  python3 .agents/skills/vnext-outline-agent/scripts/test_outline_agent.py
  ```

  Expected: the new tests fail with missing error codes or missing export headings; existing tests remain visible so regressions are distinguishable.

### Task 2: Add deterministic scope, volume, and chapter-density audits

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- Add `audit_outline_scope(packet) -> list[dict]`.
- Add `audit_volume_entity(entity, chapter_numbers) -> list[dict]`.
- Extend `audit_chapter_capacity(entity)` while preserving its returned keys.

- [ ] **Step 1: Implement the smallest scope validator**

  Require in full-book mode:

  ```text
  PROJECT.payload.one_sentence_synopsis
  PROJECT.payload.causal_summary
  precision.expected_chapters >= 1
  precision.expected_volumes >= 1
  at least one VOLUME per expected volume
  each VOLUME: chapter_start, chapter_end, detailed_plot, central_conflict,
               turning_points, payoff, next_hook
  ```

  Emit machine-readable errors: `PROJECT_SYNOPSIS_MISSING`, `OUTLINE_SCOPE_MISSING`, `VOLUME_PLAN_MISSING`, `VOLUME_DETAIL_MISSING`, and `VOLUME_RANGE_INVALID`.

- [ ] **Step 2: Strengthen full-book chapter coverage**

  Keep the existing positive-number, uniqueness, production-ready, and contiguous `1..N` checks. Add `CHAPTER_VOLUME_MISMATCH` when a chapter number falls outside its referenced volume range, and `CHAPTER_COUNT_MISMATCH` when the declared volume ranges do not cover exactly `1..expected_chapters`.

- [ ] **Step 3: Raise long-chapter evidence thresholds**

  For `STANDARD_LONG` and `MAJOR_LONG`, require at least 6 `STAGEABLE_CORE` beats, 3 payload clusters, and 3 scenes. Require at least two distinct active actors across core beats, at least two non-empty `new_information_or_choice` values, and at least two distinct `delta` dimensions across the chapter. Emit `CHAPTER_PAYLOAD_SHORTFALL`, `CHAPTER_ACTOR_DIVERSITY_SHORTFALL`, or `CHAPTER_INFORMATION_SHORTFALL`.

- [ ] **Step 4: Add repetition checks without pretending to judge literary quality**

  Within a chapter reject duplicate `beat_id`, duplicate action text, and duplicate core-delta text. Across chapters in full-book mode reject identical `chapter_function` plus `core_delta` pairs with `DUPLICATE_CHAPTER_BEAT_PATTERN`. This is a deterministic anti-template floor, not a semantic originality score.

- [ ] **Step 5: Run focused tests and the full suite**

  Run:

  ```bash
  python3 .agents/skills/vnext-outline-agent/scripts/test_outline_agent.py
  ```

  Expected: all new tests and all existing tests pass.

### Task 3: Make Markdown export reflect the required hierarchy

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`
- Modify: `.agents/skills/vnext-outline-agent/references/output-contract.md`

**Interfaces:**
- Extend `SECTION_ORDER` with `全书一句话总纲`, `卷级详细剧情`, and `全章目录与推进表`.
- Keep `render_packet_markdown(packet, title, project_id) -> str` as the public renderer.

- [ ] **Step 1: Add deterministic renderers**

  Render the project synopsis and causal summary as prose, render volumes sorted by `chapter_start`, render chapter index rows sorted by `chapter_no`, then render detailed chapter plans sorted by `chapter_no`. Chapter plans must not be consumed by the compact index section.

- [ ] **Step 2: Include completion telemetry in the document header**

  Show declared volumes, declared chapters, actual detailed chapters, and `COMPLETE`/`INCOMPLETE` status. A partial packet must visibly say `INCOMPLETE` even when it is valid as an intermediate phase packet.

- [ ] **Step 3: Run export-order tests**

  Run:

  ```bash
  python3 .agents/skills/vnext-outline-agent/scripts/test_outline_agent.py
  ```

### Task 4: Rewrite the Skill workflow so the producer cannot bypass the contract

**Files:**
- Modify: `.agents/skills/vnext-outline-agent/SKILL.md`
- Modify: `.agents/skills/vnext-outline-agent/references/output-contract.md`
- Modify: `.agents/skills/vnext-outline-agent/references/runtime-core.md`

**Interfaces:**
- The Skill must produce packets accepted by the runtime without manually disabling full-book checks.
- Packet phases are `SCOPE`, `VOLUMES`, `CHAPTER_INDEX`, `CHAPTER_BATCH`, and `FINAL_FULL_BOOK`.

- [ ] **Step 1: Replace the six-phase prose with an explicit production sequence**

  Require:

  ```text
  source mechanism extraction and originality divergence
  → project one-sentence synopsis and causal summary
  → freeze volume count, chapter count, and ranges
  → write every volume's detailed plot
  → write the full chapter index
  → write all chapter plans in numbered batches
  → merge with PATCH packets
  → set full_book_detailed_required=true only for final audit/export
  ```

- [ ] **Step 2: Define the chapter packet minimum in plain language**

  State that a title and one-line result are not a chapter plan. Every chapter must identify named active characters, scene-specific opposition, at least six live beats, information changes, choices, costs, relation/resource changes, and a continuation hook that is not a generic “stronger enemy appears”.

- [ ] **Step 3: Add explicit originality gates**

  Require a divergence table covering protagonist wound, world engine, antagonist strategy, relationship engine, progression currency, and final moral choice. Reject direct reuse of source names, signature scenes, or copied reveal order; preserve only high-level mechanisms.

### Task 5: Regenerate and verify the target outline

**Files:**
- Modify: `高手下山，我有九个无敌师父-仿写大纲.md`
- Modify: `.outline/guimen_packet.json`
- Modify: `audit-report.md`

**Interfaces:**
- The final packet must set `full_book_detailed_required=true` and declare the actual chapter count.
- The output must contain every chapter from `1..N`, not just a detailed window.

- [ ] **Step 1: Replace the old one-chapter packet with a complete scoped packet**

  Choose and freeze a new original story scale after the volume plan is written; do not copy the source novel's chapter count. Every volume gets a chapter range and detailed plot before chapter plans are created.

- [ ] **Step 2: Apply, audit, and export**

  Run:

  ```bash
  python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py apply --db .outline/novel.db --project-id PROJECT.guimen --expected-version <current> --packet .outline/guimen_packet.json --message '完整分卷与逐章大纲修复'
  python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py audit --db .outline/novel.db --project-id PROJECT.guimen
  python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py export --db .outline/novel.db --project-id PROJECT.guimen --out '高手下山，我有九个无敌师父-仿写大纲.md'
  ```

- [ ] **Step 3: Verify requirements and regressions**

  Run:

  ```bash
  python3 .agents/skills/vnext-outline-agent/scripts/test_outline_agent.py
  rg -n '^# (全书一句话总纲|卷级详细剧情|全章目录与推进表|指定窗口详细章纲)' '高手下山，我有九个无敌师父-仿写大纲.md'
  rg -n 'INCOMPLETE|CHAPTER_PLAN_MISSING|final_capacity.: .THIN' audit-report.md '高手下山，我有九个无敌师父-仿写大纲.md'
  ```

  Expected: tests pass, the output headings appear in order, no incomplete marker remains in the final export, and the audit reports zero hard errors.
