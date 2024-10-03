"""
    Bookmark Api
    Collection
    Tags

"""
from bookmarky.api.collects.base import Base
from bookmarky.api.models.tag import Tag
from bookmarky.api.models.bookmark import Bookmark


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
        self.per_page = 50

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

    def get_tags_for_bookmarks(self, bookmarks: list) -> list:
        """Get all the Tags for list of Bookmarks."""
        b_ids = self._get_bookmark_ids(bookmarks)
        sql = """
            SELECT t.id, t.name, t.slug, bt.bookmark_id
            FROM tags t
                JOIN bookmark_tags bt
                    ON bt.tag_id = t.id
            WHERE bt.bookmark_id IN %s
        """
        if not bookmarks:
            return []
        self.cursor.execute(sql, (b_ids,))
        tag_matches = self.cursor.fetchall()
        for tag_match in tag_matches:
            for bookmark in bookmarks:
                if bookmark["id"] == tag_match[3]:
                    if "tags" not in bookmark:
                        bookmark["tags"] = []
                    tag = {
                        "id": tag_match[0],
                        "name": tag_match[1],
                        "slug": tag_match[2],
                    }
                    bookmark["tags"].append(tag)
        return bookmarks
    
    def get_tags_for_bookmark(self, bookmark_id: int) -> list:
        """Get all the Tags for a single Bookmark, returning hydrated Tag objects."""
        select_fields = Tag()._get_field_names_str(prefix="t")
        sql = f"""
            SELECT {select_fields}
            FROM bookmark_tags bt
                JOIN tags t
                    ON bt.tag_id = t.id
            WHERE
                bt.bookmark_id = %s;
        """
        self.cursor.execute(sql, (bookmark_id,))
        raws = self.cursor.fetchall()
        return self.load_presiteines(raws)

    def _get_bookmark_ids(self, bookmarks: list) -> tuple:
        """Unpack a Bookmarks, getting their Ids as a tuple. We'll unpack a list of dicts or a list
        of Bookmark entities.
        """
        b_ids = []
        for bookmark in bookmarks:
            if isinstance(bookmark, Bookmark):
                b_ids.append(bookmark.id)
            elif isinstance(bookmark, dict):
                b_ids.append(bookmark["id"])
        return tuple(b_ids)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/tags.py
