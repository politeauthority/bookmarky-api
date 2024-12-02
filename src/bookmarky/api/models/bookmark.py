"""
    Bookmarky Api
    Model Bookmark

"""
import logging

from bookmarky.shared.models.bookmark import FIELD_MAP, FIELD_META, FIELD_MAP_METAS
from bookmarky.api.models.base_entity_meta import BaseEntityMeta
from bookmarky.api.collects.bookmark_tags import BookmarkTags
from bookmarky.api.collects.bookmark_tracks import BookmarkTracks


class Bookmark(BaseEntityMeta):

    model_name = "bookmark"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(Bookmark, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.field_map_metas = FIELD_MAP_METAS
        self.table_name = "bookmarks"
        self.immutable = False
        self.createable = True
        self.setup()
        self.rw_only_own = True
        self.tags = {}
        self.metas = {}

    def __repr__(self):
        """Bookmark model representation."""
        if self.url and self.title:
            return "<%s: %s - %s %s>" % (self.__class__.__name__, self.id, self.url, self.title)
        elif self.url:
            return "<%s: %s - %s>" % (self.__class__.__name__, self.id, self.url)
        elif self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def delete(self) -> bool:
        """Delete a model Bookmark and all of it's supporting data."""
        logging.info(f"Deleting Bookmark: {self}")
        super(Bookmark, self).delete()
        logging.info("Deleting BookmarkTags")
        BookmarkTags().delete_for_bookmark(self.id)
        BookmarkTracks().delete_for_bookmark(self.id)
        return True

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/bookmark.py
