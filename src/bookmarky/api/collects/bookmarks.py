"""
    Bookmark Api
    Collection
    Bookmarks

"""
from bookmarky.api.collects.base_entity_metas import BaseEntityMetas
from bookmarky.api.models.bookmark import Bookmark


class Bookmarks(BaseEntityMetas):

    collection_name = "bookmarks"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(Bookmarks, self).__init__(conn, cursor)
        self.table_name = Bookmark().table_name
        self.collect_model = Bookmark
        self.field_map = self.collect_model().field_map
        self.per_page = 20

    def get_by_tag_id(self, tag_id: int) -> list:
        """Get a collection of Bookmarks that have the given Tag ID."""
        bookmark_fields = self._gen_fields_for_join_sql()
        sql = f"""
            SELECT {bookmark_fields}
            FROM bookmarks b
                JOIN bookmark_tags bt
                    ON b.id = bt.bookmark_id
            WHERE
                bt.tag_id = %s
            LIMIT 20;
        """
        self.cursor.execute(sql, (tag_id,))
        rows = self.cursor.fetchall()
        if not rows:
            return []
        entities = self.build_from_lists(rows)
        entities = self.get_metas_for_entities("bookmark", entities)
        return entities

    def _gen_fields_for_join_sql(self) -> str:
        """
        """
        sql_fields = ""
        for field, info in self.field_map.items():
            sql_fields += f"b.{field},"
        sql_fields = sql_fields[:-1]
        return sql_fields

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/bookmarks.py
