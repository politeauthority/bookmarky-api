--- 
--- Migration 4
--- Bookmarky specific
---
--- Add hidden to Bookmarks
---

ALTER TABLE bookmarks
	ADD COLUMN hidden BOOLEAN DEFAULT False;


ALTER TABLE tags
	ADD COLUMN hidden BOOLEAN DEFAULT False;

-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/4.sql
