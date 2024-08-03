--- 
--- Bookmarky speccific
---
---
--- Create bookmarks
---
CREATE TABLE IF NOT EXISTS bookmarks (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    tags TEXT[],
    name VARCHAR,
    url VARCHAR,
    deleted BOOLEAN DEFAULT False,
    UNIQUE (user_id, url)
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