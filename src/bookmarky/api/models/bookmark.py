"""
    Bookmarky Api
    Model Bookmark

"""
from bookmarky.shared.models.bookmark import FIELD_MAP
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class Bookmark(BaseEntityMeta):

    model_name = "bookmark"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(Bookmark, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "bookmarks"
        self.immutable = True
        self.createable = True
        self.setup()

# End File: bookmarky/src/bookmarky/api/models/bookmark.py
