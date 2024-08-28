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

    def remove(self, bookmark_id: int, tag_id: int) -> bool:
        """Remove a Bookmark Tag if possible."""
        if not bookmark_id or not tag_id:
            logging.warning("Cannot remove BookmarkTag, bookmark_id: %s, tag_id: %s" % (
                bookmark_id, tag_id))
            return False
        self.bookmark_id = bookmark_id
        self.tag_id = tag_id
        self.get_by_bookmark_and_tag_id()
        if self.delete():
            logging.debug("Deleted BookmarkTag: %s" % self)
            return True
        else:
            logging.error("Failed deleting BookmarkTag")
            return False

    def get_by_bookmark_and_tag_id(self, bookmark_id: int = None, tag_id: int = None) -> bool:
        """Get a BookmarkTag by Bookmark.id and Tag.id"""
        if bookmark_id:
            self.bookmark_id = bookmark_id
        if tag_id:
            self.tag_id = tag_id
        if not self.bookmark_id or not self.tag_id:
            logging.error("Cannot Get BookmarkTag with bookmark_id: %s, tag_id: %s" % (
                self.bookmark_id,
                self.tag_id
            ))
            return False
        sql = f"""
            SELECT {self._gen_all_sql_fields()}
            FROM {self.table_name}
            WHERE
                bookmark_id = %s AND
                tag_id = %s;
            """
        logging.debug(f"\n\n We tried this {sql}\n\n")
        self.cursor.execute(sql, (self.bookmark_id, self.tag_id))
        raw = self.cursor.fetchone()
        if raw:
            self.build_from_list(raw)
            return True
        else:
            logging.warning("No BookmarkTag was found with bookmark_id %s or tag_id %s" % (
                self.bookmark_id,
                self.tag_id
            ))
            return False

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/bookmark_tag.py
