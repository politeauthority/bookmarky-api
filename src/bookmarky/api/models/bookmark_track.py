"""
    Bookmarky Api
    Model
    Bookmark Track

"""
from bookmarky.shared.models.bookmark_track import FIELD_MAP
from bookmarky.api.models.base import Base


class BookmarkTrack(Base):

    model_name = "bookmark_track"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(BookmarkTrack, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "bookmark_tracks"
        self.immutable = False
        self.createable = True
        self.setup()

    def __repr__(self):
        """Representation of a BookmarkTag."""
        if self.bookmark_id and self.tag_id:
            return "<BookmarkTrack %s:%s>" % (self.bookmark_id, self.user_id)
        else:
            return "<BookmarkTrack>"

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/bookmark_track.py
