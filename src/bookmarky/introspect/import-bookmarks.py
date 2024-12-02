#!/usr/bin/env python
"""
    Bookmarky Api
    Import

"""
import logging

import arrow
from bs4 import BeautifulSoup

from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.models.bookmark_tag import BookmarkTag
from bookmarky.api.models.tag import Tag
from bookmarky.api.utils import db

IMPORT_FILE = "/work/bookmarks-export.html"
USER_ID = 1

db.connect()


class ImportBookmarks:

    def __init__(self):
        self.import_tag = None

    def run(self):
        print("Starting import")
        self.get_import_tag()
        bookmarks = self.parse_firefox()
        self.import_bookmarks(bookmarks)

    def parse_firefox(self) -> list:
        """Parse Firefox Bookmarks."""
        logging.info("Importing Firefox")
        logging.info(f"Import: {IMPORT_FILE}")
        with open(IMPORT_FILE, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        bookmarks = []
        for link in soup.find_all('a'):
            bookmarks.append({
                'title': link.text,
                'url': link.get('href'),
                'add_date': link.get('add_date')
            })
        return bookmarks

    def get_import_tag(self):
        """Get the Tag we'll be associating the imported bookmarks with."""
        tag = Tag()
        fields = [
            {
                "field": "user_id",
                "value": USER_ID,
                "op": "eq"
            },
            {
                "field": "slug",
                "value": "imported",
                "op": "eq"
            },
        ]
        if tag.get_by_fields(fields):
            self.import_tag = tag
            return tag
        tag.user_id = USER_ID
        tag.name = "Imported"
        tag.slug = "imported"
        tag.save()
        logging.info(f"Created Tag: {tag}")
        self.import_tag = tag
        return tag

    def import_bookmarks(self, bookmarks: list) -> bool:
        """Import the bookmarks."""
        for import_bookmark in bookmarks:
            bookmark = Bookmark()
            bookmark.user_id = USER_ID
            bookmark.title = import_bookmark["title"]
            bookmark.url = import_bookmark["url"]
            bookmark.created_ts = arrow.get(int(import_bookmark["add_date"])).datetime
            bookmark.save()
            bt = BookmarkTag()
            bt.bookmark_id = bookmark.id
            bt.tag_id = self.import_tag.id
            bt.save()
            print("Saved: %s" % bookmark)


if __name__ == "__main__":
    ImportBookmarks().run()
