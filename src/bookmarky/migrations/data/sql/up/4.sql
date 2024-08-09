--- Migration 4 SQL
--- Directorories
--- 
--- Create directories
---
CREATE TABLE IF NOT EXISTS directories (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    path VARCHAR,
    slug VARCHAR,
    deleted BOOLEAN DEFAULT False,
    UNIQUE (user_id, path)
);

--- End File: politeauthority/bookmarky/migrations/data/sql/up/4.sql
