"""
    Bookmark Api
    Collection
    Directories

"""
from bookmarky.api.collects.base import Base
from bookmarky.api.models.directory import Directory


class Directories(Base):

    collection_name = "directories"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(Directories, self).__init__(conn, cursor)
        self.table_name = Directory().table_name
        self.collect_model = Directory
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/directories.py
