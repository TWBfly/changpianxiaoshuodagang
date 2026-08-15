# Output contract

The final Markdown export is deterministic and renders each committed object
once in its primary section (the roster is a compact name index with stable IDs). It contains these sections in
order: project metadata, characters, events, props, locations, lines,
promises, beats, causal links, foreshadowing, time facts, space facts,
negative facts, relations, and provenance. IDs are sorted within each section;
the packet JSON is retained for round-trip auditing.

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
forbidden drift, and computed `capacity_audit`. `PRODUCTION_READY` is emitted
only when the computed audit is `FULL`; packet-supplied `FULL`/`PASS` flags are
not evidence.

Audit output is JSON with `ok`, `errors`, `warnings`, and `counts`. Errors are
machine-readable and include `code`, `message`, and `object_id` when known.
`DEGRADED` graph state is a warning only when the Canon transaction succeeded;
it must never be rendered as `ok` graph synchronization.
