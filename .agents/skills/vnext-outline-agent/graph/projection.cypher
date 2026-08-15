UNWIND $delete_edges AS row
OPTIONAL MATCH ()-[old:REL {edge_id: row.id, project_id: $project_id}]-()
DELETE old;

UNWIND $delete_entities AS row
MATCH (n:Entity {id: row.id, project_id: $project_id})
DETACH DELETE n;

UNWIND $entities AS row
MERGE (n:Entity {id: row.id, project_id: $project_id})
SET n += row.props,
    n.project_id = $project_id,
    n.kind = row.kind,
    n.canon_version = $canon_version;

UNWIND $edges AS row
OPTIONAL MATCH ()-[old:REL {edge_id: row.id, project_id: $project_id}]-()
DELETE old
WITH row
MATCH (s:Entity {id: row.source, project_id: $project_id}), (t:Entity {id: row.target, project_id: $project_id})
MERGE (s)-[r:REL {edge_id: row.id, project_id: $project_id}]->(t)
SET r += row.props,
    r.type = row.type,
    r.project_id = $project_id,
    r.canon_version = $canon_version;
