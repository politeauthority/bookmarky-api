--- 
--- Migration 9
--- Auto Features
---
---
--- Create auto_features
---
CREATE TABLE IF NOT EXISTS auto_features (
    id SERIAL PRIMARY KEY,
    created_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    entity_id INTEGER NOT NULL,
    entity_type VARCHAR NOT NULL,
    auto_feature_type VARCHAR NOT NULL,
    auto_feature_value VARCHAR NOT NULL,
    enabled BOOLEAN DEFAULT False,
    UNIQUE (user_id, entity_id, entity_type, auto_feature_type, auto_feature_value)
);

DROP TABLE tag_features;

-- End File: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/9.sql
