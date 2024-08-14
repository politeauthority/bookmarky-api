--- 
--- Migration 6
--- Recreate directories
---
--- Drop table directories
---
DROP TABLE directories;

--- 
--- Create directories
---
CREATE TABLE IF NOT EXISTS directories (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    parent_id INTEGER,
    name VARCHAR,
    slug VARCHAR,
    deleted BOOLEAN DEFAULT False,
    UNIQUE (user_id, name, parent_id)
);

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/6.sql
