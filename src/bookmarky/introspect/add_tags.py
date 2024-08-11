"""
    Bookmarky Introspect
    Introspect - Add Tags

"""
import tldextract

from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.collects.tags import Tags
# from bookmarky.api.models.tag import Tag
from bookmarky.api.utils import db
from bookmarky.shared.utils import xlate
from bookmarky.introspect.modules.add_reddit_tags import AddRedditTags


# logging.config.dictConfig(log_config)
# logger = logging.getLogger(__name__)
# logger.propagate = True

USER_IDS = [1]


class AutoAddTags:

    def __init__(self):
        if not db.connect():
            print("Failed database connection, exiting")
            exit(1)
        self.col_bookmarks = Bookmarks()
        self.col_tags = Tags()
        self.tags = {}

    def run(self) -> bool:
        """Primary entrypoint"""
        print("run")
        self.known_domains = {
            "google.com": "Google",
            "reddit.com": "Reddit",
            "github.com": "Github"
        }

        self.by_bookmarks()
        return True

    def by_bookmarks(self):
        bookmarks = self.col_bookmarks.get_all()
        for bookmark in bookmarks:
            self.handle_bookmark(bookmark)

    def handle_bookmark(self, bookmark: Bookmark) -> bool:
        """Handle tags for a single Bookmark."""
        print(bookmark)
        # tags = self.col_tags.get_by_user_id(bookmark.user_id)
        the_url = tldextract.extract(bookmark.url)
        tags = []
        if the_url.domain == "reddit" and the_url.suffix == "com":
            tags += AddRedditTags().run(bookmark)
        if not tags:
            return True
        tags_to_add = []
        if bookmark.tags:
            print("bookmark has tags")
            bookmark.tags = xlate.merge_unqiue(bookmark.tags, tags_to_add)
        else:
            bookmark.tags = tags
        bookmark.save()
        print("Saved Tags for %s" % bookmark)
        return True


if __name__ == "__main__":
    AutoAddTags().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/auto_add_tags.py
