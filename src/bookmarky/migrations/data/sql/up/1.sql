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

<<<<<<< HEAD
---
--- Create roles
---
=======
>>>>>>> ecf2a33 (Bootstrap (#1))
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR,
    slug_name VARCHAR
);

---
<<<<<<< HEAD
--- Create perms
=======
--- Create role_perms
>>>>>>> ecf2a33 (Bootstrap (#1))
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
<<<<<<< HEAD
);
=======
);
>>>>>>> ecf2a33 (Bootstrap (#1))
