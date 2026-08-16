# Output contract

The final Markdown export is deterministic and renders each committed object
once in its primary section (the roster is a compact name index with stable IDs). It contains these sections in
order: project metadata, one-sentence synopsis, detailed volume plots,
complete chapter index, characters, events, props, locations, lines,
promises, beats, causal links, foreshadowing, time facts, space facts,
negative facts, relations, and provenance. IDs are sorted within each section;
the packet JSON is retained for round-trip auditing.

FINAL_FULL_BOOK adds a hard completion contract:

~~~json
{
  "precision": {
    "production_stage": "FINAL_FULL_BOOK",
    "full_book_detailed_required": true,
    "expected_volumes": 7,
    "expected_chapters": 420
  },
  "entities": [
    {"kind":"PROJECT","payload":{
      "one_sentence_synopsis":"前因—发展—结局的一句话总纲",
      "causal_summary":"完整因果总纲"
    }},
    {"kind":"VOLUME","payload":{
      "chapter_start":1,"chapter_end":60,
      "detailed_plot":"本卷具体发生的剧情",
      "central_conflict":"本卷不可调和冲突",
      "turning_points":["..."],"payoff":"...","next_hook":"..."
    }}
  ]
}
~~~

The runtime rejects a final packet with missing scope, missing volume ranges,
missing chapters, repeated chapter function/core-delta pairs, or insufficient
4000–6000-character dramatic payload. Intermediate phase packets may omit the
full-book flag, but their export status is INCOMPLETE or INTERMEDIATE.

Every character dossier must expose: identity/name, biography, topology and
relationships, personality, growth history and arc, desire/goal/interest,
constraints and strategy, agency, highlights, fate, and evidence sources.

Every event/beat must expose: active actor or world process, participants and
roles, location, valid time, causal inputs and outputs, setup/payoff links,
reversal or climax role, and provenance. Every promise shows creation,
maturity, reveal, payoff, or an explicit unresolved risk.

Every `CHAPTER_PLAN` must expose its chapter number, volume, target prose
contract, chapter function, core delta, concrete conflict, dynamic beats,
payload clusters, scene payloads, explicit compression, continuation source,
forbidden drift, and computed `capacity_audit`. In final full-book mode,
`PRODUCTION_READY` is emitted only when the computed audit has at least 6
stageable core beats, 3 payload clusters, 3 core scenes, 2 active actors, 2
information/choice updates, and 2 delta dimensions. Packet-supplied `FULL`/`PASS`
flags are not evidence.

Audit output is JSON with `ok`, `errors`, `warnings`, and `counts`. Errors are
machine-readable and include `code`, `message`, and `object_id` when known.
`DEGRADED` graph state is a warning only when the Canon transaction succeeded;
it must never be rendered as `ok` graph synchronization.
