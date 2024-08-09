"""
    Bookmarky Test
    Test Tools
    Fixture: DB
    Mock a db connection.

"""
import logging

conn = True
cursor = None


class Conn:

    def commit(self):
        return True


class Cursor:

    def __init__(self, one=None, two=None):
        self.lastrowid = 1
        self.result_to_return = []
        return None

    def execute(self, sql: str, params=None) -> bool:
        logging.debug("Would have executed: %s" % sql)
        return True

    def fetchone(self):
        return self.result_to_return

    def fetchall(self):
        return self.result_to_return

    def commit(self):
        return True

# End File: politeauthority/bookmarky/tests/cver-test-tools/fixtures/db.py
