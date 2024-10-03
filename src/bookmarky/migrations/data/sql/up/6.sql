--- 
--- Migration 6
--- Bookmarky specific
---
--- Add user_id to Bookmark Tags, and create a Tag Features table.
---

-- ALTER TABLE bookmark_tags
-- 	ADD COLUMN user_id INTEGER NOT NULL;

CREATE TABLE IF NOT EXISTS tag_features (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    tag_id INTEGER,
    user_id INTEGER,
    name VARCHAR,
    value VARCHAR,
    data VARCHAR
);


-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/6.sql
