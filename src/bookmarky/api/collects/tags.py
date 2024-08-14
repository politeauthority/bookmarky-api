"""
    Bookmark Api
    Collection - Tags

"""
from bookmarky.api.collects.base import Base
from bookmarky.api.models.tag import Tag


class Tags(Base):

    collection_name = "tags"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Tags, self).__init__(conn, cursor)
        self.table_name = Tag().table_name
        self.collect_model = Tag
        self.field_map = self.collect_model().field_map
        self.per_page = 20

    def get_by_user_id(self, user_id: int) -> list:
        """Get all Tags for a User by user_id."""
        sql = f"""
            SELECT *
            FROM {self.table_name}
            WHERE
                user_id = %s;
        """
        self.cursor.execute(sql, (user_id,))
        raws = self.cursor.fetchall()
        return self.load_presiteines(raws)

    def get_tag_ids_by_user_and_name(self, user_id: int, tags: list) -> list:
        """Get tags where the tags supplied match the User.id"""
        sql = f"""
            SELECT id
            FROM {self.table_name}
            WHERE
                user_id = %s AND
                name IN %s;
        """
        self.cursor.execute(sql, (user_id, tuple(tags)))
        # print(self.cursor.mogrify(sql, tuple(tags),))
        the_ids = []
        raws = self.cursor.fetchall()
        for raw in raws:
            the_ids.append(raw[0])
        return the_ids


# End File: politeauthority/bookmarky/src/bookmarky/api/collects/tags.py
