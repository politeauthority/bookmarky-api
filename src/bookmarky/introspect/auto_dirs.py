"""
    Bookmarky Introspect
    Introspect
    Add Directories

"""
import tldextract

from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.collects.tags import Tags
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.models.bookmark_tag import BookmarkTag
from bookmarky.api.utils import db
from bookmarky.introspect.modules.add_reddit_tags import AddRedditTags

KNOWN_DOMAINS = {
    "reddit.com": "Reddit",
    "github.com": "Development"
}


class AutoDirs:

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
        tag_ids = []
        if the_url.domain == "reddit" and the_url.suffix == "com":
            tag_ids += AddRedditTags().run(bookmark)
        if not tag_ids:
            return True
        for tag_id in tag_ids:
            bt = BookmarkTag()
            bt.bookmark_id = bookmark.id
            bt.tag_id = tag_id
            bt.save()
        print("Saved Tags for %s" % bookmark)
        return True


if __name__ == "__main__":
    AutoDirs().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/auto_dirs.py
