---
name: vnext-outline-agent
description: Use when creating, auditing, repairing, or integrating a Chinese long-form novel outline with named characters, multi-line plot causality, time/space consistency, provenance, and Neo4j-backed narrative memory. This skill writes outlines and structured planning data, never prose, and uses only local Python, SQLite, and optional local Neo4j.
---

# VNext long-form outline agent

## Purpose

Produce an executable, auditable outline rather than novel prose. The runtime is
`.agents/skills/vnext-outline-agent/scripts/outline_agent.py`; it is standard
library Python and has no model, Ollama, remote API, or third-party service
dependency.

## Non-negotiable invariants

- Every person is a named `CHAR.*` entity with identity, biography, desire,
  goal, interests, constraints, strategy, agency, growth, highlights, fate,
  and provenance. Never emit placeholders such as 路人甲/乙.
- `CORE`/`MAJOR` characters additionally carry a lived biography, private life,
  life constraints, decision model, arc, highlights, and fate.
- Characters act from their own goals. A plot beat must have an active actor or
  an explicit world process; do not add people, objects, clues, or rescues from
  nowhere.
- `Canon` is committed truth. `Plan` is intended future structure. Candidates
  stay outside Canon until selected. Every important fact, event, promise, and
  relation has provenance and stable IDs.
- Events are hyperedges: represent one N-ary event as an `EVENT.*` entity plus
  `PARTICIPATES_IN` relations carrying roles (initiator, target, evidence,
  location, witness, beneficiary, etc.). Do not flatten an event into unrelated
  binary facts.
- Causal inputs/outputs, temporal order, spatial access, negative facts, and
  promise lifecycle must be explicit. Reject cycles, orphan events, broken
  references, unresolved promises, and unexplained late arrivals.
- A packet is explicitly `SNAPSHOT` (omitted Canon is deleted) or `PATCH`
  (omitted Canon is preserved); repeated snapshots are idempotent.
- Neo4j is a rebuildable projection, not the source of truth. SQLite is the
  transaction ledger and outbox. If local Neo4j cannot authenticate/connect,
  record `DEGRADED` and surface the reason; never claim graph sync succeeded.

## Workflow

1. Read the user brief and the existing outline. Extract constraints and
   unresolved decisions; do not write prose.
2. Build or update a packet with `CHAR`, `EVENT`, `PROP`, `LOC`, `LINE`, and
   `PROMISE` entities plus typed edges. Include `time.valid_from/to` and
   `space.location_id` wherever applicable.
3. Run the state machine: `STATE → AGENCY → SEARCH → SELECT → OUTLINE →
   INTEGRATE`. Keep candidate packets separate until selection.
4. Validate before commit. Fix the first reported `ValidationError`; do not
   bypass validation or silently drop information.
5. Commit the complete packet to SQLite, then enqueue/project its outbox
   changes to local Neo4j. Query bounded neighborhoods and causal paths for
   later phases; keep retrieval IDs and provenance in the context packet.
6. Export stable Markdown and an audit report. The final outline must contain
   character dossiers/topology, plot synopsis and act/line beats, causal and
   foreshadowing tables, timeline, locations, promises/payoffs, negative facts,
   and unresolved risks.

## Commands

Run from the novel project directory:

```bash
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py init \
  --db .outline/novel.db --project-id novel-001 --title '项目名'
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py apply \
  --db .outline/novel.db --project-id novel-001 --packet packet.json \
  --expected-version 0 --message '初始大纲'
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py context \
  --db .outline/novel.db --project-id novel-001 --anchor CHAR.a \
  --anchor EVENT.1 --max-hops 2 --source auto
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py audit \
  --db .outline/novel.db --project-id novel-001
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py graph-sync \
  --db .outline/novel.db --project-id novel-001
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py graph-rebuild \
  --db .outline/novel.db --project-id novel-001
python3 .agents/skills/vnext-outline-agent/scripts/outline_agent.py export \
  --db .outline/novel.db --project-id novel-001 --out outline.md
```

Use `NEO4J_URI`/`NEO4J_ADDRESS`, `NEO4J_USER` or `NEO4J_USERNAME`, and
`NEO4J_PASSWORD` only for a local Neo4j instance. The projection uses
`cypher-shell` and the checked-in Cypher allowlist; no driver, APOC, GDS, or
remote endpoint is required.

## Failure handling

Handle `INVALID_PACKET`, `STALE_VERSION`, `CAUSAL_CYCLE`,
`NEO4J_SHELL_NOT_FOUND`, `NEO4J_TIMEOUT`, `NEO4J_QUERY_FAILED`, and
`QUERY_NOT_ALLOWED` as actionable states. Preserve the SQLite commit and mark
the graph outbox `DEGRADED` when Neo4j is unavailable. Include the error code,
object ID, and provenance in the user-facing audit.

Read [runtime-core.md](references/runtime-core.md) for packet and graph rules
and [output-contract.md](references/output-contract.md) for the stable export
shape before changing the runtime.
