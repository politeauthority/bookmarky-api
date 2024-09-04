"""
    Bookmarky Debug
    Debug General

"""
import logging

from bookmarky.api.utils import glow
from bookmarky.api.collects.bookmark_tags import BookmarkTags
from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.utils import db
# from bookmarky.api.utils import glow


class Debug:

    def __init__(self):
        """Start the database connection, load up useful collections."""
        if not db.connect():
            logging.critical("Failed database connection, exiting")
            exit(1)
        self.col_b = Bookmarks()
        self.col_bt = BookmarkTags()

    def run(self):
        """Primary entry point for debugging."""
        self.like_query()

    def like_query(self):
        sql = """
            SELECT *
            FROM bookmarks
            WHERE title LIKE %s
        """
        glow.db["cursor"].execute(sql, ("%news%",))
        # results = glow.db["cursor"].fetchall()
        # import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    Debug().run()


# End File: politeauthority/bookmarky-api/src/bookmarky/debug.py
