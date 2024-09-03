--- 
--- Migration 3
--- Bookmarky specific
---
--- Add notes to Bookmarks
---

ALTER TABLE bookmarks
	ADD COLUMN notes TEXT;

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/3.sql
