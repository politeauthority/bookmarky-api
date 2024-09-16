"""
    Bookmarky Api
    Model User

"""
from bookmarky.shared.models.user import FIELD_MAP, FIELD_MAP_METAS
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class User(BaseEntityMeta):

    model_name = "user"

    def __init__(self, conn=None, cursor=None):
        """Create the User instance."""
        super(User, self).__init__(conn, cursor)
        self.table_name = "users"
        self.field_map = FIELD_MAP
        self.field_map_metas = FIELD_MAP_METAS
        self.createable = True
        self.user_id_field = "id"
        self.metas = {}
        self.setup()

    def __repr__(self):
        """User model representation."""
        if self.id and not self.name:
            return "<User %s>" % self.id
        if self.name and self.id:
            return "<User: %s %s>" % (self.id, self.name)
        return "<User>"


# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/user.py
