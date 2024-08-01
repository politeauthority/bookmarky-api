"""
    Bookmark Api
    Collection
    Bookmarks

"""
from bookmarky.api.collects.base import Base
from bookmarky.api.models.bookmark import Bookmark


class Bookmarks(Base):

    collection_name = "bookmarks"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Bookmarks, self).__init__(conn, cursor)
        self.table_name = Bookmark().table_name
        self.collect_model = Bookmark
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: bookmarky/src/bookmarky/api/collects/bookmarks.py
