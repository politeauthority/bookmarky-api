"""
    Bookmarky Migrations
    Migrate
    Entrypont for Bookmarky migrations

"""
import logging
from logging.config import dictConfig
import os

from bookmarky.migrations.data.data_options import DataOptions
from bookmarky.migrations.data.data_rbac import DataRbac
from bookmarky.migrations.data.data_users import DataUsers
from bookmarky.api.utils import db
from bookmarky.api.utils import glow
from bookmarky.api.models.migration import Migration

# from bookmarky.migrate.data.data_test_data import DataTestData
# from bookmarky.migrate.data.data_misc import DataMisc


CURRENT_MIGRATION = 4

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})


class Migrate:

    def __init__(self):
        self.role_admin_id = None

    def run(self):
        """Primary entry point for migrations."""
        # self.create_table_sql()
        logging.info("Working with database %s" % glow.db["NAME"])
    # self.create_database()
        if not db.connect():
            logging.critical("Failed database connection, exiting")
            exit(1)
        self.last_migration = self.get_migration_info()
        self.run_migrations()
        self.create_rbac()
        self.create_users()
        self.create_options()
        logging.info("Migrations were successful")

    def create_database(self) -> True:
        """Create the database for Bookmarky.
        @todo: This could be done more securily by attempting to connect to the database first.
        """
        conn, cursor = db.connect_no_db()
        sql = "CREATE DATABASE IF NOT EXISTS `%s`;" % glow.db["NAME"]
        cursor.execute(sql)
        conn.commit()
        logging.info("Created database: %s" % glow.db["NAME"])
        return True

    def get_migration_info(self) -> Migration:
        """Get the info from the last migration ran"""
        Migration().create_table()
        last = Migration()
        last.get_last_successful()
        if not last.id:
            return False
        return last

    def run_migrations(self) -> bool:
        """Determine the migrations we need to run, and execute them."""
        if self.last_migration:
            logging.info("Last migration ran: #%s" % self.last_migration.number)
        else:
            logging.info("Running first migration")
        if self.last_migration and CURRENT_MIGRATION == self.last_migration.number:
            logging.info("Migration: %s Caught Up" % CURRENT_MIGRATION)
            return True
        if self.last_migration:
            migration_no = self.last_migration.number + 1
        else:
            migration_no = 1

        # logging.warning("MIGRATIONS ARE NOT BEING RUN YET")
        while migration_no <= CURRENT_MIGRATION:
            self.run_migration(migration_no)
            migration_no += 1
        return True

    def run_migration(self, migration_no: int):
        """Running a single migration.
        @todo: This is broken right now, needs to be updated for PSQL
        """
        logging.info("Running Migration #%s" % migration_no)
        this_migration = Migration()
        this_migration.number = migration_no
        if glow.general["ENV"] == "dev":
            APPLICATION_DIR = "/work/src/bookmarky/"
            logging.warning("Using Dev Migrations location: %s" % APPLICATION_DIR)

        else:
            APPLICATION_DIR = "/app/bookmarky/"
            logging.debug("Using Migrations location: %s" % APPLICATION_DIR)

        migration_file = os.path.join(
            APPLICATION_DIR, "migrations/data/sql/up/%s.sql" % migration_no)
        with open(migration_file, 'r') as sql_file:
            sql_content = sql_file.read()
        try:
            glow.db["cursor"].execute(sql_content)
            glow.db["conn"].commit()
        except Exception as e:
            logging.critical(f"Migration {migration_no} failed: {e}")
            this_migration.success = False
            self.this_migration.save()
            exit(1)
        logging.info("Applied Migration Up: %s" % migration_no)
        this_migration.success = True
        this_migration.save()
        return True

    def create_options(self):
        """Create the Options and set their defaults."""
        logging.info("Creating Options")
        DataOptions().create()

    def create_rbac(self):
        """Create the Rbac roles/role perms and perms."""
        logging.info("Creating Roles")
        db.connect()
        self.rbac = DataRbac().create()

    def create_users(self):
        """Create the users and api keys."""
        logging.info("Creating Users and Keys")
        DataUsers().create()

    # def create_test_data(self) -> bool:
    #     """Create the test data if we're in a test environment."""
    #     if not glow.general["CVER_TEST"]:
    #         return True
    #     logging.info("Creating Test Data")
    #     DataTestData().create()
    #     return True

    # def create_misc(self):
    #     """Create misc data."""
    #     logging.info("Creating misc data")
    #     db.connect()
    #     DataMisc().create()

    # def create_table_sql(self):
    #     """Create table SQL for migrations."""
    #     print(User().create_table_sql())


if __name__ == "__main__":
    Migrate().run()


# End File: politeauthority/bookmarky/src/bookmarky/migrations/migrate.py
