--- 
--- Migration 8
--- Update column name for boomarks
---
ALTER TABLE bookmarks 
    RENAME COLUMN name TO title;

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/8.sql
