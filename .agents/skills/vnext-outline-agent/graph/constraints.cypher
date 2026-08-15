CREATE CONSTRAINT entity_id IF NOT EXISTS
FOR (n:Entity) REQUIRE n.id IS UNIQUE;
CREATE INDEX entity_project IF NOT EXISTS
FOR (n:Entity) ON (n.project_id);
CREATE INDEX entity_kind IF NOT EXISTS
FOR (n:Entity) ON (n.kind);
