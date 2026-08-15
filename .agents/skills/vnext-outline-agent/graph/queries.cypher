// character_neighborhood
MATCH (a:Entity {id: $anchor_id, project_id: $project_id})-[r:REL*1..2]-(n:Entity {project_id: $project_id})
WHERE all(x IN r WHERE x.project_id = $project_id)
RETURN a.id AS anchor_id, n.id AS node_id,
       [x IN r | {type:x.type, edge_id:x.edge_id}] AS path;

// causal_path
MATCH p=(a:Entity {id:$from_id, project_id:$project_id})-[:REL*1..8]->(b:Entity {id:$to_id, project_id:$project_id})
WHERE all(x IN relationships(p) WHERE x.project_id = $project_id AND x.type IN ["CAUSES", "ENABLES", "BLOCKS", "REQUIRES"])
RETURN [x IN nodes(p) | x.id] AS node_ids;

// hyperedge_context
MATCH (e:Entity {kind:"EVENT", id:$event_id, project_id:$project_id})<-[r:REL {type:"PARTICIPATES_IN", project_id:$project_id}]-(p:Entity {project_id:$project_id})
RETURN e.id AS event_id, collect({id:p.id, role:r.role, kind:p.kind}) AS participants;
