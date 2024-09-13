"""
    Bookmark Api
    Collection - Bookmark Tags

"""
import logging

from polite_lib.utils import xlate

from bookmarky.api.collects.base import Base
from bookmarky.api.models.bookmark_tag import BookmarkTag


class BookmarkTags(Base):

    collection_name = "bookmark_tags"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(BookmarkTags, self).__init__(conn, cursor)
        self.table_name = BookmarkTag().table_name
        self.collect_model = BookmarkTag
        self.field_map = self.collect_model().field_map
        self.per_page = 20

    def delete_for_bookmark(self, bookmark_id: int) -> bool:
        """Delete all BookmarkTags for a given Tag ID."""
        sql = """
            DELETE
            FROM bookmark_tags as bt
            WHERE
                bookmark_id = %s;
            """
        bookmark_id = xlate.convert_any_to_int(bookmark_id)
        logging.debug("\n%s\n" % self.cursor.mogrify(sql, (bookmark_id,)))
        self.cursor.execute(sql, (bookmark_id,))
        self.conn.commit()
        logging.debug("Deleted BookmarkTags for Bookmark.ID: %s" % bookmark_id)
        return True

    def delete_for_tag(self, tag_id: int) -> bool:
        """Delete all BookmarkTags for a given Tag ID."""
        sql = """
            DELETE
            FROM bookmark_tags as bt
            WHERE
                tag_id = %s;
            """
        bookmark_id = xlate.convert_any_to_int(tag_id)
        logging.debug("\n%s\n" % self.cursor.mogrify(sql, (bookmark_id,)))
        self.cursor.execute(sql, (bookmark_id,))
        self.conn.commit()
        logging.debug("Deleted BookmarkTags for Tag.ID: %s" % bookmark_id)
        return True


# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/bookmark_tags.py
