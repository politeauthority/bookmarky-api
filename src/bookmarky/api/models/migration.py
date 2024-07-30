"""
    Bookmarky Api
    Model - Migration

"""
from bookmarky.api.models.base_entity_meta import BaseEntityMeta
from bookmarky.shared.models.migration import FIELD_MAP


class Migration(BaseEntityMeta):

    model_name = "migration"

    def __init__(self, conn=None, cursor=None):
        super(Migration, self).__init__(conn, cursor)
        self.table_name = "migrations"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.setup()

    def get_last_successful(self) -> bool:
        """Get the last successful Migration."""
        sql = """
            SELECT *
            FROM %s
            WHERE success is True
            ORDER BY number DESC
            LIMIT 1""" % (self.table_name)
        print(sql)
        self.cursor.execute(sql)
        run_raw = self.cursor.fetchone()
        if not run_raw:
            return False
        self.build_from_list(run_raw)
        return True

# End File: politeauthority/bookmarky/src/bookmarky/api/models/migration.py
