--- 
--- Migration 2
--- Bookmarky specific
---
---
--- Create bookmarks
---
CREATE TABLE IF NOT EXISTS bookmarks (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    title VARCHAR,
    url VARCHAR,
    directory_id INTEGER,
    deleted BOOLEAN DEFAULT False,
    UNIQUE (user_id, url)
);

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

---
--- Create tags
---
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    slug VARCHAR NOT NULL,
    deleted BOOLEAN DEFAULT False,
    UNIQUE (user_id, slug)
);


-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/2.sql
