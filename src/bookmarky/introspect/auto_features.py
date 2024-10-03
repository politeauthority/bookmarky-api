"""
    Bookmarky Introspect
    Introspect
    Auto Features
    Tool for testing Auto Features

"""
import logging.config

from bookmarky.shared.utils.log_config import log_config
from bookmarky.api.utils import db
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.utils.auto_tag_features import AutoTagFeatures

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class AutoFeatures:
    def __init__(self):
        if not db.connect():
            print("Failed database connection, exiting")
            exit(1)

    def run(self):
        user_id = 1
        bookmark = Bookmark()
        bookmark.get_by_id(321)
        print(bookmark)
        AutoTagFeatures().run(user_id, bookmark)


if __name__ == "__main__":
    if not db.connect():
        print("Failed database connection, exiting")
        exit(1)
    AutoFeatures().run()

# End File: politeauthority/bookmarky/src/bookmarky/introspect/auto_features.py
