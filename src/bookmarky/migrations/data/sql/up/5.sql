--- 
--- Migration 5
--- Bookmarky specific
---

---
--- Create bookmark tags
---
CREATE TABLE IF NOT EXISTS bookmark_tags (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    bookmark_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    UNIQUE (bookmark_id, tag_id)
);

---
--- Remove bookmark's tag column
---
ALTER TABLE bookmarks
	DROP COLUMN tags;

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/5.sql
