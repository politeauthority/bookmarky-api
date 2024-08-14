"""
    Bookmarky Api
    Model Bookmark Tag

"""
from bookmarky.shared.models.bookmark_tag import FIELD_MAP, FIELD_META
from bookmarky.api.models.base import Base


class BookmarkTag(Base):

    model_name = "bookmark"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(BookmarkTag, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.table_name = "bookmark_tags"
        self.immutable = False
        self.createable = True
        self.setup()


# End File: politeauthority/bookmarky/src/bookmarky/api/models/bookmark_tag.py
