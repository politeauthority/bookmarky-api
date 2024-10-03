"""
    Bookmarky Api
    Model
    Tag Feature

"""
from bookmarky.shared.models.tag_feature import FIELD_MAP
from bookmarky.api.models.base_entity_meta import Base


class TagFeature(Base):

    model_name = "tag_feature"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(TagFeature, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        # self.ux_key = FIELD_META["ux_key"]
        self.table_name = "tag_features"
        self.immutable = True
        self.createable = True
        self.setup()

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/tag_feature.py
