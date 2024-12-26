"""
    Bookmarky Api
    Util
    Handles Auto Features for a single Bookmark.
    We expect that the User's enabled AutoFeatures will be submitted as an argument to this class.

"""
import logging
from urllib.parse import urlparse
import re

from bookmarky.api.models.auto_feature import AutoFeature
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.models.bookmark_tag import BookmarkTag


class AutoFeatures:

    def __init__(self, user_id: int, auto_features: list):
        """Initialize the class, taking in a list of a User's AutoFeatures, and applying them where
        they should be.
        """
        self.user_id = user_id
        self.afs = auto_features
        self.bookmark = None
        self.data = {
            "tags_added": []
        }

    def run(self, bookmark: Bookmark) -> bool:
        if not self.afs:
            logging.info("No Auto Features given, exiting Handle Auto Features")
            return True
        logging.info(f"Starting Handle Auto Features for: {bookmark}")
        self.bookmark = bookmark
        return self.handle_bookmark()

    def handle_bookmark(self) -> bool:
        """Handle all Auto Feature operations for the Bookmark we're working on."""
        logging.info(f"Working Bookmark: {self.bookmark}")
        self.parsed_url = urlparse(self.bookmark.url)
        for af in self.afs:
            if af.auto_feature_type == "domain":
                self.handle_domain_feature(af)
            elif af.auto_feature_type == "url-regex":
                self.handle_url_regex_feature(af)
        logging.info(
            "For %s added tags: %s" % (
                self.bookmark,
                len(self.data["tags_added"])))
        return True

    def handle_domain_feature(self, af: AutoFeature) -> bool:
        """Handle the domain auto setting features for the Bookmark.
        @todo: This matching is a little lazy, ideally we will pull out all subdomains, and match
        against that. I think.
        """
        logging.info("Handling `domain` Auto Features")
        logging.info(af)
        if af.auto_feature_value in self.parsed_url.netloc:
            if af.entity_type == "tags":
                self.add_tag(af.entity_id)

    def handle_url_regex_feature(self, af: AutoFeature) -> bool:
        """Handle the url-regex auto setting features for the Bookmark."""
        logging.info("Handling `url-regex` Auto Features")
        logging.info(af)
        # x = re.search("/r/tifu/", txt)
        if re.search(af.auto_feature_value, self.bookmark.url):
            print("We found a match!")
            logging.info(af)
            logging.info(self.bookmark)
            if af.entity_type == "tags":
                self.add_tag(af.entity_id)
                return True
        else:
            log_msg = f"No match for regex url on {self.bookmark.url} for pattern "
            log_msg += f'"{af.auto_feature_value}")'
            logging.info(log_msg)
            return False

    def add_tag(self, tag_id: int) -> bool:
        """Add a Tag association to a Bookmark, given the Tag's ID."""
        bt = BookmarkTag()
        bt.user_id = self.bookmark.user_id
        bt.bookmark_id = self.bookmark.id
        bt.tag_id = tag_id
        if bt.save():
            logging.info(f"Successfully Tagged Bookmark with Tag ID: {tag_id}")
            self.data["tags_added"].append(tag_id)
            return True
        else:
            logging.error(
                f"Error associating Bookmark ID: {self.bookmark.id} with Tag ID: {tag_id}")
            return False

    # def handle_tag_feature(self, tag_feature: TagFeature) -> bool:
    #     logging.info(f"Working on {tag_feature}")
    #     if tag_feature.name == "domain_tag":
    #         self.handle_domain_tag(tag_feature)
    #         return True
    #     else:
    #         logging.error("Unknown Tag Feature name: %s" % tag_feature)
    #         return False

    # def handle_domain_tag(self, tag_feature: TagFeature) -> bool:
    #     """If the Bookmark is from the a Domain."""
    #     parsed_url = urlparse(self.bookmark.url)
    #     print(parsed_url)
    #     if parsed_url.netloc == tag_feature.value:
    #         self.add_tag(tag_feature)
    #         print("We got a match!")
    #     return True

    # def add_tag(self, tag_feature: TagFeature) -> bool:
    #     """Add the Tag to the Bookmark and update self.data to indicate that."""
    #     bookmark_tag = BookmarkTag()
    #     bookmark_tag.bookmark_id = self.bookmark.id
    #     bookmark_tag.tag_id = tag_feature.tag_id
    #     if bookmark_tag.save():
    #         msg = f"Successfully tagged Bookmark: {self.bookmark} with "
    #         msg += f"Tag ID: {tag_feature.tag_id}"
    #         logging.info(msg)
    #         self.data["bookmark_tags_added"].append(bookmark_tag)
    #         return True
    #     else:
    #         logging.error("Failed to saved Bookmark Tag")
    #         return False

# End File: politeauthority/bookmarky-api/src/bookmarky/api/utils/handle_auto_features.py
