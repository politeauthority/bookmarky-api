"""
    Bookmark Api
    Collection
    AutoFeatures

"""
from bookmarky.api.collects.base_entity_metas import BaseEntityMetas
from bookmarky.api.models.auto_feature import AutoFeature


class AutoFeatures(BaseEntityMetas):

    collection_name = "auto_feature"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(AutoFeatures, self).__init__(conn, cursor)
        self.table_name = AutoFeature().table_name
        self.collect_model = AutoFeature
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/auto_features.py
