"""
    Bookmarky Api
    Util
    Auto Tag Features
    This module appliees Tag Features to a single Bookmark where applicable.

"""
import logging
from urllib.parse import urlparse

from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.models.bookmark_tag import BookmarkTag
from bookmarky.api.models.tag_feature import TagFeature
from bookmarky.api.collects.tag_features import TagFeatures


class AutoTagFeatures:

    def __init__(self):
        self.tfc = TagFeatures()
        self.bookmark = None
        self.data = {
            "bookmark_tags_added": []
        }

    def run(self, user_id: int, bookmark: Bookmark) -> bool:
        logging.info("Starting Auto Tag Features")
        self.bookmark = bookmark
        self.user_id = user_id
        features = self.tfc.get_by_user_id(user_id)
        if not features:
            logging.info("User has no Tag Features")
            return True
        for feature in features:
            self.handle_tag_feature(feature)
        logging.info("Auto Added BoomarkTags: %s" % str(self.data["bookmark_tags_added"]))
        return True

    def handle_tag_feature(self, tag_feature: TagFeature) -> bool:
        logging.info(f"Working on {tag_feature}")
        if tag_feature.name == "domain_tag":
            self.handle_domain_tag(tag_feature)
            return True
        else:
            logging.error("Unknown Tag Feature name: %s" % tag_feature)
            return False

    def handle_domain_tag(self, tag_feature: TagFeature) -> bool:
        """If the Bookmark is from the a Domain."""
        parsed_url = urlparse(self.bookmark.url)
        print(parsed_url)
        if parsed_url.netloc == tag_feature.value:
            self.add_tag(tag_feature)
            print("We got a match!")
        return True

    def add_tag(self, tag_feature: TagFeature) -> bool:
        """Add the Tag to the Bookmark and update self.data to indicate that."""
        bookmark_tag = BookmarkTag()
        bookmark_tag.bookmark_id = self.bookmark.id
        bookmark_tag.tag_id = tag_feature.tag_id
        if bookmark_tag.save():
            msg = f"Successfully tagged Bookmark: {self.bookmark} with "
            msg += f"Tag ID: {tag_feature.tag_id}"
            logging.info(msg)
            self.data["bookmark_tags_added"].append(bookmark_tag)
            return True
        else:
            logging.error("Failed to saved Bookmark Tag")
            return False

# End File: politeauthority/bookmarky/src/bookmarky/api/utils/auto_tag_features.py
