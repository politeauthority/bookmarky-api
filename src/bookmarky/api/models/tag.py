"""
    Bookmarky Api
    Model - Tag

"""
from bookmarky.shared.models.tag import FIELD_MAP, FIELD_META
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class Tag(BaseEntityMeta):

    model_name = "tag"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(Tag, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.table_name = "tags"
        self.immutable = True
        self.createable = True
        self.setup()

    def __repr__(self):
        """Tag model representation."""
        if self.name:
            return "<%s: %s - %s>" % (self.__class__.__name__, self.id, self.name)
        elif self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__


# End File: politeauthority/bookmarky/src/bookmarky/api/models/ctrl_tag.py
