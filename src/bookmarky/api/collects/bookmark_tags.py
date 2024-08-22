"""
    Bookmark Api
    Collection - Bookmark Tags

"""
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

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/bookmark_tags.py
