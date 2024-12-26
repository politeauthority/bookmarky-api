"""
    Bookmarky Introspect
    Introspect
    Manual Auto Features

"""
import logging.config

from bookmarky.api.utils import db
# from bookmarky.api.utils import glow
from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.collects.auto_features import AutoFeatures
from bookmarky.shared.utils.log_config import log_config
from bookmarky.api.utils.auto_features import AutoFeatures as UtilAutoFeatures


logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True

USER_ID = 1


class ManualAutoFeatures:

    def __init__(self):
        self.af_col = AutoFeatures()
        self.afs = []
        self.b_col = Bookmarks()
        self.bookmarks = []

    def run(self) -> bool:
        """Primary entrypoint."""
        logging.info("Starting Manual Auto Features for User: %s" % USER_ID)
        self.load_afs()
        self.load_bookmarks()
        for bookmark in self.bookmarks:
            UtilAutoFeatures(USER_ID, self.afs).run(bookmark)
        return True

    def load_afs(self) -> bool:
        """Load all AutoFeatures for the User."""
        self.afs = self.af_col.get_by_user_id(USER_ID)

    def load_bookmarks(self) -> bool:
        """Load all Bookmarks and AutoFeatures for a given User ID."""
        logging.info("Loaded %s AutoFeatures" % (len(self.afs)))
        # self.bookmarks = self.b_col.get_by_user_id(USER_ID)
        self.bookmarks = self.b_col.get_by_ids([606, 101])
        logging.info("Loaded %s Bookmarks" % (len(self.bookmarks)))
        return True


if __name__ == "__main__":
    if not db.connect():
        print("Failed database connection, exiting")
        exit(1)
    ManualAutoFeatures().run()


# End File: politeauthority/bookmarky-api/src/bookmarky/introspect/manual_auto_features.py
