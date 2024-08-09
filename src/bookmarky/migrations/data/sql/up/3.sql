--- 
--- Migration 3
--- Generic tables
--- Ideally this will go down to migration 1 when we're ready to merge down.
---
---
--- Create entity_metas
---
CREATE TABLE IF NOT EXISTS entity_metas (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    entity_type VARCHAR,
    entity_id INTEGER,
    name VARCHAR,
    type VARCHAR,
    value VARCHAR
);

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/3.sql
