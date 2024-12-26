"""
    Bookmarky Api
    Model AutoFeature

"""
from bookmarky.shared.models.auto_feature import FIELD_MAP
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class AutoFeature(BaseEntityMeta):

    model_name = "auto_feature"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(AutoFeature, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "auto_features"
        self.createable = True
        self.setup()

    def __repr__(self):
        """AutoFeature model representation."""
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        else:
            return "<%s>" % (self.__class__.__name__)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/auto_feature.py
