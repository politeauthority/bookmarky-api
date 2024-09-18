--- 
--- Migration 5
--- Bookmarky specific
---
--- Add hidden to Bookmarks
---

ALTER TABLE directories
	ADD COLUMN hidden BOOLEAN DEFAULT False;



-- End file: politeauthority/bookmarky-api/src/bookmarky/migrations/data/sql/up/5.sql
