"""
    Bookmarky Api
    Model
    Bookmark Tag

"""
import logging
from bookmarky.shared.models.bookmark_tag import FIELD_MAP, FIELD_META
from bookmarky.api.models.base import Base


class BookmarkTag(Base):

    model_name = "bookmark_tag"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(BookmarkTag, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.table_name = "bookmark_tags"
        self.immutable = False
        self.createable = True
        self.setup()

    def __repr__(self):
        """Representation of a BookmarkTag."""
        if self.bookmark_id and self.tag_id:
            return "<BookmarkTag %s:%s>" % (self.bookmark_id, self.tag_id)
        else:
            return "<BookmarkTag>"

    def create(self, bookmark_id: int, tag_id: int) -> bool:
        """Create a Bookmark Tag if possible."""
        if not bookmark_id or not tag_id:
            logging.warning("Cannot create BookmarkTag, bookmark_id: %s, tag_id: %s" % (
                bookmark_id, tag_id))
            return False
        self.bookmark_id = bookmark_id
        self.tag_id = tag_id
        if self.save():
            logging.debug("saved new BookmarkTag: %s" % self)
            return True
        else:
            logging.error("Failed saving BookmarkTag")
            return False


# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/bookmark_tag.py
