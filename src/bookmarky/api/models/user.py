"""
    Bookmarky Api
    Model User

"""
from bookmarky.shared.models.user import FIELD_MAP
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class User(BaseEntityMeta):

    model_name = "user"

    def __init__(self, conn=None, cursor=None):
        """Create the User instance."""
        super(User, self).__init__(conn, cursor)
        self.table_name = "users"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def __repr__(self):
        """User model representation."""
        if self.id and not self.name:
            return "<User %s>" % self.id
        if self.name and self.id:
            return "<User: %s %s>" % (self.id, self.name)
        return "<User>"


# End File: bookmarky/src/bookmarky/api/models/user.py
