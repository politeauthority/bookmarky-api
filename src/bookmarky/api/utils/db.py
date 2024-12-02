"""
    DB
    Util

"""
import logging

import psycopg2

from bookmarky.api.utils import glow


def connect() -> bool:
    """Connect to a postgres database."""
    try:
        logging.info("Connecting to postgres at %s:%s" % (glow.db["HOST"], glow.db["PORT"]))
        conn = psycopg2.connect(
            dbname=glow.db["NAME"],
            user=glow.db["USER"],
            password=glow.db["PASS"],
            host=glow.db["HOST"],
            port=glow.db["PORT"]
        )
        logging.info("Connected to PostgreSQL database!")
        conn.autocommit = True
        glow.db["conn"] = conn
        glow.db["cursor"] = conn.cursor()
        return True
    except psycopg2.Error as e:
        logging.critical("Error connecting to PostgreSQL database:", e)
        return False


def connect_no_db() -> tuple:
    """Connect to a postgres database."""
    try:
        conn = psycopg2.connect(
            dbname=glow.db["NAME"],
            user=glow.db["USER"],
            password=glow.db["PASS"],
            host=glow.db["HOST"],
            port=glow.db["PORT"]
        )
        logging.debug("Connected to PostgreSQL database!")
        logging.info("Connected to PostgreSQL database!")
        conn.autocommit = True
        glow.db["conn"] = conn
        glow.db["cursor"] = conn.cursor()
        return conn, conn.cursor()
    except psycopg2.Error as e:
        logging.critical("Error connecting to PostgreSQL database:", e)
        return False


def close() -> bool:
    """Close the database connection.
    """
    glow.db["cursor"].close()
    glow.db["conn"].close()
    return True

# End File: politeauthority/bookmarky-api/src/bookmarky/api/utils/db.py
