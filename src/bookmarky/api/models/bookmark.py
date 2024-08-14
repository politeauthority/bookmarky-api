"""
    Bookmarky Api
    Model Bookmark

"""
import logging

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
        self.tags = {}

    def __repr__(self):
        """Bookmark model representation."""
        if self.url and self.name:
            return "<%s: %s - %s %s>" % (self.__class__.__name__, self.id, self.url, self.name)
        elif self.url:
            return "<%s: %s - %s>" % (self.__class__.__name__, self.id, self.url)
        elif self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_tags(self):
        """Get all Tags for a Bookmark"""
        if not self.id:
            logging.warning("Cannot get Bookmark Tags without a bookmark.id")
            return False
        sql = """
            SELECT t.id
            FROM bookmark_tags bt
                JOIN tags t
                    ON bt.tag_id = t.id
            WHERE
                bookmark_id = %s
        """
        print(sql)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/bookmark.py
