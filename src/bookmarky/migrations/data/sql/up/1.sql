--- Migration 1 SQL
--- Create initial tables
---
--- Create api_keys
---
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    client_id VARCHAR UNIQUE,
    key VARCHAR,
    last_access TIMESTAMP,
    last_ip VARCHAR,
    expiration_date TIMESTAMP,
    enabled BOOLEAN DEFAULT True,
    UNIQUE (user_id, client_id)
);


---
--- Create bookmarks
---
CREATE TABLE IF NOT EXISTS bookmarks (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    tags TEXT[],
    url VARCHAR,
    deleted BOOLEAN DEFAULT False,
    UNIQUE (user_id, url)
);
