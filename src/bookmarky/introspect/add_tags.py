"""
    Bookmarky Introspect
    Introspect
"""
from urllib.parse import urlparse

from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.collects.tags import Tags
from bookmarky.api.models.tag import Tag
from bookmarky.api.utils import db


# logging.config.dictConfig(log_config)
# logger = logging.getLogger(__name__)
# logger.propagate = True

USER_IDS = [1]


class AutoAddTags:

    def run(self):
        """Run by User ID"""
        print("run")
        self.known_domains = {
            "google.com": "Google",
            "reddit.com": "Reddit",
            "github.com": "Github"
        }
        if not db.connect():
            print("Failed database connection, exiting")
            exit(1)
        for user_id in USER_IDS:
            # @todo restrict these queries to just keys
            self.user_id = user_id
            self.tags = self.get_all_tags()
            self.tag_keys()
            self.tag_all_bookmarks()

    def tag_keys(self):
        self.tag_key_names = []
        for tag in self.tags:
            self.tag_key_names.append(tag.name)
        return True

    def get_all_tags(self) -> bool:
        tags_col = Tags()
        tags = tags_col.get_all()
        print("Loaded Tags: %s" % len(tags))
        return tags

    def tag_all_bookmarks(self) -> list:
        bookmarks_col = Bookmarks()
        bookmarks = bookmarks_col.get_all()
        print("Parsing Num Bookmarks: %s" % len(bookmarks))
        for bookmark in bookmarks:
            if bookmark.name:
                print(bookmark.name)
            print(bookmark.url)
            print("\n")
            self._parse_bookmark(bookmark)

    def _parse_bookmark(self, bookmark: Bookmark):
        print("Parsing bookmark domain")
        print(bookmark)
        domain = urlparse(bookmark.url).netloc
        print(domain)
        tags = []
        subreddit_tag = self._set_reddit_subreddit_tag(bookmark)
        if subreddit_tag:
            tags.append(subreddit_tag)
        if bookmark.tags:
            for tag in tags:
                # @todo: we shouldnt have to cast tag ids to string here
                if str(tag.id) not in bookmark.tags:
                    bookmark.tags.append(tag.id)
                    print("Added tag %s" % tag)
        else:
            tag_ids = []
            for tag in tags:
                tag_ids.append(tag.id)
            bookmark.tags = tag_ids
            print("Adding virgin tags")
        if not bookmark.save():
            print("error updating tags for bookmark %s" % bookmark)
        # if not self._set_domain_tag(bookmark):
        #     print("failed setting bookmark domain tag")

    def _set_domain_tag(self, bookmark) -> bool:
        domain_tag = self._get_domain_tag_id(bookmark)
        if not bookmark.tags:
            bookmark.tags = [domain_tag.id]
            bookmark.save()
            print("Adding Tag: %s to Bookmark %s" % (domain_tag.id, bookmark))

        elif str(domain_tag.id) not in bookmark.tags:
            bookmark.tags.append(domain_tag.id)
            bookmark.save()
            print("Adding Tag: %s to Bookmark %s" % (domain_tag.id, bookmark))

        else:
            print("Bookmark %s already has domain tag: %s" % (bookmark, domain_tag))
        return True

    def _get_domain_tag_id(self, bookmark: Bookmark) -> Tag:
        domain = urlparse(bookmark.url).netloc
        print(domain)
        domain_tag = self.get_or_make_tag(domain)
        if not domain_tag:
            print("error getting domain tag")
            return False
        return domain_tag

    def _set_reddit_subreddit_tag(self, bookmark: Bookmark) -> Tag:
        domain = urlparse(bookmark.url).netloc
        if domain != "www.reddit.com":
            return False
        if "reddit.com/r/" not in bookmark.url:
            return False
        find_section = "reddit.com/r/"
        subreddit_start = bookmark.url.find(find_section)
        subreddit_section = bookmark.url[subreddit_start + len(find_section):]
        subreddit = subreddit_section[:subreddit_section.find("/")]
        tag_name = "reddit-sub-%s" % subreddit
        tag = self.get_or_make_tag(tag_name)
        return tag

    def get_or_make_tag(self, tag_name: str) -> Tag:
        if tag_name not in self.tag_key_names:
            new_tag = Tag()
            new_tag.user_id = self.user_id
            new_tag.name = tag_name
            new_tag.slug = tag_name
            new_tag.save()
            return new_tag
        else:
            for tag in self.tags:
                if tag.name == tag_name:
                    return tag


if __name__ == "__main__":
    AutoAddTags().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/auto_add_tags.py
