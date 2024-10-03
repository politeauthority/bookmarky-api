"""
    Bookmark Api
    Collection
    Tag Features

"""
from bookmarky.api.collects.base import Base
from bookmarky.api.models.tag_feature import TagFeature


class TagFeatures(Base):

    collection_name = "tag_features"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(TagFeatures, self).__init__(conn, cursor)
        self.table_name = TagFeature().table_name
        self.collect_model = TagFeature
        self.field_map = self.collect_model().field_map
        self.per_page = 50


# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/tag_features.py
