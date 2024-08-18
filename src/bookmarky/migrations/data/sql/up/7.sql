--- 
--- Migration 7
--- Add Directories back to Bookmarks
---
--- Add directory_id column
---
ALTER TABLE bookmarks
    ADD COLUMN directory_id INTEGER;


-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/7.sql
