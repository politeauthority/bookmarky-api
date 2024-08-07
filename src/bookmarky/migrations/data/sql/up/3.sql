--- 
--- Migration 3
--- Bookmarky updates
---
ALTER TABLE bookmarks
    ADD COLUMN directory VARCHAR;

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/3.sql