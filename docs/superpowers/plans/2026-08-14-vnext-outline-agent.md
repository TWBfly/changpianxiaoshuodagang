# VNext Long-Form Outline Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Codex Skill plus a zero-remote-API Python runtime that preserves a long-form outline as versioned Canon, validates characters/causality/timeline/provenance, projects it to local Neo4j, represents compound events as hyperedges, and exports a complete Markdown Master Outline.

**Architecture:** SQLite is the single transactional source of truth. Neo4j is an idempotent graph projection driven by the SQLite change outbox; compound events are represented as reified `Event` nodes with role-bearing `PARTICIPATES_IN` incidence edges. The Codex Skill performs semantic story construction in stages and sends JSON packets to the deterministic runtime for validation, commit, graph sync, retrieval, audit, and export.

**Tech Stack:** Codex Skill; Python 3.11+ standard library (`argparse`, `sqlite3`, `json`, `dataclasses`, `enum`, `typing`, `hashlib`, `pathlib`, `subprocess`, `unittest`); local Neo4j 2026.03.1 through `cypher-shell`; Markdown.

## Global Constraints

- No Ollama, remote model, HTTP API, WebSocket, cloud service, Neo4j Aura, Neo4j Python Driver, APOC, GDS, NetworkX, Pydantic, SQLAlchemy, vector database, or web frontend.
- Neo4j is local infrastructure only; Python invokes the installed `cypher-shell` executable with bounded input and never sends data to a remote service.
- SQLite is the only Canon source; Neo4j and Markdown are rebuildable projections.
- Every individual actor with dialogue, judgment, action, relationship, or causal effect has a stable ID, real name, and identity; placeholder names are hard errors.
- Every important character has desire, goal, interest, constraint, strategy, relationship state, biography cause, arc, highlight path, and fate path.
- Every important entity and event has provenance; every compound event preserves its participant roles as one hyperedge projection.
- Candidate, Plan, and Canon data remain isolated; unselected candidates never enter live Canon.
- No prose generation; output is outline data and Markdown outline only.
- Every non-trivial branch has one runnable `unittest` check before implementation is considered complete.
- This workspace is not a Git repository; use test/checkpoint output instead of commit commands.

---

## File Map

Create the following files under `changpianxiaoshuodagang/`:

```text
.agents/skills/vnext-outline-agent/SKILL.md
.agents/skills/vnext-outline-agent/references/runtime-core.md
.agents/skills/vnext-outline-agent/references/output-contract.md
.agents/skills/vnext-outline-agent/graph/constraints.cypher
.agents/skills/vnext-outline-agent/graph/projection.cypher
.agents/skills/vnext-outline-agent/graph/queries.cypher
.agents/skills/vnext-outline-agent/scripts/outline_agent.py
.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py
projects/<project-slug>/outline.db
projects/<project-slug>/packets/
projects/<project-slug>/master-outline.md
projects/<project-slug>/audit-report.md
```

`outline_agent.py` is intentionally one runtime file: the first version has one executable boundary and no speculative package hierarchy. The Skill files are instruction/data contracts; the runtime does not generate story text.

## Task 1: Runtime Skeleton and Canon Schema

**Files:**
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- Produces `CanonicalStore`, `CommitResult`, `AuditReport`, `ValidationError`, and CLI parser used by all later tasks.
- `CanonicalStore(db_path: Path)` opens SQLite with foreign keys and WAL.
- `CanonicalStore.init_project(project_id: str, title: str) -> int` creates schema and returns version `0`.
- `CanonicalStore.apply_packet(project_id: str, packet: dict, expected_version: int, message: str) -> CommitResult` is the only write entry point.
- `CanonicalStore.get_version(project_id: str) -> int` returns the current integer version.

- [ ] **Step 1: Write the failing tests**

```python
import tempfile
import unittest
from pathlib import Path

from outline_agent import CanonicalStore, ValidationError


class CanonicalStoreTests(unittest.TestCase):
    def test_init_creates_version_zero_and_empty_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            self.assertEqual(store.init_project("PROJECT.demo", "Demo"), 0)
            self.assertEqual(store.get_version("PROJECT.demo"), 0)

    def test_stale_expected_version_is_rejected_without_partial_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            packet = {"entities": [], "edges": []}
            store.apply_packet("PROJECT.demo", packet, 0, "first")
            with self.assertRaises(ValidationError):
                store.apply_packet("PROJECT.demo", packet, 0, "stale")
            self.assertEqual(store.get_version("PROJECT.demo"), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the expected failure**

Run:

```bash
cd changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts
python3 -m unittest -v test_outline_agent.CanonicalStoreTests
```

Expected: FAIL with `ModuleNotFoundError: No module named 'outline_agent'`.

- [ ] **Step 3: Implement the minimal schema and write path**

Implement `outline_agent.py` with these SQLite tables:

```sql
CREATE TABLE IF NOT EXISTS projects(
  project_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entities(
  project_id TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  namespace TEXT NOT NULL,
  status TEXT NOT NULL,
  name TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY(project_id, entity_id),
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS edges(
  project_id TEXT NOT NULL,
  edge_id TEXT NOT NULL,
  edge_type TEXT NOT NULL,
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  namespace TEXT NOT NULL,
  status TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY(project_id, edge_id),
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS commits(
  project_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  parent_version INTEGER,
  message TEXT NOT NULL,
  snapshot_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY(project_id, version)
);
CREATE TABLE IF NOT EXISTS changes(
  change_id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  action TEXT NOT NULL,
  before_json TEXT,
  after_json TEXT NOT NULL,
  projection_status TEXT NOT NULL DEFAULT 'PENDING',
  projection_error TEXT,
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
```

`apply_packet` must validate `expected_version`, insert all objects and edges in one transaction, insert a commit row with SHA-256 of canonical JSON, append outbox rows, increment the project version, and roll back every write on any error.

- [ ] **Step 4: Run the tests and verify they pass**

Run the command from Step 2. Expected: `2 tests ... OK`.

- [ ] **Step 5: Run the full runtime smoke check**

Run:

```bash
python3 outline_agent.py --help
```

Expected: usage lists `init`, `apply`, `context`, `audit`, `graph-sync`, and `export` subcommands.

## Task 2: Deterministic Character, Provenance, Causality, and Timeline Audit

**Files:**
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- `audit_packet(packet: dict) -> AuditReport` validates a packet before commit.
- `AuditReport.errors: list[dict]` contains hard failures; `.warnings: list[dict]` contains non-blocking findings.
- `AuditReport.ok: bool` is true only when `errors` is empty.
- `ValidationError` carries `code`, `message`, and `object_id`.

- [ ] **Step 1: Write failing audit tests**

```python
    def test_unnamed_actor_and_missing_agency_are_hard_errors(self):
        packet = {
            "entities": [{
                "id": "CHAR.bad", "kind": "CHARACTER", "namespace": "CANON",
                "name": "路人甲", "payload": {"identity": "护卫"},
            }],
            "edges": [],
        }
        report = audit_packet(packet)
        self.assertFalse(report.ok)
        codes = {item["code"] for item in report.errors}
        self.assertIn("PLACEHOLDER_PERSON", codes)
        self.assertIn("CHARACTER_WITHOUT_AGENCY", codes)

    def test_event_requires_provenance_and_causal_actor(self):
        packet = {
            "entities": [{
                "id": "EVENT.1", "kind": "EVENT", "namespace": "PLAN",
                "name": "突发反转", "payload": {"action": "发生"},
            }],
            "edges": [],
        }
        report = audit_packet(packet)
        self.assertFalse(report.ok)
        codes = {item["code"] for item in report.errors}
        self.assertIn("MISSING_PROVENANCE", codes)
        self.assertIn("ORPHAN_EVENT", codes)
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest -v test_outline_agent
```

Expected: FAIL with `NameError: name 'audit_packet' is not defined`.

- [ ] **Step 3: Implement the audit rules**

Implement these deterministic checks:

```python
PLACEHOLDER_NAMES = ("路人甲", "路人乙", "官员A", "官员B", "护卫一", "神秘人", "某个手下")
REQUIRED_CHARACTER_FIELDS = ("identity", "desires", "goals", "interests", "constraints", "preferred_strategy")

def audit_packet(packet: dict) -> AuditReport:
    # index IDs, names, kinds, and edges first;
    # reject duplicate IDs, broken references, placeholder individuals,
    # missing character agency/desire, missing provenance, orphan events,
    # unowned lines, unresolved promises, causal cycles, and impossible time order.
```

Use DFS only on `CAUSES`, `PRECEDES`, and `RESULTS_IN` edges; relationship graphs are allowed to contain cycles. Require `EVENT.*.payload.active_actor` or a `world_process_id`, and require event `provenance_refs`, `causal_inputs`, and `causal_outputs`. Require compound events to declare `participants` and at least two participants when `requires_hyperedge` is true. Do not reject Cohort nodes for lacking a personal name because Cohort is explicitly a group, not an individual.

- [ ] **Step 4: Run the audit tests and the full unit suite**

Run:

```bash
python3 -m unittest -v test_outline_agent
```

Expected: all current tests PASS, including cycle, broken-reference, provenance, line-owner, promise-chain, and timeline cases.

- [ ] **Step 5: Verify non-trivial audit behavior with a one-command demo**

Run:

```bash
python3 outline_agent.py audit --packet /tmp/vnext_bad_packet.json
```

Expected: non-zero exit status and JSON containing `PLACEHOLDER_PERSON`, `MISSING_PROVENANCE`, and `ORPHAN_EVENT`; no commit is attempted.

## Task 3: Neo4j Constraints, Property Graph Projection, and Hyperedge Incidence

**Files:**
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/graph/constraints.cypher`
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/graph/projection.cypher`
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/graph/queries.cypher`
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- `GraphProjector(shell: str = "cypher-shell", database: str = "neo4j")` uses local subprocess execution.
- `GraphProjector.ensure_schema() -> None` applies constraints and indexes.
- `GraphProjector.sync(project_id: str, changes: list[dict]) -> ProjectionResult` idempotently projects entities and edges.
- `GraphProjector.query(script_name: str, params: dict) -> list[dict]` runs an allowlisted query script only.
- `ProjectionResult.applied: int`, `.degraded: list[dict]` report outbox state.

- [ ] **Step 1: Write the failing graph contract test**

```python
    def test_hyperedge_packet_requires_all_roles(self):
        packet = {
            "entities": [
                {"id": "CHAR.a", "kind": "CHARACTER", "namespace": "CANON", "name": "沈砚", "payload": {"identity": "县令", "desires": ["保住县城"], "goals": ["查粮案"], "interests": ["权力"], "constraints": ["权限不足"], "preferred_strategy": "谈判", "provenance_refs": ["USER.1"]}},
                {"id": "EVENT.1", "kind": "EVENT", "namespace": "PLAN", "name": "查粮", "payload": {"active_actor": "CHAR.a", "requires_hyperedge": True, "provenance_refs": ["USER.1"], "causal_inputs": ["RULE.audit"], "causal_outputs": ["EVENT.2"]}},
            ],
            "edges": [{"id": "EDGE.1", "type": "PARTICIPATES_IN", "source": "CHAR.a", "target": "EVENT.1", "namespace": "PLAN", "payload": {"role": "initiator"}}],
        }
        report = audit_packet(packet)
        self.assertIn("HYPEREDGE_PARTICIPANT_SHORTFALL", {e["code"] for e in report.errors})
```

- [ ] **Step 2: Run the graph contract test and verify it fails**

Run:

```bash
python3 -m unittest -v test_outline_agent.CanonicalStoreTests.test_hyperedge_packet_requires_all_roles
```

Expected: FAIL because hyperedge participant validation is not implemented.

- [ ] **Step 3: Add Cypher schema and idempotent projection**

`constraints.cypher` must contain:

```cypher
CREATE CONSTRAINT entity_id IF NOT EXISTS
FOR (n:Entity) REQUIRE n.id IS UNIQUE;
CREATE INDEX entity_project IF NOT EXISTS
FOR (n:Entity) ON (n.project_id);
CREATE INDEX entity_kind IF NOT EXISTS
FOR (n:Entity) ON (n.kind);
```

`projection.cypher` must use generic `:Entity` nodes and `:REL` relationships so dynamic relationship types do not require APOC:

```cypher
UNWIND $entities AS row
MERGE (n:Entity {id: row.id})
SET n += row.props,
    n.project_id = $project_id,
    n.kind = row.kind,
    n.canon_version = $canon_version;

UNWIND $edges AS row
MATCH (s:Entity {id: row.source}), (t:Entity {id: row.target})
MERGE (s)-[r:REL {edge_id: row.id}]->(t)
SET r += row.props,
    r.type = row.type,
    r.project_id = $project_id,
    r.canon_version = $canon_version;
```

The runtime must call `subprocess.run([shell, "-u", user, "-p", password, "-d", database, "--format", "plain", "--param", "..."], input=cypher, text=True, capture_output=True, check=False)` without a shell. Credentials come only from environment variables and never enter packets or Markdown.

The projection must preserve the hyperedge pattern: an `EVENT.*` entity is the reified hyperedge node, and each participant is a `PARTICIPATES_IN` `REL` with `role`, `source_ids`, and valid-time properties. Replaying the same change must leave one node and one relationship per stable ID.

- [ ] **Step 4: Run the local Neo4j integration check**

Run:

```bash
NEO4J_USER=neo4j NEO4J_PASSWORD='configured-local-password' \
python3 -m unittest -v test_outline_agent.Neo4jProjectionTests
```

Expected: constraints apply, a compound event returns all participants and roles, and a second sync reports `applied=0` for already-projected changes. If credentials are absent, the test must fail clearly with `NEO4J_CONFIG_MISSING`, not silently downgrade a production graph run.

- [ ] **Step 5: Verify projection degradation is recoverable**

Run `graph-sync` once with a deliberately invalid local database name, then restore the correct name and run it again. Expected: SQLite Canon version is unchanged, the first run records `DEGRADED`, and the second run replays pending outbox rows to `APPLIED`.

## Task 4: Graph Retrieval and Context Packets

**Files:**
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/graph/queries.cypher`
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- `CanonicalStore.get_context(project_id: str, anchors: list[str], max_hops: int = 2) -> dict` returns a bounded `state_context_packet`.
- `state_context_packet` has `hard_canon`, `character_states`, `relationships`, `causal_paths`, `active_lines`, `promises`, `timeline_facts`, `negative_facts`, `provenance_refs`, and `retrieval_sufficiency`.
- `GraphProjector.query("character_neighborhood", {"anchor_ids": [...]}) -> list[dict]` returns typed graph rows.

- [ ] **Step 1: Write the failing retrieval test**

```python
    def test_context_packet_keeps_hyperedge_roles_and_negative_facts(self):
        packet = build_demo_packet()
        context = build_context_from_packet(packet, ["CHAR.a"], max_hops=2)
        self.assertEqual(context["retrieval_sufficiency"], "SUFFICIENT")
        self.assertEqual(context["hyperedges"][0]["participants"][0]["role"], "initiator")
        self.assertIn("PROP.burned-ledger", context["negative_facts"])
```

- [ ] **Step 2: Run it and verify it fails**

Run:

```bash
python3 -m unittest -v test_outline_agent.ContextPacketTests
```

Expected: FAIL because `build_context_from_packet` is not defined.

- [ ] **Step 3: Implement bounded structured retrieval**

Use a deterministic sequence: filter by project, namespace, `status`, and `canon_version`; anchor by stable IDs; traverse only allowlisted edge types; filter by valid time; attach negative facts and contradictory records; then stop when hard Canon, relevant relationships, causal path, and provenance are present. Return `INSUFFICIENT` with missing categories instead of fabricating facts.

Add Cypher queries for:

```cypher
// character_neighborhood
MATCH (a:Entity {id: $anchor_id})-[r:REL*1..2]-(n:Entity)
WHERE all(x IN r WHERE x.project_id = $project_id)
RETURN a.id AS anchor_id, n.id AS node_id,
       [x IN r | {type:x.type, edge_id:x.edge_id}] AS path;

// causal_path
MATCH p=(a:Entity {id:$from_id})-[:REL*1..8]->(b:Entity {id:$to_id})
WHERE all(x IN relationships(p) WHERE x.type IN ["CAUSES", "ENABLES", "BLOCKS", "REQUIRES"])
RETURN [x IN nodes(p) | x.id] AS node_ids;

// hyperedge_context
MATCH (e:Entity {kind:"EVENT", id:$event_id})<-[r:REL {type:"PARTICIPATES_IN"}]-(p:Entity)
RETURN e.id AS event_id, collect({id:p.id, role:r.role, kind:p.kind}) AS participants;
```

- [ ] **Step 4: Run unit and local graph retrieval tests**

Run:

```bash
python3 -m unittest -v test_outline_agent.ContextPacketTests test_outline_agent.Neo4jProjectionTests
```

Expected: all tests PASS and no Plan/Candidate record appears in a Canon-only context packet.

- [ ] **Step 5: Verify the stop rule**

Run `context` with an unknown anchor. Expected: exit code `2`, JSON `retrieval_sufficiency=INSUFFICIENT`, and a non-empty `missing` list; no guessed entity is inserted.

## Task 5: Markdown Master Outline Export and Audit Report

**Files:**
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- `CanonicalStore.export_markdown(project_id: str, output_path: Path) -> Path` writes a stable, ID-linked Master Outline.
- `CanonicalStore.export_audit(project_id: str, output_path: Path) -> Path` writes errors, warnings, assumptions, graph health, and unresolved references.

- [ ] **Step 1: Write the failing export test**

```python
    def test_export_is_stable_and_contains_all_required_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            store.apply_packet("PROJECT.demo", build_valid_packet(), 0, "demo")
            first = Path(tmp) / "one.md"
            second = Path(tmp) / "two.md"
            store.export_markdown("PROJECT.demo", first)
            store.export_markdown("PROJECT.demo", second)
            self.assertEqual(first.read_text(), second.read_text())
            text = first.read_text()
            self.assertIn("# 项目总契约与禁止事项", text)
            self.assertIn("# 全人物总表", text)
            self.assertIn("CHAR.a", text)
            self.assertIn("EVENT.1", text)
```

- [ ] **Step 2: Run it and verify it fails**

Run:

```bash
python3 -m unittest -v test_outline_agent.ExportTests
```

Expected: FAIL because `export_markdown` is not implemented.

- [ ] **Step 3: Implement deterministic export**

Sort entities by the fixed section order below and then by stable ID:

```python
SECTION_ORDER = (
    "PROJECT", "RULE", "LOCATION", "FACTION", "CHARACTER", "COHORT",
    "ACT", "LINE", "EVENT", "PROMISE", "CLIMAX", "RESOURCE", "OBJECT", "EVIDENCE",
)
```

Emit all 23 sections from the design specification, preserve IDs in headings and tables, include relation edge lists, include a “开放余波与假设” section, and include a graph projection status line. Write through a sibling temporary file and `os.replace`.

- [ ] **Step 4: Run export and audit tests**

Run:

```bash
python3 -m unittest -v test_outline_agent.ExportTests
```

Expected: PASS, stable byte-for-byte output, and audit output identifies every hard error by code and object ID.

- [ ] **Step 5: Verify a valid demo export manually**

Run:

```bash
python3 outline_agent.py export --db /tmp/vnext-demo/outline.db \
  --project-id PROJECT.demo --out /tmp/vnext-demo/master-outline.md
```

Expected: the file contains project contract, world rules, named cast, topology, N-line structure, causal spine, foreshadow/payoff map, time/space, volume/chapter nodes, provenance, and audit status.

## Task 6: CLI, Skill Instructions, and Packet Contracts

**Files:**
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/SKILL.md`
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/references/runtime-core.md`
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/references/output-contract.md`
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/outline_agent.py`
- Test: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`

**Interfaces:**
- CLI commands: `init`, `apply`, `context`, `audit`, `graph-sync`, `export`.
- `apply` accepts a JSON packet path and prints `{version, snapshot_hash, outbox_count}`.
- `SKILL.md` instructs Codex to build in the order `STATE → AGENCY → SEARCH → SELECT → OUTLINE INTEGRATE`.

- [ ] **Step 1: Write the failing CLI and packet tests**

```python
    def test_cli_init_and_apply_emit_machine_readable_json(self):
        # invoke main([...]) without a shell and parse stdout as JSON
        result = main(["init", "--db", db, "--project-id", "PROJECT.demo", "--title", "Demo"])
        self.assertEqual(result, 0)
        result = main(["apply", "--db", db, "--project-id", "PROJECT.demo", "--expected-version", "0", "--packet", packet, "--message", "demo"])
        self.assertEqual(result, 0)
```

- [ ] **Step 2: Run it and verify it fails**

Run:

```bash
python3 -m unittest -v test_outline_agent.CliTests
```

Expected: FAIL because `main` does not yet expose the subcommands.

- [ ] **Step 3: Implement CLI and Skill contracts**

`SKILL.md` must state that Codex:

```text
1. reads only the current phase packet and relevant graph context;
2. creates named characters before chapter events;
3. derives events from actor desire/interest/pressure;
4. records every important object with provenance;
5. constructs N acts and N lines from actual state changes;
6. sends JSON packets to `apply` only after deterministic validation;
7. runs `graph-sync`, `audit`, and `export` before claiming completion;
8. never writes prose or upgrades Plan to Canon implicitly.
```

`output-contract.md` must define exact packet keys: `entities`, `edges`, `assumptions`, `open_questions`, `source_refs`, and `precision`. `runtime-core.md` must include only the hard rules needed by the current phase, including hyperedge role integrity and Neo4j projection status.

- [ ] **Step 4: Run CLI, contract, and full unit tests**

Run:

```bash
python3 -m unittest -v test_outline_agent
python3 outline_agent.py --help
```

Expected: all tests PASS and each command has a help line.

- [ ] **Step 5: Verify invalid packet behavior**

Run `apply` with a packet missing `entities` and `edges`. Expected: exit code `2`, machine-readable `INVALID_PACKET`, no version increment, and no graph-sync attempt.

## Task 7: End-to-End Demonstration and Release Gate

**Files:**
- Create: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/demo_packet.json`
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts/test_outline_agent.py`
- Modify: `changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/SKILL.md`

**Interfaces:**
- `demo_packet.json` is a complete minimal project packet with two named core characters, one named opposition actor, two locations, two lines, one compound event, one promise, one causal chain, and one closure.
- End-to-end command sequence must produce `outline.db`, `master-outline.md`, `audit-report.md`, and a Neo4j projection for the demo project.

- [ ] **Step 1: Write the failing end-to-end test**

```python
    def test_demo_packet_has_no_hard_errors_and_exports_required_sections(self):
        packet = load_json(Path("demo_packet.json"))
        report = audit_packet(packet)
        self.assertTrue(report.ok, report.errors)
        self.assertEqual({e["kind"] for e in packet["entities"] if e["kind"] == "CHARACTER"}, {"CHARACTER"})
        text = render_packet_markdown(packet)
        for heading in ("项目总契约", "全人物总表", "动态 N 线", "全书主因果链", "伏笔"):
            self.assertIn(heading, text)
```

- [ ] **Step 2: Run it and verify the expected failure**

Run:

```bash
python3 -m unittest -v test_outline_agent.DemoTests
```

Expected: FAIL because `demo_packet.json` and `render_packet_markdown` do not yet exist.

- [ ] **Step 3: Add the valid demo packet and full command path**

The demo must use actual names and identities, for example `CHAR沈砚` and `CHAR顾青禾`, not placeholders. Its compound event must have at least two participant roles and an explicit object/location participant. Its promise must link creation → reinforcement → reveal → payoff. Its two lines must collide through a shared resource and close with distinct residues.

- [ ] **Step 4: Run the complete release checks**

Run:

```bash
cd changpianxiaoshuodagang/.agents/skills/vnext-outline-agent/scripts
python3 -m unittest -v
python3 outline_agent.py init --db /tmp/vnext-demo/outline.db --project-id PROJECT.demo --title "Demo"
python3 outline_agent.py apply --db /tmp/vnext-demo/outline.db --project-id PROJECT.demo --expected-version 0 --packet demo_packet.json --message "demo outline"
python3 outline_agent.py graph-sync --db /tmp/vnext-demo/outline.db --project-id PROJECT.demo
python3 outline_agent.py audit --db /tmp/vnext-demo/outline.db --project-id PROJECT.demo
python3 outline_agent.py export --db /tmp/vnext-demo/outline.db --project-id PROJECT.demo --out /tmp/vnext-demo/master-outline.md
```

Expected: all tests PASS; `audit` exits `0`; graph sync reports every outbox change `APPLIED`; export exits `0` and writes the complete Markdown file.

- [ ] **Step 5: Record release evidence**

Write the exact test command, exit codes, Neo4j version, graph projection count, Canon version, and exported file checksum to `changpianxiaoshuodagang/projects/PROJECT.demo/audit-report.md`. If Neo4j is not reachable, mark the run `DEGRADED` and do not claim Production Ready.

## Self-Review Checklist

- Spec coverage: Tasks 1–2 cover Canon, stable IDs, names, agency, provenance, causality, time and line/promise checks; Task 3 covers Neo4j and hypergraph incidence; Task 4 covers typed/temporal graph retrieval and negative facts; Task 5 covers Master Outline integration; Task 6 covers Codex Skill and CLI; Task 7 covers release evidence.
- Placeholder scan: every implementation step has a concrete file, interface, test command, expected result, and failure behavior.
- Type consistency: `CanonicalStore`, `AuditReport`, `GraphProjector`, `ProjectionResult`, `get_context`, `apply_packet`, `audit_packet`, `export_markdown`, `export_audit`, and `main` are introduced before later tasks consume them.
- Deliberate simplification: no native hypergraph engine, GDS, APOC, vectors, or embeddings; event-node reification plus Cypher preserves the required N-ary causal structure with lower operational cost.
- Completion boundary: outline generation remains in Codex Skill; the runtime can prove structure and provenance but cannot prove literary quality by itself.
