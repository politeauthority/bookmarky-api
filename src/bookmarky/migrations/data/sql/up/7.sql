--- Migration 7 SQL
--- Create Bookmarky click track table
---
---
--- Create bookmark_track
---
CREATE TABLE IF NOT EXISTS bookmark_track (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    bookmark_id INTEGER NOT NULL
);
