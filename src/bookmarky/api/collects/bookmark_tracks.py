"""
    Bookmark Api
    Collection - Bookmark Tracks

"""
from datetime import datetime
import logging

from polite_lib.utils import xlate

from bookmarky.api.collects.base import Base
from bookmarky.api.models.bookmark_track import BookmarkTrack
from bookmarky.api.utils import sql_tools


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

    def get_popular_bookmarks(self, user_id: int, since_date: datetime = None, limit: int = 20) -> list:
        """Get Bookmarks with the most records in the bookmark_tracks table for a given User ID. An
        optional `since_date` can be passed to narrow down records that have been seen since that
        date in the bookmark_tracks table.
        We return a list of Bookmark IDs.
        """
        no_date_limit_sql = "bookmark_tracks bt ON b.id = bt.bookmark_id"
        date_limit_sql = """
            bookmark_tracks bt ON b.id = bt.bookmark_id AND
                                        bt.created_ts > '%s'
        """ % (sql_tools.sql_safe(since_date))
        if since_date:
            join_sql = date_limit_sql
        else:
            join_sql = no_date_limit_sql
        sql = f"""
            SELECT b.id AS bookmark_id, COUNT(bt.id) AS click_count
            FROM bookmarks b
                LEFT JOIN {join_sql}
            WHERE
                b.user_id = %s
            GROUP BY b.id
            HAVING COUNT(bt.id) > 0
            ORDER BY click_count DESC
            LIMIT %s;
        """
        self.cursor.execute(sql, (user_id, limit))
        results = self.cursor.fetchall()
        return results

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
