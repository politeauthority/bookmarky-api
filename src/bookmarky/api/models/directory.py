"""
    Bookmarky Api
    Model
    Directory

"""

from bookmarky.shared.models.directory import FIELD_MAP, FIELD_META
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class Directory(BaseEntityMeta):

    model_name = "directory"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Directory, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.table_name = "directories"
        self.immutable = False
        self.createable = True
        self.setup()
        self.rw_only_own = True

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/directory.py
