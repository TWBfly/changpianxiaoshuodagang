# Runtime core

The runtime has one authoritative path:

`packet JSON → audit_packet → SQLite transaction/version → changes outbox → cypher-shell projection → bounded context → Markdown/audit export`

SQLite tables are `projects`, `entities`, `edges`, `commits`, and `changes`.
`projects.version` is optimistic concurrency control. A packet with a stale
`expected_version` fails before mutation. The commit stores a canonical JSON
hash and complete `snapshot_json`, so a repeatable packet is idempotent and any
committed version can be reconstructed.

`packet_mode` defaults to `SNAPSHOT`: omitted entities/edges generate DELETE
outbox entries. Set `packet_mode: "PATCH"` when only listed IDs should be
overlaid on the current Canon; the merged effective snapshot is audited and
committed.

## Packet minimum

```json
{
  "entities": [{"id":"CHAR.a","kind":"CHAR","name":"沈砚",
    "payload":{"identity":"县令","desires":["查明粮案"],
      "goals":["阻止灭口"],"interests":["保全辖区"],"constraints":["证据不足"],
      "preferred_strategy":"查账","agency":"主动调查",
      "biography":"...","growth_arc":"...","fate":"...",
      "provenance_refs":["brief-1"]}}],
  "edges": [],
  "negative_facts": ["PROP.burned-ledger"]
}
```

An event needs `active_actor` (or `world_process`), `causal_inputs`,
`causal_outputs`, and provenance. A hyperedge needs at least two participant
edges and one `initiator` role. All edge endpoints must exist in the same
packet or already committed Canon. Packet-level `assumptions`,
`open_questions`, `source_refs`, `precision`, and `negative_facts` are stored
alongside the Canon snapshot and round-trip through context/export; they are
not discarded metadata.

Chapter plans use the same `payload` contract. A `PRODUCTION_READY` plan must
contain a target prose contract, structured dynamic beats, payload clusters,
scene payloads, compression rules, continuation source, and forbidden drift.
The runtime computes capacity from those structures; `FULL`, `PASS`, and
`anti_self_certification` are never accepted as proof when supplied by a packet.

## Hypergraph mapping

Neo4j stores an event as a reified node:

```text
(CHAR.a)-[:REL {type:'PARTICIPATES_IN', role:'initiator'}]->(EVENT.1)
(CHAR.b)-[:REL {type:'PARTICIPATES_IN', role:'target'}]->(EVENT.1)
(EVENT.1)-[:REL {type:'RESULTS_IN'}]->(PROP.x)
```

The event node preserves the whole N-ary relation, event time, location,
evidence, and provenance. Do not replace it with pairwise character edges.

## Degraded graph behavior

`graph-sync` may fail after a successful Canon commit. The CLI marks pending
changes `DEGRADED` with the local error. Retry after starting/authenticating
Neo4j; do not delete or rewrite Canon to hide the failure. Context and export
remain available from SQLite, but reports must state that graph retrieval was
not available. `context --source auto` tries bounded Neo4j retrieval and adds a
`GRAPH_DEGRADED` status on local credential failure; `--source neo4j` makes the
failure hard and `--source sqlite` never contacts Neo4j. `graph-rebuild` clears
only the project projection and replays the current Canon outbox.
