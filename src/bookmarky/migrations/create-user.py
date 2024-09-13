"""
    Create User Script

"""
import logging

import arrow

from bookmarky.api.utils import db
from bookmarky.api.utils import auth

from bookmarky.migrations.data.data_users import DataUsers

ADMIN_ROLE_ID = 1


def run(user, email):
    if not db.connect():
        logging.critical("Failed database connection, exiting")
    create(user, email)


def create(user, email) -> bool:
    """Create the first admin level user, but only if one doesn't already exist."""
    logging.info("Creating First Admin User")
    client_id = auth.generate_client_id()
    api_key = auth.generate_api_key()
    expire_at = (arrow.utcnow().shift(hours=4)).datetime
    DataUsers().create_user(
        user,
        email,
        ADMIN_ROLE_ID,
        client_id,
        api_key,
        expire_at)
    return True


if __name__ == "__main__":
    run("new", "new@example.com")
