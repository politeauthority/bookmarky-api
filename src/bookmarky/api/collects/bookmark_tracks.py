"""
    Bookmark Api
    Collection - Bookmark Tracks

"""
import logging

from polite_lib.utils import xlate

from bookmarky.api.collects.base import Base
from bookmarky.api.models.bookmark_track import BookmarkTrack


class BookmarkTracks(Base):

    collection_name = "bookmark_tracks"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(BookmarkTracks, self).__init__(conn, cursor)
        self.table_name = BookmarkTrack().table_name
        self.collect_model = BookmarkTrack
        self.field_map = self.collect_model().field_map
        self.per_page = 20

    def delete_for_bookmark(self, bookmark_id: int) -> bool:
        """Delete all BookmarkTracks for a given Bookmark ID."""
        sql = """
            DELETE
            FROM bookmark_tracks as bt
            WHERE
                bookmark_id = %s;
            """
        bookmark_id = xlate.convert_any_to_int(bookmark_id)
        self.cursor.execute(sql, (bookmark_id,))
        self.conn.commit()
        logging.debug("Deleted BookmarkTracks for Bookmark.ID: %s" % bookmark_id)
        return True


# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/bookmark_tracks.py
