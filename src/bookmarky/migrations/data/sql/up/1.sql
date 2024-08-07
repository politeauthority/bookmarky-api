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
--- Create users
---
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    role_id INTEGER,
    org_id INTEGER,
    last_access TIMESTAMP
);

---
--- Create roles
---
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR,
    slug_name VARCHAR
);

---
--- Create perms
---
CREATE TABLE IF NOT EXISTS perms (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR,
    slug_name VARCHAR
);

---
--- Create role_perm
---
CREATE TABLE IF NOT EXISTS role_perms (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER,
    perm_id INTEGER,
    enabled BOOLEAN DEFAULT True
);

--- 
--- Create options
---
CREATE TABLE IF NOT EXISTS options (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR,
    name VARCHAR UNIQUE,
    value TEXT,
    acl_write TEXT[],
    acl_read TEXT[],
    hide_value BOOLEAN
);

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/1.sql
