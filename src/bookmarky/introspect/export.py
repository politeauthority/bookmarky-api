"""
    Bookmarky Introspect
    Introspect
    Export

    Export all Bookmarks, Tags and Directories for a User.

"""
from bookmarky.api.utils import db
from bookmarky.api.collects.tags import Tags
# from bookmarky.api.models.bookmark import Bookmark
# from bookmarky.api.models.bookmark_tag import BookmarkTag
# from bookmarky.api.utils import db
# from bookmarky.introspect.modules.add_reddit_tags import AddRedditTags


# logging.config.dictConfig(log_config)
# logger = logging.getLogger(__name__)
# logger.propagate = True


class Export:
    def __init__(self):
        if not db.connect():
            print("Failed database connection, exiting")
            exit(1)
        self.export_data = {}
        self.user_id = 1

    def run(self):
        self.get_tags()
        self.get_dirs()

    def get_tags(self):
        tags = Tags().get_by_user_id(self.user_id)
        for tag in tags:
            self.export_data["tags"] = {
                "name": tag.name,
                "slug": tag.slug
            }
        return True

    def get_dirs(self):
        return True

if __name__ == "__main__":
    Export().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/export.py
