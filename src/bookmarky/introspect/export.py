"""
    Bookmarky Introspect
    Introspect
    Export

    Export all Bookmarks, Tags and Directories for a User.

"""
import json

from bookmarky.api.utils import db
from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.collects.directories import Directories
from bookmarky.api.collects.tags import Tags

# logging.config.dictConfig(log_config)
# logger = logging.getLogger(__name__)
# logger.propagate = True


class Export:
    def __init__(self):
        if not db.connect():
            print("Failed database connection, exiting")
            exit(1)
        self.export_data = {
            "tags": [],
            "directories": [],
            "bookmarks": [],
            "settings": {}
        }
        self.user_id = 1

    def run(self):
        self.get_tags()
        self.get_dirs()
        self.get_bookmarks()
        self.create_export_file()

    def get_tags(self) -> bool:
        """Get all of a User's Tags for export."""
        tags = Tags().get_by_user_id(self.user_id)
        for tag in tags:
            export_tag = {
                "name": tag.name,
                "slug": tag.slug,
                "hidden": tag.hidden,
                "deleted": tag.deleted
            }
            self.export_data["tags"].append(export_tag)
        return True

    def get_dirs(self) -> bool:
        """Get all of a User's Directories for export."""
        the_dirs = Directories().get_by_user_id(self.user_id)
        for the_dir in the_dirs:
            export_dir = {
                "id": the_dir.id,
                "name": the_dir.name,
                "slug": the_dir.slug,
                # "parent_id": the_dir.parent_id,
                "hidden": the_dir.hidden,
                "deleted": the_dir.deleted
            }
            self.export_data["directories"].append(export_dir)
        return True

    def get_bookmarks(self) -> bool:
        """Get all of a User's Bookmarks for export."""
        bookmarks = Bookmarks().get_by_user_id(self.user_id)
        for bookmark in bookmarks:
            export_bookmark = {
                "title": bookmark.title,
                "url": bookmark.url,
                "hidden": bookmark.hidden,
                "deleted": bookmark.deleted,
                "notes": bookmark.notes,
                "tags": []
            }
            tags = Tags().get_tags_for_bookmark(bookmark.id)
            for tag in tags:
                export_tag = {
                    "name": tag.name,
                    "slug": tag.slug
                }
                export_bookmark["tags"].append(export_tag)
            self.export_data["bookmarks"].append(export_bookmark)
        return True

    def create_export_file(self) -> bool:
        """Create the export file."""
        export_data = json.dumps(self.export_data)
        export_file = open("export.json", "w")
        export_file.write(export_data)
        export_file.close()
        print("Successfully wrote export file")
        print("Bookmarks: %s" % len(self.export_data["bookmarks"]))
        print("Tags: %s" % len(self.export_data["tags"]))
        print("Dirs: %s" % len(self.export_data["directories"]))
        return True


if __name__ == "__main__":
    Export().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/export.py
