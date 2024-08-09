"""
    Bookmarky Api
    Model Bookmark

"""
from bookmarky.shared.models.bookmark import FIELD_MAP, FIELD_META
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class Bookmark(BaseEntityMeta):

    model_name = "bookmark"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(Bookmark, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.table_name = "bookmarks"
        self.immutable = False
        self.createable = True
        self.setup()
        self.rw_only_own = True

    def __repr__(self):
        """Bookmark model representation."""
        if self.url and self.name:
            return "<%s: %s - %s %s>" % (self.__class__.__name__, self.id, self.url, self.name)
        elif self.url:
            return "<%s: %s - %s>" % (self.__class__.__name__, self.id, self.url)
        elif self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__


# End File: politeauthority/bookmarky/src/bookmarky/api/models/bookmark.py
