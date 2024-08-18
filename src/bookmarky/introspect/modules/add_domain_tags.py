"""
    Bookmarky Introspect
    Introspect
    Add Domain Tags

"""
import logging

from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.models.tag import Tag
from bookmarky.shared.utils import xlate


class AddDomainTags:

    def __init__(self):
        self.tags = []

    def run(self, bookmark: Bookmark) -> list:
        """Checks a Reddit url for subreddits, and returns appropriate tag_ids for that sub
        Reddit.
        """
        self.bookmark = bookmark
        subreddit = self.get_sub_reddit(self.bookmark.url)
        if not subreddit:
            return []
        self.tags.append(self.get_subreddit_tag(subreddit))
        return self.tags

    def get_sub_reddit(self, url: str) -> str:
        """Find if the reddit url is a Sub Reddit, if it is return the name of the Sub Reddit.
        @todo: This is probably more appropriate for a regex but I'm being lazy right now.
        """
        if "reddit.com/r/" not in url:
            return False
        part = url[url.find("reddit.com/r/") + 13:]
        subreddit = part[:part.find("/")]
        return subreddit

    def get_subreddit_tag(self, subreddit: str) -> int:
        """Create the Sub Reddit Tag if doesn't already exist, returning the Tag.id
        """
        tag = Tag()
        tag.user_id = self.bookmark.user_id
        tag.slug = "r-%s" % xlate.slugify(subreddit)
        tag.name = "r/%s" % subreddit
        if not tag.get_by_ux_key():
            logging.debug(f"Creating Tag {tag.name}")
            tag.save()
            return tag.id
        else:
            logging.debug(f"Found Tag {tag.name}")
            return tag.id

# End File: politeauthority/bookmarky-api/src/bookmarky/introspect/modules/add_domain_tags.py
